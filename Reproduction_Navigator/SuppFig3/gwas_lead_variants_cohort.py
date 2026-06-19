#!/usr/bin/env python3
"""
RiceGraphPanGS – Fig 3: Per-type category breakdown
Two cohorts: 705rice (alone) and 705+1171rice (merged)
"""

import csv, os
from collections import Counter, defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
OUT_DIR = "/Users/goley/projects/RiceGraphPanGS/Lead variants/figures"
os.makedirs(OUT_DIR, exist_ok=True)

SNP_COLOR   = "#4C72B0"
INDEL_COLOR = "#DD8452"
SV_COLOR    = "#55A868"
TYPES       = ["SNP", "INDEL", "SV"]
TYPE_COLORS = [SNP_COLOR, INDEL_COLOR, SV_COLOR]

# Full-name → abbreviation mapping
CAT_ABBR = {
    "Yield components":   "YC",
    "Heading date":        "HD",
    "Plant architecture":  "PA",
    "Seed morphology":     "SM",
    "Taste quality":       "TQ",
}

plt.rcParams.update({
    "font.family":      "Arial",
    "font.size":        9,
    "axes.titlesize":   10,
    "axes.labelsize":   9,
    "xtick.labelsize":  8,
    "ytick.labelsize":  8,
    "legend.fontsize":  8,
    "figure.dpi":       300,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.linewidth":   0.8,
    "axes.grid":        False,
    "grid.alpha":       0.25,
    "grid.linewidth":   0.5,
})

DATA_PATH = "/Users/goley/projects/RiceGraphPanGS/Lead variants/Our_GWAS_Lead_Variants.tsv"

# ---------------------------------------------------------------------------
# DATA LOADER
# ---------------------------------------------------------------------------
def load_cohort(cohort_names):
    """
    cohort_names: list of cohort strings to include.
    Returns list of dicts {type, category}.
    """
    rows = []
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] in ("", "Marker"):
                continue
            cohort = row[8].strip()
            if cohort in cohort_names:
                rows.append({
                    "type":     row[3].upper().strip(),
                    "category": row[5],
                })
    return rows

# ---------------------------------------------------------------------------
# PLOT FUNCTION
# ---------------------------------------------------------------------------
def _wrap(s, width=1):
    """Split a phrase into one word per line."""
    return "\n".join(s.split())

def plot_fig3(data_rows, cohort_label, out_prefix):
    n_total = len(data_rows)

    type_cat_cnt = defaultdict(lambda: Counter())
    for r in data_rows:
        if r["type"] in TYPES:
            type_cat_cnt[r["type"]][r["category"]] += 1

    all_cats = sorted(c for c in set(r["category"] for r in data_rows) if c.strip())

    matrix = np.array(
        [[type_cat_cnt[t][c] for c in all_cats] for t in TYPES],
        dtype=float
    )

    # ── figure ────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(
        1, 3, figsize=(5, 3.2),
        gridspec_kw={"wspace": 0.45}
    )
    fig.suptitle(
        f"Trait Category Breakdown by Variant Type ({cohort_label})",
        fontweight="bold", y=1.02, fontsize=10
    )

    # Fixed y-axis: one row per category, shared across all panels
    cats_fixed = sorted(all_cats)
    ypos = np.arange(len(cats_fixed))

    for ax, t, color in zip(axes, TYPES, TYPE_COLORS):
        idx  = TYPES.index(t)
        vals = matrix[idx]
        pcts = vals / vals.sum() * 100

        # Retrieve values in fixed category order
        vals_ordered = np.array([type_cat_cnt[t][c] for c in cats_fixed], dtype=float)
        pcts_ordered = vals_ordered / vals_ordered.sum() * 100

        ax.barh(
            ypos, vals_ordered,
            color=color, alpha=0.85,
            edgecolor="white", linewidth=0.5,
            height=0.65
        )

        for k, (v, p) in enumerate(zip(vals_ordered, pcts_ordered)):
            ax.text(
                v + max(vals_ordered) * 0.005, k,
                f"{int(v)} ({p:.1f}%)",
                va="center", ha="left", fontsize=7.5, color="#333333"
            )

        ax.set_yticks(ypos)
        ax.set_yticklabels(
            [CAT_ABBR.get(c, c) for c in cats_fixed], fontsize=8
        )
        if ax != axes[0]:
            ax.set_yticklabels([])
        ax.set_xlim(0, max(vals_ordered) * 1.50)
        ax.invert_yaxis()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        type_total = int(vals_ordered.sum())
        type_pct   = type_total / n_total * 100
        ax.set_title(
            f"{t}\n(n = {type_total:,},  {type_pct:.1f}%)",
            color=color, fontweight="bold", fontsize=9
        )

    # ── legend strip at bottom (two lines) ─────────────────────────────────
    present = [(full, abbr) for full, abbr in CAT_ABBR.items()
               if full in all_cats]
    line1 = "  |  ".join(f"{abbr}" for _, abbr in present)
    line2 = "  |  ".join(f"{full}" for full, _ in present)
    fig.text(0.5, 0.040, line1, ha="center", va="bottom",
             fontsize=7.5, color="#555555", style="italic")
    fig.text(0.5, 0.010, line2, ha="center", va="bottom",
             fontsize=6.8, color="#555555", style="italic")

    # Shared y-axis label on the left panel only
    axes[0].set_ylabel("Trait Category", fontsize=8)

    # X-axis label
    axes[1].set_xlabel("Number of Lead Variants", fontsize=9)

    plt.subplots_adjust(bottom=0.19)

    out_png = f"{OUT_DIR}/{out_prefix}.png"
    out_pdf = f"{OUT_DIR}/{out_prefix}.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close()
    print(f"  ✓ saved  {out_png}")
    return matrix, all_cats, n_total

# ---------------------------------------------------------------------------
# STATS TABLE
# ---------------------------------------------------------------------------
def print_stats(matrix, all_cats, n_total, label):
    print(f"\n{'─' * 60}")
    print(f"  {label}")
    print(f"{'─' * 60}")
    print(f"{'Category':<28} {'SNP':>8} {'INDEL':>8} {'SV':>8} {'Total':>8}")
    print("─" * 64)
    for cat in all_cats:
        j   = all_cats.index(cat)
        SNP = int(matrix[0][j])
        IND = int(matrix[1][j])
        SV  = int(matrix[2][j])
        tot = SNP + IND + SV
        print(f"{cat:<28} {SNP:>6,}  {IND:>6,}  {SV:>6,}  {tot:>6,}")
    print("─" * 64)
    totals = matrix.sum(axis=1).astype(int)
    grand  = int(matrix.sum())
    for i, t in enumerate(TYPES):
        p = totals[i] / grand * 100
        print(f"{'Total '+t:<28} {totals[i]:>6,}  ({p:.1f}%)")

# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------
print("=" * 62)
print("  Fig 3 — Per-type Category Breakdown")
print("=" * 62)

# 1) 705rice alone
rows_705 = load_cohort(["705rice"])
print(f"\n705rice cohort: {len(rows_705):,} variants")
m705, cats_705, n705 = plot_fig3(
    rows_705, "705rice", "fig3_per_type_breakdown_705rice"
)
print_stats(m705, cats_705, n705, "Type × Category (705rice)")

# 2) 705rice + 1171rice merged
rows_mix = load_cohort(["705rice", "1171rice"])
print(f"\n705rice + 1171rice merged: {len(rows_mix):,} variants")
mMix, cats_Mix, nMix = plot_fig3(
    rows_mix, "705+1171rice", "fig3_per_type_breakdown_705_1171rice"
)
print_stats(mMix, cats_Mix, nMix, "Type × Category (705+1171rice)")

# 3) Comparison summary
print(f"\n{'═' * 62}")
print("  Comparison Summary")
print(f"{'═' * 62}")
for label, m, n in [
    ("705rice          ", m705,  n705),
    ("1171rice (prior) ", None,  309),
    ("705+1171rice mix ", mMix,  nMix),
]:
    if m is not None:
        t0,t1,t2 = m.sum(axis=1)
    else:
        t0,t1,t2 = 217, 43, 49
    print(
        f"  {label}  "
        f"SNP={t0:>4.0f}({t0/n*100:.1f}%)  "
        f"INDEL={t1:>4.0f}({t1/n*100:.1f}%)  "
        f"SV={t2:>4.0f}({t2/n*100:.1f}%)"
    )

print(f"\n  ✓ All done — figures in {OUT_DIR}/")
