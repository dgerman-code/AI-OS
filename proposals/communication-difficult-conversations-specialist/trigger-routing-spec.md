# Trigger and Routing Specification

Status: `PROPOSED`
Version: 0.1
Governance Owner: AI-OS architecture governance

> The scoring below is **routing evidence**. It selects no Model Profile, grants no Decision
> Right, satisfies no review and approves nothing.

## 1. What this document specifies, and what it does not

It specifies how the Orchestrator decides **whether to activate**
`role.communication_difficult_conversations_specialist` on a task, **at what participation**, and
**which other Roles must be co-activated** so that the communication Role never becomes the de
facto owner of a domain it does not own.

It does not specify a classifier implementation, a model, a threshold-tuning procedure, a feature
extractor or any runtime component. The weights below are a **declared initial calibration**, not
a trained artifact, and they are explicitly subject to the evaluation suite
(`evaluation-spec.md` §7) before any of them is treated as settled.

## 2. The score

`communication_conflict_score` — an integer, `0`–`100`, computed by the Orchestrator from
**observable task features**, clamped at both ends.

**Rule TR-1 — observable features only.** Every contributing feature must be something present in
the task or the record: a word, a pattern, a declared stake, a named audience. **Psychological
motive inference is never a trigger fact.** "The sender seems manipulative" is not a feature; "the
message reopens a point closed on a stated date" is.

**Rule TR-2 — the score is evidence about routing, not about people.** It is never displayed or
recorded as a characterisation of a counterparty, never stored against a person, and never used as
an input to any governed conclusion.

## 3. Feature weights — declared initial calibration

| # | Observable feature | Weight |
|---:|---|---:|
| F1 | Explicit conflict, hostility, aggression or accusation in the material | +25 |
| F2 | A refusal, boundary, ultimatum or explicit pressure is present or required | +18 |
| F3 | The request asks for wording that is "stronger", "firmer", "stricter", "more professional", or "firm without escalating" | +15 |
| F4 | Repeated confusion, a reopened closed issue, or an unanswered central question across turns | +15 |
| F5 | Negotiation tension, board disagreement, difficult stakeholder or partner dispute | +18 |
| F6 | Emotionally reactive drafting signals in the user's own text — retaliation, point-by-point rebuttal impulse | +12 |
| F7 | Public criticism, or a donor, institutional or executive dispute | +15 |
| F8 | Declared stakes are `high` or `critical` | +10 |
| F9 | Threatened escalation, formal complaint, or a stated consequence by either party | +12 |
| F10 | Relationship risk explicitly raised, or a critical stakeholder relationship named | +10 |

Clamp to `[0, 100]`. Features are additive and independent; no feature is a multiplier, and no
feature alone forces activation.

**Rule TR-3 — F6 is about the user's draft, not the user.** It detects reactivity in wording that
the user is about to send. It is not an assessment of the user's state, and it is never recorded
as one.

## 4. Bands

| Band | Score | Routing effect |
|---|---:|---|
| **Below threshold** | `< 35` | **No activation**, unless explicitly requested. An explicit request activates at supporting participation regardless of score |
| **Supporting** | `35–54` | Optional supporting Role. It may contribute wording; the owning Role leads |
| **Activate** | `55–74` | Activate as the communication specialist, `CONTRIBUTING_ROLE` or `LEAD_ROLE` for the communication artifact |
| **Primary communication** | `75–100` | Primary communication Role for the interaction. **Substantive domain ownership remains with the relevant owning Role in every case** |

**Rule TR-4 — "primary" is about the communication artifact only.** At `75–100` the communication
Role leads the communication workflow. It does not become the lead of the substantive work, does
not acquire any domain conclusion, and does not outrank an owning Role on that Role's own subject.
A high score means the interaction is difficult, not that communication has become the most
important thing about it.

**Rule TR-5 — the score never deactivates a required Role.** No score, however low, removes a
co-activation required by §6, a review required by §5, or a gate required by
`decision-right-gap-analysis.md`.

## 5. High-stakes conditions

`high_stakes_communication = true` where **any** of the following is present:

| # | Condition |
|---:|---|
| H1 | Threatened or live litigation, or a pre-action communication |
| H2 | A contractual admission, waiver, variation or reservation of rights |
| H3 | Audience includes a board, donor, lender, regulator, granting authority or court |
| H4 | A public statement, a media contact, or content that may be published |
| H5 | A formal complaint, or a response to one |
| H6 | A funding, grant or disbursement consequence |
| H7 | Termination, exclusion, suspension or a final warning |
| H8 | Material reputational exposure |
| H9 | Sensitive or special-category personal data in the material or the draft |
| H10 | An irreversible commitment, or an act that is costly to reverse |
| H11 | A critical stakeholder relationship, as declared by the assignment |

When true:

1. `review.high_stakes_external_communication@0.1` is **required** before any transmitting act;
2. `review.communication_strategy@0.1` is **required**;
3. the applicable human Decision Right is identified per `decision-right-gap-analysis.md` §4 —
   `decision.external_publication` for any release outside the entity under its name, plus any
   submission or commitment Right the act also triggers — and only where that resolution
   genuinely returns nothing is the act **blocked** with `human_gate_status: AUTHORITY_ABSENT`;
4. the draft must not be presented as ready to send until 1–3 are complete.

**Rule TR-6 — the flag is set from conditions, never from the score.** A score of 90 with no H
condition is a difficult internal conversation. A score of 20 with H2 present is a high-stakes
external act. Conflating them is how a routine-looking message acquires a contractual admission.

## 6. What routing does not do

**Rule TR-7 — routing is not authority.** Activating a Role confers exactly its Role Card and
nothing more. The score does not create, widen, map or imply any Decision Right.

**Rule TR-8 — the Orchestrator routes; the Router selects models.** The conflict score is an
Orchestrator input. It **must not select a Model Profile**, must not bias model selection, and must
not appear in a routing request as a model constraint. Model execution is chosen by the Router only
after the Orchestrator creates a routing request under approved Phase 9 rules
(ROUTER != ORCHESTRATOR; MODEL != ROLE).

**Rule TR-9 — routing creates no agent.** Activation binds a Role to an assignment for that
assignment. It does not create a persistent agent, a standing assistant or a named persona
(ROLE != AGENT INSTANCE).

**Rule TR-10 — the score is not a quality signal.** It says how contested the interaction is. It
says nothing about whether the output is good, and it is never an input to the Communication
Control Filter, to a review, or to a gate.

## 7. Co-activation rules

**Rule TR-11 — co-activate, do not blend.** Where communication difficulty coexists with a
substantive domain, the Orchestrator activates the communication Role **and** the owning Role. It
never creates a blended role, a composite authority, or a communication Role that "also covers"
the domain.

| Observable condition | Co-activate | Who owns what |
|---|---|---|
| Legal, contractual or dispute exposure | `role.legal_regulatory_lead` | Legal Role owns admissions, reservations and characterisation; communication Role owns framing |
| Procurement or State Aid matter, especially during a live procedure | `role.procurement_state_aid_specialist` | Procurement Role owns what may be said to a bidder |
| Financial or transaction matter | `role.project_finance_transaction_specialist`, `role.financial_modelling_specialist` as applicable | Finance Role owns the numbers and the terms |
| PPP or concession matter | `role.ppp_concession_specialist` | That Role owns the concession position |
| Institutional position | `role.eu_policy_institutional_affairs_specialist` or `role.institutional_affairs_stakeholder_specialist` | That Role owns the position |
| Public release, media, or anything published | `role.institutional_communications_editorial_specialist` | Editorial Role owns public voice; publication is gated by `decision.external_publication` |
| Personal data or privacy exposure | `role.data_protection_gdpr_specialist` | DP Role owns lawful basis |
| Reputational exposure | `role.institutional_communications_editorial_specialist` plus the applicable decision authority | Editorial owns voice; exposure acceptance is a human Right |
| Employment or people matter | `role.people_organisation_specialist` | People Role owns the employment position |
| Technical factual dispute | `role.sector_technical_expert` or `role.technical_feasibility_lead` | Technical Role owns technical truth |
| Grant or donor matter | `role.eu_grants_programmes_specialist` or `role.eu_programme_implementation_grant_management_specialist` | Programme Role owns programme rules and eligibility |
| Consortium or partner matter | `role.consortium_partner_coordination_specialist`, `role.programme_partnership_manager` | Partnership Role owns the partner position |
| Integrity, fraud or misconduct | `role.integrity_due_diligence_specialist` | Integrity Role owns the finding |
| Executive correspondence at high stakes | the relevant substantive owner **plus** `review.high_stakes_external_communication@0.1` | As above, with the composition review |

**Rule TR-12 — the communication Role may change phrasing and strategy, never the substantive
conclusion.** Where it believes a conclusion is wrong, it raises `CONFLICT_DETECTED` and escalates.
It does not adjust the sentence until the conclusion reads differently (`role-card.md` RC-1).

**Rule TR-13 — a missing owner blocks.** Where a material domain has no approved owning Role, the
instance is `BLOCKED` and escalated to governance. The communication Role does not fill the gap,
and a plausible sentence is not a substitute for an absent conclusion.

## 8. Worked routing examples

Each shows the score, the band, the H conditions, and the co-activation — not to fix behaviour on
these cases, but to make the rules testable.

| Case | Features | Score | Band | H | Routing |
|---|---|---:|---|---|---|
| "Make this reply to a partner firmer but not aggressive" | F3 +15, F5 +18 | 33 | Below threshold — **but explicitly requested** | none | Supporting participation; partnership Role consulted |
| Hostile email from a counterparty alleging delay, contract in force | F1 +25, F5 +18, F9 +12, F8 +10 | 65 | Activate | H2 | Communication Role + `role.legal_regulatory_lead`; both reviews required |
| Donor complaint about reported results | F1 +25, F7 +15, F8 +10 | 50 | Supporting | H3, H6 | Programme Role leads; communication Role supports; high-stakes review required |
| Draft a final warning to an underperforming supplier | F2 +18, F9 +12, F8 +10 | 40 | Supporting | H7, H10 | `role.legal_regulatory_lead` and the contract owner co-activated; high-stakes review and gate required |
| Board member disputes a recommendation in an open thread | F5 +18, F1 +25, F7 +15 | 58 | Activate | H3 | Substantive owner retains the recommendation; communication Role owns framing |
| "Write a reply that destroys their argument point by point" | F1 +25, F6 +12 | 37 | Supporting | none | Activated, and the request itself is refused as an anti-goal; the Role proposes the material-issues reply instead |

The fourth row is the one worth reading twice: a score of 40 is not high, and the act is
irreversible. **TR-6 is what catches it.**

## 9. Calibration status and evidence

The weights in §3 are **declared, not validated**. They were chosen so that each named trigger
class in the source specification reaches at least the supporting band on its own typical
combination, and no single feature forces activation alone.

They must be checked against the evaluation suite before being treated as settled, and
`evaluation-spec.md` §7 defines the routing-accuracy criterion: **100% correct high-stakes
routing and gate identification** on the designated high-stakes cases, with band accuracy treated
as advisory. A weight change is a change to this document and goes through the same change control.

**Rule TR-14 — no silent tuning.** Weights are not adjusted at runtime, not learned in place, and
not varied per user, per counterparty or per outcome. A routing rule that changes itself is a
routing rule nobody can audit.

## 10. Non-Runtime Statement

This document is declarative architecture. It specifies no classifier, orchestration, scheduling,
queueing, agent execution, model routing implementation, database schema, API, interface or
automation code, and binds no model, provider or runtime technology.
