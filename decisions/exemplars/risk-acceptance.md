# Risk Acceptance

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Risk Acceptance
- Decision ID: `decision.risk_acceptance`
- Version: 0.1
- Status: PROPOSED
- Decision Family: Legal / Compliance / Risk Acceptance
- Decision Class: `RISK_ACCEPTANCE_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

## Decision Subject

**One** identified, characterised residual risk, within a declared risk class and below a declared ceiling.

An unquantified or uncharacterised risk cannot be accepted under this Right — not because acceptance would be unwise, but because there is nothing determinate to accept.

## Decision Effect

The entity **carries** the risk knowingly. That is the entire effect, and it is a change in who bears an exposure, not a change in the exposure.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE` | **No effect by itself** | No effect | None | Unchanged | None | **Risk remains recorded**, now as accepted | **Mandatory** |
| `APPROVE_WITH_CONDITIONS` | No effect by itself | No effect | None | Unchanged | None | Risk recorded as accepted; mitigation conditions open and owned | **Mandatory** |
| `REJECT` | No effect | No effect | None | Unchanged | None | Risk remains unaccepted and open | n/a |
| `ESCALATE` | No effect | No effect | None | Unchanged | None | Routed to a higher ceiling | n/a |

**Accepting a risk permits no progression.** That separation is deliberate and is the most easily lost distinction in the registry: accepting the risk and proceeding despite it are two decisions, and in practice they are taken in one breath. Where progression is also required, `decision.exceptional_progression` or the applicable gate Right is exercised **separately**.

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `EXECUTIVE_AUTHORITY` | Executive authority over the exposed unit, within the risk-appetite ceiling | The exposure lands on the unit |
| `GOVERNANCE_BODY_AUTHORITY` | Where the risk exceeds the executive ceiling, or is reputational, integrity-related or regulatory | Above the ceiling the arrangement requires a body |
| `FUNCTIONAL_AUTHORITY` | **Only** within a function's own domain and below its stated ceiling — security risk to security authority, and so on | Beyond its domain a function cannot weigh a consequence falling elsewhere |

`role.enterprise_project_risk_specialist` quantifies and characterises the risk and is **not eligible**: analysing an exposure is not carrying it.

## Cardinality

`SINGLE_HOLDER` within an executive or functional ceiling; **`GOVERNANCE_BODY_DECISION`** above it. The ceiling comes from the organisation's risk-appetite policy, which is an **input to** this registry and not an entry in it — `decision.risk_appetite_setting` is classified as executive policy out of Phase 7 scope for that reason.

## Delegation Policy

**`DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`.**

Delegable downward within a risk class and a stated lower ceiling. **Re-delegation prohibited.** Delegation cannot raise a ceiling, cannot cross into another risk class, and cannot convert a body decision into an individual one.

## Revocation and Supersession

Revocation ends future exercise; **it does not un-accept an accepted risk**, and the entity remains exposed to what it carried. A later decision may supersede the acceptance — by withdrawing it prospectively, or by re-accepting on changed characterisation — and the original acceptance remains in the record with the exposure it described.

## Prerequisites

The risk is **identified, characterised and quantified where quantifiable**, with unquantifiable residual stated as `UNKNOWN` rather than omitted; the evidence basis is stated; mitigation options have been considered and their rejection recorded; and the risk falls within a class and ceiling this Right covers.

## Workflow / Handoff / Review References

`workflow.project_development_readiness` S5; `workflow.risk_assessment_and_register_cycle`; `workflow.software_change_delivery` S4 and S6 via `decision.security_risk_acceptance`; informed by `review.risk_quantification`, `review.security`, `review.esg_safeguards`, `review.legal_compliance`.

## Required Evidence

Beyond the generic eighteen: the risk identifier and its register entry; the characterisation and quantification, or the explicit statement that it is unquantifiable; the residual after mitigation; the mitigation options rejected and why; the ceiling relied on; and the expiry.

## Open Item, Finding and Risk Handling

**The risk remains recorded after acceptance**, in the register, with its acceptance attached. It is not closed, not downgraded and not removed. **A review finding remains a finding after the risk it describes is accepted** — Phase 6 governs findings and this Right does not reach them.

The two together give the rule that matters: an organisation that has accepted every risk on its register still has every risk on its register.

## Expiry / Re-Decision Trigger

**Mandatory expiry.** Re-decision is also required where: the risk's characterisation changes materially; the mitigation assumed at acceptance fails or lapses; the exposure grows beyond the ceiling relied on; or the risk-appetite policy changes.

## Exceptional Progression Rule

**Not within this Right — and no progression of any kind is within it.** Stated explicitly because the inference is so natural: accepting a risk feels like clearing the way, and it is not. Where progression past the accepted risk is also required, `decision.exceptional_progression` or the applicable gate Right is exercised separately, and the risk **remains open** in the register either way.

## Risk / Waiver Boundary

This Right accepts **risk** and waives **nothing**. It does not waive a process requirement, a review, a control or a contractual obligation — a process waiver is separately scoped because its effects differ. And it **cannot accept legal or regulatory nonconformance**: the entity may carry commercial exposure by choice; it cannot decide to be non-compliant with law, and no registry declaration makes that possible.

## Emergency Rule

**None.**

## Knowledge-State Effect

**None.** Acceptance does not resolve `UNKNOWN`, settle `CONFLICT_DETECTED`, or turn an `ASSUMPTION` into a fact. Deciding to live with uncertainty is not the removal of uncertainty.

## Out-of-Scope Authority

This Right does **not**: permit progression; satisfy or relabel any review; close any finding; waive any process, control or obligation; accept legal or regulatory nonconformance; accept a risk outside its declared class or above its ceiling; accept an uncharacterised risk; or accept a risk on behalf of a third party who carries it.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
