# Battery Energy Storage Systems (BESS)

Status: PROPOSED — Phase 4 exemplar Specialisation Card

## Identity
- Skill Name: Battery Energy Storage Systems (BESS)
- Skill ID: `specialisation.bess`
- Type: `SPECIALISATION`
- Primary Skill Family: Technical / Engineering
- Secondary Skill Family Tags: Finance & Economics; Commercial & Market
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

### When Type = SPECIALISATION
- Specialisation Class: `SECTOR`
- Bounded context:
  - Sector: grid-connected and behind-the-meter battery energy storage
  - Programme / call / framework: not applicable
  - Institution / funder: not applicable
  - Technology / version: not bound — this Specialisation bounds an asset class, not a product or platform version
  - Jurisdiction: not bound; market rules arrive through the assignment and through `specialisation.regulated_market` where applicable
  - Metric / methodology: not applicable
  - Operating context: not applicable
- Applicability boundary: applies where the asset under analysis is an electrochemical storage system whose value, degradation and risk profile depend on cycling behaviour. It stops at the point where the question is no longer storage-specific — a substation, a grid connection queue or a PPA is not made a BESS question by sitting next to a battery.
- Base capability: none singular. This Specialisation bounds several technical, cost and commercial Skills rather than extending one.

**This card is the exemplar for the `Type: SPECIALISATION` template path**, which had no instance before Wave 3. It is deliberately a SECTOR case, the most heavily used Specialisation class in the registry.

## Purpose
Carry what is specific to battery storage as an asset class — degradation and cycle life, augmentation, round-trip efficiency, thermal and safety behaviour, revenue stacking across markets, and the cost structure that follows from all of it — so that a technical, cost or commercial method applied to a BESS project is applied against storage reality rather than against general power-plant intuition.

A Specialisation exists here because the method does not change between asset classes: comparing options, estimating cost, forecasting revenue are the same techniques for a battery and a water treatment plant. What changes is every benchmark, norm, failure mode and convention the technique consumes. That is a bounded context, not a capability.

## Capability Definition
### Enables
- selecting storage-appropriate benchmarks: round-trip efficiency, degradation curves, augmentation intervals, availability conventions;
- reasoning about cycle-life and depth-of-discharge trade-offs and their effect on whole-life cost and warranty position;
- recognising revenue-stacking structures and the constraints between stacked services;
- identifying storage-specific technical risks — thermal runaway, fire safety and separation, state-of-health measurement, augmentation planning;
- testing whether a general power-sector benchmark transfers to storage, and stating when it does not.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Applicability Boundary — what this Specialisation does not do

Selecting this Specialisation narrows applicability. It **adds no capability and no authority**:

- it does not let a Role perform a method it is not mapped to. A Role without a cost capability does not gain one by being storage-literate;
- it does not transfer any professional conclusion. `role.sector_technical_expert` gives a sector opinion, `role.technical_feasibility_lead` reaches the feasibility conclusion, `role.capex_cost_engineering_specialist` owns cost, `role.asset_om_technical_operations_specialist` owns the operating and availability basis. Those boundaries are unchanged by storage context;
- it does not confer safety, grid-code or certification authority. Storage safety certification and grid compliance are statutory or licensed acts outside this registry;
- it is not a Skill in disguise. If a future revision starts describing what a practitioner *does* rather than what is *true of the asset class*, it has become a Skill and must be reclassified.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.technical_feasibility_lead`, `role.sector_technical_expert`, `role.capex_cost_engineering_specialist`, `role.asset_om_technical_operations_specialist`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md` section 4; `skills/mappings/wave-2-domain-completion-role-skill-mapping.md` sections 20, 22 and 23

In Wave 2 this Specialisation appears inside `at-least-one-of` ALTERNATIVE sector sets for three Roles, because exactly one asset class normally governs an assignment and selecting several would blend incompatible benchmark bases. That cardinality lives in the mapping records, not here.

`role.financial_modelling_specialist` and `role.commercial_demand_specialist` are **not** listed. Both consume storage assumptions, but they consume them as inputs from the technical and cost Roles at those Roles' stated knowledge state. Adding them would let a modelling Role originate storage-technical positions.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant when the assignment's asset class is battery storage and a general power-sector benchmark would give a materially wrong answer.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: the Role must already be mapped to the technical, cost or commercial capability being bounded. This Specialisation bounds a method; it does not supply one. Competence statement only; confers no authority.
- Incompatibilities: must not be combined with a second sector Specialisation for the same analysis unless the project genuinely spans asset classes, because benchmark bases do not blend.

## Inputs
- asset configuration: chemistry, power and energy rating, C-rate, augmentation strategy;
- duty cycle and market participation model;
- manufacturer warranty and degradation terms;
- applicable grid code, connection terms and safety standards, at stated versions.

## Outputs / Contributions

Context-level contribution. This Specialisation contributes storage-specific parameters, benchmarks and caveats into artifacts owned by the consuming Roles; it owns nothing.

- Role-owned artifacts this contributes to:
  - `artifact.sector_technical_opinion` and `artifact.sector_benchmark_input` owned by `role.sector_technical_expert`;
  - `artifact.feasibility_study` and `artifact.technical_basis_of_design` owned by `role.technical_feasibility_lead`;
  - `artifact.cost_estimate` and `artifact.basis_of_estimate` owned by `role.capex_cost_engineering_specialist`;
  - `artifact.om_strategy` and `artifact.availability_and_lifecycle_basis` owned by `role.asset_om_technical_operations_specialist`.
- What this capability explicitly does **not** produce: any of those artifacts, any feasibility, cost or availability conclusion, or a safety or grid-compliance determination.

## Support-Only Boundary
- Roles retaining ownership of the conclusion: each consuming Role, for its own artifact and conclusion.
- What this capability may produce: storage-specific benchmarks, parameters, transferability judgements and caveats.
- What it may never produce: the conclusion those inputs feed.

## Independent Review Boundary

> This is bounded context, not a quality-control or review technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

Storage expertise in the author does not substitute for `review.engineering_technical` or `review.cost_estimate`, both of which are performed by someone who did not author the work.

## Evidence and Source Requirements
- Preferred source classes: manufacturer datasheets and warranty terms at stated revision; measured performance and degradation data with test conditions; applicable grid codes and safety standards at their editions; independent test-house results.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source.** Also insufficient: vendor marketing claims, benchmarks from a different chemistry or duty cycle presented as applicable, and degradation figures quoted without cycle depth, temperature and C-rate.
- Currency / version requirements: chemistry and product generation move fast; every benchmark carries its vintage, and a benchmark whose vintage is not stated is an ASSUMPTION.
- Assumptions that must be explicit: augmentation strategy, end-of-life criterion, duty cycle assumed for degradation.
- Reproducibility requirements: parameters traceable to a named source with its conditions.

## Knowledge-State Constraints
- Minimum acceptable input state: for a decision-grade contribution, asset configuration and warranty terms at FACT, measured data at FACT with stated conditions.
- States this Specialisation may help derive or propose: FACT for documented characteristics; ASSUMPTION for any transferred benchmark; CONFLICT_DETECTED where manufacturer terms and observed behaviour disagree.
- States it may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict-detection obligations: divergence between warranty terms, datasheet and measured behaviour is raised as `CONFLICT_DETECTED`, never averaged.

This Specialisation may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Specialisation level; resolved by the consuming Role and workflow.
- Decision Right Reference(s): none at Specialisation level; resolved by the consuming Role and workflow.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Specialisation owns no review or authority.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: knows storage differs from generation in degradation and duty-cycle behaviour.
- WORKING: applies storage benchmarks correctly within a supplied configuration.
- ADVANCED: reasons about cycle-life and augmentation trade-offs and tests benchmark transferability.
- EXPERT: adjudicates conflicting degradation and warranty evidence and sets the storage basis for escalation.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation.

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: a material shift in prevailing chemistry, warranty convention or applicable safety standard invalidates carried benchmarks.
- Controlled source / standard references: none embedded; sources are bound per assignment.

## Adjacent Skills / Packs
- `specialisation.solar`, `specialisation.industrial`, `specialisation.transport` and the other sector Specialisations — siblings in the same ALTERNATIVE sets; benchmarks are not portable between them.
- `specialisation.regulated_market` — supplies market-rule context where revenue depends on regulated access.
- `skill_pack.project_finance_metrics` — governs coverage conventions where a storage project is project-financed.

## Completion / Use Criteria
Correctly applied when every storage-specific parameter carries its source and conditions, transferred benchmarks are labelled as assumptions with their vintage, non-transferable general benchmarks are flagged rather than used, and the consuming Role's conclusion remains that Role's.

## Failure Modes to Avoid
- Applying a benchmark from a different chemistry, duty cycle or product generation.
- Quoting degradation without depth of discharge, temperature and C-rate.
- Letting storage literacy read as authority over feasibility, cost or safety.
- Blending two sector Specialisations in one benchmark basis.
- Treating a warranty term as measured performance.

## Reclassification Warning
If this Specialisation begins to describe what a practitioner does rather than what is true of the asset class, it has become a Skill and must be reclassified. If it begins to require independent professional ownership, standalone artifact ownership, review identity or human approval authority, stop and reassess the registry classification.
