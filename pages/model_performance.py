"""
Model Performance Page - Econometric Validation, Residual Diagnostics & Interactive Retraining.
Features XGBoost evaluation metrics (RMSE, MAE, MAPE, R²), baseline benchmarks (Random Forest, Ridge),
actual vs predicted overlays, residual analysis, feature importances, and interactive hyperparameter refitting.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any

from config.settings import COLORS, TARGET_COL
from config.styles import render_metric_card
from models.trainer import load_saved_model_and_metadata, train_and_evaluate_model
from utils.feature_engineering import build_features, get_feature_columns
from utils.plot_utils import (
    plot_actual_vs_predicted,
    plot_residual_distribution,
    plot_feature_importance,
    apply_fintech_theme
)
from utils.metrics import format_metric_explanation

def render_model_performance_page(df: pd.DataFrame) -> None:
    """
    Renders the dedicated Machine Learning model audit and performance diagnostics page.
    """
    st.markdown("<h2>Econometric Model Performance & Machine Learning Diagnostics</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p>Comprehensive statistical evaluation of the gradient boosted decision tree (XGBoost) model. "
        "Strictly evaluated on out-of-sample chronological test partitions to prevent lookahead data leakage.</p>",
        unsafe_allow_html=True
    )

    model, metadata = load_saved_model_and_metadata()
    if model is None or metadata is None:
        with st.spinner("Initializing first-run model training..."):
            res = train_and_evaluate_model(df)
            model = res["model"]
            metadata = res["metadata"]

    test_metrics = metadata.get("test_metrics", {})
    train_metrics = metadata.get("train_metrics", {})
    residual_diag = metadata.get("residual_diagnostics", {})

    # 1. Executive Metric KPI Cards
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.markdown(render_metric_card("TEST RMSE", f"{test_metrics.get('rmse', 0):.4f}", "Root Mean Sq Error", "neg"), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric_card("TEST MAE", f"{test_metrics.get('mae', 0):.4f}", "Mean Absolute Error", "neg"), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric_card("TEST MAPE", f"{test_metrics.get('mape', 0):.2f}%", "Pct Forecast Error", "neg"), unsafe_allow_html=True)
    with m4:
        st.markdown(render_metric_card("R-SQUARED (R2)", f"{test_metrics.get('r2', 0):.4f}", "Variance Explained", "pos"), unsafe_allow_html=True)
    with m5:
        dw = residual_diag.get("durbin_watson", 2.0)
        st.markdown(render_metric_card("DURBIN-WATSON", f"{dw:.3f}", "Serial Independence", "neutral"), unsafe_allow_html=True)
    with m6:
        st.markdown(render_metric_card("TRAIN/TEST SPLIT", f"{metadata.get('train_samples')}/{metadata.get('test_samples')}", "Chronological Split", "neutral"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Benchmark Comparison Table
    st.markdown("<h3>Algorithmic Benchmark Evaluation (Out-of-Sample Test Partition)</h3>", unsafe_allow_html=True)
    benchmarks = metadata.get("benchmark_comparison", {})
    bench_rows = []
    for model_name, bm in benchmarks.items():
        bench_rows.append({
            "Algorithm": model_name,
            "RMSE": bm.get("rmse"),
            "MAE": bm.get("mae"),
            "MAPE (%)": f"{bm.get('mape'):.2f}%",
            "R² Score": bm.get("r2"),
            "Max Absolute Error": bm.get("max_error")
        })
    bench_df = pd.DataFrame(bench_rows).sort_values("R² Score", ascending=False)
    st.dataframe(bench_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. Interactive Diagnostic Plots: Actual vs Predicted & Residuals
    feat_df = build_features(df, drop_na=True)
    feature_cols = metadata.get("feature_columns", get_feature_columns())
    X = feat_df[feature_cols].values
    y = feat_df[TARGET_COL].values
    dates = feat_df["date"]
    
    test_size = metadata.get("test_samples", 26)
    split_idx = len(X) - test_size
    X_test, y_test = X[split_idx:], y[split_idx:]
    dates_test = dates.iloc[split_idx:]
    y_pred_test = model.predict(X_test)

    c_plot1, c_plot2 = st.columns(2)
    with c_plot1:
        fig_avp = plot_actual_vs_predicted(dates_test, y_test, y_pred_test)
        st.plotly_chart(fig_avp, use_container_width=True)

    with c_plot2:
        fig_res = plot_residual_distribution(y_test, y_pred_test)
        st.plotly_chart(fig_res, use_container_width=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Feature Importance & Learning Curve
    c_feat, c_learn = st.columns(2)
    
    with c_feat:
        feature_ranks = metadata.get("feature_ranking", [])
        top_names = [f["feature"] for f in feature_ranks]
        top_vals = [f["importance"] for f in feature_ranks]
        fig_fi = plot_feature_importance(top_names, top_vals, top_n=10)
        st.plotly_chart(fig_fi, use_container_width=True)

    with c_learn:
        # Plot Learning Curve from metadata
        learning_data = metadata.get("learning_curve", [])
        if learning_data:
            lc_df = pd.DataFrame(learning_data)
            fig_lc = go.Figure()
            fig_lc.add_trace(go.Scatter(
                x=lc_df["sample_size"],
                y=lc_df["train_rmse"],
                mode="lines+markers",
                name="Train RMSE",
                line={"color": COLORS["text_secondary"], "width": 2}
            ))
            fig_lc.add_trace(go.Scatter(
                x=lc_df["sample_size"],
                y=lc_df["val_rmse"],
                mode="lines+markers",
                name="Validation RMSE",
                line={"color": COLORS["primary"], "width": 2.5}
            ))
            apply_fintech_theme(fig_lc, "LEARNING CURVE (SAMPLE SIZE VS. RMSE)")
            fig_lc.update_xaxes(title_text="Training Partition Sample Size")
            fig_lc.update_yaxes(title_text="RMSE Error")
            st.plotly_chart(fig_lc, use_container_width=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 5. Interactive Hyperparameter Retraining Panel
    st.markdown("<h3>Interactive Model Retraining & Hyperparameter Tuning</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem;'>Adjust hyperparameter constraints and trigger a live refit against the calibrated dataset:</p>", unsafe_allow_html=True)

    current_params = metadata.get("hyperparameters", {})

    hp1, hp2, hp3, hp4 = st.columns(4)
    with hp1:
        new_n_est = st.slider("n_estimators (Boosting Trees)", min_value=50, max_value=400, value=int(current_params.get("n_estimators", 150)), step=25)
    with hp2:
        new_depth = st.slider("max_depth (Tree Depth)", min_value=2, max_value=8, value=int(current_params.get("max_depth", 4)), step=1)
    with hp3:
        new_lr = st.slider("learning_rate (Shrinkage)", min_value=0.01, max_value=0.25, value=float(current_params.get("learning_rate", 0.05)), step=0.01)
    with hp4:
        new_sub = st.slider("subsample (Row Subsampling)", min_value=0.5, max_value=1.0, value=float(current_params.get("subsample", 0.85)), step=0.05)

    if st.button("Retrain XGBoost Model Now"):
        with st.spinner("Retraining model with Time-Series Cross-Validation..."):
            train_res = train_and_evaluate_model(
                df,
                n_estimators=new_n_est,
                max_depth=new_depth,
                learning_rate=new_lr,
                subsample=new_sub
            )
            st.success("Model successfully retrained and persisted to disk!")
            st.rerun()

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 6. Plain-Language Econometric Guide
    st.markdown("<h3>Metric Interpretation Guide</h3>", unsafe_allow_html=True)
    explanations = format_metric_explanation()
    e_cols = st.columns(len(explanations))
    for i, (key, info) in enumerate(explanations.items()):
        with e_cols[i]:
            st.markdown(f"""
            <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1rem; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 700; color: {COLORS['primary']}; text-transform: uppercase;">
                    {info['name']}
                </div>
                <div style="font-size: 0.825rem; color: {COLORS['text_primary']}; margin: 0.4rem 0;">
                    {info['meaning']}
                </div>
                <div style="font-size: 0.75rem; color: {COLORS['text_muted']}; border-top: 1px solid {COLORS['border']}; padding-top: 0.35rem;">
                    <b>Target:</b> {info['benchmark']}
                </div>
            </div>
            """, unsafe_allow_html=True)
