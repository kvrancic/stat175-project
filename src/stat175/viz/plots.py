"""Plot helpers for the report and the lightning-talk teasers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


POLICY_COLORS: dict[str, str] = {
    "random": "#888888",
    "betweenness": "#1b9e77",
    "distance_threshold": "#d95f02",
    "gnn": "#7570b3",
}

POLICY_DISPLAY_NAMES: dict[str, str] = {
    "random": "Random",
    "betweenness": "Edge betweenness / cost",
    "distance_threshold": "Distance threshold (community bubble)",
    "gnn": "GNN-learned cost (ours)",
}


def pareto_frontier(
    df: pd.DataFrame,
    metric: str = "steady_state_prevalence",
    metric_low: str = "steady_state_ci_low",
    metric_high: str = "steady_state_ci_high",
    facet_col: str = "campus",
    R0: float | None = None,
    output_path: str | Path | None = None,
) -> plt.Figure:
    """Plot one Pareto curve per policy, faceted by campus."""
    if R0 is not None:
        df = df[df["R0"] == R0]
    campuses = sorted(df[facet_col].unique())
    n_campuses = len(campuses)
    columns = min(3, n_campuses)
    rows = (n_campuses + columns - 1) // columns

    figure, axes = plt.subplots(rows, columns, figsize=(5 * columns, 3.5 * rows), squeeze=False)
    for axis_index, campus in enumerate(campuses):
        axis = axes[axis_index // columns][axis_index % columns]
        sub = df[df[facet_col] == campus]
        for policy_name in sorted(sub["policy"].unique()):
            curve = sub[sub["policy"] == policy_name].sort_values("budget_fraction")
            color = POLICY_COLORS.get(policy_name, "#000")
            label = POLICY_DISPLAY_NAMES.get(policy_name, policy_name)
            axis.plot(curve["budget_fraction"], curve[metric], marker="o", color=color, label=label)
            axis.fill_between(
                curve["budget_fraction"],
                curve[metric_low],
                curve[metric_high],
                alpha=0.2,
                color=color,
            )
        axis.set_title(f"{campus}{f' (R0={R0})' if R0 is not None else ''}")
        axis.set_xlabel("Cost budget (fraction of total cost)")
        axis.set_ylabel(metric.replace("_", " "))
        axis.set_ylim(0, max(0.05, axis.get_ylim()[1]))
        axis.legend(loc="best", fontsize=8)
        axis.grid(alpha=0.25)

    for unused_index in range(n_campuses, rows * columns):
        axes[unused_index // columns][unused_index % columns].axis("off")

    figure.tight_layout()
    if output_path is not None:
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
    return figure


def ranking_heatmap(
    df: pd.DataFrame,
    metric: str = "steady_state_prevalence",
    R0: float | None = None,
    output_path: str | Path | None = None,
) -> plt.Figure:
    """Heatmap of (policy, campus) AUC rank, lower is better. Optionally filter to one R0."""
    if R0 is not None:
        df = df[df["R0"] == R0]
    auc_rows = (
        df.groupby(["campus", "policy"])
        .apply(
            lambda group: float(
                np.trapezoid(
                    group.sort_values("budget_fraction")[metric].to_numpy(),
                    group.sort_values("budget_fraction")["budget_fraction"].to_numpy(),
                )
            ),
            include_groups=False,
        )
        .reset_index(name="auc")
    )
    auc_rows["rank_within_campus"] = auc_rows.groupby("campus")["auc"].rank(method="min").astype(int)
    pivot = auc_rows.pivot(index="policy", columns="campus", values="rank_within_campus")
    figure, axis = plt.subplots(figsize=(1.2 * len(pivot.columns) + 2, 0.8 * len(pivot.index) + 1.5))
    sns.heatmap(pivot, annot=True, cmap="RdYlGn_r", cbar=False, ax=axis)
    axis.set_title(
        f"Policy AUC ranking per campus (1 = best){f', R0={R0}' if R0 is not None else ''}"
    )
    figure.tight_layout()
    if output_path is not None:
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
    return figure


def auc_table(df: pd.DataFrame, metric: str = "steady_state_prevalence") -> pd.DataFrame:
    """Return a (policy, campus, R0) AUC table."""
    return (
        df.groupby(["R0", "policy", "campus"])
        .apply(
            lambda group: float(
                np.trapezoid(
                    group.sort_values("budget_fraction")[metric].to_numpy(),
                    group.sort_values("budget_fraction")["budget_fraction"].to_numpy(),
                )
            ),
            include_groups=False,
        )
        .reset_index(name="auc")
    )
