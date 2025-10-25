# --- pages/2_Recent_History.py (V5.1 with Conditional Formatting) ---

import streamlit as st
import pandas as pd
# Access all data and functions from the core system
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
    
    # ------------------------------------------------
    # --- PANDAS STYLING FOR INTERACTIVE DATA ---
    # ------------------------------------------------
    
    # Function to apply the color based on the number of completed quests
    def style_performance(row):
        count = row['Completed Quests Count']
        total = row['Total Quests Count']
        
        if count >= 7:
            # Peak Performance (Green)
            color = 'background-color: #28a74555' # Light green
        elif count >= 4:
            # Solid Effort (Blue)
            color = 'background-color: #007bff55' # Light blue
        else:
            # Missed Day (Red/Yellow)
            color = 'background-color: #dc354555' # Light red
            
        # Apply the color only to the 'Quests (Completed/Total)' column for focus
        styles = [color if col == 'Quests (Completed/Total)' else '' for col in row.index]
        return styles

    # --- Display DataFrame of Summary Data ---
    st.subheader(f"Last {len(history_df)} Days of Activity Summary")
    
    # Prepare the summary DataFrame
    summary_df = history_df[['Date', 'Completed Quests Count', 'Total Quests Count', 'End Level', 'End Gold']].copy()
    summary_df.columns = ['Date', 'Completed Quests Count', 'Total Quests Count', 'End Level', 'End Gold'] 
    summary_df['Quests (Completed/Total)'] = summary_df['Completed Quests Count'].astype(str) + " / " + summary_df['Total Quests Count'].astype(str)
    
    # Drop the redundant columns before displaying
    summary_df = summary_df.drop(columns=['Completed Quests Count', 'Total Quests Count'])
    
    # Apply the styling to the DataFrame
    styled_df = summary_df.style.apply(style_performance, axis=1)

    # Display the styled DataFrame
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- Detailed Daily View (same as V5.0) ---
    st.subheader("Daily Quest Details")
    
    dates = summary_df['Date'].tolist()
    selected_date = st.selectbox("Select a Date to view details:", dates[::-1])
    
    if selected_date:
        # Re-fetch the detailed data for the selected day from Firestore
        import firebase_admin
        from firebase_admin import firestore
        db = firebase_admin.firestore.client()

        doc = db.collection('hunters').document(hunter['name']).collection('history').document(selected_date).get()
        if doc.exists:
            day_data = doc.to_dict()
            completed_keys = set(day_data.get('completed_quests', []))
            
            st.markdown(f"#### Quests Completed on {selected_date}")
            
            completed_names = [QUESTS.get(key, {}).get('name', f"Unknown Quest ({key})") for key in completed_keys]
            
            if completed_names:
                st.success("✅ " + "\n✅ ".join(completed_names))
            else:
                st.warning("No quests were logged on this day.")

else:
    st.info("No history data found. Start completing quests on the main page to see your log!")