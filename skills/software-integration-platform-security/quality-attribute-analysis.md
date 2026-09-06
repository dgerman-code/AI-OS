# Quality Attribute Analysis

Status: PROPOSED — Phase 4 exemplar Skill Card

## Identity
- Skill Name: Quality Attribute Analysis
- Skill ID: `skill.quality_attribute_analysis`
- Type: `SKILL`
- Primary Skill Family: Software / Integration / Platform / Security
- Secondary Skill Family Tags: Strategy & Analysis
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: `skill.security_constraint_allocation` (retired; security constraint allocation is this Skill with the security dimension selected, supplemented by `skill.requirement_traceability`)
- Superseded By: none

## Purpose
Turn non-functional expectations into stated, attributable, testable quality requirements and allocate them across a solution structure — so that "it must be secure and fast" becomes specific constraints with sources, thresholds and owners.

This Skill absorbed the retired `skill.security_constraint_allocation`, and that history is the reason its boundary is drawn as tightly as it is below. A capability that allocates security constraints sits one careless sentence away from reading as architecture-owned security authority.

## Capability Definition
### Enables
- elicitation of quality expectations and their conversion into stated attributes;
- selection of the relevant dimensions for the solution at hand;
- threshold and measurement definition so an attribute is testable rather than aspirational;
- allocation of attributes across components, boundaries and interfaces;
- trade-off analysis where attributes conflict, with the conflict made explicit rather than averaged away;
- identification of which attributes require a specialist Role's ownership.

### Selectable dimensions
Include, and are not limited to:
- **security** — confidentiality, integrity, authentication, authorisation, auditability;
- **privacy** — data minimisation, purpose limitation, retention, residency;
- **resilience** — fault tolerance, degradation behaviour, recovery objectives;
- **performance** — latency, throughput, resource envelope;
- **availability** — uptime, maintenance windows, failover behaviour.

Selecting a dimension scopes the analysis. **It transfers no ownership whatsoever** — see the boundary below.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary

Inside: what the quality requirements are, where they come from, how they are measured, and which part of the solution carries each one.

Outside, and this is the load-bearing part of this card:

- **Security ownership remains with `role.security_engineer`.** Selecting the security dimension lets this Skill state that a boundary requires authentication and allocate that constraint. It does **not** produce the threat model, the control design, the control-adequacy conclusion, or accreditation. Those are owned by `role.security_engineer` through `skill.threat_modelling`, `skill.security_control_design` and `skill.security_control_validation`, reviewed under `review.security`, and gated by `decision.security_accreditation` and `decision.security_risk_acceptance`.
- **Personal-data ownership remains with `role.data_protection_gdpr_specialist`.** Selecting the privacy dimension lets this Skill allocate a retention or residency constraint. It does **not** produce the DPIA, the lawful-basis determination, or any conclusion on the adequacy of a transfer. Those are owned through `skill.privacy_impact_analysis` and `skill.lawful_basis_analysis` and gated by `decision.dpia_acceptance` and `decision.lawful_basis_adoption`.
- **Not verification.** Stating a threshold is not evidence it is met. Demonstrating that is testing and validation, owned elsewhere.
- **Not architecture approval.** Adoption of the architecture carrying these attributes is gated by `decision.architecture_adoption`.

An analysis that concludes "the system is secure" has left this Skill's boundary. The correct output is "these constraints apply, allocated here, from these sources, and security ownership sits with the Security Engineer."

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.solution_architect`, `role.data_database_architect`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, section 8

`role.data_database_architect` is present for **transitive Pack compatibility**, not because a mapping record maps this Skill to it directly. `skill_pack.supabase` is mapped to that Role and requires this Skill, because the platform's authorisation model is expressed in the data model and its constraints bound achievable quality attributes. Rejecting the Role here would make a valid Pack activation fail. Eligibility only: relationship and trigger come from the mapping record for the Pack.

`role.security_engineer` and `role.data_protection_gdpr_specialist` remain **not** listed, and this addition does not change that: they own the specialist conclusions this Skill defers to, and they exercise them through their own capabilities, not through this one. Widening the allowlist for Pack compatibility widens nothing else — the Data & Database Architect gains eligibility to use the technique, not any security or data-protection conclusion. Other engineering Roles are Wave 2 mapping decisions.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant when a solution structure is being defined and non-functional expectations exist but are unstated, unattributed or untestable.

## Alternative Choice Set
- Choice set reference: none.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: `skill.solution_decomposition`, since attributes are allocated across a structure that must already exist. `skill.requirement_traceability` where attributes must be traced to their originating obligation. Competence statements only; confer no authority.
- Incompatibilities: must not be combined with, or presented as, specialist security or data-protection ownership. Where a regulated data category or an accreditation requirement is in scope, the specialist Role is engaged rather than substituted.

## Methods / Techniques
- quality attribute elicitation and scenario formulation;
- dimension selection and scoping;
- threshold, metric and measurement-method definition;
- allocation across components, trust boundaries and interfaces;
- trade-off and tension analysis with explicit resolution or escalation;
- specialist-ownership identification and hand-off framing.

## Inputs
- functional scope and solution decomposition;
- obligations and constraints from verified sources, including regulatory and contractual;
- operating context: load profile, data classification, residency, availability expectations;
- criticality band;
- specialist inputs where a dimension is specialist-owned.

## Outputs / Contributions

Method-level contribution. This Skill contributes structured quality requirements and their allocation into Role-owned architecture artifacts; it owns none of them.

- Role-owned artifacts this contributes to:
  - `artifact.solution_architecture_specification` owned by `role.solution_architect`;
  - `artifact.architecture_decision_record` owned by `role.solution_architect`.
- What this capability explicitly does **not** produce: a threat model, a security control design or adequacy conclusion, a DPIA, a lawful-basis determination, a test result, or an architecture adoption decision.

## Support-Only Boundary
- Roles retaining ownership of the conclusion: `role.security_engineer` for every security conclusion; `role.data_protection_gdpr_specialist` for every personal-data conclusion.
- What this capability may produce: stated attributes, thresholds, allocations, trade-off analysis, and the identification that a specialist conclusion is required.
- What it may never produce: the security conclusion or the data-protection conclusion, in any form, including by implication from a completed allocation.

## Independent Review Boundary

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

Analysing quality attributes does not discharge `review.architecture` or `review.security`; both are performed under their own profiles by someone who did not author the work.

## Evidence and Source Requirements
- Preferred source classes: contractual service commitments; regulatory obligations from verified instruments; measured operating data; documented platform constraints from authoritative vendor documentation; specialist Role outputs.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source.** Also insufficient: unmeasured performance folklore, vendor marketing claims, and thresholds carried over from an unrelated system without restatement.
- Currency / version requirements: platform-derived constraints carry the platform version they were established against.
- Assumptions that must be explicit: every threshold not derived from an obligation or measurement is an ASSUMPTION and labelled as one.
- Reproducibility requirements: each attribute names its source and its measurement method.

## Knowledge-State Constraints
- Minimum acceptable input state: obligations and specialist inputs relied on for a decision-grade allocation must be REVIEWED or APPROVED; measured data must be FACT.
- States this Skill may help derive or propose: ASSUMPTION for unevidenced thresholds; CALCULATION for derived envelopes; CONFLICT_DETECTED where attributes are mutually unsatisfiable or where an obligation conflicts with a platform constraint.
- States this Skill may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict-detection obligations: an irreconcilable tension between attributes, or between an attribute and a regulatory obligation, is raised as `CONFLICT_DETECTED` and escalated. It is never resolved by silently relaxing the stricter attribute.

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Skill level; resolved by the consuming Role and workflow. The consuming Solution Architect assignment carries `review.architecture` and `review.security`.
- Decision Right Reference(s): none at Skill level; resolved by the consuming Role and workflow.
- Trigger condition for review / decision dependency: set by the consuming Role Card.

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction: unrestricted; jurisdiction selects applicable privacy and regulatory constraints.
- Sector: unrestricted.
- Programme / framework: unrestricted.
- Technology / version: unrestricted; technology Packs supply platform constraints.
- Criticality restrictions: at Enhanced Decision-Grade and above, security and privacy dimensions may not be closed without the specialist Role engaged.
- Data / confidentiality restrictions: analysis inherits the classification of the data it reasons about.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: distinguishes functional from quality requirements.
- WORKING: states attributes with thresholds and allocates them across a given decomposition.
- ADVANCED: designs measurement methods, resolves trade-offs explicitly, identifies where specialist ownership is required.
- EXPERT: structures quality attribute regimes across a portfolio and adjudicates cross-cutting tensions for escalation.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation. Depth in the security dimension never substitutes for `role.security_engineer`.

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: none intrinsic; platform-derived constraints expire with their platform Pack.
- Controlled source / standard references: none embedded.

## Adjacent Skills / Packs
- `skill.solution_decomposition` — supplies the structure attributes are allocated across.
- `skill.requirement_traceability` — traces attributes to originating obligations.
- `skill.threat_modelling`, `skill.security_control_design` — Security Engineer capabilities this Skill defers to.
- `skill.privacy_impact_analysis`, `skill.lawful_basis_analysis` — Data Protection capabilities this Skill defers to.
- `skill_pack.supabase` — supplies platform constraints that bound achievable attributes.

## Completion / Use Criteria
Correctly applied when each material attribute is stated, attributed to a source, given a measurable threshold and allocated to a component; trade-offs are explicit; and every dimension requiring specialist ownership is flagged rather than closed.

## Failure Modes to Avoid
- Concluding a system is secure or compliant from a completed allocation.
- Carrying thresholds from another system without restating their basis.
- Averaging away a genuine trade-off instead of escalating it.
- Treating a platform default as an obligation.
- Allowing depth in the security dimension to read as security ownership.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification.
