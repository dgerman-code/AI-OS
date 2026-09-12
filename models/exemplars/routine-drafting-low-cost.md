# Exemplar 1 — Routine drafting, low-cost eligible model

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that the cheapest eligible model is chosen by a *preference operating inside an already-filtered set*, not by cost winning an argument.

## Task context
Internal drafting of a routine progress note. Criticality **Routine / Standard**. Material sensitivity `INTERNAL`.

## Requirements
`capability.summarisation` `BASELINE`; `capability.instruction_fidelity` `BASELINE`. Text in, text out. No tool use, no structured output, no long context.

## Candidate assessment
| Candidate | Eligible? | Why |
|---|---|---|
| `model.compact_general_a` @ `deployment.tenant_internal_a` | **Yes** | Meets both requirements; `COST_LOW`; `LATENCY_INTERACTIVE` |
| `model.frontier_reasoning_b` @ `deployment.tenant_internal_a` | **Yes** | Meets both comfortably; `COST_PREMIUM` |
| `model.vision_specialist_c` @ `deployment.public_hosted_c` | **No** | Deployment maximum sensitivity is `PUBLIC`; task material is `INTERNAL`. Excluded at **stage 2**, before capability was considered |

## Selection
`model.compact_general_a` @ `deployment.tenant_internal_a`, on `PREFER_LOWER_COST_CLASS` at stage 7.

## What this actually shows
The cheap model won **a ranking among two eligible candidates**, having first survived legality, sensitivity, capability, independence and lifecycle. It never competed with the third candidate at all: that one was removed at stage 2 and was not in the set cost could reach.

This is the ordinary case, and it is worth stating because it is the one people imagine the governance is obstructing. It is not: **sufficient capability at lower cost is the right answer, and the architecture reaches it by filtering first rather than by weighing cost against privacy.**

**Not shown:** that the note is correct. The output is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`, exactly as it would be from the premium candidate.
