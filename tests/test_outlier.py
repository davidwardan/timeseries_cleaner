import pandas as pd
from timeseries_cleaner.preprocessing import OutlierRemover


def test_zscore_outlier_removal():
    series = pd.Series([10] * 10 + [200])
    remover = OutlierRemover(method="zscore", threshold=2)
    cleaned = remover.fit_transform(series)
    assert 200 not in cleaned.values
    assert len(cleaned) == 10