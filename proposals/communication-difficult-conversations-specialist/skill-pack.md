# Difficult Conversations Skill Pack — Candidate

Status: `PROPOSED`
Template: Skill Pack Template (Phase 4 standard candidate)
Inherits: `standard.skill.common_constraints@0.1`

> Candidate only. Listing a Skill here does not create it, and listing a Role here confers
> eligibility, never a requirement. Role-to-Skill mapping records remain the sole authoritative
> source for relationship type and context trigger; this card is not.

## Identity
- Pack Name: **Difficult Conversations & Communication Control**
- Pack ID (as fixed by the source prompt): `pack.communication.difficult_conversations@0.1`
- Registry-normalised alternative (see `README.md` §7, open item **OG-1**):
  `skill_pack.communication_difficult_conversations@0.1`
- Type: Skill Pack
- Pack Class: `METHOD`
- Contributing Skill Families: Strategy & Analysis; Research & Evidence; Knowledge, Documentation
  & Disclosure
- Included Specialisations: none
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS architecture governance
- Effective Date: on approval, not before
- Review Date: 12 months from approval
- Expiry / Invalidation Trigger: a change to `method.communication.calm_direct_control`, to the
  role's Decision Right references, or to the approved skill universe entries below
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Bundle the capabilities required to diagnose a difficult interaction, decide a communication
response posture, and draft under control — so that they travel together, versioned, rather than
being reassembled per assignment.

## Scope

### Covers
- diagnosis of an adversarial, ambiguous or high-stakes interaction;
- separation of fact, assumption and interpretation in contested text;
- issue triage and response classification;
- boundary, refusal and escalation drafting;
- channel, timing and documentation judgement;
- application of the Communication Control Filter.

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model / runtime selection;
- any Role scope not already granted by the assigned Role Card;
- legal, financial, technical, compliance or institutional conclusions;
- psychological or clinical assessment.

## Compatible Roles — Allowlist Only

- `role.communication_difficult_conversations_specialist` *(candidate — this pack's primary
  consumer; both are PROPOSED together)*
- `role.institutional_communications_editorial_specialist`
- `role.institutional_affairs_stakeholder_specialist`
- `role.people_organisation_specialist`
- `role.programme_partnership_manager`
- `role.consortium_partner_coordination_specialist`
- `role.project_delivery_lead`
- `role.portfolio_programme_manager`

Canonical mapping reference: a Role-to-Skill mapping record must exist per Role above before
activation. **None exists today**; this list is eligibility, not mapping.

### Typical Use — Advisory, Non-Authoritative

Usually relevant where `communication_conflict_score >= 35` (`trigger-routing-spec.md`), or where
an assignment explicitly requests communication strategy for a contested interaction. Non-binding.

## Included Skills

### Required Skills — existing approved skill-universe entries

These already exist in `skills/master-skill-universe.md` and are **referenced, not created**:

| `skill.<id>` | What it contributes here |
|---|---|
| `skill.fact_extraction` | Extracting stated assertions from an interaction record, as `EVIDENCE` bound to their location, without importing the surrounding characterisation |
| `skill.assumption_analysis` | Making the reconstructed objective and the inferred counterparty position explicit as assumptions |
| `skill.evidence_mapping` | Linking every `FACT_CLAIM` in a draft to the `EVIDENCE` that supports it |
| `skill.source_verification` | Establishing whether a cited prior message, date or commitment actually exists in the record |
| `skill.problem_structuring` | Decomposing a long hostile thread into separable issues |
| `skill.position_mapping` | Stating the user's position and the counterparty's position as distinct objects |
| `skill.stakeholder_mapping` | Identifying who is on the thread, who decides, and who is merely copied |
| `skill.relationship_risk_analysis` | Assessing what a given response posture costs the relationship |
| `skill.risk_identification` | Surfacing escalation, documentation, legal-exposure and disclosure risks |
| `skill.negotiation_preparation` | Preparing position, boundary set and anticipated moves for a negotiation episode |
| `skill.meeting_brief_preparation` | Producing the interaction brief for a meeting or call |
| `skill.engagement_strategy_design` | Choosing channel, sequence and audience for the engagement |
| `skill.document_structuring` | Structuring a formal escalation or final-position message |
| `skill.technical_writing` | Precise, unambiguous prose under adversarial reading |
| `skill.editorial_quality_control` | Final pass for clarity, consistency and register |
| `skill.decision_criteria_design` | Framing the binary or option-set question a message asks for |
| `skill.action_tracking` | Naming the next step, its owner and its date |
| `skill.change_detection` | Noticing that a new draft, term or claim differs from the prior version |

### Candidate Skills — genuinely missing, marked as candidates

These have **no equivalent** in the approved skill universe. Each is proposed, none is created by
this document, and each requires Skill Registry change control:

| Candidate `skill.<id>` | Why no existing skill covers it |
|---|---|
| `skill.interaction_response_triage` *(candidate)* | Classifying each issue in a record as `RESPOND / CLARIFY / REDIRECT / IGNORE / DOCUMENT / ESCALATE`. The universe has risk and issue analysis, but no response-posture classification |
| `skill.boundary_formulation` *(candidate)* | Expressing a limit as self-directed action that holds without requiring the other party's agreement |
| `skill.refusal_design` *(candidate)* | Producing an unambiguous no with minimum sufficient rationale and an optional narrower alternative |
| `skill.de_escalation_framing` *(candidate)* | Reducing conflict temperature without weakening a protection — the constraint, not the softening, is the skill |
| `skill.communication_reactivity_detection` *(candidate)* | Detecting reactivity **in wording**, explicitly not in people. No existing skill does this, and no clinical skill may substitute |
| `skill.conversational_control` *(candidate)* | Restoring structure when the exchange changes topic, reopens a closed point or avoids the question |
| `skill.non_response_strategy` *(candidate)* | Evaluating silence and delay as deliberate moves with recorded reasons |
| `skill.communication_control_filtering` *(candidate)* | Applying the ten-factor filter and recording component scores |

**Rule SP-1 — a candidate skill is not a skill.** Until each is registered through Phase 4 change
control, an assignment relying on it is relying on an unregistered capability. The pack is not
activatable in a governed run while any Required Skill is a candidate.

### Optional Skills
- `skill.consultation_design` — where the interaction is part of a structured consultation
- `skill.legal_issue_spotting` — **only** to raise that legal input is needed; never to conclude
- `skill.claim_substantiation` — where a factual claim in the thread must be evidenced
- `skill.document_version_control` — where the exchange concerns successive drafts of an instrument

### Alternative Skills
None. No skill in this pack has an interchangeable substitute; substitution here would change
what the pack does.

## Pack Dependencies and Layering

- **Depends on / layers over:** none. This is a base `METHOD` pack.
- **Depended on by (informational):** none today.
- **Layering metadata:** where a programme, institution or sector pack is also active, this pack
  adds communication-control technique and adds no domain rule. It inherits every constraint of
  the other pack unchanged.

No circular dependency exists because there is no dependency.

## Precedence With Overlapping Packs

Where another active pack addresses the same subject with different requirements:

1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** pack prevails — a programme or
   institutional communication rule beats this generic method pack;
3. where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate;
4. the Role Card and any stricter workflow or assignment control prevail over every pack.

**This pack may tighten a communication requirement. It may never relax one**, and in particular
it may never relax a programme's or institution's own disclosure, tone, language or approval rule.

## Duplicate Effective Activation

Where a Skill above is also mapped individually to the same Role, it activates **once**, under
the stricter of the two obligations, with this pack's evidence rules applied on top. Detectable
at validation time.

## Authority Limits of Activation

Activating this pack cannot satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

In particular, activating this pack **never** produces authority to send, publish, file or
transmit, and never converts a drafted message into an approved one.

## Applicability

- Jurisdiction(s): none-specific; jurisdictional content belongs to the owning substantive Role
- Sector(s): none-specific
- Programme / framework: none-specific
- Institution / financing framework: none-specific
- Technology / version: none
- Operating context: any interaction with a named counterparty inside an assigned scope
- Criticality conditions: activation is permitted at every band; at high and critical bands the
  Review Profile references below become mandatory
- Assignment prerequisites: the mandatory assignment attributes of `role-card.md`

## Controlled Methodology / Source Package

| Source / authority | Identifier | Version | Effective date | Status |
|---|---|---|---|---|
| AI-OS architecture governance | `method.communication.calm_direct_control` | 0.1 | on approval | PROPOSED |

No external controlled source is required, and **no AI-generated content is listed as a
controlled source**. Public communication principles are general knowledge and are not cited as a
controlled source; where a specific published work would be needed, that is a licensing question
and is out of this pack's scope (`README.md` §3).

## Evidence Requirements

- **Required evidence classes:** the interaction record; substantive conclusions at their
  versions; approved positions as references.
- **Minimum source quality:** the record itself, unedited and attributed. A paraphrase of a thread
  is not the thread.
- **Required provenance:** sender, recipient set, timestamp and thread position for every message
  relied on.
- **Currency requirements:** a substantive conclusion older than its own validity rule is `UNKNOWN`.
- **Assumptions that must remain explicit:** inferred objective; reconstructed counterparty
  position; any reading of intent.
- **Reproducibility requirements:** the triage classification per issue, the filter component
  scores, and the conflict-score inputs must be reproducible from the record.

## Knowledge-State Constraints

- Minimum input state for ordinary use: interaction record `SOURCE`; substantive conclusions
  `DRAFT` and attributed.
- Minimum input state for decision-grade use: substantive conclusions `REVIEWED` or `APPROVED`.
- States the pack may support deriving: `EVIDENCE` bound to a location in the record, and a
  **new linked** `FACT_CLAIM` supported by it; `DRAFT` for role outputs. The record stays
  `SOURCE`; there is **no** `SOURCE` → `FACT_CLAIM` transition and the deprecated label `FACT`
  is not used (`role-card.md` RC-4).
- States the pack may not promote autonomously: everything above `DRAFT`, and every transition to
  `REVIEWED`, `APPROVED` or `CANONICAL`.
- Conflict / contradiction escalation rule: `CONFLICT_DETECTED` and escalate; never resolve
  silently by choosing the more convenient version.

Skills in this pack contribute to Role-owned knowledge-state work and **can never execute a
knowledge-state transition**.

## Review Dependencies

- `review.communication_strategy@0.1` *(candidate)* — triggered under `role-card.md` **RC-5**, which is the single authoritative trigger
- `review.high_stakes_external_communication@0.1` *(candidate)* — triggered by any high-stakes
  condition of `trigger-routing-spec.md` §5
- `review.legal_compliance` — where legal exposure is material
- `review.institutional_position` — where the message states or implies an institutional position
- `review.data_protection` — where personal data is disclosed

Dependencies only. Any evaluation or filtering capability in this pack — including the
Communication Control Filter — is a **quality-control technique, not independent review**. It
discharges no `review.<id>`, satisfies no `Author != Critical Reviewer` obligation, and creates no
reviewer identity.

## Decision Dependencies

- As resolved by `decision-right-gap-analysis.md` §4 for the intended external act.

Dependencies only; the pack acquires no human authority.

## External / Regulated Boundary

- Licensed / regulated activity boundary: legal, employment, tax and regulatory positions.
- Required authorised professional class: as determined by the owning substantive Role.
- External submission / filing / publication boundary: every transmitting act of `role-card.md`
  §Output Artifact Interfaces.
- Production / deployment boundary: none; this pack produces no deployable artifact.
- Withdrawal / correction path: a correcting communication is a **new** governed act with its own
  gate. There is no undo.

## Data / Confidentiality Controls

- Personal data categories: identities, contact data, employment and performance data, grievance
  content, and any special-category data the thread contains.
- Privileged / legally sensitive information: legal advice, litigation strategy, without-prejudice
  and settlement material. The pack must not widen the audience of privileged material.
- Commercial / restricted information: pricing, live-procedure bid content, transaction terms,
  unpublished financials, third-party confidential material.
- Storage / residency: as labelled by the assignment.
- Cross-context reuse restrictions: **prohibited** without a governed handoff or scope transfer.

## Version and Change Control

A new pack version is required on a material change to the methodology basis, the required skill
composition, the compatible Role set, the evidence requirements, or the review / decision
dependencies.

## Activation Criteria

- an assignment binds `role.communication_difficult_conversations_specialist` (or an eligible Role
  above with a valid mapping record); **and**
- the assignment names a bounded interaction within one scope; **and**
- every Required Skill above is registered and current.

## Deactivation / Invalidation Criteria

- the methodology version is superseded;
- a Required Skill is deprecated or its mapping is withdrawn;
- the assignment's scope binding changes;
- the interaction record is withdrawn or its disclosure basis lapses.

## Pack Integrity Rules

- Required Skills must be present when the pack is activated; a candidate skill is not present
  (SP-1).
- Optional Skills do not widen Role authority.
- Pack activation must not import facts, positions or tone from another project or organisation
  context.
- Where pack requirements conflict with the Role Card or a stricter workflow control, the stricter
  rule prevails and the conflict is escalated.

## Prerequisites and Incompatibilities

- **Prerequisite capabilities:** competence in the Required Skills. Competence statements confer
  no authority.
- **Incompatibilities:** must not be combined with any pack or context that would have it produce
  a clinical, diagnostic or therapeutic output; must not be activated on a data classification
  whose disclosure basis for the assignment is absent.

## Adjacent Packs

- `skill_pack.bid_proposal_management` — overlaps on persuasive written output; that pack owns bid
  narrative, this one owns contested interaction. Neither owns the other's artifact.

## Completion / Use Criteria

The pack is properly applied when every issue carries a triage classification, every factual
assertion is source-linked, the filter component scores are recorded, and the required reviews and
the human gate — or the fail-closed block — are named.

## Failure Modes to Avoid

Advisory:
- treating pack activation as professional authority;
- treating the filter score as a release approval;
- using a candidate skill as if it were registered;
- embedding one counterparty's history into the pack rather than into the assignment;
- letting the pack's tone rules override a programme's own communication rules.

## Reclassification Warning

If this pack begins to own a recurring standalone professional artifact or an authority boundary
independent of an assigned Role, stop and reassess whether the capability belongs in the Role
Registry instead. That reassessment is precisely why
`role.communication_difficult_conversations_specialist` is proposed as a Role rather than as a
specialisation bolted onto an existing one — see `self-check.md` §7.
