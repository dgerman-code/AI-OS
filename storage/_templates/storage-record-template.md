# Storage Record Template

Status: PROPOSED — Phase 10 template candidate
Inherits: `standard.storage.common_constraints@0.1`

The shape every governed record in the operational database carries. Not a schema: no types, no DDL, no keys beyond what governance requires.

## Identity
- **Stable logical ID**: `<namespace>.<id>` — the governance identity, immutable, never reused
- **Record version**: monotonic within this logical object, immutable once written
- **Internal surrogate key**: implementation detail if used. **Never quoted in a governed record, never stable across a rebuild**
- **Domain**: one of the ten in `storage/data-domain-model.md`

## Governance state
- **Lifecycle status**: in the owning phase's vocabulary, unchanged by Phase 10
- **Scope**: organisation / programme / project / product, per Phase 2
- **Sensitivity labels**: a **set** of Phase 8 classes. **Not a level, not a ceiling, not ordered**
- **Required handling controls**: per label
- **Residency constraints**: allowed jurisdictions; cross-border posture
- **Effective period**: valid-from; valid-until where the class has one
- **Freshness**: Phase 8 fields where the class has them — derived, never overwritten historically

## Provenance and lineage
- **Origin**: including Phase 8 origin classification where applicable
- **Producer**: the human, governed act, or Routing Decision reference that produced it
- **`derived_from` / `supersedes` / `superseded_by` / `corrects` / `corrected_by`**: append-only links

## Recorded references
> Every reference is **stable logical ID plus version, written as recorded values**. A pointer resolving to current state is an enrichment, never the record (`storage/versioning-and-lineage.md` §7).

- **Registry references**: each `RESOLVED`, `FUTURE_GOVERNANCE_REFERENCE` (non-executable) or `DANGLING` (quarantine)
- **Cross-domain references**: same rule

## Audit
- **Creating audit event**: the event ID that produced this version — immutable
- **Human identity reference** and **system identity**: two fields, always

## What this record is not
- It is **not** an authority. No column grants a Decision Right, satisfies a review, promotes anything to canonical, or makes content true.
- It holds **no secret value** and no credential — references only.
- It carries **no scalar sensitivity**, no maximum, no ceiling, no ordering.
