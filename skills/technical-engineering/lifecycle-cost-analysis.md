# Lifecycle Cost Analysis

Status: PROPOSED — Phase 4 exemplar Skill Card

## Identity
- Skill Name: Lifecycle Cost Analysis
- Skill ID: `skill.lifecycle_cost_analysis`
- Type: `SKILL`
- Primary Skill Family: Technical / Engineering
- Secondary Skill Family Tags: Finance & Economics
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose
Compare technical options on a whole-life basis — capital, operating, maintenance, replacement and disposal implications over an asset's life — so that an option that is cheaper to build but more expensive to own is visible as such at the point the technical choice is made.

This card exists in its current form because the Wave 1 audit found a real boundary defect through it. The Technical / Feasibility Lead had been mapped to CAPEX and OPEX estimation, which put cost origination inside a Role that does not own it. Those mappings were removed and this Skill was demoted to OPTIONAL and support-only. The constraints below are the substance of that fix, not decoration.

## Capability Definition
### Enables
- whole-life cost structuring across capital, operating, maintenance, major-replacement and disposal phases;
- lifecycle comparison of technical options on a common basis and a stated horizon;
- discounting and present-value comparison where a discount basis is supplied;
- sensitivity of the option ranking to cost-input uncertainty;
- identification of the cost drivers that separate options, so that estimation effort can be directed;
- explicit statement of which comparisons cannot be made because a specialist cost input does not exist.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary

Inside: comparing technical options on cost inputs that already exist and are owned by someone else.

**Outside, and this is the operative constraint of this card:**

- **Cost and O&M inputs are specialist-owned.** This Skill consumes them; it never originates them.
  - CAPEX estimation, cost breakdown, basis of estimate and contingency are owned by `role.capex_cost_engineering_specialist`, whose artifacts are `artifact.basis_of_estimate`, `artifact.cost_estimate` and `artifact.contingency_analysis`.
  - Operating and maintenance cost basis, availability and maintenance regime are owned by `role.asset_om_technical_operations_specialist`, whose artifacts are `artifact.om_strategy`, `artifact.availability_and_lifecycle_basis` and `artifact.operating_cost_driver_definition`.
- **This Skill may never create an authoritative CAPEX or OPEX estimate.** Not by derivation, not by benchmark, not by scaling a figure from another project, not by filling a gap to complete a comparison.
- **This Skill may never issue a cost acceptance conclusion** and cannot satisfy `decision.cost_estimate_acceptance`.
- **Where a specialist-owned cost input does not exist, the comparison is reported as cost-unquantified.** Completing the analysis on self-generated figures is the specific failure this boundary prevents. An incomplete comparison that says so is correct; a complete comparison built on invented inputs is a boundary breach whatever its arithmetic.
- **Not a financial model.** Whole-life comparison for a technical decision is not a project financial model; that is owned by `role.financial_modelling_specialist` and gated by `decision.financial_model_external_reliance`.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.technical_feasibility_lead`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, section 4

`role.capex_cost_engineering_specialist` and `role.asset_om_technical_operations_specialist` are **not** listed. They own the cost inputs and would exercise whole-life reasoning through their own owned artifacts, not through a support-only Skill scoped to option comparison. Adding them would reintroduce exactly the ambiguity this card was tightened to remove.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant when two or more technically viable options differ materially in whole-life cost profile and specialist cost inputs for each option already exist. Where they do not exist, the correct action is to request them, not to proceed.

## Alternative Choice Set
- Choice set reference: none.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: `skill.technical_option_comparison`, which this Skill supplies a cost dimension to, and `skill.design_basis_definition`, since options must be defined to a comparable design maturity. Competence statements only; confer no authority.
- Incompatibilities: **must not be combined with cost origination.** Where the same assignment would have this Skill both generate and consume a cost figure, the assignment is invalid and the specialist Role is engaged instead.

## Methods / Techniques
- whole-life cost structuring by phase over a stated horizon;
- normalisation of options to a comparable design maturity and boundary;
- present-value comparison against a supplied discount basis;
- ranking-stability sensitivity to input uncertainty;
- cost-driver identification and differential analysis;
- explicit gap reporting where a required specialist input is absent.

## Inputs
- specialist-owned CAPEX inputs, at their owner's stated accuracy class and knowledge state;
- specialist-owned operating, maintenance and replacement cost inputs and the availability basis;
- the technical option set and its design maturity;
- horizon, discount basis and boundary conventions, supplied by the assignment;
- criticality band.

## Outputs / Contributions

Method-level contribution. The comparison is embedded in a Role-owned technical artifact; this Skill owns nothing.

- Role-owned artifacts this contributes to:
  - `artifact.feasibility_study` owned by `role.technical_feasibility_lead`;
  - `artifact.technical_basis_of_design` owned by `role.technical_feasibility_lead`.
- What this capability explicitly does **not** produce: `artifact.cost_estimate`, `artifact.basis_of_estimate`, `artifact.contingency_analysis`, `artifact.operating_cost_driver_definition`, `artifact.availability_and_lifecycle_basis`, any authoritative cost figure, or any cost acceptance conclusion.

## Support-Only Boundary
- Roles retaining ownership of the conclusion: `role.capex_cost_engineering_specialist` for capital cost; `role.asset_om_technical_operations_specialist` for operating, maintenance and availability basis.
- What this capability may produce: a whole-life comparison of technical options on inputs those Roles own, plus the sensitivity of the ranking to those inputs.
- What it may never produce: any cost figure presented as an estimate, any cost conclusion, or a comparison completed on inputs it generated itself.

## Independent Review Boundary

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

A lifecycle comparison does not discharge `review.cost_estimate` or `review.engineering_technical`; both are performed under their own profiles by someone who did not author the work.

## Evidence and Source Requirements
- Preferred source classes: specialist-owned cost artifacts at their stated accuracy class; vendor O&M requirements; measured performance data from identified sources; the assignment's stated discount and horizon conventions.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source**, and an AI-generated cost figure is not a cost input under any circumstances. Also prohibited as an estimate substitute: benchmarks from unrelated projects, scaled figures without a specialist basis, and vendor indicative pricing presented as an estimate.
- Currency / version requirements: cost inputs carry their base date, currency and escalation basis; comparison across inputs with different base dates without normalisation is invalid.
- Assumptions that must be explicit: horizon, discount rate, escalation, residual value, replacement intervals and boundary — each labelled ASSUMPTION unless supplied as an approved input.
- Reproducibility requirements: the comparison must be reproducible from the stated inputs and conventions alone.

## Knowledge-State Constraints
- Minimum acceptable input state: for a comparison informing a decision-grade technical conclusion, cost inputs must be REVIEWED or APPROVED by their owning Role. DRAFT or CALCULATION inputs may be used only for a preliminary comparison explicitly labelled non-decision-grade.
- States this Skill may help derive or propose: CALCULATION for the comparison; ASSUMPTION for every convention not supplied; UNKNOWN where a required input is absent.
- States this Skill may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict-detection obligations: where CAPEX and O&M inputs rest on incompatible design assumptions, or where a cost input contradicts the design basis, raise `CONFLICT_DETECTED` and escalate rather than reconciling the figures independently.

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Skill level; resolved by the consuming Role and workflow. The consuming Technical / Feasibility Lead assignment carries `review.engineering_technical` and `review.factual_evidence`.
- Decision Right Reference(s): none at Skill level; resolved by the consuming Role and workflow. The consuming assignment carries `decision.technical_basis_freeze` and `decision.feasibility_acceptance`; `decision.cost_estimate_acceptance` belongs to the cost-owning Role and is explicitly **not** reachable through this Skill.
- Trigger condition for review / decision dependency: set by the consuming Role Card.

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction: unrestricted.
- Sector: unrestricted; sector Specialisations supply realistic lifecycle profiles and replacement intervals.
- Programme / framework: unrestricted.
- Technology / version: not applicable.
- Criticality restrictions: at Enhanced Decision-Grade and above, a lifecycle comparison may not inform a technical conclusion unless every material cost input is specialist-owned and at least REVIEWED.
- Data / confidentiality restrictions: cost inputs are frequently commercially restricted and inherit their classification.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: understands that build cost and ownership cost differ and that both bear on option choice.
- WORKING: structures whole-life comparison on supplied inputs and conventions.
- ADVANCED: normalises options to comparable maturity, tests ranking stability, identifies decisive cost drivers.
- EXPERT: designs comparison frameworks across option families and adjudicates incompatible cost bases for escalation.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation. No proficiency level permits originating a cost estimate.

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: a comparison is invalidated when any input cost artifact becomes SUPERSEDED or the design basis materially changes.
- Controlled source / standard references: none embedded.

## Adjacent Skills / Packs
- `skill.technical_option_comparison` — the comparison this Skill supplies a cost dimension to.
- `skill.design_basis_definition` — establishes the maturity at which options are comparable.
- `skill.asset_performance_analysis`, `skill.om_strategy_design` — Asset O&M capabilities supplying operating inputs.
- `skill.sensitivity_analysis` — general technique for testing ranking stability.

## Completion / Use Criteria
Correctly applied when every cost input is attributed to its owning Role and knowledge state; horizon, discount and boundary conventions are stated; the comparison is reproducible; ranking sensitivity is reported; and any missing specialist input is reported as a gap leaving the comparison cost-unquantified rather than filled.

## Failure Modes to Avoid
- Generating a missing cost input to complete the comparison.
- Presenting a lifecycle figure as an estimate.
- Comparing options at different design maturities or base dates without normalisation.
- Treating a stable ranking as a cost conclusion.
- Allowing a whole-life comparison to substitute for the cost specialist's involvement at a decision gate.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification.
