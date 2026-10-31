"""
System-wide settings, color constants, paths, and economic parameters.
Adheres strictly to the professional dark analytics theme without emojis.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DB_PATH = DATA_DIR / "inflation_data.db"
MODELS_DIR = BASE_DIR / "saved_models"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"

# Ensure runtime directories exist
for p in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, ASSETS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Application Metadata
APP_NAME = "Parivar-Arth"
APP_SUBTITLE = "India Inflation Impact Analyzer & Personal Cost Predictor"
APP_VERSION = "2.4.0-PROD"
PROJECT_TYPE = "B.Sc. Data Science Capstone & Enterprise Analytics"

# Color Palette (Corporate Bloomberg/TradingView FinTech Dark Theme)
COLORS = {
    "bg": "#0B1220",
    "bg_secondary": "#111827",
    "card": "#182234",
    "card_hover": "#1E2B42",
    "border": "#263348",
    "border_light": "#334460",
    "primary": "#3B82F6",
    "primary_hover": "#2563EB",
    "primary_subtle": "rgba(59, 130, 246, 0.12)",
    "success": "#10B981",
    "success_subtle": "rgba(16, 185, 129, 0.12)",
    "warning": "#F59E0B",
    "warning_subtle": "rgba(245, 158, 11, 0.12)",
    "danger": "#EF4444",
    "danger_subtle": "rgba(239, 68, 68, 0.12)",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "grid": "#1E293B",
}

# Official MoSPI CPI Base 2012=100 Weights (All India Combined)
CPI_BASKET_WEIGHTS = {
    "Food and Beverages": 45.86,
    "Pan, tobacco and intoxicants": 2.38,
    "Clothing and footwear": 6.53,
    "Housing": 10.07,
    "Fuel and light": 6.84,
    "Miscellaneous": 28.32,
}

# Detailed Sub-category weights inside Miscellaneous
CPI_MISC_SUB_WEIGHTS = {
    "Transport and communication": 8.59,
    "Health": 5.89,
    "Education": 4.46,
    "Personal care and effects": 3.89,
    "Household goods and services": 3.80,
    "Recreation and amusement": 1.68,
}

# Personal Household Expense Categories and their closest CPI benchmark mapping
HOUSEHOLD_CATEGORY_MAPPING = {
    "Food": {
        "cpi_component": "Food and Beverages",
        "description": "Groceries, vegetables, dairy, grains, dining",
        "volatility": "High",
        "essential": True,
    },
    "Fuel": {
        "cpi_component": "Fuel and light",
        "description": "LPG cylinders, petrol, diesel, domestic gas",
        "volatility": "High",
        "essential": True,
    },
    "Transport": {
        "cpi_component": "Transport and communication",
        "description": "Public commute, cab aggregator, auto-rickshaw",
        "volatility": "Medium",
        "essential": True,
    },
    "Rent": {
        "cpi_component": "Housing",
        "description": "Residential lease or housing maintenance",
        "volatility": "Low",
        "essential": True,
    },
    "Healthcare": {
        "cpi_component": "Health",
        "description": "Consultations, diagnostics, prescription medicine",
        "volatility": "Medium",
        "essential": True,
    },
    "Education": {
        "cpi_component": "Education",
        "description": "School/college fees, textbooks, courses",
        "volatility": "Low",
        "essential": True,
    },
    "Utilities": {
        "cpi_component": "Household goods and services",
        "description": "Electricity, water, domestic maintenance, broadband",
        "volatility": "Low",
        "essential": True,
    },
    "Entertainment": {
        "cpi_component": "Recreation and amusement",
        "description": "Streaming subscriptions, movies, leisure trips",
        "volatility": "Low",
        "essential": False,
    },
    "Shopping": {
        "cpi_component": "Clothing and footwear",
        "description": "Apparel, footwear, consumer durables",
        "volatility": "Medium",
        "essential": False,
    },
    "Other": {
        "cpi_component": "Personal care and effects",
        "description": "Personal hygiene, salon, miscellaneous ad-hoc expenses",
        "volatility": "Low",
        "essential": False,
    },
}

# RBI Monetary Policy Framework Targets
RBI_INFLATION_TARGET = 4.0
RBI_UPPER_TOLERANCE = 6.0
RBI_LOWER_TOLERANCE = 2.0

# Model Pipeline Hyperparameters
ML_RANDOM_STATE = 42
ML_TEST_SIZE = 0.20
ML_CV_FOLDS = 5
LAG_PERIODS = [1, 2, 3, 6, 12]
ROLLING_WINDOWS = [3, 6, 12]

# Target column for headline forecasting
TARGET_COL = "cpi_general_yoy"
DATE_COL = "date"
