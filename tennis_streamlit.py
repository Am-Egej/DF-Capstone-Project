import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_scripts.welcome import welcome
from streamlit_scripts.rankings import rankings
from streamlit_scripts.player import player
from streamlit_scripts.compare import compare


# Set page configuration
st.set_page_config(page_title="Tennis Dashboard", layout="wide")

# Create tabs
tabs = st.tabs(["🏠🎾 Welcome", "📊 Leaderboard", "👤🎾 Player Profile", "⚖️ Compare Players"])

# Read PostgreSQL to csv
df = pd.read_csv('data/PostgreSQL_tennis_data.csv', parse_dates=['date'], low_memory=False)

# Convert all column names to lowercase
df.columns = df.columns.str.lower()

# Welcome Tab
with tabs[0]:
    welcome()


# Rankings Tab
with tabs[1]:
    rankings(df)


# Player Profile Tab
with tabs[2]:
    player(df)


# Compare Players Tab
with tabs[3]:
    compare(df)

    

    