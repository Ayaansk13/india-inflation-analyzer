"""
Dynamic Recommendation Engine for Parivar-Arth.
Generates mathematically targeted, non-static household savings strategies
conditioned on user expenditure distributions and sector-specific inflation shocks.
"""

from typing import Dict, List, Any, Tuple
import pandas as pd

def analyze_household_vulnerability(
    expenses: Dict[str, float],
    category_inflation: Dict[str, float]
) -> Dict[str, Any]:
    """
    Computes household exposure metrics:
    - Absolute cost increase per category
    - Top inflation driver (highest absolute monetary increase)
    - Vulnerability score
    """
    total_spend = sum(expenses.values())
    if total_spend <= 0:
        total_spend = 1.0  # Guard against division by zero

    category_deltas = {}
    weighted_inflation_sum = 0.0

    for cat, amount in expenses.items():
        rate = category_inflation.get(cat, 5.0)
        monthly_delta = amount * (rate / 100.0) / 12.0
        annual_delta = amount * (rate / 100.0)
        share = (amount / total_spend) * 100.0
        
        category_deltas[cat] = {
            "current_spend": amount,
            "share_pct": round(share, 1),
            "inflation_rate": round(rate, 2),
            "monthly_increase": round(monthly_delta, 2),
            "annual_increase": round(annual_delta, 2),
        }
        weighted_inflation_sum += (amount / total_spend) * rate

    # Sort categories by highest absolute monthly cost increase
    sorted_drivers = sorted(
        category_deltas.items(),
        key=lambda item: item[1]["monthly_increase"],
        reverse=True
    )
    
    top_driver_name = sorted_drivers[0][0] if sorted_drivers else "Food"
    top_driver_info = sorted_drivers[0][1] if sorted_drivers else {}

    # Discretionary vs Essential spend
    essential_cats = ["Food", "Fuel", "Transport", "Rent", "Healthcare", "Education", "Utilities"]
    essential_spend = sum(expenses.get(c, 0.0) for c in essential_cats)
    discretionary_spend = total_spend - essential_spend

    return {
        "total_spend": round(total_spend, 2),
        "personal_inflation_rate": round(weighted_inflation_sum, 2),
        "total_monthly_increase": round(sum(d["monthly_increase"] for d in category_deltas.values()), 2),
        "total_annual_increase": round(sum(d["annual_increase"] for d in category_deltas.values()), 2),
        "top_driver": top_driver_name,
        "top_driver_details": top_driver_info,
        "category_breakdown": category_deltas,
        "essential_ratio": round((essential_spend / total_spend) * 100.0, 1),
        "discretionary_ratio": round((discretionary_spend / total_spend) * 100.0, 1),
    }

def generate_savings_recommendations(
    analysis: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Synthesizes tailored, actionable, high-ROI financial mitigations.
    Adapts dynamically to the household's top inflation driver and discretionary leakages.
    """
    top_driver = analysis["top_driver"]
    expenses = {cat: val["current_spend"] for cat, val in analysis["category_breakdown"].items()}
    category_inflation = {cat: val["inflation_rate"] for cat, val in analysis["category_breakdown"].items()}
    recommendations = []

    # 1. Primary Sector Action Plans
    if top_driver == "Food":
        food_spend = expenses.get("Food", 0)
        food_inf = category_inflation.get("Food", 6.0)
        recommendations.append({
            "category": "Food & Provisions",
            "priority": "HIGH",
            "title": "Bypassing Retail Aggregators for Dry Staples & Pulses",
            "impact_level": "High Impact",
            "action": (
                f"With Food inflation running at {food_inf}%, retail markup on staples (wheat, basmati rice, pulses, cooking oil) "
                f"adds 15-22% to unit costs. Transitioning dry grocery procurement to wholesale co-operatives (e.g. Kendriya Bhandar / APMC outlets) "
                f"or quarterly bulk buying eliminates mid-stream retail distributor premiums."
            ),
            "estimated_savings_monthly": round(food_spend * 0.12, 0),
            "implementation_timeframe": "Immediate (Next Grocery Cycle)"
        })
        recommendations.append({
            "category": "Food & Dining",
            "priority": "MEDIUM",
            "title": "Mitigating Vegetable Volatility via Seasonal Crop Substitution",
            "impact_level": "Medium Impact",
            "action": (
                "Perishable food crops (tomatoes, onions, green chillies) experience episodic 40-70% monsoon spikes. "
                "Adopting seasonal vegetable calendars and replacing out-of-season greenhouse produce with locally abundant native tubers "
                "and legumes shields household food outlay from supply-chain volatility."
            ),
            "estimated_savings_monthly": round(food_spend * 0.07, 0),
            "implementation_timeframe": "1-2 Weeks"
        })

    elif top_driver in ["Fuel", "Transport"]:
        transport_spend = expenses.get("Transport", 0) + expenses.get("Fuel", 0)
        fuel_inf = category_inflation.get("Fuel", 5.5)
        recommendations.append({
            "category": "Mobility & Fuel",
            "priority": "HIGH",
            "title": "Commute Multimodal Optimization & Transit Passes",
            "impact_level": "High Impact",
            "action": (
                f"Combined mobility outlay is your highest inflation transmitter ({fuel_inf}% annual trend). "
                f"Replacing two peak solo automobile commute days per week with metro rail, commuter train, or intra-office "
                f"carpooling reduces petroleum fuel consumption by approximately 30-38%."
            ),
            "estimated_savings_monthly": round(transport_spend * 0.22, 0),
            "implementation_timeframe": "Within 7 Days"
        })
        recommendations.append({
            "category": "Fuel Efficiency",
            "priority": "LOW",
            "title": "Fleet Maintenance Calibration & Surcharge Mitigation",
            "impact_level": "Low Impact",
            "action": (
                "Maintaining recommended tyre PSI pressure (+2 PSI on highway runs) and periodic engine tuning yields a 6-9% mileage boost. "
                "Pairing refuels with zero-surcharge institutional fuel cards provides an additional 1.5% cashback rebate."
            ),
            "estimated_savings_monthly": round(transport_spend * 0.06, 0),
            "implementation_timeframe": "Immediate"
        })

    elif top_driver in ["Rent", "Utilities"]:
        housing_spend = expenses.get("Rent", 0) + expenses.get("Utilities", 0)
        recommendations.append({
            "category": "Housing & Energy",
            "priority": "HIGH",
            "title": "Residential Energy Efficiency & Peak Tariff Modulation",
            "impact_level": "High Impact",
            "action": (
                "Electricity tariffs and domestic cooling costs represent sticky recurring overheads. "
                "Calibrating air conditioner thermostats to the Bureau of Energy Efficiency (BEE) recommended 24°C "
                "and transitioning high-uptime ceiling fans to 28W brushless DC (BLDC) motors lowers utility load by up to 24%."
            ),
            "estimated_savings_monthly": round(housing_spend * 0.10, 0),
            "implementation_timeframe": "1 Month"
        })
        recommendations.append({
            "category": "Lease Management",
            "priority": "MEDIUM",
            "title": "Long-Term Rental Agreement Indexation Cap",
            "impact_level": "Medium Impact",
            "action": (
                "During lease renewals, negotiate a multi-year term with escalation pegged to the official CPI Housing Index "
                "(currently ~4-5%) rather than standard arbitrary 10-12% landlord renegotiation clauses."
            ),
            "estimated_savings_monthly": round(expenses.get("Rent", 0) * 0.05, 0),
            "implementation_timeframe": "At Lease Renewal"
        })

    elif top_driver == "Healthcare":
        health_spend = expenses.get("Healthcare", 0)
        recommendations.append({
            "category": "Healthcare & Wellness",
            "priority": "HIGH",
            "title": "Bioequivalent Generic Medicine Substitution (Jan Aushadhi)",
            "impact_level": "High Impact",
            "action": (
                "For chronic prescriptions (cardiovascular, diabetes, hypertension), sourcing WHO-GMP certified generic equivalents "
                "via Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) centers provides the identical active pharmaceutical "
                "ingredient at a 50% to 75% discount compared to premium branded formulations."
            ),
            "estimated_savings_monthly": round(health_spend * 0.35, 0),
            "implementation_timeframe": "Next Prescription Refill"
        })

    # 2. Discretionary Expense Optimization (If Shopping or Entertainment > 15% of budget)
    if analysis["discretionary_ratio"] >= 15.0:
        disc_spend = expenses.get("Entertainment", 0) + expenses.get("Shopping", 0)
        recommendations.append({
            "category": "Discretionary Optimization",
            "priority": "MEDIUM",
            "title": "Subscription Rationalization & 72-Hour Purchase Cooling Rule",
            "impact_level": "Medium Impact",
            "action": (
                f"Discretionary spending accounts for {analysis['discretionary_ratio']}% of total monthly cash flow. "
                f"Conducting an audit of auto-renewing digital subscriptions (OTT, fitness, micro-services) and enforcing a mandatory "
                f"72-hour cooling period for non-essential online shopping curbs impulse inflation exposure."
            ),
            "estimated_savings_monthly": round(disc_spend * 0.20, 0),
            "implementation_timeframe": "Immediate"
        })

    # 3. Macro Emergency Cushion Rule
    total_savings_potential = sum(r["estimated_savings_monthly"] for r in recommendations)
    recommendations.append({
        "category": "Financial Resiliency",
        "priority": "HIGH",
        "title": "Inflation-Indexed Liquid Emergency Reserve Allocation",
        "impact_level": "Strategic",
        "action": (
            f"By implementing the targeted sector mitigations above, the household can liberate approximately "
            f"INR {total_savings_potential:,.0f} per month (INR {total_savings_potential * 12:,.0f} annually). "
            f"Direct these freed funds into high-yield liquid mutual funds or inflation-protected treasury deposits "
            f"yielding 6.8%-7.2% to ensure household capital beats the headline CPI depletion rate."
        ),
        "estimated_savings_monthly": total_savings_potential,
        "implementation_timeframe": "Ongoing Systemic"
    })

    return recommendations
