import pandas as pd
import psycopg2
from config import DB_CONFIG

def load_to_postgres():
    df = pd.read_csv('data/processed/cleaned_matches.csv')
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            date DATE,
            player1 TEXT,
            player2 TEXT,
            winner TEXT,
            tournament TEXT,
            is_grand_slam BOOLEAN
        );
    """)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO matches (date, player1, player2, winner, tournament, is_grand_slam)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (row['date'], row['player1'], row['player2'], row['winner'], row['tournament'], row['is_grand_slam']))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_to_postgres()
