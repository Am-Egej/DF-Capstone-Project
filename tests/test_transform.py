import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.transform import clean_data

def test_grand_slam_tagging():
    sample = pd.DataFrame({
        'tournament': ['Wimbledon', 'US Open', 'ATP 250'],
        'Date': ['2023-07-01', '2023-09-01', '2023-06-01']
    })

    result = clean_data(sample)
    assert result['is_grand_slam'].sum() == 2
