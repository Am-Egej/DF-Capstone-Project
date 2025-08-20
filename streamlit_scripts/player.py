import streamlit as st
import pandas as pd
import altair as alt


def player(df):
    # Title
    st.header("👤🎾 Tennis Player Profile")

    # Extract unique player names
    players = {player for col in ["Player_1", "Player_2"] for player in df[col] if pd.notna(player)}
    sorted_players = sorted(players)

    # Player selection
    # Set default only if present
    default_player = "GAUFF C." if "GAUFF C." in sorted_players else sorted_players[0]

    # Create selectbox
    selected_player = st.selectbox("👤 Select a Player", options=sorted_players, index=sorted_players.index(default_player))

    # Create 'Year' column
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year

    # Filter matches involving selected player
    player_df = df[(df["Player_1"] == selected_player) | (df["Player_2"] == selected_player)]

    # Basic Stats
    matches_played = len(player_df)
    years_active = player_df["Year"].nunique()
    wins = len(player_df[player_df["Winner"] == selected_player])
    losses = matches_played - wins
    win_pct = round((wins / matches_played) * 100, 1)

    # Rank Extraction
    player_df["Rank"] = player_df.apply(
        lambda row: row["Rank_1"] if row["Player_1"] == selected_player else (
            row["Rank_2"] if row["Player_2"] == selected_player else None
        ),
        axis=1
    )
    highest_rank = int(player_df["Rank"].min())

    # Round Analysis
    round_order = ['1St Round', '2Nd Round', '3Rd Round', '4Th Round', 
                   'Round Robin', 'Quarterfinals', 'Semifinals', 'The Final']
    round_order = [r.upper() for r in round_order]

    round_map = {round_name: i for i, round_name in enumerate(round_order)}
    player_df["Round_Num"] = player_df["Round"].map(round_map)

    max_round_num = player_df["Round_Num"].max()
    highest_round = [k for k, v in round_map.items() if v == max_round_num][0]

    # Display Metrics
    st.subheader(f"⚡ Performance Metrics - {selected_player}")

    # First row:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Years Active", years_active)
    col2.metric("Matches Played", matches_played)
    col3.metric("Highest Rank Achieved", highest_rank)
    col4.metric("Highest Round Reached", highest_round)

    # Second Row:
    col1.metric("Wins", wins)
    col2.metric("Losses", losses)
    col3.metric("Win %", f"{win_pct}%")
    

    # Rank Over Time
    st.subheader(f"📈 Rank Over Time - {selected_player}")

    # Prepare data
    rank_over_time = player_df.sort_values("Date")[["Date", "Rank"]].dropna()
    rank_over_time["Month"] = rank_over_time["Date"].dt.strftime("%b-%y")

    # Build chart 
    chart = alt.Chart(rank_over_time).mark_line(interpolate='monotone', point=True).encode(
        x=alt.X("Month:N", title="Month", sort=None),
        y=alt.Y("Rank:Q", title="Rank"),
        tooltip=["Month", "Rank"]
    ).properties(
        title="📈 Rank Over Time",
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # See recent matches
    st.subheader(f"🥎 Recent matches - {selected_player}")

    # Data preparation
    player_df["Date OG"] = player_df["Date"].copy()
    player_df["Date"] = player_df["Date"].dt.date
    player_df["Player"] = df["Player_2"].where(df["Player_1"] != selected_player, df["Player_1"])
    player_df["Player Rank"] = df["Rank_2"].where(df["Player_1"] != selected_player, df["Rank_1"])
    player_df["Opponent"] = df["Player_2"].where(df["Player_1"] == selected_player, df["Player_1"]) 
    player_df["Opponent Rank"] = df["Rank_2"].where(df["Player_1"] == selected_player, df["Rank_1"]) 
    
    cols_to_see = ["Tournament", "Date", 
                   "Surface", "Round", 
                   "Best of", 
                   "Player", "Player Rank",
                   "Opponent", "Opponent Rank",
                   "Winner", 
                   "Set_Scores"
                   ]
    st.dataframe(player_df[cols_to_see].sort_values(by="Date", ascending=False), hide_index=True)


    # Wins Per Year
    st.subheader(f"🏆 Wins Per Year - {selected_player}")

    # Prepare data
    wins_per_year = (
        player_df[player_df["Winner"] == selected_player]
        .groupby("Year")
        .size()
        .reset_index(name="Wins")
    )

    # Build smooth line chart
    chart = alt.Chart(wins_per_year).mark_line(interpolate='monotone', point=True).encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Wins:Q", title="Wins"),
        tooltip=["Year", "Wins"]
    ).properties(
        title="🏆 Wins Per Year",
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # Top Opponents
    st.subheader(f"👥 Most Frequently faced opponent(s) (2020 - 2024) - {selected_player}")

    # Prepare data
    top_opponents = player_df["Opponent"].value_counts().head(5).reset_index()
    top_opponents.columns = ["Opponent", "Matches"]

    # Build Altair chart
    chart = alt.Chart(top_opponents).mark_bar().encode(
        x=alt.X("Opponent", sort="-y"),  # Sort by match count descending
        y="Matches",
        tooltip=["Opponent", "Matches"]
    ).properties(
        title="Top 5 Most Frequent Opponents",
        width=600,
        height=400
    )

    # Display in Streamlit
    st.altair_chart(chart, use_container_width=True)


        


       


if __name__ == "__main__":
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    player(df)