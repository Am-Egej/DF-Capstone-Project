import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.transform import transform_data 
from scripts.transform import extract_set_scores

def test_extract_set_scores_valid():
    input_data = ["6-4", "3-6", "7-5"]
    result = extract_set_scores(input_data)
    actual = result.to_dict()
    expected = {
        'Set1_Player1': 6, 'Set1_Player2': 4,
        'Set2_Player1': 3, 'Set2_Player2': 6,
        'Set3_Player1': 7, 'Set3_Player2': 5,
        'Set4_Player1': None, 'Set4_Player2': None,
        'Set5_Player1': None, 'Set5_Player2': None,
    }

    for key in expected:
        a, e = actual[key], expected[key]
        if pd.isna(a) and pd.isna(e):
            continue
        assert a == e, f"Mismatch at {key}: {a} != {e}"


def test_extract_set_scores_invalid_format():
    input_data = ["6-4", "bad", "7-5"]
    result = extract_set_scores(input_data)
    assert pd.isna(result["Set2_Player1"])
    assert pd.isna(result["Set2_Player2"])


def test_extract_set_scores_empty():
    result = extract_set_scores([])
    for i in range(1, 6):
        assert pd.isna(result[f"Set{i}_Player1"])
        assert pd.isna(result[f"Set{i}_Player2"])


def test_transform_data_with_mocked_csvs():
    # Create mock DataFrames
    df_mock = pd.DataFrame({
        "Date": ["2021-06-01", "2019-05-01"],
        "Score": ["6-4 3-6", "7-5 6-7"],
        "Pts_1": [100, 200],
        "Odd_1": [1.5, 2.0],
        "Player": ["nadal", "djokovic"]
    })
    mock_dfs = [df_mock.copy(), df_mock.copy()]

    result_df = transform_data(dfs=mock_dfs, save_it=False)

    # Check that dates are from 2020 to 2024
    assert all(result_df["Date"].dt.year >= 2020), "Found dates before 2020"
    assert all(result_df["Date"].dt.year <= 2024), "Found dates after 2024"

    # Check that excluded columns are dropped
    assert "Pts_1" not in result_df.columns
    assert "Odd_1" not in result_df.columns

    # Check that set score columns are present
    assert "Set1_Player1" in result_df.columns
    assert "Set1_Player2" in result_df.columns
    assert "Set2_Player1" in result_df.columns
    assert "Set2_Player2" in result_df.columns

    # Check score results:
    assert result_df.iloc[0]["Set1_Player1"] == 6
    assert result_df.iloc[0]["Set1_Player2"] == 4
    assert result_df.iloc[0]["Set2_Player1"] == 3
    assert result_df.iloc[0]["Set2_Player2"] == 6

    # Check that string columns are upper-cased
    assert all(result_df["Player"].str.contains("NADAL|DJOKOVIC"))
