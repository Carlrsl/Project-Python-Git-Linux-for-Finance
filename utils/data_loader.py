import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def get_data(tickers, period="1y"):
    # Handle empty inputs
    if not tickers:
        return pd.DataFrame()
    
    if isinstance(tickers, str):
        tickers = [t.strip().upper() for t in tickers.split(',')]

    try:
        print(f"[INFO] Fetching data from Yahoo Finance: {tickers}")
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