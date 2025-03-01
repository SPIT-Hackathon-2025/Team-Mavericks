import json
import google.generativeai as genai
from dotenv import load_dotenv
import os
from notion.notion import create_task
from cal.calendar_service import create_event


load_dotenv()

# Configure the Gemini API with your API key
api_key = os.getenv("GEMINI2")
if not api_key:
    print("Error: Gemini key not found")
    exit()

genai.configure(api_key=api_key)

async def extract_meeting_details(email_body,websocket):
    """Extracts meeting details if the email is a Meeting Request."""
    prompt = f"""
    The following email contains a meeting request. Extract the key details:
    - Event Name
    - Event Description
    - Event Time (if mentioned give in iso format, otherwise return '')
    - Guests in the event

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "event_name", "event_description", "event_time", "guests".
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response =model.generate_content(prompt)
    
    # Extract the text from the response
    content =response._result.candidates[0].content.parts[0].text
    
    # Remove the "```json" markdown block
    content = content.strip("```json\n").strip("```")
    print("content",content)
    await websocket.send_text(f"mail_details: {json.loads(content)}")

    create_event(json.loads(content))
    await websocket.send_text(f"action_performed")
    return json.loads(content)

async def extract_task_details(email_body,websocket):
    """Extracts task details if the email is a Task Assignment."""
    prompt = f"""
    The following email contains a task assignment. Extract the key details:
    - Task Name
    - Task Description
    - Due Date (if mentioned in yyyy-mm-dd format, otherwise return '')

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "task_name", "task_description", "due_date".
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response =model.generate_content(prompt)
    content = response._result.candidates[0].content.parts[0].text
    
    # Remove the "```json" markdown block
    content = content.strip("```json\n").strip("```")
    jsonFormat=json.loads(content)
# create_task("Fix API Bug 2", "Done", "Low", "2025-02-08", ["nilimajnc@gmail.com"])
    priority = jsonFormat.get('priority', 'Medium')  # Default to "Medium" if key is missing or None
    
    if priority:  
        print(f"Priority is set to {priority}")
    else:
        print("Priority is empty or undefined")

    await websocket.send_text(f"mail_details: {jsonFormat}")

    create_task(jsonFormat["task_name"],jsonFormat["task_description"],"Todo",priority,jsonFormat['due_date'],[]);
    await websocket.send_text(f"action_performed")




    return json.loads(content)


async def extract_followUp_details(email_body,websocket):
    """Extracts task details if the email is followup."""
    prompt = f"""
    The following email is a follow-up to a meeting. Extract the key details:

    -Meeting Topic  
    -Meeting Date in yyyy-mm-dd format
    -meeting Time(if mentioned, otherwise return "")  
    -Action Items (list of tasks with assignees and deadlines if available)
    -Next Steps (if mentioned, otherwise return "")  
    -Small Description: A short summary (2-3 lines) capturing the purpose and key points of the email.
    -Priority Level: Classify as "High", "Medium", or "Low" based on urgency (e.g., deadlines, explicit follow-ups, or pending actions).

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "meeting_topic", "meeting_date","meeting_time", "action_items", "response_request", "next_steps", "desciption", "priority".
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response =model.generate_content(prompt)
    content = response._result.candidates[0].content.parts[0].text
    
    # Remove the "```json" markdown block
    content = content.strip("```json\n").strip("```")
    await websocket.send_text(f"mail_details {content}")
    await websocket.send_text(f"action performed")

    return json.loads(content)


async def extract_transcript(email_body,websocket):
    """Generates a response email using an LLM."""
    prompt = f"""
    The following email is a transcript of a meeting. Extract the following details for the Minutes of Meeting (MoM):

    - **Meeting Information:**  
        - **Title:** [Extract the meeting title/topic]
        - **Date:** [Extract the meeting date in yyyy-mm-dd format]
        - **Time:** [Extract the meeting time, or return an empty string if not mentioned]
        - **Attendees:** [List of attendees, if available, or return an empty string, can take from cc bcc also]
    
    - **Agenda:**  
        [List the agenda points discussed during the meeting]
        
    - **Minutes:**  
        [Summarize the discussions for each agenda point and list the action items with deadlines and assigned individuals]
        
    - **Decisions Made:**  
        [List any decisions made during the meeting]

    - **Next Meeting:**  
        - **Date:** [Extract date for the next meeting in yyyy-mm-dd format]
        - **Time:** [Extract time for the next meeting in iso format]
        - **Location:** [Extract location for the next meeting, or return an empty string if not mentioned]
        
    - **Adjournment:**  
        - **Time of Adjournment:** [Time the meeting was adjourned]
        
    - **Additional Notes:**  
        [Include any extra remarks or observations from the meeting]

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "title", "date","time", "attendees", "agenda", "minutes", "descision made", "next meeting", "adjournment", "additional notes".
    """
    # Call LLM to generate a response (Replace with actual LLM call)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response =model.generate_content(prompt)
    content = response._result.candidates[0].content.parts[0].text
    
    # Remove the "```json" markdown block
    content = content.strip("```json\n").strip("```")
    await websocket.send_text(f"mail_details {content}")
    
    return json.loads(content)

def generate_response_llm(email_text, category):
    """Generates a response email using an LLM."""
    prompt = f"""
    You are an email assistant. Based on the following email and its category, generate a polite and professional response.

    Category: {category}
    Email:
    {email_text}

    Return the response as a JSON object with field: "response".
    """
    # Call LLM to generate a response (Replace with actual LLM call)
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    content = response._result.candidates[0].content.parts[0].text
    
    # Remove the "```json" markdown block
    content = content.strip("```json\n").strip("```")
    return json.loads(content)
    # return json.loads(response.text)

