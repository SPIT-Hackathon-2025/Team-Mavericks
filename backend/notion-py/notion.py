import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def create_task(task_name, status, priority, due_date, assignee_emails):
    try:
        users_response = notion.users.list()
        users = users_response.get("results", [])

        print("users", users)
        assignees = [
            {"id": user["id"]} for user in users
            if "person" in user and user["person"].get("email") in assignee_emails
        ]
        print("assignees", assignees)

        response = notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Task": {
                    "title": [{"text": {"content": task_name}}]
                },
                "Status": {
                    "status": {"name": status}
                },
                "Priority": {
                    "select": {"name": priority}
                },
                "Due Date": {
                    "date": {"start": due_date}
                },
                "Assignee": {
                    "people": assignees
                }
            }
        )

        print("✅ Task Created:", response)
    except Exception as error:
        print("❌ Error creating task:", getattr(error, "response", {}).get("data", str(error)))

create_task("Fix API Bug 2", "Done", "Low", "2025-02-08", ["nilimajnc@gmail.com"])
