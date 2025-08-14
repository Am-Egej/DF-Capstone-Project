import pandas as pd

def transform_data(dfs, save_it=True):
    transformed_dfs = []

    for df in dfs:
        #df['Date'] = pd.to_datetime(df['Date'])
        df['is_grand_slam'] = df['Tournament'].str.contains('Australian Open|Wimbledon|US Open|Australian Open')
        
        transformed_dfs.append(df)

    df_combined = pd.concat(transformed_dfs, ignore_index=True)

    if save_it:
        df_combined.to_csv('data/processed/transformed_tennis_data.csv', index=False)

    return df_combined

if __name__ == "__main__":
    df_atp = pd.read_csv('data/raw/atp_tennis.csv', low_memory=False)
    df_wta = pd.read_csv('data/raw/wta.csv', low_memory=False)

    dfs = [df_atp, df_wta]
    transform_data(dfs)
