# Codex Prompt — Final Independent Phase 7 Foundation Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-7-decision-rights`
Audit baseline commit: `e08411351e214d8d15939c5db3448f7802b7c69d`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 7 APPROVED or CANONICAL.

This is the final independent re-audit after remediation of the six prior blockers.

Read at minimum:
- `architecture/decision-rights-registry-design.md`
- `decisions/_standards/common-decision-right-constraints.md`
- `decisions/_templates/decision-right-card-template.md`
- `decisions/_templates/decision-record-template.md`
- `decisions/master-decision-right-universe.md`
- all eight `decisions/exemplars/*.md`
- `reviews/phase-7-foundation-self-check.md`
- `reviews/phase-7-foundation-audit-remediation.md`
- approved Phase 3–6 artifacts only as needed for regression/reference checks.

## 1. Cross-Right separation of duties

PASS only if `DECISION_RIGHT_SEPARATION` exists consistently in architecture, constraints, template, Decision Record evidence model, and relevant exemplar cards.

Verify:
- concrete related `decision.<id>` only;
- objective/testable activation conditions;
- only `SEPARATION_REQUIRED` / `SAME_HOLDER_PERMITTED` modes;
- bounded subject/context;
- reason recorded;
- same human cannot exercise both Rights where active separation is required;
- dual eligibility labels do not bypass separation;
- delegation does not bypass separation;
- within-Right cardinality does not substitute for cross-Right separation;
- absence of a second eligible holder leaves the second Right invalidly exercisable / gate unsatisfied;
- no staffing/runtime algorithm is introduced;
- Decision Record can prove separation compliance.

Stress-test specifically:
- `decision.risk_acceptance` ↔ `decision.production_release` for the same change carrying the accepted residual risk;
- `decision.exceptional_progression` ↔ downstream release/submission/publication/contract commitment where the unresolved item is material to that act;
- `decision.emergency_production_change` ↔ ordinary release/ratification control where independence would otherwise be defeated.

Report exact bypass loophole count.

## 2. Production release conditional outcome

Audit `decisions/exemplars/production-release.md`.

PASS only if:
- pre-release conditions are clearly distinct from post-release obligations;
- every material pre-release condition must be satisfied before the release gate is satisfied and before deployment goes live;
- post-release obligations may remain open only if explicitly classified and non-blocking to release readiness;
- post-release obligations are carried into the Decision Record with owner/trigger/expiry or revisit criterion;
- later failure triggers re-decision/escalation/rollback without retroactively erasing the original decision;
- no wording remains equivalent to “go live once all conditions met” while also allowing post-release conditions;
- `APPROVE_WITH_CONDITIONS` cannot smuggle a material pre-release blocker through the gate.

Report exact timing/gate ambiguity count.

## 3. Decision Universe count/classification

Verify exact accounting:
- families = 9
- candidate Rights = 35
- upstream-ID candidates = 33
- architecture-gap candidates = 2
- `LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT` = 34
- Review/quality gate in disguise = 10
- Role responsibility in disguise = 8
- Workflow progression logic in disguise = 4
- Runtime/IAM in disguise = 2
- Executive-policy items = 3
- `DUPLICATE / OVERLAP` = 1
- upstream references accounted for = 95 / 95

Verify `decision.canonical_knowledge_status_change` is classified as `DUPLICATE / OVERLAP` with `decision.canonical_knowledge_promotion`, with both identifiers retained and normalization deferred to Phase 8.

Flag any arithmetic mismatch or double-counting.

## 4. Cancellation / termination boundedness

Audit architecture and universe handling of `decision.cancellation_or_termination`.

PASS only if:
- it is explicitly `NOT CARDABLE UNTIL BOUNDED` or equivalent;
- it confers no exercisable authority;
- pre-commitment cancellation and post-commitment termination are explicitly distinguished;
- differing holder eligibility/evidence/external-obligation implications are visible;
- it is not referenced as a valid universal kill-switch;
- no replacement card or final split IDs were silently created;
- any exemplar that previously depended on it no longer treats it as an active Right.

## 5. Reference integrity

Across all eight exemplar cards, extract every concrete `decision.*` token.

PASS only if invalid/undefined Decision IDs = 0.

Specifically verify the following do NOT remain as code-form registry references:
- `decision.project_readiness_progression`
- `decision.grant_submission`
- `decision.contractual_commitment`

Verify actual stable IDs remain:
- `decision.stage_gate_progression`
- `decision.granting_authority_submission`
- `decision.contract_commitment`

Do not count plain-language prose labels as registry IDs.

## 6. Human Approval Matrix consistency

Compare all eight matrix rows directly with their exemplar cards.

At minimum compare:
- cardinality;
- delegation policy;
- external-commitment flag;
- exceptional-progression flag;
- risk-acceptance flag;
- knowledge-state effect.

PASS only if discrepancy count = 0.

Verify especially:
- `decision.exceptional_progression` includes `MULTI_HOLDER_ALL_REQUIRED` not only across domains but also at a terminal gate;
- `decision.granting_authority_submission` includes consortium/co-financing/value-threshold escalation;
- `decision.external_publication` includes third-party-disclosure escalation;
- `decision.production_release` includes governance-body cardinality where accreditation applies.

If matrix prose is abbreviated, it must still be semantically exact.

## 7. Gate / authority regression

Verify prior PASS areas remain intact:
- Role competence != Decision Right authority;
- Workflow lead != approval authority;
- reviewer != approval authority;
- artifact owner != external commitment authority;
- no eligible holder => no valid decision;
- request/meeting/email != valid gate satisfaction by itself;
- invalid authority => gate unsatisfied;
- `DEFER`, `ESCALATE`, `REJECT` do not satisfy positive gate unless explicitly declared otherwise;
- delegation cannot widen subject/effect;
- delegation cannot bypass cardinality;
- revocation affects future exercise, not historical records;
- corrections use new linked Decision Records, never silent mutation.

## 8. Review / knowledge-state regression

Verify:
- Decision Right cannot make Review `SATISFIED`;
- exceptional progression leaves unresolved review/finding open;
- risk acceptance does not erase risk/finding;
- generic approval does not imply `CANONICAL`;
- Decision Right cannot convert `UNKNOWN` or `ASSUMPTION` into FACT;
- Decision Right cannot resolve `CONFLICT_DETECTED` by authority alone;
- canonical governance remains Phase 8-bound.

## 9. Exception / risk / emergency regression

Verify:
- `decision.exceptional_progression` authorizes movement, not fictional resolution;
- `decision.risk_acceptance` does not itself permit progression/release/submission/publication/commitment;
- law/regulation cannot be waived by registry declaration;
- emergency authority is pre-designated, bounded, temporary and non-delegable where declared;
- urgency/deadline is not authority;
- skipped reviews remain skipped/open and are not retroactively satisfied;
- retrospective review does not rewrite historical emergency decisions;
- ordinary `decision.production_release` remains distinct from emergency change authority.

## 10. Decision Record evidence model

Verify the model now has 19 elements and includes proof of applicable `DECISION_RIGHT_SEPARATION` relationships and compliance.

PASS only if:
- separation evidence is attributable per decision instance;
- historic decisions remain immutable records;
- supersession/reversal uses linked new records;
- open risks/findings/reviews at decision time are preserved;
- model remains semantic architecture, not DB schema.

## 11. Open-question dispositions

Verify current dispositions are coherent:
1. organisational authority eligibility -> `RUNTIME / ORGANISATION-PHASE CONCERN`
2. one human exercising multiple Rights in one chain -> `RESOLVED IN FOUNDATION`
3. mandatory separation between some Rights -> `RESOLVED IN FOUNDATION`
4. abstention/dissent -> `SAFE TO DEFER WITH EXPLICIT RULE`
5. global vs Right-specific expiry -> `SAFE TO DEFER WITH EXPLICIT RULE`
6. shared risk-class ceiling -> `RUNTIME / ORGANISATION-PHASE CONCERN`
7. canonical promotion -> `PHASE 8 CONCERN`
8. first-class composition vs bounded prerequisites -> `SAFE TO DEFER WITH EXPLICIT RULE`
9. emergency retrospective ratification model -> `SAFE TO DEFER WITH EXPLICIT RULE`
10. reversal model -> `SAFE TO DEFER WITH EXPLICIT RULE`

Flag if questions 2 or 3 are marked resolved but cross-Right separation is materially incomplete in design, constraints, template, cards or Decision Record evidence.

## 12. Exemplar audit

Audit each independently:
1. `decision.exceptional_progression`
2. `decision.stage_gate_progression`
3. `decision.granting_authority_submission`
4. `decision.external_publication`
5. `decision.contract_commitment`
6. `decision.risk_acceptance`
7. `decision.production_release`
8. `decision.emergency_production_change`

For each report PASS/FAIL and one concise reason, checking:
- bounded subject/effect;
- holder eligibility;
- cardinality;
- delegation;
- prerequisites/evidence;
- outcome semantics;
- cross-Right separation;
- review/knowledge-state boundaries;
- out-of-scope authority;
- expiry/re-decision.

## 13. Upstream / non-runtime regression

Verify:
- Phase 3 Role changes = 0;
- approved Phase 4 architecture/mapping changes = 0;
- approved Phase 5 Workflow semantic changes = 0;
- approved Phase 6 Handoff/Review semantic changes = 0;
- all Phase 7 artifacts remain `PROPOSED`;
- no DB/API/UI/runtime/orchestrator/model/agent/IAM implementation;
- no named real human/organisation assignment;
- no PR created.

## 14. Deferred matters are truly non-blocking

Check whether the following are safe to leave for later:
- organisational mapping of holder eligibility classes;
- shared risk-ceiling policy;
- Phase 8 canonical governance;
- abstention/dissent detail;
- global vs per-Right expiry standard;
- retrospective ratification model;
- reversal pattern;
- carding of remaining uncarded Decision Rights;
- currently one-ended separation relations pointing to uncarded but valid candidate Rights.

If any deferred issue can still create an authority bypass in the eight current exemplars, treat it as blocking.

## Approval threshold

- PASS if all six prior blockers are fully closed and no material regression exists.
- PASS WITH NON-BLOCKING NOTES if only the explicitly deferred Phase 8/runtime/organisation/card-expansion matters remain.
- PASS WITH CHANGES if one or more bounded Phase 7 corrections are still required before human approval.
- FAIL if separation-of-duties remains bypassable, production-release gating remains ambiguous, matrix/card mismatch remains, invalid IDs remain, cancellation placeholder is still exercisable/unbounded as an active Right, or any authority/review/truth boundary regresses.

Do not recommend mass card generation merely because the foundation passes.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. CROSS-RIGHT SEPARATION
PASS / FAIL + bypass loophole count + any asymmetry findings.

### C. PRODUCTION RELEASE CONDITIONS
PASS / FAIL + timing/gate ambiguity count.

### D. UNIVERSE CLASSIFICATION
Exact counts and PASS/FAIL.

### E. CANCELLATION / TERMINATION
PASS / FAIL + boundedness/carding finding.

### F. REFERENCE INTEGRITY
Valid/invalid Decision-reference counts + list of any invalid IDs.

### G. HUMAN APPROVAL MATRIX
PASS / FAIL + discrepancy count.

### H. GATE / AUTHORITY REGRESSION
PASS / FAIL + any authority leakage.

### I. REVIEW / KNOWLEDGE / RISK / EMERGENCY REGRESSION
PASS / FAIL + findings.

### J. DECISION RECORD
PASS / FAIL + 19-element/separation-evidence finding.

### K. EIGHT EXEMPLAR DECISION RIGHTS
Each PASS / FAIL with concise reason.

### L. OPEN QUESTIONS
All ten dispositions + any remaining ambiguity.

### M. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–6 changes, Phase 7 status, runtime/PR status.

### N. REMAINING BLOCKERS
If none: NONE.

### O. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 7
- READY AFTER LISTED CHANGES
- NOT READY

### P. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.