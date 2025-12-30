import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import get_data
from quant_b.portfolio_manager import simulate_portfolio
from quant_b.statistics import calculate_global_metrics
from quant_b.visuals import plot_correlation_heatmap
from quant_b.risk import calculate_risk_metrics
from quant_b.optimization import optimize_portfolio

st.set_page_config(page_title="Asset Management Dashboard", layout="wide")

def main():
    st.title("Asset Management Dashboard")
    st.markdown("---")

    tab_a, tab_b = st.tabs(["Quant A (Single Asset)", "Quant B (Portfolio)"])

    with tab_b:
        st.header("Multi-Asset Portfolio Management")
        
        col1, col2 = st.columns(2)
        with col1:
            default_tickers = "AAPL, MSFT, TSLA, BTC-USD, GOLD, EURUSD=X, ^FCHI"
            tickers_input = st.text_input("Assets (comma separated)", default_tickers)
        with col2:
            period = st.selectbox("Analysis Period", ["6mo", "1y", "2y", "5y"], index=1)
            
        if st.button("Load Data & Run Analysis"):
            with st.spinner("Processing data and running simulations..."):
                
                df = get_data(tickers_input, period)
                
                if not df.empty and len(df.columns) > 1:
                    assets = df.columns.tolist()
                    num_assets = len(assets)
                    
                    st.success(f"Data loaded successfully for: {', '.join(assets)}")

                    # --- SECTION 1: ALLOCATION ---
                    with st.container(border=True):
                        st.subheader("1. Portfolio Allocation")
                        st.write("Define your custom weights below:")
                        
                        cols = st.columns(num_assets)
                        weights = []
                        
                        for i, asset in enumerate(assets):
                            default_w = 1.0 / num_assets
                            w = cols[i].number_input(f"{asset}", min_value=0.0, max_value=1.0, value=default_w, step=0.05)
                            weights.append(w)
                        
                        total_weight = sum(weights)
                        if abs(total_weight - 1.0) > 0.01:
                            st.warning(f"Warning: Weights sum to {total_weight:.2f}. They will be re-normalized to 100% automatically.")

                    # --- SECTION 2: PERFORMANCE ---
                    results = simulate_portfolio(df, weights)
                    metrics = results['metrics']

                    st.markdown("---")
                    with st.container(border=True):
                        st.subheader("2. Portfolio Performance")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Total Return", f"{metrics['Total Return']:.2%}", help="Cumulative return over the selected period.")
                        m2.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}", help="Risk measured by annualized standard deviation.")
                        m3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}", help="Risk-adjusted return. Higher is better.")
                        m4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}", help="Maximum peak-to-trough decline.")
                        
                        st.write("### Portfolio Trajectory (Growth of $1)")
                        
                        df_norm = (df / df.iloc[0]) 
                        df_combined = df_norm.copy()
                        df_combined["PORTFOLIO"] = results['cumulative_returns']
                        
                        fig = px.line(df_combined, title="Portfolio vs Individual Assets")
                        fig.update_traces(selector=dict(name="PORTFOLIO"), line=dict(width=4, color='white'))
                        st.plotly_chart(fig, use_container_width=True)

                    # --- SECTION 3: ADVANCED RISK ---
                    st.markdown("---")
                    with st.container(border=True):
                        st.subheader("3. Advanced Risk Analysis")
                        
                        col_risk1, col_risk2 = st.columns(2)
                        
                        with col_risk1:
                            st.write("#### Correlation Matrix")
                            _, corr_matrix = calculate_global_metrics(df)
                            plot_correlation_heatmap(corr_matrix)
                            
                        with col_risk2:
                            st.write("#### Value at Risk (VaR) Models")
                            risk_data = calculate_risk_metrics(results['daily_returns'])
                            
                            if risk_data:
                                c1, c2 = st.columns(2)
                                c1.metric("VaR Historical", f"{risk_data['VaR_Hist']:.2%}", 
                                         help="Maximum expected loss (95% confidence) based on past returns.")
                                c2.metric("VaR Parametric", f"{risk_data['VaR_Para']:.2%}", 
                                         help="Maximum expected loss (95% confidence) based on normal distribution.")
                                
                                st.metric("Expected Shortfall (CVaR)", f"{risk_data['CVaR_Hist']:.2%}", 
                                         help="Average loss in the worst 5% of cases (Historical).")

                    # --- SECTION 4: OPTIMIZATION ---
                    st.markdown("---")
                    with st.container(border=True):
                        st.subheader("4. Portfolio Optimization (Markowitz)")

                        with st.expander("See Optimized Allocation & Efficient Frontier", expanded=True):
                            opt_results = optimize_portfolio(df)
                            mc_data = opt_results['monte_carlo_results']
                            
                            col_opt1, col_opt2 = st.columns(2)
                            
                            with col_opt1:
                                st.write("#### Efficient Frontier (Monte Carlo)")
                                fig_eff = px.scatter(
                                    x=mc_data[0], y=mc_data[1], color=mc_data[2],
                                    labels={'x': 'Volatility', 'y': 'Return', 'color': 'Sharpe'},
                                    color_continuous_scale='Viridis'
                                )
                                fig_eff.add_trace(go.Scatter(
                                    x=[opt_results['volatility']], y=[opt_results['return']],
                                    mode='markers', marker=dict(color='red', size=15, symbol='star'),
                                    name='Optimal Portfolio'
                                ))
                                st.plotly_chart(fig_eff, use_container_width=True)
                                
                            with col_opt2:
                                st.write("#### Optimal Weights")
                                labels = list(opt_results['weights'].keys())
                                values = list(opt_results['weights'].values())
                                fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                                st.plotly_chart(fig_pie, use_container_width=True)
                                
                                st.metric("Max Sharpe Ratio", f"{opt_results['sharpe']:.2f}")
                                st.success("The red star is the portfolio with the highest risk-adjusted return.")
                else:
                    st.error("Insufficient data. Please select at least 2 valid assets.")

    with tab_a:
        st.info("Module under development by Quant A Team Member.")

if __name__ == "__main__":
    main()