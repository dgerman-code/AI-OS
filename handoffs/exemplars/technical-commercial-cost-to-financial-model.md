# Handoff — Technical, Commercial and Cost Basis to Financial Model

Status: PROPOSED — Phase 6 exemplar Handoff Card
Inherits: `standard.handoff.common_constraints@0.1`

## Identity
- Handoff Name: Technical, Commercial and Cost Basis to Financial Model
- Handoff ID: `handoff.technical_commercial_cost_to_financial_model`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.handoff.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

A **converging** handoff: three separately owned positions arrive at one receiver who must combine them without owning any of them. This is where the model's assumptions are born, and where an unlabelled input becomes an unattributed model assumption that nobody can later trace to a Role.

## Trigger

`HANDOFF_TRIGGER` — `workflow.project_development_readiness` S2 and S3 have exited at least `COMPLETE_WITH_OPEN_ITEMS`, and financial modelling is due.

## Sender Role(s)

`SENDER_ROLE` — three senders, each transferring only its own owned position:

| Sender | Transfers | Retains |
|---|---|---|
| `role.technical_feasibility_lead` | `artifact.technical_basis_of_design`, `artifact.feasibility_study` | Ownership of both, and the feasibility conclusion |
| `role.commercial_demand_specialist` | `artifact.demand_study` | Ownership and the demand basis conclusion |
| `role.capex_cost_engineering_specialist` | `artifact.cost_estimate`, `artifact.contingency_analysis` | Ownership and the cost conclusion |

Conditionally, where activated: `role.asset_om_technical_operations_specialist` transfers `artifact.operating_cost_driver_definition` and retains its ownership.

**No sender transfers ownership; no ownership transfers on this handoff.** Each remains answerable for its own position after the model consumes it.

## Receiver Role(s)

`RECEIVER_ROLE` — `role.financial_modelling_specialist`.

**Bounded next activity:** cash-flow and debt-schedule modelling, scenario and sensitivity analysis, and assumptions-register maintenance against the transferred positions. The receiver **does not author** the technical, demand or cost positions and may not adjust them — it models them.

## Subject

`HANDOFF_SUBJECT` — the three (or four) owned artifacts above, plus responsibility for the next bounded activity.

## Required Package Contents

`HANDOFF_PACKAGE`, per sender:

1. the sender's artifact(s) at a stated version;
2. **every assumption the sender's position rests on**, each with basis, source and the sender as named owner;
3. the sender's own uncertainty statement — ranges, confidence, sensitivity of its position to its inputs;
4. what the sender's position explicitly does **not** establish;
5. source verification records for facts asserted;
6. the sender's open items with Phase 5 §14A classification.

Plus, across the package: the consolidated assumption register from S1, and any `CONFLICT_DETECTED` between the three positions already identified.

Item 4 per sender is what stops the receiver from treating silence as endorsement.

## Required Knowledge States

`STATE_REQUIREMENT` — each sender artifact at `DRAFT` minimum; **`REVIEWED` at Enhanced Decision-Grade and above** for `artifact.cost_estimate` and `artifact.demand_study`, whose review requirements the Workflow already carries. Assumptions labelled `ASSUMPTION`; unresolved inputs `UNKNOWN`; facts traceable to `SOURCE`.

This Handoff promotes no state.

## Provenance / Traceability Requirements

`PROVENANCE_REQUIREMENT` — version identity per artifact; the version the model will cite recorded at transfer, so the model's inputs remain identifiable when a sender revises; source verification per asserted fact; and a superseded-input flag on anything already replaced.

## Carried Open Items

`OPEN_ITEM_CARRY` — every unresolved item from S2 and S3, classified. **Any item that materially moves a model output is `MATERIAL_TO_NEXT_STEP_OR_GATE`**, and remains so inside the model: it does not become a modelling detail by entering the model.

Where two senders' positions conflict, the conflict travels as `CONFLICT_DETECTED` with both positions. **The receiver may not resolve it by choosing one** — that is an `ESCALATED` outcome under the Workflow, not a modelling choice.

## Receipt Semantics

`RECEIPT_ACKNOWLEDGEMENT` — `RECEIVED` means `role.financial_modelling_specialist` accepts the packages as complete enough to model.

It does **not** mean the receiver endorses the technical, demand or cost positions; does not satisfy `review.cost_estimate`, `review.engineering_technical` or any other review; does not make any input `REVIEWED`, `APPROVED` or `CANONICAL`; and does not move ownership. **A modelled assumption remains the sending Role's assumption**, cited in the register with that Role as owner — the model is where it is used, not where it becomes true.

## Return-for-Rework Conditions

`RETURN_FOR_REWORK` where: an assumption arrives without a basis or owner; a sender's position lacks its uncertainty statement; item 4 is missing; a version is ambiguous; or an input the model requires is absent.

**The receiver may not default a missing input.** Under `standard.handoff.common_constraints` §6, reinterpreting a missing input as an assumption is prohibited: it manufactures a basis no Role owns, and it is the single most likely failure at this handoff.

## Blocking Conditions

`HANDOFF_BLOCK` where: any sender artifact is `SUPERSEDED`; an unresolved `CONFLICT_DETECTED` between two sender positions is material to a headline output; or the band requires `REVIEWED` inputs and a sender artifact is `DRAFT`.

## Review / Decision References

`REVIEW_REFERENCE` — at Enhanced Decision-Grade and above, `review.cost_estimate` must be `SATISFIED` over `artifact.cost_estimate`, and `review.evidence_integrity_provenance` `SATISFIED` over the consolidated evidence base, before transfer.

`DECISION_REFERENCE` — `decision.cost_estimate_acceptance` and `decision.demand_basis_acceptance` where the band requires them before the model relies on those positions.

Neither may be bypassed by transferring anyway.

## Criticality Scaling

| Band | Package depth |
|---|---|
| Routine / Standard | Items 1, 2, 6 per sender |
| Enhanced Review Candidate | All 6 items per sender; consolidated register mandatory |
| Enhanced Decision-Grade | All items; `review.cost_estimate` and `review.evidence_integrity_provenance` `SATISFIED`; per-assumption owner attribution independently checkable |
| Major / Systemic | As above; no material `CONFLICT_DETECTED` may be carried into the model unresolved or unescalated |

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no ownership, package or reference change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, transport, notification, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
