import yfinance as yf
import pandas as pd
import streamlit as st

def get_market_data(tickers, period="1y"):
    """
    Fetch historical data for a list of tickers.
    """
    # Download data from Yahoo Finance
    # group_by='ticker' organizes data nicely by asset
    data = yf.download(tickers, period=period, group_by='ticker', auto_adjust=True)
    
    # Create an empty DataFrame to store Close prices
    df_close = pd.DataFrame()
    
    # Loop through each ticker to extract the 'Close' price
    for t in tickers:
        try:
            # Try to get the Close column
            df_close[t] = data[t]['Close']
        except KeyError:
            # If ticker is wrong, show error
            st.error(f"Error: Could not retrieve data for {t}")
            
    return df_close

def normalize_data(df):
    """
    Normalize data to base 100 for comparison.
    Formula: (Price / Initial_Price) * 100
    """
    # We divide the whole dataframe by the first row (iloc[0])
    return (df / df.iloc[0]) * 100