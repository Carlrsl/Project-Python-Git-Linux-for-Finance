### Python, Git, & Linux for Finance | Final Project

## 🚀 Live Access
The dashboard is deployed and accessible in real-time here: 
**[http://13.49.241.13:8501](http://13.49.241.13:8501)**

---

## 👥 Authors
* **Louis Roze** – Quantitative Lead (Module A: Univariate Predictive Intelligence)
* **Carl Roussel** – Quantitative Lead (Module B: Multivariate Portfolio Management)

---

## 🏛️ Project Overview
This project is an institutional-grade quantitative terminal designed to analyze financial assets through two distinct research modules. It integrates real-time data fetching, machine learning ensemble models, and modern portfolio optimization techniques.

### 📊 Module A: Univariate Intelligence (Louis Roze)
Focuses on deep-dive analysis of single assets (Stocks, Crypto, Forex, Gold) using predictive modeling.
* **Backtesting Engine**: Comparison between *Buy & Hold*, *MA Crossover*, and *Bollinger Bands* strategies.
* **ML Ensemble Engine**: Implementation of a **Voting Classifier** combining XGBoost, Random Forest, and Logistic Regression.
* **Statistical Integrity**: Use of `TimeSeriesSplit` to eliminate look-ahead bias during training.
* **Interactive Controls**: Dynamic sliders for strategy parameters and confidence thresholds.

### 📈 Module B: Multivariate Portfolio Management (Carl Roussel)
Extends the analysis to a multi-asset universe (12 assets) to optimize risk-adjusted returns.
* **Markowitz Optimization**: Implementation of the **Efficient Frontier** using Monte Carlo simulations.
* **Risk Metrics**: Advanced tail-risk assessment featuring **Value-at-Risk (VaR)** and **Expected Shortfall (CVaR)**.
* **Performance Attribution**: Visual comparison of the strategic portfolio against all individual universe components.
* **Correlation Analysis**: Interactive heatmaps to identify diversification effects and hedge opportunities.


---

## 🛠️ Tech Stack & DevOps
* **Language**: Python 3.12 (Object-Oriented Programming).
* **Frontend**: Streamlit.
* **Cloud & Linux**: Deployed on **AWS EC2 (Ubuntu)**.
* **Automation**: Daily financial audit reports generated automatically via **Cron Jobs**.
* **Version Control**: Git-flow methodology with feature branching.
