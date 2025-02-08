### get
all

http://127.0.0.1:8000/events

### get 
on date

http://127.0.0.1:8000/events/2025-02-08

### post

body

http://127.0.0.1:8000/events/

```
{
    "summary": "Meeting with Team",
    "location": "Conference Room C",
    "description": "Discuss project updates and next steps.",
    "start": {
        "dateTime": "2025-02-08T22:00:00+05:30",  
        "timeZone": "Asia/Kolkata"
    },
    "end": {
        "dateTime": "2025-02-08T23:00:00+05:30",  
        "timeZone": "Asia/Kolkata"
    },
    "attendees": ["tejashree.bhangale@gmail.com", "diassavio629@gmail.com"]
}
```