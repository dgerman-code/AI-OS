# Phase 4 — Wave 1 Exemplar Role-to-Skill Mapping

Status: PROPOSED — Phase 4 working baseline

## Purpose

Test the Role-to-Skill mapping architecture on 11 representative approved Roles before expanding to all 59.

This mapping does not change any Role Card. It only defines capability applicability.

**This document is the canonical mapping source for the Roles it covers.** Relationship type and context trigger are written here and nowhere else. Skill, Specialisation and Pack Cards may declare compatible-Role allowlists and reference these records, but may not declare a relationship type or define a trigger.

Relationship types:
- REQUIRED_CORE — intrinsic to the Role across substantially all assignments
- REQUIRED_FOR_CONTEXT — mandatory when the stated trigger is true; a trigger is required
- OPTIONAL — may improve execution; never a catch-all for weakly related capability
- ALTERNATIVE — one of a choice set; a choice condition is required
- PROHIBITED_IN_CONTEXT — must not be activated in the stated context; a rationale is required

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

### REQUIRED_FOR_CONTEXT
- `skill.market_sizing`
  - trigger: assignment requires sizing a market, addressable demand or population
- `skill.market_segmentation`
  - trigger: assignment requires segmenting a market, customer base or beneficiary population
- `skill.competitor_analysis`
  - trigger: assignment covers competition, competitive positioning or market landscape
- `skill.source_monitoring`
  - trigger: recurring monitoring of a defined source set; source class (official / institutional / policy / regulatory / market) is stated on the assignment
- `skill_pack.labour_market_skills_intelligence`
  - trigger: labour-market, workforce or skills intelligence assignment

### OPTIONAL
- `skill.benchmarking`
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

### REQUIRED_FOR_CONTEXT
- `skill.partner_mapping`
  - trigger: assignment involves consortium or partner formation, partner search or partnership composition
- `skill_pack.erasmus_plus`
  - trigger: programme = Erasmus+
- `skill_pack.cove`
  - trigger: action / programme context = CoVE
- `skill_pack.life_programme`
  - trigger: programme = LIFE
- `skill_pack.horizon_europe`
  - trigger: programme = Horizon Europe
- `skill_pack.bid_proposal_management`
  - trigger: formal competitive bid / proposal process with a governed submission cycle

### OPTIONAL
- `skill.consultation_design`
- `skill.deliverable_planning`
- `skill.milestone_management`

### Programme capability note
Eligibility interpretation, work-package logic, budget logic and submission requirement mapping are **not** mapped as standalone Skills. They are pack-internal components of the applicable programme Pack, because they are meaningless outside a specific programme rulebook and current call version and must inherit that Pack's currency rules. Reporting cadence is covered by `skill.deliverable_planning` plus `skill.milestone_management` rather than a separate scheduling Skill.

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
- `skill.lifecycle_cost_analysis`
  - choice / use condition: available only to support technical option comparison, using cost inputs owned and supplied by the cost and O&M specialists

### Cost boundary
This Role has **no CAPEX or OPEX estimation mapping**. Cost estimation is owned elsewhere and is not obtainable through this Role's skill set:
- CAPEX estimation, cost breakdown and contingency remain owned by `role.capex_cost_engineering_specialist`;
- operating and maintenance cost basis, availability and maintenance regime remain owned by `role.asset_om_technical_operations_specialist`.

`skill.lifecycle_cost_analysis` is mapped as OPTIONAL and support-only. It may be used **only** to compare technical options on a whole-life basis, and **only** on cost inputs already produced by the owning specialist Roles. It does not permit this Role to originate a CAPEX or OPEX estimate, to issue a cost conclusion, or to satisfy `decision.cost_estimate_acceptance`. Where no specialist-owned cost input exists, the option comparison must be reported as cost-unquantified rather than completed on self-generated cost figures.

### Boundary
Sector specialisation refines technical competence but does not transfer Sector Technical Expert ownership where a distinct sector expert is required.

## 5. Financial Modelling Specialist

Role: `role.financial_modelling_specialist`

### REQUIRED_CORE
- `skill.financial_model_design`
- `skill.cash_flow_modelling`
- `skill.sensitivity_analysis`
- `skill.assumption_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.financial_statement_modelling`
  - trigger: model must produce or reconcile to three-statement outputs
- `skill.capex_modelling`
  - trigger: model carries a capital expenditure profile
- `skill.opex_modelling`
  - trigger: model carries an operating cost profile
- `skill.working_capital_modelling`
  - trigger: working-capital movements are material to the cash flow or covenant test
- `skill.debt_schedule_modelling`
  - trigger: financing includes debt
- `skill.financing_scenario_analysis`
  - trigger: multiple financing structures / capital-stack options
- `skill_pack.project_finance_metrics`
  - trigger: project-finance structure OR lender-facing debt model

### OPTIONAL
- `skill.discounted_cash_flow_analysis`
- `skill.financial_evidence_reconciliation`

### Duplicate-activation note
`skill.project_finance_ratio_analysis` is **not** mapped separately here. It is a required component of `skill_pack.project_finance_metrics`, and mapping it individually as well would create a duplicate effective activation of the same capability. It is retained in the Master Skill Universe as a standalone Skill only for Roles that need ratio analysis without the full metrics Pack; where the Pack is active, the Pack governs.

The modelling Skills above are contextual rather than core because a valid financial model does not always carry a capital profile, an operating profile, working-capital movements or three-statement output. Making them REQUIRED_CORE would force activation of capabilities that some assignments genuinely do not need.

### Boundary
Does not obtain CAPEX, demand, tax, legal or financing-transaction ownership by consuming inputs from those domains. Cost and demand inputs are consumed at the knowledge state supplied by their owning Roles and are never originated here.

## 6. Legal & Regulatory Lead

Role: `role.legal_regulatory_lead`

### REQUIRED_CORE
- `skill.legal_issue_spotting`
- `skill.regulatory_mapping`
- `skill.jurisdiction_mapping`
- `skill.obligation_mapping`
- `skill.source_verification`

### REQUIRED_FOR_CONTEXT
- `skill.contract_review`
  - trigger: assignment includes a contract, agreement or binding instrument to review (includes clause-level analysis)
- `skill.licensing_requirement_analysis`
  - trigger: activity is licensed, authorised or otherwise subject to a permission regime
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

### Specialist-domain support boundary
Activating a domain Specialisation here provides legal interpretation capability only. It does **not** replace the approved specialist Role that owns the domain conclusion, and this Role's mapping cannot substitute for their involvement:
- public procurement and State Aid conclusions remain owned by `role.procurement_state_aid_specialist`;
- personal-data conclusions, DPIA acceptance and lawful-basis adoption remain owned by `role.data_protection_gdpr_specialist`;
- ESG / E&S conclusions remain owned by `role.esg_es_specialist`;
- tax positions remain owned by `role.tax_specialist`.

Where both this Role and the specialist Role are engaged, this Role's output is a legal-perimeter input, not the domain conclusion. Legal source currency is covered by `skill.source_verification` with a legal-source trigger.

### Boundary
Specialisation does not replace jurisdiction-specific licensed human legal authority where required.

## 7. Product Manager / Business Analyst

Role: `role.product_manager_business_analyst`

### REQUIRED_CORE
- `skill.requirements_elicitation`
- `skill.acceptance_criteria_design`
- `skill.problem_structuring`
- `skill.decision_criteria_design`

### ALTERNATIVE
- `skill.user_story_design` OR `skill.use_case_modelling`
  - choice condition: use `skill.user_story_design` for incremental, iteratively delivered product work where value is expressed per increment; use `skill.use_case_modelling` where the requirement is transaction- or process-centric, actor and precondition structure is material, or the requirement must be traceable to a regulated or contractual specification. Exactly one is required per requirement set; both may be used only where a governed rationale records why.

### REQUIRED_FOR_CONTEXT
- `skill.process_mapping`
  - trigger: assignment covers an existing or target business process, or a process change is in scope
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
- `skill.technical_option_comparison`

### REQUIRED_FOR_CONTEXT
- `skill.api_contract_design`
  - trigger: solution exposes or consumes an interface contract
- `skill.integration_pattern_selection`
  - trigger: solution integrates two or more systems or services
- `skill.requirement_traceability`
  - trigger: quality attributes, including security and privacy constraints, must be traced to their originating requirement or obligation
- `skill_pack.supabase`
  - trigger: Supabase is part of selected / constrained platform context
- `skill_pack.postgresql`
  - trigger: PostgreSQL is part of selected / constrained data platform
- `skill_pack.vercel`
  - trigger: Vercel is part of selected / constrained deployment platform

### OPTIONAL
- `skill.observability_design`
- `skill.performance_testing`

### Security capability note
There is no `skill.security_constraint_allocation` mapping. Allocating security constraints across a solution is covered by `skill.quality_attribute_analysis` with the security dimension selected, supplemented by `skill.requirement_traceability` where constraints must be traced to their originating obligation. A separate allocation Skill would have read as an architecture-owned security capability and blurred the boundary with `role.security_engineer`.

Selecting the security dimension does not transfer security ownership: threat modelling, control design and control validation remain owned by `role.security_engineer`, and personal-data conclusions remain owned by `role.data_protection_gdpr_specialist`.

### Boundary
Technology Pack activation provides platform-specific constraints; it does not authorize vendor commitment, production change or implementation ownership.

## 9. Data & Database Architect

Role: `role.data_database_architect`

### REQUIRED_CORE
- `skill.data_model_design`
- `skill.schema_design`
- `skill.data_quality_rule_design`
- `skill.requirement_traceability`

### REQUIRED_FOR_CONTEXT
- `skill.data_pipeline_design`
  - trigger: architecture includes ingestion, movement or transformation of data between systems or stores
- `skill.metric_definition`
  - trigger: architecture must support governed analytical metrics or reporting definitions
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
- `skill.document_version_control`
- `skill.document_configuration_control`
- `skill.knowledge_state_metadata_management`

### REQUIRED_FOR_CONTEXT
- `skill.evidence_indexing`
  - trigger: evidence corpus must be indexed for retrieval, disclosure or audit
- `skill.traceability_matrix_design`
  - trigger: claims, requirements or obligations must be traced to evidence in a governed matrix
- `skill_pack.version_control_document_configuration`
  - trigger: governed multi-version document / evidence environment
- `skill.source_monitoring`
  - trigger: canonical knowledge depends on recurring updates to a defined official-source set

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

### REQUIRED_FOR_CONTEXT
- `skill.proposal_commercial_narrative`
  - trigger: assignment requires a written proposal, offer or bid narrative
- `skill.partner_mapping`
  - trigger: commercial motion depends on partners, channel or consortium composition
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

Counted from the post-remediation mappings in this document. The previous version of this section claimed `skill.source_verification` was mapped to four Roles while the mapping then contained three; the figures below are derived from the mappings as they now stand.

Capabilities mapped to more than one Wave 1 Role:
- `skill.source_verification` — 4 Roles: Research / Market Intelligence, EU Grants & Programmes, Legal & Regulatory, Knowledge & Evidence Steward. It reaches four only after remediation, because the former `skill.legal_source_currency_check` merged into it and Legal & Regulatory now maps it directly with a legal-source trigger.
- `skill.requirement_traceability` — 4 Roles: EU Grants & Programmes, Legal & Regulatory, Solution Architect, Data & Database Architect. Solution Architect is new in this remediation, replacing the removed `skill.security_constraint_allocation`.
- `skill.partner_mapping` — 2 Roles: EU Grants & Programmes, Sales / Business Development.
- `skill.source_monitoring` — 2 Roles: Research / Market Intelligence, Knowledge & Evidence Steward. This is the reusable replacement for the two removed monitoring Specialisations, and its arrival is itself evidence that the Specialisations were mis-classified.
- `skill.technical_option_comparison` — 2 Roles: Technical / Feasibility Lead, Solution Architect.
- `skill.metric_definition` — 2 Roles: Product Manager / BA, Data & Database Architect.
- `skill.market_segmentation` and `skill.competitor_analysis` — 2 Roles each: Research / Market Intelligence, Sales / Business Development.
- `skill.deliverable_planning` and `skill.milestone_management` — 2 Roles each: Project / Delivery Lead, EU Grants & Programmes; together they replace the removed `skill.reporting_schedule_management`.
- `skill.traceability_matrix_design`, `skill.change_detection`, `skill.customer_journey_mapping` — 2 Roles each.
- `skill_pack.bid_proposal_management` — 2 Roles: EU Grants & Programmes, Sales / Business Development, now that the standalone Skill form is removed.
- `skill_pack.supabase` and `skill_pack.postgresql` — 2 Roles each: Solution Architect, Data & Database Architect.
- sector specialisations — Technical / Feasibility Lead, and later Sector Technical Expert / Project Development Roles outside Wave 1.

`skill.sensitivity_analysis` is mapped to one Wave 1 Role only (Financial Modelling). Its expected reuse in Strategy, Commercial & Demand, Economic / CBA and Risk is a Wave 2 expectation, not a demonstrated Wave 1 result, and is stated as such rather than counted here.

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
5. The current Master Skill Universe is broad enough for Wave 1. The six candidate skills it referenced have now been normalized, and the reusable capability classes the exemplar mappings needed have been added.
6. REQUIRED_CORE was over-used in the first pass. A capability belongs in REQUIRED_CORE only when it is intrinsic to the Role across substantially all assignments; where a competent assignment can proceed without it, it is REQUIRED_FOR_CONTEXT with an explicit trigger. This remediation moved 24 REQUIRED_CORE entries to a weaker relationship on that test (20 to REQUIRED_FOR_CONTEXT, 2 to OPTIONAL, 2 into a single ALTERNATIVE choice set) and removed 4 outright as pack-internal programme components. REQUIRED_CORE across Wave 1 fell from 79 entries to 52.
7. Two boundary defects were found by mapping rather than by reading Role Cards: cost estimation reachable through the Technical / Feasibility Lead skill set, and a whole professional methodology (`skill.integrity_due_diligence`) represented as a single Skill. Mapping is therefore a useful boundary test in its own right and should stay adversarial in Wave 2.

# Normalization Candidates — Resolved

All six Wave 1 normalization candidates have been resolved. None becomes a standalone Skill ID.

| Candidate | Disposition |
|---|---|
| `skill.eligibility_analysis` | Moved into the applicable EU programme Packs as a pack-internal component. Meaningless outside a specific programme rulebook and call version. |
| `skill.work_package_logic_design` | Moved into the applicable EU programme Packs as a pack-internal component. |
| `skill.budget_logic_analysis` | Moved into the applicable EU programme Packs as a pack-internal component. |
| `skill.submission_requirement_mapping` | Moved into the applicable programme and institution Packs as a pack-internal component; requirements are institution-specific and version-sensitive. |
| `skill.bid_proposal_management` | Removed as a standalone Skill. Represented only as `skill_pack.bid_proposal_management`. |
| `skill.security_constraint_allocation` | Removed. Covered by `skill.quality_attribute_analysis` with the security dimension selected, supplemented by `skill.requirement_traceability` where constraints must trace to their originating obligation. |

None of these identifiers may be reintroduced as a `skill.<id>` without new evidence of reuse independent of its Pack.

Skill Cards are still not mass-generated. Wave 2 mapping and exemplar Skill Cards remain the next step.

All mappings remain PROPOSED.