import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.extract import fetch_and_save_dataset

def test_count_csv():
    # There should only be 1 csv file saved.
    found_csv = fetch_and_save_dataset()
    should_be = 1
    assert found_csv == should_be, f"Expected {should_be} csv, but found {found_csv}."

