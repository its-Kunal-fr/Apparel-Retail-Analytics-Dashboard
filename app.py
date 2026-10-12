from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from src.data_processing import add_derived_columns, summarize_kpis, validate_sales_data

st.set_page_config(page_title="Apparel Retail Analytics", page_icon="🧵", layout="wide")
CATEGORIES = ["Women", "Men", "Kids", "Footwear", "Accessories"]
REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Online", "Store", "Marketplace"]


@st.cache_data
def make_demo_data(rows: int = 1800) -> pd.DataFrame:
    """Create reproducible synthetic data for demonstration only."""
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=365, freq="D")
    products = {
        "Women": ["Kurta", "Dress", "Top", "Jeans"],
        "Men": ["Shirt", "Trousers", "T-shirt", "Jacket"],
        "Kids": ["Kids Set", "School Wear", "Kids Dress"],
        "Footwear": ["Sneakers", "Sandals", "Formal Shoes"],
        "Accessories": ["Scarf", "Belt", "Bag", "Cap"],
    }
    category = rng.choice(CATEGORIES, rows, p=[.29, .25, .16, .18, .12])
    product = [rng.choice(products[c]) for c in category]
    base_price = {"Women": 950, "Men": 1100, "Kids": 600, "Footwear": 1450, "Accessories": 450}
    unit_price = np.array([base_price[c] for c in category]) * rng.uniform(.65, 1.55, rows)
    units = rng.choice([1, 2, 3, 4, 5], rows, p=[.49, .27, .13, .07, .04])
    order_ids = [f"ORD-{n:06d}" for n in rng.integers(1, int(rows * .72), rows)]
    returned_units = np.array([rng.binomial(int(u), .055) for u in units])
    data = pd.DataFrame({
        "order_date": rng.choice(dates, rows), "order_id": order_ids, "product": product,
        "category": category, "region": rng.choice(REGIONS, rows),
        "channel": rng.choice(CHANNELS, rows, p=[.42, .38, .20]), "units": units,
        "unit_price": np.round(unit_price, 2),
        "unit_cost": np.round(unit_price * rng.uniform(.42, .72, rows), 2),
        "returned_units": returned_units,
    })
    return add_derived_columns(data)


def money(value: float) -> str:
    return f"₹{value:,.0f}"


st.title("🧵 Apparel Retail Analytics Dashboard")
st.caption("Decision-support prototype for sales, profitability, product mix and returns.")
st.info("Demo mode: all figures are generated synthetic data, not actual company results.")
raw = make_demo_data()
issues = validate_sales_data(raw)
if issues:
    st.error("Data validation needs attention: " + " | ".join(issues))
    st.stop()

with st.sidebar:
    st.header("Dashboard controls")
    st.caption("Filters update all charts and KPIs.")
    min_date, max_date = raw["order_date"].min().date(), raw["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    selected_categories = st.multiselect("Product category", CATEGORIES, default=CATEGORIES)
    selected_regions = st.multiselect("Region", REGIONS, default=REGIONS)
    selected_channels = st.multiselect("Sales channel", CHANNELS, default=CHANNELS)
    st.divider()
    st.caption("Production use requires a licensed data source and a verified refresh process.")

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df = raw[
    raw["order_date"].dt.date.between(start_date, end_date)
    & raw["category"].isin(selected_categories)
    & raw["region"].isin(selected_regions)
    & raw["channel"].isin(selected_channels)
].copy()
if df.empty:
    st.warning("No rows match these filters. Expand the date range or select more categories, regions, or channels.")
    st.stop()

k = summarize_kpis(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", money(k["revenue"]))
c2.metric("Gross profit", money(k["gross_profit"]))
c3.metric("Gross margin", f'{k["gross_margin_pct"]:.1f}%')
c4.metric("Orders", f'{k["orders"]:,}')
c5, c6, c7, c8 = st.columns(4)
c5.metric("Average order value", money(k["average_order_value"]))
c6.metric("Units sold", f'{k["units_sold"]:,}')
c7.metric("Return rate", f'{k["return_rate_pct"]:.1f}%')
c8.metric("Products represented", f'{df["product"].nunique():,}')

st.subheader("1. What is happening over time?")
daily = df.groupby(pd.Grouper(key="order_date", freq="W")).agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum")).reset_index()
left, right = st.columns(2)
with left:
    fig = px.line(daily, x="order_date", y="revenue", markers=True, title="Weekly revenue trend", labels={"order_date": "Week", "revenue": "Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.line(daily, x="order_date", y="gross_profit", markers=True, title="Weekly gross profit", labels={"order_date": "Week", "gross_profit": "Gross profit (₹)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("2. Which categories and regions contribute?")
left, right = st.columns(2)
category_summary = df.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("gross_profit", "sum"), units=("units", "sum")).sort_values("revenue", ascending=False)
with left:
    fig = px.bar(category_summary, x="category", y="revenue", color="category", title="Revenue by category", labels={"category": "Category", "revenue": "Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    region_summary = df.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("gross_profit", "sum")).sort_values("revenue", ascending=False)
    fig = px.bar(region_summary, x="region", y="revenue", color="profit", title="Regional revenue (colour indicates gross profit)", labels={"region": "Region", "revenue": "Revenue (₹)", "profit": "Gross profit (₹)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("3. Product performance and returns")
product_summary = df.groupby(["product", "category"], as_index=False).agg(revenue=("revenue", "sum"), profit=("gross_profit", "sum"), units=("units", "sum"), returned_units=("returned_units", "sum"))
product_summary["return_rate_pct"] = np.where(product_summary["units"] > 0, product_summary["returned_units"] / product_summary["units"] * 100, 0)
top_n = st.slider("Number of products to show", min_value=5, max_value=15, value=10)
top_products = product_summary.nlargest(top_n, "revenue")
fig = px.bar(top_products.sort_values("revenue"), x="revenue", y="product", color="category", orientation="h", hover_data=["profit", "units", "return_rate_pct"], title=f"Top {top_n} products by revenue", labels={"revenue": "Revenue (₹)", "product": "Product", "category": "Category"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("4. Channel mix and detailed table")
left, right = st.columns(2)
with left:
    channel = df.groupby("channel", as_index=False).agg(revenue=("revenue", "sum"))
    fig = px.pie(channel, names="channel", values="revenue", hole=.48, title="Revenue share by channel")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown("**Filtered category summary**")
    st.dataframe(category_summary, use_container_width=True, hide_index=True)
with st.expander("View filtered order-line data"):
    st.dataframe(df.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
    st.download_button("Download filtered data as CSV", df.to_csv(index=False).encode("utf-8"), file_name="apparel_retail_filtered.csv", mime="text/csv")
st.caption("Interpret revenue alongside gross margin and return rate before making assortment or promotion decisions.")
