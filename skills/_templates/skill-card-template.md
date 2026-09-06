# Skill Card Template

Status: PROPOSED — Phase 4 standard candidate
Template Version: 0.1
Inherits: `standard.skill.common_constraints@0.1`

## Identity
- Skill Name:
- Skill ID: `skill.<id>` or `specialisation.<id>`
- Type: `SKILL | SPECIALISATION`
- Primary Skill Family:
- Secondary Skill Family Tags: optional; navigation only, never authority or exclusive Role compatibility
- Version:
- Status: PROPOSED
- Governance Owner:
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes:
- Superseded By:

### When Type = SPECIALISATION
- Specialisation Class: `SECTOR | PROGRAMME | INSTITUTION | TECHNOLOGY | JURISDICTION | METRIC | OPERATING_CONTEXT`
- Bounded context — complete the fields that apply:
  - Sector:
  - Programme / call / framework:
  - Institution / funder:
  - Technology / version:
  - Jurisdiction:
  - Metric / methodology:
  - Operating context:
- Applicability boundary: state precisely where this Specialisation applies and, equally, where it stops applying.
- Base capability: the `skill.<id>` this Specialisation bounds, where one exists.

A Specialisation is the **same authority model** as a Skill — it bounds a context, it never adds authority. It is represented here rather than in a separate card type so that a second, competing authority model is not created.

## Purpose
State the reusable capability this Skill provides and why it exists independently of any single Role, project, model or workflow.

## Capability Definition
### Enables
- 

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary
Define what is inside and outside this Skill so that it does not overlap adjacent Skills or hide a Role.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.** This section declares only which Roles may use this capability at all.

- Compatible Role allowlist: `role.<id>`, `role.<id>`, … or a governed compatibility rule
- Canonical mapping reference: `mapping.<id>` or the mapping registry entry for each Role above

Do **not** write `REQUIRED_CORE`, `REQUIRED_FOR_CONTEXT`, `OPTIONAL`, `ALTERNATIVE` or `PROHIBITED_IN_CONTEXT` here as a role relationship. Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

Non-binding description of when this capability is usually relevant, to help a human author a correct mapping record.

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

## Alternative Choice Set
- Choice set reference: the mapping-defined set this capability belongs to, if any
- The **selection condition is defined in the mapping record**, not here.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: what must already be present to apply this competently. Competence statement only; confers no authority.
- Incompatibilities: capabilities, contexts or data classifications this must not be combined with, and why.

## Methods / Techniques
List reusable methods, techniques or analytical operations that constitute the Skill.

## Inputs
List information classes, artifacts or evidence types needed to use the Skill properly.

## Outputs / Contributions
Describe contributions to Role-owned outputs.

- Role-owned artifact this contributes to: `artifact.<id>` owned by `role.<id>`
- What this capability explicitly does **not** produce:

Do not claim first-class professional artifact ownership unless the capability is reclassified as a Role. A capability that cannot name an owning Role and artifact is a candidate hidden Role — stop and reassess.

## Support-Only Boundary
Complete where this capability touches the methodology of a different approved Role.

- Role retaining ownership of the conclusion: `role.<id>`
- What this capability may produce: inputs, analysis, evidence
- What it may never produce: the conclusion owned by that Role

## Independent Review Boundary
If this capability evaluates, validates, tests, checks readiness or otherwise assesses work, state explicitly:

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

## Evidence and Source Requirements
- Preferred source classes:
- Insufficient / prohibited source classes:
- Currency / version requirements:
- Assumptions that must be explicit:
- Reproducibility requirements:

## Knowledge-State Constraints
- Minimum acceptable input state:
- States this Skill may help derive or propose:
- States this Skill may not promote autonomously:
- Conflict-detection obligations:

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**. Transitions are performed by the owning Role under the applicable review and decision path.

## Review / Decision Dependencies
- Review Profile Reference(s): `review.<id>` or none
- Decision Right Reference(s): `decision.<id>` or none
- Trigger condition for review / decision dependency:

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction:
- Sector:
- Programme / framework:
- Technology / version:
- Criticality restrictions:
- Data / confidentiality restrictions:

## Proficiency Guidance
Optional assignment-level guidance using the controlled vocabulary (AWARENESS / WORKING / ADVANCED / EXPERT — no other vocabulary is permitted in Phase 4):
- AWARENESS:
- WORKING:
- ADVANCED:
- EXPERT:

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation.

## Currency / Refresh
- Effective Date:
- Review Date:
- Expiry / invalidation trigger:
- Controlled source / standard references:

## Adjacent Skills / Packs
- `skill.<id>`
- `skill_pack.<id>`

## Completion / Use Criteria
Define what must be true for the Skill to be considered correctly applied within an assignment.

## Failure Modes to Avoid
Advisory examples of misuse, overreach, stale methodology or incorrect evidence treatment.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification.