"""
PDF Report Generator for India Inflation Impact Analyzer
Generates an official, branded academic & household financial assessment report.
"""

from datetime import datetime
from typing import Dict, Any, List

try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False


def clean_text(text: Any) -> str:
    """Sanitize glyphs for standard Helvetica PDF."""
    if text is None:
        return ""
    return str(text).replace("₹", "Rs. ").replace("•", "-").replace("—", "-")


if HAS_FPDF:
    class InflationReportPDF(FPDF):
        def header(self):
            # Top Banner (Teal)
            self.set_fill_color(15, 118, 110)
            self.rect(0, 0, 210, 18, "F")
            self.set_text_color(255, 255, 255)
            self.set_font("Helvetica", "B", 12)
            self.set_xy(10, 4)
            self.cell(0, 10, "INDIA INFLATION IMPACT ANALYZER - Household Cost Report", ln=0, align="L")
            self.set_font("Helvetica", "", 9)
            self.cell(0, 10, "BK Birla College, Kalyan (B.Sc. DS & IT)", ln=0, align="R")
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            disclaimer = "Academic planning model. Predictions are statistical estimates based on MoSPI CPI data. Not certified financial advice."
            self.cell(0, 5, disclaimer, align="C", ln=1)
            self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C", ln=0)


def generate_pdf_report(
    household_name: str,
    city_type: str,
    monthly_income: float,
    current_spend: float,
    extra_rupees: float,
    personal_inflation_rate: float,
    headline_inflation_rate: float,
    category_rows: List[Dict[str, Any]],
    top_tips: List[str]
) -> bytes:
    """Generate printable PDF byte buffer for household inflation assessment."""
    if not HAS_FPDF:
        return b""

    pdf = InflationReportPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 1. Title Block
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(11, 31, 58)  # Navy
    pdf.cell(0, 8, f"Personal Cost Impact Assessment: {clean_text(household_name)}", ln=1)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    now_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
    pdf.cell(0, 5, f"Assessment Generated: {now_str} | Region: {city_type} | ML Model: XGBoost Regressor", ln=1)
    pdf.ln(3)

    # 2. Executive Impact Box
    if personal_inflation_rate <= headline_inflation_rate:
        pdf.set_fill_color(220, 252, 231)  # Light Green
        pdf.set_text_color(21, 128, 61)
        status_text = "STATUS: RESILIENT (Personal Inflation <= National Average)"
    else:
        pdf.set_fill_color(254, 243, 199)  # Light Amber
        pdf.set_text_color(180, 83, 9)
        status_text = "STATUS: AT RISK (High Inflation Exposure to Rising Commodity Baskets)"

    pdf.rect(10, pdf.get_y(), 190, 20, "F")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_xy(14, pdf.get_y() + 2)
    pdf.cell(180, 5, status_text, ln=1)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    pdf.set_x(14)
    summary_line = (
        f"Projected Monthly Increase: Rs. {extra_rupees:,.0f} | "
        f"Personal Inflation Rate: {personal_inflation_rate:.2f}% | "
        f"National Headline Rate: {headline_inflation_rate:.2f}%"
    )
    pdf.cell(180, 5, summary_line, ln=1)
    
    pdf.set_x(14)
    annual_burden = extra_rupees * 12
    pdf.cell(180, 5, f"Estimated Compounded Annualized Burden: Rs. {annual_burden:,.0f} / year", ln=1)
    pdf.ln(10)

    # 3. Monthly Financial Overview
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(11, 31, 58)
    pdf.cell(0, 6, "1. Monthly Budget Baseline & Deficit Projection", ln=1)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_text_color(51, 65, 85)

    col_w = [45, 45, 50, 50]
    pdf.set_font("Helvetica", "B", 8)
    headers = ["Monthly Income", "Current Spend", "Next Mo. Projected", "Extra Rupee Burden"]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.cell(col_w[0], 7, f"Rs. {monthly_income:,.0f}", border=1, align="C")
    pdf.cell(col_w[1], 7, f"Rs. {current_spend:,.0f}", border=1, align="C")
    pdf.cell(col_w[2], 7, f"Rs. {(current_spend + extra_rupees):,.0f}", border=1, align="C")
    pdf.cell(col_w[3], 7, f"+ Rs. {extra_rupees:,.0f}/mo", border=1, align="C")
    pdf.ln(10)

    # 4. Category-wise Breakdown Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(11, 31, 58)
    pdf.cell(0, 6, "2. Category-Wise Inflation Breakdown (MoSPI Calibrated)", ln=1)

    cat_cols = [55, 35, 35, 35, 30]
    cat_headers = ["Commodity Category", "Current (Rs.)", "Forecast Rate", "Next Mo. (Rs.)", "Extra Cost"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(241, 245, 249)
    for i, h in enumerate(cat_headers):
        pdf.cell(cat_cols[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    for row in category_rows:
        pdf.cell(cat_cols[0], 7, clean_text(row["name"]), border=1)
        pdf.cell(cat_cols[1], 7, f"Rs. {row['current']:,.0f}", border=1, align="R")
        pdf.cell(cat_cols[2], 7, clean_text(row["rate"]), border=1, align="C")
        pdf.cell(cat_cols[3], 7, f"Rs. {row['projected']:,.0f}", border=1, align="R")
        pdf.cell(cat_cols[4], 7, f"+ Rs. {row['extra']:,.0f}", border=1, align="R")
        pdf.ln()

    pdf.ln(6)

    # 5. Targeted Saving Levers
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(11, 31, 58)
    pdf.cell(0, 6, "3. Targeted Expense-Trimming Recommendations", ln=1)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for tip in top_tips:
        pdf.cell(5, 5, "-", ln=0)
        pdf.multi_cell(185, 5, clean_text(tip))
        pdf.ln(1)

    # Output bytes
    return bytes(pdf.output())
