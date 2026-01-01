import streamlit as st
import plotly.graph_objects as go
from quant_a.strategies import run_ma_crossover_strategy, run_bollinger_strategy, get_performance_metrics
from quant_a.strategies import run_ai_strategy

def render_quant_a(df, asset_names_map):
    st.header("Single Asset Predictive Research")
    
    # Asset selection using the full name map
    selected_ticker = st.selectbox(
        "Select Instrument", 
        df.columns, 
        format_func=lambda x: f"{x} - {asset_names_map.get(x, '')}"
    )

    # --- TECHNICAL APPENDIX (Storytelling) ---
    with st.expander("🎓 Methodology & AI Architecture (Read More)", expanded=False):
        st.markdown("""
        ### Predictive Engine Architecture
        Our system utilizes a **Machine Learning Ensemble** approach (Voting Classifier) to stabilize directional signals. 
        It combines three distinct algorithms:
        1. **XGBoost**: Captures complex non-linear price patterns.
        2. **Random Forest**: Reduces variance and prevents over-fitting.
        3. **Logistic Regression**: Provides a stable linear baseline.

        **Statistical Rigor**: 
        Training is conducted via **TimeSeriesSplit**. This method strictly respects chronological order (never using future data to predict the past), effectively eliminating **look-ahead bias**.
        """)

    # --- STRATEGY CONTROLS ---
    st.divider()
    col_strat, col_params = st.columns([1, 2])
    
    with col_strat:
        strategy_type = st.radio("Backtesting Strategy", 
                                ["Buy & Hold", "AI Ensemble Strategy", "MA Crossover", "Bollinger Mean-Reversion"])
    
    with col_params:
        # Prepare single asset data
        asset_df = df[[selected_ticker]].rename(columns={selected_ticker: 'Close'})
        
        if strategy_type == "MA Crossover":
            s_win = st.slider("Short Window", 5, 50, 20)
            l_win = st.slider("Long Window", 51, 200, 100)
            results = run_ma_crossover_strategy(asset_df, s_win, l_win)
        
        elif strategy_type == "Bollinger Mean-Reversion":
            win = st.slider("Window", 10, 50, 20)
            std_dev = st.slider("Std Dev", 1.0, 3.0, 2.0, 0.5)
            results = run_bollinger_strategy(asset_df, win, std_dev)
            
        elif strategy_type == "AI Ensemble Strategy":
            threshold = st.slider("AI Confidence Threshold", 0.50, 0.70, 0.55, 0.01)
            results = run_ai_strategy(df, selected_asset=selected_ticker, threshold=threshold)
            
        else: # Buy & Hold
            results = run_ma_crossover_strategy(asset_df, 1, 2)
            results['Cumulative_PNL'] = results['Benchmark_PNL']

    # --- PERFORMANCE METRICS ---
    st.write("#### Performance Analytics")
    metrics = get_performance_metrics(results['Cumulative_PNL'])
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Return", f"{metrics['Total Return']:.2%}")
    m2.metric("Ann. Volatility", f"{metrics['Annual Vol']:.2%}")
    m3.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
    m4.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
    m5.metric("Hit Ratio", f"{metrics['Hit Ratio']:.2%}")

    # --- MAIN CHART (Double Curve Requirement) ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=results.index, y=results['Benchmark_PNL'], name="Benchmark (Price)", line=dict(color='gray', dash='dash')))
    fig.add_trace(go.Scatter(x=results.index, y=results['Cumulative_PNL'], name="Strategy Equity Curve", line=dict(color='#00FFCC', width=3)))
    
    fig.update_layout(title=f"Backtest: {strategy_type} vs Benchmark", template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

    # --- RISK INSIGHTS ---
    col_hist, col_dd = st.columns(2)
    with col_hist:
        st.write("#### Returns Distribution")
        st.bar_chart(results['Strategy_Returns'])
    with col_dd:
        st.write("#### Drawdown Analysis")
        peak = results['Cumulative_PNL'].cummax()
        dd = (results['Cumulative_PNL'] - peak) / peak
        st.area_chart(dd, color="#FF4B4B")