# Product Manager / Business Analyst

Status: PROPOSED — Phase 3 reference role card

## Identity
- Role Name: Product Manager / Business Analyst
- Role ID: `role.product_manager_business_analyst`
- Capability Domain: Digital Product / Software / Data
- Role Type: Professional Delivery Role
- Profile Level: CORE
- Version: 0.1
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: none
- Superseded By: none

## Purpose
Translates user, business and institutional needs into prioritised product requirements, decision criteria and acceptance logic without assuming engineering, security or production-deployment authority.

## Professional Scope
### Owns
- problem framing and stakeholder need synthesis;
- product requirements and acceptance criteria;
- prioritisation logic and release-scope recommendations;
- process / business-rule modelling;
- product outcome and success-metric definition.

### Does Not Own
- technical architecture or implementation design;
- security accreditation;
- data-architecture ownership;
- production deployment approval;
- executive business strategy beyond assigned product scope.

## Professional Decision Right
May issue a professional conclusion on product requirement completeness, priority, acceptance logic and readiness for design / engineering. This does not constitute engineering feasibility approval, production release approval or executive business approval.

## Context Breadth Limit
- Minimum context: product / feature / service workstream.
- Multi-project context: allowed for a shared product platform when boundaries are explicit.
- Cross-context inheritance: reusable patterns may transfer; user data, business rules and decisions require authorised inheritance.

## Typical Input Interfaces
- user / stakeholder needs;
- business process descriptions;
- policy / operational constraints;
- product analytics and support evidence;
- architecture / technical feasibility findings;
- organisational goals and decision criteria.

## Minimum Input Knowledge State
- Standard output minimum: FACT / SOURCE / clearly labelled ASSUMPTION.
- Decision-grade output minimum: critical business rules and constraints REVIEWED or APPROVED where available.
- If minimum is not met: requirements remain provisional and are not treated as release-ready.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.product_requirements`
  - Description: product / feature requirements, business rules and acceptance criteria
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes for material requirements
  - Independent Review Required: conditional
  - Decision Right Reference: optional `decision.product_scope_approval`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: refresh on material user, policy, process or architecture change
- Artifact Type / ID: `artifact.release_scope_recommendation`
  - Description: prioritised scope and release-readiness recommendation
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: `decision.production_release_scope`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: deployment
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE
  - Validity / Expiry / Refresh Rule: invalidate on material requirement, risk or feasibility change

## Required Methodologies
- problem framing and requirements engineering;
- stakeholder / user-need analysis;
- process and business-rule modelling;
- prioritisation and value / risk trade-off analysis;
- acceptance-criteria design.

## Core Skills
- requirements analysis;
- user-story / use-case modelling;
- prioritisation;
- stakeholder synthesis;
- KPI / outcome definition;
- process mapping.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: user research, approved policies, process evidence, analytics, support records, stakeholder decisions.
- Prohibited or insufficient source classes: unsupported preferences presented as requirements; AI-generated user needs without evidence.
- Currency / version / effective-date requirements: business-rule and policy versions must be current for decision-grade requirements.
- Claims that must be source-backed: material user pain points, regulatory constraints, business rules and performance assumptions.
- Assumptions that must be explicitly labelled: expected behaviour, adoption, volume and stakeholder preference.
- Calculations / logic that must be reproducible: prioritisation scores or value/risk matrices where used.
- Knowledge-state transitions this role may propose: DRAFT, ASSUMPTION, FACT where verified, CONFLICT_DETECTED.
- Conflict-detection obligations: flag contradictions among stakeholders, policy, technical feasibility and user evidence.

## Role-Specific Authority Limits
- must not silently convert stakeholder preference into approved product scope;
- must not override architecture, security or legal constraints;
- must not authorise production release.

## Input Acceptance Rules
- Required fields / artifacts: product context, target users / stakeholders, problem statement, known constraints.
- Conditions for ACCEPTED_WITH_CONDITIONS: non-critical gaps are explicit and assigned for validation.
- Conditions for RETURNED_FOR_REWORK: problem ownership unclear, critical business rules missing or stakeholder requirements materially conflict without escalation.

## Review Obligation
- Review Required: conditional
- Review Profile Reference(s): `review.product_requirements_quality`

## Human Decision Gates
- Decision Right Reference(s): `decision.product_scope_approval`, `decision.production_release_scope`
- Required sequence: specialist output -> required review -> human decision
- Approval invalidation condition: material requirement, risk, feasibility or policy change.

## Mandatory Assignment Attributes
- product / platform scope;
- target user / stakeholder context;
- criticality;
- applicable policy / regulatory perimeter where relevant;
- language;
- data classification where user data is involved.

## Adjacent / Boundary Roles
- `role.strategy_business_analyst` — enterprise / strategic analysis boundary.
- `role.solution_architect` — system architecture boundary.
- `role.ux_ui_information_architecture_specialist` — UX / interaction-design boundary.
- `role.data_database_architect` — data-architecture boundary.

## Incompatible Assignments / Independence Constraints
- must not independently review the same critical requirements package it authored where independent review is required.

## Escalation Conditions
- stakeholder conflict materially affects scope;
- legal / security / architecture constraints invalidate planned functionality;
- acceptance criteria cannot be made observable;
- production commitment is requested without required decision right.

## Completion Criteria
- requirements and acceptance criteria are explicit;
- evidence and assumptions are distinguishable;
- priorities and unresolved conflicts are visible;
- decision and review gates are identified.

## Failure Modes to Avoid
- solutioning before the problem is defined;
- treating roadmap position as approval;
- hiding stakeholder conflict;
- turning an AI-generated feature idea into an assumed user requirement.