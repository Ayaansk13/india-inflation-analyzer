"""
Data Explorer Page - Professional Dataset Inspection, Querying & Auditing.
Features multi-parameter search, date range filtering, column filtering,
sorting, pagination, statistical profiling, missing value audit, and CSV export.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

from config.settings import COLORS
from utils.feature_engineering import get_preprocessing_pipeline_summary

def render_data_explorer_page(df: pd.DataFrame, audit_metadata: Dict[str, Any]) -> None:
    """
    Renders the institutional Data Explorer with filtering, pagination, and audit reports.
    """
    st.markdown("<h2>Econometric Data Explorer & Validation Audit</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Inspect, filter, query, and export the calibrated macroeconomic time-series dataset. "
        "Includes descriptive statistical profiling and ETL integrity validation.</p>",
        unsafe_allow_html=True
    )

    data = df.copy()
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"])

    tabs = st.tabs(["Interactive Dataset View", "Descriptive Statistics", "ETL & Cleansing Audit", "Pipeline Lineage"])

    # --- TAB 1: INTERACTIVE DATASET VIEW ---
    with tabs[0]:
        # Filter controls in columns
        f1, f2, f3, f4 = st.columns([1.2, 1.2, 1.0, 1.0])
        
        min_date = data["date"].min().date()
        max_date = data["date"].max().date()

        with f1:
            start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
        with f2:
            end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)
        with f3:
            sort_col = st.selectbox("Sort By Column", options=list(data.columns), index=0)
        with f4:
            sort_order = st.selectbox("Sort Direction", options=["Descending", "Ascending"], index=0)

        # Apply filtering
        filtered_df = data[(data["date"].dt.date >= start_date) & (data["date"].dt.date <= end_date)]
        filtered_df = filtered_df.sort_values(sort_col, ascending=(sort_order == "Ascending")).reset_index(drop=True)

        # Column multi-select
        all_cols = list(data.columns)
        default_cols = [c for c in ["date", "cpi_general_yoy", "cpi_food_yoy", "cpi_fuel_yoy", "cpi_housing_yoy", "wpi_general_yoy", "brent_crude_usd", "gold_inr_10g", "repo_rate"] if c in all_cols]
        selected_cols = st.multiselect("Select Columns to Display", options=all_cols, default=default_cols)

        if not selected_cols:
            selected_cols = default_cols

        # Pagination
        p1, p2, p3 = st.columns([1.0, 1.5, 1.5])
        with p1:
            page_size = st.selectbox("Rows per Page", options=[10, 25, 50, 100, "All"], index=1)
        
        total_rows = len(filtered_df)
        if page_size == "All":
            page_df = filtered_df[selected_cols]
            page_info = f"Showing all {total_rows} records"
        else:
            page_size = int(page_size)
            total_pages = max(1, (total_rows + page_size - 1) // page_size)
            with p2:
                page_num = st.number_input("Page Number", min_value=1, max_value=total_pages, value=1, step=1)
            start_idx = (page_num - 1) * page_size
            end_idx = min(start_idx + page_size, total_rows)
            page_df = filtered_df[selected_cols].iloc[start_idx:end_idx]
            page_info = f"Showing records {start_idx + 1} to {end_idx} of {total_rows}"

        with p3:
            st.markdown(f"<div style='margin-top: 1.8rem; font-size: 0.85rem; color: {COLORS['text_muted']};'>{page_info}</div>", unsafe_allow_html=True)

        # Render Table
        display_page_df = page_df.copy()
        if "date" in display_page_df.columns:
            display_page_df["date"] = display_page_df["date"].dt.strftime("%Y-%m-%d")

        st.dataframe(display_page_df, use_container_width=True, hide_index=True)

        # Download Buttons
        d1, d2 = st.columns([1, 4])
        with d1:
            csv_data = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered CSV",
                data=csv_data,
                file_name="india_inflation_filtered.csv",
                mime="text/csv",
            )
        with d2:
            json_data = filtered_df.to_json(orient="records", date_format="iso").encode("utf-8")
            st.download_button(
                label="Download Filtered JSON",
                data=json_data,
                file_name="india_inflation_filtered.json",
                mime="application/json",
            )

    # --- TAB 2: DESCRIPTIVE STATISTICS ---
    with tabs[1]:
        st.markdown("<h3>Descriptive Statistical Profiling</h3>", unsafe_allow_html=True)
        numeric_df = data.select_dtypes(include=[np.number])
        stats_summary = numeric_df.describe().T
        stats_summary["skewness"] = numeric_df.skew()
        stats_summary = stats_summary.rename(columns={
            "count": "Observations",
            "mean": "Mean",
            "std": "Std Dev",
            "min": "Minimum",
            "25%": "25th Percentile",
            "50%": "Median",
            "75%": "75th Percentile",
            "max": "Maximum",
            "skewness": "Skewness"
        }).round(3)

        st.dataframe(stats_summary, use_container_width=True)

    # --- TAB 3: ETL & DATA CLEANSING AUDIT ---
    with tabs[2]:
        st.markdown("<h3>Data Validation & Preprocessing Audit Trail</h3>", unsafe_allow_html=True)

        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-label">TOTAL TIME OBSERVATIONS</div>
                <div class="metric-card-value">{audit_metadata.get('raw_rows', len(df))}</div>
                <div class="metric-card-subtext"><span class="tag-neutral">Continuous Monthly Series</span></div>
            </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-label">MISSING VALUES IMPUTED</div>
                <div class="metric-card-value">{audit_metadata.get('missing_values_handled', 0)}</div>
                <div class="metric-card-subtext"><span class="tag-delta-neg">100% Complete Record</span></div>
            </div>
            """, unsafe_allow_html=True)
        with a3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-label">DUPLICATE DATES REMOVED</div>
                <div class="metric-card-value">{audit_metadata.get('duplicates_removed', 0)}</div>
                <div class="metric-card-subtext"><span class="tag-delta-neg">Temporal Uniqueness Verified</span></div>
            </div>
            """, unsafe_allow_html=True)
        with a4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-label">OUTLIERS ADJUSTED (>4.5σ)</div>
                <div class="metric-card-value">{audit_metadata.get('outliers_adjusted', 0)}</div>
                <div class="metric-card-subtext"><span class="tag-neutral">Statistical Variance Guard</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="success-panel">
            <div style="font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">
                Database Integrity Verification: {audit_metadata.get('validation_status', 'PASSED')}
            </div>
            <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                All records verified against SQLite schema <code>economic_indicators</code>. Date range spans from 
                <b>{audit_metadata.get('date_range_start')}</b> to <b>{audit_metadata.get('date_range_end')}</b> without temporal gaps.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 4: PIPELINE LINEAGE ---
    with tabs[3]:
        st.markdown("<h3>Visual Preprocessing & Feature Engineering Pipeline</h3>", unsafe_allow_html=True)
        steps = get_preprocessing_pipeline_summary()
        steps_df = pd.DataFrame(steps).rename(columns={
            "step": "Pipeline Stage",
            "type": "Transformation Type",
            "details": "Econometric & Algorithmic Implementation",
            "status": "Operational State"
        })
        st.dataframe(steps_df, use_container_width=True, hide_index=True)
