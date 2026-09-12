# Retry, Replay and Idempotency

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Seven retry classes

Every step in a workflow definition carries **exactly one** declared class. An unclassified step is **non-retryable by default** — the strict reading, because the cost of wrongly retrying an authority-bearing act is unbounded and the cost of wrongly refusing a safe retry is a human looking at it.

| # | Class | May the orchestrator retry automatically? | Conditions |
|---:|---|---|---|
| 1 | `SAFE_AUTOMATIC_RETRY` | **Yes** | Pure, internal, idempotent; no external effect; no governed record written |
| 2 | `RETRY_REQUIRING_REVALIDATION` | **Yes, after re-checking** | Preconditions, evidence freshness, scope, sensitivity and assignment eligibility are re-evaluated **before** the retry, not assumed from the first attempt |
| 3 | `RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT` | **No, until acknowledged** | A human records that they know a retry is happening and why; the acknowledgement is an intervention record |
| 4 | `NON_RETRYABLE_GOVERNED_ACT` | **Never** | Decision Records, approvals, signatures, external publication, contract commitments, risk acceptance, purge, destructive migration. **Performed once, by a governed party** |
| 5 | `REPLAYABLE_READ_ONLY` | **Yes** | Reads and derivations that write nothing; replay is free by construction |
| 6 | `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT` | **Never automatically** | Something left the system. Recovery is **compensation**, which is a new act, separately authorised |
| 7 | `IDEMPOTENT_AT_LEAST_ONCE` | **Yes** | The step carries an idempotency key and the target deduplicates; repetition is safe **because the receiver makes it so**, not because the sender tried once |

## 2. Exactly-once is not claimed

> **Across an orchestrator, a database, object storage and any external system, exactly-once delivery is not achievable, and this architecture does not assert it.**

What is provided instead, stated precisely:

| Guarantee | Where it holds | How |
|---|---|---|
| **Idempotent-at-least-once** | Classes 1, 2, 5 and 7 | Repetition is safe or deduplicated at the receiver |
| **At-most-once by governed record** | Class 4 | The governed record is the deduplication mechanism: a Decision Record for this act either exists or does not, and the second attempt finds the first |
| **Exactly-once** | **Nowhere** | Not claimed |

Class 4's guarantee is worth being precise about, because it is the one that matters. It is not achieved by the orchestrator being careful. It is achieved because the **act's existence is a governed fact recorded in an append-only store with a uniqueness constraint** — so a blind replay does not produce a second approval, it produces a failed write, which is exactly the outcome wanted.

## 3. Replay after recovery

A recovered or resumed run replays from its last **checkpoint**, and replay walks the retry classes:

| Step class on the replay path | Action |
|---|---|
| 1, 5, 7 | **Re-execute** |
| 2 | **Revalidate, then re-execute** |
| 3 | **Stop and request acknowledgement** |
| 4 | **Do not re-execute.** Resolve the existing governed record by reference and continue from it |
| 6 | **Do not re-execute.** Determine whether the effect occurred; if unknown, `BLOCKED` and `ESCALATED` |

Class 6 with an unknown outcome is the hardest case in this document and gets the strictest answer: **external side-effect uncertainty stops the run.** The orchestrator cannot tell whether the message was sent, and guessing in either direction is a decision someone else has to own.

## 4. Idempotency keys

A trigger carries an **idempotency key** derived from the workflow, the scope and the subject. A second trigger with a live run under the same key is recorded and **ignored as stale** — it does not start a second run, and it does not cancel the first.

The key is a runtime construct and carries no governance meaning: **two runs being distinct does not make their outputs distinct**, and two runs being the same does not make one of them approved.

## 5. What retry never does

- It never re-executes a class-4 act.
- It never widens a constraint to make the retry succeed.
- It never changes the assignee's independence position to get past a check.
- It never converts a `BLOCKED` run to `RUNNING`: retry re-executes a step, while a block is an unmet constraint, and only a governed act resolves one.
- It never continues past the policy's attempt limit. Exhaustion is `ESCALATED` — a human deciding, not the loop deciding for them.
