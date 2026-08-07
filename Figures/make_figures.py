# -*- coding: utf-8 -*-
"""
Builds the two result figures of the SIICUSP 2026 abstract from the RouTrip
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

HERE = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 8,
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


def panel_tag(ax, text):
    ax.set_title(text, loc="left", color=INK, fontweight="bold", pad=6)


# ---------------------------------------------------------------- figure 1
def figure_gap_and_time(path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 1.85))
    x = list(range(len(SIZES)))

    for a in ALGOS:
        ax1.plot(x, GAP[a], color=COLORS[a], marker=MARKERS[a], markersize=4.5,
                 linewidth=1.7, markeredgecolor="white", markeredgewidth=0.7,
                 label=a, clip_on=False)
    panel_tag(ax1, "(a) Solution quality")
    ax1.set_ylabel("Mean optimality gap (%)")
    ax1.set_xlabel("Instance size (cities)")
    ax1.set_ylim(-0.15, 4.6)
    style_axes(ax1)

    for a in ALGOS:
        ax2.plot(x, TIME[a], color=COLORS[a], marker=MARKERS[a], markersize=4.5,
                 linewidth=1.7, markeredgecolor="white", markeredgewidth=0.7,
                 label=a, clip_on=False)
    panel_tag(ax2, "(b) Runtime")
    ax2.set_yscale("log")
    ax2.set_ylabel("Mean runtime (s, log scale)")
    ax2.set_xlabel("Instance size (cities)")
    ax2.set_yticks([0.1, 1, 10])
    ax2.set_yticklabels(["0.1", "1", "10"])
    ax2.minorticks_off()
    style_axes(ax2)

    for ax in (ax1, ax2):
        ax.set_xticks(x)
        ax.set_xticklabels([str(c) for c in CITIES])
        ax.set_xlim(-0.15, len(SIZES) - 0.85)

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, -0.02), handlelength=1.8,
               columnspacing=1.6, labelcolor=INK)

    fig.tight_layout(rect=(0, 0.09, 1, 1))
    fig.subplots_adjust(wspace=0.32)
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- figure 2
def figure_tradeoff_and_winrate(path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 1.85))

    # (a) quality x time on the largest instance
    xs = {a: TIME[a][-1] for a in ALGOS}
    ys = {a: GAP[a][-1] for a in ALGOS}

    # Non-dominated set (minimise both runtime and gap).
    pareto = [a for a in ALGOS
              if not any(xs[b] <= xs[a] and ys[b] <= ys[a] and
                         (xs[b] < xs[a] or ys[b] < ys[a]) for b in ALGOS)]

    label_offset = {"LKH3": (13, 7), "HGS": (-31, -3), "ILS": (7, 5),
                    "ALNS": (-8, 10), "GNN": (9, 5)}
    for a in ALGOS:
        ax1.scatter(xs[a], ys[a], s=55, color=COLORS[a], marker=MARKERS[a],
                    edgecolor="white", linewidth=0.8, zorder=3)
        ax1.annotate(a, (xs[a], ys[a]), textcoords="offset points",
                     xytext=label_offset[a], fontsize=7.5, color=INK)

    for a in pareto:  # non-dominated marker gets a visible ring
        ax1.scatter(xs[a], ys[a], s=190, facecolor="none",
                    edgecolor=COLORS[a], linewidth=1.0, zorder=2)
        ax1.annotate("best trade-off", (xs[a], ys[a]),
                     textcoords="offset points", xytext=(13, -6),
                     fontsize=7, color=INK_SOFT, style="italic")

    panel_tag(ax1, "(a) Quality vs. runtime on TSP100")
    ax1.set_xscale("log")
    ax1.set_xlabel("Mean runtime (s, log scale)")
    ax1.set_ylabel("Mean optimality gap (%)")
    ax1.set_xlim(0.08, 60)
    ax1.set_ylim(-0.35, 5.0)
    ax1.set_xticks([0.1, 1, 10])
    ax1.set_xticklabels(["0.1", "1", "10"])
    ax1.minorticks_off()
    style_axes(ax1)

    # (b) win rate
    order = sorted(ALGOS, key=lambda a: WIN[a])
    ypos = list(range(len(order)))
    for y, a in zip(ypos, order):
        ax2.barh(y, WIN[a], height=0.55, color=COLORS[a], zorder=2)
        ax2.text(WIN[a] + 2.5, y, f"{WIN[a]}%", va="center", fontsize=7.5,
                 color=INK_SOFT)

    panel_tag(ax2, "(b) Win rate")
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(order, color=INK)
    ax2.set_xlabel("Runs reaching the best known solution (%)")
    ax2.set_xlim(0, 118)
    ax2.set_xticks([0, 25, 50, 75, 100])
    ax2.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax2.yaxis.grid(False)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(length=3, width=0.8)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.30)
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print("wrote", path)
    print("non-dominated at TSP100:", pareto)


if __name__ == "__main__":
    figure_gap_and_time(os.path.join(HERE, "fig1_gap_time.png"))
    figure_tradeoff_and_winrate(os.path.join(HERE, "fig2_tradeoff_winrate.png"))
