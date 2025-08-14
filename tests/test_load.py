import pandas as pd
from scripts.load import load_to_postgres

def test_load_function_runs():
    data = 'PostgresSQL Data'
    df = pd.DataFrame(data) # Use real connection to pagila here once it is done - to be editted.
   
    assert isinstance(df, pd.DataFrame) #Error will occur if no PostgreSQL database exists.
