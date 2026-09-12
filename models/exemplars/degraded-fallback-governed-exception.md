# Exemplar 9 — Degraded fallback requiring a governed exception

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** the boundary between an operator's choice, a human acknowledgement, and a **governed Phase 7 exception** — and that degradation is never silent.

## Task context
Code review of a security-relevant change, feeding a release gate. Criticality **Enhanced Decision-Grade**. Review Profile declares **`DIFFERENT_MODEL_FAMILY_REQUIRED`** against the producing decision.

## What happened
The only candidate satisfying both family diversity and `capability.code_review` `STRONG` on current internal evaluation became **`SUSPENDED`** after an incident. The remaining diverse-family candidate claims `capability.code_review` at **`BASELINE`** — eligible on every hard constraint, **materially weaker on the dimension the task turns on**.

## The three possible responses
| Response | Verdict |
|---|---|
| Use the `BASELINE` candidate silently | **Prohibited.** Silent degradation. The record would show an ordinary selection and the review would appear to have been performed at the required strength |
| Use it, declared as `DEGRADED_FALLBACK` with operator acknowledgement | **Insufficient here.** The degradation is material, at Decision-Grade, on a review feeding a release gate |
| Use it under a **governed exception** with an upstream Phase 7 Decision Right | **The only permitted route** |
| Drop family diversity to reach the stronger same-family model | **Prohibited as a routing act.** Waiving mandatory review independence requires a valid Decision Right — a routing choice is not one |
| `BLOCKED_FOR_ROUTING` and wait for the suspension to resolve | **Always available, and often correct** |

## Outcome recorded
`DEGRADED_FALLBACK`, naming: the dimension (`capability.code_review`, `STRONG` required, `BASELINE` provided); what that risks (defect classes the weaker candidate is less likely to find); the Phase 7 exception reference; and the expiry — **the exception covers this review, not a standing arrangement**.

## What this actually shows
Three different acts are kept apart here, and they are routinely treated as one:

1. **Operator choice** — selecting among eligible candidates, or asking for something stronger. Ordinary, recorded.
2. **Acknowledgement** — accepting a declared, immaterial-to-material degradation. Human, recorded, not an authority act.
3. **Governed exception** — proceeding where a material Decision-Grade requirement is unmet. **A Phase 7 Decision Right, held by a human, exercised separately** — and under Phase 7's own separation rules, not by whoever is running the review.

**The fourth row matters most.** Dropping the diversity requirement would have produced a stronger model and a compliant-looking record — and would have waived an independence control by routing choice, which is the substitution this boundary exists to prevent.

**The exception does not make the review stronger.** It records that the organisation proceeded with a known weaker control, named what that costs, and put a human's name against it. The review's findings are what they are, and Phase 6 still governs whether it is `SATISFIED`.
