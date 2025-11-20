import streamlit as st
# Import shared utilities
from utils.data_loader import get_data
# Import Quant B specific modules
from quant_b.statistics import calculate_global_metrics, normalize_prices
from quant_b.visuals import plot_correlation_heatmap, plot_normalized_prices

# Page Configuration (Must be the first command)
st.set_page_config(page_title="Asset Management Dashboard", layout="wide")

def main():
    st.title("Asset Management Dashboard")
    st.markdown("---")

    # Create tabs for the two main modules
    tab_a, tab_b = st.tabs(["Quant A (Single Asset)", "Quant B (Portfolio)"])

    # --- QUANT B MODULE (Portfolio Analysis) ---
    with tab_b:
        st.header("Multi-Asset Analysis")
        
        # 1. User Inputs
        col1, col2 = st.columns(2)
        with col1:
            default_tickers = "AAPL, MSFT, GOOGL, BTC-USD, GLD"
            tickers_input = st.text_input("Assets (comma separated)", default_tickers)
        with col2:
            period = st.selectbox("Analysis Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
            
        # 2. Trigger Analysis Button
        if st.button("Run Portfolio Analysis"):
            with st.spinner("Fetching market data..."):
                # A. Data Fetching (Shared Module)
                df = get_data(tickers_input, period)
                
                # Check if we have valid data and enough assets
                if not df.empty and len(df.columns) > 1:
                    
                    # B. Calculations (Backend)
                    returns, corr_matrix = calculate_global_metrics(df)
                    df_norm = normalize_prices(df)
                    
                    # C. Visualization (Frontend)
                    
                    # Section 1: Performance Chart
                    st.subheader("Performance Comparison")
                    plot_normalized_prices(df_norm)
                    
                    # Section 2: Correlation Matrix
                    st.subheader("Correlation Analysis")
                    st.info("Correlation values range from -1 (Inverse) to +1 (Identical movement).")
                    plot_correlation_heatmap(corr_matrix)
                    
                elif len(df.columns) == 1:
                    st.warning("Please select at least 2 assets to calculate correlations.")
                    # Still display the chart for the single asset
                    st.line_chart(df)
                else:
                    st.error("No data found. Please check the ticker symbols.")

    # --- QUANT A MODULE (Placeholder) ---
    with tab_a:
        st.info("Module under development by Quant A Team Member.")

# Application Entry Point
if __name__ == "__main__":
    main()