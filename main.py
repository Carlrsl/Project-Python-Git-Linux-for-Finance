import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Quant B Imports (Your Modules)
from utils.data_loader import get_data
from quant_b.portfolio_manager import simulate_portfolio
from quant_b.statistics import calculate_global_metrics
from quant_b.visuals import plot_correlation_heatmap
from quant_b.risk import calculate_risk_metrics
from quant_b.optimization import optimize_portfolio

# Quant A Imports (Louis's Modules)
from quant_a.strategies import run_ai_strategy, calculate_performance_metrics
from quant_a.visuals import plot_ai_strategy, display_ai_metrics
from quant_a.prediction import train_predict_ensemble

st.set_page_config(page_title="Multi-Asset Management AI Platform", layout="wide")

def main():
    st.title("Asset Management Dashboard")
    st.markdown("---")

    # The two main modules of the platform
    tab_a, tab_b = st.tabs(["📊 Quant A (Single Asset AI)", "📈 Quant B (Portfolio Management)"])

    # --- SHARED DATA LOADING ---
    default_tickers = "AAPL, MSFT, TSLA, BTC-USD, GOLD, EURUSD=X, ^FCHI"
    
    # Using a sidebar for shared parameters to keep the UI clean
    st.sidebar.header("Global Settings")
    tickers_input = st.sidebar.text_input("Assets for Portfolio", default_tickers)
    period = st.sidebar.selectbox("Analysis Period", ["6mo", "1y", "2y", "5y"], index=1)
    
    # Load data once for both tabs
    df = get_data(tickers_input, period)

    # --- TAB A: QUANT A (LOUIS) ---
    with tab_a:
        st.header("Single Asset Analysis & AI Prediction")
        
        if not df.empty:
            # Asset selection for Single Asset analysis
            asset_list = df.columns.tolist()
            selected_asset = st.selectbox("Select Asset to Analyze", asset_list)
            
            st.markdown("---")
            
            # Sub-tab for Quant A focus: Strategy Backtesting & ML
            col_a1, col_a2 = st.columns([2, 1])
            
            with col_a2:
                st.subheader("AI Model Configuration")
                st.write("Ensemble Model: XGBoost + Random Forest + Logistic Regression")
                if st.button("Run AI Backtest"):
                    with st.spinner("Training AI Ensemble..."):
                        # Run the strategy logic
                        strategy_results = run_ai_strategy(df, selected_asset)
                        ai_metrics = calculate_performance_metrics(strategy_results['Cumulative_AI'])
                        
                        # Display metrics
                        display_ai_metrics(ai_metrics)
                        
                        # Store in session state to keep results visible
                        st.session_state['ai_results'] = strategy_results
                        st.session_state['selected_asset_ai'] = selected_asset
            
            with col_a1:
                if 'ai_results' in st.session_state and st.session_state['selected_asset_ai'] == selected_asset:
                    plot_ai_strategy(st.session_state['ai_results'], selected_asset)
                else:
                    st.info("Select an asset and click 'Run AI Backtest' to see results.")
        else:
            st.error("Please ensure data is loaded in the sidebar.")

    # --- TAB B: QUANT B (CARL) ---
    with tab_b:
        st.header("Multi-Asset Portfolio Management")
        
        if not df.empty and len(df.columns) > 1:
            assets = df.columns.tolist()
            num_assets = len(assets)
            
            st.success(f"Data loaded successfully for: {', '.join(assets)}")

            # --- SYNERGY: AI INSIGHTS FOR PORTFOLIO ---
            with st.expander("💡 Smart Allocation Suggestion (Powered by Quant A)", expanded=False):
                if st.button("Generate AI Signals"):
                    bullish_assets = []
                    for asset in assets:
                        prob, _ = train_predict_ensemble(df, asset)
                        if prob > 0.55:
                            bullish_assets.append(f"**{asset}** ({prob:.1%})")
                    
                    if bullish_assets:
                        st.success(f"AI Signal: Strong bullish conviction on {', '.join(bullish_assets)}. Consider increasing these weights.")
                    else:
                        st.info("AI Signal: No strong conviction detected on these assets for the next period.")

            # --- SECTION 1: ALLOCATION ---
            with st.container(border=True):
                st.subheader("1. Portfolio Allocation")
                cols = st.columns(num_assets)
                weights = []
                for i, asset in enumerate(assets):
                    w = cols[i].number_input(f"{asset}", min_value=0.0, max_value=1.0, value=1.0/num_assets, step=0.05)
                    weights.append(w)
                
                if abs(sum(weights) - 1.0) > 0.01:
                    st.warning("Weights will be re-normalized to 100%.")

            # --- SECTION 2: PERFORMANCE ---
            results = simulate_portfolio(df, weights)
            metrics = results['metrics']

            with st.container(border=True):
                st.subheader("2. Portfolio Performance")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Return", f"{metrics['Total Return']:.2%}")
                m2.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
                m3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
                m4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
                
                df_combined = (df / df.iloc[0]).copy()
                df_combined["PORTFOLIO"] = results['cumulative_returns']
                fig = px.line(df_combined, title="Portfolio vs Individual Assets")
                fig.update_traces(selector=dict(name="PORTFOLIO"), line=dict(width=4, color='white'))
                st.plotly_chart(fig, use_container_width=True)

            # --- SECTION 3: ADVANCED RISK ---
            with st.container(border=True):
                st.subheader("3. Advanced Risk Analysis")
                col_risk1, col_risk2 = st.columns(2)
                with col_risk1:
                    _, corr_matrix = calculate_global_metrics(df)
                    plot_correlation_heatmap(corr_matrix)
                with col_risk2:
                    risk_data = calculate_risk_metrics(results['daily_returns'])
                    if risk_data:
                        c1, c2 = st.columns(2)
                        c1.metric("VaR Historical", f"{risk_data['VaR_Hist']:.2%}")
                        c2.metric("VaR Parametric", f"{risk_data['VaR_Para']:.2%}")
                        st.metric("Expected Shortfall (CVaR)", f"{risk_data['CVaR_Hist']:.2%}")

            # --- SECTION 4: OPTIMIZATION ---
            with st.container(border=True):
                st.subheader("4. Portfolio Optimization (Markowitz)")
                opt_results = optimize_portfolio(df)
                col_opt1, col_opt2 = st.columns(2)
                with col_opt1:
                    mc_data = opt_results['monte_carlo_results']
                    fig_eff = px.scatter(x=mc_data[0], y=mc_data[1], color=mc_data[2], color_continuous_scale='Viridis')
                    fig_eff.add_trace(go.Scatter(x=[opt_results['volatility']], y=[opt_results['return']], mode='markers', marker=dict(color='red', size=15, symbol='star')))
                    st.plotly_chart(fig_eff, use_container_width=True)
                with col_opt2:
                    fig_pie = go.Figure(data=[go.Pie(labels=list(opt_results['weights'].keys()), values=list(opt_results['weights'].values()), hole=.3)])
                    st.plotly_chart(fig_pie, use_container_width=True)
                    st.metric("Max Sharpe Ratio", f"{opt_results['sharpe']:.2f}")
        else:
            st.error("Insufficient data. Please select at least 2 valid assets.")

if __name__ == "__main__":
    main()
