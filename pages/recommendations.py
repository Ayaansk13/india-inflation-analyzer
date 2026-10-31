"""
Dynamic Recommendations Page - Targeted Inflation Mitigation Strategies.
Analyzes household vulnerabilities and generates customized, non-static saving actions
tailored to the top inflation driver (Food, Fuel, Housing, Healthcare, etc.).
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from config.settings import COLORS
from config.styles import render_metric_card
from utils.recommendations import analyze_household_vulnerability, generate_savings_recommendations
from pages.household_impact import get_latest_category_inflation_rates

def render_recommendations_page(df: pd.DataFrame) -> None:
    """
    Renders dynamic, sector-tailored inflation mitigation strategies.
    """
    st.markdown("<h2>Dynamic Savings Recommendations & Mitigation Engine</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Algorithmic optimization engine generating non-static, high-ROI financial actions. "
        "Every recommendation is dynamically conditioned on your highest inflation expenditure driver "
        "and your discretionary spending ratios.</p>",
        unsafe_allow_html=True
    )

    # 1. Retrieve or Initialize User Analysis
    if "latest_analysis" not in st.session_state or "latest_recommendations" not in st.session_state:
        category_rates = get_latest_category_inflation_rates(df)
        default_expenses = {
            "Food": 18000, "Fuel": 4500, "Transport": 3000, "Rent": 18000,
            "Healthcare": 3500, "Education": 7000, "Utilities": 3000,
            "Entertainment": 2500, "Shopping": 3500, "Other": 2000
        }
        analysis = analyze_household_vulnerability(default_expenses, category_rates)
        recs = generate_savings_recommendations(analysis)
        st.session_state["latest_analysis"] = analysis
        st.session_state["latest_recommendations"] = recs
    else:
        analysis = st.session_state["latest_analysis"]
        recs = st.session_state["latest_recommendations"]

    # 2. Executive Synthesis Metric Cards
    top_driver = analysis["top_driver"]
    driver_info = analysis["top_driver_details"]
    monthly_extra = analysis["total_monthly_increase"]
    total_savings = sum(r["estimated_savings_monthly"] for r in recs[:-1])  # exclude reserve summary
    net_cushion = total_savings - monthly_extra

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(render_metric_card("HIGHEST INFLATION DRIVER", top_driver.upper(), f"+INR {driver_info.get('monthly_increase', 0):,.0f} / mo", "pos"), unsafe_allow_html=True)
    with r2:
        st.markdown(render_metric_card("EST. MONTHLY INFLATION GAP", f"INR {monthly_extra:,.0f}", "Purchasing Power Deficit", "pos"), unsafe_allow_html=True)
    with r3:
        st.markdown(render_metric_card("RECOVERABLE SAVINGS", f"INR {total_savings:,.0f}", "Monthly Mitigation Potential", "neg"), unsafe_allow_html=True)
    with r4:
        cushion_tag = "neg" if net_cushion >= 0 else "pos"
        cushion_str = f"+INR {net_cushion:,.0f} Surplus" if net_cushion >= 0 else f"-INR {abs(net_cushion):,.0f} Deficit"
        st.markdown(render_metric_card("NET PURCHASING BUFFER", cushion_str, "After Recommended Actions", cushion_tag), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Dynamic Strategy Panels
    st.markdown(f"<h3>Targeted Financial Strategies for {top_driver} Exposure</h3>", unsafe_allow_html=True)

    for i, r in enumerate(recs):
        priority = r["priority"]
        border_color = COLORS["primary"]
        badge_bg = COLORS["primary_subtle"]
        badge_color = COLORS["primary"]

        if priority == "HIGH":
            border_color = COLORS["warning"]
            badge_bg = COLORS["warning_subtle"]
            badge_color = COLORS["warning"]
        elif priority == "MEDIUM":
            border_color = COLORS["primary"]
            badge_bg = COLORS["primary_subtle"]
            badge_color = COLORS["primary"]

        st.markdown(f"""
        <div style="background: {COLORS['card']}; border: 1px solid {COLORS['border']}; border-left: 4px solid {border_color}; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
                <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: {COLORS['text_muted']};">
                    {r['category']} &nbsp;|&nbsp; <span style="background: {badge_bg}; color: {badge_color}; padding: 2px 6px; border-radius: 4px; font-weight: 700;">{priority} PRIORITY</span>
                </div>
                <div style="font-size: 0.95rem; font-weight: 700; color: {COLORS['success']};">
                    Est. Monthly Savings: INR {r['estimated_savings_monthly']:,.0f}
                </div>
            </div>
            <div style="font-size: 1.1rem; font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.5rem;">
                {r['title']}
            </div>
            <div style="font-size: 0.9rem; color: {COLORS['text_secondary']}; line-height: 1.5; margin-bottom: 0.75rem;">
                {r['action']}
            </div>
            <div style="font-size: 0.75rem; color: {COLORS['text_muted']};">
                Implementation Timeframe: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{r['implementation_timeframe']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Net Resiliency Evaluation Panel
    if net_cushion >= 0:
        st.markdown(f"""
        <div class="success-panel">
            <div style="font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">
                Purchasing Power Neutrality Achieved
            </div>
            <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                By executing these targeted operational adjustments, your household fully offsets the projected 
                <b>INR {monthly_extra:,.0f}</b> monthly inflation drag and generates an additional <b>INR {net_cushion:,.0f}</b> 
                in monthly discretionary surplus (<b>INR {net_cushion * 12:,.0f}</b> annually).
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-panel">
            <div style="font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">
                Severe Inflation Drag Detected
            </div>
            <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                The targeted sector optimizations recover <b>INR {total_savings:,.0f}</b> per month, leaving an unhedged 
                gap of <b>INR {abs(net_cushion):,.0f}</b>. Consider reviewing discretionary expenditures or exploring 
                additional income indexation.
            </div>
        </div>
        """, unsafe_allow_html=True)
