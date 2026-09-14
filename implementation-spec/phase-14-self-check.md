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
| Validator checks | **97**, in 14 groups: `structure` 6 · `containment` 6 · `invariants` 5 · `knowledge` 6 · `scope` 6 · `routing` 3 · `events` 5 · `authority` 5 · `persistence` 7 · `races` 5 · `approval` 4 · `completeness` 6 · `fidelity` 11 · `crossdoc` 22 |
| Validator | `validation/phase_14_validation.py`, standard library only, deterministic, no network |
| Adversarial fixture | `validation/phase_14_mutation_probes.py`, **59 committed controlled weakenings**, 59 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR` |
| Governed commands | **36**, each with exactly one transaction contract; the two sets are compared and equal |
| Durable uniqueness constraints | **23** (U1–U23), one canonical inventory, every stated count derived from it |
| Executable production code, migrations, manifests, SDK dependencies | **0** |
| Approved Phase 1–13 artifacts modified | **0** |
| Decision Rights created | **0** |
| Operations specified as permanently refusing until a Right is mapped | **4** |

Phase 14 validator result: `97/97 PASS` on default, `--verbose` and `--json`.

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

Current result: **59 probes, 59 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR`**, each caught by a named
substantive check. The twelve added in revision 5 are in §11.1, the sixteen from revision 4 in
§10.1, the twelve from revision 3 in §9.1, and the original set is:

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
| 1 | Three incompatible statements about the Routing Request lifecycle | **One lifecycle.** `RequestRouting` no longer exists as a governed command; the prospective envelope is constructed **inside** `route()` and reaches storage only with a validated answer. Four branches are encoded identically in the API inventory, the router contract and the transaction table: **B1** invalid answer → zero writes, zero audit events, one refusal event; **B2** selection and **B3** valid non-selection → request and decision commit together, 2 audit events; **B4** re-submission → the decision only, 1 audit event. A valid refusal **is** recorded because Phase 11 §3 says the refusals are the important half; an invalid answer is not, because it is the absence of an answer. **U6 was wrong and is corrected**: Phase 11 §5 says a retry re-submits the *same* request and every attempt's decision is recorded, so uniqueness is `(routing_request_ref, submission_ordinal)`, not one decision per request |
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
5. **A green harness has now four times missed real contradictions.** 74/74, then 81/81, then
   90/90 with 47 probes' worth of confidence, each coexisted with blockers an independent reader
   found. Every round the missed defects were cross-document or localized — never inside one
   table a single check was looking at. The `crossdoc` group has grown from 6 checks to 22 for
   that reason, and the honest reading is unchanged: **it closes what was found.** 97/97 and
   59/59 are not evidence that nothing else is wrong, and this package's credibility should not
   be rated higher merely because the numbers went up.

7. One probe of revision 5 — the outbox losing its stable identity and uniqueness — came back
   `REDUNDANT` on its first run, because the check it attacked asked whether the constraint rows
   existed rather than what they constrained. The check now parses each row's constraint cell.
   That gap was found by the fixture, is recorded here rather than quietly repaired, and is the
   reason the fixture exists.
6. **The earlier form of this note said "twice".** 74/74 and 19/19 coexisted with
   six blockers, five of which were cross-document disagreements no single-document check could
   see. The `crossdoc` group exists because of that, and the honest reading is that it closes the
   contradictions that were found — not that no others remain.
