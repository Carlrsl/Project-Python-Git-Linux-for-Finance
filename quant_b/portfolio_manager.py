import numpy as np
import pandas as pd

def simulate_portfolio(df_prices, weights):
    asset_returns = df_prices.pct_change().dropna()
    
    weights = np.array(weights)
    if np.sum(weights) != 0:
        weights = weights / np.sum(weights)

    portfolio_daily_returns = asset_returns.dot(weights)
    
    portfolio_cumulative_returns = (1 + portfolio_daily_returns).cumprod()

    if not portfolio_cumulative_returns.empty:
        portfolio_cumulative_returns = portfolio_cumulative_returns / portfolio_cumulative_returns.iloc[0]


    if not portfolio_cumulative_returns.empty:
        total_return = portfolio_cumulative_returns.iloc[-1] - 1
    else:
        total_return = 0.0
        
    annual_volatility = portfolio_daily_returns.std() * np.sqrt(252)

    if annual_volatility == 0:
        sharpe_ratio = 0
    else:
        sharpe_ratio = (portfolio_daily_returns.mean() / portfolio_daily_returns.std()) * np.sqrt(252)
    
    rolling_max = portfolio_cumulative_returns.cummax()
    drawdown = portfolio_cumulative_returns / rolling_max - 1.0
    max_drawdown = drawdown.min()

    metrics = {
        "Total Return": total_return,
        "Annual Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown
    }
    
    return {
        "cumulative_returns": portfolio_cumulative_returns,
        "daily_returns": portfolio_daily_returns,
        "metrics": metrics
    }