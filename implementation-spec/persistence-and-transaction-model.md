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

### 5.2 Required durable uniqueness constraints

Each row is a `UNIQUE` constraint or unique index that **must exist** before the corresponding
act is implementable.

| # | Record | Constraint | Prevents |
|---:|---|---|---|
| U1 | Decision Record | `UNIQUE (decision_record_ref)` | A duplicate identity entering history |
| U2 | Decision Record | `UNIQUE (decision_right_ref, governed_subject, gate_instance_ref, decided_by)` | The same holder deciding the same gate twice under one Right |
| U3 | Review Instance | `UNIQUE (review_instance_ref)` | Duplicate identity |
| U4 | Review Instance | `UNIQUE (review_request_ref, reviewer_identity)` | One reviewer answering one request twice |
| U5 | Routing Decision | `UNIQUE (routing_decision_ref)` | Duplicate identity |
| U6 | Routing Decision | `UNIQUE (routing_request_ref)` | Two decisions answering one request |
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
| U19 | Approval state | `UNIQUE (subject_ref, subject_version) WHERE status = 'ACTIVE'` | Two live approval states for one thing |
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

For every governed act the implementation states six things. The table below specifies the
principal acts; an act not listed inherits the same obligation and must be specified before it is
built.

| Act | Read set | Validation set | Concurrency check | Writes (one transaction) | Uniqueness relied on | Failure before commit |
|---|---|---|---|---|---|---|
| **Create run** | Workflow Definition @v, Orchestrator Policy @v, scope node, approval state | Intake checks 1–7 (§2 of orchestrator contract) | Run-ref availability | `workflow_run`, `scope_binding`, 2 execution events, 1 audit event | U14, U18 | Recorded refusal; **no run row** |
| **Activate stage** | Run state, Workflow Definition @v, task | Halted guard, task in definition, phase plan | Run `record_version` | `work_item`, `gate_instance`(s), execution event | U11, U13 | Nothing written |
| **Assign** | Work Item, bound Task's required Role, attempt counter | Halted guard, role match, agent instance type, insert preflight | Work Item `record_version` | `assignment`, counter update, execution event | U12 | Counter unchanged; no assignment |
| **Route** | Run, Work Item, Routing Policy @v, candidate universe | Halted guard; answer type, request identity, run binding, router identity, six-part completeness; phase plan | Run `record_version` | `routing_request`, `routing_decision`, 2 execution events | U5, U6 | **No routing request and no routing event** |
| **Invoke model** | Recorded Routing Decision, Work Item | Halted guard, decision is this run's, outcome eligible, model/profile lineage, result identity preflight | Run `record_version` | `model_invocation`, `model_result`, execution event | U7, U8 | Nothing written |
| **Review gate** | Gate instance, Review Profile @v, review request | Halted guard, instance lineage, independence class, eligibility class, SoD rules A-4, insert preflight, phase plan | Gate instance `record_version` | `review_instance`, gate outcome, execution event, audit event | U3, U4, U10 | Gate unchanged |
| **Decision gate** | Gate instance, Decision Right @v, holder set, active separations | Halted guard, five gate-satisfaction conditions, 19-element completeness, separation check | Gate instance `record_version` | `decision_record`, gate outcome, execution event, audit event | U1, U2, U10, P-11 | Gate unchanged; **no Decision Record** |
| **Pause** | Run state, interventions | Halted guard, intervention contract, transition preflight (`allow_noop=false`) | Run `record_version` | `human_intervention`, phase transition, execution event | U9 | Nothing written |
| **Cancel / terminate** | Run state, interventions | Terminal reachability, **the same intervention contract**, insert preflight | Run `record_version` | `human_intervention`, terminal state, execution event, audit event | U9 | Nothing written |
| **Scope transfer** | Source run, retained Decision Records, mechanism registry, target definition | All source-side clauses **and** every target-run creation condition, via one shared preflight | Source run `record_version` | Authorisation event, new run, provenance link | U14, U18 | **No authorisation event, no partial run** |
| **Promote to canonical** | Knowledge item @v, evidence, conflicts, freshness, Decision Record | Preconditions 1–9 | Canonical `record_version` | `canonical_record` (new version), prior marked `SUPERSEDED`, audit event | U15 | Nothing written |

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

Where a governed act must both commit locally and cause an external effect:

1. the intent record and an **outbox row** are written **in the same local transaction** as the
   governed act;
2. C16 drains the outbox, performs the external call with the recorded idempotency key, and
   records the execution record and the external-effect uncertainty state;
3. an unknown outcome remains `ATTEMPTED_OUTCOME_UNKNOWN` and enters reconciliation.

**Rule P-20 — the outbox is not a queue product.** It is a table and a drain loop. No queue,
broker, worker framework or event bus is specified, named or required.

**Rule P-21 — the outbox never authorises.** A row in the outbox carries the authorisation
reference; it does not substitute for one. An outbox row for a class-4 act whose authorisation
record is absent is refused at insert by a `NOT NULL` foreign key.

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
| D1 | Uniqueness held in a closure-backed in-memory list | 20 durable constraints, §5.2 | Phase 14 §4.2; process memory does not survive a restart or a second process |
| D2 | No concurrency tokens | `record_version` on every mutable governed row, version-pinned writes | Phase 10 §5; Phase 11 races 2, 3, 7 |
| D3 | No object storage protocol | §8 staged commit with orphan quarantine | Phase 10 `versioning-and-lineage.md` §6 |
| D4 | No outbox, no external-effect uncertainty | §9, and O-29 | Phase 14 §4.4, §7 |
