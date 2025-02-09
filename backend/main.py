from cal.calendar_service import router as calendar_router
import asyncio
from notion.notion import triggerCronJob,get_due_tasks
from email_parser.main import process_emails
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders





app = FastAPI()
# Allow CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("Application is starting...")
    asyncio.create_task(asyncio.to_thread(triggerCronJob))
    # asyncio.create_task(asyncio.to_thread(process_emails))


@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")

# Include Google Calendar routes
app.include_router(calendar_router)
connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection handler"""
    await websocket.accept()
    print("WebSocket connection established!")

    connected_clients.add(websocket)
    
    # Run process_emails on first connection
    await process_emails(websocket)

    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@app.get("/mom")
async def mom():
    file_path = Path("email_parser/emails/Transcript mail.json")

    if not file_path.exists():
        return {"error": "File not found"}

    try:
        # Read JSON file asynchronously using asyncio.to_thread
        data = await asyncio.to_thread(lambda: json.load(open(file_path, "r", encoding="utf-8")))

        if isinstance(data, list):  # Ensure data is a list before reversing
            data.reverse()

        return data
    except Exception as e:
        return {"error": str(e)}

from email.message import EmailMessage


@app.get("/mail-mom/{title}")
async def mail_mom(title: str):
    file_path = Path("email_parser/emails/Transcript mail.json")

    if not file_path.exists():
        return {"error": "File not found"}

    try:
        # Read JSON file asynchronously
        data = await asyncio.to_thread(lambda: json.load(open(file_path, "r", encoding="utf-8")))

        # Find the email by title
        email_data = next((item for item in data if item.get("title") == title), None)
        if not email_data:
            return {"error": "Transcript not found"}

        # Format transcript text
        transcript_text = json.dumps(email_data, indent=4)

        # Save as text file
        transcript_path = Path(f"{title}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        # Email setup
        sender_email = "practicals321@gmail.com"
        receiver_email = "nilimajnc@gmail.com"
        subject = f"Meeting Transcript: {title}"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_password = "rkkv zkwm dwhf jqvb"

        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(f"Attached is the meeting transcript for '{title}'.")

        # Attach transcript file
        with open(transcript_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="plain", filename=transcript_path.name)

        # Send email
        async def send_email():
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, smtp_password)
                server.send_message(msg)

        await send_email()

        return {"success": f"Transcript '{title}' emailed successfully"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/today")
async def today():
    # Get today's date
    tasks= get_due_tasks()
    return {"tasks": tasks}
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
