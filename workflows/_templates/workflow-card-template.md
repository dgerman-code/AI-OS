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

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|

Participation is one of `LEAD_ROLE`, `CONTRIBUTING_ROLE`, `CONSULTED_ROLE`. The two reference types — `REVIEW_REQUIRED_REFERENCE` and `HUMAN_GATE_REFERENCE` — are **not** Role participation and are recorded against stages, not in this table.

**Activation is a separate column, not a participation type**: `ALWAYS` or `CONDITIONAL(<objective trigger>)`. A Role that produces an owned artifact only when a trigger applies is `CONTRIBUTING_ROLE` with `Activation: CONDITIONAL(...)` — never `CONSULTED_ROLE` on the grounds that it is conditional. `CONSULTED_ROLE` means the Role owns and advances nothing in that Stage.

The authority boundary note states what the Role does **not** gain by participating. A blank note is a defect.

### Parameterized Role Slots

Governed by the **Role Slot Binding Rule** (`architecture/workflow-registry-design.md` §4, `standard.workflow.common_constraints` §14D). Complete only where the pattern declares a slot instead of a concrete Role. Omit the section entirely for Workflows with no slots; do not leave it as an empty placeholder.

| Slot | Allowed source | Required ownership / interface condition | Permitted participation | Required artifact-ownership relationship | Phase 4 capability validation | Cardinality |
|---|---|---|---|---|---|---|

Wildcards are prohibited. A slot cannot grant ownership — the bound Role must already own the relevant artifact or conclusion. A slot cannot bind a System Control Profile, Review Profile, Decision Right, model or runtime identity. Where no approved Role satisfies the constraints, the instance is `BLOCKED` or invalid; the slot is not widened.

## Composed Workflow References

`WORKFLOW_REFERENCE` entries. Omit the section entirely where the Workflow composes nothing; a Workflow that does not cleanly compose a candidate child says so rather than forcing a reference.

| Referenced Workflow | Version / reference policy | Bounded purpose | Expected inputs | Expected outputs | Parent Stage(s) | Activation |
|---|---|---|---|---|---|---|

A reference is declarative: it names a child pattern, it does not execute it. It transfers no Role ownership, Skill compatibility, review identity, Decision Right, gate or knowledge-state authority. Where the parent relies on an output the child produces only past a child gate or review, state that dependency here — it may not be silently dropped. Self-reference, direct or transitive, is a registry defect.

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
- **Open-Item Materiality:** which open items this Stage may carry as `NON_MATERIAL_TO_NEXT_STEP`, and which classes of item are `MATERIAL_TO_NEXT_STEP_OR_GATE` here and therefore cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit

## Branches / Exception Paths

`BRANCH` — conditional divergences, each with its condition stated.
`EXCEPTION_PATH` — what happens when the normal path cannot proceed, including where it escalates to.

State explicitly that no exception path bypasses a gate or review reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` — which stages can be returned to, on what condition, and what provenance and prior state history is preserved across the loop.

## Open-Item Materiality

State which open items are `MATERIAL_TO_NEXT_STEP_OR_GATE` for this Workflow's terminal gate, and confirm that a material item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit — the outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED` unless a **named external human Decision Right** explicitly permits progression with that item still unresolved. Where that exception applies, the gate reference is recorded and the item stays open; the Workflow neither decides the waiver nor asserts it was granted.

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
