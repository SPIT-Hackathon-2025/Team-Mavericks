import imaplib
import email
import json
import re
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup  # For removing HTML tags

# Gmail IMAP server details
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "practicals321@gmail.com"
EMAIL_PASSWORD = "rkkv zkwm dwhf jqvb"  # Use an app password

def decode_email_header(value):
    """Decode email headers to readable format"""
    decoded_parts = email.header.decode_header(value)
    decoded_str = ""
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            if enc:
                decoded_str += part.decode(enc, errors='ignore')  # Decode with encoding
            else:
                decoded_str += part.decode(errors='ignore')  # Default to 'ignore' if no encoding
        else:
            decoded_str += part  # Add non-bytes part directly
    return decoded_str if decoded_str else "No Subject"

def clean_email_body(body):
    """Clean email body by removing HTML tags, excessive spaces, and special characters"""
    if not body:
        return "No Content"

    body = BeautifulSoup(body, "html.parser").get_text(separator=" ")  # Remove HTML tags
    body = re.sub(r"\s+", " ", body).strip()  # Remove extra spaces and newlines

    return body

def fetch_unread_emails(attachments_folder, emails_folder):
    try:
        # Create folder for attachments and emails if not already present
        os.makedirs(attachments_folder, exist_ok=True)
        os.makedirs(emails_folder, exist_ok=True)

        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")  # Select Inbox

        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK" or not messages[0]:
            return None  # No new emails

        email_ids = messages[0].split()
        print(f"📩 Found {len(email_ids)} new unread emails!")

        email_data = []

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Extract metadata
                    subject = decode_email_header(msg["Subject"])
                    sender = msg.get("From")
                    recipient = msg.get("To")
                    cc = msg.get("Cc", "")  # Extract CC field
                    bcc = msg.get("Bcc", "")
                    date_raw = msg.get("Date")

                    # Convert Date to Standard Format
                    try:
                        date_parsed = email.utils.parsedate_to_datetime(date_raw)
                        date_str = date_parsed.strftime("%Y-%m-%d %H:%M:%S")
                        filename_timestamp = date_parsed.strftime("%Y%m%d_%H%M%S")
                    except:
                        date_str = "Unknown Date"
                        filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    # Extract email body and attachments
                    email_body = ""
                    attachments = []

                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        filename = part.get_filename()
                        if filename:
                            filename = decode_email_header(filename)
                            filepath = os.path.join(attachments_folder, filename)

                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            attachments.append(filename)
                        
                        elif content_type == "text/plain":
                            payload = part.get_payload(decode=True)
                            if payload:
                                email_body = payload.decode(errors="ignore").strip()
                        elif content_type == "text/html" and not email_body:
                            payload = part.get_payload(decode=True)
                            if payload:
                                email_body = BeautifulSoup(payload, "html.parser").get_text()

                    # Clean email body
                    clean_body = clean_email_body(email_body)

                    # Store email metadata
                    email_info = {
                        "from": sender,
                        "to": recipient,
                        "cc": cc,
                        "bcc": bcc,
                        "subject": subject,
                        "date": date_str,
                        "body": clean_body,
                        "attachments": attachments
                    }

                    email_data.append(email_info)

                    # Save each email as a separate JSON file
                    json_filename = os.path.join(emails_folder, f"email_{filename_timestamp}.json")
                    with open(json_filename, "w", encoding="utf-8") as json_file:
                        json.dump(email_info, json_file, indent=4, ensure_ascii=False)
                    
                    print(f"✅ Saved email '{subject}' to {json_filename}")

        mail.logout()
        return email_data, json_filename

    except Exception as e:
        print("❌ Error:", str(e))
        return None
