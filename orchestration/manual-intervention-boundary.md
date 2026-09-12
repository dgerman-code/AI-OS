# Manual Intervention Boundary

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. The Human Intervention Record

Every human act on an execution produces a first-class record. It is not a log line, not an annotation, and not optional.

| Field | Content |
|---|---|
| **Intervention ID** | `intervention.<id>` — stable, unique, never reused |
| **Run and position** | The `run.<id>`, and the stage or activity instance affected |
| **Human identity reference** | The person. **Not the account, and not the service identity that executed the change** |
| **Act** | One of the six in §2 |
| **Reason** | Why, in governed vocabulary where one exists |
| **Authority reference** | The Decision Record where the act requires one; **absent is a failure for those acts, not a blank field** |
| **Bounded effect** | Exactly what changes, and nothing beyond it |
| **Expiry** | Where the effect is time-bounded |
| **Timestamps** | Act time; effective time where they differ |
| **Resulting state** | The run's four axes before and after |

Interventions are **append-only**. An intervention that was wrong is followed by another naming it, never edited away.

## 2. Six permitted acts

| # | Act | Effect | Requires a Decision Right? |
|---:|---|---|---|
| 1 | **Resume** | `PAUSED` → `RUNNING` or `READY` | No — but resume re-runs the checks of `orchestration/failure-escalation-recovery.md` §5 |
| 2 | **Pause** | → `PAUSED` | No |
| 3 | **Cancel** | → `CANCELLED` | No. Deciding work is not wanted is not an exercise of authority over the work's content |
| 4 | **Reassign** | A new Assignment Attempt; the prior is recorded with its outcome | No — **but the new assignee must satisfy every constraint the old one did**, including independence |
| 5 | **Approve a permitted operational exception** | A bounded, expiring adjustment to a coordination parameter | **Yes.** A named, valid, approved Right whose declared subject covers it |
| 6 | **Supply missing evidence** / **request rework** | Evidence enters through the governed path; rework opens a bounded loop | No for supplying; the evidence is still assessed on its own merits |

## 3. What intervention never does

> **An administrator's ability to perform an action is not authority to authorise one.**

No intervention, by anyone, at any level of system access:

- satisfies a review, or substitutes for a reviewer;
- exercises a Decision Right that the person does not hold;
- creates a Decision Right, or widens one;
- promotes anything to canonical;
- makes produced content correct;
- lowers a sensitivity label, relaxes a residency constraint or widens a scope;
- converts `NOT_SATISFIED`, `DEFER`, `ESCALATE`, `EXPIRED` or `NO_APPLICABLE_DECISION_RIGHT` into a continuation;
- re-executes a `NON_RETRYABLE_GOVERNED_ACT`;
- edits or deletes an execution event, a Decision Record, a review finding or an audit event;
- resumes a run past a stop condition that still holds.

Act 5 is the only one requiring a Right, and its scope is deliberately narrow: it adjusts **coordination parameters** — a concurrency limit, a gate's waiting window before escalation, a retry allowance — and never a governed requirement. **There is no intervention that adjusts a governed requirement**, because that adjustment is a Phase 7 governed exception, made in Phase 7, not here.

## 4. Where a human is required rather than permitted

The twelve stop conditions. In each, the run has already stopped; intervention is how it gets an answer, and the answer comes from the governed party, not from the intervener's position.

Where the required governed party does not exist — **no approved Right covers the act** — no amount of seniority substitutes. The escalation goes to Phase 7's carding governance, and the run stays blocked until a Right exists or the work changes.

## 5. Attribution

Two identities are always recorded and never merged: the **human** who intervened, and the **system identity** that executed the change. This is the Phase 10 rule, and its value shows up at exactly one moment — when someone asks afterwards which of the two is being claimed.
