# Phase 14 Self-Check

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1

This is a **producer self-check**, not an independent audit. It records what this package
claims, what it does not, and where each Phase 13 obligation is discharged. Every number below
is read from an executable artifact, not written by hand.

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
| **R-2** | Persistent uniqueness / at-most-once | `persistence-and-transaction-model.md` §5 — twenty named durable constraints; `ON CONFLICT DO NOTHING` prohibited (P-7); a duplicate is a failure, not a newer entry (P-8); **exactly-once claimed nowhere** (P-9); reference-kind check constraints (P-10); durable decision-chain separation (P-11) | **Yes** |

## 3. Additional Phase 14 mandatory items

| Prompt § | Item | Where | Complete? |
|---|---|---|---|
| 4.3 | Concurrency and race implementation | `failure-recovery-race-model.md` §2 — all ten races with enforcement mechanisms; five outcomes; `LAST_WRITE_WINS` absent (F-1); optimistic concurrency and version-pinned writes (P-12…P-14); idempotency keys; correlation/causation; late review and late Decision handled **asymmetrically** with F-3 forbidding a shared code path | Yes |
| 4.4 | Compensation and non-replayable acts | `orchestrator-runtime-contract.md` §11; `failure-recovery-race-model.md` §7 — four-record lineage; four external-effect uncertainty states; the two forbidden assumptions (F-10); compensation request/authorisation/execution; originals never altered (F-14); **compensation may itself be unauthorised** (F-15) | Yes |
| 4.5 | Full `SUPERSEDED` path | `orchestrator-runtime-contract.md` §12 — eight object families, none destructive; a Decision Record is never superseded by amendment | Yes |
| 4.6 | Deferred Decision Rights | `open-items-and-blocked-authorities.md` §1 — four blocked authorities, each with operations, candidate identifier, enforcement hook, resolution path and the accepted consequence; B-1 forbids approximation | Yes |
| 6 | Specification depth | Every persisted record specified with field, type, nullability, mutability, uniqueness, references, lifecycle, allowed writer, authority, audit and error outcomes | Yes |
| 7 | Transactional rule under durable storage | `persistence-and-transaction-model.md` §7 — an eleven-act table with read set, validation set, concurrency check, writes, uniqueness relied on and pre-commit failure behaviour; staged/outbox/reconciliation where atomicity cannot span (§8, §9) | Yes |
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

Eleven, enumerated in `open-items-and-blocked-authorities.md` §2 (OI-1 … OI-11), each classified
as an **implementation precondition** (OI-2, OI-3, OI-4, OI-6, OI-8) or a
**production/organisational engineering deferral** (OI-1, OI-5, OI-7, OI-9, OI-10, OI-11). The
twelfth, OI-12, was **false and has been removed**: the Phase 4 approval record does state its
baseline commit, and the error originated in the Phase 13 review's own grep. Phase 14 declines to
make the remaining eleven because making them would create governance no approved phase
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
| Validator checks | **74**, in 13 groups: `structure` 6 · `containment` 6 · `invariants` 5 · `knowledge` 6 · `scope` 6 · `routing` 3 · `events` 5 · `authority` 5 · `persistence` 6 · `races` 5 · `approval` 4 · `completeness` 6 · `fidelity` 11 |
| Validator | `validation/phase_14_validation.py`, standard library only, deterministic, no network |
| Adversarial fixture | `validation/phase_14_mutation_probes.py`, **19 committed controlled weakenings**, 19 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR` |
| Executable production code, migrations, manifests, SDK dependencies | **0** |
| Approved Phase 1–13 artifacts modified | **0** |
| Decision Rights created | **0** |
| Operations specified as permanently refusing until a Right is mapped | **4** |

Phase 14 validator result: `74/74 PASS` on default, `--verbose` and `--json`.

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

Current result: **19 probes, 19 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR`**, each caught by a named
substantive check:

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
| 5 | Audit-event cardinality contradicted itself across prose, schema and tables | One rule, stated in both owning documents: **one audit event per persisted governed-record mutation, same transaction, linked to that record** (P-14a). No grouping (P-14c). Act-level correlation is distinguished from record-level cardinality (P-14b). §7.2 enumerates **17 governed acts** with their exact audit and execution counts; refusals write none (P-14e) |
| 6 | U19 keyed on a nonexistent `ACTIVE` approval status | Currentness is now a **pointer**, not a status: `approval_state_record` is an immutable version history (U21) and `approval_state_current` holds at most one row per subject version (U19). The rule is total — it covers `APPROVED_WITH_CONDITIONS` and every other operative status — and `ACTIVE` is explicitly absent (Rules AP-4a…AP-4c, P-9a, P-9b) |
| 7a | Rule I-1 claimed every reference is a stable-ID/version pair while the inventory held unversioned instance identities | Two categories: **A** governed definitions and profiles carry *(stable ID, version)*; **B** immutable runtime-instance and governed-record identities carry a stable identity **alone**, because there is no second version of an event that occurred. Rule I-1b states why this loses no reproducibility |
| 7b | A false OI-12 claiming Phase 4's approval record carried no baseline | Corrected. `reviews/phase-4-final-approval.md` line 7 states `Approved Baseline Commit: 8ddacb2b…`; the commit resolves, is an ancestor, and Phase 4's artifacts are byte-identical to it. OI-12 is **removed, not resolved** — there was never an open question. The error originated in the Phase 13 review and is named as mine |

## 7. Known limitations of this self-check

1. It is a producer self-check. The producer of a specification is the last party who should
   certify it.
2. It asserts that obligations are **specified**, not that they are **correct**. Whether the
   twenty uniqueness constraints are the right twenty, whether the eleven-act transaction table
   is exhaustive, and whether the thirty adversarial tests cover the real attack surface are
   questions for an independent audit.
3. Nothing here has been executed. A specification cannot be run, and no test in this package
   has been written, let alone passed.
4. The four blocked authorities mean an implementation built exactly to this specification would
   hold no canonical positions, destroy nothing, re-parent no scope, and never contract a schema
   against governed data. That is intended and it is also a substantial functional limit.
