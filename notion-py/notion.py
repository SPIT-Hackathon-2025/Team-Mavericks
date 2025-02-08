import os
import time
import smtplib
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")  
SMTP_PORT = int(os.getenv("SMTP_PORT", 587)) 
EMAIL_SENDER = os.getenv("EMAIL_SENDER") 
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  


def send_email(to_email, task_name, due_date):
    """Send email notification for due tasks."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = f"🔔 Task Reminder: {task_name} is due today!"

        body = f"Hello,\n\nYour task '{task_name}' is due on {due_date}. Please take necessary action.\n\nBest,\nTask Reminder Bot"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() 
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())

        print(f"📩 Email sent to {to_email} for task: {task_name}")
        return True
    except Exception as error:
        print(f"❌ Failed to send email to {to_email}: {error}")
        return False


def check_due_tasks():
    """Check Notion for due tasks and send reminders."""
    try:
        print("🔎 Checking for tasks due today...")

        IST = timezone(timedelta(hours=5, minutes=30))
        today = datetime.now(IST).date()

        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID,
                "filter": {
                    "and": [
                        {"property": "Due Date", "date": {"equals": today.isoformat()}},
                        {"property": "Reminder Sent", "select": {"is_empty": True}},  # Only tasks without sent status
                    ]
                },
            }
        )

        tasks = response.get("results", [])
        if not tasks:
            print("✅ No pending reminders to send.")
            return

        print(f"🔔 {len(tasks)} Tasks Due Today:")
        for task in tasks:
            task_id = task["id"]
            task_name = task["properties"]["Task"]["title"][0]["text"]["content"]
            due_date = task["properties"]["Due Date"]["date"]["start"]
            assignees = task["properties"].get("Assignee", {}).get("people", [])

            emails = [notion.users.retrieve(user["id"])["person"]["email"] for user in assignees]

            for email in emails:
                if send_email(email, task_name, due_date):
                    notion.pages.update(
                        task_id,
                        properties={"Reminder Sent": {"select": {"name": "Sent"}}}
                    )
                    print(f"✅ Updated Notion: Reminder Sent for '{task_name}'")

    except Exception as error:
        print("❌ Error checking due tasks:", str(error))

#2 minutes
schedule.every(2).minutes.do(check_due_tasks)

# Run Scheduler
while True:
    schedule.run_pending()
    time.sleep(30)
