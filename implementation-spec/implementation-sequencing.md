# Implementation Sequencing

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

## 1. The sequencing principle

Build **the things that make a bypass impossible before the things that would use the bypass.**

Every ordering decision below follows from one observation: a governance property enforced by a
constraint survives a second process, a restart, a race and a careless caller. A governance
property enforced by the order in which one process calls its own methods survives none of them.
So identity, uniqueness and concurrency come before any act that depends on them, and every act
that produces an external effect comes last.

**Rule SQ-1 — no milestone is complete while a later one is needed to make its guarantees
true.** A milestone that "will be safe once M6 lands" is not complete.

## 2. Milestones

| M | Milestone | Delivers | Depends on |
|---|---|---|---|
| **M0** | Foundations | Repository, CI, static checks S1–S8, test harness skeleton, no application code | — |
| **M1** | Identity and scope | All reference types with kind-carrying equality and no subclass slack; scope nodes, canonical paths, ancestry with the separator-boundary test; sensitivity and residency | M0 |
| **M2** | Persistence spine | The ten data domains; every `IMM`/`APP` column rule; **every constraint in the canonical uniqueness inventory** (`persistence-and-transaction-model.md` §5.2 — currently **23**, U1–U23); `record_version` and version-pinned writes; append-only grants and their verification | M1 |
| **M3** | Audit and provenance | Audit events in the same transaction as every governed write; provenance records; the write-only execution-event interface; the observability plane, structurally unreadable | M2 |
| **M4** | Approval state registry | The registry, the bootstrap transcription, and the runtime oracle | M2 |
| **M5** | Definition registry | Git-sourced definitions at named versions; the registry projection; definition-load validation (bounded subjects, declared effects, acyclic graphs, declared rework loops) | M4 |
| **M6** | Concurrency proof | The ten races under real contention against real PostgreSQL; all outcomes named; `LAST_WRITE_WINS` demonstrated absent | M2, M3 |
| **M7** | Run lifecycle | Runs, Work Items, assignments, the four axes, the transition table reconciled against the architecture, the halted guard, `unblock` | M5, M6 |
| **M8** | Gates and evidence | The four gate kinds, the exclusive evidence contract, gate instances, `SATISFIED_WITH_OPEN_ITEMS` propagation | M7 |
| **M9** | Review and independence | Review requests and instances; independence classes; **identity-level SoD**; producer-review prohibition; bounded-contributor rule | M8 |
| **M10** | Decision authority | Decision Rights resolution, holder eligibility, cardinality, delegation, `DECISION_RIGHT_SEPARATION` with durable enforcement, the 19-element Decision Record | M8, M9 |
| **M11** | Knowledge and canonical | The four axes; versioning with no in-place edit; conflicts; freshness; canonical promotion **with precondition 9 refusing** | M10 |
| **M12** | Router | Candidate universe, fixed precedence stages, lexicographic preferences, the six-part reproducibility set, `route()` as one atomic act | M7, M10 |
| **M13** | Model invocation | The provider-neutral adapter contract; invocation and result lineage; a recording stub only | M12 |
| **M14** | Rework and retry | Bounded rework loops with iteration counting and retained instances; the seven retry classes; exhaustion escalation | M7, M8 |
| **M15** | Outbox and reconciliation | The outbox table and drain; external-effect uncertainty states; the reconciliation sweep | M2, M3, M6 |
| **M16** | Compensation | Intent / authorisation / execution lineage; compensation request / authorisation / execution | M10, M15 |
| **M17** | Supersession | The full `SUPERSEDED` path across runs, records, knowledge, artifacts, policies and registry versions | M11, M14 |
| **M18** | Security and access | Human/service/agent identity separation; RLS with the separator-boundary predicate; least-privilege grants per component; secrets boundary | M2, M4 |
| **M19** | Command surface | The command envelope, idempotency, the error vocabulary, the query surface | M7–M18 |
| **M20** | Assurance completion | **Every ID in each canonical assurance inventory** (`test-and-assurance-strategy.md` §2a), not a range: adversarial (**70**), positive controls (**13**), architecture invariant (**12**), approval-gate (**8**), static CI (**10**). Plus the mutation harness with honest classification | all |

## 3. Dependency graph, compressed

```
M0 → M1 → M2 →┬→ M3 →┬→ M6 ─────────────┐
              │      │                   │
              ├→ M4 → M5 → M7 → M8 →┬→ M9 → M10 →┬→ M11 → M17
              │                     │            │
              │                     └→ M14       ├→ M12 → M13
              │                                  │
              └→ M18                             └→ M16 ← M15 ← M6
                                                        │
                                            M19 ← all ──┘ → M20
```

## 4. Stop/go gates

A milestone is not complete until its gate passes. **A gate is not waivable by schedule
pressure**, and there is no partial credit.

| Gate | Blocks | Criterion |
|---|---|---|
| **G-A** | Leaving M1 | Every pair in the 21-object chain proven non-equal and non-substitutable; subclass, duck-typed and string substitution each refused; the separator-boundary ancestry test passes |
| **G-B** | Leaving M2 | Every constraint in the canonical uniqueness inventory (currently **23**) exists and is demonstrated by a failing duplicate insert each; no `ON CONFLICT DO NOTHING` anywhere; append-only grants verified |
| **G-C** | Leaving M3 | Every governed write has its audit event in the same transaction; the execution-event interface exposes **no read operation**; S2 passes |
| **G-D** | Leaving M4 | Absence of an approval row reads as `PROPOSED` and refuses; the bootstrap creates no row its source does not name |
| **G-E** | Leaving M6 | **All ten races** resolve to their named outcomes under two-process contention; `LAST_WRITE_WINS` demonstrated absent |
| **G-F** | Leaving M7 | All sixteen ordinary APIs refuse on a halted run; the transition table reconciles with the architecture document; observational equality holds for every refused act |
| **G-G** | Leaving M8 | Each gate kind admits exactly one evidence type; every ID in this gate's §4.1 manifest row passes |
| **G-H** | Leaving M9 | Every ID in this gate's §4.1 manifest row passes; independence is evaluated on **identities**, not labels |
| **G-I** | Leaving M10 | Every ID in this gate's §4.1 manifest row passes, including via delegation; the separation check is durable, not in-memory; `NO_APPLICABLE_DECISION_RIGHT` is not `403` |
| **G-J** | Leaving M11 | Every ID in this gate's §4.1 manifest row passes; `PromoteToCanonical` **refuses**; no epistemic conversion edge exists |
| **G-K** | Leaving M12 | A21 passes for each of the six elements; every ID in this gate's §4.1 manifest row passes; an **invalid** route answer leaves **no governed record and no audit event, and appends exactly one refusal execution event** — which is coordination history and never governance evidence (O-25a) |
| **G-L** | Leaving M13 | No vendor name outside a Provider/Deployment Profile; S1 and S7 pass |
| **G-M** | Leaving M14 | Every ID in this gate's §4.1 manifest row passes; prior iterations retained; exhaustion escalates |
| **G-N** | Leaving M15 | Every ID in this gate's §4.1 manifest row passes: an interrupted external call reaches `ATTEMPTED_OUTCOME_UNKNOWN` and neither assumption is made; the eleven transitions of persistence §9.4 are exercised under contention and a stale token settles nothing |
| **G-O** | Leaving M16 | Compensation requires its own authorisation; an unauthorised compensation escalates with the effect standing |
| **G-P** | Leaving M18 | RLS and application scope checks are independently sufficient; no credential grants a Right |
| **G-Q** | Leaving M19 | No bypass parameter exists anywhere; S8 passes |
| **G-R** | Leaving M20 | **Every ID in every canonical assurance inventory passes** — adversarial **70**, positive controls **13**, architecture invariant **12**, approval-gate **8**, static CI **10**, all derived from the owning tables and none expressed as a range; mutation classifications re-derived independently; every documented count derived from its canonical inventory |

### 4.1 The assurance manifest — which gate requires which ID

**This table is the manifest.** It assigns **every** ID of **every** canonical assurance
inventory (`test-and-assurance-strategy.md` §2a) to exactly one gate. A gate row above that names
"this gate's §4.1 manifest row" requires every ID in its row here, and nothing else in this
document expresses an assurance requirement as a contiguous range.

**Rule SQ-1a — the manifest is a partition, derived and checked.** The validator parses the five
canonical inventories and the rows below, and fails on either error: an ID in an inventory that
appears in **no** manifest row (a test nobody's gate requires), or an ID in a manifest row that
exists in **no** inventory (a gate requiring a test nobody wrote). An ID appearing in two rows is
also a failure: a requirement owned twice is owned by neither. Suffixed IDs (`A12a`, `A17b`,
`P-A12c`) and non-contiguous IDs are first-class here; prefix matching is prohibited (Rule T-17).

**Rule SQ-1b — adding a test adds a manifest row entry in the same change.** A new adversarial
row or positive control that is not assigned here fails the validator rather than sitting outside
every gate, which is exactly how A48–A55 and P-A49 came to be required by nothing.

| Gate | Milestone | Required assurance IDs |
|---|---|---|
| **G-A** | M1 | A22, A23, A24, A25, I1, I2, I6, S3 |
| **G-B** | M2 | A26, A27, A30, I4, I7, S5, S6 |
| **G-C** | M3 | A29, A31, A36, A37, I5, I12, S2, S10 |
| **G-D** | M4 | A32, A33, A34, A35, P-A32, P-A34, P1, P2, P3, P4 |
| **G-E** | M6 | A13, I3, I8, S9 |
| **G-F** | M7 | A4, A5, A6, A7, A11, A12a, A12b, A12c, A12d, A12e, A12f, P-A12, P-A12c, I9, S4 |
| **G-G** | M8 | A1, A2, A3, A8, A9, A10 |
| **G-H** | M9 | A19, A20, P5, P6 |
| **G-I** | M10 | A18, P7, P8, I10 |
| **G-J** | M11 | A15, A16, A17a, A17b, A47, P-A17, I11 |
| **G-K** | M12 | A21, A38, A39, A40, A53, A54, P-A38, P-A40 |
| **G-L** | M13 | S1, S7 |
| **G-M** | M14 | A14, A28, A44, A45, A46, A55, A61, P-A44 |
| **G-N** | M15 | A41, A42, A43, A48, A49, A50, A51, A52, A56, A57, A58, A59, A60, A62, A63, A64, P-A41, P-A42, P-A49, P-A56, P-A62 |
| **G-O** | M16 | *(none assigned — see the note below)* |
| **G-P** | M18 | S8 |
| **G-Q** | M19 | *(none assigned — see the note below)* |
| **G-R** | M20 | *(none assigned — G-R requires **every** ID in every inventory and therefore owns none exclusively)* |

**Note on the three rows with no exclusive IDs.** G-O, G-Q and G-R carry criteria that are not
expressed as assurance IDs: compensation lineage, the absence of a bypass parameter, and the
whole-inventory requirement respectively. Writing a placeholder ID into those rows to make the
table look uniform would create an orphan, which Rule SQ-1a exists to reject. G-R is deliberately
the one gate that requires everything, and it is stated that way rather than by restating the
partition.

## 5. Four things that must never be built "temporarily"

**Rule SQ-2.** Each of these, once built, is used; and once used, removing it is a fight. None
is built at any milestone, at any point, for any reason:

| # | Never built |
|---:|---|
| 1 | A bypass parameter — `force`, `skip_checks`, `as_admin`, `bypass_rls`, `allow_unapproved` |
| 2 | An in-memory-only uniqueness or concurrency mechanism "until the constraints land" |
| 3 | A placeholder Decision Right, a default holder, or a configuration value naming an approver |
| 4 | A path that reads the execution-event or observability store to answer a governance question |

## 6. What gates progression past this specification

**Rule SQ-3.** No milestone begins until Phase 14 has passed independent audit and explicit human
approval. This specification is `PROPOSED`; it authorises nothing by existing.

**Rule SQ-4 — four blocked operations gate their dependents.** `PromoteToCanonical`,
`ReparentScopeNode`, `DestroyGovernedContent` and `ApplyDestructiveMigration` are built as
always-refusing enforcement hooks. Any feature whose value depends on one of them succeeding is
**out of scope until the applicable Phase 7 governed change maps the Right**, and is not
approximated by a workaround.
