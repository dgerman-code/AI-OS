# Migration and Environment Governance

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

## 1. Two authorities, kept apart

> **The repository is the authority for what a migration is. The environment is the authority for what has been applied.**

Neither can answer the other's question, and the failure of every drift incident is that someone read one as the other. The repository cannot know what ran; the database cannot know what was intended.

## 2. Migration governance

| Element | Rule |
|---|---|
| **Migration ID and version** | Stable, ordered, never reused, never renumbered once committed |
| **Forward migration** | Every migration has one, committed and reviewed before it exists as an applied fact |
| **Rollback versus forward-fix** | **Non-destructive migrations may declare a rollback. Destructive migrations may not** — the data is gone, and a script that pretends otherwise is the most dangerous artifact in the repository. Destructive change is corrected by **forward fix**, and that is a decision made before the migration, not after the failure |
| **Compatibility window** | Each architecture revision declares which schema versions it supports. The window is explicit and finite; "probably still works" is not a window |
| **Data backfill** | A separate, separately-reviewed step. A schema migration that silently rewrites data is two changes wearing one name |
| **Destructive-change control** | Dropping a column or table, narrowing a type, or purging data requires a named Phase 7 Decision Right exercised **before** the migration is written. It is never inferred from the migration existing |
| **Migration evidence** | Applied first in development, then test/staging, with the result recorded. A migration reaching production without a recorded lower-environment result is blocked |
| **Schema version recording** | The environment records its current schema version; every governed connection checks it against the declared compatibility window and **blocks on mismatch rather than degrading** |
| **History immutability** | Migration history is append-only. A migration that was applied and later reverted is two history entries, never an erasure |

## 3. Three environments

| Environment | Data | Credentials | Schema | Purpose |
|---|---|---|---|---|
| **Development** | Synthetic fixtures only | Own, never shared | May run ahead of production within the compatibility window | Building and first application of migrations |
| **Test / staging** | Synthetic fixtures only | Own, never shared | Matches the candidate production version | Migration evidence, restore testing, reconciliation testing |
| **Production** | Governed data | Own, never shared, most restricted | The approved version | The only environment holding real governed records |

### 3.1 Production data is never cloned downward

Stated as a rule, not a preference. A lower environment holding real restricted material is an **incident**: the labels, residency constraints and handling controls travel with the content, and no lower environment is approved for them. Fixtures are synthetic, are generated from the schema and the label vocabulary, and are recognisable as synthetic.

Where a production-shaped dataset is genuinely needed to reproduce a defect, the path is a **narrowly scoped, time-bounded, separately authorised** extraction with the labels preserved and the environment treated as production for its duration — which is expensive, and is meant to be.

### 3.2 Promotion path

Development → test/staging → production, forward only. Each step records the migration result and the schema version reached. A change may not enter production having skipped a step, and a hotfix is not an exception to that: it is the same path, executed quickly.

### 3.3 Storage separation

Each environment has its own buckets or containers, its own encryption key references and its own secret references. Nothing is shared, because a shared bucket makes environment separation a naming convention.

## 4. What is architecture and what is configuration

| Architecture — stated here | Configuration — not observable from this repository |
|---|---|
| That environments are separated and never share credentials | Which accounts exist |
| That schema mismatch blocks | The connection check's implementation |
| That destructive change needs a named Right | Which Right, once Phase 7 cards one |
| That branch history bearing an approval is not rewritten | Whether the forge enforces it today |

Phase 10 claims only the left column. **It makes no claim about the current configuration of any forge, project, database or bucket, because none is observable from inside the repository and an unobservable claim is not a check.**
