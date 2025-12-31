import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier
from quant_a.indicators import compute_technical_indicators

def train_predict_ensemble(df, ticker):
    # Retrieve technical features from our previous module
    data = compute_technical_indicators(df, ticker)
    
    # Define features (X) and target (y)
    # Target is already shifted in compute_technical_indicators
    features = ['Dist_MA20', 'RSI', 'BB_Width', 'Hist_Vol']
    X = data[features]
    y = data['Target']
    
    # TimeSeriesSplit: 5 folds to ensure strict chronological validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Base models for our Ensemble
    # 1. Random Forest for robustness to noise
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    
    # 2. XGBoost for capturing non-linear patterns
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, eval_metric='logloss')
    
    # 3. Logistic Regression as a stable linear baseline
    lr = LogisticRegression()
    
    # Soft Voting: takes the average of predicted probabilities
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb), ('lr', lr)],
        voting='soft'
    )
    
    # Backtesting loop using the TimeSeriesSplit logic
    # We train on the past to predict the "future" fold
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        ensemble.fit(X_train, y_train)
    
    # Final prediction for the next day
    # We take the very last row of available data
    latest_data = X.tail(1)
    prediction_prob = ensemble.predict_proba(latest_data)[0][1]
    
    # We also return the ensemble object if we want to run more tests
    return prediction_prob, ensemble

def get_ensemble_signals(df, ticker):
    # This function generates a full history of signals for the backtest
    data = compute_technical_indicators(df, ticker)
    features = ['Dist_MA20', 'RSI', 'BB_Width', 'Hist_Vol']
    X = data[features]
    y = data['Target']
    
    # Simple walk-forward: we use 70% for training and predict on the remaining 30%
    split = int(0.7 * len(data))
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    
    ensemble = VotingClassifier(
        estimators=[
            ('rf', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
            ('xgb', XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, eval_metric='logloss')),
            ('lr', LogisticRegression())
        ],
        voting='soft'
    )
    
    ensemble.fit(X_train, y_train)
    
    # Probability of price going up for the test set
    test_signals = ensemble.predict_proba(X_test)[:, 1]
    
    # Return the test period price and corresponding AI signals
    return data['Close'].iloc[split:], test_signals
