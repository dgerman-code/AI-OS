# Phase 15 — Intent Understanding, Work Planning & Dynamic Workflow Composition

## Repository / branch

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`
Approved architecture basis: Phase 13 approval commit `2c4b90def9a60f8b384feef10f8428c5b437597c`

This branch is an **architecture proposal** only. Do not modify any approved Phase 1–13 artifact. Do not create runtime code, migrations, provider SDK integrations, queues, workers, schedulers, deployment, IaC, secrets, or production configuration. Do not create a PR.

All new Phase 15 artifacts must remain `PROPOSED`.

---

# 1. Problem to solve

AI-OS currently coordinates execution once a governed Workflow is already selected. That is insufficient for the intended product experience.

The user must be able to write a natural-language request without knowing or naming:

- Workflow IDs;
- Role IDs;
- Skills;
- Review Profiles;
- Decision Rights;
- Model Profiles;
- routing policies;
- work-item structures;
- orchestration internals.

AI-OS must understand the request, infer the intended work safely, and transform it into a governed execution proposal before the existing Orchestrator begins.

The target product behavior is:

```text
Natural-language request
        ↓
Intent understanding
        ↓
Context / scope resolution
        ↓
Objective and deliverable inference
        ↓
Task / work classification
        ↓
Criticality / risk / high-stakes assessment
        ↓
Role + Skill requirement inference
        ↓
Existing Workflow matching
        ↓
If no exact Workflow: compose an instance-level Execution Plan
        ↓
Add conditional specialist roles
        ↓
Resolve Review requirements
        ↓
Resolve applicable Decision Rights
        ↓
Resolve required knowledge / evidence / sources
        ↓
Create Tasks / Work Items / dependencies
        ↓
Governance preflight
        ↓
Hand off to the approved Orchestrator
        ↓
Model Router / execution
```

The user should not be forced to manually choose a workflow, role, model, or agent.

---

# 2. Architectural boundary

Create a first-class subsystem **before the existing Orchestrator**:

## Intent & Work Planning Layer

It may contain these logical functions, but they are **not autonomous agents** and must not be modeled as standing personas:

1. Request Interpreter
2. Context Resolver
3. Work Classifier
4. Workflow Planner
5. Governance Preflight

Preserve the identity chain and explicitly extend it where needed. At minimum:

`REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK != WORK ITEM != ROLE != MODEL != ORCHESTRATOR != HUMAN AUTHORITY`

Do not collapse Work Plan into Workflow Registry identity.

The layer must never:

- invent a Role, Skill, Review Profile, Decision Right, or approved Workflow;
- turn a generated plan into an approved reusable Workflow;
- select or exercise human authority;
- treat confidence as authority;
- downgrade criticality, sensitivity, residency, materiality, review or decision requirements;
- silently cross scope boundaries;
- infer a missing Decision Right from apparent business necessity;
- convert AI output into approved or canonical knowledge;
- create a permanent autonomous agent.

---

# 3. Required distinction: reusable Workflow vs instance-level Work Plan

This distinction is foundational.

## Workflow

A governed reusable registry pattern, as defined by Phase 5.

## Work Plan / Execution Proposal

A task-specific, instance-level composition created from approved/proposed inputs for one request. It may reference approved Workflows, Roles, Skills, Review Profiles, Decision Rights and knowledge requirements, but it is not itself a Workflow Registry object.

The system must support two paths:

### A. MATCH

The request maps cleanly to one approved Workflow or approved Workflow composition.

Example:

`prepare an EU grant application` → `workflow.eu_grant_application_development`

### B. COMPOSE

No exact reusable Workflow exists. The planner creates an **instance-level Work Plan** from governed primitives and approved identities.

Example:

```text
Stage 1 — evidence intake
Stage 2 — financial analysis
Stage 3 — legal review
Stage 4 — communication strategy
Stage 5 — drafting
Stage 6 — independent review
Stage 7 — human Decision Right
```

This plan must not be written back as an approved Workflow automatically.

If repeated plan patterns emerge, AI-OS may produce a separate **PROPOSED workflow candidate suggestion** for human governance review. It must never self-register or self-approve it.

---

# 4. Core design requirements

Design the architecture for these behaviors.

## 4.1 Natural-language intent understanding

The Request Interpreter must derive a structured `Work Intent` from ordinary user language.

At minimum infer or represent explicitly as `UNKNOWN`:

- user objective;
- requested outcome / deliverable;
- action vs analysis vs advice vs drafting vs monitoring vs decision support;
- relevant entities;
- scope candidates;
- urgency / deadline if stated;
- external vs internal act;
- reversible vs irreversible act;
- whether a consequential commitment may occur;
- whether external transmission is contemplated;
- whether user is asking to execute or only prepare/recommend;
- language / audience / channel where relevant.

Do not force questions when a safe inference is possible.

## 4.2 Clarification policy

Define an explicit principle:

> Infer when safe; clarify only when ambiguity can materially change scope, authority, professional conclusion, irreversible action, or governed outcome.

Create a clarification decision model. It must distinguish:

- safe defaults;
- recoverable ambiguity;
- material ambiguity requiring clarification;
- authority ambiguity requiring clarification or block;
- scope ambiguity requiring clarification;
- low-confidence but low-consequence inference.

The system must not ask the user to choose internal architecture objects such as Workflow IDs or Roles unless the user explicitly wants to.

## 4.3 Context / scope resolution

Infer the most likely governed scope from request context and available references, but never cross a separator boundary by guess.

Support:

- GLOBAL;
- ORGANISATION;
- INDEPENDENT BUSINESS / VENTURE;
- PERSONAL / AD-HOC INITIATIVE;
- PERMANENT FUNCTION / BUSINESS AREA;
- PROGRAMME / PORTFOLIO;
- PRODUCT / SERVICE;
- PROJECT;
- OPERATIONAL WORKSTREAM;
- TASK-level context where applicable.

Where multiple scopes are materially plausible and selecting the wrong one changes available knowledge, authority, residency, or sensitivity handling, clarification is mandatory.

## 4.4 Criticality / high-stakes inference

Use the approved project-criticality policy and all inherited governance requirements.

The Work Planner must be able to detect that an apparently simple request becomes high-stakes because it involves, for example:

- IFI/DFI;
- PPP/project finance/blended finance;
- public/municipal/sovereign actors;
- regulated infrastructure;
- procurement / State Aid / public funding;
- cross-border issues;
- ESG / E&S;
- covenants, security, offtake;
- lender / investor / regulator / grant authority / board submission;
- integrity / sanctions / AML;
- data / cyber / safety;
- legal or contractual commitment;
- external institutional communication.

Criticality may raise rigor and never lower approved requirements.

## 4.5 Role and Skill inference

The planner must infer which approved Roles and Skills are needed from semantics of the task.

Examples:

- financial model → Financial Modelling Specialist;
- PPP suitability → PPP / Concession Specialist + Legal & Regulatory Lead + Funding & Bankability Architect where applicable;
- grant application → EU Grants & Programmes Specialist + Grant Financial Compliance / Budget Specialist + reporting/deliverables roles where applicable;
- difficult external reply → Difficult Conversations & Communication Strategy capability if approved in the future;
- legally consequential correspondence → Legal role co-activation;
- publication → Institutional Communications + applicable Decision Right.

Role activation must be based on governed compatibility / capability requirements, not free-form persona selection.

If a required Role/Skill is unavailable, unapproved, or incompatible, fail closed or produce a constrained plan rather than inventing it.

## 4.6 Workflow matching and composition

Define a deterministic, inspectable planning sequence:

1. derive Work Intent;
2. resolve scope;
3. derive work requirements;
4. derive criticality and risk flags;
5. infer required Role/Skill capabilities;
6. search approved Workflow candidates;
7. score / rank applicability;
8. select one where fit is sufficiently strong and no governance conflict exists;
9. otherwise compose an instance-level Work Plan from approved primitives;
10. attach reviews, Decision Rights, evidence requirements and stop conditions;
11. validate the plan;
12. hand it to the Orchestrator only after governance preflight passes.

Do not let a semantic similarity score override an explicit Workflow precondition, Role constraint, Review Profile, Decision Right, or scope boundary.

## 4.7 Reviews and Decision Rights

The planner must infer review and authority requirements from the contemplated acts and artifacts.

It must never ask merely "is this high stakes?" and then make up a gate.

It must resolve applicable named approved Review Profiles and Decision Rights.

Missing applicable authority blocks.

A Work Plan that includes an external act must identify whether the system is:

- only preparing content;
- requesting review;
- requesting a Decision Right exercise;
- authorized to execute a non-authority-bearing action;
- blocked from transmission.

## 4.8 Knowledge and evidence planning

The planner must identify what evidence / sources / prior context are required before a stage can safely execute.

Use Phase 8 semantics:

- SOURCE
- EVIDENCE
- FACT_CLAIM
- ASSUMPTION
- CALCULATION
- INFERENCE
- AI_SUGGESTION
- UNKNOWN

Do not turn assumptions or AI suggestions into facts merely because a plan needs them.

## 4.9 Work-item generation

Define how a Work Plan becomes Tasks / Work Items before handoff to the Orchestrator.

The Work Planner may instantiate work items only from validated plan stages and approved definitions.

Each Work Item must carry enough information for deterministic downstream orchestration, including at least:

- work intent reference;
- scope reference;
- stage / dependency references;
- required Role / Skill envelope;
- expected artifact / output;
- required input knowledge states;
- review/gate requirements;
- sensitivity / residency / handling constraints;
- criticality;
- completion criteria;
- failure / escalation disposition.

Do not choose a model here. Model selection stays Phase 9 Router responsibility.

---

# 5. Planning object model

Propose exact first-class records, with stable identities and status semantics. At minimum evaluate the need for:

- `Request`
- `WorkIntent`
- `ScopeResolution`
- `WorkRequirementSet`
- `WorkflowMatchAssessment`
- `WorkPlan`
- `PlanStage`
- `RoleRequirement`
- `SkillRequirement`
- `ReviewRequirement`
- `DecisionRequirement`
- `EvidenceRequirement`
- `ClarificationRequirement`
- `PlanningFinding`
- `PlanValidationResult`
- `WorkflowCandidateSuggestion`

For each, state:

- purpose;
- authority status;
- source of truth;
- lifecycle;
- versioning;
- whether AI may create it;
- whether human approval is needed;
- whether it may be persisted;
- whether it may affect execution directly.

Keep AI-generated planning records non-authoritative unless and until an approved rule says otherwise.

---

# 6. Confidence is not authority

Create a confidence model only if useful, and explicitly separate:

- semantic confidence;
- scope confidence;
- workflow-fit confidence;
- role-fit confidence;
- risk-detection confidence;
- authority-resolution confidence.

A confidence score must never:

- grant a Right;
- waive review;
- change knowledge state;
- make a candidate Workflow approved;
- let the system cross scope;
- substitute for missing evidence.

Low confidence may trigger clarification or additional evidence retrieval. High confidence never grants authority.

---

# 7. Planning failure modes

Create an explicit failure taxonomy, including at least:

- NO_VALID_SCOPE
- AMBIGUOUS_SCOPE
- NO_MATCHING_WORKFLOW
- PLAN_COMPOSITION_REQUIRED
- REQUIRED_ROLE_UNAVAILABLE
- REQUIRED_SKILL_UNAVAILABLE
- REVIEW_PROFILE_UNAVAILABLE
- NO_APPLICABLE_DECISION_RIGHT
- EVIDENCE_REQUIREMENT_UNSATISFIED
- CRITICALITY_UNRESOLVED
- CONFLICTING_REQUIREMENTS
- UNSAFE_INFERENCE
- PLAN_VALIDATION_FAILED

For each, define whether the result is:

- clarify;
- block;
- escalate;
- compose a plan;
- continue with constrained scope;
- produce recommendation only.

---

# 8. Examples that MUST be fully worked

Create detailed worked examples with the internal planning objects shown.

## Example 1 — ordinary writing request

"Create a LinkedIn post about this news."

The system should infer a lightweight communication workflow, not ask the user to choose a Role or Workflow.

## Example 2 — difficult partner communication

"Review this partner email. They blame us for the delay. Check whether they are right and prepare a firm but professional response. I do not want to damage the relationship."

The system should detect fact/evidence work, possible legal/contractual implications, communication strategy, external transmission gate, and appropriate reviews.

## Example 3 — investment / IFI request

"Prepare me for a meeting with EIB about this municipal infrastructure project."

The system should infer project context, bankability/funding analysis, likely technical/financial/legal inputs, high-stakes context, meeting pack artifact, and review requirements.

## Example 4 — ambiguous authority request

"Send them confirmation that we accept the terms."

The system must detect possible contractual commitment, resolve applicable Decision Rights, and block or request authority rather than simply drafting/sending.

## Example 5 — no exact Workflow exists

A multi-domain user request that requires a composed Work Plan. Demonstrate that the plan is instance-level and does not self-register as a Workflow.

## Example 6 — repeated pattern

Show how the system can suggest a `PROPOSED` Workflow candidate after repeated similar Work Plans without auto-approval.

---

# 9. Human experience requirement

The product UX must hide internal complexity by default.

The normal user should see:

- what AI understood;
- what it plans to produce;
- important assumptions / missing information;
- only the clarification questions that materially matter;
- where human approval is required;
- progress / blockers / results.

The user should not normally see or have to select:

- Role IDs;
- Skill IDs;
- Workflow IDs;
- Review Profile IDs;
- Model Profiles;
- Router details;
- orchestration state-machine internals.

These may remain inspectable for governance/admin/debug views.

---

# 10. Relationship to the Orchestrator

Do **not** rewrite or weaken approved Phase 11 architecture.

Instead define a clean handoff boundary:

```text
Natural-language Request
        ↓
Phase 15 Intent & Work Planning Layer
        ↓
VALIDATED WORK PLAN / WORKFLOW SELECTION
        ↓
Trigger compatible with Phase 11
        ↓
Approved Orchestrator
```

The planner prepares a valid trigger envelope; the Orchestrator remains responsible for run creation, stage activation, assignment, routing requests, reviews, Decision Right requests, waiting, retries, rework, blocking, escalation and completion.

The planner must never behave as a second Orchestrator.

---

# 11. Architecture deliverables

Create a self-contained Phase 15 architecture package under:

`planning/`

Recommended artifacts:

1. `architecture/intent-work-planning-architecture.md`
2. `planning/request-intent-model.md`
3. `planning/context-scope-resolution.md`
4. `planning/work-classification-and-criticality.md`
5. `planning/role-skill-requirement-inference.md`
6. `planning/workflow-matching-and-composition.md`
7. `planning/work-plan-object-model.md`
8. `planning/clarification-policy.md`
9. `planning/governance-preflight.md`
10. `planning/orchestrator-handoff-contract.md`
11. `planning/failure-and-escalation-model.md`
12. `planning/workflow-candidate-learning-boundary.md`
13. `planning/user-experience-contract.md`
14. `planning/exemplars.md`
15. `planning/open-items.md`
16. `planning/phase-15-self-check.md`
17. `validation/phase_15_validation.py`
18. `validation/phase_15_mutation_probes.py`

You may adjust filenames only if necessary for coherence. Do not modify approved Phase 1–13 files.

---

# 12. Assurance requirements

The Phase 15 validator must test substantive cross-document consistency, not only phrase presence.

At minimum test that:

- Work Plan never becomes Workflow identity;
- planner never grants authority;
- planner never chooses a Model Profile;
- planner does not cross scope on confidence;
- high confidence cannot waive clarification where authority/scope is material;
- missing Decision Right fails closed;
- candidate Workflow remains PROPOSED;
- composed plan remains instance-level;
- Role/Skill requirements resolve against approved registries or are explicitly unavailable;
- review requirements do not become satisfied by planning;
- generated knowledge remains correctly typed;
- user is not required to provide internal IDs;
- Orchestrator handoff requires a validated workflow/work-plan path;
- repeated plan detection cannot self-register a Workflow;
- clarification policy distinguishes safe inference from material ambiguity.

Add adversarial mutation probes for nearby cross-document contradictions.

Do not overstate harness credibility. Report first-run redundant or escaped probes honestly.

---

# 13. Non-goals

Do not implement:

- LLM inference runtime;
- embeddings or semantic search engine;
- production planner service;
- vector DB;
- provider integration;
- workflow execution runtime;
- agent framework;
- live RAG;
- production UI;
- database migrations;
- queues/workers/schedulers;
- autonomous approval;
- automatic registry mutation.

This phase defines architecture and contracts only.

---

# 14. Required final report

Return sections A–R:

A. FINAL ARCHITECTURE SUMMARY
B. BASELINE / CONTAINMENT
C. PROBLEM STATEMENT
D. IDENTITY / SEPARATION MODEL
E. REQUEST / INTENT MODEL
F. SCOPE / CONTEXT RESOLUTION
G. WORK CLASSIFICATION / CRITICALITY
H. ROLE / SKILL INFERENCE
I. WORKFLOW MATCHING / DYNAMIC COMPOSITION
J. CLARIFICATION POLICY
K. REVIEWS / DECISION RIGHTS / GOVERNANCE PREFLIGHT
L. KNOWLEDGE / EVIDENCE PLANNING
M. ORCHESTRATOR HANDOFF
N. FAILURE / ESCALATION MODEL
O. UX CONTRACT
P. ASSURANCE / VALIDATION / MUTATION RESULTS
Q. OPEN ITEMS / BLOCKERS
R. READINESS VERDICT

The only acceptable readiness wording at foundation stage is one of:

- `READY FOR INDEPENDENT PHASE 15 ARCHITECTURE REVIEW`
- `NOT READY — REMAINING BLOCKERS`

Do not create human approval. Do not create a PR.