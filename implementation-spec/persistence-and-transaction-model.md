# Persistence and Transaction Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 14 §4.2 (persistent uniqueness / at-most-once) and §7 (transactional rule).

> **No executable migration, DDL file, ORM model or connection configuration is created by this
> document.** Constraint shapes are written in SQL-like notation because that is the precise way
> to say what must hold; they are a specification, not a migration.

## 1. Three layers, three different jobs

| Layer | Authoritative for | Must never become |
|---|---|---|
| **Git** | Governed architecture, standards, templates, registry **definitions**, policies, schemas and migrations as source; human approval records; the architecture's own review and audit trail | The operational database. It answers what the system *is*, never what happened at 14:02 |
| **PostgreSQL** | Operational governance **records** and their relationships, lifecycle, lineage and queryable state | The architecture's source. A row asserting a Role's competence is a projection, not a definition |
| **Object storage** | The **bytes** of files and large artifacts, and their immutable snapshots | The artifact registry. It holds content; it knows nothing about what the content means |

**Rule P-1 — the record is authoritative for what should exist.** That is why a missing object is
detectable and an orphaned object is not adoptable, and it is why **the metadata commit comes
last and the metadata read comes first**.

## 2. Seven facets, separately recorded

A stored governed object carries seven things routinely confused with one another. Each is a
separate column or a separate table, and **none is derivable from another**.

| Facet | Column family | What it is not |
|---|---|---|
| Logical object identity | `*_ref` | Not the row, not the path, not the hash |
| Storage location | `storage_location` | Not identity — it changes without the object changing |
| Version identity | `*_version` | Not a timestamp, and not a commit |
| Content hash | `content_hash` + `hash_algorithm` | Not identity, and not authenticity of the claim the bytes make |
| Mutable metadata | `display_*`, `tags` | Not governed content |
| Immutable audit/history record | `audit_event` table | Not the object, and never rewritten with it |
| Runtime instance / event identity | Observability plane | Not the governed act |

**Rule P-2.** A backend that can assign, infer or overwrite the **logical identity**, the
**version identity** or the **audit record** is out of bounds. Where a hosted product offers such
a capability, it is disabled and the disabling is recorded.

## 3. Logical schema boundaries — ten data domains

| # | Domain | Holds | Write path | Discipline |
|---:|---|---|---|---|
| 1 | `governance` | Approval baselines, schema-compatibility declarations, configuration version records, legal holds, retention class definitions | Human decision, recorded | Append-only |
| 2 | `registry_projection` | Read-only projections of Git-sourced definitions at named versions | Definition sync | Replaceable projection; **never a source** |
| 3 | `execution` | Runs, Work Items, assignments, stage/status transitions, handoff records, rework loop instances | The acting identity via the governed path | Append-only transitions |
| 4 | `review` | Review requests, instances, findings, reviewer identity references, independence class references | The reviewing identity | Append-only findings |
| 5 | `decision` | Decision Records, Right exercise references, expiry and bounded-effect fields | An eligible human exercising a carded Right | **Append-only, never amended** |
| 6 | `knowledge` | Memory items, knowledge claims, canonical records, source and evidence metadata, conflict states | The governed promotion path | Append-only history with supersession |
| 7 | `routing` | Routing Requests, Routing Decisions, candidate universe bindings, per-candidate results, the six-part reproducibility set | The routing act | Append-only |
| 8 | `artifact` | Artifact records, storage location references, content hashes, retention class, hold flags, supersession links | The governed write path | Append-only versions |
| 9 | `audit` | Audit events, provenance records | The audit writer | Append-only, never deleted |
| 10 | `correlation` | Bounded runtime-event and correlation metadata | The emitting system | Append-only; **no governed record may cite this domain as a reason** |

**Rule P-3 — domain 10 is quarantined by design.** A foreign key from any governance table into
`correlation` is prohibited. Correlation metadata is not evidence and not a decision.

**Rule P-4 — domain 2 is a projection.** It may be dropped and rebuilt from Git at any time
without governance loss. Any query that would change a governed outcome if the projection were
stale must read the version recorded on the governed record instead.

## 4. Append-only, mechanically

**Rule P-5.** Where the backend can enforce append-only **structurally**, it must. Where it can
only enforce it by permission, **the limitation is recorded rather than assumed away** — an
architecture that claims immutability it cannot produce is worse than one that states the gap.

Enforcement ladder, strongest first:

| # | Mechanism | Use where |
|---:|---|---|
| 1 | No `UPDATE`/`DELETE` grant on the table for any application role; inserts only | Every append-only domain |
| 2 | A `BEFORE UPDATE OR DELETE` rule/trigger that raises | Belt and braces on domains 5, 6, 9 |
| 3 | Generated/immutable column constraints on `IMM` fields | All governed tables |
| 4 | Periodic verification that the grants still hold, recorded as an assurance result | All |

**Rule P-6 — the superuser gap, stated.** A database owner or migration role can bypass (1) and
(2). That capability is a **credential**, not authority (`security-identity-access.md` §6), and
its use is itself an auditable act. This specification does not claim the database can prevent
its owner from writing; it claims that doing so is detectable, attributable and prohibited.

## 5. Uniqueness and at-most-once — Phase 14 §4.2

### 5.1 Why this section exists

Phase 11's at-most-once guarantee for `NON_RETRYABLE_GOVERNED_ACT` is **not** achieved by the
orchestrator being careful. It is achieved because the act's existence is a governed fact in an
append-only store **with a uniqueness constraint**, so a blind replay produces a failed write
rather than a second approval. The Phase 12 reference held that constraint in process memory,
which does not survive a restart, a second process or a race. Production requires it in the
database.

### 5.2 Required durable uniqueness constraints — the canonical inventory

**This table is the canonical uniqueness inventory.** Every reference to "the uniqueness
constraints" anywhere in this package means these rows, and any document that states a count
states the count *of this table*. The validator derives the number from here and checks every
document that cites one, so a constraint added without updating a milestone fails rather than
drifting.

Each row is a `UNIQUE` constraint or unique index that **must exist** before the corresponding
act is implementable.

| # | Record | Constraint | Prevents |
|---:|---|---|---|
| U1 | Decision Record | `UNIQUE (decision_record_ref)` | A duplicate identity entering history |
| U2 | Decision Record | `UNIQUE (decision_right_ref, governed_subject, gate_instance_ref, decided_by)` | The same holder deciding the same gate twice under one Right |
| U3 | Review Instance | `UNIQUE (review_instance_ref)` | Duplicate identity |
| U4 | Review Instance | `UNIQUE (review_request_ref, reviewer_identity)` | One reviewer answering one request twice |
| U5 | Routing Decision | `UNIQUE (routing_decision_ref)` | Duplicate identity |
| U6 | Routing Decision | `UNIQUE (routing_request_ref, submission_ordinal)` | Two decisions for one **submission**. **Not** one decision per request: Phase 11 `model-router-invocation-boundary.md` §5 rule 1 says a retry re-submits the *same* request, and rule 3 says **every** attempt's decision is recorded |
| U7 | Model Result | `UNIQUE (model_result_ref)` | A retried invocation producing a second result |
| U8 | Model Invocation | `UNIQUE (idempotency_key)` | A duplicate external call under one key |
| U9 | Human Intervention | `UNIQUE (intervention_ref)` | A repeated intervention identity |
| U10 | Gate evidence | `UNIQUE (gate_instance_ref, evidence_ref)` | The same evidence counted twice |
| U11 | Gate instance | `UNIQUE (run_ref, work_item_ref, gate_requirement_ref, rework_iteration)` | Two live instances of one requirement in one iteration |
| U12 | Assignment | `UNIQUE (work_item_ref, attempt_ordinal)` | Two assignments claiming one attempt |
| U13 | Work Item | `UNIQUE (run_ref, task_ref, rework_iteration)` | Double stage start (race 2) |
| U14 | Workflow Run | `UNIQUE (run_ref)`; `UNIQUE (idempotency_key) WHERE status IS NOT TERMINAL` | Duplicate trigger (race 1) |
| U15 | Canonical Record | `UNIQUE (subject_key, scope_path) WHERE status = 'ACTIVE'` | Two live canonical positions on one subject in one scope |
| U16 | Knowledge item | `UNIQUE (knowledge_ref, item_version)` | Version collision |
| U17 | Irreversible act intent | `UNIQUE (act_kind, governed_subject, idempotency_key)` | A second attempt at a once-only external act |
| U18 | Scope node | `UNIQUE (scope_path)`; `UNIQUE (parent_ref, kind, slug)` | Ambiguous scope identity |
| U19 | Approval state — **current pointer** | `PRIMARY KEY (subject_ref, subject_version)` on `approval_state_current` | Two rows claiming to be the current approval state for one subject version. **There is no `ACTIVE` status**: currentness is a pointer, not a status (§5.4a) |
| U21 | Approval state — **history** | `PRIMARY KEY (approval_ref, approval_version)` on `approval_state_record`, immutable | A version collision in the immutable history |
| U22 | Provider attempt | `UNIQUE (provider_attempt_ref)`; `UNIQUE (model_invocation_ref, attempt_ordinal)` | Two records of one attempt at an external effect |
| U23 | Retry attempt | `UNIQUE (work_item_ref, attempt_ordinal)` | Two retry dispatches claiming one attempt ordinal |
| U20 | Rework loop | `UNIQUE (run_ref, rework_loop_id, iteration_ordinal)` | Iteration collision |

**Rule P-7 — at-most-once is a constraint, not a code path.** For every class-4 act the
implementation relies on the named constraint. A duplicate is a **failed write**, surfaced as
`DUPLICATE_GOVERNED_IDENTITY`, never a silently ignored insert. `ON CONFLICT DO NOTHING` is
prohibited on every table above: it converts a governance failure into a success.

**Rule P-8 — a duplicate is a failure, not a newer entry.** Two objects claiming one identity is
a governance failure → `BLOCK` and `ESCALATE`. Nothing is overwritten.

**Rule P-9 — exactly-once is not claimed.** Across an orchestrator, a database, object storage
and any external system, exactly-once delivery is not achievable and this specification does not
assert it. What is provided: idempotent-at-least-once for classes 1, 2, 5, 7; **at-most-once by
governed record** for class 4; and **exactly-once nowhere**.

**Rule P-9x — "at-least-once" names an internal retry class, never an external guarantee.** The
class-7 name `IDEMPOTENT_AT_LEAST_ONCE` is the approved Phase 11 vocabulary for how the
**orchestrator** may re-attempt a step whose target deduplicates. It is **not** a statement about
what crosses the provider boundary. Across that boundary this specification provides
**at-most-once per dispatch item and per dispatch key** and nothing stronger (PO-17): a crossed
item never presents its key again (PO-14), and a lost call is resolved by reconciliation and a new
governed attempt rather than by redelivery. Any active statement asserting external at-least-once
delivery contradicts PO-17 and is wrong.

### 5.2a Row-currentness is a pointer, never a status

An earlier revision keyed U19 on a status value `ACTIVE` that the approval-state vocabulary does
not contain, and left `APPROVED_WITH_CONDITIONS` outside the uniqueness rule entirely. Both are
corrected by separating two things that were conflated:

| Question | Answered by |
|---|---|
| *What did this approval decide?* | The **approval status** on the record: `PROPOSED`, `APPROVED`, `APPROVED_WITH_CONDITIONS`, `SUPERSEDED`, `REVOKED` |
| *Which record is the one in force right now?* | The **current pointer**, `approval_state_current` |

`approval_state_record` is an immutable version history: rows are appended, never edited.
`approval_state_current` holds at most one row per `(subject_ref, subject_version)`, pointing at
the approval-state version in force. Recording a new approval writes a new history row and
re-points the pointer **in the same transaction**, under a version-pinned write.

**Rule P-9a — every operative status is covered, and none is privileged.** The pointer may point
at a record whose status is `APPROVED`, `APPROVED_WITH_CONDITIONS`, `PROPOSED` or `REVOKED`. All
four are operative answers to "what is in force"; only `SUPERSEDED` is not, because a superseded
record by definition has a successor the pointer moved to. Uniqueness therefore holds regardless
of status, which is what the earlier status-keyed rule could not do.

**Rule P-9b — absence of a pointer row reads as `PROPOSED`.** It does not read as approved, and
it is not an error. This is the same fail-closed default the approval registry states.

### 5.3 Reference-kind constraints

**Rule P-10.** Every stored reference persists its **kind** alongside its id, and a check
constraint requires the id's prefix to equal the kind. Additionally:

| Column | Check |
|---|---|
| `decision_record.decided_by` | kind = `human` |
| `review_instance.reviewer_identity` | kind = `human` |
| `human_intervention.by` | kind = `human` |
| `routing_decision.decided_by` | kind = `router` |
| `assignment.role` | kind = `role` |
| `assignment.agent_instance` | kind = `agent_instance` |
| `canonical_record.promotion_decision_record` | kind = `decision_record`, `NOT NULL` |

These are the ten denials expressed where they cannot be argued with.

### 5.4 Decision-chain separation

**Rule P-11.** `DECISION_RIGHT_SEPARATION` rule 1 is enforced as a durable check, not an
in-memory one. For each active `SEPARATION_REQUIRED` pair `(R1, R2)`, a partial unique/exclusion
constraint or an equivalent pre-commit query ensures that no two Decision Records exist with the
same `(decision_chain_id, governed_subject)` where one names `R1`, the other names `R2`, and both
name the same `decided_by` — **including via delegation**, for which the delegating holder's
identity is carried on the record.

## 6. Optimistic concurrency

**Rule P-12 — no last-write-wins, anywhere.** `LAST_WRITE_WINS` is absent from this
specification's vocabulary exactly as it is absent from Phase 10's conflict vocabulary and Phase
11's race vocabulary, and for the same reason: it resolves a conflict by discarding a governed
change without anyone seeing it.

Every mutable governed row carries:

| Field | Type | Notes |
|---|---|---|
| `record_version` | bigint | Monotonic per row; incremented by the governed write path only |
| `updated_at` | timestamptz | Operational; **never a concurrency token** |

**Rule P-13 — version-pinned writes.** Every update states the `record_version` it read. A
mismatch fails the write with `STALE_WRITE` and **writes nothing**. The loser re-reads and
decides; **nothing is merged automatically**.

**Rule P-14 — timestamps are not tokens.** No concurrency decision anywhere uses a timestamp
comparison. Clocks are for recording when, never for deciding who wins.

## 7. The transactional rule under durable storage

> **construct → validate → preflight → commit**

### 7.1 The audit-cardinality rule, stated once

Three statements in an earlier revision of this package disagreed: the prose said one audit event
per governed record write, the audit schema referenced one governed record, and the transaction
table emitted one audit event for several writes in some rows and none in others. One rule, and
it is applied everywhere below:

> **Rule P-14a — one audit event per persisted governed-record mutation, in the same
> transaction, linked to that exact record.** A higher-level governed act that mutates *n*
> governed records therefore produces *n* audit events. It produces execution events according
> to what it coordinated, which is a different count and a different question.

**Rule P-14b — act-level correlation is not record-level cardinality.** All the audit events of
one act share a `correlation_id`, and each carries the `causation_id` of the execution event that
coordinated it. Correlation is how the rows are gathered back into an act; it is **not** a
licence to write one row for several records.

**Rule P-14c — no grouping.** Multiple governed-record changes are never written behind one
audit event. Phase 10 `storage/audit-provenance-model.md` authorises no such grouping, and a
grouped row cannot answer "which record moved from which version to which", which is the only
question the audit event exists to answer.

**Rule P-14d — what does and does not count as a governed-record mutation.**

| Counts | Does not count |
|---|---|
| `INSERT` of a governed record | An execution event (it is not a governed record) |
| `VERSION_APPEND` — a new version row | A runtime event, metric, trace or log line |
| `LINK_APPEND` — an append-only lineage link | A read |
| `LIFECYCLE_STATE_CHANGE` — including every terminal transition | A `registry_projection` refresh (a projection, not a governed record) |
| `METADATA_CHANGE` on a `MUT` column | **An outbox row or any of its claim/lease transitions** (operational — Rule P-20a; the governed records of the same act are audited normally) |

### 7.2 Every governed act, with its exact audit rows

**This table is exhaustive over the governed-command inventory** of
`api-command-contracts.md` §5.1. Its row keys are that table's `Act` keys, and the two sets are
**exactly equal** — checked, not asserted (Rule Q-7a). An act appearing here with no command
would be a contract nothing calls; a command with no act here would have no commit contract and
could not be built.

Columns: read set · validation/preflight set · concurrency check · exact governed writes ·
**exact audit-event count** · execution-event count · durable constraints relied on ·
pre-commit refusal behaviour.

| Act | Branch | Read set | Validation / preflight set | Concurrency check | Governed writes (one transaction) | **Audit events** | Exec events | Constraints | Failure before commit |
|---|---|---|---|---|---|---|---|---|---|
| **create_run** | — | Workflow Definition @v, Orchestrator Policy @v, scope node, approval state | Intake checks 1–7 (orchestrator §2) | Run-ref availability | `workflow_run`, `scope_binding` | **2** | 2 | U14, U18 | Recorded refusal; **no run row** |
| **activate_stage** | — | Run state, Workflow Definition @v, task | Halted guard, task in definition, phase plan | Run `record_version` | `work_item`, `gate_instance` × *g* | **1 + *g*** | 1 | U11, U13 | Nothing written |
| **assign** | — | Work Item, bound Task's required Role, attempt counter | Halted guard, role match, agent instance type, insert preflight | Work Item `record_version` | `assignment`, Work Item attempt counter | **2** | 1 | U12 | Counter unchanged; no assignment |
| **route** | B1 invalid answer | Run, Work Item, Routing Policy @v, candidate universe | Halted guard; answer type, request identity, run and Work Item binding, Router identity, six-part completeness on a selection | Run `record_version` | **0 — no request, no decision** | **0** | 1 (refusal) | — | **Nothing written.** The prospective envelope is discarded |
| **route** | B1r invalid answer against an already durable request | as B1, plus the durable request and its highest `submission_ordinal` | as B1 | Run `record_version` | **0 — the existing Routing Request is preserved, no decision is created, and `submission_ordinal` is not advanced** | **0** | 1 (refusal) | U6 | **Nothing written.** The prospective envelope is discarded and the run's phase, posture and wait axes are unchanged |
| **route** | B2 selection, first submission | as B1 | as B1, answer valid and `ELIGIBLE_CANDIDATE` | Run `record_version` | `routing_request`, `routing_decision` | **2** | 2 | U5, U6 | Nothing written |
| **route** | B3 non-selection, first submission | as B1 | as B1, answer valid and a recorded refusal | Run `record_version` | `routing_request`, `routing_decision`, **run state × *s*** — the exact appends, postures and wait subject of Rule Q-17b, in the same transaction | **2 + *s*** | 2 | U5, U6 | Nothing written |
| **route** | B4s re-submission, selection | as B1, plus the durable request | as B1; the request is already durable and the ordinal is next; answer valid and `ELIGIBLE_CANDIDATE` | Run `record_version` | `routing_decision` only | **1** | 1 | U5, U6 | Nothing written |
| **route** | B4n re-submission, non-selection | as B4s | as B4s, answer valid and a recorded refusal | Run `record_version` | `routing_decision`, **run state × *s*** — the same appends, postures and wait subject as B3, by Rule Q-17b | **1 + *s*** | 1 | U5, U6 | Nothing written |
| **invoke_model** | S1 local intent | Recorded Routing Decision, Work Item | Halted guard, decision is this run's, outcome eligible. **No provider call occurs in this transaction** | Run `record_version` | `model_invocation` intent, `provider_attempt` at `NOT_ATTEMPTED` — **plus an outbox row, which is operational (P-20a) and is not audited** | **2** | 1 | U8, U22, O1–O3 | Nothing written |
| **record_provider_attempt_outcome** | S3 outcome only | Staged attempt, Routing Decision | Attempt is staged; observed outcome is one of the four states | Attempt `record_version` | `provider_attempt` state | **1** | 1 | U22 | Nothing written |
| **record_provider_attempt_outcome** | S4 outcome + result | as S3 | as S3, outcome `CONFIRMED_APPLIED` with content; five-element lineage equality (M-11); release-identity comparison (M-11a) | Attempt `record_version` | `provider_attempt` state, `model_result` | **2** | 1 | U7, U22 | Nothing written |
| **reconcile_external_effect** | S5 still unknown | Uncertain attempt, external system under its idempotency key | Attempt is `ATTEMPTED_OUTCOME_UNKNOWN`; the external system cannot answer | Attempt `record_version` | `reconciliation` recording the unresolved determination | **1** | 1 | — | Nothing written; the attempt stays uncertain and escalates |
| **reconcile_external_effect** | S5 resolved | as above | The external system answers under the idempotency key | Attempt `record_version` | `reconciliation`, `provider_attempt` state, and `model_result` where applied with retrievable content | **2 or 3** | 1 | U7, U22 | Nothing written |
| **request_review** | — | Gate instance, Review Profile @v | Halted guard; gate kind is `REVIEW` | Gate instance `record_version` | `review_request` | **1** | 1 | — | Nothing written |
| **review_gate** | — | Gate instance, Review Profile @v, review request | Halted guard, instance lineage, independence class, eligibility class, SoD rules A-4, insert preflight, phase plan | Gate instance `record_version` | `review_instance`, gate instance outcome | **2** | 1 | U3, U4, U10 | Gate unchanged |
| **request_decision** | — | Gate instance, Decision Right @v | Halted guard; gate kind is `DECISION`; Right resolves at an approved version | Gate instance `record_version` | `decision_request` | **1** | 1 | — | Nothing written |
| **decision_gate** | — | Gate instance, Decision Right @v, holder set, active separations | Halted guard, five gate-satisfaction conditions, 19-element completeness, separation check | Gate instance `record_version` | `decision_record`, gate instance outcome | **2** | 1 | U1, U2, U10, P-11 | Gate unchanged; **no Decision Record** |
| **supply_gate_evidence** | — | Gate instance, the evidence object | Halted guard; evidence type admissible for the gate kind; evidence lineage names this gate instance; insert preflight | Gate instance `record_version` | Evidence record, gate instance outcome | **2** | 1 | U10 | Gate unchanged |
| **record_intervention** | — | Run state, interventions | Halted guard; the one intervention contract | Run `record_version` | `human_intervention` | **1** | 1 | U9 | Nothing written |
| **pause** | — | Run state, interventions | Halted guard, intervention contract, transition preflight (`allow_noop=false`) | Run `record_version` | `human_intervention`, run phase change | **2** | 1 | U9 | Nothing written |
| **resume** | — | Run state, interventions | Intervention contract; run is `PAUSED`; transition preflight | Run `record_version` | `human_intervention`, run phase change | **2** | 1 | U9 | Nothing written |
| **unblock** | — | Run state, interventions, standing gates | The five `unblock` conditions (orchestrator O-5) | Run `record_version` | `human_intervention`, run state → phase **and** posture in one append (P-14g) | **2** | 1 | U9 | Nothing written |
| **cancel_run** | — | Run state, interventions | Terminal reachability for `CANCELLED`; **the intervention contract**; insert preflight. A human act | Run `record_version` | `human_intervention`, run terminal state | **2** | 1 (`TERMINAL`, human + system identity) | U9 | Nothing written |
| **terminate_run** | — | Run state, the constraint that would be breached | Terminal reachability for `TERMINATED`; **a named constraint**; acting system identity present. **No intervention is accepted; a supplied one is a refusal** | Run `record_version` | `constraint_stop_record`, run terminal state | **2** | 1 (`TERMINAL`, system identity only, `human_identity_ref` **NULL**) | — | Nothing written |
| **fail_run** | — | Run state, retry history | Terminal reachability for `FAILED`; a recorded cause; no permitted retry resolved it | Run `record_version` | `failure_record`, run terminal state | **2** | 1 | — | Nothing written |
| **supersede_run** | — | Both runs | Terminal reachability for `SUPERSEDED`; the superseding run exists and names this one | Run `record_version` | Run terminal state, supersession link | **2** | 1 | — | Nothing written |
| **complete_run** | — | Run state, gates, posture | Posture permits the outcome; no unsatisfied gate; phase permits; each carried item has an upstream rule | Run `record_version` | Run terminal state | **1** | 1 | — | Nothing written |
| **retry** | R1 automatic (classes 1, 5) | Work Item bound retry class, attempt history | Halted guard; class permits; attempt limit not reached | Run `record_version` | `retry_attempt`, run state → `RUNNING`, **posture unchanged** | **2** | 1 | U23 | Nothing written |
| **retry** | R2 revalidating (class 2) | as R1, plus preconditions, freshness, scope, sensitivity, eligibility | as R1, **plus** all of those re-evaluated before dispatch | Run `record_version` | `revalidation_record`, `retry_attempt`, run state → `RUNNING`, **posture unchanged** | **3** | 2 | U23 | Nothing written |
| **retry** | R2f revalidation fails (class 2) | as R2 | A re-evaluated precondition no longer holds | Run `record_version` | `revalidation_record`, run state → `BLOCKED` **with posture `GATE_UNSATISFIED`** | **2** | 1 | — | Nothing written |
| **retry** | R3 awaiting acknowledgement (class 3) | as R1, interventions | No acknowledgement intervention exists yet | Run `record_version` | `retry_hold_record`, run state → `WAITING`, **wait reason `WAITING_FOR_HUMAN`, wait subject the acknowledgement, posture unchanged** | **2** | 1 | — | Nothing written |
| **retry** | R3a acknowledged (class 3) | as R3 | An acknowledgement intervention exists | Run `record_version` | `retry_attempt`, run state → `RUNNING`, **wait reason and subject cleared, posture unchanged** | **2** | 1 | U23 | Nothing written |
| **retry** | R4 refused, non-retryable (class 4) | Work Item bound retry class | The request is made at all | Run `record_version` | `retry_refusal_record`, run state → `BLOCKED` **with posture `GATE_UNSATISFIED`**, run state → `ESCALATED` **with posture `GATE_UNSATISFIED`** | **3** | 2 | — | Nothing written. **This branch is never "nothing written": refusing is a governed act** |
| **retry** | R6 refused, external side effect (class 6) | Work Item class, the attempt's external-effect state | The request is made at all | Run `record_version` | `retry_refusal_record` naming the external-effect state, run state → `BLOCKED` **with posture `GATE_UNSATISFIED`**, run state → `ESCALATED` **with posture `GATE_UNSATISFIED`** | **3** | 2 | — | Nothing written |
| **retry** | R7 idempotent (class 7) | as R1, the target's deduplication guarantee | The step carries an idempotency key **and** the target deduplicates | Run `record_version` | `retry_attempt`, run state → `RUNNING`, **posture unchanged** | **2** | 1 | U23 | Nothing written |
| **retry** | RX unclassified | Work Item bound lineage | No retry class is declared — non-retryable by default | Run `record_version` | `retry_refusal_record`, run state → `BLOCKED` **with posture `GATE_UNSATISFIED`**, run state → `ESCALATED` **with posture `GATE_UNSATISFIED`** | **3** | 2 | — | Nothing written |
| **rework_iteration** | — | Rework loop declaration @v, prior iteration | Entry condition met; `max_iterations` not exhausted | Loop `record_version` | `rework_loop_instance`, `work_item` × *w*, `gate_instance` × *g* | **1 + *w* + *g*** | 1 | U11, U13, U20 | Nothing written |
| **open_sub_run** | — | Parent run, target scope node | Halted guard; parent scope narrows to child scope (S-8, S-9) | Parent run `record_version` | Child `workflow_run`, child `scope_binding` | **2** | 1 | U14, U18 | Nothing written |
| **scope_transfer** | — | Source run, retained Decision Records, mechanism registry, target definition | All source-side clauses **and** every target-run creation condition, via one shared preflight | Source run `record_version` | `scope_transfer_authorisation`, target `workflow_run`, target `scope_binding`, provenance link | **4** | 2 | U14, U18 | **No authorisation record, no partial run** |
| **create_knowledge_item** | — | Scope node, evidence and source links | Four axes complete; type-specific requirements (derivation, reasoning); links resolve | — (insert) | `knowledge_item` v1 | **1** | 1 | U16 | Nothing written |
| **adopt_ai_suggestion** | — | The `AI_SUGGESTION` item, its basis | The new item's type is supported by **its own** basis; the adoption link is not evidence (K-4); the suggestion is not mutated in type or origin | Suggestion `record_version` | New `knowledge_item` v1, adoption link, suggestion governance state | **3** | 1 | U16 | Nothing written |
| **raise_conflict** | — | The items in tension | Items resolve at the versions named; conflict class is one of the seven | — (insert) | `conflict_record`, conflict flag × *n* | **1 + *n*** | 1 | — | Nothing written |
| **resolve_conflict** | — | Conflict record, items in tension, Review Instance | Eligible Role; reasoning present; residual uncertainty present; review present. **No Decision Right** (K-13a) | Conflict `record_version` | `conflict_resolution`, conflict status change | **2** | 1 | — | Nothing written |
| **apply_consequent_status_change** | — | The resolution, the target record, the mapped Right | The change's own Right resolves and a Decision Record exists for it | Target `record_version` | Target governance-state transition, link from the resolution | **2** | 1 | — | Nothing written. **Where the change is a canonical one, BA-1 blocks it and nothing is ever written** |
| **transcribe_approval_state** | — | Source approval record at its commit, subject, subject version | Source resolves **at the cited commit**; every written field derives from the source; approving authority is human; no field is invented | Current-pointer `record_version` | `approval_state_record` (new immutable version), `approval_state_current` (create or move) | **2** | 1 | U19, U21 | Nothing written; the subject stays `PROPOSED` |
| **record_new_approval_state** | — | Source approval record, Decision Record, subject | Source resolves; the governed act's Right resolves; the Decision Record resolves and its `decided_by` is human | Current-pointer `record_version` | `approval_state_record` (new immutable version), `approval_state_current` (move) | **2** | 1 | U19, U21 | Nothing written |
| **promote_to_canonical** | — | Knowledge item @v, evidence, conflicts, freshness, Decision Record | Preconditions 1–9 | — | **0 — nothing is ever written** | **0** | 1 (refusal) | — | **Blocked at precondition 9 (BA-1). Zero governed writes, zero audit events, one refusal execution event** |
| **reparent_scope_node** | — | Scope node, descendants | — | — | **0 — nothing is ever written** | **0** | 1 (refusal) | — | **Blocked (BA-2).** As above |
| **destroy_governed_content** | — | The target record | — | — | **0 — nothing is ever written** | **0** | 1 (refusal) | — | **Blocked (BA-3).** As above |
| **apply_destructive_migration** | — | Migration manifest, classifier verdict | Declared class matches the classifier; legal holds absent | — | **0 — nothing is ever written** | **0** | 1 (refusal) | — | **Blocked (BA-4).** As above |

*g* = gate instances created, *w* = work items created, *n* = items the conflict flags, *s* = the
run-state appends the non-selection outcome requires (Rule Q-17b: **1** for `NO_ELIGIBLE_MODEL`
and `ACT_REQUIREMENT_OUTSTANDING`, **2** for `CANDIDATE_UNIVERSE_INCOMPLETE` and
`NO_APPLICABLE_DECISION_RIGHT`). Each is a
real count, not a placeholder: an act that creates three gate instances writes three audit events
for them.

**Rule P-14g — a run-state transition is one version append, carrying every axis it
changes.** Phase, governance posture, wait reason and wait subject are four axes of **one**
governed record, the `workflow_run`. A transition that changes several of them at once is a
single `LIFECYCLE_STATE_CHANGE` append and therefore **one** audit event; two *successive*
transitions — a block and then an escalation — are two appends and two audit events. This is why
`unblock` writes two records and not three, and why R4 writes three and not two. The exact writes
column below always names the posture the append carries, so a halted or escalated posture is a
committed fact and not a remark in prose.

**Rule P-14e — a refused transaction writes no audit event, including the blocked four.** A
refusal mutates no governed record, so there is none to audit. It produces **one execution
event** recording the refusal and the gap, because a refusal is coordination history and that is
exactly what execution events are for. The four blocked acts above are the standing case: their
entire history is execution events.

**Rule P-14f — counting the audit rows is a build-time obligation.** An implementation adding a
governed write to any act above updates this table's count in the same change. The count is what
the assurance suite asserts (`test-and-assurance-strategy.md` §3, A31), so a write added without
updating it fails the suite rather than passing silently.

**Rule P-15.** Every row's writes are **one database transaction**. A governed act that would
span two transactions is redesigned until it does not, or it is expressed with the staged
protocol of §8 and explicitly loses its atomicity claim.

**Rule P-16.** No ordinary governed failure leaves an internally inconsistent partial governance
state. The observational-equality invariant (Rule O-25) is a property the persistence layer must
preserve, and it is verified by the concurrency and adversarial tests in
`test-and-assurance-strategy.md`.

## 8. Object storage commit protocol

Atomicity cannot span PostgreSQL and an object store. This specification does not pretend it can.

**Declared commit order:** upload the object → **verify the returned content hash** → commit the
metadata record.

| Interruption point | Result | Handling |
|---|---|---|
| Before upload | Nothing exists | None needed |
| Upload succeeded, hash mismatch | Bad bytes, no record | Delete-on-write-path permitted for the un-referenced upload; record the mismatch |
| Upload succeeded, metadata commit failed | **Orphaned object** | `RECONCILE` → **`QUARANTINE`**; the object is unreferenced, is expired under its retention class, and is **never adopted by a later record** |
| Metadata committed | Artifact exists | Normal |

**Rule P-17.** Nothing reads an object the registry does not know about, so an interrupted
sequence leaves an orphaned object and **never a visible artifact**.

**Rule P-18 — orphans are never adopted.** A later record may not claim existing bytes by hash
or by path. Adoption would make a partially-completed write indistinguishable from a completed
one.

**Rule P-19 — objects are never overwritten in place.** A new version is a new object version.

## 9. Outbox for external effects

### 9.1 What the outbox is, and what it is not

Where a governed act must both commit locally and cause an external effect:

1. the intent record and an **outbox row** are written **in the same local transaction** as the
   governed act;
2. C16 drains the outbox, performs the external call with the recorded idempotency key, and
   records the execution record and the external-effect uncertainty state;
3. an unknown outcome remains `ATTEMPTED_OUTCOME_UNKNOWN` and enters reconciliation.

**Rule P-20 — the outbox is not a queue product.** It is a table and a drain loop. No queue,
broker, worker framework or event bus is specified, named or required.

**Rule P-20a — an outbox row is an operational record, never a governed one.** It carries no
authority, satisfies no gate, and is never governance evidence. It is therefore **not** a
governed-record mutation under Rule P-14d, and writing one produces **no audit event**. The
governed records of the same act — the invocation intent and the provider attempt — are audited
normally, and the drain's own activity is execution-event history. This is the approved Phase
10/11 distinction applied without exception: delivery plumbing is not governance. Every audit
count in §7.2 is derived on this classification, and the assurance suite asserts it (A48).

**Rule P-21 — the outbox never authorises.** A row in the outbox carries the authorisation
reference; it does not substitute for one. An outbox row for a class-4 act whose authorisation
record is absent is refused at insert by a `NOT NULL` foreign key.

### 9.2 The dispatch item — stable identity and durable columns

| # | Field | Is |
|---:|---|---|
| 1 | `outbox_ref` | The **stable identity** of one dispatch item, assigned in the enqueuing transaction and never reassigned |
| 2 | `model_invocation_ref` | The governed intent this dispatch item serves |
| 3 | `provider_attempt_ref` | The **one** provider attempt this dispatch item resolves |
| 4 | `provider_idempotency_key` | The key presented to the provider. Stable for the life of the row |
| 5 | `claim_state` | One of the six values of §9.3 |
| 6 | `lease_owner` | The claimant service identity currently holding the row, or `NULL` |
| 7 | `lease_expires_at` | When the current claim stops being renewable by its owner, or `NULL` |
| 8 | `claim_token` | The per-claim fencing token. A fresh value on every acquisition; `NULL` when unowned |
| 9 | `claim_generation` | A monotonically increasing integer. **Every** state-changing write increments it. Never reset, never reused |
| 10 | `boundary_crossed` | Boolean, **append-only from `false` to `true`**. Set `true` in the same transaction that enters `DISPATCH_PENDING`, and never set back |
| 11 | `terminal_reason` | Why a terminal state was reached: `OUTCOME_OBSERVED`, `RECONCILED`, `RETIRED_BEFORE_DISPATCH` or `UNRESOLVED`. `NULL` while the row is not terminal |

**Rule PO-1 — the provider idempotency key is stable and never regenerated.** It is derived in
the enqueuing transaction from `(model_invocation_ref, provider_attempt_ref)` and stored. Every
dispatch of the item — including any permitted redispatch — presents the **same** key.
Regenerating it silently converts "the provider deduplicates" into "the provider sees a new
request".

### 9.2a Operational constraints — implementable, and time-free

These constraints are **operational** and are deliberately **not** rows of the canonical governed
uniqueness inventory of §5.2, because an outbox row is not a governed record. They are named
`O1`–`O5` so that no count of the `U` inventory changes.

| # | Constraint | Prevents |
|---:|---|---|
| O1 | `PRIMARY KEY (outbox_ref)` | A duplicate dispatch identity. **This is the only identity constraint on the row**; no second constraint restates it |
| O2 | `UNIQUE (provider_attempt_ref)` | Two dispatch items racing to satisfy one provider attempt |
| O3 | `UNIQUE (provider_idempotency_key)` | Two items presenting one key to the provider |
| O4 | `CHECK ( (claim_state IN ('CLAIMED','DISPATCH_PENDING')) = (lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL AND claim_token IS NOT NULL) )` | A row that is owned without an owner, a token or an expiry — or unowned while still carrying them |
| O5 | `CHECK (claim_generation >= 0)` — a **row-shape** constraint only: it bounds the column's domain and **enforces no ordering between successive updates** | A negative or absent generation. It does **not** enforce monotonicity; Rule PO-4 says where monotonicity actually lives |

**Rule PO-2 — ownership is a property of the row, never of an index.** An earlier revision
declared a partial unique index predicated on `lease_expires_at > now()`. **That is not
implementable**: a unique index predicate must be immutable, and `now()` is not — the same stored
row would enter and leave the index as time passed, with no write. It is removed and not replaced
by an equivalent. Exclusivity comes from the fact that `lease_owner` is **one column on one row**:
there is nowhere for a second simultaneous owner to be recorded. What makes that exclusivity
*enforceable under contention* is Rule PO-3, not a constraint.

**Rule PO-3 — every state-changing write is one atomic conditional update, or it did not
happen.** Each transition of §9.4 is a single statement whose `WHERE` clause carries, at minimum,
`outbox_ref = <the item>` **and** `claim_generation = <the generation the writer read>`, plus the
transition's own precondition. Zero rows updated means another writer moved the row first, and the
loser **performs no external call and writes nothing**. There is no read-then-write path, and no
advisory lock substitutes for the compare-and-swap.

**Rule PO-4 — the generation is the fence, and the fence is the predicate — not a constraint.**
Every successful state-changing write sets `claim_generation = claim_generation + 1`. A writer
holding an older generation, or an older `claim_token`, matches no row and its write is rejected
**by the `WHERE` clause**, not by application logic. This is what makes an expired owner harmless
without any clock comparison at write time: the moment anyone else transitions the row, every
token the old owner holds is stale.

**Monotonicity is not claimed as a database guarantee.** `O5` is a domain constraint on one row
and cannot compare a new value with the old one; no ordinary `CHECK` can, and this specification
does not pretend otherwise. What actually prevents a generation from going backwards is that
**every** transition of §9.4 both requires `claim_generation = <the value read>` and writes
`+ 1`: a write that tried to lower it would first have to match the current value, and would then
be the only writer able to do so — at which point the next writer's read-then-CAS rejects it. The
guarantee is therefore *per-transition*, enforced by the predicate set, and it holds only because
no write path outside §9.4 exists. A trigger or an `IDENTITY` column could add a database-level
guarantee; neither is specified here, because neither is needed and both would be a mechanism a
reader could mistake for the contract.

**Rule PO-5 — `lease_expires_at` schedules attention, it does not grant or revoke ownership.** It
is read by the recovery sweep to decide *which rows to look at*. It is never the mechanism by
which ownership changes hands; that is always an explicit transition under PO-3. A clock skew
therefore cannot transfer ownership, and a long garbage-collection pause cannot cause two writers
to both believe they hold the row — the second one's write simply matches nothing.

**Rule PO-6 — the claimant is a named service identity.** `lease_owner` holds the acting service
identity of `security-identity-access.md`, never a hostname, a process id or a worker number. A
row whose owner does not resolve to a registered service identity is recovered by the sweep, not
trusted.

### 9.3 Claim state vocabulary — six states, one boundary

`PENDING` · `CLAIMED` · `DISPATCH_PENDING` · `UNCERTAIN` · `SETTLED` · `ABANDONED`

| State | Means | `boundary_crossed` | Leaves to |
|---|---|---|---|
| `PENDING` | Enqueued; unowned; **no call has been made under any claim** | `false` | `CLAIMED` |
| `CLAIMED` | A claimant holds the row and is preparing the call. **No call may be made from this state** | `false` | `DISPATCH_PENDING`; or back to `PENDING` on recovery |
| `DISPATCH_PENDING` | The durable, committed **intent to call**. The call is made only after this state commits, so from here the system can **never again** conclude locally that no call occurred | **`true`** | `SETTLED`; or `UNCERTAIN` on recovery |
| `UNCERTAIN` | The boundary was crossed and no outcome is durable. The provider attempt is `ATTEMPTED_OUTCOME_UNKNOWN` | `true` | `SETTLED` via reconciliation; or `ABANDONED` |
| `SETTLED` | Terminal. The provider attempt reached a recorded external-effect state **and** the governed stage 3/4 transaction committed | `true` (or `false` only where the item was retired before any call) | — |
| `ABANDONED` | Terminal. Reconciliation could not resolve the effect. **Never re-dispatched** | `true` | — |

**Rule PO-7 — the call happens strictly between two committed states, and the earlier one is
already on the pessimistic side.** The ordering is: commit `DISPATCH_PENDING` → make the call →
commit the outcome. The single crash window that matters — after the call, before the outcome —
therefore finds the row already in `DISPATCH_PENDING` with `boundary_crossed = true`, which is
read as *the call may have happened*, never as *the call did not happen*.

**Rule PO-8 — `CLAIMED` is the only state that is safely re-dispatchable, and it is safe for a
structural reason.** No call is ever made from `CLAIMED`; a claimant that wants to call must first
commit `DISPATCH_PENDING`. A `CLAIMED` row whose owner disappeared therefore cannot have crossed
the boundary, and `boundary_crossed = false` records that as a durable fact rather than as an
inference. This is the one place where "nothing left the system" is a conclusion the local state
is actually entitled to.

**Rule PO-9 — `boundary_crossed` is monotone.** It goes `false` → `true` exactly once, in the
transaction that enters `DISPATCH_PENDING`, and no transition ever sets it back. A contract that
allowed it to be cleared would allow a crossed boundary to be forgotten, which is the failure this
whole section exists to make impossible.

**Rule PO-10 — an expired claim is never proof, and is never treated as one.** The recovery sweep
decides what a stale row becomes **by reading `boundary_crossed`, never by reading the clock or
the previous state's name**: `false` → back to `PENDING`; `true` → `UNCERTAIN` and mandatory
reconciliation. Expiry says a claimant stopped reporting. It says nothing whatever about the
provider.

### 9.4 Every transition, token-fenced

Every row below is one atomic conditional update under Rule PO-3. "Fencing" states what the
predicate must carry beyond `outbox_ref` and the state precondition.

| # | Transition | Reads | Predicate (all clauses required) | Writes | Fencing | Redispatch permitted after? | Provider reconciliation mandatory? |
|---:|---|---|---|---|---|---|---|
| T1 | `PENDING` → `CLAIMED` | The row | `claim_state = 'PENDING'` **AND** `claim_generation = <read>` | `claim_state='CLAIMED'`, `lease_owner`=claimant, fresh `claim_token`, `lease_expires_at`=now + lease duration, `claim_generation`+1 | Generation | **Yes** — nothing has left the system | No |
| T2 | `CLAIMED` → `DISPATCH_PENDING` | The row, the attempt, the stable key | `claim_state='CLAIMED'` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `claim_state='DISPATCH_PENDING'`, **`boundary_crossed=true`**, `claim_generation`+1 | Token **and** generation | **No** — the call is about to be made | Yes, if no outcome commits |
| T3 | Claim renewal, `CLAIMED` or `DISPATCH_PENDING` → same state | The row | `claim_state` unchanged **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `lease_expires_at` extended, `claim_generation`+1; **`claim_state` and `boundary_crossed` unchanged** | Token **and** generation | Unchanged by renewal | Unchanged by renewal |
| — | **The external call** | — | **Not a transition. No database statement is atomic with it** (Rule PO-11) | — | — | — | — |
| T4 | `DISPATCH_PENDING` → `SETTLED`, outcome **observed** (`CONFIRMED_APPLIED` or `CONFIRMED_NOT_APPLIED`) | The row, the provider response | `claim_state='DISPATCH_PENDING'` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `claim_state='SETTLED'`, `lease_owner`/`claim_token`/`lease_expires_at` cleared (O4), `claim_generation`+1 | Token **and** generation | n/a — terminal | No |
| T5 | `DISPATCH_PENDING` → `UNCERTAIN`, outcome **unknown to the caller itself** (timeout, reset, ambiguous response) | The row | `claim_state='DISPATCH_PENDING'` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `claim_state='UNCERTAIN'`, owner columns cleared, `claim_generation`+1 | Token **and** generation | **Never** — PO-14 is unconditional | **Yes** |
| T6 | `CLAIMED` → `PENDING`, expired-claim recovery | The row | `claim_state='CLAIMED'` **AND** `boundary_crossed = false` **AND** `lease_expires_at <= now()` **AND** `claim_generation = <read>` | `claim_state='PENDING'`, owner columns cleared, `claim_generation`+1 | Generation | **Yes** — PO-8 | No |
| T7 | `DISPATCH_PENDING` → `UNCERTAIN`, expired-claim recovery | The row | `claim_state='DISPATCH_PENDING'` **AND** `boundary_crossed = true` **AND** `lease_expires_at <= now()` **AND** `claim_generation = <read>` | `claim_state='UNCERTAIN'`, owner columns cleared, `claim_generation`+1 | Generation | **Never** — PO-14 is unconditional | **Yes** |
| T8 | `UNCERTAIN` → `SETTLED`, reconciliation resolved | The row, the external system under the stable key | `claim_state='UNCERTAIN'` **AND** `claim_generation = <read>` | `claim_state='SETTLED'`, `claim_generation`+1 | Generation | n/a — terminal | The transition **is** the reconciliation outcome |
| T9 | `UNCERTAIN` → `ABANDONED`, reconciliation unanswerable | The row | `claim_state='UNCERTAIN'` **AND** `claim_generation = <read>` | `claim_state='ABANDONED'`, `claim_generation`+1 | Generation | **Never** | Already attempted and failed; the run blocks and escalates |
| T10 | `PENDING` → `SETTLED`, **unowned** retirement before any call (the governed intent was superseded, cancelled or terminated) | The row, the governed intent's terminal state | `claim_state = 'PENDING'` **AND** `boundary_crossed = false` **AND** `lease_owner IS NULL` **AND** `claim_generation = <read>` | `claim_state='SETTLED'`, `terminal_reason='RETIRED_BEFORE_DISPATCH'`, owner columns remain `NULL` (O4), `claim_generation`+1 | Generation. **No token exists, because no claimant holds the row** | n/a — terminal | No |
| T11 | `CLAIMED` → `SETTLED`, **owner-fenced** retirement before any call | The row, the governed intent's terminal state | `claim_state = 'CLAIMED'` **AND** `boundary_crossed = false` **AND** `lease_owner = <the writer's own service identity>` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | as T10 | Owner, token **and** generation | n/a — terminal | No |

**Rule PO-10a — retirement is fenced by ownership, and no one retires another claimant's row.**
An owned row is retired only by **its own** claimant, through T11, whose predicate names
`lease_owner`, `claim_token` and `claim_generation` together. A writer that is not the owner, or
that holds a stale token or a stale generation, matches **zero rows and writes nothing** — it does
not fall back to T10, because T10's predicate requires `lease_owner IS NULL`. An owned row whose
claimant has gone is recovered first (T6 to `PENDING`) and only then retired (T10); recovery and
retirement are two transitions and are never collapsed into one, because collapsing them is how a
live claimant's row gets retired out from under it.

**Rule PO-10b — retirement is never a substitute for settlement.** T10 and T11 apply **only**
where `boundary_crossed = false` and the governed intent itself has reached a terminal state —
the run was cancelled or terminated, or the invocation was superseded. `terminal_reason` records
`RETIRED_BEFORE_DISPATCH` so that a `SETTLED` row retired without a call is distinguishable, at a
glance and in a query, from a `SETTLED` row whose provider attempt actually resolved. A crossed
item is **never** retired; it goes to `UNCERTAIN` and reconciles.

**Rule PO-11 — no database statement is atomic with the provider call.** The call sits between
T2 and T4/T5 and is deliberately not a row of the table above. Any contract that placed it inside
a transition would be claiming a distributed transaction, which §9.5 denies.

**Rule PO-12 — a stale token settles nothing.** T4, T5 and T3 require the writer's `claim_token`
to match the stored one **and** its generation to match. A writer that resumes after the row was
recovered by T6 or T7 holds neither, matches no row, and its settlement is rejected by the
predicate. It must re-read the row and act on what it finds; it must **not** re-call the provider
on the strength of what it remembers.

**Rule PO-13 — successful governed persistence settles the dispatch item in the same
transaction.** The stage 3/4 transaction of `api-command-contracts.md` §5.5 — which commits the
provider-attempt outcome and, where applicable, the Model Result — carries **T4** in the same
local transaction. A committed outcome with the dispatch item left in `DISPATCH_PENDING` is not a
state this specification permits, and A59 is the adversarial test that asserts it. The governed
records are audited; the T4 transition beside them is operational and is not (P-20a).

**Rule PO-14 — a crossed boundary is never re-dispatched. There is no exception.** Once
`boundary_crossed = true`, this dispatch item will not present its key to the provider again
under any condition — not on a `CONFIRMED_NOT_APPLIED` reconciliation, not under a recorded
provider-deduplication guarantee, not after any elapsed time, and not on any human instruction
short of a new governed act. The earlier revision allowed a conditional redispatch and specified
**no fenced transition that could perform it**: there was a permission with no path, which is a
worse defect than either a permission or a prohibition, because an implementer would have had to
invent the path.

The simpler architecture is chosen because it loses nothing. Where reconciliation reports
`CONFIRMED_NOT_APPLIED`, the effect demonstrably did not occur and the work may proceed — but it
proceeds as a **new governed provider attempt**: a new `ProviderAttemptRef` at the next
`attempt_ordinal` under U22, a new dispatch item with its own `outbox_ref`, and its own **new**
`provider_idempotency_key` derived per PO-1 from that new pair. That is what Phase 11 means by
re-attempting where the retry class permits, and it is a governed act with an audit trail rather
than an operational replay that leaves the same row looking as though it were dispatched once.

**Rule PO-14a — the key is reused only where the boundary was not crossed.** T6 re-claims an
uncrossed item, and that item keeps its `outbox_ref`, its `provider_attempt_ref` and its
`provider_idempotency_key`, because nothing left the system and it is the **same** attempt. Once
the boundary is crossed, a continuation is a new attempt with a new key — never the old key on a
new try, and never the old row.

**Rule PO-14b — receiver-side deduplication licenses nothing here.** Whether a provider
deduplicates on the key is a property of the provider, recorded on the deployment's Provider
Profile, and it bears on the **retry class** a step declares (`api-command-contracts.md` Q-25). It
is **not** a permission to re-dispatch a crossed item, and this protocol does not rely on it for
any safety property. A protocol whose correctness depended on a remote system's documented
behaviour would be asserting a guarantee it cannot verify.

### 9.5 Deduplication at the receiver

**Rule PO-15 — the only redelivery this protocol performs is pre-boundary.** T6 re-claims an item
whose claim expired while `boundary_crossed` was still `false`, and re-presents the same key. That
is safe because no call was made, not because anyone deduplicates. Where a provider does happen to
deduplicate, the effect is that a redelivery **this protocol never performs** would have been
harmless; the protocol claims nothing from it (PO-14b).

**Rule PO-16 — after the boundary, reconciliation is the only path.** An item with
`boundary_crossed = true` becomes `UNCERTAIN`, its attempt is `ATTEMPTED_OUTCOME_UNKNOWN`, and
reconciliation (`failure-recovery-race-model.md` §6.1) is **mandatory** — whatever the step's
retry class, and whether or not the provider deduplicates. Where reconciliation cannot answer, the
item is `ABANDONED`, the run `BLOCK`s and `ESCALATE`s, and a retry request against the step is
branch **R6**. Where it answers `CONFIRMED_APPLIED` and the effect must be undone, that is
compensation — its own governed act. Where it answers `CONFIRMED_NOT_APPLIED`, continuation is a
**new** governed attempt under PO-14, not a replay of this one. Absence of evidence that the
effect occurred is never evidence that it did not.

**Rule PO-17 — no distributed transaction and no exactly-once.** The protocol is at-most-once
locally (`O1`–`O5` with U8 and U22): each dispatch item crosses the provider boundary **at most
once**, because the crossing is recorded before it happens and is never repeated. Externally it is
therefore at-most-once-per-item and **nothing stronger** — not exactly-once, and not
at-least-once, since a lost call is resolved by reconciliation and by a new governed attempt
rather than by redelivery. Nothing above spans the local database and the provider in one
transaction.

### 9.6 The five crash points

| Crash point | Durable state found | Recovery |
|---|---|---|
| **Before the claim** | `PENDING`, unowned, `boundary_crossed = false` | T1. Nothing left the system |
| **After the claim, before the dispatch intent** | `CLAIMED`, `boundary_crossed = false`, lease expired | **T6** back to `PENDING`. Nothing left the system, because no call is ever made from `CLAIMED` (PO-8) |
| **At the call boundary — after `DISPATCH_PENDING` commits, before or during the call** | `DISPATCH_PENDING`, `boundary_crossed = true`, lease expired | **T7** to `UNCERTAIN`; attempt `ATTEMPTED_OUTCOME_UNKNOWN`; **reconciliation, never redispatch** — PO-14 admits no exception, and a provider's deduplication guarantee is not one (PO-14b) |
| **After provider acceptance, before local outcome persistence** | Identical to the row above, and deliberately so: an outcome the system did not commit is an outcome the system does not have | **T7**, as above |
| **During reconciliation** | `UNCERTAIN`, unowned | Re-run the sweep. T8 on an answer, T9 where it remains unanswerable. Reconciliation is idempotent and records determinations of fact; it decides nothing (F-11) |

**Rule PO-18 — the durable unknown path.** `ATTEMPTED_OUTCOME_UNKNOWN` is written onto the
provider attempt in its own local transaction by the recovering drain — never held in the memory
of the process that crashed. That state change is a governed-record mutation and **is** audited;
the accompanying T7 transition beside it is operational and is **not**.

**Rule PO-19 — safe redispatch versus mandatory reconciliation, exactly.**

| Condition | May **this dispatch item** be dispatched (or re-dispatched)? | What happens instead |
|---|---|---|
| `PENDING`, `boundary_crossed = false` | **Yes** — T1 then T2, under its own key | — |
| `CLAIMED`, claim expired, `boundary_crossed = false` | **Yes** — T6 back to `PENDING`, then as above, **same key** (PO-14a). No call was made from `CLAIMED` | — |
| `DISPATCH_PENDING` | **Never** | T7 to `UNCERTAIN`; mandatory reconciliation |
| `UNCERTAIN`, reconciliation says `CONFIRMED_APPLIED` | **Never** | T8 to `SETTLED`. Undoing the effect, if required, is compensation — its own governed act |
| `UNCERTAIN`, reconciliation says `CONFIRMED_NOT_APPLIED` | **Never** | T8 to `SETTLED`. Continuation is a **new** governed provider attempt at the next ordinal, with a **new** key (PO-14) |
| `UNCERTAIN`, reconciliation unanswerable | **Never** | T9 to `ABANDONED`; the run blocks and escalates; a retry request is branch R6 |
| `ABANDONED` | **Never**, under any condition | As above |
| `SETTLED` | **Never** — terminal | — |

Read down the second column: after `boundary_crossed = true` it is `Never` in every row, with no
condition attached. That uniformity is the point of choosing this architecture, and it is what
makes the rule checkable rather than a judgement call at three in the morning.

## 10. Retention, holds and deletion

Six deletion acts are distinguished, and **none of them deletes an audit or canonical record**:

| Act | Effect |
|---|---|
| Soft state change | A lifecycle state change; nothing removed |
| Content expiry under a retention class | Bytes expire; the record and its history remain |
| Orphan quarantine and expiry | An unreferenced object is expired; nothing governed changes |
| Legal-hold-blocked deletion | Refused while a hold is active, for every act above |
| Governed destruction of content | **Requires a mapped Decision Right — none exists** (BA-3) |
| Backup lifecycle | Independent of all of the above |

**Rule P-22.** `backup != archive != audit`. A backup is a recovery mechanism, an archive is a
retention state, and an audit record is governance history. None substitutes for another.

## 11. Supabase position

PostgreSQL is the specified operational store. Supabase is **one implementation option** for
hosting it and is not architecture identity. Where a Supabase-specific capability is used it is
labelled as an option and must have a stated plain-PostgreSQL equivalent:

| Supabase capability | Plain-PostgreSQL equivalent | Governance note |
|---|---|---|
| Row Level Security policies | PostgreSQL RLS (the same feature) | **RLS is enforcement, not authority** |
| Service-role key | A database role with elevated grants | **A credential, not human authority** |
| Auth/user table | An external identity provider projection | An identity is not an authority |
| Storage buckets | Any S3-compatible object store | Bytes only |
| Edge functions | Any application runtime | No governance logic may live only there |

**Rule P-23.** No governed invariant may depend on a capability unique to one hosted product. An
invariant that cannot be expressed in plain PostgreSQL plus application code is redesigned.

## 12. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | Uniqueness held in a closure-backed in-memory list | The durable constraints of §5.2 | Phase 14 §4.2; process memory does not survive a restart or a second process |
| D2 | No concurrency tokens | `record_version` on every mutable governed row, version-pinned writes | Phase 10 §5; Phase 11 races 2, 3, 7 |
| D3 | No object storage protocol | §8 staged commit with orphan quarantine | Phase 10 `versioning-and-lineage.md` §6 |
| D4 | No outbox, no external-effect uncertainty | §9, and O-29 | Phase 14 §4.4, §7 |
