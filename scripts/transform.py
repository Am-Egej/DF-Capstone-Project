import pandas as pd
import os

def extract_set_scores(set_list):
    result = {}
    for i in range(5):
        if i < len(set_list):
            try:
                p1, p2 = map(int, set_list[i].split('-'))
                result[f'Set{i+1}_Player1'] = p1
                result[f'Set{i+1}_Player2'] = p2
            except:
                result[f'Set{i+1}_Player1'] = None
                result[f'Set{i+1}_Player2'] = None
        else:
            result[f'Set{i+1}_Player1'] = None
            result[f'Set{i+1}_Player2'] = None
    return pd.Series(result)


def transform_data(dfs=[], save_it=True):
    if dfs == []: 
        df_atp = pd.read_csv('data/raw/atp_tennis.csv', low_memory=False)
        df_wta = pd.read_csv('data/raw/wta.csv', low_memory=False)
        dfs = [df_atp, df_wta]

    transformed_dfs = []
    cols_to_exclude = ['Pts_1', 'Pts_2', 'Odd_1', 'Odd_2',]

    for df in dfs:
        df = df.copy()
        
        # Drop unnecessary columns
        df.drop(columns=cols_to_exclude, errors='ignore', inplace=True)

        # Extract the date
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Select data from 2015 onwards
        df = df.loc[df['Date'].dt.year >= 2020]

        # Extract scores per set
        df['Score'] = df['Score'].str.strip()
        df['Set_Scores'] = df['Score'].str.split()
        df = df.join(df['Set_Scores'].apply(extract_set_scores))

        # Drop orginal 'Scores' column
        df.drop(columns=['Score'], inplace=True)

        # Replace Numeric NaNs with -1
        numeric_cols = [col for col in df.columns if df[col].dtype.kind in 'iuf']
        df[numeric_cols] = df[numeric_cols].fillna(-1) 

        # Replace Non-Numeric NaNs with "Missing Data"
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        df[non_numeric_cols] = df[non_numeric_cols].fillna("Missing Data")

        # Convert all object-type columns to string type
        df = df.astype({col: 'string' for col in df.select_dtypes(include='object').columns})
        
        # Apply title case to all string-type columns
        df[df.select_dtypes(include='string').columns] = df.select_dtypes(include='string').apply(lambda x: x.str.title())

        # Append the the transformed DataFrame to transformed_dfs
        transformed_dfs.append(df)

    df_combined = pd.concat(transformed_dfs, ignore_index=True)

    if save_it:
        # Ensure output directory exists
        os.makedirs('data/processed', exist_ok=True)
        df_combined.to_csv('data/processed/transformed_tennis_data.csv', index=False)
        print("✅ Transformed csv was saved")
    return df_combined

if __name__ == "__main__":
    transform_data()
