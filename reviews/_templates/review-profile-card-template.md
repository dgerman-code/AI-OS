# Review Profile Card Template

Status: PROPOSED — Phase 6 standard candidate
Template Version: 0.1
Inherits: `standard.review.common_constraints@0.1`

Every Review Profile Card uses this structure. Sections are mandatory. A section that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Review Name:
- Review ID: `review.<stable_snake_case_name>`
- Version:
- Status: PROPOSED
- Review Family:
- Governance Owner:
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By:

## Purpose

Why this review exists and what reliance it supports. Two or three sentences.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|

The owning Role is the producer. It is by definition ineligible to satisfy this review where the independence class is not `PRODUCER_REVIEW`.

## Applicability / Trigger

The objective condition under which this review is required, and the criticality bands in which it is mandatory rather than advisory.

## Required Evidence Package

What must be available for the review to proceed. An incomplete package produces `REVIEW_BLOCKED`, not a finding.

## Independence Class

One of `PRODUCER_REVIEW`, `PEER_REVIEW`, `CROSS_DOMAIN_REVIEW`, `INDEPENDENT_ASSURANCE_REVIEW`, with the criticality band at which a higher class becomes required.

## Reviewer Eligibility

Which approved `role.<id>` may satisfy this review, and the ownership or competence condition each must meet. Eligibility must be checkable against the producing assignment and Workflow participation.

## Reviewer Prohibitions

Who may **not** satisfy it, and why. At minimum the producer of the subject in the same assignment instance. A blank prohibition list is a defect.

## Review Scope
### Checks
### Does Not Check

The "Does Not Check" list names the neighbouring `review.<id>` that covers what this one does not. This is where mega-review creep is prevented.

## Method at Architecture Level

What kind of examination this is — not a procedure, not a checklist instance, not an SOP.

## Finding Taxonomy Application

How `NO_FINDING` / `OBSERVATION` / `MINOR_FINDING` / `MAJOR_FINDING` / `CRITICAL_FINDING` apply to this subject, with an example of what would constitute each here.

## Satisfaction Criteria

What makes this review `SATISFIED`. Must state explicitly that satisfaction is not approval, that an unresolved `CRITICAL_FINDING` can never be satisfied, and how unresolved `MAJOR_FINDING`s are treated.

## Rework and Closure Requirements

Rework destination by finding class; the evidence required to close each; and what is preserved across closure.

## Re-Review Triggers

What material change to the subject makes a prior satisfaction `STALE`.

## Criticality Scaling

How independence class, evidence depth and finding-closure rigour change by band. Must state that criticality changes depth, not review identity.

## Workflow / Handoff References

Which Phase 5 Workflow stages carry this as a `REVIEW_REQUIRED_REFERENCE`, and which Handoffs require it `SATISFIED` before transfer.

## Decision Right Boundary

Which `decision.<id>` this review informs and does not make. Must state that the review neither exercises nor satisfies it.

## Versioning / Change Control

Version history, with confirmation that no version change silently altered independence, severity application or satisfaction semantics.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
