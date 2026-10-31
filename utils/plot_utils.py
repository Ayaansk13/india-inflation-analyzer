"""
Plotly Charting Utilities for Parivar-Arth.
Strict Bloomberg / TradingView Dark Analytics Theme (#0B1220 / #182234 / #3B82F6).
Zero emojis, high contrast, clean typography, responsive layout.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional

from config.settings import COLORS, RBI_INFLATION_TARGET, RBI_UPPER_TOLERANCE, RBI_LOWER_TOLERANCE

def apply_fintech_theme(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    """
    Applies unified institutional dark styling to Plotly figures.
    """
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"family": "Manrope, Inter, sans-serif", "size": 15, "color": COLORS["text_primary"]}
        },
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        height=height,
        margin={"l": 40, "r": 30, "t": 55, "b": 40},
        font={"family": "Inter, sans-serif", "color": COLORS["text_secondary"], "size": 12},
        hoverlabel={
            "bgcolor": COLORS["bg_secondary"],
            "font_size": 12,
            "font_family": "Inter, sans-serif",
            "font_color": COLORS["text_primary"],
            "bordercolor": COLORS["border"]
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1.0,
            "font": {"size": 11, "color": COLORS["text_secondary"]},
            "bgcolor": "rgba(0,0,0,0)"
        },
        xaxis={
            "gridcolor": COLORS["border"],
            "zerolinecolor": COLORS["border"],
            "tickfont": {"color": COLORS["text_muted"], "size": 11},
            "showline": True,
            "linecolor": COLORS["border"],
        },
        yaxis={
            "gridcolor": COLORS["border"],
            "zerolinecolor": COLORS["border"],
            "tickfont": {"color": COLORS["text_muted"], "size": 11},
            "showline": True,
            "linecolor": COLORS["border"],
        }
    )
    return fig

def plot_cpi_historical_trend(df: pd.DataFrame) -> go.Figure:
    """
    Renders headline CPI trend alongside the RBI Monetary Policy tolerance corridor.
    """
    fig = go.Figure()

    # RBI Tolerance Band (2.0% - 6.0%)
    fig.add_hrect(
        y0=RBI_LOWER_TOLERANCE,
        y1=RBI_UPPER_TOLERANCE,
        line_width=0,
        fillcolor="rgba(16, 185, 129, 0.08)",
        layer="below",
        annotation_text="RBI TARGET CORRIDOR (2.0% - 6.0%)",
        annotation_position="top left",
        annotation_font={"size": 10, "color": COLORS["success"]}
    )

    # RBI Midpoint Target Line (4.0%)
    fig.add_hline(
        y=RBI_INFLATION_TARGET,
        line_dash="dot",
        line_color=COLORS["warning"],
        line_width=1.2,
        annotation_text="4.0% MIDPOINT ANCHOR",
        annotation_position="bottom right",
        annotation_font={"size": 10, "color": COLORS["warning"]}
    )

    # Headline CPI YoY
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["cpi_general_yoy"],
        mode="lines",
        name="CPI General YoY (%)",
        line={"color": COLORS["primary"], "width": 2.5},
        hovertemplate="Date: %{x|%b %Y}<br>CPI Inflation: %{y:.2f}%<extra></extra>"
    ))

    apply_fintech_theme(fig, "INDIA HEADLINE CPI INFLATION (YOY) VS. RBI MONETARY CORRIDOR")
    fig.update_yaxes(title_text="Annual Inflation Rate (%)")
    return fig

def plot_cpi_category_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Multi-line comparative chart of primary CPI basket components.
    """
    fig = go.Figure()

    palette = {
        "Food & Beverages": "#10B981",
        "Fuel & Light": "#F59E0B",
        "Housing": "#8B5CF6",
        "Clothing & Footwear": "#EC4899",
        "Miscellaneous": "#06B6D4"
    }

    cols = [
        ("cpi_food_yoy", "Food & Beverages"),
        ("cpi_fuel_yoy", "Fuel & Light"),
        ("cpi_housing_yoy", "Housing"),
        ("cpi_clothing_yoy", "Clothing & Footwear"),
        ("cpi_misc_yoy", "Miscellaneous"),
    ]

    for col, name in cols:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df[col],
                mode="lines",
                name=name,
                line={"color": palette.get(name, COLORS["primary"]), "width": 1.8},
                hovertemplate=f"{name}: %{{y:.2f}}%<extra></extra>"
            ))

    apply_fintech_theme(fig, "CONSUMER PRICE INDEX: BASKET COMPONENT DYNAMICS (YOY %)")
    fig.update_yaxes(title_text="Component Inflation (%)")
    return fig

def plot_wpi_vs_cpi(df: pd.DataFrame) -> go.Figure:
    """
    Comparative pass-through trajectory: Wholesale Price Index (WPI) vs Consumer Price Index (CPI).
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["wpi_general_yoy"],
        mode="lines",
        name="WPI (Wholesale) YoY (%)",
        line={"color": "#F59E0B", "width": 2, "dash": "dash"},
        hovertemplate="WPI YoY: %{y:.2f}%<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["cpi_general_yoy"],
        mode="lines",
        name="CPI (Retail Consumer) YoY (%)",
        line={"color": COLORS["primary"], "width": 2.5},
        hovertemplate="CPI YoY: %{y:.2f}%<extra></extra>"
    ))

    apply_fintech_theme(fig, "PRODUCER TO CONSUMER TRANSMISSION: WPI VS. CPI")
    fig.update_yaxes(title_text="Annual Rate of Change (%)")
    return fig

def plot_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Institutional correlation matrix heatmap.
    """
    cols = [
        "cpi_general_yoy", "cpi_food_yoy", "cpi_fuel_yoy", "cpi_housing_yoy",
        "wpi_general_yoy", "brent_crude_usd", "gold_inr_10g", "usd_inr", "repo_rate"
    ]
    avail_cols = [c for c in cols if c in df.columns]
    labels = [
        c.replace("_yoy", "").replace("_usd", "").replace("_inr_10g", "").replace("_", " ").upper()
        for c in avail_cols
    ]

    corr = df[avail_cols].corr().values

    fig = go.Figure(data=go.Heatmap(
        z=corr,
        x=labels,
        y=labels,
        colorscale=[
            [0.0, "#EF4444"],
            [0.5, "#182234"],
            [1.0, "#3B82F6"]
        ],
        zmin=-1.0,
        zmax=1.0,
        colorbar={
            "title": "Corr",
            "titleside": "right",
            "tickcolor": COLORS["text_muted"],
            "tickfont": {"color": COLORS["text_secondary"]}
        },
        text=np.round(corr, 2),
        texttemplate="%{text}",
        textfont={"size": 10, "color": COLORS["text_primary"]}
    ))

    apply_fintech_theme(fig, "CROSS-ASSET & INFLATION CORRELATION MATRIX", height=460)
    fig.update_xaxes(tickangle=-35)
    return fig

def plot_forecast_chart(historical_df: pd.DataFrame, forecast_df: pd.DataFrame) -> go.Figure:
    """
    Renders historical CPI alongside 1M, 3M, 6M forward forecast with 95% confidence bands.
    """
    fig = go.Figure()

    # Recent historical slice (last 24 months for clarity)
    hist_slice = historical_df.tail(24)

    fig.add_trace(go.Scatter(
        x=hist_slice["date"],
        y=hist_slice["cpi_general_yoy"],
        mode="lines+markers",
        name="Historical Observed CPI (%)",
        line={"color": COLORS["text_secondary"], "width": 2},
        marker={"size": 4, "color": COLORS["text_secondary"]},
        hovertemplate="Observed: %{y:.2f}%<extra></extra>"
    ))

    # Upper confidence interval
    fig.add_trace(go.Scatter(
        x=forecast_df["date"],
        y=forecast_df["cpi_forecast_upper"],
        mode="lines",
        name="95% Upper Bound",
        line={"width": 0},
        showlegend=False,
        hoverinfo="skip"
    ))

    # Lower confidence interval with shaded fill
    fig.add_trace(go.Scatter(
        x=forecast_df["date"],
        y=forecast_df["cpi_forecast_lower"],
        mode="lines",
        name="95% Confidence Interval",
        fill="tonexty",
        fillcolor="rgba(59, 130, 246, 0.15)",
        line={"width": 0},
        hovertemplate="Lower: %{y:.2f}%<extra></extra>"
    ))

    # Point Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df["date"],
        y=forecast_df["cpi_forecast"],
        mode="lines+markers",
        name="XGBoost Forecast (%)",
        line={"color": COLORS["primary"], "width": 2.8, "dash": "solid"},
        marker={"size": 7, "color": COLORS["primary"]},
        hovertemplate="Point Forecast: %{y:.2f}%<extra></extra>"
    ))

    apply_fintech_theme(fig, "MULTI-HORIZON CPI INFLATION PROJECTION WITH 95% CONFIDENCE INTERVALS")
    fig.update_yaxes(title_text="Projected YoY Rate (%)")
    return fig

def plot_actual_vs_predicted(dates: pd.Series, y_true: np.ndarray, y_pred: np.ndarray) -> go.Figure:
    """
    Renders model prediction overlay versus ground truth test observations.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=y_true,
        mode="lines+markers",
        name="Actual CPI YoY (%)",
        line={"color": COLORS["text_primary"], "width": 2.2},
        marker={"size": 5, "color": COLORS["text_primary"]},
        hovertemplate="Actual: %{y:.2f}%<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=y_pred,
        mode="lines+markers",
        name="Predicted (XGBoost) (%)",
        line={"color": COLORS["primary"], "width": 2.2, "dash": "dash"},
        marker={"size": 5, "color": COLORS["primary"]},
        hovertemplate="Predicted: %{y:.2f}%<extra></extra>"
    ))

    apply_fintech_theme(fig, "OUT-OF-SAMPLE EVALUATION: ACTUAL VS. PREDICTED")
    fig.update_yaxes(title_text="CPI General YoY (%)")
    return fig

def plot_residual_distribution(y_true: np.ndarray, y_pred: np.ndarray) -> go.Figure:
    """
    Renders residual errors scatter plot and zero-line benchmark.
    """
    residuals = y_true - y_pred
    fig = go.Figure()

    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["text_muted"], line_width=1)

    fig.add_trace(go.Scatter(
        x=y_pred,
        y=residuals,
        mode="markers",
        name="Residuals",
        marker={
            "size": 7,
            "color": COLORS["primary"],
            "opacity": 0.8,
            "line": {"color": COLORS["border"], "width": 1}
        },
        hovertemplate="Fitted: %{x:.2f}<br>Residual: %{y:.3f}<extra></extra>"
    ))

    apply_fintech_theme(fig, "RESIDUAL PLOT (PREDICTED VALUE VS. RESIDUAL ERROR)")
    fig.update_xaxes(title_text="Fitted Values")
    fig.update_yaxes(title_text="Residual Error (y - y_hat)")
    return fig

def plot_feature_importance(feature_names: List[str], importances: np.ndarray, top_n: int = 12) -> go.Figure:
    """
    Horizontal bar chart of top XGBoost feature importances.
    """
    df = pd.DataFrame({"feature": feature_names, "importance": importances})
    df = df.sort_values("importance", ascending=True).tail(top_n)

    fig = go.Figure(go.Bar(
        x=df["importance"],
        y=df["feature"],
        orientation="h",
        marker={
            "color": COLORS["primary"],
            "line": {"color": COLORS["border"], "width": 1}
        },
        hovertemplate="Feature: %{y}<br>Importance: %{x:.4f}<extra></extra>"
    ))

    apply_fintech_theme(fig, f"TOP {top_n} ECONOMETRIC FEATURE IMPORTANCES (GAIN)")
    fig.update_xaxes(title_text="Relative Gain Importance")
    return fig

def plot_household_expense_breakdown(expense_dict: Dict[str, float]) -> go.Figure:
    """
    Renders user household expenditure share as a sleek horizontal stacked bar or donut chart.
    """
    labels = list(expense_dict.keys())
    values = list(expense_dict.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        textinfo="label+percent",
        textfont={"size": 11, "family": "Inter, sans-serif"},
        marker={
            "colors": [
                "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899",
                "#06B6D4", "#6366F1", "#14B8A6", "#F97316", "#64748B"
            ],
            "line": {"color": COLORS["card"], "width": 2}
        },
        hovertemplate="Category: %{label}<br>Monthly: INR %{value:,.0f} (%{percent})<extra></extra>"
    )])

    apply_fintech_theme(fig, "HOUSEHOLD EXPENDITURE BASKET ALLOCATION", height=380)
    fig.update_layout(showlegend=False)
    return fig

def plot_category_inflation_impact(impact_df: pd.DataFrame) -> go.Figure:
    """
    Grouped bar chart showing Current Expense vs. Predicted Inflated Expense by category.
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=impact_df["Category"],
        y=impact_df["Current Expense"],
        name="Current Monthly Spend (INR)",
        marker_color=COLORS["border_light"],
        hovertemplate="Current: INR %{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=impact_df["Category"],
        y=impact_df["Predicted Expense"],
        name="Projected Monthly Spend (INR)",
        marker_color=COLORS["primary"],
        hovertemplate="Projected: INR %{y:,.0f}<extra></extra>"
    ))

    apply_fintech_theme(fig, "PROJECTED CATEGORY-WISE EXPENDITURE ESCALATION")
    fig.update_yaxes(title_text="Monthly Outlay (INR)")
    return fig
