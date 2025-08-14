import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.transform import transform_data

def test_grand_slam_tagging():
    sample = pd.DataFrame({
        'Tournament': ['Wimbledon', 'US Open', 'ATP 250'],
        'Date': ['2023-07-01', '2023-09-01', '2023-06-01']
    })

    result = transform_data(sample, save_it=False)
    grand_slams = result['is_grand_slam'].sum()
    should_be = 2
    assert grand_slams == should_be, f"Expected {should_be} grand slams, but found {grand_slams}."
