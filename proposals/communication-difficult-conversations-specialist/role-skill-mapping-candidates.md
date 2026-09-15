# Candidate Role-to-Skill Mapping — Difficult Conversations & Communication Strategy Specialist

Status: `PROPOSED`
Template: Phase 4 Role-to-Skill Mapping convention (`skills/mappings/`), applied to a candidate Role
Version: 0.1
Governance Owner: AI-OS architecture governance
Inherits: `standard.skill.common_constraints@0.1`

> **This is a proposal surface, not a mapping record.** The approved Phase 4 mapping documents in
> `skills/mappings/` are the canonical source of relationship type and context trigger for the
> Roles they cover. This document covers a **candidate** Role that no approved mapping covers, is
> not written into `skills/mappings/`, and authorises no activation of anything. It exists because
> OG-2 was decided and the mapping is now writable as a proposal; writing it down does not make it
> authoritative, and Phase 4 mapping remains its own governed act (OG-6).

## 1. Why this document exists now, and what it is not

Before the OG-2 decision there was no decided Role to map from, so no mapping could be proposed
without prejudging the decision. The decision of 2026-09-15
(`human-governance-decisions-og1-og2.md`, commit `903c58dfa565f5f14a9af19efcccceabae328f26`) settles
that the capability is a candidate **Professional Delivery Role**. This document states which Skills
that Role would require, and on what basis, so that a Phase 4 change-control pass has something
specific to accept or reject.

| It is | It is not |
|---|---|
| A candidate mapping proposal for one candidate Role | A Phase 4 mapping record |
| A statement of which Skills the Role requires, with triggers | An authorisation to activate any Skill |
| A document that names candidate Skills as candidates | A document that brings a Skill into existence |
| Traceable input to Skill Registry and Phase 4 change control | An amendment to `skills/mappings/` — which this package does not touch |

## 2. Relationship types

The five Phase 4 types, used as the approved mapping documents define them:

| Type | Means |
|---|---|
| `REQUIRED_CORE` | Intrinsic to the Role across substantially all assignments |
| `REQUIRED_FOR_CONTEXT` | Mandatory when the stated trigger is true; a trigger is required |
| `OPTIONAL` | May improve execution; never a catch-all for weakly related capability |
| `ALTERNATIVE` | One of a choice set; a choice condition is required |
| `PROHIBITED_IN_CONTEXT` | Must not be activated in the stated context; a rationale is required |

## 3. Candidate Role

Role: `role.communication_difficult_conversations_specialist` *(candidate — unregistered,
unapproved, not part of the approved 59-Role universe)*

### REQUIRED_CORE — approved Skills

Referenced, never duplicated. Each exists in the approved skill universe and is cited by its
approved identifier; this document neither restates nor redefines any of them.

- `skill.fact_extraction`
- `skill.assumption_analysis`
- `skill.evidence_mapping`
- `skill.problem_structuring`
- `skill.position_mapping`
- `skill.risk_identification`
- `skill.technical_writing`
- `skill.editorial_quality_control`
- `skill.action_tracking`

### REQUIRED_CORE — candidate Skills

**None of these exists.** Each is a candidate under OG-5 and requires Skill Registry change control
before it can be activated for any Role.

- `skill.interaction_response_triage` *(candidate)*
- `skill.boundary_formulation` *(candidate)*
- `skill.refusal_design` *(candidate)*
- `skill.de_escalation_framing` *(candidate)*
- `skill.communication_reactivity_detection` *(candidate)*
- `skill.conversational_control` *(candidate)*
- `skill.non_response_strategy` *(candidate)*
- `skill.communication_control_filtering` *(candidate)*

### REQUIRED_FOR_CONTEXT

| Skill | Trigger |
|---|---|
| `skill.source_verification` | The record's own history is contested — a cited prior message, date or commitment is in issue |
| `skill.stakeholder_mapping` | More than two parties are on the interaction, or the decider is not the correspondent |
| `skill.relationship_risk_analysis` | The interaction is with a party the entity has a continuing relationship with |
| `skill.negotiation_preparation` | The interaction is an episode in a negotiation with positions and concessions |
| `skill.meeting_brief_preparation` | The deliverable is preparation for a meeting or call |
| `skill.engagement_strategy_design` | Channel, sequence or audience is itself in question |
| `skill.document_structuring` | The deliverable is a formal escalation or final-position message |
| `skill.decision_criteria_design` | The message asks the counterparty for a decision |
| `skill.change_detection` | The exchange concerns successive versions of a draft, term or claim |
| `skill_pack.communication_difficult_conversations@0.1` *(candidate)* | Any assignment applying the methodology — and the pack is **not activatable** while any Required Skill in it is a candidate (`skill-pack.md` SP-1) |

### OPTIONAL

- `skill.consultation_design` — the interaction is part of a structured consultation
- `skill.legal_issue_spotting` — **only** to raise that legal input is needed; never to conclude
- `skill.claim_substantiation` — a factual claim in the thread must be evidenced
- `skill.document_version_control` — the exchange concerns successive drafts of an instrument

### ALTERNATIVE

None. No Skill required by this Role has an interchangeable substitute, and substitution would
change what the Role produces.

### PROHIBITED_IN_CONTEXT

| Skill | Context | Rationale |
|---|---|---|
| `skill.legal_issue_spotting` | Any use beyond flagging that legal input is needed | Spotting is not concluding. A legal conclusion is `role.legal_regulatory_lead`'s, and this Role may not reach one by any route (RC-1) |
| Any clinical, diagnostic or psychometric Skill | Every context | The Role reads **wording**, never people. No clinical Skill may substitute for `skill.communication_reactivity_detection`, and no psychological diagnosis is within scope |

## 4. Fail-closed behaviour

**Rule RM-1 — a candidate Skill is unavailable, and unavailability blocks.** Eight of the
`REQUIRED_CORE` Skills above do not exist. Until each is registered, an assignment that relied on it
would be relying on an unregistered capability, and `skill-pack.md` SP-1 makes the pack
non-activatable while any Required Skill is a candidate. This document does not soften that; it
records what would need to exist.

**Rule RM-2 — this document authorises nothing.** It confers no eligibility, activates no Skill,
registers no Role, and does not make the Role assignable. A reader who treats it as a Phase 4
mapping record has read it as the thing its first paragraph says it is not.

**Rule RM-3 — no approved registry is edited by this package.** `skills/mappings/`,
`skills/master-skill-universe.md` and `roles/master-role-universe.md` are untouched. The approved
Role universe remains 59 Roles.

## 5. What a Phase 4 pass would still have to do

1. Decide each candidate Skill on its own merits (OG-5) — eight decisions, not one.
2. Decide whether this decomposition is right at all: eight Skills, or three, or one pack.
3. Write the authoritative mapping in `skills/mappings/`, if the Role is registered.
4. Decide the pack's composition and its compatible-Role allowlist under Phase 4 conventions.

None of that is done here, and none of it is implied by the OG-2 decision.

## 6. Non-Runtime Statement

This document is declarative proposal material. It specifies no implementation, schema, storage,
activation mechanism or runtime, and binds no model, provider or runtime technology.
