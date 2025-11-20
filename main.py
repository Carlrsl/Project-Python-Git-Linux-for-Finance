import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Import shared utilities
from utils.data_loader import get_data

# Import Quant B specific modules
from quant_b.portfolio_manager import simulate_portfolio
from quant_b.statistics import calculate_global_metrics
from quant_b.visuals import plot_correlation_heatmap
from quant_b.risk import calculate_risk_metrics
from quant_b.optimization import optimize_portfolio

# Page Configuration (Must be the first command)
st.set_page_config(page_title="Asset Management Dashboard", layout="wide")

def main():
    st.title("Asset Management Dashboard")
    st.markdown("---")

    # Create tabs for the two main modules
    tab_a, tab_b = st.tabs(["Quant A (Single Asset)", "Quant B (Portfolio)"])

    # --- QUANT B MODULE (Portfolio Analysis) ---
    with tab_b:
        st.header("Multi-Asset Portfolio Management")
        
        # 1. Data Selection
        col1, col2 = st.columns(2)
        with col1:
            default_tickers = "AAPL, MSFT, GOOGL, BTC-USD"
            tickers_input = st.text_input("Assets (comma separated)", default_tickers)
        with col2:
            period = st.selectbox("Analysis Period", ["6mo", "1y", "2y", "5y"], index=1)
            
        # 2. Run Analysis Button
        if st.button("Load Data & Run Analysis"):
            with st.spinner("Processing data and running simulations..."):
                
                # A. Fetch Data
                df = get_data(tickers_input, period)
                
                # Check if data is valid
                if not df.empty and len(df.columns) > 1:
                    assets = df.columns.tolist()
                    num_assets = len(assets)
                    
                    st.success(f"Data loaded successfully for: {', '.join(assets)}")
                    
                    # --- SECTION 1: WEIGHT SELECTION ---
                    st.subheader("1. Portfolio Allocation")
                    st.write("Define your custom weights below:")
                    
                    # Create columns for weight inputs
                    cols = st.columns(num_assets)
                    weights = []
                    
                    # Dynamic input widgets based on number of assets
                    for i, asset in enumerate(assets):
                        # Default weight is Equal Weight (1/N)
                        default_w = 1.0 / num_assets
                        w = cols[i].number_input(f"{asset}", min_value=0.0, max_value=1.0, value=default_w, step=0.05)
                        weights.append(w)
                    
                    # Check if weights sum to 1 (Tolerance of 1%)
                    total_weight = sum(weights)
                    if abs(total_weight - 1.0) > 0.01:
                        st.warning(f"Warning: Weights sum to {total_weight:.2f}. They will be re-normalized to 100% automatically during simulation.")
                    
                    # --- SECTION 2: SIMULATION ---
                    # Run Portfolio Simulation
                    results = simulate_portfolio(df, weights)
                    metrics = results['metrics']
                    
                    st.markdown("---")
                    st.subheader("2. Portfolio Performance")
                    
                    # Display Key Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Total Return", f"{metrics['Total Return']:.2%}")
                    m2.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
                    m3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
                    m4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
                    
                    # Chart: Portfolio Curve vs Individual Assets
                    st.write("### Portfolio Trajectory (Growth of $1)")
                    
                    # Merge Portfolio data with individual asset data (normalized)
                    df_norm = (df / df.iloc[0]) # Normalize base 1
                    df_combined = df_norm.copy()
                    df_combined["PORTFOLIO"] = results['cumulative_returns']
                    
                    # Plotting
                    fig = px.line(df_combined, title="Portfolio vs Individual Assets")
                    # Highlight the Portfolio line (Thicker white line)
                    fig.update_traces(selector=dict(name="PORTFOLIO"), line=dict(width=4, color='white'))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # --- SECTION 3: RISK ANALYSIS ---
                    st.markdown("---")
                    st.subheader("3. Advanced Risk Analysis")
                    
                    col_risk1, col_risk2 = st.columns(2)
                    
                    with col_risk1:
                        st.write("#### Correlation Matrix")
                        # Reuse existing correlation function
                        _, corr_matrix = calculate_global_metrics(df)
                        plot_correlation_heatmap(corr_matrix)
                        
                    with col_risk2:
                        st.write("#### Value at Risk (VaR)")
                        # Calculate VaR and CVaR
                        risk_data = calculate_risk_metrics(results['daily_returns'])
                        
                        if risk_data:
                            st.info(f"Value at Risk (95%): {risk_data['VaR_95_Historical']:.2%}")
                            st.info(f"Expected Shortfall (CVaR): {risk_data['CVaR_95_Historical']:.2%}")
                            st.caption("Interpretation: With 95% confidence, the portfolio will not lose more than the VaR value in a single day.")
                    
                    # --- SECTION 4: OPTIMIZATION ---
                    st.markdown("---")
                    st.subheader("4. Portfolio Optimization (Markowitz)")
                    
                    st.write("Mathematical optimization to find the weights that maximize the Sharpe Ratio.")
                    
                    # Use an expander to keep the UI clean
                    with st.expander("See Optimized Allocation"):
                        with st.spinner("Running optimization algorithm..."):
                            opt_results = optimize_portfolio(df)
                            
                            col_opt1, col_opt2 = st.columns(2)
                            
                            with col_opt1:
                                st.write("#### Optimal Weights")
                                labels = list(opt_results['weights'].keys())
                                values = list(opt_results['weights'].values())
                                
                                fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                                st.plotly_chart(fig_pie, use_container_width=True)
                                
                            with col_opt2:
                                st.write("#### Optimized Metrics")
                                st.metric("Exp. Annual Return", f"{opt_results['return']:.2%}")
                                st.metric("Exp. Volatility", f"{opt_results['volatility']:.2%}")
                                st.metric("Max Sharpe Ratio", f"{opt_results['sharpe']:.2f}")
                                
                            st.success(f"Optimization improved Sharpe Ratio to {opt_results['sharpe']:.2f}")

                else:
                    st.error("Insufficient data. Please select at least 2 valid assets.")

    # --- QUANT A MODULE (Placeholder) ---
    with tab_a:
        st.info("Module under development by Quant A Team Member.")

# Application Entry Point
if __name__ == "__main__":
    main()