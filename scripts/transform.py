import pandas as pd

def transform_data(df, save_it=True):
    df['Date'] = pd.to_datetime(df['Date'])
    df['is_grand_slam'] = df['Tournament'].str.contains('Australian Open|Wimbledon|US Open|Australian Open')
    if save_it:
        df.to_csv('data/processed/transformed_atp_tennis.csv', index=False)
    return df

if __name__ == "__main__":
    df = pd.read_csv('data/raw/atp_tennis.csv')
    transform_data(df)
