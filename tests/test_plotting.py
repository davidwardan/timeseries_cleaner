import matplotlib
matplotlib.use("Agg")  # headless backend for CI

import pandas as pd
from timeseries_cleaner import Plotter, OutlierRemover


def test_compare_series_runs():
    idx = pd.date_range("2025-01-01", periods=50, freq="H")
    ser = pd.Series(range(50), index=idx)
    ser.iloc[10] = 999
    cleaned = OutlierRemover().fit_transform(ser)
    ax = Plotter.compare_series(ser, cleaned, show=False)
    assert ax is not None