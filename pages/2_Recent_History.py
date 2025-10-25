# --- pages/2_Recent_History.py ---

import streamlit as st
import pandas as pd
# Access all data and functions from the core system
from core_system import initialize_firebase, daily_reset_and_check, load_history_data, QUESTS

st.set_page_config(page_title="History Log", layout="wide")
initialize_firebase() # Connect
daily_reset_and_check() # Ensure state is current
hunter = st.session_state.hunter

st.title("Recent History Log 📜")
st.markdown("---")

history_df = load_history_data(limit=30) # Load last 30 days

if not history_df.empty:
    # --- Display DataFrame of Summary Data ---
    st.subheader(f"Last {len(history_df)} Days of Activity Summary")
    
    # Select only the relevant summary columns for the user
    summary_df = history_df[['Date', 'Completed Quests Count', 'End Level', 'End Gold']].copy()
    summary_df.columns = ['Date', 'Quests (Completed/Total)', 'End Level', 'End Gold'] # Rename columns for display
    summary_df['Quests (Completed/Total)'] = summary_df['Quests (Completed/Total)'].astype(str) + " / " + str(len(QUESTS))

    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- Detailed Daily View ---
    st.subheader("Daily Quest Details")
    
    # Get the dates for selection (reversed to show most recent first)
    dates = summary_df['Date'].tolist()
    selected_date = st.selectbox("Select a Date to view details:", dates[::-1])
    
    if selected_date:
        # Load the raw history data (requires a new function or reusing parts of core)
        # For simplicity, we'll use the core function with a limit of 1 and filter
        import firebase_admin
        from firebase_admin import firestore
        db = firebase_admin.firestore.client()

        doc = db.collection('hunters').document(hunter['name']).collection('history').document(selected_date).get()
        if doc.exists:
            day_data = doc.to_dict()
            completed_keys = set(day_data.get('completed_quests', []))
            
            st.markdown(f"#### Quests Completed on {selected_date}")
            
            # Display a list of completed quest names
            completed_names = [QUESTS.get(key, {}).get('name', f"Unknown Quest ({key})") for key in completed_keys]
            
            if completed_names:
                # Group all quest names that were completed
                st.success("✅ " + "\n✅ ".join(completed_names))
            else:
                st.warning("No quests were logged on this day.")

else:
    st.info("No history data found. Start completing quests on the main page to see your log!")