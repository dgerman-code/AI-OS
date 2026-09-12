# Storage Failure Modes

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

Fifteen modes, each with a declared architectural outcome. The outcome vocabulary is fixed: **BLOCK · RETRY · RECONCILE · ESCALATE · QUARANTINE · RESTORE · HUMAN REVIEW**. More than one may apply, in the order stated.

| # | Failure | Detected by | Outcome | Why that outcome |
|---:|---|---|---|---|
| 1 | **Database unavailable** | Connection or transaction failure | **BLOCK**, then **RETRY** | No governed act is recorded while its record cannot be written. Proceeding and recording later is an act with no record, which is the thing the database exists to prevent |
| 2 | **Object upload succeeds, metadata transaction fails** | The declared commit order (`storage/versioning-and-lineage.md` §6) | **RECONCILE** → **QUARANTINE** the orphan | Nothing reads an object with no record, so the artifact never existed. The orphan is quarantined and expired, **never adopted by a later record** |
| 3 | **Metadata commits, object upload fails or is later missing** | Integrity sweep, or a read | **QUARANTINE** the record, **ESCALATE** | The record is authoritative for what should exist, which is exactly why the gap is detectable. It is not repaired by inventing bytes |
| 4 | **Content hash mismatch** | Verification on read or sweep | **QUARANTINE**, **ESCALATE** | The bytes are not the bytes that were recorded. Which of the two is wrong is not a decision storage may take |
| 5 | **Object missing entirely** | Sweep or read | **QUARANTINE** the record, **ESCALATE**, then **RESTORE** if a verified copy exists | Same reasoning as 3, with a recovery path where one exists |
| 6 | **Stale schema version** | The compatibility check on connection | **BLOCK** | Degrading is worse: a partially-understood schema writes records that look valid and are not |
| 7 | **Dangling cross-registry reference** | Write-time check and baseline rebuild re-check | **QUARANTINE** the record, **ESCALATE** | **Never repointed at a current equivalent.** Repointing answers *what is it now* to a question asking *what was it then* |
| 8 | **Duplicate stable ID** | Uniqueness constraint | **BLOCK**, **ESCALATE** | Two objects claiming one identity is a governance failure, not a newer entry. Nothing is overwritten |
| 9 | **Conflicting version write** | Version pinning on the governed write path | **BLOCK**, then **RECONCILE** by re-reading and re-applying | **Last-write-wins is not available** — it is absent from the conflict vocabulary precisely because it silently discards a governed change. The writer re-reads and decides |
| 10 | **Incomplete migration** | Migration history plus schema version | **BLOCK** the environment, **ESCALATE**, **HUMAN REVIEW** | A half-applied schema is neither version. Only a human decides forward-fix or restore |
| 11 | **Restore from a stale backup** | Restore reconciliation | **RECONCILE** against repository baseline, object storage and terminal states, then **HUMAN REVIEW** before the state is trusted | The gap between the restore point and now is the part that must be examined; `RETRACTED` objects are re-retracted before becoming readable |
| 12 | **Storage provider outage** | Availability | **BLOCK** writes to affected classes, **RETRY** reads | Availability is never a reason to relax a constraint — the Phase 9 rule, applied to storage. No fallback to a location not approved for the labels |
| 13 | **Secret compromise** | Detection or disclosure | **BLOCK**, revoke, **ESCALATE**, **HUMAN REVIEW** | The credential is revoked; the identity's governance meaning is untouched; every write in the exposure window is unverified pending review |
| 14 | **Access-control misconfiguration** | Policy review, access audit, or an unexpected read | **BLOCK** the affected path, **ESCALATE**, **HUMAN REVIEW** | A permission that was wider than intended was still exercised by someone. What was reachable is an audit question, not a cleanup task |
| 15 | **Accidental public exposure** | Monitoring, disclosure or audit | **QUARANTINE**, revoke, **ESCALATE**, **HUMAN REVIEW** | The exposure is a **recorded event**. What was reachable, for how long, and by whom, is determined and recorded — not resolved quietly |

## The two rules that generate most of this table

1. **The record is authoritative for what should exist.** That is why a missing object is detectable and an orphaned object is not adoptable, and it is why the metadata commit comes last and the metadata read comes first.
2. **No failure relaxes a constraint.** Unavailability, urgency, an outage or an incomplete migration never make a non-compliant location, a stale schema or an unverified write acceptable. Phase 9 established this for routing; Phase 10 does not weaken it for storage.

## What is never an outcome

**Silently continuing.** No row above resolves to "proceed and record it later", "use the nearest available location", "repoint the reference", "take the newer copy" or "assume the object is fine". Each of those is a plausible operational instinct, and each converts a detectable failure into an undetectable one.
