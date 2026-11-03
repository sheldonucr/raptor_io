"""Regenerates Figure 6 of GS-WP-03 (end-to-end wall time) from Table 4.

The comparison tool is deliberately unnamed: see the note in the white paper.
Data: whitepapers/wp03-signoff-correlation.html, Table 4.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "figs", "signoff")

labels   = ["RISC_CORE\nstatic", "RISC_CORE\ndynamic", "LPU\nstatic", "LPU\ndynamic"]
ref_wall = [198.0, 447.0, 566.0, 876.0]      # commercial sign-off tool, end to end
gs_wall  = [8.6, 41.1, 20.8, 230.0]          # GridStack 1.5, end to end
speedup  = ["23.0×", "10.9×", "27.2×", "3.8×"]

TEXT  = "#172b32"
MUTED = "#52646b"
TEAL  = "#087964"
BLUE  = "#215fa4"
GRID  = (23/255, 43/255, 50/255, 0.12)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": TEXT, "axes.labelcolor": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": (23/255, 43/255, 50/255, 0.28),
})

fig, ax = plt.subplots(figsize=(10.0, 4.8), dpi=150)
fig.patch.set_alpha(0)
ax.set_facecolor("none")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.grid(axis="y", color=GRID, linewidth=1)
ax.set_axisbelow(True)

x = np.arange(len(labels))
w = 0.36
ax.bar(x - w/2, ref_wall, w, label="Commercial sign-off tool (in-design)",
       color=BLUE, edgecolor="none")
ax.bar(x + w/2, gs_wall, w, label="GridStack 1.5", color=TEAL, edgecolor="none")

for xi, (r, g, sp) in enumerate(zip(ref_wall, gs_wall, speedup)):
    ax.annotate(f"{r:g} s", (xi - w/2, r), textcoords="offset points", xytext=(0, 5),
                ha="center", fontsize=9, color=MUTED)
    ax.annotate(f"{g:g} s", (xi + w/2, g), textcoords="offset points", xytext=(0, 5),
                ha="center", fontsize=9, color=MUTED)
    ax.annotate(sp, (xi, max(r, g)), textcoords="offset points", xytext=(0, 26),
                ha="center", fontsize=13, color=TEAL, weight="bold")

ax.set_ylabel("Wall time, end to end (s)", fontsize=10.5)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylim(0, 1000)
leg = ax.legend(frameon=False, loc="upper left", fontsize=10.5)
for t in leg.get_texts():
    t.set_color(TEXT)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "walltime.png"), transparent=True)
print("wrote", os.path.join(OUT, "walltime.png"))
