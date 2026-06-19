"""
Heritability plot: all phenotypes in gray style
No BLUP highlight
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARAMETERS
# ============================================================
CSV_FILE = "Her.csv"

FIG_SIZE = (4, 3)
DPI = 600

Y_MIN = 0.30
Y_MAX = 1.01
OUT_PNG = "heritability_methods_lines_gray.png"
OUT_PDF = "heritability_methods_lines_gray.pdf"

LINE_COLOR = "#B8B8B8"
EDGE_COLOR = "#9A9A9A"

LINE_WIDTH = 0.80
LINE_ALPHA = 0.80
MARKER_SIZE = 20
# ============================================================


plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "axes.linewidth": 0.9,
    "axes.labelsize": 12,
    "xtick.labelsize": 8,
    "ytick.labelsize": 10,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


df_raw = pd.read_csv(CSV_FILE, header=None)

row0 = df_raw.iloc[0].values
row1 = df_raw.iloc[1].values


# ── Parse column structure ──────────────────────────────────
col_map = {}
current = None

for i, cell in enumerate(row0):
    cell = str(cell).strip()

    if cell and cell not in ("nan", "", "Phenotypes"):
        current = cell
        col_map[current] = []

    if current and i > 0:
        col_map[current].append(i)


col_info = {}
current = None

for i, cell in enumerate(row0):
    c = str(cell).strip()

    if c and c not in ("nan", "", "Phenotypes"):
        current = c

    t = str(row1[i]).strip() if i < len(row1) else ""

    if t in ("Linear", "Graph"):
        col_info[i] = (current, t)


# ── Extract data ────────────────────────────────────────────
phenotypes = []
data = {}

for idx in range(2, len(df_raw)):
    ph = str(df_raw.iloc[idx, 0]).strip()

    if not ph or ph in ("nan", ""):
        continue

    phenotypes.append(ph)
    data[ph] = {}

    for v, cols in col_map.items():
        data[ph][v] = {
            "Linear": np.nan,
            "Graph": np.nan,
        }

        for ci in cols:
            ref = col_info.get(ci, (None, None))[1]

            if ref in ("Linear", "Graph"):
                val = str(df_raw.iloc[idx, ci]).strip()
                data[ph][v][ref] = float(val) if val not in ("nan", "") else np.nan


print(f"Loaded {len(phenotypes)} phenotypes")


# ── X-axis order ────────────────────────────────────────────
methods = [
    ("SNP", "Linear"),
    ("SNP", "Graph"),
    ("SNP_INDEL_SV", "Linear"),
    ("SNP_INDEL_SV", "Graph"),
]

labels = [
    "SNP\n(Linear)",
    "SNP\n(Graph)",
    "SNP_INDEL_SV\n(Linear)",
    "SNP_INDEL_SV\n(Graph)",
]

x = np.arange(len(methods))


# ── Plot ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=FIG_SIZE)

for ph in phenotypes:
    y = np.array([
        data[ph].get(v, {}).get(r, np.nan)
        for v, r in methods
    ])

    mask = ~np.isnan(y)

    ax.plot(
        x[mask],
        y[mask],
        color=LINE_COLOR,
        linewidth=LINE_WIDTH,
        alpha=LINE_ALPHA,
        zorder=1,
    )

    ax.scatter(
        x[mask],
        y[mask],
        s=MARKER_SIZE,
        facecolor="white",
        edgecolor=EDGE_COLOR,
        linewidth=0.65,
        alpha=LINE_ALPHA,
        zorder=2,
    )


# ── Axes ────────────────────────────────────────────────────
ax.set_xlim(-0.1, 3.2)
ax.set_ylim(Y_MIN, Y_MAX)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8)

ax.set_ylabel(r"Heritability [$H^2$]")

for xpos in x[1:]:
    ax.axvline(
        xpos,
        linestyle=(0, (4, 4)),
        color="#9E9E9E",
        lw=0.8,
        alpha=0.65,
        zorder=0,
    )

ax.grid(axis="y", color="#DADADA", lw=0.6, alpha=0.7)
ax.grid(axis="x", visible=False)

# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)

ax.tick_params(
    axis="both",
    direction="out",
    length=3.5,
    width=0.8,
    colors="black",
)


# ── Save ────────────────────────────────────────────────────
plt.tight_layout()

plt.savefig(OUT_PNG, dpi=DPI, bbox_inches="tight", facecolor="white")
plt.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")


print(f"Saved: {OUT_PNG}")
print(f"Saved: {OUT_PDF}")