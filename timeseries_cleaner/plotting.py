"""Plotting helpers for before/after diagnostics."""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


class Plotter:
    # ------------------------------------------------------------------
    @staticmethod
    def compare_series(
        original: pd.Series,
        transformed: pd.Series,
        *,
        title: Optional[str] = None,
        legend: tuple[str, str] = ("Original", "Transformed"),
        show: bool = True,
        ax: Optional[plt.Axes] = None,
    ) -> plt.Axes:
        """Line‑plot original vs transformed series on the same axes."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(original.index, original.values, label=legend[0], alpha=0.6)
        ax.plot(transformed.index, transformed.values, label=legend[1], alpha=0.8)
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()
        if title:
            ax.set_title(title)
        if show:
            plt.show()
        return ax

    # ------------------------------------------------------------------
    @staticmethod
    def highlight_outliers(
        original: pd.Series,
        cleaned: pd.Series,
        *,
        title: str = "Outlier Removal",
        show: bool = True,
        ax: Optional[plt.Axes] = None,
    ) -> plt.Axes:
        """Scatter removed outliers on top of cleaned series."""
        outlier_mask = ~original.index.isin(cleaned.index)
        outliers = original[outlier_mask]
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(original.index, original.values, label="Original", alpha=0.4)
        ax.scatter(
            outliers.index, outliers.values, color="red", label="Outliers", zorder=5
        )
        ax.plot(cleaned.index, cleaned.values, label="Cleaned", alpha=0.9)
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()
        if show:
            plt.show()
        return ax
