import streamlit as st
from datetime import date

# --- CONFIG & DATA (No changes here) ---
BASE_XP = 1000
XP_MULTIPLIER = 1.5
QUESTS = {
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

# --- Function to initialize the hunter's state ---
def initialize_state():
    if 'hunter' not in st.session_state:
        st.session_state.hunter = {
            "name": "Hunter", "rank": "E-Rank", "level": 1, "xp": 0,
            "xp_to_next_level": int(BASE_XP), "gold": 0, "skill_points": 0,
            "stats": {"str": 5, "intel": 5, "wil": 5, "fin": 5, "cha": 5},
            "last_login": "2000-01-01", "completed_daily_quests": []
        }

# --- Initialize the game ---
initialize_state()

# Daily Reset Logic
today = date.today().isoformat()
if st.session_state.hunter['last_login'] < today:
    st.session_state.hunter['last_login'] = today
    st.session_state.hunter['completed_daily_quests'] = []
    st.info("A new day has begun. Daily Quests have been reset!")

# --- UI DISPLAY ---
st.set_page_config(page_title="Solo Leveling System", layout="wide")
st.title("SOLO LEVELING: THE HUNTER'S ASCENT")
st.markdown("---")

# --- DASHBOARD ---
hunter = st.session_state.hunter
col1, col2, col3, col4 = st.columns(4)
with col1:
    hunter['name'] = st.text_input("Hunter Name", value=hunter['name'])
with col2:
    st.metric("Rank", hunter['rank'])
with col3:
    st.metric("Level", hunter['level'])
with col4:
    st.metric("Gold (G)", hunter['gold'])

xp_percent = int((hunter['xp'] / hunter['xp_to_next_level']) * 100) if hunter['xp_to_next_level'] > 0 else 0
st.progress(xp_percent, text=f"XP: {hunter['xp']} / {hunter['xp_to_next_level']}")
st.markdown("---")

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
            st.rerun() # FIXED: Changed to st.rerun()

with col2:
    st.subheader("System Store")
    for key, item in STORE_ITEMS.items():
        cost = item['cost']
        if st.button(f"Buy '{item['name']}' ({cost} G)", key=f"buy_{key}"):
            if hunter['gold'] >= cost:
                hunter['gold'] -= cost
                st.success(f"Purchased '{item['name']}'!")
                st.rerun() # FIXED: Changed to st.rerun()
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
        if st.button("Complete ✔️", key=key, disabled=is_completed, use_container_width=True):
            hunter['xp'] += quest['xp']
            hunter['gold'] += quest['gold']
            stat, points = quest['stat_bonus']
            hunter['stats'][stat] += points
            hunter['completed_daily_quests'].append(key)
            
            if hunter['xp'] >= hunter['xp_to_next_level']:
                hunter['level'] += 1
                hunter['xp'] -= hunter['xp_to_next_level']
                hunter['xp_to_next_level'] = int(BASE_XP * (hunter['level'] ** XP_MULTIPLIER))
                hunter['skill_points'] += 5
                st.balloons()
                st.success(f"LEVEL UP! You are now Level {hunter['level']}!")
            
            st.rerun() # FIXED: Changed to st.rerun()
    st.markdown("---")
