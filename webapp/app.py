"""Streamlit demo: SIS containment on Harvard1, visualized as a dorm-clustered graph.

Usage:
    uv run streamlit run webapp/app.py

The full screen is the campus contact graph: nodes are students, spatially
grouped by dorm. When the simulation runs, infected nodes light up red
step-by-step (drag the slider, or click Play).
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.collections import LineCollection
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from scripts._cache_loader import load_cache  # noqa: E402

import scipy.sparse as sp  # noqa: E402
from scipy.sparse.csgraph import connected_components  # noqa: E402

from stat175.costs.edge_costs import compute_costs, edges_from_adjacency  # noqa: E402
from stat175.policies.base import PolicyInput, apply_removal  # noqa: E402
from stat175.policies.betweenness import EdgeBetweennessOverCost  # noqa: E402
from stat175.policies.distance_threshold import DistanceThreshold  # noqa: E402
from stat175.policies.gnn_policy import GNNPolicy  # noqa: E402
from stat175.policies.random_baseline import RandomEdgeRemoval  # noqa: E402
from stat175.sim.sis import spectral_radius  # noqa: E402


CAMPUS = "Harvard1"
DORM_COLUMN = 4  # facebook100 attribute column for dorm/house

# 12 largest dorm codes for Harvard1 (the 12 undergrad houses + freshman yard
# cluster). Codes 0 and 12+ are mostly missing-data or tiny non-undergrad
# affiliations and would only clutter the visualization.
UNDERGRAD_DORM_CODES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 27)

# Randomly sample roughly this many students from the undergrad-house subgraph
# so the canvas stays readable. The induced subgraph is sparser and shows the
# dorm clusters clearly.
TARGET_NODES = 1200

# Hardcoded simulation defaults (match configs/default.yaml main experiment).
N_STEPS = 200
N_SEEDS = 10
SEED = 42

POLICY_OPTIONS = ["random", "betweenness", "distance_threshold", "gnn"]
POLICY_LABELS = {
    "random": "Random",
    "betweenness": "Edge betweenness / cost",
    "distance_threshold": "Distance threshold (community bubbles)",
    "gnn": "GNN (learned)",
}


def _take_giant_component(adj, features, attrs):
    n_components, component_labels = connected_components(adj, directed=False)
    if n_components <= 1:
        return adj, features, attrs
    component_sizes = np.bincount(component_labels)
    giant = np.where(component_labels == int(np.argmax(component_sizes)))[0]
    return adj[giant][:, giant].tocsr(), features[giant], attrs[giant]


@st.cache_resource(show_spinner="Loading Harvard undergrad contact graph...")
def load_harvard():
    """Restrict Harvard1 to undergrad dorms, randomly subsample students, take giant component."""
    cache = load_cache(CAMPUS)
    full_adjacency = cache["adjacency"]
    attributes = cache["attributes"]
    full_features = cache["features"]

    dorms = attributes[:, DORM_COLUMN].astype(np.int64)
    keep = np.isin(dorms, np.array(UNDERGRAD_DORM_CODES, dtype=np.int64))
    keep_indices = np.where(keep)[0]

    sub_adj = full_adjacency[keep_indices][:, keep_indices].tocsr()
    sub_attrs = attributes[keep_indices]
    sub_features = full_features[keep_indices]

    sub_adj, sub_features, sub_attrs = _take_giant_component(sub_adj, sub_features, sub_attrs)

    if sub_adj.shape[0] > TARGET_NODES:
        rng = np.random.default_rng(SEED)
        chosen = np.sort(rng.choice(sub_adj.shape[0], size=TARGET_NODES, replace=False))
        sub_adj = sub_adj[chosen][:, chosen].tocsr()
        sub_attrs = sub_attrs[chosen]
        sub_features = sub_features[chosen]
        sub_adj, sub_features, sub_attrs = _take_giant_component(sub_adj, sub_features, sub_attrs)

    edges = edges_from_adjacency(sub_adj)
    costs = compute_costs("sigmoid_dot", sub_features, edges)

    return {
        "adjacency": sub_adj,
        "attributes": sub_attrs,
        "features": sub_features,
        "edges": edges,
        "sigmoid_dot_costs": costs,
        "lambda_1": spectral_radius(sub_adj),
    }


@st.cache_resource(show_spinner=False)
def load_encoder_cached():
    try:
        from scripts.train_gnn_helpers import load_encoder

        return load_encoder(CAMPUS)
    except FileNotFoundError:
        return None


@st.cache_resource(show_spinner="Computing dorm-clustered layout...")
def dorm_layout(attributes_bytes: bytes, n: int):
    # The bytes arg is just a cache key; recover the array from the loaded cache.
    cache = load_harvard()
    dorms = cache["attributes"][:, DORM_COLUMN].astype(np.int64)
    unique_dorms = np.array(sorted({int(d) for d in dorms}))
    counts = {int(d): int((dorms == d).sum()) for d in unique_dorms}
    ordered = sorted(unique_dorms, key=lambda d: -counts[int(d)])

    big_radius = 16.0
    centers: dict[int, tuple[float, float]] = {}
    for i, d in enumerate(ordered):
        theta = 2.0 * np.pi * i / max(1, len(ordered))
        centers[int(d)] = (big_radius * np.cos(theta), big_radius * np.sin(theta))

    rng = np.random.default_rng(0)
    xs = np.zeros(n, dtype=np.float64)
    ys = np.zeros(n, dtype=np.float64)
    for d in ordered:
        idxs = np.where(dorms == int(d))[0]
        if idxs.size == 0:
            continue
        cx, cy = centers[int(d)]
        cluster_radius = 0.4 + 0.13 * np.sqrt(idxs.size)
        angle = rng.uniform(0.0, 2.0 * np.pi, size=idxs.size)
        radial = cluster_radius * np.sqrt(rng.uniform(0.0, 1.0, size=idxs.size))
        xs[idxs] = cx + radial * np.cos(angle)
        ys[idxs] = cy + radial * np.sin(angle)
    return xs, ys


@st.cache_resource(show_spinner=False)
def edge_segments():
    """All inter-supernode edges as 2-D line segments for matplotlib."""
    cache = load_harvard()
    edges = cache["edges"]
    xs, ys = dorm_layout(b"_", int(cache["adjacency"].shape[0]))
    segs = np.stack(
        [np.column_stack([xs[edges[:, 0]], ys[edges[:, 0]]]),
         np.column_stack([xs[edges[:, 1]], ys[edges[:, 1]]])],
        axis=1,
    )
    return segs


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
                "No trained GNN encoder for Harvard1. Run scripts/03_train_gnn.py."
            )
        return GNNPolicy(encoder, features, device="cpu")
    raise ValueError(f"unknown policy {name}")


def simulate_history(adjacency, residual_edges, beta: float, gamma: float,
                     n_steps: int, n_seeds: int, seed: int):
    """Run a single SIS realization, returning the infected history and per-step transmission edges.

    Returns
    -------
    history : ndarray of shape (n_steps + 1, n) with the infected boolean state at each step.
    transmissions_per_step : list of length n_steps + 1 where each element is an int64 array
        of indices into ``residual_edges`` for edges (u, v) such that one endpoint went S->I
        in this step and the other endpoint was I at the previous step. Step 0 is empty.
    """
    n = int(adjacency.shape[0])
    rng = np.random.default_rng(seed)
    log_one_minus_beta = np.log1p(-beta) if beta > 0 else 0.0
    adjacency_float = adjacency.astype(np.float32)
    u_idx = residual_edges[:, 0]
    v_idx = residual_edges[:, 1]

    seeds = rng.choice(n, size=min(n_seeds, n), replace=False)
    infected = np.zeros(n, dtype=bool)
    infected[seeds] = True

    history = np.zeros((n_steps + 1, n), dtype=bool)
    history[0] = infected
    transmissions_per_step: list[np.ndarray] = [np.empty(0, dtype=np.int64)]
    for step in range(1, n_steps + 1):
        previous = infected
        susceptible = ~previous
        infected_count = adjacency_float @ previous.astype(np.float32)
        if log_one_minus_beta == 0.0:
            infect_probability = np.zeros_like(infected_count, dtype=np.float64)
        else:
            infect_probability = 1.0 - np.exp(log_one_minus_beta * infected_count)
        new_infections = susceptible & (rng.random(n) < infect_probability)
        recoveries = previous & (rng.random(n) < gamma)
        infected = (previous & ~recoveries) | new_infections
        history[step] = infected

        transmission_mask = (
            (new_infections[u_idx] & previous[v_idx])
            | (new_infections[v_idx] & previous[u_idx])
        )
        transmissions_per_step.append(np.where(transmission_mask)[0].astype(np.int64))
    return history, transmissions_per_step


def render_frame(xs: np.ndarray, ys: np.ndarray, segments, sizes: np.ndarray,
                 infected_mask: np.ndarray, step_index: int, n_steps: int) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(11, 11), dpi=90)
    figure.patch.set_facecolor("#0d1117")
    axis.set_facecolor("#0d1117")
    if segments is not None:
        line_collection = LineCollection(segments, colors="#1f2733", linewidths=0.25, alpha=0.18)
        axis.add_collection(line_collection)
    susceptible_mask = ~infected_mask
    axis.scatter(
        xs[susceptible_mask], ys[susceptible_mask],
        s=sizes[susceptible_mask] * 1.5, c="#5a6472", alpha=0.85, linewidths=0,
    )
    axis.scatter(
        xs[infected_mask], ys[infected_mask],
        s=sizes[infected_mask] * 2.4, c="#ff3b3b", alpha=0.95, linewidths=0,
    )
    axis.set_xticks([]); axis.set_yticks([])
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.set_aspect("equal")
    prevalence = float(infected_mask.mean())
    axis.set_title(
        f"Harvard1   step {step_index}/{n_steps}    prevalence {prevalence:.1%}",
        color="#f0f6fc", fontsize=14, pad=12,
    )
    figure.tight_layout()
    return figure


def build_animation_gif(
    history: np.ndarray,
    xs: np.ndarray,
    ys: np.ndarray,
    residual_segments: np.ndarray,
    removed_segments: np.ndarray,
    transmissions_per_step: list,
    sizes: np.ndarray,
    n_steps: int,
    frame_step: int = 2,
    fps: int = 12,
) -> bytes:
    """Render the SIS trajectory into an in-memory looping GIF.

    Edges in the residual graph are drawn faintly behind the nodes. On any step
    where a susceptible node was infected by an infectious neighbor, the edge
    between them is overlaid in red for that frame, so the GIF surfaces the
    contact pathways the epidemic actually used.
    """
    figure, axis = plt.subplots(figsize=(11, 11), dpi=80)
    figure.patch.set_facecolor("#0d1117")
    axis.set_facecolor("#0d1117")
    axis.add_collection(
        LineCollection(residual_segments, colors="#1f2733", linewidths=0.25, alpha=0.18)
    )
    if removed_segments.shape[0] > 0:
        axis.add_collection(
            LineCollection(
                removed_segments, colors="#d4a017", linewidths=0.45, alpha=0.55,
            )
        )
    transmission_collection = LineCollection(
        np.empty((0, 2, 2)), colors="#4a1f1f", linewidths=0.8, alpha=0.4,
    )
    axis.add_collection(transmission_collection)
    axis.set_xlim(xs.min() - 1.0, xs.max() + 1.0)
    axis.set_ylim(ys.min() - 1.0, ys.max() + 1.0)
    axis.set_xticks([]); axis.set_yticks([])
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.set_aspect("equal")
    susceptible_scatter = axis.scatter(
        [], [], s=42, c="#5a6472", alpha=0.85, linewidths=0,
    )
    infected_scatter = axis.scatter(
        [], [], s=60, c="#ff3b3b", alpha=0.95, linewidths=0,
    )
    title_artist = axis.set_title(
        f"Harvard1   step 0/{n_steps}    prevalence 0.0%",
        color="#f0f6fc", fontsize=14, pad=12,
    )
    figure.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.02)

    frames: list[Image.Image] = []
    for step in range(0, n_steps + 1, frame_step):
        mask = history[step]
        susceptible_scatter.set_offsets(np.column_stack([xs[~mask], ys[~mask]]))
        infected_scatter.set_offsets(np.column_stack([xs[mask], ys[mask]]))

        # Show transmission edges from the [step - frame_step + 1, step] window
        # so no transmission gets skipped when we subsample frames.
        window_start = max(0, step - frame_step + 1)
        active_indices = np.concatenate(
            [transmissions_per_step[i] for i in range(window_start, step + 1)]
        ) if step > 0 else np.empty(0, dtype=np.int64)
        if active_indices.size > 0:
            transmission_collection.set_segments(residual_segments[active_indices])
        else:
            transmission_collection.set_segments(np.empty((0, 2, 2)))

        title_artist.set_text(
            f"Harvard1   step {step}/{n_steps}    prevalence {float(mask.mean()):.1%}",
        )
        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", facecolor=figure.get_facecolor())
        buffer.seek(0)
        frames.append(Image.open(buffer).convert("P", palette=Image.Palette.ADAPTIVE))
    plt.close(figure)

    gif_buffer = io.BytesIO()
    frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=False,
        disposal=2,
    )
    return gif_buffer.getvalue()


# ---------------------------------------------------------------------------

st.set_page_config(page_title="Harvard1 SIS containment", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 3rem; padding-bottom: 0rem; max-width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

cache = load_harvard()
adjacency = cache["adjacency"]
edges = cache["edges"]
features = cache["features"]
costs = cache["sigmoid_dot_costs"]
lambda_1 = cache["lambda_1"]
n_nodes = int(adjacency.shape[0])

xs, ys = dorm_layout(b"_", n_nodes)
segments = edge_segments()
node_marker_sizes = np.full(n_nodes, 14.0)

KNOB_KEYS = ("R0", "gamma", "policy", "budget")
KNOB_LABELS = {"R0": "R₀", "gamma": "γ (recovery)", "policy": "Policy", "budget": "Budget"}
KNOB_DEFAULTS = {"R0": 3.0, "gamma": 0.10, "policy": "distance_threshold", "budget": 0.05}
for knob_key, default_value in KNOB_DEFAULTS.items():
    st.session_state.setdefault(f"knob_{knob_key}", default_value)
st.session_state.setdefault("active_knob", "R0")

with st.sidebar:
    st.header("Harvard: SIS containment")
    st.caption(
        f"{n_nodes:,} students randomly sampled from the 12 undergrad-house subgraph, with "
        f"{edges.shape[0]:,} contacts visible, grouped by dorm."
    )

    run_button = st.button("Run simulation", type="primary", use_container_width=True)

    # 2x2 grid of knob buttons. Click one to reveal its control underneath.
    grid_rows = (KNOB_KEYS[0:2], KNOB_KEYS[2:4])
    for row in grid_rows:
        columns = st.columns(2)
        for column, knob in zip(columns, row):
            is_active = st.session_state["active_knob"] == knob
            if column.button(
                ("● " if is_active else "") + KNOB_LABELS[knob],
                use_container_width=True,
                key=f"btn_{knob}",
                type="primary" if is_active else "secondary",
            ):
                st.session_state["active_knob"] = knob
                st.rerun()

    active = st.session_state["active_knob"]
    if active == "R0":
        st.slider(
            "Reproduction number R0", 0.5, 8.0,
            float(st.session_state["knob_R0"]), 0.1, key="knob_R0",
        )
    elif active == "gamma":
        st.slider(
            "Recovery rate gamma", 0.01, 0.5,
            float(st.session_state["knob_gamma"]), 0.01, key="knob_gamma",
        )
    elif active == "policy":
        st.selectbox(
            "Containment policy", POLICY_OPTIONS,
            index=POLICY_OPTIONS.index(st.session_state["knob_policy"]),
            format_func=lambda k: POLICY_LABELS[k], key="knob_policy",
        )
    elif active == "budget":
        st.slider(
            "Cost budget (fraction of total)", 0.0, 0.5,
            float(st.session_state["knob_budget"]), 0.005, key="knob_budget",
        )

R0 = float(st.session_state["knob_R0"])
gamma = float(st.session_state["knob_gamma"])
policy_name = st.session_state["knob_policy"]
budget_fraction = float(st.session_state["knob_budget"])
beta = R0 * gamma / lambda_1

if "history" not in st.session_state:
    st.session_state["history"] = None
    st.session_state["meta"] = None
    st.session_state["gif"] = None

if run_button:
    encoder = load_encoder_cached()
    if policy_name == "gnn" and encoder is None:
        st.error("No trained GNN encoder for Harvard1. Run `python scripts/03_train_gnn.py` first.")
    else:
        with st.spinner("Selecting edges to remove..."):
            policy = build_policy(policy_name, encoder, features)
            inputs = PolicyInput(
                adjacency=adjacency,
                edges=edges,
                costs=costs,
                budget=budget_fraction * float(costs.sum()),
                seed=SEED,
            )
            removed = (
                policy.select(inputs)
                if budget_fraction > 0
                else np.empty(0, dtype=np.int64)
            )
            residual = apply_removal(adjacency, edges, removed)
        with st.spinner("Running SIS simulation..."):
            residual_edges = edges_from_adjacency(residual)
            history, transmissions_per_step = simulate_history(
                residual, residual_edges,
                beta=beta, gamma=float(gamma),
                n_steps=N_STEPS, n_seeds=N_SEEDS, seed=SEED,
            )
            residual_segments = np.stack(
                [np.column_stack([xs[residual_edges[:, 0]], ys[residual_edges[:, 0]]]),
                 np.column_stack([xs[residual_edges[:, 1]], ys[residual_edges[:, 1]]])],
                axis=1,
            )
            if removed.size > 100000: # todo
                removed_pairs = edges[removed]
                removed_segments = np.stack(
                    [np.column_stack([xs[removed_pairs[:, 0]], ys[removed_pairs[:, 0]]]),
                     np.column_stack([xs[removed_pairs[:, 1]], ys[removed_pairs[:, 1]]])],
                    axis=1,
                )
            else:
                removed_segments = np.empty((0, 2, 2), dtype=np.float64)
        with st.spinner("Rendering animation..."):
            gif_bytes = build_animation_gif(
                history=history, xs=xs, ys=ys,
                residual_segments=residual_segments,
                removed_segments=removed_segments,
                transmissions_per_step=transmissions_per_step,
                sizes=node_marker_sizes, n_steps=N_STEPS,
            )
        st.session_state["history"] = history
        st.session_state["gif"] = gif_bytes
        st.session_state["meta"] = {
            "policy": policy_name, "R0": R0, "budget": budget_fraction,
            "n_removed": int(removed.size),
            "cost_used": float(costs[removed].sum()) if removed.size else 0.0,
            "recovery": gamma,
        }

history = st.session_state.get("history")
meta = st.session_state.get("meta")

gif_bytes = st.session_state.get("gif")
if gif_bytes is None:
    figure = render_frame(
        xs, ys, segments, node_marker_sizes,
        np.zeros(n_nodes, dtype=bool), 0, N_STEPS,
    )
    st.pyplot(figure, clear_figure=True, use_container_width=True)
    st.caption("Configure the sidebar and press **Run simulation** to start.")
else:
    st.markdown(
        f"{POLICY_LABELS[meta['policy']]} + R0={meta['R0']:.1f} + "
        f"budget={meta['budget']:.1%} + Recovery={meta['recovery']:.1f} + {meta['n_removed']:,} edges removed",
    )
    st.image(gif_bytes, use_container_width=True)
