"""
Econometric Multi-Horizon Forecaster and Scenario Simulation Engine for Parivar-Arth.
Generates 1-Month, 3-Month, and 6-Month recursive forward projections
with confidence bounds and what-if exogenous shock scenario simulations.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from config.settings import TARGET_COL, DATE_COL
from utils.feature_engineering import build_features, get_feature_columns
from models.trainer import load_saved_model_and_metadata, train_and_evaluate_model

def generate_multi_step_forecast(
    df: pd.DataFrame,
    horizon_months: int = 6,
    scenario_adjustments: Optional[Dict[str, float]] = None
) -> pd.DataFrame:
    """
    Computes recursive multi-step forecasts for the next 1 to 6 months.
    Applies scenario shocks if provided (e.g. crude oil spike, food supply shock).
    Calculates 95% confidence intervals based on residual error propagation.
    """
    model, metadata = load_saved_model_and_metadata()
    if model is None or metadata is None:
        # Auto-train if model does not exist yet
        res = train_and_evaluate_model(df)
        model = res["model"]
        metadata = res["metadata"]

    feature_cols = metadata.get("feature_columns", get_feature_columns())
    std_residual = metadata.get("residual_diagnostics", {}).get("std_residual", 0.45)

    # Work on a copy of recent historical data
    working_df = df.copy().sort_values("date").reset_index(drop=True)
    
    last_date = working_df["date"].iloc[-1]
    last_cpi_gen = working_df["cpi_general"].iloc[-1]
    
    forecast_records = []

    # Scenario modifiers
    shocks = scenario_adjustments or {}
    crude_multiplier = 1.0 + (shocks.get("crude_pct", 0.0) / 100.0)
    food_pct_shock = shocks.get("food_shock_pts", 0.0)
    repo_rate_delta = shocks.get("repo_rate_delta_bps", 0.0) / 100.0

    for step in range(1, horizon_months + 1):
        target_date = last_date + relativedelta(months=step)
        
        # Build features on current working history
        feat_df = build_features(working_df, drop_na=False)
        
        # Create candidate next row
        next_row = {}
        next_row["date"] = target_date
        next_row["month"] = target_date.month
        next_row["quarter"] = (target_date.month - 1) // 3 + 1
        next_row["year"] = target_date.year
        next_row["sin_month"] = np.sin(2 * np.pi * target_date.month / 12.0)
        next_row["cos_month"] = np.cos(2 * np.pi * target_date.month / 12.0)
        
        # Pull latest available lags from recent working_df
        recent_cpi_yoy = working_df["cpi_general_yoy"].values
        recent_food_yoy = working_df["cpi_food_yoy"].values if "cpi_food_yoy" in working_df.columns else recent_cpi_yoy
        recent_crude = working_df["brent_crude_usd"].values if "brent_crude_usd" in working_df.columns else [75.0]
        recent_wpi = working_df["wpi_general_yoy"].values if "wpi_general_yoy" in working_df.columns else recent_cpi_yoy
        
        next_row["cpi_general_yoy_lag1"] = recent_cpi_yoy[-1]
        next_row["cpi_general_yoy_lag2"] = recent_cpi_yoy[-2] if len(recent_cpi_yoy) > 1 else recent_cpi_yoy[-1]
        next_row["cpi_general_yoy_lag3"] = recent_cpi_yoy[-3] if len(recent_cpi_yoy) > 2 else recent_cpi_yoy[-1]
        next_row["cpi_general_yoy_lag6"] = recent_cpi_yoy[-6] if len(recent_cpi_yoy) > 5 else recent_cpi_yoy[-1]
        next_row["cpi_general_yoy_lag12"] = recent_cpi_yoy[-12] if len(recent_cpi_yoy) > 11 else recent_cpi_yoy[-1]

        next_row["cpi_food_yoy_lag1"] = recent_food_yoy[-1] + food_pct_shock
        next_row["cpi_food_yoy_lag2"] = recent_food_yoy[-2] if len(recent_food_yoy) > 1 else recent_food_yoy[-1]
        next_row["cpi_food_yoy_lag3"] = recent_food_yoy[-3] if len(recent_food_yoy) > 2 else recent_food_yoy[-1]

        next_row["wpi_yoy_lag1"] = recent_wpi[-1]
        next_row["wpi_yoy_lag2"] = recent_wpi[-2] if len(recent_wpi) > 1 else recent_wpi[-1]

        next_row["crude_lag1"] = recent_crude[-1] * crude_multiplier
        next_row["crude_lag2"] = recent_crude[-2] if len(recent_crude) > 1 else recent_crude[-1]

        # Rolling statistics from recent predictions
        next_row["cpi_yoy_rolling_mean_3m"] = float(np.mean(recent_cpi_yoy[-3:]))
        next_row["cpi_yoy_rolling_mean_6m"] = float(np.mean(recent_cpi_yoy[-6:]))
        next_row["cpi_yoy_rolling_mean_12m"] = float(np.mean(recent_cpi_yoy[-12:]))
        next_row["cpi_yoy_rolling_std_6m"] = float(np.std(recent_cpi_yoy[-6:])) if len(recent_cpi_yoy) >= 6 else 0.5

        next_row["cpi_mom_change"] = float(np.mean(recent_cpi_yoy[-3:])) / 12.0
        next_row["crude_yoy"] = 5.0 * crude_multiplier
        next_row["gold_yoy"] = 8.5
        next_row["food_fuel_spread"] = (next_row["cpi_food_yoy_lag1"] - 4.5)
        next_row["repo_rate"] = (working_df["repo_rate"].iloc[-1] if "repo_rate" in working_df.columns else 6.50) + repo_rate_delta
        next_row["usd_inr"] = working_df["usd_inr"].iloc[-1] if "usd_inr" in working_df.columns else 83.80

        # Construct vector aligned with feature_cols
        X_step = np.array([[next_row.get(col, 0.0) for col in feature_cols]])
        
        # Predict headline YoY
        pred_yoy = float(model.predict(X_step)[0])
        
        # Confidence intervals: error increases with sqrt(horizon)
        horizon_se = std_residual * np.sqrt(step)
        ci_lower = max(0.0, pred_yoy - 1.96 * horizon_se)
        ci_upper = pred_yoy + 1.96 * horizon_se

        # Compute next month projected index level
        monthly_growth = (pred_yoy / 100.0) / 12.0
        last_cpi_gen = last_cpi_gen * (1.0 + monthly_growth)

        record = {
            "step": step,
            "horizon": f"+{step} Month" if step == 1 else f"+{step} Months",
            "date": target_date,
            "cpi_forecast": round(pred_yoy, 2),
            "cpi_forecast_lower": round(ci_lower, 2),
            "cpi_forecast_upper": round(ci_upper, 2),
            "projected_cpi_index": round(last_cpi_gen, 2),
        }
        forecast_records.append(record)

        # Append simulated step to working dataframe for recursive lag dependency
        simulated_row = {
            "date": target_date,
            "cpi_general": last_cpi_gen,
            "cpi_general_yoy": pred_yoy,
            "cpi_food_yoy": pred_yoy + food_pct_shock,
            "cpi_fuel_yoy": 5.0 * crude_multiplier,
            "wpi_general_yoy": pred_yoy * 1.1,
            "brent_crude_usd": recent_crude[-1] * crude_multiplier,
            "gold_inr_10g": working_df["gold_inr_10g"].iloc[-1] * 1.005,
            "usd_inr": next_row["usd_inr"],
            "repo_rate": next_row["repo_rate"]
        }
        working_df = pd.concat([working_df, pd.DataFrame([simulated_row])], ignore_index=True)

    forecast_df = pd.DataFrame(forecast_records)
    return forecast_df

def get_predefined_scenarios() -> Dict[str, Dict[str, Any]]:
    """
    Returns pre-configured macro stress test scenarios for what-if simulation.
    """
    return {
        "Baseline": {
            "name": "Baseline Projection",
            "description": "Continuation of current monetary stance and mean-reverting commodity dynamics.",
            "shocks": {"crude_pct": 0.0, "food_shock_pts": 0.0, "repo_rate_delta_bps": 0.0}
        },
        "Crude Spike (+25%)": {
            "name": "Geopolitical Energy Shock",
            "description": "Middle-East logistics disruption driving Brent Crude up +25% (~$95/bbl).",
            "shocks": {"crude_pct": 25.0, "food_shock_pts": 0.5, "repo_rate_delta_bps": 25.0}
        },
        "Deficient Monsoon (+15% Food)": {
            "name": "El Nino & Monsoon Deficit",
            "description": "Kharif crop damage causing severe vegetable and pulses price surge.",
            "shocks": {"crude_pct": 0.0, "food_shock_pts": 2.5, "repo_rate_delta_bps": 50.0}
        },
        "RBI Hawkish Tightening (+50 bps)": {
            "name": "Aggressive RBI Monetary Tightening",
            "description": "50 bps repo rate hike to 7.00% to dampen demand-side pressures.",
            "shocks": {"crude_pct": -5.0, "food_shock_pts": -0.8, "repo_rate_delta_bps": 50.0}
        },
        "Global Disinflation (-15% Crude)": {
            "name": "Global Commodity Softening",
            "description": "Synchronized global slowdown lowering import commodity input costs.",
            "shocks": {"crude_pct": -15.0, "food_shock_pts": -1.2, "repo_rate_delta_bps": -25.0}
        }
    }
