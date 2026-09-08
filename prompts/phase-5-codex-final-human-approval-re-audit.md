# Codex Prompt — Final Human-Approval Re-Audit for Phase 5

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-5-workflow-registry`
Audit baseline commit: `adf45adf4ca33510a15281c5e776160d5720b859`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 5 APPROVED or CANONICAL.

This is the final, narrow human-approval re-audit after the targeted cleanup. The previous re-audit had already passed M3, M4, M5, regression/phase boundaries, authority leakage, and universe/card-generation boundaries. It failed only on residual M1 wording loopholes and seven M2 participation-table mismatches. Those are the only areas that must be re-checked in depth, with regression confirmation that prior PASS areas remain intact.

Read at minimum:
- `workflows/exemplars/project-development-readiness.md`
- `workflows/exemplars/eu-grant-application-development.md`
- `workflows/exemplars/software-change-delivery.md`
- `workflows/exemplars/decision-grade-document-preparation.md`
- `reviews/phase-5-final-targeted-cleanup.md`
- `architecture/workflow-registry-design.md`
- `workflows/_standards/common-workflow-constraints.md`
- `workflows/_templates/workflow-card-template.md`
- `workflows/master-workflow-universe.md`

## 1. M1 — terminal review / open-item materiality closure

Verify all three terminal-stage cases:

### Project Development Readiness
- S7 Entry Criteria
- Completion Criteria

### EU Grant Application Development
- S6 Entry Criteria
- Completion Criteria

### Software Change Delivery
- S6 Entry Criteria
- Completion Criteria

PASS only if all are true:
1. Missing required `review.<id>` is not sufficient merely because its absence is recorded.
2. Required review must be satisfied under the future Phase 6 review semantics before normal progression/completion.
3. Missing required review gives `BLOCKED`, `REWORK_REQUIRED`, or `ESCALATED` unless a **named external human `decision.<id>`** explicitly permits progression without the review.
4. If a Decision Right permits progression, the review remains explicitly unsatisfied/open.
5. The Workflow does not state or imply that it waives, satisfies, downgrades, or cancels the review requirement.
6. No phrase remains reasonably readable as "record it and continue".

## 2. M1 — deadline / schedule pressure closure

Audit every deadline, time-pressure, release-date-pressure, urgent, expedited, or equivalent exception path in all four exemplar cards.

PASS only if every such path explicitly states:
1. `COMPLETE_WITH_OPEN_ITEMS` is allowed only when **every carried item affecting that progression is `NON_MATERIAL_TO_NEXT_STEP`**.
2. Any `MATERIAL_TO_NEXT_STEP_OR_GATE` item causes `BLOCKED`, `REWORK_REQUIRED`, or `ESCALATED`.
3. Progression with a material unresolved item is possible only through a **named external human `decision.<id>`** explicitly permitting it.
4. The unresolved item remains open and is carried forward; Workflow does not resolve or downgrade it.
5. Missing required review remains unsatisfied if such progression is permitted.
6. Deadline pressure itself is explicitly not a Decision Right and cannot remove a review or human gate.

Also verify the previously discovered residual Exemplar D material-`CONFLICT_DETECTED` path is closed: visibility alone must not release progression.

## 3. M2 — top-level / per-stage participation reconciliation

Mechanically compare the top-level `Participating Roles` table stage lists against every per-Stage `Participating Roles` list for all four exemplars.

Required result:
- Project Development Readiness discrepancy count = 0
- EU Grant Application Development discrepancy count = 0
- Software Change Delivery discrepancy count = 0
- Decision-Grade Document Preparation discrepancy count = 0

Specifically verify the seven prior mismatches:

### Project Development Readiness
Top-level stage lists include S6 consistently for:
- `role.sector_technical_expert`
- `role.asset_om_technical_operations_specialist`
- `role.procurement_state_aid_specialist`
- `role.insurance_risk_transfer_specialist`

Their original conditional activation semantics must remain conditional and tied to the same objective trigger.

### EU Grant Application Development
- `role.consortium_partner_coordination_specialist` includes S6 at top level.
- `role.grant_financial_compliance_budget_specialist` no longer claims S4 unless it actually participates there.

### Software Change Delivery
- `role.data_database_architect` no longer claims S3 unless it actually participates there.
- S5 implementing-engineer participation is explicitly named by role IDs rather than left in an aggregate phrase that hides mismatches.

## 4. M2 semantics regression

Verify:
- participation types remain exactly `LEAD_ROLE`, `CONTRIBUTING_ROLE`, `CONSULTED_ROLE`;
- Activation remains a separate property;
- `CONSULTED_ROLE` artifact/conclusion mismatch count = 0;
- artifact/conclusion-producing conditional specialists remain `CONTRIBUTING_ROLE`;
- no conditional activation widens Role scope or Phase 4 compatibility.

## 5. Prior PASS regression

Confirm no regression in:
- M3 Security Engineer S3 participation and ownership;
- Security Engineer exclusions from `skill.quality_attribute_analysis` and `skill_pack.supabase`;
- M4 `WORKFLOW_REFERENCE` semantics;
- M5 Role Slot Binding Rule semantics;
- authority leakage = 0;
- Phase 3 Role Card changes = 0;
- approved Phase 4 architecture/mapping changes = 0;
- all Phase 5 artifacts remain `PROPOSED`;
- no self-promotion to `REVIEWED`, `APPROVED`, or `CANONICAL`;
- AI output remains `AI_SUGGESTION`/`DRAFT` until governed adoption;
- no runtime/database/API/orchestrator/model implementation;
- no PR created as part of this path.

## 6. Universe / carding regression

Verify counts remain:
- 49 unique candidate Workflow IDs
- 7 rejected candidates
- 20 audit-flagged candidates blocked from carding
- 8 overlap groups visible/open
- 4 exemplar cards

No mass card generation.

## Approval threshold

- PASS if the remaining M1/M2 issues are fully closed and no regression exists.
- PASS WITH NON-BLOCKING NOTES only if the only remaining items are explicitly deferred Phase 6/7/runtime matters.
- PASS WITH CHANGES if any further bounded Phase 5 correction is still needed.
- FAIL if any "record it and continue" loophole, participation mismatch, authority leakage, unconstrained progression, or phase-boundary regression remains.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. M1 TERMINAL REVIEW SEMANTICS
PASS / FAIL + exact remaining loophole count.

### C. M1 DEADLINE / MATERIALITY PATHS
PASS / FAIL + exact remaining loophole count.

### D. M2 PARTICIPATION CONSISTENCY
PASS / FAIL + discrepancy count for each of the four exemplars.

### E. M2 PARTICIPATION / ACTIVATION SEMANTICS
PASS / FAIL + consulted-role artifact/conclusion mismatch count.

### F. PRIOR-PASS REGRESSION
M3 / M4 / M5 / authority / Phase 3 / Phase 4 / runtime / PR status.

### G. UNIVERSE / CARDING BOUNDARY
Report counts: 49 / 7 / 20 / 8 / 4.

### H. REMAINING BLOCKERS
If none: NONE.

### I. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 5
- READY AFTER LISTED CHANGES
- NOT READY

### J. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.