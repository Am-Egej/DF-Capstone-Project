import psycopg2
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.config import DB_CONFIG
from scripts.load import load_to_postgres

def get_row_count(table_name):
    """Helper function to count rows in a PostgreSQL table."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                query = f"SELECT COUNT(*) FROM {table_name};"
                cur.execute(query)
                return cur.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Database error while counting rows in '{table_name}': {e}")
        raise

def test_data_loaded_successfully():
    test_table_name = "test_tennis_matches"
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    load_to_postgres(df, limit=True, table_name= test_table_name)

    expected_row_count = 5  
    actual_row_count = get_row_count(test_table_name)
    assert actual_row_count == expected_row_count, (
        f"Expected {expected_row_count} rows, but found {actual_row_count}."
    )

def test_empty_dataframe_insertion():
    test_table_name = "test_empty_table"
    empty_df = pd.DataFrame(columns=[
        "Tournament", "Date", "Series", "Court", "Surface", "Round", "Best_of",
        "Player_1", "Player_2", "Winner", "Rank_1", "Rank_2", "Source", "Set_Scores",
        "Set1_Player1", "Set1_Player2", "Set2_Player1", "Set2_Player2",
        "Set3_Player1", "Set3_Player2", "Set4_Player1", "Set4_Player2",
        "Set5_Player1", "Set5_Player2"
    ])
    load_to_postgres(empty_df, table_name=test_table_name)
    assert get_row_count(test_table_name) == 0


