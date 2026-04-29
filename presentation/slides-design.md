# Lightning Talk Slide Design — Visual Spec

A slide-by-slide description of how the deck **looks**. The transcript in `lightning-talk.md` is the spoken track; this deck is its supporting layer. The slides do not echo the transcript verbatim, but they do carry real content — definitions, equations, citations, captions, and the figures from `paper/figures/`. The audience should be able to glance at a slide and pick up something the speaker isn't currently saying out loud.

Designed for a fast click-through cadence (~13-18 seconds per slide on average across 22 slides for a 5-minute talk). Several slides are short interstitials; the figure-driven slides earn an extra beat.

---

## Global design system

**Aspect ratio.** 16:9, 1920×1080 master.

**Palette.**
- **Ink** `#0B1020` — primary background; near-black with a faint blue cast.
- **Paper** `#F4F1EA` — off-white text.
- **Coral** `#FF5A4E` — primary accent; the GNN curve, headline metrics, the "above threshold" zone.
- **Mint** `#7FE7B5` — secondary accent; the "below threshold / contained" zone, distance-threshold curve.
- **Slate** `#3A4256` — muted grey-blue; axis labels, baselines, betweenness curve.
- **Mist** `#9FA8B8` — tertiary; random baseline curve, footnotes, captions.

**Typography.**
- Display: **Inter Tight** 700/900 for slide titles.
- Body: **Inter** 400/500.
- Monospace / equations: **JetBrains Mono** with KaTeX-quality math typesetting.
- Body text size 22-28 pt; titles 36-48 pt.

**Recurring chrome (kept light).**
- Bottom-right speaker tag: `KARLO` / `ALEC` / `JACKSON` / `RYAN` in JetBrains Mono 14 pt, Coral, 60% opacity. The handoff slides change it explicitly.
- Bottom-left slide number: `13 / 22` in JetBrains Mono 14 pt, Slate.
- Top-right: project shorthand in Mist 12 pt: `STAT 175 · cost-aware edge removal`.
- A 1 px coral hairline along the bottom 4% of every slide separates chrome from content.

**Transitions.** Slide-to-slide: 220 ms horizontal wipe with cubic-bezier `(0.22, 0.61, 0.36, 1)`. Within-slide builds: 180 ms fade-up + 8 px translate.

**Pacing convention.**
- Title slides and section dividers: 6-10 seconds.
- Content slides with definitions / equations: 12-18 seconds.
- Figure slides: 18-25 seconds (the audience needs time to read the plot).

---

## Figure assets index (use these — they already exist)

All figures below are pre-rendered in `paper/figures/`. Every relevant slide has an explicit `[PLACEHOLDER → <path>]` marker indicating which file to drop in. **Do not regenerate these — they are produced by `scripts/08_make_figures.py` from the locked seeds.**

| File | Used on slide |
|---|---|
| `paper/figures/main_pareto_R0_0.8.png` | Slide 14 (subcritical regime, optional inset) |
| `paper/figures/main_pareto_R0_1.5.png` | **Slide 13 (HEADLINE)** |
| `paper/figures/main_pareto_R0_3.0.png` | Slide 14 (panel B) |
| `paper/figures/main_pareto_R0_6.0.png` | Slide 14 (panel C — flip) |
| `paper/figures/main_ranking_R0_1.5.png` | Slide 15 |
| `paper/figures/main_ranking_R0_3.0.png` | Slide 15 (alternate) |
| `paper/figures/robustness_compliance_R0_1.5.png` | Slide 16 |
| `paper/figures/robustness_sir_R0_1.5.png` | Slide 17 (left) |
| `paper/figures/robustness_adversarial_seed_R0_1.5.png` | Slide 17 (right) |
| `paper/figures/ablation_gnn_arch_R0_3.0.png` | Slide 18 |
| `paper/figures/ablation_cost_function_R0_3.0.png` | Slide 19 |
| `paper/figures/ablation_synthetic_topology_R0_3.0.png` | Slide 20 (optional) |
| `paper/figures/cross_campus_regression.png` | Slide 20 |

Numerical figures cited inline (already in `results/summary/headline_numbers.json`):
- GNN @ R₀=1.5, 5% budget: prevalence reduction of **+0.0402** (4.0 pp).
- Distance Threshold @ same: **+0.0222** (2.2 pp).
- Edge Betweenness @ same: **+0.0171** (1.7 pp).
- Random baseline @ same: **+0.0158** (1.6 pp).

The web-app screenshot for Slide 21 does **not yet exist**: take a fresh capture of `webapp/app.py` running locally with `R₀ = 1.5`, `Budget = 5%`, `Caltech36`, GNN policy selected; save as `presentation/assets/webapp_screenshot.png`.

---

## Slide 1 — Title

**Speaker:** Karlo (~10 s)

**Layout.** Full-bleed Ink background. Left half: a slow-rotating force-directed visualization of Caltech36 at 30% opacity, edges in Mist. Right half: vertically centered text block.

**Content.**
- Pre-title in Coral, all caps, letter-spaced 0.18em: `STAT 175 · FINAL PROJECT · SPRING 2026`
- Title in Paper, Inter Tight 900, 72 pt, two lines:
  > Cost-Constrained Edge Removal
  > for Epidemic Containment
- Subtitle in Mist, Inter 400 italic, 26 pt:
  > Learning the cost of breaking a friendship.
- Author block, 22 pt, Paper at 80% opacity, two columns:
  > Karlo Vrančić &nbsp; Alec [Lastname]
  > Jackson [Lastname] &nbsp; Ryan [Lastname]
- Footer, JetBrains Mono 16 pt, Slate: `UC Berkeley · Prof. Austern · 28 April 2026`

**Background graphic.** The rotating Caltech36 visualization is real — produced by `pyvis` over `data/processed/Caltech36.npz`. Render once, embed as PNG.

---

## Slide 2 — Why edge removal

**Speaker:** Karlo (~14 s)

**Layout.** Left: a short bulleted list. Right: a small table mapping policy → real-world counterpart.

**Left.** Title `WHAT INTERVENTIONS LOOK LIKE`, Inter Tight 700, 32 pt, Paper. Body, Inter 400, 22 pt, Mist for the lead-in / Paper for the items:

> Public-health interventions don't remove people. They restrict who can meet whom:
> - school closures
> - dorm reassignments
> - contact-tracing isolation
> - travel restrictions
> - gathering size limits

**Right.** A compact 3-column table, Inter 500, 18 pt, with Slate hairlines:

| Real intervention | Edge-set affected | Cost |
|---|---|---|
| Dorm reassignment | within-dorm ties | high |
| Class cancellation | classmate ties | medium |
| Travel ban | between-campus ties | depends on connectivity |
| Quarantine cluster | one node's full neighborhood | very high |

**Caption below the table**, Mist 14 pt: `The cost depends on which ties are broken — that's the framing this project starts from.`

---

## Slide 3 — The formal problem

**Speaker:** Karlo → handoff to Alec (~14 s)

**Layout.** Centered formal optimization problem, with annotations to the side.

**Center.** A boxed equation block, JetBrains Mono 28 pt, Paper:

```
minimize    Σ  c(e)
            e ∈ E_cut

subject to  prevalence_∞( G \ E_cut ) ≤ θ
            E_cut ⊆ E
```

**Right-side annotations**, Mist 16 pt, with thin Slate leader lines:
- `c(e) = σ(⟨x_u, x_v⟩)` — the cost proxy, defined on Slide 7.
- `prevalence_∞` — steady-state SIS infected fraction.
- `θ` — the public-health tolerance.
- `G \ E_cut` — the residual graph after cuts.

**Bottom caption**, Mist 14 pt: `Equivalently: a cost-weighted variant of the immunization problem (Tong et al. 2012; Saha et al. 2015).`

**Why this slide exists.** The transcript stays informal at this point; the slide gives the audience the formal version so technical viewers can lock in.

---

## Slide 4 — Five campuses

**Speaker:** Alec (handoff arrives here, ~10 s)

**Layout.** A 5-column comparison table, with each campus as a vertical card.

**Top of each card** (Inter Tight 700, 24 pt, Paper):
- `Caltech36`
- `Bowdoin47`
- `Harvard1`
- `Penn94`
- `Tennessee95`

**Each card body** (Inter 400, 16 pt, four rows, Mist labels / Paper values):
- `n =` (giant component size)
- `m =` (giant component edges)
- `clustering =` (global clustering coefficient)
- `λ_1 =` (leading eigenvalue)

> Approximate values from `results/summary/threshold_sanity.json` — fill in when generating the deck. Caltech36 ≈ 762 nodes; Penn94 ≈ 41 000 nodes. Clustering range ≈ 0.13–0.26.

**Bottom caption**, Mist 14 pt:
> Five Facebook100 campuses, chosen for diversity in global clustering coefficient. Loaded from the `.mat` files at archive.org/details/oxford-2005-facebook-matrix and restricted to the giant component. Node attributes: dorm, year, major, gender, status, high school.

---

## Slide 5 — SIS dynamics

**Speaker:** Alec (~14 s)

**Layout.** Left: SIS compartment diagram. Right: a short definition block.

**Left.** Two large rounded squares — `S` (Mint) and `I` (Coral) — with two arrows:
- S → I labeled `β · (# infected neighbors)`
- I → S labeled `γ`

A small marker dot animates slowly between the two states while the slide is on screen.

**Right.** Title `SUSCEPTIBLE → INFECTED → SUSCEPTIBLE`, Inter Tight 700, 22 pt, Paper. Body, Inter 400, 20 pt:

> Each step (discrete time):
> - infected → susceptible w.p. γ
> - susceptible → infected w.p. 1 − (1 − β)^k
>   where k = # infected neighbors

> Why SIS, not SIR:
> - mimics endemic respiratory diseases without permanent immunity
> - admits a non-trivial steady-state (the primary outcome)

**Bottom caption**, Mist 14 pt: `Pastor-Satorras & Vespignani (2001); implementation in src/stat175/sim/sis.py.`

---

## Slide 6 — The spectral threshold

**Speaker:** Alec (~16 s)

**Layout.** Left: the canonical phase-transition plot. Right: equation + intuition.

**Left.** A clean illustrative plot, hand-drawn quality:
- X-axis: `R₀ = β · λ₁(A) / γ`, ticks at 0.5, 1, 2, 4.
- Y-axis: `steady-state prevalence`, 0 to 0.6.
- A sigmoidal curve crossing zero around R₀ = 1.
- Vertical dashed Slate line at `R₀ = 1`, labeled `τ_c`.
- Mint shading left of `τ_c`, Coral shading right.
- Floating labels: `dies out` (mint), `endemic` (coral).
- A small Coral pin marker on the curve at R₀ ≈ 1.5 — labeled `our headline R₀`.

> Generate this from `results/summary/threshold_sanity.json` if a real version is preferred over an illustration; otherwise use a hand-drawn schematic.

**Right.** Title `EPIDEMIC THRESHOLD`, Inter Tight 700, 28 pt, Paper. Body, JetBrains Mono 32 pt for the equation:

> τ_c = 1 / λ₁(A)

Below the equation, Inter 400, 20 pt:

> The SIS process dies out iff β/γ < τ_c.
> Cutting edges shrinks λ₁(A), which raises τ_c, which pushes the system toward the contained regime.

**Bottom caption**, Mist 14 pt: `Wang, Chakrabarti, Wang & Faloutsos (2003).`

**R₀ values we sweep:** `0.8, 1.5, 3.0, 6.0` — listed in a small JetBrains Mono 16 pt strip below the equation. The 1.5 value is highlighted in Coral.

---

## Slide 7 — Cost function

**Speaker:** Alec (~16 s)

**Layout.** Left: equation + feature list. Right: a small worked example.

**Left.** Title `COST = SIMILARITY`, Inter Tight 700, 28 pt, Paper.

Equation block, JetBrains Mono 28 pt:

> c(u, v) = σ( ⟨x_u, x_v⟩ )

Below it, Inter 400, 20 pt:

> Each node carries a one-hot feature vector over six attributes (`dorm, year, major, gender, status, high-school`). Vectors are L2-normalized. Missing values are their own category.

**Right.** A worked example in two stacked rows:

Row 1 — `Alice` and `Bob`, both freshmen in Adams Hall majoring in CS:
- Their feature vectors share 4 of 6 hot indices.
- `⟨x_Alice, x_Bob⟩ ≈ 0.67`
- `c = σ(0.67) ≈ 0.66` — **expensive edge** (Coral).

Row 2 — `Alice` and `Carol`, freshman vs senior, different dorm, different major:
- Their feature vectors share 0 of 6 hot indices.
- `⟨x_Alice, x_Carol⟩ ≈ 0.0`
- `c = σ(0.0) = 0.50` — **cheaper edge** (Mint).

**Bottom caption**, Mist 14 pt:
> Observed cost band on real Facebook100 features: `c ∈ [0.50, 0.73]`. The narrow range is documented in `WARNINGS.md` and motivates the cost-function ablation (Slide 19).

---

## Slide 8 — The four policies

**Speaker:** Jackson (~12 s)

**Layout.** A 2×2 grid of cards, each 660×320, with a one-sentence description.

**Cards** (Inter Tight 700, 26 pt for the title; Inter 400, 18 pt for the body):

| | |
|---|---|
| **1. Random** *(baseline)* | Pick edges uniformly until budget exhausted. The floor every other policy must beat. |
| **2. Edge betweenness / cost** *(classical)* | Rank edges by `betweenness(e) / c(e)`, greedy fill. NetworkX with `k=300` pivot sampling on Penn94 / Tennessee95 (Brandes 2008). |
| **3. Distance Threshold** *(realistic)* | Louvain communities → meta-graph → cut edges between communities at hop-distance > X. The "stay in your bubble" policy. |
| **4. GNN policy** *(novel)* | 2-layer GraphSAGE → 16-dim embeddings → cost = σ(⟨z_u, z_v⟩) → score = NetMelt eigenscore / cost. |

The fourth card has a Coral border (1.5 px) to flag it as the novel contribution. The other three have a thin Slate border (1 px).

**Bottom caption**, Mist 14 pt: `All four implement the same Policy interface in src/stat175/policies/. Locked by Project Outline §3.`

---

## Slide 9 — Random and Betweenness

**Speaker:** Jackson (~14 s)

**Layout.** Two equal columns, each with a label, a one-line definition, and a tiny cartoon graph.

**Left — Random.**
- Title `RANDOM`, Inter Tight 700, 28 pt, Slate.
- Definition, Inter 400, 18 pt:
  > Sample edges uniformly without replacement until cumulative cost reaches the budget.
- Why include it:
  > Bounds the "do nothing intelligent" baseline. Any cost-aware method should clear it.
- Tiny illustration: 30-node graph, 8 random edges crossed out.

**Right — Edge Betweenness.**
- Title `EDGE BETWEENNESS / COST`, Inter Tight 700, 28 pt, Slate.
- Definition, Inter 400, 18 pt:
  > For each edge `e`, compute `betweenness(e)` (fraction of shortest paths through `e`). Score = `betweenness(e) / c(e)`. Greedy by score.
- Notes:
  > k=300 pivot sampling on the two largest campuses (~5×10¹⁰ ops at exact). Documented in `WARNINGS.md`.
- Tiny illustration: same 30-node graph, the 4 highest-betweenness bridges highlighted Coral.

**Bottom caption**, Mist 14 pt: `Bang-for-buck framing: if a structural bottleneck is also socially cheap, cut it first.`

---

## Slide 10 — Distance Threshold (the "realistic" one)

**Speaker:** Jackson (~16 s)

**Layout.** Left: visualization of the policy. Right: explanation.

**Left.** A 50-node graph, partitioned into 4 community bubbles via Louvain (each bubble shaded a different muted color). Edges within bubbles are kept (Mist). Cross-bubble edges are colored by meta-graph hop distance:
- `d = 1` (adjacent bubbles): Slate, kept.
- `d ≥ 2`: Coral, marked for removal.

A small legend in the corner: `bubble distance`.

**Right.** Title `DISTANCE THRESHOLD`, Inter Tight 700, 28 pt, Paper. Body, Inter 400, 20 pt:

> Step 1. Run Louvain on the residual graph → community labels.
> Step 2. Build the meta-graph (one node per community).
> Step 3. For threshold X, cut edges (u, v) with `d_meta(c_u, c_v) > X`.
> Step 4. X is the budget knob — sweep it.

> **Why this is the policy a government can actually run.** It maps to "you're allowed to interact within your dorm-and-class bubble; not across bubbles." No per-edge optimization; just one threshold.

**Bottom caption**, Mist 14 pt: `Implemented in src/stat175/policies/distance_threshold.py.`

---

## Slide 11 — The GNN pipeline

**Speaker:** Jackson (~22 s)

**Layout.** Centered architecture diagram, top half. Bottom half: training objective + score function.

**Top half — pipeline diagram.** Five horizontal stages with arrows:

```
[ X ∈ R^{n × 598} ]  →  [ TruncatedSVD → R^{n × 64} ]  →  [ SAGE × 2 layers ]  →  [ z ∈ R^{n × 16} ]  →  [ c(u,v) = σ(⟨z_u, z_v⟩) ]
```

Each stage is a rounded rectangle, 1 px Mist border. The middle stage `SAGE × 2 layers` is filled with Coral at 8% alpha to indicate the learned component.

Annotations in JetBrains Mono 14 pt below specific stages:
- Below `TruncatedSVD`: `(speed-up; documented in WARNINGS.md)`.
- Below `SAGE × 2`: `hidden_dim=32, embed_dim=16, dropout=0.5`.
- Below `cost`: `analogous to the hand-designed σ(⟨x_u, x_v⟩)`.

**Bottom half.** Two side-by-side panels.

*Left — Training objective:*

> **Self-supervised link prediction.**
> - positive pairs = real edges
> - negative pairs = sampled non-edges
> - loss = BCE on `σ(⟨z_u, z_v⟩)`
> - 40 epochs, Adam, lr = 1e-3
> - per-campus encoder; ≈ 14 minutes per campus locally

*Right — Edge score:*

> **NetMelt eigenscore (Tong et al. 2012):**
> `score(e) = (u_i · v_j + u_j · v_i) / c(u, v)`
> where `u, v` are the leading eigenvectors of the adjacency.
> Greedy fill until budget exhausted.

**Bottom caption**, Mist 14 pt: `Implemented in src/stat175/models/gnn.py + src/stat175/policies/gnn_policy.py.`

---

## Slide 12 — What's actually novel

**Speaker:** Jackson → handoff to Ryan (~12 s)

**Layout.** Two columns separated by a thin Coral hairline.

**Left — Hand-designed cost.**
- JetBrains Mono 22 pt: `c(u, v) = σ(⟨x_u, x_v⟩)`
- Inter 400, 18 pt:
  > Same dorm? Same major? Probably close. Encoded by hand from the feature schema.

**Right — Learned cost.**
- JetBrains Mono 22 pt: `c(u, v) = σ(⟨z_u, z_v⟩)`
- Inter 400, 18 pt:
  > Embedding similarity learned from local neighborhoods. Captures shared neighbors, second-order ties, structural roles — properties no hand-designed feature combination expresses.

**Bottom strip**, full-width, Coral 24 pt centered:
> The cost function itself is what's learned end-to-end. The architecture is a means.

---

## Slide 13 — Headline result

**Speaker:** Ryan (~22 s)

**Layout.** Single Pareto frontier figure, 80% slide width, centered. Headline numbers in a sidebar to the right.

**Center.**

> **[PLACEHOLDER → `paper/figures/main_pareto_R0_1.5.png`]**

Caption below the figure, Mist 14 pt:
> Cost budget vs steady-state SIS prevalence at R₀ = 1.5. Mean over 50 stochastic realizations per cell, 95% bootstrap CIs. Five campuses pooled.

**Sidebar (right).** Title `AT 5% BUDGET`, Inter Tight 700, 22 pt, Paper. Then a 4-row stack:
- `GNN`: **−4.0 pp** (Coral, bold)
- `Distance`: −2.2 pp (Mint)
- `Betweenness`: −1.7 pp (Slate)
- `Random`: −1.6 pp (Mist)

**Top-left badge**, Inter Tight 700, 22 pt, Coral: `R₀ = 1.5 — near the threshold`.

---

## Slide 14 — How it depends on R₀

**Speaker:** Ryan (~22 s)

**Layout.** Three Pareto plots arranged horizontally — sub-critical, near-threshold (recap), endemic — to show the regime sweep.

**Three panels** (33% slide width each):

**Panel A — R₀ = 0.8 (sub-critical)**
> **[PLACEHOLDER → `paper/figures/main_pareto_R0_0.8.png`]**
> Caption: `Below threshold; all policies converge to ≈ 0 quickly.`

**Panel B — R₀ = 3.0 (super-critical, mid)**
> **[PLACEHOLDER → `paper/figures/main_pareto_R0_3.0.png`]**
> Caption: `GNN advantage shrinks as the regime deepens.`

**Panel C — R₀ = 6.0 (heavily endemic)**
> **[PLACEHOLDER → `paper/figures/main_pareto_R0_6.0.png`]**
> Caption: `Distance Threshold and Betweenness now match or beat GNN.`

**Top banner**, full slide width, Inter 400, 20 pt, Paper:
> **The picture flips with regime.** Cost-aware learning helps most where the disease is barely sustaining itself; brute-force structural cuts dominate when every path is overflowing.

---

## Slide 15 — Per-campus ranking

**Speaker:** Ryan (~14 s)

**Layout.** A heatmap of policy rankings across campuses, plus a small AUC summary table to its right.

**Center.**

> **[PLACEHOLDER → `paper/figures/main_ranking_R0_1.5.png`]**

Caption: `Ranking of policies (1 = best, 4 = worst) at each campus, R₀ = 1.5. GNN wins 5/5 at this regime.`

**Right.** A compact 5×4 AUC table (rows = campus, cols = policy), values from `results/summary/auc_by_policy_campus.csv`. Coral cell highlight on the per-row max.

**Bottom caption**, Mist 14 pt:
> AUC = area under the prevalence-vs-budget curve, lower is better (less infected per dollar spent).

---

## Slide 16 — Robustness: imperfect compliance

**Speaker:** Ryan (~14 s)

**Layout.** Single figure on the left, takeaway block on the right.

**Left.**

> **[PLACEHOLDER → `paper/figures/robustness_compliance_R0_1.5.png`]**

Caption, Mist 14 pt: `Steady-state prevalence vs budget, with 0% / 20% / 40% / 60% non-compliance. R₀ = 1.5.`

**Right.** Title `IF EVERYONE ONLY HALF-LISTENS`, Inter Tight 700, 26 pt, Paper. Body, Inter 400, 20 pt:

> - Each "removed" edge is independently un-removed with probability `p` before simulation.
> - GNN at **60% compliance** still beats every other policy at **100% compliance**, in the near-threshold regime.
> - The cost-aware ranking is robust to the dominant real-world failure mode.

**Bottom caption**, Mist 14 pt: `Setup follows Project Outline §4. Implementation in scripts/05_run_robustness.py.`

---

## Slide 17 — Robustness: SIR + adversarial seeding

**Speaker:** Ryan (~16 s)

**Layout.** Two figures side by side, each with a one-sentence takeaway underneath.

**Left panel — SIR.**

> **[PLACEHOLDER → `paper/figures/robustness_sir_R0_1.5.png`]**

Title above: `SIR model`, Inter Tight 700, 22 pt, Paper.
Takeaway, Inter 400, 18 pt:
> Same regime split as SIS, slightly sharper. The qualitative ranking is not an artifact of choosing SIS.

**Right panel — Adversarial seeding.**

> **[PLACEHOLDER → `paper/figures/robustness_adversarial_seed_R0_1.5.png`]**

Title above: `Adversarial seeding`, Inter Tight 700, 22 pt, Paper.
Takeaway, Inter 400, 18 pt:
> Initial infections placed at the top eigenvector-component nodes (worst case). GNN policy now wins **both** regimes — including R₀ = 6 where it had been third under random seeding.

**Bottom caption**, Mist 14 pt: `Reduced simulation budget on these panels (n_realizations = 20) is documented in WARNINGS.md.`

---

## Slide 18 — Ablation: GNN architecture

**Speaker:** Ryan (~12 s)

**Layout.** Single figure on the left, single sentence finding on the right.

**Left.**

> **[PLACEHOLDER → `paper/figures/ablation_gnn_arch_R0_3.0.png`]**

Caption, Mist 14 pt: `Pareto frontiers for the GNN policy with three encoder choices, R₀ = 3.0. Curves are statistically indistinguishable.`

**Right.** Title `THE FRAMEWORK, NOT THE OPERATOR`, Inter Tight 700, 28 pt, Paper. Body, Inter 400, 22 pt:

> GraphSAGE, GAT, and GCN produce the same downstream Pareto frontier (within bootstrap CI).
>
> What's load-bearing is the **end-to-end cost-learning pipeline** — link-prediction objective + spectral selector — not the message-passing operator. Architecture choice is largely arbitrary.

---

## Slide 19 — Ablation: cost function

**Speaker:** Ryan (~14 s)

**Layout.** Single figure with annotations.

**Left.**

> **[PLACEHOLDER → `paper/figures/ablation_cost_function_R0_3.0.png`]**

Caption, Mist 14 pt: `Pareto frontiers under five cost functions: sigmoid_dot (primary), cosine, raw_dot, uniform, oracle_lognormal.`

**Right.** Title `WHERE THE GNN ADVANTAGE COMES FROM`, Inter Tight 700, 24 pt, Paper. Body, Inter 400, 18 pt:

> - `uniform` cost — every edge costs the same — shows what's left of each policy when cost is removed from the picture.
> - `oracle_lognormal` — a cost with high dynamic range — the GNN advantage **widens**.
> - `sigmoid_dot` (the primary) — the GNN advantage exists but is bounded by the narrow `[0.50, 0.73]` cost band documented in `WARNINGS.md`.
> - **Implication:** the cost-aware framing depends on cost having meaningful variance. A dataset with richer features would amplify the result.

---

## Slide 20 — Cross-campus regression

**Speaker:** Ryan (~12 s)

**Layout.** Single figure with a short methods footnote.

**Center.**

> **[PLACEHOLDER → `paper/figures/cross_campus_regression.png`]**

Caption, Mist 14 pt:
> Pearson correlation between policy AUC and eight descriptive graph statistics, faceted by R₀ and policy. Five campuses; univariate per cell.

**Bottom block.** Title `WHEN DOES THE GNN WIN?`, Inter Tight 700, 22 pt, Paper. Body, Inter 400, 18 pt:

> - **Not enough campuses (n=5) to do honest multivariate inference** — a multivariate fit on 8 predictors is exactly determined.
> - Univariate slopes still tell a directional story: GNN advantage **grows** with global clustering, **shrinks** with degree assortativity.
> - Loading 10 more campuses would push n to 15 and unlock a 4-predictor multivariate fit. The Facebook100 loader supports it; only `data/processed/<name>.npz` caches need to be regenerated.

> Optional swap: **[PLACEHOLDER → `paper/figures/ablation_synthetic_topology_R0_3.0.png`]** — Pareto under ER, BA, WS, configuration model, SBM topologies. Use if there's a question about "is this Facebook100-specific?"

---

## Slide 21 — Honest limitations

**Speaker:** Ryan (~14 s)

**Layout.** Two columns, each a short bulleted list. Single Coral closing line at the bottom.

**Left — What we are not solving.**
- **Friendship ≠ contact.** Facebook100 is a stable friendship graph; epidemics spread on transient contact graphs. Edge weights here are correlates of contact frequency, not contact frequency itself.
- **SIS is a simplification.** Real respiratory pathogens have latency, age structure, behavior change.
- **Cost is a proxy.** σ(⟨x, x⟩) is a stand-in for "social distance"; we don't claim it equals the dollar cost of a school closure.

**Right — Where we cut corners.**
- Reduced GNN encoder (TruncatedSVD pre-projection, hidden_dim=32, embed_dim=16, 40 epochs) for local-laptop tractability. Documented in `WARNINGS.md`. Full-fidelity Colab/A100 retraining script in `notebooks/01_colab_train_full_gnn.py`.
- Sampled betweenness with `k=300` pivots on Penn94 / Tennessee95.
- Three robustness/ablation panels run at `n_realizations = 20` instead of 50 (also in `WARNINGS.md`).

**Bottom strip**, Coral 24 pt:
> The contribution is the **framing** — that cost-awareness reorders policy rankings — not a deployable COVID intervention.

---

## Slide 22 — Web app teaser

**Speaker:** Ryan (~12 s)

**Layout.** Annotated screenshot of the Streamlit app.

**Center.**

> **[PLACEHOLDER → `presentation/assets/webapp_screenshot.png`]** — does not yet exist. Capture by running `uv run streamlit run webapp/app.py`, set `R₀ = 1.5`, `Budget = 5%`, `Caltech36`, GNN policy. Save the full-window PNG.

Coral arrows with annotations point to:
- **Sidebar controls** → "campus, R₀, budget, policy, cost function — all live."
- **Animated SIS curve** → "per-step prevalence on the residual graph."
- **Network panel** (pyvis) → "removed edges greyed out; nodes sized by infection probability."
- **Pareto frontier** → "selected campus, all four policies, your current point marked."

**Right sidebar — feature list**, Inter 400, 18 pt:
> - Five campuses pre-loaded.
> - Switch between SIS and SIR.
> - Compare policies side-by-side in the comparison tab.
> - Built with Streamlit + pyvis. Runs locally on a laptop. No GPU required for inference.

**Bottom caption**, Mist 14 pt: `Source in webapp/app.py.`

---

## Slide 23 — Live demo (interstitial)

**Speaker:** Ryan (~30 s if live, ≤ 4 s if skipped)

**Layout.** Full-bleed Coral panel. Centered, Inter Tight 900, 200 pt, Ink:

> **DEMO**

Below in JetBrains Mono 24 pt, Ink: `→ webapp/app.py`

That's it. The presenter alt-tabs to Streamlit during this slide and runs through one (campus × policy × budget) configuration end-to-end.

If the live demo fails or gets skipped, this slide is on screen for under 4 seconds and the deck moves to Slide 24.

---

## Slide 24 — Closing

**Speaker:** Ryan (~10 s)

**Layout.** Mirror of the title slide, simplified.

**Content.**
- Pre-title in Coral, all caps, letter-spaced 0.18em: `THANK YOU`
- Title, Paper, Inter Tight 900, 56 pt:
  > Questions?
- Below, in Mist 22 pt:
  > Code, paper draft, all figures: in the project repo.
  > Reproduce the headline plot: `python scripts/04_run_pareto.py && python scripts/08_make_figures.py`.
- Authors, Mist 18 pt, single line:
  > Karlo Vrančić · Alec [Lastname] · Jackson [Lastname] · Ryan [Lastname]
- Acknowledgement, Mist 14 pt:
  > With thanks to Prof. Austern for the cost-function framing and the Track 1 latitude.

Background: the same rotating Caltech36 visualization from Slide 1, at 30% opacity. (Same render — no need to regenerate.)

---

## Speaker handoff cheat-sheet

| Slide | Speaker | Notes |
|---|---|---|
| 1-3 | **Karlo** | Title, motivation, formal problem. End on slide 3 with "Alec, take it from the math." |
| 4-7 | **Alec** | Campuses, SIS, threshold, cost. End on slide 7 with "Jackson, what do we actually do with this?" |
| 8-12 | **Jackson** | Four policies + GNN pipeline + novelty. End on slide 12 with "Ryan, results." |
| 13-24 | **Ryan** | Headline + regime sweep + robustness + ablations + limitations + demo + close. |

The bottom-right speaker tag updates per slide so the audience always knows who's talking.

---

## Easter eggs (kept short and tasteful)

A handful, not a parade:
- **Slide 6** — the Coral pin marker on the phase-transition curve sits exactly at R₀ = 1.5, which is the headline regime on Slide 13. Quiet visual call-forward.
- **Slide 8** — the GNN card has a Coral border; the others have Slate. Communicates "this is the novel one" without saying it.
- **Slide 13** — the Coral GNN curve has a soft glow. **Slide 14**, panel C — the glow has migrated to the Distance Threshold curve. The winner gets the glow.
- **Slide 22** — the Streamlit screenshot's settings (`R₀ = 1.5`, `Budget = 5%`, `Caltech36`) match Slide 13's headline numbers exactly. The live demo on Slide 23 will reproduce the headline result if Ryan starts from those defaults.
- **Slide 1 and Slide 24** — the rotating Caltech36 background is the same render. The deck "loops back" visually.

---

## Implementation notes

- **Tooling.** Either Keynote with custom typography, or Reveal.js with a custom theme. Both can render the chrome (speaker tag, slide number) globally and the figure placeholders as `<img>`/`<image>` tags pointing to `paper/figures/...`.
- **Build order.** Generate the deck **after** running `scripts/08_make_figures.py` so all figures are fresh. Then capture the webapp screenshot for Slide 22.
- **No re-rendering of figures inside the deck.** Every numerical plot uses the existing PNG from `paper/figures/`. Decoupling the deck from the data pipeline keeps the figures consistent with the paper.
- **Numerical values.** All headline numbers cited in the deck are present in `results/summary/headline_numbers.json`. Re-pull from there if any value needs updating.
