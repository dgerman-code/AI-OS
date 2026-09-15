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
| `validation/phase_16_validation.py` | **204/204 PASS** |
| `validation/phase_16_mutation_probes.py` | **91/99 DETECTED**, 8 ESCAPED (all defence-in-depth, enumerated below), 0 REDUNDANT, 0 RUNNER_ERROR, against a pristine copied control at 204/204 |
| `implementation/phase-16/tests/test_activation_invariants.py` | **71 tests, OK** — the 15 mandatory acceptance scenarios plus the B1–B4 negative cases |
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

## 2a. What the B1–B5 remediation changed, and what it exposed

An independent review returned five blockers. Each was a case of this package asserting
something it had not established.

| # | What was wrong | What it means |
|---:|---|---|
| **B1** | Role IDs were slugged from display names, inventing three identities that exist nowhere; every other registry was scraped from backticked mentions, reporting 224 Skills, 44 Review Profiles, 97 Decision Rights and 57 Workflows where the carded sets are 6, 6, 8 and 4 | The registry views were **failing open**. `registry-eligibility-contract.md` now states the evidence rule; eligibility is a declaration plus a version plus a human approval record, and anything missing resolves to the empty set |
| **B2** | `material_digest()` omitted clarifications, scope ancestry, the Orchestrator policy reference, stage `expected_artifact` and the declared open items | Changing any of them left an issued basis standing that no longer described the plan. All are now digested, and a classification invariant makes an unclassified new field an error at import |
| **B3** | Issued bases were mutable and handed back by reference; the trigger builder compared one digest | A holder could edit an issued governed record and nothing downstream could tell. The basis is frozen and sealed, the store owns the lifecycle, and `verify_basis` checks issuance, version, seal, status, both identities, scope, ancestry, mode, criticality, both bindings, policy, digest, spec version and the two false flags — one condition at a time, so a refusal names the field |
| **B4** | Duplicate stage ids collapsed silently, stage owners were never resolved, and Skill-to-Role bindings were never checked | Three ways to issue a basis over a composition that does not hold together. All three now block before issuance |
| **B5** | The probe fixture omitted the approved registry documents, and counted any non-zero exit as detection | The fixture was not isolated and the totals were not honest. Both are fixed; see §2b |

## 2b. The mutation harness, and why its numbers dropped

The previous harness reported 47/47 caught. That number was not earned:

- the throwaway copy did not contain `roles/`, `skills/`, `reviews/`, `decisions/` or
  `workflows/`, and the registry module derived the repository root from its own `__file__`, so
  every probe run silently read the **real** tree. The isolation was fictional;
- any non-zero exit counted as a catch, so an import error, a path error or a crashed
  interpreter were all indistinguishable from a detection.

Now: the copy carries every read-only dependency, the registry root is pinned to it, a
**pristine copied control must pass** before any mutation result is counted, and outcomes are
four — `DETECTED`, `ESCAPED`, `REDUNDANT`, `RUNNER_ERROR` — with `RUNNER_ERROR` never counted
as a detection. The result is **91 detected of 99, 0 redundant, 0 runner errors**.

The eight escapes are enumerated in the harness's own docstring. Every one breaks a *second*
line of defence while a stronger first line still holds — the payload seal, the material
digest, the `work_plan.` prefix check, or a guard made unreachable by the duplicate-stage block.
Two of them, `the Role cross-check is dropped` and the seal-covered tampers, are mutations that
change no result on a clean tree at all. They are kept and named rather than deleted: a probe
that escapes for a stated reason is evidence, and a probe quietly removed is not.

## 3. Where the assurance is weak, stated plainly

| # | Limit |
|---:|---|
| L-1 | **The validator tests the reference implementation, not a production system.** The implementation is in-memory and single-process. Nothing here shows the rules survive concurrency, a real store, or a real provider boundary |
| L-2 | **Correctness of the Execution Basis as an idea is untested and untestable here.** Every check assumes the object is the right answer to PO-4. If independent review judges it the wrong answer, a green validator says nothing |
| L-3 | **The material-field list is asserted against itself.** The validator checks that scope, objective, criticality and the requirement sets are material. It cannot check that the list is *complete*, because completeness is a judgement about what changes authority |
| L-4 | **Registry views are still derived by parsing approved documents.** The parse now reads declarations rather than mentions, cross-checks Roles against the approved universe in both directions, and requires named approval evidence per kind — but the parser is Phase 16 code. A declaration format that changed in an approved card would empty that registry, which fails closed; a card that declared two identities would not be noticed |
| L-4a | **The approval evidence is a quoted phrase from each approval record.** That is evidence, and it is also brittle: an approval record reworded in a later governed pass takes its whole kind to empty until the phrase is updated. Fail-closed is the right direction for that brittleness, but it is brittleness |
| L-4b | **Carded sets are small.** Six Skills, six Review Profiles, eight Decision Rights, four Workflows. The bridge is demonstrated against what is actually approved, not against the candidate universes, and a plan needing an uncarded capability blocks. That is correct and it is also narrow |
| L-5 | **The prose layer is thin on purpose.** Around fifteen prose checks, not a hundred. The instruction was useful rather than exhaustive, and prose-only gaps are recorded as debt |
| L-5a | **Eight probes escape.** Each for a stated reason, none of them a rule nobody checks — but "defence in depth" is an explanation, not a proof, and a reviewer should read §2b rather than take it on trust |
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

**Pattern 3 — a check that reads the module's own list.** The check for caller-injected
governed records iterated `FORBIDDEN_IN_TRIGGER` itself, so deleting an entry from that list
deleted the check along with it. The probe that removed `review_instance` escaped for exactly
that reason. The validator now also lists the required members literally.

**Pattern 4 — a mutation masked by a different guard.** A probe that disables one check while a
stronger check still refuses looks like a validator gap and is not one. Several C-6 probes
escaped this way until the checks were rewritten to isolate the rule — MATCH mode, so no
stage-owner guard stands in; and asserting the specific `BlockReason`, so a plan blocked for
some other reason is not counted as this rule working.

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
