# Communication Specialist — Exhaustive B3 Remediation

## Purpose

Close the one remaining blocker from the short independent blocker-closure review of baseline `8d1991649a22290ad5a1a18c058635d39e605457`.

This is **not** a redesign and not a general re-audit cycle. It is an exhaustive consistency sweep for one already-known invariant:

> A Decision Right may never substitute for a mandatory Review Profile satisfaction, an unresolved `CRITICAL_FINDING`, an unresolved `CONFLICT_DETECTED`, a missing/stale substantive conclusion, or any other unresolved professional-review/ownership condition. Decision authority and review satisfaction are separate governance objects.

The prior remediation correctly fixed this in the primary workflow and formal-escalation workflow, but the same exception survived in three second locations:

- `workflow-meeting-preparation.md`
- `workflow-boundary-setting.md`
- `workflow-refusal.md`

The independent closure review therefore returned FAIL solely because B3 remained partially open.

## Repository / branch

Repository: `dgerman-code/AI-OS`

Branch: `proposal/communication-difficult-conversations-specialist`

Required starting baseline: `8d1991649a22290ad5a1a18c058635d39e605457`

Before editing, verify branch HEAD descends from this baseline and print the actual HEAD SHA.

## Scope

You may modify only:

- proposal files under `proposals/communication-difficult-conversations-specialist/`
- `validation/communication_package_validation.py`
- `validation/communication_package_probes.py`

Do not modify approved Phase 1–15 artifacts, approved registries, Phase 14, human governance decision records, or unrelated prompts.

Do not create or approve any Decision Right.
Do not register the candidate Role, Skills, mappings, Workflows, or Review Profiles.
Do not create a PR.

## Required remediation

### 1. Fix all three known B3 survivors

Inspect and remediate the terminal-progression / exception language in:

1. `workflow-meeting-preparation.md`
2. `workflow-boundary-setting.md`
3. `workflow-refusal.md`

Each must become consistent with DIR-2 / FE-1 and with the approved review/authority separation.

At minimum:

- an unsatisfied mandatory review is never curable by a Decision Right;
- an unresolved `CRITICAL_FINDING` is never curable by a Decision Right;
- `CONFLICT_DETECTED` cannot be bypassed by a Decision Right unless the governing upstream architecture explicitly defines a distinct conflict-resolution authority path; do not invent one here;
- a missing, stale, or unresolved substantive-owner conclusion cannot be cured by communication authority;
- Decision Rights remain necessary where applicable, but they are additive to review satisfaction, never substitutes for it;
- terminal progression requires both review satisfaction and applicable Decision Right resolution as separate conditions.

If an unresolved placeholder exception remains valid, keep it narrowly scoped exactly as DIR-2 / FE-1 define it and do not generalise it.

### 2. Exhaustive package-wide sweep for the same semantic anti-pattern

Do not stop after the three named files.

Search every active package Markdown file for any wording equivalent to any of the following ideas:

- a named Decision Right permits progression despite an unsatisfied review;
- human authority can override a review requirement;
- Decision Right exercise can cure `CRITICAL_FINDING`;
- Decision Right exercise can cure `CONFLICT_DETECTED`;
- Decision Right exercise can cure a missing/stale substantive conclusion;
- unresolved professional-review items may remain if a decider permits progression;
- review satisfaction and Decision Right resolution are collapsed into one condition.

This search must be semantic, not only exact-string matching.

If additional second locations exist, remediate them in the same commit. Do not create a new blocker family; this is the same B3 invariant.

### 3. Add one package-wide validator check

Add a single structural/semantic validator check whose purpose is to guard the **entire workflow family**, not only named files.

It should inspect all six active workflow cards and fail if any workflow states or encodes that a Decision Right can substitute for:

- required review satisfaction;
- an unresolved critical finding;
- unresolved conflict;
- missing/stale substantive-owner conclusion.

Do not make the check pass merely because DIR-2 or FE-1 exists somewhere. It must inspect each active workflow independently enough to catch a contradictory second location.

Prefer parsing the relevant terminal/exception sections over broad self-source token checks.

### 4. Add targeted probes

Add at least three new mutation probes that plant the forbidden exception separately into:

- Meeting Preparation;
- Boundary Setting;
- Refusal.

Each must be detected independently.

Also add one mutation in a fourth workflow location to prove the new package-wide check is not hard-coded only to those three filenames.

No probe may return REDUNDANT on the first final run.

### 5. Fix stale assurance reporting

The prior closure review observed drift between documented and executed probe counts. Update any active self-check / assurance count so it reflects the actual final number after this remediation.

Do not claim harness perfection. Preserve known limitations honestly.

## Required verification

Run and report:

1. `communication_package_validation.py` default
2. `communication_package_validation.py --verbose`
3. `communication_package_validation.py --json`
4. `communication_package_probes.py`
5. Phase 8 validator
6. Phase 9 validator
7. Phase 10 validator, preserving inherited 145/147 result
8. Phase 11 validator, preserving inherited 159/160 result
9. `git diff --check`
10. containment check against the branch merge-base

Then perform a manual B3 sweep across **all six workflow files** and print a table with one row per workflow and columns:

- workflow
- mandatory review separately required? YES/NO
- Decision Right separately required where applicable? YES/NO
- Decision Right allowed to cure review/critical/conflict/substantive-owner gap? MUST BE NO
- terminal rule fail-closed? YES/NO

## Stop rule

This remediation is intended to end the repeated second-location loop for B3.

Do not introduce new architecture concepts. Do not redesign the package. Do not broaden scope into unrelated non-blocking issues.

If, after the exhaustive sweep, the same B3 anti-pattern exists anywhere else in the active package, fix it now in this same commit rather than deferring it to another audit cycle.

## Deliverable

Commit the remediation to the existing branch.

Return:

A. Summary
B. Starting baseline and remediation SHA
C. Files changed
D. Exact B3 survivors fixed
E. Exhaustive six-workflow sweep result
F. Validator/probe changes
G. Test results
H. Containment
I. Remaining blockers
J. Verdict

Required verdict if successful:

`READY FOR FINAL SHORT B3 CLOSURE CHECK`

Do not create a PR.
