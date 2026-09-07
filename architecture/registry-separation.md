# AI-OS Registry Separation

Status: PROPOSED — Phase 2 architecture refinement

AI-OS separates professional work, control logic, review methodology, reusable specialisations and human authority into distinct architectural objects.

## 1. System Control Profiles

Purpose: coordinate work without becoming substantive professional authors or approvers.

Initial profiles:
- Chief Orchestrator
- Context Manager
- Workflow Controller
- Model Router

Control profiles may select workflows, activate roles, allocate context, coordinate handoffs and escalate issues. They must not independently create authoritative professional conclusions, approve outputs, self-review their own control decisions, or promote AI output to canonical knowledge.

## 2. Role Registry

Purpose: store reusable professional methodologies that can be assumed by different AI runtimes or humans.

Examples:
- Financial Modelling Specialist
- EU Programme Implementation & Grant Management Specialist
- Legal & Regulatory Lead
- Full-Stack Software Engineer
- Data & Database Architect

A role is independent of model, provider and agent instance.

## 3. Skill / Specialisation Registry

Purpose: store reusable capability packs that do not justify first-class role identity.

Examples:
- EIB
- EBRD
- Erasmus+
- CoVE
- LIFE
- Supabase
- PostgreSQL
- Labour Market & Skills Intelligence
- Bid / Proposal Management
- Solar Energy
- BESS
- DSCR / LLCR / PLCR modelling

A named technology, institution, programme, metric or sector is normally a skill/specialisation unless it has a genuinely distinct methodology and authority boundary that justifies a role.

## 4. Review Profile Registry

Purpose: store versioned independent-review methodologies outside the delivery-role definition.

A Review Profile contains at minimum:
- review scope;
- required methodology;
- mandatory checks;
- materiality / severity criteria;
- evidence requirements;
- output schema;
- escalation rules;
- independence constraints.

Examples:
- Independent Financial Model Review
- Independent Technical Review
- IFI / Bankability Review
- Legal / Compliance Review
- ESG / Safeguards Review
- Architecture Review
- Security Review
- Independent Code Review
- Factual / Evidence Review
- Red Team / Challenger Review

Review Profiles preserve Author != Critical Reviewer without duplicating every review function as an ordinary delivery role.

## 5. Workflow Registry

Purpose: define repeatable sequences of roles, review profiles, handoffs, gates and escalation rules for classes of work.

Teams are assembled by workflows; they are not hard-coded into role identities.

## 6. Decision Rights Register

Purpose: define human authority and approval gates.

A decision-right entry maps:
- decision type;
- scope / domain;
- authorised human or responsibility class;
- required confirmation form;
- escalation path;
- whether delegation is permitted.

AI must never impersonate a human approval authority. Decision rights are not AI-assumable professional roles.

## 7. Knowledge / Canonical Governance

Purpose: control the state and promotion of knowledge, evidence, assumptions, decisions and methodology.

AI-generated material does not become canonical automatically. Promotion to APPROVED / CANONICAL requires the applicable governance path.

## 8. Model Registry

Purpose: describe available runtime models and their capabilities, constraints, cost and routing suitability.

Models are replaceable execution runtimes and do not define the roles themselves.

## Relationship

SYSTEM CONTROL
    -> selects WORKFLOW
        -> activates ROLES
            -> binds SKILLS / SPECIALISATIONS
                -> produces structured HANDOFFS
                    -> invokes REVIEW PROFILES
                        -> reaches HUMAN DECISION RIGHTS
                            -> may promote approved material through KNOWLEDGE GOVERNANCE

MODEL REGISTRY provides runtimes to execute eligible AI-assumable roles and control profiles, but does not own professional methodology.