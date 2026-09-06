# Claude Code Prompt — Phase 4 Remediation After Wave 1 Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`

Apply the Phase 4 remediation required by the independent Wave 1 audit.

This is an APPLY task, not audit-only.

Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not mass-generate Skill Cards or Skill Packs.
Do not create new first-class Roles.
Do not create Review Profile Registry or Decision Rights Register.
Do not introduce model/runtime bindings or database/orchestration implementation.

## Read first

1. `prompts/phase-4-wave-1-skill-registry-audit.md`
2. the independent audit result supplied by the user
3. `architecture/skill-registry-design.md`
4. `architecture/role-to-skill-mapping-rules.md`
5. `skills/master-skill-universe.md`
6. `skills/_standards/common-skill-constraints.md`
7. `skills/_templates/skill-card-template.md`
8. `skills/_templates/skill-pack-template.md`
9. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
10. approved Phase 3 Role Cards for all 11 Wave 1 roles

## Required remediation

### 1. Fix HIGH B1 — Technical / Feasibility boundary

In `skills/mappings/wave-1-exemplar-role-skill-mapping.md`:
- REMOVE `skill.capex_estimation` from Technical / Feasibility Lead.
- REMOVE `skill.opex_estimation` from Technical / Feasibility Lead.
- CHANGE `skill.lifecycle_cost_analysis` from REQUIRED_CORE to REQUIRED_FOR_CONTEXT or OPTIONAL.
- Add explicit trigger/boundary that lifecycle-cost work uses specialist-owned cost inputs and supports technical option comparison only.
- Preserve CAPEX / Cost Engineering and Asset O&M ownership boundaries.

Do not change the approved Role Card.

### 2. Fix HIGH B2 — remove hidden-Role skill

In `skills/master-skill-universe.md`:
- REMOVE `skill.integrity_due_diligence`.
- Preserve narrower reusable capabilities such as counterparty screening, sanctions screening, source verification, evidence mapping, and risk analysis.
- Add explicit note that integrity due-diligence conclusions remain owned by `role.integrity_due_diligence_specialist`.

### 3. Fix HIGH B3 — one canonical source for relationship type/trigger

Architecture rule:
**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger.**

Update:
- `architecture/role-to-skill-mapping-rules.md`
- `skills/_standards/common-skill-constraints.md`
- `skills/_templates/skill-card-template.md`
- `skills/_templates/skill-pack-template.md`

Requirements:
- Skill / Specialisation / Pack cards may declare compatible-role allowlists, governed compatibility rules, and canonical mapping references.
- They must NOT independently declare REQUIRED_CORE / REQUIRED_FOR_CONTEXT / OPTIONAL / ALTERNATIVE / PROHIBITED_IN_CONTEXT as writable role relationships.
- If a card needs to explain typical use, make it clearly advisory/non-authoritative.

### 4. Resolve all six Wave 1 normalization candidates

Apply these exact decisions:

A. `skill.eligibility_analysis`
- MOVE INTO applicable EU programme packs.
- Remove standalone mapping/reference as a Skill ID.

B. `skill.work_package_logic_design`
- MOVE INTO applicable EU programme packs.
- Remove standalone mapping/reference as a Skill ID.

C. `skill.budget_logic_analysis`
- MOVE INTO applicable EU programme packs.
- Remove standalone mapping/reference as a Skill ID.

D. `skill.submission_requirement_mapping`
- MOVE INTO applicable programme/institution packs.
- Remove standalone mapping/reference as a Skill ID.

E. `skill.bid_proposal_management`
- REMOVE standalone Skill use.
- Use `skill_pack.bid_proposal_management` only.

F. `skill.security_constraint_allocation`
- REMOVE standalone candidate.
- Map need to `skill.quality_attribute_analysis`, supplemented by `skill.requirement_traceability` where relevant.

### 5. Apply REQUIRED_CORE corrections in Wave 1

Update `skills/mappings/wave-1-exemplar-role-skill-mapping.md` as follows.

#### Research / Market Intelligence
- `skill.benchmarking` -> OPTIONAL or REQUIRED_FOR_CONTEXT
- `skill.market_sizing` -> REQUIRED_FOR_CONTEXT with market-sizing trigger
- `skill.market_segmentation` -> REQUIRED_FOR_CONTEXT with market/segment trigger
- `skill.competitor_analysis` -> REQUIRED_FOR_CONTEXT with competition/market landscape trigger

#### EU Grants & Programmes
- remove the four standalone programme micro-skills listed above
- `skill.partner_mapping` -> REQUIRED_FOR_CONTEXT with consortium / partner formation trigger
- remove any standalone `skill.bid_proposal_management` usage; retain `skill_pack.bid_proposal_management` where applicable

#### Financial Modelling
- `skill.financial_statement_modelling` -> REQUIRED_FOR_CONTEXT
- `skill.capex_modelling` -> REQUIRED_FOR_CONTEXT
- `skill.opex_modelling` -> REQUIRED_FOR_CONTEXT
- `skill.working_capital_modelling` -> REQUIRED_FOR_CONTEXT
- avoid duplicate mandatory activation of `skill.project_finance_ratio_analysis` when `skill_pack.project_finance_metrics` is active; retain the standalone Skill only where it has independent non-pack meaning

#### Legal & Regulatory
- `skill.contract_review` -> REQUIRED_FOR_CONTEXT
- remove `skill.contract_clause_analysis` after normalization below
- `skill.licensing_requirement_analysis` -> REQUIRED_FOR_CONTEXT
- add explicit support-only boundaries for public procurement, State Aid, GDPR and other specialist domains so mapping cannot replace approved specialist Roles

#### Product Manager / Business Analyst
- make `skill.user_story_design` and `skill.use_case_modelling` ALTERNATIVE with a clear choice condition
- `skill.process_mapping` -> REQUIRED_FOR_CONTEXT

#### Solution Architect
- `skill.api_contract_design` -> REQUIRED_FOR_CONTEXT
- `skill.integration_pattern_selection` -> REQUIRED_FOR_CONTEXT
- replace `skill.security_constraint_allocation` with `skill.quality_attribute_analysis` plus `skill.requirement_traceability` where relevant

#### Data & Database Architect
- `skill.data_pipeline_design` -> REQUIRED_FOR_CONTEXT
- `skill.metric_definition` -> REQUIRED_FOR_CONTEXT

#### Knowledge & Evidence Steward
- `skill.evidence_indexing` -> REQUIRED_FOR_CONTEXT
- `skill.traceability_matrix_design` -> REQUIRED_FOR_CONTEXT

#### Sales / Business Development
- `skill.proposal_commercial_narrative` -> REQUIRED_FOR_CONTEXT
- `skill.partner_mapping` -> REQUIRED_FOR_CONTEXT

Project / Delivery Lead: no REQUIRED_CORE change.

### 6. Normalize duplicate and ambiguous IDs in Master Skill Universe

Apply these exact changes unless direct repository evidence shows a hard conflict, in which case STOP and report before changing:

- `skill.consortium_coordination` -> merge into `skill.partner_coordination`
- `skill.contract_clause_analysis` -> merge into `skill.contract_review`
- `skill.legal_source_currency_check` -> merge into `skill.source_verification`
- replace `specialisation.official_source_monitoring` with reusable `skill.source_monitoring`
- replace `specialisation.policy_source_monitoring` with `skill.source_monitoring` plus policy-source context trigger
- `skill.reporting_schedule_management` -> remove; use `skill.deliverable_planning` + `skill.milestone_management`
- `skill.version_control` -> rename to `skill.document_version_control`
- `skill.control_design` -> rename to `skill.risk_control_design`
- `skill.canonical_status_management_support` -> rename to `skill.knowledge_state_metadata_management`
- `skill.publication_readiness_check` -> rename to `skill.publication_requirements_validation`
- REMOVE `skill.technical_due_diligence_support`
- REMOVE `skill.integrity_due_diligence`

Propagate these changes to all Phase 4 files in the branch.
Do not rewrite historical Phase 3 audit/remediation prompts merely because old wording appears there.

### 7. Add missing reusable capability classes required before exemplar cards

Add these to `skills/master-skill-universe.md` in the appropriate families, keeping them as reusable techniques rather than hidden professional roles:

- `skill.source_monitoring`
- `skill.results_framework_design`
- `skill.indicator_design`
- `skill.monitoring_evaluation_design`
- `skill.learning_outcome_design`
- `skill.assessment_design`
- `skill.grant_cost_eligibility_analysis`
- `skill.grant_compliance_monitoring`
- `skill.portfolio_prioritisation_analysis`
- `skill.benefits_realisation_tracking`
- `skill.accounting_record_reconciliation`
- `skill.tax_position_analysis`
- `skill.insurance_programme_analysis`
- `skill.financing_term_analysis`
- `skill.threat_modelling`
- `skill.security_control_design`
- `skill.security_control_validation`
- `skill.security_testing`
- `skill.privacy_impact_analysis`
- `skill.lawful_basis_analysis`
- `skill.database_migration_planning`
- `skill.disclosure_access_matrix_design`
- `skill.disclosure_tracking`

Add support-only boundary language where a capability touches a distinct approved Role's methodology.

### 8. Clarify ambiguous boundaries

In `skills/master-skill-universe.md` add short boundary notes for:
- `skill.relationship_risk_analysis`: stakeholder relationship risk only; formal integrity/counterparty conclusions remain outside this Skill.
- `skill.quality_attribute_analysis`: selectable dimensions may include security, privacy, resilience, performance and availability, but this does not replace Security or Data Protection professional ownership.
- `skill_pack.ifi_financial_appraisal`: clarify that it is a generic method pack only if it does not duplicate institution-specific packs; otherwise reframe or remove duplication.
- `skill_pack.technical_writing_documentation`: clarify that the Pack adds governed templates/conventions and controlled documentation requirements beyond `skill.technical_writing`.

### 9. Add safe Specialisation representation

Update `skills/_templates/skill-card-template.md` to safely support Specialisations.

Preferred approach:
- `Type: SKILL | SPECIALISATION`
- add `Specialisation Class` when Type = SPECIALISATION
- add bounded-context fields such as sector/programme/institution/technology/metric/operating context
- add applicability boundary

Do not create a second competing authority model.

### 10. Add pack dependency model

Update `skills/_templates/skill-pack-template.md` and common constraints with:
- `Type: Skill Pack`
- contributing Skill Families
- Included Specialisations
- dependent/nested packs
- explicit dependency/layering metadata
- no circular pack dependencies
- precedence rule for overlapping packs
- duplicate-activation resolution when a Skill is both individually mapped and included in a Pack
- pack activation cannot satisfy licensing, competence, review-independence or human-authority requirements

Specific clarification:
- CoVE should state dependency/layering on applicable Erasmus+ rules where that dependency applies.

### 11. Clarify Skill Families

In `skills/master-skill-universe.md` add concise family-scope definitions matching the audit:

- Research & Evidence = source acquisition, verification, claim/evidence analysis
- Documentation / Knowledge / Disclosure = governed records, configuration, lineage, disclosure packaging
- Stakeholder & Institutional = institutional/stakeholder analysis
- Sales / Marketing / Customer = commercial acquisition, communication, customer lifecycle
- Commercial & Market = market/commercial analysis, not sales execution
- Product / UX / Content = product-facing information/content design
- Legal / Compliance / Procurement = legal obligations and regulated interpretation
- ESG / Risk / Integrity = risk methods and diligence inputs without approval authority
- Software / Integration / Platform: add explicit Security subfamily or rename to `Software / Integration / Platform / Security`
- Data / Analytics / AI = distinguish architecture/analytical techniques from platform implementation/security

Permit one primary family plus optional secondary-family tags.
Family assignment must never imply authority or exclusive Role compatibility.
Do NOT create an Assurance family.

### 12. Normalize proficiency vocabulary

Use one vocabulary everywhere in active Phase 4 architecture/templates:
- AWARENESS
- WORKING
- ADVANCED
- EXPERT

Replace `FOUNDATION` where it appears in active Phase 4 files.

### 13. Template / standard safety additions

Update common constraints and templates to require:
- mapping registry as sole relationship/trigger authority;
- duplicate effective activation detection;
- circular pack dependency prevention;
- overlapping-pack conflict handling;
- Skill may contribute to Role-owned knowledge-state work but cannot execute a knowledge-state transition;
- support-only boundary when touching another approved Role methodology;
- prerequisite capabilities;
- incompatibilities;
- alternative-choice-set references;
- primary + optional secondary families;
- quality-control/evaluation/validation/publication-readiness capabilities are NOT independent review;
- explicit Role-owned artifact/contribution boundary;
- supersedes / superseded-by metadata.

### 14. Correct Wave 1 reuse note

The audit found the Wave 1 document says `skill.source_verification` is mapped to four roles, but actual mapping contains three.
Correct the statement to match the actual post-remediation mappings.

### 15. Inventory estimate

Update the approximate inventory statement in `skills/master-skill-universe.md` so it does not claim “about 150” if the actual proposed Skill count materially differs after remediation.
Prefer a generated exact or approximate count based on the current file after changes.
Do not make count a target.

## Validation

After edits, run a repository-wide Phase 4 validation.

Required checks:

1. No active Phase 4 references to removed IDs:
- `skill.integrity_due_diligence`
- `skill.technical_due_diligence_support`
- `skill.consortium_coordination`
- `skill.contract_clause_analysis`
- `skill.legal_source_currency_check`
- `specialisation.official_source_monitoring`
- `specialisation.policy_source_monitoring`
- `skill.reporting_schedule_management`
- `skill.version_control`
- `skill.control_design`
- `skill.canonical_status_management_support`
- `skill.publication_readiness_check`
- `skill.eligibility_analysis`
- `skill.work_package_logic_design`
- `skill.budget_logic_analysis`
- `skill.submission_requirement_mapping`
- `skill.bid_proposal_management`
- `skill.security_constraint_allocation`

Historical audit/remediation prompts may retain these IDs as historical instructions and should be excluded from active-registry defect counts.

2. Wave 1 Technical / Feasibility mapping has zero CAPEX/OPEX estimation mappings.

3. Every REQUIRED_FOR_CONTEXT mapping in Wave 1 has an explicit trigger.

4. Every ALTERNATIVE mapping has an explicit choice condition.

5. No Skill / Pack template independently owns mapping relationship type or trigger.

6. One canonical mapping source rule is explicit in architecture + constraints + templates.

7. Pack cycle prevention and duplicate-activation handling are explicit.

8. All Phase 4 artifacts remain PROPOSED / working status, not APPROVED or CANONICAL.

9. No approved Phase 3 Role Cards are changed.

10. No Review Profile Registry or Decision Rights Register is created.

11. No model/runtime binding is introduced.

12. Re-run the seven stress-test scenarios conceptually and report PASS / PASS WITH NON-BLOCKING NOTE / FAIL.

13. Report current counts of unique:
- Skills
- Specialisations
- Skill Packs

14. Report any remaining one-off/micro-skill concerns, but do not automatically delete additional items beyond this prompt.

## Commit / Push

If all mandatory validation passes:

Commit exactly:
`docs: remediate Phase 4 skill registry after Wave 1 audit`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. CHANGES APPLIED
Files and substantive changes.

### B. HIGH FINDINGS
B1: RESOLVED / NOT RESOLVED
B2: RESOLVED / NOT RESOLVED
B3: RESOLVED / NOT RESOLVED

### C. NORMALIZATION
Old IDs -> disposition / target IDs, plus zero-active-reference validation.

### D. WAVE 1 MAPPING
List changed relationship classifications and trigger additions.

### E. TEMPLATE / PACK MODEL
Summarize canonical mapping-source rule, Specialisation representation, pack dependency/cycle/precedence handling, and proficiency normalization.

### F. VALIDATION
All mandatory checks, counts, and seven stress tests.

### G. COMMIT / PUSH
Commit SHA and push result.

### H. REMAINING NON-BLOCKING ITEMS
Only items not required by this remediation.

If any mandatory validation fails, do not claim completion. Fix it first or stop and report the blocker.