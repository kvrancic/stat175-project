# Project Progress Log

A running log of what has been done, why, and what comes next. Updated on every commit.

## Format
Each entry: ISO date · commit short SHA · 1-2 line summary · why · what's next.

---

## 2026-04-26

**Initialized repo and scaffolded the project layout.**

- Why: locked the design with the team in the meeting on 2026-04-26 (see `docs/latest-meeting.txt` and `docs/Project Outline.txt`); converting Outline decisions into code.
- What's in: `pyproject.toml` with pinned scientific-Python + PyG + Streamlit stack; `src/stat175/{data,costs,sim,policies,models,eval,viz}` skeleton; `configs/`, `scripts/`, `notebooks/`, `paper/`, `webapp/`, `presentation/`; `.gitignore`; this log.
- Locked decisions (from `docs/Project Outline.txt`):
  - 5 campuses: Caltech36, Bowdoin47, Harvard1, Penn94, Tennessee95.
  - Primary epidemic: SIS (SIR as robustness check).
  - Cost: σ(⟨x_u, x_v⟩) on L2-normalized one-hot features.
  - 4 policies: Random, Edge betweenness, GNN-based, Distance Threshold.
  - Outcomes: steady-state prevalence (primary), peak prevalence (secondary).
- Data note: the team pre-staged 5 zip files under `data/` from networkrepository.com (.mtx adjacency-only). The Facebook100 node attributes (dorm/year/major/gender/status/high-school) live in the original Oxford `.mat` files at `archive.org/download/oxford-2005-facebook-matrix/facebook100.zip`. `scripts/01_download_data.py` fetches that archive (~206MB) and extracts only the 5 .mat files we need.
- What's next: write `scripts/01_download_data.py`, `src/stat175/data/facebook100.py`, `src/stat175/data/features.py`, `src/stat175/data/synthetic.py`. Verify Caltech36 loads end-to-end. Commit M1.

**M2 done — SIS/SIR simulator, 5 cost functions, threshold sanity passing.**

- Why: locked in the simulation substrate so all four policies plug into the same harness. Verified the SIS phase transition empirically before building anything that depends on it.
- What's in: `src/stat175/sim/sis.py` (vectorized stochastic SIS over sparse adjacency, returns mean ± 95% bootstrap CI of steady-state prevalence + peak + time-to-extinction); `src/stat175/sim/sir.py` (SIR robustness model, returns final-epidemic-size + peak); `src/stat175/costs/edge_costs.py` (sigmoid_dot primary, plus cosine, raw_dot, uniform, oracle_lognormal for ablation/robustness); `src/stat175/eval/metrics.py`; `configs/default.yaml` with the locked R0 grid {0.8, 1.5, 3.0, 6.0} and budget grid; `notebooks/00_threshold_sanity.py`; `scripts/02_build_features.py` (idempotent feature/edge/cost cache).
- Sanity numbers (results/summary/threshold_sanity.json): λ(A) ranges from 74.2 (Caltech36) to 247.4 (Harvard1); R0=0.8 dies out everywhere, R0=3.0 yields 22%–41% steady-state prevalence, R0=6.0 yields 44%–60%. Monotone and consistent with τ_c = 1/λ(A).
- What's next: M3 — implement the four Outline-locked policies (Random, Betweenness, Distance Threshold, GNN). The GNN policy is the novel contribution; train it with supervised regression on (random-edge-subset, simulated steady-state prevalence) pairs.

**M3 done — four Outline-locked policies, all four selecting cleanly at a 5% budget on Caltech36.**

- Why: the four policies are the per-comparison units of the project and need a single uniform interface so the harness in M4 can drive them with one loop.
- What's in: `src/stat175/policies/base.py` (Policy protocol + greedy_fill_by_score + apply_removal helper), `random_baseline.py`, `betweenness.py` (pivot-sampled edge betweenness ÷ cost), `distance_threshold.py` (Louvain-induced community-bubble cut, the realistic implementable form Austern endorsed). The GNN policy lives in `gnn_policy.py` and uses learned embeddings z_v from a self-supervised link-prediction encoder (`src/stat175/models/training.py`) to derive σ(⟨z_u, z_v⟩) as the cost, then ranks edges by NetMelt eigenscore u_i·u_j divided by that learned cost (Tong et al. 2012, anchor paper from useful-readings-A.md sec 3). GNN architectures (GraphSAGE, GAT, GCN) live behind a single GNNEncoder in `src/stat175/models/gnn.py` for the M5 architecture ablation.
- Decision (logged for the discussion section): chose self-supervised link prediction over training-by-simulation because (a) it trains in seconds without depending on the SIS simulator, (b) the link-prediction logit σ(⟨z_u, z_v⟩) is naturally interpretable as edge importance / removal cost, and (c) it is robust to simulation noise. The supervised-on-simulation variant remains a candidate for M5 ablation if the link-prediction version underperforms in the main experiment.
- Smoke numbers (Caltech36, 5% budget, R0=3, n_realizations=20): no-removal steady = 0.402; random = 0.386; betweenness = 0.380; distance_threshold = 0.383; GNN = 0.389. All four reduce prevalence relative to no-removal; betweenness leads at this single budget point. The full Pareto sweep in M4 will show whether method ranking is consistent across budgets and R0 regimes.
- What's next: M4 — write the Pareto evaluation harness, the figure-generating viz module, and `scripts/04_run_pareto.py`. Train one GNN per campus and persist the encoders. Run the full grid (5 campuses × 4 policies × 4 R0 values × 8 budget fractions × 50 realizations) to `results/main_pareto.parquet` and produce the central frontier plots.
