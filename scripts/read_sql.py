import psycopg2
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.config import DB_CONFIG

def read_from_postgreSQL(table_name):
    """Helper function to read data from in a PostgreSQL table."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                query = f"SELECT COUNT(*) FROM {table_name};"
                cur.execute(query)
                return cur.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Database error while reading data from '{table_name}': {e}")
        raise


if __name__ == "__main__":
    test = read_from_postgreSQL()
    print(test)