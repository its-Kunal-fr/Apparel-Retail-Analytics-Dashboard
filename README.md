# Apparel Retail Analytics Dashboard

An interactive business intelligence dashboard for apparel and textiles retail. It demonstrates how sales, product, customer, returns, and inventory indicators can support practical decisions.

## Features
- Interactive date, region, category, and channel filters
- KPI cards for revenue, gross profit, gross margin, orders, average order value, units sold, and return rate
- Revenue and profit trends, category and regional comparisons, and top-product analysis
- Synthetic demo data so the app runs without credentials or external APIs
- KPI definitions and a dashboard design / implementation report

## Technology
Python, Streamlit, Pandas, NumPy, Plotly.

## Run locally
1. Install Python 3.10 or newer.
2. Clone this repository and open its folder.
3. Create a virtual environment with `python -m venv .venv`.
4. Activate it and run `pip install -r requirements.txt`.
5. Start the dashboard with `streamlit run app.py`.

## Data notice
The default dashboard generates synthetic demonstration data. Figures are illustrative and must not be represented as real company performance. For real analysis, replace the generator with a suitable, licensed public dataset and document its provenance and limitations.

## Potential public sources
- UCI Online Retail: https://archive.ics.uci.edu/dataset/352/online+retail (check whether the product taxonomy suits apparel)
- Kaggle datasets: https://www.kaggle.com/datasets (review the specific dataset license and provenance)
- India data portal: https://www.data.gov.in/ (verify relevance and license)

## Project structure
- `app.py` — interactive Streamlit dashboard
- `src/data_processing.py` — validation and KPI calculations
- `docs/KPI_Documentation.md` — KPI formulas and business rationale
- `reports/Dashboard_Design.md` — dashboard design and implementation plan
- `requirements.txt` — Python dependencies

## Responsible interpretation
Revenue alone does not establish business health. Review profitability, returns, inventory, seasonality, and promotions together. The prototype does not claim real-world findings.
