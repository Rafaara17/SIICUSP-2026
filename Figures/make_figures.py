# -*- coding: utf-8 -*-
"""
Builds the four result figures of the SIICUSP 2026 abstract from the RouTrip
benchmark data.

The aggregated numbers below are copied verbatim from ``anim_tsp.py`` (dicts
GAP, TIME and WIN), which in turn were extracted from
"Comparacao New-Algo TSPs.xlsx".  They are duplicated here instead of imported
because ``anim_tsp`` requires ManimCE, which is not needed to draw the figures.

Run:  python3 "Figures/make_figures.py"
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- data
ALGOS = ["LKH3", "HGS", "ILS", "ALNS", "GNN"]   # plot / legend order
SIZES = ["TSP5", "TSP10", "TSP20", "TSP50", "TSP100"]
CITIES = [5, 10, 20, 50, 100]

GAP = {  # mean optimality gap (%) by size
    "LKH3": [0.0, 0.0, 0.0, 0.006, 0.0],
    "ILS":  [0.0, 0.0, 0.0, 0.029, 0.258],
    "ALNS": [0.0, 0.887, 1.996, 3.911, 4.251],
    "HGS":  [0.0, 0.0, 0.0, 0.0, 0.0],
    "GNN":  [0.0, 0.0, 0.0, 0.051, 1.336],
}
TIME = {  # mean time (s) by size
    "LKH3": [0.061, 0.062, 0.073, 0.102, 0.135],
    "ILS":  [0.071, 0.091, 0.553, 3.417, 8.124],
    "ALNS": [0.323, 0.338, 1.242, 5.034, 27.945],
    "HGS":  [0.067, 0.073, 0.346, 1.940, 7.432],
    "GNN":  [0.837, 1.011, 2.027, 5.276, 12.030],
}
WIN = {"LKH3": 99, "HGS": 100, "ILS": 89, "ALNS": 49, "GNN": 79}

# Print-safe re-stepping of the palette used in anim_tsp.py: same five hue
# families, darkened so every series clears 3:1 contrast on white paper.
# Validated (adjacent pairs, light surface): worst CVD dE 9.4, worst
# normal-vision dE 18.1, all contrasts >= 3:1.  Under all-pairs the gold/red
# CVD pair sits at 6.3, which is why every series also carries a distinct
# marker shape and the scatter panel is directly labelled.
COLORS = {"LKH3": "#2F6BB5", "HGS": "#A87C00", "ILS": "#0F7A5A",
          "ALNS": "#8B5CF0", "GNN": "#C43B33"}
MARKERS = {"LKH3": "o", "HGS": "s", "ILS": "^", "ALNS": "D", "GNN": "v"}

INK = "#1a1a1a"        # primary text
INK_SOFT = "#555555"   # secondary text / axis labels
GRID = "#d9d9d9"

# Each figure is a single-column float in a twocolumn a4 layout with 2.6 cm
# side margins and 0.8 cm gutter, so \columnwidth is exactly 7.5 cm.  Drawing
# at that width and including at \columnwidth keeps the scale at 1:1, which is
# what holds the tick labels at their true 7.5 pt on paper.
FIG_W = 7.5 / 2.54

HERE = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7,
    "axes.edgecolor": "#8a8a8a",
    "axes.linewidth": 0.8,
    "text.color": INK,
    "axes.labelcolor": INK_SOFT,
    "xtick.color": INK_SOFT,
    "ytick.color": INK_SOFT,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def style_axes(ax, yaxis_grid=True):
    """Recessive frame: no top/right spines, soft horizontal grid only."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if yaxis_grid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
    ax.tick_params(length=3, width=0.8)


def size_axis(ax):
    """Shared x axis of the two by-instance-size figures."""
    x = list(range(len(SIZES)))
    ax.set_xticks(x)
    ax.set_xticklabels([str(c) for c in CITIES])
    ax.set_xlim(-0.15, len(SIZES) - 0.85)
    ax.set_xlabel("Instance size (cities)")


def series_legend(ax):
    """
    Legend sits inside the axes, upper left.  In both series figures every
    curve climbs to the right, so that corner is empty; keeping the legend
    there instead of under the axes buys ~1 cm of height, which is what lets
    the float land next to the sentence that cites it.
    """
    ax.legend(loc="upper left", ncol=2, frameon=False, fontsize=6.5,
              handlelength=1.2, columnspacing=0.9, handletextpad=0.35,
              borderpad=0.1, labelspacing=0.3, labelcolor=INK)


# ---------------------------------------------------------------- figure 1
def figure_gap(path):
    # Figures 1 and 2 have to share one column, and LaTeX weighs the height of
    # an already-placed float against the next one twice, so this height is
    # what keeps the pair together instead of spilling figure 2 onto page 2.
    fig, ax = plt.subplots(figsize=(FIG_W, 1.20))
    x = list(range(len(SIZES)))

    for a in ALGOS:
        ax.plot(x, GAP[a], color=COLORS[a], marker=MARKERS[a], markersize=4.0,
                linewidth=1.5, markeredgecolor="white", markeredgewidth=0.7,
                label=a, clip_on=False)
    # Figures 1 and 2 are short enough that a rotated label past ~12 characters
    # runs off the axes, so the qualifiers live in the caption instead.
    ax.set_ylabel("Gap (%)")
    ax.set_ylim(-0.15, 5.9)  # headroom for the legend over the ALNS curve
    ax.set_yticks([0, 1, 2, 3, 4])
    size_axis(ax)
    style_axes(ax)
    series_legend(ax)

    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- figure 2
def figure_time(path):
    fig, ax = plt.subplots(figsize=(FIG_W, 1.20))  # see figure_gap
    x = list(range(len(SIZES)))

    for a in ALGOS:
        ax.plot(x, TIME[a], color=COLORS[a], marker=MARKERS[a], markersize=4.0,
                linewidth=1.5, markeredgecolor="white", markeredgewidth=0.7,
                label=a, clip_on=False)
    ax.set_yscale("log")
    ax.set_ylabel("Runtime (s)")  # see figure_gap
    ax.set_ylim(0.045, 300)  # headroom for the legend over the ALNS curve
    ax.set_yticks([0.1, 1, 10])
    ax.set_yticklabels(["0.1", "1", "10"])
    ax.minorticks_off()
    size_axis(ax)
    style_axes(ax)
    series_legend(ax)

    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- figure 3
def figure_tradeoff(path):
    fig, ax = plt.subplots(figsize=(FIG_W, 1.55))

    xs = {a: TIME[a][-1] for a in ALGOS}
    ys = {a: GAP[a][-1] for a in ALGOS}

    # Non-dominated set (minimise both runtime and gap).
    pareto = [a for a in ALGOS
              if not any(xs[b] <= xs[a] and ys[b] <= ys[a] and
                         (xs[b] < xs[a] or ys[b] < ys[a]) for b in ALGOS)]

    label_offset = {"LKH3": (12, 8), "HGS": (-28, -2), "ILS": (6, 5),
                    "ALNS": (-9, 9), "GNN": (7, 5)}
    for a in ALGOS:
        ax.scatter(xs[a], ys[a], s=55, color=COLORS[a], marker=MARKERS[a],
                   edgecolor="white", linewidth=0.8, zorder=3)
        ax.annotate(a, (xs[a], ys[a]), textcoords="offset points",
                    xytext=label_offset[a], fontsize=7.5, color=INK)

    for a in pareto:  # non-dominated marker gets a visible ring
        ax.scatter(xs[a], ys[a], s=190, facecolor="none",
                   edgecolor=COLORS[a], linewidth=1.0, zorder=2)
        ax.annotate("best trade-off", (xs[a], ys[a]),
                    textcoords="offset points", xytext=(12, -7),
                    fontsize=7, color=INK_SOFT, style="italic")

    ax.set_xscale("log")
    ax.set_xlabel("Mean runtime (s, log scale)")
    ax.set_ylabel("Mean optimality gap (%)")
    ax.set_xlim(0.08, 60)
    ax.set_ylim(-0.35, 5.0)
    ax.set_xticks([0.1, 1, 10])
    ax.set_xticklabels(["0.1", "1", "10"])
    ax.minorticks_off()
    style_axes(ax)

    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("wrote", path)
    print("non-dominated at TSP100:", pareto)


# ---------------------------------------------------------------- figure 4
def figure_winrate(path):
    fig, ax = plt.subplots(figsize=(FIG_W, 1.35))

    order = sorted(ALGOS, key=lambda a: WIN[a])
    ypos = list(range(len(order)))
    for y, a in zip(ypos, order):
        ax.barh(y, WIN[a], height=0.55, color=COLORS[a], zorder=2)
        ax.text(WIN[a] + 2.5, y, f"{WIN[a]}%", va="center", fontsize=7.5,
                color=INK_SOFT)

    ax.set_yticks(ypos)
    ax.set_yticklabels(order, color=INK)
    ax.set_xlabel("Runs reaching the best known solution (%)")
    ax.set_xlim(0, 118)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=3, width=0.8)

    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    figure_gap(os.path.join(HERE, "fig1_gap.png"))
    figure_time(os.path.join(HERE, "fig2_time.png"))
    figure_tradeoff(os.path.join(HERE, "fig3_tradeoff.png"))
    figure_winrate(os.path.join(HERE, "fig4_winrate.png"))
