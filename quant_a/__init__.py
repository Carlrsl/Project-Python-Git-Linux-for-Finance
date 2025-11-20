# quant_a/indicators.py

import yfinance as yf
import pandas as pd

def get_asset_data(ticker, start_date, end_date, interval='1d'):
    """ Récupère les données de clôture via yfinance. """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        if data.empty:
            return pd.DataFrame()
        return data[['Close']].rename(columns={'Close': 'Price'})
    except Exception:
        return pd.DataFrame()

# Vous pouvez ajouter ici d'autres indicateurs techniques (RSI, Bollinger Bands...) si vous le souhaitez.