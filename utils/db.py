"""
SQLite Database interface for Parivar-Arth.
Handles persistent storage of economic indicators, model forecasts, and audit logs.
"""

import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any
from pathlib import Path
from config.settings import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initializes the database schema if tables do not already exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Historical Economic Time Series Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS economic_indicators (
            date TEXT PRIMARY KEY,
            cpi_general REAL,
            cpi_general_yoy REAL,
            cpi_food REAL,
            cpi_food_yoy REAL,
            cpi_fuel REAL,
            cpi_fuel_yoy REAL,
            cpi_housing REAL,
            cpi_housing_yoy REAL,
            cpi_clothing REAL,
            cpi_clothing_yoy REAL,
            cpi_misc REAL,
            cpi_misc_yoy REAL,
            wpi_general REAL,
            wpi_general_yoy REAL,
            brent_crude_usd REAL,
            gold_inr_10g REAL,
            usd_inr REAL,
            repo_rate REAL,
            source TEXT DEFAULT 'MoSPI_RBI_Historical'
        );
        """)

        # User Simulation / Predictions History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_simulation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_current_expense REAL,
            predicted_personal_inflation REAL,
            additional_monthly_cost REAL,
            additional_annual_cost REAL,
            primary_inflation_driver TEXT,
            expense_breakdown_json TEXT
        );
        """)

        # Model Metadata & Audit Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT,
            rmse REAL,
            mae REAL,
            mape REAL,
            r2 REAL,
            hyperparameters_json TEXT,
            feature_count INTEGER,
            train_records INTEGER,
            test_records INTEGER
        );
        """)

        conn.commit()

def save_indicators(df: pd.DataFrame, if_exists: str = "replace") -> int:
    """Saves economic indicator DataFrame into SQLite."""
    init_db()
    with get_connection() as conn:
        # Ensure date is string format YYYY-MM-DD
        df_to_save = df.copy()
        if "date" in df_to_save.columns:
            df_to_save["date"] = pd.to_datetime(df_to_save["date"]).dt.strftime("%Y-%m-%d")
        
        df_to_save.to_sql("economic_indicators", conn, if_exists=if_exists, index=False)
        return len(df_to_save)

def load_indicators() -> pd.DataFrame:
    """Loads all economic indicators ordered by date."""
    init_db()
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM economic_indicators ORDER BY date ASC", conn)
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df

def log_user_simulation(
    total_expense: float,
    personal_inflation: float,
    add_monthly: float,
    add_annual: float,
    top_driver: str,
    breakdown_json: str
) -> int:
    """Logs user household simulation for analytics."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO user_simulation_history (
            total_current_expense,
            predicted_personal_inflation,
            additional_monthly_cost,
            additional_annual_cost,
            primary_inflation_driver,
            expense_breakdown_json
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (total_expense, personal_inflation, add_monthly, add_annual, top_driver, breakdown_json))
        conn.commit()
        return cursor.lastrowid

def log_model_run(
    model_name: str,
    rmse: float,
    mae: float,
    mape: float,
    r2: float,
    hyperparams_json: str,
    feature_count: int,
    train_count: int,
    test_count: int
) -> int:
    """Logs model training metrics into database audit trail."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO model_runs (
            model_name, rmse, mae, mape, r2,
            hyperparameters_json, feature_count, train_records, test_records
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (model_name, rmse, mae, mape, r2, hyperparams_json, feature_count, train_count, test_count))
        conn.commit()
        return cursor.lastrowid
