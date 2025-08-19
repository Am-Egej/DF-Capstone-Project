import streamlit as st
import pandas as pd
#import plotly.express as px
#import plotly.graph_objects as go
import altair as alt

# Set page configuration
st.set_page_config(page_title="Tennis Dashboard", layout="wide")

# Create tabs
tabs = st.tabs(["🏠 Welcome", "📊 Rankings", "🎾 Player Profile", "⚔️ Compare Players"])

df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)

# Welcome Tab
with tabs[0]:
    st.title("Welcome to the Tennis Stats Dashboard")
    st.markdown("""
    This app helps you explore proffessional tennis matches from 2020 2024.  
    The data will be updated on the 31st of December every year; the next update will be on 31/12/2025.  
    Use the tabs above to navigate through the features.  
    """)

# Rankings Tab
with tabs[1]:
    # Display grouped bar chart
    st.title("Top 10 Players with Most Wins by Surface")

    # Multiselect for Source
    source_options = sorted(df['Source'].dropna().unique())
    selected_sources = st.multiselect(
        "Select Tour(s)", 
        options=source_options, 
        default=source_options
    )

    # Multiselect for Surface
    surface_options = sorted(df['Surface'].dropna().unique())
    selected_surfaces = st.multiselect(
        "Select Surface(s)", 
        options=surface_options, 
        default=surface_options
    )

    # Filter by both Surface and Source
    filtered_df = df[
        df['Surface'].isin(selected_surfaces) & 
        df['Source'].isin(selected_sources)
    ]

    # Count wins per player per surface
    wins_by_surface = (
        filtered_df.groupby(['Winner', 'Surface', 'Source'])
        .size()
        .reset_index(name='Wins')
    )

    # Get top N players by total wins
    top_n = st.slider("Number of Top Players to Display", min_value=1, max_value=50, value=10)
    top_players = (
        wins_by_surface.groupby('Winner')['Wins']
        .sum()
        .nlargest(top_n)
        .index
    )

    # Filter to top players only
    wins_by_surface = wins_by_surface[wins_by_surface['Winner'].isin(top_players)]

    # Sort players by total wins for consistent chart order
    player_order = (
        wins_by_surface.groupby('Winner')['Wins']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    # Altair grouped bar chart
    chart = alt.Chart(wins_by_surface).mark_bar().encode(
        x=alt.X('Winner:N', sort=player_order, title='Player'),
        y=alt.Y('Wins:Q', title='Number of Wins'),
        color=alt.Color('Surface:N', title='Surface'),
        tooltip=['Winner', 'Surface', 'Wins']
    ).properties(
        title='Wins by Surface for Each Player',
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # Show pivoted table for reference
    pivot_df = wins_by_surface.pivot_table(
        index=['Winner', 'Source'],
        columns='Surface',
        values='Wins',
        fill_value=0
    ).reset_index()


    pivot_df.columns = ['Player', 'Source'] + [f"{col} Wins" for col in pivot_df.columns[2:]]
    pivot_df['Total (Selected surfaces)'] = pivot_df.iloc[:, 2:].sum(axis=1)
    pivot_df = pivot_df.sort_values('Total (Selected surfaces)', ascending=False).head(top_n)

    pivot_df = pivot_df.reset_index(drop=True)
    pivot_df.index = pivot_df.index + 1

    #st.dataframe(pivot_df, hide_index=True)
    st.dataframe(pivot_df)





# Player Profile Tab
with tabs[2]:
    st.header("Player Profile")

    players = {player for col in ["Player_1", "Player_2"] for player in df[col] if pd.notna(player)}
    sorted_players = sorted(players)

    selected_player = st.selectbox(
        "Select Player", 
        options=sorted_players, 
    )

    # Ensure 'year' column exists
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    player_df = df[(df["Player_1"] == selected_player) | (df["Player_2"] == selected_player)]

    st.title(f"Metrics - {selected_player}:")

    matches_played = len(player_df)
    years_active = player_df['Year'].nunique()

    st.metric("Matches Played", matches_played)
    st.metric("Years Active", years_active)

    wins = len(player_df[player_df["Winner"] == selected_player])
    losses = matches_played - wins

    st.metric("Wins", wins)
    st.metric("Losses", losses)

    st.title(f"Wins per year - Selected player:")
    wins_per_year = player_df[player_df["Winner"] == selected_player].groupby("Year").size()
    st.line_chart(wins_per_year)

    st.title(f"Top opponents - {selected_player}:")
    opponents = player_df.apply(
        lambda row: row["Player_2"] if row["Player_1"] == selected_player else row["Player_1"], axis=1
    )
    opponent_counts = opponents.value_counts().head(5)

    st.bar_chart(opponent_counts)

    player_df["Player"] = player_df.apply(
        lambda row: selected_player if selected_player in [row["Player_1"], row["Player_2"]] else None,
        axis=1
    )

    player_df["Rank"] = player_df.apply(
        lambda row: row["Rank_1"] if row["Player_1"] == selected_player else (
            row["Rank_2"] if row["Player_2"] == selected_player else None
        ),
        axis=1
    )

    highest_rank = player_df["Rank"].min()
    st.metric("Highest Rank Achieved", int(highest_rank))

    st.title(f"Rank over time - {selected_player}:")
    player_df["Date"] = pd.to_datetime(player_df["Date"])
    rank_over_time = player_df.sort_values("Date")[["Date", "Rank"]]
    st.line_chart(rank_over_time.set_index("Date"))



    # Highest round played per year
    # Define round hierarchy
    round_order = ['1St Round', '2Nd Round', '3Rd Round', '4Th Round', 
                'Round Robin', 'Quarterfinals', 'Semifinals', 'The Final']

    round_map = {round_name: i for i, round_name in enumerate(round_order)}
    player_df["Round_Num"] = player_df["Round"].map(round_map)

    max_round_num = player_df["Round_Num"].max()
    highest_round = [k for k, v in round_map.items() if v == max_round_num][0]
    st.metric("Highest Round Reached", highest_round)

    metrics_df = pd.DataFrame({
        "Metric": [
            "Highest Rank Achieved",
            "Highest Round Reached",
            "Active years (range = 2020 - 2024)",
            "First Year Played",
            "Last Year Played",
            "Total Matches Played",
            "Total matches Won",
            "Total matches Lost",
            "Win %",
        ],
        "Value": [
            int(highest_rank),
            highest_round,
            years_active,
            player_df["Year"].min(),
            player_df["Year"].max(),
            matches_played,
            wins,
            losses,
            f"{round(int(wins)/int(matches_played), 4)*100}%",
        ]
    })
    
    st.dataframe(metrics_df)



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
