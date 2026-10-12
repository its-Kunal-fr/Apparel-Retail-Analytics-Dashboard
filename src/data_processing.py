"""Reusable data preparation and KPI functions for the apparel retail dashboard."""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {
    "order_date", "order_id", "product", "category", "region", "channel",
    "units", "unit_price", "unit_cost", "returned_units"
}


def validate_sales_data(df: pd.DataFrame) -> list[str]:
    """Return validation issues; an empty list means required fields are present and usable."""
    issues: list[str] = []
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        issues.append("Missing required columns: " + ", ".join(sorted(missing)))
        return issues
    if df.empty:
        issues.append("Dataset is empty.")
        return issues
    if (df["units"] < 0).any():
        issues.append("Units contains negative values; confirm cancellation treatment.")
    if (df["returned_units"] < 0).any():
        issues.append("Returned units cannot be negative.")
    if (df["returned_units"] > df["units"]).any():
        issues.append("Returned units exceed units sold in at least one row.")
    if (df["unit_price"] < 0).any() or (df["unit_cost"] < 0).any():
        issues.append("Price and cost should be non-negative.")
    return issues


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with revenue, cost, profit and returned-value measures."""
    out = df.copy()
    out["order_date"] = pd.to_datetime(out["order_date"], errors="coerce")
    out["revenue"] = out["units"] * out["unit_price"]
    out["cost"] = out["units"] * out["unit_cost"]
    out["gross_profit"] = out["revenue"] - out["cost"]
    out["returned_value"] = out["returned_units"] * out["unit_price"]
    return out


def summarize_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Calculate aggregate KPIs from rows representing order-line items."""
    revenue = float(df["revenue"].sum())
    profit = float(df["gross_profit"].sum())
    orders = int(df["order_id"].nunique())
    units = int(df["units"].sum())
    return {
        "revenue": revenue,
        "gross_profit": profit,
        "gross_margin_pct": profit / revenue * 100 if revenue else 0.0,
        "orders": orders,
        "average_order_value": revenue / orders if orders else 0.0,
        "units_sold": units,
        "return_rate_pct": float(df["returned_units"].sum()) / units * 100 if units else 0.0,
    }
