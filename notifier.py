# --- notifier.py (The FINAL, All-in-One Version) ---

import os
import json
import datetime
import pytz
import random
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client

# ----------------- CONFIGURATION -----------------
# All secrets will be fetched from GitHub Secrets
NTFY_TOPIC = "solo-leveling-badri-system-alert-2025"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
YOUR_WHATSAPP_NUMBER = os.environ.get("YOUR_WHATSAPP_NUMBER")
FIREBASE_CREDS_JSON_STRING = os.environ.get("FIREBASE_CREDS_JSON")

# ----------------- SENDER FUNCTION -----------------
def send_whatsapp_notification(title, message):
    """Sends a WhatsApp message using Twilio credentials from environment variables."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, YOUR_WHATSAPP_NUMBER]):
        print("[WhatsApp] Twilio credentials are not set or are empty. Skipping.")
        return
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        full_message = f"*{title}*\n\n{message}"
        client.messages.create(body=full_message, from_=TWILIO_FROM_NUMBER, to=YOUR_WHATSAPP_NUMBER)
        print("[WhatsApp] Notification sent successfully!")
    except Exception as e:
        print(f"[WhatsApp] Failed to send notification: {e}")

# ----------------- FIREBASE & REPORTING FUNCTIONS -----------------
def initialize_firebase():
    """Initializes Firebase using credentials from environment variables."""
    if not firebase_admin._apps:
        if FIREBASE_CREDS_JSON_STRING:
            try:
                creds_dict = json.loads(FIREBASE_CREDS_JSON_STRING)
                creds = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(creds)
                print("[Firebase] Initialized successfully.")
                return firestore.client()
            except Exception as e:
                print(f"[Firebase] CRITICAL ERROR initializing: {e}")
                return None
        else:
            print("[Firebase] Credentials JSON not found in environment.")
            return None
    return firestore.client()

def generate_and_send_eod_report(db):
    """Fetches data from Firebase, generates an EOD report, and sends it via WhatsApp."""
    print("[EOD Report] Starting report generation...")
    try:
        hunter_ref = db.collection('hunters').document('Hunter')
        hunter_doc = hunter_ref.get()
        if not hunter_doc.exists:
            print("[EOD Report] Error: Hunter document not found.")
            return

        hunter_data = hunter_doc.to_dict()
        completed_today = len(hunter_data.get('completed_daily_quests', []))
        total_quests = 18 # You can adjust this number

        title = f"👑 Monarch's EOD Report: {datetime.date.today().isoformat()} 👑"
        message = (
            f"Quests Completed Today: {completed_today}/{total_quests}\n"
            f"Current Level: {hunter_data.get('level', 'N/A')}\n"
            f"XP Progress: {hunter_data.get('xp', 0)}/{hunter_data.get('xp_to_next_level', 'N/A')}\n"
            f"Final Gold: {hunter_data.get('gold', 0)} G\n\n"
            "Report generated automatically. Your efforts have been recorded. Rest and prepare for tomorrow's ascent."
        )
        send_whatsapp_notification(title, message)
        print("[EOD Report] Report sent successfully.")
    except Exception as e:
        print(f"[EOD Report] CRITICAL ERROR generating report: {e}")

# ----------------- MAIN EXECUTION LOGIC -----------------
if __name__ == "__main__":
    IST = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(IST)
    current_hour = now_ist.hour
    #current_hour = 22  # For testing purposes, set to 10 PM

    print(f"Script triggered at hour: {current_hour} (IST)")

    # Check if it's time for the EOD Report (e.g., 9 PM)
    if  current_hour == 22: # 10 PM
        db = initialize_firebase()
        if db:
            generate_and_send_eod_report(db)
    else:
        # Here you can add logic for other times (e.g., morning motivation)
        print(f"No special task scheduled for hour {current_hour}. Exiting.")