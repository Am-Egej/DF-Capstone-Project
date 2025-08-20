import psycopg2
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.config import DB_CONFIG


def extract_from_postgreSQL(table_name="tennis_matches"):
    """Reads all data from a PostgreSQL table and returns it as a pandas DataFrame."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            query = f"SELECT * FROM {table_name};"
            df = pd.read_sql_query(query, conn)
            df.to_csv('data/PostgreSQL_tennis_data.csv', index=False)
            return df
    except psycopg2.Error as e:
        print(f"Database error while reading data from '{table_name}': {e}")
        raise



if __name__ == "__main__":
    data = extract_from_postgreSQL()