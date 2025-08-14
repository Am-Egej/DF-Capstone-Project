import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.extract import fetch_and_save_dataset

def test_count_csv():
    # There should only be 1 csv file saved.
    assert fetch_and_save_dataset() == 1
