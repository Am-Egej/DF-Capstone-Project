import pandas as pd

def clean_data():
    df = pd.read_csv('data/raw/atp_tennis.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    #df['is_grand_slam'] = df['tournament'].str.contains('Australian Open|Wimbledon|US Open|Roland Garros')
    df.to_csv('data/processed/cleaned_matches.csv', index=False)

if __name__ == "__main__":
    clean_data()
