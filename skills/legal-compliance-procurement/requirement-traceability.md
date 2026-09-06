# Requirement Traceability

Status: PROPOSED — Phase 4 exemplar Skill Card

## Identity
- Skill Name: Requirement Traceability
- Skill ID: `skill.requirement_traceability`
- Type: `SKILL`
- Primary Skill Family: Legal / Compliance / Procurement
- Secondary Skill Family Tags: Product / UX / Content; Data / Analytics / AI; Software / Integration / Platform / Security
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose
Maintain a defensible chain from each requirement or obligation back to the source that imposes it and forward to the artifact, decision or test that discharges it — so that at any point it can be shown which obligations are met, which are open, and what breaks if a source changes.

It sits in Legal / Compliance / Procurement as its primary family because the hardest version of the problem is regulatory: an obligation whose origin cannot be named cannot be defended. The same structure serves product requirements and data architecture, which is why it carries secondary family tags rather than being duplicated per domain.

## Capability Definition
### Enables
- forward tracing from source or obligation to requirement, design, artifact and verification;
- backward tracing from an artifact or test to the obligation it discharges;
- coverage analysis: which obligations have no discharging artifact;
- orphan detection: which requirements have no originating source;
- impact analysis when a source is superseded or a requirement changes;
- traceability structure design proportionate to criticality;
- explicit recording of the discharge status of each obligation.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary

Inside: the linkage structure and its completeness.

Outside:
- **whether a requirement is correct, adequate or well-formed.** Requirement quality is owned by the Role that owns the requirement — `role.product_manager_business_analyst` for product requirements, under `review.product_requirements_quality`.
- **whether an obligation has actually been met.** Tracing shows a link exists; it does not verify that the linked artifact discharges the obligation in substance. That judgement belongs to the owning Role and, where required, to independent review.
- **approving requirements or scope.** Approval is a human decision right — `decision.product_scope_approval` for product scope, `decision.contract_commitment` and related rights on the legal side.
- **compliance conclusions.** A complete traceability matrix is not a statement of compliance; that conclusion is owned by `role.legal_regulatory_lead` or the applicable specialist Role.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.eu_grants_programmes_specialist`, `role.legal_regulatory_lead`, `role.solution_architect`, `role.data_database_architect`, `role.sales_business_development_specialist`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, sections 3, 6, 8 and 9

`role.sales_business_development_specialist` is present for **transitive Pack compatibility**, not because a mapping record maps this Skill to it directly. `skill_pack.bid_proposal_management` is mapped to that Role and requires this Skill — the compliance matrix in a competitive bid is a traceability structure — so rejecting the Role here would make a valid Pack activation fail. Eligibility only: relationship and trigger come from the mapping record for the Pack.

`role.product_manager_business_analyst` is a natural candidate and its Role Card supports the capability, but the current Wave 1 mapping does not map it. It is therefore **not** listed here: the allowlist is built from approved Role Cards and existing mapping records, not from what seems reasonable. Adding it is a Wave 2 mapping decision.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant where obligations come from an external rulebook that will be audited against, where a solution must show that quality or security constraints came from somewhere, or where a superseded source must be traced to everything it affects.

## Alternative Choice Set
- Choice set reference: none.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: `skill.obligation_mapping` or `skill.regulatory_mapping` where obligations must first be extracted from source material. Competence statement only; confers no authority.
- Incompatibilities: none. It must not be presented as evidence of compliance or as independent review.

## Methods / Techniques
- obligation and requirement decomposition to a traceable unit;
- bidirectional link construction between source, requirement, artifact and verification;
- coverage and orphan analysis;
- impact analysis on supersession or amendment;
- matrix granularity design proportionate to criticality;
- discharge-status recording with explicit UNKNOWN where unresolved.

## Inputs
- verified source material and its currency status;
- the obligation or requirement set;
- the artifacts, designs, decisions and tests intended to discharge them;
- the applicable criticality band, which sets required granularity.

## Outputs / Contributions

Method-level contribution. The traceability structure is embedded in, or attached to, a Role-owned artifact.

- Role-owned artifacts this contributes to:
  - `artifact.eu_application_package` owned by `role.eu_grants_programmes_specialist`;
  - `artifact.legal_analysis` owned by `role.legal_regulatory_lead`;
  - `artifact.solution_architecture_specification` owned by `role.solution_architect`;
  - `artifact.data_architecture_specification` owned by `role.data_database_architect`.
- What this capability explicitly does **not** produce: a compliance conclusion, a requirement-quality judgement, a scope approval, or a statement that an obligation is satisfied in substance.

## Support-Only Boundary
- Role retaining ownership of the conclusion: `role.legal_regulatory_lead` for whether obligations are met as a matter of law; the requirement-owning Role for whether requirements are adequate.
- What this capability may produce: linkage, coverage figures, gaps, orphans, impact sets.
- What it may never produce: the compliance conclusion or the adequacy judgement.

## Independent Review Boundary

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

A complete matrix authored by the same person who wrote the requirements is a self-check. Independent review is performed under the applicable `review.<id>` by someone who did not author the work.

## Evidence and Source Requirements
- Preferred source classes: verified authoritative instruments; executed contracts; approved requirement baselines; programme rulebooks at a stated version.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source.** An AI-proposed link is a candidate for human confirmation, never a traced link.
- Currency / version requirements: every traced source carries its version and effective date, so that supersession triggers impact analysis rather than silent staleness.
- Assumptions that must be explicit: any inferred link not stated by the source.
- Reproducibility requirements: each link must name its basis.

## Knowledge-State Constraints
- Minimum acceptable input state: obligations traced for decision-grade use must derive from SOURCE or FACT material; DRAFT obligations may be traced but the resulting coverage is preliminary and must be labelled so.
- States this Skill may help derive or propose: CALCULATION for coverage figures; CONFLICT_DETECTED where two sources impose incompatible obligations; UNKNOWN for undischarged obligations.
- States this Skill may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict-detection obligations: incompatible obligations from different authoritative sources are raised as `CONFLICT_DETECTED`; a gap is never closed by relaxing the requirement to match the artifact.

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Skill level; resolved by the consuming Role and workflow.
- Decision Right Reference(s): none at Skill level; resolved by the consuming Role and workflow.
- Trigger condition for review / decision dependency: set by the consuming Role Card.

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction: unrestricted.
- Sector: unrestricted.
- Programme / framework: unrestricted; programme Packs may impose their own matrix format.
- Technology / version: not applicable.
- Criticality restrictions: at Enhanced Decision-Grade and above, granularity must be sufficient to show per-obligation discharge status, not category-level coverage.
- Data / confidentiality restrictions: a matrix may aggregate restricted material and inherits the strictest classification of anything it links.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: understands that requirements should be traceable to a source.
- WORKING: maintains a matrix against a given obligation set and reports coverage.
- ADVANCED: designs granularity for criticality, runs impact analysis on supersession, detects orphans and incompatible obligations.
- EXPERT: designs traceability regimes spanning multiple rulebooks and reconciles conflicting obligation sets for escalation.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation.

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: none intrinsic; the traced sources carry currency, not the technique.
- Controlled source / standard references: none embedded.

## Adjacent Skills / Packs
- `skill.obligation_mapping` — extracts obligations that this Skill then traces.
- `skill.regulatory_mapping` — establishes the regulatory perimeter.
- `skill.traceability_matrix_design` — designs the matrix instrument; this Skill maintains and analyses the linkage.
- `skill.source_verification` — establishes that traced sources are current.

## Completion / Use Criteria
Correctly applied when every material obligation has a named source and a discharge status, orphans and gaps are visible rather than implied, supersession triggers impact analysis, and unresolved items are UNKNOWN rather than absent.

## Failure Modes to Avoid
- Presenting a complete matrix as a compliance conclusion.
- Tracing to a document that exists rather than to the part that discharges the obligation.
- Letting granularity collapse to category level so that coverage looks complete.
- Closing a gap by rewriting the requirement.
- Leaving superseded sources traced without impact analysis.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification.
