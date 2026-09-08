# Production Release

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Production Release
- Decision ID: `decision.production_release`
- Version: 0.1
- Status: PROPOSED
- Decision Family: Product / Software / Security / Release
- Decision Class: `COMMITMENT_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

## Decision Subject

Release of **one** change set, at a stated version, into a production environment serving real users or real data.

## Decision Effect

The change becomes live. Reversibility depends on the change: a code deployment may be rolled back, a data migration may not, and the card requires the rollback position to be stated precisely because the two are routinely treated alike.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE` | S6 exits; release proceeds | n/a — terminal | **Change live in production** | Unchanged | None | Open defects retained with their deferral status | Version-bound |
| `APPROVE_WITH_CONDITIONS` | Release proceeds on stated conditions | n/a | Live once conditions met | Unchanged | None | Conditions open and owned; **monitoring conditions may be post-release** | **Mandatory** |
| `REJECT` | Blocked | n/a | None | Unchanged | None | Retained | n/a |
| `DEFER` | Not permitted; gate unsatisfied | n/a | None | Unchanged | None | Retained | n/a |

This is the one Right where a **post-release condition** is legitimate — a monitoring window, a staged rollout percentage — because the condition governs the live change rather than qualifying the decision. Such conditions carry an owner and a review point.

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `FUNCTIONAL_AUTHORITY` | Release authority over the production environment | The environment's owner carries the availability consequence |
| `EXECUTIVE_AUTHORITY` | Where the change alters a service commitment or carries regulatory exposure | Beyond the technical function's remit |
| `GOVERNANCE_BODY_AUTHORITY` | Where the change is safety-relevant or requires accreditation | The arrangement requires a body |

**`role.platform_devops_engineer` is not eligible by virtue of owning the pipeline.** The Phase 5 card states that building the pipeline is not authority to release through it; this states the same boundary from the authority side, and it is the most common place where operational capability is mistaken for authority.

None of `role.product_manager_business_analyst`, `role.solution_architect`, `role.software_qa_test_automation_specialist` or `role.security_engineer` is eligible. Each contributes to the readiness position; none of them decides.

## Cardinality

`SINGLE_HOLDER` at Routine and Enhanced Review Candidate; **`MULTI_HOLDER_ALL_REQUIRED`** at Enhanced Decision-Grade — release authority plus the functional authority for each domain with an open condition, typically security. `GOVERNANCE_BODY_DECISION` where accreditation applies.

## Delegation Policy

**`DELEGABLE_WITHIN_ELIGIBILITY`**, bounded to a change class and a period, typically for an on-call rotation. **Re-delegation prohibited.** Not delegable where cardinality is `MULTI_HOLDER_ALL_REQUIRED` or a body decision. **A delegation for routine changes does not extend to a change carrying an open `MAJOR` security finding** — the change class bound is real.

## Revocation and Supersession

Revocation ends future exercise. **It does not un-release a live change**; withdrawing one is a new release decision on the reverting change, or an emergency decision where the situation warrants. A later release supersedes an earlier one as the live version; both records stand.

## Prerequisites

Every acceptance criterion is tested; `review.security` and `review.test_coverage` are `SATISFIED` for the criticality band, or `decision.exceptional_progression` has been exercised over each named unsatisfied one; open defects at or above the band's severity carry `decision.defect_deferral`; residual security risk carries `decision.security_risk_acceptance`; the rollback position is stated; and where the release includes them, `decision.production_database_migration` and `decision.production_infrastructure_change` are separately taken.

## Workflow / Handoff / Review References

`workflow.software_change_delivery` S6 (`HUMAN_GATE_REFERENCE`); `handoff.software_implementation_to_security_and_test_review` (upstream); informed by `review.security`, `review.test_coverage`, `review.code`, `review.architecture`.

## Required Evidence

Beyond the generic eighteen: the change set version; test evidence against each acceptance criterion; the security position and residual risk; open defects with severity and deferral status; the rollback position and its limits; the review statuses at decision time; and the environments the change touches.

## Open Item, Finding and Risk Handling

Open defects **remain open in production**. A deferred defect is a live defect with a decision attached, and the deferral does not close it. An open security finding at release becomes an open security finding on a live system — the record states the escalation in consequence.

## Expiry / Re-Decision Trigger

Bound to the change-set version. **Any change to the change set after decision voids the decision** — including a "trivial" rebuild, because what was tested is what was decided on.

## Exceptional Progression Rule

**Not within this Right.** Releasing with an unsatisfied `review.security` requires `decision.exceptional_progression` first. **Release-date pressure is not a basis** — the Phase 5 card denies it and this Right does not create what that card denies.

## Risk / Waiver Boundary

Accepts **no** risk by itself: residual security risk requires `decision.security_risk_acceptance` separately, and defect deferral requires `decision.defect_deferral`. Waives **no** review. Cannot waive a regulatory obligation attaching to the system.

## Emergency Rule

**None — and this is the key boundary of this card.** This Right has no emergency mode, no expedited path and no reduced prerequisite set. A genuine emergency uses `decision.emergency_production_change`, a **separate Right with a different holder class, a time limit and a mandatory retrospective obligation**. Collapsing the two would let every urgent release borrow the emergency Right's reduced prerequisites while keeping this one's absent retrospective duty, which is the worst combination available.

## Knowledge-State Effect

**None.**

## Out-of-Scope Authority

This Right does **not**: authorise a production database migration or infrastructure change; accredit the system (`decision.security_accreditation`); accept security risk; defer a defect; satisfy or relabel any review; approve product scope; commit to a service level (`decision.service_level_commitment`); or authorise an emergency change.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
