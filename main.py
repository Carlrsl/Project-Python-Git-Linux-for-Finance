import streamlit as st
import yfinance as yf

# Page Configuration (Must be the first command)
st.set_page_config(page_title="Finance Dashboard", layout="wide")

def main():
    st.title("Finance Dashboard - Carl & Louis")
    
    # Create Tabs
    tab_home, tab_quant_a, tab_quant_b = st.tabs(["Home", "Quant A", "Quant B (Portfolio)"])

    # --- HOME TAB ---
    with tab_home:
        st.header("Welcome")
        st.write("This dashboard is a collaborative project for Python for Finance.")
        st.info("Use the tabs above to navigate between modules.")

    # --- QUANT A TAB (Placeholder for Louis) ---
    with tab_quant_a:
        st.header("Single Asset Analysis")
        st.write("Analysis for a single asset will be here.")
        st.warning("Work in progress...")

    # --- QUANT B TAB (Portfolio Manager - YOUR WORK) ---
    with tab_quant_b:
        st.header("Portfolio Analysis Module")
        
        # 1. User Inputs
        col1, col2 = st.columns(2)
        with col1:
            tickers_input = st.text_input("Enter Assets (comma separated)", "AAPL, MSFT, GOOGL, BTC-USD")
        with col2:
            period_input = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
        
        # 2. Run Analysis Button
        if st.button("Run Analysis"):
            # Clean up the input list
            tickers_list = [x.strip().upper() for x in tickers_input.split(',')]
            
            # Import your function dynamically
            from quant_b.portfolio_manager import get_market_data, normalize_data
            
            st.write("Fetching data...")
            
            # Get Data
            df = get_market_data(tickers_list, period=period_input)
            
            # Display Data
            if not df.empty:
                st.success("Data loaded successfully!")
                
                # Plot Normalized Data
                st.subheader("Performance Comparison (Base 100)")
                df_normalized = normalize_data(df)
                st.line_chart(df_normalized)
            else:
                st.error("No data found. Please check the ticker symbols.")

# Entry point of the application
if __name__ == "__main__":
    main()