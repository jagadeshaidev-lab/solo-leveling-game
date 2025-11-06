# --- notifier.py (The Upgraded Version) ---

import requests
import datetime
import pytz
import os  # <-- KOTHAGA IMPORT CHEYI
from twilio.rest import Client  # <-- KOTHAGA IMPORT CHEYI

# ----------------- NTFY CONFIGURATION -----------------
NTFY_TOPIC = "solo-leveling-badri-system-alert-2025" 

# ----------------- TWILIO CONFIGURATION -----------------
# Ee details manam GitHub Secrets nunchi teeskuntam
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER") # e.g., 'whatsapp:+14155238886'
YOUR_WHATSAPP_NUMBER = os.environ.get("YOUR_WHATSAPP_NUMBER") # e.g., 'whatsapp:+919876543210'

# --- FUNCTION 1: Ntfy (Already undi) ---
def send_notification(message, title, tags=""):
    # ... (ee function lo em change ledu) ...
    pass # Just for example

# --- FUNCTION 2: WhatsApp (Kotha function) ---
def send_whatsapp_notification(message, title):
    """Sends a notification via Twilio WhatsApp Sandbox."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, YOUR_WHATSAPP_NUMBER]):
        print("Twilio credentials are not set. Skipping WhatsApp notification.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        full_message = f"*{title}*\n\n{message}" # WhatsApp lo title bold ga kanipistundi
        
        message = client.messages.create(
            body=full_message,
            from_=TWILIO_FROM_NUMBER,
            to=YOUR_WHATSAPP_NUMBER
        )
        print(f"WhatsApp notification sent successfully!")
    except Exception as e:
        print(f"Failed to send WhatsApp notification: {e}")


if __name__ == "__main__":
    IST = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(IST)

    # ... (existing time logic antha same) ...
    if 6 <= now_ist.hour < 12:
        title = "🌅 Rise and Shine, Hunter!"
        message = "A new day has begun. Your daily quests are waiting. Let's get stronger today!"
        tags = "sunrise,partying_face"
    elif 19 <= now_ist.hour < 22:
        title = "🌙 Evening Report Due"
        message = "The day is ending. Don't forget to log your quests and submit your EOD Vigilance report."
        tags = "night_with_stars,clipboard"
    else:
        title = "System Check-in"
        message = "Just checking in, Hunter. Keep up the hustle."
        tags = "robot_face"
        
    # Ippudu manam rendu functions ni call chestunnam
    send_notification(message, title, tags)
    send_whatsapp_notification(message, title)
