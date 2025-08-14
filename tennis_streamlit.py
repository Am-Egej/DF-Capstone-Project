import streamlit as st

# Set page config
st.set_page_config(page_title="Tennis Dashboard", layout="wide")

# Create tabs
tabs = st.tabs(["🏠 Welcome", "📊 Rankings", "🎾 Player Profile", "⚔️ Compare Players"])

# Welcome Tab
with tabs[0]:
    st.title("Welcome to the Tennis Stats Dashboard")
    st.markdown("""
    This app helps you explore player rankings, view individual profiles, and compare players head-to-head.
    
    Use the tabs above to navigate through the features.
    """)

# Rankings Tab
with tabs[1]:
    st.header("ATP Rankings")
    st.markdown("Here you can view the latest rankings.")
    # Example placeholder
    st.dataframe({"Player": ["Novak Djokovic"], "Rank": [1]})

# Player Profile Tab
with tabs[2]:
    st.header("Player Profile")
    player_name = st.text_input("Enter player name:")
    if player_name:
        st.markdown(f"Showing profile for **{player_name}**")
        # Add logic to fetch and display player stats
        st.write("🏆 Titles: 20")
        st.write("🎯 Win Rate: 85%")

# Compare Players Tab
with tabs[3]:
    st.header("Compare Players")
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.text_input("Player 1")
    with col2:
        player2 = st.text_input("Player 2")

    if player1 and player2:
        st.markdown(f"Comparing **{player1}** vs **{player2}**")
        # Add comparison logic here
        st.write("📈 Head-to-head: Player 1 leads 5–3")
