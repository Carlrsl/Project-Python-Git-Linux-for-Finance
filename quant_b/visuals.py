import plotly.express as px
import streamlit as st

def plot_correlation_heatmap(corr_matrix):
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",                  # Display values with 2 decimal places
        aspect="auto",
        color_continuous_scale="RdBu_r",  # Red = Positive Correlation, Blue = Negative
        zmin=-1, 
        zmax=1,
        origin='lower'
    )
    
    fig.update_layout(title="Asset Correlation Matrix")
    st.plotly_chart(fig, use_container_width=True)

def plot_normalized_prices(df_normalized):
    fig = px.line(df_normalized, title="Performance Comparison (Base 100)")
    
    fig.update_layout(
        xaxis_title="Date", 
        yaxis_title="Normalized Price (Start=100)",
        legend_title="Assets"
    )
    
    st.plotly_chart(fig, use_container_width=True)