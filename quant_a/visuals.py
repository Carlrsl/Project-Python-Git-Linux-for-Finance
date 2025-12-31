import plotly.graph_objects as go
import streamlit as st

def plot_ai_strategy(strategy_df, ticker):
    # Main chart: Price vs Strategy Cumulative Value
    fig = go.Figure()
    
    # Adding the Benchmark (Buy & Hold)
    fig.add_trace(go.Scatter(
        x=strategy_df.index, 
        y=strategy_df['Cumulative_BH'],
        name="Buy & Hold",
        line=dict(color='gray', width=1, dash='dash')
    ))
    
    # Adding the AI Strategy curve
    fig.add_trace(go.Scatter(
        x=strategy_df.index, 
        y=strategy_df['Cumulative_AI'],
        name="AI Ensemble Strategy",
        line=dict(color='#00FFCC', width=3)
    ))
    
    fig.update_layout(
        title=f"Strategy Comparison: {ticker}",
        xaxis_title="Date",
        yaxis_title="Cumulative Return (Base 1)",
        template="plotly_dark",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_ai_metrics(metrics):
    # Displaying metrics in professional columns
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("Total Return", f"{metrics['Total Return']:.2%}")
    c2.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
    c3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
    c4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
