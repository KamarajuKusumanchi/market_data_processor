#!/usr/bin/env python3

# changelog:
# * 2026-05-11 initial version is from @claude.
# * 2026-05-16 enhancements: added market df, bull/bear coloring, winner highlight.
# * 2026-05-16 enhancements: market reference lines (previous_week_close, current_week_min/max).
# * 2026-05-16 refactor: modularized into focused functions.

# tags | weekly contest

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

market = pd.DataFrame({
    "name":  ["previous_week_close", "current_week_min", "current_week_max"],
    "level": [737.62,                 731.83,             749.53],
})

predictions = pd.DataFrame({
    "name":  ["Suraj", "Ankit", "Arun", "Pritesh", "Sanjay", "Raju",
              "Dylon", "Nirav", "Anil", "Kiran", "Nitin", "Sunil", "Sri [X]"],
    "level": [735,     742,     726,    720,      723,     734,
              730,     748,     726,    716,      730,     745,    738],
})

winner = "Nirav"
title  = "SP500 predictions for\n2026-05-11 through 2026-05-15"

# Market reference lines: key → (color, display label)
MARKET_STYLES = {
    "previous_week_close": ("black",     "prev close"),
    "current_week_min":    ("darkgoldenrod", "week min"),
    "current_week_max":    ("darkgoldenrod", "week max"),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def market_level(name):
    return market.loc[market["name"] == name, "level"].values[0]

def prediction_color(names, level, winner, bull_threshold):
    """Return dot color: purple for winner, green for bull, red for bear."""
    if winner in names:
        return "purple"
    return "green" if level >= bull_threshold else "red"

def build_groups(predictions, winner, bull_threshold):
    """Group predictions sharing the same level; attach label and color."""
    groups = predictions.groupby("level")["name"].apply(", ".join).reset_index()
    groups["label"] = groups["name"].apply(lambda x: f"[{x}]" if "," in x else x)
    groups["color"] = groups.apply(
        lambda r: prediction_color(r["name"].split(", "), r["level"], winner, bull_threshold),
        axis=1,
    )
    return groups

def yticks(levels):
    """Min, max, and every multiple-of-5 in between."""
    lo, hi = int(levels.min()), int(levels.max())
    mid = list(range(int(np.ceil(lo / 5) * 5), int(np.floor(hi / 5) * 5) + 1, 5))
    return sorted(set([lo, hi] + mid))

# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

TICK_LEN  = 0.03   # half-tick length in data x-coords
LINE_HALF = 0.18   # half-width of market reference lines

def draw_predictions(ax, groups):
    for _, row in groups.iterrows():
        ax.scatter(0, row.level, color=row.color, s=60, zorder=3)
        ax.annotate(row.label, xy=(0, row.level), xytext=(0.12, row.level),
                    fontsize=9, va="center", color=row.color,
                    arrowprops=dict(arrowstyle="-", color=row.color, lw=0.8))

def draw_ticks(ax, level_ticks, name_levels):
    for t in level_ticks:
        ax.plot([-TICK_LEN, 0], [t, t], color="gray", lw=0.8, clip_on=False)
    for lvl in name_levels:
        ax.plot([0, TICK_LEN], [lvl, lvl], color="gray", lw=0.8, clip_on=False)

def draw_market_lines(ax, market, styles):
    for name, (color, label) in styles.items():
        lvl = market_level(name)
        ax.plot([-LINE_HALF, LINE_HALF], [lvl, lvl],
                color=color, lw=1.0, linestyle="--", zorder=1)
        ax.annotate(f"{label} {lvl:.2f}", xy=(LINE_HALF, lvl),
                    xytext=(LINE_HALF + 0.02, lvl),
                    fontsize=9, va="center", ha="left", color=color)

def style_axes(ax, ticks, title):
    # x=0 sits at axes fraction x_lo / (x_hi - x_lo) = 0.3 / 1.5 = 0.2
    ax.text(0.2, 1.03, title,
            fontsize=10, color="gray", ha="center", va="bottom",
            transform=ax.transAxes)
    ax.set_ylabel("Level", color="gray")
    ax.text(1.18, 0.5, "Name", transform=ax.transAxes, color="gray",
            va="center", ha="center", rotation=-90)
    ax.set_xlim(-0.3, 1.2)
    ax.set_ylim(713, 751)
    ax.set_yticks(ticks)
    ax.tick_params(axis="y", left=True, right=False, length=5,
                   direction="out", color="gray", labelcolor="gray", pad=4)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axvline(0, color="#378ADD", lw=2, zorder=2)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    bull_threshold = market_level("previous_week_close")
    groups = build_groups(predictions, winner, bull_threshold)
    ticks  = yticks(groups["level"])

    fig, ax = plt.subplots(figsize=(4, 8))

    draw_predictions(ax, groups)
    draw_ticks(ax, ticks, groups["level"])
    draw_market_lines(ax, market, MARKET_STYLES)
    style_axes(ax, ticks, title)

    plt.tight_layout()
    # plt.savefig("/mnt/user-data/outputs/dot_plot.png", dpi=150, bbox_inches="tight")
    plt.savefig("dot_plot.png", dpi=150, bbox_inches="tight")

if __name__ == "__main__":
    main()