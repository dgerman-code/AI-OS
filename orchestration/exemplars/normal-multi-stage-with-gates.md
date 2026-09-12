# Exemplar 1 — The ordinary run: model-assisted work, a review, a human decision

Status: PROPOSED — Phase 11 exemplar execution run
Inherits: `standard.orchestration.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders. No real project, person, model or decision is referenced.

**Proves:** that the ordinary case reaches the end **through** its gates rather than around them, and that the orchestrator's contribution is coordination and nothing else.

## The run

| | |
|---|---|
| Run | `run.2026.market_brief.0041` |
| Workflow | `workflow.market_brief` @ v6 — **immutable for this run** |
| Policy | `orch_policy.standard_analysis` @ v3 |
| Scope | `project.delta` — exactly one |
| Criticality | Enhanced Review Candidate |
| Sensitivity | {`INTERNAL`, `CONFIDENTIAL`} |

## What happened, stage by stage

| Stage | Dispatch kind | Outcome | Run state after |
|---|---|---|---|
| 1 — Gather inputs | **Scheduled** machine activity | Completed | `RUNNING` / posture `GOVERNANCE_CLEAR` |
| 2 — Draft the brief | **Requested** routing → `rd.2026.brief.0902`; model produced the draft | Draft exists as `AI_SUGGESTION`, `ORIGIN: AI_GENERATED` | `RUNNING` / `GOVERNANCE_CLEAR` |
| 3 — Review | **Requested** review against `review.analysis` | `SATISFIED_WITH_OPEN_ITEMS` — two minor items | `RUNNING` / **`OPEN_ITEMS_CARRIED`** |
| 4 — Decision gate | **Requested** exercise of `decision.external_publication` | Decision Record produced by an eligible human | `RUNNING` / `OPEN_ITEMS_CARRIED` |
| 5 — Publish | **Scheduled**, class `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT` | Completed | **`COMPLETED_WITH_OPEN_ITEMS`** |

## What the orchestrator did

Detected that stages 3 and 4 applied, created the Review Request and the Decision Request, waited, and recorded both outcomes **by reference**. It did not review, decide, or interpret either answer.

## What the orchestrator did not do

- **It did not treat stage 2's completion as a review.** The draft was `AI_SUGGESTION` when stage 2 ended and remained so until a reviewer said otherwise.
- **It did not complete the run as `COMPLETED`.** Two open items were carried, so the posture was `OPEN_ITEMS_CARRIED` and the only terminal outcome available was `COMPLETED_WITH_OPEN_ITEMS`. Each item names the upstream rule permitting it to be carried; an item without one would have blocked.
- **It did not let stage 3's reviewer be stage 2's producer.** The Assignment Envelope for stage 2 recorded the review restriction (field 8), so the exclusion was mechanical rather than a matter of someone noticing.

## What this shows

The ordinary case is worth writing down because it is the one people imagine governance is obstructing. It is not: **the work got done, through five stages, with a model doing the drafting** — and every governed conclusion in it was reached by the party that owns that conclusion.

The one thing the run cannot tell you is whether the brief is any good. That is stage 3's answer, recorded separately, and it says `SATISFIED_WITH_OPEN_ITEMS` rather than "yes".
