#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter

BLUP_FILE = "Yield_SNBR_BLUP_values.tsv"

OUT_FIG = "Yield_SNBR_BLUP_continuous_selection_plot.pdf"
OUT_SELECTED = "Yield_SNBR_selected_lines_continuous.tsv"

Y_COL = "YieldPerPlant_BLUP"
SNBR_COL = "ScaleOfNeckBlastResistance_BLUP"
SUBPOP_COL = "Subpopulation"

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans"]
mpl.rcParams["axes.linewidth"] = 1.5

PALETTE = {
    "japonica": "#6FA87C",
    "indica": "#D9798A",
    "other": "#BDBDBD"
}


def clean_subpop(x):
    if pd.isna(x):
        return "other"

    x = str(x).strip().lower()

    if "japonica" in x:
        return "japonica"

    if "indica" in x:
        return "indica"

    return "other"


def main():
    df = pd.read_csv(BLUP_FILE, sep="\t")

    df[Y_COL] = pd.to_numeric(df[Y_COL], errors="coerce")
    df[SNBR_COL] = pd.to_numeric(df[SNBR_COL], errors="coerce")

    df = df.dropna(subset=[Y_COL, SNBR_COL]).copy()

    if SUBPOP_COL not in df.columns:
        df[SUBPOP_COL] = "other"

    df[SUBPOP_COL] = df[SUBPOP_COL].apply(clean_subpop)

    yield_cutoff = df[Y_COL].quantile(0.75)
    snbr_cutoff = df[SNBR_COL].quantile(0.25)

    df["Top25_Yield"] = df[Y_COL] >= yield_cutoff
    df["Bottom25_SNBR"] = df[SNBR_COL] <= snbr_cutoff
    df["Selected"] = df["Top25_Yield"] & df["Bottom25_SNBR"]

    df[df["Selected"]].to_csv(
        OUT_SELECTED,
        sep="\t",
        index=False
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    for subpop in ["japonica", "indica", "other"]:
        tmp = df[
            (df[SUBPOP_COL] == subpop) &
            (~df["Selected"])
        ]

        if tmp.empty:
            continue

        ax.scatter(
            tmp[Y_COL],
            tmp[SNBR_COL],
            s=70,
            c=PALETTE[subpop],
            alpha=0.72,
            edgecolors="none",
            zorder=2
        )

    selected = df[df["Selected"]]

    for subpop in ["japonica", "indica", "other"]:
        tmp = selected[selected[SUBPOP_COL] == subpop]

        if tmp.empty:
            continue

        ax.scatter(
            tmp[Y_COL],
            tmp[SNBR_COL],
            s=190,
            c=PALETTE[subpop],
            alpha=0.98,
            edgecolors="black",
            linewidths=1.8,
            zorder=5
        )

    ax.axvline(
        yield_cutoff,
        color="black",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        zorder=1
    )

    ax.axhline(
        snbr_cutoff,
        color="black",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        zorder=1
    )

    ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

    ax.set_xlabel(
        "Grain yield per plant (BLUP)",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_ylabel(
        "Scale of neck blast resistance (BLUP)",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_title(
        "Selection of high-yield and neck blast-resistant rice lines",
        fontsize=16,
        fontweight="bold",
        pad=18
    )

    ax.text(
        0.70,
        0.08,
        "High yield and\nblast-resistant lines",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

    legend_elements = [
        Line2D(
            [0], [0],
            marker="o",
            color="none",
            markerfacecolor=PALETTE["japonica"],
            markeredgecolor="none",
            markersize=11,
            label="Japonica"
        ),
        Line2D(
            [0], [0],
            marker="o",
            color="none",
            markerfacecolor=PALETTE["indica"],
            markeredgecolor="none",
            markersize=11,
            label="Indica"
        ),
        Line2D(
            [0], [0],
            marker="o",
            color="black",
            markerfacecolor="white",
            markeredgecolor="black",
            markeredgewidth=1.6,
            markersize=12,
            label="Top 25% Yield & Bottom 25% SNBR"
        )
    ]

    legend = ax.legend(
        handles=legend_elements,
        loc="lower left",
        frameon=False,
        fontsize=12,
        handletextpad=0.6
    )

    legend_texts = legend.get_texts()
    legend_texts[0].set_fontstyle("italic")
    legend_texts[0].set_fontweight("bold")

    legend_texts[1].set_fontstyle("italic")
    legend_texts[1].set_fontweight("bold")

    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.5)

    ax.tick_params(
        axis="both",
        which="major",
        labelsize=14,
        width=1.5,
        length=6
    )

    ax.grid(False)

    plt.tight_layout()

    plt.savefig(
        OUT_FIG,
        bbox_inches="tight"
    )

    plt.close()

    print(f"[INFO] Input file: {BLUP_FILE}")
    print(f"[INFO] Output figure: {OUT_FIG}")
    print(f"[INFO] Selected table: {OUT_SELECTED}")
    print(f"[INFO] Yield cutoff: {yield_cutoff:.4f}")
    print(f"[INFO] SNBR cutoff: {snbr_cutoff:.4f}")
    print(f"[INFO] Selected lines: {df['Selected'].sum()} / {df.shape[0]}")


if __name__ == "__main__":
    main()