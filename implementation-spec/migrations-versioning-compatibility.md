# Migrations, Versioning and Compatibility

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

> **No migration file is created by this document.** Migrations are source artifacts governed in
> Git; this specifies the rules they must satisfy.

## 1. Six version planes, never merged

| Plane | Versions | Changed by | Immutable history? |
|---|---|---|---|
| **Git commit** | The repository's state | A reviewed commit | Yes — history is not rewritten on an approval-bearing branch |
| **Registry version** | A definition — Role Card, Review Profile, Decision Right Card, Workflow Definition, Routing Policy, Model/Provider/Deployment Profile | Human authors, in the repository | Yes, by new committed version |
| **Database record version** | One governed record | The governed write path | Yes — a new version row; the prior is retained |
| **Object version** | Bytes at a storage location | An upload | Yes — **objects are never overwritten in place** |
| **Snapshot version** | An immutable point-in-time export | The producing process | Yes, immutable once written |
| **Schema version** | The database's structure | An applied migration | Yes — **migration history is immutable** |

**Rule G-1.** A version identifier is **not a timestamp and not a commit**. Conflating any two
planes loses the ability to answer "which definition did this record use", which is the whole of
reproducibility.

## 2. Migration classes

| Class | Definition | Governance |
|---|---|---|
| `ADDITIVE` | Adds a table, a nullable column, an index, a new enum value that nothing yet emits | Ordinary change control |
| `BACKFILL` | Populates a new structure from existing data without changing meaning | Ordinary change control, plus a verification query |
| `TIGHTENING` | Adds a constraint that current data already satisfies | Ordinary, plus a pre-flight proving current data satisfies it |
| `SEMANTIC` | Changes what an existing column **means**, or changes an approved vocabulary | **Requires an approved architecture change first.** Never a migration-only decision |
| `DESTRUCTIVE` | Drops or rewrites governed data, or removes a governed record family | **`BLOCKED` — no approved Decision Right exists** (BA-4) |

**Rule G-2 — expand / migrate / contract.** Every structural change is three separately deployed
migrations: expand (additive, both shapes valid) → migrate (backfill and dual-write) → contract
(remove the old shape). The contract step against **governed** data is `DESTRUCTIVE` and is
therefore blocked; against a projection (`registry_projection`) or an operational-metadata column
it is ordinary.

**Rule G-3 — a migration never changes governed meaning.** Renaming an approved vocabulary
value, collapsing two axes into one column, widening an enum used in a governance decision, or
relaxing a uniqueness constraint from §5.2 of the persistence model are **semantic changes** and
require a governed architecture change through the applicable phase's change path — not a
migration and a code review.

## 3. Destructive migration is blocked

**Rule G-4.** `decision.production_database_migration` exists in
`decisions/master-decision-right-universe.md` as an **uncarded candidate**. There is no approved
Decision Right for executing a migration against production data.

Therefore:

> **Any migration classified `DESTRUCTIVE` is `BLOCKED / UNIMPLEMENTABLE UNTIL RIGHT IS
> MAPPED`.**

The enforcement hook is built and always refuses:

1. every migration declares its class in a manifest committed alongside it;
2. an automated classifier independently derives the class from the migration's statements and
   **fails the build on disagreement** with the declared class — a mis-declared class is a
   defect, not a shortcut;
3. applying a `DESTRUCTIVE` migration requires a Decision Record under a mapped Right; the lookup
   returns `NO_APPLICABLE_DECISION_RIGHT` and the apply refuses;
4. there is no `--force`, no environment variable and no break-glass parameter on the applier.

**Rule G-5 — the classifier is conservative.** Anything it cannot prove is non-destructive is
classified `DESTRUCTIVE`. `DROP`, `TRUNCATE`, a type change that can lose precision, a `NOT NULL`
addition without a default on a populated column, a constraint removal on a governance table, and
any `UPDATE` touching an `IMM` column are destructive by definition.

**Rule G-6 — a legal hold blocks regardless.** No migration touches data under a legal hold, at
any classification, under any authority. The hold is checked at apply time.

## 4. Backward compatibility

**Rule G-7 — historical records must stay readable and interpretable, forever.** This is
stronger than "the schema still parses": a record written under vocabulary version *n* must
remain interpretable when the vocabulary is at *n+k*.

| Change | Rule |
|---|---|
| Adding an enum value | Permitted. Existing rows unaffected |
| Removing an enum value | **Prohibited** while any row uses it. The value is marked deprecated and stops being emitted; rows keep it |
| Renaming an enum value | **Prohibited.** A rename is a removal and an addition, and it breaks historical interpretation |
| Adding a required field | Permitted for **new** record versions only. Existing versions keep their shape; the field is `NULL`-able for them, and the requirement is enforced per record version |
| Changing a field's meaning | `SEMANTIC`. Requires an architecture change |
| Tightening a constraint | Permitted where existing data satisfies it; otherwise the data question is answered first |

**Rule G-8 — record-version-aware reads.** Governed records carry the vocabulary/schema version
they were written under. Readers interpret each record under **its own** version, not under the
current one. A reader that assumes the latest vocabulary will silently mis-read history the first
time a value is deprecated.

## 5. Registry version compatibility

**Rule G-9.** A Workflow Definition, Review Profile, Decision Right Card, Routing Policy or
Model Profile version referenced by a historical record is resolvable **at that version**,
permanently. Retiring a definition tombstones it; the tombstone resolves.

**Rule G-10 — a run uses one version of each definition for its lifetime.** A definition updated
mid-run does not change the run. The run records the versions at intake and uses those. A newer
version applies to the **next** run.

**Rule G-11 — compatibility declarations are governance records.** A schema-compatibility
declaration (which schema versions a given application version can read and write) lives in the
`governance` data domain, append-only, and is checked at deploy time. A deployment whose
application version has no declaration for the live schema version does not start.

## 6. Approval and migration

**Rule G-12.** A schema version is a subject kind in the approval state registry
(`approval-state-registry.md` §4.1). A migration that has not been approved as a schema version
is not applied to an environment that requires approval — which is every environment holding
governed records.

**Rule G-13 — migration history is immutable.** An applied migration is never edited. A mistake
is corrected by a new migration, and the mistake stays in the history.

## 7. Rollback

**Rule G-14 — schema rollback is a new migration, never a reversal.** There is no `down`
migration executed against governed data. Recovering from a bad migration is a forward migration
that restores the required structure, classified and governed like any other — and where it is
destructive, it is blocked like any other.

**Rule G-15 — data restored from a backup does not un-happen the intervening history.** See
`failure-recovery-race-model.md` Rule F-17.

## 9. The approval-state bootstrap

The approval-state registry must be populated before it can be consulted, and populating it must
not require an approval the registry cannot yet answer for. That is a migration, and it is
governed like one.

| Property | Requirement |
|---|---|
| Class | `BACKFILL` — it populates a new structure from existing data without changing meaning |
| Manifest | Enumerates **every subject it will write**, each with its source record path and commit. A subject not in the manifest gets no row |
| Derivation | Every field is transcribed from the source record by `TranscribeApprovalState`. Nothing is invented, and `decision_right_ref` is left **null** where the source states none (Rule AP-2b) |
| Verification | Every `source_approval_record` resolves at its cited commit, and every `subject_version` is an ancestor of the current baseline |
| Review | The manifest and the transcription output are reviewed under a Review Profile **before** any runtime consults the registry |
| Authority | **None is exercised.** The bootstrap records decisions humans already made; it creates no approval (Rule AP-2) |
| Afterwards | The bootstrap is **not** a standing capability. Later transcription of an approval made outside the runtime uses the same command, one subject at a time, with the same source requirement |

**Rule G-16 — the bootstrap cannot approve itself.** The migration that populates the registry
is a schema/data change like any other, and its own approval state is recorded by the same
mechanical transcription from the human record that approves it. There is no circularity,
because at no point does anything in this chain *decide* anything: every row records a decision a
human made and wrote down elsewhere.

## 8. What is deliberately not specified

| Not specified | Why |
|---|---|
| A migration tool or framework | Implementation choice; the rules above are tool-independent |
| Concrete DDL | Phase 14 produces no executable migration |
| Zero-downtime deployment mechanics | Operational engineering |
| A specific hosted database product's migration tooling | Vendor independence (`persistence-and-transaction-model.md` §11) |
