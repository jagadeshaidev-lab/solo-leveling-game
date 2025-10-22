# --- SOLO LEVELING SYSTEM V2.0 ---
import streamlit as st
import json
import os
from datetime import date, timedelta

# --- CONFIG & DATA ---
DATA_FILE = "hunter_data.json"  # File to store all progress
BASE_XP = 1000
XP_MULTIPLIER = 1.5

QUESTS = {
    # Work Quests
    "server_check": {"name": "Morning Watchtower Scan (Servers)", "xp": 20, "gold": 2, "stat_bonus": ("wil", 1)},
    "tickets": {"name": "Slaying the Assigned Beasts (Tickets)", "xp": 100, "gold": 10, "stat_bonus": ("intel", 1)},
    "standup": {"name": "Evening War Council (Stand-up)", "xp": 30, "gold": 3, "stat_bonus": ("cha", 1)},

    # Personal Quests
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

# --- DATA PERSISTENCE FUNCTIONS ---
def save_data():
    """Saves the hunter's state to a JSON file."""
    if 'hunter' in st.session_state:
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.hunter, f, indent=4)

def load_data():
    """Loads the hunter's state from a JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None # Handle case of empty or corrupted file
    return None

# --- STATE INITIALIZATION ---
def initialize_state():
    """Initializes the session state, loading data if it exists."""
    if 'hunter' not in st.session_state:
        saved_data = load_data()
        if saved_data:
            st.session_state.hunter = saved_data
        else:
            # First time running the app
            st.session_state.hunter = {
                "name": "Hunter", "rank": "E-Rank", "level": 1, "xp": 0,
                "xp_to_next_level": int(BASE_XP), "gold": 0, "skill_points": 0,
                "stats": {"str": 5, "intel": 5, "wil": 5, "fin": 5, "cha": 5},
                "last_login": "2000-01-01", 
                "completed_daily_quests": [],
                "daily_bonus_claimed": False
            }

# --- Initialize and Set Page Config ---
st.set_page_config(page_title="Solo Leveling System", layout="wide")
initialize_state()
hunter = st.session_state.hunter # Convenience variable

# --- DAILY RESET & PENALTY LOGIC ---
today = date.today().isoformat()
if hunter['last_login'] < today:
    # Check if mandatory quests from *yesterday* were missed
    yesterday_mandatory_missed = False
    for key, quest in QUESTS.items():
        if quest.get("is_mandatory") and key not in hunter.get('completed_daily_quests', []):
            yesterday_mandatory_missed = True
            break
    
    if yesterday_mandatory_missed:
        penalty_gold = 20
        hunter['gold'] = max(0, hunter['gold'] - penalty_gold) # Prevent negative gold
        st.error(f"SYSTEM PENALTY: Mandatory quest missed yesterday. -{penalty_gold} Gold.")

    # Reset for the new day
    hunter['last_login'] = today
    hunter['completed_daily_quests'] = []
    hunter['daily_bonus_claimed'] = False
    st.info("A new day has begun. Daily Quests have been reset!")
    save_data() # Save the reset state

# --- UI DISPLAY ---
st.title("SOLO LEVELING: THE HUNTER'S ASCENT")
st.markdown("---")

# --- DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    new_name = st.text_input("Hunter Name", value=hunter['name'])
    if new_name != hunter['name']:
        hunter['name'] = new_name
        save_data()
with col2:
    st.metric("Rank", hunter['rank'])
with col3:
    st.metric("Level", hunter['level'])
with col4:
    st.metric("Gold (G)", hunter['gold'])

xp_percent = int((hunter['xp'] / hunter['xp_to_next_level']) * 100) if hunter['xp_to_next_level'] > 0 else 0
st.progress(xp_percent, text=f"XP: {hunter['xp']} / {hunter['xp_to_next_level']}")
st.markdown("---")

# --- STATS & STORE ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Hunter Stats")
    stats = hunter['stats']
    st.markdown(f"**💪 STR (Strength):** `{stats['str']}`")
    st.markdown(f"**🧠 INT (Intelligence):** `{stats['intel']}`")
    st.markdown(f"**🧘 WIL (Willpower):** `{stats['wil']}`")
    st.markdown(f"**💰 FIN (Finance):** `{stats['fin']}`")
    st.markdown(f"**🤝 CHA (Charisma):** `{stats['cha']}`")
    
    if hunter['skill_points'] > 0:
        st.subheader(f"Skill Points to Allocate: {hunter['skill_points']}")
        stat_to_upgrade = st.selectbox("Choose a stat to upgrade:", options=list(stats.keys()))
        if st.button("Upgrade Stat"):
            hunter['stats'][stat_to_upgrade] += 1
            hunter['skill_points'] -= 1
            save_data()
            st.rerun()

with col2:
    st.subheader("System Store")
    for key, item in STORE_ITEMS.items():
        cost = item['cost']
        if st.button(f"Buy '{item['name']}' ({cost} G)", key=f"buy_{key}"):
            if hunter['gold'] >= cost:
                hunter['gold'] -= cost
                st.success(f"Purchased '{item['name']}'! Enjoy your reward, Hunter.")
                save_data()
                st.rerun()
            else:
                st.error("Not enough Gold!")
st.markdown("---")

# --- DAILY QUESTS ---
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
                hunter['xp'] -= quest['xp']
                hunter['gold'] -= quest['gold']
                stat, points = quest['stat_bonus']
                hunter['stats'][stat] -= points
                hunter['completed_daily_quests'].remove(key)
                st.warning(f"Reversed '{quest['name']}'.")
                save_data()
                st.rerun()
        else:
            if st.button("Complete ✔️", key=key, use_container_width=True):
                hunter['xp'] += quest['xp']
                hunter['gold'] += quest['gold']
                stat, points = quest['stat_bonus']
                hunter['stats'][stat] += points
                hunter['completed_daily_quests'].append(key)
                st.success(f"Quest '{quest['name']}' completed! Well done.")
                
                # Level Up Check
                if hunter['xp'] >= hunter['xp_to_next_level']:
                    hunter['level'] += 1
                    hunter['xp'] -= hunter['xp_to_next_level']
                    hunter['xp_to_next_level'] = int(BASE_XP * (hunter['level'] ** XP_MULTIPLIER))
                    hunter['skill_points'] += 5
                    st.balloons()
                    st.success(f"LEVEL UP! You are now Level {hunter['level']}!")
                
                save_data()
                st.rerun()
    st.markdown("---")

# --- DAILY COMPLETION BONUS ---
all_quests_done = all(key in hunter['completed_daily_quests'] for key in QUESTS.keys())
if all_quests_done and not hunter.get('daily_bonus_claimed'):
    bonus_xp = 100
    bonus_gold = 25
    hunter['xp'] += bonus_xp
    hunter['gold'] += bonus_gold
    hunter['daily_bonus_claimed'] = True
    st.subheader("🏆 PERFECT DAY! 🏆")
    st.success(f"All daily quests completed! Bonus: +{bonus_xp} XP, +{bonus_gold} G!")
    st.balloons()
    save_data()

# --- MANUAL ENTRY ---
st.header("Manual Entry / Partial Quest")
with st.expander("Add XP for partial or unlisted tasks"):
    manual_desc = st.text_input("Task Description (e.g., '1 hour AI course')")
    manual_xp = st.number_input("XP Gained", min_value=0, step=10)
    manual_gold = st.number_input("Gold Gained", min_value=0, step=1)
    
    if st.button("Add Custom XP"):
        if manual_xp > 0 or manual_gold > 0:
            hunter['xp'] += manual_xp
            hunter['gold'] += manual_gold
            st.success(f"Manually added '{manual_desc}'! +{manual_xp} XP, +{manual_gold} G.")
            save_data()
            st.rerun()
        else:
            st.warning("Please enter some XP or Gold to add.")
