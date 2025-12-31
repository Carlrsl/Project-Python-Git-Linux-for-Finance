import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Quant A Imports (Louis's Modules)
from quant_a.strategies import run_ai_strategy, calculate_performance_metrics
from quant_a.visuals import plot_ai_strategy, display_ai_metrics
from quant_a.prediction import train_predict_ensemble