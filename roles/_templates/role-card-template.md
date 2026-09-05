# Role Card Template

Status: TEMPLATE — Phase 3
Template Version: 0.2

All Professional Delivery Role Cards inherit `standard.role.common_constraints` unless an approved exception is stated.

Use the **Core Profile** for low-risk roles and assignments. Use the **Extended Regulated / Decision-Grade Profile** when the role handles regulated, high-stakes, irreversible, external-submission, production or decision-grade outputs.

## Identity
- Role Name:
- Role ID: `role.<namespace>`
- Capability Domain:
- Role Type: Professional Delivery Role
- Version:
- Status: PROPOSED / APPROVED / DEPRECATED
- Methodology Owner:
- Supersedes: optional role version / ID
- Superseded By: optional role version / ID

## Purpose
One concise statement of why this role exists and what professional outcome it owns.

## Professional Scope
### Owns
- 
- 

### Does Not Own
- 
- 

## Professional Decision Right
State the professional conclusion this role may issue within its competence, and what that conclusion does **not** constitute.

Example distinction: may issue a draft legal analysis for review; may not issue a binding legal opinion, execute a filing or bind a client.

## Typical Input Interfaces
Describe input **types / artifact classes**, not named upstream roles.
- 
- 

## Output Artifact Interfaces
For each material output, specify:
- Artifact Type / ID:
- Description:
- Default Knowledge State: DRAFT / CALCULATION / AI_SUGGESTION / other permitted state
- Evidence / Source Linkage Required: yes / no
- Independent Review Required: yes / no
- Decision Right Reference: optional `decision.<id>`
- Reversibility Class: REVERSIBLE / COSTLY_TO_REVERSE / IRREVERSIBLE
- Validity / Expiry / Refresh Rule: if applicable

## Required Methodologies
Methodologies are part of role identity. They define the professional method the role must apply and are centrally version-controlled.
- 
- 

## Required Skills / Skill Packs
Skills are execution capabilities that may be attached at assignment time without changing role identity.
- Core skills:
- Optional/domain skill packs:

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes:
- Prohibited or insufficient source classes:
- Currency / version requirements:
- Claims that must be source-backed:
- Assumptions that must be explicitly labelled:
- Calculations / logic that must be reproducible:
- Knowledge-state transitions this role may propose:
- Conflict-detection obligations:

## Role-Specific Authority Limits
List only limits that add to `standard.role.common_constraints`.
- 

## Input Acceptance Rules
State what the role must verify before accepting a material handoff.
- Required fields / artifacts:
- Conditions for ACCEPTED_WITH_CONDITIONS:
- Conditions for RETURNED_FOR_REWORK:

## Review Obligation
Do not copy review methodology here.
- Review Required: yes / conditional / no
- Review Profile Reference(s): `review.<id>`
- Workflow / artifact determines trigger: yes

## Human Decision Gates
Do not name the human approver here unless the decision record requires it. Reference Decision Rights Registry IDs.
- Decision Right Reference(s): `decision.<id>`
- Required sequence: specialist output -> required review -> human decision, unless explicitly defined otherwise
- Approval invalidation condition: define whether material input / assumption / version change invalidates prior approval

## Assignment Attributes
Assigned at runtime and not part of role identity:
- seniority
- responsibility level
- criticality
- organisation / programme / project / product / workstream / task scope
- language
- jurisdiction / regulatory perimeter, where applicable
- applicable standards / versions
- data classification / confidentiality
- residency / processing constraints
- model runtime

## Incompatible Assignments / Independence Constraints
List role-specific incompatibilities only. Generic author-review separation belongs to Review Profiles and workflow controls.
- 

## Escalation Conditions
List role-specific triggers in addition to the common inherited standard.
- 

## Completion Criteria
State observable conditions for the role's work to be considered complete.
- 
- 

## Failure Modes to Avoid
Role-specific professional failure modes only.
- 
- 

## Extended Regulated / Decision-Grade Profile
Complete this block when applicable.

### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional:
- Jurisdiction / competence gateway:
- Formal sign-off required:

### External Standards / Controlled Sources
- Standard / law / programme / donor / technical framework:
- Version / effective date required:
- Official source class required:

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment:
- Deadline / submission window:
- Withdrawal / correction path:

### Sensitive Information Controls
- Personal data categories:
- Privileged / legally sensitive material:
- Commercial / inside / restricted information:
- Storage / disclosure constraints:

## Change Control
Changes to purpose, professional decision right, required methodology, regulated-activity boundary or review obligation require explicit Role Registry review and versioning.

When a new version supersedes an old one, the workflow must define whether in-flight assignments continue under the old version or must be revalidated against the new version.