# Lightning Talk Slide Design — Visual Spec

A slide-by-slide description of how the deck **looks**, not what we **say**. The transcript in `lightning-talk.md` is the spoken track; this deck is its supporting visual layer. None of the slides repeat the transcript verbatim. Most slides have under twelve words of body text; many have none.

Designed for a fast click-through cadence (~15-20 seconds per slide on average across 20 slides for a 5-minute talk). The audience should feel momentum, not feel they're being asked to read.

---

## Global design system

**Aspect ratio.** 16:9, 1920×1080 master.

**Palette.**
- **Ink** `#0B1020` — primary background; near-black with a faint blue cast.
- **Paper** `#F4F1EA` — off-white text and surface accents; warm, not clinical.
- **Coral** `#FF5A4E` — single primary accent, used for the GNN curve, the headline metric, and the "above threshold" zone.
- **Mint** `#7FE7B5` — secondary accent for the "below threshold / contained" zone, distance-threshold curve.
- **Slate** `#3A4256` — muted grey-blue for axis labels, baselines, betweenness curve.
- **Mist** `#9FA8B8` — tertiary, used for the random baseline curve and footnotes.

The deck never uses pure white or pure black — everything is slightly warmed to feel like printed paper rather than a screen.

**Typography.**
- Display: **Inter Tight** in weights 700 and 900 for slide titles.
- Body: **Inter** 400/500 for the rare moments there is body text.
- Monospace: **JetBrains Mono** for equations rendered with a subtle ligature for `<-`, `->`, `λ`, `τ`.
- Math is rendered through KaTeX-quality typesetting (think: nice italic Greek, properly kerned subscripts), not Unicode glyphs.

**Recurring chrome.**
- A 1-pixel coral hairline runs along the bottom 14% of every slide. It functions as a "cost budget bar": the bar **fills from left to right** across the entire 20-slide deck. By Slide 20, it's full. This is the deck's quiet visual joke — the talk itself is a budget that gets spent.
- Bottom-right corner: a tiny tag that cycles speaker names (`Karlo` → `Alec` → `Jackson` → `Ryan`) in a 50% opacity Inter 400, so the audience always knows who is talking without anyone having to introduce themselves mid-talk.
- Bottom-left corner: slide number rendered as a **percentage** (`05% / 100%`) instead of `5 / 20`. Reinforces the budget metaphor.
- A faint, animated 30-node graph drifts slowly in the upper-right of every slide at 8% opacity. Same graph, same node positions, but the **edge set thins out** as the deck progresses — by Slide 20, only ~40% of the original edges remain. The audience may or may not notice; if they do, it's a wink at what the project is about.

**Transitions.**
- Slide-to-slide: a 220 ms horizontal wipe with a soft cubic-bezier ease (`0.22, 0.61, 0.36, 1`).
- Within-slide builds: 180 ms fade-up with 8 px translate. Never spinning, never flying — feels like cards being placed, not animated.

**No clipart. No stock photos. No bullet-point template chrome.** Everything is custom data viz, custom typography, or empty space.

---

## Slide 1 — Title

**Speaker:** Karlo (~12 s)

**Layout.** Full-bleed Ink background. A single slow-rotating force-directed graph fills the left half at 35% opacity, with edges pulsing faintly between mint and coral as if a contagion is rippling across them — but in reverse, the pulse always damps out before reaching the right edge. Subliminal: containment.

**Right half.** Vertically centered:
- Pre-title in Coral, all caps, letter-spaced 0.18em: `STAT 175 · FINAL PROJECT`
- Title in Paper, Inter Tight 900, 84 pt, max two lines:
  > Cost-Constrained Edge Removal
  > for Epidemic Containment
- Subtitle in Mist, 28 pt, italic: `On the social graphs of five U.S. universities.`
- Author line, 22 pt, Paper at 70% opacity: `Karlo Vrančić · Alec [Lastname] · Jackson [Lastname] · Ryan [Lastname]`
- Date stamp, JetBrains Mono, 18 pt, Slate: `Spring 2026 · Prof. Austern`

**Easter egg.** The pulsing color of the graph follows the speaking cadence — when Karlo's voice picks up, the pulses speed up. (If we don't have audio reactivity, fake it with a fixed 1.2 Hz pulse that feels like a calm heartbeat.)

---

## Slide 2 — The premise

**Speaker:** Karlo (~10 s)

**Layout.** Three stacked words, centered, large.

```
WHO MEETS WHOM
```

In Inter Tight 900, 160 pt, Paper. No subtitle. No body text. Negative space everywhere.

The animated graph drifts very slowly behind the text, cropped tight so individual edges are visible.

**Build.** The phrase enters one word at a time, 200 ms apart. After all three land, the word `MEETS` glows briefly in Coral, then settles back to Paper.

The point of this slide is to land the word "meets" — the unit of analysis is an edge, not a person.

---

## Slide 3 — The constraint

**Speaker:** Karlo (~12 s)

**Layout.** Split into two halves by a thin vertical hairline in Slate.

**Left half.** A small icon row, Inter Tight 600, 36 pt:

> **Lockdowns.** Closed schools. Travel bans.

Each phrase has a tiny strikethrough that draws itself in over the prior phrase as Karlo speaks. The phrases gray out one by one — a visual purge of the obvious answers.

**Right half.** A single phrase in Coral, 56 pt:

> **You don't remove people.**
> **You remove ties.**

The word `ties` is underlined with a hand-drawn-style coral squiggle that completes after a 400 ms delay.

Easter egg: the strike-throughs on the left are hand-drawn SVGs that look like marker scratches, slightly imperfect — a small humanizing touch in an otherwise clean design.

---

## Slide 4 — The question

**Speaker:** Karlo → handoff to Alec (~10 s)

**Layout.** Single slide, full-width text block, vertically centered.

The headline question, Inter Tight 700, 56 pt, in Paper:

> What is the **lowest-cost** set of edges to cut
> so the disease stays under control?

The two phrases `lowest-cost` and `under control` are highlighted with a 6 px Coral underline. Everything else is Paper.

Below the question, in Slate, JetBrains Mono, 22 pt — a stripped formal restatement that reads like a function signature:

```
minimize  Σ cost(e)  s.t.  prevalence(G \ E_cut) < threshold
        e ∈ E_cut
```

This is the only slide where the audience is asked to read math-y text. It's the formalization moment. The transition out is unusually slow (340 ms) so the formal version sticks.

---

## Slide 5 — The model

**Speaker:** Alec (~14 s)

**Layout.** Centered SIS compartment diagram, animated.

Three large rounded squares horizontally arranged, each 240×240, with 80 px gaps:

- `[ S ]` in Mint
- `[ I ]` in Coral
- (back to S)

Two arrows:
- S → I labeled `β · (# infected neighbors)` in JetBrains Mono, 22 pt
- I → S labeled `γ` in JetBrains Mono, 22 pt, looping back via a curved arrow above the diagram

Below the diagram, four lines arrange as a tight footnote in Mist, 18 pt:
> Susceptible · Infected · Susceptible — recovery without immunity. The COVID-style assumption.

**Build.** A small marker dot starts in `S`, animates rightward to `I` (green→red transition mid-flight), pauses, then loops back along the upper arrow to `S`. Repeats slowly while Alec speaks.

**Easter egg.** Watch carefully — every fifth cycle, the dot doesn't recover. A trail of red marker dots accumulates faintly in `I`. By the time Alec says "endemic," there are 5-6 dots stuck. (Subliminal: this is the endemic regime.)

---

## Slide 6 — The threshold

**Speaker:** Alec (~16 s)

**Layout.** Left-right split, 50/50.

**Left.** A clean phase-transition plot.
- X-axis: `R₀ = β · λ₁(A) / γ`, JetBrains Mono 16 pt.
- Y-axis: `Steady-state prevalence`.
- A canonical sigmoidal curve rises from 0 around R₀ = 1 and saturates near 0.7.
- A thin Slate vertical dashed line at `R₀ = 1`, labeled `τ_c` in italic.
- The region left of the dashed line is shaded **Mint** at 18% alpha; the region right is shaded **Coral** at 18% alpha.
- Two small floating labels: "dies out" (mint, left), "endemic" (coral, right).

**Right.** A single equation, JetBrains Mono 56 pt, centered:

> τ_c = 1 / λ₁(A)

Above the equation in Mist 18 pt: `Wang, Chakrabarti, Wang, Faloutsos (2003)`.

Below the equation in Paper 22 pt: `Cut edges → shrink λ₁ → push τ_c right → contain.`

**Build.** The phase-transition curve draws itself left-to-right in 700 ms when the slide opens. The equation fades in 200 ms after the curve completes.

**Easter egg.** A tiny coral pin marker sits on the curve, just barely above the threshold, around R₀ ≈ 1.5. Its position is exactly where most of our headline results live. Audience won't catch this on first viewing; speakers can if they look down at the laptop.

---

## Slide 7 — The cost

**Speaker:** Alec (~16 s)

**Layout.** Three-column visual.

**Column 1 — features.** Two stacked illustrations of a node's feature vector, rendered as a small grid of 6×3 cells:
- Top: `Alice` — cells colored by category (`dorm: Adams · year: 2024 · major: CS · gender: F`), shown as 18 mostly-empty cells with 4 highlighted in Coral.
- Bottom: `Bob` — same grid, 4 highlighted cells, partially overlapping with Alice's.

Above the grids, in Mist 16 pt: `One-hot encoding · L2-normalized`.

**Column 2 — operation.** A massive circle-symbol stack, Inter Tight 900, vertically centered:

> ⟨ x_u , x_v ⟩

Below it, in JetBrains Mono 28 pt: `→ σ(·)`

**Column 3 — cost.** A single number rendered huge: `0.71`, Inter Tight 900, 120 pt, Coral. Below it, in Paper 22 pt: `expensive edge`.

**Build.** Cells in Column 1 highlight one-by-one; the dot-product symbol in Column 2 pulses; the cost number in Column 3 ticks up rapidly from `0.50` to `0.71` over 600 ms (counter animation).

**Easter egg.** A second mini-example flashes for 800 ms after the first lands: a 2nd `0.53` (mint) appears beneath the `0.71`, labeled `acquaintance — cheap`. Then it fades. Reinforces "high cost = similar = close friend" without saying it aloud.

---

## Slide 8 — Four policies

**Speaker:** Jackson (~12 s)

**Layout.** A 2×2 grid of cards. Each card is 720×360, with 80 px gutters. Ink background; cards have a subtle 1 px Slate border and a tiny coral corner accent in the top-left.

Each card contains:
- Top-left: a single rank number (`01`, `02`, `03`, `04`) in JetBrains Mono 28 pt, Coral.
- Center: a small custom icon (described below), 120×120, Mint stroke on Ink.
- Bottom: a one-word label, Inter Tight 700, 32 pt, Paper.

**Cards.**
1. `Random` — icon: a fistful of broken-line edges scattered randomly.
2. `Betweenness` — icon: a bridge-shaped graph with one central edge highlighted Coral.
3. `Distance` — icon: three concentric Mint circles (community bubbles) with edges between rings highlighted Coral.
4. `GNN` — icon: a small network with a stylized neural-net "lens" overlay (three small dots → larger dot).

**Build.** All four cards fade in simultaneously, but the borders draw themselves left-to-right across the 2×2 grid like a TV scan-line. Total animation: 500 ms.

After Jackson names the policies, the GNN card's coral corner-accent **expands** into a thin coral border around the entire card — a visual cue that this is the novel one — and stays that way through Slide 9 (continuous between slides).

---

## Slide 9 — Three are obvious

**Speaker:** Jackson (~18 s)

**Layout.** A horizontal scroll of three vignettes, each 33% width. The vignettes are tight, micro-illustrated, with one short label.

**Vignette 1 — Random.**
- Visual: a small graph (~30 nodes); about 8 edges flicker and disappear at random.
- Label below, Mist 18 pt: `the floor`.

**Vignette 2 — Betweenness / cost.**
- Visual: the same graph with a single bridge edge highlighted Coral, then deleted in a slow fade.
- Label below, Mist 18 pt: `bang for buck`.

**Vignette 3 — Distance threshold.**
- Visual: the same graph partitioned into three Mint-shaded community bubbles by Louvain; cross-bubble edges fade out one by one.
- Label below, Mist 18 pt: `stay in your bubble`.

A tiny line connects the three vignettes at the top, like a ruler with tick marks at `naive`, `classical`, `realistic`. The ruler is JetBrains Mono 14 pt, Slate.

**Easter egg.** The graphs in all three vignettes are the **same** initial graph, just with different cuts applied — so the audience can visually compare which cuts each policy makes. None of the speakers point this out; the parallelism does the work.

---

## Slide 10 — The novel one

**Speaker:** Jackson (~22 s)

**Layout.** Centered architecture diagram, 80% slide width.

A horizontal flow with five labeled stages, connected by Slate arrows:

```
[ feature matrix X ]
        ↓
[ TruncatedSVD → 64-dim ]
        ↓
[ GraphSAGE × 2 layers ]   ← labeled "self-supervised on link prediction"
        ↓
[ embeddings  z_v ∈ R^16 ]
        ↓
[ cost(u,v) = σ(⟨z_u, z_v⟩) ]
```

Each stage is a rounded rectangle with a 1 px Mist border. The middle stage (`GraphSAGE`) is filled with Coral at 8% alpha to highlight that it's the learned component.

A second arrow exits the bottom of the final stage:

```
       ↓
[ score(e) = (u_i v_j + u_j v_i) / cost(u,v) ]   ← in JetBrains Mono 22 pt
       ↓
[ greedy fill until budget ]
```

The phrase `(u_i v_j + u_j v_i)` is annotated with a tiny floating label in Mist 14 pt: `NetMelt eigenscore (Tong 2012)`. The annotation has a thin leader line.

**Build.** The diagram draws itself one stage at a time, with a 250 ms beat between each. The annotations appear last. Total: ~1.5 s.

**Easter egg.** The arrow between `GraphSAGE` and `embeddings` is animated — small Coral dots travel down the arrow continuously, slow, suggesting messages passing in a graph neural network.

---

## Slide 11 — Why bother training a model

**Speaker:** Jackson (~14 s)

**Layout.** Two side-by-side columns. Left labeled `HAND-DESIGNED`, right labeled `LEARNED`. Big serifed labels in Inter Tight 700, 28 pt, Paper.

**Left.**
- A small text snippet in JetBrains Mono 18 pt:
  ```
  cost(u,v) = σ(<x_u, x_v>)
  ```
- Below it, in Mist 16 pt: `Same dorm? Same year? Probably close.`
- Sketch of two stick-figure faces with overlapping social circles.

**Right.**
- A small text snippet in JetBrains Mono 18 pt:
  ```
  cost(u,v) = σ(<z_u, z_v>)
  ```
- Below it, in Mist 16 pt: `What does the graph itself say about closeness?`
- Sketch of the same two faces, but now connected through a flickering web of secondary nodes — implying that the model picks up shared neighbors, second-order ties, etc.

The two columns are separated by a thin vertical Coral hairline. At the bottom, a single line in Paper 24 pt:

> The cost function is what's learned.

Underlined word: `learned`.

---

## Slide 12 — Handoff card

**Speaker:** Jackson → Ryan (~5 s)

A throwaway transition slide, intentionally minimal:

- Centered, single line, Inter Tight 700, 72 pt, Paper:
  > **Does it work?**
- Below, in Mist 24 pt: `Five campuses. Four policies. Eight budgets.`

The chrome budget-bar at the bottom is now ~60% filled. The number tag at the bottom-left reads `60% / 100%`.

This slide is on screen for under 4 seconds. It exists to give Ryan a clean visual reset before the results.

---

## Slide 13 — Headline result

**Speaker:** Ryan (~22 s)

**Layout.** A single, large, beautifully typeset Pareto-frontier plot, 75% slide width, centered. Margins: generous.

**Plot details.**
- X-axis: `cost budget (% of total)`, ticks at `0`, `0.5`, `1`, `2`, `5`, `10`, `20`, `40`. Logish spacing.
- Y-axis: `steady-state prevalence`, 0 to 0.6.
- Four curves:
  - **GNN** in Coral, 3 px stroke, with a soft 8 px Coral glow. Marker dots at every tick.
  - **Distance Threshold** in Mint, 2 px stroke. Square markers.
  - **Edge Betweenness** in Slate, 2 px stroke. Triangle markers.
  - **Random** in Mist, 1.5 px stroke, dashed. Small open-circle markers.
- All four curves descend roughly monotonically; GNN sits visibly below the others in the 0-10% budget range, then converges with the others by 40%.
- A vertical Slate dashed line at `5%` budget. At its intersection with each curve, a small annotation in JetBrains Mono 14 pt:
  - GNN: `−4.0 pp`
  - Distance: `−2.2 pp`
  - Betweenness: `−1.7 pp`
  - Random: `−1.6 pp`
- The GNN annotation is in Coral 16 pt and bolder than the others.
- Title above the plot, Inter Tight 700, 28 pt, Paper: `R₀ ≈ 1.5 — near the threshold`.
- Caption below in Mist 14 pt: `Mean over 50 stochastic SIS runs · 95% bootstrap CIs · Caltech36, Bowdoin47, Harvard1, Penn94, Tennessee95.`

**Build.** Curves animate left-to-right one at a time in stacking order: Random → Betweenness → Distance → GNN. Each takes 600 ms. The 5% annotation appears last with a soft fade and a small "tick" sound (if audio is enabled — visual only otherwise).

**Easter egg.** The Coral glow around the GNN curve subtly pulses at the same 1.2 Hz heartbeat as the title slide. Continuity.

---

## Slide 14 — But the picture flips

**Speaker:** Ryan (~14 s)

**Layout.** Same plot as Slide 13 transitions in place to a new R₀.

The transition: title text morphs from `R₀ ≈ 1.5 — near the threshold` to `R₀ = 6.0 — heavily endemic`. The four curves smoothly interpolate to their R₀=6 shapes (we precompute the keyframes and tween them).

In the new state:
- Distance Threshold (Mint) and Betweenness (Slate) sit visibly **below** GNN (Coral).
- GNN no longer has its glow — the glow has migrated to Distance Threshold.
- The 5% annotation now ranks Distance > Betweenness > GNN > Random.

A small overlay text in the upper-right of the plot, Coral 22 pt:
> **The GNN is not always the answer.**

This slide is the talk's intellectual pivot — the moment it goes from "look at our cool method" to "the cost-aware framing reorders everything." The visual trick (same plot, smooth tween, glow follows the winner) does the heavy lifting.

---

## Slide 15 — Robustness in three rows

**Speaker:** Ryan (~24 s)

**Layout.** Three small horizontal panels stacked vertically. Each panel is a mini-plot, 20% slide height.

**Row 1 — Compliance.**
- Title left, Inter Tight 600, 22 pt: `Compliance`
- Mini bar chart: GNN @ 60% compliance vs all four policies @ 100% compliance, side-by-side. GNN's reduced bar is **still taller** than the next-best.
- Caption right, Mist 14 pt: `60% beats every other policy at 100%.`

**Row 2 — SIR vs SIS.**
- Title left: `SIR alternative`
- Mini side-by-side Pareto frontiers — SIS on the left, SIR on the right. The same regime-split pattern is visible, but **sharper** in SIR.
- Caption right: `Same regime split — sharper.`

**Row 3 — Adversarial seeding.**
- Title left: `Adversarial seeding`
- Mini bar chart: GNN policy at R₀=6 wins both random and adversarial seeding (with an arrow pointing to the adversarial bar).
- Caption right: `GNN takes both regimes when seeded at the eigenvector backbone.`

The three rows are separated by 24 px gaps and a faint Slate hairline.

**Build.** Each row fades in 250 ms after the previous. Total: ~1 s.

**Easter egg.** The titles of the three rows form a vertical alignment that mirrors the spacing of the SIS/SIR/etc. panels in our paper's results figure — visual continuity between the talk and the paper for anyone who's read both.

---

## Slide 16 — Architecture doesn't matter

**Speaker:** Ryan (~10 s)

**Layout.** Three nearly-identical bar charts side by side, each 30% slide width, with the same y-axis scale.

- Bar 1: `GraphSAGE` — bar height 0.040
- Bar 2: `GAT` — bar height 0.039
- Bar 3: `GCN` — bar height 0.041

All three bars are Coral. Y-axis labeled `prevalence reduction at 5% budget`, Mist 12 pt.

Below the three plots, centered, Inter Tight 700, 32 pt, Paper:

> **The framework is what matters,** not the message-passing operator.

The word `framework` is underlined in Coral.

A tiny Mist 14 pt footnote: `Cost-learning > architecture choice.`

**Easter egg.** The three bar charts have identical axis labels but slightly different shades of Ink in their plot backgrounds (`#0B1020`, `#0C1122`, `#0A0F1E`). The variation is invisible to the human eye but it's a callback to "the architectures look identical because they basically are."

---

## Slide 17 — Honest caveat

**Speaker:** Ryan (~14 s)

**Layout.** Almost-empty slide. Ink background. A single block-quote, vertically centered, in Paper 38 pt, italic, max width 60% slide:

> Facebook100 is a **friendship graph**, not a contact graph.
>
> We're not solving COVID.

The two phrases `friendship graph` and `not a contact graph` are subtly underlined in Slate (not Coral — this is a quiet moment, not a punchline).

Below the quote, in Mist 18 pt:

> What we're showing is that **cost-aware framing** changes which policies look "best."

A single small Coral square sits at the bottom-center of the slide as a visual full-stop. Nothing else.

**Easter egg.** The quote's typography uses real "smart quotes" (`"` `"`), proper em dashes (`—`), and slightly hung punctuation. The kind of typography care that academic slides rarely bother with. Subliminal: we sweat the details.

---

## Slide 18 — Web app teaser

**Speaker:** Ryan (~12 s)

**Layout.** Mostly screenshot, framed.

A high-res mock of the Streamlit app, taking 75% of the slide. The screenshot has:
- A sidebar on the left with sliders (`R₀ = 1.5`, `Budget = 5%`, campus dropdown showing `Caltech36`).
- A main panel showing an animated SIS curve and a small graph viz with greyed-out edges.
- A small Pareto frontier in the bottom-right of the app.

A Coral arrow points to the campus selector with an annotation in JetBrains Mono 16 pt: `pick a campus`.
A Coral arrow points to the budget slider: `dial the budget`.
A Coral arrow points to the graph viz: `watch it spread`.

In the upper-right corner of the slide, in JetBrains Mono 16 pt, Coral:

> **DEMO →**

Below the screenshot, centered, in Paper 22 pt:

> Built with Streamlit. Runs locally on a laptop.

**Build.** Static — no animation. The slide stays on screen long enough for Ryan to switch to the live demo.

**Easter egg.** The screenshot's settings (`R₀ = 1.5`, `Budget = 5%`, `Caltech36`) match exactly the headline numbers from Slide 13. If anyone is paying attention, the demo will reproduce the headline result live.

---

## Slide 19 — Live demo (placeholder)

**Speaker:** Ryan (~30 s if live, skipped if presenting in pre-recorded mode)

**Layout.** Single Coral panel covering 100% of the slide. Centered, Inter Tight 900, 200 pt, Ink:

> **LIVE**

That's it. It's a "we're switching applications now" interstitial. The presenter alt-tabs to Streamlit during this slide.

If live demo is unavailable, this slide is skipped automatically (deck logic). The deck's chrome budget-bar at the bottom does NOT advance during this slide — it's a free interlude.

---

## Slide 20 — Closing

**Speaker:** Ryan (~10 s)

**Layout.** Mirror of the title slide, but inverted.

- Pre-title, Coral, all caps, letter-spaced 0.18em: `THANK YOU`
- Title, Paper, Inter Tight 900, 64 pt:
  > Questions?
- Below, Mist 22 pt:
  > Code: `github.com/[handle]/stat175-project` *(or whatever URL we end up with)*
  > Paper draft & figures: `paper/main.pdf` in the repo.
- The same drifting graph from Slide 1, now visibly **thinner** (≈ 40% of original edges remain — the deck has been "cutting" edges for the entire talk).

The chrome budget-bar at the bottom is **fully filled**, and the slide-number tag reads `100% / 100%`.

**Easter egg.** Below the URLs, in Mist 12 pt at 50% opacity: `Caltech 36 · Bowdoin 47 · Harvard 1 · Penn 94 · Tennessee 95`. Just the campus list, hung as a typographic flourish at the bottom of the closing slide.

---

## Easter eggs index (for the curious)

A summary of the small touches scattered through the deck, in case the team wants to call attention to any during the Q&A.

| # | Slide | Egg |
|---|---|---|
| 1 | All slides | Coral budget-bar fills left-to-right across the entire deck. |
| 2 | All slides | Drifting graph in upper-right loses edges as the talk progresses. |
| 3 | All slides | Slide numbers shown as `XX% / 100%`, not `n / 20`. |
| 4 | All slides | Bottom-right speaker tag cycles names — no in-talk introductions needed. |
| 5 | Slide 5 | A red dot accumulates in the `I` compartment every fifth cycle — endemic regime, visualized. |
| 6 | Slide 6 | A coral pin marker on the phase-transition curve sits exactly where our headline R₀=1.5 result lives. |
| 7 | Slide 7 | A second `0.53` cost example flashes briefly to anchor "cheap edge" without saying it. |
| 8 | Slide 9 | All three vignettes share the same starting graph — visual A/B/C comparison without narration. |
| 9 | Slide 10 | Animated Coral dots travel down the GraphSAGE arrow continuously — graph-message-passing as ambient motion. |
| 10 | Slide 13 | GNN curve glow pulses at the same heartbeat (1.2 Hz) as the title slide. |
| 11 | Slide 14 | The Coral glow migrates from GNN to Distance Threshold — winner gets the glow. |
| 12 | Slide 16 | The three nearly-identical Ink shades behind the bars are a subliminal "they're basically the same." |
| 13 | Slide 17 | Real smart quotes, em dashes, and hung punctuation — typographic care as a credibility signal. |
| 14 | Slide 18 | The Streamlit screenshot's settings match Slide 13's headline numbers exactly. |
| 15 | Slide 19 | Budget-bar pauses during the live demo — the talk's "cost" doesn't advance during exploration. |
| 16 | Slide 20 | The drifting graph is visibly thinner than Slide 1 — the audience watched containment happen. |

---

## Deck-level notes

- **Total slides:** 20 (19 if `LIVE` is skipped). Average dwell ≈ 15 seconds; Slide 13 (headline plot) and Slide 14 (regime flip) get ~22 seconds each. Several slides (2, 12, 19) are under 8 seconds.
- **Color discipline:** every Coral element in the deck represents either *cost* or *the GNN's role*. Mint always means *contained / safe / community*. Slate is *baseline / classical*. Mist is *random / footnote / ambient*.
- **No clip art, no stock images, no template chrome.** Everything custom.
- **No bullet point lists.** Anywhere. If a slide feels like it needs bullet points, the slide isn't the right slide.
- **Transcript is sovereign.** None of the slides repeat lines from `lightning-talk.md`. The slides anchor the audience visually while the speakers do the talking.
- **Build implementation hint:** Keynote with custom typography or Reveal.js (`reveal.js`) would both implement this cleanly. Keynote has nicer slide-to-slide transitions out of the box; Reveal.js makes the budget-bar and animated chrome elements easier to script.
