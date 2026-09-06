# Skill Pack Template

Status: PROPOSED — Phase 4 standard candidate
Template Version: 0.1
Inherits: `standard.skill.common_constraints@0.1`

## Identity
- Pack Name:
- Pack ID: `skill_pack.<id>`
- Type: Skill Pack
- Pack Class: `SPECIALISATION | PROGRAMME | INSTITUTION | TECHNOLOGY | SECTOR | METHOD | OPERATING_CONTEXT | COMPOSITE`
- Contributing Skill Families:
- Included Specialisations: `specialisation.<id>`
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

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.** This section declares only which Roles may activate this Pack at all.

- Compatible Role allowlist: `role.<id>`, `role.<id>`, … or a governed compatibility rule
- Canonical mapping reference: `mapping.<id>` or the mapping registry entry for each Role above

Do **not** write `REQUIRED_CORE`, `REQUIRED_FOR_CONTEXT`, `OPTIONAL`, `ALTERNATIVE` or `PROHIBITED_IN_CONTEXT` here as a role relationship. Listing a Role confers eligibility, never a requirement.

### Typical Use — Advisory, Non-Authoritative
Non-binding note on when this Pack is usually relevant, to help a human author a correct mapping record. States no obligation; the mapping record decides.

## Included Skills
### Required Skills
- `skill.<id>`

### Optional Skills
- `skill.<id>`

### Alternative Skills
- `skill.<id>` or `skill.<id>`

## Pack Dependencies and Layering
- Depends on / layers over: `skill_pack.<id>` — direction and reason
- Depended on by (informational): `skill_pack.<id>`
- Layering metadata: what this Pack adds on top of each dependency, and what it inherits unchanged

Rules:
- **No circular pack dependencies.** If this Pack depends on Pack B, B must not depend directly or transitively on this Pack. A cycle is a validation failure, not a warning: activation order and precedence become undefinable.
- Dependency is transitive for activation, subject to the duplicate-activation rule below.
- Layering never accumulates authority. A stack of Packs confers exactly the authority of the assigned Role Card and nothing beyond it.

Example of correct direction: a CoVE Pack declares that it layers over the applicable Erasmus+ rules Pack where the CoVE action operates under Erasmus+; the Erasmus+ Pack does not declare a dependency on CoVE.

## Precedence With Overlapping Packs
Where another active Pack addresses the same subject with different requirements:
1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** Pack prevails over the more generic — institution over generic method, programme over generic delivery;
3. where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate to the consuming workflow rather than resolving silently;
4. the Role Card and any stricter workflow or assignment control prevail over every Pack.

Precedence never operates in the permissive direction: a Pack may tighten a requirement, never relax one.

## Duplicate Effective Activation
Where a Skill in this Pack is also mapped individually to the same Role, it is activated **once**, under the **stricter** of the two obligations, with this Pack's currency, evidence and controlled-source rules applied on top. The individual mapping is retained only where it has meaning independent of this Pack.

Duplicate effective activation must be detectable at validation time, not discovered during execution.

## Authority Limits of Activation
Activating this Pack **cannot** satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

Those obligations are discharged only through the assigned Role Card, the applicable Review Profile and the applicable Decision Right.

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

Skills in this Pack may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**. Transitions are performed by the owning Role under the applicable review and decision path.

## Review Dependencies
- Review Profile Reference(s): `review.<id>` or none
- Trigger condition:

These are dependencies only; the Pack does not perform independent assurance by identity.

Any evaluation, validation, testing or readiness-checking capability included in this Pack is a **quality-control technique, not independent review**. It does not discharge a `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation and creates no reviewer identity.

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

## Prerequisites and Incompatibilities
- Prerequisite capabilities or Packs: competence statements only; confer no authority.
- Incompatibilities: Packs, contexts or data classifications this must not be combined with, and why.

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