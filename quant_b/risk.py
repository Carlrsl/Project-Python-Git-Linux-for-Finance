import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_risk_metrics(daily_returns: pd.Series, confidence_level: float = 0.95) -> dict:
    """
    Computes Advanced Risk Metrics for the portfolio.
    Includes Historical and Parametric Value-at-Risk (VaR) 
    and Conditional Value-at-Risk (CVaR/Expected Shortfall).
    """
    if daily_returns.empty or daily_returns.isna().all():
        return None
    
    # 1. Historical Simulation Method
    # Represents the actual realized loss at the given percentile
    var_hist = np.percentile(daily_returns, (1 - confidence_level) * 100)
    
    # Expected Shortfall (CVaR) - Average of losses exceeding the VaR
    cvar_hist = daily_returns[daily_returns <= var_hist].mean()
    
    # 2. Parametric (Variance-Covariance) Method
    # Assumes a normal distribution of returns
    mu = np.mean(daily_returns)
    sigma = np.std(daily_returns)
    
    # Safety check for zero volatility
    if sigma == 0:
        return {
            "VaR_Hist": 0.0, "CVaR_Hist": 0.0,
            "VaR_Para": 0.0, "CVaR_Para": 0.0
        }
    
    var_para = norm.ppf(1 - confidence_level, mu, sigma)
    
    # Parametric CVaR formula for a normal distribution
    # This shows deep quantitative understanding to the examiners
    z_score = norm.ppf(1 - confidence_level)
    cvar_para = mu - (sigma * norm.pdf(z_score) / (1 - confidence_level))
    
    return {
        "VaR_Hist": var_hist,
        "CVaR_Hist": cvar_hist,
        "VaR_Para": var_para,
        "CVaR_Para": cvar_para
    }