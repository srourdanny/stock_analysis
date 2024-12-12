import pandas as pd

# List of CSV filenames and corresponding stock symbols
csv_files = {
    "amzn_daily.csv": "amzn",
    "goog_daily.csv": "goog",
    "meta_daily.csv": "meta",
    "nvda_daily.csv": "nvda",
    "orcl_daily.csv": "orcl",
    "tsla_daily.csv": "tsla"
}

# Dictionary to store individual dataframes
dataframes = {}

# Read, process, and store each dataframe
for file_name, symbol in csv_files.items():
    # Read the CSV file
    df = pd.read_csv(file_name, header=None, names=["date", "open", "high", "low", "close", "volume"], parse_dates=["date"])

    # Ensure data types are correct
    df["open"] = pd.to_numeric(df["open"], errors='coerce')
    df["high"] = pd.to_numeric(df["high"], errors='coerce')
    df["low"] = pd.to_numeric(df["low"], errors='coerce')
    df["close"] = pd.to_numeric(df["close"], errors='coerce')
    df["volume"] = pd.to_numeric(df["volume"], errors='coerce')

    # Drop rows with NaN values
    df.dropna(inplace=True)

    # Set the date column as the index
    df.set_index("date", inplace=True)

    # Store the dataframe in the dictionary without stock symbol in column names
    dataframes[symbol] = df.copy()

    # Rename columns to include stock symbol for combined dataframe
    df.columns = [f"{col} ({symbol})" for col in df.columns]

    # Update the dataframe in the dictionary for the combined dataframe
    dataframes[symbol + "_combined"] = df

# Combine all dataframes into one wide dataframe
combined_df = pd.concat([dataframes[symbol + "_combined"] for symbol in csv_files.values()], axis=1)

# Save the combined dataframe to a CSV
combined_df.to_csv("combined_stocks.csv")

# Save each individual dataframe to its own variable
amzn_df = dataframes['amzn']
goog_df = dataframes['goog']
meta_df = dataframes['meta']
nvda_df = dataframes['nvda']
orcl_df = dataframes['orcl']
tsla_df = dataframes['tsla']

# Print the head of each dataframe
print("Amazon DataFrame:\n", amzn_df.head())
print("Google DataFrame:\n", goog_df.head())
print("Meta DataFrame:\n", meta_df.head())
print("NVIDIA DataFrame:\n", nvda_df.head())
print("Oracle DataFrame:\n", orcl_df.head())
print("Tesla DataFrame:\n", tsla_df.head())
print("Combined DataFrame:\n", combined_df.head())
