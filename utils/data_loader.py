import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300) # Cache data for 5 minutes to minimize API calls
def get_data(tickers, period="1y"):
    """
    Fetches adjusted closing prices for a list of tickers from Yahoo Finance.
    Used by both Quant A and Quant B modules.
    
    Args:
        tickers (str or list): List of tickers or a comma-separated string.
        period (str): History period (e.g., '1mo', '1y', '5y').
        
    Returns:
        pd.DataFrame: DataFrame containing only 'Close' prices.
                      Returns an empty DataFrame on failure.
    """
    # Handle empty inputs
    if not tickers:
        return pd.DataFrame()
    
    # Clean input string: " AAPL, msft " -> ['AAPL', 'MSFT']
    if isinstance(tickers, str):
        tickers = [t.strip().upper() for t in tickers.split(',')]

    try:
        print(f"[INFO] Fetching data from Yahoo Finance: {tickers}")
        
        # group_by='ticker' ensures a consistent structure for multiple assets
        # auto_adjust=True gets the split/dividend adjusted price
        data = yf.download(tickers, period=period, group_by='ticker', auto_adjust=True)
        
        df_close = pd.DataFrame()

        # Case 1: Single Asset (YFinance structure is flat or simple)
        if len(tickers) == 1:
            ticker = tickers[0]
            if not data.empty:
                # Handle potential MultiIndex if yfinance returns it even for one asset
                if isinstance(data.columns, pd.MultiIndex):
                    # Extract Close column safely
                    try:
                        df_close[ticker] = data[('Close', ticker)]
                    except KeyError:
                         # Fallback if structure is different
                        df_close[ticker] = data['Close']
                else:
                    df_close[ticker] = data['Close']
        
        # Case 2: Multiple Assets (YFinance structure is MultiIndex)
        else:
            for t in tickers:
                # Check if the ticker exists in the returned data columns
                if t in data.columns.levels[0]:
                    df_close[t] = data[t]['Close']
        
        # Remove rows with NaN values (e.g., non-trading days)
        df_close.dropna(inplace=True)
        return df_close

    except Exception as e:
        st.error(f"Data download error: {e}")
        return pd.DataFrame()