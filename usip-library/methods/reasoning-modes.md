# أنماط الاستدلال / reasoning modes

> مولّد من `data/reasoning_modes.json` (الملحق A24). [الفهرس](../README.md)

## الاستنباط / Deductive (`deductive`)

**متى:** rules, specs, contracts, schemas or laws are given and the question is what they imply

**الخطوات:**

1. Write the premises as numbered statements, each with its source.
2. Derive the conclusion step by step; cite the premise numbers on every step.
3. Check each premise is actually true here (a valid argument from a false premise is still false).

**الفخ:** Treating an unverified premise as a fact; a sound-looking chain built on an assumption.

**الفحص:** Every step cites a premise; every premise has a source or is labelled an assumption.

## الاستقراء / Inductive (`inductive`)

**متى:** there are many observations, logs, samples or past cases and the question is the general pattern

**الخطوات:**

1. State the sample: how many cases, how they were selected, what is missing.
2. State the pattern and its strength (count, rate, range), not just its direction.
3. Look for the counter-example before generalising; one solid counter-example limits the claim.

**الفخ:** Generalising from a small or self-selected sample; survivorship bias.

**الفحص:** The claim carries its sample size and selection; at least one search for a counter-example is recorded.

## التفسير الأفضل / Abductive (best explanation) (`abductive`)

**متى:** something broke or looks odd and the question is why: debugging, diagnosis, incident review

**الخطوات:**

1. List at least three rival explanations, including a boring one (config, typo, stale cache).
2. For each, write what you would observe if it were true and what would rule it out.
3. Run the cheapest discriminating test first; keep the explanation that survives, with its evidence.

**الفخ:** Stopping at the first plausible story; fixing a symptom.

**الفحص:** Three or more hypotheses were written and the chosen one survived a test that could have killed it.

## القياس والتمثيل / Analogical (`analogical`)

**متى:** the problem is new but resembles a solved one in another domain, product or codebase

**الخطوات:**

1. Name the source case and map its parts to the target one by one.
2. Mark where the mapping breaks (scale, users, constraints, licence).
3. Transfer the mechanism, not the surface; test the transferred piece alone first.

**الفخ:** Copying surface features; ignoring the place where the analogy breaks.

**الفحص:** A written part-to-part map with at least one stated break point.

## السببية والمضاد للواقع / Causal and counterfactual (`causal`)

**متى:** the question is whether X causes Y, what an intervention will change, or what would have happened otherwise

**الخطوات:**

1. Draw the causal chain X → mechanism → Y and name the confounders.
2. State the counterfactual: what happens to Y without X?
3. Prefer an intervention or a controlled comparison over a correlation; say which one you have.

**الفخ:** Reading correlation as causation; forgetting the do-nothing baseline.

**الفحص:** A baseline or counterfactual is written next to every causal claim.

## التفكير النظمي / Systems (`systems`)

**متى:** many parts interact: pipelines, organisations, feedback loops, second-order effects, long-running projects

**الخطوات:**

1. Draw the stocks, flows and feedback loops (reinforcing and balancing).
2. Find the bottleneck and the leverage point; change one thing there.
3. Ask for the second-order effect of every change: who or what reacts?

**الفخ:** Optimising one part and moving the bottleneck; ignoring delays in feedback.

**الفحص:** The bottleneck is named and each change has a written second-order effect.

## التفكير الجانبي / Lateral (provocation) (`lateral`)

**متى:** the usual answers are stale, the brief asks for something new, or every plan looks the same

**الخطوات:**

1. Write the dominant assumption of the field, then a provocation (Po) that reverses, removes, exaggerates or distorts it.
2. Extract a usable principle from the provocation (movement, not judgement).
3. Turn the principle into a concrete option and give it the same value test as the others (a five-minute experiment).

**الفخ:** Keeping an idea because it is surprising; skipping the value test.

**الفحص:** The provocation, the extracted principle and the value test are all written.

## الوزن البايزي / Bayesian weighing (`bayesian`)

**متى:** evidence of different strength must be combined into a degree of belief before a decision

**الخطوات:**

1. Write the prior from a base rate (reference class), not from the story.
2. For each piece of evidence write a likelihood ratio: how much more likely is it if the hypothesis is true than if it is false?
3. Update with think.py bayes, then check whether the decision flips when any ratio is halved or doubled.

**الفخ:** Ignoring the base rate; counting the same evidence twice; ratios of 100 from one anecdote.

**الفحص:** Prior has a reference class, evidence items are independent, and the sensitivity line is reported.

