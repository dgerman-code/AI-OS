# Exemplar 5 — A destructive migration that needed a decision before it needed a script

Status: PROPOSED — Phase 10 exemplar storage record
Inherits: `standard.storage.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders. No SQL is written here and none is implied.

**Proves:** that the repository is the authority for what a migration *is*, the environment for what has been *applied*, and that a destructive change is authorised before it exists rather than reviewed after it runs.

## The proposed change

Migration `mig.0037`: remove a legacy free-text field from the `review` domain, superseded by structured finding fields introduced in `mig.0031`.

**It is destructive.** The field holds content in production records, and removing it destroys that content.

## What had to happen first

| Step | Outcome |
|---|---|
| 1. Classify the change | **Destructive.** Dropping a column holding governed content |
| 2. Seek authority | A named Phase 7 Decision Right covering destructive schema change, exercised by an eligible human, **before the migration was written** |
| 3. Result | **`NO_APPLICABLE_DECISION_RIGHT`** — no approved Phase 7 Right covers destructive schema change |

The approved Phase 7 register carries no Right whose subject is a schema change, and the nearest candidates do not reach: a Right permitting progression past an unresolved item has a **governed work item** as its subject, not a data structure, and reading it as authority to destroy field content would widen its declared subject — which its own card forbids.

## The outcome

**`BLOCKED`, and escalated for governance design.** Not "proceed with care", not "approved by the reviewer of the migration", not a migration written and held pending someone noticing.

`mig.0037` was **not written**. What was recorded is the block, the constraint that could not be satisfied, and the specific gap: no carded Right covers destructive schema change. Carding one is **a Phase 7 act**, and Phase 10 identifies the gap without any power to fill it.

## What was done instead

`mig.0038`, **non-destructive**: the legacy field is marked deprecated in the schema-compatibility declaration, stops being written, and stays readable.

| Element | Value |
|---|---|
| Migration ID | `mig.0038` |
| Class | Non-destructive |
| Rollback | Declared, because it is non-destructive — nothing is lost to roll back to |
| Compatibility window | Architecture revisions declaring schema `s.14`–`s.16` |
| Backfill | **None.** A backfill would have been a separate, separately-reviewed step |
| Evidence | Applied in development, then test/staging, both results recorded, before production was eligible |
| History | Appended. If later reverted, that is **two entries**, never an erasure |

## The two authorities, visible

| Question | Answered by | Never by |
|---|---|---|
| What is `mig.0038`? | The repository | The database, which cannot know what was intended |
| Has `mig.0038` been applied in production, when, by which identity, with what result? | The production environment's own migration history | The repository, which cannot know what ran |

A drift incident is what happens when one is read as the other. Keeping both is not redundancy; it is the only way either question has an answer.

## What remains true

The deprecated field's existing content is **retained and readable**. Nothing was retracted, purged or superseded — deprecation is none of the six acts of `storage/backup-retention-recovery.md` §4, and calling it deletion would have been the same error at a smaller scale than `mig.0037`.
