import streamlit as st

def welcome():
    st.title("Welcome to the Tennis Stats Dashboard")
    st.markdown("""
    This app helps you explore proffessional tennis matches from 2020 2024.  
    The data will be updated on the 31st of December every year; the next update will be on 31/12/2025.  
    Use the tabs above to navigate through the features.  
    """)


if __name__ == "__main__":
    welcome()