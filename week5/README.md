# Week 5 — Apparel & Textiles Trend Analysis and Forecasting

This project extends the Apparel Retail Analytics Dashboard with a reproducible trend-analysis and forecasting workflow.

## Objective
Analyze monthly apparel demand, compare baseline forecasting methods, generate a short-term forecast, and translate the results into inventory and merchandising decisions.

## Repository contents
- `sample_monthly_sales.csv`: 60 months of **synthetic demonstration data**. It is not actual retailer data or official market statistics.
- `forecast_trends.py`: data validation, trend plotting, model comparison, and forecast generation.
- `outputs/`: created locally when the script runs; includes model metrics, forecast CSV, and PNG charts.

## Methods
1. **3-month moving average** — simple baseline that smooths short-term noise.
2. **Seasonal-naïve forecast** — uses the corresponding month from the previous year as a benchmark.
3. **Linear trend regression** — estimates a linear time trend.
4. **SARIMA** — seasonal time-series model used for the forward forecast when Statsmodels is available; the script falls back to seasonal naïve if fitting fails.

Models are compared on a chronological holdout window using MAE, RMSE, and WAPE. Lower values indicate smaller errors. Never randomly shuffle time-series rows.

## Run locally
Use Python 3.10+.

```bash
pip install -r requirements.txt
python week5/forecast_trends.py
```

To use your own monthly data:

```bash
python week5/forecast_trends.py --input path/to/monthly_sales.csv --horizon 6
```

Required columns: `date` (month-start date, e.g. `2025-01-01`) and `units_sold`. Optional fields such as category, net sales, average selling price, promotion flag, and stockout flag can be retained for future extensions.

## Outputs
The script writes:
- `week5/outputs/model_comparison.csv`
- `week5/outputs/future_forecast.csv`
- `week5/outputs/historical_trend.png`
- `week5/outputs/forecast.png`

## Interpretation and limitations
Synthetic data is included so the workflow runs immediately. Do not describe its results as real market findings. For a business-grade analysis, replace it with documented retailer data or public monthly trade data, verify product-code definitions, account for inflation and exchange rates where relevant, flag promotions and stockouts, and validate forecasts with rolling-origin backtesting. Market-value growth, trade values, fiber production, and retailer unit sales are different measures and must not be combined as if they were the same series.

## Public sources for real-world context
- [Textile Exchange — Materials Market Reports](https://textileexchange.org/knowledge-center/)
- [UN Comtrade](https://comtradeplus.un.org/)
- [World Bank Data](https://data.worldbank.org/)
- [Google Trends](https://trends.google.com/trends/)

## Business recommendations to test
- Replenish proven products based on category-level demand rather than broad market growth alone.
- Use forecast intervals and supplier lead times when setting safety stock.
- Track forecast bias alongside accuracy to reduce excess inventory and stockouts.
- Treat sustainability and recycled-content claims as evidence and supplier-traceability requirements.
