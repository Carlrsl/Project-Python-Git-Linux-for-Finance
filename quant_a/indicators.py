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
    # Volatility Indicator: Bollinger Bands
    data['Std_Dev'] = data['Close'].rolling(window=20).std()
    data['Upper_Band'] = data['MA20'] + (data['Std_Dev'] * 2)
    data['Lower_Band'] = data['MA20'] - (data['Std_Dev'] * 2)
    data['BB_Width'] = (data['Upper_Band'] - data['Lower_Band']) / data['MA20']

    # Performance Indicator: Historical Volatility (Annualized)
    data['Log_Ret'] = np.log(data['Close'] / data['Close'].shift(1))
    data['Hist_Vol'] = data['Log_Ret'].rolling(window=21).std() * np.sqrt(252)
    
    # Target Variable: 1 if next day return is positive, 0 otherwise
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

    