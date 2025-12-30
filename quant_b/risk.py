import numpy as np
from scipy.stats import norm

def calculate_risk_metrics(daily_returns, confidence_level=0.95):
    if daily_returns.empty:
        return None
    
    var_hist = np.percentile(daily_returns, (1 - confidence_level) * 100)
    cvar_hist = daily_returns[daily_returns <= var_hist].mean()
    
    mu = np.mean(daily_returns)
    sigma = np.std(daily_returns)
    
    var_para = norm.ppf(1 - confidence_level, mu, sigma)
    cvar_para = mu - (sigma * norm.pdf(norm.ppf(1 - confidence_level)) / (1 - confidence_level))
    
    return {
        "VaR_Hist": var_hist,
        "CVaR_Hist": cvar_hist,
        "VaR_Para": var_para,
        "CVaR_Para": cvar_para
    }