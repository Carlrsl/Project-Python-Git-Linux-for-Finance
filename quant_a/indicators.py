import pandas as pd
import numpy as np

def compute_technical_indicators(df, ticker):
    # Create a copy to avoid modifying the original dataframe
    data = df[[ticker]].copy()
    data.columns = ['Close']
    
    return data
# Trend Indicators: Moving Averages and Distance from Trend
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['Dist_MA20'] = (data['Close'] - data['MA20']) / data['MA20']
    # Momentum Indicator: Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))