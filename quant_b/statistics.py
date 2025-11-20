import pandas as pd

def calculate_global_metrics(df):
    """
    Calculates daily returns and the correlation matrix for the portfolio.
    
    Args:
        df (pd.DataFrame): DataFrame of asset prices (Close).
        
    Returns:
        tuple: (returns_dataframe, correlation_matrix)
    """
    # 1. Calculate daily percentage change (Returns)
    # dropna() ensures we don't have NaN values for the first calculation
    returns = df.pct_change().dropna()
    
    # 2. Calculate Pearson correlation matrix
    # Essential for analyzing diversification benefits between assets
    correlation_matrix = returns.corr()
    
    return returns, correlation_matrix

def normalize_prices(df):
    """
    Normalizes asset prices to a Base 100 for visual comparison.
    Formula: (Price_t / Price_0) * 100
    
    Args:
        df (pd.DataFrame): Raw price DataFrame.
        
    Returns:
        pd.DataFrame: Normalized DataFrame starting at 100.
    """
    # Divide the entire DataFrame by the first row to set start at 1.0, then multiply by 100
    return (df / df.iloc[0]) * 100