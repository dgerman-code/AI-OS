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

| `role.<id>` | Eligibility class | Scope basis in its Role Card | Dimension covered |
|---|---|---|---|
| A second `role.financial_modelling_specialist` instance that did not build this model | `FULL_PROFILE_REVIEWER_ELIGIBLE` | Owns financial modelling methodology — the whole of this Profile's satisfaction criteria | All |
| `role.accounting_financial_due_diligence_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns reconciliation, normalised-earnings analysis and financial evidence discipline; **its Role Card does not cover financial-model integrity or modelling methodology** | Reconciliation, accounting tie-out, evidence consistency and due-diligence dimensions only |
| `role.funding_bankability_architect` | `BOUNDED_REVIEW_CONTRIBUTOR` (`CROSS_DOMAIN_REVIEW`) | Owns bankability reasoning from model outputs, not model construction | Whether outputs support the bankability use they are put to — **cannot conclude on model integrity** |

**Full Profile satisfaction rests solely with the first row**, whose approved scope includes financial modelling methodology. The two bounded contributors check their own dimension only, and their contributions do not aggregate into full-Profile satisfaction. An earlier revision listed the accounting Role without that bound, which would have given it model-integrity authority its Role Card does not grant.

## Reviewer Instance Segregation

**`SEGREGATION_REQUIRED` at Enhanced Decision-Grade and above**; `ALLOWED_IF_INDEPENDENTLY_ELIGIBLE` below it.

The model's inputs are themselves separately reviewed — `review.cost_estimate` over the cost basis, `review.engineering_technical` over the technical basis — and those domains are interdependent with the model that consumes them. At decision-grade, one instance satisfying both the model Profile and an input Profile would let a single reading of an assumption pass twice as two independent checks. Below that band the concentration risk is proportionate and same-instance satisfaction is permitted where each Profile's eligibility and independence pass separately.

## Review Dependencies

| Prerequisite `review.<id>` | Required status | Activation condition | Bounded purpose |
|---|---|---|---|
| `review.cost_estimate` | `SATISFIED` | The model consumes `artifact.cost_estimate` **and** the band is Enhanced Decision-Grade or above | The model's cost inputs are sound before model integrity is assessed against them |
| `review.evidence_integrity_provenance` | `SATISFIED` | Band is Enhanced Decision-Grade or above | The assumption register's sources are traceable before the register is reconciled to the model |

An unsatisfied or `STALE` prerequisite makes this review `REVIEW_BLOCKED`, not failed — the model may be perfectly sound and simply not yet assessable. **Neither prerequisite contributes to this Profile's satisfaction**: this review still evaluates model integrity entirely on its own criteria, and a satisfied `review.cost_estimate` says nothing about whether the model is correctly built.

## Reviewer Prohibitions

- The `role.financial_modelling_specialist` instance that built or extended the model in this assignment;
- either `BOUNDED_REVIEW_CONTRIBUTOR` above, as a **satisfier of this Profile**;
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
