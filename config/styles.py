"""
Custom CSS styling and HTML components for Parivar-Arth.
Strict Bloomberg / TradingView / Stripe dark analytics theme with no emojis.
"""

from config.settings import COLORS

def get_custom_css() -> str:
    """
    Returns the comprehensive CSS stylesheet that converts Streamlit into
    a bespoke enterprise analytics platform.
    """
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Reset & Base */
    html, body, [class*="st-"], .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: {COLORS['bg']} !important;
        color: {COLORS['text_primary']} !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    /* Hide standard Streamlit header, footer, and menu */
    header[data-testid="stHeader"] {{
        background: {COLORS['bg']} !important;
        border-bottom: 1px solid {COLORS['border']};
        z-index: 99;
    }}
    footer {{
        visibility: hidden;
        height: 0;
    }}
    #MainMenu {{
        visibility: hidden;
    }}

    /* Main Container Padding */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1400px !important;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Manrope', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: {COLORS['text_primary']} !important;
        letter-spacing: -0.025em !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}

    h1 {{
        font-size: 1.85rem !important;
        line-height: 1.25 !important;
    }}

    h2 {{
        font-size: 1.4rem !important;
        line-height: 1.3 !important;
        border-bottom: 1px solid {COLORS['border']};
        padding-bottom: 0.4rem;
        margin-top: 1.5rem !important;
    }}

    h3 {{
        font-size: 1.15rem !important;
        line-height: 1.35 !important;
        font-weight: 600 !important;
    }}

    p, span, label, div {{
        color: {COLORS['text_secondary']};
        font-size: 0.925rem;
        line-height: 1.5;
    }}

    code, pre {{
        font-family: 'JetBrains Mono', monospace !important;
        background-color: {COLORS['bg_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Bespoke Card Container */
    .metric-card {{
        background-color: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 1.15rem 1.25rem;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .metric-card:hover {{
        border-color: {COLORS['border_light']};
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }}

    .metric-card-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: {COLORS['text_muted']};
        margin-bottom: 0.35rem;
    }}

    .metric-card-value {{
        font-family: 'Manrope', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        color: {COLORS['text_primary']};
        line-height: 1.15;
        letter-spacing: -0.02em;
    }}

    .metric-card-subtext {{
        font-size: 0.775rem;
        margin-top: 0.4rem;
        color: {COLORS['text_secondary']};
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }}

    .tag-delta-pos {{
        color: {COLORS['danger']};
        background: {COLORS['danger_subtle']};
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.72rem;
    }}

    .tag-delta-neg {{
        color: {COLORS['success']};
        background: {COLORS['success_subtle']};
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.72rem;
    }}

    .tag-neutral {{
        color: {COLORS['primary']};
        background: {COLORS['primary_subtle']};
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.72rem;
    }}

    /* Standardized Streamlit Metric Widgets override */
    [data-testid="stMetric"] {{
        background-color: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }}
    [data-testid="stMetricLabel"] p {{
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-weight: 600 !important;
        color: {COLORS['text_muted']} !important;
    }}
    [data-testid="stMetricValue"] div {{
        font-family: 'Manrope', sans-serif !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: {COLORS['text_primary']} !important;
    }}

    /* Platform Navigation Bar */
    .platform-header {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    .brand-title {{
        font-family: 'Manrope', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {COLORS['text_primary']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .brand-badge {{
        font-size: 0.68rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: {COLORS['primary']};
        background: {COLORS['primary_subtle']};
        border: 1px solid {COLORS['primary']};
        padding: 2px 8px;
        border-radius: 4px;
    }}

    .header-status {{
        display: flex;
        align-items: center;
        gap: 1.2rem;
        font-size: 0.8rem;
        color: {COLORS['text_muted']};
    }}

    .status-indicator {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: {COLORS['success']};
        margin-right: 6px;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {COLORS['primary']} !important;
        color: #FFFFFF !important;
        border: 1px solid {COLORS['primary']} !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.25rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
    }}

    .stButton > button:hover {{
        background-color: {COLORS['primary_hover']} !important;
        border-color: {COLORS['primary_hover']} !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35) !important;
    }}

    /* Secondary / Outline Button */
    .stButton.button-secondary > button {{
        background-color: transparent !important;
        color: {COLORS['text_primary']} !important;
        border: 1px solid {COLORS['border']} !important;
    }}
    .stButton.button-secondary > button:hover {{
        background-color: {COLORS['card']} !important;
        border-color: {COLORS['border_light']} !important;
    }}

    /* Form Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stMultiSelect {{
        background-color: {COLORS['bg_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        color: {COLORS['text_primary']} !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
    }}

    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 1px {COLORS['primary']} !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid {COLORS['border']};
        padding-bottom: 4px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 6px 6px 0 0;
        color: {COLORS['text_secondary']};
        font-weight: 500;
        font-size: 0.875rem;
        padding: 8px 16px;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['card']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-bottom: 1px solid {COLORS['card']} !important;
        color: {COLORS['primary']} !important;
        font-weight: 600 !important;
    }}

    /* DataFrames / Tables */
    [data-testid="stDataFrame"] {{
        background-color: {COLORS['card']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 8px !important;
        overflow: hidden;
    }}

    /* Callout & Alert Panels */
    .info-panel {{
        background-color: {COLORS['card']};
        border-left: 3px solid {COLORS['primary']};
        border-top: 1px solid {COLORS['border']};
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }}

    .warning-panel {{
        background-color: {COLORS['card']};
        border-left: 3px solid {COLORS['warning']};
        border-top: 1px solid {COLORS['border']};
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }}

    .success-panel {{
        background-color: {COLORS['card']};
        border-left: 3px solid {COLORS['success']};
        border-top: 1px solid {COLORS['border']};
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }}

    .danger-panel {{
        background-color: {COLORS['card']};
        border-left: 3px solid {COLORS['danger']};
        border-top: 1px solid {COLORS['border']};
        border-right: 1px solid {COLORS['border']};
        border-bottom: 1px solid {COLORS['border']};
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }}

    /* Sidebar Clean Styling */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['bg_secondary']} !important;
        border-right: 1px solid {COLORS['border']} !important;
    }}

    [data-testid="stSidebarNav"] {{
        padding-top: 1rem;
    }}

    /* Section Separator */
    .section-divider {{
        height: 1px;
        background-color: {COLORS['border']};
        margin: 2rem 0;
    }}

    /* Bespoke Segmented Radio Navbar (Bloomberg / Stripe Style) */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
        background-color: {COLORS['bg_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 8px !important;
        padding: 5px !important;
    }}

    div[data-testid="stRadio"] label {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 6px !important;
        padding: 6px 14px !important;
        margin: 0 !important;
        cursor: pointer !important;
        font-size: 0.825rem !important;
        font-weight: 500 !important;
        color: {COLORS['text_secondary']} !important;
        transition: all 0.15s ease !important;
        display: inline-flex !important;
        align-items: center !important;
    }}

    div[data-testid="stRadio"] label:hover {{
        background-color: {COLORS['card']} !important;
        color: {COLORS['text_primary']} !important;
    }}

    div[data-testid="stRadio"] label:has(input:checked),
    div[data-testid="stRadio"] label[data-checked="true"] {{
        background-color: {COLORS['card']} !important;
        border: 1px solid {COLORS['primary']} !important;
        color: {COLORS['text_primary']} !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }}

    div[data-testid="stRadio"] input[type="radio"] {{
        display: none !important;
    }}
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {{
        font-size: 0.825rem !important;
        color: inherit !important;
    }}
    </style>
    """

def render_metric_card(label: str, value: str, subtext: str = "", delta_type: str = "neutral") -> str:
    """
    Renders a custom HTML metric card with no emojis and clean typography.
    """
    badge_class = "tag-neutral"
    if delta_type == "pos":
        badge_class = "tag-delta-pos"
    elif delta_type == "neg":
        badge_class = "tag-delta-neg"

    subtext_html = ""
    if subtext:
        subtext_html = f'<div class="metric-card-subtext"><span class="{badge_class}">{subtext}</span></div>'

    return f"""
    <div class="metric-card">
        <div class="metric-card-label">{label}</div>
        <div class="metric-card-value">{value}</div>
        {subtext_html}
    </div>
    """

def render_top_header(active_page: str = "Overview") -> str:
    """
    Renders the Bloomberg/TradingView style executive banner.
    """
    return f"""
    <div class="platform-header">
        <div class="brand-title">
            PARIVAR-ARTH
            <span class="brand-badge">PRO ANALYTICS</span>
            <span style="font-size: 0.85rem; font-weight: 500; color: {COLORS['text_muted']}; margin-left: 10px;">
                | &nbsp; {active_page}
            </span>
        </div>
        <div class="header-status">
            <div><span class="status-indicator"></span>LIVE SYSTEM ACTIVE</div>
            <div>BASE YEAR: 2012=100</div>
            <div>TARGET: 4.0% +/- 2.0%</div>
            <div>SECURITY: ENTERPRISE GRADE</div>
        </div>
    </div>
    """
