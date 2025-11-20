import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_risk_metrics(portfolio_returns, confidence_level=0.95):
    """
    Calculates Value at Risk (VaR) and Conditional Value at Risk (CVaR)
    using both Historical and Parametric methods.
    
    Args:
        portfolio_returns (pd.Series): Daily returns of the portfolio.
        confidence_level (float): Confidence level (default 0.95).
        
    Returns:
        dict: Dictionary containing VaR and CVaR values.
    """
    if portfolio_returns.empty:
        return {}

    # 1. Historical Method (Non-parametric)
    # VaR is the q-th quantile of the return distribution
    var_historical = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
    
    # CVaR is the average of returns falling below the VaR threshold
    cvar_historical = portfolio_returns[portfolio_returns <= var_historical].mean()

    # 2. Parametric Method (Gaussian / Normal Distribution)
    mu = portfolio_returns.mean()
    sigma = portfolio_returns.std()
    
    # PPF = Percent Point Function (Inverse of CDF)
    var_parametric = norm.ppf(1 - confidence_level, mu, sigma)
    
    # Analytical formula for Gaussian CVaR
    cvar_parametric = mu - (sigma * norm.pdf(norm.ppf(1 - confidence_level)) / (1 - confidence_level))

    return {
        "VaR_95_Historical": var_historical,
        "CVaR_95_Historical": cvar_historical,
        "VaR_95_Parametric": var_parametric,
        "CVaR_95_Parametric": cvar_parametric
    }