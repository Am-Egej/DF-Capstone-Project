import pandas as pd

def clean_data(df = pd.read_csv('data/raw/atp_tennis.csv')):
    df['Date'] = pd.to_datetime(df['Date'])
    df['is_grand_slam'] = df['Tournament'].str.contains('Australian Open|Wimbledon|US Open|Roland Garros')
    df.to_csv('data/processed/transformed_atp_tennis.csv', index=False)
    return df

if __name__ == "__main__":
    df = pd.read_csv('data/raw/atp_tennis.csv')
    clean_data()
