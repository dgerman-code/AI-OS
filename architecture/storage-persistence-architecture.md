# Storage and Persistence Architecture

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`
Human-approved Phase 9 baseline: `a94de435f0a47f9910d804029cc74bb7c995434a`

Phase 10 answers one question: **where does each thing the approved architecture describes actually live, and which system is allowed to say what it is.** It adds no governance semantics. Where it appears to, that is a defect.

## 1. Three layers, three different jobs

| Layer | What it is authoritative for | What it must never become |
|---|---|---|
| **GitHub** | Governed architecture, standards, templates, registry **definitions**, policies, schemas and migrations as source; human approval records; the review and audit trail of the architecture itself | The operational database. It answers what the system *is*, never what happened at 14:02 |
| **PostgreSQL** (currently via Supabase) | Operational governance **records** and their relationships, lifecycle, lineage and queryable state | The architecture's source. A row asserting a Role's competence is a projection, not a definition |
| **Object storage** | The **bytes** of files and large artifacts, and their immutable snapshots | The artifact registry. It holds content; it knows nothing about what the content means |

Everything else in Phase 10 follows from keeping those three jobs apart.

## 2. The identity boundary

> **`REPOSITORY OBJECT != DATABASE RECORD != FILE OBJECT != ARTIFACT != CANONICAL RECORD != DECISION RECORD != RUNTIME EVENT != SECRET != CREDENTIAL`**

Nine objects, and the collapse of any pair is a governance failure rather than an implementation shortcut:

| Denial | What collapsing it would destroy |
|---|---|
| `REPOSITORY OBJECT != DATABASE RECORD` | The distinction between what the architecture says and what the system did |
| `DATABASE RECORD != FILE OBJECT` | The ability to know an object is missing — bytes with no record are invisible, a record with no bytes is detectable |
| `FILE OBJECT != ARTIFACT` | Artifact identity would become a path, and a path is an address that changes |
| `ARTIFACT != CANONICAL RECORD` | A file would become true by being stored |
| `CANONICAL RECORD != DECISION RECORD` | Phase 8's promotion and Phase 7's authority would merge |
| `DECISION RECORD != RUNTIME EVENT` | Something happening would become something being authorised |
| `RUNTIME EVENT != SECRET` | Event payloads would become an exfiltration surface by default |
| `SECRET != CREDENTIAL` | A rotated value and the identity that uses it would share a lifecycle, and revocation would lose its meaning |

### 2.1 Seven facets, separately recorded

A stored governed object carries seven things that are routinely confused with one another. Each is recorded separately, and none is derivable from another:

| Facet | What it answers | What it is not |
|---|---|---|
| **Logical object identity** | Which governed object this is | Not the row, not the path, not the hash |
| **Storage location** | Where a representation currently sits | Not identity — it changes without the object changing |
| **Version identity** | Which version of that object this is | Not a timestamp, and not a commit |
| **Content hash** | Whether these exact bytes are unchanged | Not identity, and not authenticity of the claim the bytes make |
| **Mutable metadata** | Display name, tags, operational annotations | Not governed content — changing it changes nothing governed |
| **Immutable audit/history record** | What happened to the object and who did it | Not the object, and never rewritten with it |
| **Runtime instance / event identity** | Which execution touched it | Not the governed act, which is recorded separately or did not occur |

A storage backend that can assign, infer or overwrite the first, third or sixth of these is out of bounds.

## 3. What Phase 10 inherits and does not touch

| Inherited | From | Treatment |
|---|---|---|
| Role / Skill / Workflow / Handoff separation | Phases 3–6 | Persisted as defined. **No Role Card, Skill Card or Workflow is modified**, and no database column grants any of them authority |
| Review Profiles and reviewer independence | Phase 6 | Persisted. Independence is a property of the review, never of the database identity that wrote the row |
| Decision Rights and append-only decision history | Phase 7 | Persisted append-only. **No Right is carded, granted, widened or implied by a grant, a policy or a service account** |
| Sensitivity classes, freshness, origin, `AI_SUGGESTION`, terminal `RETRACTED` | Phase 8 | Used unchanged. No new class, no ordering, no new terminal state |
| Model / Provider / Deployment / Routing Policy / Routing Decision identity and the six-part reproducibility set | Phase 9 | Persisted so that a historical Routing Decision reconstructs **exactly** the references it used |
| `ROUTER != ORCHESTRATOR` | Phase 9 | Preserved. Phase 10 stores records; it schedules, retries and sequences nothing |

## 4. Inventory

| Vocabulary | Members | Owner document |
|---|---|---|
| Identity denials | **9** | This document §2 |
| Identity facets | **7** | This document §2.1 |
| Source-of-truth rows | **21** | `storage/source-of-truth-matrix.md` |
| Data domains | **10** | `storage/data-domain-model.md` |
| Identifier kinds | **5** | `storage/versioning-and-lineage.md` §1 |
| Version planes | **6** | `storage/versioning-and-lineage.md` §2 |
| Artifact record fields | **22** | `storage/artifact-object-model.md` |
| Hash uses | **4** | `storage/artifact-object-model.md` §4 |
| Access dimensions | **7** | `storage/access-control-and-rls-boundary.md` §2 |
| Audit event fields | **11** | `storage/audit-provenance-model.md` §2 |
| History kinds | **4** | `storage/audit-provenance-model.md` §1 |
| Consistency boundaries | **6** | `storage/versioning-and-lineage.md` §5 |
| Deletion acts | **6** | `storage/backup-retention-recovery.md` §4 |
| Failure modes | **15** | `storage/failure-modes.md` |
| Environments | **3** | `storage/migration-and-environment-governance.md` §3 |
| Adapter boundaries | **5** | This document §8 |
| Common storage constraints | **31** | `storage/_standards/common-storage-governance-constraints.md` |
| Templates | **3** | `storage/_templates/` |
| Exemplars | **5** | `storage/exemplars/` |

## 5. GitHub's boundary

GitHub is authoritative for **definitions** and for the **history of the architecture**. Its semantics are used as they are, not reinvented:

- a **commit** is an immutable point in the architecture's history;
- a **branch** isolates a phase's proposed work until it is approved;
- a **tag** may mark an approved baseline, but the approval itself is a committed record (`reviews/phase-N-final-approval.md`), because a tag is movable and an approval is not;
- **history is never rewritten** on a branch carrying an approval record.

### 5.1 Architecture versus executable code

The repository holds both, and the line between them is enforced rather than assumed: architecture documents, standards, templates, registry definitions, policies, schema definitions and migration files are **governed content**; validation harnesses are **tooling that reads governed content and implements no part of the system**; anything that would execute a part of AI-OS in production is neither, and does not exist yet.

### 5.2 Schema and migration references

The repository versions migrations. It does **not** hold, mirror or reconstruct the operational database's state. What it records is the **compatibility declaration**: which schema versions this architecture revision expects. What the environment records is which migration was actually applied, when, by which identity, and with which outcome. Reading one as the other is the defect §5.3 exists to prevent.

### 5.3 Branch protection is a requirement, not an observation

Phase 10 states the **architectural requirement** — approval records and their baselines must not be rewritable, and a human approval must be attributable to a person. Whether the forge is currently configured to enforce that is **runtime configuration, not architecture**, is not observable from inside this repository, and is therefore **not claimed** anywhere in Phase 10. The Phase 10 validator asserts the requirement is stated; it asserts nothing about the forge.

### 5.4 What must never be in the repository

Secret values, private keys, access tokens, connection strings containing credentials, raw sensitive source payloads, personal data, privileged material, customer content, and any database dump. The Phase 10 validator scans for these, and its scan is the reason this list is short and specific rather than a caution.

## 6. Human control

Three acts belong to humans and to no stored process:

1. **Approval of an architecture baseline** — recorded in the repository as a committed record naming a commit, and never inferred from a merge, a tag or a green check.
2. **Authorisation of a destructive or high-risk migration** — a Phase 7 Decision Right exercised before the migration exists.
3. **Authorisation of a physical purge, a legal hold, or a restore into a governed environment** — each a named decision with a recorded reason.

Four things no storage act reaches: **the truth of stored content**; **a review's outcome**; **a canonical promotion**; **an authority that Phase 7 did not card**.

## 7. Reproducibility

A historical record must reconstruct what it referenced. Concretely: a Routing Decision retains the Phase 9 six-part reproducibility set as **literal recorded values**, not as foreign keys into current rows — because a foreign key resolves to what the object is *now*, and the question asked afterwards is what it was *then*. The same rule governs Decision Records, canonical promotions and review findings: **every governed record stores the referenced identity and version as recorded values, and any join to current state is an enrichment, never the record.**

## 8. Anti-lock-in: five adapter boundaries

| Surface | What is portable | What is vendor-specific and isolated |
|---|---|---|
| **Relational store** | ANSI/PostgreSQL semantics: tables, constraints, transactions, row-level security as a concept | Backend-specific extensions, managed conveniences, generated client libraries |
| **Object storage** | Bucket/prefix/key addressing, object versioning, immutability retention, server-side encryption | Provider-specific lifecycle, event and replication features |
| **Secret management** | Reference-by-name resolution, rotation, revocation, audit | The particular vault or manager |
| **Git host** | Commits, branches, tags, review history | Forge-specific automation, checks and protection configuration |
| **Authorisation** | Declared access dimensions and deny-by-default evaluation | The backend's own policy language and session context mechanics |

Supabase is the **current** PostgreSQL and object-storage implementation. No governance semantic in Phases 1–10 depends on a Supabase-specific feature; where one is used it sits behind the relevant boundary above, and the Phase 10 validator checks that the governance documents do not reach across it.

## 9. Not built in Phase 10

| Not built | Why |
|---|---|
| Any live Supabase project, table, bucket or policy | Architecture phase. Nothing was connected to, created or deployed |
| SQL DDL or migration files | The migration **governance** is defined; the migrations themselves follow approval |
| Service accounts, credentials or secrets | §5.4 and `storage/access-control-and-rls-boundary.md` |
| An API, client or SDK | Runtime |
| An orchestrator, queue or scheduler | Phase 11 — `ROUTER != ORCHESTRATOR` and neither is a storage layer |
| RAG, embeddings or an index design | A retrieval system is a consumer of this architecture, not part of it |
| Real Model, Provider or Deployment Profiles | Phase 9 did not create them and Phase 10 does not |
| Concrete RPO/RTO numbers | Not derivable from architecture; recovery **classes** are defined instead |
