"""
Household Impact & Personal Cost Predictor Page.
Allows users to input granular category-wise expenses, computes personalized weighted inflation,
forecasts projected monthly/annual budgetary escalation, and logs simulations for auditing.
"""

import json
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

from config.settings import COLORS, HOUSEHOLD_CATEGORY_MAPPING
from config.styles import render_metric_card
from utils.recommendations import analyze_household_vulnerability, generate_savings_recommendations
from utils.plot_utils import plot_household_expense_breakdown, plot_category_inflation_impact
from utils.db import log_user_simulation

def get_latest_category_inflation_rates(df: pd.DataFrame) -> Dict[str, float]:
    """
    Extracts latest observed and model-derived sector inflation rates.
    """
    latest = df.iloc[-1]
    rates = {
        "Food": float(latest.get("cpi_food_yoy", 6.2)),
        "Fuel": float(latest.get("cpi_fuel_yoy", 5.5)),
        "Transport": float(latest.get("cpi_misc_yoy", 4.8) * 1.05),
        "Rent": float(latest.get("cpi_housing_yoy", 4.2)),
        "Healthcare": float(latest.get("cpi_misc_yoy", 4.8) * 1.15),
        "Education": float(latest.get("cpi_misc_yoy", 4.8) * 1.02),
        "Utilities": float(latest.get("cpi_fuel_yoy", 5.5) * 0.75),
        "Entertainment": float(latest.get("cpi_misc_yoy", 4.8) * 0.85),
        "Shopping": float(latest.get("cpi_clothing_yoy", 5.1)),
        "Other": float(latest.get("cpi_general_yoy", 4.8)),
    }
    return rates

def render_household_impact_page(df: pd.DataFrame) -> None:
    """
    Renders the Personal Cost Predictor form, metrics, and visualization impact.
    """
    st.markdown("<h2>Personal Cost Predictor & Household Inflation Impact</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Quantify your household's localized exposure to inflationary price pressure. "
        "Unlike the national CPI (which reflects an aggregate 1.4-billion population basket), "
        "your effective inflation rate is determined strictly by your family's personal spending distribution.</p>",
        unsafe_allow_html=True
    )

    category_rates = get_latest_category_inflation_rates(df)

    # 1. Budget Presets for Instant Evaluation
    st.markdown("<h3>Select Household Budget Preset</h3>", unsafe_allow_html=True)
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)

    presets = {
        "Middle-Class Family (₹65,000)": {
            "Food": 18000, "Fuel": 4500, "Transport": 3000, "Rent": 18000,
            "Healthcare": 3500, "Education": 7000, "Utilities": 3000,
            "Entertainment": 2500, "Shopping": 3500, "Other": 2000
        },
        "Metro Professional (₹1,15,000)": {
            "Food": 28000, "Fuel": 8000, "Transport": 6000, "Rent": 38000,
            "Healthcare": 5000, "Education": 5000, "Utilities": 6000,
            "Entertainment": 9000, "Shopping": 10000, "Other": 5000
        },
        "Budget Conservative (₹35,000)": {
            "Food": 13000, "Fuel": 2500, "Transport": 1800, "Rent": 9000,
            "Healthcare": 2000, "Education": 2500, "Utilities": 1800,
            "Entertainment": 800, "Shopping": 1000, "Other": 600
        }
    }

    if "household_expenses" not in st.session_state:
        st.session_state["household_expenses"] = presets["Middle-Class Family (₹65,000)"].copy()

    with p_col1:
        if st.button("Middle-Class Family (INR 65k)"):
            st.session_state["household_expenses"] = presets["Middle-Class Family (₹65,000)"].copy()
            st.rerun()
    with p_col2:
        if st.button("Metro Professional (INR 115k)"):
            st.session_state["household_expenses"] = presets["Metro Professional (₹1,15,000)"].copy()
            st.rerun()
    with p_col3:
        if st.button("Budget Conservative (INR 35k)"):
            st.session_state["household_expenses"] = presets["Budget Conservative (₹35,000)"].copy()
            st.rerun()
    with p_col4:
        if st.button("Reset Custom Input"):
            st.session_state["household_expenses"] = {k: 0.0 for k in HOUSEHOLD_CATEGORY_MAPPING.keys()}
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 2. Expense Input Grid
    st.markdown("<h3>Monthly Category Expenditures (INR)</h3>", unsafe_allow_html=True)
    
    current_inputs = st.session_state["household_expenses"]
    updated_expenses = {}

    col_left, col_right = st.columns(2)
    categories = list(HOUSEHOLD_CATEGORY_MAPPING.keys())
    half = len(categories) // 2

    with col_left:
        for cat in categories[:half]:
            meta = HOUSEHOLD_CATEGORY_MAPPING[cat]
            inf_label = f"Latest YoY: {category_rates.get(cat, 5.0):.2f}%"
            val = float(current_inputs.get(cat, 0.0))
            new_val = st.number_input(
                f"{cat} ({meta['description']}) - {inf_label}",
                min_value=0.0,
                max_value=1000000.0,
                value=val,
                step=500.0,
                key=f"input_{cat}"
            )
            updated_expenses[cat] = new_val

    with col_right:
        for cat in categories[half:]:
            meta = HOUSEHOLD_CATEGORY_MAPPING[cat]
            inf_label = f"Latest YoY: {category_rates.get(cat, 5.0):.2f}%"
            val = float(current_inputs.get(cat, 0.0))
            new_val = st.number_input(
                f"{cat} ({meta['description']}) - {inf_label}",
                min_value=0.0,
                max_value=1000000.0,
                value=val,
                step=500.0,
                key=f"input_{cat}"
            )
            updated_expenses[cat] = new_val

    st.session_state["household_expenses"] = updated_expenses

    # 3. Analyze Household Vulnerability
    analysis = analyze_household_vulnerability(updated_expenses, category_rates)
    recs = generate_savings_recommendations(analysis)

    # Save to session state for PDF generation and recommendations tab
    st.session_state["latest_analysis"] = analysis
    st.session_state["latest_recommendations"] = recs

    # Log to SQLite
    try:
        log_user_simulation(
            total_expense=analysis["total_spend"],
            personal_inflation=analysis["personal_inflation_rate"],
            add_monthly=analysis["total_monthly_increase"],
            add_annual=analysis["total_annual_increase"],
            top_driver=analysis["top_driver"],
            breakdown_json=json.dumps(updated_expenses)
        )
    except Exception:
        pass

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Impact Metric KPI Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    national_cpi = df["cpi_general_yoy"].iloc[-1]
    pers_inf = analysis["personal_inflation_rate"]
    inf_gap = pers_inf - national_cpi

    with k1:
        st.markdown(render_metric_card("TOTAL MONTHLY OUTLAY", f"INR {analysis['total_spend']:,.0f}", "Current Expenditure", "neutral"), unsafe_allow_html=True)
    with k2:
        gap_str = f"{inf_gap:+.2f}% vs National"
        delta_tag = "pos" if inf_gap > 0 else "neg"
        st.markdown(render_metric_card("PERSONAL INFLATION", f"{pers_inf:.2f}%", gap_str, delta_tag), unsafe_allow_html=True)
    with k3:
        st.markdown(render_metric_card("EST. EXTRA MONTHLY", f"+INR {analysis['total_monthly_increase']:,.0f}", "Purchasing Power Gap", "pos"), unsafe_allow_html=True)
    with k4:
        st.markdown(render_metric_card("EST. EXTRA ANNUAL", f"+INR {analysis['total_annual_increase']:,.0f}", "Annualized Depletion", "pos"), unsafe_allow_html=True)
    with k5:
        driver = analysis["top_driver"]
        driver_delta = analysis["top_driver_details"].get("monthly_increase", 0)
        st.markdown(render_metric_card("PRIMARY COST DRIVER", driver.upper(), f"+INR {driver_delta:,.0f} / mo", "pos"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 5. Visual Breakdown Charts
    ch_col1, ch_col2 = st.columns(2)

    with ch_col1:
        fig_donut = plot_household_expense_breakdown(updated_expenses)
        st.plotly_chart(fig_donut, use_container_width=True)

    # Prepare Impact Dataframe for Grouped Bar Chart
    impact_records = []
    for cat, d in analysis["category_breakdown"].items():
        impact_records.append({
            "Category": cat,
            "Current Expense": d["current_spend"],
            "Predicted Expense": d["current_spend"] + d["monthly_increase"],
            "Monthly Delta": d["monthly_increase"],
            "Annual Delta": d["annual_increase"],
            "Inflation Rate": d["inflation_rate"],
            "Share (%)": d["share_pct"]
        })
    impact_df = pd.DataFrame(impact_records)

    with ch_col2:
        fig_impact = plot_category_inflation_impact(impact_df)
        st.plotly_chart(fig_impact, use_container_width=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 6. Detailed Escalation Table
    st.markdown("<h3>Category Cost Escalation Matrix</h3>", unsafe_allow_html=True)
    
    display_table = impact_df[[
        "Category", "Current Expense", "Share (%)", "Inflation Rate",
        "Predicted Expense", "Monthly Delta", "Annual Delta"
    ]].rename(columns={
        "Current Expense": "Current Spend (INR)",
        "Inflation Rate": "Sector YoY Rate (%)",
        "Predicted Expense": "Projected Monthly (INR)",
        "Monthly Delta": "Additional Monthly (+INR)",
        "Annual Delta": "Additional Annual (+INR)"
    })

    st.dataframe(display_table, use_container_width=True, hide_index=True)

    # 7. Quick Navigation Action Buttons
    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("Proceed to Dynamic Savings Recommendations"):
            st.session_state["nav_selection"] = "Dynamic Recommendations"
            st.rerun()
    with b2:
        if st.button("Generate Downloadable Executive PDF Report"):
            st.session_state["nav_selection"] = "Reports"
            st.rerun()
