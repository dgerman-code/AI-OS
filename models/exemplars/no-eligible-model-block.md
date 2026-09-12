# Exemplar 7 — No eligible model: BLOCK rather than silent degradation

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that `BLOCKED_FOR_ROUTING` is a **correct outcome**, and that "best available" does not exist in this architecture.

## Task context
Structured extraction from privileged legal correspondence for a Decision-Grade submission. Criticality **Enhanced Decision-Grade**. Material sensitivity **`PRIVILEGED`** and `PERSONAL_DATA`.

## Requirements
`MAX_DATA_SENSITIVITY_ALLOWED` ≥ `PRIVILEGED`; `REQUIRED_RESIDENCY_OR_JURISDICTION`; `NO_TRAINING_ON_INPUT`; `capability.structured_extraction` `STRONG` on `INTERNAL_EVALUATION`, verdict `CURRENT_FOR_USE`; `MINIMUM_RELIABILITY_CLASS` raised.

## Candidate assessment
| Candidate | Eligible? | Excluded by |
|---|---|---|
| `model.extractor_e` @ `deployment.sovereign_region_e` | **No** | Deployment maximum is `PERSONAL_DATA`; the material is also `PRIVILEGED`, which no approved deployment currently covers |
| `model.extractor_e` @ `deployment.local_inference_e` | **No** | Covers `PRIVILEGED`; extraction evidence is `PAST_REFRESH_INTERVAL` → **`STALE_AND_BLOCKING`** at this band |
| `model.midsize_analyst_d` @ `deployment.private_cloud_d` | **No** | `BASELINE` structured extraction — below the minimum |
| `model.frontier_reasoning_b` @ `deployment.public_hosted_b` | **No** | Deployment maximum `PUBLIC`. Excluded at **stage 2** |

## Outcome
**`NO_ELIGIBLE_MODEL` → `BLOCKED_FOR_ROUTING`**, naming the unsatisfiable combination: no approved deployment covers `PRIVILEGED`, and the one that does has stale evidence for this band.

## What this actually shows
Four candidates, each failing for a different reason, and **none of them "closest"**. The second row is the tempting one: the right deployment, the right model, evidence three weeks past its refresh interval. Routing there would have been a degradation on the exact dimension — extraction reliability on privileged material — that the band's evidence requirement exists to protect.

**There is no partial eligibility.** "Fewest violations" is not a concept this architecture contains, and a block is not the router failing. It is the router reporting, accurately, that the work as specified needs something the registry cannot lawfully or capably provide — and handing that to the people who can change the requirement, approve a deployment for `PRIVILEGED`, refresh the evaluation, or do the work another way.

Each of those is a decision someone must take deliberately. **The one outcome the architecture refuses is the one where nobody decides anything and the work quietly gets done by something unqualified to do it.**
