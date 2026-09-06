# Claude Code Prompt — Phase 4 Wave 2 Remediation After Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected starting HEAD: `61e165a960018e6d5aa38f4d3e3a4d049e55800e`

Independent Wave 2 audit verdict:
- FINAL VERDICT: FAIL
- CRITICAL/HIGH: 48 existing-card compatibility conflicts
- NEXT STEP: GO AFTER LISTED CHANGES
- CARD GENERATION: NOT YET — KEEP SELECTIVE

This is a narrowly scoped APPLY remediation.

Do not create new Skill / Specialisation / Skill Pack Cards.
Do not modify approved Phase 3 Role Cards.
Do not modify Wave 1 mappings.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not introduce implementation, model/runtime binding, orchestration, database schema or agent-framework design.

## Read first

1. `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`
2. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
3. `skills/master-skill-universe.md`
4. `skills/_standards/common-skill-constraints.md`
5. `architecture/role-to-skill-mapping-rules.md`
6. all 10 exemplar Skill / Skill Pack Cards
7. every approved Phase 3 Role Card touched by a remediation decision
8. `reviews/phase-3-final-approval.md`

## Audit findings to remediate

### A. Direct Skill Card allowlist conflicts
The audit found 37 direct Wave 2 Skill mappings that conflict with existing Skill Card allowlists:
- `skill.source_verification`: 20 Role mappings
- `skill.requirement_traceability`: 7 Role mappings
- `skill.source_monitoring`: 8 Role mappings
- `skill.lifecycle_cost_analysis`: 2 Role mappings

For the first three Skills:
1. independently inspect every affected Wave 2 Role mapping against the Role Card;
2. if the mapping is professionally valid and does not widen authority, add the Role to the Skill Card compatible-role allowlist;
3. update only mapping-reference / compatibility explanatory prose as needed;
4. do not change authority, artifact, review, decision, evidence or knowledge-state boundaries;
5. if any direct mapping is not defensible from the Role Card, REMOVE or reclassify the mapping rather than widening the allowlist.

For `skill.lifecycle_cost_analysis`, do NOT widen the Skill Card.
The reviewed card explicitly restricts this Skill to support-only technical-option comparison by `role.technical_feasibility_lead` and explicitly excludes CAPEX / Cost Engineering and Asset O&M as consuming Roles.

Therefore remove the Wave 2 direct mappings of `skill.lifecycle_cost_analysis` from:
- CAPEX / Cost Engineering Specialist
- Asset O&M / Technical Operations Specialist

If those Roles need lifecycle-related work, use their existing Role-owned cost/O&M capabilities already present in the Universe; do not recreate the support-only Skill under another ID.

### B. Carded Skill Pack allowlist conflicts
The audit found all 11 Wave 2 mappings to the five carded Packs use Roles absent from the Pack Cards’ compatible-role allowlists:

- `skill_pack.bid_proposal_management` -> Project Development Lead
- `skill_pack.life_programme` -> EU Programme Implementation & Grant Management Specialist
- `skill_pack.project_finance_metrics` -> Funding & Bankability Architect
- `skill_pack.project_finance_metrics` -> Project Finance / Transaction Specialist
- `skill_pack.project_finance_metrics` -> PPP / Concession Specialist
- `skill_pack.supabase` -> Full-Stack Software Engineer
- `skill_pack.supabase` -> Integration / API Engineer
- `skill_pack.supabase` -> Platform / DevOps Engineer
- `skill_pack.supabase` -> Database / Data Engineer
- `skill_pack.cove` -> EU Programme Implementation & Grant Management Specialist
- `skill_pack.cove` -> Learning / VET Design Specialist

For each of the 11:
1. verify the Wave 2 mapping is defensible from the consuming Role Card;
2. if valid, add the Role to the Pack Card compatible-role allowlist and update mapping-reference / compatibility prose only;
3. if invalid, remove or reclassify the Wave 2 mapping instead of widening the Pack Card;
4. preserve all Pack authority/boundary/source/knowledge-state sections unchanged.

Do NOT add `role.security_engineer` to `skill_pack.supabase` or `skill.quality_attribute_analysis`; the audit independently confirmed that the decision to exclude Security Engineer is CORRECT.

### C. Economic / CBA relationship contradiction
The audit found `skill.economic_cost_benefit_analysis` is both:
- REQUIRED_CORE; and
- a member of a mutually exclusive one-of ALTERNATIVE set with `skill.cost_effectiveness_analysis`.

Fix this so the mapping is logically coherent.

Preferred architecture unless the Role Card proves otherwise:
- remove `skill.economic_cost_benefit_analysis` from REQUIRED_CORE;
- retain the one-of ALTERNATIVE set between economic CBA and cost-effectiveness analysis with its existing operational choice condition.

If the Role Card requires a different structure, document the reason and ensure no capability is simultaneously REQUIRED_CORE and mutually exclusive ALTERNATIVE.

### D. Asset O&M PROHIBITED_IN_CONTEXT trigger
The audit found the Asset O&M prohibition on `skill.opex_estimation` too broad.

Narrow it to match the Role Card exactly:
- prohibition applies only where a dedicated cost-engineering assignment exists / cost-estimate ownership is assigned to CAPEX / Cost Engineering;
- outside that condition, do not claim a global prohibition beyond the Role Card.

Preserve Asset O&M’s own approved operating-cost-driver / lifecycle / O&M ownership boundaries.

### E. Specialisation class note
The audit found the actual Wave 2 data exercises seven Specialisation classes, not six.

Correct the Wave 2 summary/statistics if it says six.

For future carding only, record as a non-blocking Wave 3 note that:
- `specialisation.admin_console`
- `specialisation.institutional_website`
look like OPERATING_CONTEXT rather than TECHNOLOGY.

Do not create or reclassify Specialisation Cards in this remediation unless the Master Skill Universe itself actively misclassifies them and changing that metadata is necessary for consistency. If changed, do not alter authority semantics.

## New mandatory compatibility validation rule

The audit exposed a gap: Transitive Pack Compatibility covered Pack components, but direct Role-to-Skill and Role-to-Pack mappings were not systematically checked against card allowlists.

Add one explicit architecture rule, in the appropriate active standard/rules documents:

### Direct Mapping Compatibility Rule
For every active Role-to-Skill, Role-to-Specialisation or Role-to-Skill-Pack mapping:
- if the target capability has a card, the consuming Role MUST be permitted by that card’s compatible-role allowlist or governed compatibility rule;
- absence from the allowlist is a validation failure;
- runtime may not widen allowlists;
- remediation must either (a) widen compatibility through governed card change after Role-boundary review, or (b) remove/reclassify the mapping;
- this compatibility rule does NOT define relationship type or context trigger; those remain solely in Role-to-Skill mapping records.

Also preserve the existing Transitive Pack Compatibility Rule for Pack components.

The two rules together must cover:
1. direct Role -> Skill
2. direct Role -> Specialisation (when carded)
3. direct Role -> Skill Pack
4. transitive Pack -> component Skill

## Full compatibility re-check

After remediation, independently re-check ALL active mappings across Wave 1 + Wave 2 against every currently existing Skill / Pack Card, not just the 48 findings.

Report separately:
- direct Skill mapping compatibility
- direct Pack mapping compatibility
- transitive Pack-component compatibility
- uncarded capabilities as NOT YET VALIDATABLE

Zero testable incompatibilities must remain.

## Boundary preservation requirements

For every existing card edited in this remediation:
- preserve Skill Boundary / Support-Only Boundary / Outputs-Contributions / Review-Decision / Evidence / Knowledge-State / Authority Limits sections byte-identically where possible;
- allowed edits: compatible-role allowlist, canonical mapping references, compatibility explanatory prose, identity metadata only if needed for an audit-cited classification correction;
- do not add a Role simply because it seems adjacent; there must be a valid Wave 1 or Wave 2 mapping and approved Role Card basis.

## Statistical update

Recompute Wave 2 statistics after removing/reclassifying mappings, including:
- active mapping count
- relationship distribution
- unique Skills / Specialisations / Packs
- REQUIRED_CORE min/max/average
- ALTERNATIVE member count and set count
- PROHIBITED count
- any changed single-role-use/reuse figures if the mapping document contains them

Do not leave stale numbers in the mapping file.

## Validation before commit

Run and report all checks:

1. Exactly 48 Wave 2 Role subjects remain.
2. Wave 1 file unchanged.
3. Phase 3 Role Cards unchanged.
4. All active IDs exist in Master Skill Universe.
5. Zero deprecated active IDs.
6. Zero Candidate Universe Gap IDs in active mappings.
7. Zero direct Skill mapping/card allowlist incompatibilities across Wave 1 + Wave 2 for carded Skills.
8. Zero direct Pack mapping/card allowlist incompatibilities across Wave 1 + Wave 2 for carded Packs.
9. Zero transitive Pack-component incompatibilities for currently carded components.
10. Uncarded capabilities/components explicitly reported NOT YET VALIDATABLE.
11. `skill.lifecycle_cost_analysis` is NOT directly mapped to CAPEX / Cost Engineering.
12. `skill.lifecycle_cost_analysis` is NOT directly mapped to Asset O&M.
13. `skill.lifecycle_cost_analysis` reviewed card boundary remains unchanged.
14. Security Engineer remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase`.
15. No Role is simultaneously REQUIRED_CORE and mutually exclusive ALTERNATIVE for the same capability.
16. Economic / CBA appraisal-method set is logically coherent.
17. Asset O&M `skill.opex_estimation` prohibition has the narrower Role-Card-consistent trigger.
18. All REQUIRED_FOR_CONTEXT mappings retain explicit triggers.
19. All ALTERNATIVE sets retain cardinality and operational choice conditions.
20. All PROHIBITED_IN_CONTEXT mappings retain concrete defensible bases.
21. Direct Mapping Compatibility Rule exists explicitly.
22. Transitive Pack Compatibility Rule remains intact.
23. Mapping records remain the sole authoritative source for relationship type and trigger.
24. No edited card gains professional authority, artifact ownership, independent review identity, or human decision authority.
25. No model/runtime binding.
26. No new Skill / Specialisation / Pack Cards.
27. All active Phase 4 artifacts remain PROPOSED / working.
28. Wave 2 Specialisation class count summary matches actual active data.
29. Wave 2 statistics are recomputed from actual active mappings after remediation.
30. Independent re-audit can validate the result without relying on Claude console history.

## Commit / Push

If all mandatory checks pass:

Commit exactly:
`docs: remediate Phase 4 Wave 2 after independent audit`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. REMEDIATION APPLIED
Files changed and exact categories of fixes.

### B. DIRECT SKILL COMPATIBILITY
Before/after conflict counts and any mappings removed instead of allowlist widening.

### C. DIRECT PACK COMPATIBILITY
Before/after conflict counts and allowlist changes/removals.

### D. RELATIONSHIP FIXES
Economic/CBA contradiction and Asset O&M prohibition fix.

### E. SECURITY / LIFECYCLE BOUNDARIES
Confirm Security Engineer decision and lifecycle-cost support-only boundary remain intact.

### F. COMPATIBILITY RULES
Direct Mapping Compatibility + Transitive Pack Compatibility status.

### G. STATISTICAL RECHECK
Updated actual mapping statistics.

### H. VALIDATION
Checks 1–30 PASS / FAIL.

### I. REMAINING TESTABLE INCOMPATIBILITIES
If none: NONE.

### J. REMAINING NON-BLOCKING NOTES
Uncarded/unvalidated coverage and Wave 3 notes only.

### K. COMMIT / PUSH
Commit SHA and push result.

### L. NEXT-STEP READINESS
Choose:
- READY FOR FINAL WAVE 2 RE-AUDIT
- NOT READY

Do not claim Phase 4 approval or card-generation readiness.