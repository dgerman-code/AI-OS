# Communication Specialist — Governed Registry Package Foundation

Status: PROPOSED
Branch: `proposal/communication-difficult-conversations-specialist`

## Purpose

Convert the existing proposal `proposals/communication-difficult-conversations-specialist-production-spec.md` into a governance-safe AI-OS registry package without altering any approved Phase 1–13 artifact and without claiming Phase 14 approval or production readiness.

This is a proposal/package-generation task, not runtime implementation.

## Architectural constraints

Preserve these invariants:

- ROLE != AGENT INSTANCE
- MODEL != ROLE
- ROUTER != ORCHESTRATOR
- REVIEW PROFILE != REVIEW INSTANCE
- DECISION RIGHT != DECISION RECORD
- KNOWLEDGE != CANONICAL RECORD
- CREDENTIAL != HUMAN AUTHORITY
- external send/publication authority is always human-only where an applicable approved Decision Right requires it
- missing authority fails closed
- no celebrity impersonation or endorsement claim

The canonical capability name is:

**Difficult Conversations & Communication Strategy Specialist**

Canonical Role candidate ID:

`role.communication_difficult_conversations_specialist`

Compatibility / research alias only:

`jefferson-fisher-communication`

Canonical methodology candidate:

`method.communication.calm_direct_control@0.1`

Canonical skill pack candidate:

`pack.communication.difficult_conversations@0.1`

Recommended product-facing mode:

**Calm Direct Mode**

Compatibility alias only:

**Fisher Mode**

Recommended filter name:

**Communication Control Filter**

Optional attribution wording:

> Communication methodology informed by publicly available principles associated with Jefferson Fisher’s work on difficult conversations, boundaries, clarity, assertiveness, emotional self-control, and conversational leadership.

Add the disclaimer where attribution is shown:

> Not affiliated with or endorsed by Jefferson Fisher.

Do not copy proprietary books, paid courses, transcripts, or protected frameworks.

## Required package

Create a self-contained proposal package under:

`proposals/communication-difficult-conversations-specialist/`

with the following artifacts, all `Status: PROPOSED`:

1. `README.md` — package map, provenance, non-goals, governance boundary.
2. `role-card.md` — Role Card candidate following the current AI-OS Role Card Standard.
3. `methodology-card.md` — Calm Direct Control methodology, principles, anti-goals, safety/limits.
4. `skill-pack.md` — skills/specialisations required by the role; map to existing approved skills where possible and clearly mark only truly missing skills as candidates.
5. `workflow-difficult-interaction-response.md` — primary workflow candidate.
6. `workflow-meeting-preparation.md`.
7. `workflow-boundary-setting.md`.
8. `workflow-refusal.md`.
9. `workflow-formal-escalation.md`.
10. `workflow-thread-diagnostics.md`.
11. `review-profile-communication-strategy.md`.
12. `review-profile-high-stakes-external-communication.md`.
13. `trigger-routing-spec.md` — activation scoring and co-activation rules.
14. `communication-control-filter.md` — the ten-factor filter and scoring semantics.
15. `conversation-diagnostics-contract.md` — structured diagnostic I/O.
16. `runtime-prompt-assembly.md` — how approved role/methodology/workflow/scope/task context would assemble a runtime prompt; do not create a permanent autonomous agent.
17. `decision-right-gap-analysis.md` — map existing applicable rights, especially `decision.external_publication`; if a private high-stakes external-send Right does not exist, keep candidate `decision.external_high_stakes_communication_send` explicitly PROPOSED and blocked pending Phase 7 change control.
18. `evaluation-spec.md` — evaluation suite, adversarial tests, high-stakes cases, co-specialist cases, silence/non-response cases.
19. `examples.md` — representative examples only; do not duplicate proprietary phrasing.
20. `self-check.md` — completeness, provenance, authority, routing, safety, and no-scope-creep checks.

## Role ownership boundary

The Role owns:

- communication strategy;
- conversational framing;
- tone;
- brevity;
- boundary formulation;
- response/non-response recommendation;
- issue triage;
- de-escalation;
- conversational redirection;
- difficult-message drafting;
- meeting preparation;
- escalation/documentation recommendation.

It does NOT own:

- legal conclusions;
- financial conclusions;
- compliance conclusions;
- technical truth;
- institutional-position adoption;
- contractual interpretation;
- risk acceptance;
- publication/send authority;
- canonicalisation of disputed facts;
- psychological diagnosis.

When those domains are material, require co-activation of the relevant approved specialist role and do not allow this communication role to override the substantive conclusion.

## Trigger model

Use a 0–100 Communication Conflict Score.

- `<35`: no activation unless explicitly requested.
- `35–54`: optional supporting role.
- `55–74`: activate.
- `75–100`: primary communication role, while substantive domain ownership remains with the relevant role.

The trigger model must consider, at minimum:

conflict, hostility, accusation, refusal, boundary, negotiation tension, stakeholder confrontation, pressure, ultimatum, public criticism, repeated confusion, possible deflection, escalation risk, relationship risk, high-stakes email, request to make wording stronger/firm/professional without escalation.

Do not treat psychological motive inference as a trigger fact.

## Multi-role coordination

Use co-activation, not agent proliferation.

Examples:

- conflict + legal issue → communication role + Legal & Regulatory Lead;
- conflict + public/institutional communication → communication role + Institutional Communications / Editorial Specialist;
- conflict + grant/donor issue → communication role + applicable programme/grant role;
- conflict + PPP/transaction issue → communication role + PPP / Concession Specialist or Project Finance / Transaction Specialist;
- high-stakes executive correspondence → communication role + relevant substantive owner + high-stakes communication review.

The communication role may change phrasing and strategy but must not change substantive conclusions without the owning role’s updated conclusion.

## High-stakes rule

Before drafting, evaluate whether the correct action is:

- respond now;
- delay;
- do not respond;
- document only;
- move channel;
- obtain substantive specialist review;
- obtain independent communication review;
- escalate;
- request human approval before transmission.

For high/critical stakes, require explicit review and human send/publication gate where applicable.

## Communication diagnostics

Support at least:

- objective;
- user position;
- other-party position;
- actual disagreement;
- facts;
- assumptions;
- emotional triggers;
- power/decision context;
- boundary issues;
- possible deflection;
- possible strategic confusion;
- unnecessary arguments;
- respond / clarify / redirect / ignore / document / escalate classification;
- escalation risk;
- relationship risk;
- documentation risk;
- recommended channel;
- recommended timing;
- recommended next move;
- recommended response.

Use cautious language for inferred motives: `possible`, `appears to`, `may indicate`, `potential risk`.

No diagnosis such as narcissism, gaslighting, lying, manipulation, etc. without evidence; prefer observable communication-behaviour descriptions.

## Communication Control Filter

The filter must evaluate:

1. GOAL
2. EMOTION
3. CLARITY
4. BREVITY
5. BOUNDARY
6. DEFENSIVENESS
7. CONTROL
8. RELEVANCE
9. ESCALATION
10. NEXT STEP

Scores may be 0–100 but are advisory only and confer no authority.

## Evaluation requirements

Create tests for at least:

- angry email;
- passive-aggressive message;
- refusal;
- boundary setting;
- hostile stakeholder;
- board disagreement;
- partner delay;
- false accusation;
- irrelevant accusation;
- repeated confusion;
- negotiation pressure;
- ultimatum;
- donor disagreement;
- executive disagreement;
- relationship-preserving refusal;
- final warning;
- formal escalation;
- legal-sensitive correspondence;
- request requiring another specialist;
- case where silence is better than response;
- case where communication role must defer to Legal;
- case where publication/send authority is missing and must block;
- case where a substantive expert conclusion conflicts with the user’s preferred wording;
- case where a hostile message contains a fact that materially changes the user’s position;
- case where emotional de-escalation must not weaken a formal legal position.

Evaluate clarity, brevity, respect, boundary quality, strategic focus, escalation risk, factual discipline, emotional control, directness, optionality, domain deference, and authority compliance.

## Deliverable quality

The package must be detailed enough that a separate engineering team can later implement it without inventing role ownership, trigger semantics, review requirements, authority boundaries, or prompt behavior.

Do not implement runtime code now.
Do not add a real provider/model integration.
Do not alter approved 59-role registry artifacts.
Do not create or silently approve a new Decision Right.
Do not create a PR.

At the end, return:

A. Package summary
B. Architecture decisions
C. Role boundary
D. Skills/methodology
E. Workflow package
F. Trigger/routing model
G. Review/authority model
H. Evaluation package
I. Files created
J. Open governance gaps
K. Validator/self-check status
L. Readiness verdict

Final readiness wording if complete:

`READY FOR INDEPENDENT COMMUNICATION SPECIALIST PACKAGE REVIEW`
