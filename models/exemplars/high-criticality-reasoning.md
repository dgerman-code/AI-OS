# Exemplar 2 — High-criticality analysis requiring stronger reasoning evidence

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that criticality raises **evidence, freshness and reliability** requirements — and that "stronger model" is not the same as "larger model".

## Task context
Covenant analysis feeding a financing recommendation. Criticality **Enhanced Decision-Grade**. Material sensitivity `CONFIDENTIAL`.

## Requirements
`capability.advanced_reasoning` `STRONG`; `capability.instruction_fidelity` `STRONG`; `capability.citation_evidence_handling` `STRONG`; `MINIMUM_RELIABILITY_CLASS` raised. Accepted evidence at this band: `INTERNAL_EVALUATION` only, verdict `CURRENT_FOR_USE`.

## Candidate assessment
| Candidate | Eligible? | Why |
|---|---|---|
| `model.frontier_reasoning_b` v4 | **No** | Claims `SPECIALISED` advanced reasoning on `INTERNAL_EVALUATION` — but the evidence is `PAST_REFRESH_INTERVAL`, and at this band stale evidence is **`STALE_AND_BLOCKING`** |
| `model.frontier_reasoning_b` v5 | **No** | Newer version; reasoning evidence is `PROVIDER_DECLARED` only. **Not an accepted class at this band** |
| `model.midsize_analyst_d` | **Yes** | `STRONG` on all three, on current internal evaluation. Smaller and less celebrated than either candidate above |
| `model.compact_general_a` | **No** | `BASELINE` advanced reasoning — below the minimum |

## Selection
`model.midsize_analyst_d`, the **smallest eligible candidate**.

## What this actually shows
The two largest candidates were excluded **on evidence, not on capability**: one because its evaluation had gone stale, one because nobody but its provider had assessed it. Neither exclusion is a claim that the model is weak.

**"Largest" is not a governance property.** What Decision-Grade requires is that someone competent checked, recently, on work like this — and a model nobody has evaluated is not made eligible by being impressive.

**Freshness is use-specific:** v4's stale evidence would have been `STALE_BUT_USABLE` for exemplar 1's drafting task, at the same moment, unchanged.
