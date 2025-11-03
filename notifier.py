# --- notifier.py ---

import requests
import datetime
import pytz # Library to handle timezones

# ----------------- CONFIGURATION -----------------
# IKKADA NEE SECRET CHANNEL NAME PETTU MAWA
NTFY_TOPIC = "solo-leveling-badri-system-alert-2025" 
# -----------------------------------------------

# --- notifier.py (Corrected function) ---

# --- notifier.py (Guaranteed Fix) ---

def send_notification(message, title, tags=""):
    """Sends a notification to your ntfy.sh topic."""
    try:
        # We MUST encode both the title and the message to handle emojis
        encoded_title = title.encode('utf-8')
        encoded_message = message.encode('utf-8')

        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=encoded_message,
            headers={
                "Title": encoded_title,
                "Tags": tags 
            }
        )
        print(f"Notification sent successfully: '{title}'")
    except Exception as e:
        print(f"Failed to send notification: {e}")

# This is the main part that runs when the script is executed
if __name__ == "__main__":
    # --- Time-based Logic ---
    # We will use India Standard Time (IST)
    IST = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(IST)

    # Check if it's morning (6 AM to 12 PM)
    if 6 <= now_ist.hour < 12:
        title = "🌅 Rise and Shine, Hunter!"
        message = "A new day has begun. Your daily quests are waiting. Let's get stronger today!"
        tags = "sunrise,partying_face"
    # Check if it's evening (7 PM to 10 PM)
    elif 19 <= now_ist.hour < 22:
        title = "🌙 Evening Report Due"
        message = "The day is ending. Don't forget to log your quests and submit your EOD Vigilance report."
        tags = "night_with_stars,clipboard"
    else:
        # If run at any other time, just send a generic message
        title = "System Check-in"
        message = "Just checking in, Hunter. Keep up the hustle."
        tags = "robot_face"
        
    send_notification(message, title, tags)