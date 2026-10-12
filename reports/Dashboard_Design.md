# Week 4 Internship Report: Interactive Apparel Retail Analytics Dashboard

## 1. Executive summary
This project prototypes an interactive dashboard for apparel and textiles retail. It brings sales performance, profitability, category and regional mix, channels, and returns into a single decision-support experience. The goal is to guide stakeholders from a business question to an insight and then to an action.

**Prototype status:** the dashboard runs with synthetic demonstration data. Connect and validate a suitable, licensed public dataset before presenting findings as empirical conclusions.

## 2. Business objectives
The dashboard is designed to answer:
1. How are revenue and gross profit changing over time?
2. Which categories and products contribute most to sales and gross profit?
3. Do regions and channels show different patterns?
4. What is the average order value?
5. Are returns unusually high in any category or product?
6. What data is needed to support inventory decisions?

These questions matter because apparel retailers manage seasonal demand, assortment, promotions, fit and sizing, multiple channels, and inventory risk. Revenue alone cannot show whether growth is profitable or whether returns undermine performance.

## 3. Stakeholders
- Retail managers: sales, profitability and regional performance.
- Merchandising teams: category/product mix, demand and returns.
- Marketing teams: channel contribution and campaign planning.
- Inventory planners: units sold, stock availability and future inventory turnover.
- Analysts/data stewards: data quality, metric definitions, refresh and reconciliation.

## 4. KPI selection and rationale
The prototype uses revenue, gross profit, gross margin, order count, average order value, units sold, return rate, category contribution, regional performance and channel mix. The formulas, business questions and caveats are documented in `docs/KPI_Documentation.md`.

The set balances **scale** (revenue, orders, units), **quality of sales** (profit and margin), **basket behaviour** (average order value), **product experience** (returns), and **business mix** (category, region and channel). Inventory turnover is a future KPI because it requires reliable inventory snapshots.

## 5. Dashboard design and navigation
The prototype is a single-page dashboard with persistent filters in the left sidebar: date range, category, region and channel. The main canvas follows a top-to-bottom narrative:
1. Performance snapshot: revenue, gross profit, margin, orders, average order value, units, return rate and product count.
2. Trend story: weekly revenue and gross-profit lines.
3. Mix story: category revenue and regional revenue/profit comparisons.
4. Product story: top-N products with profit, units and return-rate hover details.
5. Channel story: revenue share by channel.
6. Evidence/export: summary table, filtered detail rows and CSV download.

### Conceptual wireframe
```text
+---------------------------------------------------------------+
| APPAREL RETAIL ANALYTICS       Demo-data status / freshness    |
+-------------------+-------------------------------------------+
| FILTERS           | Revenue | Gross Profit | Margin | Orders   |
| Date range        | AOV     | Units         | Returns| Products |
| Category          +----------------------+--------------------+
| Region            | Weekly revenue       | Weekly profit      |
| Channel           +----------------------+--------------------+
|                   | Category comparison  | Regional comparison|
|                   +-------------------------------------------+
|                   | Top products / return details             |
|                   +----------------------+--------------------+
|                   | Channel mix          | Summary / export   |
+-------------------+-------------------------------------------+
```

### Visual choices
- KPI cards provide a fast read on scale and profitability.
- Line charts reveal direction and possible seasonality.
- Bar charts support accurate ranking across categories, regions and products.
- A donut chart communicates channel share when there are few channels; exact values remain available in data.
- Hover details and filters allow investigation without overcrowding the screen.
- CSV export supports follow-up analysis and audit of the filtered subset.

## 6. Visual storytelling workflow
1. **Notice:** identify a meaningful movement in revenue, margin, orders or returns.
2. **Locate:** filter to the categories, regions, channels or products associated with the movement.
3. **Explain:** compare revenue against margin, units and returns; investigate promotions, pricing, stockouts or return reasons in source systems.
4. **Act:** assign an owner and proposed action, such as reviewing discount depth or product sizing information.
5. **Verify:** compare the next period with a baseline and record whether the action helped.

Charts show associations, not proof of causation. Validate explanations before changing prices, inventory or campaigns.

## 7. Data source and integration strategy
### Prototype schema
One row represents an order line. Required fields are order date, order ID, product, category, region, channel, units, unit price, unit cost and returned units. Revenue, cost, gross profit and returned value are derived fields.

### Potential public sources
- UCI Online Retail: https://archive.ics.uci.edu/dataset/352/online+retail — transactional retail data; verify its taxonomy and field suitability for apparel.
- Kaggle: https://www.kaggle.com/datasets — search for fashion/apparel retail datasets and review each dataset's license and provenance.
- India data portal: https://www.data.gov.in/ — check relevance and license of any selected dataset.

Do not claim that a dataset supports a KPI if required fields are missing. If cost, returns or inventory are unavailable, omit those metrics or label any modelling assumptions explicitly.

### Integration workflow
1. Record source URL, retrieval date, license and version.
2. Profile columns, types, nulls, duplicates, ranges and date coverage.
3. Standardise dates, currency, product/category labels and region names.
4. Define order-line grain and resolve duplicates using source identifiers.
5. Handle cancellations and returns according to documented rules.
6. Map source fields to the dashboard schema; never fabricate missing fields.
7. Reconcile revenue and order totals with the source dataset.
8. Save a reproducible cleaned dataset and data dictionary.

## 8. Step-by-step implementation
1. **Environment:** install Python 3.10+, create a virtual environment and install `requirements.txt`.
2. **Ingestion:** replace the demo generator with a loader for the chosen CSV, API or warehouse; keep raw data separate.
3. **Validation:** test required columns, nulls, duplicates, ranges and reconciliation.
4. **Transformation:** calculate revenue, cost, gross profit and return metrics in `src/data_processing.py`.
5. **KPI layer:** centralise definitions so charts do not use inconsistent calculations.
6. **Interface:** use Streamlit sidebar controls; every KPI and chart must use the same filtered data.
7. **Visuals:** build trends, category/region bars, top-product analysis and channel mix with Plotly.
8. **Verification:** test filter combinations, empty selections, missing values, zero revenue, date boundaries and CSV totals.
9. **Deployment:** deploy to an approved Streamlit-compatible host; keep secrets out of source control.
10. **Review:** ask representative stakeholders to complete common tasks and provide feedback.

## 9. Data refresh and maintenance
- **Prototype:** data is generated in the app; no external refresh is configured.
- **CSV production:** refresh based on source publication frequency, validate the new file, retain dated snapshots and display the latest successful refresh time.
- **API/warehouse production:** use an approved scheduled pipeline with retries, logs, schema checks and alerts. Never commit API keys to GitHub.
- **Every refresh:** check freshness, row counts, null rates, duplicates, outliers and reconciliation; flag or block failed refreshes.
- **Monthly:** review KPI definitions, category mappings, access rights, performance and stakeholder feedback.

## 10. Interactivity and accessibility
Filters should apply consistently and selected segments should be visible. Hover tooltips provide detail and users can download filtered rows. Use descriptive titles, labelled axes, readable number formats, adequate contrast and do not rely on colour alone. Show an empty-state message when no records match filters.

## 11. Evaluation plan
Evaluate the dashboard against:
- Business relevance: each KPI answers a defined business question.
- Correctness: formulas, totals and filter behaviour are tested.
- Usability: stakeholders can find trends and comparisons quickly.
- Traceability: source, license, transformations and metric definitions are documented.
- Maintainability: preparation is separated from interface and refresh errors are visible.
- Responsible use: synthetic data is labelled and sensitive customer data is minimised.

Acceptance tests: filtered totals match a manual calculation; return rate uses the documented unit denominator; CSV totals match the visible filtered view; and an empty selection does not crash the app.

## 12. Limitations and next steps
Synthetic data cannot establish real market trends. Inventory turnover, sell-through, stockout rate, markdown rate, customer retention and size-level return analysis need additional trustworthy fields. The prototype does not model tax, discounts, channel fees, shipping costs or net profit. Add these only with clear definitions and validated data.

## 13. Conclusion
The dashboard makes analytics more actionable by linking sales scale to profitability, returns and business mix. A documented KPI layer, consistent filters, validation checks and transparent refresh process help decision-makers trust the visual story. The next step is to connect a licensed public dataset, validate its suitability and replace illustrative figures before drawing business conclusions.
