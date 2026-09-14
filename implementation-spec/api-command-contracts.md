# API and Command Contracts

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

> **No executable API code, route handler, OpenAPI document or client SDK is created by this
> document.** Command shapes are written concretely because that is the precise way to say what
> the contract is.

## 1. Command / query separation

| | Commands | Queries |
|---|---|---|
| Effect | Change governed state | None |
| Shape | Named governed act | Named read |
| Idempotency | **Required** — every command carries a key | Not applicable |
| Audit | One audit event per governed write | None |
| May infer authority | **Never** | **Never** |

**Rule Q-1.** A query never changes governed state, including "read and mark as seen". Anything
that marks is a command.

**Rule Q-2.** A command is named for the **governed act**, not for the table it writes.
`ExerciseDecisionRight` is a command; `UpdateGateRow` is not, and would be a way to reach a gate
outcome without going through the act that governs it.

## 2. The rule that governs every command

**Rule Q-3 — authentication is not authority.** An authenticated caller has proved *who they
are*. Nothing about a governed act follows from that. Specifically, none of these makes a
command permissible:

- the caller is authenticated;
- the caller has an admin role, a service role, a database grant or an RLS exemption;
- the caller owns the workflow, the project or the tenant;
- the request carries a valid API key or a signed token;
- the caller is senior, or is the only person available;
- the request is urgent, or a deadline has passed;
- a model returned a high confidence value;
- a previous step completed successfully.

**Rule Q-4.** A command that requires human authority **carries a reference to a Decision Record
that already exists**, or it creates one through the single command that does so
(`ExerciseDecisionRight`), which itself requires an eligible human identity, a resolvable Right,
cardinality satisfaction and separation compliance. There is no third path and no bypass
parameter.

## 3. Command envelope

Every command carries the same envelope. A missing field is a rejection, not a default.

| Field | Null | Notes |
|---|---|---|
| `command_name` | NO | From the catalogue in §5 |
| `idempotency_key` | NO | Caller-supplied, unique per intended act; see §6 |
| `actor_human_identity` | Conditional | Present iff a human initiated the act |
| `actor_system_identity` | NO | The service identity executing it. **Never merged with the above** |
| `scope_path` | NO | The scope the act is claimed to occur in; validated against the target's binding |
| `expected_record_version` | Conditional | Required for every command that updates a mutable governed row |
| `correlation_id` | NO | Operational only |
| `decision_chain_id` | Conditional | Required for every command in a governed decision chain |
| `payload` | NO | Command-specific |

**Rule Q-5.** `actor_human_identity` is never defaulted from the authenticated principal for a
governed act. A service calling on a schedule has **no** human identity, and a command requiring
one is refused rather than attributed to the service.

## 4. Preconditions are evaluated server-side, against stored state

**Rule Q-6.** Every precondition is evaluated against records the system holds, never against
objects the caller supplied. A caller may construct a plausible Decision Record, Routing
Decision, Review Instance or authorisation; it will not be found in the governed lineage and so
it satisfies nothing.

**Rule Q-7 — no caller-injected governed records.** There is **no** command anywhere in this
catalogue that accepts a fully-formed Routing Decision, Review Instance, Decision Record,
Canonical Record or Model Result from a caller and records it. Each of those is produced by the
component that owns the act, from a request the system itself issued.

## 5. Command catalogue

### 5.1 The canonical governed-command inventory

This table is **the** inventory of governed commands. It is owned by this document, parsed by
the validator, and it is what "the governed command set" means anywhere in this package.

The **Act** column is the load-bearing addition. It names the transaction contract in
`persistence-and-transaction-model.md` §7.2 that specifies how the command commits. The two sets
must be **exactly equal**: a command with no act has no commit contract and cannot be built; an
act with no command is a contract for something nothing calls. `—` means the command changes no
governed state and therefore has no transaction row; there are none in this table, because a
command that changes nothing is a query (§8).

Where two API names are one governed act, the Act column carries the same key for both and the
alias is explicit rather than implied.

`Auth` column:

| Class | Means |
|---|---|
| `H` | Requires a human **Decision Record** under a mapped Decision Right |
| `R` | Requires an **eligible Role's** recorded professional conclusion, checked by review. **Not** an exercise of authority and **not** a Decision Right |
| `h` | Requires a human identity, but no Right |
| `S` | System-initiated. No human authority, and none is synthesised |
| `N` | **No authority of any kind**, and either a human or the system may initiate. The envelope's ordinary actor fields apply: `actor_system_identity` always, `actor_human_identity` iff a human initiated. Raising a conflict flag is the case this exists for — Phase 8: *raising one requires no authority* |

`R` exists because Phase 8 draws a distinction this catalogue must not flatten: a Decision Right
may decide what the organisation *does* about something; it cannot decide what is *accurate*.

**Rule Q-3a — `H` is not a way of saying "important".** A command is `H` only where a **mapped**
Decision Right governs the act itself. A command that *records the outcome of* an act someone
else already authorised is not `H` merely because the act was authoritative — that conflation is
how a recording API becomes a way to manufacture approval (§5.3).

| # | Command | Auth | **Act** | Preconditions (beyond the envelope) | Governed writes | Principal errors |
|---:|---|---|---|---|---|---|
| 1 | `CreateWorkflowRun` | h | `create_run` | Intake checks 1–7 | Run, scope binding | `DEFINITION_NOT_RESOLVABLE`, `SCOPE_NOT_PERMITTED`, `SENSITIVITY_UNASSESSED`, `DANGLING_REFERENCE`, `DUPLICATE_TRIGGER` |
| 2 | `ActivateStage` | S | `activate_stage` | Halted guard; task in definition @v | Work Item, gate instances | `RUN_HALTED`, `TASK_NOT_IN_DEFINITION` |
| 3 | `AssignWorkItem` | S | `assign` | Halted guard; role matches bound lineage; agent instance type | Assignment, attempt counter | `RUN_HALTED`, `ROLE_MISMATCH`, `IDENTITY_KIND_INVALID` |
| 4 | `RequestRouting` | S | `request_routing` | Halted guard | Routing request | `RUN_HALTED` |
| 5 | `Route` | S | `route` | Halted guard; full Router-answer validation incl. six-part completeness | Routing request, Routing Decision | `ROUTER_ANSWER_INVALID`, `ROUTER_IDENTITY_INVALID`, `REPRODUCIBILITY_SET_INCOMPLETE`, `NO_ELIGIBLE_MODEL`, `CANDIDATE_UNIVERSE_INCOMPLETE` |
| 6 | `InvokeModel` | S | `invoke_model` | Halted guard; decision is this run's recorded decision; outcome eligible; five-element lineage equality; release-identity comparison | Model Invocation, Model Result | `DECISION_NOT_RECORDED`, `OUTCOME_NOT_ELIGIBLE`, `PROFILE_LINEAGE_MISMATCH`, `RELEASE_IDENTITY_DIVERGED` |
| 7 | `RequestReview` | S | `request_review` | Halted guard; gate is a `REVIEW` gate | Review request | `GATE_KIND_MISMATCH` |
| 8 | `SubmitReviewInstance` | h | `review_gate` | Reviewer identity is human; independence class matches; SoD rules A-4; eligibility class covers the Profile | Review Instance, gate outcome | `INDEPENDENCE_CLASS_MISMATCH`, `PRODUCER_REVIEW_PROHIBITED`, `BOUNDED_CONTRIBUTOR_CANNOT_SATISFY`, `INDEPENDENCE_DECLARATION_MISSING` |
| 9 | `RequestDecision` | S | `request_decision` | Halted guard; gate is a `DECISION` gate; Right resolvable | Decision request | `RIGHT_NOT_RESOLVABLE`, `NO_APPLICABLE_DECISION_RIGHT` |
| 10 | `ExerciseDecisionRight` | H | `decision_gate` | The five gate-satisfaction conditions; 19-element completeness; separation compliance | Decision Record, gate outcome | `HOLDER_NOT_ELIGIBLE`, `CARDINALITY_UNSATISFIED`, `SEPARATION_VIOLATION`, `PREREQUISITE_UNSATISFIED`, `IDENTITY_KIND_INVALID` |
| 11 | `SupplyGateEvidence` | h | `supply_gate_evidence` | Evidence type matches the gate kind exactly; evidence lineage names this gate instance | Evidence record, gate outcome | `EVIDENCE_TYPE_INADMISSIBLE`, `EVIDENCE_LINEAGE_MISMATCH` |
| 12 | `RecordIntervention` | h | `record_intervention` | The one intervention contract | Intervention | `INTERVENTION_INVALID`, `FOREIGN_RUN_LINEAGE`, `DUPLICATE_GOVERNED_IDENTITY` |
| 13 | `PauseRun` | h | `pause` | Intervention contract; transition preflight (`allow_noop=false`) | Intervention, run phase | as above, `TRANSITION_NOT_APPROVED` |
| 14 | `ResumeRun` | h | `resume` | Intervention contract; transition preflight from `PAUSED` | Intervention, run phase | as above, `TRANSITION_NOT_APPROVED` |
| 15 | `UnblockRun` | h | `unblock` | The five `unblock` conditions | Intervention, run phase, posture | `RUN_NOT_HALTED`, `GATE_STILL_STANDING` |
| 16 | `CancelRun` | h | `cancel_run` | Terminal reachability for `CANCELLED`; **the intervention contract**. A human act: the work is not wanted | Intervention, run terminal state | `TERMINAL_NOT_REACHABLE`, `INTERVENTION_INVALID`, `FOREIGN_RUN_LINEAGE` |
| 17 | `TerminateRun` | **S** | `terminate_run` | Terminal reachability for `TERMINATED`; **a named constraint** that continuing would breach. **No human intervention is accepted and none is synthesised** | Constraint stop record, run terminal state | `TERMINAL_NOT_REACHABLE`, `CONSTRAINT_NOT_NAMED`, `UNEXPECTED_HUMAN_INTERVENTION`, `SYSTEM_IDENTITY_MISSING` |
| 18 | `FailRun` | S | `fail_run` | Terminal reachability for `FAILED`; a recorded cause; no permitted retry or recovery resolved it | Failure record, run terminal state | `TERMINAL_NOT_REACHABLE`, `CAUSE_NOT_RECORDED` |
| 19 | `SupersedeRun` | S | `supersede_run` | Terminal reachability for `SUPERSEDED`; the superseding run exists and names this one | Run terminal state, supersession link | `TERMINAL_NOT_REACHABLE`, `SUPERSEDING_RUN_NOT_FOUND` |
| 20 | `CompleteRun` | S | `complete_run` | Posture permits; no unsatisfied gate; phase permits. Covers `COMPLETED` and `COMPLETED_WITH_OPEN_ITEMS` | Run terminal state | `POSTURE_FORBIDS_COMPLETION`, `GATES_UNSATISFIED` |
| 21 | `Retry` | S | `retry` | Retry class from bound lineage permits; class-4 and class-6 halt per O-20 | Retry attempt record, run phase | `RETRY_CLASS_FORBIDS` |
| 22 | `OpenReworkIteration` | S | `rework_iteration` | Entry condition met; `max_iterations` not exhausted | Rework loop instance, Work Items, gate instances | `REWORK_ENTRY_CONDITION_UNMET`, `MAX_ITERATIONS_EXHAUSTED` |
| 23 | `OpenSubRun` | S | `open_sub_run` | Parent scope narrows to child scope | Child run, child scope binding | `SCOPE_WIDENING_REFUSED` |
| 24 | `TransferScope` | H | `scope_transfer` | All source clauses **and** the full target-run preflight | Authorisation record, target run, target scope binding, provenance link | `AUTHORISATION_NOT_CORROBORATED`, `MECHANISM_NOT_APPROVED`, `TARGET_PREFLIGHT_FAILED` |
| 25 | `CreateKnowledgeItem` | h | `create_knowledge_item` | Four axes complete; type-specific requirements | Knowledge item v1 | `AXIS_INCOMPLETE`, `DERIVATION_REQUIRED`, `REASONING_REQUIRED` |
| 26 | `AdoptAISuggestion` | h | `adopt_ai_suggestion` | Creates a **new linked item**; never mutates the suggestion; the adoption link does not count as evidence | New knowledge item, adoption link, suggestion governance state | `EPISTEMIC_CONVERSION_PROHIBITED`, `ADOPTION_IS_NOT_EVIDENCE` |
| 27 | `RaiseConflict` | N | `raise_conflict` | — (raising needs no authority) | Conflict record, conflict flags on the items | — |
| 28 | `ResolveConflict` | **R** | `resolve_conflict` | An eligible Role's conclusion with reasoning and residual uncertainty; a Review Instance checking it. **No Decision Right is required or invented** | Conflict resolution, conflict status | `ROLE_NOT_ELIGIBLE`, `REASONING_REQUIRED`, `RESIDUAL_UNCERTAINTY_REQUIRED`, `REVIEW_REQUIRED` |
| 29 | `ApplyConsequentStatusChange` | H | `apply_consequent_status_change` | The separate governed act a resolution may lead to — supersession, retraction, or a canonical change. Requires its own mapped Right for that change | Knowledge/canonical status transition, link from the resolution | `NO_APPLICABLE_DECISION_RIGHT` where the change is a canonical one (BA-1) |
| 30 | `TranscribeApprovalState` | **h** | `transcribe_approval_state` | §5.3. A mechanical transcription of an **already-existing** authoritative human approval record. **Creates no approval and exercises no Right** | Approval-state history row, current pointer | `APPROVAL_SOURCE_UNRESOLVABLE`, `APPROVAL_SOURCE_MISSING`, `TRANSCRIPTION_NOT_MECHANICAL` |
| 31 | `RecordNewApprovalState` | **H** | `record_new_approval_state` | §5.3. Persists the result of a **new** governed approval, revocation or supersession act that has already satisfied its Decision Right semantics | Approval-state history row, current pointer | `DECISION_RECORD_REQUIRED`, `NO_APPLICABLE_DECISION_RIGHT`, `APPROVAL_SOURCE_UNRESOLVABLE` |
| 32 | `PromoteToCanonical` | H | `promote_to_canonical` | Preconditions 1–9 | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** until the Right is mapped (BA-1) |
| 33 | `ReparentScopeNode` | H | `reparent_scope_node` | — | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-2) |
| 34 | `DestroyGovernedContent` | H | `destroy_governed_content` | — | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-3) |
| 35 | `ApplyDestructiveMigration` | H | `apply_destructive_migration` | — | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-4) |

**Rule Q-7a — the two sets are equal by construction and by check.** Every Act key above appears
exactly once as a transaction-contract row, and every transaction-contract row appears at least
once here. The validator derives both sets and compares them; an omission on either side is a
failure, not a documentation gap. Duplicate coverage is permitted **only** through an explicit
alias — the same Act key on two command rows — and there are currently none.

### 5.2 What `RecordApprovalState` was, and why it is now two commands

An earlier revision had one command, `RecordApprovalState`, class `H`. That was contradictory in
a way that mattered: class `H` asserts a mapped Decision Right governs the act, while the
approval registry says transcription **creates no approval** and that a historical source may
legitimately carry no Right or Decision Record at all. One command cannot be both.

Worse, the conflation pointed the wrong way. If recording *is* an `H` act, then whoever can call
the recording API is exercising authority — which is exactly how a service account becomes a way
to manufacture approval.

### 5.3 The two approval acts

| | `TranscribeApprovalState` | `RecordNewApprovalState` |
|---|---|---|
| **Purpose** | Transcribe an already-existing authoritative human approval record into machine-readable form | Persist the result of a **new** governed approval, revocation or supersession act |
| **Auth class** | `h` — a human runs a bounded transcription; **no Right is exercised** | `H` — the underlying act was governed by a mapped Right |
| **Creates approval?** | **No.** It records a decision a human already made | **No.** It records a decision a human already made |
| **Source record** | **Mandatory and verifiable** — path plus commit, and it must resolve at that commit | **Mandatory and verifiable** |
| `decision_right_ref` / `decision_record_ref` | **Nullable**, exactly where the authoritative historical source did not record them | **`NOT NULL`** where the governed act required a Right; the Decision Record must resolve |
| **Scope of use** | The bounded bootstrap of §9, and later transcription of an approval record created outside the runtime | Ordinary runtime operation after a governed approval act |
| **On no source record** | **Fail closed**: the subject stays `PROPOSED` / not approved | Fail closed, the same way |

**Rule Q-14 — neither command creates approval, and no caller can make one do so.** Both persist
a decision a human already made and recorded elsewhere. Specifically:

1. Neither command accepts an approval status the source record does not state.
2. Neither accepts a `decision_record_ref` that does not resolve to a real Decision Record whose
   `decided_by` is a human.
3. `TranscribeApprovalState` is **mechanical**: every field it writes is derived from the source
   record, and a field with no counterpart in the source is a refusal
   (`TRANSCRIPTION_NOT_MECHANICAL`), not a blank to fill in.
4. Being authenticated, being an administrator, holding a service role, or owning the database
   confers no ability to call either command into producing an approval — because neither
   command has a parameter through which a decision could be supplied that a source record does
   not already contain.

**Rule Q-15 — the bootstrap is a bounded, reviewable process, not a standing privilege.** The
transcription of the existing `reviews/phase-*-final-approval.md` records is a **one-off,
enumerated, reviewed** migration described in `approval-state-registry.md` §9 and
`migrations-versioning-compatibility.md` §9. It is not a runtime capability that remains
available afterwards, and it creates no row for a subject its source record does not name.

**Rule Q-9a — `CancelRun` and `TerminateRun` are different acts and do not share a contract.**
Phase 11 `orchestration/state-machine-and-transitions.md` §3 defines `CANCELLED` as *stopped
before completion by a human act; the work is not wanted*, requiring **an intervention record**;
and `TERMINATED` as *stopped by the system because continuing would breach a constraint*,
requiring **a named constraint**. An earlier revision of this catalogue collapsed them and
required a human identity for both, which would either block a required termination or fabricate
human provenance for a machine act. Both outcomes are worse than the bug.

On `TerminateRun` the envelope's `actor_human_identity` is **absent**, and Rule Q-5 forbids
defaulting it from the authenticated principal. The acting `actor_system_identity`, the named
constraint, and the execution and audit records carry the provenance. Terminal semantics are
identical in both cases: immutable, no outgoing transition, and re-examination only by a new run
that names this one.

**Rule Q-8 — the four blocked commands exist and always refuse.** They are specified, their
enforcement hook is built, and every call returns `NO_APPLICABLE_DECISION_RIGHT` with the gap
recorded. They are not omitted (which would leave an undefined behaviour), not stubbed to
succeed, and not made configurable.

**Rule Q-8a — what a blocked command writes, exactly.**

| | Count |
|---|---|
| Governed record writes | **0** |
| Audit events | **0** — an audit event records a mutation, and there is none (Rule P-14e) |
| Execution events | **1** — class `GATE_OUTCOME_RECORDED`, recording the act requested, the constraint class, **each Right considered and why it does not reach**, and the specific gap |
| Run state change | None. A refusal is not a transition; where the *caller's* act was a governed stage, the halted guard governs what happens next |

The single execution event is the whole trace of the refusal, and it is coordination history —
not evidence that anything was authorised, and not evidence that it was not.

**Rule Q-8b — a refused transaction of any kind writes no audit event.** This is general, not
special to the blocked four: an audit event is the record of a mutation, so a transaction that
mutates nothing produces none. `audit-provenance-observability.md` Rule V-6c says the same thing
from the audit side.

## 6. Idempotency

**Rule Q-9.** Every command carries a caller-supplied `idempotency_key` scoped to
`(command_name, scope_path, governed_subject)`.

| Situation | Behaviour |
|---|---|
| First call | Executes; the key and the resulting governed identity are recorded |
| Exact repeat, same payload hash | Returns the **original** result. No second act |
| Repeat, **different** payload hash | `IDEMPOTENCY_KEY_CONFLICT`. **Nothing is executed** |
| Repeat while the first is in flight | `IN_PROGRESS`; the caller retries the read, not the act |
| Repeat of a class-4 governed act | The durable uniqueness constraint refuses; `DUPLICATE_GOVERNED_IDENTITY` |

**Rule Q-10.** Idempotency is **at-most-once at the API boundary**, and never a claim of
exactly-once delivery end to end.

## 7. Error contract

Errors are a governed vocabulary, not free text. Each error names what was refused and why, and
**never** suggests a way around it.

| Class | Meaning | HTTP-equivalent |
|---|---|---|
| `VALIDATION_ERROR` | The request is malformed | 400 |
| `IDENTITY_KIND_INVALID` | A reference of the wrong kind was supplied | 400 |
| `PRECONDITION_UNSATISFIED` | A governed precondition does not hold | 409 |
| `RUN_HALTED` | The run is terminal, blocked, escalated, or authority-absent | 409 |
| `STALE_WRITE` | `expected_record_version` did not match | 409 |
| `DUPLICATE_GOVERNED_IDENTITY` | A governed identity already exists | 409 |
| `IDEMPOTENCY_KEY_CONFLICT` | The key was reused with a different payload | 409 |
| `NO_APPLICABLE_DECISION_RIGHT` | No approved Right covers the act | 409, **never 403** |
| `SEPARATION_VIOLATION` | A `SEPARATION_REQUIRED` relationship is active and would be breached | 409 |
| `EVIDENCE_TYPE_INADMISSIBLE` | Evidence of the wrong kind for the gate | 409 |
| `SCOPE_WIDENING_REFUSED` | The act would widen scope, sensitivity or residency | 409 |
| `CONSTRAINT_NOT_NAMED` | A termination did not name the constraint that continuing would breach | 409 |
| `ROLE_NOT_ELIGIBLE` | The concluding Role's approved scope does not cover the conclusion | 409 |
| `RELEASE_IDENTITY_DIVERGED` | The observed originator release differs from the one the Routing Decision recorded | 409 |
| `AUTHORIZATION_DENIED` | The caller may not **reach** this resource | 403 |

**Rule Q-11 — `NO_APPLICABLE_DECISION_RIGHT` is not `403`.** They are different facts.
`403` says *you* may not do this; `NO_APPLICABLE_DECISION_RIGHT` says **nobody** may, because no
approved Right covers the act. Collapsing them invites someone to fix a governance gap by
granting a permission.

**Rule Q-12 — no remediation hints.** An error never says "retry with force", "use the admin
endpoint" or "set `skip_checks=true`". Those parameters do not exist, so there is nothing to
hint at.

## 8. Query surface

| Query | Returns | Note |
|---|---|---|
| `GetRunState` | The four axes, gates, open items | Never an inferred approval |
| `ListGovernedRecords` | Records by scope, subject, version | Recorded values only |
| `ResolveApplicable` | The applicable canonical record for a subject in a scope | Returns **"no position"** where an ancestor-fallback determination is absent (S-12) |
| `ReconstructRoutingDecision` | The full six-part set as recorded | **Never re-resolved against the registry as it stands today** |
| `GetApprovalState` | The machine-readable approval state | The approval oracle, not prose |
| `ExplainGateStatus` | Which conditions hold and which do not | A diagnostic; satisfies nothing |

**Rule Q-13.** `ExplainGateStatus` returns *why a gate is unsatisfied*. It is a diagnostic and
never a step toward satisfaction: nothing about calling it changes a gate.

## 9. Divergence note

The Phase 12 reference implementation exposes governed acts as Python methods on one
orchestrator object with no envelope, no idempotency key and no separated actor identities. This
document specifies the production boundary; the reference demonstrates the semantics those
commands must preserve.
