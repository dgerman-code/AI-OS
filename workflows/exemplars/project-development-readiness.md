# Project Development Readiness

Status: PROPOSED — Phase 5 exemplar Workflow Card
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: Project Development Readiness
- Workflow ID: `workflow.project_development_readiness`
- Version: 0.1
- Status: PROPOSED
- Workflow Family: Project / Investment Development
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands. Routine runs a reduced stage set; Enhanced Decision-Grade and Major / Systemic run the full set with the additional reviews in *Criticality Scaling*.
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose

A defined project must reach a readiness position that a human can take to an investment, financing or stage-gate decision. That position depends on technical, commercial, financial, legal and E&S conclusions that **nine different Roles own separately**. This Workflow coordinates their sequencing, dependency and integration.

It exists because the integration is real work and the failure mode is specific: under gate pressure, an integrating lead starts *writing* the specialist positions instead of *assembling* them. That is the failure this card is built to make visible.

## Trigger

`TRIGGER` — a project has a stable definition and a named forward gate (investment, financing, or a defined stage gate) against which readiness must be assessed.

## Preconditions

- `PRECONDITION` — `artifact.project_definition_document` exists, at minimum `DRAFT`, owned by `role.project_development_lead`.
- `PRECONDITION` — the forward gate is named, with its evidence expectations identified.
- `PRECONDITION` — criticality band is determined under `architecture/project-criticality-policy.md`.
- `PRECONDITION` — for Enhanced Decision-Grade and above, `artifact.project_definition_document` is `REVIEWED` before Stage S4 may be entered.

## Scope
### Covers
- sequencing and dependency management across the readiness workstreams;
- convening specialist contributions in the order their inputs become available;
- integration of specialist positions into a coherent readiness assessment;
- maintenance of the open-item, assumption and gate-critical risk position;
- preparation to the point the forward gate decision becomes due.

### Does Not Cover
- **the feasibility conclusion** — owned by `role.technical_feasibility_lead`;
- **the demand basis** — owned by `role.commercial_demand_specialist`;
- **the cost estimate** — owned by `role.capex_cost_engineering_specialist`;
- **the financial model and its integrity position** — owned by `role.financial_modelling_specialist`;
- **the bankability position** — owned by `role.funding_bankability_architect`;
- **the legal and regulatory analysis** — owned by `role.legal_regulatory_lead`;
- **the E&S assessment** — owned by `role.esg_es_specialist`;
- **the risk quantification** — owned by `role.enterprise_project_risk_specialist`;
- **the evidence integrity position** — owned by `role.knowledge_evidence_steward`;
- the investment, financing, land or stage-gate decision itself;
- any independent review of the above.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.project_development_lead` | `LEAD_ROLE` | `ALWAYS` | S1–S7 | Coordinates, integrates and maintains the open-item position. Gains **no** specialist conclusion. Its Role Card excludes specialist conclusions in technical, financial, legal, tax and ESG disciplines; leading this Workflow does not alter that. |
| `role.technical_feasibility_lead` | `CONTRIBUTING_ROLE` | `ALWAYS` | S2, S6 | Owns the feasibility position and technical basis. Contributes it; does not receive cost ownership — `skill.lifecycle_cost_analysis` remains support-only under Phase 4 and CAPEX/OPEX estimation stays with the cost Roles. |
| `role.sector_technical_expert` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the project's sector or technology is one for which a sector Specialisation exists and the technical basis depends on it)` | S2 | Owns `artifact.sector_technical_opinion` and nothing else. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.commercial_demand_specialist` | `CONTRIBUTING_ROLE` | `ALWAYS` | S2, S6 | Owns the demand study and demand basis. Does not own tariff or revenue decisions. |
| `role.capex_cost_engineering_specialist` | `CONTRIBUTING_ROLE` | `ALWAYS` | S3, S6 | Owns the cost estimate and contingency analysis. Not obtainable through any other Role's contribution. |
| `role.asset_om_technical_operations_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(an operating-cost or O&M basis is required by the forward gate or by the financial model)` | S3 | Owns `artifact.operating_cost_driver_definition`. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.financial_modelling_specialist` | `CONTRIBUTING_ROLE` | `ALWAYS` | S4, S6 | Owns the financial model and its assumptions register. Consumes S2–S3 outputs as inputs; does not author them. |
| `role.funding_bankability_architect` | `CONTRIBUTING_ROLE` | `ALWAYS` | S5, S6 | Owns the bankability assessment and funding strategy. Does not own financing decisions. |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `ALWAYS` | S3, S6 | Owns the legal and regulatory analysis. Does not issue a formal legal opinion within this Workflow. |
| `role.esg_es_specialist` | `CONTRIBUTING_ROLE` | `ALWAYS` | S3, S6 | Owns E&S screening and assessment. Does not own the E&S action-plan commitment. |
| `role.enterprise_project_risk_specialist` | `CONTRIBUTING_ROLE` | `ALWAYS` | S5, S6 | Owns the risk register methodology, quantification and allocation analysis. |
| `role.knowledge_evidence_steward` | `CONTRIBUTING_ROLE` | `ALWAYS` | S1, S6, S7 | Owns evidence integrity, provenance and the gap/conflict position. Does not own any substantive conclusion. |
| `role.procurement_state_aid_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the project is subject to public procurement rules or carries State Aid exposure)` | S3 | Owns `artifact.procurement_route_analysis` and `artifact.state_aid_assessment`. Contributing rather than consulted **because it owns artifacts** when activated. |
| `role.insurance_risk_transfer_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(an insurance programme is material to the bankability or risk-allocation position)` | S5 | Owns `artifact.insurance_programme_design`. Contributing rather than consulted **because it owns an artifact** when activated. |

## Composed Workflow References

**None.** This is a deliberate finding rather than an omission.

`workflow.decision_grade_document_preparation` is the obvious candidate: S6–S7 of this Workflow produce a decision-grade document, and the child's S3–S5 (fact/assumption/calculation separation, traceability and coherence, review requirement and approval preparation) map onto them closely. But the child's S1 evidence base and S2 specialist contribution do **not** sit inside S6–S7 — they are this Workflow's own S1 and S2–S5, spread across the whole pattern rather than confined to the segment that would carry the reference.

A `WORKFLOW_REFERENCE` here would therefore point at a child whose preconditions this parent satisfies in a different place than the reference sits, which is a partial and overlapping fit, not a clean composition. Per `standard.workflow.common_constraints` §14C the reference is not made: **representability is the point, not a tidy-looking claim.** Whether the child should be decomposed so that its document-production segment can be referenced independently is a question for a wider exemplar set, and is recorded as such in the remediation record.

## Activated Skills / Packs

References only. Every entry below is already compatible under the approved Phase 4 mapping records; this card creates no compatibility.

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `specialisation.infrastructure_project_preparation` | `role.project_development_lead` | direct (Wave 2) |
| sector Specialisation (e.g. `specialisation.bess`, `specialisation.solar`) | `role.technical_feasibility_lead` | direct (Wave 1, grouped sector set) |
| `skill.lifecycle_cost_analysis` | `role.technical_feasibility_lead` | direct, **support-only**, Wave 1 |
| `skill_pack.project_finance_metrics` | `role.financial_modelling_specialist`, `role.funding_bankability_architect` | direct (Wave 1 / Wave 2) |
| `skill.requirement_traceability` | `role.knowledge_evidence_steward` | direct (Wave 1, migrated in Wave 3) |
| `skill.source_verification` | `role.knowledge_evidence_steward` | direct (Wave 1) |

If any instance appears to need a capability outside these bases, that is a Phase 4 mapping finding, raised there. It is not resolved here.

## Inputs

| Input | Required state |
|---|---|
| `artifact.project_definition_document` | `DRAFT` minimum; `REVIEWED` before S4 at Enhanced and above |
| Named forward gate and its evidence expectations | stated |
| Criticality band determination | stated |
| Prior `artifact.research_evidence_pack` where one exists | any; `SUPERSEDED` inputs must be flagged, not silently used |

## Stages

S2 and S3 may run in parallel. S4 depends on both. S5 depends on S4. S1, S6 and S7 are strictly sequential relative to the rest.

### Stage `S1` — Evidence baseline and gate framing
- **Objective:** establish what is known, what is assumed, and what the named gate will demand — before any workstream commits effort against the wrong target.
- **Entry Criteria:** preconditions satisfied; forward gate named.
- **Participating Roles:** `role.project_development_lead` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`).
- **Activities:** frame gate evidence expectations; assemble and verify the existing evidence base; separate `FACT` / `ASSUMPTION` / `CALCULATION` in the inherited material; open the assumption register.
- **Artifact Contributions:** `artifact.preparation_gap_register` (owned by `role.project_development_lead`); `artifact.evidence_integrity_record` and `artifact.evidence_gap_conflict_report` (owned by `role.knowledge_evidence_steward`).
- **Knowledge-State Expectations:** inherited sources carry their own states; nothing is promoted here. Unverifiable inputs are recorded `UNKNOWN` rather than assumed.
- **Gate / Review References:** none.
- **Exit Criteria:** gap register exists and names every gate-critical unknown; assumption register open; no material `CONFLICT_DETECTED` left unrecorded.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `CANCELLED`.
- **Open-Item Materiality:** a named gate-critical unknown may exit as `NON_MATERIAL_TO_NEXT_STEP` only where no S2–S5 workstream depends on it. An unverifiable input that any downstream workstream will consume is `MATERIAL_TO_NEXT_STEP_OR_GATE` and blocks; naming it does not clear it.

### Stage `S2` — Technical and demand basis
- **Objective:** establish the technical basis and the demand basis as **two separately owned positions**, because the financial model depends on both and must not receive them merged.
- **Entry Criteria:** S1 exited; project configuration stable enough to assess.
- **Participating Roles:** `role.technical_feasibility_lead` (`CONTRIBUTING_ROLE`), `role.commercial_demand_specialist` (`CONTRIBUTING_ROLE`), `role.sector_technical_expert` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(sector Specialisation exists and the technical basis depends on it)`), `role.project_development_lead` (`LEAD_ROLE`, coordination only).
- **Activities:** technical option comparison and feasibility analysis; design-basis definition; market sizing, segmentation and demand analysis; sector opinion where triggered.
- **Artifact Contributions:** `artifact.feasibility_study` and `artifact.technical_basis_of_design` (owned by `role.technical_feasibility_lead`); `artifact.demand_study` (owned by `role.commercial_demand_specialist`); `artifact.sector_technical_opinion` (owned by `role.sector_technical_expert`).
- **Knowledge-State Expectations:** outputs enter `DRAFT`. Where AI-assumed, content enters `AI_SUGGESTION` and does not advance by stage movement.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.engineering_technical`, `review.operational_feasibility` (Enhanced and above); `HUMAN_GATE_REFERENCE` → `decision.technical_basis_freeze`, `decision.demand_basis_acceptance` — both become **due**, not satisfied, here.
- **Exit Criteria:** feasibility position stated with its uncertainties; demand basis stated with its assumptions labelled; both attributed to their owning Roles.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** any unresolved item that changes the technical or demand basis the financial model will consume is `MATERIAL_TO_NEXT_STEP_OR_GATE` and cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit toward S4. Presentation and formatting items are `NON_MATERIAL_TO_NEXT_STEP`.

### Stage `S3` — Cost, legal, regulatory and E&S positions
- **Objective:** establish the cost basis and the constraint set that bound what the project can be, from four Roles that do not substitute for one another.
- **Entry Criteria:** S1 exited; technical basis at least provisionally available from S2.
- **Participating Roles:** `role.capex_cost_engineering_specialist`, `role.legal_regulatory_lead`, `role.esg_es_specialist` (all `CONTRIBUTING_ROLE`); `role.asset_om_technical_operations_specialist`, `role.procurement_state_aid_specialist` (both `CONTRIBUTING_ROLE`, `Activation: CONDITIONAL` per the participation table); `role.project_development_lead` (`LEAD_ROLE`).
- **Activities:** CAPEX estimation and contingency analysis; operating cost driver definition where triggered; regulatory mapping and legal analysis; E&S screening and assessment against the applicable safeguard standard; procurement and State Aid route analysis where triggered.
- **Artifact Contributions:** `artifact.cost_estimate`, `artifact.contingency_analysis` (owned by `role.capex_cost_engineering_specialist`); `artifact.operating_cost_driver_definition` (owned by `role.asset_om_technical_operations_specialist`); `artifact.legal_analysis` (owned by `role.legal_regulatory_lead`); `artifact.es_risk_screening`, `artifact.es_impact_assessment` (owned by `role.esg_es_specialist`); `artifact.procurement_route_analysis`, `artifact.state_aid_assessment` (owned by `role.procurement_state_aid_specialist`).
- **Knowledge-State Expectations:** `DRAFT`; assumptions explicitly labelled and carried to the register opened in S1.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.cost_estimate`, `review.legal_compliance`, `review.esg_safeguards`, `review.procurement_state_aid`; `HUMAN_GATE_REFERENCE` → `decision.cost_estimate_acceptance`, `decision.es_assessment_acceptance`.
- **Exit Criteria:** cost basis stated with contingency rationale; regulatory perimeter stated; E&S category and material issues stated; no constraint discovered here left unreflected in the gap register.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unresolved cost, regulatory, E&S or procurement constraint that bounds what the project can be is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S4 and S7. A missing required `review.cost_estimate` or `review.esg_safeguards` where the criticality band requires it is likewise material — its absence is visible but not satisfied.

### Stage `S4` — Financial modelling
- **Objective:** express the technical, demand, cost and constraint positions as a governed financial model with a visible assumptions register.
- **Entry Criteria:** S2 and S3 exited, at least `COMPLETE_WITH_OPEN_ITEMS`; at Enhanced and above, `artifact.project_definition_document` is `REVIEWED`; every input assumption carried from S1–S3 is available and labelled.
- **Participating Roles:** `role.financial_modelling_specialist` (`CONTRIBUTING_ROLE`), `role.project_development_lead` (`LEAD_ROLE`).
- **Activities:** cash-flow and debt-schedule modelling; scenario and sensitivity analysis; assumptions-register maintenance; model integrity checking.
- **Artifact Contributions:** `artifact.financial_model`, `artifact.financial_model_assumptions_register`, `artifact.financial_model_integrity_report` — all owned by `role.financial_modelling_specialist`.
- **Knowledge-State Expectations:** model outputs are `CALCULATION` resting on labelled `ASSUMPTION` inputs. **Any assumption still `UNKNOWN` from S1 remains visible here** and is not silently defaulted.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.financial_model` (mandatory at Enhanced and above); `HUMAN_GATE_REFERENCE` → `decision.financial_model_external_reliance` where the model will leave the organisation.
- **Exit Criteria:** model runs against the S2–S3 basis; assumptions register complete and traceable to source; integrity position stated; open items carried.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an `UNKNOWN` assumption that materially moves a model output is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S5 and S7. It is not defaulted, not averaged and not cleared by advancing.

### Stage `S5` — Bankability and risk position
- **Objective:** test the modelled project against financier requirements and against a quantified risk position.
- **Entry Criteria:** S4 exited; funding route candidates identified.
- **Participating Roles:** `role.funding_bankability_architect`, `role.enterprise_project_risk_specialist` (both `CONTRIBUTING_ROLE`); `role.insurance_risk_transfer_specialist` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(insurance programme material to bankability or risk allocation)`); `role.project_development_lead` (`LEAD_ROLE`).
- **Activities:** bankability assessment against lender requirements; funding strategy development; risk identification, quantification and allocation analysis; insurance programme analysis where triggered.
- **Artifact Contributions:** `artifact.bankability_assessment`, `artifact.funding_strategy`, `artifact.financing_readiness_roadmap` (owned by `role.funding_bankability_architect`); `artifact.risk_register`, `artifact.risk_quantification_analysis`, `artifact.risk_allocation_matrix` (owned by `role.enterprise_project_risk_specialist`); `artifact.insurance_programme_design` (owned by `role.insurance_risk_transfer_specialist`).
- **Knowledge-State Expectations:** `DRAFT`; residual risks that cannot be quantified are `UNKNOWN`, never omitted.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.bankability`, `review.risk_quantification`, `review.insurance_adequacy`; `HUMAN_GATE_REFERENCE` → `decision.funding_strategy_adoption`, `decision.risk_acceptance`, `decision.risk_allocation_adoption`.
- **Exit Criteria:** bankability gaps named; risk position quantified or explicitly `UNKNOWN`; allocation proposal stated without being adopted.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unquantifiable risk that bears on the bankability position or on `decision.risk_acceptance` is `MATERIAL_TO_NEXT_STEP_OR_GATE`. Recording it as `UNKNOWN` makes it visible, not disposed of.

### Stage `S6` — Integration and coherence check
- **Objective:** assemble the specialist positions into one readiness picture and surface every contradiction **between** them — the one thing no single specialist Role can do.
- **Entry Criteria:** S2–S5 exited.
- **Participating Roles:** `role.project_development_lead` (`LEAD_ROLE`); every `CONTRIBUTING_ROLE` from S2–S5 re-engaged to confirm its own position; `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`).
- **Activities:** cross-workstream coherence checking; contradiction identification; traceability of every readiness claim to its owning artifact; consolidation of open items and assumptions.
- **Artifact Contributions:** `artifact.development_readiness_assessment` (owned by `role.project_development_lead`) — assembled **from** the specialist artifacts, citing each, never restating a specialist conclusion in the lead's own voice; `artifact.evidence_integrity_record` updated by `role.knowledge_evidence_steward`.
- **Knowledge-State Expectations:** a contradiction between two specialist positions is raised as `CONFLICT_DETECTED` and **blocks or branches**; it is not averaged, reconciled by the lead, or narrated away.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.project_integration_coherence`, `review.project_readiness`, `review.evidence_integrity_provenance`.
- **Exit Criteria:** every readiness claim traced to an owning artifact and Role; every conflict either resolved by the owning Roles or carried as an explicit open item; assumption register current.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** every unresolved `CONFLICT_DETECTED` between two specialist positions is `MATERIAL_TO_NEXT_STEP_OR_GATE` without exception — a contradiction the readiness assessment would have to paper over cannot exit as `COMPLETE_WITH_OPEN_ITEMS`. The outcome is `REWORK_REQUIRED` or `ESCALATED`.

### Stage `S7` — Gate preparation
- **Objective:** present the readiness position so a human can decide — including presenting the reasons not to.
- **Entry Criteria:** S6 exited; required reviews for the criticality band satisfied or their absence explicitly recorded.
- **Participating Roles:** `role.project_development_lead` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`).
- **Activities:** assemble the gate package; state the open items, unresolved assumptions and gate-critical risks at the front, not the annex; state what the position does **not** establish.
- **Artifact Contributions:** `artifact.development_readiness_assessment` finalised as a `DRAFT` decision input; `artifact.programme_stage_gate_readiness` where a programme gate applies.
- **Knowledge-State Expectations:** the package remains `DRAFT` or `REVIEWED`. It does **not** become `APPROVED` by reaching this stage.
- **Gate / Review References:** `HUMAN_GATE_REFERENCE` → `decision.stage_gate_progression`; additionally `decision.project_definition_freeze`, `decision.feasibility_acceptance`, `decision.business_case_approval` and `decision.investment_or_financing_use` where the instance reaches them. Where the package is transmitted externally, the artifact's own `Transmitting Act` gate is preserved under `standard.workflow.common_constraints` §8.
- **Exit Criteria:** the gate decision is **due** and the decision-maker has what they need, including the open items.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `ESCALATED`, `CANCELLED`.
- **Open-Item Materiality:** any open item bearing on the evidence basis of `decision.stage_gate_progression`, or on a transmitting act where the package is issued externally, is `MATERIAL_TO_NEXT_STEP_OR_GATE`. Such an item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit; the outcome is `BLOCKED` or `ESCALATED` unless a **named external human Decision Right** explicitly permits the gate to be reached with it unresolved — in which case the gate reference is recorded and the item stays open.

## Branches / Exception Paths

- `BRANCH` — **sector specialisation triggered:** where the project is in a covered sector, `role.sector_technical_expert` is engaged at S2 and the corresponding sector Specialisation activates for `role.technical_feasibility_lead`.
- `BRANCH` — **public exposure triggered:** where procurement, State Aid or a public counterparty is present, `role.procurement_state_aid_specialist` is engaged at S3 and the criticality band is re-tested.
- `BRANCH` — **no external financing:** where no lender or investor is involved, S5's bankability half is reduced to a funding-route position; the risk half is **not** reduced.
- `EXCEPTION_PATH` — **material input superseded:** a `SUPERSEDED` input to any completed stage returns the dependent stages to `REWORK_REQUIRED`. It does not permit proceeding on the stale input.
- `EXCEPTION_PATH` — **unresolvable specialist conflict:** `ESCALATED` out of the Workflow. The lead may not adjudicate between two specialist Roles' conclusions.
- `EXCEPTION_PATH` — **gate deadline pressure:** exits as `COMPLETE_WITH_OPEN_ITEMS` with the items visible, or `BLOCKED`. It never exits by dropping a review or gate reference. There is no expedited path around `decision.stage_gate_progression`.

No exception path bypasses any `HUMAN_GATE_REFERENCE` or `REVIEW_REQUIRED_REFERENCE` carried by the normal path.

## Rework Rules

`REWORK_LOOP` targets: S6 → S2/S3/S4/S5 on a discovered contradiction; S4 → S2/S3 on an invalidated input; S5 → S4 on a model change; any stage → S1 where the evidence base itself is found unsound.

Across every loop, the prior artifact versions, their knowledge states, the evidence links, the open items and the reason for rework are preserved. A rework loop may not be used to retire an inconvenient prior finding.

## Open-Item Materiality

For this Workflow's terminal gate, `MATERIAL_TO_NEXT_STEP_OR_GATE` covers: any unresolved specialist conclusion the readiness position relies on; any `CONFLICT_DETECTED` between specialist positions; any `ASSUMPTION` that materially moves a gate-critical output; any missing `review.<id>` the criticality band requires; and any item bearing on a transmitting act where the package is issued to lenders, investors or authorities.

**A material item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit at the progression it is material to.** The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.

The only exception is a **named external human Decision Right** that explicitly permits proceeding with that item unresolved. Where it applies, this Workflow records the `decision.<id>` reference and the item **remains open and unresolved** — it is not relabelled resolved and not removed from the carry-forward. This Workflow does not decide the waiver, does not define its conditions and does not assert that it was granted. Who holds such a right and what granting it means is Phase 7.

## Completion Criteria

`COMPLETION_CRITERION` — S7 exited with the gate decision due, every readiness claim traced to an owning Role's artifact, every open item and unresolved assumption visible, and every required review either satisfied or its absence recorded.

Completion is a coordination position. It is **not** approval, not a readiness *decision*, and not a statement that the project is ready.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the project is discontinued; the forward gate is withdrawn or replaced; a precondition is found to be false in a way no rework can repair; or a human decision stops the preparation.

On cancellation, all artifacts, evidence, provenance, open items and gate records are retained. Artifacts that reached a governed state keep it.

## Outputs / Resulting Artifact States

| Artifact | Owning Role | State at completion |
|---|---|---|
| `artifact.development_readiness_assessment` | `role.project_development_lead` | `DRAFT` or `REVIEWED` |
| `artifact.feasibility_study`, `artifact.technical_basis_of_design` | `role.technical_feasibility_lead` | `DRAFT` or `REVIEWED` |
| `artifact.demand_study` | `role.commercial_demand_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.cost_estimate`, `artifact.contingency_analysis` | `role.capex_cost_engineering_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.financial_model` and register | `role.financial_modelling_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.bankability_assessment`, `artifact.funding_strategy` | `role.funding_bankability_architect` | `DRAFT` or `REVIEWED` |
| `artifact.legal_analysis` | `role.legal_regulatory_lead` | `DRAFT` or `REVIEWED` |
| `artifact.es_impact_assessment` | `role.esg_es_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.risk_register` and quantification | `role.enterprise_project_risk_specialist` | `DRAFT` or `REVIEWED` |
| `artifact.evidence_integrity_record` | `role.knowledge_evidence_steward` | `DRAFT` or `REVIEWED` |

No artifact reaches `APPROVED` or `CANONICAL` through this Workflow.

## Authority / Review Boundary

This Workflow owns no professional conclusion. Specifically:

- `role.project_development_lead` leads it and **does not absorb** the specialist conclusions — the feasibility, demand, cost, financial, bankability, legal, E&S or risk conclusions. Its `artifact.development_readiness_assessment` **cites** those positions; it does not restate them as its own. Where the assessment and a specialist artifact disagree, the specialist artifact governs and the assessment is defective.
- No stage performs an independent review. Every `review.<id>` above is a **requirement reference** to be defined by the later Review Profile Registry.
- No stage makes, satisfies or bypasses a decision right. `decision.stage_gate_progression` and every other gate referenced above is a **human decision right**, held outside this Workflow and neither exercised nor satisfied by reaching the stage that makes it due.
- **Participation in this Workflow grants no professional authority.** A Role gains nothing beyond its own Role Card by participating, including at `LEAD_ROLE`.

## Criticality Scaling

| Band | Effect |
|---|---|
| Routine / Standard | S1–S4 and S6–S7; S5 reduced to a funding-route position where no external financier is involved; review references advisory. |
| Enhanced Review Candidate | Full stage set; `review.cost_estimate` and `review.financial_model` become expected; assumption register mandatory at S4. |
| Enhanced Decision-Grade (automatic at €50m, or on any complexity trigger) | Full stage set mandatory; `artifact.project_definition_document` must be `REVIEWED` before S4; `review.financial_model`, `review.project_readiness` and `review.evidence_integrity_provenance` mandatory; traceability required claim-by-claim at S6. |
| Major / Systemic | As Enhanced Decision-Grade, plus mandatory `review.project_integration_coherence` and specialist escalation at S6, and no `COMPLETE_WITH_OPEN_ITEMS` exit at S7 for gate-critical items. |

Criticality changes depth, review intensity and mandatory stage set. **Role identity does not change**, and criticality does not create a second Workflow — there is no separate large-project or small-project variant of this pattern.

## Evidence / Traceability Requirements

At completion: every readiness claim traceable to a named artifact and owning Role; every assumption traceable to the S1 register with its current status; every calculation traceable to its model version; every source verified or recorded `UNKNOWN`; every conflict recorded with its disposition; every rework loop recorded with its reason; every gate reference recorded as due, satisfied or explicitly not reached.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no authority, Role scope, gate or artifact-ownership change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
