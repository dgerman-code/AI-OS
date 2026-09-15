# Communication Strategy Review — Review Profile Candidate

Status: `PROPOSED`
Template: Review Profile Card Template (Phase 6 standard candidate)
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: **Communication Strategy Review**
- Review ID: `review.communication_strategy@0.1`
- Version: 0.1 · Status: PROPOSED
- Review Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Establish that a communication strategy and the draft implementing it are professionally fit for
purpose from a difficult-conversation and communication-control perspective: that the objective is
served, the facts are disciplined, the boundary holds, nothing material is conceded, and the
escalation posture is proportionate. It supports reliance on the **communication** quality of the
artifact and on nothing else.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.communication.communication_strategy` | `role.communication_difficult_conversations_specialist` *(candidate)* |
| `artifact.communication.draft_communication` | as above |
| `artifact.communication.interaction_brief` | as above |
| `artifact.communication.escalation_recommendation` | as above |
| `artifact.communication.conversation_diagnostic` | as above |

The owning Role is the producer and is by definition ineligible to satisfy this review, since the
independence class below is never `PRODUCER_REVIEW`.

## Applicability / Trigger

**The trigger is Rule RC-5 of `role-card.md`, and this Profile restates no variant of it.** An
earlier revision stated the condition here and a narrower one in the Role Card and workflows —
mandatory whenever another Role's conclusion was carried or a consequential boundary was stated,
against mandatory at high and critical stakes only. Two rules meant the fail-closed one was
reachable only by a reader who happened to open this document, and the gap fell exactly where it
mattered: a low-stakes message can carry a legal conclusion.

Required where **any** RC-5 condition holds:

| RC-5 condition | Here |
|---|---|
| **RC-5.1** stakes `HIGH` or `CRITICAL` | Includes `high_stakes_communication = true` (`trigger-routing-spec.md` §5) |
| **RC-5.2** the draft carries or reformulates another Role's substantive conclusion | Regardless of stakes |
| **RC-5.3** the draft states a consequential boundary, refusal, escalation, commitment, concession, deadline, admission-sensitive position or institutional position | Regardless of stakes |
| **RC-5.4** a workflow-specific mandatory condition applies | A formal escalation is mandatory at **every** band (`workflow-formal-escalation.md` S5) |

Advisory **only** where none of the four holds — routine low- or medium-stakes communication
carrying no other Role's conclusion and stating no consequential position. Advisory means the
review may be performed and its findings recorded; it never means its findings may be ignored
once made, and it never lowers this Profile's independence class.

## Required Evidence Package

- the interaction record with per-message provenance;
- the Conversation Diagnostic, including the triage table and its reasons;
- the Communication Strategy, including the rejected postures and why;
- the draft under review, at an identified version;
- every substantive conclusion the draft carries, cited at its version and owner;
- the constraint set in force (`must_not_admit`, reservations, mandate limits);
- the Communication Control Filter component scores and the rubric version.

An incomplete package produces `REVIEW_BLOCKED`, not a finding. In particular, a draft submitted
without the conclusions it carries cannot be reviewed: the reviewer cannot tell whether a
conclusion moved.

## Independence Class

`PEER_REVIEW` at `LOW` and `MEDIUM`.
**`CROSS_DOMAIN_REVIEW` at `HIGH`.**
**`INDEPENDENT_ASSURANCE_REVIEW` at `CRITICAL`**, and for every formal escalation regardless of
band.

The class rises because the failure this review exists to catch — a well-written message that has
quietly moved someone's position — is least visible to someone inside the same work.

## Reviewer Eligibility

| `role.<id>` | Eligibility class | Scope basis in its Role Card | Dimension covered |
|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate, different instance)* | `FULL_PROFILE_REVIEWER_ELIGIBLE` | Its `Owns` list covers every satisfaction criterion below | All dimensions |
| `role.institutional_communications_editorial_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns editorial standards and institutional voice | Clarity, register, institutional tone |
| `role.institutional_affairs_stakeholder_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns institutional stakeholder positioning | Relationship risk, escalation proportionality |
| `role.people_organisation_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns people-matter conclusions | Boundary quality and escalation posture in employment matters |
| `role.legal_regulatory_lead` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns legal conclusions | Whether the draft makes an admission or waives a right — **it does not cover communication quality** |
| `role.knowledge_evidence_steward` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns evidence provenance | Factual discipline and source linkage |

**Partial expertise does not aggregate into full authority.** Four bounded contributors do not
between them satisfy this Profile; a `FULL_PROFILE_REVIEWER_ELIGIBLE` reviewer is required for
satisfaction, and the bounded rows cover named dimensions only.

Eligibility must be checkable against the Role Card, the producing assignment and the Workflow
participation record.

## Reviewer Instance Segregation

**`SEGREGATION_REQUIRED`.** A Role instance that contributed a substantive conclusion at S6 of
`workflow-difficult-interaction-response.md` must not review the same dimension it contributed —
it would be checking whether its own conclusion survived the phrasing. It may review a different
dimension where its eligibility row permits.

The producing instance of the communication Role is segregated absolutely.

## Review Dependencies

| Prerequisite `review.<id>` | Required status | Activation condition | Bounded purpose |
|---|---|---|---|
| `review.factual_evidence` | `SATISFIED` | The draft asserts contested facts about events | Establish the factual basis before communication quality is assessed |
| `review.legal_compliance` | `SATISFIED` | The draft touches a legal position, admission or reservation | Establish the legal position; this Profile does not assess it |

An unsatisfied, `STALE` or missing prerequisite makes this review `REVIEW_BLOCKED`, not failed.
Satisfaction is not transitive and the dependency transfers nothing. Self-dependency and cycles are
prohibited and none exists.

## Reviewer Prohibitions

- the producing instance of `role.communication_difficult_conversations_specialist`, absolutely;
- any instance that contributed a substantive conclusion the draft carries, for that dimension;
- any human holding the Decision Right that will gate the transmission, where they would then be
  both the reviewer and the decider on the same subject;
- any Role with no eligibility row above, at any dimension.

## Review Scope

### Checks
- the stated objective is coherent and the draft serves it;
- facts asserted are traceable to the record or to an approved source, and placeholders are
  present rather than invented values;
- assumptions and reconstructions are labelled;
- issue triage is reasoned and the `IGNORE` classifications pass the materiality test;
- the boundary, where present, is self-directed and carries no unestablished consequence;
- acknowledgement does not read as concession;
- no material refusal, deadline, condition, reservation or evidence point has been softened;
- brevity does not remove something load-bearing;
- escalation posture is proportionate to the record;
- optionality is preserved — no unnecessary admission, promise or characterisation;
- pattern labels are hedged, observable-behaviour based, and describe no person;
- the non-response and delay options were genuinely evaluated;
- required adjacent reviews and the human gate are named, and the draft does not present itself as
  ready to send where they are unsatisfied.

### Does Not Check
- whether the underlying facts are true — `review.factual_evidence`;
- the legal position, admissions or reservations — `review.legal_compliance`;
- the institutional position stated — `review.institutional_position`;
- lawful basis for disclosing personal data — `review.data_protection`;
- the financial or commercial substance — `review.financial_evidence`, `review.commercial_claims`;
- the technical substance — `review.engineering_technical`;
- provenance integrity of the record itself — `review.evidence_integrity_provenance`;
- whether the communication should be sent — that is a `decision.<id>`, not a review.

## Method at Architecture Level

A comparative examination: the reviewer reads the record, the diagnostic and the draft together,
and tests whether the draft's claims, concessions and omissions are each supported by the record
and by the cited conclusions. It is not a checklist run and not a style pass; the central question
is *what does this draft commit us to that the record does not already commit us to?*

## Finding Taxonomy Application

| Class | What it looks like here |
|---|---|
| `NO_FINDING` | The draft serves the objective, concedes nothing unsupported, and its omissions are reasoned |
| `OBSERVATION` | A sentence could be shorter; a closing line is warmer than necessary |
| `MINOR_FINDING` | An unlabelled assumption; a reason that adds attack surface without adding clarity |
| `MAJOR_FINDING` | An acknowledgement that reads as concession; a boundary stated as a command; a non-material accusation answered at length; the non-response option not evaluated |
| `CRITICAL_FINDING` | A carried conclusion changed in meaning; an invented fact, date or quotation; a softened material protection; an unestablished consequence stated as available; a psychological characterisation; a draft presented as ready to send with a required gate unsatisfied |

## Satisfaction Criteria

`SATISFIED` requires: the evidence package complete; every prerequisite review `SATISFIED` and not
`STALE`; no unresolved `CRITICAL_FINDING`; and every `MAJOR_FINDING` either closed or explicitly
carried under a named external human Decision Right that permits progression with it open.

**Satisfaction is not approval.** It does not authorise transmission, does not exercise any
Decision Right, does not promote the draft beyond `REVIEWED`, and does not attest that the
underlying facts are true. An unresolved `CRITICAL_FINDING` can **never** be satisfied, under any
band, by any authority, and no Decision Right may set this review to `SATISFIED`.

## Rework and Closure Requirements

| Finding class | Rework destination | Evidence to close |
|---|---|---|
| `OBSERVATION` | Optional | None; recorded |
| `MINOR_FINDING` | Producer, S8 of the parent Workflow | Revised text |
| `MAJOR_FINDING` | Producer, S7 or S8 | Revised strategy or text, plus the reasoning that addresses the finding |
| `CRITICAL_FINDING` | Producer, and the owning Role where a conclusion moved | The corrected artifact **and** the owning Role's confirmation that its conclusion is intact |

Preserved across closure: the original draft version, the finding, the reasoning, and the revision
history. Nothing is overwritten.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: the draft text changes; the audience or channel changes;
any carried conclusion is superseded; a new material message arrives in the thread; the stakes band
rises; or the constraint set changes.

## Criticality Scaling

`LOW`/`MEDIUM`: `PEER_REVIEW`; the evidence package may cite conclusions by reference.
`HIGH`: `CROSS_DOMAIN_REVIEW`; every carried conclusion must be supplied at its version, not merely
cited. `CRITICAL`: `INDEPENDENT_ASSURANCE_REVIEW`; the reviewer must additionally confirm the
gate identification and that the producer did not present the draft as ready to send.
**Criticality changes depth, not review identity.**

## Workflow / Handoff References

- `workflow.communication_difficult_interaction_response@0.1` S10 — `REVIEW_REQUIRED_REFERENCE`
- `workflow.communication_meeting_preparation@0.1` S6
- `workflow.communication_boundary_setting@0.1` S4
- `workflow.communication_refusal@0.1` S5
- `workflow.communication_formal_escalation@0.1` S5

Any Handoff transferring a Draft Communication for transmission requires this review `SATISFIED`
before transfer.

## Decision Right Boundary

This review **informs** the applicable transmission Right resolved by
`decision-right-gap-analysis.md` §4. That resolution does not branch on publicity: **any release
of a content item outside the entity under the entity's name resolves
`decision.external_publication`**, whether the audience is the public or one named recipient.
Submission, disclosure, transmission and commitment Rights apply **in addition** where the act is
also one of those things, never instead of the release Right because the communication happens to
be private (DG-1, DG-2, DG-3).

It **neither exercises nor satisfies** that Right. A satisfied communication review is an input a
decider may rely on; it is not the decision, and no combination of satisfied reviews substitutes
for one.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter independence class, severity
application or satisfaction semantics.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer
assignment, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
