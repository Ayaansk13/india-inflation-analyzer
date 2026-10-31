"""
Statistical and Econometric Evaluation Metrics for Parivar-Arth.
Calculates RMSE, MAE, MAPE, R-squared, and residual diagnostics.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

def compute_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Computes standard regression performance metrics.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    # Residuals
    residuals = y_true - y_pred
    
    # 1. Mean Squared Error and RMSE
    mse = float(np.mean(residuals ** 2))
    rmse = float(np.sqrt(mse))
    
    # 2. Mean Absolute Error
    mae = float(np.mean(np.abs(residuals)))
    
    # 3. Mean Absolute Percentage Error (handling near-zero cases safely)
    denom = np.where(np.abs(y_true) < 1e-4, 1e-4, np.abs(y_true))
    mape = float(np.mean(np.abs(residuals / denom)) * 100.0)
    
    # 4. R-squared (Coefficient of Determination)
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    ss_res = float(np.sum(residuals ** 2))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    # 5. Maximum Absolute Error
    max_error = float(np.max(np.abs(residuals)))
    
    return {
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "mape": round(mape, 2),
        "r2": round(r2, 4),
        "max_error": round(max_error, 4),
        "mse": round(mse, 4)
    }

def compute_residual_diagnostics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
    """
    Analyzes model error residuals for bias, heteroscedasticity,
    and first-order serial correlation (Durbin-Watson).
    """
    residuals = np.asarray(y_true) - np.asarray(y_pred)
    n = len(residuals)
    
    mean_res = float(np.mean(residuals))
    std_res = float(np.std(residuals))
    
    # Durbin-Watson statistic: sum((e_t - e_{t-1})^2) / sum(e_t^2)
    # DW ~ 2.0 implies no first-order serial correlation
    if n > 1:
        diff = np.diff(residuals)
        dw_stat = float(np.sum(diff ** 2) / np.sum(residuals ** 2)) if np.sum(residuals ** 2) > 0 else 2.0
    else:
        dw_stat = 2.0

    return {
        "mean_residual": round(mean_res, 4),
        "std_residual": round(std_res, 4),
        "durbin_watson": round(dw_stat, 3),
        "residual_skew": round(float(pd.Series(residuals).skew()), 3) if n > 2 else 0.0,
        "sample_size": n
    }

def format_metric_explanation() -> Dict[str, Dict[str, str]]:
    """
    Provides plain-language interpretations of technical econometric metrics.
    """
    return {
        "RMSE": {
            "name": "Root Mean Squared Error",
            "meaning": "Measures the average magnitude of prediction error, giving higher penalty to large outliers.",
            "benchmark": "Values under 0.60 indicate high predictive accuracy for India CPI YoY rate."
        },
        "MAE": {
            "name": "Mean Absolute Error",
            "meaning": "Direct average distance between predicted inflation rate and actual observed inflation rate.",
            "benchmark": "An MAE of 0.35% means on average predictions deviate by only 35 basis points."
        },
        "MAPE": {
            "name": "Mean Absolute Percentage Error",
            "meaning": "Relative percentage deviation of forecasts relative to true underlying values.",
            "benchmark": "Values under 8.0% signify institutional-grade time series forecasting."
        },
        "R2": {
            "name": "R-Squared (Coefficient of Determination)",
            "meaning": "Proportion of variance in headline inflation explained by the XGBoost model and exogenous features.",
            "benchmark": "Values above 0.85 indicate that the model captures over 85% of economic volatility."
        },
        "Durbin-Watson": {
            "name": "Durbin-Watson Autocorrelation Test",
            "meaning": "Tests if model residuals suffer from time-dependent inertia.",
            "benchmark": "A score close to 2.0 (1.6 to 2.4) proves residuals are white-noise and model is free from look-ahead leakage."
        }
    }
