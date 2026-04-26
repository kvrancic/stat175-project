# Second-iteration research briefing: cost-weighted edge removal for epidemic containment

**Bottom line up front.** The 2024–2026 literature reveals a clear, exploitable gap at the intersection of three mature threads: spectral edge-removal methods (NetMelt/GreedyWalk), GNN-based epidemic intervention, and feature-aware cost modeling. No published paper combines all three. The closest recent work—Li, Eliassi-Rad & Zhang at SDM 2024—extends spectral edge intervention with Frank-Wolfe optimization but remains feature-agnostic. Meanwhile, the KDD 2024 survey on GNNs in epidemic modeling (Liu et al.) explicitly flags intervention optimization as underexplored. A paper that bridges GNN-learned, feature-based edge scoring with provable spectral containment guarantees on realistic social networks fills a gap the field is actively calling for. The venue landscape is favorable: LoG 2025/2026, NeurIPS NPGML workshop, and journals like *Scientific Reports* and *Journal of Complex Networks* are all publishing in this exact space.

---

## 1. Edge removal, link deletion, and network dismantling (2024–2026)

The edge-removal-for-epidemics space has seen meaningful progress since 2023, shifting from purely structural heuristics toward budgeted optimization, spectral perturbation theory, and learned dismantling. The most important recent paper is **Li, Eliassi-Rad & Zhang (SDM 2024)**, which proves that the classic eigenscore product from Tong et al. equals the gradient of the leading eigenvalue, then develops a **Frank-Wolfe algorithm** for budget-constrained edge-weight reduction on weighted graphs. This directly extends the NetMelt framework with continuous relaxation and provable convergence. Equally significant, **Yi, Shan, Paré & Johansson (CDC 2024 / IEEE TNSE 2026)** prove **supermodularity** of infection counts under edge deletion for certain SIR variants, establishing approximation guarantees that the student's project could exploit or extend.

On the practical side, **Soriano-Paños & Rocha (arXiv:2311.14817, updated June 2025)** propose semi-metric distortion sparsification (SMDS), identifying edges that break the triangle inequality as dynamically redundant for epidemic processes—a principled alternative to betweenness-based removal. **Grassia & Mangioni (CompleNet 2024)** introduce **eGDM-RL**, combining Graph Attention Networks with Deep Q-Networks for edge dismantling, making it the first RL-based edge-removal method (as opposed to node removal). A **Scientific Reports (2025)** paper (DOI: 10.1038/s41598-025-33300-3) systematically compares edge removal strategies and explicitly recommends categorizing edges by both transmission potential and social cost of restriction—directly motivating the student's cost-weighted formulation. At WWW 2025, **Zhou et al. (DOI: 10.1145/3696410.3714806)** address large-scale edge manipulation for connectivity minimization with scalable algorithms, and a 2025 paper on **Community-based Edge Percolation (CEP)** achieves 30.6% improvement over prior art by integrating community detection with explosive percolation for edge targeting.

For cost-heterogeneous dismantling specifically, **Shen, Wang, Deng & Wu (Chaos, Solitons & Fractals, 2024)** study spatial network disintegration with heterogeneous node/edge removal costs, though without learned cost functions. **No 2024–2026 paper explicitly models edge removal cost as a function of node attributes or learned embeddings**—this is the open gap.

**Key papers for citation:**

- Li, Eliassi-Rad & Zhang. "Optimal Intervention on Weighted Networks via Edge Centrality." SDM 2024. **arXiv:2303.09086**
- Yi, Shan, Wang, Paré & Johansson. "Dynamic Curing and Network Design in SIS Epidemic Processes." CDC 2024 / IEEE TNSE 2026. **arXiv:2211.06028** (v2 Aug 2024)
- Soriano-Paños & Rocha. "Quantifying Edge Relevance for Epidemic Spreading via Semi-Metric Topology." **arXiv:2311.14817** (v2 June 2025)
- Grassia & Mangioni. "Edge Dismantling with Geometric RL (eGDM-RL)." CompleNet 2024. DOI: 10.1007/978-3-031-57515-0_15
- "Designing Network Based Intervention Strategies from Edge-Based Infection Probability." Scientific Reports, 2025. DOI: 10.1038/s41598-025-33300-3
- Zhou et al. "Highly-Efficient Minimization of Network Connectivity in Large-Scale Graphs." WWW 2025. DOI: 10.1145/3696410.3714806
- Shen, Wang, Deng & Wu. "Spatial Network Disintegration with Heterogeneous Cost." Chaos, Solitons & Fractals, 2024. DOI: 10.1016/j.chaos.2024.114494
- Welikala, Lin & Antsaklis. "Hierarchical Analysis and Control of Epidemic Spreading over Networks." **arXiv:2509.24665** (Sep 2025)
- Barik et al. "Integrated Epidemic Simulation Workflow for Submodular Intervention Strategies." **arXiv:2411.05243** (Nov 2024)

**Publication wedge:** Extend Li et al.'s Frank-Wolfe framework with feature-dependent edge costs (sigmoid of dot product), prove that the resulting objective retains approximate submodularity (leveraging Yi et al.'s supermodularity results), and show that GNN-learned scoring outperforms gradient-based eigenscore heuristics when costs are heterogeneous.

---

## 2. GNN + epidemic papers (2024–2026)

The GNN-epidemic intersection has matured substantially, with the **Liu, Wan, Prakash, Lau & Jin KDD 2024 survey (arXiv:2403.19852)** serving as the definitive reference. This survey explicitly identifies GNN-based intervention optimization as a major open direction, noting that most existing work uses GNNs for forecasting or state estimation, not policy learning. The survey itself should be cited as justification for the student's contribution.

For **GNN-based learned interventions**, the most directly relevant new work is **MIND (arXiv:2508.00706, 2025)**, a GNN with attention that solves network dismantling without handcrafted features, generalizing from small synthetic graphs to million-node real networks. While MIND focuses on node removal, its architecture—attention-based message passing trained on small graphs with transfer to large ones—is directly adaptable to edge scoring. **Dong et al. (Scientific Reports, 2024, DOI: 10.1038/s41598-024-78626-6)** combine ego-aware GNNs with Q-learning for vaccination, outperforming centrality-based methods. The **DGI framework (arXiv:2403.12399, WWW 2025)** uses a GNN as a differentiable propagation model with gradient-guided edge flipping for influence maximization—directly analogous to the student's problem.

For **RL + epidemic intervention**, **Ling, Mondal & Ukkusuri (arXiv:2305.05163, IEEE JBHI 2024)** combine GNNs with deep RL for vaccine allocation on mobility networks, reducing infections by 7–10%. **Feng et al.'s IDRLECA (arXiv:2102.08251, ACM TKDD 2024)** pairs a GNN for infection risk estimation with RL for individual-level mobility interventions—the closest existing architecture to what the student proposes, but for node-level rather than edge-level intervention. **Siahkali et al. (CCTA 2025)** apply multi-agent DDPG directly to networked SIS epidemic control under budget constraints. A new **survey by Liu et al. (arXiv:2603.25771, 2026)** comprehensively covers RL for epidemic control.

For **edge-level GNN methods**, **Natterer et al. (arXiv:2408.06762, TRB 2025)** use GNNs to predict edge-level outcomes of road capacity reduction policies—a directly analogous problem. **Liu et al.'s Edge Priority Detector (arXiv:2403.07943, 2024)** provides a unified framework for GNN-based edge importance scoring. **Pahng & Hormoz (arXiv:2410.14109, 2024)** introduce learnable continuous edge directions using complex-valued Laplacians—methodologically relevant for learning edge-level parameters controlling flow.

For **neural combinatorial optimization**, **X²GNN (ICLR 2025)** achieves strong results on MaxCut, MIS, and MinVertexCover through unsupervised GNN combining exploration and exploitation. **DiffUCO (arXiv:2406.01661, ICML 2024)** applies diffusion models with GNN backbones to unsupervised combinatorial optimization. However, **Nath & Kuhnle (arXiv:2406.11897, 2024)** provide a cautionary benchmark showing several learned heuristics fail to outperform greedy algorithms on MaxCut—the student should address this by comparing against strong baselines.

**Key papers for citation:**

- Liu, Wan, Prakash, Lau & Jin. "A Review of GNNs in Epidemic Modeling." KDD 2024. **arXiv:2403.19852**
- Tian et al. "MIND: Learning Network Dismantling Without Handcrafted Inputs." **arXiv:2508.00706** (2025)
- Ling, Mondal & Ukkusuri. "Cooperating GNNs with DRL for Vaccine Prioritization." IEEE JBHI 2024. **arXiv:2305.05163**
- Feng et al. "IDRLECA: Contact Tracing and Epidemic Intervention via DRL." ACM TKDD 2024. **arXiv:2102.08251**
- Dong et al. "GNN + Q-Learning for Vaccination in Complex Networks." Scientific Reports 2024. DOI: 10.1038/s41598-024-78626-6
- Dynamic Gradient Influencing (DGI). WWW 2025. **arXiv:2403.12399**
- Natterer et al. "GNN for Road Capacity Reduction Policies." **arXiv:2408.06762** (2024)
- Liu et al. "Edge Priority Detector." **arXiv:2403.07943** (2024)
- Sanokowski et al. "DiffUCO: Diffusion for Unsupervised Neural CO." ICML 2024. **arXiv:2406.01661**
- Liu et al. "RL in Infectious Disease Control (Survey)." 2026. **arXiv:2603.25771**

**Publication wedge:** Position the GNN component as bridging the "prediction vs. optimization" gap flagged by the KDD 2024 survey. The student's GNN learns edge-level scores that are feature-aware and cost-informed—this is distinct from MIND (node-level, feature-free) and IDRLECA (node-level, mobility-based).

---

## 3. Homophily, segregation, and assortativity (2024–2026)

This area has seen a burst of activity, driven partly by the heterophilic GNN literature. The most significant paper for the student's project is **Rizi, Michielan, Stegehuis & Kivelä (Nature Communications, 2025, arXiv:2412.07901)**, which introduces a maximum-entropy model decomposing homophily into within- and across-group contributions and proves that **group-dependent homophily substantially alters network percolation thresholds**—directly connecting segregation structure to epidemic containment effectiveness. This paper provides the theoretical justification for why the student's feature-based edge costs (capturing homophily/segregation) should affect intervention performance.

For **segregation metric comparison**, **Mironov & Prokhorenkova (arXiv:2412.09663, LoG 2024)** systematically evaluate existing homophily measures and propose "unbiased homophily" satisfying all five desirable axiomatic properties. **Saxena, Kumar & Meena (arXiv:2509.18289, ASONAM 2025)** provide a comprehensive tutorial covering all major definitions—Coleman's index, Newman's assortativity, edge/node/class/adjusted homophily—and extend to higher-order structures. **Luan et al.'s Heterophilic Graph Learning Handbook (arXiv:2407.09618)** reviews 500+ papers and provides systematic homophily metric comparisons. **Zheng, Luan & Chen (arXiv:2406.18854, NeurIPS 2024)** propose disentangled homophily metrics that separate distinct structural signals, showing standard measures can mislead.

For **segregation–epidemic connections**, **La (Complex Networks 2023/2024)** uses multi-type branching processes to derive conditions under which homophily increases or decreases epidemic persistence—the direction depends on network parameters. A **Scientific Reports (2025)** computational study shows structural inequalities exacerbate infection disparities, with segregation between socioeconomic groups intensifying disease spreading rates. **Hiraoka et al. (PNAS 2025)** study how disease-induced herd immunity depends on network mixing patterns including homophily.

**Key papers for citation:**

- Rizi, Michielan, Stegehuis & Kivelä. "Homophily within and across groups." Nature Communications, 2025. **arXiv:2412.07901**
- Mironov & Prokhorenkova. "Revisiting Graph Homophily Measures." LoG 2024. **arXiv:2412.09663**
- Saxena, Kumar & Meena. "Homophily in Complex Networks: Measures, Models, Applications." ASONAM 2025. **arXiv:2509.18289**
- Luan et al. "The Heterophilic Graph Learning Handbook." **arXiv:2407.09618** (2024)
- Zheng, Luan & Chen. "What is Missing in Homophily?" NeurIPS 2024. **arXiv:2406.18854**
- La. "Effects of Homophily in Epidemic Processes." Complex Networks 2023. DOI: 10.1007/978-3-031-53499-7_24
- Kretschmer, Leszczensky & McMillan. "Strong ties, strong homophily?" Social Forces, 2025. DOI: 10.1093/sf/soae169

**Publication wedge:** Use Rizi et al.'s theoretical framework to predict which Facebook100 campuses should show the largest differential between cost-aware and cost-blind intervention strategies, based on their homophily decomposition. Validate these predictions empirically.

---

## 4. Facebook100 usage (2024–2026)

Facebook100 remains actively used, primarily for **GNN benchmarking and fairness evaluation**, not epidemic modeling. **Vink, Takes & Saxena (Complex Networks 2024 / PLoS ONE 2025, DOI: 10.1371/journal.pone.0336212)** use Facebook100 subnetworks to evaluate group fairness of community detection algorithms. **Gkartzios et al. (WWW 2025, DOI: 10.1145/3696410.3714625)** propose fair community detection via group modularity, likely using Facebook100 as a benchmark. **Loveland et al. (arXiv:2410.04287, LoG 2024)** study how local homophily creates fairness problems in GNNs, using Facebook100-type social network data. **Panayiotou & Magnani (Complex Networks 2024)** implement fairness-aware Louvain on social networks including Facebook100. Several GNN out-of-distribution generalization papers use Facebook100 for node classification (predicting student gender).

**Critically, no 2024–2026 paper uses Facebook100 for epidemic modeling or network intervention.** This represents a clear novelty claim for the student's project: Facebook100 with its rich node attributes (dormitory, graduation year, major, gender) provides natural cost heterogeneity for edge removal that purely synthetic or contact-trace networks cannot.

**Publication wedge:** The student can claim to be the first to apply cost-weighted epidemic intervention to Facebook100, connecting the dataset's extensive use in fairness research to epidemic equity considerations. This bridges two active communities.

---

## 5. Post-COVID retrospective analyses (2024–2026)

The retrospective literature has shifted from descriptive analyses to **counterfactual and causal evaluations** of specific interventions. **She, Smith, Pytlarz, Sundaram & Paré (PLoS Computational Biology, 2024, DOI: 10.1371/journal.pcbi.1012569)** develop a framework centered on reproduction number estimates for counterfactual analysis, validated on university testing-for-isolation strategies at UIUC and Purdue. **Ragonnet et al. (PLoS Medicine, 2025, DOI: 10.1371/journal.pmed.1004512)** use age-stratified models across 74 countries to retrospectively evaluate school closures, finding nuanced, country-dependent effects. **Tan, Luo, Chew et al. (2025)** develop a transmission network model using Singapore's comprehensive contact tracing data to compare forward, backward, bidirectional, and generational tracing strategies—the most detailed network-based tracing retrospective available.

For **mobility-based evaluations**, **Valdano et al. (PLoS ONE, 2025, DOI: 10.1371/journal.pone.0319267)** analyze Chile's municipality-level mobility network across COVID waves, showing structural resilience of mobility patterns. A **Scientific Reports (2025)** paper (DOI: 10.1038/s41598-025-16861-1) demonstrates that standard causal methods for evaluating social distancing policies are highly sensitive to geographic spillovers—failing to account for them can reverse estimated effect signs. **Liu et al. (JMIR 2024, DOI: 10.2196/55013)** systematically evaluate biases in smartphone mobility data, showing nonrepresentativeness for disadvantaged minorities significantly impacts epidemic modeling outcomes.

**Key papers:**

- She et al. "Counterfactual Analysis of Epidemics Using Reproduction Number Estimates." PLoS Comp Biol 2024. DOI: 10.1371/journal.pcbi.1012569
- Ragonnet et al. "School Closures Impact on COVID-19 in 74 Countries." PLoS Medicine, 2025. DOI: 10.1371/journal.pmed.1004512
- Tan et al. "Comparison of Contact Tracing Methods." 2025 (Singapore data)
- Social distancing spillover effects. Scientific Reports, 2025. DOI: 10.1038/s41598-025-16861-1
- Guy et al. "Contact Tracing Strategies: Systematic Review." PLoS Global Public Health, 2025. DOI: 10.1371/journal.pgph.0004579

**Publication wedge:** Frame edge removal as a formalization of the "social bubble" policies evaluated retrospectively. The student's k-hop restrictions and household bubbles directly model real interventions whose effectiveness is now being quantified.

---

## 6. Creative and transformative angles for 2026

Several emerging directions could elevate the student's paper from a workshop contribution to a venue like Nature Communications.

**Graph foundation models** are the hottest topic in graph ML. Surveys by **Wang et al. (arXiv:2505.15116, 2025)** and **Liu et al. (arXiv:2310.11829, updated 2025)** define the space. Most provocatively, **arXiv:2509.24256 (2025)** proposes a GFM for combinatorial optimization on graphs using curriculum-pretrained structural priors—directly relevant to framing edge removal as a transferable CO problem. The student could pre-train a GNN on multiple Facebook100 campuses and demonstrate zero-shot transfer to unseen ones.

**Diffusion models on graphs** offer a counterfactual framing: instead of scoring edges for removal, generate the optimal post-intervention graph via conditional diffusion. **DiffUCO (arXiv:2406.01661, ICML 2024)** already applies diffusion to unsupervised CO. **PDDM (IJCAI 2025)** generates realistic social graphs using GCN/GAT denoising. The student could frame containment as "generate the closest graph to the original that keeps spectral radius below threshold while minimizing feature-based cost."

**Fairness-constrained epidemic intervention** is increasingly important. **arXiv:2510.07536 (2025)** explicitly states that "a social network estimated by tracking human movement may lead to epidemic intervention strategies that discriminate across income levels" and proposes fair graph estimation methods. **FUGNN (arXiv:2405.17034, KDD 2024)** reconciles fairness and utility in GNNs via spectral methods. **GraphGini (arXiv:2402.12937, 2024)** incorporates Gini coefficients as GNN fairness measures. Adding a fairness constraint to the edge removal objective—ensuring no demographic group bears disproportionate intervention cost—would be novel and timely.

**Differential privacy for GNN-based interventions** is feasible with frameworks like **DPAR (WWW 2024)**, **ProGAP (arXiv:2304.08928, WSDM 2024)**, and **GraphPrivatizer (LoG 2024)**. A DP-constrained version of the cost-weighted edge removal would address real-world deployment concerns.

**Causal GNN approaches** are maturing. **Leung (arXiv:2211.07823, updated May 2025)** uses GNNs for causal inference under network confounding, proving doubly robust estimator normality. **CausalGNN** and related work frame epidemic forecasting as causal, enabling counterfactual "what if we removed these edges?" reasoning.

**Key papers:**

- Wang et al. "Graph Foundation Models: Comprehensive Survey." **arXiv:2505.15116** (2025)
- GFM for CO on Graphs. **arXiv:2509.24256** (2025)
- Sanokowski et al. DiffUCO. ICML 2024. **arXiv:2406.01661**
- "Estimating Fair Graphs from Graph-Stationary Data." **arXiv:2510.07536** (2025)
- FUGNN. KDD 2024. **arXiv:2405.17034**
- GraphGini. **arXiv:2402.12937** (2024)
- ProGAP. WSDM 2024. **arXiv:2304.08928**
- Finkelshtein et al. "Equivariance Everywhere All at Once." **arXiv:2506.14291** (2025)

---

## 7. Publication-focused analysis

**The gap is clear and citable.** The KDD 2024 survey (arXiv:2403.19852) flags GNN-based intervention optimization as underexplored. The Scientific Reports 2025 paper explicitly calls for cost-differentiated edge removal. Matamalas et al. (Science Advances, 2018) critiques purely structural approaches for ignoring epidemic parameters. No existing paper combines feature-aware cost modeling + GNN-learned edge scoring + spectral containment guarantees.

**Active venues for 2025–2026:**

- **LoG 2025** (UCLA, Sep/Oct 2025): Proceedings track in PMLR + non-archival extended abstracts. **Best fit for a graph ML + network science paper.** LoG 2026 is also being organized.
- **NeurIPS 2025 NPGML workshop** (New Perspectives in Graph ML): Successor to GLFrontiers. Jure Leskovec keynoting on "Relational Foundation Models." ≤6 pages, non-archival. Deadline ~Sep 2025.
- **NeurIPS 2025 NEGEL workshop** (Non-Euclidean Foundation Models & Geometric Learning): Deadline Aug 24, 2025. ≤9 pages.
- **KDD 2025 MLG** (Mining and Learning with Graphs): Recurring workshop series, Toronto, Aug 2025.
- **ICLR 2026 GRaM workshop** (Geometry, Relational Algebra, Manifolds): Has paper + competition tracks. Already closed for 2026.
- **Complex Networks 2026**: Explicitly lists "Complex Networks and Epidemics" as a topic. Special journal issue invitations.
- **NetSciX 2026** (Auckland): Network science + GNN tutorial track.

**Journal targets, ranked by fit:**

1. **Scientific Reports**: Published the most directly relevant 2025 paper on edge-based intervention. Realistic acceptance timeline.
2. **Journal of Complex Networks** (Oxford): Strong fit for the theoretical + computational mix.
3. **Network Science** (Cambridge): Ideal for methodological contributions.
4. **PNAS Nexus**: Open access, multidisciplinary. Good for the "bridging CS and public health" angle.
5. **Nature Communications**: Stretch goal. The fairness + epidemic equity angle could justify this if results are strong.

**Recommended timeline:**

| Target | Deadline | Format |
|--------|----------|--------|
| LoG 2025 extended abstract | ~Jun 2025 | 4-page non-archival |
| NeurIPS 2025 NPGML | ~Sep 2025 | 6-page workshop |
| LoG 2026 proceedings | ~Jun 2026 | Full paper (PMLR) |
| Journal submission | Fall 2026 | Scientific Reports or J Complex Networks |

---

## 8. Tools, benchmarks, and datasets (2024–2026)

**New epidemic simulation tools:**

- **EpiLearn (arXiv:2406.01661, KDD epiDAMIK 2024)**: Unified PyTorch library for ML-based epidemic modeling. GitHub: https://github.com/Emory-Melody/EpiLearn. Supports GNN-based forecasting, source detection, and intervention. **This is the most relevant new tool** for the student.
- **Epydemix (PLoS Comp Biol 2025, DOI: 10.1371/journal.pcbi.1013735)**: Stochastic compartmental models with ABC calibration, age-stratified contact matrices. GitHub: https://github.com/epistorm/epydemix-data/
- **EpiHiper (PNAS Nexus 2024, DOI: 10.1093/pnasnexus/pgae557)**: HPC framework for large-scale epidemic simulation on dynamic networks. Production-grade, used by federal agencies.
- **epydemic**: Maintained Python library for epidemic simulation on networks with Gillespie dynamics. GitHub: https://github.com/simoninireland/epydemic

**Temporal graph benchmarks:**

- **TGB 2.0 (NeurIPS 2024 Datasets & Benchmarks)**: 9 datasets, up to 72M edges. GitHub: https://github.com/shenyangHuang/TGB. Standard for temporal graph methods.
- **SocioPatterns**: Ongoing face-to-face proximity network datasets from schools, hospitals, workplaces at 20-second resolution. http://www.sociopatterns.org/datasets/
- **Copenhagen Networks Study (Scientific Data, 2019, DOI: 10.1038/s41597-019-0325-x)**: Multi-layer temporal network of 700+ students. Still the premier multi-layer contact dataset.

**Benchmarking gap:** No dedicated benchmark exists for network intervention optimization. **Creating a standardized Facebook100-based epidemic intervention benchmark could itself be a contribution.**

---

## 9. Spectral and percolation connections (2024–2026)

**Artime et al. (Nature Reviews Physics, 2024, arXiv:2509.19867)** provide the authoritative review bridging percolation theory and spectral methods for network dismantling, covering message-passing for bond percolation thresholds, spectral partitioning, and ML-based dismantling with a public code repository. This is essential background.

The most directly useful new result is **Luo (arXiv:2505.06489, May 2025)**, who derives the sensitivity of the Fiedler value λ₂ to topological changes and proposes the **Fiedler Vector Gradient Iterative Attack (FGIA)** for locally optimal edge removal. This reveals an intrinsic relationship between spectral edge importance and community partition. A **Physical Review E (2024)** paper by Porter's group studies **first-order edge dynamical importance (FoEDI)**—a first-order approximation of how the leading eigenvalue changes upon edge removal—proving it always overestimates Δλ/λ for removals. This provides tight bounds the student can exploit.

For edge-addition (the dual problem), **Xia & Cao (Automatica, 2025, DOI: 10.1016/j.automatica.2025.112238)** study maximizing the smallest eigenvalue of grounded Laplacians. **Zhou, Zehmakan & Zhang (IEEE TKDE, 2025)** develop efficient algorithms for spectral optimization via edge manipulation.

**Zhao et al. (Mathematical Methods in Applied Sciences, 2025)** provide a unified edge-based percolation derivation for SIR on random graphs, including an R package. **Bianconi & Dorogovtsev (PRE 2024)** extend percolation theory to hypergraphs.

**Key papers:**

- Artime et al. "Robustness and Resilience of Complex Networks." Nature Reviews Physics, 2024. **arXiv:2509.19867**
- Luo. "FGIA: Locally Optimal Percolation via Fiedler Vector Gradient." **arXiv:2505.06489** (2025)
- Porter group. "First-Order Edge Dynamical Importance." Physical Review E 110, 064304 (2024)
- Zhao et al. "Edge-Based Percolation for SIR on Random Graphs." MMAS, 2025. DOI: 10.1002/mma.10963

**Publication wedge:** Connect the FoEDI perturbation theory to the student's cost-weighted objective: the cost-effectiveness ratio of removing edge (i,j) is FoEDI(i,j)/cost(i,j), where cost is the sigmoid of node-feature dot product. This gives a theoretically grounded, feature-aware edge scoring that the GNN can learn to approximate and improve upon.

---

## 10. The professor's direction: cost-weighted, feature-based edge removal

This is where the novelty claim is strongest. After extensive search, **no 2024–2026 paper explicitly models edge removal cost as a function of node attributes or learned embeddings for epidemic containment**. The closest existing work:

- **Li et al. (SDM 2024, arXiv:2303.09086)**: Budget-constrained spectral edge intervention, but costs are not feature-dependent.
- **Shen et al. (Chaos, Solitons & Fractals, 2024)**: Heterogeneous removal costs for spatial networks, but costs are exogenous, not learned from features.
- **Scientific Reports (2025)**: Explicitly recommends differentiating edges by social cost of restriction, but provides no optimization framework.
- **Generalized Network Dismantling (Ren et al., PNAS 2019)**: Allows arbitrary node costs, predates 2024 and handles nodes not edges.

For **feature-based edge scoring**, the GNN literature provides methodological building blocks. The **Edge Priority Detector (arXiv:2403.07943)** learns edge importance scores via GNN. **CoED GNN (arXiv:2410.14109)** learns continuous edge weights jointly with GNN parameters. **Natterer et al. (arXiv:2408.06762)** predict edge-level policy outcomes using per-edge GNN inputs—the most directly analogous architecture.

For **enforceable/implementable policies**, the k-hop restriction and household bubble concepts connect to **Rizi et al. (PRE 2024)** on contact tracing effectiveness in networks with cliques, and to the retrospective literature on bubble policies. The **Kretschmer et al. (Social Forces, 2025)** finding that strong-tie homophily exceeds weak-tie homophily provides theoretical grounding for why feature-based costs should correlate with tie strength and hence intervention difficulty.

**This section confirms the student's central contribution is novel and timely.** The recommendation is to frame the sigmoid-of-dot-product cost model as a specific instance of a broader "feature-informed edge intervention" framework, and show the GNN can learn to approximate and improve upon the theoretically optimal cost-effectiveness scoring.

---

## 11. Publication positioning

The student's paper fills a gap at the intersection of three well-cited threads. Here is how to frame each contribution for maximum impact:

**Contribution 1 (methodological):** First feature-aware, cost-weighted edge removal framework for epidemic containment that jointly considers network topology, node attributes, and intervention feasibility. Extends NetMelt/GreedyWalk from uniform to heterogeneous costs informed by node features.

**Contribution 2 (computational):** GNN architecture that learns edge-level intervention scores incorporating both spectral importance and feature-based cost, outperforming classical eigenscore heuristics when costs are heterogeneous. Positioned as bridging the "prediction vs. optimization" gap identified by the KDD 2024 survey.

**Contribution 3 (empirical):** Systematic evaluation on Facebook100 with diverse segregation profiles, showing that homophily structure (as characterized by Rizi et al.'s decomposition) predicts when cost-aware strategies most outperform cost-blind ones. First epidemic intervention study on Facebook100.

**Contribution 4 (robustness):** Analysis of partial compliance, topology perturbation, and model swaps showing that GNN-learned strategies degrade gracefully compared to brittle optimal solutions.

**Recommended venue ranking:**

1. **LoG 2025/2026 proceedings** (PMLR): Best balance of prestige, fit, and feasibility. The extended abstract track allows parallel journal submission.
2. **NeurIPS 2025 NPGML workshop**: High visibility, non-archival, Leskovec keynote audience.
3. **Scientific Reports**: Full journal paper with comprehensive experiments. Recent precedent for edge-removal epidemic papers.
4. **KDD 2026 Applied Data Science**: If reframed around real-world deployment considerations.

**Open problems the paper addresses (with citations):**

- "Not all contacts are modifiable" → cost-weighted formulation (Scientific Reports 2025)
- "GNN-based intervention optimization is underexplored" → GNN edge scoring (Liu et al. KDD 2024)
- "Spectral approaches ignore epidemic parameters" → feature-informed costs (Matamalas et al. 2018)
- "Denoising mechanisms for GNNs in epidemiology remain to be studied" → robustness analysis (Liu et al. survey)

---

## 12. Robustness and partial compliance (2024–2026)

The robustness literature has expanded in two directions: stochastic compliance modeling and adversarial graph robustness.

For **stochastic compliance**, a paper in the *European Journal of Applied Mathematics* models non-compliance spreading via social contagion alongside disease spread, finding that at **70% compliance** social distancing substantially reduces cases, but below 50% effectiveness drops sharply. **arXiv:2503.06804 (March 2025)** uses filtering theory for optimal epidemic control under partial information. **arXiv:2503.07251 (March 2025)** addresses the "dark figure" problem of undetected infections via cascade state approaches.

For **adversarial GNN robustness**, **arXiv:2406.03097 (2024)** comprehensively treats GNN resilience to topological perturbations in sparse graphs—directly relevant to edge removal robustness. **arXiv:2504.19820 (April 2025)** proposes hierarchical uncertainty-aware GNNs combining message-passing with uncertainty estimation. **arXiv:2403.07185 (TMLR, 2024)** surveys uncertainty quantification for GNNs covering aleatoric vs. epistemic uncertainty.

For **distributionally robust optimization**, **Song et al. (IISE Transactions, 2024)** combine DRO with dynamic epidemic control, accounting for decision-dependent distributional shifts.

**Key papers:**

- Stochastic Optimal Control Under Partial Information. **arXiv:2503.06804** (2025)
- Stochastic Epidemic Models with Partial Information. **arXiv:2503.07251** (2025)
- GNN Resilience to Topological Perturbations. **arXiv:2406.03097** (2024)
- Hierarchical Uncertainty-Aware GNN. **arXiv:2504.19820** (2025)
- Uncertainty in GNNs Survey. TMLR 2024. **arXiv:2403.07185**

**Publication wedge:** Model partial compliance as stochastic edge re-insertion after removal, show the GNN-learned strategy is more robust to this noise than spectral-only approaches because it accounts for feature-based "compliance likelihood" (edges between close friends are harder to enforce removal of).

---

## 13. Causal inference on networks (2024–2026)

This area has exploded. The most directly relevant paper is **DeepNetTMLE (arXiv:2412.04799, Dec 2024)**, which uses deep-learning-enhanced TMLE to estimate treatment effects under network interference, **tested specifically on SIR epidemic simulations with varied quarantine coverages**. This provides a ready-made framework for evaluating the student's edge removal strategies causally.

**Bong, Ventura & Wasserman (arXiv:2410.11743, updated Jan 2026)** provide the definitive treatment of causal inference using augmented epidemic models, distinguishing observational from counterfactual interpretations of SIR-type models and adjusting for time-varying confounders. **Leung (arXiv:2211.07823, updated May 2025)** proves GNN-based doubly robust estimators are asymptotically normal for causal inference under network confounding—directly usable for evaluating whether the GNN's edge scores have causal, not merely associative, predictive power.

For **interference/spillover**, **Jiang & Athey (arXiv:2309.00141, updated Nov 2024)** propose mixed randomization designs for causal inference when SUTVA is violated, with variance bounds of O(d²n⁻¹). **Chen, Cai et al. (arXiv:2502.19741, Feb 2025)** address latent confounders under networked interference, using a flu vaccination example with herd immunity spillovers. **Bargagli-Stoffi et al. (Annals of Applied Statistics, 2025)** develop Network Causal Trees for detecting heterogeneous treatment and spillover effects.

**Viviano, Imbens et al. (PNAS, 2024)** introduce causal message-passing modeling how treatment effects propagate through networks—a framework directly applicable to understanding how edge removal effects cascade. **CausalGNN-type approaches** and **STOAT (arXiv:2506.09544, June 2025)** integrate causal reasoning into spatial-temporal epidemic forecasting.

**Key papers:**

- DeepNetTMLE. **arXiv:2412.04799** (Dec 2024)
- Bong, Ventura & Wasserman. "Causal Inference Using Augmented Epidemic Models." **arXiv:2410.11743** (updated Jan 2026)
- Leung. "GNNs for Causal Inference Under Network Confounding." **arXiv:2211.07823** (updated May 2025)
- Jiang & Athey. "Causal Inference Under Network Interference." **arXiv:2309.00141** (updated Nov 2024)
- Chen et al. "Causal Effect Estimation Under Networked Interference with Latent Confounders." **arXiv:2502.19741** (Feb 2025)
- Bargagli-Stoffi et al. "Heterogeneous Treatment and Spillover Effects." Annals of Applied Statistics, 2025. DOI: 10.1214/24-AOAS1913
- STOAT. **arXiv:2506.09544** (June 2025)

**Publication wedge:** Use DeepNetTMLE or Bong et al.'s framework to evaluate the causal effect of the student's edge removal strategies, moving beyond simulation-based evaluation to formal causal claims about intervention effectiveness under interference.

---

## Top 10 most promising papers for direct citation and building on

These are the papers most likely to appear in the student's related work section and most directly enabling the proposed contributions:

| # | Paper | ID | Why essential |
|---|-------|----|---------------|
| 1 | Liu et al. "GNNs in Epidemic Modeling" survey | **arXiv:2403.19852** | Identifies the exact gap the paper fills |
| 2 | Li, Eliassi-Rad & Zhang, SDM 2024 | **arXiv:2303.09086** | Best modern spectral edge intervention; extend with feature costs |
| 3 | Rizi et al. "Homophily within and across groups" | **arXiv:2412.07901** | Proves homophily structure affects epidemic thresholds |
| 4 | Yi et al. supermodularity results | **arXiv:2211.06028** | Approximation guarantees for edge deletion |
| 5 | MIND network dismantling | **arXiv:2508.00706** | GNN architecture for dismantling; adapt for edges |
| 6 | Scientific Reports 2025 edge intervention | DOI: 10.1038/s41598-025-33300-3 | Explicitly calls for cost-differentiated edge removal |
| 7 | Artime et al. resilience review | **arXiv:2509.19867** | Bridges percolation + spectral + ML dismantling |
| 8 | Mironov & Prokhorenkova homophily measures | **arXiv:2412.09663** | Rigorous metric comparison for segregation analysis |
| 9 | DeepNetTMLE | **arXiv:2412.04799** | Causal evaluation framework tested on SIR epidemics |
| 10 | Luo FGIA spectral perturbation | **arXiv:2505.06489** | Eigenvalue perturbation theory for edge removal |

---

## Proposed publication strategy

**Title framing:** "Learning Cost-Aware Edge Immunization: GNN-Based Epidemic Containment with Feature-Informed Intervention Costs" (or similar emphasizing the feature-cost novelty).

**Dual-track submission strategy:**

**Track A (fast, high-visibility):** Submit a 4-page extended abstract to **LoG 2025** (deadline likely June 2025) presenting the framework and preliminary results on 3–5 Facebook100 campuses. LoG's non-archival track allows simultaneous journal development. If rejected, pivot to **NeurIPS 2025 NPGML** (deadline ~Sep 2025).

**Track B (full paper):** Develop the complete paper with all 13 experiments by Fall 2025. Target **LoG 2026 proceedings track** (PMLR, deadline ~Jun 2026) as the primary venue. Parallel-submit to **Scientific Reports** or **Journal of Complex Networks** if preferring a journal outlet. The fairness angle (demonstrating that cost-blind intervention disproportionately burdens minority-group edges) could justify **Nature Communications** if the empirical results are striking.

**Key framing decisions:**

- **Lead with the cost-weighted gap.** Every reviewer will ask "what's new beyond NetMelt?" Answer: feature-informed costs, GNN learning, and robustness.
- **Anchor in the KDD 2024 survey's gap.** Cite Liu et al. early to establish that GNN-based intervention optimization is the community's declared open problem.
- **Use Rizi et al.'s theory predictively.** Show that campuses with high within-group homophily (per the Nature Communications decomposition) exhibit the largest gap between cost-aware and cost-blind strategies.
- **Include a fairness analysis.** Even a small section showing demographic impact of different strategies significantly strengthens the paper for any venue.
- **Benchmark rigorously.** The Nath & Kuhnle cautionary paper (arXiv:2406.11897) means reviewers will check whether the GNN actually beats simple baselines. Ensure comparisons against strong heuristics (eigenscore/cost ratio, weighted betweenness/cost ratio) are included.

The combination of theoretical grounding (spectral perturbation + supermodularity), practical relevance (cost-weighted, compliance-aware), methodological novelty (GNN edge scoring with feature costs), and timely dataset usage (Facebook100 for epidemic intervention) positions this paper to fill a gap that multiple recent papers explicitly identify. The window is open—no one has claimed this intersection yet.