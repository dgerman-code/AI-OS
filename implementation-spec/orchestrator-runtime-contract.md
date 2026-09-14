# Orchestrator Runtime Contract

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 findings **M-2** (execution-event semantics, jointly with
`audit-provenance-observability.md`) and Phase 14 §4.1 (bounded rework loops).

## 1. What the orchestrator is, and is not

A **coordination control plane**. It reads approved definitions and current governed state,
instantiates bounded execution records, activates already-defined stages, requests governed acts
from the phases that own them, waits, records, and escalates.

It is the one component positioned to see everything at once, which is exactly why it is given
authority over nothing. **A coordinator that could approve would be the shortest path around
every gate in the architecture.**

| It may | It may never |
|---|---|
| Read approved definitions and governed state | Invent authority |
| Instantiate execution records | Infer approval from completion |
| Activate defined workflow stages | Infer competence from model output |
| Request role-capable work | Turn a model result into a reviewed, approved or canonical result |
| Submit a routing request | Choose a provider, endpoint, deployment or model |
| Request reviews and Decision Right exercise | Self-satisfy a review or self-exercise a Right |
| Pause while waiting on humans or prerequisites | Treat a timeout or an expiry as approval |
| Carry open items forward **where upstream semantics permit** | Silently resolve findings, conflicts or `UNKNOWN` states |
| Record execution state and correlation metadata | Rewrite governed history |
| Retry **where retry is explicitly safe** | Replay an authority-bearing act |
| Escalate where continuation is not allowed | Lower sensitivity, residency or materiality constraints |
| Narrow what a stage sees | **Never** cross a scope boundary, and never widen where material may go |
| — | **Never** use operational logs as governance evidence |

## 2. Trigger intake

A trigger is a **request, not a start**. Intake validates, in this order, before any work is
scheduled:

| # | Check | Failure outcome |
|---:|---|---|
| 1 | The Workflow Definition resolves at a named version in the approved baseline | `BLOCK` |
| 2 | The Orchestrator Policy resolves at a named version | `BLOCK` |
| 3 | Exactly one governed scope is named and the originator may act in it | `BLOCK` |
| 4 | Sensitivity labels, handling controls and residency constraints are present or explicitly assessed | `BLOCK` — **unassessed is restricted, never permissive** |
| 5 | Criticality band resolves | `BLOCK` |
| 6 | The trigger is not a duplicate of a live run under the same idempotency key | `IGNORE_AS_STALE`, recorded |
| 7 | Every declared prerequisite artifact, evidence or decision reference resolves, or is declared `FUTURE_GOVERNANCE_REFERENCE` and therefore non-executable | `BLOCK` on a dangling reference |

**Rule O-1.** A trigger failing any check produces a **recorded refusal, not a run that fails
later**. The distinction matters because a run that started and then blocked has already
consumed assignments, routing requests and possibly external effects.

## 3. Run state — four orthogonal axes

### 3.1 Axis A — run phase (10 non-terminal)

`CREATED` · `VALIDATING` · `READY` · `RUNNING` · `WAITING` · `RETRY_PENDING` ·
`REWORK_REQUIRED` · `PAUSED` · `BLOCKED` · `ESCALATED`

### 3.2 Axis B — terminal outcome (6)

`COMPLETED` · `COMPLETED_WITH_OPEN_ITEMS` · `CANCELLED` · `TERMINATED` · `FAILED` · `SUPERSEDED`

### 3.3 Axis C — wait reason (5)

Every `WAITING` run names its reason **and its subject**. A wait with no named subject is a
defect: it cannot be told from a stall.

### 3.4 Axis D — governance posture (4)

`GOVERNANCE_CLEAR` · `OPEN_ITEMS_CARRIED` · `GATE_UNSATISFIED` · `AUTHORITY_ABSENT`

**Rule O-2.** `GATE_UNSATISFIED` and `AUTHORITY_ABSENT` permit **no** terminal completion
outcome. The permitted-completion map is a constant, not a policy setting.

**Rule O-3 — the transition table is the architecture's.** `ALLOWED_TRANSITIONS` and
`TERMINAL_REACHABLE_FROM` are derived from `orchestration/state-machine-and-transitions.md` §6
and reconciled against that document by an automated check. A table that drifts from the
architecture fails; it does not agree with itself.

## 4. The halted guard

**Rule O-4.** One guard, called by **every** ordinary governed API before it changes anything:
stage activation, assignment, routing request, route, model invocation, review, decision,
external gate satisfaction, human work, prerequisite, retry, intervention recording, pause,
sub-run, scope transfer and completion.

It refuses when the run is terminal, or is in `BLOCKED` or `ESCALATED`, or carries posture
`AUTHORITY_ABSENT`.

**Rule O-5.** `unblock()` is the **only** API exempt from the guard, and it earns the exemption
by being harder rather than easier:

1. the run is terminal → refuse;
2. the run is not in a halted phase → refuse;
3. a validated human intervention naming **this** run (the one intervention contract, §9);
4. no gate still stands unresolved against continuation;
5. every fallible check precedes the first mutation.

**Rule O-6.** Stopping a halted run — `CANCELLED`, `TERMINATED` — stays permitted. **Stopping is
always permitted; only completing is governed.**

**Rule O-6a — cancellation and termination are asymmetric, and the asymmetry is load-bearing.**
Phase 11 `orchestration/state-machine-and-transitions.md` §3:

| Terminal | Definition | Requires |
|---|---|---|
| `CANCELLED` | Stopped before completion **by a human act**; the work is not wanted | **An intervention record**, through the one intervention contract of §9 |
| `TERMINATED` | Stopped **by the system** because continuing would breach a constraint | **A named constraint**. No intervention, and none is fabricated |
| `FAILED` | Stopped by an error that no permitted retry or recovery resolved | A recorded cause |
| `SUPERSEDED` | Replaced by another run for the same subject | The superseding `run.<id>` |

An earlier revision of this package required a human intervention for both cancellation and
termination. That is wrong in both directions: it blocks the system from stopping work that
would breach a constraint, and where it does not block it, it invents human provenance for a
machine act. A termination therefore records the acting **system identity**, the named
constraint, its execution event and its audit event — and no human identity at all, because
there was none.

Terminal semantics are identical across all four: immutable, no outgoing transition, and
re-examination only by creating a new run that names this one.

## 5. Work Items and assignment

**Rule O-7 — `TASK != WORK ITEM`.** A Task is the unit of *definition*, bound to a Workflow
Definition at a version. A Work Item is the unit of *assignment*, created by activating a stage.
Reassignment never rewrites the workflow.

**Rule O-8 — the required Role comes from bound lineage.** The Role an assignment must match is
read from the Work Item's bound Task, not from an argument the caller supplies.

**Rule O-9 — an assignment confers nothing.** It does not make its holder a reviewer and does
not make them a Decision Right holder. The assignment envelope carries what the Role, Skill and
scope already carry, and nothing more.

**Rule O-10 — attempt counting is validate-then-commit.** The attempt number is computed as a
local value; the Assignment is constructed (which is what validates the Agent Instance
reference); the insert is preflighted; **only then** is the counter written, the record appended
and the event emitted. There is no decrement-on-exception anywhere: the design is
validate-then-commit, not mutate-then-rollback.

## 6. Gates

### 6.1 Four gate kinds, one admissible evidence type each

| Gate kind | Admissible evidence | Produced by |
|---|---|---|
| `REVIEW` | `ReviewInstance` | C5 |
| `DECISION` | `DecisionRecord` | C6 |
| `HUMAN_WORK` | `HumanWorkCompletion` | Human, via C15 |
| `GOVERNED_PREREQUISITE` | `PrerequisiteEvidence` | The governed producer of the prerequisite |

**Rule O-11 — the evidence contract is exclusive.** Each gate kind admits **exactly one**
evidence type. Offering a Model Result, a Routing Decision, an execution event, a log line, a
Review Instance to a `DECISION` gate, or a Decision Record to a `REVIEW` gate is refused as an
evidence error.

### 6.2 Seven gate outcomes; two continue

| Outcome | Effect |
|---|---|
| `SATISFIED` | Continue |
| `SATISFIED_WITH_OPEN_ITEMS` | Continue; posture `OPEN_ITEMS_CARRIED`; items recorded and carried **where an upstream rule permits** |
| `NOT_SATISFIED` | `REWORK_REQUIRED` or `BLOCKED`. **Never continuation** |
| `DEFER` | `WAITING` or `ESCALATED`. **Never `APPROVE`** |
| `ESCALATE` | `ESCALATED`. **Never `APPROVE`** |
| `EXPIRED` | `ESCALATED`, posture unchanged. **Never an approval** |
| `NO_APPLICABLE_DECISION_RIGHT` | `BLOCKED` **and** `ESCALATED`; posture `AUTHORITY_ABSENT` |

**Rule O-12 — `GATE REQUIREMENT != GATE INSTANCE`.** A requirement is declared in the Workflow
Definition at a version. An instance is this run's instance of it, with its own identity.
Repeated activation and reused requirement ids do not displace an existing instance.

**Rule O-13 — exact lineage.** A gate instance is satisfied only by evidence that names this
run, this Work Item, this gate instance, the declared Profile or Right, and — for reviews — the
declared independence class. Every part is checked by lookup against records the orchestrator
itself holds.

**Rule O-14 — `SATISFIED_WITH_OPEN_ITEMS` is not a discount.** Each carried item requires an
upstream rule permitting it to be carried. An item with no such rule makes the outcome
`NOT_SATISFIED`.

## 7. Bounded rework loops — Phase 14 §4.1

**Rule O-15 — the graph is acyclic; rework is a declared loop.** The dependency graph of a
Workflow Definition is a **DAG**. Rework is **not a back-edge** in it — a hidden cycle is a run
that can never be shown to terminate, and worse, one whose repetitions look like progress.

A rework loop is declared in the Workflow Definition with:

| # | Declared | Notes |
|---:|---|---|
| 1 | `rework_loop_id` | Stable within the Workflow Definition version |
| 2 | Entry condition | Which governed outcome opens it — a `NOT_SATISFIED` review, a `REJECT` decision, a rework request. Objective and testable |
| 3 | Loop body | The stage set re-executed |
| 4 | Exit condition | Which governed outcome closes it |
| 5 | `max_iterations` | An integer, declared. **There is no default and no unbounded value** |

### 7.1 `rework_loop_instance`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `rework_loop_ref` | `ReworkLoopRef` | NO | IMM | |
| `run_ref` | ref | NO | IMM | |
| `rework_loop_id` + `workflow_version` | pair | NO | IMM | The declaration this instantiates |
| `iteration_ordinal` | int | NO | IMM | Starts at 1; strictly increasing |
| `entry_condition_evidence` | ref | NO | IMM | The governed outcome that opened this iteration |
| `stage_instances` | set of refs | NO | APP | **This iteration's** instances |
| `opened_at` / `closed_at` | timestamps | NO / YES | IMM / APP | |
| `close_reason` | enum | YES | APP | `EXIT_CONDITION_MET` \| `MAX_ITERATIONS_EXHAUSTED` \| `RUN_TERMINATED` |

Constraint: `UNIQUE (run_ref, rework_loop_id, iteration_ordinal)`.

**Rule O-16 — prior iterations are retained.** Each iteration is recorded as a **distinct set of
stage instances**, and the prior iteration's instances are retained. The question of how many
times something was reworked has an answer, and so does the question of what changed between
iterations. Nothing is overwritten by a re-run.

**Rule O-17 — exhaustion escalates.** Exhausting `max_iterations` is not a failure of the work;
it is the discovery that the loop is **not converging**, which is a thing a human needs to see.
The run goes `ESCALATED` with the loop identity, the iteration count, and each iteration's
closing outcome. It does not fail, does not complete, and does not silently iterate once more.

**Rule O-18 — no graph-cycle ambiguity.** A Workflow Definition whose stage dependency graph
contains a cycle **outside a declared rework loop** is rejected at definition load. The check is
a topological sort over the dependency edges with declared loop bodies contracted to a single
node.

## 8. Retry and replay

Every step carries **exactly one** declared retry class. **An unclassified step is non-retryable
by default** — the strict reading, because the cost of wrongly retrying an authority-bearing act
is unbounded and the cost of wrongly refusing a safe retry is a human looking at it.

| # | Class | Automatic retry? | Conditions |
|---:|---|---|---|
| 1 | `SAFE_AUTOMATIC_RETRY` | Yes | Pure, internal, idempotent; no external effect; no governed record written |
| 2 | `RETRY_REQUIRING_REVALIDATION` | Yes, **after re-checking** | Preconditions, evidence freshness, scope, sensitivity and assignment eligibility re-evaluated **before** the retry, never assumed from the first attempt |
| 3 | `RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT` | No, until acknowledged | The acknowledgement is an intervention record |
| 4 | `NON_RETRYABLE_GOVERNED_ACT` | **Never** | Decision Records, approvals, signatures, external publication, contract commitments, risk acceptance, purge, destructive migration. **Performed once, by a governed party** |
| 5 | `REPLAYABLE_READ_ONLY` | Yes | Writes nothing; replay is free by construction |
| 6 | `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT` | **Never automatically** | Something left the system. Recovery is **compensation**, a new act, separately authorised |
| 7 | `IDEMPOTENT_AT_LEAST_ONCE` | Yes | Carries an idempotency key and the target deduplicates; repetition is safe **because the receiver makes it so** |

**Rule O-19 — retry class comes from the Work Item's bound lineage**, never from a caller
argument. A caller cannot substitute a permissive class.

**Rule O-20 — a refused retry is a halt, and a halt is a write.** `retry()` on a class-4 or
class-6 step — or on a step with no declared class — transitions the run to `BLOCKED` →
`ESCALATED` with posture `GATE_UNSATISFIED` **and writes a `retry_refusal_record`** naming the
class, the act and why no number of attempts produces what is missing. It does not raise into
the caller's control flow, does not silently no-op, and is never "nothing written": three
governed writes, three audit events, two execution events.

**Rule O-20a — every retry class has a defined branch.** Nine branches — R1, R2, R2f, R3, R3a,
R4, R6, R7 and RX — each with its preconditions, its phase and posture before and after, its
exact governed writes, its audit and execution counts, whether a dispatch record exists and
whether an escalation record exists. They are specified in `api-command-contracts.md` §5.6 and
committed branch by branch in `persistence-and-transaction-model.md` §7.2. **No branch is
ambiguous and none writes nothing.**

**Rule O-20b — a refusal is one transaction.** The refusal record, the block and the escalation
commit together or not at all. A run that is `BLOCKED` without its refusal record is not a state
this specification permits.

**Rule O-20c — compensation is never reached by retrying.** An unknown external effect is
reconciled; a confirmed one that must be undone is compensated through its own lineage (§11).
Re-running it is the duplicate-irreversible-act failure class 6 exists to prevent.

**Rule O-21 — guarantees, stated exactly.**

| Guarantee | Where it holds | How |
|---|---|---|
| Idempotent-at-least-once | Classes 1, 2, 5, 7 | Repetition is safe or deduplicated at the receiver |
| **At-most-once by governed record** | Class 4 | The governed record **is** the deduplication mechanism: the record either exists or does not, and the second attempt finds the first |
| **Exactly-once** | **Nowhere** | **Not claimed** |

Class 4's guarantee is not achieved by the orchestrator being careful. It is achieved because
the act's existence is a governed fact in an append-only store **with a durable uniqueness
constraint** — so a blind replay produces a failed write, not a second approval. See
`persistence-and-transaction-model.md` §5.2.

## 9. Human intervention — one contract

Six intervention acts: resume · pause · cancel · reassign · supply evidence · request rework.
Each attributable and bounded.

**Rule O-22 — one intervention contract, used by every consuming path.** Ordinary recording,
`pause`, `unblock`, and **every terminal outcome that accepts an intervention** validate through
the same read-only contract. A terminal-specific weaker validator is prohibited: that asymmetry
is precisely how a foreign-run or non-record object reaches a store.

The contract refuses, before any mutation:

| # | Check |
|---:|---|
| 1 | Wrong object type |
| 2 | Missing or invalid stable intervention identity |
| 3 | Duplicate stable identity (read-only preflight against the run's own history) |
| 4 | Foreign run lineage — an intervention naming run B is never usable on run A |
| 5 | Invalid human authority reference — kind must be `human` |
| 6 | Any other governed field mismatch the record model requires |

**Rule O-23 — human wins.** Where a human intervention races an automated continuation, the
intervention is recorded first and the continuation `BLOCK`s. A coordinator that raced a human
and won would be the clearest possible statement that human control is decorative.

**Rule O-24 — an administrator's ability is not authority.** Every human act on an execution
names the human, the reason, the scope of the act and its effect. The ability to perform an
action is not authority to authorise one.

## 10. The transactional shape of every governed act

> **construct → validate → preflight → commit**

**Rule O-25 — the atomicity invariant.** If an ordinary governed act fails, then phase, posture,
terminal state, Work Item counters, gate outcomes, governed record stores, and execution-event
history must remain **observationally identical** to their pre-call state.

**Rule O-26 — preflight parity.** A preflight must never be more permissive than the commit it
stands in for. Where a commit path tolerates "already in that state" as a no-op, its preflight
does too; where the commit path does not, the preflight must not either. A preflight looser than
its commit passes an act that then fails half-applied.

**Rule O-27 — no rollback-on-exception.** Recovery by catching an exception and undoing a
mutation is prohibited. Every fallible check precedes the first mutation.

Per-act read/validate/commit sets are specified in
`persistence-and-transaction-model.md` §7.

## 11. Compensation and non-replayable acts — Phase 14 §4.4

**Rule O-28.** Compensation is **a new governed act**, never a rollback of a completed external
act. There is no "undo" anywhere in this specification for anything that left the system.

An irreversible or non-retryable act is represented as a four-record lineage:

| # | Record | Contains |
|---:|---|---|
| 1 | **Intent record** | What is to be done, to which subject, under which Right, with which idempotency key. Written **before** any external call |
| 2 | **Authorisation record** | The Decision Record exercising the Right. `NOT NULL` before execution |
| 3 | **Execution record** | The attempt, its idempotency key, its outcome, and the observed external reference |
| 4 | **External-effect uncertainty state** | `NOT_ATTEMPTED` \| `ATTEMPTED_OUTCOME_UNKNOWN` \| `CONFIRMED_APPLIED` \| `CONFIRMED_NOT_APPLIED` |

**Rule O-29 — uncertainty is a state, not a gap.** Where the external call was made and the
local commit certainty is unknown, the state is `ATTEMPTED_OUTCOME_UNKNOWN`. The run does **not**
retry, does **not** assume failure, and does **not** assume success. It enters reconciliation
(`failure-recovery-race-model.md` §6).

**Rule O-30 — the compensation lineage.** Compensating a confirmed external effect requires its
own: compensation **request** → compensation **authorisation** (a Decision Record under a Right
whose declared subject covers the compensating act) → compensation **execution** record. The
original act's records are retained unchanged; compensation links to them and supersedes
nothing.

## 12. The `SUPERSEDED` path — Phase 14 §4.5

**Rule O-31 — supersession is never destructive.** In every case below the superseded object
remains intact and readable, and a link records what replaced it.

| Object | Superseded by | Retained |
|---|---|---|
| Workflow Run | A new run created under a supersession decision; the prior reaches terminal `SUPERSEDED` | All records, events, gates and evidence of the prior run |
| Knowledge item version | A later promoted version | Content, evidence links, conflict flags |
| Canonical Record | A new canonical version for the same `(subject_key, scope_path)` | The prior record, marked `SUPERSEDED` |
| Artifact version | A new artifact version | Prior bytes and prior record; **no canonical history is rewritten** |
| Registry definition version | A new committed version | Git history, not rewritten on an approval-bearing branch |
| Orchestrator / Routing Policy version | A new version | The prior, referenced by historical records at its version |
| Decision Record | **Never superseded by amendment.** A new Decision Record links via element 16 | The prior record, permanently |
| Approval state record | A new approval-state record | The prior, with `superseded_by` |

**Rule O-32.** A run reaching terminal `SUPERSEDED` requires a recorded governed act naming the
superseding run. A run does not become superseded by the mere existence of a newer run.

## 13. Execution events — coordination history, never governance evidence

Specified in full in `audit-provenance-observability.md` §3. Stated here because it is an
orchestrator obligation:

**Rule O-33.** The orchestrator **writes** execution events and **never reads them on a governed
path**. No gate satisfaction, decision validation, evidence lookup, promotion precondition or
authority check may read the execution event store. Corroboration is always against typed
governed records.

## 14. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `ExecutionEvent` has 5 fields and is documented as "Governance evidence" | The 13-field contract, explicitly **not** governance evidence | Phase 11 `execution-audit-and-provenance.md` §1–2; Phase 13 M-2 |
| D2 | `REWORK_REQUIRED` exists as a phase with no loop identity, iteration counter or retained iteration instances | §7 in full | Phase 11 `scheduling-and-dependency-model.md` §3; Phase 14 §4.1 |
| D3 | Compensation named, not represented | §11 four-record lineage | Phase 11 retry class 6; Phase 14 §4.4 |
| D4 | `SUPERSEDED` in the state model, not exercised | §12 | Phase 14 §4.5 |
| D5 | Append-only uniqueness held in process memory | Durable uniqueness | Phase 14 §4.2 |
