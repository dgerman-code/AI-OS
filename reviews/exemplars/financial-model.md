# Financial Model Review

Status: PROPOSED — Phase 6 exemplar Review Profile Card
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: Financial Model Review
- Review ID: `review.financial_model`
- Version: 0.1
- Status: PROPOSED
- Review Family: Finance / Economics
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

A financial model is the artifact most likely to be relied on by people who cannot inspect it. This review verifies that the model is internally sound, that its assumptions are visible and owned, and that its outputs are traceable to its inputs — **without endorsing the assumptions themselves or the investment they support.**

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.financial_model` | `role.financial_modelling_specialist` |
| `artifact.financial_model_assumptions_register` | `role.financial_modelling_specialist` |
| `artifact.financial_model_integrity_report` | `role.financial_modelling_specialist` |

## Applicability / Trigger

Required whenever the model will be relied on outside the producing team, and always before external reliance. **Mandatory at Enhanced Decision-Grade and above**, and mandatory whenever `decision.financial_model_external_reliance` is in prospect.

## Required Evidence Package

The model at a stated version; the assumptions register with basis, owner and source per assumption; the integrity report; the input artifacts the model consumes (`artifact.demand_study`, `artifact.cost_estimate`, `artifact.technical_basis_of_design` and their states); scenario and sensitivity definitions; a statement of what the model does not represent.

## Independence Class

`PEER_REVIEW` at Enhanced Review Candidate; **`INDEPENDENT_ASSURANCE_REVIEW` at Enhanced Decision-Grade and above.**

## Reviewer Eligibility

- A second `role.financial_modelling_specialist` instance that did not build this model — the primary peer;
- `role.accounting_financial_due_diligence_specialist`, whose Role Card owns reconciliation and financial evidence discipline;
- `role.funding_bankability_architect` for `CROSS_DOMAIN_REVIEW` of whether outputs support the bankability use they are put to — **this class cannot conclude on model integrity itself.**

## Reviewer Prohibitions

- The `role.financial_modelling_specialist` instance that built or extended the model in this assignment;
- any Role that supplied an input assumption under review, over that assumption — it would be reviewing its own input;
- `role.project_development_lead` where it led the assignment and integrated the model into a readiness position;
- any reviewer whose independence rests only on model or runtime difference.

## Review Scope
### Checks
- structural integrity: no broken references, no circularity outside a declared and controlled resolution, no hard-coded values inside calculated ranges;
- every assumption is in the register with a basis, a source and a named owner;
- every output traces to inputs by a stated method;
- scenario and sensitivity logic behaves as declared;
- `UNKNOWN` inputs are visible as such and not silently defaulted;
- the model's stated limitations match what it actually does not represent;
- version identity is unambiguous and matches the inputs relied on.

### Does Not Check
- **whether the assumptions are right** — each assumption's substance is owned by the Role that supplied it, and reviewed under `review.cost_estimate`, `review.engineering_technical`, `review.esg_safeguards` or the applicable domain review;
- **whether the project is financeable** — `review.bankability`;
- whether the economic case is sound — `review.economic_appraisal`;
- whether the accounting treatment is correct — `review.tax_analysis` and the accounting Role's own surface;
- whether the evidence under the inputs is traceable — `review.evidence_integrity_provenance`.

## Method at Architecture Level

Independent reconstruction of selected calculation paths, register-to-model reconciliation, structural integrity testing, and behaviour testing of declared scenarios. Not a re-build of the model and not a second opinion on the investment.

## Finding Taxonomy Application

| Class | Example here |
|---|---|
| `NO_FINDING` | Structure sound, register complete, outputs traceable |
| `OBSERVATION` | A naming or layout convention that does not impair traceability |
| `MINOR_FINDING` | An assumption with a source but no named owner |
| `MAJOR_FINDING` | An output that cannot be traced to inputs; an assumption absent from the register; a sensitivity that does not behave as declared |
| `CRITICAL_FINDING` | A structural defect that changes a headline output; a hard-coded value overriding a calculated one; an `UNKNOWN` silently defaulted to a favourable value |

## Satisfaction Criteria

`SATISFIED` when structure is sound, the register is complete and reconciles to the model, every material output traces, and stated limitations are accurate.

An unresolved `CRITICAL_FINDING` **can never be satisfied**. An unresolved `MAJOR_FINDING` blocks satisfaction; this Profile permits a **bounded conditional disposition** only where the finding is confined to a scenario branch not relied on by the decision in question, the confinement is stated, and a **named external Decision Right** governs any progression that relies on the model regardless. The Profile references that right and does not grant it.

**Satisfaction is not approval and is not a view on financeability.**

## Rework and Closure Requirements

`MAJOR` and `CRITICAL` route to `role.financial_modelling_specialist` for model defects, or to the supplying Role for input defects. Closure requires the corrected model at a new version, the updated register, and a statement of what changed. **Re-review is mandatory** after any `CRITICAL` closure and after any `MAJOR` closure that moved a headline output.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: any input artifact is superseded; an assumption material to a headline output changes; model structure changes; or the scenario set relied on changes.

## Criticality Scaling

| Band | Independence | Depth |
|---|---|---|
| Routine / Standard | `PEER_REVIEW`, advisory | Structural check and register completeness |
| Enhanced Review Candidate | `PEER_REVIEW`, expected | Selected calculation paths reconstructed |
| Enhanced Decision-Grade | `INDEPENDENT_ASSURANCE_REVIEW`, mandatory | All material paths reconstructed; register reconciled line by line |
| Major / Systemic | As above, plus mandatory re-review on any material input change | Full |

## Workflow / Handoff References

Carried as a `REVIEW_REQUIRED_REFERENCE` at `workflow.project_development_readiness` S4 and S6. Required `SATISFIED` before transfer where a downstream Handoff moves the model outside the producing team.

## Decision Right Boundary

Informs `decision.financial_model_external_reliance`, `decision.financing_terms_acceptance`, `decision.financial_close` and `decision.business_case_approval`. It makes none of them, and satisfaction does not make the model relied-upon — reliance is the human act.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no independence, severity or satisfaction change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
