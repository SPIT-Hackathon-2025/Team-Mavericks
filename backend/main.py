from cal.calendar_service import router as calendar_router
import asyncio
from notion.notion import triggerCronJob
from email_parser.main import process_emails
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware




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




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
