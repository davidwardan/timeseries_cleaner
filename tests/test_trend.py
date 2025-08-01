import pytest
import pandas as pd
from timeseries_cleaner.preprocessing import ProphetTrendRemover


@pytest.mark.skip("Prophet is heavy; run locally if installed")
def test_prophet_trend_removal():
    # synthetic linear trend
    idx = pd.date_range("2025-01-01", periods=100, freq="D")
    ser = pd.Series(0.5 * range(100), index=idx)
    detrended = ProphetTrendRemover().fit_transform(ser)
    assert abs(detrended.mean()) < 1e-1