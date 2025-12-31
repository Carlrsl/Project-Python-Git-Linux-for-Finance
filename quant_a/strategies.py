import pandas as pd
import numpy as np
from quant_a.prediction import get_ensemble_signals

def run_ai_strategy(df, ticker, threshold=0.55):
    # Retrieve out-of-sample prices and AI probabilities
    prices, probabilities = get_ensemble_signals(df, ticker)
    
    strategy_df = pd.DataFrame(index=prices.index)
    strategy_df['Price'] = prices
    strategy_df['Returns'] = strategy_df['Price'].pct_change()
    
    # AI Signal: 1 if probability > threshold, 0 (cash) otherwise
    strategy_df['Signal'] = (probabilities > threshold).astype(int)
    
    return strategy_df

# Calculate strategy returns (signal is applied to the next day's return)
    strategy_df['Strategy_Returns'] = strategy_df['Returns'] * strategy_df['Signal'].shift(1)
    
    # Cumulative performance (Base 1)
    strategy_df['Cumulative_AI'] = (1 + strategy_df['Strategy_Returns'].fillna(0)).cumprod()
    strategy_df['Cumulative_BH'] = (1 + strategy_df['Returns'].fillna(0)).cumprod()