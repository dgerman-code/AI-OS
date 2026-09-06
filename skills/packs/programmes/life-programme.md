# LIFE Programme Pack

Status: PROPOSED — Phase 4 exemplar Skill Pack Card

## Identity
- Pack Name: LIFE Programme
- Pack ID: `skill_pack.life_programme`
- Type: Skill Pack
- Pack Class: `PROGRAMME`
- Contributing Skill Families: Research & Evidence; Project / Programme Delivery; Legal / Compliance / Procurement; Finance & Economics; Documentation / Knowledge / Disclosure
- Included Specialisations: `specialisation.eu_grant_delivery`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Effective Date: bound at instantiation to the applicable call and guidance version; not fixed by this card
- Review Date: on each call publication or guidance revision, whichever is earlier
- Expiry / Invalidation Trigger: see Deactivation / Invalidation Criteria
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose
Carry the programme-specific rule interpretation, application logic and submission constraints that a LIFE assignment requires, as one governed and versioned bundle whose currency can be resolved — rather than as loose capabilities that each go stale independently.

**This card defines architecture and controlled-source requirements only. It deliberately contains no current LIFE call content, deadline, budget rate, annex list or portal behaviour.** Those are instance data, bound at activation from authoritative sources, and any figure written into this card would be wrong by the next call.

## Scope
### Covers
Four capabilities that are **pack-internal controlled components, not standalone Skill IDs**. They are meaningless outside a specific programme rulebook at a specific version, and they inherit this Pack's currency rules:

1. **Eligibility analysis** — applicant, partner, activity, cost and geographic eligibility against the call and the programme regulation at their bound versions. Produces an eligibility position with explicit UNKNOWN where rules do not resolve; never an eligibility determination binding on the granting authority.
2. **Work-package logic** — decomposition into work packages, deliverables, milestones and effort consistent with the call's required structure and intervention logic.
3. **Programme budget logic** — budget construction against the applicable cost categories, rates, ceilings and co-financing structure at their bound version.
4. **Submission requirement mapping** — the complete set of required forms, annexes, declarations, formats, limits and sequencing for the specific call, traced so that completeness is demonstrable.

None may be re-created as a `skill.<id>`. They were removed as standalone Skills in the Wave 1 remediation precisely because they cannot be applied without a bound rulebook version.

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model/runtime selection;
- any Role scope not already granted by the assigned Role Card.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.eu_grants_programmes_specialist`, `role.eu_programme_implementation_grant_management_specialist`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, section 3
- Canonical mapping reference (Wave 2): `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

### Wave 2 allowlist basis

`role.eu_programme_implementation_grant_management_specialist` is admitted because its Role Card owns grant agreement obligation mapping, donor-rule compliance interpretation for implementation decisions, and amendment preparation — all of which require the programme rulebook this Pack carries, at a bound version. It consumes the Pack post-award; `role.eu_grants_programmes_specialist` consumes it pre-award. Neither gains submission authority: `decision.granting_authority_submission` remains a human decision right on both Role Cards. Eligibility only; relationship and trigger come from the Wave 2 mapping record.

`role.eu_programme_implementation_grant_management_specialist`, `role.grant_financial_compliance_budget_specialist` and `role.consortium_partner_coordination_specialist` all plausibly touch LIFE work, but none is mapped to this Pack in the current record, so none is listed. Extending the allowlist is a Wave 2 mapping decision.

Listing a Role confers eligibility, never a requirement.

### Typical Use — Advisory, Non-Authoritative
Non-binding: usually relevant when the programme is LIFE and a specific call has been selected. States no obligation; the mapping record decides.

## Included Skills
### Required Skills
- `skill.source_verification` — the call guide and programme regulation must be verified and version-anchored before any pack-internal capability is applied.
- `skill.requirement_traceability` — submission requirements are traced to their source and to the artifact discharging each.
- `skill.source_monitoring` — the bound guidance set is monitored for revision during the application window.

### Optional Skills
- `skill.partner_mapping`
- `skill.deliverable_planning`
- `skill.milestone_management`
- `skill.grant_cost_eligibility_analysis`
- `skill.document_structuring`

### Alternative Skills
None.

## Pack Dependencies and Layering
- Depends on / layers over: none. LIFE is a standalone programme framework and does not layer over another programme Pack.
- Depended on by (informational): none currently.
- Layering metadata: not applicable.

No circular dependency is possible for this Pack, since it declares none.

## Precedence With Overlapping Packs
Where another active Pack addresses the same subject with different requirements:
1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** Pack prevails — this programme Pack prevails over a generic delivery or method Pack on programme rules;
3. where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate rather than resolving silently;
4. the Role Card and any stricter workflow or assignment control prevail over this Pack.

Precedence never operates in the permissive direction.

Concretely: where `skill_pack.bid_proposal_management` supplies a generic compliance-matrix or submission-readiness practice and this Pack imposes a call-specific requirement, this Pack prevails on the programme requirement and the composite Pack supplies only process scaffolding around it.

## Duplicate Effective Activation
`skill.source_verification`, `skill.requirement_traceability` and `skill.source_monitoring` are all individually mapped to `role.eu_grants_programmes_specialist` or to other Roles, and are also required Skills here.

Where a Skill in this Pack is also mapped individually to the same Role, it is activated **once**, under the **stricter** of the two obligations, with this Pack's currency, evidence and controlled-source rules applied on top. The individual mapping is retained only where it has meaning independent of this Pack — which it does for all three, since each is reused outside LIFE.

Duplicate effective activation must be detectable at validation time, not discovered during execution.

## Authority Limits of Activation
Activating this Pack **cannot** satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

Those obligations are discharged only through the assigned Role Card, the applicable Review Profile and the applicable Decision Right. In particular, activation grants no authority to submit an application, commit a partner or approve a budget: those are `decision.granting_authority_submission`, `decision.partner_commitment` and `decision.budget_approval`, held by humans.

## Applicability
- Jurisdiction(s): EU and participating countries as defined by the bound programme rules.
- Sector(s): as scoped by the applicable LIFE sub-programme.
- Programme / framework: LIFE, at the bound programme regulation and call-guide version.
- Institution / financing framework: the managing authority / executive agency named in the bound call.
- Technology / version: not applicable.
- Operating context: application preparation and submission.
- Criticality conditions: none intrinsic; criticality raises evidence and review depth in the consuming Role.
- Assignment prerequisites: a specific call must be identified and its guidance version bound. Without a bound call, the pack-internal capabilities have no rulebook and the Pack must not be treated as active.

## Controlled Methodology / Source Package
Required at instantiation, each captured with source / authority, title / identifier, version, effective date, expiry or supersession status, and applicability:
- the LIFE programme regulation in force for the call;
- the multiannual work programme applicable to the call;
- the call document and its call-specific guide;
- the applicable general model grant agreement and its annotations;
- application form and annex templates at their call-specific versions;
- submission portal rules, formats and limits as published by the managing authority;
- any call-specific FAQ or corrigendum issued during the window.

**AI-generated content must not be listed as a controlled source.** Nor may a secondary summary, consultant guide or prior-round document stand in for the current call text.

## Evidence Requirements
- Required evidence classes: official programme and call documentation; applicant and partner legal and financial documentation; substantiation for every eligibility and capacity claim.
- Minimum source quality: authoritative publication channel of the managing authority; prior-round or third-party restatements are insufficient.
- Required provenance: every eligibility and budget position traceable to a clause in a version-identified document.
- Currency requirements: all controlled sources current for the submission date, not the drafting date.
- Assumptions that must remain explicit: any eligibility or cost position resting on an unresolved rule reading.
- Reproducibility requirements: eligibility and budget logic reproducible from the bound sources.

## Knowledge-State Constraints
- Minimum input state for ordinary use: programme sources at SOURCE state with verification complete.
- Minimum input state for decision-grade use: material eligibility and applicant facts at REVIEWED or APPROVED; unresolved items explicitly UNKNOWN and visible to the human holding the submission decision.
- States the Pack may support deriving: SOURCE, FACT, CALCULATION for budget logic, ASSUMPTION for unresolved readings, CONFLICT_DETECTED, UNKNOWN.
- States the Pack may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict / contradiction escalation rule: contradiction between the regulation, work programme, call document and FAQ is raised as `CONFLICT_DETECTED` and escalated to the managing authority route or the human decision holder. It is never resolved by preferring the reading that permits the application.

Skills in this Pack may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review Dependencies
- Review Profile Reference(s): none at Pack level; resolved by the consuming Role and workflow. The consuming EU Grants & Programmes Specialist assignment carries `review.eu_programme_compliance`.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not perform independent assurance by identity.

Any evaluation, validation, completeness-checking or submission-readiness capability included in this Pack is a **quality-control technique, not independent review**. It does not discharge a `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation and creates no reviewer identity.

## Decision Dependencies
- Decision Right Reference(s): none at Pack level; resolved by the consuming Role and workflow. The consuming assignment carries `decision.granting_authority_submission`, `decision.partner_commitment` and `decision.budget_approval`.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not acquire human authority.

## External / Regulated Boundary
- Licensed / regulated activity boundary: none intrinsic.
- Required authorised professional class: the legal representative of the applicant for binding declarations.
- External submission / filing / publication boundary: submission to the granting authority is an external act, irreversible once the window closes, and gated by `decision.granting_authority_submission`.
- Production / deployment boundary: not applicable.
- Withdrawal / correction path: as permitted by the bound call rules; must be established at instantiation, not assumed.

## Data / Confidentiality Controls
- personal data categories: personal data of staff and experts in CVs and declarations.
- privileged / legally sensitive information: partner agreements and legal declarations.
- commercial / restricted information: partner cost structures and rates.
- storage / residency requirements: as required by the applicant's own controls and the portal's terms.
- cross-context reuse restrictions: partner and cost data from one application must not be imported into another context.

## Version and Change Control
A new Pack version is required on material change in: the programme regulation, work programme, call document or its guide; model grant agreement; cost categories, rates or ceilings; required annexes or formats; portal rules; compatible Role set; evidence requirements; or review / decision dependencies.

## Activation Criteria
Programme is LIFE **and** a specific call is identified with its guidance version bound.

## Deactivation / Invalidation Criteria
This Pack ceases to be current when any of the following occurs, and must be rebound before further use:
- the call closes or is withdrawn;
- a corrigendum or revised call guide is issued;
- the programme regulation or work programme is amended;
- the model grant agreement version changes;
- portal rules, formats or limits change;
- any bound controlled source becomes SUPERSEDED.

A stale Pack must not silently satisfy a contextual mapping obligation.

## Pack Integrity Rules
- Required Skills must be present when the Pack is activated unless an explicit governed exception exists.
- Optional Skills do not widen Role authority.
- Pack activation must not silently import facts or assumptions from another application, applicant or call.
- Controlled references must be current for the submission date.
- Where Pack requirements conflict with the Role Card or a stricter workflow control, the stricter rule prevails and the conflict is escalated.

## Prerequisites and Incompatibilities
- Prerequisite capabilities or Packs: none. Competence statements only; confer no authority.
- Incompatibilities: must not be applied to a different EU programme's call. Where a CoVE or Erasmus+ action is in scope, the applicable programme Pack governs instead — programme rules are not transferable between frameworks.

## Adjacent Packs
- `skill_pack.erasmus_plus`, `skill_pack.horizon_europe` — sibling programme Packs; no dependency in either direction, and rules are not portable between them.
- `skill_pack.bid_proposal_management` — supplies generic competitive-submission process; this Pack governs on every programme-specific requirement.

## Completion / Use Criteria
Properly applied when a specific call and guidance version are bound; eligibility, work-package, budget and submission-requirement positions each trace to a clause in a version-identified source; unresolved readings are UNKNOWN rather than assumed favourably; and the human submission decision holder can see what is unresolved.

## Failure Modes to Avoid
- Using a prior-round call guide or an unversioned summary.
- Treating a pack-internal capability as a reusable Skill outside a bound call.
- Resolving a rule ambiguity in the direction that permits the application.
- Carrying partner or cost data across applications.
- Treating submission-readiness checking as independent review.
- Letting the Pack remain active after a corrigendum.

## Reclassification Warning
If the Pack begins to own a recurring standalone professional artifact, professional conclusion or authority boundary independent of an assigned Role, stop and reassess whether the capability belongs in the Role Registry instead.
