"""
Project Documentation Page - Academic & Technical Blueprint.
Includes Problem Statement, Objectives, Methodology, Mathematical Formulations,
Architecture Flow, Technology Stack, Data Sources, Machine Learning Workflow, and Future Scope.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from config.settings import COLORS, APP_VERSION

def render_documentation_page() -> None:
    """
    Renders comprehensive academic project documentation.
    """
    st.markdown("<h2>Academic Proposal & Engineering Documentation</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<p>Complete final-year B.Sc. Data Science capstone documentation. "
        f"Project Codename: <b>Parivar-Arth</b> | Version: <b>{APP_VERSION}</b></p>",
        unsafe_allow_html=True
    )

    tabs = st.tabs([
        "Executive Summary & Objectives",
        "System Architecture",
        "Econometric & ML Methodology",
        "Data Sources & Attributions",
        "Future Scope & Capstone Team"
    ])

    # --- TAB 1: EXECUTIVE SUMMARY & OBJECTIVES ---
    with tabs[0]:
        st.markdown("<h3>1. Problem Statement</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: {COLORS['card']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
            <p style="color: {COLORS['text_primary']}; line-height: 1.6; margin-bottom: 0.75rem;">
                In emerging economies like India, the official headline Consumer Price Index (CPI), published monthly by the
                Ministry of Statistics & Programme Implementation (MoSPI, Base 2012=100), measures price inflation across a fixed national
                consumption basket. However, headline CPI frequently fails to reflect the lived financial reality of individual households due to:
            </p>
            <ul style="color: {COLORS['text_secondary']}; margin-left: 1.5rem; line-height: 1.6;">
                <li><b>Aggregated Basket Disconnect:</b> While Food and Beverages carries an official 45.86% weight nationally, middle-class urban families often allocate 20-30% to housing and education, skewing actual purchasing power erosion.</li>
                <li><b>Asymmetric Category Shocks:</b> Food perishables (vegetables, pulses) and fuel exhibit extreme localized volatility, inducing abrupt micro-budget deficits.</li>
                <li><b>Absence of Predictive Tools:</b> Consumers lack proactive, forward-looking personal inflation estimators to hedge future expenses before price rises materialize.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3>2. Project Objectives</h3>", unsafe_allow_html=True)
        obj_col1, obj_col2 = st.columns(2)
        with obj_col1:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1rem 1.25rem; height: 100%;">
                <div style="font-weight: 700; color: {COLORS['primary']}; margin-bottom: 0.35rem;">1. Macroeconometric Data Engineering</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                    Construct an automated ETL pipeline that harmonizes 10+ years of monthly All-India CPI indices, Wholesale Price Index (WPI),
                    global Brent crude, MCX gold benchmarks, and RBI repo rate policy decisions into an auditable SQLite repository.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with obj_col2:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1rem 1.25rem; height: 100%;">
                <div style="font-weight: 700; color: {COLORS['primary']}; margin-bottom: 0.35rem;">2. Out-of-Sample Machine Learning</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                    Train an XGBoost regressor with econometric lag structures, rolling volatility statistics, and cyclical seasonal harmonics
                    validated via Time-Series Cross-Validation to prevent lookahead bias.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        obj_col3, obj_col4 = st.columns(2)
        with obj_col3:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1rem 1.25rem; height: 100%;">
                <div style="font-weight: 700; color: {COLORS['primary']}; margin-bottom: 0.35rem;">3. Micro-Level Personal Cost Predictor</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                    Build a granular 10-category household expense simulator computing personal weighted inflation rates,
                    expected monetary cost escalations, and future expenditure curves.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with obj_col4:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1rem 1.25rem; height: 100%;">
                <div style="font-weight: 700; color: {COLORS['primary']}; margin-bottom: 0.35rem;">4. Dynamic Mitigation & Reporting</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                    Synthesize sector-specific actionable savings recommendations conditioned on top inflation drivers,
                    complete with automated publication-grade PDF dossier generation.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 2: SYSTEM ARCHITECTURE ---
    with tabs[1]:
        st.markdown("<h3>End-to-End System Architecture</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: {COLORS['card']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="font-family: monospace; font-size: 0.85rem; color: {COLORS['text_primary']}; line-height: 1.8;">
                [ DATA SOURCES: MoSPI CPI + OEA WPI + Brent Crude + MCX Gold + RBI Repo Rate ]<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
                [ ETL PIPELINE: Deduplication + Spline Imputation + 4.5σ Outlier Capping ]<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
                [ RELATIONAL STORAGE: SQLite (data/inflation_data.db) ]<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
                [ FEATURE ENGINEERING: Lags (t-1..t-12) + 3M/6M/12M Rolling Mean/Std + Sin/Cos Seasonality ]<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
                [ MACHINE LEARNING: XGBoost Regressor (TimeSeriesSplit 5-Fold CV + Joblib Persistence) ]<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br/>
                [ APPLICATION INTERFACES: Streamlit Bloomberg UI + Plotly + ReportLab PDF Engine ]
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Software Engineering Architecture</h3>", unsafe_allow_html=True)
        tech_data = [
            {"Subsystem": "Frontend Presentation", "Technologies": "Streamlit, Custom CSS/HTML, Plotly Graph Objects", "Role": "High-density FinTech dark theme without emojis"},
            {"Subsystem": "Data Engineering & Storage", "Technologies": "Pandas, NumPy, SQLite, yfinance", "Role": "ETL, data cleaning, relational audit logging"},
            {"Subsystem": "Machine Learning", "Technologies": "XGBoost, Scikit-learn, TimeSeriesSplit", "Role": "Econometric regression, out-of-sample CV, feature importance"},
            {"Subsystem": "Persistence & Serialisation", "Technologies": "Joblib, JSON", "Role": "Model weights, hyperparameter checkpoints, metadata"},
            {"Subsystem": "Report Generation", "Technologies": "ReportLab Platypus", "Role": "Automated PDF dossier compilation"},
        ]
        st.dataframe(pd.DataFrame(tech_data), use_container_width=True, hide_index=True)

    # --- TAB 3: ECONOMETRIC & ML METHODOLOGY ---
    with tabs[2]:
        st.markdown("<h3>Mathematical & Algorithmic Formulations</h3>", unsafe_allow_html=True)

        st.markdown("#### 1. Year-on-Year (YoY) Inflation Rate Formula")
        st.latex(r"\pi_t^{\text{YoY}} = \left( \frac{\text{CPI}_t - \text{CPI}_{t-12}}{\text{CPI}_{t-12}} \right) \times 100\%")

        st.markdown("#### 2. Personal Weighted Household Inflation Index")
        st.latex(r"\pi_{\text{personal}} = \sum_{k=1}^{K} w_k \cdot \pi_k, \quad \text{where } w_k = \frac{E_k}{\sum_{j=1}^K E_j}")
        st.markdown(
            r"<p style='font-size: 0.85rem;'>Where $E_k$ denotes the monthly expenditure allocated to category $k$, "
            r"and $\pi_k$ is the sector-specific YoY price change.</p>",
            unsafe_allow_html=True
        )

        st.markdown("#### 3. XGBoost Objective Function with Regularization")
        st.latex(r"\mathcal{L}^{(t)} = \sum_{i=1}^n \left[ g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2")
        st.markdown(
            r"<p style='font-size: 0.85rem;'>Where $g_i$ and $h_i$ are first and second-order gradient statistics of the MSE loss function, "
            r"and $\gamma, \lambda$ regularize tree complexity to mitigate overfitting on cyclical shocks.</p>",
            unsafe_allow_html=True
        )

        st.markdown("#### 4. Model Evaluation Metrics")
        st.latex(r"\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2}, \quad \text{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|, \quad R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}")

    # --- TAB 4: DATA SOURCES & ATTRIBUTIONS ---
    with tabs[3]:
        st.markdown("<h3>Authoritative Data Sources & MoSPI Standards</h3>", unsafe_allow_html=True)
        sources = [
            {
                "Organization": "Ministry of Statistics & Programme Implementation (MoSPI)",
                "Dataset": "All-India Consumer Price Index (Rural, Urban, Combined) Base 2012=100",
                "Frequency": "Monthly (released on 12th of each month)",
                "Link / Status": "Official MoSPI Open Data Portal"
            },
            {
                "Organization": "Office of the Economic Adviser (DPIIT, Ministry of Commerce)",
                "Dataset": "Wholesale Price Index (WPI) Base 2011-12=100",
                "Frequency": "Monthly (released around 14th of each month)",
                "Link / Status": "eaindustry.nic.in"
            },
            {
                "Organization": "Reserve Bank of India (RBI)",
                "Dataset": "Database on Indian Economy (DBIE) - Policy Repo Rate, USD/INR Reference",
                "Frequency": "Bi-monthly Monetary Policy Committee (MPC) & Daily FX",
                "Link / Status": "dbie.rbi.org.in"
            },
            {
                "Organization": "Intercontinental Exchange (ICE) / Multi Commodity Exchange (MCX)",
                "Dataset": "Brent Crude Spot (USD/bbl) & MCX Gold Futures (INR/10g)",
                "Frequency": "Daily / Monthly Settlement Averages",
                "Link / Status": "Financial Feeds via yfinance fallback"
            }
        ]
        st.dataframe(pd.DataFrame(sources), use_container_width=True, hide_index=True)

    # --- TAB 5: FUTURE SCOPE & TEAM ---
    with tabs[4]:
        st.markdown("<h3>Future Roadmap & Production Enhancements</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: {COLORS['card']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;">
            <ul style="color: {COLORS['text_secondary']}; margin-left: 1.5rem; line-height: 1.7;">
                <li><b>RBI MPC Sentiment NLP:</b> Integrate transformer-based sentiment analysis on bi-monthly Monetary Policy Committee meeting statements to incorporate hawkish/dovish forward guidance signals.</li>
                <li><b>State-Level Disaggregation:</b> Extend models to state-specific CPI baskets (e.g. Kerala vs Uttar Pradesh) accounting for regional food habits and tax structures.</li>
                <li><b>Open Banking Account Aggregator (AA):</b> Connect directly with RBI-regulated Account Aggregators (Setu, OneMoney) to auto-populate household expense transactions with bank-grade security.</li>
                <li><b>Deep Learning Hybrid Architectures:</b> Benchmark temporal fusion transformers (TFT) and N-BEATS against XGBoost for long-horizon recursive forecasting.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Final-Year Capstone Project Credentials</h3>", unsafe_allow_html=True)
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1.25rem;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {COLORS['primary']}; font-weight: 700;">Student Author & Lead Engineer</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: {COLORS['text_primary']}; margin: 0.25rem 0;">Ayaan & Project Team</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">Final-Year B.Sc. Data Science & Machine Learning</div>
            </div>
            """, unsafe_allow_html=True)
        with c_t2:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1.25rem;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {COLORS['primary']}; font-weight: 700;">Faculty Supervision</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: {COLORS['text_primary']}; margin: 0.25rem 0;">Department of Data Science & Economics</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">University Capstone Advisory Board</div>
            </div>
            """, unsafe_allow_html=True)
