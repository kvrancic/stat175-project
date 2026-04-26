# STAT 175 Lightning Talk: Cost-Constrained Edge Removal for Epidemic Containment

**Total target: 5 minutes (~700-750 words at ~150 words/minute speaking pace)**

**Speakers:** Karlo, Alec, Jackson, Ryan

---

## Part 1: Karlo (Opening) — Slides 1-2

**Time: ~1 minute (~150 words)**

[Slide 1 — Title]

Hey everyone. We're working on epidemic containment on social networks, but with a twist: the cost of breaking a friendship matters. I'm Karlo, and the rest of the team is Alec, Jackson, and Ryan.

[Slide 2 — The Question]

Here's the question. Suppose a disease is spreading through a college's friendship graph. You can't remove people from society — that's not how real interventions work. But you can break specific connections: who's allowed to meet whom. Every connection has a cost. Severing a roommate tie is socially expensive. Severing a casual acquaintance is cheap. **Given that, what's the lowest-cost set of edges to cut so the epidemic stays under control?**

This is a constrained optimization problem on a weighted graph, with a learned component sitting inside it. Alec will unpack the math.

---

## Part 2: Alec — Slide 3

**Time: ~1 minute (~150 words)**

[Slide 3 — SIS Model + Spectral Threshold + Cost Function]

So we're using the SIS model — Susceptible–Infected–Susceptible — because COVID-style diseases don't give permanent immunity. People recover, then catch it again. There's a clean threshold for whether an SIS epidemic dies out or persists: τ_c = 1 over the leading eigenvalue of the adjacency matrix. Below τ_c, the disease dies. Above, it goes endemic.

Edge removal directly raises this threshold. Cutting bridges shrinks lambda_1, which raises τ_c, which shrinks the endemic region.

Now the cost function. We follow our advisor's suggestion: each node has feature data — dorm, year, major, gender. We L2-normalize the one-hot encoding and define cost as **sigmoid of the dot product** of two endpoint feature vectors. Similar features means socially close, means an expensive edge to cut.

Jackson, what do we do with that?

---

## Part 3: Jackson — Slide 4-5

**Time: ~1.5 minutes (~225 words)**

[Slide 4 — The Four Policies]

We compare four policies, ordered from naive to learned:

1. **Random edge removal.** The trivial baseline. Every other policy has to beat this.

2. **Edge betweenness centrality, divided by cost.** Bottleneck edges divided by what they cost to cut. This is a strong, classical structural baseline. Remove edges with the best bang-for-buck.

3. **Distance threshold.** The realistic, implementable one — the kind of policy a government can actually enforce. We partition the graph into communities, build a community meta-graph, and cut edges between communities that are far apart in that meta-graph. Equivalent to "stay within your friend bubble."

4. **The novel piece — a GNN-learned policy.** A 2-layer GraphSAGE encoder learns node embeddings z_v from a self-supervised link-prediction task. The cost of an edge is sigmoid(<z_u, z_v>) — basically, the probability the GNN thinks two nodes "should" be connected. Then we score each edge by NetMelt's eigenvector product divided by that learned cost.

[Slide 5 — Why This GNN Is Useful]

The point isn't that we invented a new architecture. The point is the cost function itself is learned end-to-end from the graph, instead of being hand-designed. The GNN turns "edges between similar people are expensive" into a quantitative, data-driven cost.

Ryan, what does this look like in practice?

---

## Part 4: Ryan — Slides 6-7

**Time: ~1 minute (~150 words)**

[Slide 6 — Results Teaser: Pareto Frontier on Caltech36]

This is one of our headline plots — the Pareto frontier on Caltech36. X-axis: cost budget as a fraction of total cost. Y-axis: SIS steady-state prevalence — the long-run fraction infected.

[POPULATE_AFTER_M4: insert frontier figure showing all 4 policies; say which dominates at low budgets and which at high budgets, in 1-2 sentences]

[Slide 7 — Robustness + What's Next]

We're running this across five Facebook100 campuses chosen for clustering-coefficient diversity, plus three robustness panels: SIR vs SIS, 100% vs 80% policy compliance, and adversarial seeding. We also have a Streamlit demo where you can pick a campus, dial R0 and the budget, and watch SIS spread on the residual graph.

The honest caveat: Facebook100 is a friendship graph, not a contact graph. We're not solving COVID. We're showing that the cost-aware framing changes which policies look "best" — and that the gap between mathematically optimal and politically enforceable is the interesting part.

That's us. Thanks!

---

## Notes for the speakers

- **Words per minute target = 150.** If you sound rushed, drop one sentence.
- **Numbers to insert after M4 finishes:** the prevalence reduction at 5% budget, the AUC-rank winner per campus, and the robustness conclusion (does the ranking flip under SIR?). All live in `results/main_pareto.parquet` and `results/robustness_*.parquet`. Run `python scripts/08_make_figures.py` to refresh `paper/figures/`.
- **What Austern cares about** (from `docs/short-brief.md`): the precision of the question, the "go beyond degree" novelty, the implementability discussion (ideal GNN vs realistic Distance Threshold), and honest limitations. Hit each of these in the talk.
- **What Austern explicitly does NOT want:** "we ran A and B, here are numbers, the end." So Ryan's closing should preview the *discussion* (cost-aware framing changes the picture) rather than just announce a winner.
