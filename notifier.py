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
            "Another day to prove your worth. Don't just build the system, become the system. Let's start with increasing STR.",
            "The System has issued a new command: 'Become Stronger'. Your daily quest to conquer the Iron Dungeon (Gym) has begun. Accept the challenge, Hunter. Arise.",
            "The dawn of a new adventure! Even the future Pirate King trains every day to master his Haki. Your gym is your training ground. Go claim your strength!",
            "The world is still asleep, but legends are forged in the quiet hours of the morning. This is your time. Go build the strength worthy of the stories they will one day tell about you."
        ]
    },
    10: { # 10 AM Water Reminder 1
        "title": "💧 Hydration Protocol 1/4",
        "messages": [
            "SYSTEM ALERT: Optimal performance requires fuel. Your body is 70% water. Hydration boosts your base STR and WIL stats for the day. Drink a glass now.",
            "First hydration check. Don't let your stats drop before the day has even begun. Fuel up.",
            "SYSTEM: Mana levels are suboptimal. Water is the most basic potion to replenish your core energy. Consume now to prevent a status debuff.",
            "Even a Devil Fruit user needs water to cross the Grand Line. Your body is your ship; don't let it run dry in the calm belt of the morning. Hydrate!",
            "The engine of your ambition runs on water. You wouldn't start a long journey with an empty tank. Fuel up now. The day has just begun."
        ]
    },
    13: { # 1 PM Water Reminder 2
        "title": "💧 Hydration Protocol 2/4",
        "messages": [
            "WARNING: Dehydration is a debuff. It lowers your INT stat, causing reduced focus. Mana AI course lo వెనకబడొద్దు. Drink water to maintain peak mental clarity.",
            "Mid-day performance check. Your focus stat (INT) is at risk. Counter the debuff with H2O.",
            "WARNING: INT stat is dropping due to low hydration. Your ability to process information and learn is being compromised. Drink water to restore focus.",
            "The sun is high, just like at Alabasta. Don't let the heat drain you. A smart navigator always manages his resources. Water is your most critical resource now.",
            "The afternoon slump is a monster. Its weakness is water. Land a critical hit on fatigue and reclaim your focus. Drink a glass now."
        ]
    },
    14: { # 2 PM Log Reminder
        "title": "📝 Afternoon Status Report",
        "messages": [
            "Creator, progress stagnate avvanivvaku. Nuvvu ee system ni build cheyadaniki pettina kashtam, nee daily logs lo kanipinchali. Log your quests. Update your status.",
            "Data is everything. Without logs, progress is just a feeling. I need data. Update your status now.",
            "Don't break the chain. Every quest you log today strengthens the habit for tomorrow. Submit your progress.",
            "System Administrator, the day's data is incomplete. Log your completed quests. Every entry is a record of your growth, turning today's effort into tomorrow's stats.",
            "A captain must know his ship's status. Your logbook is empty. Record your journey's progress. Every small victory logged today brings you one step closer to the One Piece.",
            "A battle fought but not recorded is a lesson lost. Your morning was the battle; this is the debrief. Log your progress. Acknowledge your wins. Analyze your misses. Grow."
        ]
    },
    16: { # 4 PM Water Reminder 3
        "title": "💧 Hydration Protocol 3/4",
        "messages": [
            "HUNTER ADVISORY: Continuous quests drain stamina. Water is the cheapest and most effective potion you have. Recharge now before the evening grind.",
            "Your energy levels are dipping. Replenish with water. It's a free potion, use it.",
            "Your HP and MP regeneration rates are slowing. Quests consume resources. Replenish them. Water is the key to sustained performance.",
            "The final stretch before the evening feast! A true member of the Straw Hat crew never neglects their duty. Hydrate to finish the day's adventure strong.",
            "You're not tired. You're thirsty. Don't mistake the symptom for the cause. Fix the root problem. Hydrate."
        ]
    },
    19: { # 7 PM Water Reminder 4
        "title": "💧 Hydration Protocol 4/4",
        "messages": [
            "END-OF-DAY PROTOCOL: Flushing toxins is crucial for recovery. Hydration helps muscle repair (STR recovery) and prepares your mind for tomorrow. Don't skip the final glass.",
            "Final hydration check. Prepare your body for rest and recovery. This is as important as the workout itself.",
            "SYSTEM PROTOCOL: Initiate End-of-Day Recovery. Water flushes out metabolic waste from your quests, accelerating stat recovery for tomorrow. Complete the protocol.",
            "The ship is docking for the night. Time to patch up and restock. Water aids your body's recovery, so you're ready to set sail at dawn. The Grand Line waits for no one.",
            "The work is done, but the growth has just begun. Recovery is where you get stronger. Give your body the final tool it needs for tonight's repairs: water."
        ]
    }
}

# ----------------- SENDER FUNCTIONS -----------------
def send_ntfy_notification(message, title, tags=""):
    try:
        resp = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers={"Title": title, "Tags": tags},
            timeout=5
        )
        if resp.ok:
            print(f"[ntfy] Notification sent successfully (status {resp.status_code}).")
        else:
            print(f"[ntfy] Failed to send notification: status={resp.status_code} body={resp.text}")
    except Exception as e:
        print(f"[ntfy] Failed to send notification: {e}")

def send_whatsapp_notification(title, message):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, YOUR_WHATSAPP_NUMBER]):
        print("[WhatsApp] Twilio credentials are not set. Skipping.")
        return
    try:
        def _ensure_whatsapp_prefix(num):
            if not num:
                return num
            return num if num.startswith("whatsapp:") else f"whatsapp:{num}"

        from_num = _ensure_whatsapp_prefix(TWILIO_FROM_NUMBER)
        to_num = _ensure_whatsapp_prefix(YOUR_WHATSAPP_NUMBER)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        full_message = f"*{title}*\n\n{message}"
        client.messages.create(body=full_message, from_=from_num, to=to_num)
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
        total_quests = 18  # Adjust if you add/remove quests

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
if __name__ == "__main__":
    test_hour_str = os.environ.get("TEST_HOUR_OVERRIDE")
    
    if test_hour_str and test_hour_str.isdigit():
        print(f"--- RUNNING IN TEST MODE FOR HOUR: {test_hour_str} ---")
        current_hour = int(test_hour_str)
    else:
        IST = pytz.timezone('Asia/Kolkata')
        current_hour = datetime.datetime.now(IST).hour

    print(f"Script logic is running for hour: {current_hour} (IST)")

    if current_hour == 7:
        title = "🤝 System Handshake Required"
        # IKKADA NEE JOIN CODE PETTU MAWA
        join_code = "Join automobile-one" 
        message = f"Hunter, activate the WhatsApp channel for today's messages. Your code is: `{join_code}`"
        print("Sending daily handshake reminder via ntfy...")
        send_ntfy_notification(message, title, tags="handshake")

    elif current_hour == 21:
        print("Starting EOD report generation...")
        db = initialize_firebase()
        if db:
            generate_and_send_eod_report(db)

    elif current_hour in MESSAGE_POOL:
        notification = MESSAGE_POOL[current_hour]
        title = notification["title"]
        message = random.choice(notification["messages"])
        print(f"Sending scheduled WhatsApp ping for hour {current_hour}: '{title}'")
        send_whatsapp_notification(title, message)

    else:
        print(f"No special task scheduled for hour {current_hour}. Exiting.")