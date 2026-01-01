import numpy as np
import pandas as pd
from scipy.optimize import minimize

def get_portfolio_performance(weights, returns):
    """Calculates annualized return, volatility, and Sharpe ratio."""
    weights = np.array(weights)
    port_return = np.sum(returns.mean() * weights) * 252
    port_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    sharpe = (port_return - 0.02) / port_vol if port_vol != 0 else 0
    return port_return, port_vol, sharpe

def optimize_portfolio(df):
    """
    Performs Monte Carlo simulation to find the Efficient Frontier 
    and the Max Sharpe Ratio portfolio.
    """
    returns = df.pct_change().dropna()
    num_assets = len(df.columns)
    num_portfolios = 5000 # Professional standard for simulation
    
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    # 1. Monte Carlo Simulation
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        p_ret, p_vol, p_sharpe = get_portfolio_performance(weights, returns)
        results[0,i] = p_vol
        results[1,i] = p_ret
        results[2,i] = p_sharpe

    # 2. Identify Optimal Portfolio (Max Sharpe)
    max_sharpe_idx = np.argmax(results[2])
    opt_vol = results[0, max_sharpe_idx]
    opt_ret = results[1, max_sharpe_idx]
    opt_sharpe = results[2, max_sharpe_idx]
    opt_weights = weights_record[max_sharpe_idx]
    
    # Format weights as dictionary for the UI
    weights_dict = {df.columns[i]: opt_weights[i] for i in range(num_assets)}
    
    return {
        'monte_carlo_results': results,
        'return': opt_ret,
        'volatility': opt_vol,
        'sharpe': opt_sharpe,
        'weights': weights_dict
    }

def get_min_variance_weights(returns):
    """Finds weights that minimize portfolio volatility."""
    num_assets = len(returns.columns)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    def min_vol_func(weights):
        return get_portfolio_performance(weights, returns)[1]

    res = minimize(min_vol_func, num_assets * [1./num_assets], 
                   method='SLSQP', bounds=bounds, constraints=constraints)
    return res.x