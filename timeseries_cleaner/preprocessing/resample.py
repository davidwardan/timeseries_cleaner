"""Time‑series resampling transformer."""

from __future__ import annotations

import pandas as pd

from ..utils import logger


class Resampler:  # noqa: D101
    def __init__(
        self, rule: str = "D", method: str = "mean", interpolate: bool = False
    ):
        """Resample a Series/DataFrame.

        Parameters
        ----------
        rule : str
            Pandas offset alias (e.g. "D", "H", "15T").
        method : str
            Aggregation method for downsampling ("mean", "sum", "median", etc.) or
            interpolation method for upsampling ("linear", "nearest", ...).
        interpolate : bool
            Whether to interpolate after resampling (useful for upsampling).
        """
        self.rule = rule
        self.method = method
        self.interpolate = interpolate

    # ------------------------------------------------------------------
    def fit(self, data):  # noqa: D401 (no-op)
        return self

    def transform(self, data):
        if not isinstance(data, (pd.Series, pd.DataFrame)):
            raise TypeError("Input must be pandas Series or DataFrame.")

        logger.debug("Resampling to '%s' using method '%s'", self.rule, self.method)
        upsample = data.index.inferred_freq is not None and pd.tseries.frequencies.to_offset(self.rule) < pd.tseries.frequencies.to_offset(data.index.inferred_freq)  # type: ignore[arg-type]

        if upsample:
            resampled = data.resample(self.rule).asfreq()
            if self.interpolate:
                resampled = resampled.interpolate(method=self.method)
        else:
            resampled = getattr(data.resample(self.rule), self.method)()
        return resampled

    def fit_transform(self, data):
        return self.fit(data).transform(data)
