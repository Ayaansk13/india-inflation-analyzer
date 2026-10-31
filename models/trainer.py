"""
Machine Learning Model Training Pipeline for Parivar-Arth.
Trains an XGBoost Regressor with Time-Series Split, cross-validation,
feature importance extraction, and Joblib persistence.
"""

import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path

from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from config.settings import (
    MODELS_DIR,
    ML_RANDOM_STATE,
    ML_TEST_SIZE,
    TARGET_COL,
    DATE_COL
)
from utils.feature_engineering import build_features, get_feature_columns
from utils.metrics import compute_regression_metrics, compute_residual_diagnostics
from utils.db import log_model_run

MODEL_FILE = MODELS_DIR / "xgboost_cpi_model.joblib"
METADATA_FILE = MODELS_DIR / "model_metadata.json"

def train_and_evaluate_model(
    df: pd.DataFrame,
    n_estimators: int = 150,
    max_depth: int = 4,
    learning_rate: float = 0.05,
    subsample: float = 0.85,
    colsample_bytree: float = 0.85,
    test_ratio: float = ML_TEST_SIZE
) -> Dict[str, Any]:
    """
    Executes the end-to-end econometric ML training routine:
    1. Feature matrix transformation
    2. Temporal chronological split (preventing future data contamination)
    3. Time-Series 5-Fold Cross Validation
    4. Model benchmarking (XGBoost vs Random Forest vs Ridge)
    5. Persistence to disk via Joblib
    6. Audit trail logging to SQLite
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Feature Engineering
    feat_df = build_features(df, drop_na=True)
    feature_cols = [c for c in get_feature_columns() if c in feat_df.columns]
    
    X = feat_df[feature_cols].values
    y = feat_df[TARGET_COL].values
    dates = feat_df[DATE_COL]

    # 2. Chronological Train/Test Split
    split_idx = int(len(X) * (1.0 - test_ratio))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    dates_train, dates_test = dates[:split_idx], dates[split_idx:]

    # 3. XGBoost Model Instantiation
    xgb_params = {
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "learning_rate": learning_rate,
        "subsample": subsample,
        "colsample_bytree": colsample_bytree,
        "random_state": ML_RANDOM_STATE,
        "n_jobs": -1
    }
    model = XGBRegressor(**xgb_params)

    # 4. TimeSeriesSplit Cross-Validation
    tscv = TimeSeriesSplit(n_splits=5)
    cv_rmse_scores = []
    cv_r2_scores = []

    for train_cv, val_cv in tscv.split(X_train):
        cv_model = XGBRegressor(**xgb_params)
        cv_model.fit(X_train[train_cv], y_train[train_cv])
        y_val_pred = cv_model.predict(X_train[val_cv])
        metrics_val = compute_regression_metrics(y_train[val_cv], y_val_pred)
        cv_rmse_scores.append(metrics_val["rmse"])
        cv_r2_scores.append(metrics_val["r2"])

    # 5. Fit Final Model on full Training partition
    model.fit(X_train, y_train)

    # 6. Out-of-sample Testing
    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    test_metrics = compute_regression_metrics(y_test, y_pred_test)
    train_metrics = compute_regression_metrics(y_train, y_pred_train)
    residual_diag = compute_residual_diagnostics(y_test, y_pred_test)

    # 7. Baseline Models Comparison
    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=ML_RANDOM_STATE)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_metrics = compute_regression_metrics(y_test, rf_pred)

    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    ridge_pred = ridge.predict(X_test)
    ridge_metrics = compute_regression_metrics(y_test, ridge_pred)

    # 8. Feature Importance
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    feature_ranking = [
        {"feature": feature_cols[i], "importance": round(float(importances[i]), 4)}
        for i in sorted_idx
    ]

    # 9. Learning Curve Simulation (progressive fractions of train set)
    fractions = [0.25, 0.5, 0.75, 1.0]
    learning_curve_data = []
    for frac in fractions:
        f_size = max(10, int(len(X_train) * frac))
        sub_X = X_train[:f_size]
        sub_y = y_train[:f_size]
        sub_model = XGBRegressor(**xgb_params)
        sub_model.fit(sub_X, sub_y)
        
        train_sub_pred = sub_model.predict(sub_X)
        test_sub_pred = sub_model.predict(X_test)
        
        train_rmse = float(np.sqrt(np.mean((sub_y - train_sub_pred) ** 2)))
        test_rmse = float(np.sqrt(np.mean((y_test - test_sub_pred) ** 2)))
        learning_curve_data.append({
            "sample_size": f_size,
            "fraction": frac,
            "train_rmse": round(train_rmse, 4),
            "val_rmse": round(test_rmse, 4)
        })

    # 10. Persist Model and Metadata
    joblib.dump(model, MODEL_FILE)
    
    metadata = {
        "model_name": "XGBoost Inflation Regressor",
        "trained_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hyperparameters": xgb_params,
        "feature_columns": feature_cols,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "test_metrics": test_metrics,
        "train_metrics": train_metrics,
        "cv_mean_rmse": round(float(np.mean(cv_rmse_scores)), 4),
        "cv_mean_r2": round(float(np.mean(cv_r2_scores)), 4),
        "residual_diagnostics": residual_diag,
        "benchmark_comparison": {
            "XGBoost": test_metrics,
            "RandomForest": rf_metrics,
            "RidgeRegression": ridge_metrics
        },
        "feature_ranking": feature_ranking,
        "learning_curve": learning_curve_data
    }

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # 11. SQLite Audit Trail Log
    log_model_run(
        model_name="XGBoost Regressor",
        rmse=test_metrics["rmse"],
        mae=test_metrics["mae"],
        mape=test_metrics["mape"],
        r2=test_metrics["r2"],
        hyperparams_json=json.dumps(xgb_params),
        feature_count=len(feature_cols),
        train_count=len(X_train),
        test_count=len(X_test)
    )

    return {
        "model": model,
        "metadata": metadata,
        "dates_test": dates_test,
        "y_test": y_test,
        "y_pred_test": y_pred_test,
        "feature_cols": feature_cols
    }

def load_saved_model_and_metadata() -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    """
    Loads persisted XGBoost model and training metadata from disk.
    """
    if MODEL_FILE.exists() and METADATA_FILE.exists():
        try:
            model = joblib.load(MODEL_FILE)
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            return model, metadata
        except Exception:
            return None, None
    return None, None
