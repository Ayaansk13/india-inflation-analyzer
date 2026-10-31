"""
Economic Indicators Page - Multi-Sector Inflation & Cross-Asset Dynamics.
Detailed analysis of MoSPI CPI basket categories, Wholesale Price Index (WPI),
global commodity benchmarks (Brent Crude, Gold), USD/INR, and RBI monetary policy.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

from config.settings import COLORS, CPI_BASKET_WEIGHTS
from config.styles import render_metric_card
from utils.plot_utils import plot_cpi_category_breakdown, plot_correlation_heatmap

def render_indicators_page(df: pd.DataFrame) -> None:
    """
    Renders the comprehensive Economic Indicators breakdown.
    """
    st.markdown("<h2>Macroeconomic & Sectoral Inflation Indicators</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Deconstructs price movements across official All-India Consumer Price Index (CPI) components, "
        "Wholesale Price Index (WPI), and imported commodity cost transmitters.</p>",
        unsafe_allow_html=True
    )

    latest = df.iloc[-1]
    prev_12m = df.iloc[-13] if len(df) >= 13 else df.iloc[0]

    # 1. Component Metric Row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(render_metric_card("FOOD & BEVERAGES", f"{latest['cpi_food_yoy']:.2f}%", "Weight: 45.86%", "pos" if latest['cpi_food_yoy'] > 5 else "neutral"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric_card("FUEL & LIGHT", f"{latest['cpi_fuel_yoy']:.2f}%", "Weight: 6.84%", "pos" if latest['cpi_fuel_yoy'] > 5 else "neutral"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_metric_card("HOUSING (RENT)", f"{latest['cpi_housing_yoy']:.2f}%", "Weight: 10.07%", "neutral"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_metric_card("CLOTHING & FOOTWEAR", f"{latest['cpi_clothing_yoy']:.2f}%", "Weight: 6.53%", "neutral"), unsafe_allow_html=True)
    with c5:
        st.markdown(render_metric_card("MISCELLANEOUS", f"{latest['cpi_misc_yoy']:.2f}%", "Weight: 28.32%", "neutral"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Category Trend Chart
    fig_cats = plot_cpi_category_breakdown(df)
    st.plotly_chart(fig_cats, use_container_width=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Macro Transmission: Commodities, Currency & Monetary Stance
    st.markdown("<h3>Imported Inflation & Transmission Drivers</h3>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        crude_val = latest["brent_crude_usd"]
        crude_12m_delta = ((crude_val - prev_12m["brent_crude_usd"]) / prev_12m["brent_crude_usd"]) * 100.0
        st.markdown(render_metric_card("BRENT CRUDE OIL", f"${crude_val:.2f}", f"{crude_12m_delta:+.1f}% YoY", "pos" if crude_12m_delta > 0 else "neg"), unsafe_allow_html=True)
    
    with m2:
        gold_val = latest["gold_inr_10g"]
        gold_12m_delta = ((gold_val - prev_12m["gold_inr_10g"]) / prev_12m["gold_inr_10g"]) * 100.0
        st.markdown(render_metric_card("MCX GOLD (10G)", f"INR {gold_val:,.0f}", f"{gold_12m_delta:+.1f}% YoY", "pos" if gold_12m_delta > 0 else "neutral"), unsafe_allow_html=True)

    with m3:
        fx_val = latest["usd_inr"]
        fx_12m_delta = ((fx_val - prev_12m["usd_inr"]) / prev_12m["usd_inr"]) * 100.0
        st.markdown(render_metric_card("USD / INR FX", f"INR {fx_val:.2f}", f"{fx_12m_delta:+.1f}% YoY", "pos" if fx_12m_delta > 0 else "neutral"), unsafe_allow_html=True)

    with m4:
        repo_val = latest["repo_rate"]
        st.markdown(render_metric_card("RBI REPO RATE", f"{repo_val:.2f}%", "Monetary Stance", "neutral"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Correlation Matrix Heatmap
    col_heat, col_weights = st.columns([1.2, 0.8])
    with col_heat:
        fig_corr = plot_correlation_heatmap(df)
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_weights:
        st.markdown("<h3>Official MoSPI CPI Weights (2012=100)</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size: 0.85rem;'>The Central Statistics Office (CSO) assigns weights based on the All-India Consumer Expenditure Survey (CES):</p>",
            unsafe_allow_html=True
        )
        weights_data = []
        for cat, w in CPI_BASKET_WEIGHTS.items():
            curr_rate = latest.get(f"cpi_{cat.split()[0].lower()}_yoy", latest["cpi_general_yoy"])
            weights_data.append({
                "Basket Group": cat,
                "Weight (%)": f"{w:.2f}%",
                "Current YoY (%)": f"{curr_rate:.2f}%",
                "Contribution Share": f"{(w * curr_rate / 100.0):.2f}%"
            })
        weights_df = pd.DataFrame(weights_data)
        st.dataframe(weights_df, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="info-panel" style="margin-top: 1rem;">
            <div style="font-size: 0.825rem; font-weight: 600; color: {COLORS['text_primary']};">Economic Insight</div>
            <div style="font-size: 0.8rem; color: {COLORS['text_secondary']};">
                Food and Beverages comprises nearly 46% of the national consumer basket. Consequently, supply-side agro shocks
                heavily skew headline inflation even when core inflation (excluding food and fuel) remains anchored below 4.0%.
            </div>
        </div>
        """, unsafe_allow_html=True)
