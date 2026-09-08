# Exceptional Progression

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Exceptional Progression
- Decision ID: `decision.exceptional_progression`
- Version: 0.1
- Status: PROPOSED
- Decision Family: Workflow / Progression
- Decision Class: `EXCEPTION_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

**New Right, no upstream ID.** Phase 5 and Phase 6 both wrote *"a named external human `decision.<id>` may permit progression"* and no such ID existed anywhere in the registries. This card is that ID. Its existence closes the single largest forward reference in the architecture.

## Decision Subject

One named unresolved item — a `MATERIAL_TO_NEXT_STEP_OR_GATE` open item, an unsatisfied `review.<id>`, an open `MAJOR_FINDING`, an unresolved `CONFLICT_DETECTED` or a gate-critical `UNKNOWN` — at **one** named Workflow stage exit or Handoff transfer.

**One decision, one item, one progression point.** A single exercise of this Right does not clear a list.

## Decision Effect

Permits that one progression to occur with that one item **still unresolved and still open**. It changes nothing about the item.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE_WITH_CONDITIONS` | Permitted past the named point only | Permitted where the Handoff carried the item | **None** — this Right authorises no external act | **Unchanged.** `NOT_SATISFIED` stays `NOT_SATISFIED` | Unchanged | Item **remains open**, carried forward, plus any conditions imposed | **Mandatory** |
| `REJECT` | Blocked; stage outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED` | Not permitted | None | Unchanged | Unchanged | Item remains open | n/a |
| `ESCALATE` | Not permitted; no decision made here | Not permitted | None | Unchanged | Unchanged | Item remains open | n/a |

`APPROVE` without conditions is **not permitted**. An unconditional exceptional progression is a contradiction: if nothing needs conditioning, nothing was exceptional.

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `PROJECT_OR_PROGRAMME_SPONSOR_AUTHORITY` | Sponsor authority over the path being progressed | The consequence lands on the sponsor's objective |
| `GOVERNANCE_BODY_AUTHORITY` | Where the underlying gate is itself a body decision | A body's gate cannot be excepted by an individual |
| `FUNCTIONAL_AUTHORITY` | **Only** where the unresolved item is wholly inside one function's domain and the progression has no cross-domain consequence | Beyond that, no single function can weigh a consequence falling on another |

The Workflow lead is **never** eligible by virtue of leading, and the Role that produced the artifact carrying the item is never eligible over that item.

## Cardinality

`SINGLE_HOLDER` where the unresolved item is confined to one domain; **`MULTI_HOLDER_ALL_REQUIRED`** where it spans domains or the progression point is a terminal gate — the sponsor plus the functional authority for each domain the item touches.

## Delegation Policy

**`NON_DELEGABLE`.**

This Right exists to be exercised deliberately by someone who carries the consequence. Delegation would let exceptional progression become routine by descending to whoever is nearest the deadline — which is the precise failure the Right is built to prevent.

## Revocation and Supersession

Revoking a holder ends future exercise and reverses nothing. A later valid decision may supersede this one — typically when the item is actually resolved, at which point the exception becomes moot rather than retrospectively unnecessary. **This Right cannot reverse itself**; reversing a progression already taken requires a Right whose scope permits reversal.

## Prerequisites

The item must be **named and classified** under Phase 5 §14A; the applicable review's status must be recorded as it stands; the consequence of progressing must be stated; and the Workflow must have reached the progression point by its normal path. **An exception cannot be granted in advance of the situation it excepts.**

## Workflow / Handoff / Review References

Every Phase 5 stage carrying `COMPLETE_WITH_OPEN_ITEMS` restricted to non-material items; every Phase 6 Profile whose satisfaction rules name "a named external human `decision.<id>`" — `review.project_integration_coherence`, `review.eu_programme_compliance`, `review.financial_model`, `review.security`; and every Handoff carrying a `REVIEW_REFERENCE` that must be `SATISFIED` before transfer.

## Required Evidence

Beyond the eighteen generic elements: the item's own identifier and classification; the review's status **at decision time**; the specific consequence accepted; why waiting is worse than proceeding; and the revisit trigger.

## Open Item, Finding and Risk Handling

**The item remains open.** It is carried into every subsequent stage and gate, appears in every downstream Handoff's `OPEN_ITEM_CARRY`, and is not downgraded to `NON_MATERIAL_TO_NEXT_STEP` by this decision. A second progression point past the same item requires a **second exercise** of this Right.

## Expiry / Re-Decision Trigger

**Mandatory expiry**, stated at decision time. The exception also lapses immediately if: the item changes materially; the subject artifact version changes; or the consequence stated proves understated. Lapse returns the progression to blocked and does not undo work already done.

## Exceptional Progression Rule

This Right **is** the exceptional progression rule. All eight conditions of `architecture/decision-rights-registry-design.md` §10 apply, and the fourth is the one that carries the weight: **the Record names the unresolved item.** A record that permits progression without naming what it progressed past is void, not merely incomplete.

## Risk / Waiver Boundary

**This Right accepts no risk and waives no process requirement.** It permits movement past an unresolved item; it does not accept the risk that item represents — that is `decision.risk_acceptance`, a separate decision that may or may not also be taken. It does not waive the review; the review remains required and unsatisfied.

Both distinctions matter because they are the two things a hurried organisation will read this Right as doing.

## Emergency Rule

**None.** This is a deliberate governed exception, not an emergency mechanism. Emergency acts use `decision.emergency_production_change` or the equivalent emergency Right for their domain.

## Knowledge-State Effect

**None whatsoever.** No state transition, in either direction.

## Out-of-Scope Authority

This Right does **not**: satisfy any review; resolve, close, downgrade or reclassify the item; accept risk; approve any artifact; authorise any external act, commitment, publication, submission or release; create a professional conclusion; alter any `FACT`, `ASSUMPTION`, `UNKNOWN` or `CONFLICT_DETECTED`; permit progression past a **second** item, or past the same item at a second point; or waive law or regulation.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no subject, effect, eligibility, cardinality or delegation change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
