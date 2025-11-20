import streamlit as st
# Import shared utilities
from utils.data_loader import get_data
# Import Quant B specific modules
from quant_b.statistics import calculate_global_metrics, normalize_prices
from quant_b.visuals import plot_correlation_heatmap, plot_normalized_prices

# Page Configuration (Title, layout) - Must be the first Streamlit command
st.set_page_config(page_title="Finance Dashboard", layout="wide")

def main():
    st.title("💹 Asset Management Dashboard")
    st.markdown("---")

    # Create tabs for separation of duties (Quant A vs Quant B)
    tab_a, tab_b = st.tabs(["👤 Quant A (Single Asset)", "🚀 Quant B (Portfolio)"])

    # --- QUANT B MODULE (Portfolio Analysis) ---
    with tab_b:
        st.header("Multi-Asset Analysis & Correlation")
        
        # 1. User Inputs
        col1, col2 = st.columns(2)
        with col1:
            # Default assets: Tech stocks + Bitcoin + Gold
            default_tickers = "AAPL, MSFT, GOOGL, BTC-USD, GLD"
            tickers_input = st.text_input("Assets (comma separated)", default_tickers)
        with col2:
            period = st.selectbox("Analysis Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
            
        # 2. Trigger Analysis
        if st.button("Run Portfolio Analysis"):
            with st.spinner("Fetching market data..."):
                # A. Get Data (using the shared utility)
                df = get_data(tickers_input, period)
                
                # Check if we have enough data
                if not df.empty and len(df.columns) > 1:
                    
                    # B. Calculations (Backend)
                    returns, corr_matrix = calculate_global_metrics(df)
                    df_norm = normalize_prices(df)
                    
                    # C. Visualization (Frontend)
                    
                    # Row 1: Performance Chart
                    st.subheader("📈 Performance Comparison")
                    plot_normalized_prices(df_norm)
                    
                    # Row 2: Correlation Matrix
                    st.subheader("🔥 Correlation Matrix")
                    st.info("Red indicates high positive correlation. Blue indicates negative correlation.")
                    plot_correlation_heatmap(corr_matrix)
                    
                elif len(df.columns) == 1:
                    st.warning("Please select at least 2 assets to calculate correlations.")
                    # Still show the chart for the single asset
                    st.line_chart(df)
                else:
                    st.error("No data found. Please check ticker symbols.")

    # --- QUANT A MODULE (Placeholder for Louis) ---
    with tab_a:
        st.info("Module under construction by Quant A...")

# Entry point
if __name__ == "__main__":
    main()