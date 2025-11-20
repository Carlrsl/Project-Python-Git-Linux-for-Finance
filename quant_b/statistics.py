import pandas as pd

def calculate_global_metrics(df):
    """
    Calculates daily returns and the correlation matrix.
    
    Args:
        df (pd.DataFrame): DataFrame of asset prices.
        
    Returns:
        tuple: (returns_dataframe, correlation_matrix)
    """
    # 1. Calculate daily percentage change (Returns)
    returns = df.pct_change().dropna()
    
    # 2. Calculate Pearson correlation matrix
    # Useful to analyze diversification effects
    correlation_matrix = returns.corr()
    
    return returns, correlation_matrix

def normalize_prices(df):
    """
    Normalizes prices to Base 100 for visual comparison.
    Formula: (Price_t / Price_0) * 100
    """
    # Divide the entire DataFrame by the first row
    return (df / df.iloc[0]) * 100