# --- test_notifier.py (The FINAL "Twilio Only" Test Version) ---
# This file is ONLY for local testing. DO NOT PUSH TO GITHUB.

import os
import sys
import pathlib

# Fix for ModuleNotFoundError when running from a subfolder
sys.path.append(str(pathlib.Path(__file__).parent.parent))

# --- STEP A: PASTE YOUR REAL SECRETS HERE ---
os.environ['TWILIO_ACCOUNT_SID'] = "AC383e2107cac16a848fcd411b8e599f0c"
os.environ['TWILIO_AUTH_TOKEN'] = "7034bf6b813850b7b5b9447f65be9392" # Nee real token ikkada pettu
os.environ['TWILIO_FROM_NUMBER'] = "whatsapp:+14155238886"
os.environ['YOUR_WHATSAPP_NUMBER'] = "whatsapp:+919154625353"
# NOTE: Firebase creds are not needed for this test

# --- STEP B: IMPORT ONLY THE WHATSAPP FUNCTION ---
# Manam ippudu just WhatsApp function ne import chestunnam
from notifier import send_whatsapp_notification

print("--- STARTING TWILIO-ONLY LOCAL TEST ---")
print("Bypassing all time checks and Firebase...")

try:
    # Manam direct ga WhatsApp function ni call chestunnam
    title = "Direct Test Message 🚀"
    message = "Hunter, this is a direct test from Twilio. If you see this, Twilio is working perfectly. The bug is found!"
    
    send_whatsapp_notification(title, message)
    
    print("\nWhatsApp function call finished. Check your phone!")
except Exception as e:
    print(f"\nAn error occurred while calling send_whatsapp_notification: {e}")

print("--- TWILIO-ONLY LOCAL TEST COMPLETE ---")