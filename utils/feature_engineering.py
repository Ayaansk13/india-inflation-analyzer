"""
Feature Engineering Pipeline for Parivar-Arth.
Creates econometric lag features, rolling statistics, calendar seasonality,
and cross-market differentials required for time-series forecasting.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any
from config.settings import LAG_PERIODS, ROLLING_WINDOWS, TARGET_COL

def build_features(df: pd.DataFrame, drop_na: bool = True) -> pd.DataFrame:
    """
    Transforms clean macroeconomic time series into a rich feature matrix.
    Prevents look-ahead bias by computing lags and rolling metrics strictly
    on past data points.
    """
    data = df.copy()
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"])
        data = data.sort_values("date").reset_index(drop=True)

    # 1. Temporal & Cyclical Features
    data["month"] = data["date"].dt.month
    data["quarter"] = data["date"].dt.quarter
    data["year"] = data["date"].dt.year
    
    # Cyclical sine & cosine transformations
    data["sin_month"] = np.sin(2 * np.pi * data["month"] / 12.0)
    data["cos_month"] = np.cos(2 * np.pi * data["month"] / 12.0)

    # 2. MoM Inflation Rate Momentum (Index percentage change)
    if "cpi_general" in data.columns:
        data["cpi_mom_change"] = data["cpi_general"].pct_change(1) * 100.0

    # 3. Commodity Growth Rates (YoY)
    if "brent_crude_usd" in data.columns:
        data["crude_yoy"] = data["brent_crude_usd"].pct_change(12) * 100.0
    if "gold_inr_10g" in data.columns:
        data["gold_yoy"] = data["gold_inr_10g"].pct_change(12) * 100.0

    # 4. Food vs Fuel Spread
    if "cpi_food_yoy" in data.columns and "cpi_fuel_yoy" in data.columns:
        data["food_fuel_spread"] = data["cpi_food_yoy"] - data["cpi_fuel_yoy"]

    # 5. Lag Features for Target & Key Exogenous Drivers
    for lag in LAG_PERIODS:
        data[f"cpi_general_yoy_lag{lag}"] = data[TARGET_COL].shift(lag)
        if "cpi_food_yoy" in data.columns:
            data[f"cpi_food_yoy_lag{lag}"] = data["cpi_food_yoy"].shift(lag)
        if "wpi_general_yoy" in data.columns:
            data[f"wpi_yoy_lag{lag}"] = data["wpi_general_yoy"].shift(lag)
        if "brent_crude_usd" in data.columns:
            data[f"crude_lag{lag}"] = data["brent_crude_usd"].shift(lag)

    # 6. Rolling Window Statistics (Moving Averages & Volatility)
    for w in ROLLING_WINDOWS:
        data[f"cpi_yoy_rolling_mean_{w}m"] = data[TARGET_COL].shift(1).rolling(window=w).mean()
        data[f"cpi_yoy_rolling_std_{w}m"] = data[TARGET_COL].shift(1).rolling(window=w).std()

    if drop_na:
        data = data.dropna().reset_index(drop=True)

    return data

def get_feature_columns() -> List[str]:
    """
    Returns the deterministic list of engineered input features for model training.
    """
    features = [
        "month",
        "quarter",
        "sin_month",
        "cos_month",
        "cpi_mom_change",
        "crude_yoy",
        "gold_yoy",
        "food_fuel_spread",
        "repo_rate",
        "usd_inr",
        "cpi_general_yoy_lag1",
        "cpi_general_yoy_lag2",
        "cpi_general_yoy_lag3",
        "cpi_general_yoy_lag6",
        "cpi_general_yoy_lag12",
        "cpi_food_yoy_lag1",
        "cpi_food_yoy_lag2",
        "cpi_food_yoy_lag3",
        "wpi_yoy_lag1",
        "wpi_yoy_lag2",
        "crude_lag1",
        "crude_lag2",
        "cpi_yoy_rolling_mean_3m",
        "cpi_yoy_rolling_mean_6m",
        "cpi_yoy_rolling_mean_12m",
        "cpi_yoy_rolling_std_6m",
    ]
    return features

def get_preprocessing_pipeline_summary() -> List[Dict[str, Any]]:
    """
    Returns structured metadata describing each ETL and Feature Engineering step
    for visual inspection on the dashboard.
    """
    return [
        {
            "step": "1. Data Acquisition & Sync",
            "type": "ETL Ingestion",
            "details": "Ingests historical MoSPI CPI All-India (2012=100), WPI, Brent Crude, MCX Gold, USD/INR.",
            "status": "Operational"
        },
        {
            "step": "2. Time-Series Continuity & Deduplication",
            "type": "Data Cleansing",
            "details": "Deduplicates on monthly timestamp key and aligns timestamps to standard Month-Start (MS) frequency.",
            "status": "Operational"
        },
        {
            "step": "3. Missing Value Handling",
            "type": "Imputation",
            "details": "Applies piecewise cubic spline / forward-backward filling to preserve temporal variance.",
            "status": "Operational"
        },
        {
            "step": "4. Statistical Outlier Capping",
            "type": "Outlier Treatment",
            "details": "Identifies extreme shocks exceeding 4.5 sigma thresholds to prevent model gradient explosion.",
            "status": "Operational"
        },
        {
            "step": "5. Econometric Lag Creation",
            "type": "Feature Engineering",
            "details": "Constructs t-1, t-2, t-3, t-6, t-12 lags across headline CPI, food components, WPI, and Brent crude.",
            "status": "Operational"
        },
        {
            "step": "6. Moving Averages & Volatility",
            "type": "Feature Engineering",
            "details": "Calculates 3M, 6M, and 12M moving averages and rolling standard deviations with t-1 shift.",
            "status": "Operational"
        },
        {
            "step": "7. Seasonal Harmonic Encoding",
            "type": "Mathematical Transform",
            "details": "Transforms calendar months into orthogonal sin/cos harmonics to capture monsoon and festival price cycles.",
            "status": "Operational"
        },
        {
            "step": "8. Cross-Asset Spreads",
            "type": "Feature Engineering",
            "details": "Derives food-fuel differentials and currency-adjusted import inflation pressures.",
            "status": "Operational"
        }
    ]
