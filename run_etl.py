import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.extract import fetch_and_save_dataset
from scripts.transform import transform_data 
from scripts.load import load_to_postgres

if __name__ == "__main__":
    # Run data extraction
    fetch_and_save_dataset()

    # Run data transformation
    df = transform_data()

    # Run data loading to PostgreSQL
    load_to_postgres(df)