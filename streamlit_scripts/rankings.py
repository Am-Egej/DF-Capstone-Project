import streamlit as st
import pandas as pd
import altair as alt

def rankings(df):
    # Display grouped bar chart
    st.title("Top 10 Players with Most Wins by Surface")

    # Multiselect for surface
    surface_options = sorted(df['surface'].dropna().unique())
    selected_surfaces = st.multiselect(
        "Select Surface(s)", 
        options=surface_options, 
        default=surface_options
    )

    # Multiselect for source
    source_options = sorted(df['source'].dropna().unique())
    selected_sources = st.multiselect(
        "Select Tour(s)", 
        options=source_options, 
        default=source_options
    )

    # Filter by both surface and source
    filtered_df = df[
        df['surface'].isin(selected_surfaces) & 
        df['source'].isin(selected_sources)
    ]

    # Count wins per player per surface
    wins_by_surface = (
        filtered_df.groupby(['winner', 'surface', 'source'])
        .size()
        .reset_index(name='wins')
    )

    # Get top N players by total wins
    top_n = st.slider("Number of Top Players to Display", min_value=1, max_value=50, value=10)
    top_players = (
        wins_by_surface.groupby('winner')['wins']
        .sum()
        .nlargest(top_n)
        .index
    )

    # Filter to top players only
    wins_by_surface = wins_by_surface[wins_by_surface['winner'].isin(top_players)]

    # Sort players by total wins for consistent chart order
    player_order = (
        wins_by_surface.groupby('winner')['wins']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    # Altair grouped bar chart
    chart = alt.Chart(wins_by_surface).mark_bar().encode(
        x=alt.X('winner:N', sort=player_order, title='Player'),
        y=alt.Y('wins:Q', title='Number of Wins'),
        color=alt.Color('surface:N', title='Surface'),
        tooltip=['winner', 'surface', 'wins']
    ).properties(
        title='Wins by Surface for Each Player',
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # Show pivoted table for reference
    pivot_df = wins_by_surface.pivot_table(
        index=['winner', 'source'],
        columns='surface',
        values='wins',
        fill_value=0
    ).reset_index()

    pivot_df.columns = ['player', 'source'] + [f"{col} wins" for col in pivot_df.columns[2:]]
    pivot_df['total (selected surfaces)'] = pivot_df.iloc[:, 2:].sum(axis=1)
    pivot_df = pivot_df.sort_values('total (selected surfaces)', ascending=False).head(top_n)

    pivot_df = pivot_df.reset_index(drop=True)
    pivot_df.index = pivot_df.index + 1

    pivot_df.columns = pivot_df.columns.str.replace('_', ' ').str.title()

    st.dataframe(pivot_df)

if __name__ == "__main__":
    # Read PostgreSQL to csv
    df = pd.read_csv('data/postgreSQL_tennis_data.csv', parse_dates=['date'], low_memory=False)

    # Convert all column names to lowercase
    df.columns = df.columns.str.lower()

    # Display rankings
    rankings(df)
