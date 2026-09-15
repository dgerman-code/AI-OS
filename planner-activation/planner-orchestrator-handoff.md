# Planner → Orchestrator Handoff

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

## 1. One command, one direction

The handoff builds exactly one thing: the envelope of the approved Phase 14 command
**`CreateWorkflowRun`**. It does not call it.

```text
ExecutionBasis (EXECUTABLE) → TriggerEnvelope → CreateWorkflowRun → intake checks 1–7 → run
```

**Rule HB-1 — the builder hands over a trigger, not a run.** `creates_run` is a declared field
and is `false`. Nothing in `handoff.py` creates a run, activates a stage, assigns a Work Item,
routes, invokes a model, opens a review, requests a decision or writes a governed record. Each of
those is its own approved Phase 14 command, performed by the Orchestrator.

## 2. Mapping to the approved intake checks

The envelope makes each of the seven answerable. **It performs none of them**, and the
Orchestrator validates every one independently and may refuse.

| Intake check | What the envelope supplies |
|---|---|
| 1. The definition resolves at a named version | `workflow_ref` for MATCH; `work_plan_ref` **plus the Execution Basis reference** for COMPOSE — see `po-4-and-po-12-closure.md` |
| 2. The Orchestrator Policy resolves at a named version | `orchestrator_policy_ref` |
| 3. Exactly one governed scope, and the originator may act in it | `scope_ref`, `scope_ancestry`, `originator` |
| 4. Sensitivity, handling and residency present or explicitly assessed | `sensitivity`, `residency` — `UNASSESSED` is restricted, never permissive |
| 5. Criticality band resolves | `criticality_band` |
| 6. Not a duplicate under the same idempotency key | `idempotency_key`, derived from scope + request + material digest |
| 7. Every declared prerequisite resolves, or is `FUTURE_GOVERNANCE_REFERENCE` | `prerequisite_refs`, each as `(reference, state)` |

## 3. What crosses, and what does not

| Crosses | Does not cross |
|---|---|
| The envelope, once, on an `EXECUTABLE` basis | Any pre-formed governed record |
| `PlannedWorkItemSpec` records — descriptions, not Work Items | A Work Item, a Task, a run reference or an assignment |
| Requirements: reviews, Rights, evidence | A satisfied review, an exercised Right, supplied evidence |
| Provenance: request, intent, work plan, basis | The planner's reasoning traces or confidence values |

**Rule HB-2 — `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`.** A Task belongs to an approved
Workflow definition and is unchanged by any run. A Work Item is the run's instance of it, created
by Phase 11 inside a run. A spec is neither: it carries no run reference, no runtime state, no
assignment, no execution status and no model, and its identifier lives in
`planned_work_item_spec.`. The constructor refuses any other space.

**Rule HB-3 — the trigger carries no governed record a caller supplied.** `decision_record`,
`review_instance`, `approval_state`, `gate_outcome`, `routing_decision`, `model_result`,
`intervention`, `knowledge_item` — each is created only by its own approved command, and the
builder raises on an envelope carrying one.

**Rule HB-4 — a stale basis produces nothing.** The builder recomputes the planning digest and
refuses a mismatch, so a basis cannot be used against planning inputs it was not issued against.

**Rule HB-4a — the builder verifies before it builds, and a digest is only one of the checks.**
`verify_basis` requires that the basis was ISSUED by the store presented, that its version and
its payload seal match what the store holds, that its status is `EXECUTABLE`, that request
identity, intent identity, scope, scope ancestry, execution mode, criticality, policy binding,
Workflow binding and Work Plan binding all agree with the plan, that the implementation-spec
version is the one this bridge is written against, and that `is_approval` and `is_authority` are
both still `false`. Each is checked separately so a refusal names the field. The rules are in
`execution-basis-contract.md` §4a; a digest comparison alone can say nothing about whether the
basis was ever issued, or whether it belongs to this request.

## 4. What the planner never sees again

**Rule HB-5 — there is no return path.** The builder receives no run state, no stage outcome, no
review result and no decision. A block during a run is Phase 11's escalation path, and a
genuinely new plan begins with a new request and a new basis version.

**Rule HB-6 — the Orchestrator may refuse the envelope, and that is the design working.** A
recorded refusal at intake is the correct outcome for a trigger that looked valid to its own
preflight and is not. Phase 16 treats an intake refusal as an answer, never as an error to route
around.

## 5. Non-Runtime Statement

This document is declarative architecture. It specifies no transport, queue, API, serialisation
or storage mechanism, and binds no provider or runtime technology.
