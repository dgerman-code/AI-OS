# Source-of-Truth Matrix

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

Exactly one system is authoritative for each data class. A second representation is a **projection**. A projection **is never written by anything but its projector**, is never the target of a governed write, and when it disagrees with its source it is a defect to be reconciled, never a version to be merged.

## 0. Two controlled vocabularies

The independent audit found that prose in the authority and conflict columns could say anything, and that a validator counting known substrings would miss what it did not already know to look for. Both columns are therefore **closed vocabularies**, declared here, parsed from these tables by the harness, and fail-closed: a cell that is not exactly one declared authority, or that carries no declared conflict outcome, is a **defect**.

### 0.1 Authority vocabulary

Every row's authority cell is **exactly one** of these tokens and nothing else. There is no `A or B`, no slash, no comma-separated pair, no fallback authority and no prose.

| Token | Meaning |
|---|---|
| `GITHUB` | The governed repository |
| `DB` | The operational PostgreSQL database |
| `OBJECT` | Object storage |
| `SECRETS` | The external secret manager |
| `ENV` | The environment's own configuration record — what that environment is actually running |
| `NONE` | **Deliberately not a governed source-of-truth class.** Telemetry, and nothing governed may depend on it |

A data class that would need two authorities is not one data class. **It is split into rows until each row has one** — which is what §1 rows 18/19 and 21/22/23 are.

### 0.2 Conflict outcome vocabulary

Every row's conflict cell **begins with one or more of these tokens** and then explains it. The syntax is fixed, so that "begins with" is a parse rather than a reading:

```
conflict cell := OUTCOME ( ", " ["then "] OUTCOME )*  [ " — " explanation ]
OUTCOME       := a declared token, written as a code span
```

A cell of prose alone carries no outcome and fails, however well written — including a cell that states at length that it has no conflict rule. **A cell that opens with prose fails even if it names a valid outcome later**: a token quoted mid-sentence as an illustration is an example, not a rule, and the approval re-audit was right that a parser extracting one from anywhere had stopped enforcing this paragraph.

| Outcome | Meaning |
|---|---|
| `AUTHORITY_WINS` | The authoritative system's value stands; the secondary is wrong |
| `SECONDARY_REBUILT` | The projection is discarded and rebuilt from the authoritative source |
| `QUARANTINE` | The divergent object or record is made unreadable to normal access pending assessment |
| `RECONCILE` | A bidirectional sweep determines which side is incomplete and acts per `storage/failure-modes.md` |
| `BLOCK_AND_ESCALATE` | The operation stops and a human is required |
| `APPEND_ONLY_NO_CONFLICT` | The class is append-only, so there is no prior value to conflict with; a duplicate is quarantined |
| `NOT_APPLICABLE_NO_SECONDARY` | No secondary representation exists, so no conflict is possible |
| `NOT_A_SOURCE_OF_TRUTH` | The class is non-authoritative telemetry; there is nothing to resolve because nothing governed reads it |
| `REGENERATE_DERIVATIVE` | The derivative is regenerated from the source state and never reconciled back into it |

**No outcome permits a secondary representation to overwrite an authoritative one.** Last-write-wins is absent from this vocabulary deliberately, and the harness scans for it.

## 1. The matrix

| # | Data class | Authoritative | Secondary representation | Replication | Versioning authority | Write authority | Canonical promotion implication | Conflict resolution |
|---:|---|---|---|---|---|---|---|---|
| 1 | System standards and architecture documents | `GITHUB` | `DB` index of document ID, version, approval baseline | Allowed, read-only projection | Git commit + declared document version | Human authors via reviewed commit | None. An architecture document is never promoted to canonical by being stored | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` — the repository stands and the projection is rebuilt |
| 2 | Role Registry (definitions) | `GITHUB` | `DB` registry mirror for querying and referential integrity | Allowed, read-only projection | Git commit + Role Card version | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` — the mirror is rebuilt from the approved baseline |
| 3 | Skill Registry (definitions) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Skill Card version | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` |
| 4 | Review Profile Registry (definitions) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Profile version | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` |
| 5 | Workflow Registry (definitions) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Workflow version | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` |
| 6 | Decision Rights Register (carded Rights) | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Right version | **Phase 7 carding governance only** | None. **A Right is never created by a database write** | `AUTHORITY_WINS`, then `QUARANTINE` — a mirrored Right absent from the repository is quarantined, **never honoured** |
| 7 | Knowledge / Canonical governance records | `DB` | `OBJECT` for attached payloads; `GITHUB` for the governing rules only | Not replicated | Record version + Phase 8 lifecycle | Governed promotion path under Phase 8 | **This is where promotion is recorded.** Storage records it; it never causes it | `AUTHORITY_WINS`, then `QUARANTINE` — a divergent payload is quarantined |
| 8 | Model Registry / Provider / Deployment Profiles | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + Registry Profile Version | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` |
| 9 | Routing Policies | `GITHUB` | `DB` registry mirror | Allowed, read-only projection | Git commit + policy version | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` |
| 10 | Routing Decisions | `DB` | None | Not replicated | Append-only; no version — a correction is a new linked record | The routing act, recorded once | None. **A Routing Decision is not a Decision Record** | `APPEND_ONLY_NO_CONFLICT`, then `QUARANTINE` — there is no prior value to conflict with; a duplicate is quarantined |
| 11 | Handoff records | `DB` | None | Not replicated | Append-only with status transitions recorded separately | The handoff act | None | `APPEND_ONLY_NO_CONFLICT` — there is no prior value to conflict with |
| 12 | Review instances and findings | `DB` | `OBJECT` for attached evidence files | Not replicated | Append-only findings; status transitions recorded as events | The review act, by the reviewing identity | None. A finding does not promote anything | `APPEND_ONLY_NO_CONFLICT` — there is no prior value to conflict with |
| 13 | Decision Records | `DB` | None | Not replicated | **Append-only, never amended** | Exercise of a carded Phase 7 Right by an eligible human | Records the decision; the promotion it may authorise is recorded separately | `APPEND_ONLY_NO_CONFLICT` — a correction is a new record naming the one it corrects |
| 14 | Memory items | `DB` | `OBJECT` for large payloads | Not replicated | Record version + Phase 8 freshness fields | Governed write path | None by themselves | `AUTHORITY_WINS` |
| 15 | Source / evidence metadata | `DB` | `OBJECT` for the source document itself | Not replicated | Record version | Governed write path | None. Evidence is not a claim | `AUTHORITY_WINS`, then `QUARANTINE` — a metadata row whose object is missing is quarantined |
| 16 | File and binary artifacts — **bytes** | `OBJECT` | Content hash recorded in `DB` | Versioned objects, never overwritten | Object version + content hash | Upload, then the metadata commit that makes it visible | None | `QUARANTINE`, then `RECONCILE` — a hash mismatch quarantines the object; the record is authoritative for what **should** be there |
| 17 | File and binary artifacts — **metadata and identity** | `DB` | None | Not replicated | Artifact record version | Governed write path | None | `AUTHORITY_WINS`, then `QUARANTINE` — **bytes without a record are orphaned, not stored** |
| 18 | Bounded runtime-event / correlation metadata | `DB` | None | Not replicated | Not versioned; retained by retention class | The emitting system | **None, ever.** Correlation metadata is not evidence and not a decision | `APPEND_ONLY_NO_CONFLICT` — append-only, so there is no prior value to conflict with; a duplicate correlation record is `QUARANTINE`d. **No governed record may cite this class as a reason** |
| 19 | Operational logs (telemetry and diagnostics) | `NONE` | None | Not replicated | Not versioned; rotated, sampled and discarded | The emitting system | **None, ever** | `NOT_A_SOURCE_OF_TRUTH` — this class is deliberately not authoritative for anything. Nothing governed reads it, so there is nothing to resolve. **Anything that must survive is recorded in row 18 or in the `audit` domain instead, and a log is never promoted into either** |
| 20 | Secrets and credentials | `SECRETS` | **Reference only** in `GITHUB` and `DB` | **Never replicated** | The secret manager's own version/rotation record | The secret manager, under human authorisation | None | `NOT_APPLICABLE_NO_SECONDARY` — neither other system holds a value, so no conflict is possible |
| 21 | Governed configuration | `GITHUB` | `DB` record of which configuration version an environment is at | Allowed for the recorded version only | Git commit | Human authors via reviewed commit | None | `AUTHORITY_WINS`, then `SECONDARY_REBUILT` — the repository defines the governed configuration and the recorded version is rebuilt from it |
| 22 | Environment-specific configuration values | `ENV` | `DB` record of the version in force | Allowed for the recorded version only | The environment's own change record | Environment operators | None | `BLOCK_AND_ESCALATE` — the environment is authoritative for what it is running, and a mismatch against the repository's declared compatibility window **blocks rather than degrades** |
| 23 | Secret-valued configuration items | `SECRETS` | **Reference only** | **Never replicated** | The secret manager's own rotation record | The secret manager, under human authorisation | None | `NOT_APPLICABLE_NO_SECONDARY` — a reference is not a value, so there is nothing to diverge |
| 24 | Generated reports, exports, backups and snapshots | `OBJECT` | `DB` record of what was produced, from which state, when, by whom | Backups replicated per the backup regime | Snapshot version; immutable once written | The producing process | None. **A report is a derivative, never a source** | `REGENERATE_DERIVATIVE` — the source state stands and the derivative is regenerated, never reconciled into the source |

## 2. Why registry definitions live in the repository

The alternative — authoring registry definitions directly in the database — was considered and rejected. A Role Card, a Decision Right or a Review Profile is a **governed document with a review history**, and the repository already provides the thing that makes it governable: attributable authorship, reviewable diffs, immutable history and an approval record naming a commit. Reproducing that inside the database would rebuild a worse version of it.

The database's job is what the repository is bad at: querying across registries, enforcing referential integrity between records and definitions, and holding operational state that changes far faster than an architecture does.

> **Consequence, stated rather than discovered:** the registry mirror is **derived**. It is rebuilt from an approved baseline, it is never the target of a governed write, and an application that writes to it has committed the defect this matrix exists to prevent.

## 3. No dual master, checked structurally

Each row names **exactly one** authoritative token from §0.1. There is no split row, no compound cell and no prose authority: a data class that would need two authorities has been split into rows until each has one.

The harness parses both vocabularies **out of §0.1 and §0.2 themselves** rather than holding its own copy, then requires every row to resolve. It fails on an authority cell that is not exactly one declared token — including `A or B`, a slash, a comma-separated pair, an unknown phrase, an empty cell, or a telemetry sink promoted into an authority position — and on a conflict cell carrying no declared outcome, however long or well written. Both were passing before the independent audit, and both were real: row 18 named `DB` **or** an operational log sink, and a length-only conflict check accepted a sentence whose content was that no conflict rule existed.

## 4. What replication does not mean

Replication is permitted only where it is a **read-only projection of an approved baseline**. It never means:

- that the projection may be written and reconciled back;
- that the projection may be read when it is known to be stale against its baseline;
- that a governed decision may cite the projection rather than the source.

A record citing a registry definition cites the **stable logical ID and version**, which resolve identically in both. That is the only reason the projection is safe to query.
