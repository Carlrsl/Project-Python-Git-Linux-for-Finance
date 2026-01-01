import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier
from quant_a.indicators import compute_technical_indicators

def train_predict_ensemble(df, ticker):
    data = compute_technical_indicators(df, ticker)
    
    # Matching features from indicators.py
    features = ['Dist_MA20', 'RSI', 'BB_Width', 'Hist_Vol']
    X = data[features]
    y = data['Target']
    
    tscv = TimeSeriesSplit(n_splits=5)
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, eval_metric='logloss')
    lr = LogisticRegression()
    
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb), ('lr', lr)],
        voting='soft'
    )
    
    # Walking-forward training
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        ensemble.fit(X_train, y_train)
    
    latest_data = X.tail(1)
    prediction_prob = ensemble.predict_proba(latest_data)[0][1]
    
    return prediction_prob, ensemble

def get_ensemble_signals(df, ticker):
    data = compute_technical_indicators(df, ticker)
    features = ['Dist_MA20', 'RSI', 'BB_Width', 'Hist_Vol']
    X = data[features]
    
    split = int(0.7 * len(data))
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train = data['Target'].iloc[:split]
    
    ensemble = VotingClassifier(
        estimators=[
            ('rf', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
            ('xgb', XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, eval_metric='logloss')),
            ('lr', LogisticRegression())
        ],
        voting='soft'
    )
    
    ensemble.fit(X_train, y_train)
    test_signals = ensemble.predict_proba(X_test)[:, 1]
    
    return data['Close'].iloc[split:], test_signals