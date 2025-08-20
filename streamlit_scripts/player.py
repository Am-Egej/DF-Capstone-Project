import streamlit as st
import pandas as pd
import altair as alt

def player(df):
    # Title
    st.header("👤🎾 Tennis Player Profile")

    # Extract unique player names
    players = {player for col in ["player_1", "player_2"] for player in df[col] if pd.notna(player)}
    sorted_players = sorted(players)

    # Player selection
    default_player = "GAUFF C." if "GAUFF C." in sorted_players else sorted_players[0]
    selected_player = st.selectbox("👤 Select a Player", options=sorted_players, index=sorted_players.index(default_player))

    # Create 'year' column
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    # Filter matches involving selected player
    player_df = df[(df["player_1"] == selected_player) | (df["player_2"] == selected_player)]

    # Basic Stats
    matches_played = len(player_df)
    years_active = player_df["year"].nunique()
    wins = len(player_df[player_df["winner"] == selected_player])
    losses = matches_played - wins
    win_pct = round((wins / matches_played) * 100, 1)

    # Rank Extraction
    player_df["rank"] = player_df.apply(
        lambda row: row["rank_1"] if row["player_1"] == selected_player else (
            row["rank_2"] if row["player_2"] == selected_player else None
        ),
        axis=1
    )
    highest_rank = int(player_df["rank"].min())

    # Round Analysis
    round_order = ['1St Round', '2Nd Round', '3Rd Round', '4Th Round', 
                   'Round Robin', 'Quarterfinals', 'Semifinals', 'The Final']
    round_order = [r.upper() for r in round_order]
    round_map = {round_name: i for i, round_name in enumerate(round_order)}
    player_df["round_num"] = player_df["round"].map(round_map)

    max_round_num = player_df["round_num"].max()
    highest_round = [k for k, v in round_map.items() if v == max_round_num][0]

    # Display Metrics
    st.subheader(f"⚡ Performance Metrics - {selected_player}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Years Active", years_active)
    col2.metric("Matches Played", matches_played)
    col3.metric("Highest Rank Achieved", highest_rank)
    col4.metric("Highest Round Reached", highest_round)

    col1.metric("Wins", wins)
    col2.metric("Losses", losses)
    col3.metric("Win %", f"{win_pct}%")

    # Rank Over Time
    st.subheader(f"📈 Rank Over Time - {selected_player}")
    rank_over_time = player_df.sort_values("date")[["date", "rank"]].dropna()
    rank_over_time["month"] = rank_over_time["date"].dt.strftime("%b-%y")

    chart = alt.Chart(rank_over_time).mark_line(interpolate='monotone', point=True).encode(
        x=alt.X("month:N", title="Month", sort=None),
        y=alt.Y("rank:Q", title="Rank"),
        tooltip=["month", "rank"]
    ).properties(
        title="📈 Rank Over Time",
        width=700,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    # Recent Matches
    st.subheader(f"🥎 Recent matches - {selected_player}")
    player_df["date_og"] = player_df["date"].copy()
    player_df["date"] = player_df["date"].dt.date
    player_df["player"] = df["player_2"].where(df["player_1"] != selected_player, df["player_1"])
    player_df["player_rank"] = df["rank_2"].where(df["player_1"] != selected_player, df["rank_1"])
    player_df["opponent"] = df["player_2"].where(df["player_1"] == selected_player, df["player_1"]) 
    player_df["opponent_rank"] = df["rank_2"].where(df["player_1"] == selected_player, df["rank_1"]) 

    cols_to_see = ["tournament", "date", "surface", "round", "best_of", 
                   "player", "player_rank", "opponent", "opponent_rank", 
                   "winner", "set_scores"]
    
    display_df = player_df[cols_to_see].sort_values(by="date", ascending=False)
    display_df.columns = display_df.columns.str.replace('_', ' ').str.title()

    st.dataframe(display_df, hide_index=True)

    # Wins Per Year
    st.subheader(f"🏆 Wins Per Year - {selected_player}")
    wins_per_year = (
        player_df[player_df["winner"] == selected_player]
        .groupby("year")
        .size()
        .reset_index(name="wins")
    )

    chart = alt.Chart(wins_per_year).mark_line(interpolate='monotone', point=True).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("wins:Q", title="Wins"),
        tooltip=["year", "wins"]
    ).properties(
        title="🏆 Wins Per Year",
        width=700,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    # Top Opponents
    st.subheader(f"👥 Most Frequently faced opponent(s) (2020 - 2024) - {selected_player}")
    top_opponents = player_df["opponent"].value_counts().head(5).reset_index()
    top_opponents.columns = ["opponent", "matches"]

    chart = alt.Chart(top_opponents).mark_bar().encode(
        x=alt.X("opponent", sort="-y"),
        y="matches",
        tooltip=["opponent", "matches"]
    ).properties(
        title="Top 5 Most Frequent Opponents",
        width=600,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    # Read PostgreSQL to csv
    df = pd.read_csv('data/PostgreSQL_tennis_data.csv', parse_dates=['date'], low_memory=False)

    # Convert all column names to lowercase
    df.columns = df.columns.str.lower()

    # Player insights
    player(df)
