# Execution State Model and Transitions

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Four orthogonal axes, not one enum

A single status field would force unrelated facts into one value and then lose one of them. "Waiting for a review" and "carrying an unresolved finding" are not alternatives — a run can be both, and a design that makes them alternatives eventually reports the more convenient one.

| Axis | Answers | Cardinality |
|---|---|---|
| **A — Run phase** | Where the execution is | Exactly one at a time, from 10 |
| **B — Terminal outcome** | How it ended | Exactly one once terminal; **absent** before |
| **C — Wait reason** | What it is waiting for | Exactly one **while and only while** phase is `WAITING` |
| **D — Governance posture** | What the governance state of the work is | Exactly one at all times, from 4 |

**Axis D is the one that stops completion from meaning approval**, and it is why there are four axes rather than three.

## 2. Axis A — Run phase (10, mutually exclusive, non-terminal)

| State | Meaning |
|---|---|
| `CREATED` | The trigger was accepted as a record; nothing is scheduled |
| `VALIDATING` | Intake validation is running (`architecture/orchestrator-architecture.md` §5) |
| `READY` | Validated; prerequisites met; nothing dispatched yet |
| `RUNNING` | At least one activity instance is dispatched |
| `WAITING` | Progress is suspended on something external to the orchestrator — see Axis C |
| `PAUSED` | Progress is suspended **by a human act**, recorded as an intervention |
| `RETRY_PENDING` | A step failed in a class the policy permits retrying, and a retry is scheduled |
| `REWORK_REQUIRED` | A governed outcome sent work back; a bounded rework loop is open |
| `BLOCKED` | Continuation is **not permitted** — a constraint is unmet and no path forward exists without a governed act |
| `ESCALATED` | A named human or body has been asked to resolve something the run cannot |

## 3. Axis B — Terminal outcome (6, exactly one once terminal)

| Outcome | Meaning | Requires |
|---|---|---|
| `COMPLETED` | Every stage finished and every gate was satisfied | Posture `GOVERNANCE_CLEAR` |
| `COMPLETED_WITH_OPEN_ITEMS` | Finished with items carried forward | Posture `OPEN_ITEMS_CARRIED` **and** an upstream rule that permits carrying each item |
| `CANCELLED` | Stopped before completion by a human act; the work is not wanted | An intervention record |
| `TERMINATED` | Stopped by the system because continuing would breach a constraint | A named constraint |
| `FAILED` | Stopped by an error that no permitted retry or recovery resolved | A recorded cause |
| `SUPERSEDED` | Replaced by another run for the same subject | The superseding `run.<id>` |

> **A terminal outcome is never inferred.** There is no state a run drifts into by nothing happening; a run with no activity is `WAITING`, `PAUSED` or `BLOCKED`, and each of those names what it is waiting on.

## 4. Axis C — Wait reason (5, present only while `WAITING`)

`WAITING_FOR_DEPENDENCY` · `WAITING_FOR_REVIEW` · `WAITING_FOR_DECISION` · `WAITING_FOR_HUMAN` · `WAITING_FOR_EXTERNAL_EVENT`

Each carries the reference it waits on: the dependency, the Review Request, the Decision Request, the intervention requested, or the external condition. **A wait with no named subject is a defect**, because it is indistinguishable from a stall.

## 5. Axis D — Governance posture (4, always present)

| Posture | Meaning | Permits terminal |
|---|---|---|
| `GOVERNANCE_CLEAR` | Every applicable gate satisfied; no open item; no unresolved conflict | `COMPLETED` |
| `OPEN_ITEMS_CARRIED` | Items carried forward, **each under a named upstream rule permitting it** | `COMPLETED_WITH_OPEN_ITEMS` only |
| `GATE_UNSATISFIED` | A required review, decision or human gate is unsatisfied | **No completion.** `BLOCKED`, `WAITING` or `ESCALATED` |
| `AUTHORITY_ABSENT` | An act requires a Decision Right that no approved Phase 7 Right covers | **No completion.** `BLOCKED` **and** `ESCALATED` |

`AUTHORITY_ABSENT` is a separate posture from `GATE_UNSATISFIED` deliberately. An unsatisfied gate is waiting for someone; **an absent authority is waiting for governance that does not yet exist**, and those need different escalations — the first to a reviewer or decider, the second to Phase 7's carding governance.

## 6. Transitions

Permitted phase transitions. Anything absent is **not a transition**, which is stronger than being a forbidden one.

| From | May go to |
|---|---|
| `CREATED` | `VALIDATING`, `CANCELLED` |
| `VALIDATING` | `READY`, `BLOCKED`, `TERMINATED` |
| `READY` | `RUNNING`, `WAITING`, `PAUSED`, `CANCELLED`, `BLOCKED` |
| `RUNNING` | `WAITING`, `PAUSED`, `RETRY_PENDING`, `REWORK_REQUIRED`, `BLOCKED`, `ESCALATED`, `COMPLETED`, `COMPLETED_WITH_OPEN_ITEMS`, `FAILED`, `CANCELLED`, `TERMINATED`, `SUPERSEDED` |
| `WAITING` | `RUNNING`, `REWORK_REQUIRED`, `BLOCKED`, `ESCALATED`, `PAUSED`, `CANCELLED`, `TERMINATED`, `SUPERSEDED` |
| `PAUSED` | `RUNNING`, `READY`, `CANCELLED`, `TERMINATED`, `SUPERSEDED` |
| `RETRY_PENDING` | `RUNNING`, `BLOCKED`, `ESCALATED`, `FAILED`, `CANCELLED` |
| `REWORK_REQUIRED` | `RUNNING`, `BLOCKED`, `ESCALATED`, `CANCELLED`, `TERMINATED` |
| `BLOCKED` | `RUNNING`, `WAITING`, `ESCALATED`, `CANCELLED`, `TERMINATED` — **only after the blocking constraint is satisfied by a governed act** |
| `ESCALATED` | `RUNNING`, `WAITING`, `BLOCKED`, `REWORK_REQUIRED`, `CANCELLED`, `TERMINATED` |

**Terminal outcomes have no outgoing transitions.** A terminal run is re-examined by creating a new run that names it, never by reopening it.

### 6.1 Two transitions that do not exist

- **`WAITING` → `COMPLETED` on timeout.** There is no such edge. A gate that expires produces an expiry, which moves the run to `ESCALATED` with the posture unchanged.
- **`BLOCKED` → `RUNNING` by retry.** Retry re-executes a **step**; it does not satisfy a **constraint**. A blocked run resumes only when the governed act that was missing has occurred, and the act is recorded.

## 7. Completion is not approval

Stated as a rule rather than left to the diagram: **a run reaching `COMPLETED` means every stage ran and every gate the workflow declared was satisfied.** It does not mean the output is correct, canonical or endorsed. The produced content is `AI_SUGGESTION` where a model produced it and an artifact where a human did; what makes either authoritative is Phase 6, 7 or 8 acting on it, recorded separately.

A run may therefore be `COMPLETED` over work that is later found wrong — and that is not a defect in the run, which recorded accurately what happened.

## 8. Stage and activity states

Stage instances and activity instances carry the **same four axes**, scoped to themselves. A stage instance is `COMPLETED` when its activities are; the run is not. **The run's posture is the strictest posture of its open parts**, so a single `GATE_UNSATISFIED` stage prevents run completion without anyone having to notice.
