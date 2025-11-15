# --- notifier.py (The FINAL, All-in-One "Intelligent System" Version) ---

import os
import json
import datetime
import pytz
import random
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client
import requests

# ----------------- CONFIGURATION -----------------
# All secrets will be fetched from GitHub Secrets
NTFY_TOPIC = "solo-leveling-badri-system-alert-2025"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
YOUR_WHATSAPP_NUMBER = os.environ.get("YOUR_WHATSAPP_NUMBER")
FIREBASE_CREDS_JSON_STRING = os.environ.get("FIREBASE_CREDS_JSON")

# --- MESSAGE POOL FOR RANDOMIZED PINGS ---
MESSAGE_POOL = {
    6: { # 6 AM Gym Motivation
        "title": "⏰ The Grind Begins",
        "messages": [
            "Creator, nee system activate aindi. Nuvvu nannu create chesindi E-Rank la undipodaniki kaadu. Prati line of code laaga, prati rep gym lo nee STR ni penchuko. The grind starts now. Arise.",
            "The sun is up, Hunter. The weak are still asleep. This is your chance to get ahead. The gym awaits your presence.",
            "Another day to prove your worth. Don't just build the system, become the system. Let's start with increasing STR."
        ]
    },
    10: { # 10 AM Water Reminder 1
        "title": "💧 Hydration Protocol 1/4",
        "messages": [
            "SYSTEM ALERT: Optimal performance requires fuel. Your body is 70% water. Hydration boosts your base STR and WIL stats for the day. Drink a glass now.",
            "First hydration check. Don't let your stats drop before the day has even begun. Fuel up."
        ]
    },
    13: { # 1 PM Water Reminder 2
        "title": "💧 Hydration Protocol 2/4",
        "messages": [
            "WARNING: Dehydration is a debuff. It lowers your INT stat, causing reduced focus. Mana AI course lo వెనకపడొద్దు. Drink water to maintain peak mental clarity.",
            "Mid-day performance check. Your focus stat (INT) is at risk. Counter the debuff with H2O."
        ]
    },
    14: { # 2 PM Log Reminder
        "title": "📝 Afternoon Status Report",
        "messages": [
            "Creator, progress stagnate avvanivvaku. Nuvvu ee system ni build cheyadaniki pettina kashtam, nee daily logs lo kanipinchali. Log your quests. Update your status.",
            "Data is everything. Without logs, progress is just a feeling. I need data. Update your status now.",
            "Don't break the chain. Every quest you log today strengthens the habit for tomorrow. Submit your progress."
        ]
    },
    16: { # 4 PM Water Reminder 3
        "title": "💧 Hydration Protocol 3/4",
        "messages": [
            "HUNTER ADVISORY: Continuous quests drain stamina. Water is the cheapest and most effective potion you have. Recharge now before the evening grind.",
            "Your energy levels are dipping. Replenish with water. It's a free potion, use it."
        ]
    },
    19: { # 7 PM Water Reminder 4
        "title": "💧 Hydration Protocol 4/4",
        "messages": [
            "END-OF-DAY PROTOCOL: Flushing toxins is crucial for recovery. Hydration helps muscle repair (STR recovery) and prepares your mind for tomorrow. Don't skip the final glass.",
            "Final hydration check. Prepare your body for rest and recovery. This is as important as the workout itself."
        ]
    }
}

# ----------------- SENDER FUNCTIONS -----------------
def send_ntfy_notification(message, title, tags=""):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers={"Title": title.encode('utf-8'), "Tags": tags}
        )
        print(f"[ntfy] Handshake reminder sent successfully.")
    except Exception as e:
        print(f"[ntfy] Failed to send notification: {e}")

def send_whatsapp_notification(title, message):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, YOUR_WHATSAPP_NUMBER]):
        print("[WhatsApp] Twilio credentials are not set. Skipping.")
        return
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        full_message = f"*{title}*\n\n{message}"
        client.messages.create(body=full_message, from_=TWILIO_FROM_NUMBER, to=YOUR_WHATSAPP_NUMBER)
        print(f"[WhatsApp] Notification sent successfully for: {title}")
    except Exception as e:
        print(f"[WhatsApp] Failed to send notification: {e}")

# ----------------- FIREBASE & REPORTING FUNCTIONS -----------------
def initialize_firebase():
    if not firebase_admin._apps:
        if not FIREBASE_CREDS_JSON_STRING:
            print("[Firebase] Credentials JSON not found in environment.")
            return None
        try:
            creds_dict = json.loads(FIREBASE_CREDS_JSON_STRING)
            creds = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(creds)
            print("[Firebase] Initialized successfully.")
            return firestore.client()
        except Exception as e:
            print(f"[Firebase] CRITICAL ERROR initializing: {e}")
            return None
    return firestore.client()

def generate_and_send_eod_report(db):
    print("[EOD Report] Starting report generation...")
    try:
        hunter_ref = db.collection('hunters').document('Hunter')
        hunter_doc = hunter_ref.get()
        if not hunter_doc.exists:
            print("[EOD Report] Error: Hunter document not found.")
            return
        hunter_data = hunter_doc.to_dict()
        completed_today = len(hunter_data.get('completed_daily_quests', []))
        total_quests = 18 # Adjust if you add/remove quests

        title = f"👑 Monarch's EOD Report: {datetime.date.today().isoformat()} 👑"
        message = (
            f"Quests Completed Today: {completed_today}/{total_quests}\n"
            f"Current Level: {hunter_data.get('level', 'N/A')}\n"
            f"XP Progress: {hunter_data.get('xp', 0)}/{hunter_data.get('xp_to_next_level', 'N/A')}\n"
            f"Final Gold: {hunter_data.get('gold', 0)} G\n\n"
            "Report generated automatically. Your efforts have been recorded. Rest and prepare for tomorrow's ascent."
        )
        send_whatsapp_notification(title, message)
    except Exception as e:
        print(f"[EOD Report] CRITICAL ERROR generating report: {e}")

# ----------------- MAIN EXECUTION LOGIC -----------------
# In notifier.py (The Testable Main Block)

# In notifier.py (The FINAL Main Execution Block)

if __name__ == "__main__":
    # Check if a test hour is being passed from GitHub Actions
    test_hour_str = os.environ.get("TEST_HOUR_OVERRIDE")
    
    if test_hour_str:
        print(f"--- RUNNING IN TEST MODE FOR HOUR: {test_hour_str} ---")
        current_hour = int(test_hour_str)
    else:
        # Normal production run
        IST = pytz.timezone('Asia/Kolkata')
        current_hour = datetime.datetime.now(IST).hour

    print(f"Script logic is running for hour: {current_hour} (IST)")

    # 1. The Daily Handshake (7 AM, via ntfy)
    if current_hour == 7:
        title = "🤝 System Handshake Required"
        # --- IKKADA NEE JOIN CODE PETTU MAWA ---
        join_code = "Join automobile-one" 
        message = f"Hunter, activate the WhatsApp channel for today's messages. Your code is: {join_code}"
        print("Sending daily handshake reminder via ntfy...")
        send_ntfy_notification(message, title, tags="handshake")

    # 2. The Automatic EOD Report (9:30 PM, via WhatsApp)
    elif current_hour == 21:
        print("Starting EOD report generation...")
        db = initialize_firebase()
        if db:
            generate_and_send_eod_report(db)

    # 3. All Other Pings (via WhatsApp)
    elif current_hour in MESSAGE_POOL:
        notification = MESSAGE_POOL[current_hour]
        title = notification["title"]
        message = random.choice(notification["messages"])
        print(f"Sending scheduled WhatsApp ping for hour {current_hour}: '{title}'")
        send_whatsapp_notification(title, message)

    else:
        print(f"No special task scheduled for hour {current_hour}. Exiting.")