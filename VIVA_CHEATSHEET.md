# 🎓 Complete Viva Cheat Sheet & Presentation Guide
## India Inflation Impact Analyzer & Personal Cost Predictor
**B.Sc. Data Science & IT | Final Year Project**  
**BK Birla College of Arts, Science & Commerce (Autonomous), Kalyan**  
**Team**: Arsalan & Ayaan Shaikh

---

## ⏱️ 1. The 1-Minute Elevator Pitch (Memorize This!)

> *"Respected Examiners, every month the Reserve Bank of India and MoSPI publish official headline inflation numbers — for example, 6%. But for an ordinary Indian family, a percentage number doesn't tell them how much their grocery bill, school fees, or fuel expenses will actually rise next month.*  
>  
> *Our project, **India Inflation Impact Analyzer**, solves this problem. It uses **Machine Learning (XGBoost Regressor)** trained on official MoSPI CPI time-series data to forecast category-wise inflation, and directly translates macro trends into **personalized, actionable Rupee impacts** on a household's monthly budget.*  
>  
> *Instead of saying 'inflation is 6%', our tool tells a family: 'Next month, your expenses will increase by ₹1,420 in Rupees'."*

---

## 🎬 2. The 5-Minute Live Demo Walkthrough

Follow these steps on your screen during the demo:

### Step 1: Open the App & Highlight National KPIs (30 Seconds)
- Point to the top metric cards:
  - *"Here we show the official National Headline CPI (Base 2012=100) and the latest Year-on-Year inflation."*
  - *"Notice that while Headline inflation is ~5.5%, Food & Grocery inflation is higher at 6.8%. This proves why a single national number doesn't tell the full story."*

### Step 2: Tab 1 — National Trends (1 Minute)
- Click on **📈 1. National Trends**:
  - Show the 10-year Plotly interactive line chart.
  - Show the 3-Year CAGR comparison table.
  - Examiner pitch: *"We collected 10 years of monthly historical data from MoSPI across 6 core commodity baskets: Food, Fuel, Housing, Medical, Education, and Transport."*

### Step 3: Tab 2 — Machine Learning Price Predictor (1.5 Minutes)
- Click on **🤖 2. ML Price Predictor**:
  - Select *Food & Beverages*.
  - Show the **Actual vs. Predicted Plot**: *"We tested the model on the last 12 months out-of-sample data. The predicted dashed line closely tracks actual price spikes."*
  - Point to the metrics:
    - **$R^2$ Score**: ~0.86 (*"This means our model explains over 85% of price variance."*)
    - **RMSE**: Low error points.
  - Open the **Feature Importance** dropdown: *"Our model relies on Lag 1, Lag 2, Lag 3, and 3-month rolling averages, capturing seasonal momentum."*

### Step 4: Tab 3 — Personal Impact Calculator (The Star Feature!) (1.5 Minutes)
- Click on **💰 3. Personal Impact Calculator**:
  - Click **[Load Middle-Class Family]** preset button (or enter custom numbers).
  - Point to the result banner:
    - **"Next month, your family will spend + ₹1,420 MORE."**
    - Show the horizontal bar chart showing where the extra rupees go (e.g. ₹750 in groceries, ₹280 in fuel).
  - Examiner pitch: *"This is the core innovation of our project. It translates macroeconomic indices into a household's real monthly cash-flow."*

### Step 5: Tab 4 — Smart Budget Tips (30 Seconds)
- Click on **💡 4. Smart Budget Tips**:
  - Explain that the tool gives personalized advice (e.g., seasonal vegetable swaps, power slab limits, generic medicines from Jan Aushadhi Kendras).

---

## ❓ 3. Top 10 Expected Viva Questions & Bulletproof Answers

#### Q1: Why did you choose this problem for your final year project?
> **Answer**: *"Because inflation is a universal problem affecting 1.4 billion Indians. Government websites only show raw percentages and index numbers. There is no consumer-facing tool that personalizes this data into Rupees for household budgeting."*

#### Q2: Where did you get the dataset? Is it real or synthetic?
> **Answer**: *"We used real historical data published by the Ministry of Statistics and Programme Implementation (MoSPI), Government of India. It covers monthly CPI series from 2015 to 2026 across 6 major commodity baskets (Base 2012=100)."*

#### Q3: Why did you choose XGBoost instead of Linear Regression?
> **Answer**: *"Linear Regression assumes a straight linear relationship between variables. But Indian commodity prices experience non-linear seasonal shocks (e.g., monsoon vegetable price spikes or crude oil shocks). XGBoost uses gradient boosted decision trees that handle non-linear lag relationships and outliers significantly better."*

#### Q4: What features did you engineer for the ML model?
> **Answer**: *"We engineered 5 time-series features:  
> 1. **Lag 1**: Price index from 1 month ago.  
> 2. **Lag 2 & Lag 3**: Price indices from 2 and 3 months ago.  
> 3. **Rolling Mean (3-Month)**: Moving average to smooth out short-term noise.  
> 4. **Calendar Month (1–12)**: To capture seasonal festive and monsoon patterns."*

#### Q5: How did you evaluate your model?
> **Answer**: *"We used an out-of-sample time-series test split (holding out the last 12 months). We evaluated using **RMSE (Root Mean Squared Error)** to penalize large errors, and **$R^2$ Score** (which is ~0.86), proving that 86% of the variance is captured by our model."*

#### Q6: What is the formula for Personal Inflation Rate?
> **Answer**:  
> $$\text{Personal Inflation Rate (\%)} = \frac{\sum (\text{User Expense}_i \times \text{Predicted Category Inflation}_i)}{\text{Total Monthly Household Spend}} \times 100$$  
> *"It weights each inflation rate according to the family's actual spending pattern rather than the national basket weight."*

#### Q7: Why use Streamlit instead of React/Django?
> **Answer**: *"Streamlit is native to Python and the Data Science ecosystem. It eliminates frontend overhead and allows seamless integration with Pandas, Scikit-Learn, and Plotly, enabling us to deliver a reactive, interactive dashboard in pure Python."*

#### Q8: How does the app prevent data leakage in time-series?
> **Answer**: *"In time-series data, future data must never leak into the past. We strictly split the data sequentially: training on historical months and testing on subsequent future months, rather than using random k-fold shuffling."*

#### Q9: What was the division of work between DS and IT students?
> **Answer**:  
> - **Data Science Student**: Sourced MoSPI CPI data, performed exploratory data analysis (EDA), engineered lag features, and trained/tuned the XGBoost forecasting model.  
> - **IT Student**: Architected the Streamlit web application, built the Personal Impact Calculator mathematical engine, integrated interactive Plotly visualizations, and designed the UI layout.

#### Q10: What are the future enhancements for this project?
> **Answer**:  
> *"1. State-level and rural/urban price divergence (since prices vary across Maharashtra vs Delhi).  
> 2. Integration with RBI's Account Aggregator framework to automatically read bank statements with user consent.  
> 3. Multi-language support (Hindi, Marathi) for wider accessibility."*

---

## 💡 Quick Tips for Viva Day
1. **Be confident and concise**: Answer directly in 2 sentences. Don't ramble.
2. **Always lead with the user impact**: Whenever asked about accuracy or algorithms, bring it back to *"how this helps a common Indian family save money"*.
3. **Keep the app running**: Have `streamlit run app.py` open on `localhost:8501` before the examiners call your roll numbers!
