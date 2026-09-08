# Stage Gate Progression

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Stage Gate Progression
- Decision ID: **`decision.stage_gate_progression`**
- Version: 0.1
- Status: PROPOSED
- Decision Family: Workflow / Progression
- Decision Class: `PROGRESSION_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

**Upstream ID preserved.** The Phase 7 prompt named this exemplar `decision.project_readiness_progression`; the ID actually in force upstream is `decision.stage_gate_progression`, used at `workflow.project_development_readiness` S7 and in `role.portfolio_programme_manager`. The upstream ID is kept and the divergence recorded in the universe rather than resolved by silently renaming two approved artifacts.

## Decision Subject

Progression of a defined project or programme past **one named stage gate**, on the readiness position presented for that gate.

## Decision Effect

Permits or refuses movement past that gate. It does **not** approve the investment, the financing, the business case or any specialist conclusion the readiness position cites — each of those has its own Right.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE` | Past the named gate | Downstream Handoffs eligible | None | Unchanged | None | Open items carried forward unchanged | Per band |
| `APPROVE_WITH_CONDITIONS` | Past the gate, conditionally | Eligible; conditions carried in the package | None | Unchanged | None | Conditions **open and carried**; each has a named owner | **Mandatory** |
| `REJECT` | Blocked | Not eligible | None | Unchanged | None | Retained; routed to rework | n/a |
| `DEFER` | Not permitted; gate unsatisfied | Not eligible | None | Unchanged | None | Retained | n/a |
| `ESCALATE` | Not permitted here | Not eligible | None | Unchanged | None | Retained | n/a |

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `PROJECT_OR_PROGRAMME_SPONSOR_AUTHORITY` | Sponsor authority over this project or programme | The gate exists to give the sponsor a stopping point |
| `GOVERNANCE_BODY_AUTHORITY` | Where the governing arrangement makes the gate a body decision | At investment-committee gates the body is the gate |

**`role.project_development_lead` is not eligible.** It leads `workflow.project_development_readiness`, assembles the readiness assessment and reaches this gate — and none of that is authority. This is the clearest instance in the registry of leadership not conferring approval power, and the card names it because that is where the confusion actually arises.

## Cardinality

`SINGLE_HOLDER` at Routine and Enhanced Review Candidate; **`GOVERNANCE_BODY_DECISION`** at Enhanced Decision-Grade and above, where the governing arrangement constitutes a body for the gate. A body decision is not one member acting alone, however senior.

## Delegation Policy

**`DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`.**

Delegable from sponsor authority to another holder of sponsor authority, for a named gate on a named project, for a stated period. **Re-delegation prohibited.** Not delegable at all where cardinality is `GOVERNANCE_BODY_DECISION` — a body cannot delegate its own constitution. Delegation never widens the gate's subject and never reduces the cardinality.

## Revocation and Supersession

Revocation ends future exercise and reverses no gate already passed. A later decision at the same gate — after rework — supersedes the earlier one, and both remain visible. **Reversal of a passed gate is not within this Right**; withdrawing a project already past a gate requires `decision.cancellation_or_termination`.

## Prerequisites

`workflow.project_development_readiness` has reached S7 by its normal path; the readiness assessment exists at a stated version; every required review for the criticality band is `SATISFIED` **or** `decision.exceptional_progression` has been separately exercised over each named unsatisfied one; and open items are classified.

## Workflow / Handoff / Review References

`workflow.project_development_readiness` S7 (`HUMAN_GATE_REFERENCE`); `workflow.stage_gate_progression_preparation`; informed by `review.project_readiness`, `review.project_integration_coherence` and `review.evidence_integrity_provenance`.

## Required Evidence

Beyond the generic eighteen: the readiness assessment version; every cited specialist artifact and its version; the status of each required review; the open-item register with classification; the gate criteria the position is assessed against; and what the position explicitly does not establish.

## Open Item, Finding and Risk Handling

Open items pass through unchanged. **Passing a gate resolves nothing** — an item material at S6 is material at S8. Conditions attached under `APPROVE_WITH_CONDITIONS` each carry a named owner and a due point, and remain open until separately closed.

## Expiry / Re-Decision Trigger

Re-decision is required where: a cited specialist artifact is superseded; a material assumption changes; the gate criteria change; or a stated validity period lapses before the next gate is reached.

## Exceptional Progression Rule

**Not within this Right.** Where a required review is unsatisfied, this Right cannot be exercised until `decision.exceptional_progression` is separately exercised over each named item. That separation is deliberate: it makes the number of exceptions taken visible as a count of decisions rather than invisible inside a single gate approval.

## Risk / Waiver Boundary

**None.** This Right accepts no risk and waives no requirement. A gate passed with known risk is a gate passed with known risk; accepting it is `decision.risk_acceptance`.

## Emergency Rule

**None.**

## Knowledge-State Effect

**None.** Passing a gate does not make the readiness assessment `APPROVED` or anything else.

## Out-of-Scope Authority

This Right does **not**: approve an investment, financing or expenditure; approve the business case (`decision.business_case_approval`); accept any specialist conclusion; bind the entity externally; satisfy or relabel any review; accept risk; resolve or close any open item; or authorise any transmitting act where the package is issued to lenders, investors or authorities.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
