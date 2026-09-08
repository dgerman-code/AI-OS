# Handoff — Application Content to Compliance Review

Status: PROPOSED — Phase 6 exemplar Handoff Card
Inherits: `standard.handoff.common_constraints@0.1`

## Identity
- Handoff Name: Application Content to Compliance Review
- Handoff ID: `handoff.application_content_to_compliance_review`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.handoff.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

The handoff that most needs the Handoff-vs-Review boundary stated out loud. Its receivers perform the S5 compliance cycle inside `workflow.eu_grant_application_development` — and that cycle is **producer quality control**, not the independent `review.eu_programme_compliance`. This card exists partly to make that impossible to blur under deadline pressure.

## Trigger

`HANDOFF_TRIGGER` — `workflow.eu_grant_application_development` S3 and S4 have exited and the assembled package is ready for the compliance cycle.

## Sender Role(s)

`SENDER_ROLE` — `role.eu_grants_programmes_specialist`, transferring the assembled package; and each conditionally activated specialist Role transferring its own section by attribution.

**Retains after transfer:** the grants specialist retains ownership of `artifact.eu_application_package`; each specialist retains ownership of its own contributed conclusion. Attribution is preserved through the transfer — a section does not become the package owner's work by being assembled into the package.

## Receiver Role(s)

`RECEIVER_ROLE`:

- `role.grant_financial_compliance_budget_specialist` — budget arithmetic and cost eligibility re-check, over its own owned assessment;
- `role.knowledge_evidence_steward` — source verification of factual claims and evidence integrity;
- `role.consortium_partner_coordination_specialist` — partner confirmation status check.

**Bounded next activity:** the S5 compliance and quality cycle. **None of these receivers satisfies `review.eu_programme_compliance` by performing it** — that requirement is satisfied only by an eligible reviewer under the Review Profile, and the Profile explicitly names this cycle as producer QC.

## Subject

`HANDOFF_SUBJECT` — `artifact.eu_application_package` at a stated version, its compliance matrix, and the specialist sections by attribution. Plus responsibility for the compliance cycle. No ownership transfers.

## Required Package Contents

`HANDOFF_PACKAGE`:

1. `artifact.eu_application_package` at a stated version;
2. the compliance matrix with each rulebook requirement mapped to the content addressing it;
3. the eligibility condition list with satisfied / not-satisfied / `UNKNOWN` per condition;
4. `artifact.grant_budget_structure` and `artifact.cost_eligibility_assessment`;
5. every specialist section with its owning `role.<id>` attributed;
6. the bound rulebook version with currency confirmed at assembly;
7. partner confirmation status per participant;
8. source records for every factual claim in the narrative;
9. the list of `AI_SUGGESTION` content **not yet adopted** by a named Role.

Item 9 is a package obligation, not a nicety: unadopted AI content in a governed submission is a defect the receivers must be able to see.

## Required Knowledge States

`STATE_REQUIREMENT` — package at `DRAFT`; rulebook content `SOURCE` with confirmed currency; eligibility conditions carrying an evidenced status or `UNKNOWN`, never assumed satisfied; budget figures `CALCULATION` on labelled `ASSUMPTION` inputs; **no `AI_SUGGESTION` content presented as adopted**.

This Handoff promotes no state, and specifically does not adopt AI content on any Role's behalf.

## Provenance / Traceability Requirements

`PROVENANCE_REQUIREMENT` — package version identity; rulebook version and its currency confirmation date; requirement-to-content traceability; per-claim source records; attribution chain for each specialist section back to its owning Role.

## Carried Open Items

`OPEN_ITEM_CARRY` — classified per Phase 5 §14A:

- any eligibility condition at `UNKNOWN` → `MATERIAL_TO_NEXT_STEP_OR_GATE`, always;
- any unaddressed compliance-matrix requirement → `MATERIAL_TO_NEXT_STEP_OR_GATE`;
- an unconfirmed partner required by the call's composition rules → `MATERIAL_TO_NEXT_STEP_OR_GATE`;
- an unconfirmed partner not so required → `NON_MATERIAL_TO_NEXT_STEP`, still carried;
- narrative polish items → `NON_MATERIAL_TO_NEXT_STEP`;
- any `CONFLICT_DETECTED` between a specialist section and the package narrative, or between two specialist sections, travels with both positions stated → `MATERIAL_TO_NEXT_STEP_OR_GATE`. The receivers may not resolve it: the owning Roles do, or it escalates.

## Receipt Semantics

`RECEIPT_ACKNOWLEDGEMENT` — `RECEIVED` means the receivers accept the package as complete enough to run the compliance cycle.

It does **not** mean the package is compliant; does **not** satisfy `review.eu_programme_compliance` or any other review; does **not** make the package or any section `REVIEWED`, `APPROVED` or `CANONICAL`; and does not move ownership of the package or of any specialist section.

**This is the boundary this card exists to hold.** A receiver completing the S5 cycle with no issues has performed producer quality control. The independent review requirement stands entirely unaffected.

## Return-for-Rework Conditions

`RETURN_FOR_REWORK` where: the compliance matrix has unmapped requirements; a specialist section arrives unattributed; the rulebook version is unstated or its currency unconfirmed; `AI_SUGGESTION` content is present without item 9 declaring it; or a factual claim has no source record.

The return record preserves what was returned, why, and against which package version — and a return under deadline is still a return.

## Blocking Conditions

`HANDOFF_BLOCK` where the rulebook version relied on has been **superseded since assembly**. Preparing or checking against a superseded rulebook is not permitted whatever the deadline, and the Workflow returns to S1 as `REWORK_REQUIRED`.

## Review / Decision References

`REVIEW_REFERENCE` — `review.eu_programme_compliance` is **downstream of this handoff, not satisfied by it**. At Enhanced Review Candidate and above it must be `SATISFIED` before the package reaches submission readiness at S6. `review.factual_evidence` and `review.evidence_integrity_provenance` likewise sit downstream.

`DECISION_REFERENCE` — `decision.granting_authority_submission` is not on this transfer; it gates S6. This handoff neither reaches nor influences it.

## Criticality Scaling

| Band | Package depth |
|---|---|
| Routine / Standard | Items 1–4, 6, 9 |
| Enhanced Review Candidate | All 9 items; per-claim source records mandatory |
| Enhanced Decision-Grade | All items; full specialist trigger set assessed and recorded; `review.eu_programme_compliance` mandatory downstream |
| Major / Systemic | As above; no `UNKNOWN` eligibility condition may be carried past this transfer without escalation |

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no ownership, package or reference change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, transport, notification, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
