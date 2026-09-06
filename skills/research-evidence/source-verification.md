# Source Verification

Status: PROPOSED — Phase 4 exemplar Skill Card

## Identity
- Skill Name: Source Verification
- Skill ID: `skill.source_verification`
- Type: `SKILL`
- Primary Skill Family: Research & Evidence
- Secondary Skill Family Tags: Legal / Compliance / Procurement; Documentation / Knowledge / Disclosure
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: `skill.legal_source_currency_check` (retired; legal-source currency is this Skill with a legal-source context trigger)
- Superseded By: none

## Purpose
Establish whether a source is what it claims to be, whether the issuing body had authority to issue it, and whether the version in hand is the one currently in force for the assignment date. This is the capability that stops downstream work from being built on a document that is genuine but superseded, authoritative but out of scope, or plausible but unattributable.

It exists independently of any Role because the same verification technique is applied to an official journal, a programme call guide, a market report and a contract, and the technique does not change with the domain — only the source class and the currency rule do.

## Capability Definition
### Enables
- provenance establishment: who issued the material, through what channel, and whether the channel is the authoritative one;
- authority assessment: whether the issuing body is competent to issue material of that class;
- version and edition identification, including consolidated versus original text;
- currency determination against the assignment's effective date;
- supersession and amendment-chain checking;
- detection that two sources presented as the same are materially different;
- recording the verification result as reproducible metadata rather than as an opinion.

### Does Not Establish
- professional Role authority;
- first-class output ownership;
- review authority;
- human approval authority;
- model/runtime identity.

## Skill Boundary

Inside: the source's identity, authority, version and currency.

Outside, and deliberately so:
- **whether the claim the source supports is true.** Substantiating a claim against evidence is factual review under `review.factual_evidence`, performed by someone who did not author the claim. A verified source can still be cited for a proposition it does not support.
- **what the source means in law.** Legal interpretation is owned by `role.legal_regulatory_lead`; a formal opinion is gated by `decision.formal_legal_opinion`. This Skill establishes that a legal instrument is in force and in which version, never what it requires.
- **evidence governance authority.** Deciding the knowledge state of a body of material, or promoting it, is owned by `role.knowledge_evidence_steward` and gated by `decision.canonical_knowledge_promotion` / `decision.canonical_knowledge_status_change`.
- **independent review of any kind.** Verification is a quality-control technique performed by the same person doing the work; it creates no reviewer identity.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.** This section declares only which Roles may use this capability at all.

- Compatible Role allowlist: `role.research_market_intelligence_analyst`, `role.eu_grants_programmes_specialist`, `role.legal_regulatory_lead`, `role.knowledge_evidence_steward`, `role.sales_business_development_specialist`, `role.eu_programme_implementation_grant_management_specialist`, `role.learning_vet_design_specialist`, `role.project_development_lead`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, sections 2, 3, 6 and 10
- Canonical mapping reference (Wave 2): `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

Wave 2 adds `role.project_development_lead`, `role.eu_programme_implementation_grant_management_specialist` and `role.learning_vet_design_specialist` for **transitive Pack compatibility** under `standard.skill.common_constraints` §6.1a: those Roles activate `skill_pack.bid_proposal_management`, `skill_pack.life_programme` or `skill_pack.cove`, each of which carries this Skill as a component. Eligibility only — relationship and trigger come from `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`.

`role.sales_business_development_specialist` is present for **transitive Pack compatibility**, not because a mapping record maps this Skill to it directly. `skill_pack.bid_proposal_management` is mapped to that Role and exposes this Skill as an Optional component, so rejecting the Role here would make a valid Pack activation fail. Eligibility only: whether the Skill is actually activated, and under what relationship and trigger, is decided by the mapping record for the Pack, never by this line.

Wave 2 is expected to widen this allowlist — Accounting / Financial Due Diligence, EU Policy & Institutional Affairs and Integrity / Due Diligence are obvious candidates — but a Role is added here only when its Role Card and a mapping record both support it, never by anticipation.

Listing a Role confers eligibility, never a requirement.

## Typical Use — Advisory, Non-Authoritative

> Advisory only. This section states no obligation. The mapping record decides whether the capability is required, contextual, optional, alternative or prohibited for a given Role, and it alone defines the trigger or choice condition.

Usually relevant when material is drawn from an external authority whose text changes over time — legislation, programme call guides, technical standards, institutional procedures, published statistics — and where using a superseded version would change the answer.

## Alternative Choice Set
- Choice set reference: none. This capability has no substitute; nothing else establishes source identity and currency.

## Prerequisites and Incompatibilities
- Prerequisite capabilities: `skill.source_discovery` where the source set is not already given. Competence statement only; confers no authority.
- Incompatibilities: none as a technique. It must not be presented as, or substituted for, `review.factual_evidence`.

## Methods / Techniques
- authoritative-channel identification and comparison against secondary republication;
- issuer competence check against the instrument class;
- version, edition and consolidation-status identification;
- effective-date and applicability-window determination against the assignment date;
- amendment and supersession chain tracing;
- differential comparison of two purportedly identical texts;
- verification-metadata capture sufficient for another practitioner to repeat the check.

## Inputs
- the candidate source and the channel it arrived through;
- the assignment's effective date and applicable jurisdiction / programme / framework;
- the claim or requirement the source is intended to support, so that scope mismatch is detectable;
- any prior verification record for the same source.

## Outputs / Contributions

Method-level contribution. This Skill produces verification metadata and findings that are embedded in a Role-owned artifact; it owns no artifact of its own.

- Role-owned artifacts this contributes to:
  - `artifact.research_evidence_pack` owned by `role.research_market_intelligence_analyst`;
  - `artifact.eu_funding_fit_assessment` and `artifact.eu_application_package` owned by `role.eu_grants_programmes_specialist`;
  - `artifact.legal_analysis` owned by `role.legal_regulatory_lead`;
  - `artifact.evidence_integrity_record` owned by `role.knowledge_evidence_steward`.
- What this capability explicitly does **not** produce: the substantive conclusion of any of those artifacts, an evidence-integrity determination, a legal position, or any statement that a claim is true.

## Support-Only Boundary
- Role retaining ownership of the conclusion: `role.knowledge_evidence_steward` for evidence-integrity conclusions; `role.legal_regulatory_lead` for legal interpretation of a verified instrument.
- What this capability may produce: verification findings, currency status, supersession flags, provenance metadata.
- What it may never produce: the evidence-integrity conclusion, the legal conclusion, or a knowledge-state promotion.

## Independent Review Boundary

> This is a quality-control technique. It is **not** independent review, does not discharge any `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation, and creates no reviewer identity.

Verifying one's own sources is expected practice, not assurance. Where independent review is required it is performed under the applicable `review.<id>` by someone who did not author the work.

## Evidence and Source Requirements
- Preferred source classes: official journals and registers; issuing-authority publications; programme managing-authority guidance; standards bodies; audited or officially published statistics; executed instruments.
- Insufficient / prohibited source classes: **AI-generated content is never a controlled source and cannot be verified into one.** Also insufficient: undated republication, unattributed aggregation, cached copies without provenance, and secondary summaries where the primary text is available.
- Currency / version requirements: every verified source carries issuer, identifier, version / edition, effective date, and supersession status at the assignment date.
- Assumptions that must be explicit: any inference that an unversioned source is current.
- Reproducibility requirements: the verification record must let another practitioner reach the same result from the same inputs.

## Knowledge-State Constraints
- Minimum acceptable input state: UNKNOWN is acceptable as an input state — establishing state is the point of the Skill.
- States this Skill may help derive or propose: SOURCE for verified material; FACT where the source directly evidences a factual predicate; SUPERSEDED where the chain shows replacement; CONFLICT_DETECTED where two authoritative sources materially disagree; UNKNOWN where verification fails.
- States this Skill may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict-detection obligations: a material contradiction between authoritative sources, or a source that cannot be verified but is already relied upon downstream, is raised as `CONFLICT_DETECTED` and escalated. It is never resolved by preferring the more convenient source.

This Skill may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**. Transitions are performed by the owning Role under the applicable review and decision path.

## Review / Decision Dependencies
- Review Profile Reference(s): none at Skill level; resolved by the consuming Role and workflow. Where the consuming Role is `role.knowledge_evidence_steward`, `review.evidence_integrity_provenance` applies to that Role's output; where it is `role.research_market_intelligence_analyst`, `review.factual_evidence` applies.
- Decision Right Reference(s): none at Skill level; resolved by the consuming Role and workflow.
- Trigger condition for review / decision dependency: set by the consuming Role Card, not here.

These are dependencies only; the Skill does not own review or authority.

## Applicability and Restrictions
- Jurisdiction: unrestricted; jurisdiction is an assignment attribute that selects the applicable source class.
- Sector: unrestricted.
- Programme / framework: unrestricted; programme Packs supply their own controlled-source rules on top.
- Technology / version: not applicable.
- Criticality restrictions: none, but at Enhanced Decision-Grade and above, unverifiable material may not carry a decision-grade conclusion.
- Data / confidentiality restrictions: verification must not require moving restricted material outside its permitted context.

## Proficiency Guidance
Controlled vocabulary only (AWARENESS / WORKING / ADVANCED / EXPERT):
- AWARENESS: recognises that sources have versions and effective dates.
- WORKING: verifies a single source against its authoritative channel and records the result.
- ADVANCED: traces amendment chains, resolves consolidation ambiguity, detects scope mismatch between source and claim.
- EXPERT: designs verification regimes for a governed corpus and adjudicates conflicting authoritative sources for escalation.

Proficiency does not create authority and is never evidence of licensing, credentialing or regulated authorisation.

## Currency / Refresh
- Effective Date: on approval of this card.
- Review Date: with the Phase 4 registry review cycle.
- Expiry / invalidation trigger: a material change in what counts as an authoritative channel for a governed source class.
- Controlled source / standard references: none embedded. Source classes are named generically; the specific authorities are supplied by the assignment or by an activated Pack.

## Adjacent Skills / Packs
- `skill.source_discovery` — finds candidate sources; this Skill verifies them.
- `skill.source_monitoring` — watches a verified source set for change over time.
- `skill.change_detection` — identifies what changed between versions once supersession is established.
- `skill.evidence_mapping` — links verified sources to the claims they support.

## Completion / Use Criteria
Correctly applied when every material source carries issuer, version, effective date and supersession status; unverifiable sources are flagged rather than silently used; scope mismatch between source and claim is surfaced; and the record is reproducible.

## Failure Modes to Avoid
- Treating verification as substantiation and concluding the claim is true.
- Accepting a consolidated text as the operative version without checking the consolidation date.
- Verifying a source once and reusing the result after its currency window has closed.
- Treating AI-generated summary of a source as the source.
- Resolving a contradiction between authoritative sources by selection instead of escalation.

## Reclassification Warning
If this Skill begins to require independent professional ownership, standalone decision-grade artifact ownership, independent review identity, human approval authority or System Control authority, stop and reassess the registry classification.
