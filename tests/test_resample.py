import pandas as pd
from timeseries_cleaner.preprocessing import Resampler


def test_resampler_mean_downsample():
    rng = pd.date_range("2025-01-01", periods=24, freq="H")
    ser = pd.Series(range(24), index=rng)
    res = Resampler(rule="D", method="mean").fit_transform(ser)
    assert len(res) == 1  # one day
    assert res.iloc[0] == ser.mean()