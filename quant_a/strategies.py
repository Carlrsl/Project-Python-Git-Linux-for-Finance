import pandas as pd
import numpy as np

def run_ma_crossover_strategy(df: pd.DataFrame, short_window: int, long_window: int) -> pd.DataFrame:
    """
    Implements a Moving Average Crossover strategy (Momentum).
    Short MA > Long MA = Buy Signal.
    """
    data = df.copy()
    # Renaming to 'Close' if necessary to ensure compatibility with data_loader
    if 'Close' not in data.columns and len(data.columns) == 1:
        data.columns = ['Close']
        
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    
    # Signal generation: 1 (Long), -1 (Short)
    data['Signal'] = 0.0
    data['Signal'] = np.where(data['Short_MA'] > data['Long_MA'], 1.0, -1.0)
    
    # Shift signal by 1 day to prevent look-ahead bias
    data['Strategy_Returns'] = data['Signal'].shift(1) * data['Close'].pct_change()
    data['Cumulative_PNL'] = (1 + data['Strategy_Returns'].fillna(0)).cumprod()
    data['Benchmark_PNL'] = (1 + data['Close'].pct_change().fillna(0)).cumprod()
    
    return data

def run_bollinger_strategy(df: pd.DataFrame, window: int, num_std: float) -> pd.DataFrame:
    """
    Implements a Bollinger Bands Mean-Reversion strategy.
    Price < Lower Band = Buy Signal.
    """
    data = df.copy()
    if 'Close' not in data.columns and len(data.columns) == 1:
        data.columns = ['Close']

    data['MA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper'] = data['MA'] + (num_std * data['STD'])
    data['Lower'] = data['MA'] - (num_std * data['STD'])
    
    # Signal generation: Buy at oversold, Sell at overbought
    data['Signal'] = 0.0
    data['Signal'] = np.where(data['Close'] < data['Lower'], 1.0, 
                             np.where(data['Close'] > data['Upper'], -1.0, 0.0))
    
    # Preventing look-ahead bias
    data['Strategy_Returns'] = data['Signal'].shift(1) * data['Close'].pct_change()
    data['Cumulative_PNL'] = (1 + data['Strategy_Returns'].fillna(0)).cumprod()
    data['Benchmark_PNL'] = (1 + data['Close'].pct_change().fillna(0)).cumprod()
    
    return data

def get_performance_metrics(cumulative_series: pd.Series):
    """
    Calculates institutional risk/return KPIs.
    """
    returns = cumulative_series.pct_change().dropna()
    
    # Performance metrics calculation
    total_return = cumulative_series.iloc[-1] - 1
    ann_vol = returns.std() * np.sqrt(252)
    
    # Sharpe Ratio (Risk-free rate assumed at 2.0%)
    sharpe = (returns.mean() * 252 - 0.02) / ann_vol if ann_vol != 0 else 0
    
    # Maximum Drawdown calculation
    peak = cumulative_series.cummax()
    drawdown = (cumulative_series - peak) / peak
    max_dd = drawdown.min()
    
    # Hit Ratio: percentage of winning days
    hit_ratio = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0
    
    return {
        "Total Return": total_return,
        "Annual Vol": ann_vol,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd,
        "Hit Ratio": hit_ratio
    }