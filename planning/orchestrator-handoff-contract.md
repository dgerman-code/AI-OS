# Orchestrator Handoff Contract

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. The boundary

```text
Phase 15 planner  →  trigger envelope  →  Phase 11 Orchestrator intake  →  run
```

One direction, one object, one moment. After the envelope is produced, Phase 15 has no further part
in the run.

**Rule HO-1 — the planner hands over a trigger, not a run.** It does not create a run, activate a
stage, make an assignment, issue a routing request, open a review, request a decision, wait, retry,
rework, block, escalate or complete. Every one of those is Phase 11's, and the approved Phase 11
architecture is unchanged by this phase.

**Rule HO-2 — the handoff happens only on a passing preflight.** `PlanValidationResult.outcome`
must be `PASSED`. There is no reduced handoff, no "hand over the parts that validated", and no
provisional run.

## 2. The trigger envelope

Built to make the Orchestrator's seven intake checks answerable
(`architecture/orchestrator-architecture.md` §5). It does not perform them.

| # | Field | Content | Serves intake check |
|---:|---|---|---|
| 1 | `execution_basis` | `WORKFLOW_SELECTION` or `WORK_PLAN` | 1 |
| 2 | `workflow_ref` | `workflow.<id>` @ version — present **only** for `WORKFLOW_SELECTION` | 1 |
| 3 | `work_plan_ref` | `work_plan.<id>` @ version — present **only** for `WORK_PLAN`, and never rendered as a workflow reference | 1 |
| 4 | `orchestrator_policy_ref` | The policy the plan assumes, by ID and version | 2 |
| 5 | `scope_ref` | Exactly one governed scope, with its declared ancestry | 3 |
| 6 | `originator` | The requesting human identity | 3 |
| 7 | `sensitivity` | Labels and handling controls, or explicit `UNASSESSED` | 4 |
| 8 | `residency` | Constraints, or explicit `UNASSESSED` | 4 |
| 9 | `criticality_band` | The resolved band | 5 |
| 10 | `idempotency_key` | Derived from the `Request` identity | 6 |
| 11 | `prerequisite_refs` | Every declared artifact, evidence and decision reference, each resolved or explicitly `UNKNOWN` | 7 |
| 12 | `planning_provenance` | `request.<id>`, `intent.<id>`, `work_plan.<id>`, `plan_validation.<id>` | — |
| 13 | `act_posture` | One of the five postures of `governance-preflight.md` GP-6 | — |
| 14 | `open_items` | Assumptions, `UNKNOWN`s and findings carried forward, each with the rule permitting it | — |

**Rule HO-3 — fields 2 and 3 are mutually exclusive.** A `WORK_PLAN` envelope carries no
`workflow_ref`, and a `WORKFLOW_SELECTION` envelope carries no `work_plan_ref`. An envelope
carrying both has collapsed the two identities, which is the thing PL-3 forbids.

**Rule HO-4 — the envelope carries no Model Profile, provider or routing decision.** Model
selection is Phase 9's, performed by the Router after the Orchestrator creates a routing request.
An envelope naming a model would be choosing a runtime from outside the router boundary.

**Rule HO-5 — `planning_provenance` is operational, not evidence.** It lets a reviewer trace what
the system understood. It is not evidence for anything the run concludes, and a run may not cite it
as a basis.

## 3. Work Items

**Rule HO-6 — the planner may instantiate Work Items only from validated plan stages bound to
approved definitions.** Not from an intent, not from a draft stage, not from a stage whose
requirements are unmet.

Each Work Item carries, at minimum:

| # | Field |
|---:|---|
| 1 | Work intent reference |
| 2 | Scope reference |
| 3 | Stage and dependency references |
| 4 | Required Role / Skill envelope — as approved IDs, never descriptions |
| 5 | Expected artifact / output |
| 6 | Required input knowledge states |
| 7 | Review and gate requirements, as references |
| 8 | Sensitivity, residency and handling constraints |
| 9 | Criticality band |
| 10 | Completion criteria |
| 11 | Failure and escalation disposition |

**Rule HO-7 — a Work Item is a specification of work, not an assignment.** It states which Role
envelope is required. Binding a Role instance to it is an assignment, and assignment is Phase 11's.

**Rule HO-8 — a Work Item names no model.** Field 4 is a Role and Skill envelope. What executes it
is decided later, elsewhere.

## 4. What crosses, and what does not

| Crosses | Does not cross |
|---|---|
| The envelope of §2 | The planner's reasoning traces |
| Work Items of §3 | Confidence values as decision inputs |
| Resolved references, as ID and version | Unresolved candidates the planner rejected |
| Open items with the rule permitting each | Any assertion the planner could not support |

**Rule HO-9 — confidence does not cross as an input.** Confidence values may be **recorded** in
planning provenance for inspection. They may not appear in the envelope as a field the Orchestrator
acts on, because that would make a Phase 15 estimate an input to a Phase 11 decision.

**Rule HO-10 — the Orchestrator may refuse the envelope, and that is the design working.** A
recorded refusal at intake is the correct outcome for a plan that looked valid to its own planner
and is not. Phase 15 does not treat an intake refusal as an error to route around.

## 5. What the planner never sees again

**Rule HO-11 — there is no return path.** The planner receives no run state, no stage outcome, no
review result and no decision. It cannot be woken by the run, cannot adjust a plan mid-run, and
cannot re-plan in response to a block. A block during a run is handled by Phase 11's escalation
path, and a genuinely new plan begins with a new `Request`.

**Rule HO-12 — replanning is a new request, not a continuation.** This is what keeps the planner
from becoming a second Orchestrator by increments.

## 6. Non-Runtime Statement

This document is declarative architecture. It specifies no transport, queue, API, schema,
serialisation or storage mechanism, and binds no provider or runtime technology.
