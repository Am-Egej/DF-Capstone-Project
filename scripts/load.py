import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.config import DB_CONFIG

def load_to_postgres():
    try:
        # Load the transformed data
        df = pd.read_csv('data/processed/transformed_atp_tennis.csv')
        df = df.head() # For testing purposes, to be deleted
        df = df.astype(object)  # Converts all columns to native Python types, to be deleted

        # Connect to PostgreSQL
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:

                # Create table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mystic_manuscript.atp_tennis_matches (
                        Tournament TEXT,
                        Date DATE,
                        Series TEXT,
                        Court TEXT,
                        Surface TEXT,
                        Round TEXT,
                        Best_of TEXT,
                        Player_1 TEXT,
                        Player_2 TEXT,
                        Winner TEXT,
                        Rank_1 TEXT,
                        Rank_2 TEXT,
                        Pts_1 TEXT,
                        Pts_2 TEXT,
                        Odd_1 TEXT,
                        Odd_2 TEXT,
                        Score TEXT,
                        is_grand_slam BOOLEAN
                    );
                """)

                # Prepare data for insertion
                records = df.to_records(index=False)
                values = [tuple(row) for row in records]

                # Insert data using batch method
                execute_values(cursor, """
                    INSERT INTO mystic_manuscript.atp_tennis_matches (
                        Tournament, Date, Series, Court, Surface, Round, Best_of,
                        Player_1, Player_2, Winner, Rank_1, Rank_2,
                        Pts_1, Pts_2, Odd_1, Odd_2, Score, is_grand_slam
                    ) VALUES %s
                """, values)

                print(f"✅ Inserted {len(values)} rows into atp_tennis_matches.")

    except Exception as e:
        print("❌ Error loading data to PostgreSQL:", str(e))

if __name__ == "__main__":
    load_to_postgres()
