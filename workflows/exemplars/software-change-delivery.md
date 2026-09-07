# Software Change Delivery

Status: PROPOSED — Phase 5 exemplar Workflow Card
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: Software Change Delivery
- Workflow ID: `workflow.software_change_delivery`
- Version: 0.1
- Status: PROPOSED
- Workflow Family: Product / Software / Data Delivery
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands. The criticality driver here is blast radius — data sensitivity, availability requirement, regulatory exposure and reversibility of the release — not project value.
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose

A software change passes through ten Roles with genuinely different ownership: the requirement, the interface, the architecture, the implementation, the data layer, the security position and the test evidence are each owned by someone, and none of them owns the release. This Workflow coordinates that path from change request to the production-release gate.

The failure mode it is built against is the one every delivery process eventually attempts: treating "all stages green" as authorisation to deploy.

## Trigger

`TRIGGER` — a change request, defect or requirement is accepted into delivery scope for a defined product or platform.

## Preconditions

- `PRECONDITION` — the change is described well enough to be assessed for architectural and security impact.
- `PRECONDITION` — the target system's current architecture position is available.
- `PRECONDITION` — criticality band is determined, including data sensitivity and availability requirement.

## Scope
### Covers
- requirement definition and acceptance criteria;
- interaction and interface design where user-facing;
- architecture impact assessment and decision recording;
- implementation across application, integration and data layers;
- security assessment and control validation;
- test design, execution and evidence;
- release readiness assembly to the production-release gate.

### Does Not Cover
- **production release** — `decision.production_release` is a human decision right and no stage authorises it;
- **production infrastructure change** — `decision.production_infrastructure_change` is human;
- **production database migration execution** — `decision.production_database_migration` is human;
- **security accreditation** — `decision.security_accreditation` is human and owned via `role.security_engineer`;
- **defect deferral** — `decision.defect_deferral` is human;
- **product scope approval** — `decision.product_scope_approval` is human;
- independent review of code, architecture, security or test coverage.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.product_manager_business_analyst` | `LEAD_ROLE` (S1), `CONTRIBUTING_ROLE` (S5, S6) | `ALWAYS` | S1, S5, S6 | Owns requirements and acceptance criteria. Does not own architecture, security or release. Does not approve its own scope — `decision.product_scope_approval` is human. |
| `role.ux_ui_information_architecture_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the change alters a user-facing surface)` | S1, S2 | Owns `artifact.information_architecture` and `artifact.interaction_and_interface_design`. |
| `role.solution_architect` | `LEAD_ROLE` (S2), `CONSULTED_ROLE` (S3), `CONTRIBUTING_ROLE` (S6) | `ALWAYS` at S2 and S6; `CONDITIONAL(implementation deviates from the S2 design position)` at S3 | S2, S3, S6 | Owns the solution architecture specification and architecture decision records. Does not own the security conclusion or the release. |
| `role.data_database_architect` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the change alters the data model or requires a migration)` | S2, S3 | Owns `artifact.data_architecture_specification` and `artifact.database_migration_design`. |
| `role.full_stack_software_engineer` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the change touches application code)` | S3, S5 | Owns the source change within the approved architecture. Does not alter the architecture position unilaterally. |
| `role.integration_api_engineer` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the change alters an integration or API contract)` | S3, S5 | Owns `artifact.integration_contract_specification`. |
| `role.database_data_engineer` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the change requires migration scripts or pipeline work)` | S3, S5 | Owns migration scripts and data pipeline implementation. Does not execute production migration. |
| `role.platform_devops_engineer` | `CONTRIBUTING_ROLE` | `ALWAYS` | S3, S6 | Owns the deployment pipeline and environment configuration. **Building a pipeline is not authority to release through it.** |
| `role.security_engineer` | `CONTRIBUTING_ROLE` | `ALWAYS` at S2, S4 and S6; **`CONDITIONAL(security-control implementation is in scope)` at S3** | S2, S3, S4, S6 | Owns threat modelling, security control design, `artifact.security_control_implementation` and `artifact.security_control_assessment`. This conclusion is not obtainable through the architecture Roles. Remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase` under Phase 4. |
| `role.software_qa_test_automation_specialist` | `LEAD_ROLE` (S5), `CONTRIBUTING_ROLE` (S4, S6) | `ALWAYS` at S5 and S6; `CONDITIONAL(security testing is in scope)` at S4 | S4, S5, S6 | Owns test strategy, automation and test evidence, and defect records. Does not approve release and does not defer defects. |

## Composed Workflow References

**None.** This Workflow produces evidence and a release-readiness position rather than a decision-grade document, so `workflow.decision_grade_document_preparation` is not a fit: `artifact.release_scope_recommendation` is a recommendation assembled from test and security evidence, not a document prepared through source verification and fact/assumption separation. `workflow.incident_response_and_recovery` is named on the emergency exception path as a routing destination, not as a composed child — the emergency change is governed by its own Workflow and its own gate, not nested inside this one.

## Activated Skills / Packs

References only; all bases are the approved Phase 4 records.

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `skill.requirements_elicitation`, `skill.acceptance_criteria_design` | `role.product_manager_business_analyst` | direct (Wave 1, REQUIRED_CORE) |
| `skill.user_story_design` **OR** `skill.use_case_modelling` | `role.product_manager_business_analyst` | direct — a Wave 1 ALTERNATIVE choice set; the choice condition is in the mapping record, not here |
| `skill.quality_attribute_analysis` | `role.solution_architect` | direct (Wave 1) — **not** compatible with `role.security_engineer`, and this card does not make it so |
| `skill_pack.supabase`, `skill_pack.postgresql` | `role.solution_architect`, `role.data_database_architect`, and the Wave 2 engineering Roles per the mapping record | direct (Wave 1 / Wave 2); `role.security_engineer` is deliberately excluded |
| `skill.test_automation`, `skill.defect_management` | `role.software_qa_test_automation_specialist` | direct (Wave 2 core; `skill.defect_management` added in Wave 3) |
| `skill.threat_modelling`, `skill.security_control_design` | `role.security_engineer` | direct (Wave 2) |

`role.security_engineer` is excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase` under the approved Phase 4 records. This Workflow does not widen that, and the security position reaches the platform through the architecture Roles' outputs rather than through a Pack activation.

## Inputs

| Input | Required state |
|---|---|
| Change request or accepted requirement | stated |
| Current `artifact.solution_architecture_specification` | current version identified |
| Current `artifact.data_architecture_specification` where data is in scope | current version identified |
| Applicable security control baseline | stated |

## Stages

S2's architecture and security threads run in parallel. S3 implementation threads run in parallel across layers. S4 may begin during S3 and must close before S6.

### Stage `S1` — Requirement definition
- **Objective:** turn a change request into requirements with testable acceptance criteria, before anyone designs against a guess.
- **Entry Criteria:** preconditions satisfied.
- **Participating Roles:** `role.product_manager_business_analyst` (`LEAD_ROLE`), `role.ux_ui_information_architecture_specialist` (`CONTRIBUTING_ROLE`, where user-facing).
- **Activities:** requirements elicitation; acceptance-criteria design; user-story or use-case modelling per the Phase 4 choice condition; initial information-architecture position where user-facing.
- **Artifact Contributions:** `artifact.product_requirements` (owned by `role.product_manager_business_analyst`); `artifact.information_architecture` (owned by `role.ux_ui_information_architecture_specialist`).
- **Knowledge-State Expectations:** `DRAFT`. AI-drafted requirements are `AI_SUGGESTION` until adopted by the owning Role.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.product_requirements_quality`; `HUMAN_GATE_REFERENCE` → `decision.product_scope_approval`, `decision.release_scope_approval`.
- **Exit Criteria:** every requirement has acceptance criteria that can be tested; scope boundary stated; open questions listed rather than assumed.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `CANCELLED`.
- **Open-Item Materiality:** a requirement with no testable acceptance criterion is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S2 and S5 — nothing downstream can validate it. Wording and prioritisation questions are `NON_MATERIAL_TO_NEXT_STEP`.

### Stage `S2` — Design and impact assessment
- **Objective:** establish the architecture, data and security impact **before** implementation commits to a shape that is expensive to unwind.
- **Entry Criteria:** S1 exited at least `COMPLETE_WITH_OPEN_ITEMS`.
- **Participating Roles:** `role.solution_architect` (`LEAD_ROLE`), `role.data_database_architect` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(data model or migration)`), `role.security_engineer` (`CONTRIBUTING_ROLE`, `ALWAYS`), `role.ux_ui_information_architecture_specialist` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(user-facing surface)`).
- **Activities:** architecture impact assessment; quality-attribute analysis; architecture decision recording; data model and migration design; threat modelling and security control design; interaction and interface design.
- **Artifact Contributions:** `artifact.solution_architecture_specification`, `artifact.architecture_decision_record` (owned by `role.solution_architect`); `artifact.data_architecture_specification`, `artifact.database_migration_design` (owned by `role.data_database_architect`); `artifact.security_control_assessment` (owned by `role.security_engineer`); `artifact.interaction_and_interface_design` (owned by `role.ux_ui_information_architecture_specialist`).
- **Knowledge-State Expectations:** `DRAFT`. Security findings that cannot yet be assessed are `UNKNOWN`, not absent.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.architecture`, `review.data_architecture`, `review.security`, `review.design_quality`, `review.accessibility`; `HUMAN_GATE_REFERENCE` → `decision.architecture_adoption`, `decision.technology_selection`, `decision.api_contract_publication` where an external contract is published.
- **Exit Criteria:** architecture position stated with its decisions recorded; data impact stated; threat model and control set stated; no security finding left unrecorded.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unassessed security surface, an unresolved architecture question that bounds implementation, or an `UNKNOWN` in the threat model is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S3 and S6.

### Stage `S3` — Implementation
- **Objective:** implement within the design position, across whichever layers the change touches.
- **Entry Criteria:** S2 exited; `decision.architecture_adoption` taken where the change alters the architecture position.
- **Participating Roles:** `role.full_stack_software_engineer`, `role.integration_api_engineer`, `role.database_data_engineer`, `role.platform_devops_engineer` (all `CONTRIBUTING_ROLE`, each `Activation: CONDITIONAL` on its layer being in scope); **`role.security_engineer` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(security-control implementation is in scope)`)**; `role.solution_architect` (`CONSULTED_ROLE`, `Activation: CONDITIONAL(implementation deviates from the S2 design position)`, advisory only — it owns no artifact in this Stage).
- **Activities:** source implementation; API and integration contract implementation; migration script development; **implementation of the security controls designed at S2, performed by `role.security_engineer` within the bounds of the controls that Role owns**; pipeline and environment configuration.
- **Artifact Contributions:** `artifact.source_code_change` (owned by `role.full_stack_software_engineer`); `artifact.integration_contract_specification` (owned by `role.integration_api_engineer`); `artifact.database_migration_script` (owned by `role.database_data_engineer`); `artifact.deployment_pipeline` (owned by `role.platform_devops_engineer`); `artifact.security_control_implementation` (owned **and produced here** by `role.security_engineer`).
- **Knowledge-State Expectations:** `DRAFT`. A deviation from the S2 design position is raised to `role.solution_architect`, not absorbed silently by the implementer.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.code`.
- **Exit Criteria:** implementation complete against the requirement set; deviations from design either accepted by the architecture owner or recorded as open; migration designed and scripted but **not executed against production**.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unratified deviation from the S2 design position, or an unimplemented security control the threat model requires, is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S4 and S6.

### Stage `S4` — Security assessment and control validation
- **Objective:** establish the security position on what was actually built, separately from the people who built it.
- **Entry Criteria:** implementation substantially available; threat model from S2 current.
- **Participating Roles:** `role.security_engineer` (`CONTRIBUTING_ROLE`), `role.software_qa_test_automation_specialist` (`CONTRIBUTING_ROLE`, security testing within a scope the Security Engineer defines).
- **Activities:** security control validation; security testing within the defined scope; residual risk statement.
- **Artifact Contributions:** `artifact.security_control_assessment` updated (owned by `role.security_engineer`).
- **Knowledge-State Expectations:** `DRAFT`. Unvalidated controls are `UNKNOWN`.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.security`; `HUMAN_GATE_REFERENCE` → `decision.security_risk_acceptance`, and `decision.security_accreditation` where accreditation applies.
- **Exit Criteria:** every designed control validated or explicitly not; residual risk stated; accreditation position stated where relevant.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unvalidated security control, or residual risk that has not been characterised, is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward the release gate. Recording it as `UNKNOWN` makes it visible, not disposed of.

### Stage `S5` — Test and evidence
- **Objective:** produce test evidence against the acceptance criteria — evidence, not assurance.
- **Entry Criteria:** S3 exited at least `COMPLETE_WITH_OPEN_ITEMS`; acceptance criteria from S1 current.
- **Participating Roles:** `role.software_qa_test_automation_specialist` (`LEAD_ROLE`), `role.product_manager_business_analyst` (`CONTRIBUTING_ROLE`, acceptance-criteria interpretation), implementing engineers (`CONTRIBUTING_ROLE`, defect remediation).
- **Activities:** test strategy and automation; execution; coverage analysis against acceptance criteria; defect identification, reproduction, severity characterisation and lifecycle management.
- **Artifact Contributions:** `artifact.test_strategy`, `artifact.automated_test_suite`, `artifact.test_evidence_report`, `artifact.defect_record` — all owned by `role.software_qa_test_automation_specialist`.
- **Knowledge-State Expectations:** `DRAFT`. A passing test suite is `FACT` about the tests that ran; it is not a statement that the change is correct or safe.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.test_coverage`; `HUMAN_GATE_REFERENCE` → `decision.defect_deferral` for any open defect carried past this stage.
- **Exit Criteria:** every acceptance criterion has a test result; open defects recorded with severity; **no defect is closed by deferral inside this Workflow** — deferral is the human gate above.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an untested acceptance criterion, or an open defect at or above the band's defined severity, is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S6. Deferral is not a workflow act — `decision.defect_deferral` is the external Decision Right, and only it can permit progression with such a defect open.

### Stage `S6` — Release readiness
- **Objective:** assemble the readiness position so a human can decide whether to release — and can decide not to.
- **Entry Criteria:** S4 and S5 exited; required reviews satisfied or their absence explicitly recorded.
- **Participating Roles:** `role.product_manager_business_analyst`, `role.solution_architect`, `role.platform_devops_engineer`, `role.security_engineer`, `role.software_qa_test_automation_specialist` — all `CONTRIBUTING_ROLE`. **No `LEAD_ROLE` acquires release authority at this stage.**
- **Activities:** assemble release scope, test evidence, security position, open defects, rollback position and migration plan; state what is not covered.
- **Artifact Contributions:** `artifact.release_scope_recommendation` (owned by `role.product_manager_business_analyst`) — a **recommendation**, which is what its ID says; `artifact.recovery_and_continuity_design` where rollback design is required.
- **Knowledge-State Expectations:** the readiness package is `DRAFT` or `REVIEWED`. It does **not** become `APPROVED` by reaching this stage, and "all stages complete" is not authorisation.
- **Gate / Review References:** `HUMAN_GATE_REFERENCE` → **`decision.production_release`**; additionally `decision.production_infrastructure_change` and `decision.production_database_migration` where the release includes them, and `decision.service_level_commitment` where a service commitment changes. Each is a separate human decision; reaching S6 makes them due.
- **Exit Criteria:** the release decision is due, with evidence, residual risk, open defects and rollback position in front of the decision-maker.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `ESCALATED`, `CANCELLED`.
- **Open-Item Materiality:** any item bearing on the evidence basis of `decision.production_release` — an untested criterion, an unvalidated control, an open defect above severity, a missing required review, or an absent rollback position — is `MATERIAL_TO_NEXT_STEP_OR_GATE` and cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit. The outcome is `BLOCKED` or `ESCALATED` unless a **named external human Decision Right** — `decision.defect_deferral`, `decision.security_risk_acceptance` or `decision.emergency_production_change` as applicable — explicitly permits reaching the gate with it unresolved, in which case the reference is recorded and the item stays open.

## Branches / Exception Paths

- `BRANCH` — **user-facing change:** `role.ux_ui_information_architecture_specialist` engaged at S1–S2; `review.accessibility` and `review.design_quality` enter the review set.
- `BRANCH` — **data model or migration change:** `role.data_database_architect` and `role.database_data_engineer` engaged; `decision.production_database_migration` enters the gate set at S6.
- `BRANCH` — **external API contract change:** `role.integration_api_engineer` engaged; `decision.api_contract_publication` enters the gate set at S2.
- `BRANCH` — **no security-relevant surface:** S4 reduces to a recorded screening by `role.security_engineer`. It is not skipped, and the screening is still that Role's.
- `EXCEPTION_PATH` — **security finding at S4 or S5:** returns to S2 or S3 as `REWORK_REQUIRED`. A finding is not resolved by proceeding with it noted.
- `EXCEPTION_PATH` — **architecture deviation discovered at S3 or S5:** `ESCALATED` to `role.solution_architect`; the implementing Role does not ratify its own deviation.
- `EXCEPTION_PATH` — **production incident requiring emergency change:** routes to `workflow.incident_response_and_recovery` and to `decision.emergency_production_change`. This is an **emergency gate, not the absence of one**: the change is still gated, and what was bypassed relative to the normal path is recorded.
- `EXCEPTION_PATH` — **release-date pressure:** exits S6 as `COMPLETE_WITH_OPEN_ITEMS` or `BLOCKED`. It never exits by dropping `review.security`, `review.test_coverage` or the release gate.

No exception path bypasses any gate or review reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` targets: S5 → S3 on defect; S4 → S2/S3 on a security finding; S3 → S2 on architecture deviation; S2 → S1 on requirement invalidation; S6 → any earlier stage where readiness assembly exposes a gap.

Prior versions, test evidence, defect history, security findings and the reason for rework are preserved. A rework loop may not be used to discard a recorded defect or security finding.

## Open-Item Materiality

For this Workflow's terminal gate, `MATERIAL_TO_NEXT_STEP_OR_GATE` covers: any untested acceptance criterion; any unvalidated security control or uncharacterised residual risk; any open defect at or above the band's defined severity; any unratified deviation from the adopted architecture position; any missing `review.<id>` the criticality band requires; and any absent rollback position where the release is not trivially reversible.

**A material item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit at the progression it is material to.** The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.

The only exception is a **named external human Decision Right** explicitly permitting progression with the item unresolved — `decision.defect_deferral` for an open defect, `decision.security_risk_acceptance` for residual security risk, `decision.emergency_production_change` on the emergency path. In each case the gate reference is recorded, the item **remains open and unresolved**, and this Workflow neither decides the waiver nor asserts it was granted. Release-date pressure is not such a right.

## Completion Criteria

`COMPLETION_CRITERION` — S6 exited with the release decision due; every acceptance criterion tested; security position stated; open defects recorded with severity and their deferral status; rollback position stated; required reviews satisfied or their absence recorded.

**Completion is not release.** The Workflow completes at the gate.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the change is withdrawn from scope; the requirement is invalidated; a security or architecture finding makes the change unviable; or a human decision stops delivery.

On cancellation, the source change, test evidence, defect records, security findings and decision history are retained.

## Outputs / Resulting Artifact States

| Artifact | Owning Role | State at completion |
|---|---|---|
| `artifact.product_requirements` | `role.product_manager_business_analyst` | `DRAFT` or `REVIEWED` |
| `artifact.solution_architecture_specification`, `artifact.architecture_decision_record` | `role.solution_architect` | `DRAFT` or `REVIEWED` |
| `artifact.data_architecture_specification`, `artifact.database_migration_design` | `role.data_database_architect` | `DRAFT` or `REVIEWED` |
| `artifact.source_code_change` | `role.full_stack_software_engineer` | `DRAFT` or `REVIEWED` |
| `artifact.database_migration_script` | `role.database_data_engineer` | `DRAFT` — **not executed** |
| `artifact.deployment_pipeline` | `role.platform_devops_engineer` | `DRAFT` or `REVIEWED` |
| `artifact.security_control_assessment` | `role.security_engineer` | `DRAFT` or `REVIEWED` |
| `artifact.test_evidence_report`, `artifact.defect_record` | `role.software_qa_test_automation_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.release_scope_recommendation` | `role.product_manager_business_analyst` | `DRAFT` |

No artifact reaches `APPROVED` or `CANONICAL` through this Workflow, and no artifact is promoted to `REVIEWED` by stage movement — a governed review, not progression, does that.

`artifact.production_deployment_record` is **not** an output of this Workflow. It comes into existence on the far side of the human release gate.

## Authority / Review Boundary

- **No workflow stage may authorize production release.** `decision.production_release` is a human decision right. No stage outcome, no combination of `COMPLETE` outcomes and no completion state constitutes or implies it. Building the deployment pipeline is not authority to release through it.
- Production infrastructure change, production database migration, security accreditation and defect deferral are likewise human and are referenced, never satisfied.
- The S5 test cycle is producer quality control by the QA Role and does **not** satisfy `review.test_coverage`, `review.code` or `review.security`. QA's own independence constraints in its Role Card are not relaxed by this Workflow.
- `role.security_engineer` remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase` under Phase 4. This card does not widen that, and no stage routes around it.
- **Participation in this Workflow grants no professional authority.** A Role gains nothing beyond its own Role Card by participating, including at `LEAD_ROLE`; leading a stage is coordination, not entitlement.

## Criticality Scaling

| Band | Effect |
|---|---|
| Routine / Standard | Low blast radius, no personal or regulated data: S4 reduced to recorded screening; review references advisory; `review.code` expected. |
| Enhanced Review Candidate | Personal data, availability commitment or external interface: `review.security` and `review.test_coverage` expected; rollback position mandatory at S6. |
| Enhanced Decision-Grade | Regulated, safety-relevant, or high data-sensitivity change: full S4 mandatory; `review.security`, `review.architecture` and `review.test_coverage` mandatory; `decision.security_risk_acceptance` explicit before S6. |
| Major / Systemic | As above, plus mandatory `review.data_architecture` where data changes, accreditation position required, and no `COMPLETE_WITH_OPEN_ITEMS` exit at S6 for any open defect at or above the defined severity. |

Depth, review intensity and gate explicitness change. **Role identity does not change**, and there is no separate emergency or minor-change Workflow — emergency routing is an exception path with its own gate.

## Evidence / Traceability Requirements

Every requirement traceable to acceptance criteria and to a test result; every architecture decision recorded; every security control traceable from threat model to implementation to validation; every defect traceable with severity and disposition; every deviation from design recorded with its acceptance; rollback position stated; every gate reference recorded as due, satisfied or not reached.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no authority, Role scope, gate or artifact-ownership change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology. The deployment pipeline it references is an artifact owned by a Role, not an implementation defined here.
