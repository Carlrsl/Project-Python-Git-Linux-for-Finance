import pandas as pd
import numpy as np

def compute_technical_indicators(df, ticker):
    # Create a copy to avoid modifying the original dataframe
    data = df[[ticker]].copy()
    data.columns = ['Close']
    
    return data