# Artifact and Object Storage Model

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

## 1. An artifact is not a file

A **file object** is bytes at a location. An **artifact** is a governed object that has provenance, scope, sensitivity, retention and lineage, and that *has* bytes somewhere. One artifact may have several object versions; one set of identical bytes may belong to several artifacts. Collapsing the two makes the path the identity, and a path is an address.

> **A file path or filename never defines artifact identity.** The display name is mutable metadata and may be changed without changing the artifact.

## 2. The artifact record — 22 fields

| # | Field | Content | Mutability |
|---:|---|---|---|
| 1 | **Artifact stable ID** | `artifact.<id>` — the governance identity | **Immutable** |
| 2 | **Artifact record version** | Monotonic within the artifact | Immutable once written |
| 3 | **Storage location reference** | Bucket / container, prefix, object key and object version — an address, not an identity | New version on change |
| 4 | **Display name** | Human-readable filename | **Mutable** |
| 5 | **Media type** | Declared type of the content | Immutable for the version |
| 6 | **Size** | Byte length as stored | Immutable for the version |
| 7 | **Content hash** | Algorithm identifier and digest over the stored bytes | **Immutable** |
| 8 | **Encryption state** | At-rest encryption posture and key-reference class; **never a key or a secret value** | Immutable for the version |
| 9 | **Scope** | Organisation / programme / project / product context, per Phase 2 | Changed only by a governed transfer |
| 10 | **Sensitivity labels** | A **set** of Phase 8 classes | Governed reclassification only |
| 11 | **Required handling controls** | Per label, from Phase 8 | Governed reclassification only |
| 12 | **Residency constraints** | Allowed jurisdictions and cross-border posture | Immutable for the version |
| 13 | **Provenance** | Origin, source references, whether content is `AI_GENERATED` per Phase 8 | **Immutable** |
| 14 | **Producer** | The identity that produced it — human, service, or a Routing Decision reference where a model produced it | **Immutable** |
| 15 | **Creation time** | When the version was written | **Immutable** |
| 16 | **Effective period** | Valid-from, and valid-until where the class has one | Immutable for the version |
| 17 | **Retention class** | A named class, resolved to a duration by policy — never a literal date embedded in the record | Governed change, recorded |
| 18 | **Legal hold** | Present or absent, with the hold's reference | Set and released only by a named decision |
| 19 | **Immutable snapshot flag** | Whether this version is a snapshot that must never be replaced | **Immutable once set** |
| 20 | **Supersedes / superseded-by** | Lineage links to other artifact versions or artifacts | Append-only |
| 21 | **Governance links** | References to knowledge claims, evidence records, review findings and Decision Records that cite this artifact | Append-only |
| 22 | **Lifecycle status** | Current, superseded, quarantined, retracted, archived | Transitions only, each an audit event |

## 3. Mutable or new-version-only

**Object bytes are never mutated in place.** A change produces a new object version and a new artifact record version; the prior remains readable. This is not a storage preference: a governed record may cite an artifact version, and in-place mutation would silently change what that record said.

Editable working documents are the apparent exception and are not one: an editing surface may hold working state, but **the artifact is the committed version**, and each commit is a new version.

## 4. Four uses of a hash, kept apart

| Use | What the hash does | What it does not do |
|---|---|---|
| **Identity** | *Nothing.* Identity is field 1 | A hash is not the ID. Two artifacts may hold identical bytes; one artifact's bytes may legitimately change |
| **Integrity proof** | Detects that stored bytes differ from what was recorded | Says nothing about whether the content was *correct* when written |
| **Deduplication hint** | Lets storage avoid keeping identical blocks twice | Never merges two artifacts. Deduplication is a storage optimisation and must be invisible above it |
| **Immutable snapshot verification** | Proves a snapshot is the snapshot that was taken | Does not prove the state it captured was valid |

Algorithms are declared abstractly: a **collision-resistant cryptographic digest**, with the algorithm identifier stored alongside every digest so the algorithm can be migrated without ambiguity. Naming one algorithm here would lock the architecture to today's cryptographic advice.

## 5. Where payloads may not go

Metadata about restricted content may be held centrally; the **content** may not follow it automatically. An artifact whose labels include classes that Phase 9 deployments treat as restricted carries a **storage eligibility test of the same shape**: the storage location's approved label set must be a superset of the artifact's labels, its residency must satisfy the artifact's constraints, and unknown support is **not** support.

This is the Phase 9 subset test applied to storage, deliberately and without modification. **No ceiling, no ordering, no "maximum sensitivity" field exists anywhere in Phase 10.**

## 6. Deletion and retraction of artifacts

| Act | Bytes | Record | Authority |
|---|---|---|---|
| Supersede | Prior version retained | Retained, linked | Governed write path |
| Quarantine | Retained, unreadable to normal access | Retained, status changed | Integrity or security response |
| Retract | Retained unless purged separately | **Terminal `RETRACTED`** | Phase 8 governed path |
| Archive | Moved to an archival class | Retained | Retention policy |
| Physical purge | **Destroyed** | **Tombstone retained**, naming what was purged, when, under which authority | A named human decision, blocked by any legal hold |

A purge never removes the artifact's audit history or its tombstone. Something that was cited must remain answerable as having existed, even once its bytes are gone.
