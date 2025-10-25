# --- Solo_Leveling_System.py (The Main Dashboard Page) ---

import streamlit as st
# Import all necessary components from our new core system!
from core_system import QUESTS, initialize_firebase, daily_reset_and_check, save_data, check_for_level_up

# --- APP SETUP ---
st.set_page_config(page_title="Solo Leveling System", layout="wide")
initialize_firebase() # Initialize Firebase connection
daily_reset_and_check() # Run daily login/reset logic

hunter = st.session_state.hunter

# --- UI DISPLAY: DASHBOARD ---
st.title("SOLO LEVELING: THE HUNTER'S ASCENT")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.text_input("Hunter Name", value=hunter['name'], disabled=True)
with col2: st.metric("Rank", hunter['rank'])
with col3: st.metric("Level", hunter['level'])
with col4: st.metric("Gold (G)", hunter['gold'])

xp_percent = int((hunter['xp'] / hunter['xp_to_next_level']) * 100) if hunter['xp_to_next_level'] > 0 else 0
st.progress(xp_percent, text=f"XP: {hunter['xp']} / {hunter['xp_to_next_level']}")
st.markdown("---")

# --- STATS & UPGRADE ---
def get_wil_status(wil):
    if wil >= 7:
        return "👑 Elite Discipline"
    elif wil >= 5:
        return "💪 Focused"
    else:
        return "😩 Temptation ↑"

col1, col2 = st.columns(2)
with col1:
    st.subheader("Hunter Stats")
    stats = hunter['stats']
    
# --- STATS & UPGRADE ---
def get_wil_status(wil):
    if wil >= 7:
        return "👑 Elite Discipline"
    elif wil >= 5:
        return "💪 Focused"
    else:
        return "😩 Temptation ↑"

col1, col2 = st.columns(2)
with col1:
    st.subheader("Hunter Stats")
    stats = hunter['stats']
    
    # NEW STAT DISPLAY with WIL Status
    wil_status = get_wil_status(stats['wil'])
    st.markdown(f"**💪 STR:** `{stats['str']}` **🧠 INT:** `{stats['intel']}` **💰 FIN:** `{stats['fin']}` **🤝 CHA:** `{stats['cha']}`")
    st.markdown(f"**🧘 WIL:** `{stats['wil']}` — **Status:** **{wil_status}**")
    
    if hunter['skill_points'] > 0:
        st.subheader(f"Skill Points to Allocate: {hunter['skill_points']}")
        stat_to_upgrade = st.selectbox("Choose a stat to upgrade:", options=list(stats.keys()))
        if st.button("Upgrade Stat"):
            hunter['stats'][stat_to_upgrade] += 1
            hunter['skill_points'] -= 1
            save_data()
            st.rerun()

st.markdown("---")

# --- DAILY QUESTS with TAB/BUTTON CHOICES ---
st.header("Today's Quests")

# Define the fixed percentage options
PERCENTAGE_OPTIONS = [0, 30, 50, 70, 100]

for key, quest in QUESTS.items():
    is_completed = key in hunter['completed_daily_quests']
    
    quest_col, radio_col, button_col = st.columns([3, 2, 1])
    
    with quest_col:
        # State to hold the current selected percentage
        percentage_key = f"selected_percent_{key}"
        if percentage_key not in st.session_state:
            st.session_state[percentage_key] = 0

        label = f"✅ {quest['name']}" if is_completed else quest['name']
        mandatory = " `(MANDATORY)`" if quest.get("is_mandatory") else ""
        st.markdown(f"**{label}**{mandatory}\n\n*Reward: +{quest['xp']} XP, +{quest['gold']} G*")

    if not is_completed:
        with radio_col:
            # Use st.radio for the tab/button feel (horizontal layout)
            st.session_state[percentage_key] = st.radio(
                "Completion %",
                options=PERCENTAGE_OPTIONS,
                index=0, # Start at 0%
                horizontal=True, # Makes it look like small tabs/buttons
                key=f"radio_{key}", 
                label_visibility="collapsed"
            )

        with button_col:
            percentage = st.session_state[percentage_key]
            
            # The Log button is only enabled if the selected percentage is > 0
            if st.button("Log Progress", key=key, use_container_width=True, disabled=(percentage == 0)):
                
                xp_gained = int(quest['xp'] * (percentage / 100))
                gold_gained = int(quest['gold'] * (percentage / 100))
                
                hunter['xp'] += xp_gained
                hunter['gold'] += gold_gained
                
                # Update stats
                stat, points = quest['stat_bonus']
                stat_gained = int(points * (percentage / 100))
                if stat_gained > 0:
                    hunter['stats'][stat] += stat_gained
                    
                # Mark as completed (even partial completion logs the effort)
                hunter['completed_daily_quests'].append(key)
                st.success(f"Logged {percentage}% for '{quest['name']}'. +{xp_gained} XP, +{gold_gained} G.")
                
                # Check for level up after gaining XP
                check_for_level_up() # This function handles level up and saves data
                
                save_data()
                st.rerun()
                
    st.markdown("---")