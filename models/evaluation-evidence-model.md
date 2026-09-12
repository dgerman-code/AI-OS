# Evaluation Evidence Model

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Scope: evidence semantics, not an evaluation system

Phase 9 defines **what counts as evidence for a capability claim, how strong it is, and when it goes stale.** It defines no benchmark, no harness, no test suite, no scoring function, no leaderboard and no evaluation service. Building the evaluation system is later work; **its output has to mean something first**, and that is what this document fixes.

## 2. Evidence classes

Kept distinct because they fail in different ways.

| Class | What it is | Characteristic weakness |
|---|---|---|
| `PROVIDER_DECLARED` | The provider's own statement of capability | Not independent; describes intended behaviour; changes without notice |
| `EXTERNAL_BENCHMARK` | A published benchmark result | Measures the benchmark; may be contaminated, saturated, or unrelated to the work |
| `INTERNAL_EVALUATION` | The organisation's own evaluation on its own material | Costly, narrow, and as good as its design — **and the only class measuring the work actually done here** |
| `HUMAN_EXPERT_ASSESSMENT` | A qualified human's judgement after use | Subjective, small-sample, and irreplaceable for dimensions no benchmark captures |
| `OBSERVED_PRODUCTION` | Evidence from real prior use | **Runtime-originated. Phase 9 defines its semantics and collects none of it** |
| `KNOWN_LIMITATION_OR_INCIDENT` | A recorded failure, regression, outage or defect | **Negative evidence, and it does not expire on the positive evidence's schedule** |

### Rules

1. **`PROVIDER_DECLARED` is admissible and is not proof.** It is evidence that a provider made a statement.
2. **A benchmark score is not authority.** Its relevance to this organisation's work is itself a claim requiring its own justification.
3. **Classes never merge.** Three provider declarations are not an internal evaluation, and no quantity of weak evidence becomes strong evidence.
4. **`KNOWN_LIMITATION_OR_INCIDENT` outranks positive evidence — but only where it is *applicable*.** A documented failure mode is not averaged against claims that the model performs well; where applicable it narrows or disqualifies the claim. Applicability is determined, not assumed: see §2a.
5. **A Routing Policy declares which classes it accepts, per capability and per criticality band.** Evidence the policy does not accept leaves the claim **unevidenced for that policy** — the claim still exists, and it buys no eligibility.

## 2a. Applicability of negative evidence

The first draft said negative evidence always outranks positive evidence. The audit was right that this is unbounded: it would let a stale, anecdotal, already-remediated report about a superseded release permanently dominate current verified evidence about a different context.

**Negative evidence restricts a capability claim only where it applies to it.** Applicability is assessed on seven dimensions, each recorded:

| Dimension | The question |
|---|---|
| **Release and profile version** | Does it concern **this** underlying release and this profile version, or a superseded one? |
| **Provider / deployment context** | Was it observed through this exposure, or a different one? |
| **Capability dimension** | Which claim does it bear on? A coding incident bears on coding |
| **Task or domain context** | Was it in a domain this task shares? |
| **Materiality and severity** | How bad, and does it matter for this use? |
| **Evidence quality** | Reproduced and verified, or a single unreproduced report? |
| **Freshness and effective period** | When, and does it still hold? |
| **Remediation status** | Open, mitigated, or resolved and verified? |

### Rules

1. **Stale evidence about a superseded version does not automatically dominate current evidence** about the current one. It remains relevant as history and as a reason to look, not as a standing disqualification.
2. **A context-specific incident does not automatically invalidate unrelated contexts.** A failure observed through one provider's exposure bears on that exposure; extending it further requires a reason, stated.
3. **Low-quality anecdotal evidence does not permanently override stronger verified evidence** without a recorded materiality assessment — attributable and reviewable, on the Phase 8 model.
4. **A severe, current safety or data-handling incident may restrict routing immediately, pending review.** Precaution is available where severity and currency are both present, and it is a restriction with an owner and a review point, not a permanent verdict.
5. **Conflicting evidence creates a governed conflict state, not an average.** Where positive and negative evidence both apply and disagree materially, the claim carries **`EVIDENCE_CONFLICT`** — visible, blocking for the bands whose policy says so, and cleared only by a recorded resolution. Phase 8's conflict rules govern: later is not superior, authority is not evidence, and the losing evidence is retained.
6. **No composite score is introduced by any of this.** Applicability narrows or does not narrow a specific claim on a specific dimension. Nothing is summed.

**Unassessed applicability is not inapplicability.** Negative evidence whose applicability nobody has assessed is treated as applicable until someone assesses it — the strict reading, consistent with the rest of this architecture.

## 3. Evaluation dimensions

Evaluated **separately**, never combined:

`capability fitness` · `instruction fidelity` · `structured-output reliability` · `unsupported-claim risk` · `coding correctness` · `review-detection quality` · `citation and evidence handling` · `latency class` · `cost class` · `safety and privacy suitability` · `language and domain performance`

> **No composite score exists in this architecture, and no single number may ever become routing authority.**

A composite would let strength on one dimension mask disqualifying weakness on another — a model that reasons superbly and follows instructions poorly scores well and is the wrong tool for constrained work. Dimension-specific evidence and dimension-specific thresholds are how a routing constraint stays checkable, and a rank order of models is not expressible here by design.

`review-detection quality` deserves separate mention: the ability to **find defects in work** is not the ability to produce it, and evidence of the second is not evidence of the first. A model routed to a review task on the strength of its authoring evidence has been selected on the wrong dimension.

## 4. Confidence

Each claim carries a confidence — `LOW` / `MEDIUM` / `HIGH` — reflecting evidence strength, breadth and age.

**Confidence never creates eligibility.** It ranks within the eligible set (`PREFER_HIGHER_CAPABILITY_EVIDENCE`) and nothing else. A `HIGH` confidence claim on one capability does not satisfy a requirement on another, does not compensate for a failed eligibility constraint, and does not substitute for the evidence class a policy requires.

**Confidence is about the evidence, not about the model.** High confidence that a model is weak at something is a perfectly ordinary record.

## 5. Freshness — reusing Phase 8, not reinventing it

Phase 8's model applies unchanged (`knowledge/sensitivity-and-retention-model.md` §3): **item-level temporal facts on the record, use-context verdicts at the point of use.** Phase 9 defines no new freshness states.

Item-level facts on a capability claim: as-of date; last verified; expected refresh interval; review-by; the derived age condition **`PAST_REFRESH_INTERVAL`**.

Use-context verdicts at routing time: `CURRENT_FOR_USE` · `STALE_BUT_USABLE` · `STALE_AND_BLOCKING` · `EXPIRED_FOR_USE`.

**The same evidence is current for one routing decision and blocking for another, at the same moment**, because the verdict is a property of the use: stale evidence is usable for routine drafting and blocking at Enhanced Decision-Grade. No verdict is written back onto the profile.

### Refresh triggers

`PROVIDER_VERSION_CHANGE` · `PROVIDER_TERMS_CHANGE` · `DEPLOYMENT_CHANGE` · `INCIDENT_OR_REGRESSION` · `LIFECYCLE_CHANGE` · `REVIEW_BY_REACHED` · `NEW_CONTRADICTING_EVIDENCE`

**Model behaviour drifts under a stable name.** Providers update models, terms and defaults without a version change the consumer sees, so `PROVIDER_VERSION_CHANGE` and `PROVIDER_TERMS_CHANGE` fire on *any* observed change — and `PROVIDER_TERMS_CHANGE` in particular can invalidate a `REQUIRED_DATA_HANDLING_POSTURE` constraint without touching a single capability claim.

## 6. Evidence is about a tool, never about the world

A capability claim is **never** knowledge about the world and never enters Phase 8's canonical governance as such. Evidence that a model is strong at financial analysis is evidence about the model; a financial analysis it produces is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`, whatever the evidence says, and **no evaluation result shortens that path** (`knowledge/knowledge-state-model.md` §2a).

## 7. Status

`PROPOSED`. Builds no evaluation system, defines no benchmark, produces no score.
