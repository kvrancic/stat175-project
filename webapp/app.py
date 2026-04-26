"""Streamlit demo: explore SIS containment policies on Facebook100 campuses.

Usage:
    streamlit run webapp/app.py

The app reads cached campus artifacts from data/processed/, the trained
GNN encoders from data/processed/gnn_encoders/, and runs simulations
on demand. All controls are in the left sidebar; the main pane shows
the residual graph (selected edges greyed out), the per-step
prevalence trajectory, and the cached Pareto frontier for the chosen
campus / R0.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from scripts._cache_loader import load_cache  # noqa: E402

from stat175.costs.edge_costs import compute_costs  # noqa: E402
from stat175.policies.base import PolicyInput, apply_removal  # noqa: E402
from stat175.policies.betweenness import EdgeBetweennessOverCost  # noqa: E402
from stat175.policies.distance_threshold import DistanceThreshold  # noqa: E402
from stat175.policies.gnn_policy import GNNPolicy  # noqa: E402
from stat175.policies.random_baseline import RandomEdgeRemoval  # noqa: E402
from stat175.sim.sis import SISConfig, run_sis, spectral_radius  # noqa: E402
from stat175.viz.plots import POLICY_COLORS, POLICY_DISPLAY_NAMES, pareto_frontier  # noqa: E402


CAMPUS_OPTIONS = ["Caltech36", "Bowdoin47", "Harvard1", "Penn94", "Tennessee95"]
COST_OPTIONS = ["sigmoid_dot", "cosine", "uniform"]
POLICY_OPTIONS = ["random", "betweenness", "distance_threshold", "gnn"]


@st.cache_resource(show_spinner=False)
def load_campus_artifacts(name: str):
    return load_cache(name)


@st.cache_resource(show_spinner=False)
def load_encoder_cached(name: str):
    try:
        from scripts.train_gnn_helpers import load_encoder

        return load_encoder(name)
    except FileNotFoundError:
        return None


@st.cache_data(show_spinner=False)
def precomputed_pareto_path() -> Path | None:
    path = REPO_ROOT / "results" / "main_pareto.parquet"
    if not path.exists():
        return None
    return path


def build_policy(name: str, encoder, features) -> object:
    if name == "random":
        return RandomEdgeRemoval()
    if name == "betweenness":
        return EdgeBetweennessOverCost(betweenness_pivots=300)
    if name == "distance_threshold":
        return DistanceThreshold()
    if name == "gnn":
        if encoder is None:
            raise RuntimeError(
                "No trained GNN encoder available for this campus. Run scripts/03_train_gnn.py."
            )
        return GNNPolicy(encoder, features, device="cpu")
    raise ValueError(f"unknown policy {name}")


st.set_page_config(page_title="STAT 175 — SIS containment", layout="wide")

st.title("Cost-constrained edge removal for SIS epidemic containment")
st.caption(
    "Pick a campus, an epidemic regime, and a containment policy. Watch how the "
    "selected edges and the policy's bang-for-buck score reshape the steady-state "
    "infection rate. (STAT 175 final project; data: Facebook100.)"
)

with st.sidebar:
    st.header("Setup")
    campus_name = st.selectbox("Campus", CAMPUS_OPTIONS, index=0)
    R0 = st.slider("Reproduction number R0 (= beta * lambda(A) / gamma)", 0.5, 8.0, 3.0, 0.1)
    gamma = st.slider("Recovery rate gamma", 0.01, 0.5, 0.10, 0.01)
    cost_name = st.selectbox("Cost function", COST_OPTIONS, index=0)
    policy_name = st.selectbox("Policy", POLICY_OPTIONS, index=2)
    budget_fraction = st.slider("Cost budget (fraction of total cost)", 0.0, 0.5, 0.05, 0.005)
    n_realizations = st.slider("Number of stochastic realizations", 5, 50, 20, 5)
    n_steps = st.slider("Simulation steps", 50, 400, 200, 25)
    seed = st.number_input("Random seed", min_value=0, max_value=2**31 - 1, value=42, step=1)
    run_button = st.button("Run simulation", type="primary")

with st.spinner("Loading campus artifacts..."):
    cache = load_campus_artifacts(campus_name)
    adjacency = cache["adjacency"]
    edges = cache["edges"]
    features = cache["features"]
    if cost_name == "sigmoid_dot":
        costs = cache["sigmoid_dot_costs"]
    else:
        costs = compute_costs(cost_name, features, edges)
    encoder = load_encoder_cached(campus_name)

n_nodes = int(adjacency.shape[0])
n_edges = int(edges.shape[0])
lam = spectral_radius(adjacency)
beta = R0 * gamma / lam

c1, c2, c3, c4 = st.columns(4)
c1.metric("Nodes", f"{n_nodes:,}")
c2.metric("Edges", f"{n_edges:,}")
c3.metric("lambda_1(A)", f"{lam:.2f}")
c4.metric("tau_c = 1/lambda", f"{1.0 / lam:.4f}")

if run_button:
    if policy_name == "gnn" and encoder is None:
        st.error(
            "No trained GNN encoder for this campus. Run `python scripts/03_train_gnn.py` first."
        )
    else:
        with st.spinner("Selecting edges to remove..."):
            policy = build_policy(policy_name, encoder, features)
            inputs = PolicyInput(
                adjacency=adjacency,
                edges=edges,
                costs=costs,
                budget=budget_fraction * float(costs.sum()),
                seed=int(seed),
            )
            removed = (
                policy.select(inputs)
                if budget_fraction > 0
                else np.empty(0, dtype=np.int64)
            )
            residual = apply_removal(adjacency, edges, removed)
        st.success(f"Removed {removed.size:,} edges (cost used = {float(costs[removed].sum()):.1f}).")

        with st.spinner("Running SIS simulation..."):
            sis_config = SISConfig(
                beta=beta,
                gamma=float(gamma),
                n_steps=int(n_steps),
                burn_in=min(int(n_steps) // 2, 100),
                n_realizations=int(n_realizations),
                seed=int(seed),
            )
            result = run_sis(residual, sis_config)
            no_intervention = run_sis(adjacency, sis_config)

        a, b = st.columns([1, 1])
        with a:
            figure, axis = plt.subplots(figsize=(5, 3))
            axis.plot(no_intervention.per_step_prevalence_mean, color="#888", label="no removal")
            axis.fill_between(
                np.arange(no_intervention.per_step_prevalence_mean.shape[0]),
                no_intervention.per_step_prevalence_mean - no_intervention.per_step_prevalence_std,
                no_intervention.per_step_prevalence_mean + no_intervention.per_step_prevalence_std,
                color="#888",
                alpha=0.2,
            )
            axis.plot(
                result.per_step_prevalence_mean,
                color=POLICY_COLORS.get(policy_name, "C0"),
                label=POLICY_DISPLAY_NAMES.get(policy_name, policy_name),
            )
            axis.fill_between(
                np.arange(result.per_step_prevalence_mean.shape[0]),
                result.per_step_prevalence_mean - result.per_step_prevalence_std,
                result.per_step_prevalence_mean + result.per_step_prevalence_std,
                color=POLICY_COLORS.get(policy_name, "C0"),
                alpha=0.25,
            )
            axis.set_xlabel("Step")
            axis.set_ylabel("Fraction infected")
            axis.set_title(f"{campus_name} (R0={R0:.1f})")
            axis.legend()
            axis.grid(alpha=0.25)
            st.pyplot(figure, clear_figure=True)
        with b:
            no_intervention_steady = no_intervention.steady_state_prevalence
            ci_low, ci_high = result.steady_state_ci95
            st.markdown(
                f"### Outcomes\n"
                f"- **Steady-state prevalence**: {result.steady_state_prevalence:.3f}  "
                f"(95% CI: {ci_low:.3f}, {ci_high:.3f})\n"
                f"- **Peak prevalence**: {result.peak_prevalence:.3f}\n"
                f"- **No-intervention reference**: {no_intervention_steady:.3f}\n"
                f"- Reduction vs no removal: "
                f"{(no_intervention_steady - result.steady_state_prevalence):.3f}"
            )

# Frontier from cached results, if available.
pareto_path = precomputed_pareto_path()
if pareto_path is not None:
    df = pd.read_parquet(pareto_path)
    df_subset = df[(df["campus"] == campus_name) & (np.isclose(df["R0"], R0, atol=1e-3))]
    if df_subset.empty:
        st.info(
            f"No cached Pareto frontier for ({campus_name}, R0={R0:.1f}); run "
            "`python scripts/04_run_pareto.py` to populate."
        )
    else:
        figure = pareto_frontier(df_subset, R0=R0)
        st.pyplot(figure, clear_figure=True)
else:
    st.info(
        "Run `python scripts/04_run_pareto.py` to generate cached Pareto frontiers; "
        "those will appear here automatically."
    )
