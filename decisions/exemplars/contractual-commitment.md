# Contract Commitment

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Contract Commitment
- Decision ID: **`decision.contract_commitment`**
- Version: 0.1
- Status: PROPOSED
- Decision Family: Financial / Commercial / Contractual Commitment
- Decision Class: `COMMITMENT_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

**Upstream ID preserved** — the prompt named this `decision.contractual_commitment`; upstream uses `decision.contract_commitment` across several Role Cards. The difference is orthographic and renaming would gain nothing.

## Decision Subject

Binding the entity to **one** contractual obligation set, at a stated document version, with a named counterparty.

## Decision Effect

Creates a legally binding obligation. This is the least reversible act in the registry: once given, the commitment is the counterparty's right, and nothing in this registry can withdraw it.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE` | Commitment step completes | n/a | **Entity bound** | Unchanged | None | Retained against the committed version | Version-bound |
| `APPROVE_WITH_CONDITIONS` | Completes once conditions are met **before** execution | n/a | Binding only once conditions are met | Unchanged | None | Conditions open, owned, **pre-execution** | **Mandatory** |
| `REJECT` | Blocked | n/a | None | Unchanged | None | Retained | n/a |
| `DEFER` | Not permitted | n/a | None | Unchanged | None | Retained | n/a |
| `ESCALATE` | Not permitted here | n/a | None | Unchanged | None | Retained | n/a |

Conditions are **pre-execution** only. A "condition" to be met after signature is a contractual term, negotiated with the counterparty — not a condition of this decision.

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `LEGAL_ENTITY_SIGNATORY_AUTHORITY` | Authority to bind the legal entity | Nothing less can create an obligation enforceable against it |
| `GOVERNANCE_BODY_AUTHORITY` | Where value, duration or risk exceeds the threshold the arrangement sets for individual signature | Above the threshold the arrangement requires a body |

**No other class is eligible, at any value.** `role.legal_regulatory_lead` reviews the contract and does not sign it; `role.project_finance_transaction_specialist` owns the transaction process and explicitly does not own negotiation, commitment or execution; the sponsor wants the deal, which is not authority.

## Cardinality

`SINGLE_HOLDER` where the arrangement permits individual signature at the value; **`MULTI_HOLDER_ALL_REQUIRED`** where dual signature is required; **`GOVERNANCE_BODY_DECISION`** above the body threshold. **A dual-signature requirement is one decision with two required holders, not two decisions** — the registry uses cardinality rather than chained pseudo-decisions for dual control.

## Delegation Policy

**`DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`.**

Delegable only within `LEGAL_ENTITY_SIGNATORY_AUTHORITY`, under an instrument the governing arrangement recognises, bounded by counterparty class, value ceiling and period. **Re-delegation prohibited.** Delegation cannot reduce dual signature to one and cannot exceed the delegator's own ceiling.

## Revocation and Supersession

Revoking signature authority ends future exercise and **does not unbind an executed contract**. A variation or novation is a **new commitment decision**; it supersedes the earlier commitment's operative terms without erasing the record of what was originally committed. Termination of a contract is a further separate decision under the contract's own terms.

## Prerequisites

The document exists at a stated version; `review.legal_compliance` is `SATISFIED` over the analysis, or `decision.exceptional_progression` has been exercised over each named unsatisfied element; risk allocation is analysed; `decision.risk_acceptance` is taken where residual risk exceeds the acceptance ceiling; tax and State Aid positions are taken where triggered; and counterparty screening is complete where integrity exposure exists.

## Workflow / Handoff / Review References

`workflow.contract_review_cycle`; `workflow.transaction_execution_preparation`; `workflow.partnership_development`; informed by `review.legal_compliance`, `review.commercial_structure`, `review.integrity_due_diligence`, `review.tax_analysis`.

## Required Evidence

Beyond the generic eighteen: the document version committed; the counterparty and its screening status; the legal review status at decision time; the risk allocation position and any separate risk acceptance; the value and duration; and the authority instrument relied on.

## Open Item, Finding and Risk Handling

Open findings **remain open and become findings about a binding obligation**. This is the sharpest escalation of consequence in the registry: a legal finding open at commitment is an exposure the entity now carries contractually, and the record states it as such.

## Expiry / Re-Decision Trigger

Bound to the document version. **Any change to the document after decision and before execution voids the decision.** This is stated firmly because last-minute counterparty edits are the normal case, and a commitment decision on a superseded draft is no decision at all.

## Exceptional Progression Rule

**Not within this Right.** Committing with an unsatisfied legal review requires `decision.exceptional_progression` first, over each named element.

## Risk / Waiver Boundary

Accepts **no** risk by itself — residual risk above the acceptance ceiling requires `decision.risk_acceptance` separately, and the two are deliberately not combined so that "we signed it" never doubles as "we accepted the risk". Waives no process requirement. **Cannot waive law or regulation**, and cannot make enforceable a term the applicable law does not permit.

## Emergency Rule

**None.** There is no emergency contractual commitment. Where speed is genuinely required, the answer is a delegation instrument set up in advance, not authority improvised at the moment.

## Knowledge-State Effect

**None.**

## Out-of-Scope Authority

This Right does **not**: create or endorse a legal conclusion (`decision.formal_legal_opinion`); accept risk; approve the budget the commitment draws on (`decision.budget_approval`); commit a partner or consortium member; authorise payment or a financial claim; satisfy any review; or bind any entity other than the one whose signatory authority was exercised.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
