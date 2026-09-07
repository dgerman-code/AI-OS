# Codex Prompt — Final Independent Phase 4 Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected HEAD: `85507e0d53a29cd5eaf5441aed63b902ef517235`

Act as an independent senior architecture auditor. This is the FINAL Phase 4 audit before human approval.

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark anything APPROVED or CANONICAL.
Do not propose implementation, runtime, database schema, orchestration or model binding.

Read the full Phase 4 architecture and evidence set, including:
- `architecture/skill-registry-design.md`
- `architecture/role-to-skill-mapping-rules.md`
- `skills/master-skill-universe.md`
- `skills/_standards/common-skill-constraints.md`
- Skill and Pack templates
- Wave 1 mapping
- Wave 2 mapping
- all existing Skill / Specialisation / Skill Pack Cards
- `reviews/phase-4-wave-3-cross-domain-normalization.md`
- all approved Phase 3 Role Cards referenced by mappings
- `reviews/phase-3-final-approval.md`
- `architecture/project-criticality-policy.md`

## Audit scope

### 1. Phase 4 completeness
Determine whether the intended Phase 4 deliverables are now substantively complete:
1. principles/taxonomy
2. Skill Card / Skill Pack standard
3. Master Skill Universe
4. Role-to-Skill mapping rules
5. versioned exemplar Skill/Specialisation/Pack cards
6. cross-role reuse / duplication normalization
7. independent architecture review readiness

Confirm Phase 4 does NOT accidentally implement later phases.

### 2. Role coverage and identity
Verify all 59 approved Phase 3 Roles are covered exactly once across Wave 1 + Wave 2, with exact Role IDs from actual Role Cards and no duplicates/missing Roles.

### 3. Universe integrity
Recompute and verify:
- active Skill count
- active Specialisation count
- active Pack count
- deprecated/tombstoned IDs
- zero active references to retired IDs
- zero unresolved active IDs

Check all Wave 3 merges/retirements:
- `skill.resource_planning` -> `skill.capacity_planning`
- `skill.insurance_gap_analysis` -> `skill.insurance_programme_analysis`
- `skill.traceability_matrix_design` -> `skill.requirement_traceability`
- `specialisation.affordability` -> `skill.affordability_analysis`
- `specialisation.tariff_modelling` -> `skill.tariff_analysis`

### 4. Gap decisions
Independently verify all 8 Wave 3 candidate-gap decisions are coherent and none remains ambiguously unresolved.

Pay attention to:
- `skill.negotiation_preparation`
- `skill.variance_analysis`
- `skill.defect_management`

Confirm newly added Skills are reusable capabilities, not hidden Roles or assignment prose.

### 5. Overlap / micro-skill normalization
Review all 14 named overlap groups and confirm each KEEP / MERGE / RENAME / PACK-INTERNALIZE decision is defensible.

Specifically re-check:
- requirement traceability vs matrix design
- resource vs capacity planning
- insurance gap vs programme analysis
- source discovery / comparison / verification / monitoring / change detection
- process design / mapping / SOP design
- action tracking / milestone / deliverable planning
- evidence indexing / data-room index design
- security_control_design vs risk_control_design

Flag any remaining HIGH-confidence duplicate that should be resolved before approval.

### 6. Relationship taxonomy
Audit REQUIRED_CORE / REQUIRED_FOR_CONTEXT / OPTIONAL / ALTERNATIVE / PROHIBITED_IN_CONTEXT across both waves.

Confirm:
- REQUIRED_CORE remains sparse and role-intrinsic;
- every RFC has an explicit trigger;
- every ALTERNATIVE has cardinality + operational choice condition;
- every PROHIBITED has a concrete defensible basis;
- no capability is simultaneously REQUIRED_CORE and mutually-exclusive ALTERNATIVE;
- mapping relationship types do not encode authority.

### 7. Compatibility architecture
Independently recompute all testable compatibility paths:
1. direct Role -> Skill
2. direct Role -> Specialisation where carded
3. direct Role -> Skill Pack
4. transitive Pack -> component Skill
5. reverse allowlist basis (no orphan allowlist entries)

Expected: 0 testable incompatibilities and 0 orphan allowlist entries.

Uncarded capabilities/components must be reported as NOT YET VALIDATABLE, never PASS.

### 8. Authority / boundary preservation
Across all mappings, merges, allowlist changes and new cards, verify no capability:
- widens approved Role scope;
- transfers another Role’s professional conclusion;
- creates artifact ownership;
- creates independent review identity;
- creates human decision authority;
- bypasses review / decision gates;
- turns support-only technique into professional ownership.

Re-check especially:
- `skill.lifecycle_cost_analysis` remains support-only to Technical / Feasibility Lead;
- Security Engineer remains outside `skill.quality_attribute_analysis` and `skill_pack.supabase` support path;
- Data Room vs Knowledge & Evidence Steward;
- Procurement/State Aid vs Legal;
- Funding & Bankability vs Project Finance;
- CAPEX vs Financial Modelling;
- QA/Test Automation vs Review Profiles.

### 9. New Wave 3 cards
Audit both new cards:
- `skills/strategy-analysis/negotiation-preparation.md`
- `skills/specialisations/sector/bess.md`

Verify template conformance, PROPOSED status, allowlist basis, no authority leakage, no invented review/decision/artifact IDs, and proper Specialisation semantics for BESS.

### 10. Specialisation model
Verify Specialisation classification and bounded-context semantics after Wave 3.

Specifically:
- `specialisation.admin_console` and `specialisation.institutional_website` behave as OPERATING_CONTEXT, not TECHNOLOGY;
- retired affordability/tariff pseudo-specialisations no longer act as Specialisations;
- BESS exemplar validates the standalone `Type: SPECIALISATION` template path;
- METRIC being represented only inside `skill_pack.project_finance_metrics` is either acceptable or identify as a blocker/non-blocker.

### 11. Pack/direct normalization
Verify all duplicate direct+Pack activation cases are either removed or intentionally retained under the stricter-obligation rule.

Confirm no Pack becomes a second relationship/trigger source and no Pack accumulates authority.

### 12. Statistical integrity
Recompute from actual current mappings:
- total mapping entries Wave 1 / Wave 2 / combined
- counts by relationship type
- unique used capability IDs
- unique Skills / Specialisations / Packs in mappings
- REQUIRED_CORE min/max/average per Role
- ALTERNATIVE set count
- PROHIBITED count
- single-role positive-use count and percentage
- top 20 reused IDs
- duplicate Pack/direct cases

Report any discrepancy from Wave 3 record.

### 13. Maintainability / scale
Assess whether Phase 4 is now maintainable enough to approve as architecture despite many uncarded capabilities.

Consider:
- 59-role coverage
- 205 Skills / 41 Specialisations / 21 Packs
- only 12 cards
- single-role-use ~35%
- reverse allowlist rule
- direct + transitive compatibility rules
- deprecation registry growth
- future drift risk

Distinguish clearly between:
- readiness to APPROVE Phase 4 architecture;
- readiness for selective card generation;
- readiness for controlled batch generation;
- readiness for mass generation.

### 14. Phase boundary check
Confirm Phase 4 remains architecture/governance only and has not drifted into:
- Workflow Registry
- Handoff/Review implementation
- Decision Rights Register implementation
- Memory/Canonical implementation
- Model Registry/Router
- Orchestrator
- runtime/DB schema

### 15. Approval recommendation
Decide whether Phase 4 is ready for HUMAN APPROVAL.

A few non-blocking notes are acceptable.
Any unresolved HIGH authority, identity, compatibility, active-ID or taxonomy contradiction is blocking.

## Required output

Return exactly:

### A. FINAL VERDICT
Choose one:
- PASS
- PASS WITH NON-BLOCKING NOTES
- PASS WITH CHANGES
- FAIL

### B. CRITICAL / HIGH FINDINGS
If none: NONE.

### C. PHASE 4 COMPLETENESS
PASS / FAIL with concise rationale.

### D. ROLE / ID / UNIVERSE INTEGRITY
Actual counts and PASS / FAIL.

### E. GAP & OVERLAP NORMALIZATION
8 gap decisions + material overlap verdicts.

### F. RELATIONSHIP TAXONOMY
PASS / FAIL and any misuse.

### G. COMPATIBILITY VALIDATION
Direct Skill / Direct Specialisation / Direct Pack / Transitive / Reverse allowlist counts.

### H. AUTHORITY BOUNDARIES
PASS / FAIL and any issue.

### I. NEW CARD AUDIT
Negotiation Preparation + BESS Specialisation verdicts.

### J. SPECIALISATION / PACK MODEL
PASS / FAIL and remaining notes.

### K. STATISTICAL RECHECK
Actual recomputed metrics and discrepancies.

### L. SCALE / MAINTAINABILITY
Architecture-readiness assessment.

### M. PHASE-BOUNDARY CHECK
PASS / FAIL.

### N. REMAINING BLOCKERS
If none: NONE.

### O. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 4
- READY AFTER LISTED CHANGES
- NOT READY

### P. CARD-GENERATION VERDICT
Choose exactly one:
- NOT YET — KEEP SELECTIVE
- SAFE FOR CONTROLLED BATCH GENERATION
- SAFE FOR MASS GENERATION

Do not modify anything.