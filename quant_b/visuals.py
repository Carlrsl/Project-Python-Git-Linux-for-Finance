import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_correlation_heatmap(corr_matrix):
    """
    Renders an interactive heatmap to analyze asset dependencies.
    Essential for explaining diversification benefits.
    """
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r", # Professional financial standard
        zmin=-1, 
        zmax=1,
        labels=dict(color="Correlation")
    )
    
    fig.update_layout(
        title="Cross-Asset Correlation Matrix",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_normalized_prices(df_normalized):
    """
    Compares the historical performance of all universe assets.
    """
    fig = px.line(
        df_normalized, 
        title="Asset Performance Benchmark (Base 100)",
        template="plotly_dark"
    )
    
    fig.update_layout(
        xaxis_title="Timeline", 
        yaxis_title="Indexed Value",
        legend_title="Tickers",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)