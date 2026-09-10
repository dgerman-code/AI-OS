# Claude Code Prompt — Final Phase 7 Symmetry Fix

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-7-decision-rights`
Remediation architecture baseline: `e08411351e214d8d15939c5db3448f7802b7c69d`
Final re-audit verdict: `PASS WITH CHANGES`

This is a **single-issue bounded fix**.

Do not redesign Phase 7.
Do not modify approved Phase 3–6 artifacts.
Do not change Decision Right IDs.
Do not change cardinality, holder eligibility, delegation, gate, review, risk, emergency, canonical, cancellation/termination or production-release semantics unless required solely to preserve exact consistency with the one fix below.
Do not implement runtime/DB/API/UI/orchestrator/model/agent/IAM.
Do not create a PR.
Do not mark Phase 7 APPROVED or CANONICAL.
All Phase 7 artifacts remain `PROPOSED`.

## Sole blocking finding

The final independent re-audit found exactly one remaining asymmetry:

- `decision.stage_gate_progression` declares `SEPARATION_REQUIRED` from `decision.risk_acceptance`;
- the carded `decision.risk_acceptance` does not declare the reciprocal relationship.

All other relationships between carded exemplar Rights are symmetric.

## Required fix

Update:

`decisions/exemplars/risk-acceptance.md`

Add the reciprocal `DECISION_RIGHT_SEPARATION` relationship to:

`decision.stage_gate_progression`

The relationship must match the existing stage-gate card declaration semantically:
- mode: `SEPARATION_REQUIRED`;
- same bounded subject/context as the stage-gate side;
- same objective activation condition;
- same governance reason;
- no widening of scope;
- no runtime implication.

The result must make the pair exactly symmetric.

## Consistency updates

If and only if needed for factual accuracy, update:
- `reviews/phase-7-foundation-audit-remediation.md`
- `reviews/phase-7-foundation-self-check.md`

Do not otherwise alter architecture prose.

## Validation

Run checks sufficient to prove:

1. `decision.stage_gate_progression` -> `decision.risk_acceptance` exists.
2. `decision.risk_acceptance` -> `decision.stage_gate_progression` exists.
3. Both use `SEPARATION_REQUIRED`.
4. Activation conditions are semantically identical.
5. Bounded subject/context is semantically identical.
6. Governance reason is semantically consistent.
7. All relationships between carded exemplar Decision Rights are symmetric.
8. One-ended relationships to uncarded candidate Rights remain allowed and unchanged.
9. Invalid concrete Decision refs = 0.
10. Human Approval Matrix discrepancies = 0.
11. Production-release condition semantics unchanged.
12. Universe counts unchanged: 9 families, 35 candidates, 34 boundary-refinement, 1 duplicate/overlap, 95/95 upstream refs.
13. `decision.cancellation_or_termination` remains `NOT CARDABLE UNTIL BOUNDED`.
14. Phase 3 changes = 0.
15. Phase 4 changes = 0.
16. Phase 5 changes = 0.
17. Phase 6 changes = 0.
18. All Phase 7 artifacts remain PROPOSED.
19. No runtime implementation.
20. No PR.

## Commit / push

If and only if the fix and validation pass, commit exactly:

`docs: close final Phase 7 separation symmetry gap`

Push to:

`origin architecture/phase-7-decision-rights`

Do not create a PR.

## Required final output

Return exactly:

### A. FIX
Exact reciprocal relationship added.

### B. SYMMETRY VALIDATION
PASS/FAIL + total carded-to-carded asymmetries remaining.

### C. REGRESSION
Phase 3–6 changes, universe/reference/matrix/production-release/cancellation status.

### D. FILES CHANGED
Exact files.

### E. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, PR status.

### F. NEXT STEP
Choose exactly one:
- READY FOR FINAL PHASE 7 APPROVAL RE-AUDIT
- NOT READY

Do not claim Phase 7 approval.