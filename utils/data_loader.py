import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def get_data(tickers_input, period="1y"):
    if not tickers_input:
        return pd.DataFrame()
    try:
        tickers = [t.strip().upper() for t in tickers_input.split(',')]
        data = yf.download(tickers, period=period, auto_adjust=True)
        if data.empty:
            return pd.DataFrame()
        df_close = data['Close'].copy() if len(tickers) > 1 else data[['Close']].copy()
        if len(tickers) == 1:
            df_close.columns = [tickers[0]]
        return df_close.dropna()
    except Exception:
        return pd.DataFrame()