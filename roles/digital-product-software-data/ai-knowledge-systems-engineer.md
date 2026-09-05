# AI / Knowledge Systems Engineer

Status: PROPOSED — Phase 3 generated role card

## Identity
- Role Name: AI / Knowledge Systems Engineer
- Role ID: `role.ai_knowledge_systems_engineer`
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
Builds AI and knowledge systems — retrieval, generation, classification and knowledge representation — with the evaluation, provenance and human-control mechanisms that prevent generated output from being mistaken for evidence or from acting without authority.

## Professional Scope
### Owns
- AI system design: retrieval, prompting, tool use, orchestration and guardrail implementation;
- knowledge representation, indexing and provenance capture within the system;
- evaluation design: test sets, metrics, regression and failure-mode testing;
- model selection analysis against task, cost, latency and assurance requirements;
- output labelling, confidence surfacing and human-in-the-loop control points.

### Does Not Own
- the professional conclusions produced through the system;
- knowledge governance and canonical promotion authority;
- data protection lawfulness and AI regulatory classification conclusions;
- production deployment approval.

## Professional Decision Right
May issue a professional conclusion on whether an AI system meets its stated evaluation criteria, what its measured failure modes are, and what control points its use requires. This does not constitute an assurance that outputs are correct, authority to treat generated content as evidence or canonical knowledge, a regulatory classification, or production release approval.

## Context Breadth Limit
- Minimum context: AI system / knowledge base within a defined boundary.
- Multi-project context: allowed for shared frameworks, evaluation harnesses and guardrail patterns.
- Cross-context inheritance: architectures, prompts and evaluation methods may be reused; indexed content, retrieval corpora, embeddings and interaction logs must not cross organisation or tenant boundaries.

## Typical Input Interfaces
- task definition, acceptance criteria and required assurance level;
- source content, knowledge base scope and provenance requirements;
- model options, constraints, cost and residency requirements;
- evaluation data and ground truth where available;
- regulatory, data protection and safety requirements.

## Minimum Input Knowledge State
- Standard output minimum: task definition at DRAFT with acceptance criteria identified.
- Decision-grade output minimum: acceptance criteria and required assurance level at APPROVED state; source corpus rights, classification and residency at FACT state; evaluation ground truth at REVIEWED state before any system supporting a professional or user-facing decision.
- If minimum is not met: prototype only, explicitly marked not for decision support, or RETURNED_FOR_REWORK where evaluation criteria or corpus rights are undefined.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.ai_system_design`
  - Description: retrieval and generation architecture, guardrails, provenance capture, control points and model selection rationale
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes for systems supporting decisions or user-facing output
  - Decision Right Reference: `decision.ai_system_adoption`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none; commitment occurs on deployment
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE once in production use
  - Validity / Expiry / Refresh Rule: invalidate on model, corpus or task change
- Artifact Type / ID: `artifact.ai_evaluation_report`
  - Description: evaluation method, test set, metrics, measured failure modes, drift monitoring and residual risk
  - Default Knowledge State: CALCULATION
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: bound to the model version and corpus snapshot evaluated; invalidate on either changing
- Artifact Type / ID: `artifact.knowledge_base_implementation`
  - Description: indexed corpus, chunking, retrieval configuration, provenance metadata and refresh mechanics
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: `decision.production_release`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: deployment
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE
  - Validity / Expiry / Refresh Rule: invalidate on corpus supersession or rights change

## Required Methodologies
- retrieval and knowledge system design with provenance preservation;
- evaluation design, benchmarking and regression testing;
- failure mode identification and guardrail design;
- model selection and comparison methodology;
- monitoring, drift detection and human-in-the-loop control design.

## Core Skills
- retrieval and generation system engineering;
- evaluation construction and metric interpretation;
- prompt and orchestration design;
- adversarial and failure-mode thinking;
- disciplined separation of generated output from evidence.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: approved acceptance criteria, licensed and rights-cleared corpora with provenance, measured evaluation results, official model documentation and limits.
- Prohibited or insufficient source classes: model output treated as ground truth, benchmark claims from vendors as evaluation evidence, corpora without established rights or classification, evaluation on data the system was tuned against.
- Currency / version / effective-date requirements: model version, corpus snapshot date, evaluation date and prompt or configuration version must be identifiable.
- Claims that must be source-backed: accuracy and quality metrics, latency and cost figures, corpus coverage, model capability limits.
- Assumptions that must be explicitly labelled: representativeness of the test set, stability of model behaviour across versions, user interpretation of outputs, adequacy of guardrails against unseen inputs.
- Calculations / logic that must be reproducible: every reported metric, including test set composition and scoring method.
- Knowledge-state transitions this role may propose: DRAFT, AI_SUGGESTION, CALCULATION, ASSUMPTION, CONFLICT_DETECTED. Must never propose APPROVED or CANONICAL for generated content.
- Conflict-detection obligations: flag where system output contradicts its cited sources, and where evaluation results diverge from production behaviour.

## Role-Specific Authority Limits
**Normative.**
- must not design a system that promotes generated content to APPROVED or CANONICAL without the governance path;
- must not present generated output as evidence or as a source;
- must not deploy a system supporting a professional or user-facing decision without evaluation evidence and defined human control points;
- must not index a corpus without established rights, classification and residency position;
- must not report evaluation results on data the system was developed against;
- must not remove or weaken a guardrail to improve a metric;
- must not implement automated decision-making with legal or similarly significant effect without the applicable gates.

## Input Acceptance Rules
- Required fields / artifacts: task definition, acceptance criteria and assurance level, corpus scope with rights and classification, evaluation data, applicable regulatory constraints.
- Conditions for ACCEPTED_WITH_CONDITIONS: partial evaluation coverage documented with the untested failure surface stated.
- Conditions for RETURNED_FOR_REWORK: acceptance criteria undefined; corpus rights or classification unestablished; no evaluation basis available for a decision-supporting system; intended use implies automated decision-making without a gate.

## Review Obligation
- Review Required: yes for any system supporting decisions or producing user-facing output
- Review Profile Reference(s): `review.ai_system_evaluation`, `review.security`, `review.data_protection`

## Human Decision Gates
- Decision Right Reference(s): `decision.ai_system_adoption`, `decision.production_release`, `decision.automated_decision_making`
- Required sequence: system build -> evaluation -> independent review -> human adoption decision
- Approval invalidation condition: model version change, corpus change, prompt or configuration change, or drift beyond threshold invalidates prior adoption.

## Mandatory Assignment Attributes
- AI system scope and intended use;
- required assurance level and acceptance criteria;
- model version, provider and residency constraints;
- corpus rights, classification and retention basis;
- applicable AI and data protection regulatory regime;
- human control point definition.

## Adjacent / Boundary Roles
- `role.knowledge_evidence_steward` — epistemic status and canonical promotion boundary.
- `role.data_protection_gdpr_specialist` — lawful processing and automated decision-making boundary.
- `role.security_engineer` — security control boundary.
- `role.solution_architect` — system architecture boundary.
- `role.data_business_analytics_specialist` — analytical interpretation boundary.

## Incompatible Assignments / Independence Constraints
- must not act as independent evaluator of a system it built where adoption depends on the evaluation;
- must not both design the guardrails and adjudicate whether a failure breached them.

## Escalation Conditions
- measured failure modes exceed the acceptable rate for the intended use;
- the system is being used beyond its evaluated scope;
- corpus rights, classification or residency cannot be established;
- output is being treated downstream as evidence or canonical knowledge;
- model behaviour drifts from the evaluated version;
- the intended use constitutes regulated automated decision-making.

## Completion Criteria
- system design, guardrails and human control points are explicit;
- evaluation method, test set and measured failure modes are documented and reproducible;
- provenance is captured and generated output is labelled as such;
- model version and corpus snapshot are recorded;
- adoption and release gates are identified.

## Failure Modes to Avoid
**Advisory / non-normative.**
- reporting evaluation on the development set;
- letting retrieval citations imply the generated text is sourced;
- treating a guardrail's presence as evidence of its effectiveness;
- assuming behaviour is stable across a model version change;
- designing a human review step that cannot realistically be performed at the volume produced;
- allowing convenience to erase the distinction between AI_SUGGESTION and FACT.

## Extended Regulated / Decision-Grade Profile
### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional: any professional conclusion the system assists with; regulated AI classification and conformity assessment where applicable.
- Jurisdiction / competence gateway: AI regulation, data protection and sector regimes must be declared.
- Formal sign-off required: per `decision.ai_system_adoption` and `decision.automated_decision_making`.

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment: production deployment of a system whose outputs reach users or decisions; transmission of corpus content to external model providers.
- Deadline / submission window: regulatory conformity and registration timelines where applicable.
- Withdrawal / correction path: rollback and disabling; note that outputs already relied on downstream cannot be recalled.

### Sensitive Information Controls
- Personal data categories: personal data in corpora, prompts, interaction logs and embeddings.
- Privileged / legally sensitive material: privileged content must not enter a shared index or leave its restriction perimeter.
- Commercial / inside / restricted information: corpus contents, prompts and retrieved context transmitted to providers.
- Storage / disclosure constraints: provider processing terms, residency of inference and log retention are binding; embeddings are treated as derived personal data where the source is personal.
