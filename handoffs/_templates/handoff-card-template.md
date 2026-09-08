# Handoff Card Template

Status: PROPOSED — Phase 6 standard candidate
Template Version: 0.1
Inherits: `standard.handoff.common_constraints@0.1`

Every Handoff Card uses this structure. Sections are mandatory. A section that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Handoff Name:
- Handoff ID: `handoff.<stable_snake_case_name>`
- Version:
- Status: PROPOSED
- Governance Owner:
- Inherits: `standard.handoff.common_constraints@0.1`
- Supersedes / Superseded By:

## Purpose

What transfer this pattern governs and why it needs governing.

## Trigger

`HANDOFF_TRIGGER` — the objective condition under which the transfer becomes due.

## Sender Role(s)

`SENDER_ROLE` — approved `role.<id>`, with a note on what it retains after transfer. It retains ownership of its artifact and conclusion in every case.

## Receiver Role(s)

`RECEIVER_ROLE` — approved `role.<id>`, with the bounded next activity the package enables. The receiver gains nothing beyond its own Role Card.

## Subject

`HANDOFF_SUBJECT` — the artifact(s), evidence set, dependency or responsibility-for-next-action being transferred, each attributed to its owning Role.

## Required Package Contents

`HANDOFF_PACKAGE` — everything that must travel. Enumerated, because completeness is assessed against this list.

## Required Knowledge States

`STATE_REQUIREMENT` — the state each subject element must hold at transfer, with an explicit note that the Handoff does not promote states.

## Provenance / Traceability Requirements

`PROVENANCE_REQUIREMENT` — version identity, source verification status, and the traceability record that must accompany the subject.

## Carried Open Items

`OPEN_ITEM_CARRY` — the assumptions, conflicts and unknowns that travel with the package, each classified `NON_MATERIAL_TO_NEXT_STEP` or `MATERIAL_TO_NEXT_STEP_OR_GATE` per Phase 5 §14A. Omitting a material one makes the package incomplete.

## Receipt Semantics

`RECEIPT_ACKNOWLEDGEMENT` — what `RECEIVED` means here, and the four things it does not mean: agreement with the conclusion, review satisfaction, approval or canonicalization, and transfer of ownership.

## Return-for-Rework Conditions

`RETURN_FOR_REWORK` — what causes the receiver to return the package, and what the return record preserves.

## Blocking Conditions

`HANDOFF_BLOCK` — what prevents transfer entirely, as distinct from a return.

## Review / Decision References

`REVIEW_REFERENCE` — any `review.<id>` that must be `SATISFIED` before transfer.
`DECISION_REFERENCE` — any `decision.<id>` gating the transfer.
Neither may be bypassed by the handoff.

## Criticality Scaling

How package depth, evidence and checkpoints change by band. Must state that criticality changes depth, not Role identity or ownership.

## Versioning / Change Control

Version history, with confirmation that no version change silently altered ownership, package obligations or review/gate references.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, transport, notification, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
