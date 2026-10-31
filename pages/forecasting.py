"""
Forecasting Page - Multi-Horizon Projections & What-If Scenario Stress Testing.
Recursive XGBoost time-series forecasting for 1, 3, and 6-month horizons
with confidence interval ribbons and exogenous shock simulations.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

from config.settings import COLORS
from config.styles import render_metric_card
from models.forecaster import generate_multi_step_forecast, get_predefined_scenarios
from utils.plot_utils import plot_forecast_chart

def render_forecasting_page(df: pd.DataFrame) -> None:
    """
    Renders multi-horizon forecasting and scenario simulation engine.
    """
    st.markdown("<h2>Econometric Multi-Horizon Forecasting & Scenario Simulator</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Simulates recursive multi-step forward inflation trajectories (1 to 6 months ahead) "
        "conditioned on lag momentum, seasonal harmonics, and configurable macroeconomic shocks.</p>",
        unsafe_allow_html=True
    )

    # 1. Horizon & Scenario Controls
    c_scen, c_horiz = st.columns([1.5, 1.0])
    scenarios = get_predefined_scenarios()
    
    with c_scen:
        selected_scenario_name = st.selectbox(
            "Select Macroeconomic Scenario",
            options=list(scenarios.keys()),
            index=0
        )
        current_scenario = scenarios[selected_scenario_name]
        st.markdown(f"<p style='font-size: 0.8rem; color: {COLORS['text_muted']};'>{current_scenario['description']}</p>", unsafe_allow_html=True)

    with c_horiz:
        horizon_months = st.slider("Forecast Horizon (Months Ahead)", min_value=1, max_value=6, value=6, step=1)

    # Optional Custom Shock Override Expander
    with st.expander("Custom What-If Scenario Adjustments (Fine-Tuning)", expanded=False):
        st.markdown("<p style='font-size: 0.85rem;'>Adjust specific exogenous parameters to simulate non-standard economic stress tests:</p>", unsafe_allow_html=True)
        cs1, cs2, cs3 = st.columns(3)
        base_shocks = current_scenario["shocks"].copy()
        with cs1:
            custom_crude = st.slider("Crude Oil Price Shock (%)", min_value=-50.0, max_value=80.0, value=float(base_shocks.get("crude_pct", 0.0)), step=5.0)
        with cs2:
            custom_food = st.slider("Food Price Component Shock (pts)", min_value=-5.0, max_value=10.0, value=float(base_shocks.get("food_shock_pts", 0.0)), step=0.5)
        with cs3:
            custom_repo = st.slider("RBI Repo Rate Shift (bps)", min_value=-150.0, max_value=200.0, value=float(base_shocks.get("repo_rate_delta_bps", 0.0)), step=25.0)
        
        active_shocks = {
            "crude_pct": custom_crude,
            "food_shock_pts": custom_food,
            "repo_rate_delta_bps": custom_repo
        }

    # 2. Compute Multi-Step Forecasts (Baseline vs Selected Scenario)
    with st.spinner("Generating recursive XGBoost forecast vectors..."):
        forecast_df = generate_multi_step_forecast(df, horizon_months=horizon_months, scenario_adjustments=active_shocks)
        baseline_df = generate_multi_step_forecast(df, horizon_months=horizon_months, scenario_adjustments={"crude_pct": 0, "food_shock_pts": 0, "repo_rate_delta_bps": 0})

    # 3. Forecast Metric Cards (1M, 3M, 6M)
    f_cols = st.columns(min(horizon_months, 3))
    
    if len(f_cols) >= 1 and len(forecast_df) >= 1:
        row1 = forecast_df.iloc[0]
        with f_cols[0]:
            st.markdown(render_metric_card(
                "NEXT MONTH (+1M)",
                f"{row1['cpi_forecast']:.2f}%",
                f"95% CI: [{row1['cpi_forecast_lower']:.2f}% - {row1['cpi_forecast_upper']:.2f}%]",
                "neutral"
            ), unsafe_allow_html=True)

    if len(f_cols) >= 2 and len(forecast_df) >= 3:
        row3 = forecast_df.iloc[2]
        with f_cols[1]:
            st.markdown(render_metric_card(
                "QUARTERLY (+3M)",
                f"{row3['cpi_forecast']:.2f}%",
                f"95% CI: [{row3['cpi_forecast_lower']:.2f}% - {row3['cpi_forecast_upper']:.2f}%]",
                "neutral"
            ), unsafe_allow_html=True)

    if len(f_cols) >= 3 and len(forecast_df) >= 6:
        row6 = forecast_df.iloc[5]
        with f_cols[2]:
            st.markdown(render_metric_card(
                "HALF-YEAR (+6M)",
                f"{row6['cpi_forecast']:.2f}%",
                f"95% CI: [{row6['cpi_forecast_lower']:.2f}% - {row6['cpi_forecast_upper']:.2f}%]",
                "neutral"
            ), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Interactive Forecast Chart
    fig_fc = plot_forecast_chart(df, forecast_df)
    st.plotly_chart(fig_fc, use_container_width=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 5. Projection Data Table & Divergence
    st.markdown("<h3>Forecast Trajectory Breakdown</h3>", unsafe_allow_html=True)
    
    display_fc = forecast_df.copy()
    display_fc["Baseline Point"] = baseline_df["cpi_forecast"]
    display_fc["Scenario Divergence"] = display_fc["cpi_forecast"] - display_fc["Baseline Point"]
    display_fc["Target Period"] = display_fc["date"].dt.strftime("%B %Y")
    
    table_fc = display_fc[[
        "horizon", "Target Period", "cpi_forecast", "cpi_forecast_lower",
        "cpi_forecast_upper", "projected_cpi_index", "Baseline Point", "Scenario Divergence"
    ]].rename(columns={
        "horizon": "Horizon Step",
        "cpi_forecast": "Scenario Forecast (%)",
        "cpi_forecast_lower": "95% Lower Bound",
        "cpi_forecast_upper": "95% Upper Bound",
        "projected_cpi_index": "Projected CPI Index (2012=100)",
        "Baseline Point": "Baseline (%)",
        "Scenario Divergence": "Net Shock Impact (pts)"
    })

    st.dataframe(table_fc, use_container_width=True, hide_index=True)

    # Download Projection Data
    csv_bytes = table_fc.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Forecast Projections (CSV)",
        data=csv_bytes,
        file_name=f"cpi_forecast_{selected_scenario_name.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
