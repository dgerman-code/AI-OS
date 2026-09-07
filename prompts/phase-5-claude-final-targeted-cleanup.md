# Claude Code Prompt — Final Targeted Phase 5 Cleanup

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-5-workflow-registry`
Current branch HEAD includes the final re-audit prompt commit.
Remediated baseline under re-audit: `e32d87f40ec6c5ae83d2abcc566f739e6118dbaf`.

The final independent re-audit returned **FAIL** for two narrowly bounded areas only:

- M1 materiality wording loopholes remain in terminal-stage progression / completion prose and deadline-pressure paths.
- M2 participation/activation semantics are correct, but seven top-level/per-stage participation tables are inconsistent.

M3, M4, M5, regression / phase boundaries, universe boundaries and authority leakage all PASS.

This is a **targeted cleanup only**. Do not redesign Phase 5. Do not modify Phase 3 Role Cards. Do not modify approved Phase 4 architecture/mappings. Do not change `WORKFLOW_REFERENCE`, Role Slot Binding Rule, Security Engineer M3 correction, universe counts, overlap groups or carding boundaries except where strictly needed to keep prose internally consistent with the fixes below.

Do not implement runtime, DB, API, orchestrator, model routing, agents or UI.
Do not create a PR.
Do not mark Phase 5 APPROVED or CANONICAL.
Do not generate additional Workflow Cards.

## A. Fix M1 terminal-stage review/materiality loopholes

Correct the following exemplar terminal-stage entry/completion wording so that **missing required reviews can never be treated as sufficient merely because their absence is recorded**:

1. `workflows/exemplars/project-development-readiness.md`
   - Stage S7 entry criteria
   - Completion Criteria

2. `workflows/exemplars/eu-grant-application-development.md`
   - Stage S6 entry criteria
   - Completion Criteria

3. `workflows/exemplars/software-change-delivery.md`
   - Stage S6 entry criteria
   - Completion Criteria

Required semantics everywhere:

- If a required `review.<id>` is a prerequisite for the next stage or terminal gate, the review must be satisfied under the future Phase 6 review semantics before progression.
- Merely recording that the review is missing is **not** sufficient.
- If the required review is missing, the outcome is `BLOCKED`, `REWORK_REQUIRED`, or `ESCALATED` unless a **named external human `decision.<id>`** explicitly permits progression without that review.
- If such a Decision Right permits progression, the missing review remains explicitly unresolved/open; the Workflow does not say the review was satisfied, waived by itself, or no longer required.
- Do not invent who holds the Decision Right or how waiver authority is granted; Phase 7 still owns that.

Replace any phrase equivalent to:
- "required reviews satisfied or their absence recorded"
- "required review complete or absence visible"
- "review missing but listed"
where such wording is used as entry/completion sufficiency.

## B. Fix all deadline-pressure paths

Audit all four exemplar cards for `deadline`, `time pressure`, `urgent`, `expedited`, `schedule pressure`, or equivalent exception wording.

For every path that permits `COMPLETE_WITH_OPEN_ITEMS`, make explicit:

1. `COMPLETE_WITH_OPEN_ITEMS` is permitted only when **all carried items affecting that progression are `NON_MATERIAL_TO_NEXT_STEP`**.
2. Any `MATERIAL_TO_NEXT_STEP_OR_GATE` item causes `BLOCKED`, `REWORK_REQUIRED`, or `ESCALATED`.
3. Progression with a material unresolved item is possible only via a **named external human Decision Right** explicitly permitting it.
4. The unresolved item remains open and is carried forward; the Workflow neither resolves nor downgrades it.
5. Deadline pressure never removes a review requirement or a human gate.

Apply this explicitly in all four cards even where the generic common constraint already says it. The final re-audit requires the exemplar path itself not to admit a contrary reading.

## C. Reconcile the seven M2 top-level/per-stage discrepancies

The semantics of `CONTRIBUTING_ROLE`, `CONSULTED_ROLE`, and `Activation` already pass. Do not redesign them.

Reconcile only these inconsistencies:

### Project Development Readiness
The top-level Participating Roles stage lists must include S6 for every contributing Role explicitly re-engaged in S6:
- `role.sector_technical_expert`
- `role.asset_om_technical_operations_specialist`
- `role.procurement_state_aid_specialist`
- `role.insurance_risk_transfer_specialist`

If S6 re-engagement is conditional on the same original trigger, preserve that same `Activation: CONDITIONAL(...)` semantics in S6. Do not convert them to ALWAYS.

### EU Grant Application Development
- `role.consortium_partner_coordination_specialist`: top-level stage list must include S6, because it participates in S6.
- `role.grant_financial_compliance_budget_specialist`: resolve the current mismatch where the top-level table lists S4 but S4 does not include it.
  - Prefer removing S4 from the top-level stage list unless S4 actually needs the Role to contribute an owned artifact/conclusion.
  - Do not add the Role to S4 merely to make the table match unless the Stage content truly requires it.

### Software Change Delivery
- `role.data_database_architect`: resolve the mismatch where top-level lists S3 but S3 does not include the Role.
  - Prefer removing S3 from the top-level stage list if S3 implementation belongs to `role.database_data_engineer` and the architect only owns design in S2.
  - Do not add an artificial S3 participation merely for symmetry.

## D. Consistency validation

After edits, run a focused validator covering at minimum:

1. No phrase in Project S7, EU Grant S6, or Software S6 allows required-review absence to satisfy entry/completion merely because it is recorded.
2. Every deadline-pressure `COMPLETE_WITH_OPEN_ITEMS` path is explicitly limited to `NON_MATERIAL_TO_NEXT_STEP` items.
3. Every material open item on a deadline-pressure path blocks/reworks/escalates unless a named external human Decision Right explicitly permits progression.
4. Missing required reviews remain unresolved if a Decision Right permits progression; no wording says the Workflow satisfied or waived review.
5. All four exemplar cards remain `PROPOSED`.
6. Phase 3 Role Cards unchanged.
7. Approved Phase 4 architecture/mappings unchanged.
8. M3 Security Engineer S3 remains intact.
9. Security Engineer exclusions from `skill.quality_attribute_analysis` and `skill_pack.supabase` remain intact.
10. `WORKFLOW_REFERENCE` unchanged in semantics.
11. Role Slot Binding Rule unchanged in semantics.
12. Consulted-role artifact/conclusion mismatch count remains 0.
13. Project top-level vs per-stage participation discrepancy count = 0.
14. EU Grant top-level vs per-stage participation discrepancy count = 0.
15. Software top-level vs per-stage participation discrepancy count = 0.
16. Decision-Grade Document top-level vs per-stage participation discrepancy count = 0.
17. Conditional activation triggers remain objective and unchanged except for stage-list reconciliation.
18. No authority leakage introduced.
19. No new Workflow cards created.
20. Candidate universe remains 49 unique IDs.
21. Rejected candidates remain 7.
22. Audit-flagged blocked-from-carding candidates remain 20.
23. Overlap groups remain 8.
24. Exemplar cards remain 4.
25. No runtime/database/API/orchestrator/model implementation introduced.
26. No PR created.
27. Working tree clean after commit.

Create a short review record:
`reviews/phase-5-final-targeted-cleanup.md`

Status:
`PROPOSED — READY FOR FINAL HUMAN-APPROVAL RE-AUDIT`

It must list:
- the exact terminal review/materiality phrases corrected;
- the deadline-path corrections in all four exemplars;
- the seven participation table mismatches and their exact resolution;
- validation checks 1–27 with PASS/FAIL.

## Commit / push

If and only if all 27 checks PASS, commit exactly:

`docs: close final Phase 5 audit gaps`

Push to:
`origin architecture/phase-5-workflow-registry`

Do not create a PR.

## Required output

Return exactly:

### A. TERMINAL REVIEW FIXES
Exact fixes in Project S7, EU Grant S6, Software S6.

### B. DEADLINE-PATH FIXES
All four exemplars and resulting materiality semantics.

### C. PARTICIPATION RECONCILIATION
All seven discrepancies and exact resolution.

### D. REGRESSION CHECK
M3/M4/M5 and authority/phase-boundary regression status.

### E. VALIDATION
Checks 1–27 PASS / FAIL.

### F. FILES CHANGED
Exact files and concise purpose.

### G. COMMIT / PUSH
Commit SHA, message, push result, remote HEAD, PR status.

### H. NEXT STEP
Choose exactly one:
- READY FOR FINAL HUMAN-APPROVAL RE-AUDIT
- NOT READY

Do not claim Phase 5 approval.