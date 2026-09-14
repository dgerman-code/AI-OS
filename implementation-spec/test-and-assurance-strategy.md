# Test and Assurance Strategy

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

## 1. What testing is for here, and what it is not

**Rule T-1 — a test suite is an assurance tool and never governance authority.** A green suite
is evidence that checks passed. It approves nothing, satisfies no gate, creates no Right, and
does not make an artifact canonical. A phase is approved by a human, recorded in a human approval
record; a passing validator is cited in that record as evidence and is not the decision.

**Rule T-2 — coverage is not assurance.** A test that asserts an object can be constructed proves
construction. The invariants in this architecture are about **relationships**: that a thing
cannot be substituted for another, that authority cannot be inferred, that a refusal leaves no
trace. Those need adversarial tests, not more constructors.

**Rule T-3 — no vacuous checks.** No `or True`, no tautology, no hard-coded pass counter, no
assertion that restates the implementation. A check that cannot fail is worse than no check,
because it is counted.

## 2. Nine test classes

| # | Class | Answers | Fails the build? |
|---:|---|---|---|
| 1 | **Unit** | Does this function do what it says? | Yes |
| 2 | **Contract** | Does each component honour its interface, including its refusals? | Yes |
| 3 | **Integration** | Do the components compose without a forbidden crossing becoming reachable? | Yes |
| 4 | **Adversarial** | Can a governed boundary be crossed by a caller actively trying? | Yes |
| 5 | **Mutation / controlled weakening** | Is each guard load-bearing, or is something else holding the line? | Yes |
| 6 | **Concurrency** | Do the ten races resolve to their named outcomes under real contention? | Yes |
| 7 | **Migration** | Does every migration preserve historical readability and its declared class? | Yes |
| 8 | **Recovery** | Do interrupted writes, orphans and unknown external effects reach their specified states? | Yes |
| 9 | **Architecture invariant** | Does the implementation still match the approved architecture documents? | Yes |

## 3. Adversarial tests — the required set

Each row is a test that must exist and must assert a **refusal plus observational equality**:
the whole observable state — four axes, gate outcomes, every governed record store, event count,
attempt counters — is identical before and after.

| # | Attack | Expected |
|---:|---|---|
| A1 | Offer a Model Result to a review gate, a decision gate, a human-work gate, a prerequisite gate | `EVIDENCE_TYPE_INADMISSIBLE` ×4 |
| A2 | Offer a Review Instance to a decision gate; a Decision Record to a review gate | Refused both ways |
| A3 | Offer an execution event, a log line, a metric or a trace as gate evidence | Inadmissible; there is no code path that accepts it |
| A4 | Supply a caller-constructed Routing Decision, Review Instance, Decision Record, Canonical Record | Not found in governed lineage; satisfies nothing |
| A5 | Submit a `HumanAuthorityRef`-shaped subclass, a duck-typed object, a string | `IDENTITY_KIND_INVALID` |
| A6 | Put a credential, service identity or agent instance in `decided_by` | Refused by the database check constraint |
| A7 | Complete a run with posture `AUTHORITY_ABSENT` or `GATE_UNSATISFIED` | `POSTURE_FORBIDS_COMPLETION` |
| A8 | Progress any ordinary API on a halted run | `RUN_HALTED`, all sixteen APIs |
| A9 | Widen scope, sensitivity or residency via a sub-run | `SCOPE_WIDENING_REFUSED` |
| A10 | Reach a sibling scope via a sub-run, or via `ORGANISATION/acme` → `ORGANISATION/acme_holdings` prefix | Refused; **the separator-boundary test** |
| A11 | Cross a scope with a bare mechanism reference, or with an authorisation whose Decision Record is not in the source run's retained history | `AUTHORISATION_NOT_CORROBORATED` |
| A12 | Use an intervention naming run B on run A — through recording, pause, unblock, cancel and terminate | `FOREIGN_RUN_LINEAGE`, all five paths |
| A13 | Repeat a stable governed identity — Decision Record, Review Instance, Routing Decision, Model Result, intervention | `DUPLICATE_GOVERNED_IDENTITY`, durable constraint |
| A14 | Retry a `NON_RETRYABLE_GOVERNED_ACT` or a `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT` | Halt and escalate, not an exception and not a no-op |
| A15 | Convert `AI_SUGGESTION` to `FACT_CLAIM` by approval, review, edit or acceptance | `EPISTEMIC_CONVERSION_PROHIBITED`; no such transition exists |
| A16 | Change an `origin` value after insert | Refused; column is immutable |
| A17 | Promote to canonical without precondition 9 | `NO_APPLICABLE_DECISION_RIGHT` — **and with a mapped Right mocked in, still refuses because no Right is mapped** |
| A18 | Exercise both ends of an active `SEPARATION_REQUIRED` pair as one human, directly and **via delegation** | `SEPARATION_VIOLATION` both ways |
| A19 | Satisfy a full-profile review as a `BOUNDED_REVIEW_CONTRIBUTOR` | `BOUNDED_CONTRIBUTOR_CANNOT_SATISFY` |
| A20 | Review one's own work under a class above `PRODUCER_REVIEW` | `PRODUCER_REVIEW_PROHIBITED` |
| A21 | Record a Routing Decision missing any one of the six reproducibility elements | `REPRODUCIBILITY_SET_INCOMPLETE`, six separate tests |
| A22 | Name a model on a non-eligible routing outcome | Refused by the check constraint |
| A23 | Invoke a model under a Routing Decision from another run, or record a result under a different Model Profile | `PROFILE_LINEAGE_MISMATCH` |
| A24 | Force a stale write by racing two updates | `STALE_WRITE`; **nothing written**; no merge |
| A25 | Supply `force`, `skip_checks`, `as_admin`, `bypass_rls` | Unknown field; the request is rejected |
| A26 | Reuse an idempotency key with a different payload | `IDEMPOTENCY_KEY_CONFLICT`; nothing executed |
| A27 | Adopt an orphaned storage object by hash or path | Refused |
| A28 | Exhaust a rework loop and expect it to iterate once more | `ESCALATED` with the iteration history intact |
| A29 | Read the execution-event or observability store from a governed module | Static check fails the build |
| A30 | Apply a `DESTRUCTIVE` migration, or mis-declare its class | Refused; classifier disagreement fails the build |

## 4. Concurrency tests — the ten races

Each race from `failure-recovery-race-model.md` §2 is exercised under **real contention** — two
processes against one database, not two threads with a mock. Each asserts the **named outcome**,
and each asserts that `LAST_WRITE_WINS` did not occur.

**Rule T-4 — the concurrency suite runs against a real PostgreSQL.** Races 2, 3, 7 and 10 are
enforced by constraints and version-pinned writes; a test double cannot demonstrate them. This
is the single largest assurance gap in the Phase 12 MVP and closing it is a milestone gate
(`implementation-sequencing.md` M6).

## 5. Mutation / controlled weakening

**Rule T-5.** Each load-bearing guard is removed in turn from a copy of the implementation, and
the scenario it protects is re-run. Each weakening is classified from **executable behaviour**:

| Classification | Means |
|---|---|
| `DETECTED` | Removing the guard changes observable governed behaviour and the scenario catches it |
| `REDUNDANT` | Removing it changes nothing observable, because another mechanism independently holds the line. **Recorded, never presented as a pass** |

**Rule T-6 — honesty rules.** A weakening whose target text is not found **fails loudly**; a
runner that quietly matches nothing proves exactly as much as no runner. Classifications are
re-derived by an independent check rather than trusted as labels. Documented counts are derived
from the executable manifest, never written by hand.

**Rule T-7 — required weakening targets.** At minimum: the halted guard; each uniqueness
constraint in `persistence-and-transaction-model.md` §5.2; the intervention contract; the
foreign-run lineage check; the six-part completeness check; the separation check; the scope
narrowing check; the separator-boundary ancestry test; the evidence contract; the
epistemic-conversion prohibition; the preflight in each act of §7's transaction table.

## 6. Architecture invariant tests

**Rule T-8 — compare against the documents, not against the code.** These tests parse the
approved architecture and fail when the implementation drifts, rather than agreeing with
themselves:

| # | Test |
|---:|---|
| I1 | The 21-object separation chain, parsed from `architecture/orchestrator-architecture.md` §2, matches the implemented reference types **exactly and in order** — set containment is not sufficient |
| I2 | `ALLOWED_TRANSITIONS` and `TERMINAL_REACHABLE_FROM` reconcile row by row with `orchestration/state-machine-and-transitions.md` §6 |
| I3 | Gate kinds (4), gate outcomes (7), continuing outcomes (2), retry classes (7), wait reasons (5), postures (4), phases (10), terminals (6), race outcomes (5), races (10) match the Phase 11 inventory |
| I4 | The four knowledge axes match `knowledge/knowledge-state-model.md` exactly — 8 epistemic types, 7 governance states, 4 origins |
| I5 | The nine sensitivity classes match `knowledge/sensitivity-and-retention-model.md` |
| I6 | The four applicability modes and the four ancestor-fallback rows match `knowledge/scope-isolation-and-transfer.md` |
| I7 | The scope node kinds and permitted parents reproduce `architecture/context-hierarchy.md` |
| I8 | The six reproducibility elements match `models/_templates/routing-decision-template.md` elements 20–25 |
| I9 | The 19 Decision Record elements match `architecture/decision-rights-registry-design.md` §8 |
| I10 | The 13 execution event fields match `orchestration/execution-audit-and-provenance.md` §2 |
| I11 | Every `decision.<id>` referenced by any governed artifact resolves in the Phase 7 universe |
| I12 | No governed module reads the execution-event or observability store |

**Rule T-9 — I1 is equality, not containment.** The Phase 12 validator's chain check computed
one-directional containment while its docstring claimed order. Containment passes when the
implementation has extra types or a different order. This specification requires exact ordered
equality.

## 7. Approval-gate tests

| # | Test |
|---:|---|
| P1 | An unapproved Workflow Definition version cannot start a run |
| P2 | An unapproved Decision Right Card version cannot satisfy a decision gate |
| P3 | An unapproved Review Profile version cannot satisfy a review gate |
| P4 | An unapproved schema version blocks a migration apply and a deployment |
| P5 | **Absence** of an approval-state row reads as `PROPOSED`, and refuses |
| P6 | `APPROVED_WITH_CONDITIONS` carries its conditions into every use and is not treated as `APPROVED` |
| P7 | A revoked approval refuses the **next** act and invalidates **no** historical Decision Record |
| P8 | The bootstrap transcription creates no row for a subject its source record does not name |

## 8. Static checks in CI

| # | Check |
|---:|---|
| S1 | No import of a provider SDK, HTTP client or database driver outside its designated adapter module |
| S2 | No read of the execution-event or observability store from a governed module (I12) |
| S3 | No `ON CONFLICT DO NOTHING` on any table in `persistence-and-transaction-model.md` §5.2 |
| S4 | No `UPDATE` statement targeting a column declared `IMM` |
| S5 | No `LIKE`-prefix scope predicate; the separator-boundary form only |
| S6 | No timestamp comparison used as a concurrency token |
| S7 | No vendor name in a governance module, schema column, API contract or routing rule |
| S8 | No `force` / `skip_checks` / `as_admin` / `bypass` parameter anywhere in the command surface |
| S9 | Migration declared class matches the classifier's derived class |
| S10 | Every governed table has a corresponding audit-event write in the same transaction |

## 9. Test data

**Rule T-10 — synthetic only, outside production.** No production governed record is copied into
a test fixture, a lower environment or a developer machine (`deployment-topology-and-environments.md`
Rule E-2).

**Rule T-11 — fixtures carry no real identifiers.** No real person, organisation, client,
project, provider or model appears in a fixture. Every identifier is an architecture placeholder,
following the Phase 11 exemplars' own convention.

## 10. Assurance reporting

**Rule T-12 — report the honest number.** Test counts, validator counts and mutation
classifications are read from the executable artifacts and never written by hand. A stale count
in a document is itself a finding.

**Rule T-13 — inherited conditions are reported exactly and not repaired out of scope.** Where a
regression validator carries a known inherited condition, it is reported as it stands, with its
cause, and is not "fixed" from a later phase.

**Rule T-14 — credibility is self-assessed and named.** Every assurance report states the
credibility of its own harness and what limits it. An unqualified claim of correctness is not
available.
