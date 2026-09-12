# Exemplar 7 — No eligible model: BLOCK rather than silent degradation

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that `BLOCKED_FOR_ROUTING` is a **correct outcome**, and that "best available" does not exist in this architecture.

## Task context
Structured extraction from privileged legal correspondence for a Decision-Grade submission. Criticality **Enhanced Decision-Grade**.

**Material sensitivity labels: `PRIVILEGED` + `PERSONAL_DATA`.** Two labels, **both required simultaneously**, neither above the other. Privilege can be lost by handling — which no other Phase 8 class can be — and personal data carries obligations independent of every other class.

## Candidate universe
Registry state `reg.snapshot.2026-09-11T09:00Z#4482`; universe definition `cud.decision_grade_restricted` v2. Enumerated: 4. **`CANDIDATE_UNIVERSE_COMPLETE`** — so the block below is a fact about the registry, not about what happened to load.

## Requirements
**`SUPPORTED_SENSITIVITY_CLASSES` ⊇ {`PRIVILEGED`, `PERSONAL_DATA`}** — both, explicitly; `REQUIRED_HANDLING_CONTROLS` per label; `REQUIRED_JURISDICTION`; `REQUIRED_DATA_HANDLING_POSTURE` = no training, no retention beyond the task; `capability.structured_extraction` `STRONG` on `INTERNAL_EVALUATION`, verdict `CURRENT_FOR_USE`; `MINIMUM_RELIABILITY_CLASS` raised.

**Exceptionability, per `models/routing-constraint-model.md` §5.2:** the `PRIVILEGED` handling requirement is **`ABSOLUTELY_NON_WAIVABLE`** — Phase 8 holds that a restriction arising from `PRIVILEGED` cannot be relaxed by an internal decision, so **no Phase 7 Right adjusts it**. The evidence-freshness requirement is `GOVERNED_EXCEPTION_POSSIBLE` in principle; no Right covering it was exercised here.

## Candidate assessment
| Candidate | Eligible? | Excluded by |
|---|---|---|
| `model.extractor_e` @ `deployment.sovereign_region_e` | **No** | Supports `PERSONAL_DATA`, **not `PRIVILEGED`**. Supporting one of two required labels satisfies nothing: both are required simultaneously |
| `model.extractor_e` @ `deployment.local_inference_e` | **No** | Supports **both** labels with handling controls met — and extraction evidence is `PAST_REFRESH_INTERVAL` → **`STALE_AND_BLOCKING`** at this band |
| `model.midsize_analyst_d` @ `deployment.private_cloud_d` | **No** | `BASELINE` structured extraction — below the minimum |
| `model.frontier_reasoning_b` @ `deployment.public_hosted_b` | **No** | Supports {`PUBLIC`}. Excluded at **stage 2** |

## Outcome
**`NO_ELIGIBLE_MODEL` → `BLOCKED_FOR_ROUTING`**, naming the unsatisfiable combination: only one deployment supports **both** required labels, and its evidence is stale for this band.

This is **case C** of `models/routing-precedence-and-fallback.md` §5 for the first, third and fourth rows — nothing to except. The second row is **case B territory and was not taken**: the freshness requirement is exceptionable in principle, no Right covering it was exercised, and so the candidate remains ineligible. **It is not recorded as eligible-pending-exception**, because there is no such state.

## What this actually shows
Four candidates, each failing for a different reason, and **none of them "closest"**. The first row is the one a ceiling model would have got wrong: a deployment approved for `PERSONAL_DATA` looks like a strong one, and supports **neither more nor less** of what `PRIVILEGED` requires — the two label regimes are simply different, and satisfying one says nothing about the other.

The second row is the tempting one: the right deployment, the right model, evidence three weeks past its refresh interval. Routing there would have been a degradation on the exact dimension — extraction reliability on privileged material — that the band's evidence requirement exists to protect. Reaching it lawfully would take a **governed act first**, changing the requirement, not a judgement call afterwards calling the candidate eligible.

**There is no partial eligibility.** "Fewest violations" is not a concept this architecture contains, and a block is not the router failing. It is the router reporting, accurately, that the work as specified needs something the registry cannot lawfully or capably provide — and handing that to the people who can change the requirement, approve a deployment for `PRIVILEGED`, refresh the evaluation, or do the work another way.

Each of those is a decision someone must take deliberately. **The one outcome the architecture refuses is the one where nobody decides anything and the work quietly gets done by something unqualified to do it.**
