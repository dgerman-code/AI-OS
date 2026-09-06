# Phase 4 — Wave 2 Domain Completion Role-to-Skill Mapping

Status: PROPOSED — Phase 4 working baseline

## Scope

Maps the **48 approved Roles not covered by Wave 1**, completing Role-to-Skill mapping across all 59 approved Phase 3 Roles.

Wave 1 (`skills/mappings/wave-1-exemplar-role-skill-mapping.md`) is a reviewed exemplar baseline and is **not** rewritten here. Its 11 Roles are referenced only for reuse analysis and cross-wave conflict checking.

This mapping changes no Role Card, creates no Skill, Specialisation or Skill Pack Card, and creates no first-class Role.

**Normalized in Wave 3.** Cross-domain normalization retired 5 duplicate IDs, added 3 reusable capability classes, reclassified 2 Specialisations and corrected the Project Development Lead audit-trail prose. Section 11 records it; the consolidated rationale is in `reviews/phase-4-wave-3-cross-domain-normalization.md`.

**Remediated after independent Wave 2 audit.** The audit returned FAIL on 48 card-allowlist compatibility conflicts — 37 direct Skill mappings and 11 direct Pack mappings whose consuming Roles were absent from the target card allowlists. All 48 are resolved: 45 by governed card widening after Role-Card review, 3 by removing the mapping instead. Two relationship defects were also corrected. Section 10 records the remediation in full.

## Canonical source statement

> Role-to-Skill mapping records are the sole authoritative source for relationship type, context trigger and alternative choice condition. Mapping grants capability applicability, never professional authority.

Skill, Specialisation and Skill Pack Cards may declare compatible-Role allowlists and reference these records; they may not declare a relationship type or define a trigger. Where a card's advisory text diverges from a record here, this record governs and the divergence is raised as `CONFLICT_DETECTED`.

The approved Role Card outranks this record on every question of authority, ownership, review obligation and decision right. A mapping may never widen Professional Scope.

## Relationship vocabulary

- `REQUIRED_CORE` — intrinsic to competent execution across substantially all ordinary assignments. Used sparingly; a Role Card's prose Core Skills are not mechanically converted into registry entries.
- `REQUIRED_FOR_CONTEXT` — mandatory when a stated trigger is true. Every entry carries an explicit trigger.
- `OPTIONAL` — genuinely useful but not required for a valid assignment.
- `ALTERNATIVE` — a named choice set with a stated condition and cardinality.
- `PROHIBITED_IN_CONTEXT` — must not be activated, with a concrete scope, independence or safety basis.

## Project criticality

Per `architecture/project-criticality-policy.md`, criticality increases required depth, evidence quality, review dependency, specialist engagement and contextual activation. It does **not** create a new Role identity and does **not** globally convert OPTIONAL into REQUIRED_CORE. No mapping below encodes a monetary threshold.

# 1. Role ID Verification

Every Role ID below was extracted from the actual approved Role Card at the stated path, not inferred from the Role name. 48 names, 48 unique IDs, zero overlap with the 11 Wave 1 Roles, and 11 + 48 = 59 = the approved Role Registry.

| # | Role Name | Role ID | Role Card |
|---:|---|---|---|
| 1 | Portfolio / Programme Manager | `role.portfolio_programme_manager` | `roles/portfolio-programme-project/portfolio-programme-manager.md` |
| 2 | Strategy & Business Analyst | `role.strategy_business_analyst` | `roles/strategy-business/strategy-business-analyst.md` |
| 3 | Marketing / Growth Specialist | `role.marketing_growth_specialist` | `roles/strategy-business/marketing-growth-specialist.md` |
| 4 | Operations / Service Delivery Specialist | `role.operations_service_delivery_specialist` | `roles/strategy-business/operations-service-delivery-specialist.md` |
| 5 | People / Organisation Specialist | `role.people_organisation_specialist` | `roles/strategy-business/people-organisation-specialist.md` |
| 6 | Customer / CRM Specialist | `role.customer_crm_specialist` | `roles/strategy-business/customer-crm-specialist.md` |
| 7 | Supply Chain & Procurement Operations Specialist | `role.supply_chain_procurement_operations_specialist` | `roles/strategy-business/supply-chain-procurement-operations-specialist.md` |
| 8 | EU Policy & Institutional Affairs Specialist | `role.eu_policy_institutional_affairs_specialist` | `roles/eu-institutional-programme/eu-policy-institutional-affairs-specialist.md` |
| 9 | EU Enlargement / Governance Specialist | `role.eu_enlargement_governance_specialist` | `roles/eu-institutional-programme/eu-enlargement-governance-specialist.md` |
| 10 | Institutional Affairs & Stakeholder Specialist | `role.institutional_affairs_stakeholder_specialist` | `roles/eu-institutional-programme/institutional-affairs-stakeholder-specialist.md` |
| 11 | Programme / Partnership Manager | `role.programme_partnership_manager` | `roles/eu-institutional-programme/programme-partnership-manager.md` |
| 12 | EU Programme Implementation & Grant Management Specialist | `role.eu_programme_implementation_grant_management_specialist` | `roles/eu-institutional-programme/eu-programme-implementation-grant-management-specialist.md` |
| 13 | Consortium / Partner Coordination Specialist | `role.consortium_partner_coordination_specialist` | `roles/eu-institutional-programme/consortium-partner-coordination-specialist.md` |
| 14 | Grant Financial Compliance / Budget Specialist | `role.grant_financial_compliance_budget_specialist` | `roles/eu-institutional-programme/grant-financial-compliance-budget-specialist.md` |
| 15 | Deliverables / Reporting Specialist | `role.deliverables_reporting_specialist` | `roles/eu-institutional-programme/deliverables-reporting-specialist.md` |
| 16 | Learning / VET Design Specialist | `role.learning_vet_design_specialist` | `roles/eu-institutional-programme/learning-vet-design-specialist.md` |
| 17 | Social Dialogue Specialist | `role.social_dialogue_specialist` | `roles/eu-institutional-programme/social-dialogue-specialist.md` |
| 18 | Monitoring, Evaluation & Learning Specialist | `role.monitoring_evaluation_learning_specialist` | `roles/eu-institutional-programme/monitoring-evaluation-learning-specialist.md` |
| 19 | Project Development Lead | `role.project_development_lead` | `roles/project-development-technical-commercial/project-development-lead.md` |
| 20 | Sector Technical Expert | `role.sector_technical_expert` | `roles/project-development-technical-commercial/sector-technical-expert.md` |
| 21 | Commercial & Demand Specialist | `role.commercial_demand_specialist` | `roles/project-development-technical-commercial/commercial-demand-specialist.md` |
| 22 | CAPEX / Cost Engineering Specialist | `role.capex_cost_engineering_specialist` | `roles/project-development-technical-commercial/capex-cost-engineering-specialist.md` |
| 23 | Asset O&M / Technical Operations Specialist | `role.asset_om_technical_operations_specialist` | `roles/project-development-technical-commercial/asset-om-technical-operations-specialist.md` |
| 24 | Economic / CBA Specialist | `role.economic_cba_specialist` | `roles/economics-finance-transaction/economic-cba-specialist.md` |
| 25 | FP&A / Management Finance Specialist | `role.fpa_management_finance_specialist` | `roles/economics-finance-transaction/fpa-management-finance-specialist.md` |
| 26 | Funding & Bankability Architect | `role.funding_bankability_architect` | `roles/economics-finance-transaction/funding-bankability-architect.md` |
| 27 | Project Finance / Transaction Specialist | `role.project_finance_transaction_specialist` | `roles/economics-finance-transaction/project-finance-transaction-specialist.md` |
| 28 | IFI / DFI Project Preparation Specialist | `role.ifi_dfi_project_preparation_specialist` | `roles/economics-finance-transaction/ifi-dfi-project-preparation-specialist.md` |
| 29 | PPP / Concession Specialist | `role.ppp_concession_specialist` | `roles/economics-finance-transaction/ppp-concession-specialist.md` |
| 30 | Tax Specialist | `role.tax_specialist` | `roles/economics-finance-transaction/tax-specialist.md` |
| 31 | Accounting / Financial Due Diligence Specialist | `role.accounting_financial_due_diligence_specialist` | `roles/economics-finance-transaction/accounting-financial-due-diligence-specialist.md` |
| 32 | Insurance / Risk Transfer Specialist | `role.insurance_risk_transfer_specialist` | `roles/economics-finance-transaction/insurance-risk-transfer-specialist.md` |
| 33 | Procurement / State Aid Specialist | `role.procurement_state_aid_specialist` | `roles/legal-compliance/procurement-state-aid-specialist.md` |
| 34 | ESG / E&S Specialist | `role.esg_es_specialist` | `roles/legal-compliance/esg-es-specialist.md` |
| 35 | Enterprise / Project Risk Specialist | `role.enterprise_project_risk_specialist` | `roles/legal-compliance/enterprise-project-risk-specialist.md` |
| 36 | Integrity / Due Diligence Specialist | `role.integrity_due_diligence_specialist` | `roles/legal-compliance/integrity-due-diligence-specialist.md` |
| 37 | Data Protection / GDPR Specialist | `role.data_protection_gdpr_specialist` | `roles/legal-compliance/data-protection-gdpr-specialist.md` |
| 38 | UX / UI & Information Architecture Specialist | `role.ux_ui_information_architecture_specialist` | `roles/digital-product-software-data/ux-ui-information-architecture-specialist.md` |
| 39 | Institutional Communications / Editorial Specialist | `role.institutional_communications_editorial_specialist` | `roles/digital-product-software-data/institutional-communications-editorial-specialist.md` |
| 40 | Full-Stack Software Engineer | `role.full_stack_software_engineer` | `roles/digital-product-software-data/full-stack-software-engineer.md` |
| 41 | Integration / API Engineer | `role.integration_api_engineer` | `roles/digital-product-software-data/integration-api-engineer.md` |
| 42 | Platform / DevOps Engineer | `role.platform_devops_engineer` | `roles/digital-product-software-data/platform-devops-engineer.md` |
| 43 | Database / Data Engineer | `role.database_data_engineer` | `roles/digital-product-software-data/database-data-engineer.md` |
| 44 | Data / Business Analytics Specialist | `role.data_business_analytics_specialist` | `roles/digital-product-software-data/data-business-analytics-specialist.md` |
| 45 | AI / Knowledge Systems Engineer | `role.ai_knowledge_systems_engineer` | `roles/digital-product-software-data/ai-knowledge-systems-engineer.md` |
| 46 | Security Engineer | `role.security_engineer` | `roles/digital-product-software-data/security-engineer.md` |
| 47 | Software QA / Test Automation Specialist | `role.software_qa_test_automation_specialist` | `roles/digital-product-software-data/software-qa-test-automation-specialist.md` |
| 48 | Data Room & Disclosure Manager | `role.data_room_disclosure_manager` | `roles/knowledge-documentation-disclosure/data-room-disclosure-manager.md` |

# 2. Wave 2 Mappings

## 1. Portfolio / Programme Manager

Role: `role.portfolio_programme_manager`

### REQUIRED_CORE
- `skill.portfolio_prioritisation_analysis`
- `skill.strategic_prioritisation`
- `skill.dependency_mapping`
- `skill.stage_gate_design`
- `skill.benefits_realisation_tracking`

### REQUIRED_FOR_CONTEXT
- `skill.capacity_planning`
  - trigger: portfolio decision depends on constrained delivery capacity or resource contention
- `skill.raid_management`
  - trigger: programme-level risk, assumption, issue or dependency aggregation is in assignment scope
- `specialisation.multi_partner_programme_delivery`
  - trigger: portfolio or programme spans multiple formal partner organisations
- `specialisation.eu_grant_delivery`
  - trigger: constituent projects are EU-funded and programme reporting follows grant cycles

### OPTIONAL
- `skill.roadmap_design`
- `skill.scenario_analysis`
- `skill.decision_criteria_design`
- `skill.milestone_management`

### Boundaries
- Support-only boundary: aggregated risk visibility uses `skill.raid_management` at programme level only. The project-level RAID record and delivery integration remain owned by `role.project_delivery_lead` where a delivery assignment exists; this Role aggregates without absorbing.
- No mapping confers prioritisation authority. `decision.portfolio_prioritisation` and `decision.stage_gate_progression` remain human decision rights.
- Specialist conclusions in any discipline are consumed at the state their owning Role supplies; none is originated here.

### Sparse-core rationale
Core is the aggregation-and-sequencing surface the Role owns across substantially all portfolio assignments. Capacity and RAID are contextual because a portfolio assignment can be purely compositional without a resource-contention or risk-aggregation question.

## 2. Strategy & Business Analyst

Role: `role.strategy_business_analyst`

### REQUIRED_CORE
- `skill.problem_structuring`
- `skill.option_analysis`
- `skill.decision_criteria_design`
- `skill.assumption_analysis`
- `skill.business_case_structuring`

### REQUIRED_FOR_CONTEXT
- `skill.capability_gap_analysis`
  - trigger: assignment covers organisational capability or operating-model fit
- `skill.scenario_analysis`
  - trigger: strategic case depends on materially different future states
- `skill.benchmarking`
  - trigger: option appraisal relies on external comparators
- `specialisation.public_sector_strategy`
  - trigger: counterparty or mandate is public-sector
- `specialisation.nonprofit_strategy`
  - trigger: organisation is a nonprofit or association operating to a mission mandate
- `specialisation.commercial_growth_strategy`
  - trigger: assignment is commercial growth strategy for a trading business

### OPTIONAL
- `skill.operating_model_analysis`
- `skill.roadmap_design`
- `skill.sensitivity_analysis`
- `skill.research_synthesis`

### Boundaries
- Support-only boundary vs `role.research_market_intelligence_analyst`: `skill.research_synthesis` and `skill.benchmarking` are used to structure an argument, not to own the evidence base. Where a research assignment exists, market evidence is consumed from it at its stated state; this Role does not become the owner of market-intelligence conclusions.
- No financial model construction or valuation conclusion: those remain owned by `role.financial_modelling_specialist`.
- `decision.strategic_direction` and `decision.business_case_approval` remain human decision rights.

### Sparse-core rationale
Core is the structuring surface — framing, options, criteria, assumptions, case architecture — which is intrinsic to every strategy assignment. Evidence-gathering capabilities are contextual or optional precisely to keep the boundary with Research / Market Intelligence visible.

## 3. Marketing / Growth Specialist

Role: `role.marketing_growth_specialist`

### REQUIRED_CORE
- `skill.marketing_message_design`
- `skill.campaign_design`
- `skill.market_segmentation`
- `skill.claim_substantiation`

### REQUIRED_FOR_CONTEXT
- `skill.go_to_market_analysis`
  - trigger: assignment covers launch or channel strategy for a new offer or market
- `skill.customer_journey_mapping`
  - trigger: campaign design depends on lifecycle stage or funnel behaviour
- `skill.value_proposition_design`
  - trigger: positioning or proposition is being defined rather than applied
- `skill.publication_requirements_validation`
  - trigger: asset is destined for external publication and format or disclosure requirements apply
- `specialisation.multilingual_content`
  - trigger: campaign runs in more than one language

### OPTIONAL
- `skill.competitor_analysis`
- `skill.content_structure_design`
- `skill.analytics_interpretation`
- `skill.pricing_analysis`

### PROHIBITED_IN_CONTEXT
- `skill.lawful_basis_analysis`
  - basis: Role Card Does Not Own states lawful-basis determination for personal-data processing. Marketing frequently touches personal data, so an unmapped-but-available lawful-basis capability is a live risk of the Role appearing to settle its own compliance question. Lawful basis remains owned by `role.data_protection_gdpr_specialist` and gated by `decision.lawful_basis_adoption`.

### Boundaries
- Support-only boundary vs `role.institutional_communications_editorial_specialist`: campaign and commercial messaging is this Role's; institutional positions, editorial standards and funder-visibility publication remain the Editorial Role's, and `decision.institutional_position_release` is never reachable here.
- `skill.claim_substantiation` is core because claims are the Role's main external exposure, but substantiation is a self-check: approval of public claims is gated by `review.commercial_claims` and `decision.external_publication`.
- `skill.pricing_analysis` is Optional and analytical only; pricing approval is outside Role scope.

### Sparse-core rationale
Core is the message-campaign-segment-substantiate loop the Role runs on every assignment. Everything touching legal or institutional authority is contextual, optional or prohibited.

## 4. Operations / Service Delivery Specialist

Role: `role.operations_service_delivery_specialist`

### REQUIRED_CORE
- `skill.process_design`
- `skill.process_mapping`
- `skill.service_delivery_design`
- `skill.capacity_planning`

### REQUIRED_FOR_CONTEXT
- `skill.sop_design`
  - trigger: operating procedures must be documented for repeatable execution
- `skill.operating_model_analysis`
  - trigger: assignment covers corporate operating-model structure rather than a single process
- `skill_pack.change_management_adoption`
  - trigger: process or operating-model change requires adoption across an affected population
- `specialisation.service_operations`
  - trigger: assignment is service-operations design in an ongoing operational context

### OPTIONAL
- `skill.risk_control_design`
- `skill.analytics_interpretation`
- `skill.role_responsibility_mapping`
- `skill.benchmarking`

### Boundaries
- Support-only boundary vs `role.asset_om_technical_operations_specialist`: this Role owns corporate operating-model and service-model design. Asset O&M strategy, maintenance regimes and availability basis for infrastructure and industrial assets remain owned by the Asset O&M Role — the Role Card excludes them explicitly.
- `skill.service_delivery_design` produces service-level feasibility analysis, never a contractual commitment: `decision.service_level_commitment` is a human decision right.
- No production system change or deployment authority arises from any mapping here.

### Sparse-core rationale
Core is process, service and capacity design. Operating-model analysis is contextual rather than core because many assignments are single-process improvements where a whole-model analysis would be disproportionate.

## 5. People / Organisation Specialist

Role: `role.people_organisation_specialist`

### REQUIRED_CORE
- `skill.organisation_design_analysis`
- `skill.role_responsibility_mapping`
- `skill.workforce_planning`
- `skill.capability_gap_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.training_needs_analysis`
  - trigger: capability gap is to be closed through learning rather than structure or hiring
- `skill.process_design`
  - trigger: people lifecycle processes are in assignment scope
- `skill_pack.change_management_adoption`
  - trigger: organisational change requires adoption planning across an affected population
- `specialisation.organisation_change`
  - trigger: assignment is a structural reorganisation rather than steady-state design

### OPTIONAL
- `skill.survey_research_design`
- `skill.stakeholder_segmentation`
- `skill.analytics_interpretation`
- `skill.capacity_planning`

### Boundaries
- Support-only boundary vs `role.learning_vet_design_specialist`: `skill.training_needs_analysis` identifies capability gaps and learning needs. Learning-outcome frameworks, curriculum architecture and assessment design remain owned by the Learning / VET Role and are not mapped here.
- Employment-law and collective-agreement conclusions remain owned by `role.legal_regulatory_lead`; the Role Card carries `review.legal_compliance` for that reason.
- No mapping reaches hiring, promotion, disciplinary, redundancy or termination decisions — all outside Role scope and gated by `decision.organisational_change`.

### Sparse-core rationale
Core is structure, roles, workforce and capability analysis. Sensitive personal judgements and legal conclusions are excluded by Role scope, not merely unmapped.

## 6. Customer / CRM Specialist

Role: `role.customer_crm_specialist`

### REQUIRED_CORE
- `skill.customer_journey_mapping`
- `skill.crm_process_design`
- `skill.customer_commitment_tracking`
- `skill.market_segmentation`

### REQUIRED_FOR_CONTEXT
- `skill.service_delivery_design`
  - trigger: customer lifecycle design depends on service tiers or fulfilment behaviour
- `skill.process_design`
  - trigger: complaint, escalation or resolution processes are in scope
- `skill.analytics_interpretation`
  - trigger: retention, churn or lifecycle analysis drives the design
- `skill.privacy_impact_analysis`
  - trigger: CRM design introduces new personal-data processing, profiling or a new recipient

### OPTIONAL
- `skill.customer_discovery`
- `skill.stakeholder_segmentation`
- `skill.sop_design`
- `skill.dashboard_design`

### Boundaries
- Support-only boundary vs `role.data_protection_gdpr_specialist`: `skill.privacy_impact_analysis` here is contextual and support-only. It surfaces that a DPIA is needed and assembles inputs; the DPIA itself, the lawful basis and their acceptance remain owned by the Data Protection Role under `decision.dpia_acceptance` and `decision.lawful_basis_adoption`.
- `skill.customer_commitment_tracking` records commitments; making them is gated by `decision.customer_commitment` and delegated authority limits.
- CRM platform architecture and production configuration remain outside Role scope.

### Sparse-core rationale
Core is the lifecycle-CRM-commitment-segmentation surface. Privacy capability is contextual and support-only by design, because CRM work touches personal data constantly and the boundary must be re-asserted per assignment.

## 7. Supply Chain & Procurement Operations Specialist

Role: `role.supply_chain_procurement_operations_specialist`

### REQUIRED_CORE
- `skill.sourcing_analysis`
- `skill.supplier_evaluation`
- `skill.inventory_analysis`
- `skill.capacity_planning`

### REQUIRED_FOR_CONTEXT
- `skill.counterparty_screening`
  - trigger: supplier onboarding requires integrity or ownership screening input
- `skill.contract_review`
  - trigger: supplier terms must be read for operational obligations and service levels
- `skill.risk_identification`
  - trigger: supply continuity or concentration risk is in assignment scope
- `specialisation.supply_chain_operations`
  - trigger: assignment is end-to-end supply chain rather than single-category sourcing
- `skill.negotiation_preparation`
  - trigger: supplier terms must be prepared for negotiation within delegated limits

### OPTIONAL
- `skill.benchmarking`
- `skill.demand_analysis`
- `skill.process_design`
- `skill.analytics_interpretation`

### PROHIBITED_IN_CONTEXT
- `skill.procurement_route_analysis`
  - basis: Role Card Does Not Own public procurement law, State Aid or tender-regularity conclusions. Procurement route analysis under a public-procurement regime is owned by `role.procurement_state_aid_specialist`; mapping it to commercial sourcing would let a regulated determination be produced by an operational Role.
- `skill.state_aid_screening`
  - basis: Same basis. State Aid presence and compatibility are regulated determinations owned by `role.procurement_state_aid_specialist` and gated by `decision.state_aid_route_adoption`.

### Boundaries
- Support-only boundary vs `role.integrity_due_diligence_specialist`: `skill.counterparty_screening` is contextual here to support supplier onboarding. Screening-hit adjudication, source-of-funds enquiry and the integrity conclusion remain owned by the Integrity Role and gated by `decision.counterparty_acceptance`. The Role Card already carries `review.integrity_due_diligence` for this reason.
- `skill.contract_review` is contextual and operational: contract-law conclusions and dispute positions remain owned by `role.legal_regulatory_lead`.
- Execution of purchase orders and binding supplier commitments is gated by `decision.supplier_award` and `decision.purchase_commitment`.

### Sparse-core rationale
Core is commercial sourcing, supplier and inventory analysis. The two prohibitions are the sharpest boundary in this Role and are drawn from its own Does Not Own clause rather than invented.

## 8. EU Policy & Institutional Affairs Specialist

Role: `role.eu_policy_institutional_affairs_specialist`

### REQUIRED_CORE
- `skill.institutional_mapping`
- `skill.position_mapping`
- `skill.source_verification`
- `skill.source_monitoring`

### REQUIRED_FOR_CONTEXT
- `skill.regulatory_mapping`
  - trigger: assignment requires mapping a legislative file to the regulatory perimeter it changes
- `skill.engagement_strategy_design`
  - trigger: analysis is to inform an engagement approach toward institutions
- `skill.obligation_mapping`
  - trigger: a legislative act imposes obligations that must be enumerated for internal readiness
- `specialisation.eu_institutional_context`
  - trigger: assignment concerns EU institutional process, competence or timetable

### OPTIONAL
- `skill.research_synthesis`
- `skill.change_detection`
- `skill.stakeholder_mapping`
- `skill.meeting_brief_preparation`

### Boundaries
- Support-only boundary vs `role.legal_regulatory_lead`: `skill.regulatory_mapping` and `skill.obligation_mapping` are contextual and support-only. Binding legal interpretation of EU law is excluded by this Role's own Does Not Own clause and remains owned by the Legal & Regulatory Lead under `decision.formal_legal_opinion`.
- Support-only boundary vs `role.eu_grants_programmes_specialist`: policy analysis of a funding instrument is not programme eligibility analysis. Call-level eligibility, application logic and submission remain owned by the EU Grants Role and its programme Packs.
- Adoption or publication of an organisational position is gated by `decision.institutional_position_release`; no mapping reaches it.

### Sparse-core rationale
Core is institutional and position analysis anchored on verified, monitored official sources — the Role's Does Not Own clause makes source discipline the load-bearing competence. Legal and grant capabilities are contextual and support-only to keep two named high-risk boundaries visible.

## 9. EU Enlargement / Governance Specialist

Role: `role.eu_enlargement_governance_specialist`

### REQUIRED_CORE
- `skill.institutional_mapping`
- `skill.source_verification`
- `skill.capability_gap_analysis`
- `skill.benchmarking`

### REQUIRED_FOR_CONTEXT
- `skill.source_monitoring`
  - trigger: accession or reform assessment depends on periodically republished official country assessments
- `skill.roadmap_design`
  - trigger: assignment covers reform sequencing over time
- `skill.regulatory_mapping`
  - trigger: acquis-alignment analysis requires mapping chapters to national regulatory perimeter
- `specialisation.eu_institutional_context`
  - trigger: assignment concerns EU institutional process or instrument alignment
- `specialisation.public_sector_strategy`
  - trigger: counterparty is a public administration undertaking reform

### OPTIONAL
- `skill.research_synthesis`
- `skill.source_comparison`
- `skill.stakeholder_mapping`
- `skill.change_detection`

### Boundaries
- Support-only boundary: `skill.regulatory_mapping` supports alignment analysis only. Legal conclusions on transposition of national or EU law are excluded by the Role Card and remain owned by `role.legal_regulatory_lead`.
- Assessment of a country's compliance for official purposes is outside Role scope; no mapping produces it. `skill.benchmarking` supports multi-country comparison, not an official finding.
- Funding eligibility determinations remain owned by the applicable grant Role.

### Sparse-core rationale
Core is institutional mapping, source discipline, capacity assessment and comparison. The Role reads official assessments rather than producing them, so verification is core and monitoring is contextual on republication cadence.

## 10. Institutional Affairs & Stakeholder Specialist

Role: `role.institutional_affairs_stakeholder_specialist`

### REQUIRED_CORE
- `skill.stakeholder_mapping`
- `skill.stakeholder_segmentation`
- `skill.engagement_strategy_design`
- `skill.consultation_design`

### REQUIRED_FOR_CONTEXT
- `skill.relationship_risk_analysis`
  - trigger: engagement plan depends on relationship, conflict or reputational exposure between parties
- `skill.meeting_brief_preparation`
  - trigger: assignment includes preparing the organisation for institutional meetings
- `skill.position_mapping`
  - trigger: coalition structuring requires mapping the positions of other parties
- `specialisation.eu_institutional_context`
  - trigger: engagement targets EU institutions
- `specialisation.municipal_stakeholder_context`
  - trigger: engagement is with municipal or local-authority stakeholders

### OPTIONAL
- `skill.institutional_mapping`
- `skill.action_tracking`
- `skill.partner_mapping`
- `skill.document_structuring`

### Boundaries
- Support-only boundary vs `role.eu_policy_institutional_affairs_specialist`: `skill.position_mapping` is contextual here for coalition feasibility. Policy file analysis is excluded by this Role's Does Not Own clause where a policy assignment exists.
- `skill.relationship_risk_analysis` is stakeholder relationship risk only. Formal integrity, counterparty or sanctions conclusions remain owned by `role.integrity_due_diligence_specialist` — the Skill Card states this boundary directly.
- Representation before institutions and adoption of positions are gated by `decision.institutional_engagement` and `decision.institutional_position_release`.

### Sparse-core rationale
Core is the stakeholder-map-segment-engage-consult surface intrinsic to every engagement assignment. Position mapping is contextual specifically to keep the Policy Role boundary sharp.

## 11. Programme / Partnership Manager

Role: `role.programme_partnership_manager`

### REQUIRED_CORE
- `skill.partner_mapping`
- `skill.stakeholder_mapping`
- `skill.role_responsibility_mapping`
- `skill.decision_criteria_design`

### REQUIRED_FOR_CONTEXT
- `skill.negotiation_preparation`
  - trigger: partnership or consortium terms must be prepared for negotiation within delegated limits
- `skill.relationship_risk_analysis`
  - trigger: partner portfolio carries dependency, concentration or relationship risk
- `skill.contract_review`
  - trigger: partnership or consortium agreement terms must be read for governance implications
- `specialisation.multi_partner_programme_delivery`
  - trigger: programme spans multiple formal partner organisations
- `specialisation.eu_grant_delivery`
  - trigger: partnership operates inside an EU-funded programme

### OPTIONAL
- `skill.capability_gap_analysis`
- `skill.benefits_realisation_tracking`
- `skill.scenario_analysis`
- `skill.meeting_brief_preparation`

### Boundaries
- Support-only boundary vs `role.consortium_partner_coordination_specialist`: this Role owns partnership strategy, composition and joint governance design. Operational work-package coordination, partner chasing and meeting administration are excluded by its Does Not Own clause and remain the Coordination Role's — `skill.partner_coordination` is deliberately NOT mapped here.
- Support-only boundary vs grant Roles: grant financial compliance and cost eligibility conclusions remain owned by `role.grant_financial_compliance_budget_specialist`.
- `skill.contract_review` is contextual and governance-oriented; signature of partnership or consortium agreements is gated by `decision.partnership_agreement_terms`.

### Sparse-core rationale
Core is partner portfolio, governance structure and decision architecture. The deliberate omission of `skill.partner_coordination` is the mechanism that keeps this Role distinct from Consortium Coordination — a named high-risk boundary.

## 12. EU Programme Implementation & Grant Management Specialist

Role: `role.eu_programme_implementation_grant_management_specialist`

### REQUIRED_CORE
- `skill.obligation_mapping`
- `skill.requirement_traceability`
- `skill.grant_compliance_monitoring`
- `skill.source_verification`

### REQUIRED_FOR_CONTEXT
- `skill.milestone_management`
  - trigger: implementation plan must track reporting and deliverable cycles against the grant agreement
- `skill.document_configuration_control`
  - trigger: audit-trail readiness requires governed document configuration
- `skill.risk_identification`
  - trigger: implementation risk or clawback exposure is in assignment scope
- `skill.source_monitoring`
  - trigger: donor rules or programme guidance may be revised during the implementation period
- `specialisation.eu_grant_delivery`
  - trigger: assignment is delivery of an EU-funded grant

### OPTIONAL
- `skill.deliverable_planning`
- `skill.action_tracking`
- `skill.document_gap_analysis`
- `skill.partner_coordination`

### ALTERNATIVE
- choice set: **Applicable programme rulebook Pack**
  - cardinality: at-least-one-of
  - choice condition: select the Pack matching the programme actually funding the grant under implementation; where an action operates under a framework programme, the action Pack is selected and its declared layering brings the framework Pack with it
  - members:
    - `skill_pack.erasmus_plus`
    - `skill_pack.cove`
    - `skill_pack.life_programme`
    - `skill_pack.horizon_europe`

### Boundaries
- Support-only boundary vs `role.eu_grants_programmes_specialist`: that Role owns pre-award call fit, application logic and submission. This Role owns post-award implementation against an executed grant agreement. `skill.requirement_traceability` here traces grant obligations to implementation actions, not call requirements to an application.
- Support-only boundary vs `role.grant_financial_compliance_budget_specialist`: `skill.grant_compliance_monitoring` is monitoring against obligations. Cost eligibility conclusions and budget compliance certification are excluded by this Role's Does Not Own clause and remain the Grant Financial Compliance Role's.
- Submission to and binding communication with the granting authority are gated by `decision.granting_authority_submission`.

### Sparse-core rationale
Core is obligation mapping, traceability, compliance monitoring and source discipline against an executed agreement. Programme Packs are ALTERNATIVE rather than contextual because exactly one programme rulebook governs a given grant.

## 13. Consortium / Partner Coordination Specialist

Role: `role.consortium_partner_coordination_specialist`

### REQUIRED_CORE
- `skill.partner_coordination`
- `skill.action_tracking`
- `skill.dependency_mapping`
- `skill.meeting_brief_preparation`

### REQUIRED_FOR_CONTEXT
- `skill.milestone_management`
  - trigger: coordination is against a work plan with dated milestones
- `skill.deliverable_planning`
  - trigger: partner contributions must be sequenced toward deliverables
- `specialisation.multi_partner_programme_delivery`
  - trigger: consortium spans multiple formal partner organisations
- `specialisation.eu_grant_delivery`
  - trigger: consortium operates inside an EU-funded programme

### OPTIONAL
- `skill.document_structuring`
- `skill.raid_management`
- `skill.partner_mapping`
- `skill.stakeholder_segmentation`

### PROHIBITED_IN_CONTEXT
- `skill.grant_cost_eligibility_analysis`
  - basis: Role Card Does Not Own states grant compliance, cost eligibility or reporting submission. This Role coordinates without authority; producing a cost eligibility position would convert coordination into compliance ownership. Eligibility remains owned by `role.grant_financial_compliance_budget_specialist`.

### Boundaries
- Support-only boundary vs `role.programme_partnership_manager`: partnership strategy and composition are excluded by this Role's Does Not Own clause. `skill.partner_mapping` is Optional here for coordination awareness only, never for portfolio composition.
- Coordination is explicitly without authority: the Role Card's own Core Skills name it. `decision.consortium_decision_confirmation` records confirmed decisions; it does not let this Role make them.
- Consortium agreement interpretation in dispute is outside Role scope.

### Sparse-core rationale
Core is coordination, tracking, interfaces and meeting discipline. The prohibition is drawn directly from the Does Not Own clause and marks the boundary with grant compliance.

## 14. Grant Financial Compliance / Budget Specialist

Role: `role.grant_financial_compliance_budget_specialist`

### REQUIRED_CORE
- `skill.grant_cost_eligibility_analysis`
- `skill.financial_evidence_reconciliation`
- `skill.obligation_mapping`
- `skill.evidence_indexing`

### REQUIRED_FOR_CONTEXT
- `skill.grant_compliance_monitoring`
  - trigger: budget compliance must be tracked across an implementation period
- `skill.document_gap_analysis`
  - trigger: audit readiness requires identifying missing supporting documentation
- `skill.procurement_route_analysis`
  - trigger: grant rules impose procurement or subcontracting requirements on the beneficiary
- `skill.risk_identification`
  - trigger: clawback or ineligibility exposure must be quantified
- `specialisation.eu_grant_delivery`
  - trigger: assignment is financial compliance for an EU-funded grant
- `skill.variance_analysis`
  - trigger: budget execution must be explained against plan by cost driver

### OPTIONAL
- `skill.source_verification`
- `skill.requirement_traceability`
- `skill.accounting_record_reconciliation`
- `skill.document_configuration_control`

### Boundaries
- Support-only boundary vs `role.accounting_financial_due_diligence_specialist` and `role.fpa_management_finance_specialist`: `skill.accounting_record_reconciliation` is Optional and support-only here, used to tie grant claims to underlying records. Statutory accounting treatment and quality-of-earnings conclusions remain owned by the Accounting / FDD Role; management budgeting remains the FP&A Role's.
- Support-only boundary vs `role.procurement_state_aid_specialist`: `skill.procurement_route_analysis` is contextual and limited to beneficiary compliance with donor procurement rules. Public procurement law and State Aid determinations remain owned by the Procurement / State Aid Role.
- Statutory audit or certification of expenditure is outside Role scope. `decision.grant_financial_claim` and `decision.granting_authority_submission` remain human decision rights.

### Sparse-core rationale
Core is eligibility, evidence reconciliation, obligations and evidence indexing — the Role's own owned surface. Three named boundary Roles are addressed by keeping their capabilities contextual or optional and support-only.

## 15. Deliverables / Reporting Specialist

Role: `role.deliverables_reporting_specialist`

### REQUIRED_CORE
- `skill.document_structuring`
- `skill.technical_writing`
- `skill.requirement_traceability`
- `skill.editorial_quality_control`

### REQUIRED_FOR_CONTEXT
- `skill.deliverable_planning`
  - trigger: deliverables must be sequenced against reporting cycles
- `skill.publication_requirements_validation`
  - trigger: deliverable must meet format, template or annex requirements before release
- `skill.milestone_management`
  - trigger: reporting is tied to dated periodic cycles
- `specialisation.multilingual_content`
  - trigger: deliverables are produced or edited across languages
- `skill_pack.technical_writing_documentation`
  - trigger: governed templates, house conventions and controlled documentation requirements apply beyond the writing technique itself

### OPTIONAL
- `skill.evidence_mapping`
- `skill.document_gap_analysis`
- `skill.source_verification`
- `skill.document_version_control`

### Boundaries
- Support-only boundary: `skill.requirement_traceability` traces deliverables to grant obligations for completeness. It does not produce a compliance conclusion; that remains with `role.grant_financial_compliance_budget_specialist` and `role.eu_programme_implementation_grant_management_specialist`.
- Support-only boundary vs `role.monitoring_evaluation_learning_specialist`: indicator methodology and evaluation conclusions are excluded by this Role's Does Not Own clause. Reporting narrates results; it does not define how they are measured.
- `skill.publication_requirements_validation` is quality control, not independent review, and does not discharge `review.factual_evidence` or `review.grant_compliance`. Submission is gated by `decision.granting_authority_submission`.

### Sparse-core rationale
Core is structured writing, traceability and editorial control. Specialist technical content within a deliverable is consumed from its owning Role, never authored here.

## 16. Learning / VET Design Specialist

Role: `role.learning_vet_design_specialist`

### REQUIRED_CORE
- `skill.learning_outcome_design`
- `skill.assessment_design`
- `skill.training_needs_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.capability_gap_analysis`
  - trigger: curriculum must be derived from an identified competency gap
- `skill.accessibility_analysis`
  - trigger: learning materials or assessment must meet accessibility requirements
- `skill.content_structure_design`
  - trigger: learning pathway requires structured content architecture
- `skill_pack.labour_market_skills_intelligence`
  - trigger: curriculum design must be anchored on labour-market or skills-demand evidence
- `skill_pack.cove`
  - trigger: action or programme context is CoVE and its vocational-excellence logic governs the design

### OPTIONAL
- `skill.document_structuring`
- `skill.indicator_design`
- `skill.survey_research_design`
- `specialisation.multilingual_content`

### Boundaries
- Support-only boundary vs `role.research_market_intelligence_analyst`: `skill_pack.labour_market_skills_intelligence` is contextual here to inform design. Labour-market analysis and skills forecasting are excluded by this Role's Does Not Own clause and remain a Research assignment's output, consumed at its stated state.
- Support-only boundary vs `role.monitoring_evaluation_learning_specialist`: `skill.indicator_design` is Optional and limited to learning-outcome measurement. Evaluation of programme impact is excluded by the Role Card.
- Formal accreditation, certification and awarding of qualifications are outside Role scope. `decision.curriculum_adoption` and `decision.learning_assessment_approval` remain human decision rights.

### Sparse-core rationale
Core is deliberately three: outcomes, assessment and needs analysis are intrinsic to every learning-design assignment, while framework alignment and pathway architecture vary by whether a qualification framework is in play.

## 17. Social Dialogue Specialist

Role: `role.social_dialogue_specialist`

### REQUIRED_CORE
- `skill.social_dialogue_process_design`
- `skill.consultation_design`
- `skill.position_mapping`
- `skill.stakeholder_mapping`

### REQUIRED_FOR_CONTEXT
- `skill.meeting_brief_preparation`
  - trigger: assignment includes preparing parties for dialogue sessions
- `skill.document_structuring`
  - trigger: joint-text or agenda material must be drafted to a governed structure
- `specialisation.social_partner_context`
  - trigger: dialogue involves formal social partners and their representativeness rules
- `specialisation.eu_institutional_context`
  - trigger: dialogue takes place inside EU institutional consultation procedures

### OPTIONAL
- `skill.stakeholder_segmentation`
- `skill.relationship_risk_analysis`
- `skill.source_verification`
- `skill.research_synthesis`

### Boundaries
- Support-only boundary vs `role.institutional_affairs_stakeholder_specialist`: both Roles design consultation. This Role's scope is social partners and tripartite process; institutional stakeholder engagement toward authorities remains the Institutional Affairs Role's. The two are declared adjacent in Phase 3 and the mapping preserves that split.
- Employment law and collective agreement legal conclusions remain owned by `role.legal_regulatory_lead` — the Role Card carries `review.legal_compliance` for that reason.
- Adoption or signature of joint texts is gated by `decision.joint_text_adoption`; no mapping reaches representation of any party.

### Sparse-core rationale
Core is process design, consultation, position analysis and party mapping. Neutrality between parties is the Role's defining constraint, so no capability that could produce an advocacy position is mapped.

## 18. Monitoring, Evaluation & Learning Specialist

Role: `role.monitoring_evaluation_learning_specialist`

### REQUIRED_CORE
- `skill.results_framework_design`
- `skill.indicator_design`
- `skill.monitoring_evaluation_design`

### REQUIRED_FOR_CONTEXT
- `skill.survey_research_design`
  - trigger: monitoring or evaluation requires primary data collection instruments
- `skill.statistical_analysis`
  - trigger: indicator analysis requires quantitative inference beyond descriptive reporting
- `skill.interview_research_design`
  - trigger: evaluation requires structured qualitative enquiry
- `skill.benefits_realisation_tracking`
  - trigger: programme benefits must be tracked against the results framework over time
- `specialisation.eu_grant_delivery`
  - trigger: results framework must satisfy an EU programme's monitoring requirements

### OPTIONAL
- `skill.analytics_interpretation`
- `skill.evidence_mapping`
- `skill.data_quality_rule_design`
- `skill.research_synthesis`

### Boundaries
- Support-only boundary vs `role.data_business_analytics_specialist`: `skill.statistical_analysis` and `skill.analytics_interpretation` are contextual and optional here, applied to indicator data. Business metric definition and decision-support analytics remain the Analytics Role's, whose Does Not Own clause reciprocally excludes MEL indicator methodology. The split is: MEL owns how results are measured, Analytics owns how business performance is measured.
- Independent external evaluation where a separate review mandate is required is excluded by this Role's Does Not Own clause; no mapping creates reviewer identity.
- `decision.results_framework_approval` and `decision.external_mel_use` remain human decision rights.

### Sparse-core rationale
Core is three: results framework, indicators and M&E design. Data collection and statistical treatment are contextual because many MEL assignments design the framework without executing measurement.

## 19. Project Development Lead

Role: `role.project_development_lead`

### REQUIRED_CORE
- `skill.scope_definition`
- `skill.multidisciplinary_integration`
- `skill.roadmap_design`
- `skill.delivery_readiness_assessment`
- `skill.dependency_mapping`

### REQUIRED_FOR_CONTEXT
- `skill.licensing_requirement_analysis`
  - trigger: project requires permits, consents or licensed activity authorisation
- `skill.stage_gate_design`
  - trigger: development is governed by investment or financing gates
- `skill.risk_identification`
  - trigger: development risk must be surfaced across workstreams
- `specialisation.infrastructure_project_preparation`
  - trigger: project preparation for infrastructure, utility or industrial investment
- `skill.negotiation_preparation`
  - trigger: counterparty or land terms must be prepared for negotiation within delegated limits

### OPTIONAL
- `skill.stakeholder_mapping`
- `skill.option_analysis`
- `skill.scenario_analysis`
- `skill.action_tracking`

### Boundaries
- Support-only boundary vs `role.technical_feasibility_lead`: `skill.multidisciplinary_integration` integrates specialist workstreams without absorbing them — the Role Card's own Core Skills say so. Technical feasibility conclusions and basis of design remain the Technical / Feasibility Lead's, consumed at their stated state.
- Support-only boundary vs `role.funding_bankability_architect`: readiness assessment against financing gates does not produce a bankability conclusion. Funding strategy and bankability remain the Funding & Bankability Role's under `decision.funding_strategy_adoption`.
- `skill.licensing_requirement_analysis` is contextual and support-only: statutory permits and regulatory determinations are excluded by the Role Card, and legal conclusions remain `role.legal_regulatory_lead`'s.
- `skill_pack.bid_proposal_management` is deliberately **not** mapped here, and the reason must be stated precisely because an earlier revision overstated it. This Role **does** transmit externally: `artifact.project_definition_document` and `artifact.development_readiness_assessment` both carry a submission transmitting act to lenders, investors or authorities and are COSTLY_TO_REVERSE afterwards, and the Role Card requires tender deadlines and permitting windows to be captured. What the Role does **not** own is a formal competitive response-to-solicitation process — bid/no-bid qualification, a compliance matrix built from a solicitation, multi-author narrative coordination and submission-readiness control against evaluation criteria. That is the Pack's subject, and it belongs to `role.sales_business_development_specialist` and `role.eu_grants_programmes_specialist`, which the Pack Card already lists. The distinction is between submitting a project case and competing in a governed procurement or call, so the mapping was removed rather than the Pack Card widened.
- Investment, financing and land-acquisition decisions are gated by `decision.project_definition_freeze`, `decision.stage_gate_progression` and `decision.land_or_site_commitment`.

### Sparse-core rationale
Core is definition, integration, sequencing, readiness and dependencies — the integrator surface. Every discipline-specific capability is contextual, optional or absent, which is what keeps an integrator Role from becoming a super-agent.

## 20. Sector Technical Expert

Role: `role.sector_technical_expert`

### REQUIRED_CORE
- `skill.benchmarking`
- `skill.technical_option_comparison`
- `skill.technical_risk_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.asset_performance_analysis`
  - trigger: sector opinion concerns operating or performance characteristics of an asset class
- `skill.capacity_sizing`
  - trigger: sector input concerns sizing conventions or capacity norms
- `skill.source_verification`
  - trigger: sector benchmarks or standards must be traced to an authoritative and current source

### OPTIONAL
- `skill.feasibility_analysis`
- `skill.technical_requirements_definition`
- `skill.research_synthesis`
- `skill.source_comparison`

### ALTERNATIVE
- choice set: **Sector specialisation**
  - cardinality: at-least-one-of
  - choice condition: select the specialisation matching the assignment's sector or asset class; more than one applies only where the project genuinely spans sectors, and where none matches, the assignment lacks a sector basis and must be returned rather than answered from general engineering knowledge
  - members:
    - `specialisation.solar`
    - `specialisation.bess`
    - `specialisation.water`
    - `specialisation.waste`
    - `specialisation.transport`
    - `specialisation.industrial`
    - `specialisation.health`
    - `specialisation.real_estate`

### PROHIBITED_IN_CONTEXT
- `skill.design_basis_definition`
  - basis: Role Card Does Not Own states basis of design ownership. The Sector Expert critiques and advises on sector assumptions; defining the design basis is owned by `role.technical_feasibility_lead` and frozen under `decision.technical_basis_freeze`. Mapping it here would let expert advice become design ownership.

### Boundaries
- Support-only boundary vs `role.technical_feasibility_lead`: the project feasibility conclusion is excluded by this Role's Does Not Own clause. `skill.feasibility_analysis` is Optional and used only to test whether a sector norm transfers, never to reach the feasibility conclusion.
- The Role Card records no default decision right — it inherits from the consuming workflow. No mapping introduces one.
- Cost, commercial, financial, legal and ESG conclusions are outside Role scope.

### Sparse-core rationale
Core is deliberately three, because this Role's value is depth attached through a sector specialisation rather than breadth of technique. The ALTERNATIVE sector set is the mechanism, and the prohibition prevents advice becoming design ownership.

## 21. Commercial & Demand Specialist

Role: `role.commercial_demand_specialist`

### REQUIRED_CORE
- `skill.demand_analysis`
- `skill.market_sizing`
- `skill.pricing_analysis`
- `skill.commercial_structure_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.tariff_analysis`
  - trigger: revenue is set through a regulated or contracted tariff; absorbs the retired `specialisation.tariff_modelling`
- `skill.offtake_analysis`
  - trigger: revenue depends on offtake or purchase agreements with identified counterparties
- `skill.affordability_analysis`
  - trigger: end users are price-constrained and affordability bounds achievable tariff; absorbs the retired `specialisation.affordability`
- `skill.scenario_analysis`
  - trigger: demand basis must be expressed across materially different demand futures
- `specialisation.regulated_market`
  - trigger: market is subject to regulated pricing or access rules
- `specialisation.public_service_demand`
  - trigger: demand is for a public service with non-commercial drivers
- `skill.revenue_model_design`
  - trigger: revenue structure itself must be designed rather than applied

### OPTIONAL
- `skill.market_segmentation`
- `skill.competitor_analysis`
- `skill.source_verification`

### Boundaries
- Support-only boundary vs `role.financial_modelling_specialist`: this Role produces the demand and revenue basis as an input artifact. Financial model construction and return metrics are excluded by its Does Not Own clause. `decision.demand_basis_acceptance` gates reliance on the basis.
- Support-only boundary vs `role.funding_bankability_architect`: financing structure and bankability conclusions are outside Role scope.
- Contract drafting and legal conclusions on offtake agreements remain owned by `role.legal_regulatory_lead`; regulatory tariff determinations are outside Role scope.

### Sparse-core rationale
Core is demand, sizing, pricing and commercial structure. The four Specialisations here are the densest Specialisation cluster in Wave 2 and are all bounded-context selectors, not authority.

## 22. CAPEX / Cost Engineering Specialist

Role: `role.capex_cost_engineering_specialist`

### REQUIRED_CORE
- `skill.capex_estimation`
- `skill.opex_estimation`
- `skill.cost_estimate_reconciliation`
- `skill.benchmarking`

### REQUIRED_FOR_CONTEXT
- `skill.risk_quantification`
  - trigger: contingency must be derived from quantified risk rather than a flat allowance
- `skill.capacity_sizing`
  - trigger: quantities must be derived from sizing rather than supplied
- `specialisation.infrastructure_project_preparation`
  - trigger: estimate supports infrastructure or industrial project preparation

### OPTIONAL
- `skill.technical_option_comparison`
- `skill.source_verification`
- `skill.scenario_analysis`
- `skill.sensitivity_analysis`

### ALTERNATIVE
- choice set: **Sector specialisation for cost basis**
  - cardinality: at-least-one-of
  - choice condition: select the specialisation matching the asset class being estimated, because unit rates, quantity conventions and contingency norms do not transfer across sectors; where none matches, the benchmark basis must be stated as unverified rather than assumed
  - members:
    - `specialisation.solar`
    - `specialisation.bess`
    - `specialisation.water`
    - `specialisation.waste`
    - `specialisation.transport`
    - `specialisation.industrial`
    - `specialisation.health`
    - `specialisation.real_estate`

### Boundaries
- This Role is the owner of `skill.capex_estimation` and `skill.opex_estimation`. The Wave 1 remediation removed both from `role.technical_feasibility_lead`; Wave 2 maps them here as REQUIRED_CORE, which is where the capability belongs.
- `skill.lifecycle_cost_analysis` is deliberately **not** mapped here. Its reviewed Skill Card scopes it to support-only technical-option comparison by `role.technical_feasibility_lead` and explicitly excludes this Role as a consumer, on the ground that this Role owns the cost inputs that Skill consumes. Whole-life estimating is performed through this Role's own owned capabilities — `skill.capex_estimation`, `skill.opex_estimation` and `skill.cost_estimate_reconciliation` — and the support-only Skill is not recreated under another ID.
- Support-only boundary vs `role.financial_modelling_specialist`: financial model construction and return metrics remain the Financial Modelling Role's; cost estimates are supplied as inputs at their declared accuracy class.
- Technical basis of design and scope definition remain owned by `role.technical_feasibility_lead`; procurement award remains outside Role scope. `decision.cost_estimate_acceptance` and `decision.budget_approval` are human decision rights.

### Sparse-core rationale
Core is estimation, reconciliation and benchmarking. The sector ALTERNATIVE set exists because cost benchmarks are the least transferable engineering artefact across asset classes.

## 23. Asset O&M / Technical Operations Specialist

Role: `role.asset_om_technical_operations_specialist`

### REQUIRED_CORE
- `skill.om_strategy_design`
- `skill.asset_performance_analysis`
- `skill.capacity_planning`

### REQUIRED_FOR_CONTEXT
- `skill.technical_risk_analysis`
  - trigger: operational risk and failure modes are in assignment scope
- `skill.sop_design`
  - trigger: operating procedures must be documented for the operating model

### OPTIONAL
- `skill.contract_review`
- `skill.benchmarking`
- `skill.risk_mitigation_design`
- `skill.technical_option_comparison`

### ALTERNATIVE
- choice set: **Sector specialisation for operating basis**
  - cardinality: at-least-one-of
  - choice condition: select the specialisation matching the asset class, because failure modes, maintenance regimes and availability conventions are asset-class specific; where none matches, availability assumptions must be reported as unbenchmarked
  - members:
    - `specialisation.solar`
    - `specialisation.bess`
    - `specialisation.water`
    - `specialisation.waste`
    - `specialisation.transport`
    - `specialisation.industrial`
    - `specialisation.health`
    - `specialisation.real_estate`

### PROHIBITED_IN_CONTEXT
- `skill.opex_estimation`
  - basis: **Trigger-conditional prohibition.** It applies only where a dedicated cost-engineering assignment exists, or where cost-estimate ownership is otherwise assigned to `role.capex_cost_engineering_specialist`. The basis is the Role Card's Does Not Own clause, which excludes OPEX cost estimation figures *where a cost engineering assignment exists*; the prohibition is scoped to exactly that condition and is not asserted more broadly than the Role Card supports. Outside that condition this registry asserts no prohibition. In every case the Role's own approved ownership of operating cost drivers, availability and lifecycle basis is unaffected.

### Boundaries
- Support-only boundary vs `role.operations_service_delivery_specialist`: corporate operating-model design is excluded by this Role's Does Not Own clause. This Role owns asset O&M strategy for infrastructure and industrial assets; the Operations Role owns the corporate service model. The two Role Cards exclude each other reciprocally.
- Support-only boundary vs `role.capex_cost_engineering_specialist`: this Role produces `artifact.operating_cost_driver_definition`, not cost figures — see the prohibition above.
- `skill.lifecycle_cost_analysis` is deliberately **not** mapped here. Its reviewed Skill Card scopes it to support-only technical-option comparison by `role.technical_feasibility_lead` and explicitly excludes this Role as a consumer. Lifecycle intervention and replacement logic is carried by this Role's own owned capabilities — `skill.om_strategy_design` and `skill.asset_performance_analysis`, producing `artifact.availability_and_lifecycle_basis` — and the support-only Skill is not recreated under another ID.
- Technical feasibility and basis of design remain `role.technical_feasibility_lead`'s; safety certification and operating licences are outside Role scope.

### Sparse-core rationale
Core is three: O&M strategy, asset performance and resourcing. The conditional prohibition on OPEX estimation is taken verbatim from the Role Card and is the sharpest live boundary in the technical cluster.

## 24. Economic / CBA Specialist

Role: `role.economic_cba_specialist`

### REQUIRED_CORE
- `skill.discounted_cash_flow_analysis`
- `skill.assumption_analysis`
- `skill.sensitivity_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.option_analysis`
  - trigger: appraisal requires a defined counterfactual and option set
- `skill.scenario_analysis`
  - trigger: economic result depends on materially different future states
- `skill.risk_quantification`
  - trigger: appraisal guidance requires probabilistic risk analysis
- `skill.source_verification`
  - trigger: appraisal guidance, conversion factors or unit values must be traced to a current authoritative source
- `specialisation.public_service_demand`
  - trigger: benefits accrue through a public service with non-market users

### OPTIONAL
- `skill.demand_analysis`
- `skill.statistical_analysis`
- `skill.benchmarking`
- `skill.document_structuring`

### ALTERNATIVE
- choice set: **Appraisal method**
  - cardinality: one-of
  - choice condition: use `skill.economic_cost_benefit_analysis` where benefits can be credibly monetised and compared against costs in the same unit; use `skill.cost_effectiveness_analysis` where the benefit is fixed, mandated or cannot be credibly monetised and the question is least-cost achievement. Selecting both for the same appraisal question is a methodological error and must be escalated rather than averaged
  - members:
    - `skill.economic_cost_benefit_analysis`
    - `skill.cost_effectiveness_analysis`

### Boundaries
- Support-only boundary vs `role.financial_modelling_specialist`: economic appraisal is not financial modelling. `skill.discounted_cash_flow_analysis` is used here on economic flows at a social discount rate; financial model construction and financial return metrics are excluded by this Role's Does Not Own clause.
- Support-only boundary vs `role.commercial_demand_specialist`: `skill.demand_analysis` is Optional here. Demand forecasting methodology is excluded by the Role Card and consumed from the Commercial & Demand Role at its stated state.
- Environmental impact assessment conclusions remain `role.esg_es_specialist`'s. Funding gap determination by the granting authority is outside Role scope; `decision.economic_appraisal_acceptance` gates reliance.

### Sparse-core rationale
Core is the appraisal-and-uncertainty surface. The appraisal method is **not** in core: it sits solely in the one-of ALTERNATIVE set, because exactly one of the two methods governs a given appraisal question and no capability may be simultaneously universally required and mutually exclusive with an alternative. An earlier draft listed `skill.economic_cost_benefit_analysis` in both places, which was logically incoherent; the ALTERNATIVE set is its correct and only home, and the choice condition decides which method applies.

## 25. FP&A / Management Finance Specialist

Role: `role.fpa_management_finance_specialist`

### REQUIRED_CORE
- `skill.cash_flow_modelling`
- `skill.financial_evidence_reconciliation`
- `skill.variance_analysis`
- `skill.metric_definition`
- `skill.scenario_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.working_capital_modelling`
  - trigger: liquidity planning depends on working-capital movements
- `skill.financial_statement_modelling`
  - trigger: management reporting must reconcile to a three-statement view
- `skill.accounting_record_reconciliation`
  - trigger: forecasts or variance analysis must tie back to underlying accounting records
- `skill.dashboard_design`
  - trigger: management reporting is delivered through a recurring reporting surface
- `skill.sensitivity_analysis`
  - trigger: plan must be tested against driver variation

### OPTIONAL
- `skill.analytics_interpretation`
- `skill.capacity_planning`
- `skill.benchmarking`
- `skill.statistical_analysis`

### Boundaries
- Support-only boundary vs `role.accounting_financial_due_diligence_specialist`: `skill.accounting_record_reconciliation` is contextual and support-only here. Statutory accounts, accounting policy and quality-of-earnings conclusions are excluded by this Role's Does Not Own clause and remain the Accounting / FDD Role's.
- Support-only boundary vs `role.data_business_analytics_specialist`: `skill.metric_definition` is core here for financial KPIs only. Business analytics metric definition and its `decision.metric_definition_adoption` remain the Analytics Role's where a separate analytics assignment exists.
- Project finance and transaction models remain `role.financial_modelling_specialist`'s; treasury execution, hedging and tax positions are outside Role scope.

### Sparse-core rationale
Core is cash, reconciliation, KPI definition and scenario planning. Statement modelling is contextual because many management-finance assignments are cash and driver focused without a full three-statement build.

## 26. Funding & Bankability Architect

Role: `role.funding_bankability_architect`

### REQUIRED_CORE
- `skill.funding_source_mapping`
- `skill.bankability_gap_analysis`
- `skill.financing_scenario_analysis`
- `skill.risk_allocation_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.financing_term_analysis`
  - trigger: indicative terms or instrument conditions must be analysed for financeability
- `skill.project_finance_ratio_analysis`
  - trigger: financeability depends on coverage ratios from a debt model
- `skill.roadmap_design`
  - trigger: financing readiness must be sequenced toward a target close
- `skill_pack.project_finance_metrics`
  - trigger: financing structure is project finance or a lender-facing debt model governs coverage conventions
- `skill_pack.ifi_financial_appraisal`
  - trigger: an IFI or DFI appraisal method applies and no institution-specific Pack governs

### OPTIONAL
- `skill.scenario_analysis`
- `skill.option_analysis`
- `skill.contract_review`
- `skill.source_verification`

### ALTERNATIVE
- choice set: **Institution Pack where a financing route is pursued**
  - cardinality: at-least-one-of
  - choice condition: select the Pack matching the institution actually being pursued as a financing route; where the route is commercial only, no institution Pack applies and `skill_pack.ifi_financial_appraisal` is not a substitute for one
  - members:
    - `skill_pack.eib`
    - `skill_pack.ebrd`
    - `skill_pack.world_bank`
    - `skill_pack.ifc`
    - `skill_pack.bgk`
    - `skill_pack.investeu`
    - `skill_pack.ukraine_facility`

### Boundaries
- Support-only boundary vs `role.project_finance_transaction_specialist`: this Role designs the financing strategy and assesses bankability; transaction execution, lender processes and documentation to financial close are excluded by its Does Not Own clause and remain the Transaction Role's under `decision.financial_close`.
- Support-only boundary vs `role.financial_modelling_specialist`: `skill.project_finance_ratio_analysis` is contextual and reads model outputs. Financial model construction is excluded by the Role Card. Where `skill_pack.project_finance_metrics` is active, the Pack governs ratio conventions and the direct Skill mapping is not duplicated — see the duplicate-activation note.
- Credit decisions of any financier are outside Role scope. `decision.funding_strategy_adoption`, `decision.financing_route_selection` and `decision.lender_engagement` remain human decision rights.

### Sparse-core rationale
Core is sources, gaps, scenarios and risk allocation from a financeability perspective. The institution ALTERNATIVE set is the second genuine at-least-one-of in Wave 2 and mirrors the sector sets in the technical cluster.

## 27. Project Finance / Transaction Specialist

Role: `role.project_finance_transaction_specialist`

### REQUIRED_CORE
- `skill.financing_term_analysis`
- `skill.risk_allocation_analysis`
- `skill.milestone_management`
- `skill.action_tracking`

### REQUIRED_FOR_CONTEXT
- `skill.project_finance_ratio_analysis`
  - trigger: covenant and coverage testing is required against a debt model
- `skill.contract_review`
  - trigger: financing documentation must be read for structure, conditions and covenant mechanics
- `skill.dependency_mapping`
  - trigger: conditions precedent must be tracked across interdependent workstreams
- `skill_pack.project_finance_metrics`
  - trigger: financing structure is project finance or a lender-facing debt model governs coverage conventions
- `skill.evidence_indexing`
  - trigger: closing requires assembled and indexed condition-precedent evidence
- `skill.negotiation_preparation`
  - trigger: term sheet or financing document positions must be prepared for negotiation within delegated limits

### OPTIONAL
- `skill.scenario_analysis`
- `skill.risk_identification`
- `skill.document_gap_analysis`
- `skill.source_verification`

### ALTERNATIVE
- choice set: **Institution Pack where an institutional lender participates**
  - cardinality: at-least-one-of
  - choice condition: select the Pack for each institution participating in the financing, because appraisal, safeguard and documentation requirements differ by institution; where financing is commercial only, no institution Pack applies
  - members:
    - `skill_pack.eib`
    - `skill_pack.ebrd`
    - `skill_pack.world_bank`
    - `skill_pack.ifc`
    - `skill_pack.bgk`
    - `skill_pack.investeu`
    - `skill_pack.ukraine_facility`

### Boundaries
- Support-only boundary vs `role.legal_regulatory_lead`: `skill.contract_review` is contextual and structural here. Legal drafting and legal conclusions on financing documentation are excluded by this Role's Does Not Own clause — the Role Card carries `review.legal_compliance` for that reason.
- Support-only boundary vs `role.funding_bankability_architect`: strategy and bankability remain that Role's; this Role executes the transaction process toward close.
- Negotiation, commitment and execution of financing documents, and lender credit decisions, are outside Role scope. `decision.financing_terms_acceptance` and `decision.financial_close` are human decision rights.

### Sparse-core rationale
Core is terms, risk allocation and closing discipline — milestone and action tracking are core here, unusually, because condition-precedent management is the Role's defining operational surface.

## 28. IFI / DFI Project Preparation Specialist

Role: `role.ifi_dfi_project_preparation_specialist`

### REQUIRED_CORE
- `skill.requirement_traceability`
- `skill.document_gap_analysis`
- `skill.obligation_mapping`
- `skill.evidence_indexing`

### REQUIRED_FOR_CONTEXT
- `skill.source_verification`
  - trigger: institutional policies and appraisal guidance must be traced to a current authoritative version
- `skill.source_monitoring`
  - trigger: institutional policies may be revised during a preparation cycle
- `skill.esg_screening`
  - trigger: the institution's safeguard policies require an environmental and social screening input
- `skill_pack.ifi_financial_appraisal`
  - trigger: a generic IFI appraisal method applies and no institution-specific Pack governs the appraisal
- `specialisation.ifi_esg_safeguards`
  - trigger: institutional safeguard policies govern the environmental and social workstream
- `specialisation.infrastructure_project_preparation`
  - trigger: preparation is for infrastructure, utility or industrial investment

### OPTIONAL
- `skill.dependency_mapping`
- `skill.action_tracking`
- `skill.risk_identification`
- `skill.document_structuring`

### ALTERNATIVE
- choice set: **Institution Pack**
  - cardinality: at-least-one-of
  - choice condition: select the Pack for the institution whose appraisal the package targets; this Role exists to prepare against a named institution's criteria, so an assignment with no institution identified lacks a basis and must be returned rather than prepared against generic expectations
  - members:
    - `skill_pack.eib`
    - `skill_pack.ebrd`
    - `skill_pack.world_bank`
    - `skill_pack.ifc`
    - `skill_pack.bgk`
    - `skill_pack.investeu`
    - `skill_pack.ukraine_facility`

### Boundaries
- Support-only boundary vs `role.esg_es_specialist`: `skill.esg_screening` and `specialisation.ifi_esg_safeguards` are contextual and support-only, used to track safeguard completeness. E&S risk conclusions, impact assessment and action plans remain the ESG / E&S Role's under `decision.es_assessment_acceptance`.
- Support-only boundary vs `role.project_finance_transaction_specialist`: negotiation of financing terms is excluded by this Role's Does Not Own clause.
- The institution's appraisal conclusion and credit decision are outside Role scope. `decision.ifi_submission` and `decision.lender_engagement` remain human decision rights.
- Specialist conclusions across technical, ESG, legal, economic and financial workstreams are consumed at their stated state; this Role tracks completeness, it does not author them.

### Sparse-core rationale
Core is traceability, gap tracking, obligations and evidence indexing — a completeness-control surface. Every substantive workstream capability is contextual and support-only, which is what stops a preparation Role becoming an appraisal Role.

## 29. PPP / Concession Specialist

Role: `role.ppp_concession_specialist`

### REQUIRED_CORE
- `skill.risk_allocation_analysis`
- `skill.commercial_structure_analysis`
- `skill.option_analysis`
- `skill.contract_review`

### REQUIRED_FOR_CONTEXT
- `skill.affordability_analysis`
  - trigger: the public authority's affordability envelope bounds the structure
- `skill.procurement_route_analysis`
  - trigger: the concession must be awarded through a defined procurement regime
- `skill.project_finance_ratio_analysis`
  - trigger: structure must be tested for financeability against coverage ratios
- `skill_pack.project_finance_metrics`
  - trigger: financing structure is project finance and coverage conventions govern
- `specialisation.public_service_demand`
  - trigger: the concession delivers a public service with non-commercial demand drivers
- `specialisation.regulated_market`
  - trigger: the concession operates in a regulated pricing or access regime

### OPTIONAL
- `skill.scenario_analysis`
- `skill.benchmarking`
- `skill.risk_mitigation_design`
- `skill.demand_analysis`

### Boundaries
- Support-only boundary vs `role.legal_regulatory_lead`: `skill.contract_review` is core here for structural term architecture, but legal drafting and legal conclusions on concession documentation are excluded by this Role's Does Not Own clause. The Role Card carries `review.legal_compliance` for that reason.
- Support-only boundary vs `role.procurement_state_aid_specialist`: `skill.procurement_route_analysis` is contextual and structural. Procurement conduct, award decisions and State Aid determinations remain the Procurement / State Aid Role's.
- Support-only boundary vs `role.project_finance_transaction_specialist`: financing execution is outside Role scope; `skill.project_finance_ratio_analysis` here tests structure, it does not run a transaction.
- Financial model construction and the public authority's affordability or fiscal decision are outside Role scope.

### Sparse-core rationale
Core is risk allocation, structure, options and contract architecture. Three named high-risk boundaries — Legal, Procurement, Project Finance — are each addressed by keeping the neighbouring capability contextual and support-only.

## 30. Tax Specialist

Role: `role.tax_specialist`

### REQUIRED_CORE
- `skill.tax_position_analysis`
- `skill.jurisdiction_mapping`
- `skill.legal_issue_spotting`
- `skill.source_verification`

### REQUIRED_FOR_CONTEXT
- `skill.regulatory_mapping`
  - trigger: tax treatment depends on a regulatory or treaty perimeter that must be mapped
- `skill.risk_identification`
  - trigger: tax uncertainty and disclosure exposure must be registered
- `skill.source_monitoring`
  - trigger: applicable tax law or treaty position may change during the engagement period
- `specialisation.cross_border_regulatory`
  - trigger: structure spans more than one jurisdiction

### OPTIONAL
- `skill.financial_statement_modelling`
- `skill.scenario_analysis`
- `skill.contract_review`
- `skill.obligation_mapping`

### Boundaries
- Support-only boundary vs `role.accounting_financial_due_diligence_specialist`: accounting policy and tax accounting entries are excluded by this Role's Does Not Own clause. `skill.financial_statement_modelling` is Optional here only to express tax effects, never to form an accounting treatment conclusion.
- Support-only boundary vs `role.legal_regulatory_lead`: `skill.legal_issue_spotting` is core here for tax issues specifically. Binding tax opinions where a licensed professional is required are excluded by the Role Card and gated by `decision.formal_tax_opinion`.
- Filing, certification and representation before tax authorities are outside Role scope; adopting a tax position is gated by `decision.tax_position_adoption`.

### Sparse-core rationale
Core is tax analysis, jurisdiction, issue spotting and source discipline. The licensed-professional boundary is the Role's defining constraint and no mapping approaches it.

## 31. Accounting / Financial Due Diligence Specialist

Role: `role.accounting_financial_due_diligence_specialist`

### REQUIRED_CORE
- `skill.accounting_record_reconciliation`
- `skill.financial_evidence_reconciliation`
- `skill.financial_statement_modelling`
- `skill.evidence_gap_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.working_capital_modelling`
  - trigger: net debt and working-capital analysis is in diligence scope
- `skill.source_verification`
  - trigger: statutory accounts and supporting schedules must be traced to authoritative and current versions
- `skill.risk_identification`
  - trigger: red flags must be registered as exposures for the transaction
- `skill.document_gap_analysis`
  - trigger: diligence completeness depends on identifying missing schedules or records

### OPTIONAL
- `skill.benchmarking`
- `skill.scenario_analysis`
- `skill.analytics_interpretation`
- `skill.evidence_indexing`

### Boundaries
- Support-only boundary vs `role.tax_specialist`: tax positions and computations are excluded by this Role's Does Not Own clause and remain the Tax Role's under `decision.tax_position_adoption`.
- Support-only boundary vs `role.fpa_management_finance_specialist`: this Role reconciles management, statutory and transaction bases for diligence. Management budgeting and forecasting remain the FP&A Role's.
- Audit opinions and any form of assurance conclusion are excluded by the Role Card — no mapping creates reviewer identity. Valuation conclusions are outside Role scope. `decision.due_diligence_reliance` gates reliance on findings.

### Sparse-core rationale
Core is reconciliation, statement analysis and evidence-gap discipline. The assurance boundary is absolute: the Role produces findings and scope limitations, never an opinion.

## 32. Insurance / Risk Transfer Specialist

Role: `role.insurance_risk_transfer_specialist`

### REQUIRED_CORE
- `skill.insurance_programme_analysis`
- `skill.risk_identification`

### REQUIRED_FOR_CONTEXT
- `skill.contract_review`
  - trigger: contractual or lender insurance requirements must be read from the underlying agreements
- `skill.risk_quantification`
  - trigger: exposure valuation requires quantified loss scenarios
- `skill.risk_allocation_analysis`
  - trigger: insurance sits inside a wider contractual risk allocation
- `specialisation.infrastructure_project_preparation`
  - trigger: cover is being structured for infrastructure or industrial project preparation

### OPTIONAL
- `skill.benchmarking`
- `skill.scenario_analysis`
- `skill.source_verification`
- `skill.document_gap_analysis`

### Boundaries
- Support-only boundary vs `role.enterprise_project_risk_specialist`: the enterprise risk register methodology is excluded by this Role's Does Not Own clause. `skill.risk_identification` and `skill.risk_quantification` are used here for insurable exposure only; the risk register and its methodology remain the Enterprise Risk Role's, and reciprocally that Role's card excludes insurance programme design.
- Support-only boundary vs `role.legal_regulatory_lead`: `skill.contract_review` is contextual for insurance clause interpretation. Policy wording drafting and legal interpretation of coverage disputes are excluded by the Role Card.
- Placement, broking, binding and regulated insurance advice are outside Role scope. `decision.insurance_programme_adoption`, `decision.insurance_placement` and `decision.lender_engagement` are human decision rights.

### Sparse-core rationale
Core is three: programme analysis, gap analysis and exposure identification. Quantification is contextual because many assignments assess adequacy against requirements without a modelled loss distribution.

## 33. Procurement / State Aid Specialist

Role: `role.procurement_state_aid_specialist`

### REQUIRED_CORE
- `skill.procurement_route_analysis`
- `skill.state_aid_screening`
- `skill.regulatory_mapping`
- `skill.compliance_gap_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.jurisdiction_mapping`
  - trigger: national implementing rules differ from the EU framework and must be identified
- `skill.obligation_mapping`
  - trigger: procurement or aid obligations must be enumerated for a beneficiary or authority
- `skill.decision_criteria_design`
  - trigger: tender evaluation criteria must be constructed
- `skill.source_monitoring`
  - trigger: applicable directives, thresholds or exemption regulations may be revised during the engagement
- `specialisation.public_procurement`
  - trigger: a public procurement regime applies to the award
- `specialisation.state_aid`
  - trigger: State Aid presence, compatibility or exemption route is in question

### OPTIONAL
- `skill.source_verification`
- `skill.requirement_traceability`
- `skill.risk_identification`
- `skill.contract_review`

### Boundaries
- Support-only boundary vs `role.legal_regulatory_lead`: this Role owns procurement and State Aid regime analysis. Binding legal opinions where licensed counsel is required are excluded by its Does Not Own clause and gated by `decision.formal_legal_opinion`, which appears on both Role Cards.
- Support-only boundary vs `role.supply_chain_procurement_operations_specialist`: commercial sourcing, supplier management and category strategy are excluded by this Role's Does Not Own clause. The reciprocal prohibition on that Role's mapping completes the boundary from both sides.
- Conduct of a procurement, award decisions and notification to the Commission or national authorities are outside Role scope.

### Sparse-core rationale
Core is route analysis, aid screening, regulatory perimeter and gap analysis. This Role and Supply Chain & Procurement Operations are separated by a matched pair of boundary statements plus two prohibitions on the operational side.

## 34. ESG / E&S Specialist

Role: `role.esg_es_specialist`

### REQUIRED_CORE
- `skill.esg_screening`
- `skill.environmental_social_gap_analysis`
- `skill.risk_mitigation_design`

### REQUIRED_FOR_CONTEXT
- `skill.regulatory_mapping`
  - trigger: applicable environmental or social law must be mapped to the project perimeter
- `skill.stakeholder_mapping`
  - trigger: grievance mechanism or engagement design requires an affected-party map
- `skill.consultation_design`
  - trigger: safeguard standards require structured stakeholder consultation
- `skill.risk_identification`
  - trigger: E&S risk must be registered alongside other project risk
- `specialisation.ifi_esg_safeguards`
  - trigger: an IFI or DFI safeguard policy framework governs the assessment
- `specialisation.project_es_risk`
  - trigger: assignment is project-level environmental and social risk rather than corporate sustainability
- `skill.source_monitoring`
  - trigger: safeguard standards or applicable environmental law may be revised during the assessment period

### OPTIONAL
- `skill.survey_research_design`
- `skill.source_verification`
- `skill.indicator_design`
- `skill.document_structuring`

### Boundaries
- Support-only boundary vs `role.enterprise_project_risk_specialist`: `skill.risk_identification` is contextual here for E&S risk feeding the wider register. Risk methodology, taxonomy and the register itself remain the Enterprise Risk Role's, whose card reciprocally excludes ESG impact assessment and safeguard conclusions.
- Support-only boundary vs `role.legal_regulatory_lead`: legal conclusions on environmental law are excluded by this Role's Does Not Own clause; `skill.regulatory_mapping` is contextual and perimeter-only.
- Statutory environmental impact assessment approval, permitting decisions and lender safeguard categorisation determinations are outside Role scope. Assurance over sustainability disclosures is excluded — `decision.es_assessment_acceptance`, `decision.es_action_plan_commitment` and `decision.external_reporting_release` are human decision rights.

### Sparse-core rationale
Core is three: screening, gap analysis and mitigation design. Consultation and stakeholder capabilities are contextual because they activate on safeguard standards rather than on every assignment.

## 35. Enterprise / Project Risk Specialist

Role: `role.enterprise_project_risk_specialist`

### REQUIRED_CORE
- `skill.risk_identification`
- `skill.risk_register_design`
- `skill.risk_quantification`
- `skill.risk_mitigation_design`
- `skill.risk_control_design`

### REQUIRED_FOR_CONTEXT
- `skill.scenario_analysis`
  - trigger: risk analysis requires scenario construction beyond a register
- `skill.sensitivity_analysis`
  - trigger: quantified risk must be tested against driver variation
- `skill.statistical_analysis`
  - trigger: probabilistic risk analysis with correlation handling is required
- `skill.dashboard_design`
  - trigger: risk reporting is delivered through a recurring governance surface

### OPTIONAL
- `skill.indicator_design`
- `skill.benchmarking`
- `skill.dependency_mapping`
- `skill.analytics_interpretation`

### Boundaries
- Support-only boundary — the defining one for this Role: specialist conclusions in the domains giving rise to the risks are excluded by its Does Not Own clause. This Role owns the method and the register; the substance of each risk is owned by the discipline Role that raised it. No mapping here produces a technical, financial, legal or E&S conclusion.
- Support-only boundary vs `role.insurance_risk_transfer_specialist`: insurance programme design is excluded by this Role's Does Not Own clause, matching that Role's reciprocal exclusion of risk register methodology.
- Support-only boundary vs `role.esg_es_specialist`: ESG impact assessment and safeguard conclusions are excluded by the Role Card.
- Risk acceptance and appetite setting are human decision rights: `decision.risk_acceptance` and `decision.risk_appetite_setting`.

### Sparse-core rationale
Core is five — the widest core in Wave 2 — because methodology, register, quantification, mitigation and control design are all intrinsic to this Role and none is contextual. The compensating discipline is that every domain capability is absent.

## 36. Integrity / Due Diligence Specialist

Role: `role.integrity_due_diligence_specialist`

### REQUIRED_CORE
- `skill.counterparty_screening`
- `skill.sanctions_screening`
- `skill.source_verification`
- `skill.evidence_mapping`

### REQUIRED_FOR_CONTEXT
- `skill.relationship_risk_analysis`
  - trigger: ownership or control mapping surfaces relationship and influence exposure
- `skill.risk_identification`
  - trigger: integrity and corruption risk must be registered for the engagement
- `skill.source_comparison`
  - trigger: conflicting registry or adverse-media accounts must be reconciled
- `specialisation.integrity_sanctions_context`
  - trigger: sanctions, PEP or watchlist context governs the screening perimeter
- `skill.source_monitoring`
  - trigger: counterparty status may change during an ongoing relationship and re-screening applies

### OPTIONAL
- `skill.research_synthesis`
- `skill.evidence_gap_analysis`
- `skill.document_gap_analysis`
- `skill.evidence_indexing`

### Boundaries
- This Role is the owner of the integrity conclusion. The Wave 1 remediation removed `skill.integrity_due_diligence` from the universe precisely because bundling this methodology into one Skill created a hidden Role. Wave 2 maps its genuine reusable components — screening, verification, evidence mapping — while the conclusion remains this Role's and is not obtainable by activating them elsewhere.
- Support-only boundary vs `role.legal_regulatory_lead`: legal conclusions on sanctions or AML obligations are excluded by this Role's Does Not Own clause.
- Decisions to onboard, reject, exit or report a counterparty, and suspicious activity reporting, are outside Role scope: `decision.counterparty_acceptance`, `decision.integrity_escalation` and `decision.regulatory_reporting` are human decision rights.
- No mapping produces a criminal or civil determination about any person. Unverified allegations are handled as UNKNOWN evidence, never as findings.

### Sparse-core rationale
Core is screening, verification and evidence mapping — the components that were correctly separated out of the retired bundled Skill. This Role is the clearest demonstration that decomposing a hidden Role into reusable Skills preserves the conclusion's ownership.

## 37. Data Protection / GDPR Specialist

Role: `role.data_protection_gdpr_specialist`

### REQUIRED_CORE
- `skill.privacy_impact_analysis`
- `skill.lawful_basis_analysis`
- `skill.regulatory_mapping`
- `skill.obligation_mapping`

### REQUIRED_FOR_CONTEXT
- `skill.data_model_design`
  - trigger: processing analysis requires reading the data model to establish categories and flows
- `skill.jurisdiction_mapping`
  - trigger: processing or transfer spans jurisdictions with differing regimes
- `skill.risk_identification`
  - trigger: residual data protection risk must be registered for acceptance
- `skill.source_monitoring`
  - trigger: supervisory guidance or transfer mechanisms may change during the engagement
- `specialisation.gdpr`
  - trigger: GDPR or an equivalent regime governs the processing
- `specialisation.cross_border_regulatory`
  - trigger: transfers cross a jurisdictional boundary requiring a transfer mechanism

### OPTIONAL
- `skill.process_mapping`
- `skill.requirement_traceability`
- `skill.source_verification`
- `skill.document_structuring`

### Boundaries
- Support-only boundary vs `role.security_engineer`: this Role assesses data protection; technical security control design, threat modelling and accreditation remain the Security Engineer's under `decision.security_accreditation`. The two intersect on control adequacy for personal data and must both be engaged rather than substituted.
- Support-only boundary vs `role.solution_architect`: `skill.data_model_design` is contextual and read-only here, used to establish data flows. Architecture and data-model ownership remain with the Architecture and Data Architect Roles.
- The statutory DPO function where formally appointed is excluded by the Role Card. Decisions to adopt a lawful basis, accept residual risk or notify a breach are human decision rights: `decision.lawful_basis_adoption`, `decision.dpia_acceptance`, `decision.breach_notification`.
- Communication with supervisory authorities or data subjects is outside Role scope.

### Sparse-core rationale
Core is the privacy-lawful-basis-regulatory-obligation surface this Role owns. The `skill.data_model_design` mapping is contextual and deliberately framed as read-only, because a data protection Role reading a schema must not become its owner.

## 38. UX / UI & Information Architecture Specialist

Role: `role.ux_ui_information_architecture_specialist`

### REQUIRED_CORE
- `skill.information_architecture`
- `skill.user_flow_design`
- `skill.usability_analysis`
- `skill.accessibility_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.content_structure_design`
  - trigger: content model and labelling are in assignment scope
- `skill.interview_research_design`
  - trigger: design research requires structured qualitative enquiry
- `skill.survey_research_design`
  - trigger: design research requires structured quantitative instruments
- `specialisation.institutional_website`
  - trigger: product is an institutional or public-facing website
- `specialisation.admin_console`
  - trigger: product is an internal or administrative operational interface
- `specialisation.multilingual_content`
  - trigger: interface and content must work across languages

### OPTIONAL
- `skill.process_mapping`
- `skill.requirements_elicitation`
- `skill.acceptance_criteria_design`
- `skill.publication_requirements_validation`

### Boundaries
- Support-only boundary vs `role.product_manager_business_analyst`: product prioritisation and requirement authority are excluded by this Role's Does Not Own clause. `skill.requirements_elicitation` and `skill.acceptance_criteria_design` are Optional here for design-level specification only; the requirement baseline and `decision.product_scope_approval` remain the Product Role's.
- Support-only boundary vs `role.solution_architect` and engineering Roles: technical feasibility and implementation decisions are outside Role scope.
- `skill.accessibility_analysis` is core, but accessibility conformance certification is excluded by the Role Card; `review.accessibility` is performed by someone who did not author the design.
- Brand and editorial claim approval remain with the Marketing and Editorial Roles.

### Sparse-core rationale
Core is structure, flow, usability and accessibility. Research instruments are contextual because many design assignments work from existing research rather than commissioning new.

## 39. Institutional Communications / Editorial Specialist

Role: `role.institutional_communications_editorial_specialist`

### REQUIRED_CORE
- `skill.editorial_quality_control`
- `skill.content_structure_design`
- `skill.technical_writing`
- `skill.claim_substantiation`

### REQUIRED_FOR_CONTEXT
- `skill.publication_requirements_validation`
  - trigger: content is destined for external publication under format, visibility or disclosure requirements
- `skill.source_verification`
  - trigger: editorial fact-checking requires tracing claims to authoritative and current sources
- `specialisation.multilingual_content`
  - trigger: content is produced or coordinated across languages
- `specialisation.institutional_website`
  - trigger: content is published through an institutional web channel
- `skill_pack.technical_writing_documentation`
  - trigger: governed templates, house conventions and controlled documentation requirements apply

### OPTIONAL
- `skill.document_structuring`
- `skill.document_version_control`
- `skill.position_mapping`
- `skill.stakeholder_segmentation`

### Boundaries
- Support-only boundary vs `role.marketing_growth_specialist`: this Role owns institutional and editorial content; commercial campaign design and marketing claim approval are excluded by its Does Not Own clause. The two Roles are separated by audience and purpose, not by writing technique.
- Support-only boundary vs `role.eu_policy_institutional_affairs_specialist`: adoption of institutional positions is excluded by the Role Card. This Role drafts and edits; `decision.institutional_position_release` releases.
- Legal, regulatory or technical conclusions inside content are consumed from their owning Roles at their stated state and are never authored here.
- `skill.claim_substantiation` and `skill.publication_requirements_validation` are quality control, not independent review, and do not discharge `review.factual_evidence`. Publication is gated by `decision.external_publication`.

### Sparse-core rationale
Core is editorial control, structure, writing and claim substantiation. The Role sits in the Digital Product family per the approved Master Role Universe; the mapping follows that approved classification without reopening it.

## 40. Full-Stack Software Engineer

Role: `role.full_stack_software_engineer`

### REQUIRED_CORE
- `skill.test_automation`
- `skill.data_transformation`

### REQUIRED_FOR_CONTEXT
- `skill.api_contract_design`
  - trigger: implementation must consume or expose an interface contract defined for the work
- `skill_pack.supabase`
  - trigger: Supabase is part of the selected or constrained platform context
- `skill_pack.postgresql`
  - trigger: PostgreSQL is the governed relational platform for the implementation
- `skill_pack.vercel`
  - trigger: Vercel is the governed deployment platform for the implementation
- `skill.performance_testing`
  - trigger: implementation must meet a stated performance envelope

### OPTIONAL
- `skill.sql_analysis`
- `skill.observability_design`
- `skill.technical_writing`
- `skill.integration_pattern_selection`
- `skill.defect_management`

### ALTERNATIVE
- choice set: **Implementation layer**
  - cardinality: at-least-one-of
  - choice condition: select the layers actually in assignment scope: `skill.frontend_implementation` where client-side behaviour is in scope, `skill.backend_implementation` where server-side behaviour is in scope. Full-stack assignments select both; a narrowed assignment selects one, and neither being selected means the assignment is not an implementation assignment
  - members:
    - `skill.frontend_implementation`
    - `skill.backend_implementation`

### Boundaries
- Support-only boundary vs `role.solution_architect`: system and data architecture decisions are excluded by this Role's Does Not Own clause. `skill.integration_pattern_selection` is Optional and applied within an adopted architecture, never to set one. `skill.solution_decomposition` and `skill.architecture_decision_recording` are deliberately NOT mapped.
- Support-only boundary vs `role.integration_api_engineer`: `skill.api_contract_design` is contextual here for contracts consumed or exposed by the feature. Contract ownership, versioning and deprecation practice remain the Integration / API Role's under `decision.api_contract_publication`.
- Support-only boundary vs `role.platform_devops_engineer`: `skill.observability_design` is Optional and application-level only; pipeline, environment and runtime remain the Platform Role's.
- Production deployment approval, destructive migration authority and security accreditation are outside Role scope: `decision.production_release` and `decision.production_database_migration` are human decision rights.

### Sparse-core rationale
Core is deliberately two, with implementation itself expressed as an ALTERNATIVE layer set. This is the sparsest core in Wave 2 and is intentional: a full-stack Role's breadth is scope, not universally required technique, and treating both layers as core would misrepresent a narrowed assignment.

## 41. Integration / API Engineer

Role: `role.integration_api_engineer`

### REQUIRED_CORE
- `skill.api_contract_design`
- `skill.integration_pattern_selection`
- `skill.data_transformation`
- `skill.data_quality_rule_design`

### REQUIRED_FOR_CONTEXT
- `skill.incident_response_design`
  - trigger: integration requires failure recovery and reconciliation design
- `skill.observability_design`
  - trigger: integration health must be monitored across system boundaries
- `skill.privacy_impact_analysis`
  - trigger: integration transmits personal data to a new recipient or destination
- `skill_pack.supabase`
  - trigger: Supabase is part of the selected or constrained platform context
- `skill.test_automation`
  - trigger: integration behaviour must be covered by automated tests

### OPTIONAL
- `skill.schema_design`
- `skill.performance_testing`
- `skill.technical_writing`
- `skill.threat_modelling`

### Boundaries
- Support-only boundary vs `role.solution_architect`: system architecture decisions are excluded by this Role's Does Not Own clause. This Role owns the API contract; the Architect owns the system-level integration contract specification. Both are gated by `decision.api_contract_publication`, which appears on both Role Cards.
- Support-only boundary vs `role.data_protection_gdpr_specialist`: `skill.privacy_impact_analysis` is contextual and support-only, surfacing that external transmission needs assessment. The DPIA and lawful basis remain the Data Protection Role's; `decision.external_data_transmission` gates the act.
- Support-only boundary vs `role.security_engineer`: `skill.threat_modelling` is Optional and scoped to the integration surface. Security accreditation and credential issuance authority are excluded by the Role Card.
- Data model ownership and contractual terms with third parties are outside Role scope.

### Sparse-core rationale
Core is contracts, patterns, transformation and validation. Threat modelling is Optional rather than core precisely to keep the Security Engineer boundary visible on a Role that touches credentials daily.

## 42. Platform / DevOps Engineer

Role: `role.platform_devops_engineer`

### REQUIRED_CORE
- `skill.infrastructure_as_code`
- `skill.ci_cd_design`
- `skill.release_engineering`
- `skill.observability_design`
- `skill.incident_response_design`

### REQUIRED_FOR_CONTEXT
- `skill.security_control_validation`
  - trigger: platform controls must be evidenced against a defined security policy
- `skill.database_migration_planning`
  - trigger: release includes a database migration requiring rollback planning
- `skill.capacity_planning`
  - trigger: runtime scaling or cost envelope must be sized
- `skill.performance_testing`
  - trigger: release must be validated against a performance envelope

### OPTIONAL
- `skill.test_automation`
- `skill.technical_writing`
- `skill.risk_control_design`
- `skill.sql_analysis`

### ALTERNATIVE
- choice set: **Governed platform Pack**
  - cardinality: at-least-one-of
  - choice condition: select the Pack for each platform actually in the governed stack for the environment being operated; where the platform is not covered by an existing Pack, its constraints must be established from authoritative vendor documentation and recorded as assignment context rather than assumed from an adjacent Pack
  - members:
    - `skill_pack.supabase`
    - `skill_pack.postgresql`
    - `skill_pack.vercel`

### Boundaries
- Support-only boundary vs `role.security_engineer`: `skill.security_control_validation` is contextual and evidential — it validates that controls the Security Engineer designed are in place. Security policy definition and accreditation are excluded by this Role's Does Not Own clause and gated by `decision.security_accreditation`.
- Support-only boundary vs `role.database_data_engineer` and `role.data_database_architect`: `skill.database_migration_planning` is contextual for release mechanics and rollback capability. Migration design and data architecture remain those Roles'.
- Support-only boundary vs `role.integration_api_engineer`: application logic and data model ownership are excluded by the Role Card.
- Production release approval where a human decision right applies is outside Role scope: `decision.production_release`, `decision.production_infrastructure_change`, `decision.production_database_migration` and `decision.emergency_production_change` are all human decision rights, and operating the pipeline is not approving what passes through it.

### Sparse-core rationale
Core is five: IaC, pipeline, release mechanics, observability and incident response are all intrinsic to platform operation. Security validation is contextual and deliberately evidential to keep it distinct from security ownership.

## 43. Database / Data Engineer

Role: `role.database_data_engineer`

### REQUIRED_CORE
- `skill.data_transformation`
- `skill.data_quality_rule_design`
- `skill.sql_analysis`

### REQUIRED_FOR_CONTEXT
- `skill.database_migration_planning`
  - trigger: change includes a schema or data migration requiring sequencing and rollback
- `skill.data_pipeline_design`
  - trigger: pipeline structure must be designed rather than implemented against an existing design
- `skill_pack.postgresql`
  - trigger: PostgreSQL is the governed relational platform
- `skill_pack.supabase`
  - trigger: Supabase constrains the database, auth or storage surface being engineered
- `skill.performance_testing`
  - trigger: query or pipeline performance must be validated against a stated envelope

### OPTIONAL
- `skill.observability_design`
- `skill.test_automation`
- `skill.schema_design`
- `skill.technical_writing`

### PROHIBITED_IN_CONTEXT
- `skill.metric_definition`
  - basis: Role Card Does Not Own states analytical interpretation and metric definition. This Role implements pipelines and transformations; defining what a metric means is owned by `role.data_business_analytics_specialist` and gated by `decision.metric_definition_adoption`. Mapping it here would let the implementer define the semantics they implement, which is the specific failure the two Role Cards are drawn to prevent.

### Boundaries
- Support-only boundary vs `role.data_database_architect`: data architecture and schema design ownership are excluded by this Role's Does Not Own clause. `skill.schema_design` and `skill.data_pipeline_design` are Optional and contextual respectively, applied within an approved design — the Architect owns the design, this Role implements it.
- Support-only boundary vs `role.data_protection_gdpr_specialist`: data protection lawfulness conclusions are excluded by the Role Card.
- Production migration approval and destructive operation authority are outside Role scope: `decision.production_database_migration`, `decision.production_release` and `decision.data_retention_policy_change` are human decision rights.

### Sparse-core rationale
Core is three: transformation, quality rules and SQL. Design capabilities are held at Optional or contextual to keep the implementer/architect split, and the prohibition marks the analytics boundary.

## 44. Data / Business Analytics Specialist

Role: `role.data_business_analytics_specialist`

### REQUIRED_CORE
- `skill.metric_definition`
- `skill.sql_analysis`
- `skill.analytics_interpretation`
- `skill.dashboard_design`

### REQUIRED_FOR_CONTEXT
- `skill.statistical_analysis`
  - trigger: analysis requires inference beyond descriptive comparison
- `skill.data_quality_rule_design`
  - trigger: analytical dataset reliability depends on explicit quality rules
- `skill.survey_research_design`
  - trigger: analysis requires primary data collection
- `skill.benchmarking`
  - trigger: performance must be compared against external comparators

### OPTIONAL
- `skill.data_transformation`
- `skill.evidence_mapping`
- `skill.document_structuring`
- `skill.scenario_analysis`

### Boundaries
- Support-only boundary vs `role.monitoring_evaluation_learning_specialist`: indicator methodology for monitoring and evaluation is excluded by this Role's Does Not Own clause, matching MEL's reciprocal exclusion of business analytics. This Role defines business metrics; MEL defines results indicators.
- Support-only boundary vs `role.fpa_management_finance_specialist`: statutory or financial reporting figures are excluded by the Role Card. Financial KPI definition for management purposes remains FP&A's.
- Support-only boundary vs `role.database_data_engineer`: data pipeline and warehouse implementation are excluded by the Role Card; `skill.data_transformation` is Optional and analytical only.
- Causal claims where the design does not support them are excluded by the Role Card — the Role's own Core Skills require explicit articulation of what the data cannot show. `decision.metric_definition_adoption` and `decision.external_reporting_release` are human decision rights.

### Sparse-core rationale
Core is metrics, query, interpretation and reporting design. The three reciprocal boundary Roles — MEL, FP&A and Data Engineering — are each addressed explicitly because analytics sits at the intersection of all three.

## 45. AI / Knowledge Systems Engineer

Role: `role.ai_knowledge_systems_engineer`

### REQUIRED_CORE
- `skill.ai_use_case_design`
- `skill.retrieval_design`
- `skill.prompt_method_design`
- `skill.ai_output_evaluation`
- `skill.ai_guardrail_design`

### REQUIRED_FOR_CONTEXT
- `skill.knowledge_graph_design`
  - trigger: knowledge representation requires an explicit graph or relational structure
- `skill.evidence_indexing`
  - trigger: system must surface provenance for retrieved material
- `skill.privacy_impact_analysis`
  - trigger: system processes personal data or introduces automated decision-making
- `skill.threat_modelling`
  - trigger: system exposes an attack surface requiring adversarial analysis
- `specialisation.rag_knowledge_system`
  - trigger: system is a retrieval-augmented knowledge system
- `specialisation.ai_assisted_research`
  - trigger: system supports research workflows requiring provenance discipline
- `skill.test_automation`
  - trigger: evaluation requires automated regression suites

### OPTIONAL
- `skill.data_model_design`
- `skill.observability_design`
- `skill.technical_writing`
- `skill.statistical_analysis`

### Boundaries
- Support-only boundary vs `role.knowledge_evidence_steward`: `skill.evidence_indexing` is contextual here to surface provenance inside the system. Knowledge governance and canonical promotion authority are excluded by this Role's Does Not Own clause and remain the Steward's under `decision.canonical_knowledge_promotion`. A system that captures provenance does not govern knowledge state.
- Support-only boundary vs `role.data_database_architect`: `skill.data_model_design` is Optional and system-internal.
- Support-only boundary vs `role.data_protection_gdpr_specialist` and `role.security_engineer`: `skill.privacy_impact_analysis` and `skill.threat_modelling` are contextual and support-only; data protection lawfulness and AI regulatory classification conclusions are excluded by the Role Card.
- The professional conclusions produced through the system are never this Role's. `decision.ai_system_adoption`, `decision.production_release` and `decision.automated_decision_making` are human decision rights.
- Model selection analysis under this Role compares model capability against task, cost, latency and assurance requirements. It is analysis feeding `decision.ai_system_adoption`; no mapping in this registry binds a Role to a model or runtime.

### Sparse-core rationale
Core is five, covering use-case design through guardrails, because an AI system without evaluation and guardrails is not a deliverable. Every capability touching knowledge governance, privacy or security is contextual and support-only.

## 46. Security Engineer

Role: `role.security_engineer`

### REQUIRED_CORE
- `skill.threat_modelling`
- `skill.security_control_design`
- `skill.security_testing`
- `skill.security_control_validation`

### REQUIRED_FOR_CONTEXT
- `skill.incident_response_design`
  - trigger: detection and response content is in assignment scope
- `skill.privacy_impact_analysis`
  - trigger: controls protect personal data and the data protection assessment requires security input
- `skill.risk_quantification`
  - trigger: residual security risk must be quantified for acceptance

### OPTIONAL
- `skill.regulatory_mapping`
- `skill.risk_control_design`
- `skill.observability_design`
- `skill.technical_writing`

### Boundaries
- This Role is the owner of every security conclusion. `skill.quality_attribute_analysis` is deliberately **not** mapped here, and neither is `skill_pack.supabase`. That Skill's Card excludes `role.security_engineer` on the stated ground that this Role owns the conclusions the Skill defers to and exercises them through its own capabilities; mapping it here would have contradicted a reviewed card rather than complemented it, so the mapping was dropped instead of the card being widened. Wave 2 records the reciprocal instead: when `role.solution_architect` or an engineering Role uses that Skill's security dimension, the resulting constraints are inputs, and the threat model, control design, validation and adequacy conclusion remain this Role's. Platform-specific security constraints reach this Role through the architecture Roles' outputs, not through a technology Pack mapped here.
- Support-only boundary vs `role.data_protection_gdpr_specialist`: `skill.privacy_impact_analysis` is contextual and provides security input to an assessment the Data Protection Role owns.
- Support-only boundary vs `role.enterprise_project_risk_specialist`: `skill.risk_quantification` is contextual and scoped to security exposure; enterprise risk appetite setting is excluded by this Role's Does Not Own clause.
- Security accreditation and risk acceptance are human decision rights: `decision.security_accreditation` and `decision.security_risk_acceptance`. Production deployment approval is outside Role scope.
- Legal conclusions on regulatory security obligations remain `role.legal_regulatory_lead`'s; `skill.regulatory_mapping` is Optional and perimeter-only.

### Sparse-core rationale
Core is the four security techniques the Role owns. The deliberate non-mapping of `skill.quality_attribute_analysis` is the counterpart to the Wave 1 allowlist widening: that Skill reaches architecture and engineering Roles, while every security conclusion stays here.

## 47. Software QA / Test Automation Specialist

Role: `role.software_qa_test_automation_specialist`

### REQUIRED_CORE
- `skill.test_automation`
- `skill.acceptance_criteria_design`
- `skill.defect_management`

### REQUIRED_FOR_CONTEXT
- `skill.performance_testing`
  - trigger: non-functional performance behaviour is in test scope
- `skill.security_testing`
  - trigger: security testing is in assigned test scope and the Security Engineer has defined its scope
- `skill.requirement_traceability`
  - trigger: test coverage must be traced to requirements for a release gate
- `skill.data_quality_rule_design`
  - trigger: test data or data-dependent behaviour requires explicit quality rules

### OPTIONAL
- `skill.sql_analysis`
- `skill.observability_design`
- `skill.technical_writing`
- `skill.document_structuring`

### PROHIBITED_IN_CONTEXT
- `skill.frontend_implementation`
  - basis: Role Card Does Not Own states implementation and defect correction. Beyond scope, this is an independence matter: a tester who fixes the code they test collapses the separation that makes their evidence worth anything. Implementation remains `role.full_stack_software_engineer`'s.
- `skill.backend_implementation`
  - basis: Same basis. The prohibition is contextual to the code under test — it does not prevent the same human holding an implementation assignment on a different component under a different Role assignment.

### Boundaries
- Support-only boundary vs Review Profiles: test execution and coverage reporting are quality control, not independent review. They produce evidence for a release gate; they do not discharge `review.code` or `review.test_coverage`, both of which appear on this Role Card and are performed under their own profiles.
- Support-only boundary vs `role.product_manager_business_analyst`: `skill.acceptance_criteria_design` is core here for deriving testable conditions, but product requirements and acceptance criteria authorship are excluded by this Role's Does Not Own clause. The Product Role authors the baseline; this Role derives testable conditions from it.
- Support-only boundary vs `role.security_engineer`: `skill.security_testing` is contextual and executes within a scope the Security Engineer defines; security accreditation is excluded by the Role Card.
- Release approval and go/no-go decisions are outside Role scope: `decision.production_release` and `decision.defect_deferral` are human decision rights.

### Sparse-core rationale
Core is two: automation and deriving testable conditions. The two prohibitions are an independence case rather than a pure scope case, and are the only independence-based prohibitions in Wave 2.

## 48. Data Room & Disclosure Manager

Role: `role.data_room_disclosure_manager`

### REQUIRED_CORE
- `skill.data_room_index_design`
- `skill.disclosure_access_matrix_design`
- `skill.disclosure_tracking`
- `skill.redaction_preparation`
- `skill.document_version_control`

### REQUIRED_FOR_CONTEXT
- `skill.disclosure_package_preparation`
  - trigger: a phased or staged disclosure release is being assembled
- `skill.document_configuration_control`
  - trigger: released material must be held under governed configuration control
- `skill.document_gap_analysis`
  - trigger: data room completeness must be assessed against an index
- `skill_pack.version_control_document_configuration`
  - trigger: a governed multi-version document environment applies

### OPTIONAL
- `skill.evidence_indexing`
- `skill.action_tracking`
- `skill.document_structuring`
- `skill.requirement_traceability`

### PROHIBITED_IN_CONTEXT
- `skill.knowledge_state_metadata_management`
  - basis: Role Card Does Not Own states epistemic status, canonicality or evidential quality of information. That is `role.knowledge_evidence_steward`'s, gated by `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change`. The Master Role Universe keeps these two Roles separate because they govern different things — controlled disclosure versus epistemic status — and mapping knowledge-state metadata management here would collapse that distinction.

### Boundaries
- Support-only boundary vs `role.knowledge_evidence_steward`: see the prohibition above. `skill.evidence_indexing` is Optional here for data-room indexing mechanics only, not for evidence-integrity governance.
- Support-only boundary vs `role.legal_regulatory_lead` and `role.data_protection_gdpr_specialist`: legal conclusions on confidentiality, privilege or disclosure obligations are excluded by this Role's Does Not Own clause. `skill.redaction_preparation` prepares redactions against requirements someone else determines.
- Decisions on what may lawfully or commercially be disclosed are outside Role scope: `decision.disclosure_authorisation` and `decision.data_room_access_grant` are human decision rights.
- The substantive content of disclosed documents is never this Role's.

### Sparse-core rationale
Core is five: index, access matrix, tracking, redaction and version control — the document-control surface the Role owns end to end. The single prohibition is the Phase 3 Master Role Universe distinction made executable.

# 3. Cross-Role Reuse Summary

All figures below are computed from the mapping entries in section 2, not estimated.

- Total active mapping entries: **676**
  - `REQUIRED_CORE`: 188
  - `REQUIRED_FOR_CONTEXT`: 230
  - `OPTIONAL`: 192
  - `ALTERNATIVE`: 56
  - `PROHIBITED_IN_CONTEXT`: 10
- Unique Skills used in active (non-prohibited) mappings: **183**
- Unique Specialisations used: **34**
- Unique Skill Packs used: **20**
- Roles mapped: **48**
- REQUIRED_CORE per role: min 2, max 5, mean 3.9

## Top 20 most reused capability IDs in Wave 2

| Rank | Capability | Roles |
|---:|---|---:|
| 1 | `skill.source_verification` | 21 |
| 2 | `skill.scenario_analysis` | 16 |
| 3 | `skill.benchmarking` | 14 |
| 4 | `skill.risk_identification` | 14 |
| 5 | `skill.document_structuring` | 13 |
| 6 | `skill.analytics_interpretation` | 10 |
| 7 | `skill.contract_review` | 9 |
| 8 | `skill.document_gap_analysis` | 9 |
| 9 | `skill.source_monitoring` | 9 |
| 10 | `skill.technical_writing` | 9 |
| 11 | `skill.requirement_traceability` | 8 |
| 12 | `skill.action_tracking` | 7 |
| 13 | `skill.capacity_planning` | 7 |
| 14 | `skill.evidence_indexing` | 7 |
| 15 | `skill.obligation_mapping` | 7 |
| 16 | `skill.observability_design` | 7 |
| 17 | `skill.regulatory_mapping` | 7 |
| 18 | `skill.research_synthesis` | 7 |
| 19 | `skill.stakeholder_mapping` | 7 |
| 20 | `skill.dependency_mapping` | 6 |

## Single-role capabilities across Wave 1 + Wave 2

- Capability IDs used by exactly one Role across both waves: **92** of **263** used IDs (**35.0%**).
- This is the anti-proliferation signal to watch. A capability used by exactly one Role is not automatically wrong — some methods genuinely belong to a single professional Role — but a high proportion suggests the universe carries entries that are Role-specific technique rather than reusable capability.

Single-role capability IDs:

- `skill.account_mapping` — ## 11. Sales / Business Development Specialist
- `skill.ai_guardrail_design` — AI / Knowledge Systems Engineer
- `skill.ai_output_evaluation` — AI / Knowledge Systems Engineer
- `skill.ai_use_case_design` — AI / Knowledge Systems Engineer
- `skill.architecture_decision_recording` — ## 8. Solution Architect
- `skill.assessment_design` — Learning / VET Design Specialist
- `skill.backend_implementation` — Full-Stack Software Engineer
- `skill.bankability_gap_analysis` — Funding & Bankability Architect
- `skill.business_case_structuring` — Strategy & Business Analyst
- `skill.campaign_design` — Marketing / Growth Specialist
- `skill.capex_estimation` — CAPEX / Cost Engineering Specialist
- `skill.capex_modelling` — ## 5. Financial Modelling Specialist
- `skill.ci_cd_design` — Platform / DevOps Engineer
- `skill.cost_effectiveness_analysis` — Economic / CBA Specialist
- `skill.cost_estimate_reconciliation` — CAPEX / Cost Engineering Specialist
- `skill.critical_path_analysis` — ## 1. Project / Delivery Lead
- `skill.crm_process_design` — Customer / CRM Specialist
- `skill.customer_commitment_tracking` — Customer / CRM Specialist
- `skill.data_room_index_design` — Data Room & Disclosure Manager
- `skill.debt_schedule_modelling` — ## 5. Financial Modelling Specialist
- `skill.design_basis_definition` — ## 4. Technical / Feasibility Lead
- `skill.disclosure_access_matrix_design` — Data Room & Disclosure Manager
- `skill.disclosure_package_preparation` — Data Room & Disclosure Manager
- `skill.disclosure_tracking` — Data Room & Disclosure Manager
- `skill.economic_cost_benefit_analysis` — Economic / CBA Specialist
- `skill.environmental_social_gap_analysis` — ESG / E&S Specialist
- `skill.fact_extraction` — ## 2. Research / Market Intelligence Analyst
- `skill.financial_model_design` — ## 5. Financial Modelling Specialist
- `skill.frontend_implementation` — Full-Stack Software Engineer
- `skill.funding_source_mapping` — Funding & Bankability Architect
- `skill.go_to_market_analysis` — Marketing / Growth Specialist
- `skill.grant_cost_eligibility_analysis` — Grant Financial Compliance / Budget Specialist
- `skill.information_architecture` — UX / UI & Information Architecture Specialist
- `skill.infrastructure_as_code` — Platform / DevOps Engineer
- `skill.insurance_programme_analysis` — Insurance / Risk Transfer Specialist
- `skill.inventory_analysis` — Supply Chain & Procurement Operations Specialist
- `skill.knowledge_graph_design` — AI / Knowledge Systems Engineer
- `skill.knowledge_state_metadata_management` — ## 10. Knowledge & Evidence Steward
- `skill.lawful_basis_analysis` — Data Protection / GDPR Specialist
- `skill.lead_qualification` — ## 11. Sales / Business Development Specialist
- `skill.learning_outcome_design` — Learning / VET Design Specialist
- `skill.lifecycle_cost_analysis` — ## 4. Technical / Feasibility Lead
- `skill.marketing_message_design` — Marketing / Growth Specialist
- `skill.monitoring_evaluation_design` — Monitoring, Evaluation & Learning Specialist
- `skill.offtake_analysis` — Commercial & Demand Specialist
- `skill.om_strategy_design` — Asset O&M / Technical Operations Specialist
- `skill.opex_estimation` — CAPEX / Cost Engineering Specialist
- `skill.opex_modelling` — ## 5. Financial Modelling Specialist
- `skill.opportunity_qualification` — ## 11. Sales / Business Development Specialist
- `skill.organisation_design_analysis` — People / Organisation Specialist
- `skill.portfolio_prioritisation_analysis` — Portfolio / Programme Manager
- `skill.project_scheduling` — ## 1. Project / Delivery Lead
- `skill.prompt_method_design` — AI / Knowledge Systems Engineer
- `skill.proposal_commercial_narrative` — ## 11. Sales / Business Development Specialist
- `skill.quality_attribute_analysis` — ## 8. Solution Architect
- `skill.redaction_preparation` — Data Room & Disclosure Manager
- `skill.release_engineering` — Platform / DevOps Engineer
- `skill.results_framework_design` — Monitoring, Evaluation & Learning Specialist
- `skill.retrieval_design` — AI / Knowledge Systems Engineer
- `skill.revenue_model_design` — Commercial & Demand Specialist
- `skill.risk_register_design` — Enterprise / Project Risk Specialist
- `skill.sales_pipeline_analysis` — ## 11. Sales / Business Development Specialist
- `skill.sanctions_screening` — Integrity / Due Diligence Specialist
- `skill.security_control_design` — Security Engineer
- `skill.social_dialogue_process_design` — Social Dialogue Specialist
- `skill.solution_decomposition` — ## 8. Solution Architect
- `skill.source_discovery` — ## 2. Research / Market Intelligence Analyst
- `skill.sourcing_analysis` — Supply Chain & Procurement Operations Specialist
- `skill.state_aid_screening` — Procurement / State Aid Specialist
- `skill.strategic_prioritisation` — Portfolio / Programme Manager
- `skill.supplier_evaluation` — Supply Chain & Procurement Operations Specialist
- `skill.tariff_analysis` — Commercial & Demand Specialist
- `skill.tax_position_analysis` — Tax Specialist
- `skill.usability_analysis` — UX / UI & Information Architecture Specialist
- `skill.user_story_design` — ## 7. Product Manager / Business Analyst
- `skill.work_breakdown_design` — ## 1. Project / Delivery Lead
- `skill.workforce_planning` — People / Organisation Specialist
- `specialisation.ai_assisted_research` — AI / Knowledge Systems Engineer
- `specialisation.b2b_sales` — ## 11. Sales / Business Development Specialist
- `specialisation.commercial_growth_strategy` — Strategy & Business Analyst
- `specialisation.institutional_business_development` — ## 11. Sales / Business Development Specialist
- `specialisation.integrity_sanctions_context` — Integrity / Due Diligence Specialist
- `specialisation.municipal_stakeholder_context` — Institutional Affairs & Stakeholder Specialist
- `specialisation.nonprofit_strategy` — Strategy & Business Analyst
- `specialisation.organisation_change` — People / Organisation Specialist
- `specialisation.partner_led_growth` — ## 11. Sales / Business Development Specialist
- `specialisation.project_es_risk` — ESG / E&S Specialist
- `specialisation.rag_knowledge_system` — AI / Knowledge Systems Engineer
- `specialisation.relational_data_platform` — ## 9. Data & Database Architect
- `specialisation.service_operations` — Operations / Service Delivery Specialist
- `specialisation.social_partner_context` — Social Dialogue Specialist
- `specialisation.supply_chain_operations` — Supply Chain & Procurement Operations Specialist

- Universe entries declared but **not used by any Role** across Wave 1 + Wave 2: **4**. These are listed in section 7 as Wave 3 audit candidates, not deleted here.

# 4. Specialisation Coverage

Wave 2 exercises **34** distinct Specialisation IDs across the following classes. Every one is an existing entry in `skills/master-skill-universe.md`; none is created here.

| Specialisation | Class | Roles | Why it is bounded context, not authority |
|---|---|---:|---|
| `specialisation.admin_console` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.ai_assisted_research` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.bess` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.commercial_growth_strategy` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.cross_border_regulatory` | JURISDICTION | 2 | Bounds the legal or regulatory perimeter. Perimeter is not permission: regulated determinations stay with their owning Role. |
| `specialisation.eu_grant_delivery` | PROGRAMME | 6 | Bounds the programme rulebook applied. Rules constrain the work; they confer no submission or approval authority. |
| `specialisation.eu_institutional_context` | OPERATING_CONTEXT | 4 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.gdpr` | JURISDICTION | 1 | Bounds the legal or regulatory perimeter. Perimeter is not permission: regulated determinations stay with their owning Role. |
| `specialisation.health` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.ifi_esg_safeguards` | INSTITUTION | 2 | Bounds an institution's policy framework. Institutional requirements constrain the package; the institution's own decision is outside the registry. |
| `specialisation.industrial` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.infrastructure_project_preparation` | OPERATING_CONTEXT | 4 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.institutional_website` | OPERATING_CONTEXT | 2 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.integrity_sanctions_context` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.multi_partner_programme_delivery` | OPERATING_CONTEXT | 3 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.multilingual_content` | OPERATING_CONTEXT | 5 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.municipal_stakeholder_context` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.nonprofit_strategy` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.organisation_change` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.project_es_risk` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.public_procurement` | JURISDICTION | 1 | Bounds the legal or regulatory perimeter. Perimeter is not permission: regulated determinations stay with their owning Role. |
| `specialisation.public_sector_strategy` | OPERATING_CONTEXT | 2 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.public_service_demand` | OPERATING_CONTEXT | 3 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.rag_knowledge_system` | TECHNOLOGY | 1 | Bounds a platform or product surface. Platform constraints limit what is achievable; they confer no change, deployment or vendor-commitment authority. |
| `specialisation.real_estate` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.regulated_market` | OPERATING_CONTEXT | 2 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.service_operations` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.social_partner_context` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.solar` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.state_aid` | JURISDICTION | 1 | Bounds the legal or regulatory perimeter. Perimeter is not permission: regulated determinations stay with their owning Role. |
| `specialisation.supply_chain_operations` | OPERATING_CONTEXT | 1 | Bounds the operating environment the method is applied in. It changes what is relevant, not who may conclude. |
| `specialisation.transport` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.waste` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |
| `specialisation.water` | SECTOR | 3 | Bounds which benchmarks, norms and failure modes apply. It supplies domain content; the professional conclusion stays with the Role. |

Classes exercised: INSTITUTION, JURISDICTION, OPERATING_CONTEXT, PROGRAMME, SECTOR, TECHNOLOGY.

The Specialisation model holds under Wave 2. In every case above the Specialisation narrows applicability — which sector's benchmarks, which jurisdiction's rules, which metric conventions, which operating environment — and in no case does it add a decision right, an artifact, a review identity or a scope element absent from the consuming Role Card. Sector Specialisations appear as ALTERNATIVE choice sets rather than as contextual singles for three technical Roles, because exactly one asset class normally governs and selecting several would silently blend incompatible benchmark bases.

# 5. Pack Activation and Transitive Pack Compatibility

Wave 2 activates **20** distinct Skill Packs:

| Pack | Roles activating it |
|---|---|
| `skill_pack.bgk` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |
| `skill_pack.change_management_adoption` | Operations / Service Delivery Specialist, People / Organisation Specialist |
| `skill_pack.cove` | EU Programme Implementation & Grant Management Specialist, Learning / VET Design Specialist |
| `skill_pack.ebrd` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |
| `skill_pack.eib` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |
| `skill_pack.erasmus_plus` | EU Programme Implementation & Grant Management Specialist |
| `skill_pack.horizon_europe` | EU Programme Implementation & Grant Management Specialist |
| `skill_pack.ifc` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |
| `skill_pack.ifi_financial_appraisal` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist |
| `skill_pack.investeu` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |
| `skill_pack.labour_market_skills_intelligence` | Learning / VET Design Specialist |
| `skill_pack.life_programme` | EU Programme Implementation & Grant Management Specialist |
| `skill_pack.postgresql` | Database / Data Engineer, Full-Stack Software Engineer, Platform / DevOps Engineer |
| `skill_pack.project_finance_metrics` | Funding & Bankability Architect, PPP / Concession Specialist, Project Finance / Transaction Specialist |
| `skill_pack.supabase` | Database / Data Engineer, Full-Stack Software Engineer, Integration / API Engineer, Platform / DevOps Engineer |
| `skill_pack.technical_writing_documentation` | Deliverables / Reporting Specialist, Institutional Communications / Editorial Specialist |
| `skill_pack.ukraine_facility` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |
| `skill_pack.vercel` | Full-Stack Software Engineer, Platform / DevOps Engineer |
| `skill_pack.version_control_document_configuration` | Data Room & Disclosure Manager |
| `skill_pack.world_bank` | Funding & Bankability Architect, IFI / DFI Project Preparation Specialist, Project Finance / Transaction Specialist |

Transitive compatibility is assessed under `standard.skill.common_constraints` §6.1a: where a Role may activate a Pack, every Required and selectable Optional component of that Pack must be compatible with that Role.

The five Packs with exemplar cards declare components; the remaining Packs have no card and therefore declare no components yet. Component checking results are in section 5.1; where a component has no Skill Card, it is reported as **NOT YET VALIDATABLE** rather than as a pass.

## 5.1 Component compatibility results

| Pack | Component | Kind | Result |
|---|---|---|---|
| `skill_pack.bgk` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.change_management_adoption` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.cove` | `skill.source_verification` | Required | PASS |
| `skill_pack.cove` | `skill.requirement_traceability` | Required | PASS |
| `skill_pack.cove` | `skill.source_monitoring` | Required | PASS |
| `skill_pack.cove` | `skill.partner_mapping` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.cove` | `skill.partner_coordination` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.cove` | `skill.results_framework_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.cove` | `skill.indicator_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.cove` | `skill.learning_outcome_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.cove` | `skill.grant_cost_eligibility_analysis` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.ebrd` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.eib` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.erasmus_plus` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.horizon_europe` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.ifc` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.ifi_financial_appraisal` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.investeu` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.labour_market_skills_intelligence` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.life_programme` | `skill.source_verification` | Required | PASS |
| `skill_pack.life_programme` | `skill.requirement_traceability` | Required | PASS |
| `skill_pack.life_programme` | `skill.source_monitoring` | Required | PASS |
| `skill_pack.life_programme` | `skill.partner_mapping` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.life_programme` | `skill.deliverable_planning` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.life_programme` | `skill.milestone_management` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.life_programme` | `skill.grant_cost_eligibility_analysis` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.life_programme` | `skill.document_structuring` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.postgresql` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.project_finance_metrics` | `skill.debt_schedule_modelling` | Required | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.project_finance_metrics` | `skill.project_finance_ratio_analysis` | Required | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.project_finance_metrics` | `skill.sensitivity_analysis` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.project_finance_metrics` | `skill.financing_scenario_analysis` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.project_finance_metrics` | `skill.discounted_cash_flow_analysis` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.project_finance_metrics` | `skill.cash_flow_modelling` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.supabase` | `skill.quality_attribute_analysis` | Required | PASS |
| `skill_pack.supabase` | `skill.data_model_design` | Required | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.supabase` | `skill.schema_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.supabase` | `skill.api_contract_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.supabase` | `skill.integration_pattern_selection` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.supabase` | `skill.data_quality_rule_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.supabase` | `skill.observability_design` | Optional | NOT YET VALIDATABLE — no Skill Card |
| `skill_pack.technical_writing_documentation` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.ukraine_facility` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.vercel` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.version_control_document_configuration` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |
| `skill_pack.world_bank` | — | — | NOT YET VALIDATABLE — no Pack Card, components undeclared |

Carded components checked and passing: **7**. Components or Packs without a card, reported as **NOT YET VALIDATABLE** rather than as passes: **39**.

## 5.2 Allowlist widening performed for Wave 2

Four exemplar Skill Cards were widened in the same commit, purely for transitive compatibility. Each addition confers eligibility only; no relationship type or trigger was written into any card, and every authority, artifact, review, decision, evidence and knowledge-state boundary section is byte-identical to its prior state.

| Skill Card | Roles added | Because they activate |
|---|---|---|
| `skill.source_verification` | `role.project_development_lead`, `role.eu_programme_implementation_grant_management_specialist`, `role.learning_vet_design_specialist` | `skill_pack.bid_proposal_management`, `skill_pack.life_programme`, `skill_pack.cove` |
| `skill.requirement_traceability` | `role.project_development_lead`, `role.eu_programme_implementation_grant_management_specialist`, `role.learning_vet_design_specialist` | `skill_pack.bid_proposal_management`, `skill_pack.life_programme`, `skill_pack.cove` |
| `skill.source_monitoring` | `role.eu_programme_implementation_grant_management_specialist`, `role.learning_vet_design_specialist` | `skill_pack.life_programme`, `skill_pack.cove` |
| `skill.quality_attribute_analysis` | `role.full_stack_software_engineer`, `role.integration_api_engineer`, `role.platform_devops_engineer`, `role.database_data_engineer` | `skill_pack.supabase` |

### A contradiction that was avoided rather than widened

An earlier draft of this mapping activated `skill_pack.supabase` and `skill.quality_attribute_analysis` for `role.security_engineer`. Transitive compatibility would then have required adding `role.security_engineer` to the quality-attribute Skill Card — whose prose states that Role is excluded precisely because it owns the conclusions the Skill defers to.

Under `standard.skill.common_constraints` §6.1a and the Wave 2 instruction, a genuine contradiction is reported rather than resolved by widening. The mapping was changed instead of the reviewed card: Security Engineer maps neither the Skill nor the Pack, and platform-specific security constraints reach that Role through the architecture Roles' outputs. This is recorded here because the near-miss is the useful finding, not the fix.

## 5.3 Duplicate effective activation

Cases where a Skill is both a Pack component and individually mappable to the same Role. Under §6.1 the capability activates **once**, under the **stricter** obligation, with the Pack's currency and evidence rules on top.

| Role | Capability | Pack | Handling |
|---|---|---|---|
| `role.eu_programme_implementation_grant_management_specialist` | `skill.source_verification` | `skill_pack.life_programme` / `skill_pack.cove` | Mapped REQUIRED_CORE directly and required by the Pack. Activates once under REQUIRED_CORE, the stricter obligation; the Pack's controlled-source rules apply on top. The direct mapping is retained because source discipline applies to this Role outside any programme Pack. |
| `role.eu_programme_implementation_grant_management_specialist` | `skill.requirement_traceability` | `skill_pack.life_programme` / `skill_pack.cove` | Mapped REQUIRED_CORE directly and required by the Pack. Activates once under REQUIRED_CORE; retained directly because obligation traceability applies to any grant agreement, not only Pack-covered programmes. |
| `role.eu_programme_implementation_grant_management_specialist` | `skill.source_monitoring` | `skill_pack.life_programme` / `skill_pack.cove` | Mapped REQUIRED_FOR_CONTEXT directly and required by the Pack. Where the Pack is active it governs, and the Pack's REQUIRED obligation is the stricter of the two. |
| `role.funding_bankability_architect` | `skill.project_finance_ratio_analysis` | `skill_pack.project_finance_metrics` | Mapped REQUIRED_FOR_CONTEXT directly and a required component of the Pack. Where the Pack is active it governs ratio conventions and the capability activates once. The direct mapping is retained for the case where coverage ratios are read without the full metrics Pack. |
| `role.project_finance_transaction_specialist` | `skill.project_finance_ratio_analysis` | `skill_pack.project_finance_metrics` | Same handling. |
| `role.ppp_concession_specialist` | `skill.project_finance_ratio_analysis` | `skill_pack.project_finance_metrics` | Same handling. |
| `role.learning_vet_design_specialist` | `skill.learning_outcome_design` | `skill_pack.cove` | Mapped REQUIRED_CORE directly and an optional component of the Pack. Activates once under REQUIRED_CORE, which is stricter than the Pack's optional selection. |

## 5.4 Pack dependency and cycles

Wave 2 introduces no Pack dependency. The only declared dependency in the registry remains `skill_pack.cove` layering over `skill_pack.erasmus_plus`, one-directionally. Where a Role activates `skill_pack.cove` through the ALTERNATIVE programme set, the Erasmus+ layer activates transitively and its components are subject to the same compatibility rule — currently NOT YET VALIDATABLE, since `skill_pack.erasmus_plus` has no card. No cycle exists or is introduced.

# 6. Candidate Universe Gaps — NOT ACTIVE MAPPINGS

Capabilities that Wave 2 wanted and the universe does not contain. **None appears in any active mapping in section 2.** They are recorded for a governed universe decision, not created here.

| Proposed ID | Reason it was wanted | Likely family / class | Affected Roles | Workaround used in Wave 2 |
|---|---|---|---|---|
| `skill.governance_structure_design` | Joint governance design across partner organisations is an owned surface of Programme / Partnership Manager with no matching capability; `skill.role_responsibility_mapping` covers responsibilities but not multi-party governance bodies, decision rights allocation or escalation architecture. | Stakeholder & Institutional, or Project / Programme Delivery | Programme / Partnership Manager; potentially PPP / Concession | Mapped `skill.role_responsibility_mapping` plus `skill.decision_criteria_design` as an approximation. |
| `skill.editorial_multilingual_coordination` | Coordinating editing across authors and languages is a distinct discipline from `specialisation.multilingual_content`, which bounds the context rather than supplying the coordination technique. | Product / UX / Content | Institutional Communications / Editorial; Deliverables / Reporting | Mapped `skill.editorial_quality_control` with `specialisation.multilingual_content` as context. |
| `skill.negotiation_preparation` | Named in the Core Skills prose of at least four Role Cards — Programme / Partnership Manager, Supply Chain, Project Development Lead, Project Finance / Transaction — always bounded as preparation within delegated limits, never as negotiation authority. No registry entry exists. | Strategy & Analysis, or Commercial & Market | Programme / Partnership Manager; Supply Chain & Procurement Operations; Project Development Lead; Project Finance / Transaction | Left unmapped; the underlying analysis is covered by option, risk-allocation and commercial-structure capabilities. |
| `skill.variance_analysis` | Variance analysis and driver explanation is an owned surface of FP&A with no matching capability; `skill.analytics_interpretation` is the analytics-side technique, not the management-finance one. | Finance & Economics | FP&A / Management Finance | Mapped `skill.financial_evidence_reconciliation` plus `skill.analytics_interpretation`. |
| `skill.commissioning_readiness_assessment` | Handover and commissioning readiness from an operations perspective is an owned surface of Asset O&M; `skill.delivery_readiness_assessment` is the delivery-management technique and does not carry operational acceptance content. | Technical / Engineering | Asset O&M / Technical Operations | Mapped `skill.asset_performance_analysis` and `skill.om_strategy_design`. |
| `skill.defect_management` | Defect identification, reproduction and severity characterisation is an owned surface of Software QA with no registry entry; `skill.test_automation` covers construction, not defect lifecycle discipline. | Software / Integration / Platform / Security | Software QA / Test Automation | Left unmapped; core kept at two capabilities as a result. |
| `skill.qa_response_control` | Q&A process control and consistency of information provided to competing parties is an owned surface of Data Room & Disclosure Manager with no registry entry. | Documentation / Knowledge / Disclosure | Data Room & Disclosure Manager | Mapped `skill.disclosure_tracking` and `skill.action_tracking` as an approximation. |
| `skill.accession_alignment_analysis` | Acquis-alignment and negotiating-chapter analysis is the defining surface of EU Enlargement / Governance; `skill.regulatory_mapping` and `skill.capability_gap_analysis` together approximate it but neither carries the accession-process structure. | Stakeholder & Institutional | EU Enlargement / Governance | Mapped `skill.institutional_mapping`, `skill.capability_gap_analysis` and contextual `skill.regulatory_mapping`. |

Eight candidate gaps. Each was worked around with existing capabilities rather than blocking the mapping, and each workaround is visible in the affected Role's section. The pattern is consistent: the gaps cluster where a Role Card names an owned surface in prose that the universe never turned into a reusable capability, which is exactly the seam a Wave 3 audit should examine.

Separately, **4** universe entries are declared but used by no Role across Wave 1 and Wave 2. They are not deleted here; Wave 3 should decide whether each is a genuine future capability or an entry that never earned its place.

- `skill.use_case_modelling`
- `specialisation.dscr`
- `specialisation.llcr`
- `specialisation.plcr`

# 7. Micro-Skill and Overlap Candidates for Wave 3 Audit

Surfaced by the act of mapping. Nothing is deleted or merged here.

| Candidate | Observation | Suggested Wave 3 question |
|---|---|---|
| `skill.market_sizing` / `skill.market_segmentation` / `skill.demand_analysis` | All three activate together on commercial assignments and rarely apart. Segmentation in particular reads as a step inside sizing or demand work. | Is segmentation a distinct capability or a sub-step? Test whether any Role needs it without one of the other two. |
| `skill.risk_identification` / `skill.risk_register_design` | Mapped together on every Role that carries either. A register that nothing populates, and identification with nowhere to record, are both incoherent. | Should these be one capability with the register as an output convention? |
| `skill.action_tracking` / `skill.milestone_management` / `skill.deliverable_planning` | Three tracking capabilities that co-activate across delivery, consortium and reporting Roles. The distinctions are real but narrow. | Do all three survive a reuse test, or is one a naming variant of another? |
| `skill.process_design` / `skill.process_mapping` / `skill.sop_design` | Design, mapping and procedure documentation form a chain used by the same Roles. `skill.sop_design` is close to a documentation convention. | Is `skill.sop_design` a capability or an output format of `skill.process_design`? |
| `skill.source_discovery` / `skill.source_comparison` | Both are single-Role capabilities in Wave 2 and sit adjacent to the heavily reused `skill.source_verification`. | Are these techniques inside verification rather than peers of it? |
| `skill.capacity_planning` / `skill.resource_planning` | Used by overlapping Roles with a distinction that did not survive contact with the Role Cards — several Roles could take either. | Do these describe two capabilities or one at two altitudes? |
| `skill.evidence_indexing` / `skill.data_room_index_design` | Both index material for retrieval; the difference is the destination, not the technique. | Is data-room indexing a Specialisation of evidence indexing rather than a separate Skill? |
| `skill.insurance_gap_analysis` / `skill.insurance_programme_analysis` | Added in Wave 1 remediation and now both mapped to the same single Role with no other consumer. | Do both earn distinct identity, or is gap analysis a step inside programme analysis? |
| `skill.esg_screening` / `skill.environmental_social_gap_analysis` | Co-activate on the same Role; screening reads as the first stage of gap analysis. | Same question as the insurance pair. |
| `skill.security_control_design` / `skill.risk_control_design` | Different families, similar names, and a reviewer could reasonably confuse them. | Naming disambiguation rather than a merge. |

### Pack-versus-direct duplication cases

Recorded in section 5.3. Four capabilities are both Pack components and direct mappings for the same Role. All are handled under the duplicate-activation rule and each direct mapping was retained only because it has meaning outside its Pack. `skill.project_finance_ratio_analysis` is the case to watch: it is a direct mapping for three Roles and a required component of `skill_pack.project_finance_metrics`, and if Wave 3 finds no assignment that needs it without the Pack, the direct mappings should go.

# 8. Cross-Wave Conflict Findings

Wave 1 was not modified. Its mapping records are unchanged by this step; the only Wave 1 artifacts touched are four exemplar Skill Cards, and only their compatible-role allowlists, mapping references and compatibility prose — recorded in section 5.2.

**No contradiction between Wave 1 and Wave 2 mappings was found.** Specifically checked:

- No Wave 2 Role is also a Wave 1 subject. The two waves partition the 59 approved Roles, 11 + 48, with no overlap.
- No capability is mapped at a relationship in Wave 2 that contradicts its Wave 1 relationship for a different Role. Relationship types are per Role, so divergence across Roles is expected and is not conflict.
- The Wave 1 removal of `skill.capex_estimation` and `skill.opex_estimation` from `role.technical_feasibility_lead` is honoured and completed: Wave 2 maps both as REQUIRED_CORE to `role.capex_cost_engineering_specialist`, which is where the Role Cards place ownership, and adds a conditional prohibition on `skill.opex_estimation` for `role.asset_om_technical_operations_specialist` taken verbatim from that Role Card.
- The Wave 1 exclusion of `role.security_engineer` from `skill.quality_attribute_analysis` is honoured; the near-miss and its resolution are recorded in section 5.2 as an observation, not a conflict.

One **non-conflicting observation** worth a Wave 3 look: Wave 1 maps `skill.partner_mapping` to `role.eu_grants_programmes_specialist` and `role.sales_business_development_specialist`, both REQUIRED_FOR_CONTEXT. Wave 2 maps it as REQUIRED_CORE to `role.programme_partnership_manager`. That is coherent — the capability is intrinsic to a partnership Role and contextual for others — but it makes `skill.partner_mapping` one of the most cross-cutting capabilities in the registry, and its scope statement will need to hold across three quite different uses when its Skill Card is written.

# 9. Validation Summary

Computed against this file and the current repository state.

| # | Check | Result |
|---:|---|---|
| 1 | Exactly 48 Wave 2 Role names present | PASS — 48 |
| 2 | Exactly 48 unique Role IDs, each verified from an actual Role Card | PASS — 48 unique, section 1 |
| 3 | Zero Wave 1 Roles remapped as Wave 2 subjects | PASS — 0 overlap; 11 + 48 = 59 |
| 4 | Every active `skill.<id>` exists in Master Skill Universe | PASS — 0 unresolved |
| 5 | Every active `specialisation.<id>` exists | PASS — 0 unresolved |
| 6 | Every active `skill_pack.<id>` exists | PASS — 0 unresolved |
| 7 | Zero unresolved candidate IDs inside active mappings | PASS — candidate gaps confined to section 6 |
| 8 | Every REQUIRED_FOR_CONTEXT entry has an explicit trigger | PASS — 230 entries, 0 without trigger |
| 9 | Every ALTERNATIVE set has an explicit choice condition and cardinality | PASS — 10 sets |
| 10 | Every PROHIBITED_IN_CONTEXT entry has a concrete basis | PASS — 10 entries, each citing a Role Card clause or an independence ground |
| 11 | REQUIRED_CORE remains sparse; flag any role > 8 | PASS — max 5, mean 3.9; 0 roles above 8 |
| 12 | No mapping widens approved Role authority | PASS — every section carries boundary notes derived from the Role Card |
| 13 | No mapping transfers artifact ownership or another Role's conclusion | PASS — support-only notes on every cross-Role touch |
| 14 | No mapping creates review identity or human decision authority | PASS — quality-control capabilities stated as not discharging review; decision rights referenced as dependencies only |
| 15 | No model/runtime binding | PASS — no model, vendor or runtime named in any mapping |
| 16 | No Phase 3 Role Card modified | PASS — 0 changes under `roles/` |
| 17 | No Skill / Specialisation / Pack Card created | PASS — 0 new cards |
| 18 | Exemplar-card edits are allowlist/mapping-reference only | PASS — 4 cards, boundary sections byte-identical |
| 19 | Carded Pack components pass transitive compatibility | PASS — 7 carded components pass after the widening in section 5.2 |
| 20 | Uncarded Pack components reported as NOT YET VALIDATABLE | PASS — 39 reported, not counted as passes |
| 21 | No circular Pack dependency introduced | PASS — Wave 2 introduces no dependency; CoVE to Erasmus+ remains one-directional |
| 22 | Duplicate-effective-activation cases identified and handled | PASS — 7 cases in section 5.3, each resolved once under the stricter obligation |
| 23 | At least one genuine Specialisation mapping present | PASS — 34 Specialisations across 6 classes, section 4 |
| 24 | PROHIBITED_IN_CONTEXT not fabricated | PASS — 10 entries across 8 Roles, each from a Does Not Own clause or an independence ground |
| 25 | No active deprecated ID reintroduced | PASS — 0 |
| 26 | All mapping artifacts remain PROPOSED / working | PASS |
| 27 | Candidate Universe Gaps excluded from active mappings | PASS — section 6 only |
| 28 | Cross-wave conflicts reported rather than silently fixing Wave 1 | PASS — section 8; Wave 1 mappings unmodified |
| 29 | Cross-role reuse statistics computed from actual mapping data | PASS — section 3 generated from the mapping entries |
| 30 | File sufficient for independent audit without console history | PASS — Role IDs, paths, triggers, conditions, bases, statistics, gaps and the avoided contradiction are all recorded here |

## Standing statement

Nothing in this file is APPROVED or CANONICAL. All 48 mappings, the statistics, the candidate gaps and the Wave 3 audit list remain PROPOSED and require independent audit and human approval before any mass generation of Skill, Specialisation or Skill Pack Cards.
# 10. Wave 2 Remediation Record — after independent audit

The independent audit returned **FAIL** with 48 CRITICAL/HIGH findings, all of one kind: active mappings whose consuming Role was absent from the target card's compatible-role allowlist. The finding was structural — the registry validated Pack components transitively but never validated direct mappings against cards at all.

## 10.1 Reproduction

The 48 findings were reproduced independently before any change: 37 direct Skill conflicts (`skill.source_verification` 20, `skill.source_monitoring` 8, `skill.requirement_traceability` 7, `skill.lifecycle_cost_analysis` 2) and 11 direct Pack conflicts. Transitive component conflicts were already 0 from the previous remediation. Counts matched the audit exactly.

## 10.2 Direct Skill conflicts — 37 resolved

Each affected mapping was checked against its approved Role Card before deciding to widen or remove.

**`skill.source_verification` — 21 Roles admitted.** Every affected Role Card carries an explicit `Currency / version / effective-date requirements ... are mandatory` clause and a `Claims that must be source-backed` list. Establishing provenance, authority, version and currency is exactly that surface, so all were admitted. The Skill Card's boundaries are untouched: it still determines nothing about whether a claim is true, holds no legal interpretation, no evidence-governance authority and no knowledge-state promotion.

**`skill.source_monitoring` — 9 Roles admitted.** Each depends on a governed source set that changes inside an engagement period: law as at date, guidance version, sanctions list version, institutional policy version, assessment year. Detecting that change is the Skill's purpose. Its boundaries are untouched: detection and triage only, no interpretation, no canonical rewrite, no state transition, no publication authority.

**`skill.requirement_traceability` — 8 Roles admitted.** Three own an obligation-to-artifact traceability surface outright — Deliverables / Reporting owns deliverable-to-obligation traceability, IFI / DFI owns institution requirement mapping and gap tracking, Software QA owns coverage analysis for release gates. The rest need linkage to evidence compliance without concluding on it. Boundaries untouched: linkage only, no requirement approval, no compliance conclusion.

**`skill.lifecycle_cost_analysis` — 2 mappings REMOVED, card not widened.** The reviewed card scopes this Skill to support-only technical-option comparison by `role.technical_feasibility_lead` and explicitly excludes CAPEX / Cost Engineering and Asset O&M as consumers, on the ground that those Roles own the cost inputs it consumes. Widening would have inverted the boundary that the Wave 1 audit created this card to enforce. The mappings were removed from both Roles, and each Role's section now records that its lifecycle work runs through its own owned capabilities — `skill.capex_estimation` / `skill.opex_estimation` / `skill.cost_estimate_reconciliation` for CAPEX, `skill.om_strategy_design` / `skill.asset_performance_analysis` for Asset O&M. The support-only Skill is not recreated under another ID.

## 10.3 Direct Pack conflicts — 10 admitted, 1 removed

| Pack | Role | Decision |
|---|---|---|
| `skill_pack.life_programme` | EU Programme Implementation | Admitted — owns grant obligation mapping and donor-rule interpretation, which need the rulebook this Pack binds |
| `skill_pack.cove` | EU Programme Implementation | Admitted — same basis, plus the inherited Erasmus+ layer |
| `skill_pack.cove` | Learning / VET Design | Admitted — CoVE is a vocational-excellence action and this Role's Mandatory Assignment Attributes require a programme scope and framework version reference |
| `skill_pack.project_finance_metrics` | Funding & Bankability Architect | Admitted — Core Skills name debt capacity reasoning from model outputs; carries `review.financial_model` |
| `skill_pack.project_finance_metrics` | Project Finance / Transaction | Admitted — Core Skills name covenant and coverage-ratio reasoning explicitly |
| `skill_pack.project_finance_metrics` | PPP / Concession | Admitted — owns payment mechanism and risk allocation design; carries `review.financial_model` |
| `skill_pack.supabase` | Full-Stack Software Engineer | Admitted — implements features against the platform |
| `skill_pack.supabase` | Integration / API Engineer | Admitted — builds against its interface surface |
| `skill_pack.supabase` | Platform / DevOps Engineer | Admitted — operates its environments and release path |
| `skill_pack.supabase` | Database / Data Engineer | Admitted — implements migrations and pipelines on its managed relational layer |
| `skill_pack.bid_proposal_management` | Project Development Lead | **REMOVED** — see below |

**Why the bid/proposal mapping was removed rather than the Pack widened.** *(Wording corrected in Wave 3; the original was factually too broad and is superseded by this paragraph.)* The Project Development Lead Role Card **does** carry external submission: `artifact.project_definition_document` and `artifact.development_readiness_assessment` both transmit by submission to lenders, investors or authorities and are COSTLY_TO_REVERSE afterwards, and the Role Card requires tender deadlines and permitting windows to be captured. What it does **not** own is a formal competitive response-to-solicitation process — bid/no-bid qualification, a compliance matrix built from a solicitation, multi-author narrative coordination, and submission-readiness control against evaluation criteria. That is the Pack's subject, and it belongs to `role.sales_business_development_specialist` and `role.eu_grants_programmes_specialist`, both already on the Pack Card. The distinction is between submitting a project case and competing in a governed procurement or call.

This removal cascaded. `role.project_development_lead` had been added to the `skill.source_verification` and `skill.requirement_traceability` allowlists in the previous remediation solely as a transitive consequence of this Pack mapping. With the Pack mapping gone, that basis fell away, so the Role was **removed from both Skill Card allowlists** rather than left standing without a mapping — the audit's own rule that a Role needs a valid mapping and Role Card basis, applied in the subtractive direction.

## 10.4 Relationship defects corrected

**Economic / CBA — a capability was both REQUIRED_CORE and mutually exclusive ALTERNATIVE.** `skill.economic_cost_benefit_analysis` was listed in core and as a member of the one-of set against `skill.cost_effectiveness_analysis`. That is incoherent: a capability cannot be universally required and simultaneously exclusive with an alternative. It was removed from REQUIRED_CORE; the one-of ALTERNATIVE set and its operational choice condition are retained unchanged, and core is now three capabilities. The Role Card does not require a different structure — it owns *appraisal methodology selection*, which is precisely a choice, so the ALTERNATIVE set is the correct and only home.

**Asset O&M `skill.opex_estimation` prohibition was too broad.** The Role Card excludes OPEX cost estimation figures *where a cost engineering assignment exists*. The prohibition asserted the exclusion without carrying that condition into its basis. It is now stated as trigger-conditional, applying only where a dedicated cost-engineering assignment exists or cost-estimate ownership is assigned to `role.capex_cost_engineering_specialist`, and explicitly asserting nothing beyond that condition. The Role's own approved ownership of operating cost drivers, availability and lifecycle basis is unaffected in every case.

## 10.5 Boundaries confirmed intact

- **Security Engineer** remains excluded from both `skill.quality_attribute_analysis` and `skill_pack.supabase`. The audit independently confirmed this decision as correct; nothing in this remediation changes it, and Wave 2 maps neither to that Role.
- **`skill.lifecycle_cost_analysis`** card is unchanged in every section, including its allowlist: the fix was to the mappings, not the card.
- Across all seven cards edited, only compatible-role allowlists, canonical mapping references and compatibility prose changed. Every Skill Boundary, Support-Only Boundary, Independent Review Boundary, Outputs / Contributions, Review / Decision Dependencies, Evidence and Source Requirements, Knowledge-State Constraints and Pack authority section is byte-identical to its prior state.

## 10.6 New rule closing the structural gap

`standard.skill.common_constraints` section **6.1 Direct Mapping Compatibility Rule** now requires that every active direct mapping to a carded capability be permitted by that card, with absence a validation failure, runtime widening forbidden, and remediation limited to a governed card change after Role-boundary review or removal of the mapping. It is cross-referenced from `architecture/role-to-skill-mapping-rules.md` section 8.1. Together with the existing 6.1a transitive rule it covers all four cases: direct Role→Skill, direct Role→Specialisation where carded, direct Role→Pack, and transitive Pack→component. Case 4 alone was covered before; cases 1–3 are why this audit found 48 conflicts.

# 11. Wave 3 Cross-Domain Normalization — changes to this mapping

Wave 3 normalized the registry across all 59 Roles. Changes landing in this file:

**Merges — 5 retired IDs, mappings migrated to survivors**

| Retired | Survivor | Effect here |
|---|---|---|
| `skill.resource_planning` | `skill.capacity_planning` | Asset O&M core switched to the survivor; Operations dropped a now-duplicate contextual entry (it already held the survivor in core) |
| `skill.insurance_gap_analysis` | `skill.insurance_programme_analysis` | Insurance / Risk Transfer core reduced from 3 to 2 |
| `skill.traceability_matrix_design` | `skill.requirement_traceability` | No Wave 2 effect; both consumers were Wave 1 Roles — see the governed correction recorded in the Wave 1 file |
| `specialisation.affordability` | `skill.affordability_analysis` | Commercial & Demand contextual entry removed; the surviving Skill's trigger notes the absorption |
| `specialisation.tariff_modelling` | `skill.tariff_analysis` | Same, with `skill.revenue_model_design` taking the structure-design case |

**Additions — 3 reusable capability classes, mapped where a Role Card supports them**

- `skill.negotiation_preparation` → Programme / Partnership Manager, Supply Chain & Procurement Operations, Project Development Lead, Project Finance / Transaction. All four name it in Core Skills, all four bound as preparation within delegated limits.
- `skill.variance_analysis` → FP&A / Management Finance (core), Grant Financial Compliance / Budget (contextual).
- `skill.defect_management` → Software QA / Test Automation (core), Full-Stack Software Engineer (optional). This raised the QA core from two capabilities to three, correcting an under-representation of that Role's owned surface.

**Specialisation reclassification**

`specialisation.admin_console` and `specialisation.institutional_website` are reclassified from TECHNOLOGY to OPERATING_CONTEXT in section 4. Neither binds a platform or version; both describe a product kind and audience. The Universe now carries the classification semantics that make this test explicit. After the two group-14 merges retired the METRIC-classified entries from Wave 2's active set, **six classes** are exercised in this file: SECTOR, JURISDICTION, INSTITUTION, PROGRAMME, TECHNOLOGY and OPERATING_CONTEXT. METRIC remains a valid class, exercised by `specialisation.dscr` / `llcr` / `plcr` inside `skill_pack.project_finance_metrics` rather than by a direct mapping.

**Audit-trail correction**

The Project Development Lead explanation for excluding `skill_pack.bid_proposal_management` was factually too broad and is corrected in both its role section and section 10.3. The Role does transmit externally and does track tender deadlines; what it lacks is a formal competitive response-to-solicitation process. The mapping decision is unchanged.

**Not changed by Wave 3:** every Role subject, every relationship type and trigger not listed above, the Security Engineer exclusions, and the `skill.lifecycle_cost_analysis` support-only scope.
