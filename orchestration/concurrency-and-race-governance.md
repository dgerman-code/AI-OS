# Concurrency and Race Governance

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Five outcomes

A fixed vocabulary, so that every race below resolves to something named rather than to whatever the implementation happened to do.

| Outcome | Meaning |
|---|---|
| `BLOCK` | The operation is refused; the run stops and a governed act or human is required |
| `IGNORE_AS_STALE` | The arriving event is recorded against its own request and **changes nothing** in the current run |
| `SUPERSEDE` | The arriving event is valid and replaces a prior one, which is retained and linked |
| `RECONCILE` | Both sides are examined and a determination is recorded; neither silently wins |
| `ESCALATE` | A human is required to decide which reading is correct |

**Last-write-wins is absent from this vocabulary**, exactly as it is absent from Phase 10's conflict vocabulary, and for the same reason: it resolves a conflict by discarding a governed change without anyone seeing it.

## 2. Ten races

| # | Race | Outcome | Why |
|---:|---|---|---|
| 1 | **Duplicate trigger** — a second trigger under a live idempotency key | `IGNORE_AS_STALE` | Recorded, so the duplicate is visible; no second run, and the first is untouched |
| 2 | **Double stage start** — two dispatches of one stage instance | `BLOCK` | A version-pinned write means the second fails rather than overwriting. Two live instances of one stage would make the stage's outcome ambiguous |
| 3 | **Concurrent edits to governed state** | `BLOCK`, then `RECONCILE` | Phase 10's version-pinned writes: the losing writer re-reads and decides. Nothing is merged automatically |
| 4 | **Stale assignment result** — work returns from an assignment already invalidated | `IGNORE_AS_STALE` | The assignment attempt records the result; the Work Item is unaffected, because the assignee was no longer eligible when they finished |
| 5 | **Review result after supersession** | `IGNORE_AS_STALE` | Recorded against the Review Instance, which remains a true record of that review. It does not satisfy a gate in the superseding run, which reviewed different work |
| 6 | **Decision result after cancellation** | `RECONCILE`, then `ESCALATE` if the act had effect | The Decision Record **stands** — a human exercised a Right and that happened. Whether its effect is now moot is a governance question, not a coordination one |
| 7 | **Two workers claim one Work Item** | `BLOCK` | The second claim fails. A race to be won would mean two assignment attempts believing they are current |
| 8 | **Model result after run reclassification** — sensitivity or criticality changed | `BLOCK` | The result was produced under constraints that no longer apply. It is **re-evaluated against the new constraints**, and where the new ones would have made it ineligible, it is not used |
| 9 | **Resumed run versus late retry** — a retry from before the resume arrives after it | `IGNORE_AS_STALE` | The checkpoint defines what is current; an attempt from a superseded position records its outcome and stops there |
| 10 | **Human intervention versus automated continuation** | **Human wins; automation `BLOCK`s** | The intervention is recorded first and the continuation refuses. A coordinator that raced a human and won would be the clearest possible statement that the human control is decorative |

## 3. Why case 6 is not `IGNORE_AS_STALE`

Cases 5 and 6 look symmetrical and are not, and the asymmetry is the point.

A **review result** is an assessment of work. If the work was superseded, the assessment is about something that is no longer current, and recording it is enough.

A **Decision Record** is an exercise of authority by a human. It happened. Discarding it as stale would be discarding a governed act because the coordinator had moved on — so the record stands, is retained, and whether its effect survives the cancellation is referred to a human. Where the decision authorised something with an external effect that already occurred, the run `ESCALATES` and **compensation**, not deletion, is the available response.

## 4. Concurrency limits

The Orchestrator Policy may declare limits — parallel activities per run, per scope, per assignee. These are **throughput controls**, and they carry two restrictions:

- a limit may **delay** a dispatch; it may never **skip** one, because a skipped stage is a workflow change;
- a limit may never be relaxed to get past a block, since a block is a constraint and a limit is a queue depth.

## 5. Ordering

The orchestrator guarantees ordering **only where the dependency graph declares it**. Two independent activities have no defined relative order and no execution may depend on one: an implicit ordering dependency is a hidden edge in a graph that is supposed to be explicit, and it will hold right up until the day scheduling changes.

**Causation identifiers, not timestamps**, establish what caused what. Clocks across systems are not ordered, and an audit that turns on a millisecond comparison is an audit that can be wrong.
