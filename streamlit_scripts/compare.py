import streamlit as st
import pandas as pd


def compare(df):
    st.header("Compare Players")

    # Select, WTA or ATP
    # Select round
    # Select players to compare
    ## Order:
    ### Who won their last game?
    ### Win rate in the selected round
    ### Rank


if __name__ == "__main__":
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    compare(df)