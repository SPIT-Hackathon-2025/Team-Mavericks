from fastapi import FastAPI
from cal.calendar_service import router as calendar_router
import asyncio
from notion.notion import triggerCronJob
from email_parser.main import process_emails

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Application is starting...")
    asyncio.create_task(asyncio.to_thread(triggerCronJob))
    asyncio.create_task(asyncio.to_thread(process_emails))


@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")

# Include Google Calendar routes
app.include_router(calendar_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
