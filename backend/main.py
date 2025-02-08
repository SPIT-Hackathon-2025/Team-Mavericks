from fastapi import FastAPI
from cal.calendar_service import router as calendar_router

app = FastAPI()




# Include Google Calendar routes
app.include_router(calendar_router, prefix="/calendar", tags=["Google Calendar"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
