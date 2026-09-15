# High-Stakes External Communication Review — Review Profile Candidate

Status: `PROPOSED`
Template: Review Profile Card Template (Phase 6 standard candidate)
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: **High-Stakes External Communication Review**
- Review ID: `review.high_stakes_external_communication@0.1`
- Version: 0.1 · Status: PROPOSED
- Review Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Establish that a communication about to leave the entity in a high-stakes setting has been checked
across **every** domain it touches, that each domain's conclusion is present and intact, and that
the human authority required to transmit it has been correctly identified. It is a composition
review: its job is to find the domain nobody checked, not to re-check the domains that were.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.communication.draft_communication`, where `high_stakes_communication = true` | `role.communication_difficult_conversations_specialist` *(candidate)* |
| A formal escalation artifact intended for an external recipient | as above |

The owning Role is the producer and is ineligible to satisfy this review.

## Applicability / Trigger

Mandatory where the draft is intended to leave the entity **and any** high-stakes condition of
`trigger-routing-spec.md` §5 holds: threatened or live litigation; contractual admission or waiver;
a board, donor, lender, regulator or granting-authority audience; a public statement or media
contact; a formal complaint or its response; a funding consequence; termination, exclusion or a
final warning; material reputational exposure; sensitive or special-category personal data; an
irreversible commitment; or a critical stakeholder relationship.

Not applicable to internal-only communication, and not applicable where no transmission is
contemplated. Where a message is internal today and external tomorrow, the trigger applies on the
day it becomes external.

## Required Evidence Package

- everything in the `review.communication_strategy@0.1` evidence package;
- **that review, `SATISFIED` and not `STALE`**;
- every domain conclusion the draft carries, supplied at its version by its owning Role;
- each triggered domain review and its status;
- the disclosure basis where personal, privileged or restricted material appears;
- the identified `decision.<id>` for the transmitting act, **or** the recorded fail-closed block;
- the audience, channel and timing the approval will be bound to.

An incomplete package produces `REVIEW_BLOCKED`. A package with no identified Right and no recorded
block is incomplete: "we have not decided yet" is not a gate identification.

## Independence Class

**`INDEPENDENT_ASSURANCE_REVIEW`** at every band at which this Profile applies. It applies only in
high-stakes settings, and a lesser class there would mean the last check before an irreversible
external act is performed by someone inside the work.

## Reviewer Eligibility

| `role.<id>` | Eligibility class | Scope basis in its Role Card | Dimension covered |
|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate, independent instance)* | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns communication strategy only | Communication composition and gate identification |
| `role.legal_regulatory_lead` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns legal conclusions | Admissions, waivers, reservations, litigation exposure |
| `role.institutional_communications_editorial_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns editorial standards and institutional voice | Public register and institutional voice |
| `role.data_protection_gdpr_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns lawful basis | Personal-data disclosure |
| `role.institutional_affairs_stakeholder_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns institutional positioning | Institutional relationship exposure |
| `role.enterprise_project_risk_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns risk characterisation | Exposure characterisation — **never risk acceptance** |
| `role.integrity_due_diligence_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns integrity findings | Integrity and misconduct exposure |
| `role.knowledge_evidence_steward` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns evidence provenance | Chronology and source integrity |

**No Role is `FULL_PROFILE_REVIEWER_ELIGIBLE` for this Profile**, and that is deliberate: no
approved Role's scope covers legal, institutional, data-protection, integrity, risk and
communication satisfaction criteria at once. Satisfaction therefore requires **every triggered
dimension to be covered by an eligible bounded contributor**, and the absence of a full-Profile
reviewer may not be treated as a licence for one contributor to cover the rest.

Partial expertise does not aggregate into full authority. What aggregates here is **coverage**, and
coverage is checked dimension by dimension against the trigger conditions that fired.

## Reviewer Instance Segregation

**`SEGREGATION_REQUIRED`.** This Profile is interdependent with `review.communication_strategy@0.1`
and with every domain review it composes. A Role instance that satisfied a domain review may
contribute the same dimension here only where its eligibility row permits **and** it was not the
producer of the conclusion under review. The producing instance of the communication Role is
segregated absolutely; a different instance may act as the bounded communication contributor.

## Review Dependencies

| Prerequisite `review.<id>` | Required status | Activation condition | Bounded purpose |
|---|---|---|---|
| `review.communication_strategy@0.1` | `SATISFIED` | Always | Communication quality is established before composition is checked |
| `review.legal_compliance` | `SATISFIED` | Legal exposure, admission or dispute in scope | Establish the legal position |
| `review.institutional_position` | `SATISFIED` | The draft states or implies an institutional position | Establish the position |
| `review.data_protection` | `SATISFIED` | Personal data disclosed | Establish lawful basis |
| `review.evidence_integrity_provenance` | `SATISFIED` | The draft carries a chronology or contested record | Establish record integrity |
| `review.factual_evidence` | `SATISFIED` | Contested facts asserted | Establish the factual basis |
| `review.commercial_claims` | `SATISFIED` | A commercial claim is made | Establish the claim basis |

An unsatisfied, `STALE` or missing prerequisite makes this review `REVIEW_BLOCKED`, not failed.
Satisfaction is not transitive: a satisfied legal review does not satisfy this one, and this one
does not satisfy any of them. Self-dependency and cycles are prohibited and none exists.

## Reviewer Prohibitions

- the producing instance of the communication Role, absolutely;
- any instance that produced a conclusion, for the dimension covering that conclusion;
- the human who will hold the transmission Decision Right for this subject — otherwise the last
  independent check and the decision collapse into one person;
- any Role with no eligibility row above;
- any reviewer for a dimension whose trigger did not fire — coverage is scoped, not general.

## Review Scope

### Checks
- **coverage**: every domain the draft materially touches has a current, satisfied domain review or
  an explicit recorded finding that none is required, with the reason;
- **integrity of carried conclusions**: each is present at its version and unchanged in meaning;
- **gate identification**: the applicable `decision.<id>` is named, matches the act the message
  actually performs, and is bound to this draft version, audience, channel and timing;
- **fail-closed handling**: where no Right resolves, the block is recorded with posture
  `AUTHORITY_ABSENT` and escalated, and the draft is not presented as sendable;
- **irreversibility**: the reversibility classification after the transmitting act is stated and
  correct, and any correction path is described honestly as a new act rather than an undo;
- **disclosure scope**: the audience is not wider than the material's own label permits, and
  privileged material is not circulated into a wider audience;
- **constraint compliance**: nothing in the `must_not_admit` set appears, and no reservation of
  rights has been dropped;
- **timing**: the approval window and the message's own deadline are consistent.

### Does Not Check
- the communication quality of the draft — `review.communication_strategy@0.1` covers it;
- the legal position — `review.legal_compliance`;
- the institutional position — `review.institutional_position`;
- lawful basis — `review.data_protection`;
- record provenance — `review.evidence_integrity_provenance`;
- factual truth — `review.factual_evidence`;
- commercial claim substantiation — `review.commercial_claims`;
- whether the message should be sent — a `decision.<id>`, not a review;
- whether the risk of sending is acceptable — `decision.risk_acceptance`, a human authority.

This "Does Not Check" list is long on purpose: this Profile is the one most at risk of becoming a
mega-review, because it is the last thing between a draft and the world.

## Method at Architecture Level

A composition and coverage examination. The reviewer works from the trigger conditions that fired
to the reviews and conclusions that should therefore exist, and reports what is missing. It
re-performs no domain analysis; re-performing one would both duplicate the domain review and
create an unowned second opinion.

## Finding Taxonomy Application

| Class | What it looks like here |
|---|---|
| `NO_FINDING` | Every triggered dimension is covered, every conclusion is intact, the gate is correctly identified |
| `OBSERVATION` | The approval window is tighter than necessary; the correction path could be stated more explicitly |
| `MINOR_FINDING` | A domain review is satisfied but its version citation is imprecise |
| `MAJOR_FINDING` | A triggered domain has no review and no recorded reason; the audience is wider than the previous approval assumed; the reversibility classification is understated |
| `CRITICAL_FINDING` | A carried conclusion has changed in meaning; the identified Right does not match the act performed; no Right resolves and no block was recorded; privileged material would be circulated without a basis; a `must_not_admit` item appears in the text; the draft is presented as ready to send with a prerequisite unsatisfied |

## Satisfaction Criteria

`SATISFIED` requires: the evidence package complete; every triggered prerequisite `SATISFIED` and
not `STALE`; every triggered dimension covered by an eligible bounded contributor; no unresolved
`CRITICAL_FINDING`; and every `MAJOR_FINDING` closed — **`MAJOR_FINDING`s may not be carried open
under this Profile**, because the act it precedes is costly to reverse or irreversible.

**Satisfaction is not approval, and is emphatically not permission to send.** It does not exercise
the transmission Right, does not create one where none exists, and does not convert a recorded
`AUTHORITY_ABSENT` block into a permission. An unresolved `CRITICAL_FINDING` can never be
satisfied, and no Decision Right may set this review to `SATISFIED`.

## Rework and Closure Requirements

| Finding class | Rework destination | Evidence to close |
|---|---|---|
| `OBSERVATION` | Optional | Recorded |
| `MINOR_FINDING` | Producer | Corrected citation |
| `MAJOR_FINDING` | Producer, and the missing domain's owning Role | The missing review `SATISFIED`, or a recorded reasoned finding that none is required |
| `CRITICAL_FINDING` | Producer, the owning Role, and governance where the gate was misidentified | The corrected artifact, the owning Role's confirmation, and the corrected gate identification or recorded block |

Preserved across closure: the original draft version, every finding, the coverage map at the time
of the finding, and the full revision history.

## Re-Review Triggers

`STALE` on: any text change; any change of audience, recipient set, channel or timing beyond the
stated window; supersession of any carried conclusion; any new material message in the thread; a
rise in the stakes band; a change in the constraint set; expiry of any prerequisite review; and any
change to the identified Decision Right or its holder.

## Criticality Scaling

This Profile applies only in high-stakes settings and its independence class does not vary. What
deepens at `CRITICAL`: every carried conclusion must be `APPROVED` rather than `REVIEWED`; the
coverage map must be explicit rather than inferable; and the gate identification must name the
holder eligibility class, not only the Right. Criticality changes depth, not review identity.

## Workflow / Handoff References

- `workflow.communication_difficult_interaction_response@0.1` S10 — `REVIEW_REQUIRED_REFERENCE`,
  immediately before the S11 gate
- `workflow.communication_formal_escalation@0.1` S5 — mandatory at every band

Any Handoff transferring a Draft Communication toward a transmitting act requires this review
`SATISFIED` before transfer, where its trigger fired.

## Decision Right Boundary

This review **informs** the transmission Right resolved by `decision-right-gap-analysis.md` §4 and
**neither exercises nor satisfies it**. Its most important single output is often the finding that
**no applicable Right exists** — in which case the correct outcome is a recorded fail-closed block
with posture `AUTHORITY_ABSENT`, escalated to governance, and **not** a satisfied review that lets
the message through on the grounds that nothing forbade it.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter independence class, severity
application, the no-carried-`MAJOR_FINDING` rule, or satisfaction semantics.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer
assignment, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
