import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame({
    "name":  ["Suraj", "Ankit", "Arun", "Pritesh", "Sanjay", "Raju",
              "Dylon", "Nirav", "Anil", "Kiran", "Nitin", "Sunil", "Sri"],
    "level": [735, 742, 726, 720, 723, 734, 730, 748, 726, 716, 730, 745, 738],
})

# Group names by level
groups = df.groupby("level")["name"].apply(", ".join).reset_index()
groups["label"] = groups["name"].apply(lambda x: f"[{x}]" if "," in x else x)

fig, ax = plt.subplots(figsize=(4, 8))

ax.set_title("SP500 predictions for\n2026-05-11 through 2026-05-15", fontsize=10, color="gray", pad=12)

for _, row in groups.iterrows():
    color = "#185FA5" if row.level == groups.level.max() else "#378ADD"
    ax.scatter(0, row.level, color=color, s=60, zorder=3)
    ax.annotate(row.label, xy=(0, row.level), xytext=(0.12, row.level),
                fontsize=9, va="center", color=color,
                arrowprops=dict(arrowstyle="-", color=color, lw=0.8))

ax.axvline(0, color="#378ADD", lw=2)
ax.set_ylabel("Level", color="gray")
ax.text(1.18, 0.5, "Name", transform=ax.transAxes, color="gray",
        va="center", ha="center", rotation=-90)
ax.set_xlim(-0.3, 1.2)
ax.set_ylim(713, 751)

# Ticks: min, max, and every multiple of 5 in between
min_l, max_l = groups["level"].min(), groups["level"].max()
regular = list(range(int(np.ceil(min_l / 5) * 5), int(np.floor(max_l / 5) * 5) + 1, 5))
ticks = sorted(set([min_l, max_l] + regular))

ax.set_yticks(ticks)
ax.tick_params(axis="y", left=True, right=False, length=5, direction="out", color="gray", labelcolor="gray", pad=4)
ax.tick_params(axis="x", bottom=False, labelbottom=False)

# Draw tick marks manually on the left of x=0
tick_len = 0.03  # in data coords
for t in ticks:
    ax.plot([-tick_len, 0], [t, t], color="gray", lw=0.8, clip_on=False)

# Draw name ticks on the right of x=0 — same length
for _, row in groups.iterrows():
    ax.plot([0, tick_len], [row.level, row.level], color="gray", lw=0.8, clip_on=False)

for spine in ax.spines.values():
    spine.set_visible(False)

# Draw the axis line manually
ax.axvline(0, color="#378ADD", lw=2, zorder=2)

plt.tight_layout()
# plt.savefig("/mnt/user-data/outputs/dot_plot.png", dpi=150, bbox_inches="tight")
plt.savefig("dot_plot.png", dpi=150, bbox_inches="tight")
