# Claude Code Prompt — Phase 5 Workflow Registry Foundation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-5-workflow-registry`
Starting baseline: Phase 4 human-approved branch state at commit `8a0d8d18525cb1adf54fdf74f3fb625f5be6fe3d`

Phase 4 is APPROVED as architecture. Phase 5 starts now.

This is an **architecture and registry-design task only**.
Do not implement runtime orchestration, database schema, APIs, UI, queues, agents, model routing, automation code or execution engine.
Do not alter approved Phase 3 Role Cards.
Do not alter Phase 4 mapping relationships, Skill/Pack authority boundaries or Phase 4 approval records.
Do not create a PR.
Do not mark Phase 5 APPROVED or CANONICAL.

## Phase 5 objective

Design the AI-OS **Workflow Registry**: a reusable, provider-independent registry describing how work moves from trigger to completion across Roles, Skills, artifacts, states, gates and exception paths, without letting a Workflow own professional authority or human decisions.

The Workflow Registry must sit downstream from the approved Role Registry and Skill Registry.

Core separation to preserve:

`ROLE != SKILL != WORKFLOW != REVIEW PROFILE != DECISION RIGHT != MODEL != RUNTIME`

A Workflow coordinates work. It does not become a Role, does not own a professional conclusion, does not grant review independence, does not grant human authority and does not itself make information canonical.

## Read first

Read at minimum:
- `reviews/phase-3-final-approval.md`
- `reviews/phase-4-final-approval.md`
- `architecture/skill-registry-design.md`
- `architecture/role-to-skill-mapping-rules.md`
- `architecture/project-criticality-policy.md`
- all Role Card standards/templates
- Skill / Skill Pack standards/templates
- representative approved Role Cards from project delivery, finance, legal/compliance, EU programmes, software/data and knowledge/disclosure
- current knowledge-state terminology and common constraints

Preserve established knowledge states:
`SOURCE`, `FACT`, `ASSUMPTION`, `CALCULATION`, `AI_SUGGESTION`, `DRAFT`, `REVIEWED`, `APPROVED`, `CANONICAL`, `SUPERSEDED`, `CONFLICT_DETECTED`, `UNKNOWN`.

## Required Phase 5 foundation deliverables

Create these files:

1. `architecture/workflow-registry-design.md`
2. `workflows/_templates/workflow-card-template.md`
3. `workflows/_standards/common-workflow-constraints.md`
4. `workflows/master-workflow-universe.md`
5. `workflows/exemplars/project-development-readiness.md`
6. `workflows/exemplars/eu-grant-application-development.md`
7. `workflows/exemplars/software-change-delivery.md`
8. `workflows/exemplars/decision-grade-document-preparation.md`
9. `reviews/phase-5-foundation-self-check.md`

All new Phase 5 artifacts must be `PROPOSED`.

---

# 1. Workflow identity model

Define a Workflow as a reusable governed coordination pattern that specifies:
- triggering condition;
- required inputs / preconditions;
- ordered or partially ordered stages;
- stage-entry criteria;
- stage-exit criteria;
- participating Role IDs;
- applicable Skill / Specialisation / Pack references;
- artifact inputs / contributions / outputs;
- knowledge-state expectations;
- gate references;
- exception / rollback / rework paths;
- completion criteria;
- termination / cancellation criteria;
- criticality-sensitive depth;
- version / status / governance owner.

A Workflow must NOT:
- own professional methodology that belongs to a Role;
- own a first-class professional conclusion;
- create artifact ownership where a Role Card already defines it;
- create a Review Profile or reviewer identity;
- create or grant a Decision Right;
- turn AI output into APPROVED/CANONICAL by itself;
- select or bind an AI model as identity;
- execute itself.

## Workflow ID convention

Use IDs such as:
`workflow.<stable_snake_case_name>`

Do not encode organisation, model vendor, temporary project name, individual person, version or runtime technology into the stable ID.

---

# 2. Workflow versus adjacent concepts

The architecture must explicitly distinguish:

### Workflow vs Role
Role = professional methodology/ownership boundary.
Workflow = coordination/order of work among Roles.

### Workflow vs Skill
Skill = reusable capability/technique.
Workflow = when and in what sequence capabilities/roles participate.

### Workflow vs Project Plan
Workflow = reusable registry pattern.
Project plan = assignment-specific instantiated schedule/tasks/dates/resources.

### Workflow vs SOP
SOP = operating instruction/procedure, usually organisation-specific.
Workflow = governed cross-role coordination pattern; may reference an SOP but is not necessarily one.

### Workflow vs Checklist
Checklist = verification list.
Workflow = stateful coordination path with progression, branches and gates.

### Workflow vs Review Profile
Review Profile = independent review identity/methodology, reserved for later phase.
Workflow may reference a review requirement but may not define reviewer independence.

### Workflow vs Decision Right
Decision Right = human authority.
Workflow may reference a required decision gate but does not own, satisfy or bypass it.

### Workflow vs Orchestrator
Orchestrator/runtime = later implementation that executes/schedules workflow instances.
Registry = declarative architecture only.

---

# 3. Workflow composition model

Define a minimal composition model with these primitives:

- `TRIGGER`
- `PRECONDITION`
- `STAGE`
- `ACTIVITY`
- `ARTIFACT_CONTRIBUTION`
- `STATE_EXPECTATION`
- `GATE_REFERENCE`
- `BRANCH`
- `EXCEPTION_PATH`
- `REWORK_LOOP`
- `COMPLETION_CRITERION`
- `TERMINATION_CONDITION`

Do not create a runtime DSL. Keep it human-readable and registry-oriented.

Every Stage must answer:
- Why does this stage exist?
- Which Role(s) participate?
- What may they contribute?
- What must be true to enter?
- What must be true to exit?
- What artifact/state changes are expected?
- Which gate/review reference may block progression?

---

# 4. Workflow participation relationships

Define a small controlled vocabulary for Role participation inside a Workflow. Prefer no more than 5 relationship types.

Recommended starting vocabulary to validate:
- `LEAD_ROLE` — coordinates the stage/workflow but gains no authority beyond Role Card.
- `CONTRIBUTING_ROLE` — contributes bounded work/artifact content.
- `CONSULTED_ROLE` — provides professional input when trigger applies.
- `REVIEW_REQUIRED_REFERENCE` — not a Role relationship; points to later Review Profile requirement.
- `HUMAN_GATE_REFERENCE` — not a Role relationship; points to Decision Right / human gate.

If a better controlled model is needed, refine it, but do NOT use RACI mechanically and do NOT create fake approver Roles.

A Role may be workflow lead without owning all conclusions/artifacts in the workflow.

---

# 5. Workflow stage transition semantics

Define clear progression rules:

- Stage completion is not approval.
- `DRAFT -> REVIEWED -> APPROVED -> CANONICAL` transitions cannot be inferred solely from stage movement.
- A workflow may require a knowledge state as an entry/exit condition, but may not itself promote the state unless the underlying governed human/review rule permits it.
- `CONFLICT_DETECTED` or `UNKNOWN` must be able to block or branch a workflow where material.
- Critical unresolved assumptions must not disappear merely because a workflow advances.

Define at least these generic stage outcomes:
- COMPLETE
- COMPLETE_WITH_OPEN_ITEMS
- BLOCKED
- REWORK_REQUIRED
- ESCALATED
- CANCELLED

These are workflow-instance progression outcomes, not knowledge states.

---

# 6. Criticality behavior

Inherit `architecture/project-criticality-policy.md`.

Criticality may increase:
- evidence depth;
- number of specialist contributions;
- mandatory stage depth;
- required reviews/gate references;
- traceability granularity;
- exception handling rigor;
- rework requirements.

Criticality must NOT create a new Workflow identity merely because a project is larger.

Prefer one workflow with criticality-conditioned depth over duplicate workflows such as “small-project workflow” and “large-project workflow” unless the professional process is genuinely different.

---

# 7. Workflow families / master universe

Create `workflows/master-workflow-universe.md` with a bounded candidate universe, not hundreds of workflows.

Use 8–12 families maximum. Suggested candidates to test and normalize:
- Project / Investment Development
- Programme / Grant Delivery
- Strategy / Policy / Institutional
- Commercial / Business Development
- Finance / Transaction
- Legal / Compliance / Risk
- Product / Software / Data Delivery
- Knowledge / Documentation / Disclosure
- Operations / Organisational Change

For each family list candidate reusable Workflows with one-sentence scope.

Aim for approximately **30–50 candidate workflows**, not micro-workflows.

Granularity rule:
Create a Workflow only when it represents a reusable coordination pattern across multiple activities/stages. Do not create a workflow for a single skill invocation, document heading, one-off approval click or trivial two-step action.

Flag likely overlap groups for later audit.

---

# 8. Workflow Card template

The template must include at least:

## Identity
- Workflow Name
- Workflow ID
- Version
- Status
- Workflow Family
- Governance Owner
- Criticality Applicability

## Purpose

## Trigger

## Preconditions

## Scope
- Covers
- Does Not Cover

## Participating Roles
Table with Role ID, participation type, stage(s), authority boundary note.

## Activated Skills / Packs
References only; mapping eligibility remains governed by Phase 4. A Workflow cannot make a Role compatible with a Skill that Phase 4 does not allow.

## Inputs

## Stages
For each Stage:
- Stage ID
- Objective
- Entry Criteria
- Participating Roles
- Activities
- Artifact Contributions
- Knowledge-State Expectations
- Gate / Review References
- Exit Criteria
- Possible Outcomes

## Branches / Exception Paths

## Rework Rules

## Completion Criteria

## Termination / Cancellation Criteria

## Outputs / Resulting Artifact States

## Authority / Review Boundary

## Criticality Scaling

## Evidence / Traceability Requirements

## Versioning / Change Control

## Non-Runtime Statement

---

# 9. Common workflow constraints

Create `workflows/_standards/common-workflow-constraints.md` with enforceable architecture rules, including:

1. Workflow coordination grants no professional authority.
2. Role Card authority always outranks Workflow prose.
3. Phase 4 Role-to-Skill compatibility cannot be widened by Workflow.
4. Workflow stage completion is not human approval.
5. Workflow cannot create or satisfy independent review identity.
6. Workflow cannot self-promote knowledge states.
7. AI output remains AI_SUGGESTION/DRAFT until governed transition.
8. Every external or costly-to-reverse transmitting act must preserve the applicable human-gate reference where one exists.
9. Exceptions must not silently bypass a gate.
10. Rework loops must preserve provenance and prior state/history.
11. Cancellation does not delete evidence or audit history.
12. Workflow version change must not silently alter authority or Role scope.
13. Workflow may narrow applicability but cannot widen Role/Skill applicability.
14. Runtime implementation must later validate against registry, not mutate registry semantics.

---

# 10. Four exemplar workflows

Create four detailed exemplar cards to stress-test the architecture.

## A. `workflow.project_development_readiness`
Cross-role path from project definition/evidence gathering through technical/commercial/financial/legal/ESG readiness assessment to a decision-grade readiness position.

Must preserve boundaries among:
- Project Development Lead
- Technical / Feasibility Lead
- Commercial & Demand
- CAPEX
- Financial Modelling
- Funding & Bankability
- Legal / Regulatory
- ESG / E&S
- Risk
- Knowledge & Evidence

Do not let Project Development Lead absorb specialist conclusions.

## B. `workflow.eu_grant_application_development`
From call selection and requirement capture through consortium/work-package/budget/content assembly to submission readiness.

Use relevant Roles such as:
- EU Grants & Programmes
- Consortium / Partner Coordination
- Grant Financial Compliance / Budget
- Deliverables / Reporting as applicable
- Learning/VET or sector specialists only when context triggers
- Legal / GDPR / communications where triggered

Submission remains a human decision right.

## C. `workflow.software_change_delivery`
From change request/requirement through architecture, implementation, testing, release readiness and production-release gate.

Preserve boundaries among:
- Product Manager / BA
- UX/UI
- Solution Architect
- Full-Stack
- Integration/API
- Platform/DevOps
- Data/DB Architect
- Database/Data Engineer
- Security
- QA/Test Automation

No workflow stage may authorize production release.

## D. `workflow.decision_grade_document_preparation`
Generic reusable pattern for preparing a decision-grade document from sources/evidence through drafting, specialist contribution, traceability, review requirement and human approval gate.

Must demonstrate:
- source verification;
- fact/assumption/calculation separation;
- AI_SUGGESTION boundary;
- requirement traceability;
- knowledge/evidence stewardship;
- no automatic APPROVED/CANONICAL promotion.

This exemplar should be broadly reusable across project, policy, legal, grant and investment documents without becoming a universal mega-workflow.

---

# 11. Self-check

Create `reviews/phase-5-foundation-self-check.md` and independently test at least:

1. No Phase 3 Role Card changed.
2. No Phase 4 approved architecture file materially changed.
3. No Workflow grants professional authority.
4. No Workflow owns a human decision.
5. No Workflow defines independent reviewer identity.
6. No Workflow self-promotes APPROVED/CANONICAL.
7. No Workflow widens Role-to-Skill compatibility.
8. Every exemplar has explicit trigger, entry/exit and completion semantics.
9. Every exemplar has exception/rework behavior.
10. Every exemplar preserves artifact ownership boundaries.
11. Project Development Lead does not absorb specialist conclusions.
12. EU grant workflow cannot submit autonomously.
13. Software workflow cannot release to production autonomously.
14. Decision-grade document workflow cannot self-approve.
15. Criticality changes depth, not Role identity.
16. No runtime/model/provider binding.
17. Master Workflow Universe is 30–50 candidates and avoids micro-workflows.
18. Workflow IDs are stable and provider-independent.
19. Workflow participation vocabulary is consistent across template/exemplars.
20. All Phase 5 artifacts remain PROPOSED.

Also list:
- architecture ambiguities;
- likely overlap groups;
- boundaries to defer explicitly to Phase 6 Handoff & Review;
- boundaries to defer explicitly to Phase 7 Decision Rights / Human Approval.

## Commit / Push

If all mandatory checks pass:

Commit exactly:
`docs: add Phase 5 Workflow Registry foundation`

Push to:
`origin architecture/phase-5-workflow-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. FOUNDATION CREATED
Files and summary.

### B. CORE WORKFLOW MODEL
Key architecture decisions.

### C. WORKFLOW UNIVERSE
Families and workflow count.

### D. TEMPLATE / CONSTRAINTS
Key controls.

### E. EXEMPLAR RESULTS
Four exemplar summaries and stress-test findings.

### F. PHASE BOUNDARIES
What is deferred to Phase 6 / 7 / runtime phases.

### G. SELF-CHECK
Checks 1–20 PASS / FAIL.

### H. OPEN ARCHITECTURE QUESTIONS
If none: NONE.

### I. COMMIT / PUSH
Commit SHA and push result.

### J. NEXT-STEP READINESS
Choose exactly one:
- READY FOR INDEPENDENT PHASE 5 FOUNDATION AUDIT
- NOT READY

Do not claim Phase 5 approval.