# --- notifier.py (The Corrected and Cleaned Version) ---

import requests
import datetime
import pytz
import os
import json
import random
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, firestore

# ----------------- CONFIGURATION -----------------
NTFY_TOPIC = "solo-leveling-badri-system-alert-2025" 

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
YOUR_WHATSAPP_NUMBER = os.environ.get("YOUR_WHATSAPP_NUMBER")

FIREBASE_CREDS_JSON_STRING = os.environ.get("FIREBASE_CREDS_JSON")

# --- MESSAGE POOL FOR RANDOM MESSAGES ---
MESSAGE_POOL = {
    6:  [ "Creator, nee system activate aindi... Arise.", "The sun is up, Hunter. The weak are still asleep. This is your chance to get ahead. Gym awaits.", "Another day to prove your worth. Don't just build the system, become the system. Let's start with STR." ],
    14: [ "Creator, progress stagnate avvanivvaku... Log your quests.", "Data is everything. Without logs, progress is just a feeling. I need data. Update your status now.", "Don't break the chain. Every quest you log today strengthens the habit for tomorrow. Submit your progress." ]
}

# ----------------- SENDER FUNCTIONS -----------------

def send_ntfy_notification(message, title, tags=""):
    """Sends a notification to your ntfy.sh topic."""
    try:
        # (Ntfy logic goes here, for now we pass)
        print(f"[NTFY] Would send: {title} - {message}")
        pass
    except Exception as e:
        print(f"Failed to send ntfy notification: {e}")

def send_whatsapp_notification(title, message):
    """Sends a notification via Twilio WhatsApp Sandbox."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, YOUR_WHATSAPP_NUMBER]):
        print("[WhatsApp] Twilio credentials are not set. Skipping.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        full_message = f"*{title}*\n\n{message}"
        
        msg = client.messages.create(
            body=full_message,
            from_=TWILIO_FROM_NUMBER,
            to=YOUR_WHATSAPP_NUMBER
        )
        print("[WhatsApp] Notification sent successfully!")
    except Exception as e:
        print(f"[WhatsApp] Failed to send notification: {e}")

# ----------------- FIREBASE & REPORTING FUNCTIONS -----------------

def initialize_firebase_for_notifier():
    # ... (This function is the same as before, no changes needed)
    pass # Placeholder

def generate_and_send_eod_report(db):
    # ... (This function is the same as before, no changes needed)
    pass # Placeholder

# ----------------- MAIN EXECUTION LOGIC -----------------

def get_notification_content(current_hour):
    if current_hour in MESSAGE_POOL:
        message = random.choice(MESSAGE_POOL[current_hour])
        if current_hour == 6: title = "⏰ The Grind Begins"
        elif current_hour == 14: title = "📝 Afternoon Status Report"
        else: title = "System Notification"
        return title, message, "tada"
    return None, None, None

if __name__ == "__main__":
    IST = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(IST)
    current_hour = now_ist.hour

    if current_hour == 21:
        # EOD Report Logic
        db = initialize_firebase_for_notifier()
        if db:
            generate_and_send_eod_report(db)
    else:
        # Normal Message Logic
        title, message, tags = get_notification_content(current_hour)
        if title and message:
            print(f"Sending notification for hour {current_hour}: '{title}'")
            send_ntfy_notification(message, title, tags)
            send_whatsapp_notification(title, message)
        else:
            print(f"No notification scheduled for hour {current_hour}.")