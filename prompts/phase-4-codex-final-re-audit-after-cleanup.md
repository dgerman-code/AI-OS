# Codex Prompt — Final Phase 4 Re-Audit After Cleanup

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected HEAD: `d0dbcfef0262bffbfd5540baddead10fd10a242a`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.

This is a narrow final re-audit of the three blocker classes from the failed final independent Phase 4 audit.

Read:
- `reviews/phase-4-final-audit-remediation.md`
- `reviews/phase-4-wave-3-cross-domain-normalization.md`
- `skills/master-skill-universe.md`
- `architecture/skill-registry-design.md`
- `skills/legal-compliance-procurement/requirement-traceability.md`
- the four Pack Cards: Project Finance Metrics, CoVE, LIFE, Supabase
- Wave 1 and Wave 2 mapping files
- active Skill / Specialisation / Pack cards as needed for compatibility verification

## 1. Retired taxonomy
Verify:
- no retired ID is presented as active capability guidance;
- `skill.traceability_matrix_design` appears only in historical/deprecation/migration context;
- retired `specialisation.affordability` and `specialisation.tariff_modelling` are not instructed to remain distinct;
- architecture examples no longer present affordability/tariff modelling as Specialisation methods;
- all five Wave 3 retirements remain absent from active mappings.

## 2. Pack Card reconciliation
Independently compare each card against current canonical mappings and allowlists:
- `skill_pack.project_finance_metrics`
- `skill_pack.cove`
- `skill_pack.life_programme`
- `skill_pack.supabase`

Verify card prose no longer says mapped Roles are unmapped or omitted.
Expected: 0 stale mapping-status assertions.

## 3. Inventory/statistics
Recompute from actual files, correctly handling:
- grouped parent bullets with nested IDs;
- inline ALTERNATIVE pairs such as `id1 OR id2`.

Verify current values:
- Active Universe: 205 Skills / 41 Specialisations / 21 Packs = 267
- Deprecated IDs: 23
- Wave 1 entries: 147 = 52 CORE / 61 RFC / 32 OPTIONAL / 2 ALTERNATIVE / 0 PROHIBITED
- Wave 2 entries: 676 = 188 / 230 / 192 / 56 / 10
- Combined entries: 823 = 240 / 291 / 224 / 58 / 10
- Alternative sets: 11
- REQUIRED_CORE min 2 / max 8 / average 4.07
- Positive-use IDs: 264
- Single-role positive-use IDs: 93 / 264 = 35.2%
- Cards: 12 of 267
- Carded Skills: 6/205
- Carded Specialisations: 1/41
- Carded Packs: 5/21
- Uncarded active capabilities: 255
- `skill.use_case_modelling` is counted as used

Report any discrepancy.

## 4. Duplicate activation evidence
Recompute direct-Skill + Pack overlap paths across both waves.
Verify:
- required-component overlap paths: 20
- unique Role–Skill pairs: 14
- unique Skills: 10
- optional-component overlap paths: 36
- all paths: 56

Confirm all are governed by the one-activation / stricter-obligation rule and no false claim of exhaustiveness remains.

## 5. Compatibility and authority regression
Reconfirm:
- direct Role -> Skill testable incompatibilities: 0
- direct Role -> Specialisation testable incompatibilities: 0
- direct Role -> Pack testable incompatibilities: 0
- transitive Pack -> carded component incompatibilities: 0
- orphan allowlist entries: 0
- uncarded targets remain NOT YET VALIDATABLE
- Security Engineer remains outside `skill.quality_attribute_analysis` and `skill_pack.supabase`
- `skill.lifecycle_cost_analysis` remains support-only to `role.technical_feasibility_lead`
- Phase 3 Role Cards unchanged
- all Phase 4 artifacts remain PROPOSED

## 6. Approval readiness
If and only if no blocker remains, recommend human approval of Phase 4 architecture.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. RETIRED TAXONOMY
PASS / FAIL + findings

### C. PACK CARD CONSISTENCY
PASS / FAIL + stale assertion count

### D. STATISTICAL RECHECK
Actual recomputed values and discrepancies

### E. DUPLICATE ACTIVATION RECHECK
Actual recomputed 20 / 14 / 10 / 36 / 56 values and PASS / FAIL

### F. COMPATIBILITY / AUTHORITY REGRESSION
PASS / FAIL + counts

### G. REMAINING BLOCKERS
If none: NONE.

### H. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 4
- READY AFTER LISTED CHANGES
- NOT READY

### I. CARD-GENERATION VERDICT
Choose exactly one:
- NOT YET — KEEP SELECTIVE
- SAFE FOR CONTROLLED BATCH GENERATION
- SAFE FOR MASS GENERATION

Do not modify anything.