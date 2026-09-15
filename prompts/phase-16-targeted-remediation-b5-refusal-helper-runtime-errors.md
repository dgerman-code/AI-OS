# Phase 16 Targeted Remediation — Final B5 Refusal-Helper Runtime Classification

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-16-planner-activation`

This is a FINAL TARGETED REMEDIATION for the sole remaining Phase 16 blocker.

Do not redesign Phase 16. Do not reopen B1, B2, B3 or B4. Do not modify approved Phase 1–15 artifacts, registries, approval records or upstream governance. Do not create a PR.

Independent final survivor review on exact baseline:

`5400930ac97d2fff18349ed79efa606f274de2fb`

closed B1, B3 and B4 and found exactly one remaining blocker:

**B5 — unexpected runtime faults absorbed by the assurance `refuses()` helper are converted into ordinary semantic failures and therefore counted by the mutation harness as DETECTED instead of RUNNER_ERROR.**

The review reproduced this with implementation unchanged: an injected `RuntimeError` inside the assurance helper produced JSON `status: FAIL`, exit 1, and mutation outcome DETECTED rather than RUNNER_ERROR.

## Required outcome

Fix only the assurance classification path so that unexpected assurance/infrastructure/runtime faults cannot be converted into semantic findings.

### 1. Refusal helper contract

In `validation/_planner_activation_validator_core.py`:

- `refuses()` must distinguish an expected governance/refusal exception from an unexpected infrastructure/runtime exception.
- Expected exception(s) supplied by the caller remain semantic success for a refusal check.
- A wrong but ordinary domain/governance outcome that genuinely shows implementation behaviour differs from the asserted contract may remain a semantic failure.
- Unexpected infrastructure/runtime faults such as `RuntimeError`, `ImportError`, `OSError`, `SyntaxError`, `MemoryError`, `RecursionError`, `SystemError` (and equivalent unexpected assurance execution faults) MUST escape into the validator runner as infrastructure failure rather than being converted into `False, "wrong exception ..."` or any ordinary failed check.
- Do not classify every implementation exception as infrastructure. Preserve the current intended distinction documented by the assurance sync: genuine implementation-regression behaviour should remain semantic FAIL; assurance/runtime failure should be RUNNER_ERROR.

Use the narrowest sound mechanism. If a small explicit exception-classification helper is appropriate, use one. Do not introduce broad `except Exception -> semantic fail` handling that recreates the defect elsewhere.

### 2. Validator wrapper contract

In `validation/phase_16_validation.py` and/or validator core only where needed:

- confirm a runtime fault escaping `refuses()` reaches the existing RUNNER_ERROR path;
- JSON must report top-level `status: RUNNER_ERROR` and non-zero `runner_errors` for the deliberate fault;
- exit code must remain the established RUNNER_ERROR code (currently 2, if unchanged by the existing contract);
- semantic validation failures must still be distinguishable as `status: FAIL`, not RUNNER_ERROR.

Do not shrink or replace the behavioural validator core.

### 3. Mutation harness

In `validation/phase_16_mutation_probes.py` only as needed:

- add or repair a direct probe that injects a deliberate `RuntimeError` specifically through the `refuses()` helper path;
- expected outcome for that probe MUST be `RUNNER_ERROR`;
- it MUST NOT count as DETECTED;
- retain the already-existing import-time and section-level runtime probes;
- preserve honest DETECTED / ESCAPED / REDUNDANT / RUNNER_ERROR accounting;
- pristine copied control must pass before probes are counted.

### 4. Direct regression tests

Add a narrowly targeted test proving all three cases remain distinct:

1. expected governance/refusal exception -> refusal check passes semantically;
2. genuine semantic mismatch -> validator reports FAIL;
3. injected unexpected RuntimeError inside/through `refuses()` -> validator reports RUNNER_ERROR and the mutation harness classifies RUNNER_ERROR, not DETECTED.

Do not weaken or delete existing B1/B3/B4 coverage.

## Required execution

Run:

```bash
python3 -m unittest discover -s implementation/phase-16/tests -v
python3 validation/phase_16_validation.py
python3 validation/phase_16_validation.py --json
python3 validation/phase_16_mutation_probes.py --json
python3 implementation/phase-16/examples/executable_run.py
python3 implementation/phase-16/examples/blocked_run.py
git diff --check
```

Also perform a direct temporary-copy reproduction of the exact independent-review attack:

- pristine copied validator PASS;
- inject a `RuntimeError` through the assurance refusal helper;
- validator JSON must be `RUNNER_ERROR`, not `FAIL`;
- mutation classifier outcome must be `RUNNER_ERROR`, not `DETECTED`.

## Containment

Changes should be limited to the Phase 16 assurance layer unless a tiny Phase 16 test fixture adjustment is strictly required:

- `validation/_planner_activation_validator_core.py`
- `validation/phase_16_validation.py`
- `validation/phase_16_mutation_probes.py`
- `implementation/phase-16/tests/` only if required for the regression test
- `planner-activation/phase-16-self-check.md` only if its assurance statement needs factual alignment

Do not modify implementation semantics in `domain.py`, `registries.py`, `preflight.py`, `store.py`, `handoff.py` unless the independent B5 reproduction proves this is unavoidable. The blocker is currently assurance infrastructure, not Phase 16 implementation behaviour.

## Required reporting

Return:

A. SUMMARY
B. EXACT STARTING HEAD
C. CHANGED FILES
D. B5 ROOT CAUSE
E. B5 FIX
F. DIRECT REFUSAL-HELPER RUNTIME REPRODUCTION
G. UNIT TEST RESULTS
H. VALIDATOR RESULTS
I. MUTATION RESULTS — exact DETECTED / ESCAPED / REDUNDANT / RUNNER_ERROR counts
J. CONTAINMENT
K. REMAINING BLOCKERS
L. REMEDIATION SHA
M. VERDICT

If and only if B5 is closed, all required commands pass, the exact refusal-helper RuntimeError reproduction is classified RUNNER_ERROR, and no new blocker is introduced, end exactly:

`READY FOR FINAL SHORT B5 CLOSURE REVIEW`

## Commit / push

When complete:

1. commit the targeted remediation;
2. push to `implementation/phase-16-planner-activation`;
3. do not create a PR;
4. report exact remediation SHA and confirm the final worktree is clean.
