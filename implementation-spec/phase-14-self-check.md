# Phase 14 Self-Check

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1

This is a **producer self-check**, not an independent audit. It records what this package
claims, what it does not, and where each Phase 13 obligation is discharged. Every number below
is read from an executable artifact, not written by hand.

> **Revision 4 — routing lifecycle, retry refusal, external-effect staging, audit nullability,
> assurance inventories.** Re-audit V3 returned `FAIL / NOT READY` on seven blockers: three
> incompatible statements about when a Routing Request becomes durable; a retry row saying
> "nothing written" where O-20 requires a halt; `InvokeModel` modelled as one local transaction
> across an external call; an audit field table contradicting its own nullability matrix; stale
> counts in digits and words; assurance gates frozen at `A1–A30` and `P1–P8`; and a validator
> that passed a localized count mutation because a correct count survived elsewhere. All seven
> are closed; §10 records each. The validator is 90 checks with a 15-check cross-document group,
> and the probe fixture is 47.

> **Revision 3 — transaction completeness, approval recording, assurance consistency.** The
> independent re-audit v2 found six blockers behind a green 74/74 and 19/19: the transaction
> table claimed exhaustiveness over a fraction of the governed commands, `RecordApprovalState`
> was one command doing two contradictory jobs, the terminal adversarial test still attacked a
> contract that no longer existed, the canonical-promotion test asserted and denied the same
> thing, the audit schema required a before-version on
> inserts, and the uniqueness count had drifted. All six are closed; §9 records each. The
> validator grew to 81 checks with a new cross-document group, and the probe fixture to 31.

> **Revision 2 — fidelity and contract remediation.** The independent Phase 14 audit found
> seven blockers and rated harness credibility `MEDIUM` because 8 of 9 materially contradictory
> mutations were accepted. All seven are closed; §8 records each. The validator grew from 60 to
> 74 checks, and a committed adversarial fixture now demonstrates, from executed behaviour, that
> each load-bearing rule is load-bearing.

## 1. Explicit non-production status

| Claim | Answer |
|---|---|
| Is this production-ready? | **No.** It is a specification and nothing here is built |
| Is anything deployed, provisioned or configured? | **No** |
| Are there migrations, API code, infrastructure manifests, SDKs, secrets or credentials? | **No** |
| Are any Phase 14 artifacts approved or canonical? | **No.** All are `PROPOSED` until independent audit and explicit human approval |
| Does this create, widen, infer or manufacture any Decision Right? | **No.** Four operations are specified as permanently refusing until a Phase 7 governed change maps their Rights |
| Does this modify any approved Phase 1–13 artifact? | **No.** Verified byte-identical |
| Does this claim exactly-once, distributed transactions, or production concurrency guarantees? | **No** |

## 2. Phase 13 debt closure matrix — M-1 … M-7

### 2.1 A note on the numbering

The Phase 13 review recorded findings **M-1 … M-8**. The Phase 14 prompt names **M-1 … M-6** as
mandatory and requires the matrix to cover **M-1 … M-7**. The mapping is stated rather than
assumed:

| Phase 13 review | Phase 13 approval obligation | Covered below |
|---|---|---|
| M-1 four-axis knowledge model | Obligation 1 | M-1 |
| M-2 runtime event vs governance evidence | Obligation 2 | M-2 |
| M-3 six-part routing reproducibility | Obligation 3 | M-3 |
| M-4 identity-level SoD | Obligation 4 | M-4 |
| M-5 scope identity as path | Obligation 5 | M-5 |
| M-6 machine-readable approval state | Obligation 8 | M-6 |
| M-7 baseline-citation labelling inconsistency | *(documentation)* | M-7 |
| M-8 no duplication found — nothing to close | *(no obligation)* | M-8 |
| — | Obligation 6 bounded rework loops | §2.3 R-1 |
| — | Obligation 7 persistent uniqueness / at-most-once | §2.3 R-2 |

### 2.2 The matrix

| # | Finding | Where closed | How, in one line | Complete? |
|---:|---|---|---|---|
| **M-1** | Phase 12 collapsed `Origin` / `Canonicality` | `knowledge-and-canonical-model.md` §2, §12 D1–D2 | Four separate axes with the approved vocabulary — 8 epistemic types, 7 governance states, 4 origins, orthogonal conflict; Rule K-2 prohibits any merged column; `AI_SUGGESTION` has **no** outbound epistemic edge (K-3) and adoption creates a new linked item (K-4) | **Yes** |
| **M-2** | Execution event described as governance evidence | `audit-provenance-observability.md` §2, §3; `orchestrator-runtime-contract.md` §13 | Execution events are coordination history and **never** governance evidence (V-1); enforced structurally by a **write-only** interface with no read operation, a separate store with no FK or read grant, an exclusive gate evidence contract, and a CI static check (V-2). The full 13-field contract with **separate human and system identities** (V-3) and a conditional authority reference (V-4). Six record families separated: runtime event, execution event, audit event, provenance, Decision Record, review record | **Yes** |
| **M-3** | Routing decision carried 2 of 6 reproducibility elements | `model-router-runtime-contract.md` §5 | Elements 20–25 as named columns, `NOT NULL` together for an eligible outcome and `NULL` for every non-eligible one, both directions as check constraints (M-7); plus routing policy version, declared preference order, candidate universe binding, per-candidate eligibility evidence and selection reason. Routing reproducibility claimed; model-output reproducibility explicitly not (M-8) | **Yes** |
| **M-4** | SoD stopped at an `independence_class` label | `decision-review-authority-model.md` §6 | Six actor identities recorded separately (A-3); producer-review prohibition on **identities** (A-4); model diversity is not reviewer independence (A-5); `DECISION_RIGHT_SEPARATION` with all ten normative rules including delegation (rule 4) and scarcity (rule 9); enforced durably via `decision_chain_id` (A-6, P-11); bounded contributor cannot satisfy a full Profile (A-2) | **Yes** |
| **M-5** | Scope was an opaque flat string | `scope-and-context-model.md` | Node identity **and** canonical path; the full approved graph with all four load-bearing properties; ancestry queries with the mandatory separator-boundary test (S-2); four applicability modes, declared never inferred, failing closed to `NON_INHERITABLE` (S-11); ancestor fallback with **no silent resumption** (S-12); narrowing as subset containment on an unordered label set (S-4, S-8); sub-run rule (S-9); both transfer records in full (§7.1, §7.2); the four contamination directions (§9) | **Yes** |
| **M-6** | Approval existed only as prose | `approval-state-registry.md` | A machine-readable registry answering all ten required questions; derived from and citing human approval records, creating none (AP-2); **absence reads as `PROPOSED`** (AP-4); no mass promotion, one row per explicitly named subject (AP-6); queryable `explicit_non_scope` (AP-7); supersession and revocation without erasure (AP-9…AP-11); a bootstrap that is transcription, not approval (AP-13, AP-14); **history is not rewritten to make validators green** (AP-1, AP-8) | **Yes** |
| **M-7** | Baseline-citation labelling: Phase 10 cites Phase 9's *approval-record commit* as its "human-approved baseline" while the Phase 9 record's baseline is the architecture commit | `README.md` §3 | Every baseline in this package is cited as the **architecture/implementation baseline** named by its own approval record, with the approval record named separately. `approval-state-registry.md` §4 makes the distinction structural: `subject_version` is the baseline, `source_approval_record` is the record's path **and** commit. **Phase 4's row now cites `8ddacb2b`, read from its own approval record** (§8.7). Phase 14 does **not** edit the Phase 10 document — that is documentation cleanup under governed maintenance | **Yes, for Phase 14's own artifacts** |
| **M-8** | No duplicate concepts, second sources of truth or shadow authority paths found | — | Nothing to close. This package introduces none: one approval oracle (AP-12), one intervention contract (O-22), one run-creation preflight, one scope-path representation, one uniqueness mechanism | **N/A** |

### 2.3 The two additional mandatory items

| # | Item | Where | Complete? |
|---:|---|---|---|
| **R-1** | Bounded rework loops | `orchestrator-runtime-contract.md` §7 — loop identity, iteration counter, declared `max_iterations` with **no default and no unbounded value**, retained prior iteration instances (O-16), escalation on exhaustion (O-17), DAG check with declared loop bodies contracted so there is no graph-cycle ambiguity (O-18) | **Yes** |
| **R-2** | Persistent uniqueness / at-most-once | `persistence-and-transaction-model.md` §5 — the canonical U1–U23 uniqueness inventory; `ON CONFLICT DO NOTHING` prohibited (P-7); a duplicate is a failure, not a newer entry (P-8); **exactly-once claimed nowhere** (P-9); reference-kind check constraints (P-10); durable decision-chain separation (P-11) | **Yes** |

## 3. Additional Phase 14 mandatory items

| Prompt § | Item | Where | Complete? |
|---|---|---|---|
| 4.3 | Concurrency and race implementation | `failure-recovery-race-model.md` §2 — all ten races with enforcement mechanisms; five outcomes; `LAST_WRITE_WINS` absent (F-1); optimistic concurrency and version-pinned writes (P-12…P-14); idempotency keys; correlation/causation; late review and late Decision handled **asymmetrically** with F-3 forbidding a shared code path | Yes |
| 4.4 | Compensation and non-replayable acts | `orchestrator-runtime-contract.md` §11; `failure-recovery-race-model.md` §7 — four-record lineage; four external-effect uncertainty states; the two forbidden assumptions (F-10); compensation request/authorisation/execution; originals never altered (F-14); **compensation may itself be unauthorised** (F-15) | Yes |
| 4.5 | Full `SUPERSEDED` path | `orchestrator-runtime-contract.md` §12 — eight object families, none destructive; a Decision Record is never superseded by amendment | Yes |
| 4.6 | Deferred Decision Rights | `open-items-and-blocked-authorities.md` §1 — four blocked authorities, each with operations, candidate identifier, enforcement hook, resolution path and the accepted consequence; B-1 forbids approximation | Yes |
| 6 | Specification depth | Every persisted record specified with field, type, nullability, mutability, uniqueness, references, lifecycle, allowed writer, authority, audit and error outcomes | Yes |
| 7 | Transactional rule under durable storage | `persistence-and-transaction-model.md` §7 — a branch-complete table covering every governed act with read set, preflight set, concurrency check, exact writes, exact audit count, execution count, constraints and pre-commit refusal behaviour; staged/outbox/reconciliation where atomicity cannot span (§8, §9) | Yes |
| 8 | Approval / authority safety | `decision-review-authority-model.md` §8 — A-9's five prohibitions and A-10's twelve non-substitutions; `NO_APPLICABLE_DECISION_RIGHT` is not `403` (Q-11) | Yes |
| 9 | Model / provider independence | `model-router-runtime-contract.md` §8 — a vendor-neutral adapter contract; M-15 keeps every vendor name inside Provider and Deployment Profiles, which are data; S1 and S7 enforce it in CI | Yes |
| 10 | Storage / Supabase position | `persistence-and-transaction-model.md` §11 — Supabase as one option with a plain-PostgreSQL equivalent for every capability; P-23 forbids any invariant depending on a hosted product; RLS is enforcement (X-6), service-role keys are credentials (X-14) | Yes |

## 4. Governing-invariant preservation

| Invariant | Preserved by |
|---|---|
| `ROLE != AGENT INSTANCE` | Distinct types, distinct versioning, N-1…N-6, X-3 |
| `MODEL != ROLE` | M-1, M-16; no path from a model identity to holder eligibility |
| `ROUTER != ORCHESTRATOR` | Component boundary F1/F2; `decided_by` kind check |
| `REVIEW PROFILE != REVIEW INSTANCE` | Distinct types; request and instance are different records from different actors |
| `DECISION RIGHT != DECISION RECORD` | Distinct types; §7's five satisfaction conditions; A-8 |
| `KNOWLEDGE != CANONICAL RECORD` | Distinct tables; promotion is a new canonical version, never an update |
| `ARTIFACT != STORAGE RECORD` | Distinct tables; P-17, P-18 orphan rules |
| `RUNTIME EVENT != AUDIT EVENT` | V-1, V-2, structural write-only interface, S2 |
| `CREDENTIAL != HUMAN AUTHORITY` | X-14, database check constraints, X-17's four closures |
| **Authority never inferred** | Q-3's eight non-inferences; A-10's twelve non-substitutions; E-8; E-12; K-15; V-9 |
| **Fail closed** | README §4; S-6, S-11, AP-4, G-5, O-1, and the unclassified-retry default |

## 5. Specification choices requiring human architectural decision

The open items enumerated in `open-items-and-blocked-authorities.md` §2 (OI-1 … OI-11), each classified
as an **implementation precondition** (OI-2, OI-3, OI-4, OI-6, OI-8) or a
**production/organisational engineering deferral** (OI-1, OI-5, OI-7, OI-9, OI-10, OI-11). The
twelfth, OI-12, was **false and has been removed**: the Phase 4 approval record does state its
baseline commit, and the error originated in the Phase 13 review's own grep. Phase 14 declines to
make the remaining ones because making them would create governance no approved phase
authorised. The four most consequential:

1. **OI-6** — mapping holder-eligibility classes to real people. Without it no decision gate can
   be satisfied by anyone, in any environment.
2. **OI-4** — what "delivery line" means for `INDEPENDENT_ASSURANCE_REVIEW`. AI-OS does not own
   organisation charts; condition 3 of Rule A-4 is declared and evidenced, and its absence blocks.
3. **OI-8** — the concrete residency vocabulary. Until it exists, `UNASSESSED` blocks every
   routing candidate, storage location and backup destination.
4. **OI-2** — whether repository-wide guidance exists for `max_iterations`, or each Workflow
   Definition declares its own with none.

## 6. Package inventory and validation

| Item | Count |
|---|---|
| Specification documents under `implementation-spec/` | 20 |
| Validator checks | **108**, in 14 groups: `structure` 6 · `containment` 6 · `invariants` 5 · `knowledge` 6 · `scope` 6 · `routing` 3 · `events` 5 · `authority` 5 · `persistence` 7 · `races` 5 · `approval` 4 · `completeness` 6 · `fidelity` 11 · `crossdoc` 33 |
| Validator | `validation/phase_14_validation.py`, standard library only, deterministic, no network |
| Adversarial fixture | `validation/phase_14_mutation_probes.py`, **99 committed controlled weakenings**, 99 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR` |
| Governed commands | **36**, each with exactly one transaction contract; the two sets are compared and equal |
| Durable uniqueness constraints | **23** (U1–U23), one canonical inventory, every stated count derived from it |
| Executable production code, migrations, manifests, SDK dependencies | **0** |
| Approved Phase 1–13 artifacts modified | **0** |
| Decision Rights created | **0** |
| Operations specified as permanently refusing until a Right is mapped | **4** |

Phase 14 validator result: `106/106 PASS` on default, `--verbose` and `--json`.

**Adversarial fixture.** `validation/phase_14_mutation_probes.py` is committed and runs from a
clean checkout. Each probe weakens one load-bearing rule in a temporary copy of the package and
re-runs the validator against it; classification is from executed behaviour, never from a label;
a probe whose target text is not found is an **error**, not a skip.

Two harness artefacts were found while building it and are recorded rather than left in place:

1. Three containment checks read git state and therefore failed in *every* temporary tree,
   making all probes look detected. Their verdicts are now **discarded** by the runner
   (`GIT_DEPENDENT`), and the temporary tree no longer reaches the real `.git` directory at all.
2. With those discarded, **three probes were genuinely undetected** — a renamed origin value, a
   removed separator-boundary rule, and runtime events becoming admissible evidence. Three new
   checks were added for exactly those rules, and one probe was re-targeted from a
   divergence-table description to the load-bearing statement it was supposed to attack.

Current result: **99 probes, 99 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR`**, each caught by a named
substantive check. The fourteen added in revision 7 are in §13.1, the fourteen from revision 6 in
§12.1, the twelve from revision 5 in §11.1, the sixteen from revision 4 in §10.1, the twelve from
revision 3 in §9.1, and the original set is:

| Weakening | Caught by |
|---|---|
| Model Profile takes an invented prefix | Phase 9 identity compatibility |
| An independent stable `ModelRef` is reintroduced | Phase 9 identity compatibility |
| Model Result checked against a field the decision does not hold | Routing Decision ↔ Model Result lineage |
| The release-identity divergence outcome is removed | Routing Decision ↔ Model Result lineage |
| Conflict resolution made authority-bearing | Phase 8 conflict-resolution boundary |
| Cancellation and termination collapsed | `CANCELLED` / `TERMINATED` asymmetry |
| The transaction table stops stating audit counts | Audit-event cardinality |
| U19 keys on a nonexistent `ACTIVE` status | Approval-state currentness |
| The Phase 4 baseline is contradicted | Phase 4 baseline citation |
| The identity chain is reordered | Ordered chain equality |
| An approved origin value is dropped | Origin-axis exactness |
| Self-review reduced to a class label | Self-review identity inequality |
| The separator-boundary rule is removed | Separator-boundary ancestry |
| The approval registry may create approval | Registry records but never creates |
| The execution-event contract stops denying evidence | Operational events never satisfy evidence |
| The write-only event interface gains a read operation | Operational events never satisfy evidence |
| A convenience exception for governed uniqueness | Durable uniqueness / no `ON CONFLICT DO NOTHING` |
| An administrative path for a destructive migration | No admin substitution for a missing Right |
| A blocked authority section is renamed away | Missing Rights are not silently filled |

Regression results at this baseline, reported exactly and **not repaired out of scope**:

| Validator | Result | Note |
|---|---|---|
| Phase 8 | `119/119 PASS` | |
| Phase 9 | `277/277 PASS` | |
| Phase 10 | `145/147 PASS` | **Inherited** approval-record status conditions — the Phase 10 validator scanning its own phase's human approval record |
| Phase 11 | `159/160 PASS` | **Inherited** approval-record wording condition — the phrase "without distributed exactly-once claims" in the Phase 11 approval record tripping the exactly-once scan |
| Phase 12 | `55/55 PASS` | |
| Phase 12 suite | `157 tests — OK` | |

## 8. The Phase 14 audit blockers, and how each was closed

| # | Blocker | Closed by |
|---:|---|---|
| 1 | Phase 9 Model Profile identity incompatibility — an invented `model_profile.<name>` prefix and a separately allocated `model.<name>` `ModelRef` | `domain-identity-model.md` §3.2 restates the six-layer Phase 9 stack verbatim. The Model Profile takes Phase 9's own `model.<stable_snake_case_name>`; the chain's `MODEL` is layer 2, the Underlying Model Release, **a recorded external value with no registry ID** (Rules I-4…I-9). The `ModelRef` construct is **removed**, not renamed. Model Family is added |
| 2 | Model Result validated against a `model_ref` the Routing Decision does not hold | `model-router-runtime-contract.md` §6.2 and Rules M-11/M-11a/M-11b. Five elements (20–21, 23, 24, 25) are compared for **equality**; element 22 is **observed and compared**, and a mismatch fires `PROVIDER_VERSION_CHANGE` and blocks — Phase 9 §0 rule 7 applied where the divergence is observable. A specification that required element 22 to equal itself would check nothing |
| 3 | `ResolveConflict` made authority-bearing, inventing an authority dependency | Rules K-13a…K-13e restore Phase 8 §3 rule 2 exactly: resolution is an **eligible Role's professional conclusion, checked by review**; a consequent governed status or canonical change is a **separate** act with its own mapped Right. A new auth class `R` carries this in the command catalogue, and `conflict_resolution.decision_record_ref` is **nullable** |
| 4 | `CancelRun`/`TerminateRun` collapsed, requiring human intervention for both | Separate commands, separate transaction rows, separate audit provenance. `CANCELLED` is `h` with an intervention; `TERMINATED` is **`S`** with a named constraint and **no human identity, never synthesised** (Rules O-6a, Q-9a, V-3a, F-15a) |
| 5 | Audit-event cardinality contradicted itself across prose, schema and tables | One rule, stated in both owning documents: **one audit event per persisted governed-record mutation, same transaction, linked to that record** (P-14a). No grouping (P-14c). Act-level correlation is distinguished from record-level cardinality (P-14b). §7.2 enumerates **every governed act**, branch by branch, with exact audit and execution counts; refusals write none (P-14e) |
| 6 | U19 keyed on a nonexistent `ACTIVE` approval status | Currentness is now a **pointer**, not a status: `approval_state_record` is an immutable version history (U21) and `approval_state_current` holds at most one row per subject version (U19). The rule is total — it covers `APPROVED_WITH_CONDITIONS` and every other operative status — and `ACTIVE` is explicitly absent (Rules AP-4a…AP-4c, P-9a, P-9b) |
| 7a | Rule I-1 claimed every reference is a stable-ID/version pair while the inventory held unversioned instance identities | Two categories: **A** governed definitions and profiles carry *(stable ID, version)*; **B** immutable runtime-instance and governed-record identities carry a stable identity **alone**, because there is no second version of an event that occurred. Rule I-1b states why this loses no reproducibility |
| 7b | A false OI-12 claiming Phase 4's approval record carried no baseline | Corrected. `reviews/phase-4-final-approval.md` line 7 states `Approved Baseline Commit: 8ddacb2b…`; the commit resolves, is an ancestor, and Phase 4's artifacts are byte-identical to it. OI-12 is **removed, not resolved** — there was never an open question. The error originated in the Phase 13 review and is named as mine |

## 9. The re-audit v2 blockers, and how each was closed

| # | Blocker | Closed by |
|---:|---|---|
| 1 | A12a–A12f still treated `TerminateRun` as accepting a human intervention and expected `FOREIGN_RUN_LINEAGE` — contradicting the terminal contract repaired in revision 2 | A12a–A12f is split. **A12a** keeps the foreign-lineage attack on the **five** commands that do consume an intervention. **A12b–A12f** attack the actual `TerminateRun` contract: missing named constraint, a smuggled `HumanInterventionRecord`, a missing or wrong-kind system identity, an unreachable source phase, and an already-terminal run. Each asserts full observational equality and **no fabricated human provenance**. **P-A12** is the positive control: a valid constraint-driven termination succeeds with **no** intervention and a `NULL` `human_identity_ref` |
| 2 | The transaction table claimed exhaustiveness while covering 17 of the governed commands | `api-command-contracts.md` §5.1 became **the** canonical governed-command inventory, each entry carrying an explicit **Act** key naming its transaction contract, and `persistence-and-transaction-model.md` §7.2 was keyed identically. The validator derives both sets and requires exact equality in both directions; duplicate coverage is permitted only through an explicit alias, of which there are currently none. Every previously omitted act — `RecordIntervention`, `ResumeRun`, `UnblockRun`, `SupplyGateEvidence`, `CreateKnowledgeItem`, `AdoptAISuggestion`, `RaiseConflict`, `ApplyConsequentStatusChange`, `CompleteRun` — gained a full contract, as did `RequestReview`, `RequestDecision`, `Retry`, `OpenSubRun`, `OpenReworkIteration`, `SupersedeRun` and the four blocked acts. **This row records what revision 3 did and states no current total**: the inventory sizes it quoted were correct at that revision and are not, and must never be read as, a claim about the package as it now stands — §6 holds the only current counts, and every one of them is derived from its owning table. The `RequestRouting` command named in the revision-3 wording of this row **was removed in revision 4** and is not a member of any current inventory (§10, blocker 1) |
| 3 | `RecordApprovalState` was class `H` while the registry said transcription creates no approval and may have null Right lineage | Two commands. **`TranscribeApprovalState`** (`h`) mechanically transcribes an **already-existing** authoritative record, exercises no Right, and may write null `decision_right_ref` **exactly where the source states none**. **`RecordNewApprovalState`** (`H`) persists the result of a **new** governed act and requires its Decision Record to resolve with a human `decided_by`. Neither creates approval, and neither has a parameter through which a decision the source does not contain could be supplied (Q-14, AP-2a, AP-2c). The bootstrap is a bounded, manifested, reviewed `BACKFILL` migration (`migrations-versioning-compatibility.md` §9), not a standing privilege. `security-identity-access.md` X-17a closes the recording-API route explicitly |
| 4 | The uniqueness count said 20 in milestones while the inventory held 21 | §5.2 is declared **the canonical uniqueness inventory**. Milestone M2 and gate G-B reference it and state the derived number. The validator parses the inventory, computes the count, and fails any document stating a different one |
| 5 | A17a/A17b said a mapped Right is mocked in *and* that refusal follows because none is mapped | **A17a** (`CURRENT`): under the approved universe no applicable Right is mapped, so `PromoteToCanonical` refuses with **zero governed writes, zero audit events**, one refusal execution event. **A17b** (`HYPOTHETICAL`): presenting an arbitrary or non-applicable Right, or a forged Decision Record, does not satisfy BA-1 — and the row states explicitly that **it is not evidence BA-1 is resolved**. **P-A17** records that there is deliberately **no** positive control. Every adversarial row now carries a `Basis` field, and the validator refuses a `HYPOTHETICAL` row that claims a mapped Right exists |
| 6 | The audit schema required a non-null `record_version_before` on inserts, which cannot exist | `mutation_kind` is an explicit eight-value enum, and §4.1 is a nullability matrix keyed on it: `INSERT` requires before **NULL**; `VERSION_APPEND`, `UPDATE`, `LINK_APPEND`, `LIFECYCLE_STATE_CHANGE` and `SUPERSEDE` require both; `POINTER_MOVE` is null on creation and non-null on a move; `DESTROY` is defined now — before mandatory, after null — **and remains unreachable, because BA-3 is blocked**. A refused transaction writes no audit event at any kind |

### 9.1 Assurance added for exactly these failures

Twelve new probes, each detected by a named substantive check:

| Weakening | Caught by |
|---|---|
| A12a–A12f regresses to human-intervention termination | Adversarial metadata vs command contracts |
| The termination positive control is removed | Adversarial metadata vs command contracts |
| A governed API command is dropped from the transaction table | Command set == transaction act set |
| A transaction row has no governed API command | Command set == transaction act set |
| The two approval acts collapse into one class | Approval classes vs registry semantics |
| Transcription may create approval without a source | Approval classes vs registry semantics |
| Approval history written without the pointer move | Approval classes vs registry semantics |
| A milestone's uniqueness count drifts | One inventory, cited consistently |
| A17a/A17b mixes current and hypothetical | Canonical-promotion test consistency |
| An `INSERT` audit event requires a before-version | Version-nullability matrix |
| A newly covered act stops stating its audit count | Audit cardinality |
| A blocked command is allowed a governed write | Blocked commands declare zero writes |

One further correction was made while building these: an existing probe's target had gone stale
when the transaction table's row keys changed from prose names to act keys. It failed **loudly**,
as the fixture requires, and was repaired — which is the fixture working, not a defect in it.

## 10. The re-audit V3 blockers, and how each was closed

| # | Blocker | Closed by |
|---:|---|---|
| 1 | Three incompatible statements about the Routing Request lifecycle | **One lifecycle.** `RequestRouting` no longer exists as a governed command; the prospective envelope is constructed **inside** `route()` and reaches storage only with a validated answer. The branches are encoded identically in the API inventory, the router contract and the transaction table, and **their current cardinalities are stated only in those tables** — revision 5 split B1 into B1/B1r and B4 into B4s/B4n and made B3 and B4n carry run-state appends, so any count quoted in this narrative would be the next thing to go stale. See `api-command-contracts.md` §5.4 Rules Q-17, Q-17a and Q-17b for the current branch set and counts. A valid refusal **is** recorded because Phase 11 §3 says the refusals are the important half; an invalid answer is not, because it is the absence of an answer. **U6 was wrong and is corrected**: Phase 11 §5 says a retry re-submits the *same* request and every attempt's decision is recorded, so uniqueness is `(routing_request_ref, submission_ordinal)`, not one decision per request |
| 2 | O-20 required a halt while the transaction row said "Nothing written" | **Nine branches, none writing nothing.** R1, R2, R2f, R3, R3a, R4, R6, R7 and RX each state preconditions, phase and posture before and after, exact writes, audit and execution counts, whether a dispatch record exists and whether an escalation record does. R4, R6 and RX write a `retry_refusal_record`, a block and an escalation — **3 audit events**, in one transaction. O-20 now says it plainly: **a halt is a write.** Compensation is never reached by retrying (Q-31) |
| 3 | `InvokeModel` looked like one local transaction across a provider call | **Five stages, four identities, three commands, three transactions.** Stage 1 commits intent, a `NOT_ATTEMPTED` provider attempt and an outbox row — **no provider call happens inside it**. Stage 2 is explicitly not transactional. Stage 3 records the observed outcome; stage 4 writes the Model Result **only** from `CONFIRMED_APPLIED`; stage 5 reconciles. `ModelInvocationRef`, `ProviderAttemptRef`, `ModelResultRef` and `ReconciliationRef` are never collapsed. Crash behaviour is specified at every boundary, including the one that matters: **an attempt whose lease expired reads as `ATTEMPTED_OUTCOME_UNKNOWN`, never as `NOT_ATTEMPTED`** — the single place an optimistic reading would duplicate an external effect. **A timeout is not proof that nothing happened** (Q-23). No distributed transaction and no exactly-once |
| 4 | The audit field table said `record_version_after` was always non-null; the matrix said `NULL` for `DESTROY` | The field table now states *conditional on `mutation_kind`* for **both** version columns and defers to §4.1, which is declared the only statement of nullability. `DESTROY` stays defined and **unreachable**: BA-3 is blocked and `destroy_governed_content` writes zero records |
| 5 | Stale counts in digits and words, and stale ranges | Swept across every document, in both forms. Counts are stated where they are useful and **derived**: uniqueness from the U-inventory, governed commands from the inventory table, adversarial and positive-control totals from their owning tables. The validator checks **every** occurrence, leading or trailing, in digits or in words |
| 6 | M20 and G-R required only `A1–A30` and `P1–P8` | **Five canonical assurance inventories** (§2a of the test strategy), parsed from their owning tables, supporting non-contiguous and suffixed IDs exactly. M20 and G-R require **every ID in every inventory** and state the derived sizes; the validator rejects a range, a wrong count, and any cited ID that does not exist. Rule T-17 makes the exactness explicit: a bare unsuffixed identifier is not an ID where the inventory holds only its suffixed forms, and prefix matching is prohibited in every derivation |
| 7 | A localized count mutation passed because a correct count survived elsewhere | The count check no longer asks whether *some* occurrence is right. It derives each inventory's size and checks **every** count-bearing location in every document, leading (`**23** uniqueness constraints`) and trailing (`inventory (currently **23**)`, `\| Governed commands \| **36**`), in digits and in word form. Probes 8, 9 and 10 exist precisely to prove it |

### 10.1 Assurance added for exactly these failures

Sixteen new probes. Three of them were **not** detected on first run and are the reason three
checks changed:

| Not detected at first | What it exposed | Fix |
|---|---|---|
| Stale uniqueness count in digits in one gate | The count check only matched a number *before* its subject; `inventory (currently **21**)` puts it after | Trailing-form patterns added |
| Stale governed-act count in a self-check table row | Same shape: `\| Governed commands \| **seventeen** \|` | Trailing-form patterns added |
| BA-1 stops covering governed downgrade | Nothing asserted the clarification at all | A new check, plus adversarial test A47 |

A fourth correction: the first version of the trailing patterns required `**` markers while
matching against text that had already had emphasis stripped, so they matched nothing. The
fixture reported both as `REDUNDANT`, which is what it is for.

## 11. The re-audit V4 blockers, and how each was closed

| # | Blocker | Closed by |
|---:|---|---|
| 1 | Routing B1/B3/B4 transactional state semantics were incomplete: no contract for an invalid answer after a durable request, and B3/B4 committed a non-selection decision with the run-state consequence left in prose | **Branch B1r** is specified in the API contract (Q-17a), the router contract (M-13d) and the transaction table: the durable request is preserved, no decision is created, `submission_ordinal` is **not** advanced, zero governed writes, zero audit events, one refusal execution event. **Rule Q-17b** maps each non-selection outcome to its exact run-state appends, postures and wait subject, and defines *s*; **Q-17c** commits those appends in the same transaction as the decision, so no committed state has a durable non-selection decision and a run still eligible to continue; **Q-17d** makes B4n inherit B3's consequence rather than a weaker one. B4 is split into **B4s** and **B4n**. The router's outcome table is now deterministic (M-7a) — `BLOCKED` **then** `ESCALATED`, never "or". Phase 11's same-request / every-decision-recorded semantics and U6 are unchanged |
| 2 | R2/R2f/R4/R6/RX posture semantics were incomplete, and the halted posture lived only in prose | §5.6 now carries **twelve columns**: phase before → after, **posture before → after**, wait reason · escalation, exact governed writes, audit count, execution count, whether a dispatch occurs and whether a dispatch or escalation record is created — for every one of the nine branches. R2f, R4, R6 and RX name `GATE_UNSATISFIED` **inside their exact governed writes** (Q-28a), and §7.2 states the same writes from the commit side. R3's wait reason is `WAITING_FOR_HUMAN` with the acknowledgement as its subject. **Q-28b** ties dispatch to the existence of a `retry_attempt`. Compensation remains a separate governed act and an unknown external effect is still never auto-replayed (Q-31, O-20c) |
| 3 | The outbox was three numbered steps with no implementable protocol | `persistence-and-transaction-model.md` §9 is rewritten as **§§9.1–9.6**: the nine-field dispatch item with a stable `outbox_ref`; four **operational** uniqueness constraints `O1`–`O4` (deliberately outside the canonical `U` inventory, so no governed count moves); linkage to `ModelInvocationRef` **and** `ProviderAttemptRef`; the five-value claim vocabulary `PENDING` · `CLAIMED` · `DISPATCHED` · `SETTLED` · `ABANDONED`; the atomic compare-and-swap claim precondition (P-24); the claimant as a **named service identity** (P-25); lease owner, lease expiry and the OCC `claim_token`; **no concurrent valid lease**, enforced by constraint O4 rather than by drain logic (P-26); redelivery after expiry **only from `CLAIMED`** (P-27); the stable provider idempotency key that is never regenerated (P-23); receiver-side deduplication where available (P-28) and its absence (P-29); the **four** crash points; the durable `ATTEMPTED_OUTCOME_UNKNOWN` path (P-31); and the exact redispatch-versus-reconciliation table (P-32). No vendor, no queue product, no distributed transaction, no exactly-once (P-20, P-30) |
| 4 | The outbox was audited as a governed mutation in one place and classified operational in another | **Operational**, everywhere, preserving the approved Phase 10/11 line that delivery plumbing is not governance. Rule **P-20a** is the single statement; P-14d excludes the row and every claim transition; audit Rule **V-7** repeats it from the audit side; **Q-22a** states it in the API contract. Stage 1 therefore writes **two** governed records and **two** audit events — in §5.5, in §7.2, and in the positive control P-A41. A48 is the adversarial row that fails if the old count returns |
| 5 | §5.5 said stages 3 and 4 were one transaction **and** described a crash state between them | One transaction, stated once as **Rule Q-22b**. Stage 4's boundary cell now reads "the same transaction as stage 3"; the crash row that described a state between them is replaced by an explicit **Unreachable** row; the failure model says the same thing as **F-9c**; and A52 attacks the removed recovery path. Stage 5 stays a separate transaction, because reconciliation is a separate act |
| 6 | O-25 required total execution-event equality while contracts require a refusal execution event | **Rule O-25** now states equality over **governed** state and **governed** history — the total execution-event count is explicitly excluded. **Rule O-25a** permits exactly the refusal execution events a contract names and denies them any standing as evidence, gate evidence, approval, authority or state progress, structurally, via the write-only interface of V-1. **Rule O-25b** and **Rule T-18** state the two separate assertions a test makes. No row in the test strategy requires total execution-event-count equality |
| 7 | The self-check carried stale active claims — 35 commands, 35 rows, and `RequestRouting` as a current inventory member | §9's revision-3 row is rewritten to record what that revision **did** without quoting any current total, and it states that `RequestRouting` was removed in revision 4 and is a member of no current inventory. §6 holds the only current counts and every one is derived from its owning table. The validator now parses the canonical inventories and fails any document — this one included — that states a different command, act, branch, uniqueness or assurance total in digits or in words, leading or trailing; and it fails any claim of current inventory membership for a command that is not in §5.1. Probe **12** of §11.1 reproduces the exact V4 miss |

### 11.1 Assurance added for exactly these failures

Twelve new probes, each detected by a named substantive check:

| # | Weakening | Caught by |
|---:|---|---|
| 1 | B3 commits a durable decision with no run-state append | Routing run-state consequence is atomic |
| 2 | B4n loses its run-state consequence | Routing run-state consequence is atomic |
| 3 | An invalid answer after a durable request advances the ordinal | Routing run-state consequence is atomic |
| 4 | R2f stops stating its posture | Retry posture is a committed write |
| 5 | R4/R6/RX drop the halted posture from their exact writes | Retry posture is a committed write |
| 6 | The outbox loses its stable identity and uniqueness | The outbox protocol is implementable |
| 7 | Two concurrent valid leases are permitted | The outbox protocol is implementable |
| 8 | Lease expiry is treated as proof no effect occurred | The outbox protocol is implementable |
| 9 | The outbox is counted as a governed mutation | Outbox classification is one classification |
| 10 | A crash window is reintroduced between stages 3 and 4 | Stages 3 and 4 are one transaction |
| 11 | A refused-act test requires execution-event equality | Refusal-event observational equality |
| 12 | The self-check restates a stale command/row count and reintroduces `RequestRouting` | Every normative count matches its canonical inventory · no obsolete command is claimed as current |

Probe 12 is the V4 miss reproduced exactly: it changes **only** this document's counts and
reintroduces the removed command, leaving every canonical inventory correct. The V4 harness
passed that mutation. This one does not.

## 12. The re-audit V5 blockers, and how each was closed

| # | Blocker | Closed by |
|---:|---|---|
| 1 | The external-call boundary was not crash-safe: `CLAIMED` meant no call had happened and `DISPATCHED` meant one had, but no transition was atomic with the provider call, so a crash after the call left a re-dispatchable `CLAIMED` row | A **committed pre-call state**. The vocabulary is now six values — `PENDING` · `CLAIMED` · `DISPATCH_PENDING` · `UNCERTAIN` · `SETTLED` · `ABANDONED` — and the call is made **only** after `DISPATCH_PENDING` commits with the monotone `boundary_crossed` flag set (PO-7, PO-9). `CLAIMED` is therefore the one state whose safety is structural rather than inferred (PO-8), and recovery decides what a stale row becomes by reading that flag, never the clock or the previous state's name (PO-10). Five crash points are defined, including the two that were one: the call boundary itself, and provider acceptance before local persistence. No distributed transaction, no exactly-once (PO-11, PO-17) |
| 2 | `O4` was a partial unique index predicated on `lease_expires_at > now()` — **not implementable**, since a unique-index predicate must be immutable — and `O1`/`O4` both constrained `outbox_ref` | `O1`–`O5` are redesigned as ordinary durable constraints. `O1` is the **only** identity constraint; `O4` is a time-free `CHECK` tying the ownership columns to the owning states; `O5` carries the monotonic `claim_generation`. Exclusivity is a property of the row — `lease_owner` is one column, so there is nowhere for a second owner — and is made enforceable under contention by the compare-and-swap of PO-3 and the generation fence of PO-4, not by an index (PO-2). `lease_expires_at` schedules attention and never transfers ownership (PO-5), so clock skew cannot produce two writers who both believe they hold the row |
| 3 | Only `PENDING → CLAIMED` was precise | §9.4 specifies **ten** transitions `T1`–`T10`, each with its exact reads, its full predicate, its writes, its fencing requirement, whether redispatch is permitted afterwards and whether reconciliation is mandatory. Claim renewal (T3), both expired-claim recoveries (T6, T7), both reconciliation outcomes (T8, T9) and pre-call retirement (T10) are included. Every transition fences on `claim_generation`; every transition a claimant makes also fences on `claim_token`, so a stale writer settles nothing (PO-12). Stage 3/4 success carries **T4 in the same local transaction** (PO-13), and A59 fails if a committed outcome is left beside an unsettled dispatch item |
| 4 | Two active `P-23` rules | The outbox protocol's rules are renamed into their own `PO-` namespace (`PO-1`…`PO-19`), leaving §11's `P-23` untouched, and every cross-reference in five documents is updated. The validator now derives **every** rule definition in the package and rejects any repeated identifier — which immediately found **two further collisions the V5 audit did not name**: `V-7` (introduced by revision 5's outbox-audit rule) and a false `V-5` collision caused by the `V-5-matrix` identifier. The first is renamed `V-6d`; the second was a defect in the check's own pattern and is fixed. 373 rule identifiers, each defined once |
| 5 | Stale routing and refusal prose in active locations | The self-check narrative no longer quotes any branch count and points at the owning tables instead; the router's `CANDIDATE_UNIVERSE_INCOMPLETE` text is now deterministic — `BLOCKED` **then** `ESCALATED`, posture `GATE_UNSATISFIED` — matching M-7a and Q-17b; and gate `G-K` no longer says a refused route leaves "no event", but states that an **invalid** answer leaves no governed record and no audit event while appending exactly one refusal execution event that is never governance evidence. The search was not limited to the three named lines: the new cross-document check reads every sentence of every document |
| 6 | Milestone gates omitted the remediation tests | §4.1 of the sequencing document is a **manifest**: every ID of every canonical assurance inventory is assigned to exactly one gate. Rule SQ-1a makes it a checked partition — an inventory ID in no row, a manifest ID in no inventory, or an ID in two rows all fail — and SQ-1b requires a new test to be assigned in the same change. Six gates that carried hand-written contiguous lists now point at their manifest row. A48–A55, P-A49 and the six new IDs are required by `G-K`, `G-M` and `G-N`. Suffixed and non-contiguous IDs are first-class; ranges are rejected |
| 7 | Six nearby mutations escaped the V5 harness | Three checks, all of which compare **derived** facts across **every** active location rather than reading one canonical sentence. The routing check treats **only** `persistence-and-transaction-model.md` §7.2 as the owner and compares the API branch table, the router branch table and all prose against it; it scans **paragraph units** so a wrapped sentence cannot hide, and applies the historical exemption **per sentence** so one "no longer exists" clause in a long table row cannot exempt the rest of it — which is precisely how two of the six escaped a first attempt at this check. The unknown-effect check rejects any line pairing an unknown external effect with automatic replay. The refusal-equality and obsolete-command checks already scanned every document and are extended. All six escape classes are reproduced as committed probes (§12.1, probes 8–13) |

### 12.1 Assurance added for exactly these failures

Fourteen new probes, each detected by a named substantive check:

| # | Weakening | Caught by |
|---:|---|---|
| 1 | A time-dependent partial index returns as an ownership constraint | The outbox protocol is implementable and vendor-free |
| 2 | A redundant identity uniqueness restates `O1` | The outbox protocol is implementable and vendor-free |
| 3 | The crash point after provider acceptance is removed | The external-call boundary is crash-safe and every transition is fenced |
| 4 | Settlement stops being token-fenced | The external-call boundary is crash-safe and every transition is fenced |
| 5 | Stage 3/4 success stops settling the dispatch item | The external-call boundary is crash-safe and every transition is fenced |
| 6 | A normative rule identifier is defined twice | No normative rule identifier is defined twice |
| 7 | A remediation test is required by no milestone gate | The assurance manifest partitions the canonical inventories |
| 8 | Stale routing cardinality prose returns to the self-check narrative | No active location contradicts the routing branch semantics |
| 9 | **B3** loses its run-state append in the **API** branch table | No active location contradicts the routing branch semantics |
| 10 | **B4n** loses its inherited consequence in the **API** branch table | No active location contradicts the routing branch semantics |
| 11 | **B1r** advances the submission ordinal in nearby API prose | No active location contradicts the routing branch semantics |
| 12 | A nearby **router** location drops B4n's run-state appends | No active location contradicts the routing branch semantics |
| 13 | A nearby **assurance** location requires equal total execution-event counts | A required refusal event never contradicts observational equality |
| 14 | A nearby location permits automatic redispatch of an unknown effect | No active location permits auto-redispatch of an unknown external effect |

Probes 8–13 are the six V5 escapes reproduced exactly: each edits a **second** statement of a
fact while the canonical table stays correct. Five of the fourteen were `REDUNDANT` on their
first run — three because the checks read one line at a time and the sentences that carried the
claim had wrapped, and two because a single historical clause in a long table row exempted every
other claim in the same row. Both defects were in the checks, both were found by the fixture, and
both are recorded here rather than quietly repaired.

## 13. The re-audit V6 blockers, and how each was closed

| # | Blocker | Closed by |
|---:|---|---|
| 1 | PO-14 / PO-19 permitted conditional redispatch after `boundary_crossed = true`, and `T1`–`T10` contained **no fenced path that could perform it** — a permission with no mechanism | **Option B.** Crossed-boundary redispatch is removed entirely. PO-14 now reads: once `boundary_crossed = true` this dispatch item never presents its key again, under **any** condition — not on `CONFIRMED_NOT_APPLIED`, not under a recorded deduplication guarantee, not after any elapsed time. Nothing is lost: where reconciliation reports `CONFIRMED_NOT_APPLIED` the work continues as a **new governed provider attempt** — new `ProviderAttemptRef` at the next `attempt_ordinal` under U22, new dispatch item, new key derived per PO-1 (PO-14a) — which is what Phase 11 means by re-attempting where the retry class permits, and which leaves an audit trail rather than an operational replay. PO-14b states that receiver-side deduplication licenses nothing here; PO-19's verdict column now reads `Never` in every crossed row, with no condition attached, and the validator reads that column rather than a sentence |
| 2 | F-9a / F-9d / PO-8 and T6 did not distinguish the recovery conditions | **Rule F-9a-map** is the single mapping, and it separates the five conditions the earlier wording collapsed: claim expired **before** the boundary (no call was made — a conclusion the local state is entitled to, PO-8); claim expired **after** it (nothing may be concluded); unknown effect; confirmed-not-applied; settled. F-9a no longer says an expired lease *always* reads as unknown — it says expiry proves nothing by itself and the **boundary flag** decides. Conditions 1 and 2 are named as the pair that was collapsed, and the dangerous reading is named explicitly |
| 3 | T10 retired a row from `PENDING` **or** `CLAIMED` without ownership predicates | Split into **T10** (from `PENDING`, requiring `lease_owner IS NULL`) and **T11** (from `CLAIMED`, fencing on `lease_owner`, `claim_token` **and** `claim_generation` together). **PO-10a**: a non-owner or a stale writer matches **zero rows and writes nothing**, and does **not** fall back to T10, whose predicate requires an unowned row; an abandoned owned row is recovered by T6 first and retired second, because collapsing the two is how a live claimant's row gets retired out from under it. **PO-10b**: retirement applies only where `boundary_crossed = false` **and** the governed intent is itself terminal, and `terminal_reason = RETIRED_BEFORE_DISPATCH` keeps a retired `SETTLED` row distinguishable from a resolved one |
| 4 | `CHECK (claim_generation >= 0)` cannot enforce monotonic increase, and was presented as if it could | `O5` is reclassified in its own row as a **row-shape** constraint that "enforces no ordering between successive updates", and **PO-4** states plainly that **monotonicity is not claimed as a database guarantee**: it is per-transition, enforced by every §9.4 predicate requiring `claim_generation = <the value read>` and writing `+ 1`, and it holds only because no write path outside §9.4 exists. A trigger or `IDENTITY` column is named as what a database-level guarantee **would** take, and explicitly not specified. A64 is the adversarial row that fails if anything relies on `O5` for ordering |
| 5 | `O1`–`O4` and `O1`–`O5` both appeared as current | The surviving `O1`–`O4` in `api-command-contracts.md` Q-22a is corrected; the only remaining mentions of the four-constraint inventory are in §10's revision-5 blocker row, where the sentence says what that revision did. The transition count is corrected from ten to **eleven** in both documents that state it |
| 6 | The V6 reviewer tested 14 nearby mutations and **9 escaped** | Four new checks and fourteen new probes, planted in **second and third** active locations rather than in the owner. New: a stale-writer check reading every statement for a stale generation, token or owner being allowed to act; an idempotency-key check for any permission to regenerate a dispatch item's key; an outbox-classification check that requires the governed claim to **attach to the outbox subject**; and a rule-reference check that resolves every cited `Rule <id>` against the definitions. The rule parser now reads **blockquoted** definitions (`P-14a` was being skipped), the definition count is derived rather than frozen, and the refusal-equality check scans every statement instead of only the adversarial table. Historical exclusions stay sentence-scoped and are named in one explicit pattern; git-dependent checks still grant no mutation credit |

### 13.1 Assurance added for exactly these failures

Fourteen new probes, each detected by a named substantive check:

| # | Weakening | Caught by |
|---:|---|---|
| 1 | B3 loses its run-state append in a **third** active location | No active location contradicts the routing branch semantics |
| 2 | B4n loses its inherited consequence in the Q-17d rule | No active location contradicts the routing branch semantics |
| 3 | B1r consumes an ordinal in a **third** active location | No active location contradicts the routing branch semantics |
| 4 | A stale owner's write is honoured outside the transition table | No active location weakens the stale-writer fencing semantics |
| 5 | The provider idempotency key is regenerated in a second active location | No active location permits regenerating a dispatch item's key |
| 6 | The outbox is reclassified as governed outside the owning rule | No active location reclassifies the outbox as governed |
| 7 | Refusal equality is restated to include the execution-event count | A required refusal event never contradicts observational equality |
| 8 | A stale transaction-table row count survives in active prose | Every normative count matches its canonical inventory |
| 9 | An unknown effect is auto-redispatched in a second active location | No active location permits auto-redispatch of an unknown external effect |
| 10 | A **blockquoted** rule definition collides with an active rule id | No normative rule identifier is defined twice |
| 11 | An active rule reference points at a rule that does not exist | Every active rule reference resolves to a definition |
| 12 | Crossed-boundary redispatch returns as a conditional permission | The external-call boundary is crash-safe and every transition is fenced |
| 13 | T11 stops fencing retirement on the current owner | The external-call boundary is crash-safe and every transition is fenced |
| 14 | `O5` is presented as enforcing monotonic increase | The external-call boundary is crash-safe and every transition is fenced |

Two of the fourteen were `REDUNDANT` on their first run, and both exposed a real weakness in the
checks rather than in the specification: a phrase-list that matched "advances the ordinal" but not
"advances to reserve", and a denial list that treated the word *operational* as a denial — so a row
calling the outbox operational in one column while calling its rows governed records in another
was exempt from the check written to catch exactly that. Both are fixed and both are recorded here.

## 7. Known limitations of this self-check

1. It is a producer self-check. The producer of a specification is the last party who should
   certify it.
2. It asserts that obligations are **specified**, not that they are **correct**. Whether the
   canonical uniqueness inventory holds the right constraints, whether the transaction table is
   exhaustive over the right acts, and whether the adversarial inventory covers the real attack
   surface are questions for an independent audit.
3. Nothing here has been executed. A specification cannot be run, and no test in this package
   has been written, let alone passed.
4. The four blocked authorities mean an implementation built exactly to this specification would
   hold no canonical positions, destroy nothing, re-parent no scope, and never contract a schema
   against governed data. That is intended and it is also a substantial functional limit.
5. **A green harness has now six times missed real contradictions.** 74/74, then 81/81, then
   90/90, then 97/97, then 102/102 with 73 probes' worth of confidence, each coexisted with
   blockers an independent reader found. In the V6 round the reviewer tried fourteen nearby
   mutations and **nine survived** — the harness's own probes were all passing at the time. Every round the missed defects were cross-document or localized —
   never inside one table a single check was looking at, and in the V5 round they were
   deliberately planted *beside* the canonical statement rather than in it. The `crossdoc` group
   has grown from 6 checks to 27 for that reason, and the honest reading is unchanged: **it
   closes what was found.** 102/102 and 73/73 are not evidence that nothing else is wrong, and
   this package's credibility should not be rated higher merely because the numbers went up.

8. **Defects the harness itself introduced are now a pattern, not an incident.** The duplicate
   `P-23` and the non-implementable `O4` predicate arrived in revision 5 and passed 90/90. The
   revision-6 fix then introduced a *permission with no mechanism* — PO-14 allowed a redispatch
   that no transition could perform — and passed 102/102 with 73 probes green. Each was found by
   a human reader, not by the harness. The right conclusion is not that the next round will be
   clean; it is that **this package's correctness has, every round, been established by
   independent reading and not by its own validator**, and the validator's totals should be read
   with that in front of them.

9. **Nothing in this package has been executed.** The outbox protocol is specified as
   implementable; no statement in it has been run against a database, and claims such as "this
   predicate is implementable" are reasoned judgements about SQL semantics, not test results.

7. One probe of revision 5 — the outbox losing its stable identity and uniqueness — came back
   `REDUNDANT` on its first run, because the check it attacked asked whether the constraint rows
   existed rather than what they constrained. The check now parses each row's constraint cell.
   That gap was found by the fixture, is recorded here rather than quietly repaired, and is the
   reason the fixture exists.
6. **The earlier form of this note said "twice".** 74/74 and 19/19 coexisted with
   six blockers, five of which were cross-document disagreements no single-document check could
   see. The `crossdoc` group exists because of that, and the honest reading is that it closes the
   contradictions that were found — not that no others remain.

## 7z. The V7 remediation — B1 and B2

The V7 independent re-audit returned two HIGH blockers against `46a7a89`. Both were the same
shape as the ones before them: an owner contract that was already right, contradicted by active
second locations that nobody had read.

| Blocker | What contradicted the owner contract | What it is now |
|---|---|---|
| **B1** — external delivery / replay | PO-17 defined at-most-once per dispatch item. Q-26 claimed **external at-least-once** "where the provider deduplicates"; Q-24's crash row, the T5 and T7 transition cells and the §9.6 crash summary all carried a stale "unless / except under PO-14" qualifier, left behind when PO-14 became unconditional | Q-26 is a three-row *not claimed* table — no exactly-once, no external at-least-once, nothing licensed by provider deduplication. The qualifiers are gone: T5 and T7 read **"Never — PO-14 is unconditional"**, and §9.6 says PO-14 admits no exception. **P-9x** and **O-21a** state, in the two documents whose class tables use the word *at-least-once*, that it names an internal retry class and never an external guarantee |
| **B2** — governed writes in a no-governed-write class | Q-25 assigned `SAFE_AUTOMATIC_RETRY` to stages 1, 3, 4 and 5. The approved Phase 11 class 1 requires *"no governed record written"*, and stage 1 alone writes two | Q-25 is now a per-stage table of **what each stage writes** against **its class**: stages 1, 3+4 and 5 are class 2 `RETRY_REQUIRING_REVALIDATION`; stage 2 is unchanged. **Q-25b** separates three properties an earlier revision had collapsed — *not authority-bearing*, *writes a governed record*, *replay-safe under a durable key*. **Q-25c** states that durable request identity (§6, Q-9/Q-10) is the **mechanism** that makes a client retry harmless, and is not the Phase 11 class. The approved class definitions are unchanged |

### Assurance, and four probes that came back REDUNDANT

Two checks were added and twelve probes, each planted in a distinct active location. Four probes
were `REDUNDANT` on their first run and one on the second, and every one exposed a defect in a
check rather than in the specification:

1. **A conditional redispatch planted in Q-24 was not observed.** `_HISTORICAL` carries the token
   `before the`, which every crash row contains — *"before the stage 3/4 commit"* — so the whole
   row was exempt. A qualifier **on** the no-redispatch rule is now judged without that exemption.
2. **T5 was read by nothing.** The crash-safety check filtered transitions whose text says
   *recovery*; T5 is a caller-observed unknown, not a recovery. Every transition leaving
   `DISPATCH_PENDING` is now read, and each must deny redispatch unconditionally.
3. **"Redispatch where provider deduplication permits it" was not observed.** The scan read one
   word order only. It now reads both.
4. **A governed-write step reaching the class-1 branch was not observed**, because the row scan
   did not recognise the hyphenated form *governed-write*.
5. **On the second run, the Q-26 probe was REDUNDANT** — and this one was a defect in the
   **probe**, not the check: it replaced only the row's prefix, leaving the original cell's
   *"never presents its key again"* in place, so the mutated row still denied what it was
   supposed to assert. The probe now replaces the whole row, and the check additionally reads
   Q-26's *not claimed* table as data, so a row that flips to *provided* fails whatever words it
   uses.

Also repaired, and worth naming because it is the mirror image of the usual defect: the
crash-safety check demanded the literal substring `no` in the redispatch cell and therefore
**rejected the stronger wording "Never — PO-14 is unconditional"**. A check keyed on one spelling
of a denial is not a check on the denial.
