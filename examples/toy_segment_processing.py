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
trend = np.piecewise(
    np.arange(240),
    [np.arange(240) < 120, np.arange(240) >= 120],
    [lambda x: 0.05 * x, lambda x: 0.1 * x + 4],  # slower growth after midpoint
)
seasonal = 5 * np.sin(2 * np.pi * idx.hour / 24)
noise = np.random.normal(0, 0.5, size=240)
series = pd.Series(trend + seasonal + noise, index=idx)

# Add missing block and outliers
series.iloc[50:60] = np.nan
series.iloc[[30, 180]] += 15

# Preprocessing pipeline
pipe = Pipeline(
    [
        ("impute", MissingValueImputer("ffill")),
        ("outliers", OutlierRemover(method="iqr", threshold=1.5)),
        # ("resample", Resampler(rule="D", method="mean")),
        ("detrend", ProphetTrendRemover()),  # optional heavy step
    ]
)

# 1) Define the boundaries you want to slice on
#    (any ISO-format strings or pandas Timestamps work)
sections = [
    ("2025-01-01 00:00", "2025-01-05 23:00"),  # first 72 h
    ("2025-01-06 00:00", "2025-01-11 23:00"),  # next 72 h
]

# 2) Prepare a container and reuse the *same* pipeline for each
cleaned_segments = {}

for start, end in sections:
    sub_series = series.loc[start:end]

    # Fit *and* transform on each slice independently
    cleaned_segments[(start, end)] = pipe.fit_transform(sub_series)

    # Optional: quick diagnostic
    Plotter.compare_series(
        sub_series,
        cleaned_segments[(start, end)],
        title=f"{start} → {end}",
        show=False,  # avoid popping windows in loops
    )

# Plot diagnostics
from timeseries_cleaner.plot_config import set_plot_style

set_plot_style(style="seaborn-v0_8", context="paper")
cleaned_full = pd.concat(cleaned_segments.values()).sort_index()

# Plot the final concatenated result versus original
Plotter.compare_series(series, cleaned_full, title="Full Series (Segmented Cleaning)")
plt.show()
