import numpy as np
import pandas as pd

def simulate_portfolio(df_prices, weights):
    """
    Simulates a portfolio based on historical data and user-defined weights.
    
    Args:
        df_prices (pd.DataFrame): Historical closing prices of assets.
        weights (list or np.array): List of weights (must sum to 1).
        
    Returns:
        dict: A dictionary containing metrics and cumulative return series.
    """
    # 1. Calculate daily returns of individual assets
    asset_returns = df_prices.pct_change().dropna()
    
    # 2. Ensure weights are a numpy array
    weights = np.array(weights)
    
    # Normalize weights if they don't sum to 1 (Safety check)
    if np.sum(weights) != 0:
        weights = weights / np.sum(weights)
        
    # 3. Calculate Portfolio Daily Returns
    # Dot product: (Dates x Assets) . (Assets x 1) = (Dates x 1)
    portfolio_daily_returns = asset_returns.dot(weights)
    
    # 4. Calculate Cumulative Returns (Growth of $1)
    # Formula: (1 + r1) * (1 + r2) * ...
    portfolio_cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    
    # Rebase to start at 1.0 (or 100) for the first valid date
    # We divide by the first value so the chart starts at the same point
    if not portfolio_cumulative_returns.empty:
        portfolio_cumulative_returns = portfolio_cumulative_returns / portfolio_cumulative_returns.iloc[0]

    # 5. Calculate Key Metrics (Annualized)
    # Assuming 252 trading days in a year
    if not portfolio_cumulative_returns.empty:
        total_return = portfolio_cumulative_returns.iloc[-1] - 1
    else:
        total_return = 0.0
        
    annual_volatility = portfolio_daily_returns.std() * np.sqrt(252)
    
    # Sharpe Ratio (assuming risk-free rate ~ 0 for simplicity)
    if annual_volatility == 0:
        sharpe_ratio = 0
    else:
        sharpe_ratio = (portfolio_daily_returns.mean() / portfolio_daily_returns.std()) * np.sqrt(252)
    
    # Max Drawdown Calculation
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