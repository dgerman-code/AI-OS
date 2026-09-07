# Master Workflow Universe

Status: PROPOSED — Phase 5 candidate universe
Version: 0.1
Inherits: `standard.workflow.common_constraints@0.1`

## Purpose

A bounded candidate universe of reusable coordination patterns. This is a **candidate list for audit**, not an approved registry: inclusion here confers no approval, and several entries below are expected to be merged or dropped once the overlap groups in section 11 are worked through.

The universe is deliberately small. The risk this document guards against is not too few workflows — it is a proliferation of near-identical patterns that drift apart, and micro-workflows that are really single skill invocations wearing a `workflow.` prefix.

## Granularity rule

Repeated from `standard.workflow.common_constraints` §16 because it is the rule this document is most likely to violate:

Create a Workflow only where it represents a **reusable coordination pattern across multiple activities and stages**, involving more than one Role or more than one governed state transition. Not for a single skill invocation, a document heading, a one-off approval click, a trivial two-step action, or a depth variation of an existing pattern.

## Scale

- **9 families**
- **49 candidate workflows**
- **4 carded exemplars** (marked ✎ below)

The count is not a target and must not be managed toward a number. It is reported so drift between the stated and actual universe is visible.

---

## 1. Project / Investment Development

Coordination of project preparation from definition through readiness for an investment, financing or stage gate.

| ID | Scope (one sentence) |
|---|---|
| `workflow.project_definition_and_scoping` | Establish the project definition, boundary conditions and assumptions of record as a stable basis for all downstream workstreams. |
| `workflow.project_development_readiness` ✎ | Take a defined project through technical, commercial, financial, legal and ESG workstreams to a decision-grade readiness position against a named gate. |
| `workflow.technical_feasibility_assessment` | Establish the technical basis, option comparison and feasibility position for a defined project configuration. |
| `workflow.site_permitting_and_consents_pathway` | Map, sequence and track the permitting and consents path from screening to submission readiness. |
| `workflow.stage_gate_progression_preparation` | Assemble and test the evidence position required for a specific stage gate, including open items and gate-critical risks. |

## 2. Programme / Grant Delivery

Coordination across the grant lifecycle, pre-award and post-award.

| ID | Scope |
|---|---|
| `workflow.funding_opportunity_screening` | Screen calls and funding routes against a project or organisational profile to a shortlist with a stated fit basis. |
| `workflow.eu_grant_application_development` ✎ | Take a selected call from requirement capture through consortium, work-package, budget and content assembly to submission readiness. |
| `workflow.consortium_formation_and_agreement_preparation` | Coordinate partner identification, role allocation, and preparation of the consortium arrangement to a decision-ready position. |
| `workflow.grant_implementation_mobilisation` | Move from executed grant agreement to an operating implementation baseline with obligations mapped to actions. |
| `workflow.grant_periodic_reporting_and_claim_preparation` | Assemble periodic narrative and financial reporting to submission readiness against the executed agreement. |
| `workflow.grant_amendment_preparation` | Prepare a substantiated amendment case and package to the point a granting-authority submission decision becomes due. |

## 3. Strategy / Policy / Institutional

Coordination of analysis, positioning and institutional engagement.

| ID | Scope |
|---|---|
| `workflow.strategic_option_appraisal` | Frame a strategic question, develop and test options, and reach a comparable option position for a human strategic decision. |
| `workflow.business_case_development` | Assemble a structured business case from evidence, options, economics and risk to a decision-ready position. |
| `workflow.policy_position_development` | Develop an institutional policy position from source analysis and stakeholder input to a release-ready draft. |
| `workflow.institutional_engagement_campaign` | Plan, sequence and track structured engagement with institutional counterparts around a defined objective. |
| `workflow.portfolio_prioritisation_cycle` | Run a recurring prioritisation cycle across a portfolio to a ranked position with stated criteria and evidence. |

## 4. Commercial / Business Development

Coordination of opportunity, offer and partnership work.

| ID | Scope |
|---|---|
| `workflow.opportunity_qualification_and_pursuit` | Qualify an opportunity, decide pursuit shape, and coordinate the pursuit to a bid/no-bid position. |
| `workflow.competitive_bid_preparation` | Take a qualified competitive opportunity through compliance matrix, content planning, review cycles and submission readiness. |
| `workflow.commercial_proposal_development` | Develop a non-tender commercial proposal from requirement capture to a commitment-ready draft. |
| `workflow.partnership_development` | Move a partnership from candidate identification through structure and terms analysis to a commitment-ready position. |
| `workflow.market_and_demand_evidence_build` | Assemble a defensible market, segmentation and demand evidence position for a defined asset, service or programme. |

## 5. Finance / Transaction

Coordination of modelling, funding and transaction preparation.

| ID | Scope |
|---|---|
| `workflow.financial_model_build_and_integrity_check` | Build or extend a financial model with a governed assumptions register and an integrity position before external reliance. |
| `workflow.funding_strategy_development` | Develop and test funding routes and structure to a recommended strategy for a human funding decision. |
| `workflow.bankability_assessment` | Assess a project against lender or investor requirements to a stated bankability position with gaps. |
| `workflow.ifi_appraisal_readiness_preparation` | Prepare the documentation and evidence position an IFI/DFI appraisal requires, to submission readiness. |
| `workflow.transaction_execution_preparation` | Coordinate the workstreams a transaction requires — structure, diligence, documentation position — to the point financing decisions become due. |
| `workflow.financial_due_diligence_cycle` | Run a structured financial diligence pass to findings, scope limitations and an evidence position. |

## 6. Legal / Compliance / Risk

Coordination of regulatory, contractual, integrity and risk work.

| ID | Scope |
|---|---|
| `workflow.regulatory_and_permitting_analysis` | Establish the regulatory perimeter and obligations applying to a defined activity, to a substantiated analysis position. |
| `workflow.contract_review_cycle` | Coordinate a structured contract review pass to a findings and risk-allocation position ahead of commitment. |
| `workflow.procurement_and_state_aid_route_analysis` | Analyse procurement and State Aid routes to a recommended route position for a human route decision. |
| `workflow.integrity_due_diligence_screening` | Run counterparty and sanctions screening to a findings position with escalation where triggered. |
| `workflow.risk_assessment_and_register_cycle` | Run identification, quantification, allocation and control design to a maintained risk position. |
| `workflow.esg_environmental_social_assessment` | Take E&S screening through assessment against a named safeguard standard to an action-plan-ready position. |
| `workflow.data_protection_impact_assessment_cycle` | Run a DPIA from processing-activity capture to an assessment position where a lawful-basis decision becomes due. |

## 7. Product / Software / Data Delivery

Coordination of digital change from requirement to release readiness.

| ID | Scope |
|---|---|
| `workflow.product_discovery_and_requirement_definition` | Move from problem statement through discovery to defined, traceable, acceptance-criteria-bearing requirements. |
| `workflow.software_change_delivery` ✎ | Take a change request through architecture, implementation, testing and release readiness to the production-release gate. |
| `workflow.data_platform_change_delivery` | Take a data model, pipeline or migration change through design, implementation and validation to a migration gate. |
| `workflow.security_assessment_and_control_validation` | Coordinate threat modelling, control design and validation to a security position ahead of accreditation. |
| `workflow.incident_response_and_recovery` | Coordinate detection, containment, recovery and post-incident evidence for a service or data incident. |
| `workflow.ai_system_evaluation_cycle` | Evaluate an AI system against defined criteria to an evidence position ahead of an adoption decision. |

## 8. Knowledge / Documentation / Disclosure

Coordination of evidence integrity, document preparation and controlled disclosure.

| ID | Scope |
|---|---|
| `workflow.decision_grade_document_preparation` ✎ | Prepare a decision-grade document from sources and evidence through drafting, specialist contribution, traceability and review to a human approval gate. |
| `workflow.evidence_base_construction` | Assemble and verify an evidence base, with gaps and conflicts made visible rather than resolved silently. |
| `workflow.canonical_knowledge_promotion_preparation` | Prepare the package a canonical-status decision requires, without promoting anything. |
| `workflow.data_room_preparation_and_release` | Structure, index and stage a data room through phased release to the point access decisions become due. |
| `workflow.external_publication_preparation` | Take content through substantiation, review requirement and publication-requirements validation to a release gate. |

## 9. Operations / Organisational Change

Coordination of operating model, sourcing and organisational work.

| ID | Scope |
|---|---|
| `workflow.operating_model_design_cycle` | Take an operating or service model from current-state mapping through target design to an adoption-ready position. |
| `workflow.sourcing_and_supplier_selection` | Coordinate sourcing analysis, route selection and evaluation to the point a supplier award decision becomes due. |
| `workflow.organisational_change_preparation` | Prepare an organisational change case, impact position and consultation basis to a decision-ready position. |
| `workflow.service_transition_readiness` | Assess and close readiness gaps for taking a service or asset into operation. |

---

## 10. Deliberate exclusions

These were considered and **not** created, with the reason:

| Rejected candidate | Reason |
|---|---|
| `workflow.source_verification` | A single Skill invocation (`skill.source_verification`), not a coordination pattern. |
| `workflow.document_approval` | A single gate. Approval is a `HUMAN_GATE_REFERENCE`, never a Workflow. |
| `workflow.large_project_readiness` / `workflow.small_project_readiness` | Depth variations of one pattern. Handled by criticality conditioning inside `workflow.project_development_readiness`. |
| `workflow.weekly_status_meeting` | An organisation-specific SOP with no governed state transition. |
| `workflow.model_selection` | Runtime concern. Model binding is prohibited registry-wide. |
| `workflow.role_assignment` | A System Control Profile concern, not a professional coordination pattern. |
| `workflow.erasmus_grant_application` and one per programme | Programme identity is a Pack activation inside `workflow.eu_grant_application_development`, not a separate Workflow. |

## 11. Overlap groups flagged for later audit

Recorded now so a later audit does not have to rediscover them. **None is resolved in Phase 5** — resolving them requires the exemplar set to be wider than four.

1. **`workflow.decision_grade_document_preparation` versus every document-producing Workflow.** The generic pattern is intended to be *composed into* the others rather than duplicated by them. The audit must confirm that composition is real, and that the generic pattern has not become a universal mega-workflow that swallows the specific ones.
2. **`workflow.business_case_development` / `workflow.strategic_option_appraisal` / `workflow.project_definition_and_scoping`.** Three patterns that all move from question to structured position. Likely distinct — different Roles own the conclusion in each — but the boundary needs testing.
3. **`workflow.competitive_bid_preparation` / `workflow.eu_grant_application_development` / `workflow.commercial_proposal_development`.** All three assemble a governed submission under a deadline. Candidate for one pattern with a submission-type branch, or three genuinely different gate structures.
4. **`workflow.software_change_delivery` / `workflow.data_platform_change_delivery`.** Overlapping stage shape with different owning Roles and a different terminal gate (`decision.production_release` versus `decision.production_database_migration`). May be one pattern with a branch.
5. **`workflow.bankability_assessment` / `workflow.ifi_appraisal_readiness_preparation`.** Both assess against an external financier's requirements. The distinction is institution-specific requirement mapping, which may be Pack activation rather than a separate Workflow.
6. **`workflow.risk_assessment_and_register_cycle` versus risk activity embedded in every other Workflow.** Risk work appears as a stage nearly everywhere. The audit must decide whether the standalone cycle earns its identity or is only a composed sub-pattern.
7. **`workflow.evidence_base_construction` / `workflow.decision_grade_document_preparation` stages 1–2.** Possible duplication of the same evidence-assembly coordination.
8. **`workflow.grant_periodic_reporting_and_claim_preparation` / `workflow.grant_amendment_preparation`.** Both operate against an executed agreement with the same Roles and the same granting-authority gate; may be one reporting-and-change pattern.

## 12. Status

Every entry is `PROPOSED`. Four are carded as exemplars; the remaining 45 are one-sentence candidates and are explicitly **not** validated. Card generation for the rest is not authorised by this document and should follow the same selective, assignment-driven discipline Phase 4 adopted.
