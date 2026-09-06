# Source Monitoring

Status: PROPOSED — Phase 4 exemplar Skill Card

## Identity
- Skill Name: Source Monitoring
- Skill ID: `skill.source_monitoring`
- Type: `SKILL`
- Primary Skill Family: Research & Evidence
- Secondary Skill Family Tags: Documentation / Knowledge / Disclosure
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: `specialisation.official_source_monitoring`, `specialisation.policy_source_monitoring` (both retired; source class is a context trigger on the mapping record, not a separate registry item)
- Superseded By: none

## Purpose
Keep a defined set of governed sources under recurring observation so that a material change is detected when it happens rather than when someone next happens to look — and so that downstream work built on those sources can be flagged for impact assessment.

This Skill exists because the two Specialisations it replaces were the same technique wearing two labels. The difference between watching official institutional sources and watching policy sources is the source class, which is an assignment attribute, not a different capability.

## Capability Definition
### Enables
- monitored source-set definition with explicit scope and inclusion basis;
- monitoring cadence design proportionate to how fast the source class moves and what depends on it;
- change detection against a recorded baseline;
- materiality triage: distinguishing a change that affects dependent work from a change that does not;
- supersession and amendment flagging;
- impact-notification to dependent artifacts and assignments;
- monitoring-record maintenance sufficient to show what was watched, when, and what was found.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary

Inside: detection, triage and flagging of change in a defined source set.

Outside:
- **interpreting what a change means.** A detected amendment to a regulation is a flag, not a legal conclusion; interpretation is owned by `role.legal_regulatory_lead`. A detected policy shift is a flag, not a policy position; that is owned by `role.eu_policy_institutional_affairs_specialist`.
- **rewriting canonical knowledge.** Detecting that a source underpinning canonical material has changed does not update that material. Status change is owned by `role.knowledge_evidence_steward` and gated by `decision.canonical_knowledge_status_change`.
- **promoting knowledge state.** Monitoring can propose SUPERSEDED for a source it has watched change; it cannot execute the transition, and it cannot promote anything to REVIEWED, APPROVED or CANONICAL.
- **publishing.** External communication of a detected change is gated by the consuming Role's decision rights, `decision.external_publication` among them.

The distinction that matters: monitoring says *something changed and here is what depends on it*. Everything after that sentence belongs to a Role.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.research_market_intelligence_analyst`, `role.knowledge_evidence_steward`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, sections 2 and 10

`role.legal_regulatory_lead` and `role.eu_policy_institutional_affairs_specialist` are plausible Wave 2 additions — both depend on sources that move — but neither is currently mapped, so neither is listed.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant where work has a shelf life tied to external sources: canonical knowledge dependent on official publications, programme work dependent on call guidance, or analysis dependent on periodically republished statistics. The source class — official, institutional, policy, regulatory, market — is stated on the assignment as the trigger.

## Alternative Choice Set
- Choice set reference: none.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: `skill.source_verification`, since a source set must be verified before it is worth watching, and `skill.source_discovery` where the set must first be assembled. Competence statements only; confer no authority.
- Incompatibilities: must not be operated as an automated canonical-update mechanism. Monitoring output enters a Role's judgement; it does not enter the knowledge base directly.

## Methods / Techniques
- source-set scoping and inclusion-basis recording;
- baseline capture with version and effective-date anchoring;
- cadence design against source volatility and dependency criticality;
- differential comparison against baseline;
- materiality triage against dependent work;
- supersession-chain flagging;
- dependency mapping from source to dependent artifacts for impact notification.

## Inputs
- the verified source set and its baseline versions;
- the source class and its authoritative channels;
- the register of dependent artifacts and assignments;
- criticality of the dependent work, which sets cadence and materiality thresholds.

## Outputs / Contributions

Method-level contribution. Monitoring findings feed Role-owned artifacts and workflow escalation; this Skill owns no artifact.

- Role-owned artifacts this contributes to:
  - `artifact.research_evidence_pack` and `artifact.market_intelligence_analysis` owned by `role.research_market_intelligence_analyst`;
  - `artifact.evidence_integrity_record` and `artifact.evidence_gap_conflict_report` owned by `role.knowledge_evidence_steward`.
- What this capability explicitly does **not** produce: an interpretation of the change, a revised canonical record, a knowledge-state transition, or any external communication of the change.

## Support-Only Boundary
- Role retaining ownership of the conclusion: `role.knowledge_evidence_steward` for what a change means for canonical status; the applicable domain Role for what it means substantively.
- What this capability may produce: change detections, materiality triage, supersession flags, impact sets.
- What it may never produce: the interpretation, the status change, or the updated canonical material.

## Independent Review Boundary

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

A monitoring regime that reports no change is not assurance that dependent work remains valid; it is evidence about the watched set only.

## Evidence and Source Requirements
- Preferred source classes: authoritative publication channels of the monitored bodies; official registers and journals; managing-authority guidance pages; issuer change logs.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source**, and an AI-generated summary of a change is not a detection. Also insufficient: aggregator feeds without provenance to the authoritative channel, and social or press reporting of a change as a substitute for the instrument.
- Currency / version requirements: every baseline carries the version and effective date it was captured at; a monitoring result is meaningless without its baseline.
- Assumptions that must be explicit: any assumption that absence of publication means absence of change.
- Reproducibility requirements: the source set, cadence, baseline and comparison method must be recorded well enough for another practitioner to repeat the check.

## Knowledge-State Constraints
- Minimum acceptable input state: the monitored set must be at SOURCE state with verification complete; monitoring unverified material produces unusable results.
- States this Skill may help derive or propose: SUPERSEDED for a source observed to be replaced; CONFLICT_DETECTED where a change contradicts material already relied upon; UNKNOWN where a channel becomes unavailable and currency can no longer be established.
- States this Skill may not promote autonomously: REVIEWED, APPROVED, CANONICAL — and it may not autonomously downgrade material whose status derives from a human decision.
- Conflict-detection obligations: a detected change that contradicts APPROVED or CANONICAL material is raised as `CONFLICT_DETECTED` and routed to the owning Role; it is never applied silently.

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Skill level; resolved by the consuming Role and workflow.
- Decision Right Reference(s): none at Skill level; resolved by the consuming Role and workflow. Where a detected change implies a canonical status change, the consuming Knowledge & Evidence Steward assignment carries `decision.canonical_knowledge_status_change`.
- Trigger condition for review / decision dependency: set by the consuming Role Card.

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction: unrestricted; jurisdiction scopes the monitored set.
- Sector: unrestricted.
- Programme / framework: unrestricted; programme Packs may impose their own currency-monitoring requirements on top.
- Technology / version: not applicable.
- Criticality restrictions: at Enhanced Decision-Grade and above, cadence must be short enough that a change cannot pass undetected within the decision window.
- Data / confidentiality restrictions: monitoring must not create a record that discloses restricted dependencies outside their permitted context.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: understands that governed sources change and that dependent work can go stale.
- WORKING: maintains a defined source set against a baseline and reports detected changes.
- ADVANCED: designs cadence and materiality thresholds, maps dependencies, triages impact.
- EXPERT: designs monitoring regimes across source classes and adjudicates contradiction between a detected change and existing approved material for escalation.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation.

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: a monitored source's authoritative channel changing, which invalidates the baseline until re-established.
- Controlled source / standard references: none embedded; the monitored set is supplied by the assignment or an activated Pack.

## Adjacent Skills / Packs
- `skill.source_verification` — establishes the baseline this Skill watches.
- `skill.change_detection` — analyses what changed once a change is flagged.
- `skill.evidence_gap_analysis` — assesses what a change leaves unsupported.
- `skill_pack.life_programme`, `skill_pack.cove` — supply programme source sets whose currency must be monitored.

## Completion / Use Criteria
Correctly applied when the monitored set and its inclusion basis are explicit, baselines carry versions and dates, cadence matches volatility and dependency criticality, detected changes are triaged for materiality, and dependent work is flagged for impact assessment rather than silently updated.

## Failure Modes to Avoid
- Reporting change volume instead of material impact.
- Monitoring a republication channel rather than the authoritative one.
- Letting a baseline go unrecorded, making later comparison unverifiable.
- Treating no-change as assurance that dependent work is still valid.
- Applying a detected change to canonical material without the owning Role and its decision right.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification.
