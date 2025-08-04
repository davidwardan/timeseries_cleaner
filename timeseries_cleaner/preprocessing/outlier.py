"""Outlier detection & removal transformer."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..utils import logger


class OutlierRemover:
    def __init__(
        self, method: str = "zscore", threshold: float = 3.0, window: int = 10
    ):
        self.method = method
        self.threshold = float(threshold)
        self.window = int(window)
        self.series_name: str | None = None

    # Public API
    def fit(self, series: pd.Series):
        """No‑op fit, kept for compatibility & metadata."""
        if not isinstance(series, pd.Series):
            raise TypeError("Input must be a pandas Series.")
        self.series_name = series.name
        logger.debug("Fitting OutlierRemover on %d observations", len(series))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        if not isinstance(series, pd.Series):
            raise TypeError("Input must be a pandas Series.")
        if self.method == "zscore":
            return self._zscore(series)
        if self.method == "iqr":
            return self._iqr(series)
        if self.method == "rolling_mad":
            return self._rolling_mad(series)
        raise ValueError(f"Unsupported method '{self.method}'")

    def fit_transform(self, series: pd.Series) -> pd.Series:
        return self.fit(series).transform(series)

    # Internal helpers
    def _zscore(self, series: pd.Series):
        z = (series - series.mean()) / series.std(ddof=0)
        cleaned = series[np.abs(z) < self.threshold]
        logger.debug("Z‑score removed %d outliers", len(series) - len(cleaned))
        return cleaned

    def _iqr(self, series: pd.Series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - self.threshold * iqr
        upper = q3 + self.threshold * iqr
        cleaned = series[(series >= lower) & (series <= upper)]
        logger.debug("IQR removed %d outliers", len(series) - len(cleaned))
        return cleaned

    def _rolling_mad(self, series: pd.Series):
        rolling_median = series.rolling(
            self.window, center=True, min_periods=1
        ).median()
        mad = lambda x: np.median(np.abs(x - np.median(x)))
        rolling_mad = series.rolling(self.window, center=True, min_periods=1).apply(
            mad, raw=True
        )
        diff = np.abs(series - rolling_median)
        cleaned = series[diff < self.threshold * rolling_mad]
        logger.debug("Rolling MAD removed %d outliers", len(series) - len(cleaned))
        return cleaned
