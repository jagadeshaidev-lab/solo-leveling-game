# --- test_notifier.py (The "Twilio Only" Test Version) ---

import os
import sys
import pathlib

# Fix for ModuleNotFoundError
sys.path.append(str(pathlib.Path(__file__).parent.parent))

# --- STEP A: PASTE YOUR REAL SECRETS HERE ---
os.environ['TWILIO_ACCOUNT_SID'] = "AC383e2107cac16a848fcd411b8e599f0c"
os.environ['TWILIO_AUTH_TOKEN'] = "YOUR_REAL_AUTH_TOKEN_HERE" # Nee real token ikkada pettu
os.environ['TWILIO_FROM_NUMBER'] = "whatsapp:+14155238886"
os.environ['YOUR_WHATSAPP_NUMBER'] = "whatsapp:+919154625353"
# Note: FIREBASE_CREDS_JSON ippudu avasaram ledu

# --- STEP B: IMPORT ONLY THE WHATSAPP FUNCTION ---
# Manam ippudu just WhatsApp function ne import chestunnam
from notifier import send_whatsapp_notification

print("--- STARTING TWILIO-ONLY LOCAL TEST ---")

# --- STEP C: RUN THE TEST, SKIPPING FIREBASE ---
print("Bypassing Firebase. Attempting to send a direct WhatsApp message...")

try:
    # Manam direct ga WhatsApp function ni call chestunnam
    title = "Direct Test Message"
    message = "Hunter, this is a direct test from Twilio. If you see this, Twilio is working perfectly."
    send_whatsapp_notification(title, message)
    print("\nWhatsApp function call finished successfully!")
except Exception as e:
    print(f"\nAn error occurred while calling send_whatsapp_notification: {e}")

print("--- TWILIO-ONLY LOCAL TEST COMPLETE ---")