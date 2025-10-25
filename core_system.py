# --- core_system.py ---

import streamlit as st
from datetime import date, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd # Import pandas here as it's a core utility for data handling

# --- 1. CONFIG: GAME CONSTANTS ---
BASE_XP = 1000
XP_MULTIPLIER = 1.5
# NOTE: Using the comprehensive QUESTS dictionary from your initial V4.0 code.
QUESTS  = {
    # 🌅 Morning Rituals
    "wake_early": {
        "name": "Wake Up by 6:00 AM (Rise & Shine)",
        "xp": 40,
        "gold": 4,
        "stat_bonus": ("wil", 1),
        "is_mandatory": True
    },
    "gym_morning": {
        "name": "Gym Workout (6:30–8:00 AM)",
        "xp": 150,
        "gold": 15,
        "stat_bonus": ("str", 2)
    },
    "meditation": {
        "name": "Meditate for 5–10 Minutes",
        "xp": 30,
        "gold": 3,
        "stat_bonus": ("intel", 1)
    },
    "breakfast_1": {
        "name": "Eat Proper Breakfast (Protein + Fiber)",
        "xp": 35,
        "gold": 3,
        "stat_bonus": ("str", 1)
    },

    # 💻 Work Quests – Ardhamayyela Hustle
    "server_check": {
        "name": "Daily System Check (Servers @ 9 AM)",
        "xp": 20,
        "gold": 2,
        "stat_bonus": ("wil", 1)
    },
    "ai_course_1": {
        "name": "AI Course Study (10–11 AM)",
        "xp": 200,
        "gold": 20,
        "stat_bonus": ("intel", 2),
        "is_mandatory": True
    },
    "tickets": {
        "name": "Resolve Assigned Tickets (11–12 PM)",
        "xp": 100,
        "gold": 10,
        "stat_bonus": ("intel", 1)
    },
    "breakfast_2": {
        "name": "Eat Healthy Lunch",
        "xp": 35,
        "gold": 3,
        "stat_bonus": ("str", 1)
    },
    "hydration": {
        "name": "Drink 3–4 Liters of Water",
        "xp": 25,
        "gold": 2,
        "stat_bonus": ("str", 1)
    },
    "ai_course_2": {
        "name": "AI Course Study (4–5 PM)",
        "xp": 200,
        "gold": 20,
        "stat_bonus": ("intel", 2)
    },

    # 🌙 Evening Rituals
    "walk_night": {
        "name": "Night Walk (9–10 PM)",
        "xp": 50,
        "gold": 5,
        "stat_bonus": ("wil", 1)
    },
    "standup": {
        "name": "Daily Progress Report (Stand-up @ 8:30 PM)",
        "xp": 30,
        "gold": 3,
        "stat_bonus": ("cha", 1),
        "is_mandatory": True
    },

    # 🧠 Bonus Quests – Copilot’s Picks
    "gratitude_journal": {
        "name": "Write 3 Gratitude Points",
        "xp": 20,
        "gold": 2,
        "stat_bonus": ("wil", 1)
    },
    "binaural_beats": {
        "name": "Listen to 40Hz Gamma Beats (30 mins)",
        "xp": 30,
        "gold": 3,
        "stat_bonus": ("intel", 1)
    },
    "posture_check": {
        "name": "Correct Sitting Posture (Ergo Boost)",
        "xp": 15,
        "gold": 1,
        "stat_bonus": ("str", 1)
    },
    "no_doomscrolling": {
        "name": "Avoid Doomscrolling (Digital Discipline)",
        "xp": 25,
        "gold": 2,
        "stat_bonus": ("wil", 1)
    },
    "send_meme": {
        "name": "Send a Dank Meme to a Friend",
        "xp": 10,
        "gold": 1,
        "stat_bonus": ("cha", 1)
    }
}
STORE_ITEMS = {
    "insta": {"name": "15 Mins Insta Scroll", "cost": 15},
    "tv": {"name": "1 Episode of a TV Show", "cost": 30},
    "junk": {"name": "Order Junk Food (Cheat Meal)", "cost": 100},
    "yt": {"name": "30 Mins YouTube Binge", "cost": 25}
}


# --- 2. FIREBASE DATABASE FUNCTIONS ---
def initialize_firebase():
    """Initializes Firebase and returns the Firestore client."""
    if not firebase_admin._apps:
        # Load credentials from Streamlit's secrets management
        creds_dict = dict(st.secrets["firebase_credentials"])
        creds = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(creds)
    return firestore.client()

def load_data(hunter_name="Hunter"):
    """Loads the main hunter document."""
    db = initialize_firebase()
    doc_ref = db.collection('hunters').document(hunter_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def save_data():
    """Saves the main hunter state and today's history."""
    if 'hunter' in st.session_state:
        db = initialize_firebase()
        hunter_name = st.session_state.hunter['name']
        
        # 1. Save main hunter document
        doc_ref = db.collection('hunters').document(hunter_name)
        doc_ref.set(st.session_state.hunter)
        
        # 2. Save today's history in a sub-collection
        today_str = date.today().isoformat()
        history_ref = db.collection('hunters').document(hunter_name).collection('history').document(today_str)
        history_data = {
            'completed_quests': st.session_state.hunter.get('completed_daily_quests', []),
            'gold_at_day_end': st.session_state.hunter['gold'], # Capture state for history
            'xp_at_day_end': st.session_state.hunter['xp'],
            'level_at_day_end': st.session_state.hunter['level']
        }
        history_ref.set(history_data, merge=True)
        

# --- 3. STATE INITIALIZATION & DAILY LOGIC ---
def initialize_state():
    """Initializes session state with hunter data (loads from Firebase if available)."""
    if 'hunter' not in st.session_state:
        saved_data = load_data("Hunter") 
        if saved_data:
            st.session_state.hunter = saved_data
        else:
            st.session_state.hunter = {
                "name": "Hunter", "rank": "E-Rank", "level": 1, "xp": 0,
                "xp_to_next_level": int(BASE_XP), "gold": 0, "skill_points": 0,
                "stats": {"str": 5, "intel": 5, "wil": 5, "fin": 5, "cha": 5},
                "last_login": "2000-01-01", 
                "completed_daily_quests": []
            }

def daily_reset_and_check():
    """Checks for missed mandatory quests from yesterday and resets state for today."""
    initialize_state() # Ensure state exists before checking
    hunter = st.session_state.hunter
    today = date.today().isoformat()
    
    if hunter.get('last_login') < today:
        db = initialize_firebase()
        
        # Check for missed mandatory quests from YESTERDAY
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()
        yesterday_history_doc = db.collection('hunters').document(hunter['name']).collection('history').document(yesterday_str).get()
        
        yesterday_completed = []
        if yesterday_history_doc.exists:
            yesterday_completed = yesterday_history_doc.to_dict().get('completed_quests', [])

        mandatory_quests = {k: v for k, v in QUESTS.items() if v.get("is_mandatory")}
        yesterday_mandatory_missed = any(
            key not in yesterday_completed for key in mandatory_quests
        )
        
        if yesterday_mandatory_missed and yesterday_str != '2000-01-01': # Avoid penalty on first-ever login
            penalty_gold = 20
            hunter['gold'] = max(0, hunter['gold'] - penalty_gold) # Ensure gold doesn't go negative
            st.error(f"SYSTEM PENALTY: Mandatory quest missed yesterday. -{penalty_gold} Gold.")
        
        # Reset for the new day
        hunter['last_login'] = today
        hunter['completed_daily_quests'] = []
        st.info("A new day has begun. Daily Quests have been reset!")
        save_data()
    
def check_for_level_up():
    """Checks if the Hunter has enough XP to level up."""
    hunter = st.session_state.hunter
    if hunter['xp'] >= hunter['xp_to_next_level']:
        hunter['level'] += 1
        hunter['xp'] -= hunter['xp_to_next_level']
        hunter['xp_to_next_level'] = int(BASE_XP * (hunter['level'] ** XP_MULTIPLIER))
        hunter['skill_points'] += 5
        st.balloons()
        st.success(f"LEVEL UP! You are now Level {hunter['level']}! (+5 Skill Points)")
        save_data()
        st.rerun()

def load_history_data(limit=30):
    """Fetches the last N days of quest history from Firebase as a DataFrame."""
    try:
        db = initialize_firebase()
        hunter_name = st.session_state.hunter['name']
        
        history_ref = db.collection('hunters').document(hunter_name).collection('history')
        
        # Query the last N documents, ordered by date (descending)
        docs = history_ref.order_by(firestore.FieldPath.document_id(), direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        data_list = []
        for doc in docs:
            day = doc.to_dict()
            date_str = doc.id
            
            data_list.append({
                'Date': date_str,
                'Completed Quests Count': len(set(day.get('completed_quests', []))),
                'Total Quests Count': len(QUESTS),
                'End Level': day.get('level_at_day_end', 1),
                'End XP': day.get('xp_at_day_end', 0),
                'End Gold': day.get('gold_at_day_end', 0)
            })
            
        # Reverse the list so the oldest date is at the top for proper charting
        data_list.reverse() 
        return pd.DataFrame(data_list)

    except Exception as e:
        # st.error(f"Error loading history: {e}") # Commented out to prevent errors in core module
        return pd.DataFrame()