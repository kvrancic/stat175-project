# Comprehensive research briefing: pandemic containment via cost-weighted edge removal on social networks

**The core finding of this research survey is that cost-weighted edge removal for epidemic containment sits at a well-defined but underexploited intersection of spectral graph theory, combinatorial optimization, and GNN-based learning.** The intellectual landscape is mature enough to build on—the spectral threshold τ_c = 1/λ₁(A) is rigorously established, edge-deletion algorithms like NetMelt and GreedyWalk exist, and GNN+RL frameworks for epidemic control have emerged—yet the specific combination of heterogeneous edge costs, cross-campus structural comparison on Facebook100, and learned edge-importance scoring remains an open gap. This briefing identifies the **three strongest anchor papers** (Tong et al. 2012, Saha et al. 2015, Meirom et al. 2021), catalogs ~120 relevant works across 14 thematic areas, and highlights creative angles that could elevate a STAT 175 project from competent to exceptional.

---

## 1. Foundational epidemic dynamics on networks

The theoretical backbone of this project rests on a chain of results developed between 2001 and 2015. **Pastor-Satorras and Vespignani (2001)** showed that SIS epidemics on scale-free networks have a vanishing epidemic threshold (τ_c → 0) for degree exponents γ ≤ 3, fundamentally challenging classical epidemic theory (Physical Review Letters, 86(14):3200–3203, arXiv:cond-mat/0010317). The companion paper in Physical Review E (63:066117, 2001) provided the mean-field prediction τ_c = ⟨k⟩/⟨k²⟩.

**Wang, Chakrabarti, Wang, and Faloutsos (2003)** established the spectral viewpoint: the SIS epidemic threshold on any finite graph is **τ_c = 1/λ₁(A)**, where λ₁ is the spectral radius of the adjacency matrix (SRDS '03, pp. 25–34). The extended journal version by **Chakrabarti et al. (2008)** in ACM TISSEC (10(4), Article 13) provides the rigorous proof and experimental validation on real Internet graphs. This result is the project's theoretical foundation: reducing λ₁ through edge removal directly raises the epidemic threshold.

**Newman (2002)** proved that **SIR epidemics on networks are exactly isomorphic to bond percolation** (Physical Review E, 66:016128, arXiv:cond-mat/0205009). The epidemic occurs when transmissibility T exceeds the bond percolation threshold p_c, and final epidemic size equals the giant component of the percolation cluster. This duality means edge removal for SIR containment is literally a percolation problem—a deep connection the project should exploit.

**Keeling and Eames (2005)** provided the definitive bridge between network science and epidemiology, reviewing how degree distributions, clustering, community structure, and path lengths shape epidemic dynamics (Journal of the Royal Society Interface, 2(4):295–307). **Pastor-Satorras, Castellano, Van Mieghem, and Vespignani (2015)** produced the comprehensive review of epidemic processes on networks (Reviews of Modern Physics, 87:925–979, arXiv:1408.2701), covering SIS/SIR models, quenched mean-field approximation, pair approximation, and dynamical message-passing. **Ganesh, Massoulié, and Towsley (2005)** provided rigorous probabilistic bounds: if δ/β > λ₁, the epidemic dies out in O(log n) time; if δ/β < h(G) (Cheeger constant), the epidemic persists exponentially long (IEEE INFOCOM '05, pp. 1455–1466).

For SIS versus SIR thresholds: the SIS threshold depends on the spectral radius (feedback through reinfection), while the SIR threshold maps to bond percolation (one-shot infection). **This distinction matters for COVID-like diseases with waning immunity**—SIS (or SIRS) more accurately captures endemic dynamics with recurrent waves. The project should run both models and compare how optimal edge-removal strategies differ between them.

A recent survey by **Li et al. (2024)** on epidemic spreading on higher-order networks (Physics Reports, DOI:10.1016/j.physrep.2024.01.003) and **Liu et al. (2024)** reviewing GNNs in epidemic modeling (arXiv:2403.19852) provide the most current landscape views.

---

## 2. Attack vulnerability and immunization strategies

The classical node-removal baseline begins with **Albert, Jeong, and Barabási (2000)** showing scale-free networks are robust to random failures but fragile under targeted hub removal (Nature, 406:378–382). **Holme, Kim, Yoon, and Han (2002)** extended this to both vertex and edge attacks using four strategies—degree-based and betweenness-based, static and adaptive—finding that **recalculated (adaptive) strategies are significantly more damaging** (Physical Review E, 65:056109, arXiv:cond-mat/0202410). This paper is notable for introducing edge-level attacks, making it a direct predecessor to the project.

**Cohen, Havlin, and ben-Avraham (2003)** introduced **acquaintance immunization**—randomly selecting nodes and immunizing their neighbors—which exploits the friendship paradox to achieve near-targeted performance without global knowledge (Physical Review Letters, 91:247901). **Pastor-Satorras and Vespignani (2002)** showed random immunization is futile on scale-free networks but targeted immunization of hubs is effective (Physical Review E, 65:036104). These establish the baseline the project must beat: the question is whether GNN-learned, cost-aware edge removal outperforms these classical heuristics.

Recent advances include **Artime et al. (2024)** reviewing robustness and resilience of complex networks (Nature Reviews Physics, 6:114–131) and **Vullikanti et al. (2025)** designing differentially private immunization algorithms that minimize spectral radius under edge privacy constraints (NeurIPS). **Braunstein, Dall'Asta, Semerjian, and Zdeborová (2016)** studied network dismantling via optimal node removal (PNAS, 113:12368–12373, arXiv:1603.08883), noting that edge-based dismantling is "a much easier problem" but remains underexplored. **Ren et al. (2019)** generalized dismantling to heterogeneous node costs using spectral properties of weighted Laplacians (PNAS, 116:6554–6559)—a direct conceptual precursor to cost-weighted edge removal.

---

## 3. Edge removal for epidemic containment—the project's intellectual core

This section contains the papers most directly relevant to the project, including the two strongest anchor candidates.

### ⭐ Anchor Paper #1: NetMelt

**Tong, Prakash, Eliassi-Rad, Faloutsos, and Faloutsos (2012).** "Gelling, and melting, large graphs by edge manipulation." CIKM '12, pp. 245–254. **Best Paper Award.**

NetMelt solves exactly the problem the project addresses: delete k edges to maximally reduce λ₁(A). Using first-order matrix perturbation theory, the score of edge (i,j) for deletion is **u_i·v_j + u_j·v_i** (product of left/right eigenvector components of the leading eigenvalue). The algorithm runs in **O(n+m) time** after eigendecomposition. The paper also introduces NetGel (adding edges to increase λ₁) and explores higher-order perturbation theory for improved accuracy. The eigenvector-product scoring function is elegant and directly extensible to cost-weighted settings by dividing the score by edge cost.

### ⭐ Anchor Paper #2: GreedyWalk

**Saha, Adiga, Prakash, and Vullikanti (2015).** "Approximation Algorithms for Reducing the Spectral Radius to Control Epidemic Spread." SDM '15, pp. 568–576. arXiv:1501.06614.

This is the most rigorous algorithmic treatment of cost-weighted edge removal. It defines the Spectral Radius Minimization by Edge removal (SRME) problem: given a network G and target spectral radius T, find the **minimum-cost set of edges** to remove so that λ₁(G') ≤ T. The paper **explicitly models heterogeneous edge costs c(·)**. The GreedyWalk algorithm achieves an **O(log²n)-approximation** by casting the problem as hitting closed k-walks; a primal-dual variant improves to O(log n). This is the natural starting point for the project: the student can extend it with feature-based edge cost models and GNN-learned edge scoring.

### Additional critical papers

**Van Mieghem, Stevanović, Kuipers et al. (2011)** proved that minimizing spectral radius by removing m links is **NP-complete** and compared greedy heuristics, showing that removing edges (i,j) with largest eigenvector-component product (x₁)_i·(x₁)_j is superior (Physical Review E, 84:016101). **Yi, Shan, Paré, and Johansson (2022)** directly framed edge removal for SIR containment, proving that infection-count upper bounds are **monotone supermodular** under moderate reproduction-number conditions, enabling greedy algorithms with guarantees **sharper than (1-1/e)** (SIAM Journal on Control and Optimization, 60(2):S246–S273, arXiv:2011.11087). **Enright and Meeks (2018)** studied edge deletion to bound connected component size (epidemic containment via graph fragmentation), showing NP-completeness in general but linear-time solvability on bounded-treewidth graphs (Algorithmica, 80:1857–1889).

Recent work includes **Liang, Cui, and Zhu (2023)** on edge centrality measures for epidemic suppression (Frontiers in Physics, 11:1164847), **Soriano-Paños, Costa, and Rocha (2025)** using semi-metric topology to identify epidemiologically relevant edges (J. Phys. Complex., 6:035005), and **Grassia and Mangioni (2024)** applying geometric reinforcement learning to edge dismantling—one of very few papers explicitly addressing edge (not node) dismantling via deep learning (CompleNet-Live 2024, Springer).

**The project's positioning**: "Our work builds on NetMelt (Tong et al. 2012) and GreedyWalk (Saha et al. 2015) but extends them by (1) introducing a learned, feature-based edge cost model using sigmoid of node-feature dot products, (2) comparing strategies across structurally diverse Facebook100 campuses, and (3) deploying a GNN to learn edge-removal policies from local structural and feature information."

---

## 4. Cost-aware and budgeted interventions

Most network intervention work treats all edges as equal cost—this is the project's primary contribution space. Beyond Saha et al. (2015), the landscape is sparse:

**Enns, Mounzer, and Brandeau (2012)** formulated edge removal as a two-way graph partitioning problem under budget constraint K using SDP relaxation of a QCQP (Mathematical Biosciences, 235(2):138–147). **Enns and Brandeau (2015)** compared preventive vs. reactive link removal under resource constraints, finding reactive optimization-based approaches perform best at moderate budgets (Journal of Theoretical Biology, 371:154–165). **Nandi and Medal (2016)** developed four MILP network interdiction models for edge removal (Computers & Operations Research, 69:10–24). All use uniform edge costs.

A critical theoretical finding: **spectral radius minimization by edge removal is NOT submodular**, as proved by **Li and Zhang (2021)** (CIKM '21) and confirmed by **Achterberg and Kooij (2025)** (arXiv:2501.03363). However, **Yi et al. (2022)** showed that SIR infection-count bounds *are* supermodular under certain conditions. The general immunization objective is neither submodular nor supermodular (arXiv:2410.19205, 2024). This non-submodularity means the greedy algorithm lacks worst-case guarantees, but the GreedyWalk set-cover reduction provides an alternative path to provable approximations.

For influence blocking, **He, Song, Chen, and Jiang (2012)** proved submodularity under the competitive linear threshold model (SDM '12, arXiv:1110.4723), and **Erd, Vignatti, and Silva (2021)** introduced budget-constrained influence blocking with heterogeneous node costs (Social Network Analysis and Mining, 11:55). **Hedde-von Westernhagen et al. (2025)** explicitly identified cost-heterogeneous edge removal as a gap: "categorizing edges based on both infection transmission potential and the social cost of restriction could make models more realistic" (Scientific Reports, 15:33300).

---

## 5. COVID-era real-network policy evaluation

The pandemic produced a wealth of papers evaluating interventions on actual contact networks.

**Chang, Pierson, Koh et al. (2021)** built a metapopulation SEIR model on SafeGraph mobility networks mapping 98 million people across 5.4 billion hourly edges, finding that a small minority of "superspreader" POIs account for most infections and that occupancy caps outperform uniform mobility reduction (Nature, 589:82–87). **Firth et al. (2020)** simulated COVID control on the BBC Pandemic Haslemere GPS network (469 nodes), finding secondary contact tracing reduced outbreak size to 16% but required quarantining 43% of the population (Nature Medicine, 26:1616–1622).

**Block et al. (2020)** is the most directly relevant COVID paper: it evaluated three network-aware distancing strategies—**social bubbles, similarity-seeking, and triadic closure**—showing all dramatically outperform random edge removal (Nature Human Behaviour, 4(6):588–596, arXiv:2004.07052). **Nishi et al. (2020)** showed that group division and group balancing (network restructuring) can keep R_eff ≈ 1.0 without blanket lockdowns (PNAS, 117(48):30285–30294). **Nande, Adlam et al. (2021)** demonstrated that which edges remain after distancing matters far more than how many are removed (PLOS Computational Biology, 17(1):e1008684).

**Yang, Senapati et al. (2021)** proposed local-funneling betweenness centrality for targeted COVID edge removal, finding that targeting local bottleneck edges reduces infections 10% more than global methods (PLOS Computational Biology, 17(8):e1009351, arXiv:2006.06939). **Danon et al. (2021)** used percolation theory to analyze household bubble policies (Philosophical Transactions of the Royal Society B, 376:20200284)—a beautiful example of connecting percolation to practical policy.

For contact network construction, **Mossong et al. (2008)** POLYMOD remains foundational (PLOS Medicine, 5(3):e74), **Mistry et al. (2021)** provides synthetic contact matrices for 277 sub-national regions across 35 countries with the SynthPops Python package (Nature Communications, 12:323), and **Klepac et al. (2020)** report BBC Pandemic contact patterns from 36,000 UK volunteers.

---

## 6. Facebook100 dataset

**Traud, Mucha, and Porter (2012)** is the original paper: "Social Structure of Facebook Networks" (Physica A, 391(16):4165–4180, arXiv:1102.2166). The dataset contains complete friendship networks from **100 US universities** captured in September 2005, with node attributes (gender, class year, major, dorm, high school). Networks range from ~700 nodes (Caltech36, Reed98) to ~40,000+ (Texas, Penn State, UF).

Key structural findings: at small institutions, **residence/dorm** dominates community structure; at large ones, **high school** is the primary organizing factor; class year is universally important. The data can be downloaded from the Internet Archive (archive.org/details/oxford-2005-facebook-matrix) or Network Repository (networkrepository.com/socfb.php). Each .mat file contains a sparse adjacency matrix and local_info variable with demographic attributes.

**A critical gap for the project: Facebook100 has rarely been used for systematic epidemic simulation.** While individual networks (e.g., Northwestern25) have been used for threshold models by Juul and Porter, no published study has systematically simulated SIR/SIS dynamics across all 100 campuses to exploit the natural variation in size, density, and homophily as a controlled comparison. This gap makes Facebook100 ideal for a cross-campus study of how structural heterogeneity affects optimal edge-removal strategies. The dataset has been widely used for community detection benchmarking and GNN evaluation, so there is strong precedent for its use.

---

## 7. Homophily, assortativity, and segregation metrics

**Newman (2002)** defined degree assortativity as the Pearson correlation of endpoint degrees, proving assortative networks percolate more easily (Physical Review Letters, 89:208701, arXiv:cond-mat/0205405). **Newman (2003)** extended this to categorical attributes with the assortativity coefficient r = (Σ_t x_tt − Σ_t y_t²)/(1 − Σ_t y_t²) (Physical Review E, 67:026126, arXiv:cond-mat/0209450). **Coleman (1958)** introduced the group-level "inbreeding bias" index comparing observed within-group ties to random-mixing expectations (Human Organization, 17(4):28–36).

**Karimi et al. (2018)** showed that homophily influences ranking of minorities in networks with tunable group sizes and homophily (Scientific Reports, 8:11077). **Karimi and Oliveira (2023)** demonstrated that Newman's nominal assortativity has **severe shortcomings with unequal group sizes**, proposing adjusted nominal assortativity (Scientific Reports, 13:21053). **Bojanowski and Corten (2014)** provided a comprehensive comparative analysis of segregation measures (Social Networks, 39:14–32), implemented in the R package netseg. The term "normalized homophily ratio" lacks a single canonical definition—it is used loosely across communities; Karimi and Oliveira (2023) and Bojanowski and Corten (2014) offer the most rigorous frameworks.

The connection between segregation and epidemic dynamics is well-established. **Boguñá and Pastor-Satorras (2002)** proved that degree-degree correlations shift the epidemic threshold via the spectral radius of the connectivity matrix C_kk' = k·P(k'|k) (Physical Review E, 66:047104). **Hiraoka et al. (2022)** showed vaccination homophily considerably increases the critical vaccine coverage needed for herd immunity (Physical Review E, 105:L052301). **Rizi et al. (2025)** in Nature Communications introduced a maximum-entropy model showing group-dependent homophily **substantially impacts percolation thresholds**, altering predictions for epidemic spread. A key insight for the project: **homophily can simultaneously trap infections inside communities (slowing global spread) while lowering the effective threshold within those communities (enabling local persistence)**—the optimal edges to remove depend critically on the segregation structure.

---

## 8. GNN approaches to learning interventions on graphs

### ⭐ Anchor Paper #3: RLGN

**Meirom, Maron, Mannor, and Chechik (2021).** "Controlling Graph Dynamics with Reinforcement Learning and Graph Neural Networks." ICML 2021, PMLR 139:7565–7577.

**This is the paper that most directly combines GNNs with epidemic containment.** RLGN uses a dual-GNN architecture: one module updates node representations according to epidemic dynamics (local infection propagation), while another manages long-range information. An RL agent then modulates social interaction graphs by strategically altering network structures—restricting mobility on edges, selecting nodes for testing/quarantine. It handles exponential state spaces, combinatorial action spaces, and partial observability, and was tested on real-world COVID-19 contact tracing data.

**Song, Zong, Li, Liu, and Yu (2020)** developed DURLECA at KDD: a Flow-GNN estimates virus-transmission risk from origin-destination mobility data, and an RL agent generates mobility-control actions (edge restrictions), suppressing infections while retaining 76% of city mobility (arXiv:2008.01257). **Feng, Song, Xia, and Li (2023)** introduced IDRLECA combining GNN with infection probability estimation and RL for contact tracing intervention (ACM TKDD, 17(3):1–24).

For network dismantling, **Fan et al. (2020)** introduced FINDER using structure2vec GNN + Q-learning for node removal, trained on small synthetic networks but generalizing to large real ones (Nature Machine Intelligence, 2:317–324). **Grassia, De Domenico, and Mangioni (2021)** proposed GDM using GAT-based architecture trained on brute-force optimal sequences, providing early-warning signals of collapse (Nature Communications, 12:5190). Recent work includes **Pu et al. (2024)** on SmartCore using k-core-based GNN+RL (Mathematics, 12(8):1215), **Tian et al. (2025)** on MIND eliminating handcrafted features (arXiv:2508.00706), and **Gu et al. (2025)** extending dismantling to interdependent networks (Nature Machine Intelligence, 7:1–12).

A **critical gap** exists: almost all dismantling work focuses on **node** removal, not **edge** removal. And epidemic GNN models are overwhelmingly focused on **prediction** rather than **prescription**. The combination of edge-scoring via GNN attention (as in GAT) with epidemic simulation objectives to directly learn which edges to remove is largely unexplored—this is the project's GNN contribution space.

For edge importance via node features, **GATs (Veličković et al., 2018, ICLR)** compute edge attention α_ij as a learned function of concatenated node features, implicitly scoring edge importance by endpoint compatibility. In link prediction, the standard dot-product decoder σ(h_u^T · h_v) directly quantifies edge importance as feature similarity—this is exactly the professor's suggested edge cost model. However, **Seshadhri et al. (2024)** proved theoretical limitations of low-dimensional dot-product scores for sparse graphs (PNAS, 121(8)), and work on feature heterophily shows dot products fail when dissimilar nodes form edges.

---

## 9. SIS vs SIR on networks and the spectral threshold

The **SIS threshold** τ_c = 1/λ₁(A) arises because reinfection creates feedback loops whose stability is governed by the adjacency matrix spectrum. The linearized SIS mean-field equations around the disease-free equilibrium yield the system matrix (β·A − δ·I), which is stable iff β·λ₁ < δ. The eigenvector corresponding to λ₁ identifies which nodes sustain the endemic state.

The **SIR threshold** maps to bond percolation: each edge transmits infection with probability T = 1 − e^{−β·τ_I}. The epidemic occurs iff T exceeds the percolation threshold p_c. For configuration-model networks, the SIR threshold is T_c = ⟨k⟩/(⟨k²⟩ − ⟨k⟩).

These yield **different optimal edge-removal strategies**: SIS optimization targets spectral radius reduction (ongoing transmission), while SIR optimization targets percolation threshold increase (one-shot spreading). The project should compare how the same edge-removal budget performs differently under SIS and SIR, since COVID-like diseases with waning immunity are better modeled by SIS/SIRS. **Parshani, Carmi, and Havlin (2010)** derived the SIS critical infection rate analytically using reinfection probability via percolation theory (Physical Review Letters, 104:258701).

---

## 10. Robustness and partial compliance

**Morris, Rossine, Plotkin, and Levin (2021)** proved that optimal time-limited SIR intervention strategies are **not robust to implementation error**—small timing errors produce large increases in peak prevalence (Communications Physics, 4:78, arXiv:2004.02209). For robust control, intervention must be "strong, early, and ideally sustained."

**Leng et al. (2021)** showed that non-adherence to household bubble exclusivity could push epidemic growth above threshold (Wellcome Open Research). **Reintges et al. (2022)** modeled social distancing as link activation/deletion dynamics with piecewise constant rates, finding that severity and timing matter more than speed of implementation (Journal of Theoretical Biology).

The project should include robustness analysis: simulate scenarios where only 80% of targeted edges are actually removed, or where edge removal accuracy is noisy. This is straightforward to implement as a stochastic compliance layer atop any deterministic strategy.

---

## 11. Edge importance via node features

The professor's suggestion—using sigmoid of dot product of node feature vectors as edge importance—has deep connections to the GNN and link prediction literatures. The standard link prediction decoder σ(h_u^T · h_v) is exactly this formulation. **Karasuyama and Mamitsuka (2017)** showed that optimizing edge weights through local linear reconstruction of node features provides theoretically justified adaptive edge weighting (Machine Learning, 106:307–335). **PTDNet (Luo et al., 2021)** learns which edges to remove by computing learned importance scores enforcing sparsity—directly relevant to "learning the cost of removing an edge."

For the Facebook100 data specifically, node features include gender (binary), class year (ordinal), major (categorical), dorm (categorical), and high school (categorical). The dot product of one-hot encoded features would capture same-gender, same-year, same-major, same-dorm, and same-high-school effects. The sigmoid normalizes this to [0,1], providing a natural edge cost: edges between similar nodes (high dot product) are "easier" to sever (lower social cost), while edges bridging dissimilar groups are "harder" to remove (higher social cost). This captures the real-world intuition that cross-group friendships are more socially valuable and harder to replicate.

---

## 12. Creative angles that could elevate the project

Five creative extensions ranked by novelty × feasibility:

- **Fairness-constrained edge removal.** No existing work formally optimizes edge removal for epidemic containment subject to equitable impact across demographic subgroups. The project could add constraints ensuring no racial or gender subgroup loses more than X% of its edges, then measure the cost of fairness (how much worse is epidemic containment with fairness constraints vs. unconstrained?). This connects to Karimi et al.'s work on homophily's effect on minorities and is highly timely.

- **Rewiring vs. deletion.** **Chan, Akoglu, and Tong (2016)** studied degree-preserving edge rewiring to improve graph robustness (Data Mining and Knowledge Discovery, 30(5)). Instead of deleting edges, rewire them so the network retains connectivity but reduces spectral radius. This models real interventions like rescheduling contacts rather than eliminating them. Comparing deletion vs. rewiring for the same "budget" would demonstrate deep structural understanding.

- **Bond percolation framing.** Frame edge removal as reducing bond occupation probability below the percolation threshold. Compute percolation thresholds analytically for different removal strategies (random, targeted, cost-aware) and compare with simulation. This demonstrates physics-level insight and connects to Newman's (2002) SIR-percolation duality.

- **Temporal edge removal.** Using activity-driven networks (**Perra et al. 2012**, Scientific Reports, 2:469) or SocioPatterns temporal data, study *when* (not just which) edges to remove. **Liu, Perra, Karsai, and Vespignani (2014)** derived optimal control policies from analytical epidemic threshold expressions in ADNs (Physical Review Letters, 112:118702).

- **Game-theoretic price of anarchy.** **Reluga (2010)** formulated differential games for social distancing during SIR epidemics, showing Nash equilibrium behaviors are always sub-optimal (PLOS Computational Biology, 6(5):e1000793). Compare the centralized optimal edge removal with the Nash equilibrium of voluntary distancing on the same Facebook100 network to quantify the "price of decentralization."

---

## 13. Methodological recommendations

**Python libraries.** Use **EoN (Epidemics on Networks)** for fast Gillespie-based SIR/SIS simulation: `EoN.fast_SIR()` and `EoN.fast_SIS()` with `return_full_data=True` for complete trajectories. Citation: Miller and Ting (2019), JOSS, 4(44):1731. The companion textbook is Kiss, Miller, and Simon (2017), *Mathematics of Epidemics on Networks*, Springer. **NDlib** provides broader diffusion model support (16+ models) with built-in visualization (Rossetti et al. 2018, WWW '18 Companion). For large networks, **graph-tool** (Peixoto, 2014) has C++ backend and built-in epidemic models; it is orders of magnitude faster than NetworkX.

**Additional benchmark datasets.** SocioPatterns (sociopatterns.org) provides face-to-face contact networks from schools, hospitals, and workplaces at 20-second resolution. The **Copenhagen Networks Study** offers multi-layer temporal networks of 700+ students over 4 weeks with Bluetooth proximity, phone calls, texts, and Facebook friendships (Sapiezynski et al. 2019, Scientific Data, 6:315). SNAP hosts various social network datasets.

**Experimental setup.** Run 500–1000 Monte Carlo simulations per configuration, varying initial seed nodes randomly. Set β/γ = R₀ ∈ {1.5, 2.0, 2.5, 3.0} for flu-like to COVID-like scenarios. Report final epidemic size, peak prevalence, time to peak, and epidemic probability (fraction of runs producing outbreak > 5% of population). Measure metrics as a function of fraction of edges removed (0% to 20%) and total edge-removal cost. Compare against baselines: random removal, degree-product removal, betweenness removal, and NetMelt eigenvector-product scoring.

---

## 14. Open problems and the path to a standout project

Several well-defined open problems exist in this space:

- **Closing the approximation gap.** The best known approximation for cost-weighted spectral radius minimization via edge removal is O(log²n) by GreedyWalk. Can constant-factor approximation be achieved? This is a hard theoretical question but even partial progress would be notable.

- **Adaptive edge removal during ongoing epidemics.** Most algorithms assume static snapshots. Optimal adaptive strategies that re-evaluate which edges to remove as the epidemic evolves are largely unexplored.

- **Fairness-constrained spectral optimization.** No existing work formally combines spectral radius minimization with fairness constraints across demographic groups. This is directly addressable with the Facebook100 data's demographic attributes.

- **Edge removal under incomplete information.** Real networks are never fully observed. Robust edge removal under partial or noisy network observations is an open direction.

- **Temporal edge removal complexity.** **Enev et al. (2021)** proved edge deletion to restrict epidemic size on temporal networks is NP-hard even with lifetime 2 (JCSS). Practical algorithms are lacking.

The strongest positioning for a STAT 175 project combines three moves: (1) start from the spectral edge-removal framework (NetMelt/GreedyWalk) as the algorithmic foundation, (2) introduce feature-based edge costs using the professor's sigmoid-dot-product model and show how cost heterogeneity changes optimal strategies, and (3) deploy a GNN (inspired by RLGN or GAT-based edge scoring) that learns to predict edge importance from local topology and node features, training against epidemic simulation outcomes on one set of Facebook100 campuses and testing generalization to others. The cross-campus comparison, with campuses selected for maximal structural/segregation diversity, would demonstrate how network topology shapes the effectiveness of different strategies—an insight with both theoretical and practical policy implications. Adding a fairness constraint analysis would make the project genuinely novel in the literature.

---

## Summary of the three strongest anchor papers

| Paper | Key contribution | How the project extends it |
|-------|-----------------|---------------------------|
| **Tong et al. (2012) NetMelt**, CIKM Best Paper | Edge deletion for λ₁ reduction via eigenvector-product scoring, O(n+m) time | Add feature-based edge costs; compare across diverse Facebook100 topologies |
| **Saha et al. (2015) GreedyWalk**, SDM | O(log²n)-approximation for minimum-*cost* edge removal to reduce spectral radius | Use sigmoid(feature dot product) as cost model; compare with GNN-learned costs |
| **Meirom et al. (2021) RLGN**, ICML | Dual-GNN + RL controlling epidemic dynamics by modulating graph structure | Adapt to edge-removal (not just mobility restriction); train on Facebook100 with cross-campus transfer |

These three papers, together with the foundational spectral threshold results (Wang et al. 2003, Van Mieghem et al. 2009) and the SIR-percolation duality (Newman 2002), form a complete intellectual scaffold for the project.