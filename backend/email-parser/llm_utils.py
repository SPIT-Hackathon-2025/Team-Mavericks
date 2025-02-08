import json
import ollama

def extract_meeting_details(email_body):
    """Extracts meeting details if the email is a Meeting Request."""
    prompt = f"""
    The following email contains a meeting request. Extract the key details:
    - Event Name
    - Event Description
    - Event Time (if mentioned, otherwise return '')
    - Guests in the event

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "event_name", "event_description", "event_time", "guests".
    """
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return json.loads(response["message"]["content"])

def extract_task_details(email_body):
    """Extracts task details if the email is a Task Assignment."""
    prompt = f"""
    The following email contains a task assignment. Extract the key details:
    - Task Name
    - Task Description
    - Due Date (if mentioned, otherwise return '')

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "task_name", "task_description", "due_date".
    """
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return json.loads(response["message"]["content"])


def extract_followUp_details(email_body):
    """Extracts task details if the email is followup."""
    prompt = f"""
    The following email is a follow-up to a meeting. Extract the key details:

    -Meeting Topic  
    -Meeting Date
    -meeting Time(if mentioned, otherwise return "")  
    -Action Items (list of tasks with assignees and deadlines if available)
    -Next Steps (if mentioned, otherwise return "")  
    -Small Description: A short summary (2-3 lines) capturing the purpose and key points of the email.
    -Priority Level: Classify as "High", "Medium", or "Low" based on urgency (e.g., deadlines, explicit follow-ups, or pending actions).

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "meeting_topic", "meeting_date","meeting_time", "action_items", "response_request", "next_steps", "desciption", "priority".
    """
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return json.loads(response["message"]["content"])


def extract_transcript(email_body):
    """Generates a response email using an LLM."""
    prompt = f"""
    The following email is a transcript of a meeting. Extract the key details:

    -Meeting Topic  
    -Meeting Date
    -meeting Time(if mentioned, otherwise return "")  
    -Action Items (list of tasks with assignees and deadlines if available)
    -Next Steps (if mentioned, otherwise return "")  
    -Small Description: A short summary (2-3 lines) capturing the purpose and key points of the email.
    -Priority Level: Classify as "High", "Medium", or "Low" based on urgency (e.g., deadlines, explicit follow-ups, or pending actions).

    Email Content:
    {email_body}

    Return the response as a JSON object with fields: "meeting_topic", "meeting_date","meeting_time", "action_items", "response_request", "next_steps", "desciption", "priority".
    """
    # Call LLM to generate a response (Replace with actual LLM call)
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return json.loads(response["message"]["content"])

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
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return json.loads(response["message"]["content"])

