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

`Auth` column:

| Class | Means |
|---|---|
| `H` | Requires a human **Decision Record** under a mapped Decision Right |
| `R` | Requires an **eligible Role's** recorded professional conclusion, checked by review. **Not** an exercise of authority and **not** a Decision Right |
| `h` | Requires a human identity, but no Right |
| `S` | System-initiated. No human authority, and none is synthesised |

`R` exists because Phase 8 draws a distinction this catalogue must not flatten: a Decision Right
may decide what the organisation *does* about something; it cannot decide what is *accurate*.

| Command | Auth | Preconditions (beyond the envelope) | Writes | Principal errors |
|---|---|---|---|---|
| `CreateWorkflowRun` | h | Intake checks 1–7 | Run, scope binding, events | `DEFINITION_NOT_RESOLVABLE`, `SCOPE_NOT_PERMITTED`, `SENSITIVITY_UNASSESSED`, `DANGLING_REFERENCE`, `DUPLICATE_TRIGGER` |
| `ActivateStage` | S | Halted guard; task in definition @v | Work Item, gate instances | `RUN_HALTED`, `TASK_NOT_IN_DEFINITION` |
| `AssignWorkItem` | S | Halted guard; role matches bound lineage; agent instance type | Assignment, attempt counter | `RUN_HALTED`, `ROLE_MISMATCH`, `IDENTITY_KIND_INVALID` |
| `RequestRouting` | S | Halted guard | Routing request | `RUN_HALTED` |
| `Route` | S | Halted guard; full Router-answer validation incl. six-part completeness | Request + decision + events, one transaction | `ROUTER_ANSWER_INVALID`, `ROUTER_IDENTITY_INVALID`, `REPRODUCIBILITY_SET_INCOMPLETE`, `NO_ELIGIBLE_MODEL`, `CANDIDATE_UNIVERSE_INCOMPLETE` |
| `InvokeModel` | S | Halted guard; decision is this run's recorded decision; outcome eligible | Invocation, result | `DECISION_NOT_RECORDED`, `OUTCOME_NOT_ELIGIBLE`, `PROFILE_LINEAGE_MISMATCH` |
| `RequestReview` | S | Halted guard; gate is a `REVIEW` gate | Review request | `GATE_KIND_MISMATCH` |
| `SubmitReviewInstance` | h | Reviewer identity is human; independence class matches; SoD rules A-4; eligibility class covers the Profile | Review instance, gate outcome | `INDEPENDENCE_CLASS_MISMATCH`, `PRODUCER_REVIEW_PROHIBITED`, `BOUNDED_CONTRIBUTOR_CANNOT_SATISFY`, `INDEPENDENCE_DECLARATION_MISSING` |
| `RequestDecision` | S | Halted guard; gate is a `DECISION` gate; Right resolvable | Decision request | `RIGHT_NOT_RESOLVABLE`, `NO_APPLICABLE_DECISION_RIGHT` |
| `ExerciseDecisionRight` | H | The five gate-satisfaction conditions; 19-element completeness; separation compliance | Decision Record, gate outcome | `HOLDER_NOT_ELIGIBLE`, `CARDINALITY_UNSATISFIED`, `SEPARATION_VIOLATION`, `PREREQUISITE_UNSATISFIED`, `IDENTITY_KIND_INVALID` |
| `SupplyGateEvidence` | h | Evidence type matches the gate kind exactly | Evidence record, gate outcome | `EVIDENCE_TYPE_INADMISSIBLE`, `EVIDENCE_LINEAGE_MISMATCH` |
| `RecordIntervention` | h | The one intervention contract | Intervention | `INTERVENTION_INVALID`, `FOREIGN_RUN_LINEAGE`, `DUPLICATE_GOVERNED_IDENTITY` |
| `PauseRun` / `ResumeRun` | h | Intervention contract; transition preflight | Intervention, phase | as above, `TRANSITION_NOT_APPROVED` |
| `UnblockRun` | h | The five `unblock` conditions | Intervention, phase, posture | `RUN_NOT_HALTED`, `GATE_STILL_STANDING` |
| `CancelRun` | h | Terminal reachability for `CANCELLED`; **the intervention contract**. A human act: the work is not wanted | Intervention, terminal state | `TERMINAL_NOT_REACHABLE`, `INTERVENTION_INVALID`, `FOREIGN_RUN_LINEAGE` |
| `TerminateRun` | **S** | Terminal reachability for `TERMINATED`; **a named constraint** that continuing would breach. **No human intervention is required and none is synthesised** | Terminal state, constraint record | `TERMINAL_NOT_REACHABLE`, `CONSTRAINT_NOT_NAMED` |
| `FailRun` | S | Terminal reachability for `FAILED`; a recorded cause; no permitted retry or recovery resolved it | Terminal state | `TERMINAL_NOT_REACHABLE`, `CAUSE_NOT_RECORDED` |
| `Retry` | S | Retry class from bound lineage permits | Retry dispatch, or halt per O-20 | `RETRY_CLASS_FORBIDS` |
| `OpenSubRun` | S | Parent scope narrows to child scope | Child run | `SCOPE_WIDENING_REFUSED` |
| `TransferScope` | H | All source clauses **and** the full target-run preflight | Authorisation event, new run | `AUTHORISATION_NOT_CORROBORATED`, `MECHANISM_NOT_APPROVED`, `TARGET_PREFLIGHT_FAILED` |
| `CreateKnowledgeItem` | h | Four axes complete; type-specific requirements | Knowledge item v1 | `AXIS_INCOMPLETE`, `DERIVATION_REQUIRED`, `REASONING_REQUIRED` |
| `AdoptAISuggestion` | h | Creates a **new linked item**; never mutates the suggestion | New item, adoption link | `EPISTEMIC_CONVERSION_PROHIBITED` |
| `RaiseConflict` | S or h | — (raising needs no authority) | Conflict record | — |
| `ResolveConflict` | **R** | An eligible Role's conclusion with reasoning and residual uncertainty; a Review Instance checking it. **No Decision Right is required or invented** | Conflict resolution, conflict status | `ROLE_NOT_ELIGIBLE`, `REASONING_REQUIRED`, `RESIDUAL_UNCERTAINTY_REQUIRED`, `REVIEW_REQUIRED` |
| `ApplyConsequentStatusChange` | H | The separate governed act a resolution may lead to — supersession, retraction, or a canonical change. Requires its own mapped Right for that change | Status transition, links from the resolution | `NO_APPLICABLE_DECISION_RIGHT` where the change is a canonical one (BA-1) |
| `PromoteToCanonical` | H | Preconditions 1–9 | — | **Always `NO_APPLICABLE_DECISION_RIGHT`** until the Right is mapped (BA-1) |
| `CompleteRun` (COMPLETED / COMPLETED_WITH_OPEN_ITEMS) | S | Posture permits; no unsatisfied gate; phase permits | Terminal state | `POSTURE_FORBIDS_COMPLETION`, `GATES_UNSATISFIED` |
| `ReparentScopeNode` | H | — | — | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-2) |
| `DestroyGovernedContent` | H | — | — | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-3) |
| `ApplyDestructiveMigration` | H | — | — | **Always `NO_APPLICABLE_DECISION_RIGHT`** (BA-4) |
| `RecordApprovalState` | H | Source approval record resolvable; approving authority is human | Approval state record | `APPROVAL_SOURCE_UNRESOLVABLE` |

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
