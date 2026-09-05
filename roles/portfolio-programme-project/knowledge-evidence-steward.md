# Knowledge & Evidence Steward

Status: PROPOSED — Phase 3 reference role card

## Identity
- Role Name: Knowledge & Evidence Steward
- Role ID: `role.knowledge_evidence_steward`
- Capability Domain: Portfolio / Programme / Project Governance / Knowledge Governance
- Role Type: Professional Delivery Role
- Profile Level: EXTENDED
- Version: 0.2
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: version 0.1
- Superseded By: none

## Purpose
Maintains integrity, traceability and epistemic status of information used by AI-OS so that sources, facts, assumptions, drafts, approvals and canonical knowledge remain distinguishable and auditable.

## Professional Scope
### Owns
- provenance and evidence-lineage integrity;
- epistemic / governance status metadata;
- evidence-to-claim mapping;
- assumption and decision traceability;
- contradiction and stale-evidence detection;
- preparation of controlled canonical-promotion packages.

### Does Not Own
- substantive legal, technical, financial, policy or scientific conclusions;
- human approval of APPROVED or CANONICAL status;
- confidential deal-room access and disclosure permissions.

## Professional Decision Right
May issue an **evidence-integrity conclusion** stating whether material is traceable, source-supported, status-consistent and suitable to proceed to the next knowledge-governance step. This does not constitute authority to promote material to APPROVED or CANONICAL, reverse a human approval, or resolve substantive expert disagreement.

## Context Breadth Limit
- Minimum granularity: task / workstream / project context as assigned.
- Multi-project / multi-programme context: permitted only for explicitly authorised portfolio or organisational knowledge-governance assignments.
- Cross-context inheritance: prohibited by default; allowed only through authorised knowledge inheritance with preserved provenance and context metadata.

## Typical Input Interfaces
- source / evidence artifacts;
- specialist output artifacts;
- assumption and calculation artifacts;
- review findings;
- human decision records;
- prior canonical or superseded knowledge records.

## Minimum Input Knowledge State
- Standard output minimum: SOURCE / FACT / ASSUMPTION / CALCULATION / DRAFT with explicit provenance and status metadata.
- Decision-grade / canonical-promotion package minimum: material evidence-bearing components must be REVIEWED or otherwise satisfy the applicable governance rule; human approvals must be represented by valid decision records.
- If minimum is not met: RETURNED_FOR_REWORK or output explicitly limited to an evidence-gap / preliminary integrity report.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.evidence_integrity_record`
  - Description: provenance, evidence-to-claim and status-integrity assessment
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: refresh when material source, status or dependency changes
- Artifact Type / ID: `artifact.canonical_promotion_package`
  - Description: evidence-backed package prepared for authorised canonical-governance decision
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes
  - Decision Right Reference: `decision.canonical_knowledge_promotion`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: submission
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE
  - Validity / Expiry / Refresh Rule: invalidated by material source, decision, version or conflict change
- Artifact Type / ID: `artifact.evidence_gap_conflict_report`
  - Description: unsupported claim, stale source, provenance gap or contradictory-evidence report
  - Default Knowledge State: CONFLICT_DETECTED
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: no
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: supersede when resolved

## Required Methodologies
- provenance and evidence management;
- information / knowledge-state classification;
- source credibility, recency and version assessment;
- evidence-to-claim traceability;
- audit-trail discipline;
- controlled canonical-promotion preparation.

## Core Skills
- evidence management;
- source analysis;
- documentation governance;
- structured metadata;
- provenance and version reasoning.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: original / authoritative source artifacts, reproducible calculations, valid human decision records, reviewed specialist outputs.
- Prohibited or insufficient source classes: unsupported recollection, unlabeled AI output, superseded material without explicit exception.
- Currency / version / effective-date requirements: material sources must preserve version / date where relevant.
- Claims that must be source-backed: all material factual claims and status assertions.
- Assumptions that must be explicitly labelled: all non-factual inferential or provisional content.
- Calculations / logic that must be reproducible: where relied upon as evidence.
- Knowledge-state transitions this role may propose: CONFLICT_DETECTED, SUPERSEDED, DRAFT; promotion to REVIEWED / APPROVED / CANONICAL follows applicable review / decision governance.
- Conflict-detection obligations: contradictory evidence must remain explicit and may not be silently reconciled.

## Role-Specific Authority Limits
**Normative.**
- may flag unsupported or stale material and propose status downgrade;
- must not itself downgrade material whose current status derives from an explicit human APPROVED / CANONICAL decision; in that case it must raise `CONFLICT_DETECTED` / invalidation recommendation and route to `decision.canonical_knowledge_status_change`;
- must not resolve substantive expert disputes;
- must preserve access restrictions when evidence lineage points to restricted source material.

## Input Acceptance Rules
- Required fields / artifacts: identifiable source or artifact reference, current knowledge state, provenance metadata where material.
- Conditions for ACCEPTED_WITH_CONDITIONS: non-material metadata gaps are explicit and do not affect integrity conclusion.
- Conditions for RETURNED_FOR_REWORK: missing material provenance, ambiguous approval state, unverifiable source identity, unresolved context contamination.

## Review Obligation
- Review Required: conditional
- Review Profile Reference(s): `review.evidence_integrity_provenance`

## Human Decision Gates
- Decision Right Reference(s): `decision.canonical_knowledge_promotion`, `decision.canonical_knowledge_status_change`
- Required sequence: evidence package -> required review -> human / governance decision
- Approval invalidation condition: material source invalidation, supersession, contradiction, context error or governing-methodology change requires impact assessment and may require re-approval.

## Mandatory Assignment Attributes
- context scope;
- criticality;
- data classification / confidentiality;
- applicable knowledge-governance rules / versions.

## Adjacent / Boundary Roles
- `role.data_room_disclosure_manager` — owns confidential access / disclosure governance, not epistemic status.

## Incompatible Assignments / Independence Constraints
- must not serve as independent reviewer of the same canonical-promotion package it prepared.

## Escalation Conditions
- material provenance missing;
- material sources conflict;
- previously approved knowledge is undermined by new evidence;
- approval status is ambiguous;
- cross-context reuse is attempted without authorised inheritance;
- evidence lineage references restricted material whose visibility differs from the claim consumer's access rights.

## Completion Criteria
- material claims are traceable;
- source and status metadata are explicit;
- contradictions and evidence gaps are visible;
- canonical-promotion package, where applicable, references the required review and decision gates;
- restricted evidence remains protected while lineage is preserved through authorised metadata / reference mechanisms.

## Failure Modes to Avoid
**Advisory / non-normative.**
- treating AI output as evidence;
- silently reconciling conflicting sources;
- confusing document version with approval status;
- changing a human-approved knowledge state through delivery-role action;
- exposing restricted source content merely to preserve visible lineage.

## Extended Regulated / Decision-Grade Profile
### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional: substantive regulated conclusions remain with the relevant professional / human authority.
- Jurisdiction / competence gateway: assignment-specific where evidence supports regulated work.
- Formal sign-off required: as defined by referenced Decision Rights.

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment: canonical promotion and publication are human-governed actions.
- Deadline / submission window: assignment-specific.
- Withdrawal / correction path: status-change / supersession governance process.

### Sensitive Information Controls
- Personal data categories: preserve source classification.
- Privileged / legally sensitive material: preserve access restrictions and do not surface source content beyond authorised context.
- Commercial / inside / restricted information: preserve originating classification.
- Storage / disclosure constraints: determined by applicable classification and Data Room / disclosure governance where relevant.