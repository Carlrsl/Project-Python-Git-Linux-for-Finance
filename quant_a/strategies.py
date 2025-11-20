# quant_a/strategies.py

import numpy as np
import pandas as pd

# --- Fonctions de Stratégie ---

def run_buy_and_hold(prices):
    """ Calcule la valeur cumulative de la stratégie Buy and Hold (base 100). """
    returns = prices['Price'].pct_change()
    returns.fillna(0, inplace=True)
    cumulative_value = (1 + returns).cumprod() * 100
    return cumulative_value

def run_momentum_strategy(prices, short_window=50, long_window=200):
    """ Calcule la valeur cumulative de la stratégie de croisement de moyennes mobiles. """
    data = prices.copy()
    data['Short_MA'] = data['Price'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Price'].rolling(window=long_window).mean()
    
    # Position (1: Achat, -1: Vente/Short)
    data['Signal'] = np.where(data['Short_MA'] > data['Long_MA'], 1, -1)
    
    data['Strategy_Returns'] = data['Price'].pct_change() * data['Signal'].shift(1)
    data['Strategy_Returns'].fillna(0, inplace=True)
    
    cumulative_value = (1 + data['Strategy_Returns']).cumprod() * 100
    return cumulative_value

# --- Fonction de Métriques ---

def calculate_metrics(cumulative_value, risk_free_rate=0.02):
    """ Calcule et formate les métriques clés de performance. """
    strategy_returns = cumulative_value.pct_change().dropna()
    
    annual_returns = strategy_returns.mean() * 252
    annual_volatility = strategy_returns.std() * np.sqrt(252)
    
    sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility if annual_volatility != 0 else 0.0
    
    peak = cumulative_value.cummax()
    max_drawdown = ((cumulative_value - peak) / peak).min()
    
    total_return = (cumulative_value.iloc[-1] / 100) - 1
    
    return {
        "Rend. Total": f"{total_return * 100:.2f} %",
        "Rend. Annuel": f"{annual_returns * 100:.2f} %",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown * 100:.2f} %",
    }