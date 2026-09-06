# CoVE Programme Pack

Status: PROPOSED — Phase 4 exemplar Skill Pack Card

## Identity
- Pack Name: Centres of Vocational Excellence (CoVE)
- Pack ID: `skill_pack.cove`
- Type: Skill Pack
- Pack Class: `PROGRAMME`
- Contributing Skill Families: Project / Programme Delivery; Research & Evidence; Operations / Supply Chain / People; Documentation / Knowledge / Disclosure; Finance & Economics
- Included Specialisations: `specialisation.eu_grant_delivery`, `specialisation.multi_partner_programme_delivery`
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
Carry the action-specific rules, intervention logic and partnership requirements of the Centres of Vocational Excellence action as a governed layer on top of the Erasmus+ framework it operates under — so that CoVE-specific requirements are applied without restating, and without silently contradicting, the underlying programme rules.

**This card defines architecture, layering and controlled-source requirements only. It deliberately contains no current CoVE call content, deadline, budget figure, partnership threshold or annex list.** Those are instance data bound at activation from authoritative sources.

## Scope
### Covers
Action-specific capabilities, all **pack-internal controlled components rather than standalone Skill IDs**, layered over the Erasmus+ requirements the action inherits:

- **CoVE-specific eligibility and partnership composition** — the geographic, sectoral and institutional composition requirements the action imposes beyond the base framework;
- **vocational excellence intervention logic** — the skills-ecosystem, innovation and inclusion logic the action expects, and its expression as objectives and activities;
- **CoVE work-package and activity logic** — structuring consistent with the action's expected clusters of activity;
- **CoVE-specific budget logic** — the cost structure and co-financing expectations of the action, on top of the base framework's cost categories;
- **CoVE submission requirement mapping** — the action-specific forms, annexes, declarations and limits;
- **action-specific results and sustainability requirements** — the results framework and sustainability expectations the action attaches.

None may be re-created as a `skill.<id>`; each is meaningless outside a bound call and rulebook version.

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model/runtime selection;
- any Role scope not already granted by the assigned Role Card.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.eu_grants_programmes_specialist`, `role.eu_programme_implementation_grant_management_specialist`, `role.learning_vet_design_specialist`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, section 3
- Canonical mapping reference (Wave 2): `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

### Wave 2 allowlist basis

`role.eu_programme_implementation_grant_management_specialist` is admitted on the same basis as for the LIFE Pack: it owns obligation mapping and donor-rule interpretation against an executed agreement, which requires this action's rulebook and its inherited Erasmus+ layer at bound versions.

`role.learning_vet_design_specialist` is admitted because CoVE is a vocational-excellence action and that Role's Mandatory Assignment Attributes require a programme / qualification scope and an applicable framework and version reference — exactly what this Pack binds. It consumes the action's intervention logic to shape curriculum and assessment design; it gains no eligibility, budget or submission authority, all of which remain human decision rights.

Eligibility only; relationship and trigger come from the Wave 2 mapping record.

`role.learning_vet_design_specialist`, `role.monitoring_evaluation_learning_specialist` and `role.consortium_partner_coordination_specialist` are all substantively relevant to CoVE work and their Role Cards support the domain, but none is mapped to this Pack in the current record and none is listed. Wave 2 mapping decision.

Listing a Role confers eligibility, never a requirement.

### Typical Use — Advisory, Non-Authoritative
Non-binding: usually relevant where the action or programme context is CoVE and a specific call has been selected. States no obligation; the mapping record decides.

## Included Skills
### Required Skills
- `skill.source_verification` — both the CoVE call documentation and the underlying Erasmus+ rules must be verified and version-anchored.
- `skill.requirement_traceability` — action-specific and inherited requirements must be traced separately so that the source of each is visible.
- `skill.source_monitoring` — both layers of guidance are monitored for revision during the application window.

### Optional Skills
- `skill.partner_mapping`
- `skill.partner_coordination`
- `skill.results_framework_design`
- `skill.indicator_design`
- `skill.learning_outcome_design`
- `skill.grant_cost_eligibility_analysis`

### Alternative Skills
None.

## Pack Dependencies and Layering

**This Pack declares a one-directional, conditional layering over `skill_pack.erasmus_plus`.**

- Depends on / layers over: `skill_pack.erasmus_plus` — **conditional**: the dependency applies where the CoVE action operates under Erasmus+ rules, which is the ordinary case. Where a CoVE-type action is funded under a different framework, this dependency does not apply and the governing programme Pack is declared for that instance instead.
- Depended on by (informational): none.
- Layering metadata:
  - **CoVE adds** action-specific eligibility, partnership composition, intervention logic, activity structure, budget expectations, submission requirements and results/sustainability requirements **on top of** the applicable Erasmus+ requirements.
  - **CoVE inherits unchanged** the base framework's general eligibility, cost categories, grant agreement model, reporting architecture and portal rules, except where it states a more specific or stricter requirement.
  - Activation of this Pack activates `skill_pack.erasmus_plus`, subject to the duplicate-activation rule below.

**Direction and cycle safety:**
- The dependency direction is **CoVE → Erasmus+**, and only that direction.
- **`skill_pack.erasmus_plus` must not declare a dependency on `skill_pack.cove`.** Erasmus+ is the general framework; a great many actions run under it and it cannot depend on any one of them.
- **No circular dependency exists or may be created.** A reverse declaration would make activation order and precedence undefinable and is a validation failure, not a warning.

## Precedence With Overlapping Packs
Where this Pack and `skill_pack.erasmus_plus` — or any other active Pack — address the same subject with different requirements:
1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** Pack prevails — **CoVE is more specific than Erasmus+ and prevails on action-specific matters**;
3. where neither is clearly more specific, and the requirements cannot be reconciled, raise **`CONFLICT_DETECTED`** and escalate rather than resolving silently;
4. the Role Card and any stricter workflow or assignment control prevail over every Pack.

Precedence never operates in the permissive direction. CoVE may impose a requirement Erasmus+ does not; it may **not** relax an Erasmus+ requirement. Where CoVE appears to permit what the base framework prohibits, that is not CoVE prevailing — it is an unresolved inconsistency, and it escalates as `CONFLICT_DETECTED`.

## Duplicate Effective Activation
Because this Pack activates `skill_pack.erasmus_plus` transitively, both layers will require overlapping Skills — `skill.source_verification`, `skill.requirement_traceability` and `skill.source_monitoring` at minimum — and those are also individually mapped to `role.eu_grants_programmes_specialist`.

Each such Skill is activated **once**, under the **strictest** obligation across the individual mapping, this Pack and the inherited Pack, with the currency, evidence and controlled-source rules of both Packs applied on top. The individual mapping is retained only where it has meaning independent of the Packs, which it does for all three.

Duplicate effective activation must be detectable at validation time, not discovered during execution.

## Authority Limits of Activation
Activating this Pack, and the Pack it layers over, **cannot** satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

Layering accumulates constraints, never authority. A stack of two programme Packs confers exactly the authority of the assigned Role Card and nothing more. Submission, partner commitment and budget approval remain `decision.granting_authority_submission`, `decision.partner_commitment` and `decision.budget_approval`, held by humans.

## Applicability
- Jurisdiction(s): EU and participating countries as defined by the bound programme rules.
- Sector(s): vocational education and training and the sectoral ecosystems the action addresses.
- Programme / framework: CoVE, layered over Erasmus+ at their bound versions.
- Institution / financing framework: the executive agency named in the bound call.
- Technology / version: not applicable.
- Operating context: application preparation and submission.
- Criticality conditions: none intrinsic.
- Assignment prerequisites: a specific CoVE call must be identified, its guidance version bound, **and** the applicable Erasmus+ rules version bound. Without both layers bound, the Pack must not be treated as active.

## Controlled Methodology / Source Package
Required at instantiation, each captured with source / authority, title / identifier, version, effective date, expiry or supersession status, and applicability, **for both layers**:
- the Erasmus+ programme regulation and programme guide in force for the call;
- the applicable annual work programme;
- the CoVE call document and any action-specific guidance;
- the applicable model grant agreement and annotations;
- application form and annex templates at call-specific versions;
- submission portal rules, formats and limits;
- any corrigendum or FAQ issued during the window, at either layer.

**AI-generated content must not be listed as a controlled source.** Nor may prior-round documentation or third-party summaries substitute for current call text at either layer.

## Evidence Requirements
- Required evidence classes: official programme and call documentation at both layers; partner legal, financial and operational capacity documentation; substantiation for every eligibility, composition and capacity claim.
- Minimum source quality: authoritative publication channel of the programme authority.
- Required provenance: every position traceable to a clause in a version-identified document, **with the layer identified** — action-specific or inherited.
- Currency requirements: both layers current for the submission date.
- Assumptions that must remain explicit: any position resting on an unresolved reading at either layer, and any assumption that the base framework's rule applies unchanged.
- Reproducibility requirements: eligibility, composition and budget logic reproducible from the bound sources of both layers.

## Knowledge-State Constraints
- Minimum input state for ordinary use: programme sources at both layers at SOURCE state with verification complete.
- Minimum input state for decision-grade use: material eligibility, partnership and applicant facts at REVIEWED or APPROVED; unresolved items explicitly UNKNOWN and visible to the human holding the submission decision.
- States the Pack may support deriving: SOURCE, FACT, CALCULATION for budget logic, ASSUMPTION for unresolved readings, CONFLICT_DETECTED, UNKNOWN.
- States the Pack may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict / contradiction escalation rule: any inconsistency between the CoVE layer and the Erasmus+ layer that is not resolved by the precedence rules above is raised as **`CONFLICT_DETECTED`** and escalated to the programme authority route or the human decision holder. It is never resolved by adopting the reading that permits the application, and never by assuming the action-specific text silently overrides a base prohibition.

Skills in this Pack may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review Dependencies
- Review Profile Reference(s): none at Pack level; resolved by the consuming Role and workflow. The consuming EU Grants & Programmes Specialist assignment carries `review.eu_programme_compliance`.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not perform independent assurance by identity.

Any completeness-checking, validation or submission-readiness capability applied under this Pack is a **quality-control technique, not independent review**. It does not discharge a `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation and creates no reviewer identity.

## Decision Dependencies
- Decision Right Reference(s): none at Pack level; resolved by the consuming Role and workflow. The consuming assignment carries `decision.granting_authority_submission`, `decision.partner_commitment` and `decision.budget_approval`.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not acquire human authority.

## External / Regulated Boundary
- Licensed / regulated activity boundary: none intrinsic; national VET accreditation regimes may apply to partners and are outside this Pack.
- Required authorised professional class: the legal representative of the coordinating institution for binding declarations.
- External submission / filing / publication boundary: submission is an external act, irreversible once the window closes, gated by `decision.granting_authority_submission`.
- Production / deployment boundary: not applicable.
- Withdrawal / correction path: as permitted by the bound call rules at both layers; must be established, not assumed.

## Data / Confidentiality Controls
- personal data categories: personal data of staff and experts in CVs and declarations across all partners.
- privileged / legally sensitive information: partnership agreements and mandates.
- commercial / restricted information: partner cost structures and rates.
- storage / residency requirements: per each partner's controls and the portal's terms.
- cross-context reuse restrictions: partner data from one application must not be imported into another consortium's context.

## Version and Change Control
A new Pack version is required on material change in: the CoVE call or action guidance; **the Erasmus+ layer this Pack depends on**; the model grant agreement; cost categories or co-financing structure; partnership composition requirements; required annexes or formats; portal rules; compatible Role set; evidence requirements; or review / decision dependencies.

A change at the inherited layer invalidates this Pack instance even where the CoVE text is unchanged.

## Activation Criteria
The action or programme context is CoVE **and** a specific call is identified, with both the CoVE guidance and the applicable Erasmus+ rules versions bound.

## Deactivation / Invalidation Criteria
- the call closes or is withdrawn;
- a corrigendum or revised guidance is issued at **either** layer;
- the Erasmus+ programme regulation, programme guide or work programme is amended;
- the model grant agreement version changes;
- portal rules, formats or limits change;
- any bound controlled source at either layer becomes SUPERSEDED.

A stale Pack must not silently satisfy a contextual mapping obligation.

## Pack Integrity Rules
- Required Skills must be present when the Pack is activated unless an explicit governed exception exists.
- Optional Skills do not widen Role authority.
- Pack activation must not silently import facts or assumptions from another application, consortium or call.
- Controlled references at **both** layers must be current for the submission date.
- Where Pack requirements conflict with the Role Card or a stricter workflow control, the stricter rule prevails and the conflict is escalated.

## Prerequisites and Incompatibilities
- Prerequisite capabilities or Packs: `skill_pack.erasmus_plus` where the conditional dependency applies. Competence statement only; confers no authority.
- Incompatibilities: must not be applied to a non-CoVE action, and must not be used with the Erasmus+ layer unbound where the dependency applies.

## Adjacent Packs
- `skill_pack.erasmus_plus` — the framework this Pack layers over, one-directionally.
- `skill_pack.life_programme`, `skill_pack.horizon_europe` — sibling programme frameworks; no dependency in any direction and rules are not portable.
- `skill_pack.bid_proposal_management` — composes alongside for process scaffolding; this Pack governs every programme rule.

## Completion / Use Criteria
Properly applied when both layers are bound with versions; every position is traced to a clause with its layer identified; action-specific requirements are distinguished from inherited ones; precedence is applied in the stricter/more-specific direction only; unresolved inconsistencies between layers are raised as `CONFLICT_DETECTED` rather than resolved; and the human submission decision holder can see what is unresolved.

## Failure Modes to Avoid
- Treating CoVE guidance as self-contained and leaving the Erasmus+ layer unbound.
- Reading an action-specific provision as relaxing a base-framework prohibition.
- Losing track of which layer a requirement came from.
- Declaring or implying a reverse dependency from Erasmus+ to CoVE.
- Leaving the Pack active after a corrigendum at the inherited layer.
- Resolving a cross-layer inconsistency in the direction that permits the application.

## Reclassification Warning
If the Pack begins to own a recurring standalone professional artifact, professional conclusion or authority boundary independent of an assigned Role, stop and reassess whether the capability belongs in the Role Registry instead.
