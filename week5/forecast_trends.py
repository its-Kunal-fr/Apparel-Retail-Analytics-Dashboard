"""Week 5: apparel trend analysis and monthly demand forecasting.

The included CSV is synthetic demonstration data, not real market observations.
Run from the repository root:
    python week5/forecast_trends.py
Optional:
    python week5/forecast_trends.py --input path/to/your_monthly_sales.csv --horizon 6
Expected columns: date, units_sold. Other columns are optional.
"""
from pathlib import Path
import argparse
import warnings

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "sample_monthly_sales.csv"
OUTPUT = ROOT / "outputs"


def load_data(path):
    df = pd.read_csv(path, parse_dates=["date"])
    required = {"date", "units_sold"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df = df.sort_values("date").drop_duplicates("date")
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce")
    df = df.dropna(subset=["date", "units_sold"])
    df = df.set_index("date").asfreq("MS")
    if df["units_sold"].isna().any():
        warnings.warn("Missing months found. They are interpolated for this demo; review before business use.")
        df["units_sold"] = df["units_sold"].interpolate(limit_direction="both")
    if len(df) < 24:
        raise ValueError("Use at least 24 monthly observations; 48–60+ is preferable.")
    return df


def forecast_moving_average(train, horizon, window=3):
    level = float(train["units_sold"].tail(window).mean())
    return np.repeat(level, horizon)


def forecast_seasonal_naive(train, horizon):
    y = train["units_sold"].to_numpy()
    if len(y) < 12:
        return forecast_moving_average(train, horizon)
    return np.array([y[-12 + (i % 12)] for i in range(horizon)], dtype=float)


def forecast_linear_trend(train, horizon):
    y = train["units_sold"].to_numpy()
    x = np.arange(len(y)).reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    future_x = np.arange(len(y), len(y) + horizon).reshape(-1, 1)
    return np.maximum(model.predict(future_x), 0)


def evaluate_holdout(df, test_months=12):
    train, test = df.iloc[:-test_months], df.iloc[-test_months:]
    preds = {
        "3-month moving average": forecast_moving_average(train, len(test)),
        "Seasonal naive": forecast_seasonal_naive(train, len(test)),
        "Linear trend regression": forecast_linear_trend(train, len(test)),
    }
    rows = []
    for name, pred in preds.items():
        rows.append({
            "model": name,
            "MAE": mean_absolute_error(test["units_sold"], pred),
            "RMSE": mean_squared_error(test["units_sold"], pred) ** 0.5,
            "WAPE_percent": np.abs(test["units_sold"].to_numpy() - pred).sum()
                            / max(test["units_sold"].sum(), 1) * 100,
        })
    return pd.DataFrame(rows).sort_values("WAPE_percent"), train, test, preds


def future_forecast(df, horizon):
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        model = SARIMAX(
            df["units_sold"],
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 12),
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        fitted = model.fit(disp=False)
        result = fitted.get_forecast(steps=horizon)
        frame = result.summary_frame()
        return pd.DataFrame({
            "date": pd.date_range(df.index[-1] + pd.offsets.MonthBegin(1), periods=horizon, freq="MS"),
            "forecast_units": np.maximum(frame["mean"].to_numpy(), 0).round(0),
            "lower_95": np.maximum(frame["mean_ci_lower"].to_numpy(), 0).round(0),
            "upper_95": np.maximum(frame["mean_ci_upper"].to_numpy(), 0).round(0),
            "model": "SARIMA(1,1,1)(1,1,1,12)",
        })
    except Exception as exc:
        warnings.warn(f"SARIMA could not be fitted ({exc}); returning seasonal-naive forecast.")
        pred = forecast_seasonal_naive(df, horizon)
        dates = pd.date_range(df.index[-1] + pd.offsets.MonthBegin(1), periods=horizon, freq="MS")
        return pd.DataFrame({"date": dates, "forecast_units": pred.round(0),
                             "lower_95": np.nan, "upper_95": np.nan,
                             "model": "Seasonal naive fallback"})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--horizon", type=int, default=6)
    parser.add_argument("--holdout", type=int, default=12)
    args = parser.parse_args()
    OUTPUT.mkdir(exist_ok=True)
    df = load_data(args.input)
    metrics, train, test, preds = evaluate_holdout(df, min(args.holdout, max(3, len(df)//4)))
    metrics.to_csv(OUTPUT / "model_comparison.csv", index=False)
    forecast = future_forecast(df, args.horizon)
    forecast.to_csv(OUTPUT / "future_forecast.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["units_sold"], label="Historical units", linewidth=1.8)
    plt.title("Monthly Apparel Demand: Historical Trend")
    plt.xlabel("Month"); plt.ylabel("Units sold"); plt.grid(alpha=.25); plt.legend()
    plt.tight_layout(); plt.savefig(OUTPUT / "historical_trend.png", dpi=160); plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["units_sold"], label="Historical units")
    plt.plot(pd.to_datetime(forecast["date"]), forecast["forecast_units"], marker="o", label="Forecast")
    if forecast["lower_95"].notna().any():
        plt.fill_between(pd.to_datetime(forecast["date"]), forecast["lower_95"],
                         forecast["upper_95"], alpha=.18, label="95% interval")
    plt.title("Apparel Demand Forecast")
    plt.xlabel("Month"); plt.ylabel("Units sold"); plt.grid(alpha=.25); plt.legend()
    plt.tight_layout(); plt.savefig(OUTPUT / "forecast.png", dpi=160); plt.close()

    print("\nModel comparison (lower is better):")
    print(metrics.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    print("\nForecast:")
    print(forecast.to_string(index=False))
    print(f"\nOutputs saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
