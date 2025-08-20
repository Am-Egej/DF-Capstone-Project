import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def compare(df):
    st.header("⚖️ Compare Players")

    # Tour selection
    tour_options = sorted(df['Source'].dropna().unique())
    selected_tours = st.multiselect("Choose Tour(s)", tour_options, default=tour_options)
    df = df[df["Source"].isin(selected_tours)]

    # Extract unique player names
    all_players = sorted(set(df["Player_1"].dropna()) | set(df["Player_2"].dropna()))

    # Player selection
    col1, col2 = st.columns(2)
    player_1 = col1.selectbox("Select 1st Player", all_players)
    player_2 = col2.selectbox("Select 2nd Player", all_players)

    # Preprocess date and year
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Year"] = df["Date"].dt.year

    # Round mapping
    round_order = ['1St Round', '2Nd Round', '3Rd Round', '4Th Round', 
                   'Round Robin', 'Quarterfinals', 'Semifinals', 'The Final']
    round_order = [r.upper() for r in round_order]
    round_map = {name: i for i, name in enumerate(round_order)}

    surface_options = sorted(df['Surface'].dropna().unique())

    def get_player_stats(player_name, surface_options=surface_options):
        player_df = df[(df["Player_1"] == player_name) | (df["Player_2"] == player_name)].copy()

        matches_played = len(player_df)
        years_active = player_df["Year"].nunique()
        wins = len(player_df[player_df["Winner"] == player_name])
        losses = matches_played - wins
        win_pct = round((wins / matches_played) * 100, 2) if matches_played else 0.0

        # Extract rank
        player_df["Rank"] = player_df.apply(
            lambda row: row["Rank_1"] if row["Player_1"] == player_name else row["Rank_2"],
            axis=1
        )
        highest_rank = int(player_df["Rank"].min()) if not player_df["Rank"].isna().all() else None

        # Round analysis
        player_df["Round_Num"] = player_df["Round"].map(round_map)
        max_round_num = player_df["Round_Num"].max()
        highest_round = next((k for k, v in round_map.items() if v == max_round_num), "Unknown")

        surface_results = {}
        for surface in surface_options:
            surface_df = player_df[(df["Surface"] == surface)].copy()
            surface_matches_played = len(surface_df)
            surface_wins = len(surface_df[surface_df["Winner"] == player_name])
            surface_win_frac = round((surface_wins / surface_matches_played) * 10, 2) if surface_matches_played else 0.0
            surface_results[surface] = surface_win_frac

        return pd.DataFrame({
            "Highest Rank Achieved": [highest_rank],
            "Highest Round Reached": [highest_round],
            "Active Years": [years_active],
            "First Year Played": [player_df["Year"].min()],
            "Last Year Played": [player_df["Year"].max()],
            "Matches Played": [matches_played],
            "Wins": [wins],
            "Losses": [losses],
            "Win %": [f"{win_pct:.1f}%"],
            "Clay": [surface_results.get("CLAY", 0)],
            "Grass": [surface_results.get("GRASS", 0)],
            "Hard": [surface_results.get("HARD", 0)],
        })

    # Generate stats
    stats_1 = get_player_stats(player_1)
    stats_2 = get_player_stats(player_2)

    player_1_list = [stats_1["Clay"][0], stats_1["Grass"][0], stats_1["Hard"][0], ]
    player_2_list = [stats_2["Clay"][0], stats_2["Grass"][0], stats_2["Hard"][0],]
        
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=player_1_list,
        theta=surface_options,
        fill='toself',
        name=player_1
    ))

    fig.add_trace(go.Scatterpolar(
        r=player_2_list,
        theta=surface_options,
        fill='toself',
        name=player_2
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title='Surface Performance Radar Chart'
    )

    st.plotly_chart(fig)

    # Display side-by-side
    for label in stats_1.columns:
        col1.metric(label, stats_1[label].iloc[0])
        col2.metric(label, stats_2[label].iloc[0])


if __name__ == "__main__":
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    compare(df)