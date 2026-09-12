# Data Domain Model

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

Conceptual domains, not a schema. No DDL is written here and none is implied.

## 1. What justifies a domain boundary

A domain exists only where **three things coincide**: one write authority, one lifecycle owner, and one audit posture. Where two candidate domains share all three, they are one domain. This is the whole test, and it is why there are ten rather than a tidier number.

Domains split for readability and not for ownership were rejected: a boundary that does not constrain who may write is decoration, and decoration in a data model is where authority quietly leaks.

## 2. The ten domains

| # | Domain | Owning object types | Write authority | Lifecycle owner | Audit posture |
|---:|---|---|---|---|---|
| 1 | `governance` | Approval baselines, schema-compatibility declarations, configuration version records, legal holds, retention class definitions | Human decision, recorded | Phase 7 / human authority | Append-only |
| 2 | `registry_mirror` | Projections of Role, Skill, Workflow, Review Profile, Decision Right, Model, Provider, Deployment and Routing Policy definitions | **The projector only** — rebuilt from an approved baseline | The repository | Rebuild events audited; rows not individually versioned |
| 3 | `execution` | Handoff records, work item references, stage/status transitions | The acting identity via the governed path | Phases 5–6 | Append-only transitions |
| 4 | `review` | Review instances, findings, reviewer identity references, independence class references | The reviewing identity | Phase 6 | Append-only findings |
| 5 | `decision` | Decision Records, Right exercise references, expiry and bounded-effect fields | An eligible human exercising a carded Right | Phase 7 | **Append-only, never amended** |
| 6 | `knowledge` | Memory items, knowledge claims, canonical records, source and evidence metadata, conflict states | The governed promotion path | Phase 8 | Append-only history with supersession |
| 7 | `routing` | Routing Decisions, candidate universe bindings, per-candidate results, the six-part reproducibility set | The routing act | Phase 9 | Append-only |
| 8 | `artifact` | Artifact records, storage location references, content hashes, retention class, hold flags, supersession links | The governed write path | Phase 10 | Append-only versions |
| 9 | `audit` | Audit events across every other domain | **The audit writer only; no update, no delete** | Phase 10 | Append-only and immutable |
| 10 | `runtime_meta` | Bounded execution metadata: correlation IDs, system identity references, timing, outcome class | The emitting system | Phase 11 will own this; Phase 10 reserves it | Retained by policy; **not evidence** |

### 2.1 Why `runtime_meta` exists now and is bounded

It is reserved rather than designed, because execution belongs to Phase 11 and a domain invented later tends to be bolted onto whichever table was nearest. What Phase 10 fixes is its **boundary**: it holds correlation metadata only, never payloads, never governance outcomes, and **nothing in any other domain may cite it as a reason**. A record that would be incomplete without a runtime event is a record that was written wrong.

### 2.2 Why `registry_mirror` is one domain and not nine

Nine mirrors would share one write authority (the projector), one lifecycle owner (the repository) and one audit posture. By §1 that is one domain. Splitting it would suggest the mirrors have independent authority, which is precisely what they must not have.

## 3. Fields every governed record carries

| Field group | Content | Mutability |
|---|---|---|
| **Logical identity** | Stable logical ID in the owning registry's namespace | **Immutable** |
| **Surrogate key** | Internal database key, if the implementation uses one | Immutable, and never a governance reference |
| **Version** | Record version, monotonic within the logical object | **Immutable once written** |
| **Lifecycle status** | The owning phase's vocabulary, unchanged | Transitions only, each recorded as an event |
| **Scope** | Organisation / programme / project / product context, per Phase 2 | Immutable; a scope change is a governed transfer, not an update |
| **Sensitivity labels** | A **set** of Phase 8 classes, plus required handling controls per label | Changes only through a governed reclassification, recorded |
| **Residency constraints** | Allowed jurisdictions, cross-border posture | Immutable for the version |
| **Provenance** | Origin, producer identity, source references | **Immutable** |
| **Lineage** | Derived-from, supersedes, superseded-by, corrects, corrected-by | Append-only links |
| **Effective time** | Valid-from and, where applicable, valid-until | Immutable for the version |
| **Freshness** | Phase 8 refresh interval and verdict fields, where the object class has them | Recomputed, never overwritten historically |
| **Audit reference** | The audit event that created this version | **Immutable** |

## 4. Immutable versus mutable

> **The rule: anything a governed decision could have relied on is immutable.**

Immutable once written: logical identity, version number, provenance, effective time, content hash, recorded references and versions, every audit event, every Decision Record, every appended finding.

Mutable, and mutable only through a recorded transition: lifecycle status, display name and operational annotations, retention class, hold flags, and the freshness verdict (which is **derived**, so recomputing it changes no fact).

Anything not in either list is immutable by default. Unclassified mutability is the same defect as unclassified sensitivity.

## 5. Soft delete, retraction and supersession

Three different things, and the database models them as three:

| Act | What changes | What remains | Who may |
|---|---|---|---|
| **Supersession** | A new version exists and is current; the prior version is linked as superseded | Everything. The superseded version stays readable as what it was | The governed write path for that object class |
| **Retraction** | The object enters Phase 8's **terminal** `RETRACTED` state | Everything, permanently readable as retracted | The Phase 8 governed path |
| **Soft delete** | A row is marked not-current for operational listing | Everything | The governed write path — **and it is never used on `decision`, `audit`, `knowledge` canonical history or `routing`** |

**There is no hard delete of a governed record.** Physical purge exists, is a different act with its own authority, and is defined in `storage/backup-retention-recovery.md` §4.

`RETRACTED` is terminal: no supersession, restore, migration, reclassification or retention action returns a retracted object to use. A restore that reintroduces a pre-retraction version re-applies the retraction before the object is readable.

## 6. Cross-registry reference integrity

Every reference from a record to a registry definition is **by stable logical ID and version**, and every such reference is in exactly one of three states:

| State | Meaning | Consequence |
|---|---|---|
| `RESOLVED` | The ID and version exist in the approved baseline | Normal |
| `FUTURE_GOVERNANCE_REFERENCE` | Deliberately names something not yet carded | **Non-executable.** Recorded, never treated as available — the Phase 9 rule, unchanged |
| `DANGLING` | The reference resolves to nothing and was not declared future | **Defect.** The record is quarantined and escalated; it is never silently dropped and never repointed at a successor |

Repointing a dangling reference at "the current equivalent" is specifically forbidden: it answers the question asked afterwards with today's answer, which is the failure Phase 9 §7 reproducibility exists to prevent.

## 7. Keys and referential expectations

- Foreign keys are expected **within** the operational database, between records in domains 1 and 3–10.
- References **into** `registry_mirror` are expected as declared references, checked on write and re-checked on baseline rebuild — not as hard foreign keys, because the mirror is rebuilt and a rebuild must not be able to cascade into governed records.
- References **out** to object storage are by storage location plus content hash, never by foreign key, because object storage is a different system and a foreign key across it would be the distributed-atomicity fiction the standard forbids.
