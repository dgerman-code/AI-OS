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
must be `PASSED`. There is no reduced handoff, no "hand over the parts that validated", no
provisional run, and no envelope carrying some stages while others are still unsatisfied. A plan is
handed over whole or not at all, and `failure-and-escalation-model.md` F-9 and
`governance-preflight.md` G-11 are written to the same rule: an unsatisfied requirement is a
**plan-level** outcome, never a per-stage one, because Phase 15 has no stages to run.

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
| 11 | `prerequisite_refs` | Every declared artifact, evidence and decision reference, each in exactly one of the three states of §2a | 7 |
| 12 | `planning_provenance` | `request.<id>`, `intent.<id>`, `work_plan.<id>`, `plan_validation.<id>` | — |
| 13 | `act_posture` | One of the five postures of `governance-preflight.md` GP-6 | — |
| 14 | `open_items` | Assumptions, `UNKNOWN`s and findings carried forward, each with the rule permitting it | — |

### 2a. The three prerequisite states, and why `UNKNOWN` is not one of the passable ones

The approved intake check 7 reads: *"Every declared prerequisite artifact, evidence or decision
reference resolves, or is declared `FUTURE_GOVERNANCE_REFERENCE` and therefore non-executable —
BLOCK on a dangling reference."* Two states pass it; a third does not.

| State | Means | At intake |
|---|---|---|
| **`RESOLVED`** | The reference resolves, at an ID and a version | Eligible to proceed, subject to the rest of the intake contract |
| **`FUTURE_GOVERNANCE_REFERENCE`** | A declared future reference, named as such | Permitted, and the dependent act is **non-executable** until it is satisfied |
| **`UNKNOWN`** | The planner does not hold the reference and cannot classify it as a declared future one | **Dangling. BLOCK.** No executable handoff |

**Rule HO-15 — a plain `UNKNOWN` prerequisite blocks, and is never rewritten as a declared future
reference.** `UNKNOWN` is a determinate finding about the planner's knowledge (RI-3);
`FUTURE_GOVERNANCE_REFERENCE` is a governed declaration about the work. Relabelling the first as the
second would turn "I do not know" into "this is deliberately deferred", which is the one move that
makes a dangling reference look handled. The two are never equivalent, in this document or any
other.

**Rule HO-3 — fields 2 and 3 are mutually exclusive.** A `WORK_PLAN` envelope carries no
`workflow_ref`, and a `WORKFLOW_SELECTION` envelope carries no `work_plan_ref`. An envelope
carrying both has collapsed the two identities, which is the thing PL-3 forbids.

**Rule HO-4 — the envelope carries no Model Profile, provider or routing decision.** Model
selection is Phase 9's, performed by the Router after the Orchestrator creates a routing request.
An envelope naming a model would be choosing a runtime from outside the router boundary.

**Rule HO-5 — `planning_provenance` is operational, not evidence.** It lets a reviewer trace what
the system understood. It is not evidence for anything the run concludes, and a run may not cite it
as a basis.

## 3. Planned Work Item Specifications

`work_item.<id>` is a **runtime** identity owned by the run (`orchestration/execution-run-model.md`
§3, row 6), and a **Task / Activity** is something else again: what an approved Workflow definition
says is to be done, defined once and unchanged by any run (§4 of that document). Phase 15 produces
neither. It produces a planning record, in its own identifier space:

> `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`

**Rule HO-6 — the planner produces `PlannedWorkItemSpec` records and never instantiates a runtime
Work Item.** A spec is derived only from a **validated** plan stage bound to approved definitions —
not from an intent, not from a draft stage, not from a stage whose requirements are unmet, and never
before validation has run (`intent-work-planning-architecture.md` PL-8, step 12). It is
`planned_work_item_spec.<id>`, never `work_item.<id>` and never a Task; it is not a Work Item in an
earlier state, and there is no transition between them.

Each `PlannedWorkItemSpec` carries, at minimum:

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

**Rule HO-7 — a spec is a specification of work, not an assignment.** It states which Role envelope
is required. Binding a Role instance to it is an assignment, and assignment is Phase 11's.

**Rule HO-8 — a spec names no model.** Field 4 is a Role and Skill envelope. What executes it is
decided later, elsewhere.

**Rule HO-13 — a spec carries no runtime anything.** Specifically, and exhaustively, a
`PlannedWorkItemSpec` has:

| No | Because |
|---|---|
| Runtime state, or any state from the Phase 11 state machine | State belongs to a run, and no run exists yet |
| Run ownership, or a `run.<id>` reference | It is written before any run is created |
| Assignment or execution status | Assignment is Phase 11's (HO-7) |
| A model, provider or routing decision | Phase 9's (HO-8) |
| A routing action, dispatch, claim or attempt | Those are acts, and the planner performs none |
| Orchestration semantics — activation, waiting, retry, rework, completion | PL-1 |

### 3a. What the approved Orchestrator does with a spec today: nothing

**Rule HO-14 — no approved contract consumes a `PlannedWorkItemSpec`, and Phase 15 may not claim
one does.** `PlannedWorkItemSpec` is a **proposed** Phase 15 planning object. No approved Phase 11
artifact defines it as an intake object, and this package therefore states none of the following as
current behaviour:

| Not claimed as current behaviour | Why not |
|---|---|
| That the approved Orchestrator reads a `PlannedWorkItemSpec` | No approved intake contract names it |
| That it re-validates one at intake | Intake validates the seven approved checks against the approved envelope, and a spec is not one of their inputs |
| That it instantiates a Work Item from one | Work Item creation is Phase 11's, from what its own approved contract accepts |
| That runtime identity is derived from one | Runtime identity comes into being inside a run, from approved inputs |

What **is** true today, and all that is:

- Phase 15 may **produce** a `PlannedWorkItemSpec` as non-runtime planning output.
- It may be carried in a **proposed** handoff envelope only where an approved execution-basis
  contract permits it — and none currently does.
- The translation and consumption semantics — what a downstream consumer would do with a spec, and
  under what conditions — require **explicit Phase 11 change control**, or another separately
  approved execution-basis mechanism.
- Until that exists, **COMPOSE remains non-executable under PO-4**, and producing specs changes
  nothing about that.
- **MATCH** continues to hand off through the approved Workflow-based intake path only, and its
  compatibility rests on `workflow.<id>` @ version — not on any spec.

**Rule HO-16 — a spec is not a bridge over PO-4.** Introducing `PlannedWorkItemSpec` fixed an
identity error; it did not create an execution route. No Phase 15 statement may say that producing
specs lets a Work Plan reach a run, because no such route exists — saying so would resolve PO-4 by
assertion, which `open-items.md` §2a forbids.

## 4. What crosses, and what does not

| Crosses | Does not cross |
|---|---|
| The envelope of §2 | The planner's reasoning traces |
| `PlannedWorkItemSpec` records of §3, **only where an approved execution-basis contract permits** (§3a) | Confidence values as decision inputs |
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
