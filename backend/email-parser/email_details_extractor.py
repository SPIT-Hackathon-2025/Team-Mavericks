import json
import time
from llm_utils import extract_meeting_details, extract_task_details, extract_followUp_details, extract_transcript

def extract_email_details(input_file, temp_output_file):
    """Extracts details from emails and saves intermediate results."""
    start_time = time.time()  # Start timing

    with open(input_file, "r", encoding="utf-8") as f:
        emails = json.load(f)

    for email in emails:
        category = email["category"]
        if category == "Meeting Request":
            email.update(extract_meeting_details(email["body"]))
        elif category == "Task Assignment":
            email.update(extract_task_details(email["body"]))
        elif category == "Follow-up":
            email.update(extract_followUp_details(email["body"]))
        elif category == "Transcript mail":
            email.update(extract_transcript(email["body"]))

    with open(temp_output_file, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=4)

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Details extracted and saved to {temp_output_file} in {elapsed_time:.2f} seconds")

    return temp_output_file, elapsed_time  # Return file name and execution time
