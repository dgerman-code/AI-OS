# Skill Pack Template

Status: PROPOSED — Phase 4 standard candidate
Template Version: 0.1
Inherits: `standard.skill.common_constraints@0.1`

## Identity
- Pack Name:
- Pack ID: `skill_pack.<id>`
- Pack Class: `SPECIALISATION | PROGRAMME | INSTITUTION | TECHNOLOGY | SECTOR | METHOD | OPERATING_CONTEXT | COMPOSITE`
- Version:
- Status: PROPOSED
- Governance Owner:
- Effective Date:
- Review Date:
- Expiry / Invalidation Trigger:
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes:
- Superseded By:

## Purpose
Define the bounded context this Pack enables and why its components should travel together as a governed, versioned bundle.

## Scope
### Covers
- 

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model/runtime selection;
- any Role scope not already granted by the assigned Role Card.

## Compatible Roles
For each Role, declare the intended relationship:

- `role.<id>` — `REQUIRED_FOR_CONTEXT | OPTIONAL | ALTERNATIVE | PROHIBITED_IN_CONTEXT` — rationale

Use `REQUIRED_CORE` only where the capability is genuinely universal to that Role and therefore should be reconsidered for direct inclusion in the Role Card.

## Included Skills
### Required Skills
- `skill.<id>`

### Optional Skills
- `skill.<id>`

### Alternative Skills
- `skill.<id>` or `skill.<id>`

## Applicability
- Jurisdiction(s):
- Sector(s):
- Programme / framework:
- Institution / financing framework:
- Technology / version:
- Operating context:
- Criticality conditions:
- Assignment prerequisites:

## Controlled Methodology / Source Package
List authoritative or controlled references required to apply the Pack.

For each reference capture, as applicable:
- source / authority;
- title / identifier;
- version;
- effective date;
- expiry / supersession status;
- jurisdiction / programme / technology applicability.

AI-generated content must not be listed as a controlled source.

## Evidence Requirements
- Required evidence classes:
- Minimum source quality:
- Required provenance:
- Currency requirements:
- Assumptions that must remain explicit:
- Reproducibility requirements:

## Knowledge-State Constraints
- Minimum input state for ordinary use:
- Minimum input state for decision-grade use:
- States the Pack may support deriving:
- States the Pack may not promote autonomously:
- Conflict / contradiction escalation rule:

## Review Dependencies
- Review Profile Reference(s): `review.<id>` or none
- Trigger condition:

These are dependencies only; the Pack does not perform independent assurance by identity.

## Decision Dependencies
- Decision Right Reference(s): `decision.<id>` or none
- Trigger condition:

These are dependencies only; the Pack does not acquire human authority.

## External / Regulated Boundary
Where relevant:
- licensed / regulated activity boundary;
- required authorised professional class;
- external submission / filing / publication boundary;
- production / deployment boundary;
- withdrawal / correction path.

## Data / Confidentiality Controls
- personal data categories:
- privileged / legally sensitive information:
- commercial / restricted information:
- storage / residency requirements:
- cross-context reuse restrictions:

## Version and Change Control
A new Pack version is required when a material change occurs in:
- controlled-source basis;
- programme / institutional rules;
- technology major version or platform constraint;
- jurisdiction / regulatory applicability;
- required skill composition;
- compatible Role set;
- evidence requirements;
- review / decision dependencies.

## Activation Criteria
Define the assignment conditions that activate the Pack.

Examples:
- a LIFE call is selected;
- an EIB financing route is pursued;
- PostgreSQL is the governed database technology;
- the project sector is BESS;
- project-finance covenants require DSCR / LLCR / PLCR analysis.

## Deactivation / Invalidation Criteria
Define when the Pack must stop being treated as current or applicable.

## Pack Integrity Rules
- Required Skills must be present when the Pack is activated unless an explicit governed exception exists.
- Optional Skills do not widen Role authority.
- Pack activation must not silently import facts or assumptions from another project / organisation context.
- Controlled references must be current for the assignment date.
- Where Pack requirements conflict with the Role Card or a stricter workflow control, the stricter rule prevails and the conflict is escalated.

## Adjacent Packs
- `skill_pack.<id>` — relationship / overlap boundary

## Completion / Use Criteria
Define what must be true for the Pack to be considered properly applied in a Role assignment.

## Failure Modes to Avoid
Advisory examples:
- using an expired programme guide;
- treating an institution-specific practice as a universal rule;
- using a technology Pack outside its supported version;
- treating Pack activation as professional authority;
- duplicating the same capability into multiple near-identical Packs;
- embedding project-specific facts into a reusable Pack.

## Reclassification Warning
If the Pack begins to own a recurring standalone professional artifact, professional conclusion or authority boundary independent of an assigned Role, stop and reassess whether the capability belongs in the Role Registry instead.