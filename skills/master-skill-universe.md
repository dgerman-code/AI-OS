# Master Skill Universe v0.1

Status: PROPOSED — Phase 4 working baseline

## Purpose

This document defines the first controlled universe of reusable Skills, Specialisations and Skill Packs for AI-OS Phase 4.

It is downstream from the approved Phase 3 Role Registry and must not create new first-class professional roles, review roles, human authority, workflows or model bindings.

The governing rule is:

**ROLE != SKILL != SPECIALISATION != SKILL PACK != MODEL**

The Role Registry remains authoritative for professional methodology ownership, professional scope, decision boundaries and recurring professional artifacts.

## Classification Types

### SKILL
A reusable capability or technique that may be shared across roles.

### SPECIALISATION
A bounded context extension such as sector, programme, institution, technology, jurisdiction, metric or operating environment.

### SKILL PACK
A versioned bundle of skills, specialisations, methods, controlled references and assignment constraints activated together.

## Granularity Rule

A capability should not become a separate registry item merely because it is a verb, a tool action or a sub-step.

Create a distinct Skill only when it is:
- reusable across assignments;
- professionally meaningful as a named capability;
- independently selectable or assessable;
- not merely a micro-step of another skill.

Prefer a Skill Pack when several capabilities are normally activated together because of a programme, institution, technology, sector or methodology.

## Specialisation Classification Semantics

A Specialisation bounds a **context**; it never names a **method**. The test is whether the identifier answers *where or under what rules the work applies* rather than *what the practitioner does*. An entry that answers the second question is a Skill wearing the wrong namespace, and Wave 3 retired two such entries.

Classes and what each bounds:

| Class | Bounds |
|---|---|
| `SECTOR` | an asset class or industry whose benchmarks, norms and failure modes do not transfer |
| `JURISDICTION` | a legal or regulatory perimeter |
| `INSTITUTION` | a named institution's policy framework |
| `PROGRAMME` | a funding programme's rulebook |
| `TECHNOLOGY` | a specific platform or product surface whose constraints bind the work |
| `METRIC` | a governed metric definition and its calculation conventions |
| `OPERATING_CONTEXT` | an operating environment, counterparty type or delivery mode |

`specialisation.admin_console` and `specialisation.institutional_website` are classified **OPERATING_CONTEXT**, not TECHNOLOGY. They describe the kind of product and its audience — an internal operational interface, a public institutional site — and bind no platform or version. Reserving TECHNOLOGY for entries that actually bind a platform keeps the class meaningful; `specialisation.relational_data_platform` is the genuine TECHNOLOGY case in this family.

Classification carries no authority in any class. It is a selection and duplication-control device only.

## Family Assignment Rule

Each Skill declares **one primary Skill Family** and may carry **optional secondary-family tags** where a capability genuinely reads across families.

Family assignment is a navigation and duplication-control device only. It must never imply authority, exclusive Role compatibility, or a professional ownership boundary. Role compatibility is governed by the mapping registry, not by family membership.

There is deliberately **no Assurance family**. Independent review is a Review Profile, not a Skill Family; grouping validation-flavoured Skills under an assurance label would invite exactly the confusion between technique and independent assurance that the registry separation exists to prevent.

## 1. Research & Evidence

Family scope: source acquisition, verification, and claim / evidence analysis.

### Skills
- `skill.source_discovery` — finding relevant primary and secondary sources.
- `skill.source_verification` — validating provenance, authority, version and effective date.
- `skill.fact_extraction` — extracting verifiable facts from source material.
- `skill.evidence_mapping` — linking claims, requirements and conclusions to evidence.
- `skill.evidence_gap_analysis` — identifying missing, weak or conflicting evidence.
- `skill.source_comparison` — comparing multiple authoritative or competing sources.
- `skill.change_detection` — detecting material changes across versions or time.
- `skill.research_synthesis` — synthesising evidence without erasing uncertainty or provenance.
- `skill.interview_research_design` — designing structured expert / stakeholder research inputs.
- `skill.survey_research_design` — designing structured surveys and questionnaires.
- `skill.source_monitoring` — recurring monitoring of a defined source set for material change. Replaces the former `specialisation.official_source_monitoring` and `specialisation.policy_source_monitoring`; the source class (official / institutional / policy / regulatory / market) is a context trigger on the mapping record, not a separate registry item.

### Specialisations / Packs
- `skill_pack.labour_market_skills_intelligence`

## 2. Strategy & Analysis

Family scope: structured problem framing, option and scenario analysis, and strategic prioritisation.

### Skills
- `skill.problem_structuring`
- `skill.option_analysis`
- `skill.scenario_analysis`
- `skill.sensitivity_analysis`
- `skill.assumption_analysis`
- `skill.business_case_structuring`
- `skill.strategic_prioritisation`
- `skill.operating_model_analysis`
- `skill.capability_gap_analysis`
- `skill.benchmarking`
- `skill.decision_criteria_design`
- `skill.roadmap_design`
- `skill.negotiation_preparation` — structuring positions, interests, concessions, walk-away limits and issues lists **in preparation for** a negotiation conducted under someone else's delegated authority. Support-only: it never confers a mandate to negotiate, to concede, or to commit, and no proficiency level changes that. Named in the Core Skills prose of four approved Role Cards, always bounded as preparation within delegated limits, which is why it is reusable rather than role-specific.

### Specialisations / Packs
- `skill_pack.change_management_adoption`
- `specialisation.public_sector_strategy`
- `specialisation.nonprofit_strategy`
- `specialisation.commercial_growth_strategy`

## 3. Stakeholder & Institutional

Family scope: institutional and stakeholder analysis.

### Skills
- `skill.stakeholder_mapping`
- `skill.stakeholder_segmentation`
- `skill.institutional_mapping`
- `skill.engagement_strategy_design`
- `skill.consultation_design`
- `skill.meeting_brief_preparation`
- `skill.position_mapping`
- `skill.partner_mapping`
- `skill.relationship_risk_analysis` — stakeholder relationship risk only. Formal integrity, counterparty or sanctions conclusions are outside this Skill and remain owned by `role.integrity_due_diligence_specialist`.
- `skill.social_dialogue_process_design`

### Specialisations / Packs
- `specialisation.eu_institutional_context`
- `specialisation.municipal_stakeholder_context`
- `specialisation.social_partner_context`

## 4. Project / Programme Delivery

Family scope: delivery structuring, sequencing, integration and programme-level tracking.

### Skills
- `skill.scope_definition`
- `skill.work_breakdown_design`
- `skill.project_scheduling`
- `skill.milestone_management`
- `skill.dependency_mapping`
- `skill.critical_path_analysis`
- `skill.raid_management`
- `skill.stage_gate_design`
- `skill.delivery_readiness_assessment`
- `skill.multidisciplinary_integration`
- `skill.action_tracking`
- `skill.deliverable_planning`
- `skill.partner_coordination` — includes formal consortium coordination; the former `skill.consortium_coordination` is merged here, with consortium context expressed as a mapping trigger.
- `skill.results_framework_design`
- `skill.indicator_design`
- `skill.monitoring_evaluation_design`
- `skill.grant_compliance_monitoring` — support-only; grant compliance conclusions remain owned by `role.grant_financial_compliance_budget_specialist`.
- `skill.portfolio_prioritisation_analysis` — support-only; portfolio prioritisation decisions remain a human decision right.
- `skill.benefits_realisation_tracking`

### Specialisations / Packs
- `skill_pack.bid_proposal_management`
- `specialisation.eu_grant_delivery`
- `specialisation.multi_partner_programme_delivery`
- `specialisation.infrastructure_project_preparation`

## 5. Commercial & Market

Family scope: market and commercial analysis. Sales execution belongs to Sales / Marketing / Customer.

### Skills
- `skill.market_sizing`
- `skill.market_segmentation`
- `skill.demand_analysis`
- `skill.customer_discovery`
- `skill.offtake_analysis`
- `skill.pricing_analysis`
- `skill.tariff_analysis` — tariff structure, level and mechanism analysis, including modelling the structure itself. Absorbs the retired `specialisation.tariff_modelling`, which duplicated this Skill under a Specialisation ID.
- `skill.competitor_analysis`
- `skill.go_to_market_analysis`
- `skill.revenue_model_design`
- `skill.commercial_structure_analysis`
- `skill.affordability_analysis` — ability-to-pay and affordability-envelope analysis. Absorbs the retired `specialisation.affordability`, which duplicated this Skill under a Specialisation ID.

### Specialisations / Packs
- `specialisation.regulated_market`
- `specialisation.public_service_demand`

## 6. Finance & Economics

Family scope: financial and economic modelling, appraisal and financial-evidence analysis.

### Skills
- `skill.financial_model_design`
- `skill.financial_statement_modelling`
- `skill.cash_flow_modelling`
- `skill.capex_modelling`
- `skill.opex_modelling`
- `skill.debt_schedule_modelling`
- `skill.working_capital_modelling`
- `skill.discounted_cash_flow_analysis`
- `skill.project_finance_ratio_analysis`
- `skill.financing_scenario_analysis`
- `skill.economic_cost_benefit_analysis`
- `skill.cost_effectiveness_analysis`
- `skill.variance_analysis` — explaining deviation between plan and outcome by driver, distinct from `skill.financial_evidence_reconciliation`, which ties figures back to underlying records. Support-only where it touches another Role's owned figures.
- `skill.financial_evidence_reconciliation`
- `skill.bankability_gap_analysis`
- `skill.funding_source_mapping`
- `skill.accounting_record_reconciliation` — support-only; statutory accounting conclusions remain owned by `role.accounting_financial_due_diligence_specialist`.
- `skill.tax_position_analysis` — support-only; a formal tax position or opinion remains owned by `role.tax_specialist` and its human decision rights.
- `skill.financing_term_analysis` — support-only; financing structure conclusions remain owned by the applicable finance Role.
- `skill.grant_cost_eligibility_analysis` — support-only; eligibility determinations remain owned by `role.grant_financial_compliance_budget_specialist`.

### Specialisations / Packs
- `specialisation.dscr`
- `specialisation.llcr`
- `specialisation.plcr`
- `skill_pack.project_finance_metrics`
- `skill_pack.ifi_financial_appraisal` — generic IFI appraisal method pack only. It must not duplicate institution-specific packs (`skill_pack.eib`, `skill_pack.ebrd`, `skill_pack.world_bank`, `skill_pack.ifc` and similar); where an institution pack applies, the institution pack governs and this pack contributes only method content not already covered.

## 7. Legal / Compliance / Procurement

Family scope: legal obligations and regulated interpretation.

### Skills
- `skill.legal_issue_spotting`
- `skill.regulatory_mapping`
- `skill.requirement_traceability` — linking obligations and requirements to sources, artifacts and verification, **including designing the matrix instrument and its granularity**. Absorbs the retired `skill.traceability_matrix_design`, whose content this capability's own method list already claimed.
- `skill.contract_review` — includes clause-level analysis; the former `skill.contract_clause_analysis` is merged here.
- `skill.procurement_route_analysis`
- `skill.state_aid_screening`
- `skill.compliance_gap_analysis`
- `skill.jurisdiction_mapping`
- `skill.obligation_mapping`
- `skill.licensing_requirement_analysis`
- `skill.privacy_impact_analysis` — support-only; DPIA acceptance and lawful-basis adoption remain owned by `role.data_protection_gdpr_specialist`.
- `skill.lawful_basis_analysis` — support-only; the adopted lawful basis remains owned by `role.data_protection_gdpr_specialist`.

Legal source currency is covered by `skill.source_verification` with a legal-source context trigger; the former `skill.legal_source_currency_check` is merged there.

### Specialisations / Packs
- `specialisation.public_procurement`
- `specialisation.state_aid`
- `specialisation.gdpr`
- `specialisation.cross_border_regulatory`

## 8. ESG / Risk / Integrity

Family scope: risk methods and diligence inputs, without approval authority.

### Skills
- `skill.risk_identification`
- `skill.risk_register_design`
- `skill.risk_quantification`
- `skill.risk_allocation_analysis`
- `skill.risk_mitigation_design`
- `skill.esg_screening`
- `skill.environmental_social_gap_analysis`
- `skill.counterparty_screening`
- `skill.sanctions_screening`
- `skill.insurance_programme_analysis` — programme structure, limits, deductibles and the gap between cover and contractual or lender requirements. Absorbs the retired `skill.insurance_gap_analysis`, which was a step inside it. Support-only; insurance programme adoption and placement remain owned by `role.insurance_risk_transfer_specialist` and its human decision rights.
- `skill.risk_control_design`

Integrity due diligence is not a Skill. The former `skill.integrity_due_diligence` bundled a whole professional methodology and is removed. Its reusable components remain available as `skill.counterparty_screening`, `skill.sanctions_screening`, `skill.source_verification`, `skill.evidence_mapping` and the risk-analysis Skills above. **Integrity due-diligence conclusions remain owned by `role.integrity_due_diligence_specialist`** and are not obtainable by activating any combination of these Skills.

### Specialisations / Packs
- `specialisation.ifi_esg_safeguards`
- `specialisation.project_es_risk`
- `specialisation.integrity_sanctions_context`

## 9. Technical / Engineering

Family scope: technical definition, feasibility, engineering option analysis and asset performance methods.

### Skills
- `skill.technical_requirements_definition`
- `skill.feasibility_analysis`
- `skill.technical_option_comparison`
- `skill.capacity_sizing`
- `skill.design_basis_definition`
- `skill.capex_estimation`
- `skill.cost_estimate_reconciliation`
- `skill.opex_estimation`
- `skill.lifecycle_cost_analysis`
- `skill.asset_performance_analysis`
- `skill.om_strategy_design`
- `skill.technical_risk_analysis`

Technical due diligence is not a separate Skill. The former `skill.technical_due_diligence_support` is removed as an unbounded catch-all; the underlying work is covered by `skill.feasibility_analysis`, `skill.technical_option_comparison`, `skill.technical_risk_analysis`, `skill.design_basis_definition` and `skill.evidence_gap_analysis`, with due-diligence reliance remaining a human decision right.

### Sector Specialisations
- `specialisation.solar`
- `specialisation.bess`
- `specialisation.water`
- `specialisation.waste`
- `specialisation.transport`
- `specialisation.industrial`
- `specialisation.health`
- `specialisation.real_estate`

## 10. Product / UX / Content

Family scope: product-facing information and content design.

### Skills
- `skill.requirements_elicitation`
- `skill.user_story_design`
- `skill.use_case_modelling`
- `skill.acceptance_criteria_design`
- `skill.process_mapping`
- `skill.information_architecture`
- `skill.user_flow_design`
- `skill.usability_analysis`
- `skill.accessibility_analysis`
- `skill.content_structure_design`
- `skill.editorial_quality_control`
- `skill.publication_requirements_validation` — validates that stated publication requirements are met. This is a quality-control capability and is **not** independent review and not publication authority.

### Specialisations / Packs
- `specialisation.institutional_website`
- `specialisation.admin_console`
- `specialisation.multilingual_content`

## 11. Software / Integration / Platform / Security

Family scope: software architecture, integration, platform engineering and security engineering technique. Security is an explicit subfamily below; family membership never implies authority or exclusive Role compatibility.

### Skills
- `skill.solution_decomposition`
- `skill.architecture_decision_recording`
- `skill.quality_attribute_analysis` — selectable dimensions may include security, privacy, resilience, performance and availability. Selecting a dimension does **not** transfer professional ownership: security ownership remains with `role.security_engineer` and personal-data ownership with `role.data_protection_gdpr_specialist`.
- `skill.api_contract_design`
- `skill.integration_pattern_selection`
- `skill.backend_implementation`
- `skill.frontend_implementation`
- `skill.test_automation`
- `skill.defect_management` — defect identification, reproduction, severity characterisation and defect-record discipline. Distinct from defect *correction*, which is implementation and belongs to the engineering Roles; this capability establishes that a defect is real, reproducible and correctly severity-rated, and never authorises deferral, which is a human decision right.
- `skill.release_engineering`
- `skill.ci_cd_design`
- `skill.infrastructure_as_code`
- `skill.observability_design`
- `skill.incident_response_design`
- `skill.performance_testing`

#### Security subfamily
- `skill.threat_modelling` — support-only; the threat model as a professional conclusion remains owned by `role.security_engineer`.
- `skill.security_control_design` — support-only; control adequacy conclusions and accreditation remain owned by `role.security_engineer` and its human decision rights.
- `skill.security_control_validation` — evidence-gathering and validation technique. This is **not** independent security review and not accreditation.
- `skill.security_testing` — testing technique. Findings are inputs; risk acceptance remains a human decision right.

### Technology Specialisations / Packs
- `skill_pack.supabase`
- `skill_pack.postgresql`
- `skill_pack.vercel`

## 12. Data / Analytics / AI

Family scope: data architecture and analytical / AI technique. Platform implementation, deployment and security engineering belong to Software / Integration / Platform / Security; this family covers how data is modelled, analysed and reasoned over, not how a platform is built or secured.

### Skills
- `skill.data_model_design`
- `skill.schema_design`
- `skill.data_quality_rule_design`
- `skill.data_pipeline_design`
- `skill.data_transformation`
- `skill.database_migration_planning` — support-only; production migration execution and its human decision right remain owned by the applicable engineering Role.
- `skill.sql_analysis`
- `skill.metric_definition`
- `skill.dashboard_design`
- `skill.statistical_analysis`
- `skill.analytics_interpretation`
- `skill.ai_use_case_design`
- `skill.prompt_method_design`
- `skill.ai_output_evaluation`
- `skill.retrieval_design`
- `skill.knowledge_graph_design`
- `skill.ai_guardrail_design`

### Specialisations / Packs
- `specialisation.relational_data_platform`
- `specialisation.rag_knowledge_system`
- `specialisation.ai_assisted_research`

## 13. Documentation / Knowledge / Disclosure

Family scope: governed records, configuration, lineage and disclosure packaging.

### Skills
- `skill.technical_writing`
- `skill.document_structuring`
- `skill.document_version_control`
- `skill.document_configuration_control`
- `skill.evidence_indexing`
- `skill.knowledge_state_metadata_management` — records and maintains knowledge-state metadata. A Skill may contribute to Role-owned knowledge-state work but can never execute a knowledge-state transition; promotion to APPROVED or CANONICAL remains a governed human decision.
- `skill.data_room_index_design`
- `skill.disclosure_package_preparation`
- `skill.disclosure_access_matrix_design` — support-only; disclosure authorisation and access grants remain human decision rights owned by `role.data_room_disclosure_manager`.
- `skill.disclosure_tracking`
- `skill.redaction_preparation`
- `skill.document_gap_analysis`

### Skill Packs
- `skill_pack.technical_writing_documentation` — adds governed templates, house conventions, controlled documentation requirements and currency rules **beyond** the `skill.technical_writing` technique. Where it would add nothing beyond the Skill, map the Skill directly instead of the Pack.
- `skill_pack.version_control_document_configuration`

## 14. Sales / Marketing / Customer

Family scope: commercial acquisition, commercial communication and customer lifecycle. Market analysis belongs to Commercial & Market.

### Skills
- `skill.lead_qualification`
- `skill.account_mapping`
- `skill.opportunity_qualification`
- `skill.value_proposition_design`
- `skill.sales_pipeline_analysis`
- `skill.proposal_commercial_narrative`
- `skill.marketing_message_design`
- `skill.campaign_design`
- `skill.claim_substantiation`
- `skill.customer_journey_mapping`
- `skill.crm_process_design`
- `skill.customer_commitment_tracking`

### Specialisations / Packs
- `specialisation.b2b_sales`
- `specialisation.institutional_business_development`
- `specialisation.partner_led_growth`

## 15. Operations / Supply Chain / People

Family scope: operating process, capacity and resourcing, sourcing, and workforce / organisational design and learning.

### Skills
- `skill.process_design`
- `skill.sop_design`
- `skill.service_delivery_design`
- `skill.capacity_planning` — sizing work against available capacity and resourcing it. Absorbs the retired `skill.resource_planning`, whose two consumers already carried this capability.
- `skill.supplier_evaluation`
- `skill.sourcing_analysis`
- `skill.inventory_analysis`
- `skill.workforce_planning`
- `skill.role_responsibility_mapping`
- `skill.organisation_design_analysis`
- `skill.training_needs_analysis`
- `skill.learning_outcome_design` — support-only; curriculum adoption remains a human decision right owned by `role.learning_vet_design_specialist`.
- `skill.assessment_design` — support-only; approval of an assessment for formal recognition remains a human decision right.

### Specialisations / Packs
- `specialisation.service_operations`
- `specialisation.supply_chain_operations`
- `specialisation.organisation_change`

# Cross-Family Skill Packs

The following packs intentionally span multiple Skill Families.

## EU Programme Packs
- `skill_pack.erasmus_plus`
- `skill_pack.cove` — **layers over `skill_pack.erasmus_plus`** where the CoVE action operates under Erasmus+ rules. The dependency is declared on the CoVE Pack, in that direction only; Erasmus+ must not declare a dependency on CoVE, which would create a cycle. Where a CoVE action is funded outside Erasmus+, the dependency does not apply and the governing programme Pack is declared instead.
- `skill_pack.life_programme`
- `skill_pack.horizon_europe`

Expected composition: programme rules, eligibility interpretation, intervention logic, application structure, work-package logic, budget logic, consortium requirements, reporting requirements, controlled-source currency and submission requirement mapping.

These programme capabilities are **pack-internal components, not standalone Skill IDs**. Eligibility analysis, work-package logic design, budget logic analysis and submission requirement mapping are meaningless outside a specific programme rulebook and its current call version, so they are governed by the applicable programme Pack and its currency rules rather than mapped individually. Do not reintroduce them as standalone `skill.<id>` entries.

## IFI / Funding Packs
- `skill_pack.eib`
- `skill_pack.ebrd`
- `skill_pack.world_bank`
- `skill_pack.ifc`
- `skill_pack.bgk`
- `skill_pack.investeu`
- `skill_pack.ukraine_facility`

Expected composition: institutional eligibility, appraisal logic, documentation expectations, financial / economic / ESG requirements, procurement or integrity interfaces, submission requirement mapping, submission route and source-currency controls.

As with programme packs, submission requirement mapping is a **pack-internal component, not a standalone Skill ID**: the requirements are institution-specific and version-sensitive.

## Technology Packs
- `skill_pack.supabase`
- `skill_pack.postgresql`
- `skill_pack.vercel`

Expected composition: platform-specific architecture, implementation constraints, security controls, version / service-limit currency, deployment practices and compatible Role IDs.

## Bid / Proposal Management Pack
- `skill_pack.bid_proposal_management`

Bid / proposal management is represented **only** as a Pack. There is no standalone `skill.bid_proposal_management`: the capability is a governed bundle of qualification, compliance-matrix, content-planning, review-cycle and submission-control practices that travel together and carry currency rules, not a single reusable technique.

## Project Finance Metrics Pack
- `skill_pack.project_finance_metrics`

Contains at minimum:
- `specialisation.dscr`
- `specialisation.llcr`
- `specialisation.plcr`

May additionally contain debt sculpting, covenant headroom and sensitivity conventions when later approved.

# Removed and Merged IDs — Deprecation Register

These identifiers are **retired**. None is declared in any Family above and none is mapped to any Role. They are recorded here, and referenced in the deprecation notes beside their surviving replacements, so that the reason for retirement travels with the registry and the identifier is not silently reintroduced.

A tombstone is not an active reference: a retired ID cannot be activated, cannot satisfy a mapping obligation and must not be written into a new mapping record.

| Retired ID | Reason | Where the capability lives now |
|---|---|---|
| `skill.integrity_due_diligence` | Bundled an entire professional methodology into one Skill — a hidden Role. | `skill.counterparty_screening`, `skill.sanctions_screening`, `skill.source_verification`, `skill.evidence_mapping`, risk Skills. Conclusions owned by `role.integrity_due_diligence_specialist`. |
| `skill.technical_due_diligence_support` | Unbounded catch-all. | `skill.feasibility_analysis`, `skill.technical_option_comparison`, `skill.technical_risk_analysis`, `skill.design_basis_definition`, `skill.evidence_gap_analysis`. |
| `skill.consortium_coordination` | Duplicate of a broader capability. | Merged into `skill.partner_coordination`; consortium context is a mapping trigger. |
| `skill.contract_clause_analysis` | Sub-step of a broader capability. | Merged into `skill.contract_review`. |
| `skill.legal_source_currency_check` | Domain-specific restatement of a reusable capability. | Merged into `skill.source_verification` with a legal-source trigger. |
| `skill.reporting_schedule_management` | Composite of two existing capabilities. | `skill.deliverable_planning` + `skill.milestone_management`. |
| `skill.version_control` | Ambiguous against software version control. | Renamed `skill.document_version_control`. |
| `skill.control_design` | Ambiguous against software and process controls. | Renamed `skill.risk_control_design`. |
| `skill.canonical_status_management_support` | Name implied authority over canonical status. | Renamed `skill.knowledge_state_metadata_management`. |
| `skill.publication_readiness_check` | "Check" read as assurance. | Renamed `skill.publication_requirements_validation`; explicitly not independent review. |
| `specialisation.official_source_monitoring` | Context variant mis-modelled as a Specialisation. | `skill.source_monitoring` with a source-class trigger. |
| `specialisation.policy_source_monitoring` | Context variant mis-modelled as a Specialisation. | `skill.source_monitoring` with a policy-source trigger. |
| `skill.eligibility_analysis` | Meaningless outside a programme rulebook and call version. | Pack-internal component of the EU programme Packs. |
| `skill.work_package_logic_design` | Programme-bound, not reusable standalone. | Pack-internal component of the EU programme Packs. |
| `skill.budget_logic_analysis` | Programme-bound, not reusable standalone. | Pack-internal component of the EU programme Packs. |
| `skill.submission_requirement_mapping` | Institution- and version-specific. | Pack-internal component of programme and institution Packs. |
| `skill.bid_proposal_management` | A governed bundle, not a single technique. | `skill_pack.bid_proposal_management` only. |
| `skill.security_constraint_allocation` | Read as an architecture-owned security capability. | `skill.quality_attribute_analysis` (security dimension) + `skill.requirement_traceability`. Security ownership stays with `role.security_engineer`. |
| `skill.resource_planning` | Duplicated capacity sizing; both consumers already carried the survivor. | Merged into `skill.capacity_planning`. |
| `skill.insurance_gap_analysis` | A step inside programme analysis, not a peer of it; same single consumer. | Merged into `skill.insurance_programme_analysis`. |
| `skill.traceability_matrix_design` | The survivor's own method list already claimed matrix granularity design. | Merged into `skill.requirement_traceability`. |
| `specialisation.affordability` | A Skill wearing a Specialisation ID — it names a method, not a bounded context. | Merged into `skill.affordability_analysis`. |
| `specialisation.tariff_modelling` | A Skill wearing a Specialisation ID — it names a method, not a bounded context. | Merged into `skill.tariff_analysis`. |

# Overlap Boundaries Clarified in Wave 3

These pairs and groups were examined against actual reuse across all 59 Roles and **kept distinct**, because each member carries a different professional method rather than a different name for one method. They are recorded here so a future reviewer does not re-open them without new evidence.

- **`skill.market_sizing` / `skill.market_segmentation` / `skill.demand_analysis`** — sizing a market, dividing it, and forecasting demand for a specific asset or service are three methods with different inputs and error modes. All three are multi-Role.
- **`skill.risk_identification` / `skill.risk_register_design`** — elicitation versus designing the register instrument (taxonomy, scales, aggregation). Identification reaches 14 Roles; register design is the methodology surface owned by `role.enterprise_project_risk_specialist`.
- **`skill.action_tracking` / `skill.milestone_management` / `skill.deliverable_planning`** — three different tracked objects with different cadence and completion semantics. All three are multi-Role.
- **`skill.process_design` / `skill.process_mapping` / `skill.sop_design`** — designing a target process, documenting an existing one, and writing the operating procedure are sequential and separately commissioned.
- **`skill.source_discovery` / `skill.source_comparison` / `skill.source_verification` / `skill.source_monitoring` / `skill.change_detection`** — finding, comparing, authenticating, watching and diffing are distinct operations on sources. `skill.source_discovery` is currently single-consumer because most Roles are given their source set rather than assembling it; that is a consumer count, not a duplication.
- **`skill.evidence_indexing` / `skill.data_room_index_design`** — the second carries phased-release and access-tier structure that the first does not, and it maps to a Role-owned artifact. Not merged.
- **`skill.esg_screening` / `skill.environmental_social_gap_analysis`** — triage and categorisation versus assessment against a named safeguard standard.
- **`skill.security_control_design` / `skill.risk_control_design`** — technical security controls in a system versus risk-management controls over a process. Different families, different methods; the similarity is only in the names, so both keep their IDs and carry disambiguating scope here.
- **`skill.source_monitoring` / `skill.change_detection`** — watching a defined set on a cadence versus analysing what differs between two versions.
- **`skill.privacy_impact_analysis` / `skill.security_control_validation` / `skill.threat_modelling`** — all three are mapped outside their owning Roles as explicitly support-only, and every such mapping in Wave 1 and Wave 2 carries a support-only boundary note naming the Role that retains the conclusion.

# Duplication / Granularity Controls

The following pairs must remain distinct unless later review proves otherwise:
- source verification vs factual evidence review;
- tariff analysis vs tariff modelling specialisation;
- affordability analysis vs affordability specialisation;
- requirements elicitation vs stakeholder consultation design;
- risk identification vs integrity due-diligence conclusions owned by `role.integrity_due_diligence_specialist`;
- technical feasibility analysis vs sector specialisation;
- financial modelling skills vs project-finance metric specialisations;
- data model design vs PostgreSQL technology pack;
- API contract design vs Supabase technology pack;
- technical writing skill vs Technical Writing / Documentation pack.

The following should not become separate skills without a demonstrated reuse case:
- individual menu-click actions;
- one-off document headings;
- a single software command;
- a single formula that belongs inside a broader modelling skill;
- a project-specific fact or client-specific procedure;
- a prompt for one AI model;
- a one-time workflow step.

# Initial Scale

This universe intentionally remains bounded.

Inventory counted from this file after Wave 1 remediation:
- 15 Skill Families;
- 205 reusable Skills;
- 43 Specialisations (sector / programme / institution / technology / metric / operating context);
- 21 Skill Packs, including cross-family packs for EU programmes, IFIs, technologies, bid / proposal management and project-finance metrics.

The earlier "about 150 Skills" estimate was inaccurate against the file it described and has been replaced with a counted figure. The count is **not a target** and must not be managed toward a number: it is reported so that drift between the stated and actual inventory is visible. New items still require evidence of reuse and distinct capability value, and the Granularity Rule above governs whether an item is created at all.

Net change from Wave 1 remediation: 23 reusable capability classes added, 6 removed or merged (`skill.integrity_due_diligence`, `skill.technical_due_diligence_support`, `skill.consortium_coordination`, `skill.contract_clause_analysis`, `skill.legal_source_currency_check`, `skill.reporting_schedule_management`), and 2 monitoring Specialisations replaced by the reusable `skill.source_monitoring`.

# Next Phase 4 Work

Before creating individual Skill Cards at scale:
1. audit this universe for duplicates and missing capability classes;
2. define Role-to-Skill mapping rules against all 59 approved roles;
3. select a small exemplar set of Skill Cards and Skill Packs;
4. stress-test the taxonomy against representative AI-OS projects;
5. revise before mass-generation.

No item in this document is APPROVED merely by inclusion. All entries remain PROPOSED until Phase 4 human approval.