"""Minimal pipeline to chain preprocessing steps (sklearn‑style)."""

from typing import List, Tuple, Any


class Pipeline:  # noqa: D101
    def __init__(self, steps: List[Tuple[str, Any]]):
        self.steps = steps

    # -------------------------------------------------------
    # Fit / Transform logic
    # -------------------------------------------------------
    def fit(self, data, **fit_params):
        x = data
        for _, step in self.steps:
            if hasattr(step, "fit"):
                step.fit(x, **fit_params)
            if hasattr(step, "transform"):
                x = step.transform(x)
        self._X = x  # noqa: WPS437 (internal cache)
        return self

    def transform(self, data):
        x = data
        for _, step in self.steps:
            if hasattr(step, "transform"):
                x = step.transform(x)
        return x

    def fit_transform(self, data, **fit_params):
        return self.fit(data, **fit_params)._X
