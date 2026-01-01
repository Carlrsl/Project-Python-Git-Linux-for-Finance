import pandas as pd
import numpy as np

def calculate_global_metrics(df: pd.DataFrame) -> tuple:
    """
    Computes global statistical metrics for the asset universe.
    Returns cleaned daily returns and the Pearson correlation matrix.
    """
    # 1. Calculate percentage changes
    # We drop the first row as it will always be NaN after pct_change
    returns = df.pct_change().dropna()
    
    # 2. Compute Correlation Matrix
    # Essential for the 'Risk Decomposition' section of the dashboard
    correlation_matrix = returns.corr(method='pearson')
    
    return returns, correlation_matrix

def normalize_prices(df: pd.DataFrame, base: int = 100) -> pd.DataFrame:
    """
    Normalizes asset prices to a common starting point (default 100).
    Allows for visual comparison of performance across different price scales.
    """
    if df.empty:
        return df
    
    # Using .iloc[0] to ensure all assets start at the same relative value
    return (df / df.iloc[0]) * base