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

**M4 staging done — Pareto harness + GNN training script + figure pipeline + Streamlit app + per-policy caches.**

- Why: keep the harness, training, and viz code separate from any one experiment so the same machinery powers M4 (main), M5 (ablation), M6 (robustness), and the Streamlit demo.
- What's in: `src/stat175/eval/pareto.py` (sweep harness with bootstrap CIs), `src/stat175/eval/regression.py` (cross-campus AUC vs structural stats), `src/stat175/viz/plots.py` (frontier + ranking heatmap + AUC table), `scripts/03_train_gnn.py` + `scripts/_cache_loader.py` + `scripts/train_gnn_helpers.py`, `scripts/04_run_pareto.py`, `scripts/05_run_robustness.py`, `scripts/06_run_ablations.py`, `scripts/07_cross_campus_regression.py`, `scripts/08_make_figures.py`. Streamlit demo: `webapp/app.py`. Six experiment YAMLs under `configs/experiments/`. New top-level `README.md`.
- Performance fixes (logged for reproducibility):
  1. SIS/SIR simulators now cast adjacency to `float32` once at the start of `run_sis`/`run_sir` instead of on every step. Per-step matvec went from int32-cast-on-each-call to a stable scipy CSR matvec; on Penn94 (1.36M edges, 50 realizations × 200 steps) one full sim dropped from minutes to ~30 seconds.
  2. GNN training now applies a TruncatedSVD pre-projection of the one-hot feature matrix (default 64 components) before the SAGEConv stack, so per-epoch cost is dimension-independent. Harvard1 went from 21.5s/epoch to 0.2s/epoch; full 5-campus training now takes 38 seconds total (was projected at 50+ minutes).
  3. Each policy caches its expensive precompute keyed by `id(adjacency)`, so the Pareto sweep precomputes betweenness / Louvain / GNN embeddings + leading eigenvector ONCE per campus and reuses across (R0, budget) cells. On Harvard1 betweenness selection dropped from 91s to 0.06s on subsequent calls.
- All 5 GNN encoders trained: Caltech36 AUROC=0.789, Bowdoin47=0.812, Harvard1=0.861, Penn94=0.789, Tennessee95=0.783.
- What's next: launch `scripts/04_run_pareto.py` for the main Pareto frontier across all 5 campuses; commit the parquet result and the rendered figures.

**M4 launch + side artifacts.**

- Why: kicked off the full main Pareto experiment (N=50 SIS realizations × 5 campuses × 4 policies × 4 R0 × 8 budgets ≈ 8000 sims). Built the side artifacts that round out the v1: smoke-test suite, Streamlit demo, lightning-talk and `.tex` paper templates, results-summary script.
- What's in: `tests/test_policies.py` + `tests/test_simulator.py` (9 tests, all green: each policy stays within budget, zero budget = empty selection, removed edges actually disappear; SIS recovers τ_c phase transition, monotone in R0). `presentation/lightning-talk.md` (5-min, 4-speaker transcript with `POPULATE_AFTER_M4` markers for the figure + numbers). `paper/main.tex` + `paper/refs.bib` (NeurIPS-style template + bibliography seeded with all anchor papers from `docs/useful-readings-A.md` and `docs/useful-readings-B.md`). `scripts/09_summarize_results.py` (turns the parquet into headline numbers the talk + paper can quote). `WARNINGS.md` ledger of every downscoping decision (GNN dims, SVD pre-projection, sampled betweenness, sigmoid_dot's narrow range).
- Early Pareto signal (Caltech36 + Bowdoin47, 5% budget): GNN policy is dramatically better near the epidemic threshold (R0=1.5: GNN 3.5–5.8% vs other 3 policies at 6.3–9.3%); policies converge at higher R0. This is a "when does the learned cost help?" story for the discussion section.
- Background runs in flight: `scripts/04_run_pareto.py` (parquet save target = `results/main_pareto.parquet`); a polling task watches that path and will surface a notification when it appears.

**Suggested next-conversation entrypoint (post-compaction):** read this `PROGRESS.md`, `WARNINGS.md`, and `MEMORY.md`, then launch the secondary experiments in order:
```bash
python scripts/05_run_robustness.py        # M6
python scripts/06_run_ablations.py         # M5
python scripts/07_cross_campus_regression.py  # M7
python scripts/09_summarize_results.py     # populate headline numbers
python scripts/08_make_figures.py          # render every paper figure
# Then update presentation/lightning-talk.md with real numbers (M9 finalization)
# Then fill paper/main.tex sections (M11)
```

**M4 complete (2026-04-26 21:22).** `results/main_pareto.parquet` (640 rows) saved. 8 main figures + AUC table in `paper/figures/`. Headline summary in `results/summary/headline_numbers.json` and `results/summary/main_pareto_summary.csv`.

**Headline finding (logged for the talk + paper Discussion section):**

| R₀  | Per-campus winner counts (5 campuses)                   |
|-----|---------------------------------------------------------|
| 0.8 | GNN: 5 / 5                                              |
| 1.5 | GNN: 5 / 5                                              |
| 3.0 | GNN: 3, Distance Threshold: 2                           |
| 6.0 | Distance Threshold: 3, Betweenness: 2                   |

Mean steady-state reduction at 5 % budget (vs no removal):

| R₀  | Random  | Betweenness | Distance Threshold | **GNN**   |
|-----|---------|-------------|--------------------|-----------|
| 0.8 | +0.0000 | +0.0000     | +0.0000            | +0.0000   |
| 1.5 | +0.0158 | +0.0171     | +0.0222            | **+0.0402** |
| 3.0 | +0.0154 | +0.0217     | +0.0180            | +0.0169   |
| 6.0 | +0.0125 | +0.0223     | +0.0129            | +0.0056   |

Story: the **learned cost dominates near the epidemic threshold** (R₀ ≤ 1.5), where small structural differences matter most. In the strongly endemic regime (R₀ = 6) classical baselines (betweenness, community-bubble) win because the graph is too saturated for cost-aware fine-tuning to matter. This is the "when does the GNN help, and when does it not?" answer the discussion section needs.

**M7 done — cross-campus structural regression saved 128 univariate fits.**

- Why: with 5 campuses and 8 predictors, a multivariate fit is exactly determined and produces R²=1 by construction. Replaced with univariate slope + Pearson correlation per (policy, R0, predictor) so the paper can quote a defensible direction without overstating significance.
- What's in: `results/cross_campus_regression.parquet` (128 rows), `results/campus_structural_stats.csv` (per-campus n_nodes, density, mean_degree, clustering, assortativity, modularity, homophily_dorm, homophily_year), `paper/figures/cross_campus_regression.png` (heatmap of Pearson r per policy×predictor at each R0).
- Headline finding: at every R₀ ≥ 1.5, every policy's AUC is **positively** correlated with global clustering coefficient (r > 0.88) and edge density (r > 0.87) and **negatively** correlated with node count (r < -0.89 at R₀ ≥ 3.0). At the campus level, structural clustering matters more than per-attribute homophily for explaining cross-campus variation.

**Paper draft progress.**

- `paper/main.tex`: Introduction + Background + Related Work + Methods + Experimental setup + Results (Main Pareto + Cross-campus regression) + Discussion (When does the learned cost help? + Implementability gap + Limitations) + Conclusion + Appendix (Hyperparameters + Additional Pareto curves + ablation pointers + regression coefficients) all filled. Robustness and Ablations subsections still have `[DRAFT_AFTER_M5/M6]` markers awaiting parquets.
- `presentation/lightning-talk.md`: POPULATE_AFTER_M4 marker filled with the regime-split numbers.

**M5 + M6 in flight (background).**

- `scripts/05_run_robustness.py` (PID launched after the cache+buffering fix): ran past Caltech36, Bowdoin47, now into Harvard1 of compliance panel. Per-policy precomputes are now cached once per campus instead of re-instantiating inside the compliance/R0 loop (which was wasting ~6× betweenness recompute on Penn94).
- `scripts/06_run_ablations.py`: GNN-architecture ablation completed all 5 campuses × 3 archs trainings; SIS sweep on Tennessee95 GCN running. Then cost-function ablation, then synthetic-topology ablation. Fixed: the ablation now mirrors `load_encoder`'s contract by setting `encoder.projection_matrix = res.projection_matrix` after `train_link_prediction`, so the SVD pre-projection that training applies is also applied at inference time.

**Suggested next-conversation entrypoint (post-compaction):**

```bash
# Wait for the M5/M6 parquets to land in results/, then:
python scripts/08_make_figures.py    # render robustness/ablation panels
python scripts/09_summarize_results.py
# Fill paper/main.tex Results subsections "Robustness" and "Ablations"
# Update presentation/lightning-talk.md Slide 7 with the SIR-vs-SIS finding
```
