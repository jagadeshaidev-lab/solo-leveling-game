# --- SOLO LEVELING SYSTEM V4.0 (with History & Partial Quests) ---
import streamlit as st
from datetime import date, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIG (No Changes) ---
BASE_XP = 1000
XP_MULTIPLIER = 1.5
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

# --- FIREBASE DATABASE FUNCTIONS (MODIFIED for History) ---
def initialize_firebase():
    if not firebase_admin._apps:
        creds_dict = dict(st.secrets["firebase_credentials"])
        creds = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(creds)
    return firestore.client()

def save_data():
    """Saves the main hunter state and today's history."""
    if 'hunter' in st.session_state:
        db = initialize_firebase()
        hunter_name = st.session_state.hunter['name']
        
        # Save main hunter document
        doc_ref = db.collection('hunters').document(hunter_name)
        doc_ref.set(st.session_state.hunter)
        
        # Save today's history in a sub-collection
        today_str = date.today().isoformat()
        history_ref = db.collection('hunters').document(hunter_name).collection('history').document(today_str)
        history_data = {
            'completed_quests': st.session_state.hunter.get('completed_daily_quests', [])
        }
        history_ref.set(history_data, merge=True)

def load_data(hunter_name="Hunter"):
    db = initialize_firebase()
    doc_ref = db.collection('hunters').document(hunter_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None



# --- STATE INITIALIZATION (No changes) ---
def initialize_state():
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

# --- Initialize Firebase and App State ---
st.set_page_config(page_title="Solo Leveling System", layout="wide")
db = initialize_firebase()
initialize_state()
hunter = st.session_state.hunter

# --- DAILY RESET & PENALTY LOGIC (No changes) ---
today = date.today().isoformat()
if hunter.get('last_login') < today:
    # Logic to check for missed mandatory quests from YESTERDAY
    # This now requires loading yesterday's history
    yesterday_str = (date.today() - timedelta(days=1)).isoformat()
    yesterday_history_doc = db.collection('hunters').document(hunter['name']).collection('history').document(yesterday_str).get()
    
    yesterday_completed = []
    if yesterday_history_doc.exists:
        yesterday_completed = yesterday_history_doc.to_dict().get('completed_quests', [])

    yesterday_mandatory_missed = any(
        quest.get("is_mandatory") and key not in yesterday_completed
        for key, quest in QUESTS.items()
    )
    
    if yesterday_mandatory_missed:
        penalty_gold = 20
        hunter['gold'] = hunter['gold'] - penalty_gold
        st.error(f"SYSTEM PENALTY: Mandatory quest missed yesterday. -{penalty_gold} Gold.")
    
    # Reset for the new day
    hunter['last_login'] = today
    hunter['completed_daily_quests'] = []
    st.info("A new day has begun. Daily Quests have been reset!")
    save_data()

# --- UI DISPLAY ---
st.title("SOLO LEVELING: THE HUNTER'S ASCENT")
st.markdown("---")

# --- DASHBOARD (No changes) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.text_input("Hunter Name", value=hunter['name'], disabled=True)
with col2: st.metric("Rank", hunter['rank'])
with col3: st.metric("Level", hunter['level'])
with col4: st.metric("Gold (G)", hunter['gold'])

xp_percent = int((hunter['xp'] / hunter['xp_to_next_level']) * 100) if hunter['xp_to_next_level'] > 0 else 0
st.progress(xp_percent, text=f"XP: {hunter['xp']} / {hunter['xp_to_next_level']}")
st.markdown("---")

# --- STATS & STORE (MODIFIED to remove debt system from store for now) ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Hunter Stats")
    stats = hunter['stats']
    st.markdown(f"**💪 STR:** `{stats['str']}` **🧠 INT:** `{stats['intel']}` **🧘 WIL:** `{stats['wil']}` **💰 FIN:** `{stats['fin']}` **🤝 CHA:** `{stats['cha']}`")
    if hunter['skill_points'] > 0:
        st.subheader(f"Skill Points to Allocate: {hunter['skill_points']}")
        stat_to_upgrade = st.selectbox("Choose a stat to upgrade:", options=list(stats.keys()))
        if st.button("Upgrade Stat"):
            hunter['stats'][stat_to_upgrade] += 1; hunter['skill_points'] -= 1
            save_data(); st.rerun()


st.markdown("---")

# --- (MODIFIED) DAILY QUESTS with SLIDERS ---
st.header("Today's Quests")
for key, quest in QUESTS.items():
    is_completed = key in hunter['completed_daily_quests']
    
    quest_col, slider_col, button_col = st.columns([3, 2, 1])
    
    with quest_col:
        label = f"✅ {quest['name']}" if is_completed else quest['name']
        mandatory = " `(MANDATORY)`" if quest.get("is_mandatory") else ""
        st.markdown(f"**{label}**{mandatory}\n\n*Reward: +{quest['xp']} XP, +{quest['gold']} G*")

    if not is_completed:
        with slider_col:
            percentage = st.slider("Completion %", 0, 100, 0, key=f"slider_{key}", label_visibility="collapsed")
        with button_col:
            if st.button("Log Progress", key=key, use_container_width=True):
                if percentage > 0:
                    xp_gained = int(quest['xp'] * (percentage / 100))
                    gold_gained = int(quest['gold'] * (percentage / 100))
                    
                    hunter['xp'] += xp_gained
                    hunter['gold'] += gold_gained
                    
                    # Update stats based on percentage completion
                    stat, points = quest['stat_bonus']
                    stat_gained = int(points * (percentage / 100))
                    if stat_gained > 0:
                         hunter['stats'][stat] += stat_gained
                    
                    hunter['completed_daily_quests'].append(key)
                    st.success(f"Logged {percentage}% for '{quest['name']}'. +{xp_gained} XP, +{gold_gained} G.")
                    
                    # Level Up Check
                    if hunter['xp'] >= hunter['xp_to_next_level']:
                        hunter['level'] += 1
                        hunter['xp'] -= hunter['xp_to_next_level']
                        hunter['xp_to_next_level'] = int(BASE_XP * (hunter['level'] ** XP_MULTIPLIER))
                        hunter['skill_points'] += 5
                        st.balloons(); st.success(f"LEVEL UP! You are now Level {hunter['level']}!")
                    
                    save_data()
                    st.rerun()
    st.markdown("---")

