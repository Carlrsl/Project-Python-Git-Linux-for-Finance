import pandas as pd

def calculate_global_metrics(df):
    returns = df.pct_change().dropna()
    correlation_matrix = returns.corr()
    
    return returns, correlation_matrix

def normalize_prices(df):
    return (df / df.iloc[0]) * 100