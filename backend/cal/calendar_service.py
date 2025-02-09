import datetime
import os
from fastapi import APIRouter, HTTPException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz


SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_IDS = [
    "primary",
    "fd2f0fc815e69e6b522346e34a915d7fff9725c98e4a208907ba0f7bb91f689d@group.calendar.google.com",
    "673b8ce55490ab0eca5dd0d63fff3d48168c188802b63585e8c4e9b1912d6c40@group.calendar.google.com"
]

router = APIRouter()

def get_credentials():
    creds = None
    if os.path.exists("cal/token.json"):
        creds = Credentials.from_authorized_user_file("cal/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("cal/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("cal/token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def initialize_calendar_service():
    """Helper function to authenticate and return the Google Calendar service."""
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)

def extract_event_details(event: dict):
    """Helper function to extract event details."""
    event_start = event["start"]["dateTime"]
    event_end = event["end"]["dateTime"]
    attendees = event.get("attendees", [])

    event_start_dt = datetime.datetime.fromisoformat(event_start.replace("Z", "+00:00"))
    event_end_dt = datetime.datetime.fromisoformat(event_end.replace("Z", "+00:00"))

    return event_start, event_end, attendees, event_start_dt, event_end_dt

@router.get("/events")
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

# @router.post("/events")
def create_event(event):
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        # event_start = event["start"]["dateTime"]
        event_start = event["event_time"]
        event_end = (datetime.datetime.fromisoformat(event["event_time"]) + datetime.timedelta(hours=1)).isoformat()
        # event_end = event["end"]["dateTime"]
        attendees = event.get("attendees", [])
        description = event.get("description", "")  # Get the description from the event

        # Convert event start and end times to IST
        ist = pytz.timezone('Asia/Kolkata')
        event_start_dt = datetime.datetime.fromisoformat(event_start.replace("Z","+00:00"))
        event_end_dt = datetime.datetime.fromisoformat(event_end.replace("Z","+00:00"))
        # print("event_start",event_start)
        # print("event_end",event_end)
        # event_date = event_start_dt.date()

        # Check if the datetime is naive and localize it
        if event_start_dt.tzinfo is None:
            event_start_dt = ist.localize(event_start_dt)
        else:
            event_start_dt = event_start_dt.astimezone(ist)

        if event_end_dt.tzinfo is None:
            event_end_dt = ist.localize(event_end_dt)
        else:
            event_end_dt = event_end_dt.astimezone(ist)

        print("event_start_dt",event_start_dt)
        # print("event_end_dt",event_end_dt)
        event_date = event_start_dt.date()

        # Define office hours in IST
        office_start = ist.localize(datetime.datetime.combine(event_date, datetime.time(9, 0)))
        office_end = ist.localize(datetime.datetime.combine(event_date, datetime.time(17, 0)))
        # print("office_start",office_start)
        # print("office_end",office_end)
        # Fetch all events for the day across calendars
        busy_slots = []
        for calendar_id in CALENDAR_IDS:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=office_start.isoformat(),  # These are now aware
                timeMax=office_end.isoformat(),     # These are now aware
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            for ev in events_result.get("items", []):
                ev_start = datetime.datetime.fromisoformat(ev["start"]["dateTime"].replace("Z", "+00:00"))
                ev_end = datetime.datetime.fromisoformat(ev["end"]["dateTime"].replace("Z", "+00:00"))

                # Check if the event start and end times are naive and localize them
                if ev_start.tzinfo is None:
                    ev_start = ist.localize(ev_start)
                else:
                    ev_start = ev_start.astimezone(ist)

                if ev_end.tzinfo is None:
                    ev_end = ist.localize(ev_end)
                else:
                    ev_end = ev_end.astimezone(ist)

                busy_slots.append((ev_start, ev_end))

        # Sort busy slots by start time
        busy_slots.sort()

        if not busy_slots:
            new_start=event_start_dt
            new_end=event_end_dt
        else:   
            # Find a free time slot
            new_start = office_start
            new_end = new_start + (event_end_dt - event_start_dt)

            for busy_start, busy_end in busy_slots:
                if new_end <= busy_start:  # If the new event fits before the busy slot
                    break
                new_start = busy_end  # Move to the next free slot
                new_end = new_start + (event_end_dt - event_start_dt)  # Adjust end time correctly
                if new_end > office_end:
                    raise HTTPException(
                        status_code=400,
                        detail="No available time slots within office hours."
                    )
    
        # Prepare the event object
        event_body = {
            "summary": event.get("event_name", "") ,
            "description": description,  # Add the description here
            "start": {"dateTime": new_start.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": new_end.isoformat(), "timeZone": "Asia/Kolkata"},
            "conferenceData": {
                "createRequest": {
                    "requestId": "unique-request-id",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"}
                }
            },
            "attendees": [{"email": email} for email in attendees],
        }
        # print("event_body",event_body)

        # Insert event into primary calendar
        event_result = service.events().insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1
        ).execute()

        return {
            "event": event_result,
            "meet_link": event_result.get("conferenceData", {}).get("entryPoints", [{}])[0].get("uri", "No link generated")
        }

    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"An error occurred: {error}")

@router.get("/events/{date}")
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
