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

## Candidate Universe Definition

- **Universe definition version:**
- **Inclusion rule:** which profile states, deployment classes and provider context are enumerated
- **Routing scope:** the bound applied
- **Pre-filter exclusions:** what is outside the universe, and by which rule — distinct from candidates excluded by constraints inside it
- **Availability pre-enumeration:** whether unavailable candidates are excluded before enumeration. **Default: no** — availability is a candidate property and an evaluation result, not a reason to disappear. Any other behaviour must be declared **here**, explicitly
- **On `CANDIDATE_UNIVERSE_INCOMPLETE`:** `BLOCK` or `ESCALATE`. **Never proceed.** A load failure must not silently shrink the universe

Given the same registry state reference and this version, enumeration is reproducible. A bounded universe is permitted; an unexplainable one is not.

## Eligibility Constraints

| Constraint | Value / threshold | Source of the requirement | Exceptionability class |
|---|---|---|---|

Every constraint from `models/routing-constraint-model.md` §2 that applies. **These filter.** A candidate failing any one is ineligible — not disfavoured.

**Exceptionability is derived from the source** (§5.2 there), not chosen for convenience, and **an unclassified constraint is `ABSOLUTELY_NON_WAIVABLE`** for routing. Where a class is `GOVERNED_EXCEPTION_POSSIBLE`, name the `decision.<id>` whose scope covers it — "a Decision Right exists" is not a basis.

## Preference Order — owned by this policy

The **ordered, lexicographic** list of preferences from `models/routing-constraint-model.md` §6. **This policy owns the order**, and may rank reliability above cost or cost above reliability where the work's risk permits.

Ordered, not weighted: a later preference decides only what an earlier one left tied. Weights would let a large enough cost weighting quietly outrank everything else, and this model has none to tune.

Three bounds the policy does **not** own: no ordering restores an ineligible candidate; the **hard stages 1–5 are globally fixed** and no policy reorders them; and where risk requires reliability, it is stated as `MINIMUM_RELIABILITY_CLASS` — an **eligibility constraint** — because a preference is negotiable by definition.

## Accepted Evidence Classes

Per capability and per criticality band: which of `PROVIDER_DECLARED`, `EXTERNAL_BENCHMARK`, `INTERNAL_EVALUATION`, `HUMAN_EXPERT_ASSESSMENT`, `OBSERVED_PRODUCTION`, `KNOWN_LIMITATION_OR_INCIDENT` this policy accepts. **Evidence a policy does not accept leaves the claim unevidenced for that policy.**

## Freshness Requirements
The use-context verdict required — `CURRENT_FOR_USE`, or whether `STALE_BUT_USABLE` is accepted — per criticality band.

## Availability Handling
What `UNKNOWN_AVAILABILITY` means here. **At Enhanced Decision-Grade it is not eligible**; at lower bands, whether an attempt is permitted and how it is recorded.

## Diversity Requirements
The value from `models/review-diversity-and-criticality.md` §2 and the **named prior selection** it is evaluated against. Where the prior decision is unrecorded, the constraint is unsatisfiable and routing blocks.

## Fallback Policy

Which fallback kinds are permitted; which dimensions form **explicitly permitted degradation bands** (preferences only — never an eligibility constraint); at what materiality a degradation requires human acknowledgement; and the conditions under which this policy **blocks rather than degrades**.

**Where an eligibility constraint fails, no fallback policy applies** — that is case B of `models/routing-precedence-and-fallback.md` §5, needing a Phase 7 act that produces an adjusted context *before* re-evaluation, or it is case C and blocks.

## Deterministic Tie-Break Rule
The declared, ordered rule. **Deterministic and recorded — never random, never "whichever answered first".** Two identical tasks under this version select the same candidate.

## Model Pinning
**None** by default. Where a pin exists: the justification, the named owner class, and the **expiry or review-by**. An unexpiring pin is defective.

## Act Requirements

Which of `HUMAN_SELECTION_REQUIRED`, `HUMAN_ACKNOWLEDGEMENT_REQUIRED`, `GOVERNANCE_REVIEW_REQUIRED` apply, and under what conditions.

**None of these filters a candidate or changes eligibility in either direction.** They withhold **finalisation**: every candidate may pass them and routing still not complete. A policy declaring one without a process behind it produces a permanent non-completion — a policy defect, and a visible one.

## Out-of-Scope Authority
What this policy explicitly does **not** do: approve work, accept risk, satisfy a review, promote knowledge, grant authority, or decide what work happens. A blank section is a defect.

## Versioning
Version history, confirming that no version change silently altered an eligibility constraint, an accepted evidence class, a diversity requirement or the tie-break.

## Non-Runtime Statement
This policy is declarative architecture. It specifies no matcher, engine, scoring function, SDK, API, credential or runtime.
