# Source-of-Truth Matrix

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

Exactly one system is authoritative for each data class. A second representation is a **projection**. A projection **is never written by anything but its projector**, is never the target of a governed write, and when it disagrees with its source it is a defect to be reconciled, never a version to be merged.

`GITHUB` = the governed repository. `DB` = the operational PostgreSQL database. `OBJECT` = object storage. `SECRETS` = the external secret manager. `NONE` = deliberately not authoritative anywhere, stated in the row.

## 1. The matrix

| # | Data class | Authoritative | Secondary representation | Replication | Versioning authority | Write authority | Canonical promotion implication | Conflict resolution |
|---:|---|---|---|---|---|---|---|---|
| 1 | System standards and architecture documents | `GITHUB` | `DB` index of document ID, version, approval baseline | Allowed, read-only projection | Git commit + declared document version | Human authors via reviewed commit | None. An architecture document is never promoted to canonical by being stored | Repository wins; the projection is rebuilt |
| 2 | Role Registry (definitions) | `GITHUB` | `DB` registry mirror for querying and referential integrity | Allowed, read-only projection | Git commit + Role Card version | Human authors via reviewed commit | None | Repository wins; mirror rebuilt from the approved baseline |
| 3 | Skill Registry (definitions) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Skill Card version | Human authors via reviewed commit | None | Repository wins |
| 4 | Review Profile Registry (definitions) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Profile version | Human authors via reviewed commit | None | Repository wins |
| 5 | Workflow Registry (definitions) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Workflow version | Human authors via reviewed commit | None | Repository wins |
| 6 | Decision Rights Register (carded Rights) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Right version | **Phase 7 carding governance only** | None. **A Right is never created by a database write** | Repository wins; a mirrored Right absent from the repository is quarantined, never honoured |
| 7 | Knowledge / Canonical governance records | `DB` | `OBJECT` for attached payloads; `GITHUB` for the governing rules only | Not replicated | Record version + Phase 8 lifecycle | Governed promotion path under Phase 8 | **This is where promotion is recorded.** Storage records it; it never causes it | Database wins; a divergent payload is quarantined |
| 8 | Model Registry / Provider / Deployment Profiles | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Registry Profile Version | Human authors via reviewed commit | None | Repository wins |
| 9 | Routing Policies | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + policy version | Human authors via reviewed commit | None | Repository wins |
| 10 | Routing Decisions | `DB` | None | Not replicated | Append-only; no version — a correction is a new linked record | The routing act, recorded once | None. **A Routing Decision is not a Decision Record** | Append-only: there is nothing to conflict. A duplicate is quarantined |
| 11 | Handoff records | `DB` | None | Not replicated | Append-only with status transitions recorded separately | The handoff act | None | Database wins; append-only |
| 12 | Review instances and findings | `DB` | `OBJECT` for attached evidence files | Not replicated | Append-only findings; status transitions recorded as events | The review act, by the reviewing identity | None. A finding does not promote anything | Database wins; append-only |
| 13 | Decision Records | `DB` | None | Not replicated | **Append-only, never amended** | Exercise of a carded Phase 7 Right by an eligible human | Records the decision; the promotion it may authorise is recorded separately | Append-only. A correction is a new record naming the one it corrects |
| 14 | Memory items | `DB` | `OBJECT` for large payloads | Not replicated | Record version + Phase 8 freshness fields | Governed write path | None by themselves | Database wins |
| 15 | Source / evidence metadata | `DB` | `OBJECT` for the source document itself | Not replicated | Record version | Governed write path | None. Evidence is not a claim | Database wins; a metadata row whose object is missing is quarantined |
| 16 | File and binary artifacts — **bytes** | `OBJECT` | Content hash recorded in `DB` | Versioned objects, never overwritten | Object version + content hash | Upload, then the metadata commit that makes it visible | None | Hash mismatch quarantines the object; the record is authoritative for what *should* be there |
| 17 | File and binary artifacts — **metadata and identity** | `DB` | None | Not replicated | Artifact record version | Governed write path | None | Database wins. **Bytes without a record are orphaned, not stored** |
| 18 | Runtime logs and events | `DB` (bounded metadata) or the operational log sink | None | Not replicated | None — not versioned | The emitting system | **None, ever.** An event is not evidence and not a decision | No resolution: an operational log is not a source of truth and nothing depends on it |
| 19 | Secrets and credentials | `SECRETS` | **Reference only** in `GITHUB` and `DB` | **Never replicated** | The secret manager's own version/rotation record | The secret manager, under human authorisation | None | No conflict is possible: neither other system holds a value to conflict |
| 20 | Configuration | Split, stated per item: governed configuration in `GITHUB`; environment-specific values in the environment, secret-valued items in `SECRETS` | `DB` may record which configuration version an environment is at | Allowed for the recorded version only | Git commit for governed configuration | Human authors; environment operators for environment values | None | Repository wins for governed configuration; the environment's own record wins for what it is currently running, and a mismatch **blocks** |
| 21 | Generated reports, exports, backups and snapshots | `OBJECT` | `DB` record of what was produced, from which state, when, by whom | Backups replicated per the backup regime | Snapshot version; immutable once written | The producing process | None. **A report is a derivative, never a source** | The source state wins. A derivative that disagrees is regenerated, never reconciled into the source |

## 2. Why registry definitions live in the repository

The alternative — authoring registry definitions directly in the database — was considered and rejected. A Role Card, a Decision Right or a Review Profile is a **governed document with a review history**, and the repository already provides the thing that makes it governable: attributable authorship, reviewable diffs, immutable history and an approval record naming a commit. Reproducing that inside the database would rebuild a worse version of it.

The database's job is what the repository is bad at: querying across registries, enforcing referential integrity between records and definitions, and holding operational state that changes far faster than an architecture does.

> **Consequence, stated rather than discovered:** the registry mirror is **derived**. It is rebuilt from an approved baseline, it is never the target of a governed write, and an application that writes to it has committed the defect this matrix exists to prevent.

## 3. No dual master

Each row names exactly **one** authoritative system. Row 20 names a split, and the split is **by item, not by copy**: no single configuration item is authoritative in two places. The Phase 10 validator parses this table and fails on any row whose authoritative cell names more than one system, on any row lacking a conflict rule, and on any row claiming replication of a class the standard forbids replicating.

## 4. What replication does not mean

Replication is permitted only where it is a **read-only projection of an approved baseline**. It never means:

- that the projection may be written and reconciled back;
- that the projection may be read when it is known to be stale against its baseline;
- that a governed decision may cite the projection rather than the source.

A record citing a registry definition cites the **stable logical ID and version**, which resolve identically in both. That is the only reason the projection is safe to query.
