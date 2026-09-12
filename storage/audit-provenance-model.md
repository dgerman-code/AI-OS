# Audit and Provenance Model

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

## 1. Five histories, and none substitutes for another

| History | Answers | Written by | Retention | May it stand in for another? |
|---|---|---|---|---|
| **Operational log** | What the system did mechanically | The running system | Rotated, sampled, discarded | **No.** It is not evidence and nothing that must survive lives only here |
| **Audit event** | Who or what changed which governed record, from what to what, and why | The audit writer, append-only | Retained by policy, never deleted | **No.** It records the change, not the authority for it |
| **Decision Record** | That an eligible human exercised a named Decision Right | Phase 7 governed path | Permanent, append-only | **No.** It is the authority, and it is not a log of the change it authorised |
| **Knowledge provenance** | Where a claim came from and what supports it | Phase 8 governed path | Permanent with supersession | **No.** Provenance is about content, not about operations |
| **Git commit history** | How the architecture itself changed | Reviewed commits | Permanent, not rewritten | **No.** It records the definition, never the operation |

Four operational histories and the repository's own: the substitution error is common in all directions, so each is denied explicitly. **An audit event is not a Decision Record, is not a Git commit, and is not an operational log.**

## 2. The audit event — 11 fields

| # | Field | Content |
|---:|---|---|
| 1 | **Event ID** | Stable, unique, never reused |
| 2 | **Subject reference** | The governed object's stable logical ID and the version affected |
| 3 | **Change class** | Create, new version, transition, link, quarantine, hold, purge, rebuild, restore |
| 4 | **Previous version reference** | The version before, or explicitly none for a creation |
| 5 | **New version reference** | The version after, or explicitly none for a read-class event that records one |
| 6 | **Reason / context** | Why, in the vocabulary of the owning phase — never free text alone where a governed reason class exists |
| 7 | **Decision Record reference** | Required where the change class demands an authority: purge, hold release, destructive migration, restore, reclassification. **Absent is a failure for those classes, not a blank field** |
| 8 | **Provenance reference** | The source or act the change derives from |
| 9 | **Timestamps** | Event time and, where they differ, effective time |
| 10 | **Identities** | The **human identity reference** and, separately, the **system/service identity** that executed it. Two fields, always |
| 11 | **Correlation reference** | Transaction or correlation ID linking events that belong to one operation |

An optional twelfth value may be recorded where the deployment supports it: an **immutable event reference** — a chained digest over the event and its predecessor. It is declared optional deliberately: a chain that only some environments can produce must not be something the architecture silently assumes.

## 3. Append-only, mechanically

The `audit` domain has **no update and no delete operation to grant** (`storage/access-control-and-rls-boundary.md` §4). Correction is an appended event whose change class names the event it corrects; the original stands and remains readable.

Where the backend can enforce append-only structurally, it must. Where it can only enforce it by permission, **the limitation is recorded rather than assumed away** — an architecture that claims immutability it cannot produce is worse than one that states the gap.

## 4. What must always produce an audit event

Every create, version, transition, link, quarantine, hold set or release, purge, restore, reclassification, mirror rebuild and applied migration. Reads are audited where the object carries restricted labels or where a purpose-bound grant was used, because "who looked at this" is the question asked after an exposure.

## 5. Provenance is not audit

Provenance answers *where this content came from*; audit answers *what happened to this record*. A document's provenance survives a migration that rewrites every row; an audit trail describes the migration and says nothing about the document's origin. They are stored in different domains and neither is derived from the other.
