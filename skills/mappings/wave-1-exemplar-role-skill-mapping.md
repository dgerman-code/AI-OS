# Phase 4 — Wave 1 Exemplar Role-to-Skill Mapping

Status: PROPOSED — Phase 4 working baseline

## Purpose

Test the Role-to-Skill mapping architecture on 11 representative approved Roles before expanding to all 59.

This mapping does not change any Role Card. It only defines capability applicability.

Relationship types:
- REQUIRED_CORE
- REQUIRED_FOR_CONTEXT
- OPTIONAL
- ALTERNATIVE
- PROHIBITED_IN_CONTEXT

## 1. Project / Delivery Lead

Role: `role.project_delivery_lead`

### REQUIRED_CORE
- `skill.scope_definition`
- `skill.project_scheduling`
- `skill.milestone_management`
- `skill.dependency_mapping`
- `skill.raid_management`
- `skill.delivery_readiness_assessment`
- `skill.multidisciplinary_integration`
- `skill.action_tracking`

### REQUIRED_FOR_CONTEXT
- `specialisation.multi_partner_programme_delivery`
  - trigger: delivery package spans multiple formal consortium / programme partners
- `specialisation.infrastructure_project_preparation`
  - trigger: project preparation for infrastructure / utility / industrial investment
- `specialisation.eu_grant_delivery`
  - trigger: EU-funded programme delivery

### OPTIONAL
- `skill.work_breakdown_design`
- `skill.critical_path_analysis`
- `skill.stage_gate_design`
- `skill.deliverable_planning`

### Boundary
No Legal, Financial, Technical, ESG or specialist conclusion authority is granted by these mappings.

## 2. Research / Market Intelligence Analyst

Role: `role.research_market_intelligence_analyst`

### REQUIRED_CORE
- `skill.source_discovery`
- `skill.source_verification`
- `skill.fact_extraction`
- `skill.source_comparison`
- `skill.research_synthesis`
- `skill.benchmarking`
- `skill.market_sizing`
- `skill.market_segmentation`
- `skill.competitor_analysis`

### REQUIRED_FOR_CONTEXT
- `skill_pack.labour_market_skills_intelligence`
  - trigger: labour-market, workforce or skills intelligence assignment
- `specialisation.official_source_monitoring`
  - trigger: monitoring based on official institutional sources
- `specialisation.policy_source_monitoring`
  - trigger: policy / regulatory / institutional change monitoring

### OPTIONAL
- `skill.change_detection`
- `skill.survey_research_design`
- `skill.interview_research_design`
- `skill.customer_discovery`

### Boundary
Does not become the substantive owner of Legal, Policy or Financial professional conclusions merely because it researches those domains.

## 3. EU Grants & Programmes Specialist

Role: `role.eu_grants_programmes_specialist`

### REQUIRED_CORE
- `skill.source_verification`
- `skill.requirement_traceability`
- `skill.eligibility_analysis`
- `skill.work_package_logic_design`
- `skill.partner_mapping`
- `skill.budget_logic_analysis`
- `skill.submission_requirement_mapping`

### REQUIRED_FOR_CONTEXT
- `skill_pack.erasmus_plus`
  - trigger: programme = Erasmus+
- `skill_pack.cove`
  - trigger: action / programme context = CoVE
- `skill_pack.life_programme`
  - trigger: programme = LIFE
- `skill_pack.horizon_europe`
  - trigger: programme = Horizon Europe

### OPTIONAL
- `skill.bid_proposal_management`
- `skill.consultation_design`
- `skill.reporting_schedule_management`

### Boundary
Programme pack activation does not grant consortium governance, legal-signature, budget-approval or submission authority.

## 4. Technical / Feasibility Lead

Role: `role.technical_feasibility_lead`

### REQUIRED_CORE
- `skill.technical_requirements_definition`
- `skill.feasibility_analysis`
- `skill.technical_option_comparison`
- `skill.design_basis_definition`
- `skill.technical_risk_analysis`
- `skill.lifecycle_cost_analysis`

### REQUIRED_FOR_CONTEXT
- one or more sector specialisations:
  - `specialisation.solar`
  - `specialisation.bess`
  - `specialisation.water`
  - `specialisation.waste`
  - `specialisation.transport`
  - `specialisation.industrial`
  - `specialisation.health`
  - `specialisation.real_estate`
  - trigger: assignment sector / technology matches
- `specialisation.infrastructure_project_preparation`
  - trigger: infrastructure or industrial investment project

### OPTIONAL
- `skill.capacity_sizing`
- `skill.capex_estimation`
- `skill.opex_estimation`
- `skill.technical_due_diligence_support`

### Boundary
Sector specialisation refines technical competence but does not transfer Sector Technical Expert ownership where a distinct sector expert is required.

## 5. Financial Modelling Specialist

Role: `role.financial_modelling_specialist`

### REQUIRED_CORE
- `skill.financial_model_design`
- `skill.financial_statement_modelling`
- `skill.cash_flow_modelling`
- `skill.capex_modelling`
- `skill.opex_modelling`
- `skill.working_capital_modelling`
- `skill.sensitivity_analysis`
- `skill.assumption_analysis`

### REQUIRED_FOR_CONTEXT
- `skill_pack.project_finance_metrics`
  - trigger: project-finance structure OR lender-facing debt model
- `skill.debt_schedule_modelling`
  - trigger: financing includes debt
- `skill.financing_scenario_analysis`
  - trigger: multiple financing structures / capital-stack options

### OPTIONAL
- `skill.discounted_cash_flow_analysis`
- `skill.project_finance_ratio_analysis`
- `skill.financial_evidence_reconciliation`

### Boundary
Does not obtain CAPEX, demand, tax, legal or financing-transaction ownership by consuming inputs from those domains.

## 6. Legal & Regulatory Lead

Role: `role.legal_regulatory_lead`

### REQUIRED_CORE
- `skill.legal_issue_spotting`
- `skill.regulatory_mapping`
- `skill.contract_review`
- `skill.contract_clause_analysis`
- `skill.legal_source_currency_check`
- `skill.jurisdiction_mapping`
- `skill.obligation_mapping`
- `skill.licensing_requirement_analysis`

### REQUIRED_FOR_CONTEXT
- `specialisation.public_procurement`
  - trigger: procurement-law / public-contract context
- `specialisation.state_aid`
  - trigger: State Aid relevance
- `specialisation.gdpr`
  - trigger: personal-data / privacy legal issue
- `specialisation.cross_border_regulatory`
  - trigger: multi-jurisdiction or cross-border legal perimeter

### OPTIONAL
- `skill.requirement_traceability`
- `skill.compliance_gap_analysis`

### Boundary
Specialisation does not replace jurisdiction-specific licensed human legal authority where required.

## 7. Product Manager / Business Analyst

Role: `role.product_manager_business_analyst`

### REQUIRED_CORE
- `skill.requirements_elicitation`
- `skill.user_story_design`
- `skill.use_case_modelling`
- `skill.acceptance_criteria_design`
- `skill.process_mapping`
- `skill.problem_structuring`
- `skill.decision_criteria_design`

### REQUIRED_FOR_CONTEXT
- `specialisation.institutional_website`
  - trigger: institutional/public website product
- `specialisation.admin_console`
  - trigger: internal/admin operational interface
- `specialisation.multilingual_content`
  - trigger: multilingual product requirements

### OPTIONAL
- `skill.customer_journey_mapping`
- `skill.metric_definition`
- `skill.user_flow_design`

### Boundary
Technology packs may inform requirements but do not grant architecture, engineering, security or deployment authority.

## 8. Solution Architect

Role: `role.solution_architect`

### REQUIRED_CORE
- `skill.solution_decomposition`
- `skill.architecture_decision_recording`
- `skill.quality_attribute_analysis`
- `skill.api_contract_design`
- `skill.integration_pattern_selection`
- `skill.technical_option_comparison`

### REQUIRED_FOR_CONTEXT
- `skill_pack.supabase`
  - trigger: Supabase is part of selected / constrained platform context
- `skill_pack.postgresql`
  - trigger: PostgreSQL is part of selected / constrained data platform
- `skill_pack.vercel`
  - trigger: Vercel is part of selected / constrained deployment platform

### OPTIONAL
- `skill.observability_design`
- `skill.performance_testing`
- `skill.security_constraint_allocation`

### Boundary
Technology Pack activation provides platform-specific constraints; it does not authorize vendor commitment, production change or implementation ownership.

## 9. Data & Database Architect

Role: `role.data_database_architect`

### REQUIRED_CORE
- `skill.data_model_design`
- `skill.schema_design`
- `skill.data_quality_rule_design`
- `skill.data_pipeline_design`
- `skill.metric_definition`
- `skill.requirement_traceability`

### REQUIRED_FOR_CONTEXT
- `skill_pack.postgresql`
  - trigger: selected relational database = PostgreSQL
- `skill_pack.supabase`
  - trigger: Supabase database / auth / storage context materially constrains data architecture
- `specialisation.relational_data_platform`
  - trigger: relational data platform architecture

### OPTIONAL
- `skill.sql_analysis`
- `skill.data_transformation`
- `skill.traceability_matrix_design`

### Boundary
Does not obtain Database / Data Engineer implementation ownership or production migration authority through these mappings.

## 10. Knowledge & Evidence Steward

Role: `role.knowledge_evidence_steward`

### REQUIRED_CORE
- `skill.source_verification`
- `skill.evidence_mapping`
- `skill.evidence_gap_analysis`
- `skill.evidence_indexing`
- `skill.version_control`
- `skill.document_configuration_control`
- `skill.traceability_matrix_design`

### REQUIRED_FOR_CONTEXT
- `skill_pack.version_control_document_configuration`
  - trigger: governed multi-version document / evidence environment
- `specialisation.official_source_monitoring`
  - trigger: canonical knowledge depends on recurring official-source updates

### OPTIONAL
- `skill.change_detection`
- `skill.document_gap_analysis`
- `skill.technical_writing`

### Boundary
Evidence governance does not make this Role the professional author or independent reviewer of the substantive conclusions being governed.

## 11. Sales / Business Development Specialist

Role: `role.sales_business_development_specialist`

### REQUIRED_CORE
- `skill.lead_qualification`
- `skill.account_mapping`
- `skill.opportunity_qualification`
- `skill.value_proposition_design`
- `skill.sales_pipeline_analysis`
- `skill.proposal_commercial_narrative`
- `skill.partner_mapping`

### REQUIRED_FOR_CONTEXT
- `specialisation.b2b_sales`
  - trigger: B2B sales assignment
- `specialisation.institutional_business_development`
  - trigger: institutional / public-sector / association business development
- `specialisation.partner_led_growth`
  - trigger: channel / partner-led commercial motion
- `skill_pack.bid_proposal_management`
  - trigger: formal competitive bid / proposal process

### OPTIONAL
- `skill.market_segmentation`
- `skill.competitor_analysis`
- `skill.claim_substantiation`
- `skill.customer_journey_mapping`

### Boundary
Does not gain Legal, Pricing Approval, Contract Commitment or external institutional-position authority through commercial skills.

# Cross-Exemplar Reuse Check

High-reuse capabilities in Wave 1:
- `skill.source_verification` — Research, EU Grants, Legal, Knowledge & Evidence;
- `skill.requirement_traceability` — EU Grants, Legal, Data & Database Architect;
- `skill.partner_mapping` — EU Grants, Sales / BD;
- `skill.sensitivity_analysis` — Financial Modelling and potentially Strategy / Risk in later waves;
- technology packs — Solution Architect and Data & Database Architect where context requires;
- sector specialisations — Technical / Feasibility Lead and later Sector Technical Expert / Project Development roles.

This reuse is intentional and should reduce duplicate role-specific skill creation.

# Wave 1 Stress Test Matrix

## A. €50m+ BESS infrastructure project
Expected activation includes:
- Project / Delivery Lead + infrastructure project-preparation specialisation;
- Technical / Feasibility Lead + `specialisation.bess`;
- Financial Modelling + `skill_pack.project_finance_metrics`;
- Legal / Regulatory + jurisdiction / procurement / State Aid packs as applicable;
- additional Phase 3 Roles not in Wave 1 remain required where their professional ownership is triggered.

Result expectation: PASS if no role authority is widened.

## B. €7m municipal / IFI project with ESG and procurement complexity
Expected activation is driven by public / IFI / procurement / ESG context, not monetary threshold alone.

Wave 1 proves that smaller projects can activate contextual packs without new Role identities.

## C. Erasmus+ / CoVE programme
Expected activation:
- EU Grants + appropriate programme pack;
- Project / Delivery Lead + multi-partner / EU grant delivery specialisation where assigned;
- Research + labour-market skills intelligence when skills evidence is required.

## D. LIFE project-preparation proposal
Expected activation:
- EU Grants + `skill_pack.life_programme`;
- Project / Delivery Lead + EU grant delivery;
- Technical / Feasibility and Financial Modelling capabilities according to project content.

## E. Commercial e-commerce business
Expected activation:
- Sales / BD + B2B / partner-led packs as relevant;
- Product / BA;
- Solution Architect / Data Architect technology packs only when stack context is selected.

## F. Institutional website + Supabase/PostgreSQL
Expected activation:
- Product / BA + institutional website / admin console;
- Solution Architect + Supabase / PostgreSQL / Vercel as applicable;
- Data Architect + PostgreSQL / Supabase.

Technology packs remain context-specific and do not become hidden engineering Roles.

## G. Policy / intelligence platform with evidence lineage
Expected activation:
- Research + official / policy monitoring;
- Knowledge & Evidence Steward + version / evidence governance;
- Data Architect and Solution Architect where digital platform scope applies.

# Wave 1 Findings

1. The mapping model works without changing Role identity.
2. REQUIRED_FOR_CONTEXT is essential for programme, sector and technology packs.
3. Skill reuse across Roles is viable and preferable to Role-specific duplicate skills.
4. Authority leakage can be avoided if every mapping is checked against Role Card ownership.
5. The current Master Skill Universe is broad enough for Wave 1, but several referenced candidate skills need formal normalization before mass Skill Card generation.

# Normalization Candidates Identified by Wave 1

The following identifiers are conceptually useful but need confirmation against the Master Skill Universe before becoming canonical:
- `skill.eligibility_analysis`
- `skill.work_package_logic_design`
- `skill.budget_logic_analysis`
- `skill.submission_requirement_mapping`
- `skill.bid_proposal_management`
- `skill.security_constraint_allocation`

Some may be better represented as existing Skills or as components of Skill Packs rather than new standalone Skills.

Do not mass-generate Skill Cards until these normalization candidates and the Wave 1 mapping have been independently audited.

All mappings remain PROPOSED.