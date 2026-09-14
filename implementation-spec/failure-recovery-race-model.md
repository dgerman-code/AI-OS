# Failure, Recovery and Race Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 14 §4.3 (concurrency and race implementation) and §4.4 (compensation).

## 1. Five race outcomes — a fixed vocabulary

Every race resolves to something **named**, rather than to whatever the implementation happened
to do.

| Outcome | Meaning |
|---|---|
| `BLOCK` | The operation is refused; the run stops and a governed act or human is required |
| `IGNORE_AS_STALE` | The arriving event is recorded **against its own request** and changes nothing in the current run |
| `SUPERSEDE` | The arriving event is valid and replaces a prior one, which is **retained and linked** |
| `RECONCILE` | Both sides are examined and a determination is recorded; **neither silently wins** |
| `ESCALATE` | A human is required to decide which reading is correct |

**Rule F-1 — `LAST_WRITE_WINS` is absent from this vocabulary**, exactly as it is absent from
Phase 10's conflict vocabulary and Phase 11's race vocabulary, and for the same reason: it
resolves a conflict by discarding a governed change without anyone seeing it. There is no code
path, no configuration and no fallback in this specification that implements it.

**Rule F-2 — `IGNORE_AS_STALE` is not "drop".** The arriving event is **recorded against its own
request**, so the duplicate or late result is visible. Nothing is discarded; it simply changes
nothing in the current run.

## 2. The ten races, as enforceable persistence semantics

| # | Race | Outcome | Enforcement |
|---:|---|---|---|
| 1 | **Duplicate trigger** — a second trigger under a live idempotency key | `IGNORE_AS_STALE` | U14 partial unique index on `(idempotency_key) WHERE NOT terminal`. The second insert fails; the refusal is recorded as a trigger record linked to the live run. No second run; the first untouched |
| 2 | **Double stage start** — two dispatches of one stage instance | `BLOCK` | U13 `UNIQUE (run_ref, task_ref, rework_iteration)` **plus** a version-pinned write on the run. The second fails rather than overwriting |
| 3 | **Concurrent edits to governed state** | `BLOCK`, then `RECONCILE` | `record_version` mismatch → `STALE_WRITE`, nothing written. The losing writer **re-reads and decides**; nothing is merged automatically |
| 4 | **Stale assignment result** — work returns from an assignment already invalidated | `IGNORE_AS_STALE` | The result is written against the `assignment_ref` it belongs to; the Work Item's current assignment pointer is unchanged. Eligibility is re-evaluated at completion, not assumed from dispatch |
| 5 | **Review result after supersession** | `IGNORE_AS_STALE` | The Review Instance is recorded and remains a true record of that review. It does not satisfy a gate in the superseding run, enforced by U10 keying evidence to the **gate instance**, which the superseding run does not share |
| 6 | **Decision result after cancellation** | `RECONCILE`, then `ESCALATE` if the act had effect | The Decision Record **stands** — a human exercised a Right and that happened. A reconciliation record is written; where the decision authorised an external effect that already occurred, the run `ESCALATE`s and **compensation**, not deletion, is the available response |
| 7 | **Two workers claim one Work Item** | `BLOCK` | U12 `UNIQUE (work_item_ref, attempt_ordinal)` plus a version-pinned claim. The second claim fails |
| 8 | **Model result after run reclassification** — sensitivity or criticality changed | `BLOCK` | `routing_decision.scope_binding_at_decision` is compared against the run's current binding. The result is **re-evaluated against the new constraints**, and where the new ones would have made it ineligible it is **not used** |
| 9 | **Resumed run versus late retry** | `IGNORE_AS_STALE` | The checkpoint defines what is current; an attempt from a superseded position records its outcome against its own attempt record and stops there |
| 10 | **Human intervention versus automated continuation** | **Human wins; automation `BLOCK`s** | The intervention is recorded first, in a transaction that bumps the run's `record_version`; the continuation's version-pinned write then fails |

### 2.1 Why case 6 is not `IGNORE_AS_STALE` — and why the implementation must not "simplify" it

Cases 5 and 6 look symmetrical and are not.

A **review result** is an assessment of work. If the work was superseded, the assessment is about
something no longer current, and recording it is enough.

A **Decision Record** is an exercise of authority by a human. **It happened.** Discarding it as
stale would be discarding a governed act because the coordinator had moved on. So the record
stands, is retained, and whether its effect survives the cancellation is referred to a human.

**Rule F-3.** An implementation that handles cases 5 and 6 with one shared code path has
collapsed `REVIEW INSTANCE != DECISION RECORD` in its error handling, which is exactly where such
collapses are least visible.

## 3. Failure distinctions

Seven distinctions, never merged, because the recovery for each is different:

| # | Distinction | Recovery |
|---:|---|---|
| 1 | **Transient infrastructure failure** | Retry within the declared class |
| 2 | **Deterministic defect** | No retry; escalate |
| 3 | **Governed refusal** — a constraint was not met | Not a failure at all. The refusal is the correct outcome |
| 4 | **Missing authority** | `BLOCKED` + `ESCALATED`, posture `AUTHORITY_ABSENT` |
| 5 | **Unmet dependency** | `WAITING` with a named subject |
| 6 | **External-effect uncertainty** | Reconciliation (§6) |
| 7 | **Partial write / inconsistency** | Reconciliation sweep, then `RECONCILE` or `ESCALATE` |

**Rule F-4 — a governed refusal is never reported as an error to be retried.** Distinction 3 is
the outcome working. An implementation whose retry logic cannot tell 1 from 3 will eventually
retry its way past a constraint.

**Rule F-5 — "flake" is not a root cause.** A failure is re-attempted only where its declared
retry class permits it and the failure is genuinely of kind 1. Repeating an operation because
its cause is not understood is prohibited.

## 4. Stop conditions

A run stops — and does not continue on the strength of anything else — when any of these holds:
a required Decision Right is absent; a gate is `NOT_SATISFIED` with no permitted rework path; a
rework loop has exhausted `max_iterations`; posture is `AUTHORITY_ABSENT`; a scope constraint
cannot be satisfied; a residency or sensitivity constraint cannot be satisfied; the candidate
universe is incomplete; a prerequisite reference is dangling; evidence freshness is
`STALE_AND_BLOCKING` at a band where that blocks; a material conflict is unresolved on a point
the act depends on; an external effect is in `ATTEMPTED_OUTCOME_UNKNOWN`; a human intervention
requires it.

**Rule F-6 — no stop condition is relaxable by any of:** outage, urgency, retry exhaustion,
cancellation, a missed deadline, an incomplete recovery, a model's confidence, an administrator's
capability, or a configuration flag.

## 5. Retry and replay after recovery

A recovered or resumed run replays **from its last checkpoint**, and replay walks the retry
classes (`orchestrator-runtime-contract.md` §8). Nothing is re-executed because it is convenient
to re-execute it.

**Rule F-7 — replay of an authority-bearing act is a defect, not a recovery.** A Decision
Record, approval, signature, external publication, contract commitment, risk acceptance, purge
or destructive migration is **performed once**. On replay, the durable uniqueness constraint
finds the first act and the second attempt fails — which is the outcome wanted.

**Rule F-8 — no empty acts to force progress.** There is no mechanism for re-triggering a run by
writing a no-op record, re-opening and re-closing a gate, or re-submitting an unchanged request
to move a state machine.

## 6. External-effect uncertainty and reconciliation

The hardest real case: **the external call was made and the local commit certainty is unknown.**

**Rule F-9 — uncertainty is a recorded state, not a gap.** The execution record's
`external_effect_state` is one of:

| State | Means | Next |
|---|---|---|
| `NOT_ATTEMPTED` | The outbox row exists; no call was made | Drain normally |
| `ATTEMPTED_OUTCOME_UNKNOWN` | The call was made; the outcome is not known | **Reconciliation.** No retry, no assumption either way |
| `CONFIRMED_APPLIED` | The effect occurred | Record the external reference |
| `CONFIRMED_NOT_APPLIED` | The effect did not occur | Re-attempt **only** where the retry class permits |

**Rule F-10 — the two forbidden assumptions.** In `ATTEMPTED_OUTCOME_UNKNOWN` the system must
not assume failure (and re-attempt, risking a duplicate irreversible act) and must not assume
success (and proceed on an effect that may not exist). Both are how one uncertain state becomes
two wrong ones.

### 6.0 Model invocation is the ordinary case, not an exception

The staged protocol of `api-command-contracts.md` §5.5 is the general external-effect shape
applied to the one external call this system makes by design. Its five stages map onto the four
states above exactly:

| Stage | Attempt state after it |
|---|---|
| 1 — local intent commit | `NOT_ATTEMPTED` |
| 2 — provider call | unchanged locally; **this is the window where the state on disk and the state of the world can differ** |
| 3 — observed outcome | `CONFIRMED_APPLIED`, `CONFIRMED_NOT_APPLIED`, or `ATTEMPTED_OUTCOME_UNKNOWN` |
| 4 — result recording | only from `CONFIRMED_APPLIED`, **in the same transaction as stage 3** |
| 5 — reconciliation | resolves `ATTEMPTED_OUTCOME_UNKNOWN`, or records that it remains unresolved and escalates |

**Rule F-9a — an expired claim is read by the boundary flag, and expiry alone proves nothing.**
An earlier revision said an expired lease always reads as `ATTEMPTED_OUTCOME_UNKNOWN`. That was
right about the case it was worried about and wrong about the case beside it, and the two are now
separated. Expiry says a claimant stopped reporting. What the system may conclude from it depends
entirely on whether the durable pre-call state had committed — never on the clock, never on how
long ago, and never on the previous state's name.

**Rule F-9a-map — the five conditions, distinguished exactly.** This is the single mapping; the
persistence protocol implements it and no other document restates it.

| # | Condition | Durable evidence | What the system may conclude | Next |
|---:|---|---|---|---|
| 1 | **Claim expired before the boundary was crossed** | `claim_state = 'CLAIMED'`, `boundary_crossed = false` | **No call was made.** This is a conclusion the local state is entitled to, because no call is ever made from `CLAIMED` (PO-8) | T6 back to `PENDING`; re-dispatch under the **same** key (PO-14a). The attempt stays `NOT_ATTEMPTED` |
| 2 | **Claim expired after the boundary was crossed** | `claim_state = 'DISPATCH_PENDING'`, `boundary_crossed = true` | **Nothing.** The provider may or may not have acted, and no local fact distinguishes the two | T7 to `UNCERTAIN`; the attempt becomes `ATTEMPTED_OUTCOME_UNKNOWN`; reconciliation is mandatory. **Never a re-dispatch** (PO-14) |
| 3 | **Unknown external effect** | attempt `ATTEMPTED_OUTCOME_UNKNOWN`, item `UNCERTAIN` | **Nothing**, until the external system answers. Rule F-10's two forbidden assumptions both apply | Reconciliation sweep §6.1. Unanswerable → T9 `ABANDONED`, block and escalate |
| 4 | **Confirmed not applied** | reconciliation answered under the stable key | The effect **did not occur**. That is an answer from the provider, not an inference from local state | T8 to `SETTLED`. Continuation, where the retry class permits, is a **new** governed provider attempt at the next ordinal with a **new** key — never a replay of this item (PO-14) |
| 5 | **Settled effect** | attempt `CONFIRMED_APPLIED` or `CONFIRMED_NOT_APPLIED`, item `SETTLED` | The effect is known and recorded | Nothing further. Undoing a `CONFIRMED_APPLIED` effect is compensation — a new governed act, never a rollback (§7) |

Conditions 1 and 2 are the pair the earlier wording collapsed. **The dangerous reading is
condition 2 treated as condition 1**, and what prevents it is that the pre-call state commits
before the call, so the distinction is a stored fact rather than a judgement.

**Rule F-9c — stages 3 and 4 have no boundary between them.** They are one local transaction
(`api-command-contracts.md` Rule Q-22b), so this model describes **no** crash state in which an
outcome is durable and its Model Result is not. A recovery path for that state would be a
recovery path for a state the system cannot reach, and those are how impossible states become
reachable.

**Rule F-9d — the drain protocol is specified once, in persistence §9.** Claim state, lease
owner, lease expiry, the fencing token and claim generation, the atomic acquisition predicate, the
stable provider idempotency key, the **eleven** token-fenced transitions and the five crash
points all live in `persistence-and-transaction-model.md` §§9.2–9.6. This section
states the governed consequence: an item whose **`boundary_crossed` is `true`** is **never**
re-dispatched — under any condition, including a `CONFIRMED_NOT_APPLIED` reconciliation and a
provider that deduplicates — its attempt is `ATTEMPTED_OUTCOME_UNKNOWN` until reconciliation
answers, and reconciliation is mandatory. Where the work continues after a
`CONFIRMED_NOT_APPLIED` answer, it continues as a **new** governed provider attempt with a new
identity and a new idempotency key, which is a governed act rather than an operational replay.

**Rule F-9e — the call boundary is crossed before it is crossed.** The durable intent to call
(`DISPATCH_PENDING`) commits **before** the call leaves, so no crash after the call can be
mistaken for a crash before it. Recovery therefore never infers non-occurrence from local state
after the boundary: it reads the monotone `boundary_crossed` flag, and `true` means *the provider
may have acted*. An expired claim is a statement about a claimant, never about a provider
(PO-10).

**Rule F-9b — a timeout is a state, not a verdict.** It does not mean the call failed. Rule F-10
applies unchanged: neither assumption is permitted.

### 6.1 Reconciliation sweep

A periodic, idempotent, read-mostly process that detects and records — and **decides nothing**:

| Detects | Action |
|---|---|
| Outbox rows in `ATTEMPTED_OUTCOME_UNKNOWN` past a threshold | Query the external system by idempotency key; record `CONFIRMED_*`, or `ESCALATE` if unanswerable |
| Orphaned storage objects | `QUARANTINE` and expire under the retention class; **never adopt** |
| Governed record without its audit event, or the reverse | Record the inconsistency; `ESCALATE` |
| A gate outcome without admissible evidence | `ESCALATE` — this should be unreachable, and if it is reached the constraint model has a hole worth knowing about |
| A Decision Record whose separation compliance cannot be evidenced | `ESCALATE` |
| Runs `WAITING` past a policy threshold | Record; **never auto-advance** |

**Rule F-11 — the sweep never decides.** It records determinations of fact ("the external system
reports this idempotency key was applied") and escalates questions of governance. It cannot
satisfy a gate, complete a run, resolve a conflict or compensate.

**Rule F-12 — a timeout in the sweep is not an outcome.** A run `WAITING` for a long time is
recorded as waiting for a long time. It is never converted into `EXPIRED`-as-approval, and
`EXPIRED` itself is `ESCALATED` and never an approval.

## 7. Compensation — a new governed act

**Rule F-13.** Compensation is **never** a rollback of a completed external act. There is no
undo. The four-record lineage of `orchestrator-runtime-contract.md` §11 applies, and
compensating adds three more records:

```
  intent ──► authorisation (Decision Record) ──► execution ──► external_effect_state
                                                       │
                                                       ▼   (where the effect occurred and must be undone)
  compensation_request ──► compensation_authorisation ──► compensation_execution
```

| Record | Requires |
|---|---|
| `compensation_request` | The original execution record, the reason, the proposed compensating act, its own bounded subject |
| `compensation_authorisation` | A **Decision Record** under a Right whose **declared subject covers the compensating act**. Not the original Right, unless its card covers both |
| `compensation_execution` | Its own idempotency key, its own external-effect uncertainty state |

**Rule F-14 — the original records are never altered.** Compensation **links to** them. The
original act remains in history as what it was, because it was.

**Rule F-15 — compensation may itself be unauthorised.** Where no approved Right covers the
compensating act, the outcome is `NO_APPLICABLE_DECISION_RIGHT` and the run `ESCALATE`s with the
external effect standing and recorded. This is uncomfortable and it is correct: the alternative
is a system that can perform unauthorised external acts as long as it calls them cleanups.

**Rule F-15a — termination is the system's act and needs no human.** Where continuing would
breach a constraint, the system stops the run as `TERMINATED`, naming the constraint. It does
not wait for a human, does not synthesise an intervention, and does not record a human identity
it does not have. `CANCELLED` is the different case: a human act, with an intervention record,
because the work is not wanted. Collapsing the two would either leave the system unable to stop
a breach or attribute a machine stop to a person.

**Rule F-16 — cancellation does not undo commitments.** Cancelling a governed path preserves the
reason, the state at cancellation, open findings and risks, artifacts and evidence, prior
decisions, and **external commitments already made**. There is no destructive history erasure,
and cancelling a path does not undo commitments already given to third parties.

## 8. Recovery objectives are operational, not governance

Recovery point and recovery time objectives, backup cadence and restore drills are operational
engineering decided per environment. Two governance rules bound them:

**Rule F-17.** A restore **never** rewrites audit, decision, review, routing or canonical
history. Restoring to an earlier point is itself an act, recorded, and the gap between the
restore point and the failure is a recorded gap — not silently absent history.

**Rule F-18.** `backup != archive != audit`. A backup's existence proves nothing about
governance, and a backup is never cited as evidence in any gate.
