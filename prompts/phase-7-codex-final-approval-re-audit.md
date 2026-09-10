# Codex Prompt — Final Phase 7 Approval Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-7-decision-rights`
Audit baseline commit: `cedee2cfd1a959489585eb61acd975b4f7c65c84`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 7 APPROVED or CANONICAL.

This is a narrow final approval re-audit after the sole remaining Phase 7 blocker was fixed.

The previous independent re-audit returned `PASS WITH CHANGES` with exactly one remaining blocker:
- `decision.stage_gate_progression` declared `SEPARATION_REQUIRED` from `decision.risk_acceptance`, but `decision.risk_acceptance` lacked the reciprocal declaration.

The remediation commit `cedee2cfd1a959489585eb61acd975b4f7c65c84` claims to close that one symmetry gap only.

## 1. Verify the reciprocal relationship

Read:
- `decisions/exemplars/risk-acceptance.md`
- `decisions/exemplars/stage-gate-progression.md`

Verify both sides now declare the same carded-to-carded relationship:

`decision.risk_acceptance` <-> `decision.stage_gate_progression`

PASS only if:
- both directions exist;
- both use `SEPARATION_REQUIRED`;
- activation condition is semantically equivalent;
- bounded subject/context is semantically equivalent;
- governance reason is consistent;
- no scope widening occurred;
- no runtime semantics were introduced.

## 2. Full carded-to-carded symmetry check

Read all eight `decisions/exemplars/*.md`.

For every `DECISION_RIGHT_SEPARATION` row whose target is another carded exemplar:
- confirm the reciprocal row exists in the target card;
- confirm the separation mode matches;
- confirm activation/context are semantically compatible.

One-ended relationships pointing to uncarded but valid candidate Rights are allowed and are not defects.

Report exact carded-to-carded asymmetry count.

Required result: `0`.

## 3. Factual remediation-record consistency

Read:
- `reviews/phase-7-foundation-audit-remediation.md`
- `reviews/phase-7-foundation-self-check.md`

Verify they now accurately state:
- every carded-to-carded separation relationship is declared from both ends;
- the previous `stage_gate_progression -> risk_acceptance` one-ended relation was the final asymmetry and is now reciprocated;
- no broader claim is made about symmetry to uncarded candidate Rights.

## 4. Regression check — prior PASS areas

Do not broadly redesign Phase 7. Verify only that the final symmetry fix did not regress prior PASS areas.

Confirm:
- production-release pre-release/post-release semantics unchanged and unambiguous;
- universe counts unchanged: 9 families, 35 candidates, 34 boundary-refinement, 1 duplicate/overlap, 95/95 upstream references;
- invalid/undefined concrete Decision refs across exemplars remain 0;
- Human Approval Matrix discrepancies remain 0;
- `decision.cancellation_or_termination` remains `NOT CARDABLE UNTIL BOUNDED`;
- Role competence != Decision Right authority;
- Workflow lead != approval authority;
- reviewer != approval authority;
- Review `NOT_SATISFIED` cannot be changed to `SATISFIED` by a Decision Right;
- risk acceptance does not itself permit progression/release;
- emergency authority remains bounded and does not retroactively satisfy skipped review;
- generic approval does not imply `CANONICAL`;
- Decision Record remains 19 elements including separation evidence;
- Phase 3–6 approved semantics unchanged;
- all Phase 7 artifacts remain `PROPOSED`;
- no DB/API/UI/runtime/orchestrator/model/agent/IAM implementation;
- no named real human/organisation assignment;
- no PR.

## 5. Approval threshold

Return `PASS` if:
- the reciprocal risk-acceptance/stage-gate relation is correct;
- all carded-to-carded separation relations are symmetric;
- no prior PASS area regressed;
- no new material blocker appears.

Return `PASS WITH NON-BLOCKING NOTES` only if the remaining notes are genuinely Phase 8/runtime/organisation/card-expansion concerns.

Return `PASS WITH CHANGES` if another bounded Phase 7 correction is still needed before human approval.

Return `FAIL` if any authority/separation/review/truth/gate bypass remains.

Do not recommend mass card generation merely because the phase passes.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. RECIPROCAL RELATIONSHIP
PASS / FAIL + exact finding.

### C. CARDED-TO-CARDED SYMMETRY
PASS / FAIL + exact asymmetry count.

### D. REMEDIATION RECORD ACCURACY
PASS / FAIL + any discrepancy count.

### E. REGRESSION
PASS / FAIL + concise status of production-release, universe, references, matrix, cancellation, authority/review/risk/emergency/canonical/Decision Record boundaries.

### F. UPSTREAM / NON-RUNTIME STATUS
Phase 3–6 changes, Phase 7 status, runtime/PR status.

### G. REMAINING BLOCKERS
If none: NONE.

### H. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 7
- READY AFTER LISTED CHANGES
- NOT READY

### I. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.