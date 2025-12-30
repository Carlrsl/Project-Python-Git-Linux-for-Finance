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
    features = ['Dist_MA20', 'RSI', 'BB_Width', 'Hist_Vol']
    X = data[features]
    y = data['Target']
    
    return X, y

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
    # TimeSeriesSplit: 5 folds to ensure strict chronological validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Backtesting loop using the TimeSeriesSplit logic
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        ensemble.fit(X_train, y_train)
        # Final prediction for the next day
    latest_data = X.tail(1)
    prediction_prob = ensemble.predict_proba(latest_data)[0][1]
    
    return prediction_prob, ensemble