# Approval State Registry

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 finding **M-6**.

## 1. The problem this closes

Today, approval exists **only as prose** in `reviews/phase-N-final-approval.md`. Every governed
artifact in the repository carries `Status: PROPOSED` in its header, including the eight
exemplar Decision Right Cards that the Phase 7 human approval names explicitly as covered.

Two consequences follow, and both are real:

1. **Nothing can answer "is this approved?" mechanically.** A runtime that must refuse to act on
   an unapproved definition has no oracle to ask.
2. **The header and the record disagree.** The Phase 10 validator requires every Phase 10
   artifact to remain `PROPOSED` and therefore fails on its own approval record — an artifact
   whose existence is the approval. That is not a defect in the validator's intent; it is what
   happens when approval state is inferred from a text field inside the thing being approved.

**Rule AP-1 — do not fix this by rewriting history.** Historical `Status:` fields are **not**
edited to make validators green. The header stays what it was; a separate, forward-compatible,
machine-readable registry becomes the authoritative answer.

## 2. What the registry is

A governed record family in the `governance` data domain (C2), append-only, whose rows are
**derived from and cite** human approval records — never a substitute for them.

**Rule AP-2 — the registry records approval; it never creates it.** A row exists because a human
approval record exists. Writing a row is not approving. There is no command that creates an
approval state without a resolvable source approval record and a human approving authority.

### 2.1 Two recording acts, because there are two situations

One command could not serve both, and an earlier revision's single `RecordApprovalState` — class
`H` — was contradictory: class `H` asserts a mapped Decision Right governs the act, while this
document says transcription creates no approval and that a historical source may carry no Right
at all. The conflation also pointed the wrong way: if *recording* is itself an authority-bearing
act, then whoever can call the recording API is exercising authority, which is how a service
account becomes a route to manufactured approval.

| | `TranscribeApprovalState` | `RecordNewApprovalState` |
|---|---|---|
| Situation | An authoritative human approval record **already exists** — in `reviews/`, or created outside the runtime | A **new** governed approval, revocation or supersession act has just happened and satisfied its Right |
| Auth class | `h` — a human runs a bounded transcription | `H` — the underlying act was governed by a mapped Right |
| Exercises a Right? | **No.** Transcription is mechanical | **No.** The Right was exercised by the act; this records its result |
| Creates approval? | **No** | **No** |
| `source_approval_record` | **Mandatory**, and must resolve at the cited commit | **Mandatory** |
| `decision_right_ref` / `decision_record_ref` | **Nullable**, exactly where the authoritative source did not record them | **`NOT NULL`** where the governed act required a Right; the Decision Record must resolve and its `decided_by` must be human |
| Availability | The bounded bootstrap of §9, and later transcription of an approval made outside the runtime | Ordinary runtime operation |
| With no source record | **Fail closed** — the subject stays `PROPOSED` | Fail closed, the same way |

**Rule AP-2a — transcription is mechanical or it is refused.** Every field
`TranscribeApprovalState` writes is derived from the source record. A field with no counterpart
in the source is `TRANSCRIPTION_NOT_MECHANICAL`, **not** a blank for the caller to fill. This is
what makes "records but never creates" checkable rather than aspirational: there is no parameter
through which a decision the source does not contain could be supplied.

**Rule AP-2b — nullable Right lineage is a historical fact, not a loophole.** Several approved
Phase 1–13 records predate the Decision Rights model or were human decisions taken outside it;
they state an approving human and a date and no `decision.<id>`. Transcribing them with a null
`decision_right_ref` records what is true. Inventing a Right to fill the column would be
manufacturing exactly the authority this package refuses to manufacture. `RecordNewApprovalState`
has no such latitude: a new governed approval that required a Right and cannot name its Decision
Record is refused.

**Rule AP-2c — neither command can be talked into creating approval.** Being authenticated, an
administrator, a service role or the database owner changes nothing, because neither command
accepts an approval status, a Right or a Decision Record the source record does not already
state (`api-command-contracts.md` Rule Q-14).

**Rule AP-3 — the registry is the runtime's oracle, not the governance authority.** The
authority is the human decision. The registry is how a machine finds out what that decision was,
in the same way an audit event records a change without being the authority for it.

## 3. What it must be able to answer

| Question | Field |
|---|---|
| What artifact / architecture baseline / registry version is approved? | `subject_ref` + `subject_version` + `subject_kind` |
| Is it approved? | `status` |
| Who approved it? | `approving_human_authority` |
| Under which Decision Right, where applicable? | `decision_right_ref` + `decision_record_ref` |
| When? | `approved_at` |
| On the basis of which record? | `source_approval_record` |
| Has it been superseded or revoked? | `status`, `superseded_by`, `revocation` |
| What exactly is covered? | `approval_scope` |
| What is explicitly **not** covered? | `explicit_non_scope` |
| Under what conditions, and what was deferred? | `conditions`, `deferred_items` |

## 4. `approval_state_record`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `approval_ref` | `ApprovalStateRef` | NO | IMM | |
| `approval_version` | int | NO | IMM | PK with `approval_ref` |
| `subject_kind` | enum §4.1 | NO | IMM | |
| `subject_ref` | governed ref | NO | IMM | The thing approved |
| `subject_version` | version id | NO | IMM | Baseline commit, registry version or record version |
| `status` | enum §4.2 | NO | APP | |
| `approving_human_authority` | `HumanAuthorityRef` | NO | IMM | **Check: kind must be `human`** |
| `decision_right_ref` + `registry_version` | ref pair | YES | IMM | Where the approval was a Decision Right exercise |
| `decision_record_ref` | ref | YES | IMM | `NOT NULL` whenever `decision_right_ref` is present |
| `approved_at` | timestamptz | NO | IMM | The human decision's date, not the row's insert time |
| `source_approval_record` | structured | NO | IMM | Repository path **and** commit SHA of the human approval record. Must resolve |
| `approval_scope` | structured | NO | IMM | What is covered, itemised |
| `explicit_non_scope` | structured | NO | IMM | What is **not** covered. `NOT NULL` — an approval that does not say what it excludes has not been read carefully |
| `conditions` | structured | YES | IMM | Caveats the approval attached |
| `deferred_items` | structured | YES | IMM | Items the approval explicitly deferred |
| `supersedes` / `superseded_by` | ref+version | YES | APP | |
| `revocation` | structured | YES | APP | Reason, revoking authority, Decision Record, timestamp |
| `recorded_by_*` | identity stamps | NO | IMM | Separate human and system identity |

Constraints: `PRIMARY KEY (approval_ref, approval_version)` (U21); the table is **immutable** —
no `UPDATE` and no `DELETE` on any column, including `status`; check:
`decision_right_ref IS NOT NULL → decision_record_ref IS NOT NULL`.

### 4.0a Currentness is a pointer, not a status

`status` says what an approval **decided**. It does not say which record is **in force**. Those
are different questions and an earlier revision of this document answered both with one column,
which left `APPROVED_WITH_CONDITIONS` outside the uniqueness rule and invented a status value
`ACTIVE` that this vocabulary does not contain.

`approval_state_current` is the current pointer:

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `subject_ref` | governed ref | NO | IMM | **PK with `subject_version`** — this is U19 |
| `subject_version` | version id | NO | IMM | |
| `approval_ref` + `approval_version` | ref pair | NO | MUT | Points at the history row in force |
| `record_version` | bigint | NO | MUT | Optimistic concurrency token |
| `pointed_at` | timestamptz | NO | MUT | Operational |

**Rule AP-4a — at most one current row per subject version, whatever its status.** The pointer's
primary key makes the rule total: it holds for `APPROVED`, for `APPROVED_WITH_CONDITIONS`, for
`REVOKED` and for an explicitly recorded `PROPOSED`. The only status that is never pointed at is
`SUPERSEDED`, because superseding is precisely the act of moving the pointer elsewhere.

**Rule AP-4b — moving the pointer is one transaction with the new history row**, under a
version-pinned write. A concurrent attempt fails with `STALE_WRITE` and writes nothing.

**Rule AP-4c — no `ACTIVE`.** The approval-state vocabulary is exactly the five values in §4.2.
Any document, constraint or query naming an `ACTIVE` approval status is defective.

### 4.1 Subject kinds

`ARCHITECTURE_BASELINE` · `REGISTRY_DEFINITION_VERSION` · `ARTIFACT_VERSION` ·
`IMPLEMENTATION_BASELINE` · `SCHEMA_VERSION` · `POLICY_VERSION`

### 4.2 Status values

| Status | Means |
|---|---|
| `PROPOSED` | Recorded, not approved. The default for everything |
| `APPROVED` | A human approval record exists and this row cites it |
| `APPROVED_WITH_CONDITIONS` | Approved with caveats that **remain open and carried** |
| `SUPERSEDED` | A later approval state replaced this one's operative effect |
| `REVOKED` | Withdrawn by a governed act, with reason recorded. Remains visible |

**Rule AP-4 — fail closed on absence.** The **absence** of a current-pointer row means
`PROPOSED`, never `APPROVED`. A runtime asked about an unknown subject answers "not approved" and
refuses. There is no "assume approved for convenience" default anywhere.

**Rule AP-5 — `APPROVED_WITH_CONDITIONS` is not `APPROVED`.** Its conditions remain open and are
carried into every use, exactly as `SATISFIED_WITH_OPEN_ITEMS` and `APPROVE_WITH_CONDITIONS` are.
An implementation that treats it as plain approval has discarded the conditions.

## 5. Granularity — what a human approval does and does not cover

**Rule AP-6 — no mass promotion.** A human approval of a phase does **not** promote every
individual exemplar, template or card to `APPROVED` unless its own record says so. The registry
carries one row per **explicitly approved subject**, enumerated from the approval record's own
"approved scope" section, and nothing else.

Worked example, from the current repository:

| Subject | Row? | Basis |
|---|---|---|
| Phase 7 architecture baseline `cedee2cf` | Yes, `APPROVED` | `reviews/phase-7-final-approval.md` approved-scope list |
| The eight exemplar Decision Right Cards | Yes, `APPROVED` — one row each | The record names "the eight exemplar Decision Right Cards" explicitly |
| The other 27 candidate Decision Rights | **No row** → `PROPOSED` | The record says it does **not** approve all 35 candidates as card-ready |
| `decision.cancellation_or_termination` | **No row**, and a `deferred_items` note | `NOT CARDABLE UNTIL BOUNDED` |
| Phase 12 implementation baseline `f5f8dd76` | Yes, `APPROVED_WITH_CONDITIONS` | The record's known-MVP-limitations and non-scope sections |

**Rule AP-7 — the non-scope is data, not commentary.** `explicit_non_scope` is populated from
the approval record's own "what this approval does NOT do" section and is **queryable**. A
runtime asked "may I deploy on the strength of the Phase 12 approval?" gets `no` from a field,
not from someone remembering to read the prose.

## 6. Relationship to artifact `Status:` headers

| | Artifact header `Status:` | Approval state registry |
|---|---|---|
| Audience | Human readers | Machines and humans |
| Authority | None — it is a label the author wrote | Derived from the human approval record |
| Changed by | Editing a file | A governed act citing a source approval record |
| On disagreement | **The registry wins**, and the disagreement is reported | |

**Rule AP-8 — the disagreement is reported, not silently resolved.** Where a header says
`PROPOSED` and the registry says `APPROVED`, that is the current, correct state of this
repository for the eight Decision Right Cards. It is surfaced as an informational
reconciliation report and **is not** fixed by editing either side. A later documentation-only
governed maintenance pass may align headers; Phase 14 does not.

## 7. Supersession and revocation

**Rule AP-8a — history and pointer move together or not at all.** Both recording acts write the
immutable `approval_state_record` version **and** create or move `approval_state_current` in
**one transaction**, under a version-pinned write on the pointer. A history row without its
pointer, or a pointer without its history row, is not a state this specification permits, and
`test-and-assurance-strategy.md` A35 asserts it. Each act therefore produces **two** audit
events — one per governed-record mutation, per Rule P-14a — with the pointer's recorded as
`POINTER_MOVE` (before-version null on creation, non-null on a move).

**Rule AP-9.** Approval state is **never edited in place**. A new approval writes a new
immutable `approval_version` whose own `status` reflects the new decision, and moves the current
pointer to it in the same transaction. The prior row is not rewritten to say `SUPERSEDED`: it is
superseded *by having been pointed away from*, and a query for the history of a subject reads
the version chain. A `SUPERSEDED` status value is written only on a row created to record that
outcome explicitly.

**Rule AP-10.** Revocation is a governed act: it records the reason, the revoking human
authority, and the Decision Record where one was required. The revoked row **remains visible**
— consistent with `RETRACTED` in the knowledge model, which withdraws from reliance without
erasing.

**Rule AP-11 — revocation is not retroactive to acts already performed.** Work done while an
approval stood was done under an approval that stood. Revocation changes what may be done
**next**, and triggers a recorded impact assessment of what was relied on. It never rewrites
history and never invalidates a Decision Record.

## 8. How the runtime uses it

| Use | Query | On absence |
|---|---|---|
| Intake check 1 — Workflow Definition resolves **in the approved baseline** | `GetApprovalState(workflow_ref, version)` | `BLOCK` |
| Intake check 2 — Orchestrator Policy at a named version | Same | `BLOCK` |
| Routing — the Routing Policy version in force is approved | Same | `CANDIDATE_UNIVERSE_INCOMPLETE` or `BLOCK` |
| Decision gate — the Decision Right Card version is approved | Same | `NO_APPLICABLE_DECISION_RIGHT` |
| Review gate — the Review Profile version is approved | Same | `BLOCK` |
| Migration — the schema version is approved | Same | Migration refused |

**Rule AP-12 — one oracle.** No component keeps its own notion of what is approved, no
configuration file lists approved versions, and no environment variable overrides the registry.

## 9. Bootstrapping

The registry must be populated before it can be consulted, and populating it must not itself
require an approval the registry cannot yet answer for.

**Rule AP-13 — bootstrap is a bounded, reviewable transcription, not a standing privilege.** The
initial rows are written by `TranscribeApprovalState` from the existing human approval records in
`reviews/`, each citing its path and commit SHA. The bootstrap is a **one-off enumerated
migration**, governed like any other migration (`migrations-versioning-compatibility.md` §9): it
has a manifest listing every subject it will write, it is reviewed before it runs, and it does
not leave behind a runtime capability to bulk-create approval state. The transcription is:

1. **mechanical** — one row per subject the approval record itself enumerates;
2. **verified** — every `source_approval_record` must resolve at the cited commit, and every
   `subject_version` must be an ancestor of the current baseline;
3. **reviewed** — the transcription is reviewed under a Review Profile before the registry is
   consulted by any runtime;
4. **non-creative** — a subject the approval record does not name gets **no row**, and therefore
   remains `PROPOSED`.

**Rule AP-14.** The bootstrap transcription creates no approval and needs no new Decision Right.
It records decisions that were already made by a human, in a form a machine can read.
