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

### 9.2 The dispatch item — stable identity and durable uniqueness

| # | Field | Is |
|---:|---|---|
| 1 | `outbox_ref` | The **stable identity** of one dispatch item, assigned in the enqueuing transaction and never reassigned |
| 2 | `model_invocation_ref` | The governed intent this dispatch item serves |
| 3 | `provider_attempt_ref` | The **one** provider attempt this dispatch item resolves |
| 4 | `provider_idempotency_key` | The key presented to the provider. Stable for the life of the row |
| 5 | `claim_state` | One of the five values of §9.3 |
| 6 | `lease_owner` | The claimant service identity holding the current lease, or `NULL` |
| 7 | `lease_expires_at` | When the current lease stops being valid, or `NULL` |
| 8 | `claim_token` | The compare-and-swap / OCC token. It changes on **every** claim-state transition |
| 9 | `dispatch_ordinal` | How many times this item has been claimed. Monotonic, never reset |

The outbox's durable uniqueness constraints are **operational** and are deliberately **not**
rows of the canonical governed uniqueness inventory of §5.2, because an outbox row is not a
governed record. They are named `O1`–`O4` so that no count of the `U` inventory changes:

| # | Constraint | Prevents |
|---:|---|---|
| O1 | `UNIQUE (outbox_ref)` | A duplicate dispatch identity |
| O2 | `UNIQUE (provider_attempt_ref)` | Two dispatch items racing to satisfy one provider attempt |
| O3 | `UNIQUE (provider_idempotency_key)` | Two items presenting one key to the provider |
| O4 | A partial unique index on `outbox_ref` `WHERE claim_state = 'CLAIMED' AND lease_expires_at > now()` | **Two concurrently valid leases on one dispatch item** |

**Rule P-23 — the provider idempotency key is stable and never regenerated.** It is derived in
the enqueuing transaction from `(model_invocation_ref, provider_attempt_ref)` and stored. Every
dispatch of the item — including a redelivery after an expired lease — presents the **same**
key. Regenerating it on redelivery is the defect that silently converts "the provider
deduplicates" into "the provider sees a new request".

### 9.3 Claim state vocabulary

`PENDING` · `CLAIMED` · `DISPATCHED` · `SETTLED` · `ABANDONED`

| State | Means | Leaves to |
|---|---|---|
| `PENDING` | Enqueued; no claimant | `CLAIMED` |
| `CLAIMED` | A claimant holds a valid lease; **no call has been made under this claim** | `DISPATCHED`; or back to `PENDING` on lease expiry |
| `DISPATCHED` | The call was made under this claim; the outcome is not yet durable | `SETTLED`; or `ABANDONED` on lease expiry |
| `SETTLED` | The provider attempt reached a recorded external-effect state | — |
| `ABANDONED` | A lease expired at or after dispatch. **The item is never re-dispatched from here** | Reconciliation only |

### 9.4 Claim, lease and compare-and-swap

**Rule P-24 — claiming is one atomic conditional update, or it did not happen.** A claimant
acquires an item with a single statement whose precondition is

> `claim_state = 'PENDING'` **and** (`lease_expires_at IS NULL` **or** `lease_expires_at <= now()`)
> **and** `claim_token` equals the token the claimant read

and whose effect is `claim_state = 'CLAIMED'`, `lease_owner` = the claimant service identity,
`lease_expires_at = now() + lease_duration`, a **new** `claim_token`, and
`dispatch_ordinal + 1`. Zero rows updated means another claimant won, and the loser does **not**
call the provider. There is no read-then-write path and no advisory lock substituting for the
compare-and-swap.

**Rule P-25 — the claimant is a named service identity.** `lease_owner` holds the acting service
identity of `security-identity-access.md`, never a hostname, a process id or a worker number. A
lease whose owner does not resolve to a registered service identity is not a valid lease.

**Rule P-26 — at most one valid lease, enforced durably.** Constraint **O4** is the enforcement;
the drain's control flow is not. Two claimants believing they hold one item is a **failed write**
for the second, never two provider calls.

**Rule P-27 — an expired lease is a redelivery condition, never a proof.** An item becomes
claimable again on expiry **only from `CLAIMED`**, because in `CLAIMED` no call was made under
that claim. From `DISPATCHED`, expiry moves the item to `ABANDONED` and the provider attempt to
`ATTEMPTED_OUTCOME_UNKNOWN`. **Lease expiry is never evidence that no external effect
occurred** — Rule F-9a says the same thing from the failure model's side, and it is the single
place where an optimistic reading would produce a duplicate external effect.

### 9.5 Deduplication at the receiver

**Rule P-28 — where the provider deduplicates, redelivery is at-least-once and safe.** The
stable key of Rule P-23 is presented on every dispatch, and the provider's own deduplication
makes a second arrival a no-op. This is `IDEMPOTENT_AT_LEAST_ONCE`, and the guarantee is the
**receiver's**, not the sender's.

**Rule P-29 — where the provider does not deduplicate, there is no safe redispatch after
dispatch.** The step is `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT`. An item that reached `DISPATCHED`
is never re-dispatched: it becomes `ABANDONED`, its attempt is `ATTEMPTED_OUTCOME_UNKNOWN`, and
reconciliation (`failure-recovery-race-model.md` §6.1) is **mandatory**. Where reconciliation
cannot answer, the run `BLOCK`s and `ESCALATE`s, and a retry request against that step is
branch R6.

**Rule P-30 — no distributed transaction and no exactly-once.** The protocol is at-most-once
locally (O1–O4 with U8 and U22), at-least-once externally where the provider deduplicates, and
neither where it does not. Nothing above spans the local database and the provider in one
transaction, and no delivery guarantee stronger than the receiver's is claimed.

### 9.6 The four crash points

| Crash point | Durable state found | Recovery |
|---|---|---|
| **Before the claim** | `PENDING`, no valid lease | Ordinary claim. Nothing left the system |
| **After the claim, before the call** | `CLAIMED`, lease expired | Re-claimable under Rule P-27. Nothing left the system, because the call happens strictly after the claim commits |
| **After the call, before the outcome** | `DISPATCHED`, lease expired | `ABANDONED`; the attempt becomes `ATTEMPTED_OUTCOME_UNKNOWN`; **reconciliation, never redispatch** |
| **After the outcome, before persistence commits** | `DISPATCHED`, lease expired, no outcome row | Identical to the row above, deliberately: an outcome the system did not commit is an outcome the system does not have |

**Rule P-31 — the durable unknown path.** `ATTEMPTED_OUTCOME_UNKNOWN` is written onto the
provider attempt in its own local transaction by the reclaiming drain — never held in the memory
of the process that crashed. That state change is a governed-record mutation and **is** audited;
the accompanying outbox transition to `ABANDONED` is operational and is **not**.

**Rule P-32 — safe redispatch versus mandatory reconciliation, exactly.**

| Condition | Redispatch permitted? |
|---|---|
| `claim_state = 'PENDING'` | **Yes** |
| `claim_state = 'CLAIMED'` with an expired lease | **Yes** — no call was made under that claim |
| `DISPATCHED` or `ABANDONED`, provider deduplicates on the stable key | **Only** after reconciliation reports `CONFIRMED_NOT_APPLIED` |
| `DISPATCHED` or `ABANDONED`, provider does not deduplicate | **Never.** Reconciliation is mandatory |
| Any state, reconciliation unanswerable | **Never.** The run blocks and escalates; undoing a confirmed effect is compensation, its own governed act |

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
