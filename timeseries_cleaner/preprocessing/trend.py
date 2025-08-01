"""Trend removal using Facebook Prophet."""
from __future__ import annotations

import warnings
from typing import Optional

import pandas as pd

from ..utils import logger

try:
    from prophet import Prophet  # fbprophet renamed to prophet
except ModuleNotFoundError as exc:  # pragma: no cover
    raise ModuleNotFoundError("`prophet` is required for ProphetTrendRemover. Run `pip install prophet`." ) from exc


class ProphetTrendRemover:  # noqa: D101
    def __init__(self, growth: str = "linear", seasonality_mode: str = "additive", daily: bool = False, weekly: bool = True, yearly: bool = True):
        self.growth = growth
        self.seasonality_mode = seasonality_mode
        self.daily = daily
        self.weekly = weekly
        self.yearly = yearly
        self._model: Optional[Prophet] = None

    # ------------------------------------------------------------------
    def fit(self, series: pd.Series):  # noqa: D401
        if not isinstance(series, pd.Series):
            raise TypeError("Input must be a pandas Series.")
        df = series.reset_index()
        df.columns = ["ds", "y"]
        with warnings.catch_warnings():  # supress Stan warnings
            warnings.simplefilter("ignore")
            self._model = Prophet(growth=self.growth, seasonality_mode=self.seasonality_mode)
            if self.daily:
                self._model.add_seasonality(name="daily", period=1, fourier_order=5)
            if self.weekly:
                self._model.add_seasonality(name="weekly", period=7, fourier_order=3)
            if self.yearly:
                self._model.add_seasonality(name="yearly", period=365.25, fourier_order=10)
            self._model.fit(df)
        logger.info("Prophet model fitted for trend extraction (%s points)", len(series))
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        if self._model is None:
            raise RuntimeError("Call `fit` before `transform`.")
        df = series.reset_index()
        df.columns = ["ds", "y"]
        forecast = self._model.predict(df[["ds"]])
        trend = forecast["trend"].values
        detrended = series - trend
        return pd.Series(detrended, index=series.index, name=series.name)

    def fit_transform(self, series: pd.Series) -> pd.Series:
        return self.fit(series).transform(series)