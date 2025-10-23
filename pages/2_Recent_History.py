# pages/2_Recent_History.py
import streamlit as st
import firebase_admin
from firebase_admin import firestore

# Check if the hunter has been initialized
if 'hunter' not in st.session_state:
    st.error("Please start from the main page first.")
    st.stop()

# Get the hunter data from the session state
hunter = st.session_state.hunter

st.set_page_config(page_title="History Log", layout="wide")
st.title("📜 The Hunter's Logbook")
st.markdown("---")

# We need the load_history function here as well
def load_history(hunter_name="Hunter", limit=7):
    # This will throw an error if firebase is not initialized.
    # We will fix this in the next iteration.
    db = firestore.client()
    history_ref = db.collection('hunters').document(hunter_name).collection('history')
    query = history_ref.order_by("__name__", direction=firestore.Query.DESCENDING).limit(limit)
    docs = query.stream()
    return {doc.id: doc.to_dict() for doc in docs}

QUESTS = {
    "server_check": {"name": "Daily System Check (Servers)"},
    "tickets": {"name": "Resolve Daily Tickets"},
    "standup": {"name": "Daily Progress Report (Stand-up)"},
    "gym": {"name": "Strength & Fitness Training (Gym)"},
    "ai": {"name": "Skill Upgrade: AI Course Study"},
    "finance": {"name": "Financial Market Study (Video)"},
    "love": {"name": "Connect with Your Partner"},
    "read": {"name": "Daily Reading / Knowledge Gain"}
}

history = load_history(hunter['name'], limit=7)
if not history:
    st.write("No history found yet. Start completing quests!")
else:
    for date_str, data in history.items():
        st.subheader(f"📅 {date_str}")
        completed_today = data.get('completed_quests', [])
        
        for quest_key, quest_details in QUESTS.items():
            if quest_key in completed_today:
                st.markdown(f"- ✅ ~~{quest_details['name']}~~")
            else:
                st.markdown(f"- ❌ {quest_details['name']}")
        st.markdown("---")