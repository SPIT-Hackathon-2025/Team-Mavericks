import json
import time
from email_parser.gem_utils import generate_response_llm

def generate_responses(temp_output_file, final_output_file):
    """Reads emails, generates LLM-based responses, and saves the final output."""
    start_time = time.time()  # Start timing

    with open(temp_output_file, "r", encoding="utf-8") as f:
        emails = json.load(f)

    for email in emails:
        full_email_text = f"""
        From: {email.get("from", "Unknown")}
        To: {email.get("to", "Unknown")}
        CC: {email.get("cc", "Unknown")}
        BCC: {email.get("bcc", "Unknown")}
        Subject: {email.get("subject", "No Subject")}
        Date: {email.get("date", "Unknown Date")}

        {email.get("body", "No Content")}
        """
        email["response"] = generate_response_llm(full_email_text, email["category"])
        print(f"Generated response for email from '{email['from']}'")

    with open(final_output_file, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=4)

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Final emails with responses saved to {final_output_file} in {elapsed_time:.2f} seconds")

    return elapsed_time
