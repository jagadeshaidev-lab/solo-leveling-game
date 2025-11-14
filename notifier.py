# --- notifier.py (The "Data Scientist" Version) ---

import requests
import datetime
import pytz
import os
import json # <-- Kotha import
from twilio.rest import Client
import firebase_admin # <-- Kotha import
from firebase_admin import credentials, firestore # <-- Kotha import

# ----------------- CONFIGURATION -----------------
# ... (ntfy and twilio config antha same to same) ...

# --- NEW: Firebase Configuration ---
FIREBASE_CREDS_JSON_STRING = os.environ.get("FIREBASE_CREDS_JSON")

# ----------------- FUNCTIONS -----------------
# ... (send_ntfy_notification and send_whatsapp_notification functions antha same) ...

# --- NEW: Function to Connect to Firebase ---
def initialize_firebase_for_notifier():
    if not firebase_admin._apps:
        if FIREBASE_CREDS_JSON_STRING:
            try:
                creds_dict = json.loads(FIREBASE_CREDS_JSON_STRING)
                creds = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(creds)
                print("Firebase initialized successfully for notifier.")
                return firestore.client()
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
                return None
        else:
            print("Firebase credentials not found in environment.")
            return None
    return firestore.client()

# --- NEW: Function to Generate and Send EOD Report ---
def generate_and_send_eod_report(db):
    try:
        doc_ref = db.collection('hunters').document('Hunter')
        doc = doc_ref.get()
        if doc.exists:
            hunter = doc.to_dict()
            
            # --- History nunchi aa roju data teeskundam ---
            today_str = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
            history_ref = doc_ref.collection('history').document(today_str)
            history_doc = history_ref.get()
            
            completed_count = 0
            if history_doc.exists:
                completed_count = len(history_doc.to_dict().get('completed_quests', []))
            
            total_quests = 20 # Hardcoding for now, as QUESTS dict is not here

            # --- Report Prepare Cheyadam ---
            summary_title = f"👑 MONARCH'S EOD REPORT: {today_str} 👑"
            summary_body = (
                f"Quests Completed Today: {completed_count}/{total_quests}\n"
                f"Current Level: {hunter.get('level', 'N/A')}\n"
                f"XP Progress: {hunter.get('xp', 0)}/{hunter.get('xp_to_next_level', 'N/A')}\n"
                f"Final Gold: {hunter.get('gold', 0)} G\n\n"
                "Report generated automatically. Your efforts have been recorded. Rest and prepare for tomorrow's ascent."
            )
            final_message = f"{summary_title}\n\n{summary_body}"
            
            send_whatsapp_notification("EOD Report", final_message) # Note: Title and message swapped for WhatsApp
        else:
            print("Hunter document not found.")
    except Exception as e:
        print(f"Error generating EOD report: {e}")

if __name__ == "__main__":
    IST = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(IST)
    current_hour = now_ist.hour

    # --- Night 9 PM (21:00) ki EOD Report pampali ---
    if current_hour == 21:
        print("Time to generate and send EOD report...")
        db = initialize_firebase_for_notifier()
        if db:
            generate_and_send_eod_report(db)
    else:
        # --- Migatha time lo, normal motivational messages pampali ---
        # ... (mana paatha get_notification_content logic ikkada pettukovachu) ...
        print(f"No EOD report scheduled for hour {current_hour}. Exiting.")
