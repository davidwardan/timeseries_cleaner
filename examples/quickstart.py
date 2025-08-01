"""Quick‑start demo for timeseries_cleaner.

Run:
    python examples/quickstart.py

This script generates synthetic data, applies a preprocessing pipeline,
plots before/after results, and saves the figure to disk.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from timeseries_cleaner import (
    OutlierRemover,
    Resampler,
    MissingValueImputer,
    ProphetTrendRemover,
    Plotter,
    Pipeline,
)

# Synthetic hourly data with trend, missing values, and outliers
np.random.seed(42)
idx = pd.date_range("2025-01-01", periods=240, freq="H")
trend = 0.05 * np.arange(240)
seasonal = 5 * np.sin(2 * np.pi * idx.hour / 24)
noise = np.random.normal(0, 0.5, size=240)
series = pd.Series(trend + seasonal + noise, index=idx)

# Add missing block and outliers
series.iloc[50:60] = np.nan
series.iloc[[30, 180]] += 15

# Preprocessing pipeline
pipe = Pipeline([
    ("impute", MissingValueImputer("ffill")),
    ("outliers", OutlierRemover(method="iqr", threshold=1.5)),
    ("resample", Resampler(rule="D", method="mean")),
    ("detrend", ProphetTrendRemover()),  # optional heavy step
])

cleaned = pipe.fit_transform(series)

# Plot diagnostics
Plotter.highlight_outliers(series, pipe.steps[1][1].transform(series), title="Outlier Detection (IQR)")
Plotter.compare_series(series, cleaned, title="Before vs After Pipeline")

# Save last figure
plt.savefig("examples/quickstart_output.png", dpi=150)
print("Preprocessing complete – figures saved as examples/quickstart_output.png")