import time
import json
import os
from email_parser.mails import fetch_unread_emails  # Import fetch_unread_emails from mails.py
from email_parser.gem_mail_analyzer import analyze_emails_with_ollama  # Import analyze_emails_with_ollama from mail_analyzer.py
from email_parser.email_details_extractor import extract_email_details  # Import extract_email_details
from email_parser.response_generator import generate_responses  # Import generate_responses

async def process_emails(websocket):
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
            await websocket.send_text(f"new_email {new_emails}")
            print("\n📨 New emails received. Categorizing them...\n")

            # Save emails to a JSON file (overwrite the existing file)
            with open(email_file, "w", encoding="utf-8") as f:
                json.dump(new_emails, f, indent=4, ensure_ascii=False)
            print(f"📂 Saved {len(new_emails)} emails to {email_file}.")

            # Analyze the emails with Ollama and save the results to the same filename (overwrite existing file)
            output_file = email_file  # Use the same filename for the output
            print(output_file)
            category=await analyze_emails_with_ollama(email_file, output_file,websocket)  # Analyze and categorize emails
            await websocket.send_text(f"categorized_mail {category}")

            print(f"✅ Categorized emails saved to {output_file}.")

            # Extract details and generate responses for the categorized emails
            extracted_file, _ = await extract_email_details(output_file, output_file,websocket)

            # Generate responses and overwrite the same file
            generate_responses(extracted_file, output_file)

            print(f"✅ Responses generated and saved to {output_file}.")

            with open(extracted_file, "r", encoding="utf-8") as f:
                categorized_emails = json.load(f)
            
            for email in categorized_emails:
                category = email.get('category', 'Uncategorized')  # Default to 'Uncategorized' if no category
                category_file = os.path.join(emails_folder, f"{category}.json")

                # Append emails to the category-specific JSON file
                if os.path.exists(category_file):
                    with open(category_file, "r+", encoding="utf-8") as cat_f:
                        existing_data = json.load(cat_f)
                        existing_data.append(email)
                        cat_f.seek(0)  # Move to the beginning of the file
                        json.dump(existing_data, cat_f, indent=4, ensure_ascii=False)
                else:
                    with open(category_file, "w", encoding="utf-8") as cat_f:
                        json.dump([email], cat_f, indent=4, ensure_ascii=False)

                print(f"📂 Added email to category {category} file: {category_file}")

            # Delete the original email file after processing
            os.remove(email_file)
            print(f"🗑️ Deleted the original email file: {email_file}")
        else:

            print("❌ No new emails found.")

        # Sleep for a specified interval before checking for new emails again
        print("🔄 Waiting for 5 seconds before checking for new emails...\n")
        time.sleep(5)  # Wait for 5 seconds before fetching emails again

# if __name__ == "__main__":
#     process_emails()
