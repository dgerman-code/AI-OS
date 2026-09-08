# Handoff — Project Definition to Technical Feasibility

Status: PROPOSED — Phase 6 exemplar Handoff Card
Inherits: `standard.handoff.common_constraints@0.1`

## Identity
- Handoff Name: Project Definition to Technical Feasibility
- Handoff ID: `handoff.project_definition_to_technical_feasibility`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.handoff.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

The first transfer in project preparation, and the one that sets the shape of everything downstream. If the definition arrives without its boundary conditions and assumptions, the feasibility work will silently invent them — and the invented basis will propagate into the cost estimate, the model and the readiness position with nobody owning it.

## Trigger

`HANDOFF_TRIGGER` — a project definition is stable enough to assess technically, and `workflow.project_development_readiness` S1 has exited.

## Sender Role(s)

`SENDER_ROLE` — `role.project_development_lead`.

**Retains after transfer:** ownership of `artifact.project_definition_document` and `artifact.project_development_plan`, and responsibility for maintaining the definition. Transfer moves no ownership.

## Receiver Role(s)

`RECEIVER_ROLE` — `role.technical_feasibility_lead`.

**Bounded next activity:** technical option comparison, design-basis definition and feasibility analysis against the transferred definition. The receiver gains nothing beyond its own Role Card, and specifically gains no cost-estimation ownership — `skill.lifecycle_cost_analysis` remains support-only under the approved Phase 4 record.

## Subject

`HANDOFF_SUBJECT` — `artifact.project_definition_document`, owned by `role.project_development_lead`, together with responsibility for the next bounded activity (feasibility assessment). No artifact ownership transfers.

## Required Package Contents

`HANDOFF_PACKAGE`:

1. `artifact.project_definition_document` at a stated version;
2. the boundary conditions and configuration the definition fixes;
3. the assumptions of record, each with a basis and a named owner;
4. `artifact.preparation_gap_register` — the gate-critical unknowns identified at S1;
5. `artifact.evidence_integrity_record` and `artifact.evidence_gap_conflict_report` from `role.knowledge_evidence_steward`;
6. the named forward gate and its evidence expectations;
7. the criticality band determination;
8. the sector or technology context where a sector Specialisation applies;
9. an explicit statement of what the definition does **not** fix.

Item 9 is the one most often omitted and the one that prevents the receiver from inventing a basis.

## Required Knowledge States

`STATE_REQUIREMENT`:

- `artifact.project_definition_document`: `DRAFT` minimum; **`REVIEWED` where the criticality band is Enhanced Decision-Grade or above**;
- assumptions: labelled `ASSUMPTION`, never presented as `FACT`;
- unverifiable inputs: `UNKNOWN`, present rather than omitted;
- sources: `SOURCE` with provenance.

This Handoff **does not promote any state**. It requires states; it does not create them.

## Provenance / Traceability Requirements

`PROVENANCE_REQUIREMENT` — version identity of the definition; source verification status for every fact it asserts; the traceability record linking definition elements to their basis; explicit flagging of any input already `SUPERSEDED`.

## Carried Open Items

`OPEN_ITEM_CARRY` — every unresolved item from S1, each classified per Phase 5 §14A:

- gate-critical unknowns that any downstream workstream will consume → `MATERIAL_TO_NEXT_STEP_OR_GATE`;
- unknowns relevant only to background context → `NON_MATERIAL_TO_NEXT_STEP`;
- any `CONFLICT_DETECTED` in the inherited evidence, with both positions.

**A material open item omitted from the package makes the package incomplete**, regardless of how complete the definition document itself looks.

## Receipt Semantics

`RECEIPT_ACKNOWLEDGEMENT` — `RECEIVED` means `role.technical_feasibility_lead` accepts the package as complete enough to begin feasibility assessment.

It does **not** mean: that the Role agrees the definition is sound; that any review is satisfied; that anything is `REVIEWED`, `APPROVED` or `CANONICAL`; or that ownership of the definition has moved. The receiver may accept the package and immediately record a concern about the definition — the two are unrelated acts.

## Return-for-Rework Conditions

`RETURN_FOR_REWORK` where: a boundary condition the feasibility work depends on is absent; an assumption has no owner; a material `UNKNOWN` is unstated; the definition version is ambiguous; or item 9 is missing and the receiver cannot tell what is fixed.

**The receiver may not fill a gap by assuming a value.** The return record preserves what was returned, why, and against which package version.

## Blocking Conditions

`HANDOFF_BLOCK` where: `artifact.project_definition_document` is `SUPERSEDED`; the criticality band is undetermined; or the band requires `REVIEWED` and the definition is `DRAFT`.

## Review / Decision References

`REVIEW_REFERENCE` — none required before transfer at Routine and Enhanced Review Candidate. **At Enhanced Decision-Grade and above, `review.evidence_integrity_provenance` must be `SATISFIED` over the inherited evidence base** before transfer.

`DECISION_REFERENCE` — `decision.project_definition_freeze` where the definition is frozen before transfer. Where it is not yet taken, the package states that the definition is unfrozen and may change; the transfer proceeds and the receiver's work is explicitly conditional.

Neither reference may be bypassed by transferring anyway.

## Criticality Scaling

| Band | Package depth |
|---|---|
| Routine / Standard | Items 1–4, 7, 9; definition at `DRAFT` |
| Enhanced Review Candidate | All 9 items; assumption owners mandatory |
| Enhanced Decision-Grade | All items; definition `REVIEWED`; `review.evidence_integrity_provenance` `SATISFIED`; item 9 explicit and itemised |
| Major / Systemic | As above, plus no material open item may be `NON_MATERIAL` by assertion — classification is independently checkable |

Criticality changes package and evidence depth. It changes no Role identity and moves no ownership.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no ownership, package or reference change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, transport, notification, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
