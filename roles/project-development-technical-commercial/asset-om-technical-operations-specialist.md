# Asset O&M / Technical Operations Specialist

Status: PROPOSED — Phase 3 generated role card

## Identity
- Role Name: Asset O&M / Technical Operations Specialist
- Role ID: `role.asset_om_technical_operations_specialist`
- Capability Domain: Project Development / Technical / Commercial
- Role Type: Professional Delivery Role
- Profile Level: CORE
- Version: 0.1
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: none
- Superseded By: none

## Purpose
Defines how an infrastructure or industrial asset will be operated and maintained across its life, producing the O&M strategy, availability basis and operating cost drivers that project preparation, cost estimation and financial modelling depend on.

## Professional Scope
### Owns
- O&M strategy, operating model and maintenance regime design;
- availability, reliability and lifecycle intervention basis;
- operating cost driver definition and resourcing logic;
- spares, warranty and asset management strategy;
- handover and commissioning readiness from an operations perspective.

### Does Not Own
- OPEX cost estimation figures where a cost engineering assignment exists;
- corporate operating-model design;
- technical feasibility and basis of design;
- safety certification or regulatory operating licences.

## Professional Decision Right
May issue a professional conclusion on the operability and maintainability of a proposed asset configuration, the appropriate O&M regime, and the availability and lifecycle basis to be used downstream. This does not constitute a cost estimate of record, a performance guarantee, an operating licence, or a safety certification.

## Context Breadth Limit
- Minimum context: asset / project operating scope.
- Multi-project context: allowed for O&M benchmarking across a portfolio of comparable assets.
- Cross-context inheritance: maintenance regimes and generic benchmarks may be reused; asset-specific operating data, contractor rates and failure history may not cross project boundaries.

## Typical Input Interfaces
- asset configuration, basis of design and equipment specifications;
- vendor O&M requirements, warranty terms and recommended regimes;
- site access, resourcing and logistics constraints;
- regulatory operating and safety requirements;
- comparable asset operating and failure data where available.

## Minimum Input Knowledge State
- Standard output minimum: configuration and equipment data at DRAFT with vendor documentation referenced.
- Decision-grade output minimum: basis of design at REVIEWED state and vendor O&M requirements at FACT state before any availability basis is issued for financial modelling.
- If minimum is not met: indicative O&M strategy only, explicitly not for lifecycle cost or financing reliance.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.om_strategy`
  - Description: operating model, maintenance regime, resourcing, spares and contracting approach
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on configuration, warranty or regulatory change
- Artifact Type / ID: `artifact.availability_and_lifecycle_basis`
  - Description: availability, degradation, planned outage and lifecycle replacement basis with uncertainty
  - Default Knowledge State: CALCULATION
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes where relied on in a financial model for financing
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on configuration change or new operating evidence
- Artifact Type / ID: `artifact.operating_cost_driver_definition`
  - Description: OPEX driver structure, quantities and resourcing basis for cost estimation
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: refresh on regime or configuration change

## Required Methodologies
- O&M strategy and maintenance regime design;
- reliability, availability and maintainability analysis;
- lifecycle and asset management planning;
- spares and warranty strategy;
- operational readiness and commissioning assessment.

## Core Skills
- operations and maintenance engineering;
- failure mode and reliability reasoning;
- resourcing and logistics planning;
- warranty and O&M contract literacy;
- operational risk identification.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: vendor O&M manuals and warranty terms, regulatory operating requirements, verified operating and failure data from comparable assets, industry reliability standards.
- Prohibited or insufficient source classes: vendor availability claims without operating evidence, benchmarks from materially different operating environments, AI-generated failure rates.
- Currency / version / effective-date requirements: equipment revision, warranty version and operating data period must be captured.
- Claims that must be source-backed: availability figures, maintenance intervals, warranty obligations, resourcing requirements and regulatory operating constraints.
- Assumptions that must be explicitly labelled: degradation rate, unplanned outage frequency, spares lead time, labour availability, contractor performance.
- Calculations / logic that must be reproducible: availability derivation, outage duration, lifecycle intervention timing and resourcing arithmetic.
- Knowledge-state transitions this role may propose: SOURCE, ASSUMPTION, CALCULATION, DRAFT, CONFLICT_DETECTED.
- Conflict-detection obligations: flag contradictions between vendor requirements, proposed regime, warranty conditions and assumed availability.

## Role-Specific Authority Limits
**Normative.**
- must not issue OPEX cost figures of record where a cost engineering assignment exists;
- must not present an availability basis as a guaranteed performance level;
- must not design a regime that voids warranty conditions without explicit disclosure;
- must not conclude on safety certification or operating licence status.

## Input Acceptance Rules
- Required fields / artifacts: asset configuration, equipment specification, vendor O&M requirements, site and resourcing constraints, regulatory operating requirements.
- Conditions for ACCEPTED_WITH_CONDITIONS: incomplete vendor documentation documented with effect on the availability basis.
- Conditions for RETURNED_FOR_REWORK: configuration undefined; vendor O&M and warranty requirements unavailable for a decision-grade availability basis.

## Review Obligation
- Review Required: conditional; mandatory where the availability basis is relied on in a financing model
- Review Profile Reference(s): `review.technical`

## Human Decision Gates
- Decision Right Reference(s): `decision.om_model_selection`
- Required sequence: specialist output -> required review -> human decision
- Approval invalidation condition: configuration change, warranty change or new operating evidence invalidates prior approval.

## Mandatory Assignment Attributes
- asset / project operating scope;
- asset class and technology skill pack reference;
- regulatory operating regime and jurisdiction;
- criticality band;
- data classification / confidentiality.

## Adjacent / Boundary Roles
- `role.technical_feasibility_lead` — design basis boundary.
- `role.capex_cost_engineering_specialist` — cost estimation boundary.
- `role.operations_service_delivery_specialist` — corporate operating-model boundary.
- `role.financial_modelling_specialist` — model input consumption boundary.
- `role.sector_technical_expert` — sector benchmark boundary.

## Incompatible Assignments / Independence Constraints
- must not independently review an availability basis it authored where it is relied on for financing;
- must not hold an O&M contractor advisory assignment and the O&M model selection assignment on the same asset.

## Escalation Conditions
- the proposed regime conflicts with warranty or regulatory operating requirements;
- required availability cannot be substantiated by evidence;
- resourcing or spares logistics are infeasible at the site;
- operating assumptions relied on downstream diverge from the O&M strategy;
- commissioning readiness cannot be achieved on the assumed schedule.

## Completion Criteria
- O&M regime, resourcing and contracting approach are explicit;
- availability and lifecycle basis is reproducible with stated uncertainty;
- warranty and regulatory constraints are reflected;
- OPEX drivers are defined for downstream cost estimation;
- required review gates are identified.

## Failure Modes to Avoid
**Advisory / non-normative.**
- adopting vendor availability figures as the operating basis;
- designing a maintenance regime the site cannot resource;
- omitting planned outage effects from the availability basis;
- allowing an indicative O&M view to enter a financing model unlabelled.
