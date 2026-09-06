# Claude Code Prompt — Phase 4 Exemplar Allowlist Remediation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected starting HEAD: `6e5910e342219c9a8f6f6c8b7b421405ddf38063`

The independent audit of the 10 exemplar Skill / Skill Pack Cards returned:
- FINAL VERDICT: PASS WITH CHANGES
- HIGH / CRITICAL FINDINGS: NONE
- NEXT STEP: GO AFTER LISTED CHANGES
- MASS GENERATION: NOT YET — KEEP SELECTIVE

This is a narrowly scoped APPLY task.

Do not modify Phase 3 Role Cards.
Do not create new Skill / Specialisation / Skill Pack Cards.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not introduce implementation, database, orchestration, model/runtime or agent-framework design.

## Read first

1. `skills/_standards/common-skill-constraints.md`
2. `skills/_templates/skill-card-template.md`
3. `skills/_templates/skill-pack-template.md`
4. `architecture/role-to-skill-mapping-rules.md`
5. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
6. all 10 exemplar cards
7. `skills/master-skill-universe.md`
8. approved Role Cards for all roles named below

## Problem to fix

The independent audit found no authority, artifact, review, decision, source-governance or mapping-source defects.

The only required changes are **component Skill allowlist consistency defects created by Pack activation**.

A Pack may validly activate a Skill for a Role. If so, the Skill Card's compatible-role allowlist must not reject that Role.

This does **not** make the Skill Card the source of relationship type or trigger. The mapping record remains the sole authoritative source for relationship type and trigger.

## Required card changes

Update only the relevant Skill Cards and, if needed, the active Phase 4 validation rule documentation.

### 1. `skill.source_verification`
File:
`skills/research-evidence/source-verification.md`

Add to compatible-role allowlist:
- `role.sales_business_development_specialist`

Reason:
`skill_pack.bid_proposal_management` exposes Source Verification as a component for a Pack mapped to Sales / Business Development.

Boundary must remain unchanged:
- no factual truth determination;
- no independent review;
- no legal interpretation;
- no evidence-governance authority;
- no knowledge-state promotion.

Do not add a direct relationship type or trigger to the Skill Card.

### 2. `skill.requirement_traceability`
File:
`skills/legal-compliance-procurement/requirement-traceability.md`

Add to compatible-role allowlist:
- `role.sales_business_development_specialist`

Reason:
`skill_pack.bid_proposal_management` requires Requirement Traceability for a Pack mapped to Sales / Business Development.

Boundary must remain unchanged:
- linkage only;
- no requirement approval;
- no compliance conclusion;
- no Product, Legal, Architecture or Data authority transfer.

Do not add a direct relationship type or trigger to the Skill Card.

### 3. `skill.quality_attribute_analysis`
File:
`skills/software-integration-platform-security/quality-attribute-analysis.md`

Add to compatible-role allowlist:
- `role.data_database_architect`

Reason:
`skill_pack.supabase` requires Quality Attribute Analysis for a Pack mapped to Data & Database Architect.

Boundary must remain unchanged:
- no security conclusion;
- no security accreditation;
- no security risk acceptance;
- no DPIA/lawful-basis conclusion;
- no replacement of `role.security_engineer` or `role.data_protection_gdpr_specialist`.

Do not add a direct relationship type or trigger to the Skill Card.

### 4. `skill.source_monitoring`
File:
`skills/research-evidence/source-monitoring.md`

Add to compatible-role allowlist:
- `role.eu_grants_programmes_specialist`

Reason:
Both `skill_pack.life_programme` and `skill_pack.cove` require Source Monitoring for Packs mapped to EU Grants & Programmes Specialist.

Boundary must remain unchanged:
- change detection / monitoring only;
- no policy/legal interpretation;
- no canonical rewrite;
- no knowledge-state transition;
- no external publication authority.

Do not add a direct relationship type or trigger to the Skill Card.

## Required architecture validation rule

Add one explicit validation rule in the most appropriate active Phase 4 architecture/constraint document, preferably `skills/_standards/common-skill-constraints.md` or `architecture/role-to-skill-mapping-rules.md`:

> **Transitive Pack Compatibility Rule:** if a Role is permitted to activate a Skill Pack, every Required Skill and every conditionally activated Skill inside that Pack must be compatible with that Role, either through the Skill Card allowlist or through a governed compatibility rule. A Pack must not transitively activate a Skill that explicitly excludes the consuming Role. This check does not create a Role relationship or trigger; it validates compatibility only.

Also clarify:
- Optional Pack components that can be selected for a Role must likewise not be prohibited by their Skill Card allowlist.
- If a Pack component is incompatible with a Role, activation must fail validation rather than silently widen the Skill allowlist at runtime.
- Relationship type and context trigger still come only from Role-to-Skill mapping records.

Do not create a second source of truth.

## Validation

Run and report all of the following:

1. `skill.source_verification` allowlist contains `role.sales_business_development_specialist`.
2. `skill.requirement_traceability` allowlist contains `role.sales_business_development_specialist`.
3. `skill.quality_attribute_analysis` allowlist contains `role.data_database_architect`.
4. `skill.source_monitoring` allowlist contains `role.eu_grants_programmes_specialist`.
5. No direct REQUIRED_CORE / REQUIRED_FOR_CONTEXT / OPTIONAL / ALTERNATIVE / PROHIBITED_IN_CONTEXT relationship is introduced in any Skill Card.
6. No card defines a new context trigger.
7. Wave 1 mapping remains the sole authoritative source for relationship type and trigger.
8. All four Skill boundaries remain substantively unchanged.
9. `skill.lifecycle_cost_analysis` remains unchanged.
10. LIFE, CoVE, Supabase and Bid / Proposal Pack boundaries remain unchanged.
11. No new Skill / Pack / Specialisation cards are created.
12. No Phase 3 Role Card changes.
13. No invented artifact/review/decision IDs.
14. No active deprecated ID reintroduced.
15. No model/runtime binding introduced.
16. All active Phase 4 artifacts remain PROPOSED / working.
17. The Transitive Pack Compatibility Rule is explicit and machine-checkable in principle.
18. Re-check all five Packs against their Required and Optional Skill allowlists and report any remaining incompatibility.
19. Re-check all 10 exemplar cards for second-source mapping leakage.
20. Report whether the independent audit's required changes are fully resolved.

## Commit / Push

If all mandatory checks pass:

Commit exactly:
`docs: fix exemplar Skill allowlists for Pack compatibility`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. CHANGES APPLIED
List files and exact allowlist additions plus validation-rule addition.

### B. TRANSITIVE PACK COMPATIBILITY
Explain the rule and confirm it does not become a relationship/trigger source.

### C. BOUNDARY PRESERVATION
Confirm source verification, requirement traceability, quality attribute analysis and source monitoring authority boundaries are unchanged.

### D. VALIDATION
Checks 1–20 PASS / FAIL.

### E. REMAINING INCOMPATIBILITIES
If none: NONE.

### F. COMMIT / PUSH
Commit SHA and push result.

### G. NEXT-STEP READINESS
Choose:
- READY FOR FINAL RE-CHECK
- NOT READY

Do not claim Phase 4 approval.