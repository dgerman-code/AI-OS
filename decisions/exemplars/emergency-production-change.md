# Emergency Production Change

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Emergency Production Change
- Decision ID: `decision.emergency_production_change`
- Version: 0.1
- Status: PROPOSED
- Decision Family: Emergency / Exception
- Decision Class: `EMERGENCY_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

## Decision Subject

**One** time-critical production change, at a stated version, addressing **one** declared active incident, under emergency conditions.

The scope is deliberately doubly bounded — one change, one incident. An emergency Right whose subject is "whatever the incident requires" is not an emergency Right; it is standing authority with an excuse attached.

## Decision Effect

The change goes live under reduced prerequisites, with a time limit and a **debt** — a retrospective obligation the entity owes and has not yet discharged.

## Objective Emergency Trigger

**All four must hold**, and each is objectively testable after the fact:

1. an **active** production incident is declared — degradation, outage, data-integrity failure, or an actively exploited security condition;
2. the impact is **ongoing**, not anticipated;
3. the normal `decision.production_release` path **cannot complete before material further harm** occurs;
4. the change is **directed at the incident**, not at unrelated work travelling alongside it.

A deadline is not an emergency. A release date is not an emergency. Discovering late that normal preparation was not done is not an emergency — it is the absence of preparation, and using this Right for it is a misuse recorded as such.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE_WITH_CONDITIONS` | Emergency path only | n/a | **Change live under emergency conditions** | **Unchanged — skipped reviews remain skipped and open** | None | Every bypassed prerequisite **becomes an open item**; the retrospective obligation is a condition | **Mandatory, short** |
| `REJECT` | Blocked; the incident is handled another way | n/a | None | Unchanged | None | Retained | n/a |

**`APPROVE` without conditions is not permitted.** An emergency change always carries at least the retrospective obligation, so there is no unconditional form of this decision.

## What may be bypassed, and what may never be

| May be bypassed under this Right | Never bypassable |
|---|---|
| The normal `decision.production_release` gate | **Law and regulation** — including breach-notification obligations, which are triggered by the incident and not suspended by responding to it |
| Full `review.test_coverage` against every acceptance criterion | The requirement that a **human eligible under this Right** decides — an automated or agent-initiated change is never an emergency decision |
| Full `review.security` where the change is confined to the incident surface | The **retrospective obligation** |
| The normal change-scope prerequisites | The **record**: an undocumented emergency change is not an authorised one |
| Non-incident work in the same change set — this is bypassed by **exclusion**, not by permission | Data-protection obligations arising from the incident itself |

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `FUNCTIONAL_AUTHORITY` | Named **emergency** release authority for the production environment, designated **in advance** | Designation in advance is what makes this authority rather than improvisation |
| `EXECUTIVE_AUTHORITY` | Where the incident carries regulatory, safety or material reputational exposure | Beyond the technical function's remit |

**The authority must be designated before the incident.** A person who would be an obvious choice, but was not designated, is not eligible — that is the whole difference between emergency authority and the absence of authority under pressure.

`role.platform_devops_engineer` and `role.security_engineer` are not eligible by virtue of their operational capability, however well placed they are to act.

## Cardinality

`SINGLE_HOLDER` — deliberately, because a multi-holder requirement in an active incident produces either delay or theatre. The compensating control is not a second decider at the moment; it is the **mandatory retrospective step**, where the scrutiny actually occurs.

## Delegation Policy

**`NON_DELEGABLE`.**

Emergency authority is already an exception. Delegating it would produce an exception to an exception with no one carrying the consequence. Where cover is needed, a **second holder is designated in advance** — which is designation, not delegation.

## Revocation and Supersession

Revocation ends future exercise and reverses nothing already done. The emergency change is superseded when the permanent fix is released under `decision.production_release`; the emergency record stands. **Retrospective review does not amend this decision** — it produces its own record assessing it.

## Prerequisites

Reduced but not absent: the incident is **declared**; the trigger conditions are stated; the change is confined to the incident; the rollback position is stated or its absence explicitly recorded; and the eligible authority was designated before the incident.

## Workflow / Handoff / Review References

`workflow.software_change_delivery` emergency exception path; `workflow.incident_response_and_recovery`; informed by `review.security` — which **remains unsatisfied** through and after the emergency change.

## Required Evidence

Beyond the generic eighteen, all mandatory at exercise time: the incident identifier and declaration; each of the four trigger conditions and how it was met; **every prerequisite bypassed, enumerated** — an unenumerated bypass is unauthorised; the change scope and its confinement to the incident; the rollback position; the time limit claimed; and the retrospective obligation with its due point.

## Open Item, Finding and Risk Handling

**Every bypassed prerequisite becomes an open item at the moment of decision**, classified `MATERIAL_TO_NEXT_STEP_OR_GATE`, and is carried until separately discharged. A skipped review is `NOT_SATISFIED` and stays so; **emergency use satisfies nothing retroactively.**

The emergency change leaves the system in a **known-degraded governance state**, and the register says so until the debt is paid.

## Expiry / Re-Decision Trigger

**Mandatory short expiry** covering the emergency change only. The permanent fix goes through the normal path. Where the emergency change is still live at expiry, the position **escalates** rather than lapsing quietly — an expired emergency change that nobody normalised is itself a finding.

## Exceptional Progression Rule

This Right **contains** its own exception and does not use `decision.exceptional_progression`. All eight architecture §10 conditions apply: bypassed prerequisites stay open and named, review statuses are unchanged, conditions and consequences are recorded, expiry is declared, and the decision does not claim any bypassed thing was done.

## Risk / Waiver Boundary

Accepts **no** risk formally — residual risk from the emergency change requires `decision.security_risk_acceptance` separately, in the retrospective step where it can actually be assessed. **Waives no review**: reviews are bypassed for the moment, which is not waiver, and each remains owed. **Cannot waive law or regulation**, and specifically cannot suspend a breach-notification obligation that the incident itself triggered.

## Emergency Rule

Stated in full above. Two rules bear repeating: **urgency is not authority**, and **use does not create standing authority.** A team exercising this Right monthly has not acquired ordinary release authority; it has a pattern that the retrospective process should be surfacing as a finding about the normal path.

## Knowledge-State Effect

**None.**

## Out-of-Scope Authority

This Right does **not**: authorise non-incident work in the same change set; satisfy, relabel or retroactively excuse any review; accept security risk; accredit anything; waive a breach-notification or other regulatory obligation; authorise a production database migration not required by the incident; become standing release authority; or extend to a second incident.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
