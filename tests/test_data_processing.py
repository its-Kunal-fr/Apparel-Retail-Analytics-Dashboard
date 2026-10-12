import pandas as pd
from src.data_processing import add_derived_columns, summarize_kpis, validate_sales_data


def sample_data():
    return pd.DataFrame({
        "order_date": ["2026-01-01", "2026-01-02"],
        "order_id": ["A", "A"],
        "product": ["Shirt", "Trousers"],
        "category": ["Men", "Men"],
        "region": ["North", "North"],
        "channel": ["Online", "Online"],
        "units": [2, 1],
        "unit_price": [100.0, 200.0],
        "unit_cost": [60.0, 120.0],
        "returned_units": [0, 1],
    })


def test_derived_columns_and_kpis():
    df = add_derived_columns(sample_data())
    kpis = summarize_kpis(df)
    assert df["revenue"].sum() == 400.0
    assert df["gross_profit"].sum() == 160.0
    assert kpis["orders"] == 1
    assert kpis["average_order_value"] == 400.0
    assert round(kpis["return_rate_pct"], 2) == 33.33


def test_valid_data_has_no_issues():
    df = add_derived_columns(sample_data())
    assert validate_sales_data(df) == []


def test_missing_columns_are_reported():
    assert any("Missing required columns" in item for item in validate_sales_data(pd.DataFrame({"units": [1]})))
