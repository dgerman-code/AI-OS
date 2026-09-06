# Negotiation Preparation

Status: PROPOSED — Phase 4 exemplar Skill Card

## Identity
- Skill Name: Negotiation Preparation
- Skill ID: `skill.negotiation_preparation`
- Type: `SKILL`
- Primary Skill Family: Strategy & Analysis
- Secondary Skill Family Tags: Commercial & Market; Operations / Supply Chain / People
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose
Prepare a negotiating position before someone with the mandate conducts the negotiation: what is at stake, which issues are linked, what each side plausibly wants, where the concession room is, and what the walk-away limit is — expressed so that the person holding the delegated authority can negotiate from an evidenced position rather than improvise.

This Skill was added in Wave 3 because four approved Role Cards name negotiation preparation in their Core Skills — Programme / Partnership Manager, Supply Chain & Procurement Operations, Project Development Lead, Project Finance / Transaction — and every one of them bounds it identically as *preparation within delegated limits*. A capability that four Roles name, and that all four bound the same way, is reusable rather than role-specific.

**It is carded rather than left as a Universe entry because its authority boundary is the entire point of it.** A capability named "negotiation" one sentence away from a Role that cannot commit the organisation is exactly the kind of entry that drifts into implied mandate, and the boundary below is what stops that.

## Capability Definition
### Enables
- issue identification and linkage: which terms move together and which trade against each other;
- interest analysis for each party, separated from stated positions;
- concession architecture: what may be conceded, in what order, against what;
- reservation-value and walk-away articulation, derived from analysis rather than asserted;
- BATNA assessment for the organisation and, where evidenced, for the counterparty;
- issues-list and briefing construction for the mandated negotiator;
- scenario preparation for foreseeable counterparty moves.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary

Inside: the preparation. Analysis, options, limits, briefing material.

**Outside, and this is the load-bearing part of this card:**

- **No mandate to negotiate.** Preparing a position is not being authorised to advance it. Conducting the negotiation requires delegated authority held by a person, granted outside this registry.
- **No authority to concede.** Identifying concession room is analysis. Making a concession is an act with consequences and requires the mandate.
- **No authority to commit.** Every commitment this Skill prepares for is gated by a human decision right — `decision.partnership_agreement_terms`, `decision.supplier_award`, `decision.purchase_commitment`, `decision.land_or_site_commitment`, `decision.financing_terms_acceptance`, `decision.contract_commitment` as applicable to the consuming Role. None is reachable through this Skill.
- **No legal position.** Reading what a term means in law is `role.legal_regulatory_lead`'s, gated by `decision.formal_legal_opinion`. This Skill prepares commercial positions on terms whose legal effect someone else establishes.
- **No proficiency escalation.** No level of proficiency in this Skill converts preparation into mandate. An EXPERT preparer with no delegated authority may still not negotiate.

The test to apply: if an output of this Skill would bind or move the organisation when handed to a counterparty, it has left the boundary. Preparation is consumed internally by the mandated negotiator.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.programme_partnership_manager`, `role.supply_chain_procurement_operations_specialist`, `role.project_development_lead`, `role.project_finance_transaction_specialist`
- Canonical mapping reference: `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`, sections 11, 7, 19 and 27

These are exactly the four Roles whose Core Skills name the capability, each with the same delegated-limits bound. No Role was added because negotiation seemed adjacent to its work.

`role.sales_business_development_specialist` is a plausible future consumer — it prepares commercial proposals — but its Role Card frames that as proposal and offer construction rather than negotiation preparation, and no mapping currently supports it. That is a later mapping decision, not an assumption here.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant when terms will be negotiated with an external counterparty and the organisation's position needs to be evidenced and bounded before the conversation starts.

## Alternative Choice Set
- Choice set reference: none.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: `skill.option_analysis` where the position depends on comparing structures, and the consuming Role's own domain capability, since a position on terms nobody has analysed is not preparation. Competence statements only; confer no authority.
- Incompatibilities: must not be combined with, or presented as, the mandate to negotiate. Where the same assignment would both prepare and conduct a negotiation, the conducting part sits outside this Skill and requires delegated authority.

## Methods / Techniques
- issue decomposition and linkage mapping;
- interest-versus-position separation;
- concession sequencing and trade design;
- reservation value and BATNA derivation from evidenced alternatives;
- counterparty-move scenario preparation;
- issues-list and negotiation-brief construction.

## Inputs
- the terms or structure under negotiation, at their current version;
- the organisation's delegated authority limits for the assignment — without these the preparation has no boundary and must not proceed;
- evidenced alternatives on both sides;
- domain inputs from the owning Roles: legal effect, cost basis, financing terms, technical constraints, each at its stated knowledge state.

## Outputs / Contributions

Method-level contribution. The preparation is embedded in a Role-owned artifact or briefing; this Skill owns nothing.

- Role-owned artifacts this contributes to:
  - `artifact.partnership_strategy` owned by `role.programme_partnership_manager`;
  - `artifact.sourcing_analysis` and `artifact.purchase_commitment_draft` owned by `role.supply_chain_procurement_operations_specialist`;
  - `artifact.project_development_plan` owned by `role.project_development_lead`;
  - `artifact.term_sheet_analysis` owned by `role.project_finance_transaction_specialist`.
- What this capability explicitly does **not** produce: an executed agreement, a concession, a commitment, a legal position, or any externally transmitted offer.

## Support-Only Boundary
- Role retaining ownership of the conclusion: the consuming Role for its own artifact; `role.legal_regulatory_lead` for the legal effect of any term.
- What this capability may produce: analysis, options, limits, briefing material for the mandated negotiator.
- What it may never produce: the negotiated outcome, or any act that binds the organisation.

## Independent Review Boundary

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

Preparing a position is not assurance that the position is sound. Where review is required it is performed under the applicable `review.<id>` by someone who did not author the preparation.

## Evidence and Source Requirements
- Preferred source classes: the instrument or term sheet under negotiation at its current version; documented delegated authority limits; evidenced market comparables; domain outputs from their owning Roles at stated state.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source**, and an AI-generated estimate of a counterparty's reservation value is an ASSUMPTION, never evidence. Also insufficient: assumed counterparty intent, and comparables from a materially different transaction presented as applicable.
- Currency / version requirements: the term version and the authority limits both carry dates; preparation against a superseded draft or lapsed delegation is void.
- Assumptions that must be explicit: every inference about counterparty interests, alternatives or limits.
- Reproducibility requirements: each stated limit traceable to the delegation or to the analysis that derived it.

## Knowledge-State Constraints
- Minimum acceptable input state: delegated authority limits at FACT — preparation without them has no boundary. For decision-grade preparation, material domain inputs at REVIEWED or APPROVED.
- States this Skill may help derive or propose: ASSUMPTION for counterparty inferences; CALCULATION for derived reservation values; CONFLICT_DETECTED where the prepared position would exceed delegated authority.
- States this Skill may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict-detection obligations: where the analysis indicates the achievable outcome lies outside delegated limits, raise `CONFLICT_DETECTED` and escalate for a mandate decision. Preparing a position beyond the delegation and leaving the negotiator to discover it is the specific failure this rule prevents.

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Skill level; resolved by the consuming Role and workflow.
- Decision Right Reference(s): none at Skill level; resolved by the consuming Role and workflow. The commitment each consuming Role prepares for is gated by that Role's own decision rights, listed in the boundary above.
- Trigger condition for review / decision dependency: set by the consuming Role Card.

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction: unrestricted; jurisdiction affects the legal effect of terms, which is owned elsewhere.
- Sector: unrestricted.
- Programme / framework: unrestricted; programme rules may constrain what is negotiable.
- Technology / version: not applicable.
- Criticality restrictions: at Enhanced Decision-Grade and above, delegated authority limits must be documented and current before preparation begins.
- Data / confidentiality restrictions: preparation aggregates commercially sensitive material and inherits the strictest classification of its inputs; it must not be shared with the counterparty.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: distinguishes positions from interests.
- WORKING: prepares an issues list and stated limits from supplied delegation and inputs.
- ADVANCED: designs concession sequencing, derives reservation values from evidenced alternatives, prepares for counterparty moves.
- EXPERT: structures preparation for multi-party or multi-issue negotiations and identifies where the achievable outcome requires a mandate change.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation. **No proficiency level confers a mandate to negotiate, concede or commit.**

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: preparation is invalidated when the term version changes materially or the delegated authority lapses or is varied.
- Controlled source / standard references: none embedded.

## Adjacent Skills / Packs
- `skill.option_analysis` — structures the alternatives a position rests on.
- `skill.risk_allocation_analysis` — where the negotiation is about who carries which risk.
- `skill.contract_review` — reads the instrument whose terms are being prepared.
- `skill.commercial_structure_analysis` — where the structure itself is in play.

## Completion / Use Criteria
Correctly applied when delegated authority limits are documented and current, every stated limit traces to the delegation or to evidenced analysis, counterparty inferences are labelled as assumptions, the walk-away position is explicit, and any indication that the achievable outcome lies outside the mandate is escalated rather than absorbed.

## Failure Modes to Avoid
- Preparing without documented delegated limits.
- Presenting an inferred counterparty reservation value as evidence.
- Letting a well-prepared position read as authority to advance it.
- Preparing a position beyond the mandate and leaving the negotiator to discover it.
- Treating comparables from a materially different transaction as applicable.
- Sharing preparation material with the counterparty.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification. In particular, if it ever begins to describe conducting rather than preparing, it has crossed into an authority the registry does not grant.
