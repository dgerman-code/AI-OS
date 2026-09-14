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
| 4 | `Route` | S | `route` | Halted guard; full Router-answer validation incl. six-part completeness. **The only command that makes a Routing Request durable** (§5.4) | Routing Request (first submission only), Routing Decision | `ROUTER_ANSWER_INVALID`, `ROUTER_IDENTITY_INVALID`, `REPRODUCIBILITY_SET_INCOMPLETE`, `ROUTING_REQUEST_IDENTITY_MISMATCH` |
| 5 | `InvokeModel` | S | `invoke_model` | Halted guard; decision is this run's recorded decision; outcome eligible. **Stages an external effect — it is not one local transaction** (§5.5) | Invocation intent + outbox row. The provider attempt and the Model Result are later, separate commits | `DECISION_NOT_RECORDED`, `OUTCOME_NOT_ELIGIBLE` |
| 6 | `RecordProviderAttemptOutcome` | S | `record_provider_attempt_outcome` | §5.5 stage 3–4. Records what the gateway observed: a response, a refusal, a timeout, or nothing at all | Provider attempt outcome, and on a response the Model Result | `PROFILE_LINEAGE_MISMATCH`, `RELEASE_IDENTITY_DIVERGED`, `ATTEMPT_NOT_STAGED` |
| 7 | `ReconcileExternalEffect` | S | `reconcile_external_effect` | §5.5 stage 5. Resolves an `ATTEMPTED_OUTCOME_UNKNOWN` attempt by querying the external system under its idempotency key | Attempt uncertainty resolution, and on a confirmed applied effect the Model Result | `EFFECT_STILL_UNKNOWN`, `ATTEMPT_NOT_UNCERTAIN` |
| 8 | `RequestReview` | S | `request_review` | Halted guard; gate is a `REVIEW` gate | Review request | `GATE_KIND_MISMATCH` |
| 9 | `SubmitReviewInstance` | h | `review_gate` | Reviewer identity is human; independence class matches; SoD rules A-4; eligibility class covers the Profile | Review Instance, gate outcome | `INDEPENDENCE_CLASS_MISMATCH`, `PRODUCER_REVIEW_PROHIBITED`, `BOUNDED_CONTRIBUTOR_CANNOT_SATISFY`, `INDEPENDENCE_DECLARATION_MISSING` |
| 10 | `RequestDecision` | S | `request_decision` | Halted guard; gate is a `DECISION` gate; Right resolvable | Decision request | `RIGHT_NOT_RESOLVABLE`, `NO_APPLICABLE_DECISION_RIGHT` |
| 11 | `ExerciseDecisionRight` | H | `decision_gate` | The five gate-satisfaction conditions; 19-element completeness; separation compliance | Decision Record, gate outcome | `HOLDER_NOT_ELIGIBLE`, `CARDINALITY_UNSATISFIED`, `SEPARATION_VIOLATION`, `PREREQUISITE_UNSATISFIED`, `IDENTITY_KIND_INVALID` |
| 12 | `SupplyGateEvidence` | h | `supply_gate_evidence` | Evidence type matches the gate kind exactly; evidence lineage names this gate instance | Evidence record, gate outcome | `EVIDENCE_TYPE_INADMISSIBLE`, `EVIDENCE_LINEAGE_MISMATCH` |
| 13 | `RecordIntervention` | h | `record_intervention` | The one intervention contract | Intervention | `INTERVENTION_INVALID`, `FOREIGN_RUN_LINEAGE`, `DUPLICATE_GOVERNED_IDENTITY` |
| 14 | `PauseRun` | h | `pause` | Intervention contract; transition preflight (`allow_noop=false`) | Intervention, run phase | as above, `TRANSITION_NOT_APPROVED` |
| 15 | `ResumeRun` | h | `resume` | Intervention contract; transition preflight from `PAUSED` | Intervention, run phase | as above, `TRANSITION_NOT_APPROVED` |
| 16 | `UnblockRun` | h | `unblock` | The five `unblock` conditions | Intervention, run phase, posture | `RUN_NOT_HALTED`, `GATE_STILL_STANDING` |
| 17 | `CancelRun` | h | `cancel_run` | Terminal reachability for `CANCELLED`; **the intervention contract**. A human act: the work is not wanted | Intervention, run terminal state | `TERMINAL_NOT_REACHABLE`, `INTERVENTION_INVALID`, `FOREIGN_RUN_LINEAGE` |
| 18 | `TerminateRun` | **S** | `terminate_run` | Terminal reachability for `TERMINATED`; **a named constraint** that continuing would breach. **No human intervention is accepted and none is synthesised** | Constraint stop record, run terminal state | `TERMINAL_NOT_REACHABLE`, `CONSTRAINT_NOT_NAMED`, `UNEXPECTED_HUMAN_INTERVENTION`, `SYSTEM_IDENTITY_MISSING` |
| 19 | `FailRun` | S | `fail_run` | Terminal reachability for `FAILED`; a recorded cause; no permitted retry or recovery resolved it | Failure record, run terminal state | `TERMINAL_NOT_REACHABLE`, `CAUSE_NOT_RECORDED` |
| 20 | `SupersedeRun` | S | `supersede_run` | Terminal reachability for `SUPERSEDED`; the superseding run exists and names this one | Run terminal state, supersession link | `TERMINAL_NOT_REACHABLE`, `SUPERSEDING_RUN_NOT_FOUND` |
| 21 | `CompleteRun` | S | `complete_run` | Posture permits; no unsatisfied gate; phase permits. Covers `COMPLETED` and `COMPLETED_WITH_OPEN_ITEMS` | Run terminal state | `POSTURE_FORBIDS_COMPLETION`, `GATES_UNSATISFIED` |
| 22 | `Retry` | S | `retry` | The retry class comes from the Work Item's bound lineage. **Every class has a defined branch and none of them writes nothing** (§5.6) | Branch-dependent: a retry dispatch record, or a refusal record with a block and an escalation | `RETRY_CLASS_FORBIDS`, `ACKNOWLEDGEMENT_REQUIRED`, `EXTERNAL_EFFECT_UNKNOWN` |
| 23 | `OpenReworkIteration` | S | `rework_iteration` | Entry condition met; `max_iterations` not exhausted | Rework loop instance, Work Items, gate instances | `REWORK_ENTRY_CONDITION_UNMET`, `MAX_ITERATIONS_EXHAUSTED` |
| 24 | `OpenSubRun` | S | `open_sub_run` | Parent scope narrows to child scope | Child run, child scope binding | `SCOPE_WIDENING_REFUSED` |
| 25 | `TransferScope` | H | `scope_transfer` | All source clauses **and** the full target-run preflight | Authorisation record, target run, target scope binding, provenance link | `AUTHORISATION_NOT_CORROBORATED`, `MECHANISM_NOT_APPROVED`, `TARGET_PREFLIGHT_FAILED` |
| 26 | `CreateKnowledgeItem` | h | `create_knowledge_item` | Four axes complete; type-specific requirements | Knowledge item v1 | `AXIS_INCOMPLETE`, `DERIVATION_REQUIRED`, `REASONING_REQUIRED` |
| 27 | `AdoptAISuggestion` | h | `adopt_ai_suggestion` | Creates a **new linked item**; never mutates the suggestion; the adoption link does not count as evidence | New knowledge item, adoption link, suggestion governance state | `EPISTEMIC_CONVERSION_PROHIBITED`, `ADOPTION_IS_NOT_EVIDENCE` |
| 28 | `RaiseConflict` | N | `raise_conflict` | — (raising needs no authority) | Conflict record, conflict flags on the items | — |
| 29 | `ResolveConflict` | **R** | `resolve_conflict` | An eligible Role's conclusion with reasoning and residual uncertainty; a Review Instance checking it. **No Decision Right is required or invented** | Conflict resolution, conflict status | `ROLE_NOT_ELIGIBLE`, `REASONING_REQUIRED`, `RESIDUAL_UNCERTAINTY_REQUIRED`, `REVIEW_REQUIRED` |
| 30 | `ApplyConsequentStatusChange` | H | `apply_consequent_status_change` | The separate governed act a resolution may lead to — supersession, retraction, or a canonical change. Requires its own mapped Right for that change | Knowledge/canonical status transition, link from the resolution | `NO_APPLICABLE_DECISION_RIGHT` where the change is a canonical one (BA-1) |
| 31 | `TranscribeApprovalState` | **h** | `transcribe_approval_state` | §5.3. A mechanical transcription of an **already-existing** authoritative human approval record. **Creates no approval and exercises no Right** | Approval-state history row, current pointer | `APPROVAL_SOURCE_UNRESOLVABLE`, `APPROVAL_SOURCE_MISSING`, `TRANSCRIPTION_NOT_MECHANICAL` |
| 32 | `RecordNewApprovalState` | **H** | `record_new_approval_state` | §5.3. Persists the result of a **new** governed approval, revocation or supersession act that has already satisfied its Decision Right semantics | Approval-state history row, current pointer | `DECISION_RECORD_REQUIRED`, `NO_APPLICABLE_DECISION_RIGHT`, `APPROVAL_SOURCE_UNRESOLVABLE` |
| 33 | `PromoteToCanonical` | H | `promote_to_canonical` | Preconditions 1–9 | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** until the Right is mapped (BA-1) |
| 34 | `ReparentScopeNode` | H | `reparent_scope_node` | — | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-2) |
| 35 | `DestroyGovernedContent` | H | `destroy_governed_content` | — | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-3) |
| 36 | `ApplyDestructiveMigration` | H | `apply_destructive_migration` | — | **None — zero governed writes** | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-4) |

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

### 5.4 The Routing Request lifecycle — one contract

Three earlier statements were incompatible: a `RequestRouting` command that persisted a request
independently, a `route()` that also wrote the request with the decision, and Rule M-13 saying
the request stays prospective until the answer validates. This is the single lifecycle, and
every document encodes it.

**Rule Q-16 — the Routing Request becomes durable only inside a validated routing act.**
`RequestRouting` no longer exists as a governed command. The prospective envelope is constructed
**inside** `route()`, carries a reserved stable identity, and reaches storage only in the same
transaction as the Router's answer.

The basis is Phase 11 `orchestration/model-router-invocation-boundary.md`: §4 records the
**Model Invocation Request ID** as a *runtime* identity and the **Routing Decision** as the
governed recorded value, and §3 says "A Routing Decision, **or a refusal. Both are recorded**".
Phase 10's `routing` data domain lists Routing Decisions, candidate universe bindings,
per-candidate results and the reproducibility set — and no independently persisted request.

| Stage | What exists | Durable? |
|---|---|---|
| 1. `route()` constructs the envelope | A prospective Routing Request with a reserved identity | **No** |
| 2. The configured Router is asked, with that exact object | — | **No** |
| 3. The answer is validated: type, request identity, run and Work Item binding, Router identity, six-part completeness for a selection | — | **No** |
| 4. Commit | Request **and** answer, in one transaction | **Yes** |

**Rule Q-17 — the four branches, exactly.**

| Branch | Router answer | Governed writes | Audit | Exec | Run effect |
|---|---|---|---|---|---|
| **B1 invalid** | Malformed, wrong request identity, foreign Router, or an incomplete six-part set on a selection | **0 — no request, no decision** | **0** | 1 (refusal) | None. Full observational equality |
| **B2 selection, first submission** | `ELIGIBLE_CANDIDATE` | `routing_request`, `routing_decision` | **2** | 2 | Continue |
| **B3 non-selection, first submission** | `NO_ELIGIBLE_MODEL`, `CANDIDATE_UNIVERSE_INCOMPLETE`, `NO_APPLICABLE_DECISION_RIGHT`, `ACT_REQUIREMENT_OUTSTANDING` | `routing_request`, `routing_decision` | **2** | 2 | `BLOCKED`, `BLOCKED`+`ESCALATED`, or `WAITING`, per the outcome |
| **B4 re-submission** | Any valid answer to an **already durable** request | `routing_decision` only | **1** | 1 | Per the outcome |

**Rule Q-18 — a valid refusal is recorded; an invalid answer is not.** B3 records because Phase
11 §3 says the refusals are the important half: *why* a run blocked for routing is a governed
fact, and a blocked run whose reason was never written is indistinguishable from a stall. B1
records nothing because a malformed answer is not a refusal — it is the absence of an answer, and
committing a request for it would leave a decision-shaped artifact no decision answers.

**Rule Q-19 — a retry re-submits the same request.** Phase 11 §5 rule 1. The request identity is
stable across submissions; each submission's answer is a **new** Routing Decision carrying a
`submission_ordinal`, and **every attempt's decision is recorded** (§5 rule 3), because a
diversity check evaluates against the decision that produced the artifact under review, not the
last attempt that happened to run. Uniqueness is therefore
`UNIQUE (routing_request_ref, submission_ordinal)` — **not** one decision per request.

**Rule Q-20 — idempotency.** The envelope's `idempotency_key` is scoped to
`(route, run_ref, work_item_ref, submission_ordinal)`. A repeat under the same key returns the
original decision and performs no second Router call; a repeat with a different payload is
`IDEMPOTENCY_KEY_CONFLICT` and nothing executes.

**Rule Q-21 — no caller injection path survives this.** The envelope is constructed inside
`route()` from the run's own bound lineage. There is no command that accepts a Routing Request
from a caller, and none that accepts a Routing Decision at all.

### 5.5 Model invocation is an external effect, staged

**Rule Q-22 — `InvokeModel` is not one local transaction.** A model call leaves the system.
Phase 10 forbids pretending a local transaction spans an external system, and Phase 11 requires
an unknown external outcome to stop and reconcile rather than be assumed either way. The act is
therefore staged across **three commands and five stages**, with four distinct identities that
are never collapsed.

| Identity | Is | Created at |
|---|---|---|
| `ModelInvocationRef` — **invocation intent** | The governed intent to invoke, naming the recorded Routing Decision and the deployment it selected | Stage 1 |
| `ProviderAttemptRef` — **provider attempt** | One attempt to reach the provider, with its own idempotency key and its own external-effect state | Stage 1 (staged), resolved at 3 or 5 |
| `ModelResultRef` — **model result** | The content the provider returned, as `AI_SUGGESTION` / `AI_GENERATED` / `DRAFT` | Stage 4, **only** on a confirmed response |
| `ReconciliationRef` — **uncertainty resolution** | The determination of what actually happened to an attempt whose outcome was unknown | Stage 5 |

| # | Stage | Command | Transaction boundary | Governed writes | Audit | Exec |
|---:|---|---|---|---|---|---|
| 1 | **Local intent commit** | `InvokeModel` | One local transaction. **No provider call happens inside it** | `model_invocation` (intent), `provider_attempt` at `NOT_ATTEMPTED`, outbox row | **3** | 1 |
| 2 | **External provider call** | — (C16 drains the outbox; C8 calls) | **No transaction.** This is the part that is not transactional, stated rather than hidden | none | 0 | 0 |
| 3 | **Observed outcome** | `RecordProviderAttemptOutcome` | One local transaction | `provider_attempt` state → `CONFIRMED_APPLIED`, `CONFIRMED_NOT_APPLIED` or `ATTEMPTED_OUTCOME_UNKNOWN` | **1** | 1 |
| 4 | **Result recording** | `RecordProviderAttemptOutcome`, same transaction as 3, **only** where the outcome is `CONFIRMED_APPLIED` with content | `model_result` | **+1** (2 total) | 1 |
| 5 | **Reconciliation** | `ReconcileExternalEffect` | One local transaction | `reconciliation`, `provider_attempt` state, and `model_result` where the effect is confirmed applied with retrievable content | **2 or 3** | 1 |

**Rule Q-23 — a timeout is not proof that nothing happened.** A timeout, a connection reset, a
dropped response and a crash between stages 2 and 3 all produce
`ATTEMPTED_OUTCOME_UNKNOWN`. The system does **not** assume the call failed (and retry, risking a
duplicate external effect), and does **not** assume it succeeded. It enters stage 5. This is the
one rule in this section the whole staging exists for.

**Rule Q-24 — crash behaviour at every boundary.**

| Crash point | State on recovery | Recovery action |
|---|---|---|
| Before stage 1 commits | Nothing exists | None |
| After stage 1, before the call | Intent and attempt at `NOT_ATTEMPTED`, outbox row present | The drain retries the call under the **same idempotency key** — safe, because nothing left the system |
| During stage 2 | Attempt still `NOT_ATTEMPTED` locally, but the call **may have been made** | The drain must treat an attempt whose lease expired as `ATTEMPTED_OUTCOME_UNKNOWN`, not as `NOT_ATTEMPTED`. **This is the only place where an optimistic reading would produce a duplicate external effect** |
| After the call, before stage 3 commits | Attempt `ATTEMPTED_OUTCOME_UNKNOWN` | Stage 5 |
| After stage 3, before stage 4 | Outcome recorded, no result | Stage 4 completes idempotently under U7 |
| After stage 4 | Complete | None |

**Rule Q-25 — retry classes across the stages.** Stage 1 is `SAFE_AUTOMATIC_RETRY` — it is local
and writes nothing external. Stage 2 is `IDEMPOTENT_AT_LEAST_ONCE` **only** where the provider
deduplicates on the attempt's idempotency key, and `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT`
otherwise. Stages 3, 4 and 5 are `SAFE_AUTOMATIC_RETRY`. **No stage is class 4**, because model
invocation is not an authority-bearing act — which is exactly why its output is `AI_SUGGESTION`
and satisfies no gate.

**Rule Q-26 — no distributed transaction and no exactly-once.** The staging above is
at-most-once *locally* by U7 and U8, at-least-once *externally* where the provider deduplicates,
and neither where it does not. That is stated, not hidden behind a boundary that looks atomic.

**Rule Q-27 — compensation is never a retry.** Where a confirmed external effect must be undone,
that is the compensation lineage of `failure-recovery-race-model.md` §7 — its own request, its
own authorisation, its own execution — and it is never reached by re-running `InvokeModel`.

### 5.6 Retry, branch by branch

**Rule Q-28 — every retry class has a defined branch, and none of them writes nothing.** O-20
requires a forbidden retry to halt and escalate; an earlier transaction row said "Nothing
written", which cannot both be true. Halting and escalating **is** a write.

| Branch | Classes | Precondition | Phase/posture before → after | Governed writes | Audit | Exec | Dispatch record? | Escalation record? |
|---|---|---|---|---|---|---|---|---|
| **R1 automatic** | 1 `SAFE_AUTOMATIC_RETRY`, 5 `REPLAYABLE_READ_ONLY` | Halted guard; attempt limit not reached | `RETRY_PENDING` → `RUNNING`, posture unchanged | `retry_attempt`, run phase | **2** | 1 | **Yes** | No |
| **R2 revalidating** | 2 `RETRY_REQUIRING_REVALIDATION` | As R1, **plus** preconditions, evidence freshness, scope, sensitivity and assignment eligibility re-evaluated **before** dispatch | `RETRY_PENDING` → `RUNNING` | `revalidation_record`, `retry_attempt`, run phase | **3** | 2 | **Yes** | No |
| **R2f revalidation fails** | 2 | A re-evaluated precondition no longer holds | `RETRY_PENDING` → `BLOCKED` | `revalidation_record`, run phase | **2** | 1 | No | No — a block, not an escalation |
| **R3 awaiting acknowledgement** | 3 `RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT` | No acknowledgement intervention yet | `RETRY_PENDING` → `WAITING`, wait subject = the acknowledgement | `retry_hold_record`, run phase | **2** | 1 | No | No |
| **R3a acknowledged** | 3 | An intervention recording the acknowledgement exists | `WAITING` → `RUNNING` | `retry_attempt`, run phase | **2** | 1 | **Yes** | No |
| **R4 refused, non-retryable** | 4 `NON_RETRYABLE_GOVERNED_ACT` | The request is made at all | → `BLOCKED` → `ESCALATED`, posture `GATE_UNSATISFIED` | `retry_refusal_record`, run phase (block), run phase (escalate) | **3** | 2 | **No** | **Yes** |
| **R6 refused, external side effect** | 6 `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT` | The request is made at all | → `BLOCKED` → `ESCALATED`, posture `GATE_UNSATISFIED` | `retry_refusal_record` naming the external-effect state, run phase (block), run phase (escalate) | **3** | 2 | **No** | **Yes** |
| **R7 idempotent** | 7 `IDEMPOTENT_AT_LEAST_ONCE` | The step carries an idempotency key **and** the target deduplicates | `RETRY_PENDING` → `RUNNING` | `retry_attempt`, run phase | **2** | 1 | **Yes** | No |
| **RX unclassified** | none declared | A step with no declared class | → `BLOCKED` → `ESCALATED` | `retry_refusal_record`, run phase (block), run phase (escalate) | **3** | 2 | No | **Yes** |

**Rule Q-29 — the refusal is recorded, not merely returned.** R4, R6 and RX write a
`retry_refusal_record` naming the class, the act, and why no number of attempts produces what is
missing. A caller that receives `RETRY_CLASS_FORBIDS` and sees no state change would be looking
at a system that forgot it refused.

**Rule Q-30 — atomicity.** Each branch is **one transaction**: the record, the phase change and,
for R4/R6/RX, the escalation all commit together or not at all. A run that is `BLOCKED` without
its refusal record is not a state this specification permits.

**Rule Q-31 — the R6 branch never becomes a retry.** An `ATTEMPTED_OUTCOME_UNKNOWN` external
effect is reconciled (§5.5 stage 5), and if it must be undone it is compensated. Automatically
re-running it is the duplicate-irreversible-act failure the class exists to prevent.

**Rule Q-32 — duplicate retry requests.** `retry_attempt` carries
`UNIQUE (work_item_ref, attempt_ordinal)`; a duplicate request under the same ordinal is
`DUPLICATE_GOVERNED_IDENTITY` and executes nothing.

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
