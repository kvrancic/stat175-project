# Known limitations and downscoping decisions

A running ledger of every place we traded off rigor for tractability. Each item lists what we did, why, and what a "future iteration with more compute / more time" should do instead. Update on every commit that introduces a tradeoff. Revisit before the lightning talk and again before the final `.tex` paper.

---

## GNN encoder

**What we did.** The link-prediction encoder uses:
1. A TruncatedSVD pre-projection of the one-hot feature matrix down to 64 dimensions before the GraphSAGE layers.
2. Reduced hidden_dim (32) and embed_dim (16) compared to the original plan (64 / 32).
3. 40 epochs (was 100).
4. A `max_train_pairs=200000` subsample of positive pairs per epoch on dense graphs.

**Why.** Training the original architecture on Harvard1 was 21.5 s/epoch (≈14 min total per campus), and Penn94 would have been ~30 min per campus. The whole 5-campus training would have taken ~75 minutes per re-run, which is too slow to iterate on locally during the sprint.

**What a better future iteration should do.**
- Run the original architecture (hidden_dim=64, embed_dim=32, 100 epochs, no SVD projection, full positive set) on a cluster (e.g. Harvard FASRC, a single A100, or Colab) and re-save the encoders. Local code path is unchanged; only the encoder weights get swapped in.
- Compare the SVD-projected vs full-feature variant directly in the architecture ablation (M5) so the report can quantify the cost of this approximation.
- Consider PyG's `NeighborSampler` for mini-batch training so the full feature set works without SVD.

## Edge betweenness centrality

**What we did.** Pivot-sampled betweenness with `k=300` random source nodes (`betweenness_pivots: 300` in `configs/experiments/main_pareto.yaml`).

**Why.** Exact betweenness on Penn94 (41 K nodes, 1.36 M edges) is O(VE) ≈ 5×10^10 operations — minutes-to-hours. Sampled betweenness with 300 pivots took ≈90 s on Harvard1 and is documented as a strong approximation in the network-science literature (Brandes 2008, Geisberger et al. 2008).

**What a better future iteration should do.**
- On a cluster, run exact edge betweenness for the smaller campuses (Caltech36, Bowdoin47) and compare ranking against the sampled estimator. Document the gap in the discussion section.
- For Penn94 / Tennessee95 the sampled estimator is the only viable option; quantify the variance of the score under different pivot draws (already partially handled by the seed pin).

## Distance Threshold policy

**What we did.** Implemented as a Louvain-induced community-bubble cut: partition the residual into communities, cut edges based on meta-graph hop distance.

**Why.** The Outline says "within X distance = remove" without specifying a distance metric. We chose meta-graph hop distance because it yields a natural budget knob (X) that is interpretable as "stay within bubble layers."

**Alternative future iterations should consider.**
- Direct k-hop graph distance from a small seed set of "central" nodes.
- Geographic distance (would require dorm-level coordinate data we do not have for Facebook100).
- Embedding distance (cosine distance in GNN-learned space), which would make the realistic policy itself learned.

## Cost function range

**Observation, not yet a fix.** With L2-normalized one-hot features and the sigmoid-dot proxy, observed costs lie in a narrow band: σ([0, 1]) ⊂ [0.5, 0.73]. The "bang-for-buck" division by cost in our policy scoring barely re-orders edges relative to the structural score because the divisor varies by at most ≈50 %.

**Implication.** Cost-aware policies and cost-blind policies are likely to give very similar selections under the primary cost. The cost-function ablation (M5, where we vary to `cosine` and `oracle_lognormal`) is essential for showing whether the GNN's contribution depends on having a cost with meaningful variance.

**Future iteration:** consider a cost transform that stretches the dynamic range, e.g. exp(α · ⟨x_u, x_v⟩) or rank-normalization, and document its effect.

## Simulation budget

**What we did.** N=50 stochastic SIS realizations per (campus × policy × R0 × budget) cell, n_steps=200, burn_in=100.

**Why.** Local CPU; 50 realizations is the standard practice for stable mean estimates on stochastic SIS.

**Future iteration:** push to N=200 on a cluster. Also explore longer `n_steps` for the larger campuses (Penn94 sometimes takes ~150 steps to reach steady state with low R0).

## Synthetic-topology ablation features

**What we did.** Synthetic graphs (ER, BA, WS, configuration model, SBM) have no Facebook100 attributes, so we substitute random 16-dim Gaussian features for the cost computation and skip the GNN policy on them.

**Why.** No real attributes means the GNN policy would be evaluating on noise, which is misleading. We test only Random, Betweenness, and Distance Threshold on synthetic graphs, focusing the ablation on whether the *structural* baselines are sensitive to topology.

**Future iteration:** generate synthetic graphs with planted block structure that mimics Facebook100 attribute-driven homophily, then re-include the GNN policy.

## Reproducibility caveats

- All seeds pinned to 42 by default. Random initial-infected sets, random negative pairs in GNN training, random pivot sampling in betweenness, and Louvain initialization all reroll deterministically off this seed.
- The Internet Archive download URL for Facebook100 is `https://archive.org/download/oxford-2005-facebook-matrix/facebook100.zip`. If that mirror disappears, the same files are mirrored at `networkrepository.com/socfb.php` (but only as `.mtx` adjacency, with no node attributes).
