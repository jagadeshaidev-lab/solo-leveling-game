# --- pages/1_Hunter_Store.py ---

import streamlit as st
# Access the tools from the core system
from core_system import STORE_ITEMS, initialize_firebase, daily_reset_and_check, save_data

st.set_page_config(page_title="Hunter Store", layout="wide")
initialize_firebase() # Connect to Firebase
daily_reset_and_check() # Ensure state is current and reset runs

hunter = st.session_state.hunter

st.title("System Store 🛒")
st.markdown("---")
st.info(f"**Current Gold (G):** `{hunter['gold']}`")

st.header("Rewards: Spend Gold for Downtime")
st.warning("⚠️ WARNING: Purchasing items reduces your Willpower (WIL) stat by 1.")

cols = st.columns(3)

for i, (key, item) in enumerate(STORE_ITEMS.items()):
    with cols[i % 3]: # Distribute items across 3 columns
        st.subheader(item['name'])
        st.markdown(f"Cost: **{item['cost']} G**")
        
        can_afford = hunter['gold'] >= item['cost']
        
        if st.button(f"Purchase '{item['name']}'", key=key, disabled=not can_afford, use_container_width=True):
            if can_afford:
                hunter['gold'] -= item['cost']
                
                # Penalty: Reduce Willpower
                hunter['stats']['wil'] = max(1, hunter['stats']['wil'] - 1)
                st.info("Your Willpower (WIL) stat decreased by 1.")
                
                st.success(f"PURCHASE SUCCESSFUL: You bought '{item['name']}'. -{item['cost']} Gold.")
                
                save_data()
                st.rerun()
            else:
                st.error("INSUFFICIENT GOLD.")