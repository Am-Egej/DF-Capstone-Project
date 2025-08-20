import streamlit as st
import pandas as pd


def player(df):
    # Title
    st.header("🎾 Tennis Player Profile")

    # Extract unique player names
    players = {player for col in ["Player_1", "Player_2"] for player in df[col] if pd.notna(player)}
    sorted_players = sorted(players)

    # Player selection
    selected_player = st.selectbox("Select a Player", options=sorted_players)

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
    win_pct = round((wins / matches_played) * 100, 2)

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
    round_map = {round_name: i for i, round_name in enumerate(round_order)}
    player_df["Round_Num"] = player_df["Round"].map(round_map)

    max_round_num = player_df["Round_Num"].max()
    highest_round = [k for k, v in round_map.items() if v == max_round_num][0]

    # Display Metrics
    st.subheader(f"📈 Performance Metrics: {selected_player}")

    # First row:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matches Played", matches_played)
    col2.metric("Years Active", years_active)
    col3.metric("Wins", wins)
    col4.metric("Losses", losses)

    # Second Row:
    col1.metric("Win %", f"{win_pct}%")
    col2.metric("Highest Rank Achieved", highest_rank)
    col3.metric("Highest Round Reached", highest_round)

    # Rank Over Time
    st.subheader("📈 Rank Over Time")
    rank_over_time = player_df.sort_values("Date")[["Date", "Rank"]].dropna()
    st.line_chart(rank_over_time.set_index("Date"))

    # Top Opponents
    st.subheader("👥 Top Opponents Faced")
    opponents = player_df.apply(
        lambda row: row["Player_2"] if row["Player_1"] == selected_player else row["Player_1"], axis=1
    )
    top_opponents = opponents.value_counts().head(5)
    st.bar_chart(top_opponents)

    # Wins Per Year
    st.subheader("📈 Wins Per Year")
    wins_per_year = player_df[player_df["Winner"] == selected_player].groupby("Year").size()
    st.line_chart(wins_per_year)

    # Summary Table
    st.subheader("📋 Summary Table")
    summary_df = pd.DataFrame({
        "Metric": [
            "Highest Rank Achieved",
            "Highest Round Reached",
            "Active Years",
            "First Year Played",
            "Last Year Played",
            "Total Matches Played",
            "Total Matches Won",
            "Total Matches Lost",
            "Win %",
        ],
        "Value": [
            highest_rank,
            highest_round,
            years_active,
            player_df["Year"].min(),
            player_df["Year"].max(),
            matches_played,
            wins,
            losses,
            f"{win_pct}%",
        ]
    })
    st.dataframe(summary_df)

    st.dataframe(opponents)


if __name__ == "__main__":
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    player(df)