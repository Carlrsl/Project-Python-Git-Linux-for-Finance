import plotly.express as px
import streamlit as st

def plot_correlation_heatmap(corr_matrix):
    """
    Displays an interactive Heatmap using Plotly.
    """
    # Create heatmap
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",       # Show values with 2 decimal places
        aspect="auto",
        color_continuous_scale="RdBu_r",  # Red = Correlated, Blue = Inverse
        zmin=-1, zmax=1,
        origin='lower'
    )
    
    # Update layout for a cleaner look
    fig.update_layout(title="Asset Correlation Matrix")
    
    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_normalized_prices(df_normalized):
    """
    Displays a line chart comparing normalized asset performance.
    """
    fig = px.line(df_normalized, title="Performance Comparison (Base 100)")
    fig.update_layout(xaxis_title="Date", yaxis_title="Normalized Price")
    
    st.plotly_chart(fig, use_container_width=True)