import streamlit as st
from datetime import datetime
from utils.data_loader import get_data
# We import our new specialized app modules
from quant_a.app import render_quant_a
from quant_b.app import render_quant_b

ASSET_MAP = {
    "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Motors", "NVDA": "NVIDIA Corp.",
    "BTC-USD": "Bitcoin Core", "ETH-USD": "Ethereum", "GOLD": "Gold Bullion",
    "EURUSD=X": "EUR/USD Forex", "^FCHI": "CAC 40 Index", "^GSPC": "S&P 500 Index"
}

st.set_page_config(page_title="Institutional Quant Terminal", layout="wide")

def main():
    st.sidebar.title("🛡️ Institutional Terminal")
    menu = st.sidebar.radio("NAVIGATION", ["🏠 Overview", "📊 Quant A (Predictive)", "📈 Quant B (Portfolio)"])
    
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Settings")
    tickers = st.sidebar.text_input("Universe Tickers", ", ".join(ASSET_MAP.keys()))
    period = st.sidebar.selectbox("Horizon", ["1y", "2y", "5y"], index=0)
    
    df = get_data(tickers, period)

    if menu == "🏠 Overview":
        st.title("Executive Dashboard")
        st.markdown(f"*Last System Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        # Add high-level KPIs here
        st.info("Welcome to the Quantitative Research Platform. Use the sidebar to navigate.")

    elif menu == "📊 Quant A (Predictive)":
        render_quant_a(df, ASSET_MAP)

    elif menu == "📈 Quant B (Portfolio)":
        render_quant_b(df)

if __name__ == "__main__":
    main()