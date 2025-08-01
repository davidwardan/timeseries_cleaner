# timeseries_cleaner

*A lightweight, modular toolkit for common time-series preprocessing tasks.*

![CI](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
![PyPI](https://img.shields.io/badge/pypi-coming_soon-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

---

## ✨ Features

| Task                        | Transformer                 | Status |
| --------------------------- | --------------------------- | :----: |
| Outlier detection/removal   | `OutlierRemover`            | ✅     |
| Resampling / aggregation    | `Resampler`                 | ✅     |
| Trend removal (Prophet)     | `ProphetTrendRemover`       | ✅     |
| Missing-value imputation    | `MissingValueImputer`       | ✅     |
| Chaining multiple steps     | `Pipeline` (sklearn-style)  | ✅     |
| Forthcoming                 | STL detrending, scaling, CLI | ⏳     |

All transformers follow a **`fit / transform / fit_transform`** API so they can be chained or used standalone.

---

## 🔧 Installation

> **Requires Python ≥ 3.8**

```bash
# From source (development mode)
git clone https://github.com/yourname/timeseries_cleaner.git
cd timeseries_cleaner
pip install -e .

# Or, when released on PyPI
pip install timeseries-cleaner