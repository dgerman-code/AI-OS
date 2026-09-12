# Routing Policy Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Routing Policy** is a reusable, versioned rule set: what is eligible, what is preferred, and how ties break. It is a **type**. The instance is a Routing Decision, and a policy existing in the registry has selected nothing.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Routing Policy ID: `routing_policy.<stable_snake_case_name>`
- Policy version: **named by every Routing Decision made under it**
- Scope of application: which task classes, Roles, Workflow stages or criticality bands this governs
- Owner class: never a named person
- Status: PROPOSED

## Hard Eligibility Constraints

| Constraint | Value / threshold | Source of the requirement |
|---|---|---|

Every constraint from `models/routing-constraint-model.md` §2 that applies. **These filter.** A candidate failing any one is ineligible — not disfavoured.

## Soft Preferences, in order

Ordered, not weighted. Order is the mechanism: weights would let a large enough cost weighting outrank reliability, and this model has no weights to tune.

## Accepted Evidence Classes

Per capability and per criticality band: which of `PROVIDER_DECLARED`, `EXTERNAL_BENCHMARK`, `INTERNAL_EVALUATION`, `HUMAN_EXPERT_ASSESSMENT`, `OBSERVED_PRODUCTION`, `KNOWN_LIMITATION_OR_INCIDENT` this policy accepts. **Evidence a policy does not accept leaves the claim unevidenced for that policy.**

## Freshness Requirements
The use-context verdict required — `CURRENT_FOR_USE`, or whether `STALE_BUT_USABLE` is accepted — per criticality band.

## Availability Handling
What `UNKNOWN_AVAILABILITY` means here. **At Enhanced Decision-Grade it is not eligible**; at lower bands, whether an attempt is permitted and how it is recorded.

## Diversity Requirements
The value from `models/review-diversity-and-criticality.md` §2 and the **named prior selection** it is evaluated against. Where the prior decision is unrecorded, the constraint is unsatisfiable and routing blocks.

## Fallback Policy
Which fallback kinds are permitted; whether degraded fallback is allowed and at what materiality it requires human acknowledgement or a governed Phase 7 exception; and the conditions under which this policy **blocks rather than degrades**.

## Deterministic Tie-Break Rule
The declared, ordered rule. **Deterministic and recorded — never random, never "whichever answered first".** Two identical tasks under this version select the same candidate.

## Model Pinning
**None** by default. Where a pin exists: the justification, the named owner class, and the **expiry or review-by**. An unexpiring pin is defective.

## Human Selection
Whether `HUMAN_SELECTION_REQUIRED` applies, and under what conditions. It is **not a filter**: every candidate may pass it and the constraint still be unsatisfied, because what it requires is an act.

## Out-of-Scope Authority
What this policy explicitly does **not** do: approve work, accept risk, satisfy a review, promote knowledge, grant authority, or decide what work happens. A blank section is a defect.

## Versioning
Version history, confirming that no version change silently altered a hard constraint, an accepted evidence class, a diversity requirement or the tie-break.

## Non-Runtime Statement
This policy is declarative architecture. It specifies no matcher, engine, scoring function, SDK, API, credential or runtime.
