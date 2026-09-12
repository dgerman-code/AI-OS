# Failure, Escalation and Recovery

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Seven distinctions that are routinely collapsed

| Pair | The difference | Why collapsing it is harmful |
|---|---|---|
| **PAUSE vs BLOCK** | `PAUSED` is a human suspending a run that *could* continue. `BLOCKED` is a constraint meaning it *may not* | A block recorded as a pause looks like a scheduling choice, and someone will resume it |
| **CANCEL vs TERMINATE** | `CANCELLED` is a human deciding the work is not wanted. `TERMINATED` is the system stopping work that would breach a constraint | A termination recorded as a cancellation erases the constraint that caused it |
| **RETRY vs REWORK** | Retry re-executes the **same** step after a failure. Rework re-does the **work** after a governed outcome rejected it | Rework recorded as retry hides that a review said no |
| **ESCALATE vs HUMAN REVIEW** | Escalation asks a human to **resolve a blockage**. A human review is a **governed review act** under Phase 6 | An escalation treated as a review would let an escalation satisfy a review gate |
| **FAIL vs BLOCKED** | `FAILED` is an error nothing resolved. `BLOCKED` is governance saying not yet | A block recorded as a failure invites a retry, and retry never resolves a constraint |
| **SUPERSEDE vs CANCEL** | `SUPERSEDED` means another run replaced this one for the same subject. `CANCELLED` means nobody is doing it | A supersession recorded as a cancellation loses the link to what actually carried the work |
| **Compensation vs rollback** | Rollback restores prior state inside one transactional boundary. Compensation is a **new, recorded, separately-authorised act** counteracting an effect that cannot be undone | Calling compensation rollback implies the effect never happened |

## 2. Partial failure across systems

Phase 10 established that an object upload and a database transaction cannot be one atomic act. Phase 11 inherits that and extends it: **an execution spanning the orchestrator, the database, object storage and any external system has no distributed transaction, and none is claimed.**

What replaces it, for every multi-system step:

1. a **declared commit order**, with the governed metadata record committed **last**;
2. a **reconciliation owner** — the sweep or the run that will detect an interruption;
3. a **compensating outcome** for the case where the effect is external and cannot be undone.

| Interruption | State | Outcome |
|---|---|---|
| Effect not started | Nothing happened | `RETRY` per class |
| Effect completed, governed metadata not committed | **Orphaned effect**, invisible to governance | `RECONCILE`: internal orphans are quarantined and expired; **an external one is `ESCALATED`**, because it cannot be quarantined |
| Governed metadata committed, effect missing | Detectable gap | `BLOCK` and `ESCALATE` — the record is authoritative for what should exist |
| Effect outcome unknown | Undeterminable | **`BLOCKED` and `ESCALATED`.** Never assumed in either direction |

## 3. Compensation

A compensating act is a **first-class governed act**, not an undo:

- it is **recorded** as its own execution event, naming the effect it compensates;
- it carries its **own authority requirement** — where the original act needed a Decision Right, the compensation needs one too, and absence blocks;
- it **does not delete** the original record, which remains true;
- it may itself have external effects, which are themselves non-replayable.

"We rolled it back" is not available for anything that left the system.

## 4. Twelve stop conditions

The orchestrator stops and waits for a human or a governed authority on any of these. There is no policy setting that converts one into a continuation.

| # | Condition | Outcome |
|---:|---|---|
| 1 | No applicable Decision Right for a required act | `BLOCKED` + `ESCALATED`, posture `AUTHORITY_ABSENT` |
| 2 | Material unresolved conflict in governed state | `BLOCKED` + `ESCALATED` |
| 3 | Review `NOT_SATISFIED` | `REWORK_REQUIRED` or `BLOCKED` |
| 4 | Stale or expired blocking evidence | `BLOCKED` |
| 5 | Scope mismatch between the work and the run's bound scope | `BLOCKED` — **never a silent transfer** |
| 6 | Sensitivity or residency constraint would be violated | `BLOCKED` + `TERMINATED` if continuation would breach it |
| 7 | A destructive action without a named authority | `BLOCKED` + `ESCALATED` |
| 8 | Ambiguous identity or version — a reference that resolves to more than one thing, or to none | `BLOCKED` |
| 9 | Failed integrity check — hash mismatch, missing object, quarantined record | `BLOCKED` + `ESCALATED` |
| 10 | Unknown model eligibility — the Router could not determine it | `BLOCKED`. **Unknown is not eligible** |
| 11 | Cancellation or termination race with an in-flight governed act | `RECONCILE` + `ESCALATED` |
| 12 | External side-effect uncertainty | `BLOCKED` + `ESCALATED` |

## 5. Recovery, replay and resume

Recovery restores a run to a **checkpoint**, and a checkpoint records the state **and the governed references valid at that point**. Resuming therefore compares rather than assumes:

| Check on resume | Failure outcome |
|---|---|
| Definitions and versions still resolve | `BLOCKED` |
| Evidence freshness re-evaluated **now**, not as at the checkpoint | `BLOCKED` where `STALE_AND_BLOCKING` |
| Artifacts present and hashes verified | `BLOCKED` + `ESCALATED` |
| Assignments still eligible, independence still intact | Invalidate and re-attempt, recorded |
| Class-4 acts on the replay path already recorded | Resolve by reference; **never re-execute** |
| Class-6 external effects on the replay path | Determine, or `BLOCKED` + `ESCALATED` |

**A resume is a governed event.** It is recorded, attributable where a human triggered it, and it never silently reinstates state that governance has moved past — a run resumed across a reclassification resumes into the **new** constraints.

## 6. No failure path weakens a constraint

The load-bearing rule, stated once and enforced everywhere above: **outage, urgency, retry exhaustion, cancellation, a missed deadline, an incomplete recovery and an unreachable reviewer never make a non-compliant model, deployment, storage location, reviewer, scope or sensitivity handling acceptable.** Phase 9 established this for routing and Phase 10 for storage; Phase 11 is where the pressure to break it is highest, because Phase 11 is where the work is visibly stuck.
