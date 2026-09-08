# Handoff — Software Implementation to Security and Test Review

Status: PROPOSED — Phase 6 exemplar Handoff Card
Inherits: `standard.handoff.common_constraints@0.1`

## Identity
- Handoff Name: Software Implementation to Security and Test Review
- Handoff ID: `handoff.software_implementation_to_security_and_test_review`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.handoff.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

A **diverging** handoff: one implementation goes to two receivers who ask different questions and must not be conflated. It also carries the sharpest independence hazard in the registry — `role.security_engineer` is both a sender (it implements the controls it owns) and a receiver (it assesses them), and the card must keep those two capacities apart.

## Trigger

`HANDOFF_TRIGGER` — `workflow.software_change_delivery` S3 has exited at least `COMPLETE_WITH_OPEN_ITEMS` and implementation is substantially available.

## Sender Role(s)

`SENDER_ROLE`, each conditionally activated on its layer being in scope:

| Sender | Transfers | Retains |
|---|---|---|
| `role.full_stack_software_engineer` | `artifact.source_code_change` | Ownership |
| `role.integration_api_engineer` | `artifact.integration_contract_specification` | Ownership |
| `role.database_data_engineer` | `artifact.database_migration_script` | Ownership; the script is **not executed** by this transfer |
| `role.platform_devops_engineer` | `artifact.deployment_pipeline` | Ownership |
| `role.security_engineer` | `artifact.security_control_implementation` | Ownership — **as sender in its implementing capacity** |

## Receiver Role(s)

`RECEIVER_ROLE` — two receivers with different questions:

| Receiver | Question | Bounded next activity |
|---|---|---|
| `role.security_engineer` | Are the controls present and effective? | Control validation and residual-risk statement — **in its assessing capacity** |
| `role.software_qa_test_automation_specialist` | Does the change meet its acceptance criteria? | Test execution, coverage analysis, defect management; and security testing **within a scope the Security Engineer defines** |

### The independence hazard, stated explicitly

`role.security_engineer` appears on both sides. Under the approved Phase 5 correction it implements the security controls it owns at S3 and assesses them at S4. **That is producer self-assessment**, and this Handoff does not cure it. Under `review.security`, the Role instance that designed or implemented the controls is **prohibited** from satisfying the independent security review over them.

So: this transfer produces `artifact.security_control_assessment` as the owning Role's own work — legitimate and necessary — and it leaves `review.security` **entirely unsatisfied**. A second, eligible reviewer is required, and where none exists the review is `NOT_SATISFIED` and the Workflow blocks, reworks or escalates.

## Subject

`HANDOFF_SUBJECT` — the implementation artifacts above, plus responsibility for validation and test activities. No ownership transfers.

## Required Package Contents

`HANDOFF_PACKAGE`:

1. each sender artifact at a stated version;
2. `artifact.solution_architecture_specification` and `artifact.architecture_decision_record` at the versions implemented against;
3. `artifact.product_requirements` with the acceptance criteria the change claims to meet;
4. the threat model and control design from S2, at their versions;
5. **every deviation from the S2 design position**, with its acceptance status by `role.solution_architect`;
6. the security-relevant surface introduced or altered by the change;
7. environment and configuration position for the deployment pipeline;
8. open items from S3 with Phase 5 §14A classification.

Item 5 is the package element the QA and security receivers most need and the implementers are least inclined to volunteer.

## Required Knowledge States

`STATE_REQUIREMENT` — implementation artifacts at `DRAFT`; architecture position `REVIEWED` where `decision.architecture_adoption` has been taken; threat model current against the change's actual surface; acceptance criteria testable.

This Handoff promotes no state, and receipt does not make an implementation `REVIEWED`.

## Provenance / Traceability Requirements

`PROVENANCE_REQUIREMENT` — version identity per artifact; the architecture version implemented against; requirement-to-implementation traceability; threat-to-control traceability; and identification of any dependency changed since S2.

## Carried Open Items

`OPEN_ITEM_CARRY` — classified per Phase 5 §14A:

- an unratified deviation from the adopted design → `MATERIAL_TO_NEXT_STEP_OR_GATE`;
- a designed control not implemented → `MATERIAL_TO_NEXT_STEP_OR_GATE`;
- a security-relevant surface not in the threat model → `MATERIAL_TO_NEXT_STEP_OR_GATE`;
- a known implementation limitation not affecting an acceptance criterion → `NON_MATERIAL_TO_NEXT_STEP`, still carried;
- any residual risk or control effect the sender cannot yet assess → `UNKNOWN`, carried explicitly rather than omitted;
- any `CONFLICT_DETECTED` between the implementation and the adopted architecture position, or between two senders' interface assumptions, travels with both positions → `MATERIAL_TO_NEXT_STEP_OR_GATE`. The receivers do not adjudicate it; it escalates to `role.solution_architect`.

## Receipt Semantics

`RECEIPT_ACKNOWLEDGEMENT` — `RECEIVED` means each receiver accepts the package as complete enough to begin its own activity.

It does **not** mean the implementation is correct or secure; does **not** satisfy `review.security`, `review.code` or `review.test_coverage`; does **not** make any artifact `REVIEWED`, `APPROVED` or `CANONICAL`; and does not move ownership. In particular, `role.security_engineer` receiving its own implementation for assessment **is not independent review of it**, and the card says so where a reader would most want to skip it.

## Return-for-Rework Conditions

`RETURN_FOR_REWORK` where: a deviation from the adopted architecture is undeclared; a designed control is absent without explanation; acceptance criteria are untestable as written; a version is ambiguous; or the threat model does not cover the surface the change actually alters.

A deviation discovered by a receiver rather than declared by a sender is `ESCALATED` to `role.solution_architect` — **the implementing Role does not ratify its own deviation.**

## Blocking Conditions

`HANDOFF_BLOCK` where: the architecture position implemented against has been superseded; or the change alters a security-relevant surface and no threat model covers it.

## Review / Decision References

`REVIEW_REFERENCE` — `review.security`, `review.code` and `review.test_coverage` are all **downstream of this handoff and are not satisfied by it**. At Enhanced Decision-Grade and above, `review.security` must be `SATISFIED` by an eligible reviewer before the package supports release readiness at S6.

`DECISION_REFERENCE` — `decision.production_release`, `decision.production_database_migration` and `decision.security_risk_acceptance` all sit at S6 or beyond. **This handoff reaches none of them**, and the migration script transferred here is explicitly not executed against production by this or any transfer.

## Criticality Scaling

| Band | Package depth |
|---|---|
| Routine / Standard | Items 1–3, 8; security screening only |
| Enhanced Review Candidate | All 8 items; threat model and control design mandatory |
| Enhanced Decision-Grade | All items; `review.security` mandatory downstream by an eligible reviewer; deviation register independently checkable |
| Major / Systemic | As above; no unratified deviation may be carried past this transfer |

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no ownership, package or reference change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, transport, notification, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
