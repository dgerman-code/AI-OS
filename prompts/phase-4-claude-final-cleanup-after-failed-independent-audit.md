# Claude Code Prompt — Final Phase 4 Cleanup After Failed Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected starting HEAD: `f1cf1eb7a2ab15884efa0fb9398a031fe45cba94`

The final independent Phase 4 audit returned FAIL, but the failure is concentrated in internal consistency and evidence accuracy rather than Role coverage, compatibility mechanics or authority boundaries.

Audit facts to preserve:
- Role coverage: PASS, 59/59 exactly once.
- Direct Skill compatibility: PASS.
- Direct Specialisation compatibility: PASS.
- Direct Pack compatibility: PASS.
- Transitive compatibility: PASS.
- Reverse allowlist basis: PASS.
- Authority boundaries: PASS.
- New cards Negotiation Preparation and BESS: PASS.
- Phase-boundary check: PASS.

Blocking findings to fix:
1. retired taxonomy still appears as active governing guidance;
2. four Pack Cards contradict canonical mappings in their explanatory prose;
3. inventory/reuse/duplicate-activation evidence contains stale or incomplete statistics.

This is a narrow FINAL CLEANUP APPLY task.

Do not change approved Phase 3 Role Cards.
Do not change Role coverage.
Do not add new Roles.
Do not create new Skill / Specialisation / Pack Cards.
Do not perform a new normalization programme.
Do not introduce model/runtime/orchestration/database/workflow implementation.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.

## 1. Remove stale retired-taxonomy guidance

### 1A. Requirement Traceability Card

File:
`skills/legal-compliance-procurement/requirement-traceability.md`

`skill.traceability_matrix_design` is retired and merged into `skill.requirement_traceability`.

The Card must no longer present matrix design as a distinct adjacent Skill or imply that the retired ID remains a separate capability.

Requirements:
- remove/update any prose that treats `skill.traceability_matrix_design` as a live distinct Skill;
- retain matrix design as a method/technique inside `skill.requirement_traceability` where appropriate;
- retain the Wave 3 migration note only as historical/deprecation context;
- do not remove the valid Knowledge & Evidence Steward mapping basis created by the merge;
- remove stale prose saying `role.project_development_lead` is added through bid/proposal transitive compatibility if that mapping was removed;
- ensure allowlist prose exactly matches current direct/transitive mapping basis.

### 1B. Master Skill Universe — retired affordability/tariff controls

File:
`skills/master-skill-universe.md`

The deprecation register correctly says:
- `specialisation.affordability` -> `skill.affordability_analysis`
- `specialisation.tariff_modelling` -> `skill.tariff_analysis`

But `# Duplication / Granularity Controls` still says these must remain distinct.

Remove those stale controls and replace them with current normalized guidance:
- affordability is a Skill/method, not a Specialisation;
- tariff analysis/modelling method is represented by the surviving Skill; do not recreate a tariff-modelling Specialisation unless a future bounded context distinct from the method is defined.

Also search all Phase 4 governing architecture files for stale examples that present tariff modelling or affordability as Specialisations.

At minimum review:
- `architecture/skill-registry-design.md`
- `skills/master-skill-universe.md`
- templates / standards / mapping rules

Where architecture examples still say `method / metric: ... tariff modelling, affordability`, update the conceptual examples so Specialisation examples are bounded contexts/metrics, not retired method-like pseudo-Specialisations.

Historical audit/deprecation prose MAY mention retired IDs when explicitly labelled retired/historical. Active instructions/examples may not.

## 2. Reconcile four Pack Cards with canonical mappings

The mapping records remain the sole authoritative source. Do NOT change valid mappings just to make prose true.

Fix stale contradictory advisory prose in these four Pack Cards:

### 2A. Project Finance Metrics
`skills/packs/methods/project-finance-metrics.md`

Current contradiction: after correctly admitting Funding & Bankability, Project Finance / Transaction and PPP / Concession, a later paragraph says those Roles are not mapped.

Correct the paragraph so it distinguishes:
- mapped Roles actually mapped to the Pack;
- substantively relevant but currently unmapped Roles, if any (for example IFI/DFI only if current canonical mapping confirms it is unmapped).

Do not change allowlist unless reverse-basis validation shows a real defect.

### 2B. CoVE
`skills/packs/programmes/cove.md`

Current contradiction: `role.learning_vet_design_specialist` is correctly admitted and mapped, but a later paragraph says it is not mapped/listed.

Correct advisory prose to current canonical state.

### 2C. LIFE
`skills/packs/programmes/life-programme.md`

Current contradiction: `role.eu_programme_implementation_grant_management_specialist` is correctly admitted and mapped, but a later paragraph says it is not mapped.

Correct advisory prose to current canonical state.

### 2D. Supabase
`skills/packs/technology/supabase.md`

Current contradiction: Full-Stack, Integration/API, Platform/DevOps and Database/Data Engineer are correctly admitted and mapped, but a later paragraph says none is mapped/listed.

Correct advisory prose to current canonical state.

Keep `role.security_engineer` explicitly absent unless canonical mappings changed (they should not in this cleanup).

For all four Pack Cards:
- relationship type and triggers remain only in mapping records;
- card prose may describe allowlist basis but must not contradict mappings;
- authority/boundary/source sections must remain unchanged except where a sentence itself is factually stale mapping-status prose.

## 3. Correct authoritative inventory counts

### 3A. Master Universe inventory

The independent audit recomputed:
- active Skills: 205
- active Specialisations: 41
- active Packs: 21
- total active universe entries: 267
- deprecated/tombstoned IDs: 23

Update any stale inventory statement, including the current `43 Specialisations`, to the actual counted value 41.

Do not hardcode counts without independently recomputing them from current declarations.

### 3B. Wave 3 statistical record

File:
`reviews/phase-4-wave-3-cross-domain-normalization.md`

The independent audit recomputed:
- Wave 1 entries: 147
- Wave 2 entries: 676
- combined entries: 823
- combined REQUIRED_CORE / RFC / OPTIONAL / ALTERNATIVE / PROHIBITED: 240 / 291 / 224 / 58 / 10
- unique used capability IDs: 264
  - Skills: 205
  - Specialisations: 38
  - Packs: 21
- REQUIRED_CORE per Role: min 2, max 8, average 4.07
- ALTERNATIVE sets: 11
- PROHIBITED: 10
- single-role positive-use IDs: 93 / 264 = 35.2%

Recompute independently from the actual mapping files before editing. If your recomputation differs, report the exact parser/method and reconcile against the mapping syntax rather than assuming the audit is wrong.

Known stale claims to correct if confirmed:
- 263 used IDs -> actual 264;
- 92 single-role IDs -> actual 93;
- `skill.use_case_modelling` omitted / incorrectly described as unused;
- 235 uncarded Skills is impossible against a 205-Skill universe.

Card coverage should be stated from actual current cards. The independent audit counted:
- 6 / 205 Skills carded;
- 1 / 41 Specialisations carded;
- 5 / 21 Packs carded;
- 12 total cards across 267 active capabilities.

Again: recompute, do not merely copy.

### 3C. Wave 2 stale prose counts

File:
`skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

Audit reported:
- Insurance core prose says 3, actual 2;
- QA core prose says 2, actual 3.

Locate these narrative/statistical claims and correct them to the actual relationship blocks.

Do not change mapping relationships merely to make prose match.

## 4. Recompute duplicate Pack/direct activation exhaustively

The Wave 3 review claimed an exhaustive Pack/direct normalization but recorded only a subset.

Independent audit found:
- required-component overlap paths: 20
- unique Role–Skill pairs: 14
- unique Skills: 10
- all required + optional Pack/direct overlap paths: 56

Build an independent exhaustive detector from actual Wave 1 + Wave 2 mapping blocks and current Pack component declarations.

Update `reviews/phase-4-wave-3-cross-domain-normalization.md` so it distinguishes clearly:
- required-component direct+Pack overlap paths;
- unique Role–Skill pairs;
- optional-component overlaps;
- intentionally retained cases and why direct mapping has independent meaning;
- cases resolved by stricter-obligation single activation.

Do not call a subset exhaustive.

If the actual recomputation differs from 20/14/10/56, explain exactly why and use the actual reproducible counts.

Do not remove valid direct mappings solely to lower overlap count. The purpose is evidence accuracy and governed duplicate activation, not cosmetic reduction.

## 5. Search globally for contradictions created by Wave 3

Run targeted repository searches on the Phase 4 branch for these retired IDs and stale claims:
- `skill.resource_planning`
- `skill.insurance_gap_analysis`
- `skill.traceability_matrix_design`
- `specialisation.affordability`
- `specialisation.tariff_modelling`
- phrases such as `none is mapped`, `not mapped`, `not listed`, where they appear inside the 5 card files touched by Wave 2/3 allowlist changes
- stale `43 Specialisations`
- stale `263`, `92`, `235 Skills`

Classify each hit:
- VALID HISTORICAL / DEPRECATION REFERENCE
- ACTIVE STALE REFERENCE — FIX

No active stale reference may remain.

Historical references are allowed only when unmistakably labelled retired/historical and do not instruct future activation.

## 6. Preserve compatibility and authority mechanics

After cleanup, re-run all current Phase 4 compatibility checks:
1. direct Role -> Skill
2. direct Role -> Specialisation (carded)
3. direct Role -> Pack
4. transitive Pack -> component Skill
5. reverse allowlist basis

Expected:
- 0 testable incompatibilities
- 0 orphan allowlist entries

Also confirm:
- Security Engineer remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase`;
- `skill.lifecycle_cost_analysis` remains support-only to `role.technical_feasibility_lead`;
- Phase 3 Role Cards unchanged;
- all Phase 4 artifacts remain PROPOSED;
- no later-phase implementation introduced.

## 7. Final cleanup record

Create:
`reviews/phase-4-final-audit-remediation.md`

Status:
`PROPOSED — READY FOR FINAL RE-AUDIT`

The record must contain:
- each blocker from the failed final audit;
- exact file(s) changed for that blocker;
- before/after statement;
- global stale-reference search result;
- recomputed statistics;
- exhaustive duplicate-activation statistics;
- compatibility results;
- remaining non-blocking notes only.

Do not claim human approval.

## Validation — all must PASS

1. 59 approved Roles still covered exactly once.
2. Phase 3 Role Cards unchanged.
3. 205 active Skills confirmed from declarations.
4. 41 active Specialisations confirmed from declarations.
5. 21 active Packs confirmed from declarations.
6. 23 deprecated/tombstoned IDs confirmed.
7. Zero retired IDs in active declarations.
8. Zero retired IDs in active mappings.
9. `skill.traceability_matrix_design` appears only in explicit retirement/history contexts.
10. `specialisation.affordability` appears only in explicit retirement/history contexts.
11. `specialisation.tariff_modelling` appears only in explicit retirement/history contexts.
12. No active instruction says tariff analysis vs tariff-modelling Specialisation must remain distinct.
13. No active instruction says affordability analysis vs affordability Specialisation must remain distinct.
14. Architecture examples no longer present retired method-like pseudo-Specialisations as live examples.
15. Project Finance Metrics Pack prose matches canonical mappings.
16. CoVE Pack prose matches canonical mappings.
17. LIFE Pack prose matches canonical mappings.
18. Supabase Pack prose matches canonical mappings.
19. Requirement Traceability Card prose matches current allowlist/mapping basis.
20. Zero direct Skill compatibility conflicts.
21. Zero direct Specialisation compatibility conflicts.
22. Zero direct Pack compatibility conflicts.
23. Zero transitive Pack-component compatibility conflicts.
24. Zero orphan allowlist entries.
25. Wave 1 / Wave 2 / combined mapping counts recomputed and recorded accurately.
26. Unique-used and single-role-use statistics recomputed and recorded accurately.
27. Card coverage counts recomputed and recorded accurately.
28. Duplicate Pack/direct activation evidence is exhaustive and reproducible.
29. Wave 2 Insurance/QA narrative core counts match actual blocks.
30. All Phase 4 artifacts remain PROPOSED and the cleanup record is self-contained for independent re-audit.

## Commit / Push

If all 30 checks PASS:

Commit exactly:
`docs: reconcile Phase 4 final audit findings`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. FINAL AUDIT REMEDIATION APPLIED
Files changed and blocker coverage.

### B. RETIRED TAXONOMY CLEANUP
Traceability / affordability / tariff results and global stale-reference scan.

### C. PACK CARD RECONCILIATION
Project Finance Metrics / CoVE / LIFE / Supabase before/after consistency.

### D. INVENTORY & STATISTICAL RECHECK
Actual recomputed current values.

### E. DUPLICATE ACTIVATION RECHECK
Required paths / unique Role-Skill pairs / optional paths / retained rationale.

### F. COMPATIBILITY & AUTHORITY
Five compatibility paths and preserved boundaries.

### G. VALIDATION
Checks 1–30 PASS / FAIL.

### H. REMAINING BLOCKERS
If none: NONE.

### I. REMAINING NON-BLOCKING NOTES
If none: NONE.

### J. COMMIT / PUSH
Commit SHA and push result.

### K. NEXT-STEP READINESS
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 4 RE-AUDIT
- NOT READY

Do not claim human approval or mass-generation readiness.