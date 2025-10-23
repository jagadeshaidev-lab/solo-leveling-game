# pages/1_Hunter_Store.py
import streamlit as st

# Check if the hunter has been initialized
if 'hunter' not in st.session_state:
    st.error("Please start from the main page first.")
    st.stop()

# Get the hunter data from the session state
hunter = st.session_state.hunter

st.set_page_config(page_title="Hunter Store", layout="wide")
st.title("🛒 Hunter's Store")
st.markdown("---")

st.info(f"Your current balance: **{hunter['gold']} G**")

# Use the STORE_ITEMS dictionary from the main app
# (We will need to define this again or import it later, for now, let's redefine)
STORE_ITEMS = {
    "insta": {"name": "15 Mins Insta Scroll", "cost": 15},
    "tv": {"name": "1 Episode of a TV Show", "cost": 30},
    "junk": {"name": "Order Junk Food (Cheat Meal)", "cost": 100},
    "yt": {"name": "30 Mins YouTube Binge", "cost": 25}
}

for key, item in STORE_ITEMS.items():
    if st.button(f"Buy '{item['name']}' ({item['cost']} G)", key=f"buy_{key}"):
        if hunter['gold'] >= item['cost']:
            hunter['gold'] -= item['cost']
            st.success(f"Purchased '{item['name']}'! Your new balance is {hunter['gold']} G.")
            # Note: We need a way to save this data. This will be our next challenge.
        else:
            st.error("Not enough Gold!")