"""
Parivar-Arth: India Inflation Impact Analyzer & Personal Cost Predictor.
Primary Application Orchestrator & Multi-Page Navigation Router.
Strict Bloomberg / TradingView / Stripe Dark Analytics Theme (No Emojis).
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from config.settings import APP_NAME, APP_SUBTITLE, APP_VERSION, COLORS
from config.styles import get_custom_css, render_top_header
from data.data_loader import load_or_initialize_dataset
from pages.overview import render_overview_page
from pages.indicators import render_indicators_page
from pages.data_explorer import render_data_explorer_page
from pages.forecasting import render_forecasting_page
from pages.household_impact import render_household_impact_page
from pages.recommendations import render_recommendations_page
from pages.model_performance import render_model_performance_page
from pages.reports import render_reports_page
from pages.documentation import render_documentation_page
from pages.about import render_about_page

# Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom FinTech Stylesheet
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Application Pages Definition
NAV_PAGES = [
    "Overview",
    "Economic Indicators",
    "Data Explorer",
    "Forecasting",
    "Household Impact",
    "Dynamic Recommendations",
    "Model Performance",
    "Reports",
    "Project Documentation",
    "About"
]

# Synchronize Navigation State
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "Overview"

# 1. Top Executive Banner
st.markdown(render_top_header(active_page=st.session_state["nav_selection"]), unsafe_allow_html=True)

# 2. Bespoke Platform Navigation Bar
# Horizontal segmented control styled via CSS
current_idx = NAV_PAGES.index(st.session_state["nav_selection"]) if st.session_state["nav_selection"] in NAV_PAGES else 0

selected_page = st.radio(
    label="Platform Navigation",
    options=NAV_PAGES,
    index=current_idx,
    horizontal=True,
    label_visibility="collapsed",
    key="platform_nav_radio"
)

if selected_page != st.session_state["nav_selection"]:
    st.session_state["nav_selection"] = selected_page
    st.rerun()

st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

# 3. Ingest or Load Calibrated Historical Dataset
@st.cache_data(show_spinner=False)
def get_cached_dataset():
    return load_or_initialize_dataset(force_refresh=False)

try:
    df, audit_metadata = get_cached_dataset()
except Exception as e:
    st.error(f"ETL Pipeline Ingestion Error: {str(e)}")
    df, audit_metadata = pd.DataFrame(), {}

# 4. Route to Selected Page
active = st.session_state["nav_selection"]

if active == "Overview":
    render_overview_page(df)
elif active == "Economic Indicators":
    render_indicators_page(df)
elif active == "Data Explorer":
    render_data_explorer_page(df, audit_metadata)
elif active == "Forecasting":
    render_forecasting_page(df)
elif active == "Household Impact":
    render_household_impact_page(df)
elif active == "Dynamic Recommendations":
    render_recommendations_page(df)
elif active == "Model Performance":
    render_model_performance_page(df)
elif active == "Reports":
    render_reports_page(df)
elif active == "Project Documentation":
    render_documentation_page()
elif active == "About":
    render_about_page(df)

# Footer Note (Minimal, Clean)
st.markdown(f"""
<div style="margin-top: 3.5rem; padding-top: 1.25rem; border-top: 1px solid {COLORS['border']}; display: flex; justify-content: space-between; align-items: center; font-size: 0.775rem; color: {COLORS['text_muted']};">
    <div>
        <b>{APP_NAME}</b> &nbsp;|&nbsp; B.Sc. Data Science Final-Year Capstone & Enterprise Analytics Platform
    </div>
    <div>
        MoSPI Base 2012=100 &nbsp;|&nbsp; RBI FIT Framework &nbsp;|&nbsp; XGBoost Machine Learning Pipeline
    </div>
</div>
""", unsafe_allow_html=True)
