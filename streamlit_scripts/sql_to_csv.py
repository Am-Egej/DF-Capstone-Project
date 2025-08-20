import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def extract_from_postgreSQL(table_name="tennis_matches"):
    """Reads all data from a PostgreSQL table and returns it as a pandas DataFrame."""
    try:
        # Build connection string from secrets
        db_url = (
            f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}"
            f"@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"
            f"?options={st.secrets['DB_OPTIONS']}"
        )

        # Create SQLAlchemy engine
        engine = create_engine(db_url)

        # Read data into DataFrame
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, engine)

        # Save to CSV
        df.to_csv("data/updates/postgreSQL_tennis_data.csv", index=False)

        return df

    except SQLAlchemyError as e:
        st.error(f"Database error while reading data from '{table_name}': {e}")
        raise


if __name__ == "__main__":
    data = extract_from_postgreSQL()
    print(data.head())