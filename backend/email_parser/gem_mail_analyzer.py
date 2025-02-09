import json
import ollama
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv


def categorize_email_with_ollama(email_body):
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        print("Error: Gemini key not found")
        return [], 0

    # Configure the Google Generative AI SDK with the API key
    genai.configure(api_key=api_key)
    """Uses Ollama (LLaMA) to classify an email into predefined categories and measures time taken."""
    prompt = f"""
    You are an AI email classifier. Classify the following email into one of these categories:
    1. Meeting Request
    2. Task Assignment
    3. Follow-up
    4. Transcript mail: This means that if the mail has transcript of meeting

    Email Content:
    {email_body}

    Return only the category name. without number
    """

    start_time = time.time()  # Start timer
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    end_time = time.time()  # End timer

    category = response.text.strip()
    processing_time = end_time - start_time  # Calculate time taken

    return category, processing_time

async def analyze_emails_with_ollama(input_file, output_file,websocket):
    """Reads emails from JSON, assigns categories using Ollama, and saves results with timing."""
    with open(input_file, "r", encoding="utf-8") as f:
        emails = json.load(f)

    categorized_emails = []
    total_time = 0

    for email in emails:
        category, time_taken = categorize_email_with_ollama(email["body"])
        email["category"] = category
        email["processing_time"] = round(time_taken, 3)  # Round to 3 decimal places
        categorized_emails.append(email)
        
        total_time += time_taken
        print(f"Categorized email from '{email['from']}' as '{category}' (Time: {time_taken:.3f} sec)")
       
        await websocket.send_text(f"mail_categorized {category}")  # Send message to WebSocket



    # Save results
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(categorized_emails, f, indent=4)

    print(f"\nEmails categorized and saved to {output_file}")
    print(f"Total processing time: {total_time:.3f} sec")
    print(f"Average processing time per email: {total_time / len(emails):.3f} sec" if emails else "No emails to process.")

# Run the script
