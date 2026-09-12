# Artifact Record Template

Status: PROPOSED — Phase 10 template candidate
Inherits: `standard.storage.common_constraints@0.1`

The 22 fields of `storage/artifact-object-model.md` §2, as a record. Synthetic values only.

## Identity
- **Artifact stable ID**: `artifact.<id>` — immutable, never reused
- **Artifact record version**
- **Immutable snapshot flag**: set or absent; **immutable once set**

## Location and content
- **Storage location reference**: `<bucket-or-container>` / `<prefix>` / `<object-key>` @ `<object-version>` — an **address, not an identity**
- **Display name**: mutable. **Defines nothing**
- **Media type**
- **Size**
- **Content hash**: `<algorithm-id>`:`<digest>` — integrity, **never identity** (`storage/artifact-object-model.md` §4)
- **Encryption state**: at-rest posture and key-reference class. **Never a key, never a secret value**

## Governance
- **Scope**
- **Sensitivity labels**: a **set**
- **Required handling controls**: per label
- **Residency constraints**
- **Storage eligibility**: the location's approved label set must be a **superset** of these labels; residency satisfied; **unknown support is not support**

## Provenance
- **Provenance**: origin, source references, Phase 8 origin classification
- **Producer**: human, service, or Routing Decision reference where a model produced it
- **Creation time**
- **Effective period**

## Retention
- **Retention class**: a **named class**, never a literal date
- **Legal hold**: present or absent, with reference. **Outranks every retention rule**

## Lineage and links
- **`supersedes` / `superseded_by`**
- **Governance links**: knowledge claims, evidence records, review findings, Decision Records citing this artifact — append-only

## Lifecycle
- **Status**: current · superseded · quarantined · retracted · archived

## What this record is not
- Not proof the content is correct, current, approved or canonical.
- Not a grant of access — eligibility is evaluated over the seven dimensions.
- Not deletable: a purge destroys bytes and leaves a **tombstone plus the audit history**.
