import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.config import DB_CONFIG

def load_to_postgres(df, limit=False, table_name="tennis_matches"):
    try:
        df = df.astype(object)
        df = df.where(pd.notna(df), None)

        if limit:
            df = df.head() # For testing purposes, limit to 5 rows
        
        # Connect to PostgreSQL
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                
                # Drop table if it exists
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                print(f"✅ If it already existed, the table '{table_name}' has been dropped!")

                # Create table if it doesn't exist
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        Tournament TEXT,
                        Date DATE,
                        Series TEXT,
                        Court TEXT,
                        Surface TEXT,
                        Round TEXT,
                        Best_of INT,
                        Player_1 TEXT,
                        Player_2 TEXT,
                        Winner TEXT,
                        Rank_1 INT,
                        Rank_2 INT,
                        Set_Scores TEXT,
                        Set1_Player1 INT,
                        Set1_Player2 INT,
                        Set2_Player1 INT,
                        Set2_Player2 INT,
                        Set3_Player1 INT,
                        Set3_Player2 INT,
                        Set4_Player1 INT,
                        Set4_Player2 INT,
                        Set5_Player1 INT,
                        Set5_Player2 INT
                    );
                """)

                # Prepare data for insertion
                records = df.to_records(index=False)
                values = [tuple(row) for row in records]

                # Insert data using batch method
                execute_values(cursor, f"""
                    INSERT INTO {table_name} (
                        Tournament, 
                        Date, 
                        Series, 
                        Court, 
                        Surface, 
                        Round, 
                        Best_of, 
                        Player_1, 
                        Player_2, 
                        Winner, 
                        Rank_1, 
                        Rank_2, 
                        Set_Scores, 
                        Set1_Player1, 
                        Set1_Player2, 
                        Set2_Player1, 
                        Set2_Player2, 
                        Set3_Player1, 
                        Set3_Player2, 
                        Set4_Player1, 
                        Set4_Player2, 
                        Set5_Player1, 
                        Set5_Player2
                    ) VALUES %s
                """, values)

                print(f"✅ Inserted {len(values)} rows into {table_name}.")

    except Exception as e:
        print("❌ Error loading data to PostgreSQL:", str(e))

if __name__ == "__main__":
    df = pd.read_csv('data/processed/transformed_tennis_data.csv', parse_dates=['Date'], low_memory=False)
    load_to_postgres(df)
