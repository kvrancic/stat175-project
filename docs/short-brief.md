# STAT 175 Project: Team Brief

*The short version. Read this to stay aligned. The long reference doc has everything else.*

---

## What the project is

Epidemic containment on real social networks, with costs on edges. We have a contact graph (Facebook100, several college campuses). A disease spreads on it. We want to find the lowest-cost set of edges to cut such that the epidemic stays under some containment threshold. "Cost" means removing a given edge is not free: cutting the link between close friends is expensive, cutting between acquaintances is cheap.

The scientific question, in one sentence: **given a social graph with feature information on each vertex, what is the lowest-cost set of edges whose removal contains an epidemic on the residual graph?**

This is a constrained optimization problem on a weighted graph, and it has a learned component (likely a GNN) sitting somewhere inside it. We compare our approach against classical baselines and discuss the results with honesty about the limitations.

---

## What changed in the advisor meeting (the important part)

We walked in with a different project. The original framing was about segregation metrics and node removal. Austern kept the general area but reshaped three things, and the reshaping is the whole reason the project is good now.

**Node removal became edge removal.** Her reasoning: we do not remove people from society during real outbreaks. We restrict which contacts are allowed. The natural object of intervention is the edge, not the vertex. This is the central mathematical pivot of the project.

**Cardinality became cost.** Not all edges are equal. Cutting family ties is expensive, cutting acquaintance ties is cheap. The loss function is the sum of costs of removed edges, minimized subject to a containment constraint. This turns the project from a structural comparison into a real optimization problem.

**"Which metric matters most" became "what is the lowest-cost policy."** The original framing was descriptive. The new framing is prescriptive: we propose a policy, we argue it is good, we discuss whether it is realistic. Austern said this explicitly as the scientific question we should be answering.

She also gave us a specific technical suggestion we should not forget: if each vertex has a feature vector, a natural proxy for edge importance (and therefore cost) is a dot product, possibly through a sigmoid, of the two endpoint feature vectors. Similar features imply socially close, which implies the edge is important to preserve. This gives the GNN a natural role: learn the embeddings that induce the cost function, then optimize containment under that induced cost.

---

## What she cares about (grading signal)

Austern is a theorist and she cares about the clean scientific framing more than she cares about raw numbers. Her evaluation criteria, in descending order of how much she mentioned each:

1. **A nuanced discussion of the results.** She said this three separate times in three different ways. What she does not want is "I have this graph, I ran algorithm X and Y, here are the numbers, the end." What she wants is a report where we look at the results, ask whether they make sense, discuss when and why they break, and talk about limitations honestly.

2. **Implementability.** Our proposed policies have to be things a real government could enforce. Nobody is going to tell person $i$ and person $j$ to stop talking individually. Real policies look like "stay within your $k$-hop neighborhood" or "no gatherings above size $n$" or "stay within your household cluster." The report should discuss the gap between the ideal policy the optimizer produces and the realistic policy form that could actually be deployed.

3. **A precise, well-stated question.** The scientific question should be one sentence, stated early in the report. The optimization problem should be formal (objective, constraint, decision variable). No waffling.

4. **Going beyond basic heuristics.** She said "degree is the 101." Degree-based targeting is a necessary baseline but not an acceptable main method. We need at least one thing that is smarter than degree.

5. **Robustness.** At minimum we should test how our conclusions change under a different epidemic model (SIS vs SIR), a different cost function (uniform vs feature-similarity), or imperfect policy compliance (what if only 80% follow the rule). Three robustness dimensions is enough.

6. **Reproducibility.** New requirement from the class discussion, not the advisor meeting. Austern said she should be able to reproduce anything in the report, via GitHub or direct delivery. This means the repo is a grading artifact, not an afterthought. Every plot should map to a script. Every number should map to a config.

---

## What she explicitly does not want

She said this directly: no project that reads "here is the graph, I ran method A, I ran method B, here are two tables, done." If our report looks like a benchmark page with numbers and no discussion, we fail. Honest conversation about limitations is more valuable than a big number.

She also does not want us to overclaim. She said explicitly: no one expects a definitive answer. No one expects a publishable paper. A project with a solid method, honest results, and a thoughtful discussion of what it means and where it breaks is an excellent project even if the headline findings are modest or negative.

---

## The deliverables

Three components, in descending order of how much they affect the grade.

**The report.** This is the primary artifact. Austern reads every report personally. It should have the usual sections (introduction, background, methods, experimental setup, results, discussion, implementability analysis, conclusion, references) with the discussion and implementability sections getting real weight. Length and format probably come from the syllabus, which we should check.

**Reproducible materials alongside the report.** A GitHub repo (or equivalent) with the code, configs, and scripts needed to reproduce every result in the report. Austern stated this explicitly in class: she should be able to re-run anything we present. Set up the repo early, before writing real code, so everyone works within the same structure from day one.

**The individual oral defense.** Each team member books their own slot. In person, not Zoom. Around 15 minutes. No slides, no presentation from us. Austern has already read the report and she asks exactly three questions: two about the content of the project (which we should be able to answer cleanly because we did the work), and one deeper question meant to push for real understanding. Students typically get about 2.5 out of 3 right, and 80% correct is "completely fine" in her words. She gives different questions to different team members on the same project, so coordinating answers in advance is not viable. Everyone on the team needs to understand the full project, not just their own part.

**The five-minute lightning talk.** In one of the last two classes. Group presents together. Low stakes, nearly everyone gets full credit, not judged on results. It is judged on how clearly we explain the scientific question and the method. If we have no results yet when the talk happens, that is fine. Austern brings cookies. Treat it as participation.

---

## How she grades

She said the following in the class discussion and it is worth internalizing:

No fixed quota of A's. She is not grading on a curve. If everyone demonstrates mastery, everyone gets an A. Students are not competing with each other.

The grade is mastery-based. An A means the student has shown mastery of the material, not that the student ranked above some percentile.

The midterm does not lock in the final grade. A strong project can compensate for a weak midterm. This is directly relevant to several of us.

But the project is not a free A either. She said explicitly that not every project gets full credit and that real effort is required. The upshot: effort is the right variable to optimize. The grade is a function of how good the work is, and nothing else.

---

## What is fixed and what is open

**Fixed after the advisor meeting.** Domain is epidemic containment on social networks. Intervention modality is edge removal. Edge costs exist and enter the loss function. Vertices carry feature information that can induce costs. At least one method is learned. Evaluation is simulation-based. Dataset is Facebook100.

**Open and needs a team decision before we write code:**

- *Which epidemic model is primary, which is the robustness check.* SIR and SIS are the two candidates. Austern flagged that COVID is closer to SIS because reinfection matters.
- *What the cost function actually looks like.* The dot-product-of-features proxy is the leading candidate but we have not committed. We need to decide whether features are raw one-hot Facebook100 attributes, learned attribute embeddings, or GNN-produced embeddings.
- *Which baselines we compare against.* The edge-based reformulation means the original node-based baselines (degree, betweenness) need to be rethought as edge-based. Candidate replacements: random edge removal, edge betweenness, endpoint-degree product, effective resistance, bridge detection.
- *Which learned method architecture.* The GNN can score edges directly, or learn embeddings that induce a cost function, or act as a surrogate outcome predictor. The cleanest option is probably the embeddings-induce-costs framing because it lines up with the dot-product suggestion.
- *How many campuses and which ones.* Original range was 5-10. We should pick campuses that span the descriptive-statistic space, not the largest ones (compute cost).
- *Which realistic policy forms we include.* Austern's example was $k$-hop restriction. Other options are cluster restriction, degree caps, and attribute-based restrictions. At least one realistic form should appear in the report so we can discuss the ideal-vs-realistic gap.
- *Which robustness dimensions we run.* Minimum viable set: one alternative epidemic model, one alternative cost function, one compliance perturbation. More is a bonus.

The long reference doc has the full list of open questions (there are thirty-something) organized by theme. Anyone writing code should check the relevant section before making an assumption.

---

## How we work

A few things that are not negotiable, given the individual-defense format and the reproducibility requirement.

**Everyone reads the full reference doc once.** Not just the section relevant to their module. The oral defense asks each person about the whole project and Austern explicitly said she gives different questions to different team members so coordinating answers is not viable. If someone only knows their own piece, they will lose points on the defense.

**The repo exists before code is written.** Whoever takes on repo setup does it in the first week. Standard scientific-project layout (data, src, configs, results, notebooks). README with setup and run instructions. Random seeds pinned for every experiment. Results should be regenerable end-to-end from a single command per experiment.

**Every plot in the report maps to a script in the repo.** Every number in the text maps to a config. This is a discipline thing more than a tooling thing, but it is easier to maintain from day one than to retrofit at the end.

**Weekly team check-in.** We have not set a cadence yet. This should be the first logistical decision. Even a 30-minute weekly sync where everyone states what they are working on and what is blocking them is enough.

**Open questions get closed in team meetings, not in Slack.** The reference doc has a list of open questions in Part XVI. As they get resolved, update the reference doc so it stays current. A central document that drifts out of date is worse than no central document.

---

## What we should not claim in the report

Writing this down now prevents drift later.

We will not claim real-world predictive validity. Facebook100 is a friendship graph, not a contact graph. Our epidemic model is a simplification. Our cost proxies are proxies. The project is about the structural properties of methods under stated assumptions, not about what would happen if you deployed them in a real pandemic.

We will not claim novelty in the GNN architecture. Whatever we use will be a standard off-the-shelf component (GAT or GCN variant). The novelty, if any, is in the problem framing, not in the neural network.

We will not claim definitive findings. Any finding we report should come with error bars, appropriate caveats, and explicit acknowledgment of sensitivity to design choices.

We will not overstate the COVID angle. COVID was the motivating example but the project is about epidemic containment in general. Don't write the report as if we are solving COVID.

---

## The meeting with Austern went well

One thing worth saying directly because it matters for morale: the advisor meeting was productive even though it felt rough in the moment. Austern spent fifteen minutes co-designing the project with us in real time. Theorists do not do that for ideas they find uninteresting. She engaged deeply, suggested specific technical moves (edge removal, cost functions, dot-product proxies, $k$-hop policy rules), pointed us at relevant literature areas, and said explicitly that she is happy to meet again at office hours for follow-ups. We walked out of that meeting with a better project than we walked in with. That is what a successful first meeting looks like.

---

*For everything else: see the long reference document. That doc has the formal graph definitions, the math, the full list of open questions, the literature pointers, and all the paraphrased quotes. This brief is for humans who need to stay aligned. The reference doc is for Claude Code and for anyone who needs to know a specific detail.*