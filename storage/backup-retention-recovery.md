# Backup, Retention, Deletion and Recovery

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

## 1. A backup is not an archive and not an audit trail

A backup exists to **restore a system**. It is not a retention mechanism, not a record of what happened, and its expiry is not a deletion guarantee. Treating it as any of those is how a "deleted" record survives for years in a place nobody is looking and how a legal hold is quietly broken.

## 2. What is backed up, and how

| Subject | Mechanism | Note |
|---|---|---|
| Relational database | Periodic full plus continuous change capture supporting point-in-time recovery | Point-in-time recovery is an **architectural expectation**; its window is a policy-configurable class, not a number invented here |
| Object storage | Object versioning plus cross-location copies | Versioning is not a backup by itself: it does not survive the account that holds it |
| Repository history | Distributed by construction, plus an independent copy | Git's distribution is a property, not a strategy |
| Secret manager | The manager's own mechanism | **Never copied into a backup of anything else** |

### 2.1 Recovery classes, not invented numbers

No RPO or RTO number appears in Phase 10, because none is derivable from architecture. What is defined is a **class vocabulary** for policy to populate with evidence:

| Class | Meaning |
|---|---|
| `RECOVERY_CRITICAL` | Governed records whose loss is unacceptable: `decision`, `audit`, `knowledge` canonical history, `routing` |
| `RECOVERY_STANDARD` | Operational governed records |
| `RECOVERY_DERIVABLE` | Projections and derivatives — `registry_mirror`, reports, exports. **Rebuilt, not restored** |
| `RECOVERY_TRANSIENT` | Operational logs and runtime metadata. Loss is tolerated |

## 3. Restore is a governed event

A restore reintroduces state. It is therefore:

- **authorised** by a named human decision;
- **audited** as a restore event naming what was restored, to which point, and why;
- **reconciled** before the restored state is trusted — against the repository baseline, against object storage in both directions, and against the schema version;
- **checked for terminal states**: any object that was `RETRACTED` after the restore point is re-retracted **before** it becomes readable.

> **A restore is not an undo.** It is the reintroduction of stale state, and the gap between the restore point and now is the part that must be reconciled rather than assumed empty.

**Restore testing** is a required, scheduled exercise in test/staging with its result recorded. An untested restore path is an assumption, and this is the one place where an assumption is indistinguishable from a working system right up until it matters.

## 4. Six distinct acts

Never used as synonyms:

| # | Act | What happens to content | What remains | Authority |
|---:|---|---|---|---|
| 1 | **Logical retraction** | Nothing. The object enters terminal `RETRACTED` | Everything, readable as retracted | Phase 8 governed path |
| 2 | **Business deletion request** | Nothing yet. A request is recorded and assessed against holds, retention and governance obligations | Everything, plus the request | The requester; the outcome is a decision |
| 3 | **Physical purge** | Bytes and payload destroyed | **A tombstone**: what was purged, when, under which authority, and the audit history | A named human decision, **blocked by any legal hold** |
| 4 | **Legal hold** | Nothing expires, is purged or is overwritten within scope | Everything, held | A named decision; release is a separate named decision |
| 5 | **Backup expiry** | A backup copy ages out | The live record, untouched | The backup regime. **This is not deletion of anything** |
| 6 | **Archival** | Content moves to an archival class, slower and cheaper to read | Everything, readable | Retention policy |

### 4.1 What a purge never removes

The object's **audit history** and its **tombstone**. Something that was cited must remain answerable as having existed once its bytes are gone — otherwise a purge destroys not only the content but the record that there was content, and an audit of the purge becomes impossible.

### 4.2 Legal hold outranks retention

While a hold is in force nothing in its scope expires, is purged, is archived out of reach or is overwritten. Where the backup regime **cannot** honour a hold within existing backup copies, that limitation is **recorded as a known gap** rather than described as satisfied. An architecture that claims a guarantee its mechanism cannot produce is the failure mode this section exists to avoid.

### 4.3 Supersession is none of the six

A superseded record has not been deleted, retracted, purged, held, expired or archived. It is retained, linked and readable as what it was. **A canonical or audit record does not disappear because its current representation was superseded** — that is the whole point of keeping both.

## 5. Corruption, compromise and isolation

| Condition | Architectural outcome |
|---|---|
| Content hash mismatch on read | **QUARANTINE** the object, **ESCALATE**. The record remains authoritative for what should exist |
| Systematic corruption detected | **BLOCK** writes to the affected class; restore from the last verified point; reconcile |
| Credential compromise | **Revoke** the credential, not the identity's governance meaning; audit every action taken under it; treat every write in the window as unverified pending review |
| Ransomware or destructive-actor scenario | Backups are held such that the credentials that can write live data **cannot** delete or alter backup copies. Immutability and separate authority are the control; a copy reachable with the same credential is not a backup |
| Accidental public exposure | **QUARANTINE** and revoke access immediately; audit what was reachable and for how long; **ESCALATE for human review**; the exposure itself is a recorded event, because "we fixed it quietly" is not an outcome this architecture offers |

## 6. Retention windows are policy, not architecture

Every retention duration is a **named class resolved by policy**, never a literal embedded in a record (`storage/artifact-object-model.md` field 17). An organisation changes a class and every object carrying it follows; an object carrying a hard-coded date does not, and finding all of them afterwards is the problem this avoids.
