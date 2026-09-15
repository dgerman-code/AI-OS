# Phase 16 — Assurance Synchronisation After B1/B3/B4/B5 Remediation

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-16-planner-activation`

This is a TARGETED ASSURANCE SYNCHRONISATION only.

Do not redesign Phase 16. Do not reopen closed architectural questions. Do not modify approved Phase 1–15 artifacts, registries, approval records, or upstream governance. Do not create a PR.

Current implementation/remediation line already changed the semantics in four important ways:

1. **B1** — Phase 4 architecture approval MUST NOT be treated as individual Skill approval. Current Skill cards may be `PROPOSED`; `approved_skills()` may therefore legitimately be empty unless explicit individual approval evidence exists. `carded_skills()` / declared Skill cards are evidence of card existence, not approval.
2. **B3** — `ActivationStore.issue()` requires successful-preflight provenance and must reject arbitrary/fabricated bases.
3. **B4** — Role↔Skill mappings are positive-evidence-only and section-aware; boundary/exclusion prose must never create a positive mapping; blank/placeholder owned conclusions block.
4. **B5** — unexpected runtime/import/path/crash failures are `RUNNER_ERROR`, never semantic `DETECTED`.

The implementation has been remediated, but the assurance layer still contains expectations from the pre-remediation semantics, especially assumptions that six carded Skills are individually approved and helpers/tests that search `approved_skills()` for positive mapping fixtures.

## Objective

Synchronise the Phase 16 assurance layer with the corrected implementation semantics WITHOUT weakening coverage.

## Required changes

### A. Unit tests

Update `implementation/phase-16/tests/test_activation_invariants.py` so that:

- it no longer assumes the six Phase 4 exemplar Skill cards are individually approved;
- it explicitly asserts that Phase 4 architecture approval alone does **not** make those Skill cards eligible for execution;
- card existence tests use `carded_skills()` or equivalent declared-card evidence, not `approved_skills()`;
- positive Role↔Skill parser tests operate at the mapping-parser level using carded Skills / authoritative mapping records, without implying execution eligibility;
- preflight tests prove a Skill requirement remains BLOCKED when the Skill lacks explicit individual approval, even if the card exists and mapping is positive;
- direct negative test remains for `skill.lifecycle_cost_analysis` vs CAPEX / Cost Engineering (or the exact authoritative Role ID) proving boundary/exclusion prose does not create compatibility;
- blank, whitespace and placeholder owned conclusions block;
- successful-preflight provenance is required for issuance; direct fabricated-basis-after-blocked-preflight attack remains covered;
- no test helper quietly reintroduces the false concept “approved exemplar Skill” unless actual explicit approval evidence exists.

Do not delete meaningful existing tests merely to make the suite green. Adapt fixtures to the corrected semantics.

### B. Validator

Synchronise `validation/phase_16_validation.py` (and any Phase 16 validator-core file introduced by the remediation) so that:

- it distinguishes **carded** from **individually approved** Skills;
- it does not assert `len(approved_skills()) == 6` unless repository evidence actually supports individual approval;
- it DOES assert that architecture-level Phase 4 approval cannot produce individual execution eligibility;
- it validates B3 successful-preflight provenance and fabricated-basis rejection;
- it validates B4 parser boundary/exclusion behavior and owned-conclusion substance;
- it emits structured JSON with an explicit top-level execution status sufficient for the mutation harness to distinguish semantic failure from runner/infrastructure failure;
- any unexpected runtime/import/path/crash exception produces `RUNNER_ERROR`, not an ordinary failed semantic check.

Preserve existing useful checks. Do not replace the validator with a tiny superficial wrapper that discards the prior behavioural coverage.

### C. Mutation harness

Synchronise `validation/phase_16_mutation_probes.py` so that:

- pristine copied control passes under the corrected Skill semantics;
- probes that formerly expected six approved Skills instead target the actual invariant: architecture approval alone cannot create individual Skill eligibility;
- add/retain a probe that tries to infer Skill eligibility from Phase 4 architecture approval and require semantic detection;
- add/retain the direct fabricated-basis issuance bypass probe;
- add/retain the boundary/exclusion mapping leak probe;
- add/retain blank-owned-conclusion bypass probe;
- add/retain deliberate unexpected `RuntimeError` probe and require `RUNNER_ERROR` (not DETECTED);
- `DETECTED`, `ESCAPED`, `REDUNDANT`, `RUNNER_ERROR` accounting remains honest;
- pristine-control failure means zero probes counted.

### D. Examples / docs only if required for consistency

Update Phase 16 examples or package docs only where they make statements inconsistent with the corrected B1/B3/B4/B5 semantics. Do not expand scope.

## Required execution

Run all of the following locally on the branch:

```bash
python3 -m unittest discover -s implementation/phase-16/tests -v
python3 validation/phase_16_validation.py
python3 validation/phase_16_validation.py --json
python3 validation/phase_16_mutation_probes.py --json
python3 implementation/phase-16/examples/executable_run.py
python3 implementation/phase-16/examples/blocked_run.py
git diff --check
```

Also run a direct temporary-copy check proving that an injected unexpected `RuntimeError` is classified `RUNNER_ERROR` and not `DETECTED`.

## Required reporting

Return:

A. ASSURANCE SYNC SUMMARY
B. EXACT STARTING HEAD
C. CHANGED FILES
D. UNIT TEST RESULTS
E. VALIDATOR RESULTS
F. MUTATION RESULTS — exact DETECTED / ESCAPED / REDUNDANT / RUNNER_ERROR counts
G. DIRECT B1 CHECK — carded ≠ individually approved
H. DIRECT B3 CHECK — blocked preflight + fabricated basis cannot issue
I. DIRECT B4 CHECK — boundary mapping + blank owned conclusion
J. DIRECT B5 CHECK — RuntimeError = RUNNER_ERROR
K. CONTAINMENT
L. REMAINING BLOCKERS
M. REMEDIATION SHA
N. VERDICT

If and only if the assurance layer is synchronized, all required commands pass under the corrected semantics, the direct checks pass, and there is no remaining implementation blocker, end exactly with:

`READY FOR FINAL SHORT PHASE 16 SURVIVOR CLOSURE REVIEW`

## Commit / push

When complete:

- commit the assurance synchronization;
- push to `implementation/phase-16-planner-activation`;
- do not create a PR;
- report the exact commit SHA and confirm the final worktree is clean.
