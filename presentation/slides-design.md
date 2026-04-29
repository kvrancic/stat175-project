# Lightning Talk Slide Design — Visual Spec

A slide-by-slide description of how the deck **looks**. The transcript in `lightning-talk.md` is the spoken track; this deck is its supporting layer. The slides do not echo the transcript verbatim, but they do carry real content — definitions, equations, citations, captions, and the figures from `paper/figures/`. The audience should be able to glance at a slide and pick up something the speaker isn't currently saying out loud.

**17 slides for a 5-minute talk** (~17.5 seconds per slide on average). Title and interstitials run ~6 s; content slides with definitions / equations run ~14 s; figure slides run ~22 s. The pacing budgets out to ~300 s end to end including the live demo.

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
- Body text 22-28 pt; titles 36-48 pt.

**Recurring chrome (kept light).**
- Bottom-right speaker tag: `KARLO` / `ALEC` / `JACKSON` / `RYAN` in JetBrains Mono 14 pt, Coral, 60% opacity.
- Bottom-left slide number: `10 / 17` in JetBrains Mono 14 pt, Slate.
- Top-right: project shorthand in Mist 12 pt: `STAT 175 · cost-aware edge removal`.
- A 1 px coral hairline along the bottom 4% of every slide separates chrome from content.

**Transitions.** Slide-to-slide: 220 ms horizontal wipe with cubic-bezier `(0.22, 0.61, 0.36, 1)`. Within-slide builds: 180 ms fade-up + 8 px translate.

**Time budget.**

| Section | Speaker | Slides | Target time |
|---|---|---|---|
| Opening | Karlo | 1-3 | ~60 s |
| Model + cost | Alec | 4-6 | ~60 s |
| Policies | Jackson | 7-9 | ~75 s |
| Results + demo + close | Ryan | 10-17 | ~105 s (incl. ~30 s live demo) |

---

## Figure assets index (use these — they already exist)

All figures below are pre-rendered in `paper/figures/`. Every relevant slide has an explicit `[PLACEHOLDER → <path>]` marker indicating which file to drop in. **Do not regenerate these — they are produced by `scripts/08_make_figures.py` from the locked seeds.**

| File | Used on slide |
|---|---|
| `paper/figures/main_pareto_R0_1.5.png` | **Slide 10 (HEADLINE)** |
| `paper/figures/main_pareto_R0_0.8.png` | Slide 11 (panel A — sub-critical) |
| `paper/figures/main_pareto_R0_3.0.png` | Slide 11 (panel B — mid) |
| `paper/figures/main_pareto_R0_6.0.png` | Slide 11 (panel C — flip) |
| `paper/figures/robustness_compliance_R0_1.5.png` | Slide 12 (top row) |
| `paper/figures/robustness_sir_R0_1.5.png` | Slide 12 (middle row) |
| `paper/figures/robustness_adversarial_seed_R0_1.5.png` | Slide 12 (bottom row) |
| `paper/figures/ablation_gnn_arch_R0_3.0.png` | Slide 13 (left) |
| `paper/figures/ablation_cost_function_R0_3.0.png` | Slide 13 (right) |

Optional / Q&A backups (not on a numbered slide; keep as appendix slides if time permits):
- `paper/figures/main_ranking_R0_1.5.png` — per-campus policy ranking heatmap.
- `paper/figures/main_ranking_R0_3.0.png`
- `paper/figures/ablation_synthetic_topology_R0_3.0.png` — synthetic-topology ablation.
- `paper/figures/cross_campus_regression.png` — cross-campus structural regression.

Numerical figures cited inline (already in `results/summary/headline_numbers.json`):
- GNN @ R₀=1.5, 5% budget: prevalence reduction of **+0.0402** (4.0 pp).
- Distance Threshold @ same: **+0.0222** (2.2 pp).
- Edge Betweenness @ same: **+0.0171** (1.7 pp).
- Random baseline @ same: **+0.0158** (1.6 pp).

The web-app screenshot for Slide 15 does **not yet exist**: take a fresh capture of `webapp/app.py` running locally with `R₀ = 1.5`, `Budget = 5%`, `Caltech36`, GNN policy selected; save as `presentation/assets/webapp_screenshot.png`.

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
  > Karlo &nbsp; Alec Leprevotte
  > Jackson Webster &nbsp; Ryan Jiang
- Footer, JetBrains Mono 16 pt, Slate: `Harvard · Prof. Austern · 28 April 2026`

**Background graphic.** The rotating Caltech36 visualization is real — produced by `pyvis` over `data/processed/Caltech36.npz`. Render once, embed as PNG.

---

## Slide 2 — Why edge removal

**Speaker:** Karlo (~22 s)

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

**Speaker:** Karlo → handoff to Alec (~22 s)

**Layout.** Centered formal optimization problem, with annotations to the side.

**Center.** A boxed equation block, JetBrains Mono 28 pt, Paper:

```
minimize    Σ  c(e)
            e ∈ E_cut

subject to  prevalence_∞( G \ E_cut ) ≤ θ
            E_cut ⊆ E
```

**Right-side annotations**, Mist 16 pt, with thin Slate leader lines:
- `c(e) = σ(⟨x_u, x_v⟩)` — the cost proxy, defined on Slide 6.
- `prevalence_∞` — steady-state SIS infected fraction.
- `θ` — the public-health tolerance.
- `G \ E_cut` — the residual graph after cuts.

**Bottom caption**, Mist 14 pt: `Equivalently: a cost-weighted variant of the immunization problem (Tong et al. 2012; Saha et al. 2015).`

**Why this slide exists.** The transcript stays informal at this point; the slide gives the audience the formal version so technical viewers can lock in.

---

## Slide 4 — SIS dynamics

**Speaker:** Alec (~20 s)

**Layout.** Left: SIS compartment diagram. Right: a short definition block. Bottom: dataset footer strip.

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

**Bottom dataset strip**, full slide width, Mist 14 pt:
> Run on **5 Facebook100 campuses** (Caltech36 · Bowdoin47 · Harvard1 · Penn94 · Tennessee95), chosen for diversity in global clustering coefficient. Loaded from archive.org and restricted to the giant component. Implementation in `src/stat175/sim/sis.py`.

---

## Slide 5 — The spectral threshold

**Speaker:** Alec (~22 s)

**Layout.** Left: the canonical phase-transition plot. Right: equation + intuition.

**Left.** A clean illustrative plot, hand-drawn quality:
- X-axis: `R₀ = β · λ₁(A) / γ`, ticks at 0.5, 1, 2, 4.
- Y-axis: `steady-state prevalence`, 0 to 0.6.
- A sigmoidal curve crossing zero around R₀ = 1.
- Vertical dashed Slate line at `R₀ = 1`, labeled `τ_c`.
- Mint shading left of `τ_c`, Coral shading right.
- Floating labels: `dies out` (mint), `endemic` (coral).
- A small Coral pin marker on the curve at R₀ ≈ 1.5 — labeled `our headline R₀`.

**Right.** Title `EPIDEMIC THRESHOLD`, Inter Tight 700, 28 pt, Paper. Equation in JetBrains Mono 32 pt:

> τ_c = 1 / λ₁(A)

Below the equation, Inter 400, 20 pt:

> The SIS process dies out iff β/γ < τ_c.
> Cutting edges shrinks λ₁(A), which raises τ_c, which pushes the system toward containment.

**R₀ values we sweep:** `0.8, 1.5, 3.0, 6.0` — listed in a small JetBrains Mono 16 pt strip below the equation. The 1.5 value is highlighted in Coral.

**Bottom caption**, Mist 14 pt: `Wang, Chakrabarti, Wang & Faloutsos (2003).`

---

## Slide 6 — Cost function

**Speaker:** Alec → handoff to Jackson (~20 s)

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
> Observed cost band on real Facebook100 features: `c ∈ [0.50, 0.73]`. The narrow range is documented in `WARNINGS.md` and motivated the cost-function ablation (Slide 13).

---

## Slide 7 — The four policies

**Speaker:** Jackson (~26 s)

**Layout.** A 2×2 grid of cards, each 660×320, with a one- or two-sentence description that includes the random + betweenness definitions inline (no separate slide for them).

**Cards** (Inter Tight 700, 26 pt for the title; Inter 400, 17 pt for the body):

| | |
|---|---|
| **1. Random** *(baseline)* | Sample edges uniformly without replacement until cumulative cost reaches the budget. The floor every other policy must beat. |
| **2. Edge betweenness / cost** *(classical)* | Score each edge `e` as `betweenness(e) / c(e)`, greedy fill. NetworkX with `k = 300` pivot sampling on Penn94 / Tennessee95 (Brandes 2008). Bang-for-buck framing. |
| **3. Distance Threshold** *(realistic)* | Louvain communities → meta-graph → cut edges between communities at hop-distance > X. The "stay in your bubble" policy. The kind a government can actually enforce. |
| **4. GNN policy** *(novel)* | 2-layer GraphSAGE → 16-dim embeddings → cost = σ(⟨z_u, z_v⟩) → score = NetMelt eigenscore / cost. Detailed on Slide 9. |

The fourth card has a Coral border (1.5 px) to flag it as the novel contribution. The other three have a thin Slate border (1 px).

**Bottom caption**, Mist 14 pt: `All four implement the same Policy interface in src/stat175/policies/. Locked by Project Outline §3.`

---

## Slide 8 — Distance Threshold (the "realistic" one)

**Speaker:** Jackson (~24 s)

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

## Slide 9 — The GNN pipeline (and what's novel)

**Speaker:** Jackson → handoff to Ryan (~26 s)

**Layout.** Top half: architecture diagram. Middle: training objective + edge score. Bottom strip: novelty pitch.

**Top — pipeline diagram.** Five horizontal stages with arrows:

```
[ X ∈ R^{n × 598} ]  →  [ TruncatedSVD → R^{n × 64} ]  →  [ SAGE × 2 layers ]  →  [ z ∈ R^{n × 16} ]  →  [ c(u,v) = σ(⟨z_u, z_v⟩) ]
```

Each stage is a rounded rectangle, 1 px Mist border. The middle stage `SAGE × 2 layers` is filled with Coral at 8% alpha to indicate the learned component.

Annotations in JetBrains Mono 14 pt below specific stages:
- Below `TruncatedSVD`: `(speed-up; documented in WARNINGS.md)`.
- Below `SAGE × 2`: `hidden_dim=32, embed_dim=16, dropout=0.5`.
- Below `cost`: `analogous to the hand-designed σ(⟨x_u, x_v⟩)` from Slide 6.

**Middle — two side-by-side panels.**

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

**Bottom strip — novelty pitch.** Full-width Coral 24 pt, centered:

> The cost function itself is what's learned end-to-end. The architecture is a means.

**Bottom caption**, Mist 14 pt: `Source in src/stat175/models/gnn.py + src/stat175/policies/gnn_policy.py.`

---

## Slide 10 — Headline result

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

## Slide 11 — How it depends on R₀

**Speaker:** Ryan (~22 s)

**Layout.** Three Pareto plots arranged horizontally — sub-critical, mid, endemic — to show the regime sweep and the flip at R₀ = 6.

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

## Slide 12 — Robustness in three rows

**Speaker:** Ryan (~22 s)

**Layout.** Three small horizontal panels stacked vertically, each ~25% slide height.

**Row 1 — Compliance.**

> **[PLACEHOLDER → `paper/figures/robustness_compliance_R0_1.5.png`]**

Inline caption (Inter 400, 16 pt, right-aligned next to the figure):
> 0% / 20% / 40% / 60% non-compliance, R₀ = 1.5. **GNN at 60% compliance still beats every other policy at 100%.**

**Row 2 — SIR alternative.**

> **[PLACEHOLDER → `paper/figures/robustness_sir_R0_1.5.png`]**

Inline caption:
> Same regime split as SIS, sharper. **The cost-aware ranking is not an SIS artifact.**

**Row 3 — Adversarial seeding.**

> **[PLACEHOLDER → `paper/figures/robustness_adversarial_seed_R0_1.5.png`]**

Inline caption:
> Initial infections placed at the top eigenvector-component nodes. **GNN now wins both regimes — including R₀ = 6, where it had been third under random seeding.**

**Bottom caption**, Mist 14 pt: `Reduced sim budget on these panels (n_realizations = 20) is documented in WARNINGS.md.`

---

## Slide 13 — Two ablations

**Speaker:** Ryan (~16 s)

**Layout.** Two side-by-side figures.

**Left — Architecture.**

> **[PLACEHOLDER → `paper/figures/ablation_gnn_arch_R0_3.0.png`]**

Title above: `Architecture`, Inter Tight 700, 22 pt, Paper.
Takeaway, Inter 400, 18 pt:
> GraphSAGE = GAT = GCN within bootstrap CI. **The framework is what matters; the operator doesn't.**

**Right — Cost function.**

> **[PLACEHOLDER → `paper/figures/ablation_cost_function_R0_3.0.png`]**

Title above: `Cost function`, Inter Tight 700, 22 pt, Paper.
Takeaway, Inter 400, 18 pt:
> Under `oracle_lognormal` (high cost variance), the GNN advantage **widens**. Under `uniform`, it shrinks. **The cost-aware framing depends on cost actually varying.**

**Bottom caption**, Mist 14 pt: `Other ablations (synthetic topology, cross-campus regression) deferred to the appendix and the paper.`

---

## Slide 14 — Honest limitations

**Speaker:** Ryan (~14 s)

**Layout.** Two columns, each a short bulleted list. Single Coral closing line at the bottom.

**Left — What we are not solving.**
- **Friendship ≠ contact.** Facebook100 is a stable friendship graph; epidemics spread on transient contact graphs. Edge weights here are correlates of contact frequency, not contact frequency itself.
- **SIS is a simplification.** Real respiratory pathogens have latency, age structure, behavior change.
- **Cost is a proxy.** σ(⟨x, x⟩) is a stand-in for "social distance"; we don't claim it equals the dollar cost of a school closure.

**Right — Where we cut corners.**
- Reduced GNN encoder (TruncatedSVD pre-projection, hidden_dim=32, embed_dim=16, 40 epochs) for local-laptop tractability. Documented in `WARNINGS.md`. Full-fidelity Colab/A100 retraining script in `notebooks/01_colab_train_full_gnn.py`.
- Sampled betweenness with `k=300` pivots on Penn94 / Tennessee95.
- Robustness panels run at `n_realizations = 20` instead of 50 (also in `WARNINGS.md`).

**Bottom strip**, Coral 24 pt:
> The contribution is the **framing** — that cost-awareness reorders policy rankings — not a deployable COVID intervention.

---

## Slide 15 — Web app teaser

**Speaker:** Ryan (~10 s)

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

## Slide 16 — Live demo (interstitial)

**Speaker:** Ryan (~30 s if live, ≤ 4 s if skipped)

**Layout.** Full-bleed Coral panel. Centered, Inter Tight 900, 200 pt, Ink:

> **DEMO**

Below in JetBrains Mono 24 pt, Ink: `→ webapp/app.py`

That's it. The presenter alt-tabs to Streamlit during this slide and runs through one (campus × policy × budget) configuration end-to-end — ideally using the same `R₀ = 1.5 / 5% budget / Caltech36` config from Slide 10, so the demo reproduces the headline result live.

If the live demo fails or gets skipped, this slide is on screen for under 4 seconds and the deck moves to Slide 17.

---

## Slide 17 — Closing

**Speaker:** Ryan (~6 s)

**Layout.** Mirror of the title slide, simplified.

**Content.**
- Pre-title in Coral, all caps, letter-spaced 0.18em: `THANK YOU`
- Title, Paper, Inter Tight 900, 56 pt:
  > Questions?
- Below, in Mist 22 pt:
  > Code, paper draft, all figures: in the project repo.
  > Reproduce the headline plot: `python scripts/04_run_pareto.py && python scripts/08_make_figures.py`.
- Authors, Mist 18 pt, single line:
  > Karlo · Alec Leprevotte · Jackson Webster · Ryan Jiang
- Acknowledgement, Mist 14 pt:
  > With thanks to Prof. Austern for the cost-function framing and the Track 1 latitude.

Background: the same rotating Caltech36 visualization from Slide 1, at 30% opacity.

---

## Speaker handoff cheat-sheet

| Slide | Speaker | Notes |
|---|---|---|
| 1-3 | **Karlo** | Title, motivation, formal problem. End on slide 3 with "Alec, take it from the math." |
| 4-6 | **Alec** | SIS, threshold, cost. End on slide 6 with "Jackson, what do we actually do with this?" |
| 7-9 | **Jackson** | Four policies + Distance Threshold + GNN pipeline. End on slide 9 with "Ryan, results." |
| 10-17 | **Ryan** | Headline + regime sweep + robustness + ablations + limitations + demo + close. |

The bottom-right speaker tag updates per slide so the audience always knows who's talking.

---

## Easter eggs (kept short and tasteful)

A handful, not a parade:
- **Slide 5** — the Coral pin marker on the phase-transition curve sits exactly at R₀ = 1.5, which is the headline regime on Slide 10. Quiet visual call-forward.
- **Slide 7** — the GNN card has a Coral border; the others have Slate. Communicates "this is the novel one" without saying it.
- **Slide 10** — the Coral GNN curve has a soft glow. **Slide 11**, panel C — the glow has migrated to the Distance Threshold curve. The winner gets the glow.
- **Slide 15** — the Streamlit screenshot's settings (`R₀ = 1.5`, `Budget = 5%`, `Caltech36`) match Slide 10's headline numbers exactly. The live demo on Slide 16 will reproduce the headline result if Ryan starts from those defaults.
- **Slide 1 and Slide 17** — the rotating Caltech36 background is the same render. The deck "loops back" visually.

---

## Implementation notes

- **Tooling.** Either Keynote with custom typography, or Reveal.js with a custom theme. Both can render the chrome (speaker tag, slide number) globally and the figure placeholders as `<img>`/`<image>` tags pointing to `paper/figures/...`.
- **Build order.** Generate the deck **after** running `scripts/08_make_figures.py` so all figures are fresh. Then capture the webapp screenshot for Slide 15.
- **No re-rendering of figures inside the deck.** Every numerical plot uses the existing PNG from `paper/figures/`. Decoupling the deck from the data pipeline keeps the figures consistent with the paper.
- **Numerical values.** All headline numbers cited in the deck are present in `results/summary/headline_numbers.json`. Re-pull from there if any value needs updating.
- **Optional appendix slides.** If we want backup material for Q&A, the per-campus ranking heatmap (`paper/figures/main_ranking_R0_1.5.png`), synthetic-topology ablation (`paper/figures/ablation_synthetic_topology_R0_3.0.png`), and cross-campus regression (`paper/figures/cross_campus_regression.png`) are all good candidates. Park them after Slide 17.
