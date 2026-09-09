# Decision Right Card Template

Status: PROPOSED — Phase 7 standard candidate
Template Version: 0.1
Inherits: `standard.decision.common_constraints@0.1`

Every Decision Right Card uses this structure. Sections are mandatory; a section that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Decision Name:
- Decision ID: `decision.<stable_snake_case_name>`
- Version:
- Status: PROPOSED
- Decision Family:
- Decision Class: one of `PROGRESSION_DECISION` / `APPROVAL_DECISION` / `COMMITMENT_DECISION` / `RISK_ACCEPTANCE_DECISION` / `EXCEPTION_DECISION` / `EMERGENCY_DECISION` / `REJECTION_DECISION` / `CANCELLATION_OR_TERMINATION_DECISION`
- Governance Owner:
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By:

## Decision Subject

What this Right decides **about**, bounded. Name the artifact, act or transition. "The project" is not a subject.

## Decision Effect

What deciding **does**, bounded. State the change in the world that the decision produces.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action / commitment | Review status | Knowledge state | Conditions / open items | Expiry / re-decision |
|---|---|---|---|---|---|---|---|

Not every Right permits every outcome. An outcome listed without its effects is a defect. **No outcome may set a Review to `SATISFIED`.**

## Holder Eligibility

| Eligibility class | Authority basis required | Why this class and not a lesser one |
|---|---|---|

Eligibility is authority-based, not competence-based. Role competence, Workflow leadership, reviewer status and artifact ownership each confer nothing here.

## Cardinality

`SINGLE_HOLDER` / `MULTI_HOLDER_ALL_REQUIRED` / `MULTI_HOLDER_THRESHOLD` / `GOVERNANCE_BODY_DECISION`, with threshold semantics stated declaratively where used. One person cannot count twice under two labels.

## Delegation Policy

`NON_DELEGABLE` / `DELEGABLE_WITHIN_ELIGIBILITY` / `DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`, with: who may delegate; who may receive; scope; time and context limits; re-delegation (prohibited by default); evidence required; revocation semantics.

## Revocation and Supersession

How holder or delegation revocation, decision supersession and — where permitted — decision reversal operate here. State explicitly that revocation does not erase historical decisions and that correction uses a new linked Record.

## Decision Right Separation (`DECISION_RIGHT_SEPARATION`)

Relationship-level separation of duties against **other** Decision Rights. One row per relationship; **None** with a reason where the Right has no separated counterpart.

| Related `decision.<id>` | Objective activation condition | Mode | Bounded subject / context | Reason |
|---|---|---|---|---|

Mode is `SEPARATION_REQUIRED` or `SAME_HOLDER_PERMITTED`. The related Right must be a **concrete `decision.<id>`** in this registry — a category or description is not a relationship, and an activation condition that is not objectively testable is a defect.

Where the mode is `SEPARATION_REQUIRED`, the same human instance must not exercise both Rights for the same governed subject or context in the same decision chain. Eligibility is evaluated per Right; **two eligibility classes, delegation and within-Right cardinality each fail to bypass this.** `SAME_HOLDER_PERMITTED` requires an explicit reason showing the independent-control purpose survives. This section declares no staffing, assignment or scheduling mechanism.

## Prerequisites

What must be true before this decision may validly be made, including any prerequisite `decision.<id>` with its required prior outcome, and any `review.<id>` and required status.

## Workflow / Handoff / Review References

Which Phase 5 Workflow gates, Phase 6 Handoff `DECISION_REFERENCE`s and Review Profiles point at this Right.

## Required Evidence

What the Decision Record must carry for this Right specifically, beyond the nineteen generic elements in `architecture/decision-rights-registry-design.md` §8.

## Open Item, Finding and Risk Handling

What happens to open findings, risks, assumptions, `UNKNOWN` and `CONFLICT_DETECTED` at and after this decision. They persist; state how they are carried.

## Expiry / Re-Decision Trigger

What makes a made decision stale, and what requires it to be taken again.

## Exceptional Progression Rule

Whether this Right may permit progression past an unresolved item or unsatisfied review, and under the eight conditions in the architecture §10 — or **None** with a reason.

## Risk / Waiver Boundary

What risk class this Right may accept, if any; what process requirement it may waive, if any; and what it may never do. **None** with a reason where it accepts and waives nothing.

## Emergency Rule

Objective trigger, bypassable prerequisites, never-bypassable prerequisites, time validity, retrospective obligation — or **None** with a reason.

## Knowledge-State Effect

Which governed state transitions, if any, this Right may support. `REVIEWED` is review-governed; `CANONICAL` requires distinct authority.

## Out-of-Scope Authority

What this Right explicitly does **not** authorise. This section is where the boundary is made testable; a blank one is a defect.

## Versioning / Change Control

Version history, with confirmation that no version change silently altered subject, effect, eligibility, cardinality or delegation policy.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
