# KPI Documentation: Apparel Retail Analytics

## Purpose
KPIs connect business questions to measurable indicators. The prototype uses synthetic data; its default figures are not evidence of real business performance.

| KPI | Definition / formula | Business question | Caution |
|---|---|---|---|
| Revenue | Sum of units × unit selling price | How much sales value was generated? | Define treatment of tax, discounts, cancellations and refunds. |
| Gross profit | Revenue − cost of goods sold | Which sales contribute value before operating expenses? | Unit cost must be current and consistently defined. |
| Gross margin % | Gross profit ÷ revenue × 100 | Are sales profitable relative to revenue? | Not net profit; excludes overhead and other expenses. |
| Orders | Distinct order IDs | How many orders were placed? | Deduplicate IDs and define cancelled orders. |
| Average order value | Revenue ÷ distinct orders | What is the average sales value per order? | Keep order and revenue definitions consistent. |
| Units sold | Sum of units sold | How many items were purchased? | Define whether cancellations are excluded. |
| Return rate % | Returned units ÷ units sold × 100 | What share of sold units came back? | Unit-based rate differs from order- or value-based rates. |
| Category contribution | Category revenue ÷ total filtered revenue × 100 | Which categories drive sales? | Revenue share is not profit share. |
| Regional performance | Revenue and gross profit by region | Where are sales and contribution strongest? | Consider regional size, seasonality and distribution coverage. |
| Channel mix | Channel revenue ÷ total filtered revenue × 100 | How do channels compare? | Channel fees, delivery and fulfilment costs may be excluded. |
| Product performance | Revenue, profit, units and return rate by product | Which products need attention? | Include stock availability to avoid penalising out-of-stock products. |
| Inventory turnover (future extension) | Cost of goods sold ÷ average inventory at cost | How efficiently is inventory converted into sales? | Requires reliable inventory snapshots. |

## KPI design principles
1. Use consistent date boundaries, currency, tax, discount and return definitions.
2. Display revenue beside gross profit and gross margin to avoid optimising volume alone.
3. Compare periods only when date coverage and definitions are comparable.
4. Show units and denominators alongside percentages.
5. Ensure all charts and KPIs use the same filters.
6. Show freshness, coverage and data-quality status in production.

## Illustrative decision prompts
- Revenue rises while margin falls: investigate discounts, product mix and supplier costs.
- Return rate rises for a category: examine sizing, product descriptions, fit, quality and return reasons.
- Demand is strong but stock is low: review replenishment lead time before promoting the item.
- A channel grows while contribution falls: include commissions, delivery and fulfilment costs before increasing investment.

## Required data schema
Minimum line-item schema: order date, order ID, product, category, region, channel, units, unit price, unit cost, returned units. Further useful fields include discounts, taxes, cancellation status, return reason, inventory snapshots, size, shipping cost and channel fees.

## Data quality checks
- Missing dates, product IDs, category, channel or cost
- Duplicate order-line identifiers
- Negative units, price or cost
- Returned units greater than purchased units
- Currency and timezone consistency
- Outliers, sudden volume changes and unmapped categories
- Reconciliation against source-system totals
