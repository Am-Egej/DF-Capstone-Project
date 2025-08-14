import pandas as pd
from scripts.transform import clean_data

def test_grand_slam_tagging():
    sample = pd.DataFrame({
        'tournament': ['Wimbledon', 'US Open', 'ATP 250'],
        'date': ['2023-07-01', '2023-09-01', '2023-06-01']
    })
    sample['date'] = pd.to_datetime(sample['date'])

    result = clean_data(sample)
    assert result['is_grand_slam'].sum() == 2
