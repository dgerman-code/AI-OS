# Versioning, Identity and Lineage

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

## 1. Five identifier kinds

Governance breaks when these merge. They are recorded separately and none is derivable from another.

| # | Identifier | Example shape | What it identifies | What it must never be used as |
|---:|---|---|---|---|
| 1 | **Stable logical ID** | `role.<id>`, `skill.<id>`, `review.<id>`, `workflow.<id>`, `decision.<id>`, `model.<id>`, `provider.<id>`, `deployment.<id>`, `routing_policy.<id>` | The governed object, for the life of the architecture | — it **is** the governance identity |
| 2 | **Internal surrogate key** | An opaque database key, if the implementation uses one | One row, inside one database | **Never a governance reference, never quoted in a governed record, never stable across a rebuild** |
| 3 | **Version identifier** | Registry version, record version, policy version | Which version of the logical object | Not a timestamp and not a commit |
| 4 | **Storage object identifier** | Bucket, prefix, key and object version | Where bytes currently are | **Never artifact identity** |
| 5 | **External provider identifier** | An originator's release identity, an offering reference | Something outside AI-OS that a profile describes | Never an internal identity, and never authoritative for an internal object |

> **A surrogate key is not a governance identity by implication.** If the surrogate key were ever quoted in a Decision Record, a Routing Decision or a canonical record, the record would become unreadable after a rebuild and unverifiable in any other environment. Governed records quote kind 1 and kind 3, always.

### 1.1 Mapping stable IDs to database keys

| Concern | Rule |
|---|---|
| Uniqueness | The stable logical ID is unique within its namespace and carries a uniqueness constraint. A duplicate is a **failure**, not a newer entry |
| Joins | Joins may use the surrogate key for efficiency; the **recorded** reference is always the stable ID plus version |
| Rebuild | A `registry_mirror` rebuild may assign new surrogate keys. Nothing governed may notice |
| Namespacing | The prefix (`role.`, `model.`, …) is part of the ID and is never stripped, because it is what makes a cross-registry reference checkable |
| Reuse | A stable ID is **never reused** for a different object, including after retirement |

## 2. Six version planes

| Plane | Unit | Who increments | Append-only? |
|---|---|---|---|
| **Git commit** | The repository's state | A reviewed commit | Yes — history is not rewritten on an approval-bearing branch |
| **Registry version** | A definition (Role Card, Profile, Policy) | Human authors, in the repository | Yes, by new committed version |
| **Database record version** | One governed record | The governed write path | Yes — a new version row; the prior is retained |
| **Object version** | Bytes at a storage location | An upload | Yes — **objects are never overwritten in place** |
| **Snapshot version** | An immutable point-in-time export | The producing process | Yes, immutable once written |
| **Schema version** | The database's structure | An applied migration | Yes — migration history is immutable |

An approval baseline is not a seventh plane: it is a **named Git commit**, which is why approvals are recorded rather than tagged (`architecture/storage-persistence-architecture.md` §5).

## 3. Mutation, new object, or supersession

The question that decides which, stated once:

> **Could a governed record that already exists have relied on the thing you are about to change?**

| Situation | Outcome |
|---|---|
| A display name, an operational annotation or a tag changes | **Mutation** of mutable metadata. No new version |
| A governed field changes and the object remains the same object | **New version** of the same logical object. The prior version is retained and linked |
| The object's meaning, scope or subject changes such that prior references would now mean something different | **A new logical object.** A new stable ID, and the old one is superseded, never edited |
| A version is withdrawn from use but was relied upon | **Supersession**, with both versions readable and the successor linked |
| The content was wrong and something relied on it | **Append a correction** naming what it corrects. The original stands |
| The object must not be used again, ever | **`RETRACTED`** — terminal, and no version, restore or migration undoes it |

### 3.1 Where append-only is mandatory

Decision Records, audit events, routing history, review findings, canonical promotion history, migration history, and every lineage link. In these, **there is no update and no delete** — not as a policy, as an absence of the operation.

### 3.2 Where immutability is mandatory

Any recorded reference-and-version inside a governed record; any content hash; any provenance field; any snapshot; any object version's bytes.

## 4. Lineage links

Six directed links, each append-only, each recorded on the record that asserts it:

`derived_from` · `supersedes` / `superseded_by` · `corrects` / `corrected_by` · `produced_by`

A cycle in `supersedes` or `corrects` is a defect and is detected rather than tolerated. `derived_from` may form a directed acyclic graph; it may not form a cycle either, because a derivation cycle means provenance has been asserted in both directions and one of them is false.

## 5. Six consistency boundaries

Where a governance claim is recorded, the record and everything that makes it meaningful commit together **in one database transaction** or not at all.

| # | Operation | Consistency | Why |
|---:|---|---|---|
| 1 | Routing Decision + its version references + candidate universe binding | **Strong, one transaction** | A decision whose references committed separately could name a universe it did not evaluate |
| 2 | Decision Record + linked artifact state + Right exercise reference | **Strong, one transaction** | A Right exercise that half-committed is an authority claim with no subject |
| 3 | Canonical promotion + the canonical record version it promotes | **Strong, one transaction** | Promotion of a version that does not exist is the worst available outcome |
| 4 | Review finding + the status transition it causes | **Strong, one transaction** | A status that moved without its finding is unexplainable afterwards |
| 5 | Artifact metadata + object upload | **Not atomic — cannot be.** Ordered, then reconciled | Two systems. See §6 |
| 6 | Supersession or retraction + every affected link | **Strong, one transaction** | A half-superseded object is current and not current at once |

## 6. The one boundary that cannot be atomic

An object upload and a database transaction are two systems, and no amount of design makes them one act. Phase 10 states this rather than papering over it.

**Declared commit order:** upload the object → verify the returned content hash → commit the metadata record. Nothing reads an object the registry does not know about, so an interrupted sequence leaves an **orphaned object**, never a visible artifact.

| Interruption point | Resulting state | Owner | Outcome |
|---|---|---|---|
| Upload fails | No object, no record | The writer | **RETRY.** Nothing was claimed |
| Upload succeeds, hash verification fails | Object present, unverified | Reconciliation sweep | **QUARANTINE** the object; do not commit metadata |
| Upload succeeds, metadata commit fails | Orphaned object | Reconciliation sweep | **RECONCILE** — the object is unreferenced and is quarantined, then expired under its class. It is never adopted by a later record |
| Metadata commits, object later missing | Record without bytes | Integrity check | **QUARANTINE** the record and **ESCALATE**. The record is authoritative for what should exist, which is why the gap is detectable at all |

**The compensating pattern, named:** a periodic reconciliation sweep compares committed artifact records against object storage in both directions. Records without objects are quarantined and escalated; objects without records are quarantined and expired. Neither direction is repaired by inventing the missing half.

## 7. Reconstructing a historical reference

A historical Routing Decision, Decision Record, review finding or canonical promotion stores its references as **recorded values**: the stable logical ID **and** the version, written into the record at the time.

It does not store a pointer that resolves to current state. The distinction is the whole of §7 of the master architecture: a pointer answers *what is it now*, and the question asked afterwards — usually because something went wrong — is *what was it then*. Enrichment by joining to current state is permitted for display; the record is the recorded values, and a display that silently substitutes current values for recorded ones is a defect.
