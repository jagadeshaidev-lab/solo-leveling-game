# --- pages/2_Recent_History.py (Corrected Code) ---

import streamlit as st
import pandas as pd
# Access all data and functions from the core system
# NOTE: core_system nunchi manaki kavalsinavi anni import cheskuntunnam
from core_system import initialize_firebase, daily_reset_and_check, load_history_data, QUESTS

st.set_page_config(page_title="History Log", layout="wide")
initialize_firebase() 
daily_reset_and_check()
hunter = st.session_state.hunter

st.title("Recent History Log 📜 (Performance Dashboard)")
st.markdown("---")

# Load last 30 days
history_df = load_history_data(limit=30) 

if not history_df.empty:
    
    # --- PANDAS STYLING FOR INTERACTIVE DATA ---
    def style_performance(row):
        count = row['Completed Quests Count']
        total = row['Total Quests Count']
        
        if count >= 7:
            color = 'background-color: #28a74555' # Light green
        elif count >= 4:
            color = 'background-color: #007bff55' # Light blue
        else:
            color = 'background-color: #dc354555' # Light red
            
        styles = [color if col == 'Quests (Completed/Total)' else '' for col in row.index]
        return styles

    # --- Display DataFrame of Summary Data ---
    st.subheader(f"Last {len(history_df)} Days of Activity Summary")
    
    summary_df = history_df[['Date', 'Completed Quests Count', 'Total Quests Count', 'End Level', 'End Gold']].copy()
    summary_df.columns = ['Date', 'Completed Quests Count', 'Total Quests Count', 'End Level', 'End Gold'] 
    summary_df['Quests (Completed/Total)'] = summary_df['Completed Quests Count'].astype(str) + " / " + summary_df['Total Quests Count'].astype(str)
    
    summary_df = summary_df.drop(columns=['Completed Quests Count', 'Total Quests Count'])
    
    styled_df = summary_df.style.apply(style_performance, axis=1)

    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    st.markdown("---")

    # --- Detailed Daily View (Corrected Section) ---
    st.subheader("Daily Quest Details")
    
    dates = summary_df['Date'].tolist()
    # Show the latest date first in the dropdown
    selected_date = st.selectbox("Select a Date to view details:", options=dates, index=len(dates)-1)
    
    if selected_date:
        # ---- FIX IS HERE ----
        # 1. We get the database connection from our standard function
        db = initialize_firebase()
        
        # 2. We use that 'db' to get the document
        doc_ref = db.collection('hunters').document(hunter['name']).collection('history').document(selected_date)
        doc = doc_ref.get()
        # ---- END OF FIX ----

        if doc.exists:
            day_data = doc.to_dict()
            completed_keys = set(day_data.get('completed_quests', []))
            
            st.markdown(f"#### Quests Completed on {selected_date}")
            
            # Using a loop to create a list of completed quest names
            completed_names = []
            for key in completed_keys:
                # Get quest details, if a quest is deleted it won't crash
                quest_info = QUESTS.get(key, {}) 
                quest_name = quest_info.get('name', f"Unknown Quest ({key})")
                completed_names.append(quest_name)
            
            if completed_names:
                for name in completed_names:
                    st.success(f"✅ {name}")
            else:
                st.warning("No quests were logged on this day.")

else:
    st.info("No history data found. Start completing quests on the main page to see your log!")