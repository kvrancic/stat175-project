# STAT 175 Lightning Talk: Cost-Constrained Edge Removal for Epidemic Containment

**Total target: 5 minutes (~700-750 words at ~150 words/minute speaking pace)**

**Speakers:** Karlo, Alec Leprevotte, Jackson Webster, Ryan Jiang
**Deck:** 17 slides (visual spec in `slides-design.md`)

---

## Part 1: Karlo (Opening) — Slides 1-3

**Time: ~1 minute (~150 words)**

[Slide 1 — Title]

Hey everyone. We're working on epidemic containment on social networks, but with a twist: the cost of breaking a friendship matters. I'm Karlo, and the team is Alec, Jackson, and Ryan.

[Slide 2 — Why edge removal]

Here's the setup. Suppose a disease is spreading through a college's friendship graph. You can't remove people from society — that's not how real interventions work. What public-health policy actually does is restrict who's allowed to meet whom. Closing a school, reassigning a dorm, banning a gathering — all of those are edge cuts. And every cut has a cost. Severing a roommate tie is socially expensive. Severing a casual acquaintance is cheap.

[Slide 3 — The formal problem]

So the question is: **what's the lowest-cost set of edges to cut so the epidemic stays under control?** That's a constrained optimization on a weighted graph, with a learned component sitting inside it. Alec, take it from the math.

---

## Part 2: Alec — Slides 4-6

**Time: ~1 minute (~150 words)**

[Slide 4 — SIS dynamics]

We use the SIS model — Susceptible–Infected–Susceptible — because COVID-style diseases don't give permanent immunity. People recover, then catch it again. We run everything on five Facebook100 campuses, picked for diversity in clustering coefficient.

[Slide 5 — The spectral threshold]

There's a clean threshold for whether an SIS epidemic dies out or persists: τ_c = 1 over the leading eigenvalue of the adjacency matrix. Below τ_c, the disease dies. Above, it goes endemic. Edge removal directly raises this threshold — cutting bridges shrinks lambda_1, which raises τ_c, which shrinks the endemic region.

[Slide 6 — Cost function]

Now the cost function. We follow our advisor's suggestion: each node has feature data — dorm, year, major, gender. We L2-normalize the one-hot encoding and define cost as **sigmoid of the dot product** of two endpoint feature vectors. Similar features means socially close, means an expensive edge to cut. Jackson, what do we do with that?

---

## Part 3: Jackson — Slides 7-9

**Time: ~1.25 minutes (~190 words)**

[Slide 7 — The four policies]

We compare four policies, ordered from naive to learned. **Random edge removal** — the trivial baseline. Every other policy has to beat it. **Edge betweenness centrality, divided by cost** — bottleneck edges divided by what they cost to cut. The classical bang-for-buck baseline. And then two more interesting ones.

[Slide 8 — Distance Threshold]

**Distance Threshold** — the realistic, implementable one — the kind of policy a government can actually enforce. We partition the graph into communities, build a community meta-graph, and cut edges between communities that are far apart in that meta-graph. Equivalent to "stay within your friend bubble."

[Slide 9 — The GNN pipeline]

And **the novel piece — a GNN-learned policy.** A 2-layer GraphSAGE encoder learns node embeddings z_v from a self-supervised link-prediction task. The cost of an edge is sigmoid(<z_u, z_v>) — basically, the probability the GNN thinks two nodes "should" be connected. Then we score each edge by NetMelt's eigenvector product divided by that learned cost. The point isn't that we invented a new architecture. The point is the cost function itself is learned end-to-end from the graph, instead of being hand-designed. Ryan, results.

---

## Part 4: Ryan — Slides 10-17

**Time: ~1.75 minutes (~225 words, including the live demo)**

[Slide 10 — Headline result]

This is the headline. Across all five campuses, near the epidemic threshold — that's R0 around 1.5 — the GNN policy is the clear winner. At a 5% cost budget, it cuts steady-state prevalence by **4.0 percentage points**; the next-best classical baseline only achieves **2.2**. The learned cost is roughly twice as efficient where it matters most: when the disease is barely sustaining itself.

[Slide 11 — How it depends on R₀]

But the picture flips at R0 = 6. In a heavily endemic regime, distance-threshold and edge-betweenness take over — there's nothing subtle to optimize once the graph is saturated.

[Slide 12 — Robustness]

Three robustness panels. **Compliance:** the GNN at 60% non-compliance still beats every other policy at full compliance. **SIR alternative:** same regime split, even sharper. **Adversarial seeding** — start the disease at the eigenvector backbone — the GNN now wins both regimes including R0=6 where it had been third under random seeding.

[Slide 13 — Two ablations]

The architecture ablation says GraphSAGE, GAT, and GCN are indistinguishable — the cost-learning framework matters, not the message-passing operator. And the cost-function ablation says the GNN advantage widens when cost has more dynamic range.

[Slide 14 — Honest limitations]

The honest caveat: Facebook100 is a friendship graph, not a contact graph. We're not solving COVID. We're showing that the cost-aware framing changes which policies look "best" — and the gap between the mathematically optimal GNN and the enforceable distance threshold is the interesting part.

[Slide 15 — Web app teaser → Slide 16 — DEMO]

We also built a Streamlit app where you can pick a campus, dial R0 and the budget, and watch SIS spread on the residual graph. Let me show you.

*(live demo, ~30 s — reproduce the headline at R₀ = 1.5, 5% budget, Caltech36)*

[Slide 17 — Closing]

That's us. Thanks!

---

## Notes for the speakers

- **Words per minute target = 150.** If you sound rushed, drop one sentence.
- **Slide cadence.** 17 slides over ~5 minutes ≈ 17 s/slide on average. Title and interstitials are fast (5-10 s); figure slides (10, 11, 12, 13) get more dwell (~22 s). Don't linger on Slides 4 and 7 — they're scaffolding.
- **Live demo.** Slide 16 is the alt-tab to Streamlit. Use the same `R₀ = 1.5 / 5% budget / Caltech36 / GNN` configuration that produced the headline numbers on Slide 10 — the demo will reproduce the result live, which is the strongest possible close.
- **M4 numbers are in.** Headline reduction at 5% budget: GNN +0.0402 vs distance threshold +0.0222 vs betweenness +0.0171 vs random +0.0158 at R0=1.5. The talk's Slide 10 quotes the rounded versions ("4.0pp" and "2.2pp"). All headline numbers live in `results/summary/headline_numbers.json`; raw rows in `results/main_pareto.parquet`. If a result changes after a re-run, update Slide 10's narration accordingly.
- **What Austern cares about** (from `docs/short-brief.md`): the precision of the question, the "go beyond degree" novelty, the implementability discussion (ideal GNN vs realistic Distance Threshold), and honest limitations. Hit each of these in the talk.
- **What Austern explicitly does NOT want:** "we ran A and B, here are numbers, the end." So Ryan's Slide 14 framing is non-negotiable: preview the *discussion* (cost-aware framing changes the picture, the ideal-vs-implementable gap is the contribution) rather than just announcing a winner.
- **Backup slides for Q&A.** If asked about per-campus consistency, pull up `paper/figures/main_ranking_R0_1.5.png`. If asked about whether the result is Facebook100-specific, pull up `paper/figures/ablation_synthetic_topology_R0_3.0.png`. If asked which graph statistics predict GNN dominance, pull up `paper/figures/cross_campus_regression.png`.
