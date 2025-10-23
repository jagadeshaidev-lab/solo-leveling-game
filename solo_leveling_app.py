# --- SOLO LEVELING SYSTEM V3.0 (with Firebase DB) ---
import streamlit as st
import json
import os
from datetime import date
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIG (No Changes) ---
BASE_XP = 1000
XP_MULTIPLIER = 1.5
QUESTS = {
    "server_check": {"name": "Morning Watchtower Scan (Servers)", "xp": 20, "gold": 2, "stat_bonus": ("wil", 1)},
    "tickets": {"name": "Slaying the Assigned Beasts (Tickets)", "xp": 100, "gold": 10, "stat_bonus": ("intel", 1)},
    "standup": {"name": "Evening War Council (Stand-up)", "xp": 30, "gold": 3, "stat_bonus": ("cha", 1)},
    "gym": {"name": "The Iron Temple Ritual", "xp": 150, "gold": 15, "stat_bonus": ("str", 1)},
    "ai": {"name": "The Sorcerer's Scroll (AI Course)", "xp": 200, "gold": 20, "stat_bonus": ("intel", 2), "is_mandatory": True},
    "finance": {"name": "The Gold Guardian's Broadcast", "xp": 50, "gold": 5, "stat_bonus": ("fin", 1)},
    "love": {"name": "The Alliance Call", "xp": 40, "gold": 4, "stat_bonus": ("cha", 1)},
    "read": {"name": "The Oracle's Wisdom", "xp": 30, "gold": 3, "stat_bonus": ("intel", 1)}
}
STORE_ITEMS = {
    "insta": {"name": "15 Mins Insta Scroll", "cost": 15},
    "tv": {"name": "1 Episode of a TV Show", "cost": 30},
    "junk": {"name": "Order Junk Food (Cheat Meal)", "cost": 100},
    "yt": {"name": "30 Mins YouTube Binge", "cost": 25}
}

# --- FIREBASE DATABASE FUNCTIONS (NEW) ---
def initialize_firebase():
    """Initializes the Firebase app, using Streamlit secrets for credentials."""
    if not firebase_admin._apps:
        # Load credentials from st.secrets
        creds_dict = dict(st.secrets["firebase_credentials"])
        creds = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(creds)
    return firestore.client()

def save_data():
    """Saves the hunter's state to Firestore."""
    if 'hunter' in st.session_state:
        db = initialize_firebase()
        doc_ref = db.collection('hunters').document(st.session_state.hunter['name'])
        doc_ref.set(st.session_state.hunter)

def load_data(hunter_name="Hunter"):
    """Loads the hunter's state from Firestore."""
    db = initialize_firebase()
    doc_ref = db.collection('hunters').document(hunter_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

# --- STATE INITIALIZATION (MODIFIED) ---
def initialize_state():
    """Initializes the session state, loading data from Firestore if it exists."""
    if 'hunter' not in st.session_state:
        # For simplicity, we'll use a default name to load. 
        # A login screen could be added later to support multiple users.
        saved_data = load_data("Hunter") 
        if saved_data:
            st.session_state.hunter = saved_data
        else:
            st.session_state.hunter = {
                "name": "Hunter", "rank": "E-Rank", "level": 1, "xp": 0,
                "xp_to_next_level": int(BASE_XP), "gold": 0, "skill_points": 0,
                "stats": {"str": 5, "intel": 5, "wil": 5, "fin": 5, "cha": 5},
                "last_login": "2000-01-01", 
                "completed_daily_quests": [],
                "daily_bonus_claimed": False
            }

# --- Initialize Firebase and App State ---
st.set_page_config(page_title="Solo Leveling System", layout="wide")
db = initialize_firebase()
initialize_state()
hunter = st.session_state.hunter

# --- DAILY RESET & PENALTY LOGIC (No changes here, it's perfect) ---
today = date.today().isoformat()
if hunter['last_login'] < today:
    yesterday_mandatory_missed = any(
        quest.get("is_mandatory") and key not in hunter.get('completed_daily_quests', [])
        for key, quest in QUESTS.items()
    )
    if yesterday_mandatory_missed:
        penalty_gold = 20
        hunter['gold'] = max(0, hunter['gold'] - penalty_gold)
        st.error(f"SYSTEM PENALTY: Mandatory quest missed yesterday. -{penalty_gold} Gold.")
    hunter['last_login'] = today
    hunter['completed_daily_quests'] = []
    hunter['daily_bonus_claimed'] = False
    st.info("A new day has begun. Daily Quests have been reset!")
    save_data()

# --- UI (The rest of your UI code has no major changes, just calls save_data()) ---
st.title("SOLO LEVELING: THE HUNTER'S ASCENT")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    # We will keep hunter name constant for now to use as DB document ID
    st.text_input("Hunter Name", value=hunter['name'], disabled=True)
with col2: st.metric("Rank", hunter['rank'])
with col3: st.metric("Level", hunter['level'])
with col4: st.metric("Gold (G)", hunter['gold'])

xp_percent = int((hunter['xp'] / hunter['xp_to_next_level']) * 100) if hunter['xp_to_next_level'] > 0 else 0
st.progress(xp_percent, text=f"XP: {hunter['xp']} / {hunter['xp_to_next_level']}")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Hunter Stats")
    stats = hunter['stats']
    st.markdown(f"**💪 STR:** `{stats['str']}` **🧠 INT:** `{stats['intel']}` **🧘 WIL:** `{stats['wil']}` **💰 FIN:** `{stats['fin']}` **🤝 CHA:** `{stats['cha']}`")
    if hunter['skill_points'] > 0:
        st.subheader(f"Skill Points to Allocate: {hunter['skill_points']}")
        stat_to_upgrade = st.selectbox("Choose a stat to upgrade:", options=list(stats.keys()))
        if st.button("Upgrade Stat"):
            hunter['stats'][stat_to_upgrade] += 1
            hunter['skill_points'] -= 1
            save_data(); st.rerun()

with col2:
    st.subheader("System Store")
    for key, item in STORE_ITEMS.items():
        if st.button(f"Buy '{item['name']}' ({item['cost']} G)", key=f"buy_{key}"):
            if hunter['gold'] >= item['cost']:
                hunter['gold'] -= item['cost']
                st.success(f"Purchased '{item['name']}'!")
                save_data(); st.rerun()
            else:
                st.error("Not enough Gold!")
st.markdown("---")

st.header("Daily Quests")
for key, quest in QUESTS.items():
    is_completed = key in hunter['completed_daily_quests']
    quest_col, button_col = st.columns([4, 1])
    with quest_col:
        label = f"~~{quest['name']}~~" if is_completed else quest['name']
        mandatory = " `(MANDATORY)`" if quest.get("is_mandatory") else ""
        st.markdown(f"**{label}**{mandatory}\n\n*Reward: +{quest['xp']} XP, +{quest['gold']} G*")
    with button_col:
        if is_completed:
            if st.button("Undo ↩️", key=f"undo_{key}", use_container_width=True):
                hunter['xp'] -= quest['xp']; hunter['gold'] -= quest['gold']
                stat, points = quest['stat_bonus']; hunter['stats'][stat] -= points
                hunter['completed_daily_quests'].remove(key)
                st.warning(f"Reversed '{quest['name']}'.")
                save_data(); st.rerun()
        else:
            if st.button("Complete ✔️", key=key, use_container_width=True):
                hunter['xp'] += quest['xp']; hunter['gold'] += quest['gold']
                stat, points = quest['stat_bonus']; hunter['stats'][stat] += points
                hunter['completed_daily_quests'].append(key)
                st.success(f"Quest '{quest['name']}' completed!")
                if hunter['xp'] >= hunter['xp_to_next_level']:
                    hunter['level'] += 1
                    hunter['xp'] -= hunter['xp_to_next_level']
                    hunter['xp_to_next_level'] = int(BASE_XP * (hunter['level'] ** XP_MULTIPLIER))
                    hunter['skill_points'] += 5
                    st.balloons(); st.success(f"LEVEL UP! You are now Level {hunter['level']}!")
                save_data(); st.rerun()
    st.markdown("---")

all_quests_done = all(key in hunter['completed_daily_quests'] for key in QUESTS.keys())
if all_quests_done and not hunter.get('daily_bonus_claimed'):
    bonus_xp, bonus_gold = 100, 25
    hunter['xp'] += bonus_xp; hunter['gold'] += bonus_gold
    hunter['daily_bonus_claimed'] = True
    st.subheader("🏆 PERFECT DAY! 🏆"); st.success(f"Bonus: +{bonus_xp} XP, +{bonus_gold} G!")
    st.balloons(); save_data()

with st.expander("Manual Entry / Partial Quest"):
    manual_desc = st.text_input("Task Description"); manual_xp = st.number_input("XP Gained", 0, step=10)
    manual_gold = st.number_input("Gold Gained", 0, step=1)
    if st.button("Add Custom XP"):
        if manual_xp > 0 or manual_gold > 0:
            hunter['xp'] += manual_xp; hunter['gold'] += manual_gold
            st.success(f"Manually added '{manual_desc}'! +{manual_xp} XP, +{manual_gold} G.")
            save_data(); st.rerun()