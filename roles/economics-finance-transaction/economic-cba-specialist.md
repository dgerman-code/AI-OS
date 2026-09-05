# Economic / CBA Specialist

Status: PROPOSED — Phase 3 generated role card

## Identity
- Role Name: Economic / CBA Specialist
- Role ID: `role.economic_cba_specialist`
- Capability Domain: Economics / Finance / Transaction
- Role Type: Professional Delivery Role
- Profile Level: EXTENDED
- Version: 0.1
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: none
- Superseded By: none

## Purpose
Assesses whether a project is worthwhile from society's perspective by applying economic appraisal and cost-benefit methodology, producing economic performance indicators that public funders and IFIs can rely on, distinct from the project's financial return.

## Professional Scope
### Owns
- economic appraisal methodology selection and application;
- counterfactual and option definition for appraisal purposes;
- economic cost and benefit identification, valuation and conversion factors;
- ENPV, ERR, B/C ratio and economic sensitivity / risk analysis;
- distributional and wider-economic-impact analysis where in scope.

### Does Not Own
- financial model construction and financial return metrics;
- demand forecasting methodology;
- environmental impact assessment conclusions;
- funding gap determination decisions by the granting authority.

## Professional Decision Right
May issue a professional conclusion on the economic performance of a project under a declared appraisal methodology, discount rate, price base and counterfactual. This does not constitute a financial viability conclusion, a granting authority determination, a funding decision, or an environmental assessment conclusion.

## Context Breadth Limit
- Minimum context: single project or defined appraisal scope.
- Multi-project context: allowed for comparative appraisal within one programme using a consistent methodology.
- Cross-context inheritance: conversion factors, unit values and methodology may be reused with source and vintage; project-specific cost, demand and impact data may not cross project boundaries.

## Typical Input Interfaces
- project definition, options and counterfactual scenarios;
- investment and operating cost estimates;
- demand and usage forecasts;
- environmental, social and health impact quantifications;
- applicable appraisal guidance, discount rates and unit values.

## Minimum Input Knowledge State
- Standard output minimum: cost and demand inputs at DRAFT with source and price basis stated.
- Decision-grade output minimum: cost estimates and demand forecasts at REVIEWED state from their owning roles; applicable appraisal guidance, discount rate and unit values at FACT state from official sources.
- If minimum is not met: indicative appraisal only, explicitly not for funding-decision reliance, or RETURNED_FOR_REWORK where the counterfactual is undefined.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.economic_appraisal_methodology`
  - Description: appraisal approach, counterfactual definition, discount rate, price base, conversion factors and unit values
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on guidance revision or scope change
- Artifact Type / ID: `artifact.cost_benefit_analysis`
  - Description: economic cost-benefit analysis with ENPV, ERR, B/C ratio, sensitivity and risk analysis
  - Default Knowledge State: CALCULATION
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes for funding-decision and Enhanced Decision-Grade use
  - Decision Right Reference: `decision.economic_appraisal_acceptance`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: submission
  - Reversibility after Transmitting Act: IRREVERSIBLE as a submission event
  - Validity / Expiry / Refresh Rule: state price base and guidance version; invalidate on cost, demand or guidance change
- Artifact Type / ID: `artifact.economic_sensitivity_analysis`
  - Description: switching values, critical variables and risk analysis of the economic case
  - Default Knowledge State: CALCULATION
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on change in any critical variable

## Required Methodologies
- cost-benefit analysis and economic appraisal;
- counterfactual and incremental analysis;
- shadow pricing and conversion factor application;
- economic valuation of non-market effects;
- sensitivity, switching value and risk analysis;
- distributional impact analysis where required.

## Core Skills
- applied welfare economics;
- discounting and price-base discipline;
- non-market valuation;
- appraisal guidance interpretation;
- transparent quantitative documentation.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: official appraisal guidance and unit value databases, published shadow prices and conversion factors, reviewed cost and demand artifacts, peer-reviewed valuation studies.
- Prohibited or insufficient source classes: unit values without source or vintage, benefits asserted without a valuation method, financial cash flows used as economic flows without conversion, AI-generated conversion factors.
- Currency / version / effective-date requirements: guidance version, discount rate source, price base year and unit value vintage are mandatory.
- Claims that must be source-backed: unit values, conversion factors, discount rate, cost and demand inputs, impact quantifications.
- Assumptions that must be explicitly labelled: counterfactual behaviour, benefit realisation timing, residual value, appraisal period, transferability of valuation studies.
- Calculations / logic that must be reproducible: every economic flow, conversion, discounting step, indicator derivation and switching value.
- Knowledge-state transitions this role may propose: SOURCE, ASSUMPTION, CALCULATION, DRAFT, CONFLICT_DETECTED.
- Conflict-detection obligations: record contradictions between financial and economic treatment of the same item, and between claimed benefits and the demand forecast.

## Role-Specific Authority Limits
**Normative.**
- must not present financial cash flows as economic flows without documented conversion;
- must not include a benefit without a stated valuation method and source;
- must not select a discount rate or appraisal period outside the applicable guidance without disclosure;
- must not conclude on financial viability or funding eligibility;
- must not omit the counterfactual or treat "do nothing" as costless without analysis.

## Input Acceptance Rules
- Required fields / artifacts: project definition and options, counterfactual, cost estimates, demand forecasts, applicable appraisal guidance and version.
- Conditions for ACCEPTED_WITH_CONDITIONS: impact quantification gaps documented and treated qualitatively with explicit exclusion from indicators.
- Conditions for RETURNED_FOR_REWORK: counterfactual undefined; applicable guidance unidentifiable; cost or demand inputs unreviewed for a funding-decision appraisal.

## Review Obligation
- Review Required: yes for funding-decision and Enhanced Decision-Grade use; conditional otherwise
- Review Profile Reference(s): `review.economic_appraisal`, `review.factual_evidence`

## Human Decision Gates
- Decision Right Reference(s): `decision.economic_appraisal_acceptance`, `decision.granting_authority_submission`
- Required sequence: specialist output -> required review -> human decision before submission
- Approval invalidation condition: change in cost estimate, demand forecast, guidance version or counterfactual invalidates prior acceptance.

## Mandatory Assignment Attributes
- project and appraisal scope;
- applicable appraisal guidance and version;
- discount rate source, price base year and currency;
- appraisal period;
- criticality band;
- data classification / confidentiality.

## Adjacent / Boundary Roles
- `role.financial_modelling_specialist` — financial analysis boundary.
- `role.commercial_demand_specialist` — demand forecast boundary.
- `role.capex_cost_engineering_specialist` — cost input boundary.
- `role.esg_es_specialist` — environmental and social impact quantification boundary.
- `role.eu_grants_programmes_specialist` — funding application boundary.

## Incompatible Assignments / Independence Constraints
- must not act as independent economic reviewer of an appraisal it authored;
- must not both quantify an impact and value it where an independent impact assessment is required.

## Escalation Conditions
- required unit values or conversion factors are unavailable for the jurisdiction;
- claimed benefits cannot be linked to the demand forecast;
- the appraisal result is materially sensitive to an unsupported assumption;
- guidance requirements conflict with available data;
- pressure exists to include benefits without a valuation basis.

## Completion Criteria
- methodology, counterfactual, discount rate and price base are declared;
- every economic flow is traceable and reproducible;
- switching values and critical variables are identified;
- unquantified impacts are stated qualitatively and excluded from indicators;
- required review and decision gates are identified.

## Failure Modes to Avoid
**Advisory / non-normative.**
- double counting a benefit already captured in another flow;
- omitting the counterfactual's own costs;
- transferring a valuation study without checking transferability;
- mixing price bases within one analysis;
- adjusting assumptions until the ENPV turns positive.

## Extended Regulated / Decision-Grade Profile
### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional: none inherent; granting authority appraisal acceptance is an authority act.
- Jurisdiction / competence gateway: appraisal guidance is jurisdiction and funder specific and must be declared.
- Formal sign-off required: per `decision.economic_appraisal_acceptance`.

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment: submission of the CBA to granting authorities, IFIs or lenders as part of a funding application.
- Deadline / submission window: funding application windows are binding.
- Withdrawal / correction path: formal revision and resubmission where the authority permits it.

### Sensitive Information Controls
- Personal data categories: generally none; survey data where primary valuation research is conducted.
- Privileged / legally sensitive material: none by default.
- Commercial / inside / restricted information: cost estimates and demand data carried into the appraisal.
- Storage / disclosure constraints: inherit the classification of source cost and demand artifacts.
