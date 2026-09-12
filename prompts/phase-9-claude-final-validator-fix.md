# Claude Code Prompt — Final Phase 9 Validator Fix

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Architecture/content baseline under re-audit: `0ec2c26e8a262d06bf841fb718944f4573dcfbab`

This is an extremely narrow final correction pass.

The latest independent Codex re-audit found the Phase 9 architecture itself materially sound and all nine exemplars conformant. Only two cleanup issues remain:

1. the current self-check says “the prompt’s twelve conditions” but the following table contains 13 conditions;
2. the Phase 9 validation harness still gives false confidence because some count/cardinality checks are syntax/location-sensitive and do not fail for several deliberate regressions.

Do not redesign Phase 9.
Do not modify approved Phase 3–8 semantics.
Do not add runtime, SDKs, APIs, DB, UI, RAG, agents, orchestration, provider/model cards, or real vendor references.
Keep all Phase 9 artifacts `PROPOSED`.
Do not create a PR.

## 1. Fix the self-check cardinality contradiction

In `reviews/phase-9-foundation-self-check.md`:
- find the statement equivalent to “the prompt’s twelve conditions”;
- make it match the actual table cardinality of 13 conditions;
- do not delete a condition merely to preserve the number 12;
- ensure there is no other stale current cardinality prose in the self-check.

Historical statements may remain historical if clearly labelled as such.

## 2. Make count validation structure-aware

Strengthen `validation/phase_9_validation.py` so the following deliberate regressions each produce a non-zero exit and at least one failed check.

### A. Master Routing Decision count
If `models/master-model-routing-universe.md` is changed from current authoritative Routing Decision elements count 35 to 31, validation MUST fail.

The validator must derive the authoritative Routing Decision element count from `models/_templates/routing-decision-template.md`, then reconcile every active current count claim in the master universe and self-check against the derived value.

Do not hard-code `35` as the only source of truth.

### B. Master capability-family count
If `models/master-model-routing-universe.md` is changed from 23 capability families to 24, validation MUST fail.

Derive the authoritative family count from the actual capability taxonomy table in `models/model-capability-taxonomy.md`, then reconcile current active claims.

Do not rely only on detecting English word forms such as “twenty-four”. Detect numeric forms and structured table values.

### C. Evidence applicability dimension count
If `models/evaluation-evidence-model.md` prose changes current **eight** applicability dimensions to **seven** while the table still has eight rows, validation MUST fail.

The check must be formatting-robust enough to catch:
- `eight` -> `seven`;
- `**eight**` -> `**seven**`;
- numeric `8` -> `7` where this is clearly the current applicability cardinality claim.

Derive the authoritative count from the applicability table itself.

Do not create broad false positives on unrelated historical prose.

### D. Self-check group counts
If a current per-group count in `reviews/phase-9-foundation-self-check.md` is altered, e.g. `identity-stack` from its actual current count to a stale value, validation MUST fail.

Derive actual group counts from the validator's own emitted check groups / result registry, not from a duplicated constant.

Reconcile every stated **current** group count in the self-check against those derived counts.

Historical prior totals/groups may remain if explicitly historical and not presented as current.

## 3. General rule for active inventory/cardinality claims

Where practical, create a reusable structured reconciliation layer so active current count claims are validated against authoritative parsed sources rather than ad hoc string presence.

At minimum cover current claims for:
- capability families;
- eligibility constraints;
- preferences;
- routing act requirements;
- primary lifecycle states;
- evidence classes;
- negative-evidence applicability dimensions;
- common governance constraints;
- templates;
- exemplars;
- Routing Decision elements;
- validator total;
- validator group counts stated in the current self-check.

Do not accidentally treat historical progression text such as earlier `141`, `204`, `219`, `239` totals as current-state contradictions when they are explicitly labelled as history.

## 4. Controlled failure probes

After implementation, run the normal battery first.

Then use reversible temporary edits or in-memory mutation to prove all of these fail:

1. self-check condition claim 13 -> 12;
2. master Routing Decision count 35 -> 31;
3. master capability families 23 -> 24;
4. evidence applicability current prose eight -> seven, including bold-form mutation;
5. self-check current `identity-stack` group count -> stale wrong value;
6. current validator total in self-check -> prior total;
7. vacuous `or True` injection into the harness itself if your existing anti-vacuity check supports it.

Every mutation must be fully restored before commit.

After restoration, rerun:
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_9_validation.py --verbose`
- `python3 validation/phase_9_validation.py --json`
- `python3 validation/phase_8_validation.py`

Phase 8 must remain `119/119 PASS` and untouched.

## 5. Regression boundary

Verify against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`:
- Phase 3 Roles semantic/file changes = 0;
- Phase 4 Skills = 0;
- Phase 5 Workflows = 0;
- Phase 6 Handoff/Review = 0;
- Phase 7 Decisions = 0;
- Phase 8 Knowledge/Canonical semantics = 0;
- Phase 8 validator unchanged in this pass;
- no runtime implementation;
- no real Model/Provider/Deployment profiles;
- no PR.

## 6. Commit / push

If and only if all checks pass and all controlled regressions fail as required, commit exactly:

`docs: harden final Phase 9 validation coverage`

Push to:

`origin architecture/phase-9-model-registry-router`

Do not create a PR.

## Required final output

Return exactly:

### A. FIX SUMMARY
The two remaining re-audit issues and final status.

### B. SELF-CHECK CARDINALITY
Exact correction and proof there are 13 conditions.

### C. STRUCTURE-AWARE COUNT VALIDATION
Authoritative sources used and claims reconciled.

### D. CONTROLLED FAILURE PROBES
Each deliberate mutation and result/exit code.

### E. FINAL VALIDATION
Exact Phase 9 total/result in normal/verbose/json modes and Phase 8 result.

### F. REGRESSION
Phase 3–8 change counts; runtime/profile/PR status.

### G. FILES CHANGED
Exact files and purpose.

### H. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, clean-tree status.

### I. NEXT STEP
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 9
- NOT READY

Do not claim that human approval has already occurred.