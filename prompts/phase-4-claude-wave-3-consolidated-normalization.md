# Claude Code Prompt — Phase 4 Wave 3 Consolidated Cross-Domain Normalization

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected starting HEAD: `7facd10a8132e016dc5f6f2c84500200104bad4f`

Final Wave 2 re-audit verdict:
- PASS WITH NON-BLOCKING NOTES
- Direct Skill compatibility: PASS, 0 conflicts
- Direct Pack compatibility: PASS, 0 conflicts
- Transitive compatibility: PASS, 0 conflicts
- Remaining blockers: NONE
- Next step: GO TO WAVE 3 CROSS-DOMAIN NORMALIZATION
- Card generation: NOT YET — KEEP SELECTIVE

This is the **single consolidated Wave 3 normalization pass** intended to avoid multiple micro-cycles.

Do not modify approved Phase 3 Role Cards.
Do not modify Wave 1 role subjects or relationship decisions unless a proven cross-wave normalization defect requires a governed correction; if so, document it explicitly.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not introduce model/runtime bindings, orchestration, database schema, agent framework or production implementation.
Do not mass-generate cards.

## Read first

Read all Phase 4 architecture, standards, templates, Master Skill Universe, Wave 1 mapping, Wave 2 mapping, all existing Skill / Skill Pack Cards, Phase 3 final approval, and project criticality policy.

Also read the final Wave 2 re-audit notes reflected in the current mapping/remediation record.

## Wave 3 goals

Wave 3 must normalize the Skill Registry across all 59 approved Roles before any broader card generation.

Complete all work below in one governed pass.

---

## 1. Correct the Project Development Lead audit-trail prose

The final re-audit confirmed the decision to remove `skill_pack.bid_proposal_management` from Project Development Lead is correct, but the permanent explanatory prose is factually too broad.

Correct the Wave 2 remediation/audit-trail wording so it does NOT say the Role has “no governed-submission surface” or only internal artifacts.

Use the accurate distinction:
- the Role does have external submissions to lenders, investors and authorities;
- it does have tender-deadline awareness;
- but it does NOT own a formal competitive response-to-solicitation / bid-proposal submission process;
- therefore `skill_pack.bid_proposal_management` remains out of scope.

Do not change the mapping decision.

---

## 2. Resolve the 8 Candidate Universe Gaps

Review these candidates against all 59 Role Cards and the existing Universe:

- `skill.governance_structure_design`
- `skill.editorial_multilingual_coordination`
- `skill.negotiation_preparation`
- `skill.variance_analysis`
- `skill.commissioning_readiness_assessment`
- `skill.defect_management`
- `skill.qa_response_control`
- `skill.accession_alignment_analysis`

For each choose exactly one:
- ADD AS REUSABLE SKILL
- REPRESENT WITH EXISTING SKILL / SPECIALISATION / PACK
- ROLE-SPECIFIC PROSE — DO NOT ADD
- SPLIT / REFRAME BEFORE ADDING

Apply the decision in this pass where safe:
- if ADD AS REUSABLE SKILL: add it to `skills/master-skill-universe.md` only, with family, concise scope, reuse rationale and explicit non-authority boundary;
- do NOT create a Skill Card yet unless required by section 7 selective carding below;
- if REPRESENT WITH EXISTING: update Wave 2 mapping only where the existing active mapping should change;
- if ROLE-SPECIFIC PROSE: keep it out of active mappings and document why;
- if SPLIT / REFRAME: do not activate unresolved IDs; document the proposed normalized shape.

No candidate may remain ambiguously “maybe” after Wave 3.

---

## 3. Normalize the named overlap / micro-skill groups

Audit and resolve these groups across Wave 1 + Wave 2 + Master Skill Universe:

1. market sizing / market segmentation / demand forecasting
2. risk identification / risk register design
3. action tracking / milestone management / deliverable planning
4. process design / process mapping / SOP design
5. source discovery / source comparison / source verification / source monitoring / change detection
6. capacity planning / resource planning
7. evidence indexing / data room index design
8. insurance gap analysis / insurance programme analysis
9. ESG screening / ESG gap analysis
10. `security_control_design` vs `risk_control_design`
11. `requirement_traceability` vs `traceability_matrix_design`
12. source monitoring vs change detection
13. privacy-impact / security-control support mappings where naming risks implying specialist authority
14. any additional high-confidence overlap surfaced by actual reuse data

For each choose one governed outcome:
- KEEP DISTINCT — clarify boundaries
- MERGE — choose survivor ID, deprecate retired ID, migrate mappings
- RENAME / CLARIFY — preserve ID unless rename is materially necessary; if renaming, create explicit deprecation alias/tombstone in Universe and migrate mappings
- PACK-INTERNALIZE — if capability is really pack-local and not independently reusable

Do not create micro-skills merely to preserve prose distinctions.
Do not merge skills with different professional methods simply because names look similar.

---

## 4. Reduce single-role over-cardification pressure

Recompute the 59-role reuse distribution from actual Wave 1 + Wave 2 mappings.

Current signal is approximately 95 of 265 used IDs single-role positive-use.

For every single-role-use capability, classify into one of:
- VALID REUSABLE BUT CURRENTLY SINGLE-CONSUMER
- ROLE-SPECIFIC TECHNIQUE — SHOULD NOT BE FIRST-CLASS SKILL
- PACK-INTERNAL CANDIDATE
- SPECIALISATION CANDIDATE
- NEEDS MORE CONSUMERS BEFORE CARDING

Do not rewrite all mappings merely to reduce the percentage.
Only normalize high-confidence cases.

Produce before/after single-role counts and percentage.

---

## 5. Normalize Pack-vs-direct activation

Review all duplicate direct-Skill + Pack activation cases across both waves.

Ensure:
- duplicate effective activation is one capability activation under the stricter obligation;
- direct mapping remains only when the Skill has independent meaning outside the Pack;
- Pack-internal capabilities are not redundantly exposed as direct mandatory mappings;
- no Pack widens authority;
- no relationship/trigger source moves into a Pack Card.

Resolve high-confidence duplication in this pass and report any intentionally retained duplicates.

---

## 6. Specialisation normalization

Review all active Specialisations across Wave 1 + Wave 2.

Specifically address:
- `specialisation.admin_console`
- `specialisation.institutional_website`

They behave like OPERATING_CONTEXT rather than TECHNOLOGY.

Normalize classification semantics in the Universe / normalization record where applicable, without creating authority.

Also audit whether any active Specialisation is actually:
- a hidden Skill;
- a hidden Pack;
- a hidden Role;
- too broad to be bounded context.

Correct high-confidence classification defects now.

---

## 7. Selective carding only where normalization requires it

Mass generation remains prohibited.

You MAY create a very small number of new Cards only if one of the following is necessary to validate a normalized architecture decision:
- one real standalone `Type: SPECIALISATION` exemplar, because this remains an untested template path;
- one or two high-risk normalized Skills whose authority boundary cannot be safely left implicit;
- one Pack Card whose absence prevents validating a major cross-domain normalization decision.

Hard cap: **maximum 3 new cards total** in Wave 3.

If no new card is necessary, create none.

Every new card must remain PROPOSED and pass Direct Mapping Compatibility and Transitive Pack Compatibility.

---

## 8. Strengthen compatibility validation as architecture, not runtime

Do not create production code.

Add or refine a static validation specification/checklist so future independent audits must verify all four paths:
1. direct Role -> Skill
2. direct Role -> Specialisation (when carded)
3. direct Role -> Skill Pack
4. transitive Pack -> component Skill

Also require reverse-direction validation:
- every Role in a capability card allowlist must have an actual direct or governed transitive mapping basis;
- orphan allowlist entries are a defect.

Keep mapping records as the sole source of relationship type and trigger.

---

## 9. Preserve authority boundaries

For every normalization decision, verify it does not:
- widen Role scope;
- transfer another Role’s professional conclusion;
- create artifact ownership;
- create independent review identity;
- create human decision authority;
- bypass review / decision gates;
- turn support work into ownership.

If a proposed merge would collapse two different authority boundaries, DO NOT MERGE.

---

## 10. Deliverables

Create or update as needed:
- `skills/master-skill-universe.md`
- `skills/mappings/wave-1-exemplar-role-skill-mapping.md` only if a proven normalization correction is necessary
- `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`
- `architecture/skill-registry-design.md` and/or mapping rules only where normalization policy requires clarification
- existing affected Skill / Pack Cards only for compatibility/reference/deprecation normalization
- up to 3 new cards under section 7 if necessary

Create one new consolidated record:

`reviews/phase-4-wave-3-cross-domain-normalization.md`

Status: `PROPOSED — READY FOR INDEPENDENT PHASE 4 REVIEW` only if all mandatory validation passes.

This record must contain:
- all 8 universe-gap decisions;
- all named overlap-group decisions;
- all merges/renames/deprecations and mapping migrations;
- single-role-use before/after;
- Pack/direct decisions;
- Specialisation normalization;
- new-card decisions if any;
- compatibility results;
- authority-boundary results;
- remaining non-blocking notes.

---

## 11. Validation

Run and report at least these checks:

1. All 59 approved Roles still covered exactly once across Wave 1 + Wave 2.
2. Phase 3 Role Cards unchanged.
3. No active mapping references missing IDs.
4. No deprecated ID remains active after any merge/rename.
5. Candidate Universe Gap decisions complete 8/8.
6. Named overlap decisions complete 14/14.
7. Every merge has one surviving ID and migrated mappings.
8. Every rename has explicit deprecation/tombstone handling.
9. Zero direct Skill/Card compatibility conflicts for existing cards.
10. Zero direct Pack/Card compatibility conflicts for existing cards.
11. Zero transitive Pack-component conflicts for carded components.
12. Zero orphan allowlist entries.
13. Uncarded targets remain NOT YET VALIDATABLE, not PASS.
14. No card boundary gains authority.
15. No model/runtime binding.
16. REQUIRED_CORE remains sparse.
17. Every RFC keeps an explicit trigger.
18. Every ALTERNATIVE keeps choice condition/cardinality.
19. Every PROHIBITED entry remains defensible.
20. Security Engineer remains excluded from support-only QA/Supabase path unless a new independent review proves otherwise.
21. `skill.lifecycle_cost_analysis` remains support-only to Technical / Feasibility Lead unless a new independent review proves otherwise.
22. Project Development Lead bid/proposal removal remains intact with corrected explanatory prose.
23. Specialisation classes are semantically coherent.
24. Any new cards <=3 and all PROPOSED.
25. Reverse allowlist basis check passes.
26. Pack/direct duplicate activation normalized.
27. Single-role-use statistics recomputed from actual mappings.
28. All active Phase 4 artifacts remain PROPOSED.
29. No PR created.
30. Wave 3 record is self-contained for final independent Phase 4 audit.

---

## Commit / Push

If all mandatory checks pass:

Commit exactly:
`docs: complete Phase 4 Wave 3 cross-domain normalization`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

---

## Required final output

Return exactly:

### A. WAVE 3 COMPLETED
Files changed and summary.

### B. UNIVERSE GAP DECISIONS
All 8 with final disposition.

### C. OVERLAP / MICRO-SKILL NORMALIZATION
All named groups with KEEP / MERGE / RENAME / PACK-INTERNALIZE outcomes.

### D. SINGLE-ROLE NORMALIZATION
Before/after counts and classifications.

### E. PACK / DIRECT NORMALIZATION
Resolved and retained cases.

### F. SPECIALISATION NORMALIZATION
Classification changes and any Specialisation exemplar card.

### G. SELECTIVE CARDING
0–3 cards created, with rationale.

### H. COMPATIBILITY / AUTHORITY VALIDATION
Direct Skill, direct Pack, transitive, reverse allowlist, authority-boundary results.

### I. STATISTICAL RECHECK
Updated actual counts.

### J. REMAINING NON-BLOCKING NOTES
If none: NONE.

### K. VALIDATION
Checks 1–30 PASS / FAIL.

### L. COMMIT / PUSH
Commit SHA and push result.

### M. NEXT-STEP READINESS
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 4 AUDIT
- NOT READY

Do not claim Phase 4 approval or mass-generation readiness.