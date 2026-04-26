# STAT 175 Project: Central Reference Document

## Epidemic Containment on Social Networks Under Cost-Constrained Edge Interventions

### A Working Document Capturing the State of the Project After the Advisor Meeting

---

> **Purpose of this document.** This file is the single source of truth for what we currently know about our STAT 175 project. It consolidates three things: the original project concept we walked into the advisor meeting with, everything Prof. Morgane Austern said during the meeting, and the implicit and explicit constraints she placed on the scope. It is deliberately agnostic about final decisions. Wherever a choice remains open, the document leaves it open and flags it as a question for the team to resolve. The goal is twofold. First, any team member can read this document and come up to speed on exactly where we stand without having to reconstruct the meeting from memory. Second, Prof. Austern or a TF could read this document and verify that we have correctly understood the assignment and her guidance. Nothing in this document should be read as a commitment; everything in it should be read as a foundation.

---

## Table of Contents

- **Part I: Project Context** (STAT 175 requirements, deliverables, grading)
- **Part II: The Original Project Concept** (what we walked in with)
- **Part III: The Meeting With Prof. Austern** (faithful summary of what was said)
- **Part IV: The Refined Problem Framing** (what changed in the meeting)
- **Part V: Graph-Theoretic Formulation** (vertices, edges, weights, structure)
- **Part VI: Epidemic Models** (SIR, SIS, and the choice between them)
- **Part VII: Intervention Strategies** (what we can do to the graph)
- **Part VIII: The Cost Formulation** (edge removal costs and the objective function)
- **Part IX: Edge Importance and Feature Information** (the proxy question)
- **Part X: Ideal Policies vs Realistic Policies** (the implementability question)
- **Part XI: Robustness Dimensions** (what we vary, what we perturb)
- **Part XII: The Dataset** (Facebook100, what we know, what we do not yet know)
- **Part XIII: Evaluation and Comparison** (how we compare strategies)
- **Part XIV: Literature Directions She Pointed Toward**
- **Part XV: The Nature of the Deliverable** (report, oral defense, lightning talk)
- **Part XVI: Open Questions** (the decisions we have not yet made)
- **Part XVII: What We Will Not Claim**
- **Appendix A: Glossary of Terms**
- **Appendix B: Paraphrased Quotes From the Meeting**
- **Appendix C: Things We Understood But Did Not Say Out Loud**

---

---

# Part I: Project Context

## I.1 The Course and Its Purpose for the Project

This project is for STAT 175, a graduate-level graph theory and network analysis course taught at Harvard by Prof. Morgane Austern. Prof. Austern stated explicitly in class that the purpose of the project is to help students learn how to reason about learning on networks, applied to a real research problem on real data. She said the project exists in place of an additional exam because she has "zero interest" in testing the neural-network portion of the course through a coding exam, and she finds the project to be the better way to assess whether students can use the content of the course on actual problems.

The course covers two broad portions. The first portion is classical graph theory and network analysis, which was tested in the midterm. The second portion covers learning on networks, including neural networks on graphs. The project is the primary evaluation instrument for this second portion. This framing matters: the project should visibly engage with the "learning on networks" content of the course, not just the classical part. A project that relies entirely on classical network metrics and simulation, with no learned component at all, would underuse the course material. Whether the learned component must specifically be a graph neural network, or whether a different kind of learned method on the graph would suffice, is not something Prof. Austern said explicitly. This is an open question to confirm with her.

## I.2 What the Course Values

STAT 175 is a theory-aware course, and Prof. Austern is a theorist. Her engagement style in the meeting made this clear. She cared about the mathematical cleanness of the questions we posed, she cared about the structure of the graph objects we were manipulating, and she cared about whether our methods could be interpreted and discussed in a principled way. She did not express interest in benchmark chasing, leaderboards, or raw empirical performance numbers as the primary contribution. She wanted us to propose, simulate, analyze, and then have a thoughtful discussion about limitations and implications. The emphasis was consistently on the quality of the scientific conversation around the results rather than on the results themselves.

This is worth internalizing because it shapes what "done" looks like. A STAT 175 project is done when we can walk into the oral defense and have an intelligent, honest conversation about what we built, why we built it, what it says, what it does not say, and where the limitations are. It is not done when we hit some performance threshold on some metric.

## I.3 The Deliverables

Based on what Prof. Austern said in the advisor meeting and the class-wide discussion, the deliverables for this project are the following. A full treatment of each deliverable is in Part XV; this subsection is a summary.

**A written report with reproducible materials.** There is a report due. Prof. Austern reads every report personally before any other grading component. In the class discussion she added an important requirement that was not mentioned in the advisor meeting: the report must be accompanied by reproducible materials. She said explicitly that she should be able to produce anything we provide in the report, either by being given the PowerPoint, by accessing a GitHub repository, or through some other means of direct delivery. This means we need a repository with our code, configurations, and scripts alongside the written report. We did not have page length or formatting specifics from her; those likely live in the course syllabus.

**An in-person individual oral defense.** After she reads the report, there is an individual oral defense component. It is in person, not on Zoom. Each student's slot is approximately 15 minutes. The format is exactly three questions: two questions about the content of the project that should be straightforward for someone who did the work, and one deeper question meant to challenge and differentiate. Prof. Austern said students typically get around 2.5 out of 3 right and that 80% correct is fine. Each team member books their own slot through Google Calendar invites that she will release. The defenses occur during the exam period. She explicitly said if anyone has a hard scheduling conflict, now is the time to flag it rather than later. She gives different questions to different team members so coordinating answers in advance is not viable.

**A five-minute lightning talk.** In one of the last two classes of the semester, each group gives a five-minute presentation to the class. Prof. Austern said this is explicitly low-stakes and almost everyone will get full credit. It is judged on the quality of the presentation and the explanation of the scientific question and method, not on the quality of the results. If we do not have results yet by the time of the lightning talk, that is fine. She will bring cookies and students get cookies after giving the talk.

## I.4 The Grading Philosophy

Prof. Austern was explicit about what she does not want. She does not want a project that reads like: "I have this graph, I ran algorithm X and algorithm Y, here are the numbers, the end." That form of project gets a bad grade even if the numbers look good. What she does want is a project where the team clearly understood the problem, chose methods thoughtfully, simulated something reasonable, looked at the results critically, and then had a mature discussion about limitations, implementability, additional information that would help, robustness to the assumptions being relaxed, and what the findings mean when you step back.

Her framing, compressed: the final product is not a definitive answer and it is not a paper. It is evidence that the team thought carefully about a concrete scientific question, built reasonable tools to investigate it, and can discuss the results with intellectual honesty. That is the bar.

In the class discussion she added more detail about the grading philosophy itself, and this is worth capturing:

**There is no fixed quota of A's.** She said explicitly that she does not have a target distribution of grades. If every student in the class demonstrates mastery, every student gets an A. If no student does, no student does. Students are not in competition with each other.

**The grading is mastery-based.** An A means the student has demonstrated mastery of the topic, not that they ranked in the top X% of the class. Her stated goal is to help students demonstrate mastery, which is why she met with every group individually before the project.

**The midterm does not lock in the final grade.** She specifically said that students who did poorly on the midterm can still do well in the course if they do well on the project. The project and the midterm are evaluated separately and a strong project can compensate for a weak midterm.

**But the project is not an automatic A.** She also said the opposite of the above: not every project gets full credit. Students need to put real effort in. The project is a genuine evaluation, not a participation exercise.

The combined implication is that effort is the right variable to optimize. The grade is determined by the quality of the work, not by a curve and not by a participation floor. A project that seriously engages with the question, uses appropriate methods, and has a thoughtful discussion section will do well regardless of what anyone else in the class is doing.

## I.5 Team Composition and the Reality of Individual Accountability

The team has multiple members. The individual defense format means that free-riding is structurally penalized. Everyone on the team needs to be able to talk fluently about the full project, not just the piece they personally built. Prof. Austern stated explicitly that she gives different questions to different members of the same group, so coordinating answers in advance is not a viable strategy. If one teammate builds the learned model and another runs the epidemic simulations, both of them still need to understand the cost formulation, the dataset, the evaluation protocol, and the limitations discussion. Reading this document front to back once should be sufficient to ground anyone in the shared vocabulary and the current open questions.

---

---

# Part II: The Original Project Concept

This part captures what we walked into the meeting thinking the project would be. It is preserved here not because it is the final plan (it is not) but because understanding the drift from the original concept to what Prof. Austern pushed us toward is itself informative. Several of the original elements survived; others got reshaped; a few got dropped entirely.

## II.1 The Original High-Level Question

The original framing was about social segregation and pandemic containment. The leading question was: how do different metrics of social segregation change the optimal pandemic containment strategy, and which social segregation metric matters the most? The intuition behind this framing was that real-world social networks vary in how segregated they are along latent attributes (race, major, dormitory, year, etc.), and that this segregation might fundamentally change which containment strategies are most effective. A densely interconnected network with low segregation might respond very differently to targeted interventions than a network with strong homophilous clusters.

## II.2 The Original Segregation Metrics

Three structural metrics were on the table as candidate ways to quantify segregation:

**Normalized homophily ratio.** The tendency of nodes to form ties with same-group nodes, adjusted for group size imbalances. Raw homophily is misleading when one group is much smaller than another because small groups mechanically have fewer same-group ties available, so a normalization is required to make cross-network comparisons meaningful.

**Assortativity coefficient.** Newman's standard mixing measure, which is the Pearson correlation of some attribute (often degree, but can be any node attribute) across edges. Positive assortativity means nodes preferentially connect to similar nodes; negative assortativity means the opposite.

**Clustering coefficient.** Both local (per-node) and global (graph-wide) clustering coefficients were candidates. This measures triangle density, which captures the extent to which a node's neighbors are also neighbors of each other.

The original plan was to compute all three metrics across a set of networks and then ask which one best predicts the effectiveness gap between targeted and random containment strategies.

## II.3 The Original Intervention Strategies

The original proposal had four intervention strategies, all of them node-removal based:

1. **Random removal** as the baseline, representing no information used in targeting
2. **Degree-based targeting**, removing the highest-degree nodes first, as a classical heuristic from the network robustness literature
3. **Betweenness centrality targeting**, removing nodes with the highest betweenness centrality, as a stronger classical heuristic
4. **A GNN-based approach** that learns which nodes to remove from local structural information, serving as the learned-method component

All four strategies operated on nodes. The assumption was that "containment" corresponds to "remove a set of nodes and measure the reduction in epidemic spread on the residual graph."

## II.4 The Original Dataset Plan

The original dataset was Facebook100, a collection of 100 university Facebook networks collected at a fixed point in time, each representing the friendship graph of students at one college or university. The original plan was to select a handful of campuses (roughly five to ten) whose descriptive statistics differed substantially from each other, so that the cross-campus comparison would span a meaningful range of structural diversity rather than being stuck in a narrow regime.

## II.5 What Prof. Austern Kept, Reshaped, and Dropped

Prof. Austern's reactions to this original framing mapped onto the elements as follows. The high-level interest in epidemic containment on real social networks survived entirely. The dataset choice (Facebook100) was not challenged. The idea of comparing multiple strategies including a GNN-based learned approach was kept. However, the central operation (removing nodes) was reshaped into removing edges. The central scientific question was reshaped from "which segregation metric matters most" into "what is the lowest-cost policy for containment given feature information on vertices." And the cost dimension was introduced from scratch, because the original framing had no notion that different interventions have different costs.

We will see all of this in detail in Part III.

---

---

# Part III: The Meeting With Prof. Austern

This part is a faithful reconstruction of what happened in the meeting. It is written from the transcript and it preserves the order and substance of what she said. Direct paraphrases are marked; summarized material is presented as such. The purpose of this part is to let anyone who was not in the meeting come away with the same understanding as someone who was there.

## III.1 How the Meeting Opened

The meeting opened with us admitting that our ideas were raw and high-level, and that we wanted her help deciding which direction to take. She said she was there to help us figure out what was doable, but needed something a bit more concrete to react to. We offered to walk through the project verbally rather than share a written proposal. This was partly because the pre-proposal we had in hand was more aligned with our AC209B knowledge graph project than with a graphs class, and partly because the segregation/containment idea felt more naturally graph-theoretic and therefore more appropriate for a first conversation with her.

This opening turned out to be the right move, even though it felt uncomfortable at the time. She spent the next fifteen minutes engaging substantively with the containment idea. We never got to the second project because the conversation about the first one was too productive to interrupt.

## III.2 Her First Reaction to the Containment Idea

After we described the basic setup (several college networks, pandemic spreading via a simple SIR-like model, different containment strategies compared against a baseline), she articulated the general question back to us in her own words. Her paraphrase was something like: you want to look at epidemic spread on a social network and try to understand which containment strategy is most effective depending on the topology of the graph. She marked this as a "higher question" that was interesting in principle.

Then she immediately pushed back on the formulation. Her concern was that our original framing limited us to removing nodes, and she was not sure that removing nodes was the right frame for real pandemics. She said something close to: in real life we do not remove individuals. She acknowledged that there is a sense in which isolating a sick person is equivalent to removing their node from the graph, but she noted that this is only half of what real interventions look like. Real interventions also operate on the susceptible, not just the infected. And the tools that real interventions use are typically edge-based rather than node-based: you do not remove a person from society, you restrict which contacts they can have.

## III.3 The Pivot to Edge Removal

This is the central intellectual move of the meeting. Prof. Austern said, approximately: the things that were done in practice were removing edges outside of, say, the family circle. You do not delete the person, you restrict which of their edges are allowed to remain active. She framed this as a cleaner and more realistic object of study, and she posed a concrete question around it: how do you remove a minimum amount of edges in a way that is most effective?

This question reshapes the project. Under the original framing, the intervention was "pick a set of nodes and delete them." Under her framing, the intervention is "pick a set of edges and cut them, and ideally do it while removing as few edges as possible."

She acknowledged that this could be made formal in several ways. The simplest version is: find the smallest set of edges whose removal brings the expected epidemic size (or some other containment metric) below a target threshold. A richer version associates a cost with each edge and minimizes the total cost rather than the cardinality of the removed set. The richer version is the one she seemed more interested in.

## III.4 The Introduction of Edge Costs

She introduced the cost idea as an extension of the edge-removal framing. Her logic was roughly: not all edges are equal. Removing the edge between two close friends in the same family is very costly (socially and economically) compared to removing the edge between two acquaintances who barely talk. A containment policy that ignores this asymmetry is unrealistic. The appropriate object is therefore a cost function on edges.

She suggested that the loss function for the optimization could be defined as the sum of the costs of all removed edges, subject to a containment constraint (such as "the expected fraction of the population ultimately infected must be below some threshold"). This is a constrained optimization: minimize total edge-removal cost such that the residual graph, when subjected to an epidemic simulation, does not exceed the threshold.

This framing connects cleanly to classical combinatorial optimization on graphs (minimum cut problems, network interdiction, etc.), though she did not name any specific prior literature in the meeting.

## III.5 The Question of Where Costs Come From

Having introduced costs, she then asked a question she did not answer: where do these costs come from? She said that if we had data that already annotated edges with cost information, we could just use it, but typically we do not have such data directly. She gave examples of what a cost proxy could be based on:

- **Geography.** The physical distance between two nodes. Edges between geographically close people are more costly to remove because those people interact more often and depend on each other more. Edges between geographically distant people are less costly.
- **Communication frequency.** How often two people actually interact. An edge between two people who communicate daily carries a higher cost than an edge between two people who communicate once a year. She described this as a noisy proxy for edge importance.

She noted that none of these proxies are perfect and that in practice we would only have noisy information about the true cost of removing each edge. She suggested two ways to handle this:

1. Build an idealized model in which we assume access to some oracle weights, and then discuss how such weights would actually be obtained in practice.
2. Alternatively, evaluate a posteriori the policies that were drawn in practice during real outbreaks and see how effective they were given what we know now.

The first option is the cleaner one for a project of this scope. The second is more ambitious and depends on having access to labeled ground-truth data, which we probably do not.

## III.6 The Dot Product Proxy for Edge Importance

Later in the meeting, when we asked how to frame the problem, she came back to edge importance and made a more specific suggestion. She said that if we have feature information on each vertex (such as demographic attributes, friend-of-friend counts, or anything else), a natural proxy for the importance of an edge $(u, v)$ is some function of the similarity between the feature vectors of $u$ and $v$. Her specific suggestion was a dot product or a sigmoid of a dot product. The intuition: if two nodes have very similar feature vectors, they are probably closer in a real social sense, so the edge between them is probably more important (and therefore more costly to remove).

This is worth pausing on because it is a piece of theoretical infrastructure that ties several things together at once:

- It gives us a principled way to derive edge costs from node features, which solves the "where do costs come from" problem.
- It connects naturally to learned representations, because feature vectors could be learned embeddings rather than raw attributes.
- It gives us a concrete experimental knob: we can vary the function that maps node pairs to costs and see how sensitive our results are to this choice.
- It gives the GNN component a natural home, because a GNN can learn node features that induce an edge-cost landscape, and then we can optimize containment under that induced cost structure.

## III.7 The Call to Narrow the Scope

Multiple times during the meeting, Prof. Austern emphasized that the scope needed to be narrow and concrete. She said, approximately: you want to have a concrete plan and narrow it down in a way that is manageable. She was not asking us to do less work; she was asking us to be specific about what we would do rather than vague about many things. The distinction matters. A project that says "we will run several different models under several different assumptions" is underspecified. A project that says "we will run the SIR model and the SIS model, under two specific edge-cost proxies, with three robustness perturbations" is well-scoped.

She reinforced the scope point by listing things we could do but did not need to do all of. This was meant as idea generation, not as a checklist. The items she listed were:

- Vary the underlying graph topology (test the methods on graphs with high-hub structure, graphs with dispersed structure, synthetic graphs with known properties)
- Switch the epidemic model from SIR to SIS and see how results change
- Introduce partial compliance (e.g., only 80% of people respect the policy)
- Introduce policy granularity (e.g., "all edges beyond a k-hop neighborhood are removed" rather than individually chosen edges)
- Compare simulation results against what was actually done in real-world outbreaks

She explicitly said: you do not need to do everything I just said, I am giving you ideas. The point is that you get to choose what you want to do, as long as the scope is reasonable and the discussion of results is thoughtful.

## III.8 The Literature Pointer

Midway through the meeting, she suggested we do a quick literature search on "networks and COVID-19" before committing to a direction. She noted that there are a lot of papers in this space, including work that built social networks of the United States and evaluated the effectiveness of different state-level policies (such as when and how states cut contact with each other during the pandemic). She did not ask us to read this literature exhaustively. She asked us to get a sense of what has been done and what has not been done, so that we could position our contribution appropriately.

This was paired with a general pointer about where our project should sit in relation to prior work. She was not expecting novelty in the research sense. She was expecting awareness. The project should not reinvent something that has already been done, and we should have a rough sense of whether any specific piece of our plan is something we are rediscovering or something that is genuinely underexplored.

## III.9 What She Wanted the Scientific Question to Be

Near the end of the conversation, she articulated what she thought the central scientific question should be. Her framing, paraphrased: the scientific question is "what is the lowest-cost policy" for containment, given that you have feature information on each vertex. This is a tighter and more rigorous version of our original "which segregation metric matters most" framing, and it shifts the project from being primarily descriptive (comparing metrics across networks) to being primarily prescriptive (finding the best policy under a cost constraint).

The shift is worth underlining. Under the original framing, the output of the project is a ranking of structural metrics by their predictive value for containment effectiveness. Under her framing, the output of the project is a proposed containment policy, a characterization of when it performs well, a comparison to simpler baselines, and a discussion of its implementability.

This is a significantly cleaner project structure. It also gives the learned-method component a natural home: a learned policy is a natural place for a GNN or similar graph-based model to contribute.

## III.10 The Reinfection and Model-Choice Discussion

Toward the end of the meeting, she brought up the question of which epidemic model to use. She noted that COVID-19 is not well modeled by SIR because recovered individuals do not stay immune forever; they become susceptible again after a period of time. The model that captures this is SIS (susceptible-infected-susceptible), or one of several closely related variants. She mentioned this not to insist we use SIS, but to flag that the choice of model is itself a decision we should think about and potentially vary. The robustness version of this is: run the main analysis under one model, then repeat it under a different model, and see whether the conclusions change.

This is a piece of advice about how to structure the results discussion. If the conclusions are stable under model choice, the project is stronger. If they are not, the discussion becomes about when and why the conclusions flip, which is itself interesting.

## III.11 The Closing of the Meeting

Near the end, we asked her to confirm our scoping instinct: one containment model, one or two realistic policy variants, fewer robustness checks, and a solid discussion in the report. She said yes to this, and then added more suggestions on top. Specifically, she said that the things we can vary are not just the policies but also the graphs themselves (via simulation of alternative topologies) and the epidemic models (via SIR vs SIS). She said the final product is not a definitive answer and not a paper. It is a full-picture understanding of a specific method and a nuanced conversation about the results. She closed with an open invitation to office hours for follow-up questions.

## III.12 What Was Not Discussed

A few things were notably not discussed in the advisor meeting. This matters because their absence tells us what we still need to clarify. Some of these gaps were later filled by the class-wide discussion; those items are marked.

- **The specific scoring criterion for the report.** She did not tell us how long the report should be, what its structure should look like, or which sections are mandatory. *(The class discussion added that the report must be accompanied by reproducible materials such as a GitHub repository, but the length and formatting remain unconfirmed.)*
- **The format of the lightning talk.** She mentioned it only briefly in the advisor meeting. *(The class discussion filled in the details: five minutes, in one of the last two classes, judged on presentation quality not on results, explicitly low-stakes.)*
- **Specific papers to read.** She pointed at "networks and COVID-19" as a general area but did not name any specific authors or titles. *(Still open.)*
- **Whether the GNN component is strictly required.** She never said "you must use a GNN." The project is meant to engage with the "learning on networks" portion of the course, and a GNN is the most obvious way to do this, but she did not mandate the specific form. We should confirm whether a learned method on graphs that is not strictly a GNN would also be acceptable. *(Still open.)*
- **How to handle the team split.** She did not give guidance on how work should be divided among team members, other than the implicit guidance that everyone must understand the whole project for the oral defense. *(The class discussion added that she gives different questions to different members, which reinforces the point but does not give guidance on work division.)*
- **The specific oral defense format.** The advisor meeting only said "three questions per student." *(The class discussion filled this in: two content questions plus one deeper question, approximately 15 minutes, in person, with no slides or presentation required from the student.)*

---

---

# Part IV: The Refined Problem Framing

This part states, as cleanly as we can, what the project is now, given what was said in the meeting. It does not lock in decisions that are still open. It states what has been fixed, what has been reframed, and what remains to be decided.

## IV.1 The Central Question, Restated

The central scientific question, as it stands after the meeting, is roughly the following.

> Given a social contact graph in which vertices carry feature information and edges carry costs (possibly derived from those features), what is the lowest-cost set of edges whose removal brings an epidemic on the residual graph under a containment target?

This is the core question. Everything else in the project exists either to make this question precise, to propose methods for answering it, or to discuss the realism and limitations of those methods.

The question is prescriptive (it asks for a policy) rather than descriptive (which would just characterize how the epidemic spreads under no intervention). It is constrained (there is a containment target that must be met) rather than unconstrained. And it is cost-aware (removing edges is not free) rather than cost-blind (which would ignore the asymmetry between cheap and expensive edges).

## IV.2 What Is Fixed

The following elements are fixed after the meeting. By "fixed" we mean Prof. Austern either explicitly endorsed them or treated them as obvious and did not push back.

**The general domain.** We are studying epidemic containment on social networks.

**The intervention modality.** We are removing edges, not nodes. (Nodes may still be removed in specific cases such as isolating the confirmed infected, but the central mathematical object of intervention is the edge.)

**The cost structure.** Each edge has a cost. The total objective involves minimizing the sum of costs of removed edges, subject to a containment constraint.

**Feature information on vertices.** Vertices carry features, and those features may be used to derive edge costs, edge importance scores, or inputs to learned methods.

**At least one learned method.** Because the project is the primary way the course evaluates the "learning on networks" material, at least one of our intervention strategies should be learned rather than hand-designed. The natural candidate is a GNN-based approach, though Prof. Austern did not explicitly mandate the specific form.

**Simulation-based evaluation.** We will run simulations of some epidemic process on the residual graph and measure the outcome. This is the evaluation substrate.

**The report and oral defense format.** We know we need to produce a written report and defend it individually in an oral exam.

**The lightning talk.** We know there is a five-minute group talk in one of the last two classes.

## IV.3 What Is Reframed

The following elements changed in kind during the meeting. They are not gone; they are repositioned.

**From node removal to edge removal.** The original intervention was node-based. The refined intervention is edge-based. This is the biggest single shift in the project.

**From "which segregation metric matters most" to "what is the lowest-cost policy."** The original framing was a comparison of descriptive structural metrics. The refined framing is a constrained optimization problem. The segregation metrics have not disappeared; they are now potentially useful as either (a) ways to characterize which graphs our methods perform well on, or (b) features that go into the cost function, or (c) topics for the results discussion. But they are no longer the central object of study.

**From "compare strategies" to "propose a policy and discuss its realism."** The original framing put four strategies on a level playing field and compared them. The refined framing gives us one or two main proposed policies and a set of baselines, and asks us to discuss the realism of our proposed policies in depth.

## IV.4 What Remains Open

The following elements are deliberately left open. These are decisions the team needs to make together, and they should be made before we commit to any code.

**The specific epidemic model or models.** SIR, SIS, SEIR, SEIRS, and others are all candidates. Prof. Austern flagged that COVID is closer to SIS than SIR, but did not mandate any specific model. We may use one as primary and another as a robustness check.

**The specific cost function or functions.** Several options were suggested: geographic distance, communication frequency, a dot product of node features, a sigmoid of a dot product, or even an oracle cost assumed for idealized analysis. We have not chosen among these.

**The specific containment target.** We need a concrete containment constraint, such as "the final epidemic size must be below 20% of the population" or "the peak number of concurrent infections must stay below hospital capacity." The choice of target shapes the optimization.

**The specific baseline strategies to compare against.** The original list (random, degree, betweenness, GNN) was node-based. The edge-based reformulation means we need edge-based baselines. Candidates include random edge removal, highest-weight edge removal, edges with highest product of endpoint degrees, edges on shortest paths, edges on many betweenness-heavy paths, spectral edge importance (effective resistance), and so on. We have not settled on a set.

**The specific learned method.** The GNN can be used in several ways: to score edges directly, to learn node embeddings that induce an edge cost function, to learn a policy that selects edges sequentially, or to predict containment outcomes so we can optimize against them. These are all viable. None has been chosen.

**The number of campuses and which ones.** Prof. Austern did not object to our choice of Facebook100 but also did not weigh in on how many campuses to use or how to pick them. This is our decision.

**The robustness dimensions to vary.** She listed many options (graph topology, epidemic model, partial compliance, policy granularity). The ones we pick will depend on what fits in the report timeline.

## IV.5 The Invariant Properties of a Good Final Product

Whatever we decide on the open questions, the final product should have certain invariants if it is going to meet Prof. Austern's standard. These are:

**A clearly stated scientific question.** One sentence, at the top of the report, that a reader can understand without background. This question anchors everything.

**A clearly stated optimization problem.** The scientific question translated into formal terms (what is the objective, what is the constraint, what is the decision variable, what is the feasible set).

**A set of methods, at least one of which is learned.** Each method described precisely enough that a reader could in principle reimplement it.

**Simulation results.** Outcomes of running the methods on one or more real datasets and (if we decide to include them) on synthetic perturbations of those datasets.

**A substantive discussion section.** This is where the project lives or dies in Prof. Austern's eyes. It must honestly address what worked, what did not, what assumptions are fragile, and what the limitations are.

**An implementability analysis.** This is where we discuss how our proposed policies would (or would not) translate to a real-world intervention. Prof. Austern repeatedly mentioned this as something she cares about.

---

---

# Part V: Graph-Theoretic Formulation

This part lays out the formal graph object we are working with and names the quantities we will need. Nothing here is controversial; it is the mathematical scaffolding that lets the rest of the project be precise.

## V.1 The Graph Object

Let $G = (V, E)$ be an undirected graph where $V$ is the set of vertices (representing individuals in a college's Facebook network) and $E$ is the set of edges (representing Facebook friendships at the time the data was collected). For Facebook100 the graph is undirected because Facebook friendships are mutual.

Let $n = |V|$ be the number of vertices and $m = |E|$ be the number of edges. These quantities vary across campuses in the Facebook100 dataset; some networks have a few thousand vertices, others have tens of thousands.

Each vertex $v \in V$ carries a feature vector $x_v \in \mathbb{R}^d$. The features in Facebook100 include attributes like student status, dorm, year, major, gender, and high school. These are categorical, so in practice we will one-hot encode them or embed them. Some attributes are missing for some nodes.

Each edge $e = (u, v) \in E$ carries (or will carry, after we derive it) a cost $c_e \geq 0$ representing how expensive it is to remove that edge under our policy.

## V.2 The Residual Graph After an Intervention

A containment policy is a subset of edges $S \subseteq E$ that we choose to remove. The residual graph is $G_S = (V, E \setminus S)$. All epidemic simulations and all outcome measurements are computed on $G_S$, not on $G$.

The cost of the policy $S$ is $C(S) = \sum_{e \in S} c_e$.

The central optimization problem (informally stated) is to find the policy $S$ that minimizes $C(S)$ subject to a constraint that the epidemic outcome on $G_S$ is below some threshold.

## V.3 The Epidemic Outcome

We need a way to turn "epidemic spread on the residual graph" into a single number that we can constrain. Several choices are possible:

**Final epidemic size.** The expected number (or fraction) of vertices that are ever infected over the course of the simulation.

**Peak prevalence.** The maximum number of simultaneously infected vertices at any time step during the simulation.

**Time to extinction.** How long it takes for the epidemic to burn out.

**Effective reproduction number.** The average number of secondary infections caused by each infected individual, on the residual graph.

These are not equivalent. A policy that reduces the final epidemic size may still allow a high peak, which would be catastrophic from a hospital-capacity standpoint. A policy that flattens the peak may extend the duration of the outbreak. We need to pick which outcome is the primary one and justify the choice.

## V.4 Structural Quantities Per Graph

For each graph (either a real Facebook100 campus or a synthetic perturbation), we will want to compute a standard set of descriptive statistics:

- Number of vertices and edges
- Density (the fraction of possible edges that exist)
- Degree distribution (mean, variance, maximum, skewness, whether it is consistent with a power law)
- Connected components and the size of the giant component
- Average shortest path length and diameter
- Global and average local clustering coefficients
- Degree assortativity (Newman's $r$)
- The segregation metrics from the original proposal (normalized homophily along each categorical attribute)
- Modularity under a community detection algorithm

These descriptive statistics are useful for two reasons. First, they let us characterize the networks we are working with and explain why some behave differently than others. Second, they may feed back into the policy design: a GNN that learns to predict edge importance can condition on these features.

## V.5 Subgraph Statistics and Local Features

For the learned method, we will need per-node and per-edge local features. These include:

**Per-node features.** Degree, local clustering coefficient, average neighbor degree, number of triangles the node participates in, eigenvector centrality or PageRank, and any attributes from the Facebook100 metadata.

**Per-edge features.** Whether the edge is within a cluster or between clusters, the product of endpoint degrees, the number of common neighbors (Jaccard index or related), whether the edge is a bridge or close to one (edge betweenness), whether the endpoints share attributes (homophilous or heterophilous).

These features can serve as inputs to a classical ML baseline, as inputs to a GNN, or as hand-designed scoring functions for a heuristic policy.

## V.6 Null Models

For any claim that the structure of a real graph matters, we should compare against null models. The standard ones are:

**Erdős-Rényi random graphs** with matched edge count. The weakest null; it preserves nothing except the expected density.

**Configuration model** with matched degree sequence. Preserves the degree distribution but destroys all higher-order structure. This is the standard null for asking "is this graph's clustering or assortativity more than you would expect from its degree distribution alone?"

**Stochastic block model** fit to the attribute structure. Preserves the block-level mixing patterns (how different communities connect to each other) but randomizes within blocks. This is a stronger null that isolates within-community structure.

Running a few of our methods on null graphs is not mandatory, but it is a valuable robustness check that Prof. Austern is likely to appreciate. If our methods perform well on real networks but poorly on matched nulls, that tells us something about what structural property the methods exploit.

## V.7 The Weighted Extension

If we use edge costs that are not uniform (which we probably should), the graph effectively becomes edge-weighted. Many standard graph algorithms have weighted versions: weighted betweenness centrality, weighted shortest paths, weighted spectral analysis. We will need to be consistent about whether we compute structural statistics on the unweighted graph, on the weighted graph, or both.

---

---

# Part VI: Epidemic Models

This part surveys the epidemic models that are candidates for our simulation substrate. It does not pick one. It describes each one, states its assumptions, and flags its strengths and weaknesses in the context of our project.

## VI.1 The SIR Model

The Susceptible-Infected-Recovered model is the simplest reasonable compartmental epidemic model on a graph. Each vertex is in exactly one of three states at any time:

- **S (Susceptible):** has not yet been infected
- **I (Infected):** is currently infected and can infect neighbors
- **R (Recovered):** has been infected, has recovered, and is permanently immune

At each time step, every infected vertex attempts to infect each of its susceptible neighbors with some probability $p$ per edge, and every infected vertex recovers (transitions to R) with some probability $\gamma$ per time step. Once a vertex is in R, it stays in R forever.

The parameters are the transmission probability per edge per time step, the recovery probability per time step, and the initial set of seed infections. The final epidemic size is well-defined because the process eventually terminates (every vertex is in S or R at the end).

**Strengths.** Simple, well-understood, has closed-form analytical results for some graph classes, and is the standard starting point for epidemic modeling on networks.

**Weaknesses.** Assumes permanent immunity, which is false for COVID. Assumes constant transmission probability per contact, which ignores heterogeneity.

## VI.2 The SIS Model

The Susceptible-Infected-Susceptible model differs from SIR in exactly one way: recovered individuals return to the susceptible state rather than becoming permanently immune. There are only two compartments (S and I), and vertices cycle between them.

This is a much better fit for modeling diseases where immunity wanes, which is most relevant in long-running outbreaks like COVID. It is the model Prof. Austern explicitly flagged as closer to reality.

**Strengths.** Realistic for diseases with waning immunity. Still mathematically tractable. Can exhibit endemic steady states (an infection that persists forever rather than burning out).

**Weaknesses.** The notion of "final epidemic size" is less clean because the process does not terminate. Instead, one typically measures steady-state prevalence, which is the long-run average fraction of infected vertices. This makes some comparisons across policies trickier.

## VI.3 The SEIR Model

The Susceptible-Exposed-Infected-Recovered model adds an "exposed" compartment between susceptible and infected. The exposed state represents the incubation period during which an individual has been infected but is not yet infectious. Vertices transition $S \to E \to I \to R$.

**Strengths.** More realistic for diseases with a meaningful incubation period (including COVID). Allows interventions to operate on the E compartment, which is policy-relevant (contact tracing targets people who have been exposed but are not yet symptomatic).

**Weaknesses.** More parameters to specify. More complex analytically. For our project it may be more realism than we need, unless we specifically want to study interventions that target exposed but not-yet-infectious individuals.

## VI.4 The SEIRS Model

Combines SEIR with the reinfection dynamics of SIS: $S \to E \to I \to R \to S$. This is arguably the most realistic model for COVID but also the most parameter-heavy.

## VI.5 Independent Cascade and Linear Threshold

These are two discrete cascade models from the information diffusion literature that are often used as alternatives to SIR-family models on networks. They have slightly different dynamics (a vertex gets one chance to infect each neighbor, or a vertex becomes infected once its fraction of infected neighbors crosses a threshold). They are worth knowing about because the network science literature sometimes uses them as proxies for epidemic spread, and some classical containment results (influence maximization, the Kempe-Kleinberg work) are formulated in these models.

## VI.6 The Open Question of Which Model to Use

Prof. Austern did not mandate a specific model. What she did say is that the choice of model is one of the robustness dimensions, and that results that are stable across model choices are more compelling than results that depend sensitively on the choice. The practical implication: pick one model as the primary (the one you run most experiments with) and use at least one other model as a secondary to check whether conclusions survive.

Which one is the primary is an open question. Arguments for SIR: simplest, most standard, easiest to reason about. Arguments for SIS: more realistic for COVID, which is our motivating example. Arguments for SEIR or SEIRS: most realistic, but possibly overkill.

A reasonable heuristic: use SIR as the primary because it is cleanest, and use SIS as the secondary robustness check because it captures the one feature (reinfection) that Prof. Austern specifically flagged. This is a tentative suggestion and not a commitment.

## VI.7 Stochastic vs. Deterministic Simulation

Both SIR and SIS have deterministic (mean-field) and stochastic (per-vertex) versions. On a finite graph, the stochastic version is more realistic because the mean-field approximation breaks down when the graph has a skewed degree distribution. We will run stochastic simulations, which means each epidemic realization is different, and we need to average over many runs to get reliable estimates. This multiplies the compute cost of the evaluation but is necessary for honest error bars.

## VI.8 Initial Seeding

Every simulation needs a choice of initial seed set: the vertices that start out infected at time zero. Options include:

**Uniformly random seeding.** Pick a small number of vertices at random. This is the standard choice and has the virtue of not biasing toward any particular node type.

**Adversarial seeding.** Pick the vertices whose infection would lead to the worst outcome (typically the highest-degree or most-central vertices). This gives a worst-case analysis.

**Multiple independent seedings.** Average over many random seed sets to reduce variance.

For the project, multiple independent random seedings is the cleanest choice. We pick (say) a small number of seed vertices uniformly at random, run the epidemic, record the outcome, repeat many times, and average. This gives us a stable estimate of expected outcomes per policy.

## VI.9 Computational Cost

Stochastic epidemic simulations on Facebook100 graphs (which have up to tens of thousands of vertices) are not free. A single run is fast, but we will need many runs. The full evaluation involves: several candidate policies, each with several values of its tunable parameters, on several campuses, averaged over many random seedings, possibly under both SIR and SIS. This multiplies out to tens or hundreds of thousands of simulation runs. We should estimate compute cost early and plan accordingly. Everything here is CPU work; no GPU needed for the simulations themselves (GPUs only come in if we train a GNN).

---

---

# Part VII: Intervention Strategies

This part enumerates the candidate strategies for choosing which edges to remove. These are the methods we will be comparing. The list is not final, and Prof. Austern made clear that we should go beyond degree (and by extension beyond the classical strategies) in at least one of our main methods.

## VII.1 Baseline: Random Edge Removal

Pick a random subset of edges and remove them. Vary the size of the subset and record the containment effect.

This is the trivial baseline. Every other method has to beat it. In cost-aware settings, random removal can be done in two variants: uniform random (every edge equally likely) or cost-weighted random (edges with lower cost are more likely to be picked).

Random removal is useful because it tells us how much of the observed containment effect is due to "removing enough edges to degrade connectivity" versus "removing the right edges." If a targeted method barely beats random, the targeting is not doing much work.

## VII.2 Classical Heuristic: High-Weight Edge Removal

Remove edges ranked by some structural score. Several candidate scores exist:

**Edge betweenness centrality.** The fraction of shortest paths in the graph that pass through each edge. Edges with high betweenness are bottlenecks; removing them increases path lengths and disconnects parts of the graph. Classical result: targeted removal by edge betweenness is highly effective at disconnecting graphs, but it is expensive to compute on large networks.

**Spectral edge importance.** The contribution of each edge to the spectral gap or to the effective resistance of the graph. Grounded in spectral graph theory.

**Endpoint-degree product.** Remove edges where both endpoints have high degree. A cheap proxy for "important" edges.

**Bridge detection.** Remove edges that are bridges (whose removal disconnects the graph). Trivial to detect; their removal is maximally structural.

These are hand-designed, require no training, and serve as strong classical baselines. Prof. Austern explicitly said to go beyond degree, which implies that pure degree-based methods are necessary baselines but not sufficient as the main method.

## VII.3 Cost-Aware Heuristics

Once we have edge costs, many of the above heuristics can be cost-adjusted. For example: rank edges by (betweenness / cost) and remove the edges with highest ratio. This is "bang for buck" in a greedy sense: the edge with the highest structural importance per unit cost goes first.

A related approach is to set a total cost budget $B$, then greedily pick the most structurally important edges until the budget is exhausted.

Both of these are natural extensions of the classical heuristics to the cost-aware setting, and they are the obvious baselines to compare learned methods against.

## VII.4 Combinatorial Optimization Baselines

For small graphs, we can in principle solve the optimization problem exactly using integer programming: "find the minimum-cost subset of edges whose removal causes the containment metric to fall below the threshold." This is NP-hard in general, but modern solvers can handle moderate instances.

For our project, an exact solver is probably not viable on the full Facebook100 networks, but it may be useful as a benchmark on small synthetic graphs. If our heuristic and learned methods are within some factor of the exact optimum on small instances, that is reassuring.

## VII.5 Learned Method: A GNN-Based Policy

This is the learned-method component of the project. Several distinct architectures are possible; we describe them in general terms without choosing among them.

**Option A: GNN as edge scorer.** A GNN takes the graph and node features as input, produces node embeddings, and then scores each edge by a function of its endpoint embeddings (e.g., a dot product, a bilinear form, or a small MLP). The scored edges are ranked, and the top-cost-adjusted ones are removed. Training: on synthetic or held-out graphs where we know which edge removals produce good containment outcomes, train the GNN to predict containment improvement per edge.

**Option B: GNN as node embedder feeding a cost function.** The GNN produces node embeddings, and edge costs are derived from node pair similarities (the dot product proxy Prof. Austern suggested). Then a heuristic (like "remove the lowest-cost edges first") runs on top of the learned cost structure. Training: embeddings are learned to make downstream containment effective.

**Option C: GNN as sequential policy.** The GNN is used inside a sequential decision-making loop. At each step, the model picks one edge to remove, the graph updates, and the model picks the next edge. Training: reinforcement learning, with the reward being containment effectiveness per unit cost. This is the most ambitious option and probably too complex for a semester project, but it is worth noting.

**Option D: GNN as outcome predictor.** The GNN predicts the expected epidemic outcome on the residual graph, given a proposed edge removal set. Then a classical optimizer uses the GNN's predictions as a surrogate objective. Training: supervised learning on (residual graph, epidemic outcome) pairs generated by simulation.

We have not chosen among these options. Option B is probably the cleanest because it fits naturally with Prof. Austern's dot-product suggestion and minimizes the learning burden (the GNN only has to learn embeddings, not a full decision process).

## VII.6 The Policy Form Question

Separate from the algorithm that picks edges is the question of what form the resulting policy takes. Prof. Austern made a distinction during the meeting between edge-by-edge policies (where each edge is individually decided) and structural policies (where a rule like "remove all edges crossing department boundaries" is applied uniformly). Real-world policies are almost always structural because individual-edge enforcement is impossible at scale. She suggested a specific structural rule: restrict communication to a $k$-hop neighborhood, where edges beyond $k$ hops are removed.

This gives us another axis of policy design: not just "which edges does the algorithm pick" but "what kind of rule does the algorithm have to respect." An edge-by-edge method can be ideal and unimplementable; a structural rule is implementable but less flexible. Comparing the two in our results discussion is a natural move.

## VII.7 The Trade-off Frontier

Rather than picking a single cost budget, we probably want to trace out a Pareto frontier: for each cost budget from very small to very large, what is the best containment achievable by each method? This lets us see how the methods compare across the full range, not just at one arbitrary budget. The frontier is the natural visual object for the results section of the report: one curve per method, cost on the $x$-axis, containment on the $y$-axis.

---

---

# Part VIII: The Cost Formulation

This part goes into detail on how edge costs are defined, derived, and used. This is the piece of the project that is most exposed to design choices, because there is no single right answer and the choices affect the results.

## VIII.1 Why Costs Exist

Prof. Austern's motivation for introducing costs was realism. In any real intervention, some social contacts are cheap to sever (an acquaintance you barely see, a coworker in a different department) and some are very expensive (an immediate family member, a roommate, a best friend). A containment policy that ignores this asymmetry will tend to recommend unrealistic interventions (breaking up families to stop disease spread), and will also miss opportunities to contain the disease by cheap edge cuts that do not disrupt people's lives.

The cost formulation forces the method to be economical. It says: given that every edge cut has a price, find the cheapest set of cuts that still contains the epidemic.

## VIII.2 The Basic Mathematical Object

Let $c: E \to \mathbb{R}_{\geq 0}$ be a cost function on edges. For any subset $S \subseteq E$, the total cost is

$$C(S) = \sum_{e \in S} c_e.$$

The basic constrained optimization problem is

$$\min_{S \subseteq E} C(S) \quad \text{subject to} \quad \text{Outcome}(G_S) \leq \tau,$$

where $\text{Outcome}(G_S)$ is the expected epidemic outcome on the residual graph and $\tau$ is a containment target.

The dual formulation flips the optimization:

$$\min_{S \subseteq E} \text{Outcome}(G_S) \quad \text{subject to} \quad C(S) \leq B,$$

where $B$ is a cost budget. These two problems are related (any solution of one can be turned into a solution of the other by adjusting the thresholds), and in practice we may prefer the budgeted version because the budget is a more natural handle to sweep over.

## VIII.3 Candidate Cost Functions

Prof. Austern suggested several possible bases for defining $c_e$. We describe each one with its pros and cons.

### VIII.3.1 Uniform Cost

$c_e = 1$ for all edges. The simplest possible choice. It turns the cost-aware problem into the cardinality problem (minimize the number of edges removed). Useful as a baseline because it isolates the effect of having costs at all. Uninformative in itself but valuable as a reference point.

### VIII.3.2 Geographic Distance

If we had location data for each vertex, we could define $c_e$ as a function of the distance between the endpoints (e.g., inverse distance, so that nearby pairs are expensive and distant pairs are cheap). The intuition is that geographically close people interact more intensely. Prof. Austern noted this explicitly as a natural proxy.

The Facebook100 dataset does not directly include GPS coordinates, but it does include dormitory information for some nodes, which is a coarse proxy for physical co-location within a campus. Whether this is enough to derive a meaningful geographic cost function is an open question.

### VIII.3.3 Communication Frequency

If we had data on how often two people actually communicate (messages per day, wall posts, tagged photos, etc.), we could define $c_e$ as a monotone function of that frequency. More frequent communication $\Rightarrow$ higher cost. Prof. Austern flagged this as a natural but noisy proxy.

The Facebook100 dataset includes friendship edges but not communication volume per edge. So this proxy would require either assuming we had such data (and treating the costs as placeholders we would populate in a real deployment) or generating synthetic communication volumes by some plausible mechanism. Both are defensible.

### VIII.3.4 Feature Similarity via Dot Product

This is the specific suggestion Prof. Austern made. Let $x_u$ and $x_v$ be the feature vectors of the two endpoints of an edge. Define

$$c_e = f(\langle x_u, x_v \rangle)$$

where $f$ is some monotone function, possibly a sigmoid. Nodes with similar feature vectors get high edge costs (because they are "similar," which is a stand-in for "socially close"). Nodes with dissimilar feature vectors get low edge costs.

This proxy has several nice properties:

- It is computable directly from data we already have (Facebook100 includes categorical features like year, dorm, major, etc.).
- It connects cleanly to learned embeddings: the features can be replaced with GNN-learned embeddings, which gives the GNN a natural role in shaping the cost function.
- It is interpretable: we can report which edges got high costs under this proxy and check if they correspond to intuitively "close" relationships.
- It produces a continuous cost spectrum rather than a binary classification.

Weaknesses: the choice of $f$ is arbitrary. The normalization of $x_u$ and $x_v$ affects the scale. And the proxy assumes that feature similarity is a good stand-in for social closeness, which is itself an empirical claim that might not hold on every network.

### VIII.3.5 Oracle Costs from a Known Distribution

For robustness analysis, we could assume costs are drawn from a known distribution (e.g., log-normal, matching some assumed distribution of real-world edge importances) and see how the methods perform. This disconnects the cost from the data entirely and lets us ask "if costs looked like this, which method would do best?"

### VIII.3.6 Adversarial Costs

We could also study how methods perform when costs are adversarially chosen to hurt each method. This is relevant because in practice the cost distribution may not be favorable to our chosen method's structural assumptions. Adversarial cost analysis is more ambitious than we probably have time for, but worth flagging.

## VIII.4 The Choice of Cost Function Is Part of the Methodology

Because the cost function shapes the optimization problem, the choice of cost function is itself a methodological decision. The report should defend the choice explicitly. We do not have to commit to one cost function; we can run the main analysis with one and use one or two alternatives as robustness checks. This gives us more to discuss in the results section ("our main method beats the baselines under the feature-similarity cost function, but the gap closes under the geographic cost function; here is why we think this happens...").

## VIII.5 Normalization and Scale

One technical detail: if we use cost budgets to compare across graphs, the budgets must be comparable. On a graph with many edges, a budget of 100 is a drop in the bucket. On a graph with 500 edges, it is a massive chunk of the graph. So "a budget of 100" is not a meaningful phrase on its own.

The fix is to normalize budgets as a fraction of the total cost of the graph ($\sum_{e \in E} c_e$). A budget of "5% of total cost" is comparable across graphs. Similarly, containment targets should be expressed as fractions of the total population rather than absolute numbers.

## VIII.6 The Interaction Between Costs and Containment

One subtle point: the containment effectiveness of removing an edge is not independent of its cost. High-cost edges (under the feature-similarity proxy) are precisely the edges between socially similar people, and the edges between socially similar people are often within-community rather than between-community. The classical structural wisdom is that between-community edges (bridges) are the most effective to remove for containment, because they connect otherwise isolated clusters. If our cost function makes between-community edges cheap, then the cost-aware policy and the structural policy are aligned. If it makes them expensive, they conflict.

This interaction is itself worth investigating in the results section: does the feature-similarity cost function align with or oppose classical bridge-based containment wisdom? Under what conditions?

---

---

# Part IX: Edge Importance and Feature Information

This part focuses specifically on the dot-product proxy Prof. Austern suggested, because it is a central enough idea to warrant its own treatment. It also discusses the broader question of how node features feed into the project.

## IX.1 The Suggestion, Restated

Prof. Austern said: if we have feature information on vertices, a natural proxy for edge importance is some function of the dot product of endpoint features, possibly passed through a sigmoid. The intuition is that similar features indicate social closeness, and socially close ties are more important to preserve.

Mathematically: for edge $e = (u, v)$, the proxy importance is

$$w_e = \sigma(\langle x_u, x_v \rangle)$$

where $\sigma$ is the sigmoid function, though other monotone functions are also reasonable. Importance $w_e$ and cost $c_e$ are essentially the same quantity: high importance means high cost of removal.

## IX.2 Why This Framing Is Useful

Several reasons this framing is structurally important to the project:

**It provides a principled way to derive costs from data.** Without a proxy like this, we would have to either assume oracle costs or use the Facebook100 metadata in ad hoc ways. The dot product gives us a clean mathematical object.

**It connects to learned embeddings.** If $x_u$ and $x_v$ are raw features, this is one thing. If they are embeddings produced by a GNN, the GNN is effectively learning to shape the cost function. This gives us a natural home for the GNN: rather than having the GNN score edges directly, we have it learn embeddings, and the edge cost drops out of the embedding geometry. The downstream containment policy then operates on the cost structure the GNN induced.

**It is interpretable.** We can visualize the learned cost landscape and check that it makes sense. Edges between people with similar attributes get high costs; edges between people with different attributes get low costs. We can validate this against our intuition.

**It is differentiable.** If we want to train end-to-end (e.g., learn embeddings such that the downstream containment policy performs well), the dot-product formulation gives us a smooth cost function we can differentiate through.

## IX.3 What Features Do We Actually Have?

Facebook100 provides several categorical attributes per vertex: student vs faculty status, dormitory, year of graduation, major, gender, and high school. Not all attributes are present for all vertices (missingness is a real issue in this dataset). We need to decide how to represent these.

**One-hot encoding.** The simplest representation. Each categorical attribute becomes a vector of binary indicators. The full feature vector is the concatenation of all the one-hot encodings. Pros: simple, standard, preserves all information. Cons: high-dimensional, and the dot product of two one-hot vectors just counts matching attributes, which is a crude similarity measure.

**Learned embeddings.** Each attribute is mapped to a learned embedding vector of some lower dimension, and these are concatenated to form the feature vector. Pros: more flexible, can capture non-trivial relationships (e.g., "certain combinations of major and year are more socially cohesive than others"). Cons: requires training, and we need a training signal.

**GNN-produced embeddings.** The features are not based on attributes at all; they are the output of a GNN that has processed the graph. Pros: encodes structural information (a node's role in the graph) rather than just its attributes. Cons: requires more machinery and a training objective.

A reasonable approach is to use one-hot encodings for the baseline analysis and learned embeddings (either from an attribute embedding layer or from a GNN) for the learned-method analysis. This is consistent with how a learned graph component naturally integrates into the project.

## IX.4 Handling Missing Features

Facebook100 has missing data. Some vertices are missing dorm information, some are missing year, etc. We need a principled way to handle this. Options:

**Drop the vertex.** Too aggressive; it distorts the graph structure.

**Impute the missing attribute.** Mean imputation, mode imputation, or learned imputation via methods designed for graph data.

**Use a "missing" indicator as its own category.** Add an extra dimension to the one-hot encoding that fires when the attribute is missing. This preserves all vertices and treats missingness as informative.

The last option is the cleanest for our purposes. It does not require imputation and it lets the downstream method decide how to treat missing attributes.

## IX.5 Normalizing the Dot Product

Before taking a dot product of two feature vectors, we should normalize them. Without normalization, nodes with high-magnitude feature vectors (e.g., nodes that happen to have non-missing values on many attributes) will have systematically higher dot products, which is a spurious effect. L2 normalization (dividing each vector by its own norm) is the standard fix. The dot product of two L2-normalized vectors is the cosine of the angle between them, bounded in $[-1, 1]$.

If we want to use the raw dot product as a cost (rather than passing it through a sigmoid), we should normalize first. If we use a sigmoid, normalization is less critical but still recommended for numerical stability.

## IX.6 The Feature-Cost Function as a Design Knob

We can treat the choice of feature-to-cost mapping as one of the axes we vary in the results section. Specifically, we can compare:

- **Binary match count:** the number of attributes on which the two endpoints share a value.
- **Cosine similarity on one-hot features:** closely related to the above but continuous.
- **Learned embedding similarity:** similarity on GNN-produced embeddings.
- **Oracle cost:** a synthetic cost drawn from a known distribution, independent of features, as a sanity check.

If our methods perform similarly under all these proxies, the results are robust. If they diverge, the divergence is itself interesting and worth discussing.

---

---

# Part X: Ideal Policies vs Realistic Policies

This part addresses a theme that came up repeatedly in the meeting: the distinction between policies that are mathematically optimal and policies that could actually be enforced. Prof. Austern cares about this distinction and she will ask about it in the oral defense.

## X.1 The Core Distinction

An ideal policy is one that the optimization algorithm is allowed to produce without any constraints on its form. It can say "remove edge $(u, v)$ and edge $(x, y)$ and edge $(a, b)$..." for any arbitrary subset of edges. Ideal policies achieve the best possible containment per unit cost in principle, but they are often impossible to enforce in the real world because specifying and enforcing individual edge-level rules across a population is impractical.

A realistic policy is one that can be expressed as a simple rule that a government or institution could communicate and enforce. Examples:

- "Do not travel more than $k$ kilometers from your home."
- "Do not interact with people more than $k$ edges away from you in the friendship graph."
- "Do not attend events with more than $N$ people."
- "Only interact with members of your household and immediate coworkers."

These rules have the form of threshold constraints or structural constraints rather than arbitrary edge sets. They are implementable because they can be communicated in a sentence and checked by individuals.

## X.2 The Trade-off

Ideal policies dominate realistic policies in raw performance (because realistic policies are a strict subset of ideal policies, so the best ideal policy is at least as good as the best realistic one). But realistic policies are the only policies that actually happen. Any real-world intervention is expressed in the form of a simple rule, not in the form of a list of individual edges to remove.

The interesting question for the project is therefore not "which ideal policy is best" but "how much do we lose by constraining ourselves to realistic policies, and which realistic policies are closest to the ideal?" This is a cost-of-implementability question and it is exactly the kind of question Prof. Austern wants us to discuss.

## X.3 Candidate Realistic Policy Forms

The following are candidate forms for realistic policies on a social contact graph:

**$k$-hop restriction.** Only allow contact within $k$ edges of yourself in the graph. At $k = 0$ this is total isolation; at $k = 1$ it is "only your direct friends"; at $k = 2$ it is "your friends and their friends"; and so on. Prof. Austern mentioned this explicitly as a natural implementable rule.

**Household/cluster restriction.** Partition the graph into clusters (using a community detection algorithm) and allow contact only within each cluster. This is a graph-theoretic formalization of "stay within your household bubble."

**Distance-based threshold.** If we have geographic or social-distance information, allow contact only within a threshold distance. The closest real-world analog is "stay within $k$ kilometers of home."

**Degree cap.** Allow each node to have at most $k$ contacts. A policy cap on the number of social ties any individual can maintain. The corresponding edge removal is: for each node with more than $k$ neighbors, remove enough edges to bring it down to $k$.

**Attribute-based restriction.** Allow contact only between nodes sharing a specific attribute (e.g., "only interact with people in your own dorm"). This is a coarse but implementable rule.

**Time-windowed contact.** Allow contact between any two people, but only on certain days or for limited durations. This does not fit cleanly into the static-graph formalism but is worth noting.

## X.4 Ideal vs Realistic as a Results Section

A natural move in the report is to compute two things for each method:

1. The ideal-policy performance: the best cost/containment trade-off under unconstrained edge selection.
2. The best realistic-policy performance: the cost/containment trade-off under one or more structural policy forms.

The gap between these two curves is the "implementability cost." A method that shrinks this gap (producing realistic policies that approach ideal performance) is more useful than one that achieves great ideal performance but collapses under implementability constraints.

This framing gives us a richer results section than just comparing methods on ideal performance alone.

## X.5 The Policy Learning Question

One open question is whether our learned method should directly learn a realistic policy (e.g., learn a $k$ to use, or learn a clustering to constrain on) or learn an ideal policy and then be projected onto the realistic constraint afterwards. Both approaches are valid; they have different inductive biases and produce different results. We have not decided between them.

## X.6 Robustness to Non-Compliance

Even realistic policies are not perfectly obeyed. Prof. Austern mentioned partial compliance as a robustness dimension: what if only 80% of the population follows the policy? What if 90%? This is not a different policy form; it is a perturbation of the execution of a given policy. We can simulate non-compliance by randomly flipping a fraction of the "removed" edges back into the graph before running the epidemic simulation.

The question to answer in the discussion section: do the conclusions about policy comparison survive under non-compliance, or do some methods degrade faster than others? A method that does well only under perfect compliance is fragile. A method that degrades gracefully under imperfect compliance is robust.

---

---

# Part XI: Robustness Dimensions

Prof. Austern suggested several dimensions along which we can vary the experimental setup to test whether our findings are robust. This part enumerates them and discusses which ones are most valuable for our project. We are not obligated to do all of these; we should pick a subset that fits in the time budget.

## XI.1 Varying the Epidemic Model

Run the main analysis under SIR and repeat it under SIS. See whether the ranking of methods is stable across models. If the best method under SIR is also the best under SIS, that is strong evidence that the result is not an artifact of the model choice. If the ranking flips, that is worth investigating and discussing in the report.

**Effort level:** Low. The simulation machinery is the same; we only change the state transition rules.

## XI.2 Varying the Graph Topology

Test the methods on multiple Facebook100 campuses. Then also test them on synthetic graphs generated from known models (Barabási-Albert for scale-free structure, Watts-Strogatz for small-world structure, stochastic block model for community structure). The question is whether the methods work on any graph or only on graphs with specific structural properties.

**Effort level:** Medium. Requires generating synthetic graphs and computing their descriptive statistics. Not computationally hard, but adds bookkeeping.

## XI.3 Varying the Cost Function

Run the main analysis under the primary cost function (e.g., feature-similarity dot product) and repeat it under an alternative (e.g., uniform costs, or geographic proxy). See whether the method comparison is stable across cost functions.

**Effort level:** Low. The simulation does not change; only the cost values do.

## XI.4 Varying the Compliance Rate

Simulate imperfect compliance by randomly flipping a fraction of the "removed" edges back in. Do this at 100%, 90%, 80%, 70% compliance and see how each method degrades.

**Effort level:** Low. Adds a coin flip per edge in the removal set.

## XI.5 Varying the Seed Set

Run the epidemic from different initial seeds. Uniformly random seeds are the primary; adversarial seeds (most-central nodes as the initial infected) are the worst-case stress test. Compare method rankings across seed strategies.

**Effort level:** Low. Modify the initial condition of the simulation.

## XI.6 Varying the Containment Target

Sweep the containment target (or the cost budget) across a range, and report the Pareto frontier for each method. This is not strictly a robustness check; it is a more complete evaluation. But it subsumes some robustness questions because if one method dominates across the whole frontier, the conclusion is robust to the choice of target.

**Effort level:** Medium. Requires more simulation runs (one per point on the frontier), which multiplies compute cost but is the single most valuable evaluation move we can make.

## XI.7 Varying the Transmission Probability

Epidemic dynamics depend critically on the basic transmission probability per edge. If the disease is extremely transmissible, any containment is hard. If it is barely transmissible, containment is easy. The interesting regime is in between. Sweeping the transmission probability shows us where in this regime our methods matter most.

**Effort level:** Medium. Many simulation runs at different parameter values.

## XI.8 A Minimum Viable Robustness Plan

If we had to pick the smallest set of robustness dimensions to include in the report to satisfy Prof. Austern's standards, we would pick:

1. One alternative epidemic model (SIR primary, SIS check, or vice versa)
2. One alternative cost function (primary cost function, then uniform as sanity check)
3. One compliance perturbation (e.g., compare 100% and 80% compliance)

That is three robustness dimensions on top of the main analysis. It is manageable in the time budget and it gives us enough material for a substantive discussion section.

Anything beyond this is a bonus. If time permits, add varying the transmission probability and varying the graph topology. If time is tight, drop down to the minimum viable plan.

---

---

# Part XII: The Dataset

This part describes what we know about Facebook100, what we do not yet know, and what we need to decide about dataset usage.

## XII.1 What Facebook100 Is

Facebook100 is a dataset assembled by Traud, Mucha, and Porter around 2011–2012 from Facebook network data collected in 2005. It contains the complete friendship graph for 100 U.S. colleges and universities at a single time point, along with demographic metadata for the users. The dataset has been widely used in network science research and is a standard benchmark for studying social network structure in an academic setting.

The networks vary dramatically in size, density, and structure. Some networks have a few thousand vertices (small liberal arts colleges), while others have tens of thousands (large state universities). Degree distributions, clustering patterns, and homophily levels all vary across the dataset.

## XII.2 What Each Node Has as Metadata

For each vertex, Facebook100 provides categorical attributes:

- **Student or faculty status**
- **Dormitory**
- **Major**
- **Year of graduation**
- **Gender**
- **High school**

These attributes are integers, where 0 typically indicates missing data. Not all attributes are present for all vertices.

## XII.3 What the Edges Represent

Each edge is an undirected Facebook friendship at the time of data collection. There is no edge weight in the raw data. There is no timestamp. There is no communication volume. The edge is simply a binary friendship indicator.

For our project, this means any edge weight or cost we use must be derived rather than observed. The raw dataset gives us structure and node metadata, but not edge-level importance information.

## XII.4 Selecting Campuses

We need to decide which campuses to analyze. Several considerations:

**Diversity of structure.** Pick campuses whose descriptive statistics (size, density, clustering, degree distribution, assortativity, homophily on different attributes) span a wide range. This ensures that our findings are not specific to one network type.

**Computational feasibility.** Large networks are more expensive to simulate. If we include the largest campus (which has tens of thousands of vertices), we will need to budget more compute for the simulation runs.

**Number of campuses.** The original proposal said "five to ten." The right number depends on how many robustness analyses we want to run per network. Fewer campuses with more analyses per campus may be more informative than more campuses with less depth.

**Principled selection.** One option is to compute descriptive statistics on all 100 networks and then pick representatives that span the extremes on each dimension. Another option is random selection. A third is expert selection based on prior familiarity with the dataset. We have not chosen.

## XII.5 Preprocessing Decisions

Before running any analysis, we will need to make preprocessing decisions:

**Handling isolated vertices.** Some vertices have degree zero. They play no role in epidemic spread and can be safely dropped. Doing so changes the vertex count and should be documented.

**Handling the largest connected component.** Networks may have one giant component plus small fragments. Restricting to the giant component is standard practice and makes the analysis cleaner.

**Handling missing attributes.** As discussed in Part IX, we recommend treating missingness as its own category rather than imputing.

**Normalizing the attribute space.** If we use feature similarity for cost, we should L2-normalize each node's feature vector to avoid scale artifacts.

## XII.6 The Dataset Versus Real COVID Data

A question Prof. Austern did not explicitly raise but that we should think about: is Facebook100 actually a good proxy for the contact graph through which a disease spreads? Facebook friendships are not the same thing as physical contacts. Two people can be Facebook friends without ever being in the same room, and two people can be in the same room every day without being Facebook friends.

This is a limitation of the dataset and we should acknowledge it in the report. The defense is that Facebook friendships correlate with real social ties, and real social ties correlate with physical contact opportunities, so Facebook100 is a useful proxy even if it is not a literal contact graph. But we should not overstate the realism of the substrate; the simulations are informative about what epidemic dynamics could look like under certain assumptions about the underlying social network, not literal predictions about disease spread at these campuses.

## XII.7 Ethical and Privacy Considerations

Facebook100 was collected from public Facebook profiles around 2005 and released for research purposes. It is widely used in published academic work. There are ongoing debates about the ethics of using social network datasets of this kind, particularly regarding re-identifiability and whether informed consent was obtained. For our project, we are using the dataset in its standard academic form, consistent with its intended research use. We should briefly acknowledge the ethical dimension in the report without overclaiming or overdefending.

---

---

# Part XIII: Evaluation and Comparison

This part describes how we compare methods to each other and how we present the results. It is the "experimental protocol" part of the report.

## XIII.1 The Unit of Comparison

For each method and each graph, we compute a curve: cost on the $x$-axis and expected epidemic outcome on the $y$-axis. Each point on the curve corresponds to a specific cost budget (or equivalently, a specific containment target).

Curves are the right unit of comparison because a single number (e.g., "the best containment achievable at a budget of 5%") can be misleading. Methods can cross each other on the frontier: one method may be better at low budgets and another at high budgets. A single-number comparison hides this structure.

## XIII.2 Averaging Over Randomness

Both the epidemic simulation and the seed selection are stochastic. We need to average over enough random repetitions to get stable estimates. A reasonable protocol:

- For each (method, graph, budget) triple, run the epidemic simulation with a fixed policy $N$ times (different random seed sets and different transmission outcomes).
- Compute the mean outcome and a confidence interval.
- Plot the mean as the central line and the confidence interval as a shaded band.

The choice of $N$ depends on variance. Start with $N = 100$ and check stability. If the variance is still high, increase. If it is already tight, reduce $N$ to save compute.

## XIII.3 Method Comparison Within a Graph

Within a single graph, the comparison is direct: overlay the curves of all methods on the same plot and look at which dominates where. Some methods may dominate across the whole range, others only in certain regions.

For a statistical comparison (rather than visual), we can compute the area under each curve, which gives a single summary score per method per graph. Methods with smaller area (lower cost for given containment) are better.

## XIII.4 Method Comparison Across Graphs

Across multiple graphs, the question is whether the ranking of methods is consistent or varies by graph type. Options:

**Rank aggregation.** For each graph, rank the methods; then aggregate rankings across graphs. Methods that are consistently high-ranked are robustly good; methods that flip their ranking are sensitive to graph structure.

**Regression analysis.** Regress the performance of each method on descriptive graph statistics. This lets us ask which structural properties predict when each method does well. This connects back to the original "which segregation metric matters" question, and it is the move that brings structure-aware analysis back into the project in a principled way.

**Paired comparisons.** For each pair of methods, compute the fraction of graphs where the first method outperforms the second. This gives a head-to-head win rate per method pair.

## XIII.5 Failure Mode Analysis

In addition to average performance, we should examine where each method fails. Questions like:

- On which graphs does the GNN method underperform the classical baselines?
- Are there graphs where even the best method is far from the optimum?
- Are there cost regimes where all methods collapse to near-random performance?

Understanding failure modes is part of the "substantive discussion" that Prof. Austern wants. A method that dominates on average but has catastrophic failures on certain graph types is different from a method that is consistently second-best but never catastrophically bad. The report should distinguish these cases.

## XIII.6 Visualizations

Key visualizations to include in the report:

**Pareto frontier plots.** Cost versus containment, one curve per method, one panel per graph (or one panel per graph class if we group them). The single most important figure in the report.

**Method ranking table.** A grid with methods in rows, graphs in columns, and cells colored by rank (1 = best, 2 = second best, etc.). Lets the reader see ranking consistency at a glance.

**Scatter plots of performance vs graph properties.** Each point is one (method, graph) pair; $x$-axis is some graph descriptor (clustering, assortativity, homophily); $y$-axis is the method's performance. Fits trend lines by method. Shows how performance depends on structure.

**Example interventions.** For one or two interesting graphs, show a visualization of the graph with the selected edges highlighted. This makes the analysis tangible and gives the reader intuition for what the method is actually doing.

**Robustness panels.** Grids showing how method performance changes under each robustness perturbation. One panel per perturbation dimension.

## XIII.7 What We Report in the Results Section

At minimum, the results section of the report should include:

1. A summary of the descriptive statistics of the graphs we used (how big, how clustered, etc.).
2. The Pareto frontier plots for the main analysis.
3. The ranking table across methods and graphs.
4. At least one robustness panel (e.g., SIR versus SIS).
5. At least one visualization of an example intervention.
6. Quantitative summaries of the main findings in prose.

This gives us enough material for a solid results section without overloading it.

---

---

# Part XIV: Literature Directions

Prof. Austern explicitly said to do a quick literature search on "networks and COVID-19" and more broadly on epidemic containment on networks. She did not name specific papers. This part lists the literature directions we should explore. We have not done the search yet; these are the areas to cover.

## XIV.1 Classical Epidemic Spreading on Networks

The foundational work on SIR and SIS dynamics on networks is associated with Pastor-Satorras and Vespignani (early 2000s), who showed that scale-free networks have very different epidemic thresholds than random graphs. This is the starting point for any serious network-epidemic project. Understanding the notion of an epidemic threshold and how it depends on degree distribution is essential background.

## XIV.2 Classical Network Attack and Removal

The canonical work on targeted removal of nodes for disconnection or disruption is Albert, Jeong, and Barabási (2000) on the resilience of complex networks to attack, followed by Holme, Kim, Yoon, and Han (2002) on attack vulnerability. These papers establish degree-based and betweenness-based targeting as the classical baselines. Anyone who writes about network containment without knowing this literature is working in the dark.

## XIV.3 Assortativity and Mixing

Newman's work on assortative mixing in networks (2002) defines the assortativity coefficient and discusses how different networks exhibit different mixing patterns. This is directly relevant to our segregation metrics and to the regression analysis of how structure predicts method performance.

## XIV.4 The Facebook100 Paper

Traud, Mucha, and Porter's paper on the Facebook100 dataset describes the dataset's construction and presents basic structural analyses. We should cite this paper when we describe the dataset and we should briefly acknowledge any standard findings from it that are relevant to our work.

## XIV.5 Homophily in Networks

Karimi et al. and others have worked on homophily in networks, particularly on the issue of normalizing homophily measures to account for group size imbalance. If we use normalized homophily as one of our structural metrics, we should cite the appropriate source.

## XIV.6 Networks and COVID-19 Specifically

Prof. Austern mentioned that papers exist which built social networks of the United States and evaluated state-level policy effectiveness during COVID. We should find these. The ones most likely to be relevant are those that (a) use graph-theoretic tools to analyze real policies and (b) quantify the trade-off between containment and policy cost. We have not yet identified specific authors or titles.

## XIV.7 Contact Network Inference

A related literature we should be aware of (even if we do not engage with it deeply) is contact network inference: how to construct an effective contact graph from data sources that are not direct observation of contacts. This is relevant because Facebook100 is not a contact graph in the literal sense; it is a friendship graph that serves as a proxy.

## XIV.8 Graph Neural Networks for Epidemic Prediction

There is a recent body of work applying GNNs to epidemic forecasting and intervention. We should survey this briefly to see whether our learned method has direct prior art and, if so, to position our contribution against it. We have not done this survey yet.

## XIV.9 Network Interdiction

Network interdiction is the combinatorial optimization problem of removing edges or nodes to disrupt some flow through the network. It has been studied extensively in operations research, with applications from military logistics to infrastructure security. The formulation is closely related to our cost-aware edge removal problem, and there may be relevant results on approximation algorithms and hardness. We should briefly engage with this literature.

## XIV.10 The Literature Review in the Report

The report does not need a comprehensive literature review. It needs enough engagement with prior work that a reader can see we are aware of the relevant context. A reasonable target: one to two pages of related work, covering the areas above at a high level, with specific citations for any claim or baseline that has a clear source.

---

---

# Part XV: The Nature of the Deliverable

This part describes the three things we have to produce and the grading philosophy behind them. The details here come from two sources: the original advisor meeting with Prof. Austern on our specific project, and a more recent class-wide discussion in which she explained the format and expectations for all STAT 175 projects. Where the two sources agree, we treat the information as settled. Where the class-wide discussion added detail we did not have before, we flag it as an update.

## XV.1 The Three Deliverables

The project has three components that together form the deliverable. In order of importance to the grade:

1. A written report (group deliverable)
2. An in-person individual oral defense (individual deliverable)
3. A five-minute lightning talk (group deliverable, low stakes)

We describe each in detail below. All three are required; none can be skipped.

## XV.2 The Report

The report is the primary written deliverable. Prof. Austern reads every single report personally, before any other component of the grade is determined. She has said explicitly that the report is the foundation: the oral defense is structured around it, and she walks into each defense already knowing what the project is about because she has already read the report.

### XV.2.1 What the Report Should Contain

Prof. Austern has not given a rigid structural template, but based on her comments in both the advisor meeting and the class discussion, the report should contain at minimum:

**An introduction.** The motivation, the scientific question, and a preview of what the project does.

**Background.** The graph formalism, the epidemic model, the cost formulation. Enough that a reader unfamiliar with the specifics can follow.

**Methods.** Each intervention strategy described precisely. The learned-method component (likely a GNN) described in enough detail to be understood and, critically, reproduced.

**Experimental setup.** The datasets, the parameter choices, the simulation protocol. Precise enough that someone else could run the same experiments.

**Results.** The Pareto frontier plots, the method rankings, the robustness analyses.

**Discussion.** The substantive conversation about what the results mean, what their limitations are, and what we would do with more time or better data. This is the section Prof. Austern cares about most.

**Implementability section.** The discussion of ideal versus realistic policies and the gap between them.

**Conclusion.** A short recap with the main takeaways.

**References.** Citations for all prior work mentioned.

The length and formatting should follow whatever the course syllabus specifies. We have not confirmed this yet.

### XV.2.2 The Reproducibility Requirement (Important Update)

Prof. Austern stated explicitly in the class discussion that the report must be accompanied by reproducible materials. Her exact framing: she should be able to produce anything that we provide in the report. This means that in addition to the report itself, we must make our code, data, and experimental configuration available to her, either through a shared repository (GitHub was the example she gave) or through a direct delivery of the files.

This is not optional. It is a grading criterion. A report that presents results without making those results reproducible will be penalized. In practice this means:

- We need a GitHub repository (or equivalent) that contains all the code used to produce the results in the report.
- The repository should include the configuration files, the random seeds, and any preprocessing scripts needed to go from raw data to final plots.
- The README should be sufficient to let someone outside the team run the main experiments without having to guess parameter values.
- The data we used should be either included (if small enough and license permits) or referenced with clear instructions for obtaining it.
- Trained models, if we use any, should be saved and made available if feasible.

The reproducibility requirement also shapes how we write the report. Every claim in the results section should be traceable back to a specific experiment in the repository. If a plot appears in the report, there should be a script in the repository that produces that plot. If a number appears in the text, there should be a config that produces that number. We are not expected to build a production-grade reproducibility pipeline, but we are expected to make it realistic for Prof. Austern to re-run any part of the work if she chooses.

This requirement is not a last-minute add-on; it should shape how we structure the code from day one. Setting up the repository with a clean directory structure and a working end-to-end pipeline early is much easier than retrofitting reproducibility at the end of the project.

### XV.2.3 What a Good Report Looks Like (Prof. Austern's Criteria)

From both meetings, Prof. Austern's evaluation criteria for the report are approximately the following:

**Is the report clear, well-written, and well-organized?** Presentation quality matters. A report that is hard to follow gets penalized regardless of the underlying work quality.

**Is the project tackling a precise question that is well stated?** The scientific question needs to be in the report, clearly, near the top, in one or two sentences.

**Is the project pushing beyond simple application toward something novel?** The bar for novelty is not "original research paper" but "not just rerunning standard methods with default settings." There should be some thought in the design of the methods, the cost function, the evaluation, or the robustness analysis.

**Are the results well discussed and well put in perspective?** This is the point Prof. Austern emphasized most in both meetings. A report that presents results without discussing them is weak. A report that discusses results honestly, including their limitations, is strong. The discussion section is where the grade is earned.

**Is the content correct and reproducible?** Both the correctness of the methods and the reproducibility of the results are evaluation criteria.

## XV.3 The Oral Defense

The oral defense is individual. Each team member attends their own slot alone, in person. It is not on Zoom. Prof. Austern confirmed the in-person format in the class discussion.

### XV.3.1 The Format

Each defense is approximately 15 minutes long (plus or minus, depending on how the conversation goes). No slides are required. No presentation is required. The student does not prepare anything to show. The format is entirely conversational.

The defense consists of exactly three questions. Prof. Austern stated this explicitly. The three questions are structured as follows:

**Two questions about the content of the project.** These are questions about what the project is, what methods it uses, and how the results were produced. Prof. Austern said that because each student is working on their own project, these questions should not be especially difficult. In her words, students should not have any issue answering these two questions.

**One deeper question.** The third question pushes for a deeper understanding. It is meant to be more challenging and to test whether the student can reason about the project beyond what is explicitly in the report. This is the question that differentiates strong defenses from weak ones.

Prof. Austern said that in her experience, students typically get about 2.5 out of 3 questions right, and that answering around 80% of the content correctly is completely fine. She does not expect perfection. She is not looking for students to fail; she is looking for evidence that each student has personally engaged with the project and can discuss it intelligently.

### XV.3.2 Why the Defense Is Structured This Way

Prof. Austern was explicit about why individual defenses exist. There are two reasons. First, the university has strongly encouraged instructors to include individual accountability components in response to concerns about AI-assisted work (she specifically mentioned ChatGPT in the original advisor meeting). Second, she has observed in past years that team projects can be carried by one or two members while others contribute little, and the individual defense format makes this pattern visible and penalizes it. She does not want to grade a group entirely on work that a subset of the group produced.

The practical implication for us: every team member needs to understand every piece of the project well enough to answer questions about it. Not just your own contributions. The full project. This document exists in part to make that possible. Reading it front to back should be part of every team member's preparation for the defense.

### XV.3.3 Preparation for the Defense

To prepare for the defense, each team member should be able to:

- Explain the central scientific question in one sentence
- Describe the optimization problem formally (objective, constraint, decision variable)
- Explain what each method does and why it might or might not work
- Walk through the main results and their interpretation
- Discuss the limitations of the methods and the assumptions honestly
- Answer a hypothetical question about changing one element of the setup (e.g., "what if you had used SIS instead of SIR")
- Explain the role of any part of the project, not just the parts they personally worked on

The deeper question is the one to focus extra preparation on. It is the one that students most commonly get wrong, and it is the one that most distinguishes strong defenses from weak ones. Practicing "what if" questions in advance, and being able to reason about the project under perturbations, is the best way to prepare.

### XV.3.4 Scheduling

Prof. Austern will release Google Calendar invites with many slots, allowing each student to pick one that fits their schedule. She said she wants to give a larger window than usual so that students with dense exam schedules can still find a viable slot. The defenses happen during the exam period. She does not yet have the exact start date.

The defenses will involve different questions for different team members. This is intentional. She will draw on different parts of the report for different students, so two members of the same team cannot rely on coordinating answers in advance.

If any team member has a hard scheduling conflict (for example, an exam that blocks out most of the exam period), they should raise it with Prof. Austern now, not later. She said explicitly that now is the time to flag concerns.

## XV.4 The Lightning Talk

The lightning talk is a five-minute presentation given in one of the last two classes of the semester. Each group presents. The audience is the rest of the class.

### XV.4.1 The Purpose

The lightning talk is explicitly low-stakes. Prof. Austern said that most students will get full credit for it as long as they show up and give a reasonable talk, and that doing poorly would require "something outrageous." She described it as an incentive to attend class and to have students learn what other groups are working on, rather than as a formal evaluation component.

The talk is not judged on results. This is important: Prof. Austern said explicitly that the lightning talk is not scored on the quality of what has been done or on what results are ready. If we do not have results yet, that is fine. If we only have the question and the method, that is also fine. What matters is how well we communicate.

### XV.4.2 What the Talk Should Cover

Based on Prof. Austern's description, a good five-minute talk explains four things:

1. What the project is about
2. What the scientific question is
3. Why the question is interesting or non-trivial
4. What methods or ideas we are pursuing

If we have some preliminary results, we can show them, but that is not required. The talk is evaluated on the quality of the explanation, not on the quality or quantity of the results.

### XV.4.3 Logistical Notes

The talk is five minutes. Prof. Austern confirmed this length explicitly. There are roughly 20 groups in the class, and she is splitting the presentations across two class periods so that there is time for questions.

She mentioned that she will bring cookies, and that students get cookies after giving their talk. This is a friendly detail but also worth noting: she is signaling that the atmosphere is meant to be relaxed. The lightning talk is not an adversarial evaluation.

## XV.5 The Grading Philosophy

Prof. Austern gave a detailed explanation of her grading philosophy in the class discussion. This is worth capturing in full because it shapes how we should think about the project.

### XV.5.1 No Fixed Quota of A's

She said explicitly that she does not have a fixed distribution of grades. There is no rule that a specific percentage of students receive an A and a specific percentage receive a B. Students are not in competition with each other. If every student in the class demonstrates mastery, every student receives an A. If no student demonstrates mastery, no student receives an A. The grade reflects the individual's work, not their rank relative to their peers.

### XV.5.2 Mastery-Based, Not Performance-Ranked

The grading is mastery-based. An A means the student has demonstrated mastery of the topic. A B means the student has demonstrated competence but not mastery. And so on. This is explicitly not a curve. Prof. Austern said her goal is to help students demonstrate mastery, which is part of why she met with every group individually before the project started, to help each group stay on track.

### XV.5.3 The Midterm Does Not Determine the Project Grade

Prof. Austern made a point of saying that students who did not do well on the midterm are not locked out of doing well on the project. The project and the midterm are evaluated separately, and a student who did poorly on the midterm but does well on the project can still end the semester with a strong grade. This is relevant to at least some of our team members and is worth internalizing. The project is a real chance to recover ground, and effort put into it is not wasted even if earlier grades were disappointing.

### XV.5.4 The Project Is Not an Automatic 100

Prof. Austern also said the opposite of the above: the project is not a gift. It is not the case that everyone who turns in a project automatically receives full credit. She said explicitly that not everyone will get 100, and that students should put real effort into the project because it is a genuine opportunity to demonstrate mastery of the material.

The combination of these two points (no quota on A's, but also not an automatic A) is worth internalizing: the grade is determined by the quality of the work, not by a competitive ranking and not by a participation floor. This makes effort the right variable to optimize.

### XV.5.5 The Purpose of the Project in Her View

Prof. Austern stated that the project exists for two reasons. First, it is the best way she knows to assess whether students can apply the course material to a real research problem on real data. Second, the project is itself a learning experience: the process of doing the project is part of what the course is teaching. The project is not a test of material that has already been learned; it is a vehicle for learning material that could not be learned through lectures and homework alone.

This framing implies that the project is evaluated not just on its output but also on evidence that the students learned something from doing it. The discussion section of the report and the responses in the oral defense are both opportunities to demonstrate that learning has happened.

## XV.6 The Relative Weights of the Components

Prof. Austern did not give exact percentage weights for the three components. What she did say is:

- The written report is the primary deliverable. It is what she reads first and what the oral defense is structured around.
- The individual defense carries real weight. It exists specifically to differentiate individual understanding from group output. A student who wrote a good report but cannot defend it will land worse than a student who wrote the same report and can defend it.
- The lightning talk is low-stakes and essentially a participation item.

A reasonable mental model: the report is the foundation, the defense is the differentiator, and the lightning talk is a checkbox. Do not neglect any of the three, but allocate preparation effort accordingly.

---

---

# Part XVI: Open Questions

This part is a consolidated list of decisions we have not yet made. Every item here is something the team needs to resolve before we can commit to code or experimental design. The list is grouped by theme.

## XVI.1 Model and Simulation Questions

**Which epidemic model is the primary?** SIR or SIS? Or a different variant?

**Which epidemic model is the robustness check?** Whichever one is not primary, or a third one?

**What transmission probability and recovery rate parameters do we use?** Calibrated to COVID-like dynamics, or chosen to make the simulation interesting, or swept as an independent variable?

**How many simulation repetitions per configuration?** We need a specific number, calibrated to get stable estimates.

**What seed set strategy?** Random seeds, adversarial seeds, or both?

**What containment outcome is primary?** Final epidemic size, peak prevalence, or something else?

## XVI.2 Cost Function Questions

**What is the primary cost function?** Feature-similarity dot product is the leading candidate, but we have not committed.

**What is the robustness cost function?** Uniform, geographic proxy, or something else?

**How exactly do we compute the feature-similarity cost?** Raw dot product, L2-normalized cosine similarity, sigmoid of dot product?

**Do we normalize costs across graphs?** Yes, probably as fractions of total cost. But we need to be specific about this.

**Do we treat costs as observed or learned?** Fixed costs from a deterministic proxy, or costs that are learned jointly with the GNN?

## XVI.3 Method Design Questions

**Which edge-based baselines do we include?** Random, betweenness, endpoint-degree product, bridge detection, and others. We need to pick a set.

**How many baselines total?** Probably three to five, enough to cover the space without clutter.

**Which GNN architecture and which training objective?** We described four options in Part VII. We need to pick one.

**Does the GNN score edges directly or learn embeddings that induce a cost function?** Prof. Austern's dot-product suggestion points toward the second, but the first is more direct.

**What features do we feed the GNN?** Facebook100 attributes, structural features, or both?

**How do we handle missing attributes?** Missing-as-category is the current recommendation but we have not committed.

## XVI.4 Dataset Questions

**How many Facebook100 campuses do we use?** Five to ten was the original range.

**Which specific campuses?** Picked for structural diversity, or randomly, or by some other criterion?

**Do we preprocess to keep only the giant component?** Probably yes but we have not committed.

**Do we use any synthetic graphs to supplement the real ones?** For robustness analysis across topologies.

## XVI.5 Policy Form Questions

**Do we compare ideal and realistic policies both?** Recommended but not committed.

**Which realistic policy forms do we include?** $k$-hop restriction, cluster restriction, degree cap, attribute-based. We need to pick at least one.

**How do we quantify the implementability gap?** Gap in cost? Gap in containment? Area between curves?

## XVI.6 Evaluation Questions

**Do we use Pareto frontiers or single budget points?** Probably frontiers but we need to commit.

**What cost budgets do we sweep?** A range from very low to very high, but with how many points?

**Do we include confidence intervals on plots?** Probably yes; good science demands it.

**Do we do rank aggregation across graphs?** Probably yes, but we need to decide the method.

## XVI.7 Robustness Questions

**Which robustness dimensions do we include?** At minimum: epidemic model, cost function, compliance rate. Anything beyond that is a bonus.

**How do we operationalize partial compliance?** Random flipping of removed edges back into the graph is the natural choice.

**Do we run adversarial seeding as a stress test?** Optional.

## XVI.8 Literature Questions

**Which papers do we cite as essential prior work?** We have a list of topic areas but no specific papers yet.

**Do we position our method explicitly against any single prior work?** If there is a direct predecessor (especially for the GNN-based edge scoring), we should cite it and explain the difference.

## XVI.9 Writing and Presentation Questions

**What is the structure of the report?** We have an outline but no commitment to specific section lengths.

**Who writes which section?** Divided by module or by topic?

**Who runs which experiments?** Divided by method or by dataset?

**Who does the lightning talk?** All team members or a subset?

**Who takes responsibility for the graphs and figures?** This is typically one person's job for consistency.

## XVI.10 Logistical Questions

**When is the report due?** We should check the syllabus.

**What is the target date for a complete draft?** Working backward from the due date, give ourselves at least a week of revision time.

**When do we lock in the open questions above?** Probably in a team meeting in the next one to two weeks.

**What is our weekly check-in cadence?** We should establish a rhythm now.

## XVI.11 Reproducibility and Infrastructure Questions

These questions flow directly from the reproducibility requirement that Prof. Austern introduced in the class discussion. Because she stated explicitly that she should be able to reproduce any result in the report, the repository is no longer an optional nice-to-have; it is a grading criterion.

**Where does the repository live?** GitHub is the obvious choice. We have not created it yet.

**Public or private?** Private during development, shared with Prof. Austern as a collaborator or made public at submission. We have not decided.

**What is the minimum README for full reproducibility?** It should include setup instructions, how to obtain the data, how to run each experiment, and how to regenerate each figure in the report. We have not drafted it.

**How do we handle data that cannot be redistributed?** Facebook100 has a license; we need to confirm whether we can include it in the repository or whether we must link to it externally.

**Do we save random seeds for every experiment?** Almost certainly yes. Every simulation run should be reproducible bit-for-bit given its seed.

**Do we save trained models?** If we train a GNN or any other model, the trained weights should be saved in the repository (or in a linked artifact store) so that results can be reproduced without retraining.

**Do we set up continuous integration or tests?** Probably not for a project of this scope, but at least one end-to-end "smoke test" script that runs the full pipeline on a small example would be valuable.

**Who sets up the repository?** Needs to be assigned to a specific team member. This should happen early, before any real code is written, so that everyone starts working within a clean structure.

**What is the directory layout?** A standard scientific-project layout with folders for data, source code, configs, results, and notebooks. We should agree on this at the first team meeting.

**How do we keep the repository in sync with the report?** Every claim in the report should be traceable back to a specific script and configuration in the repository. This is a discipline issue more than a tooling issue, but it is worth naming explicitly so that no one forgets about it mid-project.

---

---

# Part XVII: What We Will Not Claim

This part is a short but important statement of the limits of what this project can honestly claim. Writing it down now protects us from overclaiming later.

## XVII.1 We Will Not Claim Real-World Predictive Validity

Our simulations are on Facebook100, which is a friendship graph, not a contact graph. Our epidemic model is a simplification of real disease dynamics. Our cost function is a proxy, not an observed quantity. None of this means the project is not useful, but it does mean we cannot claim that our methods would deliver specific containment outcomes if deployed in reality. The claim is about the structural properties of the methods under the assumptions we made, not about real-world performance.

## XVII.2 We Will Not Claim the GNN Is Novel

The GNN component (if we include one) exists because the project is meant to engage with the "learning on networks" portion of the course. We are not claiming to invent a new architecture. We are applying an existing architecture (likely GAT or GCN variants) to a specific problem formulation. The novelty, if any, is in the problem setup and the integration with the cost structure, not in the neural network itself.

## XVII.3 We Will Not Claim Definitive Findings

Prof. Austern said explicitly that we are not expected to have definitive answers. Any findings we report should be presented with appropriate uncertainty, including error bars on simulation results and explicit acknowledgment of sensitivity to design choices.

## XVII.4 We Will Not Claim That Our Method Dominates

Even if our learned method performs well in our experiments, we should not claim it is the best method for this problem in general. The results are contingent on the specific graphs, the specific epidemic model, the specific cost function, and the specific training setup. Generalization beyond this scope is a claim we cannot support.

## XVII.5 We Will Not Claim to Have Solved Implementability

The discussion of ideal versus realistic policies is a discussion, not a solution. We can quantify the gap between them under our assumptions, but we cannot claim to have resolved the fundamental tension between mathematical optimality and real-world enforceability. Any real intervention involves trade-offs we are not modeling, including social costs, economic costs, political costs, and the behavioral reality that people adapt to policies in unpredictable ways.

## XVII.6 We Will Not Overstate the Relevance to COVID

Prof. Austern framed this as a COVID-inspired project but she did not ask us to model COVID specifically. Our framing should be general: "epidemic spread on social networks under cost-constrained edge interventions." COVID is an instance of this class but not the only one. Overclaiming COVID relevance would be a mistake.

---

---

# Appendix A: Glossary of Terms

**Adjacency matrix.** An $n \times n$ matrix $A$ where $A_{ij} = 1$ if there is an edge between vertices $i$ and $j$, and 0 otherwise. The standard structural representation of a graph.

**Assortativity coefficient.** Newman's correlation-based measure of how similar connected nodes are along some attribute (often degree). Positive values mean similar nodes connect; negative means opposite.

**Betweenness centrality (edge).** The fraction of shortest paths in the graph that pass through a given edge. High-betweenness edges are bottlenecks.

**Clustering coefficient.** The fraction of a node's neighbor pairs that are also connected (local), or the graph-wide average (global). Measures triangle density.

**Compartmental model.** An epidemic model that divides the population into compartments (S, I, R, etc.) and specifies transition rules between them.

**Configuration model.** A random graph model that preserves the degree sequence of a target graph but randomizes all other structure. Standard null for testing whether structural properties are explained by the degree distribution alone.

**Containment target.** The upper bound on epidemic outcome that a containment policy must satisfy. Can be expressed as a fraction of population infected, a peak prevalence, or similar.

**Cost function (on edges).** A mapping from edges to non-negative real numbers representing the cost of removing each edge.

**Degree.** The number of edges incident to a vertex. In a directed graph, in-degree and out-degree are distinguished.

**Edge-weighted graph.** A graph where each edge carries a numerical weight (or cost).

**Epidemic threshold.** The critical value of the transmission rate above which an epidemic can spread widely on a given graph, and below which it dies out.

**Facebook100.** The dataset of 100 U.S. university Facebook friendship graphs, assembled around 2011 by Traud, Mucha, and Porter.

**GAT (Graph Attention Network).** A graph neural network architecture that uses attention weights to aggregate neighbor information.

**GCN (Graph Convolutional Network).** A graph neural network architecture that aggregates neighbor features via a fixed weighting based on degree.

**GNN (Graph Neural Network).** A neural network architecture designed to operate on graph-structured data via message passing between connected nodes.

**Homophily.** The tendency of nodes to connect to similar nodes. Can be measured along any attribute.

**Independent cascade.** A discrete diffusion model where each newly infected node gets one chance to infect each of its neighbors.

**Linear threshold model.** A discrete diffusion model where a node becomes infected once the fraction of its infected neighbors exceeds a threshold.

**Normalized homophily.** Homophily corrected for group size imbalance, so that a network with unequal groups is not spuriously classified as high-homophily.

**Pareto frontier.** The set of solutions that are not dominated by any other solution in a multi-objective optimization. In our context, the curve of best-achievable containment for each cost budget.

**Policy (in this project).** A rule or procedure that, given a graph, returns a set of edges to remove for containment.

**Residual graph.** The graph that results after removing the edges specified by a policy from the original graph.

**SEIR.** Susceptible-Exposed-Infected-Recovered compartmental model, with an incubation period between exposure and infectiousness.

**SEIRS.** SEIR with reinfection (recovered become susceptible again).

**SIR.** Susceptible-Infected-Recovered compartmental model, the basic starting point for network epidemic modeling.

**SIS.** Susceptible-Infected-Susceptible compartmental model, where infected nodes return to susceptible after recovery. Captures diseases with waning immunity.

**Stochastic block model (SBM).** A random graph model that partitions vertices into blocks and specifies connection probabilities between and within blocks. Used as a null model to test whether structure goes beyond block-level mixing.

**Transmission probability.** The probability that an infected vertex transmits the disease to a susceptible neighbor along a given edge in a given time step.

---

---

# Appendix B: Paraphrased Key Statements From the Meeting

These are paraphrases of key things Prof. Austern said in the meeting, grouped by topic, preserved here for reference. They are paraphrases rather than exact quotes because the transcript had speech disfluencies and partial sentences; the substance is preserved.

**On the general question:**
- "You want to look at epidemic spread on a social network and try to understand which containment strategy is the most effective depending on the topology of the graph."

**On the node-removal framing:**
- "Removing nodes is an interesting idea, but I am not sure COVID is the best example. In real life we do not remove individuals."
- "You probably also want an intervention on the susceptible, not only on the infected."

**On edge removal:**
- "The things that were done in practice were removing edges outside of the family circle."
- "You could try to ask: how to remove a minimum amount of edges in a way that is most effective."

**On costs:**
- "Everyone has a different cost for removing an edge."
- "Your loss could basically be the sum of all the costs of the edges that you have removed."
- "A proxy for the importance of the edge could be a dot product or sigmoid of a dot product between node features. If we have very similar features, we are probably closer, and so the edge is probably more important."

**On scope:**
- "You want to have a concrete plan and narrow it down in a way that is manageable."
- "You do not need to do everything I just said. I am giving you ideas."

**On methods:**
- "Go beyond degree. Degree is the 101."
- "Adding a cost to an edge is a good idea."

**On the scientific question:**
- "The scientific question could be: what is the lowest-cost policy, if you have feature information about each vertex."

**On realistic versus ideal policies:**
- "No one is going to say 'person $i$ and person $j$ just stop talking.' A policy in practice is something like: if you are further away than $k$ hops, you stop talking."
- "Policies are enforced in many countries where if your distance is more than a kilometer you cannot meet."

**On robustness:**
- "What if some people get reinfected? What if only 80% or 90% of people satisfy the policy?"

**On the epidemic model choice:**
- "COVID is actually not an SIR model. Recovered become susceptible again. So you might also do one with SIS."

**On the nature of the deliverable:**
- "You are not expected to come up with a definitive answer. You are not expected to come up with a paper."
- "What I do not want is: I have this graph, I do degree-corrected and something else, and then I have results, and everything ends here."
- "I want you to show that you have understood and have a nuanced conversation about the results."

**On reproducibility (from the class discussion, not the advisor meeting):**
- "You will have to not only give us a detailed report, but the report should be made available either by lending me the PowerPoint or through the GitHub account. I should be able to produce anything that you provide."

**On the grading criteria for the report (from the class discussion):**
- "Is this report clear, well-written, and well-organized?"
- "Is the project tackling the precise question that you have well stated?"
- "Is the project pushing beyond simple application towards something novel?"
- "Is the content of the presentation correct and reproducible?"
- "If the results are well discussed and well put in perspective, this is a good discussion."

**On the lightning talk (from the class discussion):**
- "The lightning talk is going to be painless. Except if you do something outrageous, I expect most of you to get full credit for it."
- "You will not be judged on what you have written, on the quality of the result. The judge in the lightning talk is the quality of the presentation and the quality with which you are explaining what the question is and what method you are tackling."
- "If you don't have the results yet, but you explain what the method is, that's fine."

**On the individual defense format (from the class discussion):**
- "The group will be asked three questions. Two of them I will read the report before, so I will know what the project is about. You don't have to present a presentation, you don't have to show any slide. I have to ask three questions. Two questions about the content of the project, and knowing that you are doing your own project, you shouldn't have any issue answering any of those questions. There will be one question that will push for a deeper understanding."
- "In my experience, you end up with 2.5 out of 3 questions right. If you have 80% of the answers that are completely fine, that is what I would expect."
- "It will be in person, not on Zoom."
- "It will involve different partners [different questions for different members]."

**On why the individual defense exists (from the class discussion):**
- "Sadly, this is something that we are strongly encouraged to do. It is almost required of us to do."
- "I think it is a good chance for you guys to have some more time to really realize the weight of the importance of the project."

**On grading philosophy (from the class discussion):**
- "It is not a fixed quota of A's. If you have an A, it is that you show mastery of the topic."
- "My goal is to help you demonstrate this to me and this is why I met with every group over the last few days."
- "You are not in competition with your neighbors. If you do very well on the project and you have not done that well on the midterm, that is okay."
- "That also means that not everyone is going necessarily to get 100, and that also means that you should put some effort into the project and that you really should see it as an occasion to master the work."

**On why the project exists at all (from the class discussion):**
- "My goal for you is that you learn how to reason about learning on networks. The second part of this class is more about neural networks and I could create a whole exam where you have to do some code. I am zero interested in this. My goal is to help you learn how to use the content of this class on a real research problem, on real data. And the best way I know how to do that is to have a project."

**On the defense format:**
- "Because of ChatGPT, the college asked us to do individual defenses. Also in past years some members have carried a project on their shoulders and that is not fair to everyone, so the individual defense makes sure everyone knows what is going on."

**On defense slot length (from the class discussion):**
- "Considering the number of individual students, keep in mind it would be maybe around 15 minutes."

**On the lightning talk:**
- "It will be minimalist. It should be quite easy to prepare. You will get cookies after you give the talk."

---

---

# Appendix C: Things We Understood But Did Not Say Out Loud

This appendix records things that became clear from the meeting that we should not lose sight of, even though they were not stated in so many words.

## C.1 Prof. Austern Enjoys This Problem

She engaged at length with our idea, suggested extensions, proposed specific technical moves (the dot product proxy, the $k$-hop policy rule), and came back to the containment problem multiple times without us steering her there. This is not the behavior of a professor who thinks the project is uninteresting. Even when she criticized the original framing, she was criticizing it in the direction of making it better, not in the direction of wanting us to drop it. This is a good sign for the project. She is likely to continue engaging if we come back to her with specific questions later.

## C.2 She Is a Theorist and Wants Clean Mathematical Objects

When she pushed back on node removal and pushed toward edge removal with costs, she was not making a pragmatic suggestion about what would be easier to code. She was making a mathematical suggestion about what the right object of study is. Edges with costs give you a well-defined optimization problem; nodes with no structure around their removal do not. The underlying preference is for cleanness and formality. We should write the report in a way that respects this preference: define the problem formally, state the objective cleanly, and be precise about what we are optimizing.

## C.3 She Is Skeptical of Unrealistic Policies

She came back to implementability multiple times. This is not just a suggestion that we add a section on implementability; it is a signal that she will mentally discount any results that depend on unrealistic policies. Our results will be stronger if we show that our methods produce policies that could plausibly be enforced, or at the very least if we honestly discuss the gap between what the methods produce and what could be enforced.

## C.4 She Has Clear Opinions About Robustness

She listed several robustness dimensions, unprompted, and she did so casually as if they were obvious moves to consider. This tells us that a report without robustness analysis will look like a report that did not think very hard. Even one or two robustness dimensions, done carefully, will satisfy this expectation.

## C.5 She Is Willing to Work With Us

She invited us to her office hours for follow-ups. This is not a pro forma statement; she said it with specific framing ("if you have specific concerns, come to office hours"). We should take her up on it when we have a more concrete plan and want her input on specific decisions.

## C.6 The Meeting Was a Success

Even though it felt uncomfortable in the moment, the meeting produced everything it needed to produce: a refined framing of the scientific question, a pivot from node removal to edge removal, the introduction of costs, a specific technical suggestion (the dot product proxy), a pointer to the relevant literature area, and guidance on scope and deliverables. We walked out of the meeting with a better project than we walked in with. That is the definition of a productive meeting.

---

---

# Closing Note

This document is the state of the project as of the immediate aftermath of the advisor meeting. It is complete in the sense that it captures everything we learned, and it is incomplete in the sense that many decisions remain open. Both of these are intentional. The team should use this document as the shared context for every subsequent discussion. When a decision gets made, the relevant open question in Part XVI should be updated. When a new question arises, it should be added.

The goal is that two weeks from now, this document (with updates) will still describe the state of the project faithfully, and will still serve as the shared reference that lets any team member pick up where someone else left off. A central document that stays accurate is worth more than ten specialized documents that drift out of sync.

The next concrete step is a team meeting to walk through Part XVI and begin closing open questions. Before that meeting, every team member should read this document end to end. That is what gets the team aligned.

*End of document.*