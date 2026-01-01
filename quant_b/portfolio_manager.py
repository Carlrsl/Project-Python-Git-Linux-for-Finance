import numpy as np
import pandas as pd

def simulate_portfolio(df_prices: pd.DataFrame, weights: list) -> dict:
    """
    Computes portfolio performance based on asset prices and weight allocation.
    Includes performance attribution and risk-adjusted metrics.
    """
    # 1. Compute asset daily returns
    asset_returns = df_prices.pct_change().dropna()
    
    # 2. Normalize weights to ensure they sum to 1.0 (100%)
    weights = np.array(weights)
    if np.sum(weights) != 0:
        weights = weights / np.sum(weights)

    # 3. Calculate portfolio daily returns (Dot Product)
    portfolio_daily_returns = asset_returns.dot(weights)
    
    # 4. Generate Cumulative Equity Curve (Base 1.0)
    portfolio_cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    
    # Safety check for empty dataframes
    if portfolio_cumulative_returns.empty:
        return {"cumulative_returns": pd.Series(), "daily_returns": pd.Series(), "metrics": {}}

    # 5. Performance Metrics Calculation
    total_return = portfolio_cumulative_returns.iloc[-1] - 1
    annual_volatility = portfolio_daily_returns.std() * np.sqrt(252)

    # Sharpe Ratio: (Mean Return - Risk Free Rate) / Volatility
    # Using 2.0% as a standard institutional risk-free rate baseline
    risk_free_rate = 0.02
    excess_return = (portfolio_daily_returns.mean() * 252) - risk_free_rate
    
    if annual_volatility > 0:
        sharpe_ratio = excess_return / annual_volatility
    else:
        sharpe_ratio = 0.0
    
    # 6. Max Drawdown Analysis
    rolling_max = portfolio_cumulative_returns.cummax()
    drawdown = (portfolio_cumulative_returns - rolling_max) / rolling_max
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