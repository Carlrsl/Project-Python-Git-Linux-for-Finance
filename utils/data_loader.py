import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300) # Cache data for 5 minutes (meets requirement "updates at least every few minutes")
def get_data(tickers, period="1y"):
    """
    Fetches adjusted closing prices for a list of tickers.
    Used by both Quant A and Quant B modules.
    
    Args:
        tickers (str or list): List of tickers or comma-separated string.
        period (str): History period (e.g., '1mo', '1y', '5y').
        
    Returns:
        pd.DataFrame: DataFrame containing only 'Close' prices.
    """
    # Handle empty inputs
    if not tickers:
        return pd.DataFrame()
    
    # Clean input: " AAPL, msft " -> ['AAPL', 'MSFT']
    if isinstance(tickers, str):
        tickers = [t.strip().upper() for t in tickers.split(',')]

    try:
        print(f"📡 Fetching data from Yahoo Finance: {tickers}")
        
        # group_by='ticker' ensures a consistent structure for multiple assets
        data = yf.download(tickers, period=period, group_by='ticker', auto_adjust=True)
        
        df_close = pd.DataFrame()

        # Case 1: Single Asset (YFinance structure is flat)
        if len(tickers) == 1:
            ticker = tickers[0]
            # Check if data is not empty
            if not data.empty:
                # Handle potential multi-index issues
                if isinstance(data.columns, pd.MultiIndex):
                    df_close[ticker] = data[('Close', ticker)] if ('Close', ticker) in data.columns else data['Close']
                else:
                    df_close[ticker] = data['Close']
        
        # Case 2: Multiple Assets (YFinance structure is MultiIndex)
        else:
            for t in tickers:
                # Extract 'Close' column for each ticker if it exists
                if t in data.columns.levels[0]:
                    df_close[t] = data[t]['Close']
        
        # Remove rows with NaN values (e.g., holidays)
        df_close.dropna(inplace=True)
        return df_close

    except Exception as e:
        st.error(f"Data download error: {e}")
        return pd.DataFrame()