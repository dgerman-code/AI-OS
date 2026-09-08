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

`SENDER_ROLE` — a **closed, enumerated set**. This Handoff governs a known grant-application transfer, so every permitted sender is named with its objective activation trigger and its exact contribution. There is no open category and no "relevant specialist" clause: a Role not in this table cannot send on this Handoff, and content arriving from one makes the package incomplete.

| Sender `role.<id>` | Activation | Contribution to the package | Retains |
|---|---|---|---|
| `role.eu_grants_programmes_specialist` | `ALWAYS` | `artifact.eu_application_package`, the compliance matrix, the eligibility condition list, the bound rulebook reference | Ownership of the package and of call-fit and application logic |
| `role.legal_regulatory_lead` | `CONDITIONAL(the call raises legal-framework, IP or contractual questions)` | `artifact.legal_analysis` as an attributed section | Ownership of the analysis |
| `role.data_protection_gdpr_specialist` | `CONDITIONAL(the action processes personal data)` | `artifact.data_protection_impact_assessment` and the lawful-basis analysis as an attributed section | Ownership; the lawful basis remains unadopted |
| `role.procurement_state_aid_specialist` | `CONDITIONAL(the action carries State Aid or public-procurement exposure)` | `artifact.state_aid_assessment` as an attributed section | Ownership of the assessment |
| `role.institutional_communications_editorial_specialist` | `CONDITIONAL(the call requires dissemination or communication content)` | `artifact.dissemination_plan` as an attributed section | Ownership of the plan |
| `role.learning_vet_design_specialist` | `CONDITIONAL(the call is a vocational-excellence or learning-design action)` | `artifact.curriculum_design` and `artifact.assessment_design` as attributed sections | Ownership of both |
| `role.monitoring_evaluation_learning_specialist` | `CONDITIONAL(the call requires a results framework or indicator set)` | Results-framework and indicator content as an attributed section | Ownership of the MEL methodology |

Every activation trigger above is the same objective condition the approved Phase 5 `workflow.eu_grant_application_development` participation table already declares. This Handoff **narrows** to that set; it introduces no new sender and widens nothing.

**Retains after transfer:** as tabulated. Attribution is preserved through the transfer — a section does not become the package owner's work by being assembled into the package, and no ownership transfers on this handoff.

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
5. every specialist section with its owning `role.<id>` attributed, each traceable to a sender in the enumerated table above;
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

`RETURN_FOR_REWORK` where: the compliance matrix has unmapped requirements; a specialist section arrives unattributed, or attributed to a Role outside the enumerated sender set; the rulebook version is unstated or its currency unconfirmed; `AI_SUGGESTION` content is present without item 9 declaring it; or a factual claim has no source record.

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
