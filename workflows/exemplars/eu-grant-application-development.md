# EU Grant Application Development

Status: PROPOSED — Phase 5 exemplar Workflow Card
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: EU Grant Application Development
- Workflow ID: `workflow.eu_grant_application_development`
- Version: 0.1
- Status: PROPOSED
- Workflow Family: Programme / Grant Delivery
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands. Grant work is deadline-bound rather than value-bound, so the criticality driver here is usually consortium size, co-financing exposure and submission irreversibility rather than project value.
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose

An application to a European programme is assembled under a fixed external deadline, against a rulebook that is version-bound, by a consortium whose members are not under common control. This Workflow coordinates requirement capture, partner and work-package structuring, budget assembly and content production to **submission readiness**.

The deadline is the hazard. Every governance failure this card guards against — a dropped review, an unverified eligibility claim, a submission made because the clock ran out — is a deadline failure, not a competence failure.

## Trigger

`TRIGGER` — a specific call under a specific programme has been selected, with its published rulebook and deadline identified, and an application is to be prepared.

## Preconditions

- `PRECONDITION` — the call, its programme, its version and its deadline are identified.
- `PRECONDITION` — an `artifact.eu_funding_fit_assessment` exists at minimum `DRAFT`, owned by `role.eu_grants_programmes_specialist`.
- `PRECONDITION` — the applicable programme Pack is selected and its bound version stated.
- `PRECONDITION` — a decision to pursue this call has been taken; this Workflow does not make it.

## Scope
### Covers
- capture of call requirements and eligibility conditions from the controlled rulebook;
- consortium composition and partner role allocation coordination;
- work-package, results-framework and budget structure assembly;
- content production, compliance-matrix maintenance and internal review cycles;
- preparation to the point the submission decision becomes due.

### Does Not Cover
- **the submission itself** — `decision.granting_authority_submission` is a human decision right and is never reached by workflow progression;
- **the eligibility determination as a binding statement** — the assessment is prepared; the reliance decision is human;
- **partner commitments** — `decision.partner_commitment` and `decision.consortium_decision_confirmation` are human;
- **the cost eligibility conclusion** — owned by `role.grant_financial_compliance_budget_specialist`;
- **legal, GDPR or State Aid conclusions** — owned by their specialist Roles;
- independent review of any of the above.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.eu_grants_programmes_specialist` | `LEAD_ROLE` | `ALWAYS` | S1–S6 | Owns call fit, application logic and the application package. Leading does **not** grant submission authority, nor the cost-eligibility or legal conclusions. |
| `role.consortium_partner_coordination_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the application has more than one participant)` | S2, S3, S5, S6 | Owns consortium coordination status and partner-role allocation analysis. Does not commit partners. |
| `role.grant_financial_compliance_budget_specialist` | `CONTRIBUTING_ROLE` | `ALWAYS` | S3, S5 | Owns grant budget structure and cost-eligibility assessment. This conclusion is not obtainable through the lead Role. |
| `role.learning_vet_design_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the call is a vocational-excellence or learning-design action)` | S3, S4 | Owns `artifact.curriculum_design` and `artifact.assessment_design` only. Contributing rather than consulted **because it owns artifacts** when activated. |
| `role.monitoring_evaluation_learning_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the call requires a results framework or indicator set)` | S3 | Owns the results-framework content and the MEL methodology. Contributing rather than consulted **because it owns content in the package** when activated. |
| `role.sector_technical_expert` | `CONSULTED_ROLE` | `CONDITIONAL(the action has material sector technical content)` | S4 | **Advisory only in this Workflow** — it informs the lead's narrative and owns no artifact in S4. Where the action requires an owned sector opinion, that is outside this Workflow's scope. |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the call raises legal-framework, IP or contractual questions)` | S4 | Owns `artifact.legal_analysis`. Does not issue a formal legal opinion here. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.data_protection_gdpr_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the action processes personal data)` | S4 | Owns `artifact.data_protection_impact_assessment` and the lawful-basis analysis; does not adopt the lawful basis. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.procurement_state_aid_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the action carries State Aid or public-procurement exposure)` | S4 | Owns `artifact.state_aid_assessment`. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.institutional_communications_editorial_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the call requires dissemination or communication content)` | S4 | Owns `artifact.dissemination_plan`. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.deliverables_reporting_specialist` | `CONSULTED_ROLE` | `CONDITIONAL(the deliverable and reporting schedule must be designed into the proposal)` | S3 | **Advisory only in this Workflow** — it informs the schedule the lead writes into the package and owns no artifact in S3. |
| `role.knowledge_evidence_steward` | `CONTRIBUTING_ROLE` | `ALWAYS` | S1, S5 | Owns source verification and evidence integrity for the claims made in the application. |

## Composed Workflow References

**None.** The application package is a governed submission assembled against a rulebook, not a decision-grade document prepared for an internal approval, so `workflow.decision_grade_document_preparation` is not a clean fit: this Workflow's S5 verification cycle serves a submission gate rather than an approval gate, and its evidence discipline is bound to the call's own compliance matrix. No reference is forced.

## Activated Skills / Packs

References only; all bases are the approved Phase 4 records.

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| applicable programme Pack — `skill_pack.erasmus_plus`, `skill_pack.cove`, `skill_pack.life_programme`, `skill_pack.horizon_europe` | `role.eu_grants_programmes_specialist` | direct (Wave 1, REQUIRED_FOR_CONTEXT) |
| `skill_pack.cove` | `role.learning_vet_design_specialist` | direct (Wave 2, REQUIRED_FOR_CONTEXT) |
| `skill_pack.bid_proposal_management` | `role.eu_grants_programmes_specialist` | direct (Wave 1) |
| `skill.requirement_traceability` | `role.eu_grants_programmes_specialist`, `role.grant_financial_compliance_budget_specialist` | direct; also transitive via the programme Packs |
| `skill.source_verification`, `skill.source_monitoring` | `role.eu_grants_programmes_specialist`, `role.knowledge_evidence_steward` | direct (Wave 1); transitive via CoVE / LIFE Packs |
| `skill.grant_cost_eligibility_analysis` | `role.grant_financial_compliance_budget_specialist` | direct (Wave 2) |

Where a CoVE action operates under Erasmus+ rules, the CoVE Pack's declared layering brings the Erasmus+ Pack with it. That layering is declared on the Pack Card, not created here.

## Inputs

| Input | Required state |
|---|---|
| Call rulebook and annexes at the bound version | controlled source, currency confirmed |
| `artifact.eu_funding_fit_assessment` | `DRAFT` minimum |
| Partner expressions of interest | any; unverified partner claims are `UNKNOWN` until verified |
| Prior application material for reuse | any; `SUPERSEDED` material must be flagged, never silently reused |

## Stages

S3 and S4 overlap substantially in practice; the card treats them as partially ordered, with S4 content production unable to *close* until S3 structure is stable.

### Stage `S1` — Requirement and eligibility capture
- **Objective:** extract what the call actually requires, from the controlled rulebook at its bound version, before anyone writes anything.
- **Entry Criteria:** preconditions satisfied; rulebook version confirmed current.
- **Participating Roles:** `role.eu_grants_programmes_specialist` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`).
- **Activities:** requirement extraction into a compliance matrix; eligibility condition capture; source verification of the rulebook version; identification of which conditions the applicant cannot yet satisfy.
- **Artifact Contributions:** `artifact.institution_requirement_map` and the compliance matrix within `artifact.eu_application_package` (owned by `role.eu_grants_programmes_specialist`); `artifact.evidence_integrity_record` (owned by `role.knowledge_evidence_steward`).
- **Knowledge-State Expectations:** rulebook content is `SOURCE`. Interpretation of it is `DRAFT` and attributed. An eligibility condition whose satisfaction is not yet established is `UNKNOWN`, never assumed satisfied.
- **Gate / Review References:** none at this stage.
- **Exit Criteria:** every call requirement captured and traceable to its rulebook clause; eligibility conditions listed with a satisfied / not-satisfied / `UNKNOWN` status each.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `CANCELLED`.
- **Open-Item Materiality:** an eligibility condition whose status is `UNKNOWN` is `MATERIAL_TO_NEXT_STEP_OR_GATE` — the whole application depends on it. It cannot support a `COMPLETE_WITH_OPEN_ITEMS` exit; the outcome is `BLOCKED` or `ESCALATED`.

### Stage `S2` — Consortium composition
- **Objective:** establish who is in the consortium and in what role, as a coordination position — not as a commitment.
- **Entry Criteria:** S1 exited; eligibility conditions on partner composition known.
- **Participating Roles:** `role.consortium_partner_coordination_specialist` (`CONTRIBUTING_ROLE`), `role.eu_grants_programmes_specialist` (`LEAD_ROLE`).
- **Activities:** partner mapping against call composition requirements; role allocation analysis; identification of composition gaps.
- **Artifact Contributions:** `artifact.consortium_coordination_status` (owned by `role.consortium_partner_coordination_specialist`).
- **Knowledge-State Expectations:** partner capability claims are `ASSUMPTION` until evidenced. Partner participation is not `FACT` until the partner has confirmed it under `decision.partner_commitment`.
- **Gate / Review References:** `HUMAN_GATE_REFERENCE` → `decision.partnership_composition`, `decision.partner_commitment`, `decision.consortium_decision_confirmation` — all become due; none is satisfied here.
- **Exit Criteria:** composition proposal meets the call's stated composition requirements or its gap is explicit; every partner's status recorded as confirmed or not.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unconfirmed partner whose presence is required by the call's composition rules is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S3 and S6. An unconfirmed partner not required by those rules is `NON_MATERIAL_TO_NEXT_STEP` for S3 but remains carried.

### Stage `S3` — Work-package, results and budget structure
- **Objective:** build the structural skeleton — intervention logic, work packages, results framework and budget — that the content will hang from.
- **Entry Criteria:** S1 exited; S2 at least `COMPLETE_WITH_OPEN_ITEMS`.
- **Participating Roles:** `role.eu_grants_programmes_specialist` (`LEAD_ROLE`), `role.grant_financial_compliance_budget_specialist` (`CONTRIBUTING_ROLE`), `role.consortium_partner_coordination_specialist` (`CONTRIBUTING_ROLE`), `role.monitoring_evaluation_learning_specialist` and `role.learning_vet_design_specialist` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL` per the participation table), `role.deliverables_reporting_specialist` (`CONSULTED_ROLE`, `Activation: CONDITIONAL(reporting schedule designed into the proposal)`, advisory only).
- **Activities:** intervention-logic and work-package design (Pack-internal to the programme Pack); results-framework and indicator design where triggered; budget structure assembly; cost-eligibility assessment against the programme rules; deliverable and reporting schedule design where triggered.
- **Artifact Contributions:** work-package and intervention-logic content within `artifact.eu_application_package` (owned by `role.eu_grants_programmes_specialist`); `artifact.grant_budget_structure` and `artifact.cost_eligibility_assessment` (owned by `role.grant_financial_compliance_budget_specialist`); results-framework content (owned by `role.monitoring_evaluation_learning_specialist`); `artifact.curriculum_design` and `artifact.assessment_design` where triggered (owned by `role.learning_vet_design_specialist`).
- **Knowledge-State Expectations:** `DRAFT`. Budget figures are `CALCULATION` on labelled `ASSUMPTION` inputs; an unconfirmed partner cost is not a `FACT`.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.eu_programme_compliance`, `review.mel_methodology` (where triggered), `review.learning_design_quality` (where triggered); `HUMAN_GATE_REFERENCE` → `decision.budget_approval`, `decision.results_framework_approval`.
- **Exit Criteria:** every work package traced to an intervention-logic element and a budget line; cost eligibility assessed against the bound rulebook version; structural gaps named.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** a budget line whose cost eligibility is unassessed against the bound rulebook, or a work package with no intervention-logic basis, is `MATERIAL_TO_NEXT_STEP_OR_GATE`. Formatting and narrative-polish items are `NON_MATERIAL_TO_NEXT_STEP`.

### Stage `S4` — Content assembly and specialist contribution
- **Objective:** produce the narrative content, with each specialist section owned by the Role that owns that subject.
- **Entry Criteria:** S3 structure stable enough that content will not be invalidated by it.
- **Participating Roles:** `role.eu_grants_programmes_specialist` (`LEAD_ROLE`); conditionally activated set — `role.legal_regulatory_lead`, `role.data_protection_gdpr_specialist`, `role.procurement_state_aid_specialist`, `role.institutional_communications_editorial_specialist` and `role.learning_vet_design_specialist` as `CONTRIBUTING_ROLE` (each owns an artifact when activated), and `role.sector_technical_expert` as `CONSULTED_ROLE` (advisory only, owns nothing here). Every activation condition is in the participation table.
- **Activities:** narrative content production against the compliance matrix; specialist section contribution; dissemination and communication planning where triggered; DPIA-relevant analysis where personal data is processed; State Aid position where triggered.
- **Artifact Contributions:** narrative content within `artifact.eu_application_package`; `artifact.legal_analysis`, `artifact.data_protection_impact_assessment`, `artifact.state_aid_assessment`, `artifact.dissemination_plan` — each owned by its specialist Role, contributed to the package by reference, not absorbed.
- **Knowledge-State Expectations:** AI-drafted content enters as `AI_SUGGESTION` and remains so until a named Role adopts it as its own `DRAFT`. Volume of drafting does not change this.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.legal_compliance`, `review.data_protection`, `review.procurement_state_aid` (each where triggered); `HUMAN_GATE_REFERENCE` → `decision.lawful_basis_adoption`, `decision.state_aid_route_adoption` where those questions arise.
- **Exit Criteria:** every compliance-matrix requirement has content addressing it or an explicit gap; every specialist section attributed to its owning Role; no `AI_SUGGESTION` content left unadopted in the package.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unaddressed compliance-matrix requirement, or `AI_SUGGESTION` content left unadopted by a named Role, is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S5 and S6.

### Stage `S5` — Compliance and quality cycle
- **Objective:** test the assembled package against the call's own requirements, and verify the claims it makes.
- **Entry Criteria:** S3 and S4 exited.
- **Participating Roles:** `role.eu_grants_programmes_specialist` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`), `role.grant_financial_compliance_budget_specialist` (`CONTRIBUTING_ROLE`), `role.consortium_partner_coordination_specialist` (`CONTRIBUTING_ROLE`).
- **Activities:** compliance-matrix closure; requirement traceability check; source verification of factual claims; budget arithmetic and eligibility re-check; partner confirmation status check; publication-requirements validation.
- **Artifact Contributions:** compliance-matrix closure within `artifact.eu_application_package`; `artifact.evidence_gap_conflict_report` (owned by `role.knowledge_evidence_steward`).
- **Knowledge-State Expectations:** unverified claims are removed or marked `UNKNOWN`. **This stage's checking is quality control by the producing Roles and is not independent review** — where `review.eu_programme_compliance` is required, it is a separate requirement that this stage does not satisfy.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.eu_programme_compliance`, `review.factual_evidence`, `review.evidence_integrity_provenance`.
- **Exit Criteria:** compliance matrix fully addressed; every factual claim verified or removed; budget internally consistent and eligibility-assessed; unresolved items listed.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unverified factual claim remaining in the package, or a missing `review.eu_programme_compliance` where the criticality band requires it, is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward the submission gate. The review's absence is visible but not satisfied by visibility.

### Stage `S6` — Submission readiness
- **Objective:** reach the position where a human can decide whether to submit — and can decide not to.
- **Entry Criteria:** S5 exited; required reviews for the criticality band are **satisfied under the Phase 6 review semantics**. Recording that a required review is missing is **not** sufficient: where the review is a prerequisite for this stage or for the terminal gate, its absence gives `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED` unless a **named external human `decision.<id>`** explicitly permits progression without it — in which case the review **remains unsatisfied and open**, and this Workflow does not say it was satisfied, waived by the Workflow, or no longer required.
- **Participating Roles:** `role.eu_grants_programmes_specialist` (`LEAD_ROLE`), `role.consortium_partner_coordination_specialist` (`CONTRIBUTING_ROLE`).
- **Activities:** assemble the final package; state residual compliance gaps, unconfirmed partners and unverified claims; confirm the rulebook version has not changed since S1; present the submission decision with its risks.
- **Artifact Contributions:** `artifact.eu_application_package` finalised as `DRAFT` or `REVIEWED`.
- **Knowledge-State Expectations:** the package does **not** become `APPROVED` by reaching this stage. Submission readiness is a coordination position.
- **Gate / Review References:** `HUMAN_GATE_REFERENCE` → **`decision.granting_authority_submission`**. This is a `Transmitting Act` gate under `standard.workflow.common_constraints` §8 and is preserved on every path. Also `decision.consortium_decision_confirmation` where consortium sign-off precedes submission.
- **Exit Criteria:** the submission decision is due, with the package and its residual risks in front of the decision-maker.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `ESCALATED`, `CANCELLED`.
- **Open-Item Materiality:** any item bearing on the evidence basis of `decision.granting_authority_submission` — an unmet eligibility condition, an unverified claim, an unconfirmed required partner, a superseded rulebook version — is `MATERIAL_TO_NEXT_STEP_OR_GATE` and cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit. The outcome is `BLOCKED` or `ESCALATED` unless a **named external human Decision Right** explicitly permits reaching the gate with it unresolved, in which case the reference is recorded and the item stays open.

## Branches / Exception Paths

- `BRANCH` — **programme selection:** the applicable programme Pack activates at S1 and its rulebook governs; a CoVE action under Erasmus+ brings the Erasmus+ Pack by declared layering.
- `BRANCH` — **learning / VET action:** `role.learning_vet_design_specialist` engaged at S3–S4.
- `BRANCH` — **personal data processed:** `role.data_protection_gdpr_specialist` engaged at S4 and `decision.lawful_basis_adoption` enters the gate set.
- `BRANCH` — **single applicant:** S2 reduces to an eligibility-of-applicant check; it is not skipped.
- `EXCEPTION_PATH` — **rulebook version changes mid-preparation:** returns to S1 as `REWORK_REQUIRED`. Preparing against a superseded rulebook is not permitted, whatever the deadline.
- `EXCEPTION_PATH` — **partner withdraws:** returns to S2, and S3 budget structure to `REWORK_REQUIRED`.
- `EXCEPTION_PATH` — **deadline pressure:** `COMPLETE_WITH_OPEN_ITEMS` at S6 is available **only when every carried item affecting the submission gate is `NON_MATERIAL_TO_NEXT_STEP`**. Any `MATERIAL_TO_NEXT_STEP_OR_GATE` item — an unmet eligibility condition, an unverified claim, an unconfirmed required partner, a missing required review — gives `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`. Progression with a material item unresolved is possible **only** through a **named external human `decision.<id>`** explicitly permitting it, and that item then **remains open and carried forward**; this Workflow neither resolves nor downgrades it, and does not treat a missing review as satisfied or waived. **Deadline pressure is not such a Decision Right** and removes no review requirement and no human gate. **There is no expedited path to submission**: `decision.granting_authority_submission` is preserved in every case, and a missed deadline is an acceptable outcome where the alternative is an ungated submission.

No exception path bypasses any gate or review reference on the normal path.

## Rework Rules

`REWORK_LOOP` targets: S5 → S3/S4 on a compliance or verification failure; S4 → S3 where structure changed; S3 → S2 on composition change; any stage → S1 on a rulebook version change.

Prior package versions, the compliance-matrix history, verification records, partner status history and the reason for rework are preserved across every loop.

## Open-Item Materiality

For this Workflow's terminal gate, `MATERIAL_TO_NEXT_STEP_OR_GATE` covers: any unmet or `UNKNOWN` eligibility condition; any unverified factual claim remaining in the package; any unconfirmed partner the call's composition rules require; any budget line with unassessed cost eligibility; any missing `review.<id>` the criticality band requires; and any doubt about the currency of the bound rulebook version.

**A material item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit at the progression it is material to.** The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.

The only exception is a **named external human Decision Right** explicitly permitting progression with that item unresolved. The gate reference is recorded, the item **remains open**, and this Workflow neither decides the waiver nor asserts it was granted. Phase 7 owns that semantics. Deadline pressure is not such a right.

## Completion Criteria

`COMPLETION_CRITERION` — S6 exited with the submission decision due; compliance matrix addressed; every factual claim verified or marked; budget eligibility-assessed; partner status stated; every carried open item classified; and **every required review satisfied under the Phase 6 review semantics**. A missing required review does not become sufficient by being recorded: completion with one outstanding requires a **named external human `decision.<id>`** explicitly permitting it, and the review then remains unsatisfied and open.

**Completion is not submission.** The Workflow completes at the gate; the submission is a human act on the far side of it.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the call is withdrawn or the deadline passes; the applicant becomes ineligible; the consortium fails to form; a human decision stops the pursuit; or the submission decision is taken as "do not submit".

On cancellation, the package, evidence, verification records and gate history are retained. Reusable content remains available to future applications with its provenance intact.

## Outputs / Resulting Artifact States

| Artifact | Owning Role | State at completion |
|---|---|---|
| `artifact.eu_application_package` | `role.eu_grants_programmes_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.grant_budget_structure`, `artifact.cost_eligibility_assessment` | `role.grant_financial_compliance_budget_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.consortium_coordination_status` | `role.consortium_partner_coordination_specialist` | `DRAFT` |
| specialist sections (`artifact.legal_analysis`, `artifact.data_protection_impact_assessment`, `artifact.state_aid_assessment`, `artifact.curriculum_design`, `artifact.dissemination_plan`) | respective specialist Roles | `DRAFT` or `REVIEWED` |
| `artifact.evidence_integrity_record`, `artifact.evidence_gap_conflict_report` | `role.knowledge_evidence_steward` | `DRAFT` |

No artifact reaches `APPROVED` or `CANONICAL` through this Workflow.

## Authority / Review Boundary

- **This Workflow cannot submit.** No stage, outcome or completion state constitutes submission or authorises it. `decision.granting_authority_submission` is a human decision right, is a transmitting-act gate, and is preserved on the normal path and on every exception path including deadline pressure.
- `role.eu_grants_programmes_specialist` leads and owns the application package. It does **not** acquire the cost-eligibility conclusion, the legal analysis, the lawful-basis position, the State Aid position, the MEL methodology or the curriculum design by leading.
- The S5 compliance cycle is producer quality control and does **not** satisfy `review.eu_programme_compliance` or any other independent review requirement.
- No partner is committed by this Workflow; partner commitment is a human decision right.
- **Participation in this Workflow grants no professional authority.** A Role gains nothing beyond its own Role Card by participating, including at `LEAD_ROLE`.

## Criticality Scaling

| Band | Effect |
|---|---|
| Routine / Standard | Small single- or two-partner action: S2 reduced, specialist consultation on trigger only, review references advisory. |
| Enhanced Review Candidate | Multi-partner or material co-financing: `review.eu_programme_compliance` expected; budget eligibility assessment mandatory at S3. |
| Enhanced Decision-Grade | Large consortium, high co-financing exposure, or a public counterparty: full specialist trigger set assessed explicitly at S4; `review.eu_programme_compliance` and `review.factual_evidence` mandatory; S5 claim-by-claim verification. |
| Major / Systemic | As above, plus mandatory `review.evidence_integrity_provenance` and no `COMPLETE_WITH_OPEN_ITEMS` exit at S6 for eligibility-critical items. |

Depth and review intensity change. **Role identity does not change**, and there is no separate small-grant or large-grant Workflow.

## Evidence / Traceability Requirements

Every requirement traceable to its rulebook clause at the bound version; every claim traceable to a verified source or marked `UNKNOWN`; every budget line traceable to a work package and an eligibility basis; every specialist section attributed to its owning Role; partner status history retained; rulebook currency confirmed at S1 and re-confirmed at S6.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no authority, Role scope, gate or artifact-ownership change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
