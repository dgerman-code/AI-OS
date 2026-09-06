# Project Finance Metrics Pack

Status: PROPOSED — Phase 4 exemplar Skill Pack Card

## Identity
- Pack Name: Project Finance Metrics
- Pack ID: `skill_pack.project_finance_metrics`
- Type: Skill Pack
- Pack Class: `METHOD`
- Contributing Skill Families: Finance & Economics
- Included Specialisations: `specialisation.dscr`, `specialisation.llcr`, `specialisation.plcr`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Effective Date: on approval of this card
- Review Date: with the Phase 4 registry review cycle
- Expiry / Invalidation Trigger: see Deactivation / Invalidation Criteria
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose
Hold the governed definitions and calculation conventions for project-finance coverage metrics together, so that a ratio quoted in a model means the same thing across assignments and can be reconciled with what a lender expects.

Debt service coverage, loan life coverage and project life coverage are all sensitive to convention — what sits in cash flow available for debt service, whether ratios are pre- or post-tax, how a reserve account is treated, which discount rate a life-coverage ratio uses. Two defensible conventions produce materially different numbers. Bundling them makes the convention set explicit and versioned instead of implicit in whoever built the model.

## Scope
### Covers
- governed metric definitions for DSCR, LLCR and PLCR, each with its numerator, denominator and period convention stated;
- calculation conventions: cash flow available for debt service composition, tax treatment, reserve-account treatment, discount basis for life-coverage ratios, period granularity and averaging;
- covenant-analysis method: lock-up and default threshold testing, headroom measurement, cure-period treatment;
- sensitivity and break-even method against covenant thresholds;
- reconciliation method between metric outputs and the underlying model;
- explicit convention-divergence reporting where an institution's expected convention differs from the one applied.

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model/runtime selection;
- any Role scope not already granted by the assigned Role Card.

Specifically **not** covered:
- **Funding and bankability conclusions.** Whether a structure is bankable is owned by `role.funding_bankability_architect`. A DSCR above a threshold is an input to that conclusion, not the conclusion.
- **Transaction and financing-close authority.** Owned by `role.project_finance_transaction_specialist` and gated by `decision.financing_terms_acceptance` and `decision.financial_close`.
- **Lender commitments.** No metric output commits any lender or represents any lender's acceptance. Lender engagement is gated by `decision.lender_engagement`.
- **Financial model ownership.** The model itself is `artifact.financial_model`, owned by `role.financial_modelling_specialist` and gated for external reliance by `decision.financial_model_external_reliance`.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.financial_modelling_specialist`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, section 5

`role.funding_bankability_architect`, `role.project_finance_transaction_specialist`, `role.ppp_concession_specialist` and `role.ifi_dfi_project_preparation_specialist` all consume these metrics and their Role Cards support the domain, but none is mapped to this Pack in the current record. They are Wave 2 mapping decisions, not assumptions to be made here.

Listing a Role confers eligibility, never a requirement.

### Typical Use — Advisory, Non-Authoritative
Non-binding: usually relevant where a project-finance structure or a lender-facing debt model is in scope. States no obligation; the mapping record decides.

## Included Skills
### Required Skills
- `skill.debt_schedule_modelling` — coverage ratios are undefined without a debt service profile.
- `skill.project_finance_ratio_analysis` — the ratio analysis technique the Pack supplies governed conventions to.

### Optional Skills
- `skill.sensitivity_analysis`
- `skill.financing_scenario_analysis`
- `skill.discounted_cash_flow_analysis`
- `skill.cash_flow_modelling`

### Alternative Skills
None.

## Pack Dependencies and Layering
- Depends on / layers over: none.
- Depended on by (informational): none currently. An institution Pack may later layer institution-specific covenant conventions over this method Pack; the dependency would be declared on the institution Pack, in that direction only.
- Layering metadata: not applicable.

No circular dependency is possible for this Pack, since it declares none.

## Precedence With Overlapping Packs
Where another active Pack addresses the same subject with different requirements:
1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** Pack prevails — an institution Pack's covenant convention prevails over this generic method Pack;
3. where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate rather than resolving silently;
4. the Role Card and any stricter workflow or assignment control prevail over this Pack.

Precedence never operates in the permissive direction. Where an institution requires a stricter CFADS definition than this Pack's default, the institution's applies and the divergence is reported rather than absorbed.

## Duplicate Effective Activation
`skill.project_finance_ratio_analysis` is the live case. The Wave 1 mapping deliberately does **not** map it individually to `role.financial_modelling_specialist` precisely because it is a required Skill of this Pack, and mapping both would duplicate the activation.

Where a Skill in this Pack is also mapped individually to the same Role — as `skill.debt_schedule_modelling` currently is — it is activated **once**, under the **stricter** of the two obligations, with this Pack's conventions applied on top. The individual mapping is retained only where it has meaning independent of this Pack, which it does for debt schedule modelling, since debt schedules exist outside project finance.

Duplicate effective activation must be detectable at validation time, not discovered during execution.

## Authority Limits of Activation
Activating this Pack **cannot** satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

Those obligations are discharged only through the assigned Role Card, the applicable Review Profile and the applicable Decision Right.

## Applicability
- Jurisdiction(s): unrestricted; jurisdiction affects tax treatment within the conventions.
- Sector(s): unrestricted; commonly infrastructure, energy and utilities.
- Programme / framework: not applicable.
- Institution / financing framework: unrestricted, but an institution's own conventions prevail where they apply.
- Technology / version: not applicable.
- Operating context: project-finance structuring, lender-facing modelling, covenant testing.
- Criticality conditions: at Enhanced Decision-Grade and above, convention divergence from the expected lender basis must be explicitly reported.
- Assignment prerequisites: a debt structure and a cash-flow model must exist.

## Controlled Methodology / Source Package
Required at instantiation, each captured with source / authority, title / identifier, version, effective date, expiry or supersession status, and applicability:
- the applicable financing or facility agreement definitions where a transaction exists, which override generic convention;
- the institution's or lender's stated ratio definitions and covenant conventions where a lender is identified;
- the accounting basis underlying the model's statements;
- the applicable tax basis;
- the organisation's own approved convention set where no external one governs.

**AI-generated content must not be listed as a controlled source.** A metric convention adopted because a model produced it, rather than because a governing document states it, is not governed.

## Evidence Requirements
- Required evidence classes: the model and its assumption register; the debt terms; the governing definition source for each metric.
- Minimum source quality: executed or draft facility documentation where it exists; otherwise the institution's published convention or the organisation's approved set.
- Required provenance: every convention traceable to a named source, not to practice.
- Currency requirements: conventions current for the transaction stage.
- Assumptions that must remain explicit: every convention choice not fixed by a governing document.
- Reproducibility requirements: each ratio reproducible from the model and the stated conventions alone.

## Knowledge-State Constraints
- Minimum input state for ordinary use: model inputs may be DRAFT if labelled and outputs are explicitly preliminary.
- Minimum input state for decision-grade use: the model at REVIEWED with material specialist inputs REVIEWED or APPROVED; debt terms at FACT where a term sheet exists.
- States the Pack may support deriving: CALCULATION for ratio outputs; ASSUMPTION for convention choices; CONFLICT_DETECTED where conventions are incompatible; UNKNOWN where a governing definition is unavailable.
- States the Pack may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict / contradiction escalation rule: where the facility definition, the lender's stated expectation and the model's implemented convention diverge, raise `CONFLICT_DETECTED`. Never reconcile by adopting the convention that produces the more favourable ratio.

Skills in this Pack may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review Dependencies
- Review Profile Reference(s): none at Pack level; resolved by the consuming Role and workflow. The consuming Financial Modelling assignment carries `review.financial_model`.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not perform independent assurance by identity.

Any reconciliation, validation or checking capability included in this Pack is a **quality-control technique, not independent review**. It does not discharge a `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation and creates no reviewer identity. Reconciling ratios to the model is a self-check, not model review.

## Decision Dependencies
- Decision Right Reference(s): none at Pack level; resolved by the consuming Role and workflow. The consuming assignment carries `decision.financial_model_external_reliance` and `decision.investment_or_financing_use`.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not acquire human authority.

## External / Regulated Boundary
- Licensed / regulated activity boundary: none intrinsic; financial promotion and advice boundaries are the consuming Role's.
- Required authorised professional class: as required by the consuming Role and jurisdiction.
- External submission / filing / publication boundary: providing ratios to a lender is an external act gated by `decision.lender_engagement` and, for model reliance, `decision.financial_model_external_reliance`.
- Production / deployment boundary: not applicable.
- Withdrawal / correction path: restatement through the model owner; a ratio relied on externally cannot be silently corrected.

## Data / Confidentiality Controls
- personal data categories: none ordinarily.
- privileged / legally sensitive information: draft facility terms.
- commercial / restricted information: pricing, margins, covenant levels and sponsor returns.
- storage / residency requirements: per the transaction's confidentiality regime.
- cross-context reuse restrictions: covenant levels and conventions from one transaction must not be imported into another as defaults.

## Version and Change Control
A new Pack version is required on material change in: metric definitions or conventions; covenant-analysis method; the accounting or tax basis assumed; required skill composition; compatible Role set; evidence requirements; or review / decision dependencies.

## Activation Criteria
Financing structure is project finance, **or** a lender-facing debt model is in scope.

## Deactivation / Invalidation Criteria
- the financing structure ceases to be project finance;
- an executed facility agreement supersedes the assumed definitions, requiring rebinding;
- the institution's stated conventions change;
- the underlying model is superseded.

A stale Pack must not silently satisfy a contextual mapping obligation.

## Pack Integrity Rules
- Required Skills must be present when the Pack is activated unless an explicit governed exception exists.
- Optional Skills do not widen Role authority.
- Pack activation must not silently import covenant levels or conventions from another transaction.
- Controlled references must be current for the assignment date.
- Where Pack requirements conflict with the Role Card or a stricter workflow control, the stricter rule prevails and the conflict is escalated.

## Prerequisites and Incompatibilities
- Prerequisite capabilities or Packs: a cash-flow model and a debt structure must exist. Competence statements only; confer no authority.
- Incompatibilities: must not be used to present coverage ratios as a bankability or financeability conclusion.

## Adjacent Packs
- `skill_pack.ifi_financial_appraisal` — generic IFI appraisal method; where an institution-specific Pack applies, that Pack governs and this one supplies metric conventions only.

## Completion / Use Criteria
Properly applied when every metric's definition and convention set is stated and traced to a governing source; divergence from a lender's expected convention is reported rather than absorbed; ratios reconcile to the model; covenant headroom is measured against stated thresholds; and no ratio is presented as a financing conclusion.

## Failure Modes to Avoid
- Quoting a ratio without its convention set.
- Adopting the convention that produces the more favourable result.
- Carrying covenant levels between transactions as defaults.
- Presenting coverage headroom as evidence of bankability.
- Treating ratio-to-model reconciliation as model review.

## Reclassification Warning
If the Pack begins to own a recurring standalone professional artifact, professional conclusion or authority boundary independent of an assigned Role, stop and reassess whether the capability belongs in the Role Registry instead.
