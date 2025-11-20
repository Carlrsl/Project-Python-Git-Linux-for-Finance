import numpy as np
import pandas as pd
from scipy.optimize import minimize

def get_portfolio_performance(weights, mean_returns, cov_matrix):
    """
    Calculates portfolio return and volatility for given weights.
    """
    # Annualized Return (252 trading days)
    returns = np.sum(mean_returns * weights) * 252
    # Annualized Volatility
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return returns, std

def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    """
    Objective function to minimize (Negative Sharpe Ratio).
    Minimizing negative Sharpe is equivalent to maximizing Sharpe.
    """
    p_ret, p_var = get_portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var

def optimize_portfolio(df_prices, risk_free_rate=0.02):
    """
    Finds the optimal portfolio weights to maximize the Sharpe Ratio using Markowitz MPT.
    
    Args:
        df_prices (pd.DataFrame): Historical asset prices.
        risk_free_rate (float): Risk-free rate approximation (e.g., 0.02 for 2%).
        
    Returns:
        dict: Optimal weights and performance metrics.
    """
    # Calculate returns and covariance
    returns = df_prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    
    # Constraints: Sum of weights must be 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # Bounds: Weights must be between 0 and 1 (No short selling)
    bounds = tuple((0.0, 1.0) for asset in range(num_assets))
    
    # Initial Guess: Equal distribution
    init_guess = num_assets * [1. / num_assets,]
    
    # Run Optimization
    result = minimize(neg_sharpe_ratio, init_guess, args=args,method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Extract results
    optimal_weights = result.x
    opt_return, opt_volatility = get_portfolio_performance(optimal_weights, mean_returns, cov_matrix)
    
    return {
        "weights": dict(zip(df_prices.columns, optimal_weights)),
        "return": opt_return,
        "volatility": opt_volatility,
        "sharpe": (opt_return - risk_free_rate) / opt_volatility
    }