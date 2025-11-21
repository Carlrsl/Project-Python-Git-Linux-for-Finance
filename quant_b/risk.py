import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_risk_metrics(portfolio_returns, confidence_level=0.95):
    if portfolio_returns.empty:
        return {}

    var_historical = np.percentile(portfolio_returns, (1 - confidence_level) * 100)

    cvar_historical = portfolio_returns[portfolio_returns <= var_historical].mean()

    mu = portfolio_returns.mean()
    sigma = portfolio_returns.std()

    var_parametric = norm.ppf(1 - confidence_level, mu, sigma)
    
    cvar_parametric = mu - (sigma * norm.pdf(norm.ppf(1 - confidence_level)) / (1 - confidence_level))

    return {
        "VaR_95_Historical": var_historical,
        "CVaR_95_Historical": cvar_historical,
        "VaR_95_Parametric": var_parametric,
        "CVaR_95_Parametric": cvar_parametric
    }