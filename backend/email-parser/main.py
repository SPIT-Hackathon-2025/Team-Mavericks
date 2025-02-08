import time
import json
from mails import fetch_unread_emails  # Import fetch_unread_emails from mails.py
from mail_analyzer import analyze_emails_with_ollama  # Import analyze_emails_with_ollama from mail_analyzer.py
from email_details_extractor import extract_email_details  # Import extract_email_details
from response_generator import generate_responses  # Import generate_responses

def process_emails():
    print("🔄 Starting the email fetching and analysis process...")

    # Specify folder paths for attachments and emails
    attachments_folder = "attachments"
    emails_folder = "emails"

    while True:  # Infinite loop to keep running until you stop manually
        # Fetch unread emails
        result = fetch_unread_emails(attachments_folder, emails_folder)
        
        if result is None:
            print("❌ No new emails found.")
            continue  # Skip this iteration and check for emails again

        new_emails, email_file = result  # Unpack only if result is not None
        print(f"Fetched emails: {new_emails}")

        if new_emails:
            print("\n📨 New emails received. Categorizing them...\n")

            # Save emails to a JSON file (overwrite the existing file)
            with open(email_file, "w", encoding="utf-8") as f:
                json.dump(new_emails, f, indent=4, ensure_ascii=False)
            print(f"📂 Saved {len(new_emails)} emails to {email_file}.")

            # Analyze the emails with Ollama and save the results to the same filename (overwrite existing file)
            output_file = email_file  # Use the same filename for the output
            print(output_file)
            analyze_emails_with_ollama(email_file, output_file)  # Analyze and categorize emails

            print(f"✅ Categorized emails saved to {output_file}.")

            # Extract details and generate responses for the categorized emails
            extracted_file, _ = extract_email_details(output_file, output_file)

            # Generate responses and overwrite the same file
            generate_responses(extracted_file, output_file)

            print(f"✅ Responses generated and saved to {output_file}.")
        else:
            print("❌ No new emails found.")

        # Sleep for a specified interval before checking for new emails again
        print("🔄 Waiting for 5 seconds before checking for new emails...\n")
        time.sleep(5)  # Wait for 5 seconds before fetching emails again

if __name__ == "__main__":
    process_emails()
