# Role Card Standard v1.0 Candidate

Status: PROPOSED — Phase 3 standard candidate
Template Version: 1.0

All Professional Delivery Role Cards inherit `standard.role.common_constraints@0.1` unless an approved exception is stated.

Use **Profile Level: CORE** for ordinary professional roles. Use **Profile Level: EXTENDED** when the role handles regulated, high-stakes, irreversible/external-commitment, sensitive-information, production or decision-grade outputs.

## Identity
- Role Name:
- Role ID: `role.<namespace>`
- Capability Domain:
- Role Type: Professional Delivery Role
- Profile Level: CORE / EXTENDED
- Version:
- Status: PROPOSED / APPROVED / DEPRECATED
- Methodology Owner:
- Inherits: `standard.role.common_constraints@0.1`
- Supersedes: optional role version / ID
- Superseded By: optional role version / ID

## Purpose
One concise statement of why this role exists and what professional outcome it owns.

## Professional Scope
### Owns
- 

### Does Not Own
- 

## Professional Decision Right
State the professional conclusion this role may issue within its competence and what that conclusion does **not** constitute.

## Context Breadth Limit
State:
- minimum permitted context granularity;
- whether multi-project / multi-programme context is allowed;
- whether cross-context knowledge inheritance is allowed and under what governance condition.

## Typical Input Interfaces
Describe input **artifact classes / information types**, not named upstream roles.
- 

## Minimum Input Knowledge State
Define the minimum acceptable state for material inputs.
- Standard output minimum:
- Decision-grade output minimum:
- If minimum is not met: RETURNED_FOR_REWORK / preliminary output only / other explicit behaviour

## Output Artifact Interfaces
For each material output specify:
- Artifact Type / ID:
- Description:
- Default Knowledge State:
- Evidence / Source Linkage Required: yes / no
- Independent Review Required: yes / conditional / no
- Decision Right Reference: optional `decision.<id>`
- Reversibility at Creation: REVERSIBLE / COSTLY_TO_REVERSE / IRREVERSIBLE
- Transmitting Act: none / submission / send / publication / deployment / filing / binding commitment / other
- Reversibility after Transmitting Act: REVERSIBLE / COSTLY_TO_REVERSE / IRREVERSIBLE
- Validity / Expiry / Refresh Rule:

Reversibility is evaluated separately for creation of an artifact and for any external act that transmits, deploys, files, publishes or otherwise commits it.

## Required Methodologies
Methodologies are part of role identity and are centrally version-controlled.
- 

## Core Skills
List role-inherent competencies only. Domain / programme / technology skill packs belong to the Skill / Specialisation Registry.
- 

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes:
- Prohibited or insufficient source classes:
- Currency / version / effective-date requirements:
- Claims that must be source-backed:
- Assumptions that must be explicitly labelled:
- Calculations / logic that must be reproducible:
- Knowledge-state transitions this role may propose:
- Conflict-detection obligations:

## Role-Specific Authority Limits
**Normative.** List only limits additional to `standard.role.common_constraints@0.1`.
- 

## Input Acceptance Rules
- Required fields / artifacts:
- Conditions for ACCEPTED_WITH_CONDITIONS:
- Conditions for RETURNED_FOR_REWORK:

## Review Obligation
Reference review methodology only by ID.
- Review Required: yes / conditional / no
- Review Profile Reference(s): `review.<id>`

## Human Decision Gates
Reference human-only decision rights only by ID.
- Decision Right Reference(s): `decision.<id>`
- Required sequence: specialist output -> required review -> human decision, unless explicitly defined otherwise
- Approval invalidation condition:

## Mandatory Assignment Attributes
List only attributes whose absence makes assignment invalid for this role.
- 

## Adjacent / Boundary Roles
Optional. Use role IDs only.
- `role.<id>` — boundary statement

## Incompatible Assignments / Independence Constraints
List only role-specific incompatibilities. Generic author-review separation belongs to Review Profiles and workflow controls.
- 

## Escalation Conditions
- 

## Completion Criteria
- 

## Failure Modes to Avoid
**Advisory / non-normative.** Role-specific professional failure modes only.
- 

## Extended Regulated / Decision-Grade Profile
Required when `Profile Level: EXTENDED`.

### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional:
- Jurisdiction / competence gateway:
- Formal sign-off required:

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment:
- Deadline / submission window:
- Withdrawal / correction path:

### Sensitive Information Controls
- Personal data categories:
- Privileged / legally sensitive material:
- Commercial / inside / restricted information:
- Storage / disclosure constraints:

## Inherited and Not Repeated in Role Cards
The common standard governs:
- universal authority limits;
- universal knowledge-state taxonomy;
- universal handoff interface;
- Review vs Decision separation;
- generic conflict detection;
- generic sensitive-data obligations;
- central change control.
