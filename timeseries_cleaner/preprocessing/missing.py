"""Missing‑value imputation transformer."""
from __future__ import annotations

import pandas as pd

from ..utils import logger


class MissingValueImputer:  # noqa: D101
    def __init__(self, method: str = "ffill"):
        """Impute missing values using pandas built‑ins.

        * ffill / bfill – forward / backward fill
        * mean       – fill with series mean
        * median     – fill with series median
        * zero       – fill with 0
        * drop       – remove NA rows (mind time alignment)
        """
        self.method = method

    def fit(self, data):  # noqa: D401 (no learning needed)
        return self

    def transform(self, data):
        if not isinstance(data, (pd.Series, pd.DataFrame)):
            raise TypeError("Input must be pandas Series or DataFrame.")

        logger.debug("Imputing missing values using '%s'", self.method)

        if self.method in {"ffill", "bfill"}:
            return data.fillna(method=self.method)
        if self.method == "mean":
            return data.fillna(data.mean())
        if self.method == "median":
            return data.fillna(data.median())
        if self.method == "zero":
            return data.fillna(0)
        if self.method == "drop":
            return data.dropna()
        raise ValueError(f"Unknown imputation method '{self.method}'")

    def fit_transform(self, data):
        return self.fit(data).transform(data)