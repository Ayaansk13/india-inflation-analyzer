"""
Executive Reports Page - Automated PDF Dossier Generation.
Generates institutional-quality PDF reports with ReportLab containing
user expense inputs, inflation forecasts, dynamic recommendations, and model audit sign-offs.
"""

import os
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
from typing import Dict, Any

from config.settings import COLORS, REPORTS_DIR
from config.styles import render_metric_card
from utils.pdf_generator import generate_inflation_pdf_report
from models.trainer import load_saved_model_and_metadata
from models.forecaster import generate_multi_step_forecast
from pages.household_impact import get_latest_category_inflation_rates
from utils.recommendations import analyze_household_vulnerability, generate_savings_recommendations

def render_reports_page(df: pd.DataFrame) -> None:
    """
    Renders PDF Report configuration, generation, and file archive interface.
    """
    st.markdown("<h2>Executive Dossier & Downloadable PDF Reports</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Compile an institutional-grade PDF advisory brief combining your household's expense profile, "
        "model inflation forecasts, category cost escalations, dynamic savings mitigations, and econometric audit metrics.</p>",
        unsafe_allow_html=True
    )

    # 1. Retrieve Current Active Analysis
    if "latest_analysis" not in st.session_state:
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

    _, metadata = load_saved_model_and_metadata()
    if metadata is None:
        metadata = {}

    forecast_df = generate_multi_step_forecast(df, horizon_months=6)

    # 2. Executive Preview Cards
    st.markdown("<h3>Active Analysis Snapshot</h3>", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown(render_metric_card("CURRENT MONTHLY SPEND", f"INR {analysis['total_spend']:,.0f}", "Client Input Outlay", "neutral"), unsafe_allow_html=True)
    with p2:
        st.markdown(render_metric_card("PERSONAL INFLATION", f"{analysis['personal_inflation_rate']:.2f}%", "Effective Family CPI", "pos"), unsafe_allow_html=True)
    with p3:
        st.markdown(render_metric_card("EST. ANNUAL IMPACT", f"+INR {analysis['total_annual_increase']:,.0f}", "Annual Real Erosion", "pos"), unsafe_allow_html=True)
    with p4:
        st.markdown(render_metric_card("PRIMARY COST DRIVER", analysis["top_driver"].upper(), "Highest Escalation", "pos"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Report Generation Configuration Form
    st.markdown("<h3>Report Generation Parameters</h3>", unsafe_allow_html=True)
    
    c_name, c_notes = st.columns([1.2, 1.8])
    with c_name:
        client_name = st.text_input("Household / Client Account Name", value="Deshmukh Household")
    with c_notes:
        report_notes = st.text_input("Report Header Annotation / Notes", value="Q4 Strategic Personal Inflation Assessment")

    if st.button("Generate Executive PDF Report"):
        with st.spinner("Compiling ReportLab PDF dossier..."):
            pdf_path_str = generate_inflation_pdf_report(
                analysis_data=analysis,
                forecast_df=forecast_df,
                recommendations=recs,
                model_metadata=metadata,
                user_name=client_name
            )
            st.session_state["latest_pdf_generated"] = pdf_path_str
            st.success("PDF Dossier successfully compiled and verified!")

    # 4. Download Active Generated Report
    if "latest_pdf_generated" in st.session_state:
        pdf_file = Path(st.session_state["latest_pdf_generated"])
        if pdf_file.exists():
            with open(pdf_file, "rb") as f:
                pdf_bytes = f.read()
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="success-panel">
                <div style="font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">
                    Report Ready for Download
                </div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                    File: <code>{pdf_file.name}</code> | Size: {len(pdf_bytes) / 1024:.1f} KB | Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label=f"Download {pdf_file.name}",
                data=pdf_bytes,
                file_name=pdf_file.name,
                mime="application/pdf"
            )

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 5. Archive of Historical Reports in reports/ Directory
    st.markdown("<h3>Generated Reports Archive</h3>", unsafe_allow_html=True)
    existing_reports = sorted(REPORTS_DIR.glob("*.pdf"), key=os.path.getmtime, reverse=True)
    
    if existing_reports:
        rep_rows = []
        for rep in existing_reports[:8]:
            mtime = datetime.fromtimestamp(os.path.getmtime(rep)).strftime("%Y-%m-%d %H:%M")
            size_kb = os.path.getsize(rep) / 1024.0
            rep_rows.append({
                "Filename": rep.name,
                "Generation Timestamp": mtime,
                "File Size": f"{size_kb:.1f} KB",
                "Full Path": str(rep)
            })
        st.dataframe(pd.DataFrame(rep_rows)[["Filename", "Generation Timestamp", "File Size"]], use_container_width=True, hide_index=True)
    else:
        st.markdown(f"<p style='color: {COLORS['text_muted']}; font-size: 0.85rem;'>No archived reports yet. Click 'Generate Executive PDF Report' to compile your first dossier.</p>", unsafe_allow_html=True)
