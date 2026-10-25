"""Shared matplotlib style, palette and pitch drawing for the notebooks."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Arc, Rectangle

from epl_xt import config
from epl_xt.pitch import PITCH_LENGTH, PITCH_WIDTH

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
MUTED = "#b5b4ad"

# Categorical slots in fixed order. Scatter plots use at most the first three.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
POSITION_COLORS = {"DEF": SERIES[0], "MID": SERIES[1], "FWD": SERIES[2]}

SEQUENTIAL = LinearSegmentedColormap.from_list(
    "seq_blue", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"]
)
DIVERGING = LinearSegmentedColormap.from_list(
    "div_blue_red", ["#184f95", "#6da7ec", "#f0efec", "#ec8a89", "#b52a2a"]
)


TEAM_SHORT_NAMES = {
    "AFC Bournemouth": "Bournemouth",
    "Leicester City": "Leicester",
    "Manchester City": "Man City",
    "Manchester United": "Man Utd",
    "Newcastle United": "Newcastle",
    "Norwich City": "Norwich",
    "Stoke City": "Stoke",
    "Swansea City": "Swansea",
    "Tottenham Hotspur": "Spurs",
    "West Bromwich Albion": "West Brom",
    "West Ham United": "West Ham",
}


def short_team(name: str) -> str:
    return TEAM_SHORT_NAMES.get(name, name)


def label_points(ax: plt.Axes, xs, ys, labels, offsets: dict | None = None, fontsize: float = 8) -> None:
    """Direct-label points, nudging named labels by (dx, dy) points to avoid collisions."""
    offsets = offsets or {}
    for x, y, text in zip(xs, ys, labels, strict=True):
        dx, dy = offsets.get(text, (5, 3))
        ax.annotate(
            text,
            (x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=fontsize,
            color=TEXT_SECONDARY,
            ha="right" if dx < 0 else "left",
        )


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "semibold",
            "axes.titlelocation": "left",
            "axes.labelcolor": TEXT_SECONDARY,
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.7,
            "xtick.color": TEXT_SECONDARY,
            "ytick.color": TEXT_SECONDARY,
            "text.color": TEXT,
            "lines.linewidth": 2,
            "lines.markersize": 7,
            "legend.frameon": False,
            "axes.prop_cycle": mpl.cycler(color=SERIES),
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    """Save a figure to reports/figures/<name>.png."""
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(config.FIGURES_DIR / f"{name}.png")


def draw_pitch(ax: plt.Axes, color: str = MUTED, lw: float = 1.0) -> plt.Axes:
    """Draw StatsBomb's 120 x 80 pitch with y increasing downwards (as in the data)."""
    kw = {"fill": False, "edgecolor": color, "linewidth": lw, "zorder": 3}
    ax.add_patch(Rectangle((0, 0), PITCH_LENGTH, PITCH_WIDTH, **kw))
    ax.plot([60, 60], [0, 80], color=color, lw=lw, zorder=3)
    for x0, sign in [(0, 1), (PITCH_LENGTH, -1)]:
        ax.add_patch(Rectangle((x0, 18), sign * 18, 44, **kw))
        ax.add_patch(Rectangle((x0, 30), sign * 6, 20, **kw))
        ax.add_patch(Rectangle((x0, 36), -sign * 2, 8, **kw))  # goal
    ax.add_patch(Arc((60, 40), 20, 20, edgecolor=color, lw=lw, zorder=3))
    ax.add_patch(Arc((12, 40), 20, 20, theta1=-53, theta2=53, edgecolor=color, lw=lw, zorder=3))
    ax.add_patch(Arc((108, 40), 20, 20, theta1=127, theta2=233, edgecolor=color, lw=lw, zorder=3))
    ax.set_xlim(-3, PITCH_LENGTH + 3)
    ax.set_ylim(PITCH_WIDTH + 3, -3)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


def pitch_heatmap(
    ax: plt.Axes, grid, cmap=SEQUENTIAL, vmin=None, vmax=None, annotate: bool = False, fmt="{:.2f}"
):
    """Draw a (ny, nx) grid of zone values over the pitch. Returns the image for a colorbar."""
    im = ax.imshow(
        grid,
        extent=(0, PITCH_LENGTH, PITCH_WIDTH, 0),
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest",
        zorder=1,
    )
    draw_pitch(ax)
    if annotate:
        ny, nx = grid.shape
        top = grid.max() if vmax is None else vmax
        for r in range(ny):
            for c in range(nx):
                v = grid[r, c]
                ax.text(
                    (c + 0.5) * PITCH_LENGTH / nx,
                    (r + 0.5) * PITCH_WIDTH / ny,
                    fmt.format(v),
                    ha="center",
                    va="center",
                    fontsize=6,
                    color="white" if v > 0.45 * top else TEXT_SECONDARY,
                    zorder=4,
                )
    return im
