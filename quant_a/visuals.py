import plotly.graph_objects as go
import streamlit as st

def plot_ai_strategy(strategy_df, ticker):
    fig = go.Figure()
    
    # Adding Benchmark
    fig.add_trace(go.Scatter(
        x=strategy_df.index, 
        y=strategy_df['Benchmark_PNL'],
        name="Buy & Hold Benchmark",
        line=dict(color='gray', width=1, dash='dash')
    ))
    
    # Adding AI Strategy
    fig.add_trace(go.Scatter(
        x=strategy_df.index, 
        y=strategy_df['Cumulative_PNL'],
        name="AI Ensemble Strategy",
        line=dict(color='#00FFCC', width=3)
    ))
    
    fig.update_layout(
        title=f"Predictive Strategy Backtest: {ticker}",
        xaxis_title="Timeline",
        yaxis_title="Equity Value (Base 1.0)",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_ai_metrics(metrics):
    st.write("#### Performance Attribution")
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("Total Return", f"{metrics['Total Return']:.2%}")
    c2.metric("Ann. Volatility", f"{metrics['Annual Vol']:.2%}")
    c3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
    c4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")