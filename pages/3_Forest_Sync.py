# --- pages/3_Forest_Sync.py ---

import streamlit as st
import pandas as pd
from core_system import initialize_firebase, daily_reset_and_check, save_data, check_for_level_up, QUESTS

st.set_page_config(page_title="Forest Sync", layout="centered")
initialize_firebase() 
daily_reset_and_check()
hunter = st.session_state.hunter

DEEP_FOCUS_QUEST_KEY = "deep_focus_weekly"
HOURS_TARGET = 8 

st.title("Forest App Sync 🌲 (Weekly Focus Log)")
st.info(f"Log your focused hours to complete the **'{QUESTS[DEEP_FOCUS_QUEST_KEY]['name']}'** quest.")
st.markdown("---")

# --- Step 1: Manual Data Entry ---
st.subheader("1. Enter This Week's Focused Hours")

# We use a text input because the hours can be floating points (e.g., 8.5 hours)
hours_logged = st.number_input(
    "Total Focused Hours (from Forest App this week):",
    min_value=0.0,
    value=st.session_state.hunter.get('weekly_focus_hours', 0.0), # Maintain previous value
    step=0.1,
    format="%.1f"
)

# Store the value temporarily in the session state
st.session_state.hunter['weekly_focus_hours'] = hours_logged


# --- Step 2: Log Progress Button ---
st.subheader("2. Check & Log Progress")
quest = QUESTS[DEEP_FOCUS_QUEST_KEY]

if st.session_state.hunter['weekly_focus_hours'] >= HOURS_TARGET:
    
    completion_percent = min(100, int((hours_logged / HOURS_TARGET) * 100))
    st.success(f"Goal Reached! {hours_logged} hours logged. Completion: {completion_percent}%")

    if st.button("Log Weekly Focus Reward (100%)", use_container_width=True):
        
        # Calculate rewards based on 100% completion
        xp_gained = quest['xp']
        gold_gained = quest['gold']
        
        # Update stats
        stat, points = quest['stat_bonus']
        hunter['stats'][stat] += points
        
        hunter['xp'] += xp_gained
        hunter['gold'] += gold_gained
        
        st.success(f"Weekly Deep Focus Quest COMPLETED! +{xp_gained} XP, +{gold_gained} G, +{points} {stat.upper()}.")
        
        # Reset the weekly tracker to 0 for the next week
        st.session_state.hunter['weekly_focus_hours'] = 0.0
        
        # NOTE: Since this is a weekly quest, we don't add it to completed_daily_quests
        
        check_for_level_up()
        save_data()
        st.rerun()

else:
    remaining_hours = max(0, HOURS_TARGET - hours_logged)
    st.warning(f"Keep Growing! You need {remaining_hours:.1f} more hours to complete the weekly quest.")

st.markdown("---")
st.markdown("*Tip: Export your Forest log at the end of the week, sum the hours, and enter the total here!*")