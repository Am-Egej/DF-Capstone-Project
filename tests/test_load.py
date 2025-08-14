import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.config import DB_CONFIG
#from scripts.load import load_to_postgres

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
    table_name = "mystic_manuscript.atp_tennis_matches"
    expected_row_count = 5  # Replace later, test 5 for now
    actual_row_count = get_row_count(table_name)
    assert actual_row_count == expected_row_count, (
        f"Expected {expected_row_count} rows, but found {actual_row_count}."
    )
