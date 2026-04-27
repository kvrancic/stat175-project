# STAT 175 — Cost-Constrained Edge Removal for Epidemic Containment

This is the repo for our STAT 175 final project (Karlo, Alec, Jackson, Ryan). We study the following question:

> Given a social contact graph in which vertices carry feature information and edges carry costs derived from endpoint feature similarity, what is the minimum-cost set of edges whose removal keeps steady-state SIS prevalence below a fixed threshold?

The full design rationale lives under `docs/`. The single source-of-truth spec is `docs/Project Outline.txt`; `docs/CENTRAL-KNOWLEDGE.md` is the long-form reference; `docs/short-brief.md` is the team's executive summary; `docs/useful-readings-A.md` and `docs/useful-readings-B.md` capture the prior-work landscape.

## Reproducing every result

```bash
# 1. Install (uv recommended; pip equivalent works too).
uv sync

# 2. Stage the Facebook100 .mat files (~206 MB; idempotent).
python scripts/01_download_data.py

# 3. Cache giant-component adjacency, one-hot features, and per-edge sigmoid_dot costs.
python scripts/02_build_features.py

# 4. Train one GraphSAGE encoder per campus (link-prediction objective).
python scripts/03_train_gnn.py

# 5. Run the main Pareto experiment (5 campuses x 4 policies x 4 R0 values x 8 budgets).
python scripts/04_run_pareto.py

# 6. Robustness panels: compliance, SIR, adversarial seeding.
python scripts/05_run_robustness.py

# 7. Ablations: GNN architecture, cost function, synthetic topology.
python scripts/06_run_ablations.py

# 8. Cross-campus structural regression of policy AUC on graph stats.
python scripts/07_cross_campus_regression.py

# 9. Regenerate every paper figure into paper/figures/.
python scripts/08_make_figures.py

# 10. Headline numbers JSON + per-policy AUC summary CSV (quoted by the paper + talk).
python scripts/09_summarize_results.py

# 11. Interactive demo.
streamlit run webapp/app.py
```

## Repository layout

| Path | Purpose |
| --- | --- |
| `docs/` | Locked spec (`Project Outline.txt`), long reference, brief, lit-review readings. |
| `src/stat175/data/` | Facebook100 loader, feature builder, synthetic-graph generators. |
| `src/stat175/sim/` | Stochastic SIS and SIR simulators on sparse adjacencies. |
| `src/stat175/costs/` | Per-edge cost functions (sigmoid_dot primary; cosine, raw_dot, uniform, oracle_lognormal for ablation). |
| `src/stat175/policies/` | The four Outline-locked policies behind a single `Policy` interface. |
| `src/stat175/models/` | GraphSAGE / GAT / GCN encoders + link-prediction trainer. |
| `src/stat175/eval/` | Pareto sweep, metrics, cross-campus regression. |
| `src/stat175/viz/` | Figure helpers used by the paper and the Streamlit app. |
| `scripts/` | The numbered drivers that produce every artifact in `results/` and `paper/figures/`. |
| `configs/experiments/` | One YAML per experiment; pinned seeds; no magic numbers in scripts. |
| `notebooks/` | Sanity-check scripts (run as plain Python: `python notebooks/00_threshold_sanity.py`). |
| `webapp/` | Streamlit interactive demo. |
| `paper/` | NeurIPS-style `.tex` paper and generated figures. |
| `presentation/` | 5-minute lightning-talk markdown transcript (4 speakers). |
| `PROGRESS.md` | Running log of work, updated on every commit. |

## Datasets

We use 5 Facebook100 campuses chosen for diversity in global clustering coefficient:
**Caltech36**, **Bowdoin47**, **Harvard1**, **Penn94**, **Tennessee95**.
The original `.mat` files (with node attributes) come from
[archive.org/details/oxford-2005-facebook-matrix](https://archive.org/details/oxford-2005-facebook-matrix);
the loader restricts each network to its giant connected component.

## License

Code released under MIT for academic use; the Facebook100 dataset retains its original terms (Traud, Mucha, Porter 2011).
