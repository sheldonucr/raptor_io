import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "figs")

# ---- data from ibm_ieks_raieks_shift1_results.md ----
circuits = ["ibmpg1t", "ibmpg2t", "ibmpg3t"]
nodes    = ["54K nodes", "165K nodes", "1.04M nodes"]

be_cpu   = [2.267, 14.097, 203.929]
raieks_cpu = [0.407, 1.189, 32.642]
raieks_speedup = [5.57, 11.86, 6.25]

# normalized waveform error vs direct back euler (avg / max)
raieks_avg = [7.082e-07, 3.303e-08, 1.428e-07]
raieks_max = [5.620e-06, 7.388e-08, 7.942e-07]
ieks_max   = [6.662e-14, 1.712e-13, 1.737e-06]

# palette (aligned with noveety-ai.com light theme — deep teal + blue on off-white)
BG      = "none"
PANEL   = "#ffffff"
TEXT    = "#172b32"
MUTED   = "#52646b"
GRID    = (23/255,43/255,50/255,0.12)
TEAL    = "#087964"   # GridStack accent (primary)
BLUE    = "#215fa4"   # secondary accent
REF     = "#8a9a9f"   # neutral reference line
# back-compat aliases
EMERALD = TEAL
CYAN    = BLUE
VIOLET  = REF

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": TEXT, "axes.labelcolor": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": (23/255,43/255,50/255,0.28),
})

def style(ax):
    ax.set_facecolor("none")
    for s in ["top","right"]:
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)

# ============ 1. ACCURACY COMPARISON ============
fig, ax = plt.subplots(figsize=(9.4, 5.0), dpi=150)
fig.patch.set_alpha(0)
x = np.arange(len(circuits))
w = 0.36

b1 = ax.bar(x - w/2, raieks_avg, w, label="Average error", color=TEAL, edgecolor="none")
b2 = ax.bar(x + w/2, raieks_max, w, label="Maximum error", color=BLUE, edgecolor="none", alpha=0.9)

ax.set_yscale("log")
ax.set_ylim(1e-9, 1e-4)
ax.axhline(1e-6, color=REF, linestyle="--", linewidth=1.3, alpha=0.8)
ax.text(2.42, 1.25e-6, "1e-6", color=REF, fontsize=9, ha="right", va="bottom")

ax.set_xticks(x)
ax.set_xticklabels([f"{c}\n{n}" for c, n in zip(circuits, nodes)], fontsize=10.5)
ax.set_ylabel("Normalized waveform error vs. direct solve", fontsize=11)
ax.set_title("GridStack accuracy — advanced Krylov reduction vs. direct transient solve",
             color=TEXT, fontsize=12.5, pad=14, weight="bold")
style(ax)
leg = ax.legend(loc="upper right", frameon=False, fontsize=10.5)
for t in leg.get_texts(): t.set_color(TEXT)

for bars in (b1, b2):
    for r in bars:
        h = r.get_height()
        ax.annotate(f"{h:.1e}", (r.get_x()+r.get_width()/2, h),
                    textcoords="offset points", xytext=(0,4),
                    ha="center", fontsize=8.2, color=MUTED)

fig.tight_layout()
fig.savefig(f"{OUT}/accuracy_comparison.png", transparent=True, bbox_inches="tight")
plt.close(fig)

# ============ 2. SPEEDUP COMPARISON ============
fig, ax = plt.subplots(figsize=(9.4, 4.6), dpi=150)
fig.patch.set_alpha(0)
x = np.arange(len(circuits))
bars = ax.bar(x, raieks_speedup, 0.5,
              color=[BLUE, TEAL, BLUE], edgecolor="none")
ax.set_xticks(x)
ax.set_xticklabels([f"{c}\n{n}" for c, n in zip(circuits, nodes)], fontsize=10.5)
ax.set_ylabel("Speedup over direct transient solve (×)", fontsize=11)
ax.set_ylim(0, 13.5)
ax.set_title("GridStack CPU-time speedup — up to 11.9× faster than direct back-Euler",
             color=TEXT, fontsize=12.5, pad=14, weight="bold")
style(ax)
for r, s, bc, rc in zip(bars, raieks_speedup, be_cpu, raieks_cpu):
    ax.annotate(f"{s:.2f}×", (r.get_x()+r.get_width()/2, s),
                textcoords="offset points", xytext=(0,6),
                ha="center", fontsize=11.5, color=TEXT, weight="bold")
    ax.annotate(f"{bc:.1f}s → {rc:.2f}s", (r.get_x()+r.get_width()/2, 0.35),
                ha="center", fontsize=8.6, color="#ffffff")
fig.tight_layout()
fig.savefig(f"{OUT}/speedup_comparison.png", transparent=True, bbox_inches="tight")
plt.close(fig)

print("wrote accuracy_comparison.png and speedup_comparison.png")
