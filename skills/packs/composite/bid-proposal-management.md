# Bid / Proposal Management Pack

Status: PROPOSED — Phase 4 exemplar Skill Pack Card

## Identity
- Pack Name: Bid / Proposal Management
- Pack ID: `skill_pack.bid_proposal_management`
- Type: Skill Pack
- Pack Class: `COMPOSITE`
- Contributing Skill Families: Project / Programme Delivery; Sales / Marketing / Customer; Documentation / Knowledge / Disclosure; Legal / Compliance / Procurement; Research & Evidence
- Included Specialisations: none
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Effective Date: on approval of this card
- Review Date: with the Phase 4 registry review cycle
- Expiry / Invalidation Trigger: see Deactivation / Invalidation Criteria
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: `skill.bid_proposal_management` (retired standalone Skill)
- Superseded By: none

## Purpose
Run a formal competitive bid or proposal as a governed process with a hard external deadline: qualify the opportunity, establish what compliance actually requires, plan contributions, coordinate a coherent narrative, substantiate every claim, and reach submission readiness with time to spare.

**This Pack replaces the retired standalone `skill.bid_proposal_management` concept.** That identifier was removed because bid management is not a single reusable technique — it is a bundle of qualification, compliance, planning, coordination and control practices that only work together, carry their own currency rules, and would be misleading as one Skill. It must not be reintroduced as a `skill.<id>`.

## Scope
### Covers
- **opportunity qualification** — whether to bid at all, on capability, fit, competitive position and cost of bidding, with an explicit no-bid path;
- **requirements and compliance matrix** — extracting every mandatory requirement, format rule, limit and exclusion criterion from the solicitation and tracing each to the response element discharging it;
- **contribution planning** — who contributes what, in what sequence, against the submission date;
- **deliverable schedule** — an internal schedule with review and buffer time working backwards from the external deadline;
- **narrative coordination** — a coherent voice and consistent claims across contributions from multiple authors;
- **evidence and claim substantiation** — every capability, performance and reference claim tied to evidence that survives scrutiny;
- **submission-readiness quality control** — final completeness, format-compliance and consistency checking against the compliance matrix before submission.

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model/runtime selection;
- any Role scope not already granted by the assigned Role Card.

Specifically **not** covered:
- **Programme-specific rules.** This Pack does not replace `skill_pack.life_programme`, `skill_pack.erasmus_plus`, `skill_pack.cove`, `skill_pack.horizon_europe` or any institution Pack. It supplies process scaffolding; the programme Pack supplies the rules, and the programme Pack governs wherever both speak.
- **Legal signature and contract commitment.** Owned by `role.legal_regulatory_lead`, gated by `decision.contract_commitment` and `decision.legal_filing_or_representation`.
- **Pricing and commercial approval.** Gated by `decision.commercial_commitment`.
- **Budget approval.** Gated by `decision.budget_approval`.
- **External submission authority.** Gated by `decision.granting_authority_submission` for granting authorities and `decision.external_commercial_communication` for commercial submissions.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.eu_grants_programmes_specialist`, `role.sales_business_development_specialist`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, sections 3 and 11

Listing a Role confers eligibility, never a requirement.

### Typical Use — Advisory, Non-Authoritative
Non-binding: usually relevant where a formal competitive process has a governed submission cycle, mandatory compliance requirements and a fixed external deadline. States no obligation; the mapping record decides.

## Included Skills
### Required Skills
- `skill.opportunity_qualification` — the bid/no-bid decision precedes everything else.
- `skill.requirement_traceability` — the compliance matrix is a traceability structure; without it, completeness is asserted rather than demonstrated.
- `skill.deliverable_planning` — contribution planning against the deadline.
- `skill.milestone_management` — internal milestones with review and buffer time.

### Optional Skills
- `skill.proposal_commercial_narrative`
- `skill.claim_substantiation`
- `skill.document_structuring`
- `skill.publication_requirements_validation`
- `skill.partner_mapping`
- `skill.source_verification`

### Alternative Skills
None.

## Pack Dependencies and Layering
- Depends on / layers over: none. This Pack is deliberately independent of any programme Pack so that it can be composed with whichever one applies.
- Depended on by (informational): none currently.
- Layering metadata: not applicable. Where a programme Pack is also active, the relationship is composition governed by precedence below, not dependency.

No circular dependency is possible for this Pack, since it declares none. It must not be made to depend on a programme Pack, nor a programme Pack on it — either would create a cycle as soon as the other side composed back.

## Precedence With Overlapping Packs
Where another active Pack addresses the same subject with different requirements:
1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** Pack prevails — a programme or institution Pack is more specific than this composite process Pack and governs on every rule it covers;
3. where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate rather than resolving silently;
4. the Role Card and any stricter workflow or assignment control prevail over this Pack.

Precedence never operates in the permissive direction. Where this Pack's generic submission-readiness practice is looser than a programme Pack's mandatory format rule, the programme rule governs; this Pack never relaxes a programme requirement.

## Duplicate Effective Activation
`skill.requirement_traceability` is individually mapped to several Roles and is also required here. `skill.source_verification`, `skill.deliverable_planning`, `skill.milestone_management` and `skill.partner_mapping` are similarly reused.

Where a Skill in this Pack is also mapped individually to the same Role, it is activated **once**, under the **stricter** of the two obligations, with this Pack's process rules applied on top. The individual mapping is retained only where it has meaning independent of this Pack, which it does for all of the above.

This matters especially where this Pack and a programme Pack are both active and both require `skill.requirement_traceability`: it activates once, under the strictest obligation, with the programme Pack's format requirements governing the matrix.

Duplicate effective activation must be detectable at validation time, not discovered during execution.

## Authority Limits of Activation
Activating this Pack **cannot** satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

Those obligations are discharged only through the assigned Role Card, the applicable Review Profile and the applicable Decision Right. Reaching submission readiness is not authority to submit.

## Applicability
- Jurisdiction(s): unrestricted.
- Sector(s): unrestricted.
- Programme / framework: unrestricted; the applicable programme Pack composes alongside and governs its own rules.
- Institution / financing framework: unrestricted.
- Technology / version: not applicable.
- Operating context: formal competitive bid or proposal with a governed submission cycle.
- Criticality conditions: none intrinsic.
- Assignment prerequisites: a solicitation or call must exist with stated requirements and a deadline.

## Controlled Methodology / Source Package
Required at instantiation, each captured with source / authority, title / identifier, version, effective date, expiry or supersession status, and applicability:
- the solicitation, call or tender document and any addenda or corrigenda;
- the applicable programme or institutional rules where a programme Pack is active;
- evaluation and award criteria as published;
- format, limit and annex requirements;
- the organisation's own approved claim and reference evidence base;
- the applicable procurement or programme legal framework where it constrains the response.

**AI-generated content must not be listed as a controlled source**, and AI-drafted narrative is never evidence for a claim it makes.

## Evidence Requirements
- Required evidence classes: substantiation for every capability, performance, reference and compliance claim; evidence of eligibility and standing.
- Minimum source quality: verifiable and attributable; a claim that cannot survive a request for evidence must not be made.
- Required provenance: each claim traceable to its evidence and each requirement to its response element.
- Currency requirements: references and certifications current at the submission date, not the drafting date.
- Assumptions that must remain explicit: any claim resting on an intended rather than existing capability.
- Reproducibility requirements: the compliance matrix must be reproducible from the solicitation.

## Knowledge-State Constraints
- Minimum input state for ordinary use: solicitation at SOURCE state, verified.
- Minimum input state for decision-grade use: material claims, pricing, scope and performance statements at REVIEWED or APPROVED before anything is externally transmitted.
- States the Pack may support deriving: SOURCE, FACT, CALCULATION for schedules and coverage, ASSUMPTION for intended capability, CONFLICT_DETECTED, UNKNOWN.
- States the Pack may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict / contradiction escalation rule: contradictions between the solicitation and an addendum, or between two contributions making incompatible claims, are raised as `CONFLICT_DETECTED` and escalated. Narrative coordination must never harmonise two claims into a third that neither contributor's evidence supports.

Skills in this Pack may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review Dependencies
- Review Profile Reference(s): none at Pack level; resolved by the consuming Role and workflow. Consuming assignments carry `review.eu_programme_compliance` or `review.commercial_claims` as applicable to their Role.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not perform independent assurance by identity.

**Submission-readiness quality control is not independent review.** It is a completeness and format self-check performed by the bid team against its own matrix. It does not discharge a `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation and creates no reviewer identity. Where claim substantiation must be independently reviewed, that is `review.commercial_claims` or the applicable programme review, performed by someone who did not author the response.

## Decision Dependencies
- Decision Right Reference(s): none at Pack level; resolved by the consuming Role and workflow. Consuming assignments carry `decision.granting_authority_submission`, `decision.partner_commitment` and `decision.budget_approval`, or `decision.commercial_commitment` and `decision.external_commercial_communication`, according to Role.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not acquire human authority.

## External / Regulated Boundary
- Licensed / regulated activity boundary: none intrinsic; procurement law may constrain conduct during the process.
- Required authorised professional class: the authorised signatory for binding declarations and any priced offer.
- External submission / filing / publication boundary: submission is an external act, generally irreversible once the deadline passes, and always gated by a human decision right.
- Production / deployment boundary: not applicable.
- Withdrawal / correction path: as permitted by the solicitation; must be established rather than assumed.

## Data / Confidentiality Controls
- personal data categories: CVs and personnel data in team sections.
- privileged / legally sensitive information: legal declarations and any privileged advice on the process.
- commercial / restricted information: pricing, margins, partner terms and competitive positioning.
- storage / residency requirements: per the organisation's controls and any solicitation confidentiality terms.
- cross-context reuse restrictions: pricing and partner terms from one bid must never be imported into another; reusable narrative may be reused only after its claims are re-substantiated for the new context.

## Version and Change Control
A new Pack version is required on material change in: the process model; required skill composition; compliance-matrix method; evidence requirements; compatible Role set; or review / decision dependencies.

## Activation Criteria
A formal competitive bid or proposal process with a governed submission cycle is in scope.

## Deactivation / Invalidation Criteria
- the bid is withdrawn or the no-bid decision is taken;
- submission completes;
- the solicitation is cancelled or materially reissued, requiring re-instantiation.

A stale Pack must not silently satisfy a contextual mapping obligation.

## Pack Integrity Rules
- Required Skills must be present when the Pack is activated unless an explicit governed exception exists.
- Optional Skills do not widen Role authority.
- Pack activation must not silently import pricing, claims or partner terms from another bid.
- Controlled references must be current for the submission date.
- Where Pack requirements conflict with the Role Card or a stricter workflow control, the stricter rule prevails and the conflict is escalated.

## Prerequisites and Incompatibilities
- Prerequisite capabilities or Packs: none. Where a programme applies, the programme Pack composes alongside. Competence statements only; confer no authority.
- Incompatibilities: must not be used as a substitute for a programme Pack, and must not be treated as conferring submission, pricing or signature authority.

## Adjacent Packs
- `skill_pack.life_programme`, `skill_pack.cove`, `skill_pack.erasmus_plus`, `skill_pack.horizon_europe` — programme Packs that compose with this one and govern their own rules.

## Completion / Use Criteria
Properly applied when a bid/no-bid decision is recorded; every mandatory requirement is traced to a response element; every claim is substantiated; the internal schedule leaves review and buffer time before the external deadline; readiness checking is complete against the matrix; and the human holding the submission decision can see what remains unresolved.

## Failure Modes to Avoid
- Skipping qualification and bidding by default.
- Building the matrix from the narrative instead of the solicitation.
- Harmonising contributions into claims no contributor can evidence.
- Reusing narrative without re-substantiating its claims.
- Treating readiness checking as independent review.
- Letting this Pack's generic practice override a programme Pack's mandatory rule.
- Carrying pricing or partner terms between bids.

## Reclassification Warning
If the Pack begins to own a recurring standalone professional artifact, professional conclusion or authority boundary independent of an assigned Role, stop and reassess whether the capability belongs in the Role Registry instead.
