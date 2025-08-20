import streamlit as st
import pandas as pd
import altair as alt

def rankings(df):
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

    st.dataframe(pivot_df)



if __name__ == "__main__":
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    rankings(df)