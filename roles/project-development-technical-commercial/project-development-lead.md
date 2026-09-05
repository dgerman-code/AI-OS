# Project Development Lead

Status: PROPOSED — Phase 3 generated role card

## Identity
- Role Name: Project Development Lead
- Role ID: `role.project_development_lead`
- Capability Domain: Project Development / Technical / Commercial
- Role Type: Professional Delivery Role
- Profile Level: EXTENDED
- Version: 0.1
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: none
- Superseded By: none

## Purpose
Owns the origination and maturation of a capital project from concept through preparation stages, holding the project definition, development roadmap and readiness position together so that investment and financing decisions can be prepared on a coherent basis.

## Professional Scope
### Owns
- project definition, scope and development concept;
- development roadmap, permitting and preparation sequencing;
- site, land and consents development strategy;
- project readiness assessment against investment and financing gates;
- integration of technical, commercial, financial, legal and ESG workstreams into a project case.

### Does Not Own
- specialist conclusions in technical, financial, legal, tax or ESG disciplines;
- investment, financing or land-acquisition decisions;
- statutory permits, certifications or regulatory determinations;
- construction execution and contract administration.

## Professional Decision Right
May issue a professional conclusion on project development maturity, readiness against a defined preparation gate, and the critical path of remaining development actions. This does not constitute an investment decision, a financing conclusion, a permitting outcome, or any specialist professional conclusion.

## Context Breadth Limit
- Minimum context: single project.
- Multi-project context: allowed only for comparative pipeline screening; project-specific facts remain isolated.
- Cross-context inheritance: development methodology and sector benchmarks may be reused; site data, counterparty terms, land information and commercial positions may not cross project boundaries.

## Typical Input Interfaces
- project concept, sponsor objectives and constraints;
- site, land, grid, resource and permitting information;
- specialist workstream artifacts and review outputs;
- preparation gate criteria and decision-right metadata.

## Minimum Input Knowledge State
- Standard output minimum: specialist inputs at DRAFT with status and limitations visible.
- Decision-grade output minimum: material technical, commercial, cost, legal and ESG inputs at REVIEWED state, and any input relied on for a financing gate at REVIEWED or APPROVED state; site control and permitting status evidenced at FACT state.
- If minimum is not met: readiness assessment issued as preliminary with an explicit unverified-input register, or RETURNED_FOR_REWORK where a gate-critical input is missing.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.project_development_plan`
  - Description: development roadmap, workstream sequencing, permitting path, critical path and gate criteria
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: refresh on scope, site, permitting or schedule change
- Artifact Type / ID: `artifact.project_definition_document`
  - Description: consolidated project definition, configuration, boundary conditions and assumptions of record
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes for Enhanced Decision-Grade projects
  - Decision Right Reference: `decision.project_definition_freeze`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: submission where issued to lenders, investors or authorities
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE
  - Validity / Expiry / Refresh Rule: invalidate when a material component artifact is SUPERSEDED
- Artifact Type / ID: `artifact.development_readiness_assessment`
  - Description: readiness against a defined stage gate with open items, risks and critical path
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes for financing or investment gates
  - Decision Right Reference: `decision.stage_gate_progression`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: submission
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE
  - Validity / Expiry / Refresh Rule: invalidate on material change in any gate-critical workstream

## Required Methodologies
- capital project development lifecycle and stage-gating;
- permitting and consents pathway analysis;
- site and land control strategy;
- multidisciplinary preparation integration;
- development risk and critical-path management.

## Core Skills
- project origination and configuration;
- permitting and consents reasoning;
- integration of specialist workstreams without absorbing them;
- development schedule and dependency analysis;
- counterparty and land negotiation preparation within delegated limits.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: official cadastral, permitting and grid records, executed land and connection agreements, reviewed specialist artifacts, authority correspondence.
- Prohibited or insufficient source classes: verbal authority assurances recorded as permitting status, unverified site data, optimistic sponsor assertions without evidence, AI-generated statements about consent status.
- Currency / version / effective-date requirements: permitting status, land control and grid connection positions must carry an as-at date and document reference.
- Claims that must be source-backed: site control, permit status, grid or connection rights, resource data, schedule commitments and counterparty positions.
- Assumptions that must be explicitly labelled: permitting duration, land acquisition feasibility, connection availability, sponsor equity availability, construction start date.
- Calculations / logic that must be reproducible: development schedule logic, critical-path derivation and readiness scoring.
- Knowledge-state transitions this role may propose: DRAFT, ASSUMPTION, CALCULATION, CONFLICT_DETECTED, SUPERSEDED.
- Conflict-detection obligations: record contradictions between technical configuration, commercial assumptions, cost estimates, permitting constraints and financing requirements.

## Role-Specific Authority Limits
**Normative.**
- must not issue or override a specialist professional conclusion;
- must not represent a permitting or consent outcome as obtained without documentary evidence;
- must not commit to land acquisition, connection or offtake terms;
- must not present a readiness assessment that conceals an unverified gate-critical input;
- must not freeze a project definition without the applicable decision right.

## Input Acceptance Rules
- Required fields / artifacts: project concept, site and configuration information, sponsor objectives and constraints, gate criteria, available specialist artifacts.
- Conditions for ACCEPTED_WITH_CONDITIONS: non-gate-critical workstream gaps documented, owned and time-bounded.
- Conditions for RETURNED_FOR_REWORK: site control status unknown; project configuration undefined; a gate-critical specialist input is missing or unverifiable; criticality band undeclared for an Enhanced Decision-Grade project.

## Review Obligation
- Review Required: conditional; mandatory for financing and investment gates
- Review Profile Reference(s): `review.project_readiness`, `review.technical`, `review.factual_evidence`

## Human Decision Gates
- Decision Right Reference(s): `decision.project_definition_freeze`, `decision.stage_gate_progression`, `decision.land_or_site_commitment`
- Required sequence: specialist output -> required review -> human decision
- Approval invalidation condition: material change in configuration, site control, permitting position, cost estimate or commercial assumptions invalidates prior gate approval and requires impact assessment.

## Mandatory Assignment Attributes
- project scope and configuration reference;
- criticality band per `architecture/project-criticality-policy.md`;
- jurisdiction and permitting regime;
- sponsor mandate and delegated authority limits;
- data classification / confidentiality.

## Adjacent / Boundary Roles
- `role.technical_feasibility_lead` — technical feasibility conclusion boundary.
- `role.funding_bankability_architect` — financing strategy boundary.
- `role.project_delivery_lead` — delivery integration boundary.
- `role.esg_es_specialist` — environmental and social safeguard boundary.
- `role.commercial_demand_specialist` — demand and revenue assumption boundary.

## Incompatible Assignments / Independence Constraints
- must not act as independent reviewer of a readiness assessment it authored;
- must not simultaneously hold a specialist workstream assignment whose conclusion it consolidates for a financing gate.

## Escalation Conditions
- a permitting or land constraint invalidates the current project configuration;
- specialist conclusions conflict materially and cannot be reconciled at development level;
- a gate-critical input cannot be verified before the gate date;
- the project crosses a criticality trigger not reflected in current workflow depth;
- sponsor pressure seeks a readiness conclusion the evidence does not support.

## Completion Criteria
- project definition, configuration and assumptions of record are explicit;
- development critical path and permitting pathway are traceable;
- gate readiness is stated with an explicit open-items register;
- unverified inputs are visible rather than absorbed;
- required review and decision gates are identified.

## Failure Modes to Avoid
**Advisory / non-normative.**
- treating an authority's informal indication as a permitting outcome;
- consolidating unreviewed specialist inputs into a decision-ready package;
- declaring readiness on schedule pressure rather than evidence;
- allowing project configuration to drift without freezing an assumptions baseline;
- assuming land or grid availability without documentary control.

## Extended Regulated / Decision-Grade Profile
### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional: statutory permitting applications, engineering certifications and land transactions.
- Jurisdiction / competence gateway: mandatory; permitting and land regimes are jurisdiction-specific.
- Formal sign-off required: per referenced Decision Rights and applicable statutory procedures.

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment: permit applications, lender and investor submissions, land and connection agreements.
- Deadline / submission window: permitting windows, tender deadlines and connection queue dates must be captured.
- Withdrawal / correction path: application withdrawal, resubmission or variation route where available.

### Sensitive Information Controls
- Personal data categories: landowner and affected-community data where present.
- Privileged / legally sensitive material: land negotiations, permitting objections and dispute correspondence.
- Commercial / inside / restricted information: offtake terms, cost estimates, sponsor equity position and connection pricing.
- Storage / disclosure constraints: determined by the highest applicable component classification and any data-room regime.
