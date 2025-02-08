import datetime
import os
from typing import Dict

from fastapi import FastAPI, HTTPException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = FastAPI()
CALENDAR_IDS = [
    "primary",
    "fd2f0fc815e69e6b522346e34a915d7fff9725c98e4a208907ba0f7bb91f689d@group.calendar.google.com",
    "673b8ce55490ab0eca5dd0d63fff3d48168c188802b63585e8c4e9b1912d6c40@group.calendar.google.com"
]
def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

@app.get("/events")
def get_events():
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])
        return {"events": events}
    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"An error occurred: {error}")

@app.post("/events")
def create_event(event: dict):
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        # Extract event details
        event_start = event["start"]["dateTime"]
        event_end = event["end"]["dateTime"]
        attendees = event.get("attendees", [])  # List of email IDs

        # Convert to datetime objects for comparison
        event_start_dt = datetime.datetime.fromisoformat(event_start.replace("Z", "+00:00"))
        event_end_dt = datetime.datetime.fromisoformat(event_end.replace("Z", "+00:00"))

        # Check for overlapping events in other calendars
        for calendar_id in CALENDAR_IDS:
            if calendar_id == "primary":
                continue  # Skip checking primary since we're adding there

            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=event_start,
                timeMax=event_end,
                singleEvents=True,
                orderBy="startTime"
            ).execute()

            existing_events = events_result.get("items", [])

            # If any events exist in the given time range, return an error
            if existing_events:
                raise HTTPException(
                    status_code=400,
                    detail=f"Event conflicts with existing events in calendar {calendar_id}. Cannot create event."
                )

        # Prepare the event object
        event_body = {
            "summary": event["summary"],
            "start": {"dateTime": event_start, "timeZone": "UTC"},
            "end": {"dateTime": event_end, "timeZone": "UTC"},
            "conferenceData": {
                "createRequest": {
                    "requestId": "unique-request-id",  # Change this to a unique ID
                    "conferenceSolutionKey": {"type": "hangoutsMeet"}
                }
            },
            "attendees": [{"email": email} for email in attendees],  # Add attendees
        }

        # Insert event into primary calendar with a Google Meet link
        event_result = service.events().insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1  # Required for Meet link generation
        ).execute()

        return {
            "event": event_result,
            "meet_link": event_result.get("conferenceData", {}).get("entryPoints", [{}])[0].get("uri", "No link generated")
        }

    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"An error occurred: {error}")

@app.get("/events/{date}")
def get_events_for_day(date: str):
    try:
        day_start = datetime.datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z"
        day_end = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)).isoformat() + "Z"

        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        all_events = {}

        for calendar_id in CALENDAR_IDS:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=day_start,
                timeMax=day_end,
                singleEvents=True,
                orderBy="startTime"
            ).execute()

            events = events_result.get("items", [])
            all_events[calendar_id] = events

        return {"date": date, "events": all_events}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"Google Calendar API error: {error}")
