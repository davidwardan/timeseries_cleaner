# timeseries_cleaner/plot_config.py
import matplotlib.pyplot as plt


def set_plot_style(style: str = "default", context: str = "notebook"):
    """
    Set consistent matplotlib style across all plots.

    Parameters
    ----------
    style : str
        Matplotlib style to use (e.g., 'default', 'ggplot', 'seaborn-v0_8').
    context : str
        Context for figure sizing and font (e.g., 'notebook', 'paper').
    """
    # Apply style
    try:
        plt.style.use(style)
    except OSError:
        print(f"Style '{style}' not found. Using default.")

    # Common global settings
    plt.rcParams.update(
        {
            "figure.figsize": (10, 4),
            "axes.grid": True,
            "axes.titlesize": "medium",
            "axes.labelsize": "small",
            "legend.fontsize": "small",
            "xtick.labelsize": "x-small",
            "ytick.labelsize": "x-small",
            "figure.autolayout": True,
        }
    )

    if context == "paper":
        plt.rcParams.update(
            {
                "font.size": 8,
                "figure.dpi": 150,
            }
        )
    elif context == "notebook":
        plt.rcParams.update(
            {
                "font.size": 10,
                "figure.dpi": 100,
            }
        )
