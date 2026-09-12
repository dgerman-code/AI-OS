# Scheduling and Dependency Model

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Six dispatch kinds — what may be scheduled and what may only be requested

The distinction is the whole section. **Scheduling** means the orchestrator decides when something starts and expects it to run. **Requesting** means it asks a governed party and waits for an outcome it does not control.

| # | Dispatch kind | Scheduled or requested | What the orchestrator controls |
|---:|---|---|---|
| 1 | **Machine-executable activity** | **Scheduled** | When it starts, its inputs, its retry class |
| 2 | **Human work** | **Requested** | That the request exists, with scope, criticality and context. **Not when it is done** |
| 3 | **Review** | **Requested** | That a Review Request exists against the applicable Profile. **Not its outcome** |
| 4 | **Decision Right exercise** | **Requested** | That a Decision Request exists naming the Right. **Not whether it is exercised, or how** |
| 5 | **Model routing** | **Requested** | That a routing request exists with the constraints the stage declares. **Not which model is chosen** |
| 6 | **External event** | **Awaited** | Nothing. It arrives or it does not |

> **Human authority is not a worker queue.** Kinds 2, 3 and 4 are not "slow activities": they are acts by parties the orchestrator has no authority over. Modelling them as queue entries would make a backlog look like a bottleneck to be optimised, and the first optimisation anyone reaches for is a timeout default — which is the thing this architecture most needs to be impossible.

## 2. Eight dependency kinds

| # | Kind | Satisfied by | Unsatisfied outcome |
|---:|---|---|---|
| 1 | **Hard prerequisite** | A named prior stage or activity reaching a terminal `COMPLETED` state | `WAITING_FOR_DEPENDENCY` |
| 2 | **Review prerequisite** | A Review Instance reaching `SATISFIED` under its Profile | `WAITING_FOR_REVIEW`; **`NOT_SATISFIED` → `REWORK_REQUIRED` or `BLOCKED`, never continuation** |
| 3 | **Decision prerequisite** | A Decision Record produced by an eligible human exercising a named Right | `WAITING_FOR_DECISION`; **no Right → `AUTHORITY_ABSENT`, block and escalate** |
| 4 | **Data / evidence prerequisite** | Evidence resolving with a Phase 8 freshness verdict the band accepts | `WAITING_FOR_DEPENDENCY`; **`STALE_AND_BLOCKING` → `BLOCKED`** |
| 5 | **Artifact prerequisite** | A Phase 10 artifact record resolving, with its object present and its hash verified | `WAITING_FOR_DEPENDENCY`; **quarantined or missing → `BLOCKED`** |
| 6 | **External-system prerequisite** | A declared external condition | `WAITING_FOR_EXTERNAL_EVENT` |
| 7 | **Timing prerequisite** | A declared time or interval | `WAITING_FOR_DEPENDENCY` |
| 8 | **Conditional branch prerequisite** | A branch condition over **governed state only** | `BLOCKED` if the condition cannot be evaluated |

Kind 8 carries a restriction worth stating: a branch condition may read governed state — a review outcome, a decision, an artifact property, a criticality band. **It may not read a model's opinion, a confidence score or an operational log.** A branch that turns on a model's self-assessment has let confidence choose the path, which is the collapse Phase 9 §4 refuses in routing and this refuses in sequencing.

## 3. The graph is acyclic; rework is a declared loop

The dependency graph of a workflow definition is a **DAG**. Rework is not a back-edge in it — a hidden cycle is a run that can never be shown to terminate, and worse, one whose repetitions look like progress.

Rework is a **bounded loop construct**, declared in the workflow definition with:

- the **entry condition** — which governed outcome opens it (a `NOT_SATISFIED` review, a rejected decision, a rework request);
- the **body** — the stages re-executed;
- a **declared maximum iteration count**;
- the **exhaustion outcome** — `ESCALATED`, always, never `FAILED` and never silent continuation.

Each iteration is recorded as a distinct set of stage instances. **The prior iteration's instances are retained**, so the question of how many times something was reworked has an answer, and so does the question of what changed between iterations.

Exhausting the maximum is not a failure of the work; it is the discovery that the loop is not converging, which is a thing a human needs to see.

## 4. What the orchestrator may reorder, and what it may not

| May | May not |
|---|---|
| Dispatch independent activities concurrently within policy limits | Reorder stages the definition sequences |
| Choose among ready work items by policy priority | Skip a stage because its outputs seem unnecessary |
| Defer a dispatch to respect a concurrency limit | Start a stage whose dependencies are unmet |
| Batch requests to one party | Merge two stages into one, or split one into two |
| Schedule a retry within its class | Re-run a completed stage without a rework loop |

**Sequencing is the workflow definition's; timing is the orchestrator's.** A coordinator that could reorder stages would be editing the workflow, and the Orchestrator Policy — which is where coordination behaviour lives — is explicitly not permitted to change what a stage means (`orchestration/execution-run-model.md` §1).

## 5. Long-running executions

A run may be open for weeks, and long duration changes three things:

1. **Definitions may have moved.** The run stays bound to the versions it started with. Where a newer approved version exists, that is recorded as a **notice**, not applied: silently upgrading a running execution would mean it executed neither version.
2. **Evidence may have gone stale.** Freshness is re-evaluated **at the point of use**, not at intake. Evidence that was `CURRENT_FOR_USE` in week one and `STALE_AND_BLOCKING` in week six blocks in week six — Phase 8's verdicts are use-specific and Phase 11 does not cache them.
3. **Assignments may have lapsed.** An assignment whose assignee is no longer eligible — role changed, independence now violated by other work they have done — is **invalidated and re-attempted**, with the invalidation recorded. It is never honoured on the grounds that it was valid when made.

Checkpoints exist for this: a resume point records the state **and the governed references valid at that point**, so a resume can compare them against now rather than assume them.
