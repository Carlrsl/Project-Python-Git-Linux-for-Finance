import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from quant_b.portfolio_manager import simulate_portfolio
from quant_b.statistics import calculate_global_metrics
from quant_b.visuals import plot_correlation_heatmap
from quant_b.risk import calculate_risk_metrics
from quant_b.optimization import optimize_portfolio

def render_quant_b(df):
    st.header("Multivariate Portfolio Research & Optimization")
    
    if df.empty or len(df.columns) < 2:
        st.error("Please select at least 2 assets in the Control Panel to run Portfolio Analysis.")
        return

    assets = df.columns.tolist()
    num_assets = len(assets)

    # --- TECHNICAL APPENDIX ---
    with st.expander("🎓 Methodology: Modern Portfolio Theory (MPT)", expanded=False):
        st.markdown("""
        ### Portfolio Optimization Logic
        This module implements **Markowitz Mean-Variance Optimization**. 
        - **Objective**: Maximize the Sharpe Ratio (return per unit of risk).
        - **Efficient Frontier**: We use Monte Carlo simulations (5,000 iterations) to find the set of optimal portfolios that offer the highest expected return for a defined level of risk.
        - **Risk Decomposition**: We analyze correlations to ensure diversification benefits are maximized, reducing idiosyncratic risk.
        """)

    # --- SECTION 1: ALLOCATION STRATEGY ---
    st.divider()
    st.subheader("1. Asset Allocation & Weights")
    
    col_mode, col_info = st.columns([1, 2])
    with col_mode:
        mode = st.radio("Allocation Mode", ["Equal Weight", "Optimal Sharpe (Markowitz)"])

    if mode == "Optimal Sharpe (Markowitz)":
        with st.spinner("Calculating Optimal Frontier..."):
            opt_results = optimize_portfolio(df)
            weights_dict = opt_results['weights']
            weights = [weights_dict[asset] for asset in assets]
            st.success("Weights optimized for Maximum Sharpe Ratio.")
    else:
        weights = [1.0 / num_assets] * num_assets
        weights_dict = {asset: 1.0/num_assets for asset in assets}

    # Display Weights Sliders (Interactive Requirement)
    with st.container(border=True):
        cols = st.columns(min(num_assets, 4))
        display_weights = []
        for i, asset in enumerate(assets):
            with cols[i % 4]:
                w = st.number_input(f"{asset}", 0.0, 1.0, float(weights_dict[asset]), 0.05)
                display_weights.append(w)
        
        if abs(sum(display_weights) - 1.0) > 0.01:
            st.warning(f"Total Allocation: {sum(display_weights):.2%}. Normalizing to 100%...")

    # --- SECTION 2: PERFORMANCE COMPARISON ---
    results = simulate_portfolio(df, display_weights)
    metrics = results['metrics']

    st.subheader("2. Performance Benchmark")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Portfolio Return", f"{metrics['Total Return']:.2%}")
    m2.metric("Ann. Volatility", f"{metrics['Annual Volatility']:.2%}")
    m3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
    m4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")

    # MAIN CHART: Comparison Requirement (Portfolio vs all Assets)
    fig_comp = go.Figure()
    # Individual Assets (Translucent for clarity)
    for asset in assets:
        norm_series = df[asset] / df[asset].iloc[0]
        fig_comp.add_trace(go.Scatter(x=df.index, y=norm_series, name=asset, 
                                     line=dict(width=1, opacity=0.3), showlegend=True))
    
    # The Portfolio (Bold White)
    fig_comp.add_trace(go.Scatter(x=df.index, y=results['cumulative_returns'], 
                                 name="STRATEGIC PORTFOLIO", line=dict(width=4, color='white')))
    
    fig_comp.update_layout(title="Strategic Equity Curve vs. Universe Components", 
                           template="plotly_dark", height=500, hovermode="x unified")
    st.plotly_chart(fig_comp, use_container_width=True)

    # --- SECTION 3: RISK & OPTIMIZATION VISUALS ---
    st.divider()
    col_risk, col_opt = st.columns(2)

    with col_risk:
        st.subheader("Risk Decomposition")
        _, corr_matrix = calculate_global_metrics(df)
        plot_correlation_heatmap(corr_matrix)
        
        # VaR/CVaR Display
        risk_data = calculate_risk_metrics(results['daily_returns'])
        with st.container(border=True):
            st.write("**Tail Risk Analysis (95% Confidence)**")
            c1, c2 = st.columns(2)
            c1.metric("Historical VaR", f"{risk_data['VaR_Hist']:.2%}")
            c2.metric("Expected Shortfall (CVaR)", f"{risk_data['CVaR_Hist']:.2%}")

    with col_opt:
        st.subheader("Efficient Frontier (Monte Carlo)")
        if mode == "Optimal Sharpe (Markowitz)":
            mc_data = opt_results['monte_carlo_results']
            fig_eff = px.scatter(x=mc_data[0], y=mc_data[1], color=mc_data[2], 
                               labels={'x':'Volatility', 'y':'Return', 'color':'Sharpe'},
                               color_continuous_scale='Viridis')
            fig_eff.add_trace(go.Scatter(x=[opt_results['volatility']], y=[opt_results['return']], 
                                       mode='markers', marker=dict(color='red', size=15, symbol='star'),
                                       name='Optimal Point'))
            fig_eff.update_layout(template="plotly_dark")
            st.plotly_chart(fig_eff, use_container_width=True)
        else:
            st.info("Switch to 'Optimal Sharpe' to visualize the Efficient Frontier.")