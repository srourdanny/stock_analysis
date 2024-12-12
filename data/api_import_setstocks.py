import requests
import pandas as pd
import textwrap  # Import textwrap for formatting text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variables
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# Function to fetch data from Alpha Vantage
def fetch_stock_data(api_key, function, symbol, interval=None, outputsize=None):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': function,
        'symbol': symbol,
        'apikey': api_key
    }
    if interval:
        params['interval'] = interval
    if outputsize:
        params['outputsize'] = outputsize

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Unable to fetch data. Check your API key or parameters.'}


# Predefined stock symbols
# stocks = ['AMZN', 'GOOG', 'META', 'ORCL','NVDA','TSLA']
stocks = ['AMZN']
# Dictionary to hold DataFrames for comparison
stock_dataframes = {}

# Fetch daily and overview data for predefined stocks
for stock in stocks:
    print(f"Fetching data for {stock}...")

    # Daily historical data
    daily_data = fetch_stock_data(api_key, function='TIME_SERIES_DAILY', symbol=stock, outputsize='full')
    daily_df = pd.DataFrame(daily_data.get('Time Series (Daily)', {})).transpose()
    daily_df.index = pd.to_datetime(daily_df.index)
    daily_df.sort_index(inplace=True)

    # Stock overview
    overview_data = fetch_stock_data(api_key, function='OVERVIEW', symbol=stock)
    overview_df = pd.DataFrame([overview_data])

    # Save DataFrames in the dictionary
    stock_dataframes[stock] = {
        'daily_data': daily_df,
        'overview_data': overview_df
    }

    print(daily_data)

# Output confirmation
print("Data fetching completed for user input and predefined stocks.")

# Prepare DataFrames
amzn_daily = stock_dataframes['AMZN']['daily_data']
amzn_daily.index = pd.to_datetime(amzn_daily.index)
amzn_daily = amzn_daily.sort_index()
amzn_daily = amzn_daily.loc['2019-11-30':'2024-11-30']
print(amzn_daily.head())
amzn_daily.to_csv('amzn_daily.csv', index=True)

# goog_daily = stock_dataframes['GOOG']['daily_data']
# goog_daily.to_csv('goog_daily.csv', index=True)

# meta_daily = stock_dataframes['META']['daily_data']
# meta_daily.to_csv('meta_daily.csv', index=True)

# orcl_daily = stock_dataframes['ORCL']['daily_data']
# orcl_daily.to_csv('orcl_daily.csv', index=True)

# tlsa_daily = stock_dataframes['TLSA']['daily_data']
# tlsa_daily.to_csv('tlsa_daily.csv', index=True)