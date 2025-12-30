import numpy as np
import pandas as pd
from scipy.optimize import minimize

def get_portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return returns, std

def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_ret, p_std = get_portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_std

def run_monte_carlo(mean_returns, cov_matrix, num_assets, risk_free_rate, num_simulations=2000):
    results = np.zeros((3, num_simulations))
    for i in range(num_simulations):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        p_ret, p_std = get_portfolio_performance(weights, mean_returns, cov_matrix)
        results[0,i] = p_std
        results[1,i] = p_ret
        results[2,i] = (p_ret - risk_free_rate) / p_std
    return results

def optimize_portfolio(df_prices, risk_free_rate=0.02):
    returns = df_prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(mean_returns)
    
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    init_guess = num_assets * [1. / num_assets,]
    
    result = minimize(neg_sharpe_ratio, init_guess, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    
    optimal_weights = result.x
    opt_return, opt_volatility = get_portfolio_performance(optimal_weights, mean_returns, cov_matrix)
    
    mc_results = run_monte_carlo(mean_returns, cov_matrix, num_assets, risk_free_rate)
    
    return {
        "weights": dict(zip(df_prices.columns, optimal_weights)),
        "return": opt_return,
        "volatility": opt_volatility,
        "sharpe": (opt_return - risk_free_rate) / opt_volatility,
        "monte_carlo_results": mc_results
    }