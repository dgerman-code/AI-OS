# Phase 16 — Producer Self-Check

Status: `PROPOSED` — Phase 16 candidate.

This document is written by the party that produced the package. That is exactly why it is
worth reading sceptically, and why it is organised around what the assurance **cannot** show
rather than what it can.

Everything in the Phase 16 assurance layer is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY.
A passing check is evidence that a check passed. It approves nothing, satisfies no review,
creates no Decision Right, and does not make this proposal correct.

## 1. What was actually run

| Suite | Result |
|---|---|
| `validation/phase_16_validation.py` | **97/97 PASS** |
| `validation/phase_16_mutation_probes.py` | **47/47 CAUGHT**, 0 REDUNDANT, 0 dead patterns |
| `implementation/phase-16/tests/test_activation_invariants.py` | **31 tests, OK** — one or more per mandatory acceptance scenario |
| `implementation/phase-16/examples/executable_run.py` | runs; reaches an `EXECUTABLE` basis and a trigger answering all seven intake checks |
| `implementation/phase-16/examples/blocked_run.py` | runs; every blocked path blocks or refuses, none silently proceeds |

Inherited approved suites are reported in the delivery report rather than here, because Phase 16
did not author them and may not change them.

## 2. Where the assurance is strong

The Phase 16 validator is **behavioural first**, and that is a deliberate correction of a
failure mode this repository has hit repeatedly. Prose checks are satisfiable by editing one
sentence; a mutation planted in a second location inherits a corrective marker that was written
for the first. So most of the twelve required classes are checked by importing the reference
implementation and *attempting the forbidden act*:

- a basis in each of the five non-`EXECUTABLE` statuses is asked to produce a trigger, and each
  refusal is asserted individually rather than in aggregate;
- `exercise()` and `satisfy_review()` are called and the raise is required;
- every name in `FORBIDDEN_IN_TRIGGER` is attempted as an injected record, one probe per name,
  so the list cannot silently lose an entry;
- `is_approval` and `is_authority` are read as fields, so declaring them `true` is caught even
  though every sentence in the package still says `false`.

A rule that can be violated and merely logged is not enforced. Where a rule says something is
impossible, the check asserts the refusal, not a return value.

## 3. Where the assurance is weak, stated plainly

| # | Limit |
|---:|---|
| L-1 | **The validator tests the reference implementation, not a production system.** The implementation is in-memory and single-process. Nothing here shows the rules survive concurrency, a real store, or a real provider boundary |
| L-2 | **Correctness of the Execution Basis as an idea is untested and untestable here.** Every check assumes the object is the right answer to PO-4. If independent review judges it the wrong answer, a green validator says nothing |
| L-3 | **The material-field list is asserted against itself.** The validator checks that scope, objective, criticality and the requirement sets are material. It cannot check that the list is *complete*, because completeness is a judgement about what changes authority |
| L-4 | **Registry views are derived from approved documents by parsing.** The role count is checked (59) but the parse itself is Phase 16 code. A parser bug that dropped a role would be caught; one that merged two would not |
| L-5 | **The prose layer is thin on purpose.** Ten prose checks, not a hundred. The prompt asked for useful rather than exhaustive, and prose-only gaps are recorded as debt |
| L-6 | **`sensitivity` and `residency` default to `UNASSESSED`.** Intake check 4 is answerable, but Phase 16 performs no classification and the answer's quality depends on an upstream step this phase does not own |
| L-7 | **No inherited suite was extended.** Phase 8/9/10/11/12/14/15 validators are run unchanged as regression evidence. Phase 16 adds no check to any of them, so nothing here proves Phase 16 is compatible with an approved contract beyond what those suites already tested |

## 4. Known harness failure patterns, and what was done about them

Two patterns have caused REDUNDANT probes in earlier phases of this repository. Both are named
here rather than quietly worked around, because a self-check that hides its own failure modes is
worth less than no self-check.

**Pattern 1 — a corrective marker anywhere in a unit excuses a defect elsewhere in it.** A long
sentence or a table row that denies one thing lends its denial to an unrelated claim nearby.
Phase 16's mitigation is structural: the behavioural checks have no text unit to inherit from,
and each forbidden item is probed separately rather than as a set.

**Pattern 2 — a check keyed on one spelling of a denial.** A rule restated more strongly in
different words reads as a failure; a rule weakened in the same words reads as a pass. Phase 16's
mitigation is the same: behaviour has no spelling.

Neither mitigation is complete. The ten prose checks in §3 L-5 remain exposed to both, and the
probe list includes one prose probe per class precisely so that exposure is measured rather than
assumed.

## 5. What this package claims, and what it does not

| Claims | Does not claim |
|---|---|
| The mechanism described is implemented and the implementation refuses what the prose forbids | That the mechanism is the right one |
| PO-4 and PO-12 have a *proposed* closure with named dependencies | That either is closed |
| No approved artifact, registry or Decision Right was modified | Any authority to modify one |
| The path is demonstrable end to end at MVP level | Production, deployment or activation readiness |

## 6. Containment

Phase 16 writes only under `planner-activation/`, `implementation/phase-16/` and the two
`validation/phase_16_*.py` files. No approved Phase 1–15 artifact, approval record, registry,
validator or specification is modified. The five new open items PO-16-A through PO-16-E are
recorded in `po-4-and-po-12-closure.md` rather than left for a reviewer to discover.
