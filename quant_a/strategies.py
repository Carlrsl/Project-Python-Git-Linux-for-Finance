import pandas as pd
import numpy as np
from quant_a.prediction import get_ensemble_signals

def run_ai_strategy(df, selected_asset, threshold=0.5):
    """
    Executes the Ensemble AI strategy.
    Connects the prediction engine to the backtesting logic.
    """
    # Retrieve price data and AI probabilities from prediction.py
    price_data, signals = get_ensemble_signals(df, selected_asset)
    
    results = pd.DataFrame(index=price_data.index)
    results['Close'] = price_data
    
    # Signal: 1 (Long) if probability > threshold, else -1 (Short)
    results['Signal'] = np.where(signals > threshold, 1.0, -1.0)
    
    # Backtest with 1-day shift to eliminate look-ahead bias
    results['Strategy_Returns'] = results['Signal'].shift(1) * results['Close'].pct_change()
    results['Cumulative_PNL'] = (1 + results['Strategy_Returns'].fillna(0)).cumprod()
    results['Benchmark_PNL'] = (1 + results['Close'].pct_change().fillna(0)).cumprod()
    
    return results

def run_ma_crossover_strategy(df, short_window, long_window):
    """Standard Moving Average Crossover (Momentum)"""
    data = df.copy()
    if 'Close' not in data.columns and len(data.columns) == 1:
        data.columns = ['Close']
        
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    data['Signal'] = np.where(data['Short_MA'] > data['Long_MA'], 1.0, -1.0)
    
    data['Strategy_Returns'] = data['Signal'].shift(1) * data['Close'].pct_change()
    data['Cumulative_PNL'] = (1 + data['Strategy_Returns'].fillna(0)).cumprod()
    data['Benchmark_PNL'] = (1 + data['Close'].pct_change().fillna(0)).cumprod()
    return data

def run_bollinger_strategy(df, window, num_std):
    """Bollinger Bands Strategy (Mean-Reversion)"""
    data = df.copy()
    if 'Close' not in data.columns and len(data.columns) == 1:
        data.columns = ['Close']

    data['MA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper'] = data['MA'] + (num_std * data['STD'])
    data['Lower'] = data['MA'] - (num_std * data['STD'])
    
    data['Signal'] = np.where(data['Close'] < data['Lower'], 1.0, 
                             np.where(data['Close'] > data['Upper'], -1.0, 0.0))
    
    data['Strategy_Returns'] = data['Signal'].shift(1) * data['Close'].pct_change()
    data['Cumulative_PNL'] = (1 + data['Strategy_Returns'].fillna(0)).cumprod()
    data['Benchmark_PNL'] = (1 + data['Close'].pct_change().fillna(0)).cumprod()
    return data

def get_performance_metrics(cumulative_series):
    """Institutional Grade Risk/Return Metrics"""
    returns = cumulative_series.pct_change().dropna()
    total_return = cumulative_series.iloc[-1] - 1
    ann_vol = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() * 252 - 0.02) / ann_vol if ann_vol != 0 else 0
    peak = cumulative_series.cummax()
    max_dd = ((cumulative_series - peak) / peak).min()
    hit_ratio = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0
    
    return {
        "Total Return": total_return,
        "Annual Vol": ann_vol,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd,
        "Hit Ratio": hit_ratio
    }