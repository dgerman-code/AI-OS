# Codex Prompt — Final Independent Phase 5 Foundation Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-5-workflow-registry`
Remediated baseline commit: `e32d87f40ec6c5ae83d2abcc566f739e6118dbaf`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 5 APPROVED or CANONICAL.

This is a narrow final re-audit of the five findings from the previous independent Phase 5 foundation audit.

Read at minimum:
- `architecture/workflow-registry-design.md`
- `workflows/_standards/common-workflow-constraints.md`
- `workflows/_templates/workflow-card-template.md`
- all four `workflows/exemplars/*.md`
- `workflows/master-workflow-universe.md`
- `reviews/phase-5-foundation-audit-remediation.md`
- `reviews/phase-5-foundation-self-check.md`
- approved Phase 3 / Phase 4 artifacts only as needed for regression checks

## 1. M1 — Open-item materiality
Verify that:
- every open item used with `COMPLETE_WITH_OPEN_ITEMS` must be classified;
- the two-value progression materiality model is present and consistent;
- `MATERIAL_TO_NEXT_STEP_OR_GATE` cannot support `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` for the affected progression;
- default outcomes are `BLOCKED`, `REWORK_REQUIRED`, or `ESCALATED`;
- the only path past a material unresolved item is a named external human Decision Right that explicitly permits progression;
- the item remains unresolved/open after such a gate;
- missing required review visibility is never treated as review satisfaction;
- `UNKNOWN`, `CONFLICT_DETECTED`, and material `ASSUMPTION` are never cleared by stage movement;
- Exemplar D S4 no longer permits a gate-critical `UNKNOWN` to progress merely because it is named.

Return PASS only if there is no wording loophole that could be read as "record it and continue".

## 2. M2 — Participation vs conditional activation
Verify that:
- Role participation types remain exactly `LEAD_ROLE`, `CONTRIBUTING_ROLE`, `CONSULTED_ROLE`;
- conditional activation is a separate property, e.g. `Activation: ALWAYS | CONDITIONAL(...)`;
- artifact/conclusion-producing Roles are `CONTRIBUTING_ROLE`, even when conditionally activated;
- `CONSULTED_ROLE` is advisory/input-only and produces/advances no owned artifact or conclusion in that Stage;
- all four exemplar top-level participation tables and per-Stage role lists are consistent with each other;
- objective conditions are stated for conditional participation;
- no conditional activation widens Role scope or Phase 4 capability compatibility.

Count any remaining consulted-role artifact/conclusion mismatch.

## 3. M3 — Software S3 Security Engineer
Verify in `workflow.software_change_delivery`:
- if `artifact.security_control_implementation` remains in S3, `role.security_engineer` participates in S3 as `CONTRIBUTING_ROLE` under an objective conditional activation;
- S3 activity text attributes security-control implementation to Security Engineer;
- artifact ownership remains Security Engineer's;
- Security Engineer remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase`;
- no other security/architecture authority boundary regressed.

## 4. M4 — Declarative Workflow composition
Verify `WORKFLOW_REFERENCE`:
- exists as a declarative composition primitive;
- points to stable `workflow.<id>` and does not execute the child;
- requires bounded purpose, expected inputs, expected outputs, and related parent Stage(s);
- cannot transfer Role ownership, Skill compatibility, review identity, Decision Rights, gates, or knowledge-state authority;
- child gates/reviews cannot be silently dropped;
- direct and transitive cycles are prohibited;
- conditional references require objective conditions;
- no runtime scheduling/call-stack/state-machine/database semantics were introduced.

Also verify the repository no longer falsely claims that `workflow.decision_grade_document_preparation` is already composed into parent exemplars if no valid concrete reference exists. It may remain a candidate reusable child pattern.

## 5. M5 — Parameterized Role slots
Verify the Role Slot Binding Rule:
- approved concrete `role.<id>` is the only permitted binding source;
- ownership/interface constraints are explicit;
- permitted participation types/cardinality are explicit;
- slots cannot grant ownership;
- every capability must independently pass Phase 4 compatibility;
- no wildcard or dynamic authority loophole exists;
- no System Control Profile, Review Profile, Decision Right, model or runtime identity can bind into a Role slot;
- lack of an eligible approved Role makes the instance blocked/invalid rather than widening the slot.

Audit Exemplar D's `SLOT.document_owner` and `SLOT.specialist_contributor` specifically.

## 6. Regression checks
Verify:
- Phase 3 Role Cards changed: 0;
- approved Phase 4 architecture/mappings changed: 0;
- all Phase 5 artifacts remain `PROPOSED`;
- identity separation remains intact;
- authority leakage remains 0;
- Workflow cannot self-promote `REVIEWED`, `APPROVED`, or `CANONICAL`;
- AI output remains `AI_SUGGESTION` / `DRAFT` until governed adoption/transition;
- forward `review.*` / `decision.*` references remain Phase 6/7 dependencies, not locally defined semantics;
- no runtime/database/API/orchestrator/model implementation exists;
- no PR exists as part of this remediation path.

## 7. Universe/card-generation boundary
Verify:
- 49 candidate Workflow IDs remain unique;
- 7 rejected candidates remain exclusions;
- 20 audit-flagged candidates remain explicitly blocked from carding until boundary tests pass;
- 8 overlap groups remain visible/open;
- only 4 exemplar cards exist unless an explained bounded correction is present;
- no mass card generation occurred.

Do not fail the foundation merely because 45 candidates are uncarded: card coverage is not the purpose of this approval gate.

## Approval threshold
- PASS if all five findings are fully remediated and no regression is found.
- PASS WITH NON-BLOCKING NOTES if only clearly deferred Phase 6/7/runtime matters remain.
- PASS WITH CHANGES if any bounded foundation correction is still required.
- FAIL if authority leakage, identity confusion, unsafe open-item semantics, unconstrained role slots, or runtime leakage remains.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. M1 MATERIALITY
PASS / FAIL + exact remaining loopholes if any.

### C. M2 PARTICIPATION / ACTIVATION
PASS / FAIL + consulted-role mismatch count.

### D. M3 SOFTWARE SECURITY S3
PASS / FAIL + findings.

### E. M4 WORKFLOW COMPOSITION
PASS / FAIL + findings.

### F. M5 ROLE SLOT BINDING
PASS / FAIL + findings.

### G. REGRESSION / PHASE BOUNDARY
PASS / FAIL + counts/findings.

### H. UNIVERSE / CARDING BOUNDARY
PASS / FAIL + 49 / 7 / 20 / 8 / 4 counts.

### I. REMAINING BLOCKERS
If none: NONE.

### J. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 5 FOUNDATION
- READY AFTER LISTED CHANGES
- NOT READY

### K. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.