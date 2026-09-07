# Workflow Card Template

Status: PROPOSED — Phase 5 standard candidate
Template Version: 0.1
Inherits: `standard.workflow.common_constraints@0.1`

Every Workflow Card uses this structure. Sections are mandatory unless marked optional. A section that does not apply is filled with an explicit "None" and a reason, never deleted — an absent section is indistinguishable from an overlooked one.

---

## Identity
- Workflow Name:
- Workflow ID: `workflow.<stable_snake_case_name>`
- Version:
- Status: PROPOSED
- Workflow Family:
- Governance Owner:
- Criticality Applicability: which bands of `architecture/project-criticality-policy.md` this pattern serves
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes:
- Superseded By:

## Purpose

What coordination problem this pattern solves, in two or three sentences. Not a description of the work itself — a description of why the work needs coordinating across Roles.

## Trigger

`TRIGGER` — the condition that makes this Workflow applicable. State the condition, not the calendar.

## Preconditions

`PRECONDITION` — what must already exist or be true before the Workflow may start. Include required knowledge states of inputs.

## Scope
### Covers
### Does Not Cover

The "Does Not Cover" list is where authority boundaries are made visible. Name the conclusions, decisions and artifacts this Workflow coordinates *around* but never owns.

## Participating Roles

| Role ID | Participation | Stage(s) | Authority boundary note |
|---|---|---|---|

Participation is one of `LEAD_ROLE`, `CONTRIBUTING_ROLE`, `CONSULTED_ROLE`. The two reference types — `REVIEW_REQUIRED_REFERENCE` and `HUMAN_GATE_REFERENCE` — are **not** Role participation and are recorded against stages, not in this table.

The authority boundary note states what the Role does **not** gain by participating. A blank note is a defect.

## Activated Skills / Packs

References only. Mapping eligibility remains governed by Phase 4: a Workflow cannot make a Role compatible with a Skill that Phase 4 does not allow. Cite the capability and the Role it attaches to, and confirm the Phase 4 basis is direct or transitive.

| Capability ID | For Role | Phase 4 basis |
|---|---|---|

## Inputs

Artifacts, evidence and context the Workflow consumes, with the knowledge state each must hold.

## Stages

For each Stage, in order (state explicitly where stages may run in parallel):

### Stage `S<n>` — <name>
- **Stage ID:**
- **Objective:** why this stage exists, distinct from every other stage
- **Entry Criteria:** what must be true to enter, including `STATE_EXPECTATION` on inputs
- **Participating Roles:** role IDs with participation type
- **Activities:** `ACTIVITY` items, each within a participating Role's own scope
- **Artifact Contributions:** `ARTIFACT_CONTRIBUTION` items — which Role-owned artifact each contribution goes to, and who owns it
- **Knowledge-State Expectations:** `STATE_EXPECTATION` — states expected on entry and on exit, with an explicit note that the Workflow does not itself promote them
- **Gate / Review References:** `GATE_REFERENCE` — `decision.<id>` and `review.<id>` pointers that may block progression
- **Exit Criteria:** testable conditions for leaving the stage
- **Possible Outcomes:** the subset of `COMPLETE` / `COMPLETE_WITH_OPEN_ITEMS` / `BLOCKED` / `REWORK_REQUIRED` / `ESCALATED` / `CANCELLED` that can occur here

## Branches / Exception Paths

`BRANCH` — conditional divergences, each with its condition stated.
`EXCEPTION_PATH` — what happens when the normal path cannot proceed, including where it escalates to.

State explicitly that no exception path bypasses a gate or review reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` — which stages can be returned to, on what condition, and what provenance and prior state history is preserved across the loop.

## Completion Criteria

`COMPLETION_CRITERION` — what makes this Workflow complete. Complete is a coordination position, never an approval; say so.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — what causes the Workflow to stop without completing, and what survives cancellation.

## Outputs / Resulting Artifact States

What exists at the end and in which knowledge state, with ownership attributed to the owning Role in every case.

## Authority / Review Boundary

The explicit statement of what this Workflow does not do: which conclusions it does not own, which decisions it does not make, which reviews it does not perform or satisfy, and which artifact ownership it does not alter. This section is not boilerplate — it is written against this specific Workflow's real leakage risks.

## Criticality Scaling

How the pattern deepens across criticality bands: which stages become mandatory, which Roles become required rather than consulted, which reviews and gates are added, and how evidence and traceability requirements tighten. State explicitly that criticality changes depth, not Role identity, and does not create a second Workflow.

## Evidence / Traceability Requirements

What must be traceable at completion: source linkage, assumption register, calculation provenance, open items, gate records and rework history.

## Versioning / Change Control

Version history, and confirmation that no version change silently altered authority, Role scope, gate references or artifact ownership.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
