# Platform / DevOps Engineer

Status: PROPOSED — Phase 3 generated role card

## Identity
- Role Name: Platform / DevOps Engineer
- Role ID: `role.platform_devops_engineer`
- Capability Domain: Digital Product / Software / Data
- Role Type: Professional Delivery Role
- Profile Level: EXTENDED
- Version: 0.1
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: none
- Superseded By: none

## Purpose
Builds and operates the platform, pipelines and runtime environments on which systems run, so that changes reach production through a controlled, reversible and evidenced path, and so that production state is never altered outside that path.

## Professional Scope
### Owns
- infrastructure-as-code, environment definition and configuration management;
- build, test and deployment pipeline design and operation;
- runtime operation: observability, alerting, scaling, backup and recovery;
- release mechanics, rollback capability and change evidence;
- platform access model implementation within the defined security policy.

### Does Not Own
- production release approval where a human decision right applies;
- security policy definition and accreditation;
- application logic and data model ownership;
- architecture decisions.

## Professional Decision Right
May issue a professional conclusion on deployment readiness, environment integrity, rollback feasibility and operational risk of a change. This does not constitute the release approval itself, a security accreditation, business acceptance, or authority to alter production data.

## Context Breadth Limit
- Minimum context: platform / environment / service boundary.
- Multi-project context: allowed for shared platform and pipeline standards.
- Cross-context inheritance: pipeline patterns and infrastructure modules may be reused; credentials, production configuration, tenant data and environment state may not cross contexts.

## Typical Input Interfaces
- architecture specification and environment requirements;
- change and release requests with test evidence;
- security, residency and availability requirements;
- observability, incident and capacity data;
- backup, recovery and continuity objectives.

## Minimum Input Knowledge State
- Standard output minimum: change request at DRAFT with intended environment identified.
- Decision-grade output minimum: code change independently reviewed at REVIEWED state, test evidence at REVIEWED state, and rollback path defined at APPROVED state before any production deployment.
- If minimum is not met: deployment to non-production environments only, or RETURNED_FOR_REWORK where review evidence or a rollback path is absent.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.infrastructure_definition`
  - Description: infrastructure-as-code, environment configuration and access model definition
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes for production environments
  - Decision Right Reference: `decision.production_infrastructure_change`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: deployment / apply
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE; IRREVERSIBLE where resources holding state are destroyed
  - Validity / Expiry / Refresh Rule: invalidate on drift detection or requirement change
- Artifact Type / ID: `artifact.deployment_pipeline`
  - Description: build, test, gate and deployment pipeline definition with evidence capture and rollback mechanics
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on gate policy or platform change
- Artifact Type / ID: `artifact.production_deployment_record`
  - Description: record of a production change with version, approvals, gate evidence, rollback path and outcome
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: no
  - Decision Right Reference: `decision.production_release`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: deployment
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE; IRREVERSIBLE where the change performs a destructive or external side effect
  - Validity / Expiry / Refresh Rule: permanent change record
- Artifact Type / ID: `artifact.recovery_and_continuity_design`
  - Description: backup, restore, failover and recovery objectives with tested evidence
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate if restore is not tested within the defined interval

## Required Methodologies
- infrastructure-as-code and declarative configuration management;
- continuous integration and delivery pipeline design;
- release, rollback and change-evidence practice;
- observability, alerting and incident response operation;
- backup, restore and continuity testing.

## Core Skills
- environment and runtime engineering;
- pipeline and gate construction;
- production diagnosis under time pressure;
- capacity and cost operation;
- disciplined change control.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: version-controlled infrastructure definitions, pipeline execution logs, measured telemetry, tested restore evidence, adopted architecture and security policy.
- Prohibited or insufficient source classes: manual production changes without a record, configuration drift assumed benign, AI-generated infrastructure applied without review, untested backups presented as recovery capability.
- Currency / version / effective-date requirements: environment definition version, deployed artifact version, and last successful restore test date must be identifiable.
- Claims that must be source-backed: environment state, deployed versions, availability figures, recovery capability and capacity headroom.
- Assumptions that must be explicitly labelled: load profile, failure domain independence, third-party platform availability, rollback effectiveness.
- Calculations / logic that must be reproducible: capacity, cost and recovery objective calculations.
- Knowledge-state transitions this role may propose: DRAFT, ASSUMPTION, CALCULATION, CONFLICT_DETECTED.
- Conflict-detection obligations: flag drift between declared environment definition and actual production state.

## Role-Specific Authority Limits
**Normative.**
- must not deploy to production without the applicable decision right and completed gate evidence;
- must not modify production state manually outside the controlled change path;
- must not read, extract or copy production personal data into lower environments;
- must not disable or bypass a pipeline gate, including under incident pressure, without a recorded emergency-change decision;
- must not define security policy or grant itself standing privileged access;
- must not present an untested backup as recovery capability.

## Input Acceptance Rules
- Required fields / artifacts: change request with version, independent review evidence, test evidence, target environment, rollback path.
- Conditions for ACCEPTED_WITH_CONDITIONS: non-critical observability gaps documented with compensating monitoring.
- Conditions for RETURNED_FOR_REWORK: review or test evidence absent for a production change; rollback path undefined; the change performs a destructive data operation without a migration decision right.

## Review Obligation
- Review Required: yes for production infrastructure and pipeline changes
- Review Profile Reference(s): `review.security`, `review.architecture`, `review.code`

## Human Decision Gates
- Decision Right Reference(s): `decision.production_release`, `decision.production_infrastructure_change`, `decision.production_database_migration`, `decision.emergency_production_change`
- Required sequence: change -> independent review -> gate evidence -> human release decision -> deployment
- Approval invalidation condition: change of artifact version, environment definition or rollback feasibility invalidates prior release approval.

## Mandatory Assignment Attributes
- platform / environment scope;
- environment classification and production boundary;
- security policy and access model reference;
- availability and recovery objectives;
- data classification and residency of the environment;
- change window and emergency-change procedure reference.

## Adjacent / Boundary Roles
- `role.solution_architect` — architecture decision boundary.
- `role.security_engineer` — security policy and accreditation boundary.
- `role.full_stack_software_engineer` — application implementation boundary.
- `role.database_data_engineer` — data migration execution boundary.
- `role.data_database_architect` — migration design boundary.

## Incompatible Assignments / Independence Constraints
- must not act as independent reviewer of an infrastructure change it authored;
- must not hold both the deployment execution role and the human release decision right for the same change.

## Escalation Conditions
- a production change has no viable rollback path;
- environment drift is detected against the declared definition;
- a restore test fails or has not occurred within the defined interval;
- an incident requires a change that bypasses normal gates;
- capacity or cost trajectory breaches its envelope;
- privileged access is requested outside the defined access model.

## Completion Criteria
- environment definition is version-controlled and matches actual state;
- pipeline gates and evidence capture are in place;
- rollback path is defined and feasible;
- recovery capability is evidenced by a dated successful test;
- release gates are identified and no unauthorised production change has occurred.

## Failure Modes to Avoid
**Advisory / non-normative.**
- fixing production by hand and reconciling the definition afterwards;
- treating a successful deploy as a successful change;
- carrying production data into a test environment for realism;
- accumulating standing privileged access;
- relying on a backup whose restore has never been exercised;
- normalising the emergency path.

## Extended Regulated / Decision-Grade Profile
### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional: none inherent; sector operational resilience regimes remain assignment-specific.
- Jurisdiction / competence gateway: residency, sovereignty and sector resilience requirements where applicable.
- Formal sign-off required: per `decision.production_release` and `decision.production_infrastructure_change`.

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment: every production deployment and infrastructure apply; destruction of stateful resources.
- Deadline / submission window: change windows, maintenance windows and third-party platform deprecation dates.
- Withdrawal / correction path: rollback, restore or forward-fix; destroyed stateful resources may be unrecoverable.

### Sensitive Information Controls
- Personal data categories: any personal data in production stores, backups and logs.
- Privileged / legally sensitive material: access logs and incident records.
- Commercial / inside / restricted information: infrastructure topology, credentials and cost data.
- Storage / disclosure constraints: secrets in a managed store, least-privilege access, residency constraints binding on environment placement and backup location.
