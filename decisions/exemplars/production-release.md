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
| `APPROVE_WITH_CONDITIONS` | Release proceeds **only once every pre-release condition is met** | n/a | Live once every **pre-release condition** is met; **post-release obligations do not gate going live** | Unchanged | None | Pre-release conditions **must be closed before the gate is satisfied**; post-release obligations remain open, owned and carried | **Mandatory** |
| `REJECT` | Blocked | n/a | None | Unchanged | None | Retained | n/a |
| `DEFER` | Not permitted; gate unsatisfied | n/a | None | Unchanged | None | Retained | n/a |

### Pre-release conditions and post-release obligations are different things

`APPROVE_WITH_CONDITIONS` may carry both classes, and **it may carry them only if the decision names each one as one or the other.** An unclassified condition is a defect in the decision, not a matter of interpretation.

| | **Pre-release condition** | **Post-release obligation** |
|---|---|---|
| What it is | Something that must be true **for the release to be authorised** — a re-run test, a fix to a blocking defect, a sign-off the readiness position depends on | Something owed **about a change that is already live** — a monitoring window, a staged rollout step-up, a follow-up measurement |
| Effect on the gate | **The gate is not satisfied and the change does not go live until it is met.** | None. The gate was satisfied without it. |
| Where it may be open | Only before deployment | Only after deployment |
| If it fails | The release is not authorised; the decision is re-taken | The declared re-decision, escalation or rollback path is triggered |

Rules this card holds itself to:

1. **Any pre-release condition material to release authorisation is met before the gate is satisfied and before the change is live.** There is no state in which the change is live and a material pre-release condition is still open.
2. A post-release obligation may remain open after release **only** where it does not invalidate release readiness; is explicitly classified as post-release in the decision; is carried into the Decision Record; and has a named owner and an expiry or revisit trigger.
3. **Failure of a post-release obligation triggers the declared re-decision, escalation or rollback path.** It does not retroactively invalidate the release, and the original decision is not treated as never having existed — the record stands and a new one supersedes it.
4. **"Conditions are met" is not used here to mean anything other than pre-release conditions.** Where the phrase would be ambiguous, this card names the class.
5. **`APPROVE_WITH_CONDITIONS` cannot be used to move a material pre-release blocker past the gate.** Doing that is exceptional progression, and it requires `decision.exceptional_progression` — a separate Right, held by someone else under the separation relationship below.

This is the one Right where a post-release obligation is legitimate at all, because a live change is a thing that can still be watched. That legitimacy does not extend backwards into the authorisation.

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

## Decision Right Separation (`DECISION_RIGHT_SEPARATION`)

| Related `decision.<id>` | Objective activation condition | Mode | Bounded subject / context | Reason |
|---|---|---|---|---|
| `decision.risk_acceptance` | This release carries a residual risk accepted under that Right, on the same change set | **`SEPARATION_REQUIRED`** | This change set and that risk | The declared counterpart of the risk-acceptance card's first row. The person who decided the entity can live with the exposure is not the person who decides to create it. |
| `decision.security_risk_acceptance` | This release carries an accepted residual **security** risk on the same change set | **`SEPARATION_REQUIRED`** | This change set and that security risk | Same control, at the point it is most often collapsed: release authority and security acceptance land in the same escalation path under deadline pressure. |
| `decision.exceptional_progression` | An exception was taken over an unresolved item material to **this** release — an unsatisfied `review.security` or `review.test_coverage`, or an open `MAJOR_FINDING` | **`SEPARATION_REQUIRED`** | This change set and that named item | Otherwise one holder excepts the blocker and then releases past it, which is a single unchecked act wearing two records. |
| `decision.emergency_production_change` | This release normalises, replaces or ratifies a change made earlier under emergency authority for the same incident | **`SEPARATION_REQUIRED`** | That incident and its emergency change | The emergency Right's only compensating control is retrospective scrutiny. If the emergency holder also authorises the normalising release, that scrutiny is self-assessment. |
| `decision.defect_deferral` | A defect deferred under that Right is at or above this band's severity in this change set | **`SEPARATION_REQUIRED`** | This change set and that defect | Same pattern as risk acceptance: deciding a defect can wait and deciding to ship with it are separate judgements. |

**Within-Right cardinality does not satisfy any of these.** A `MULTI_HOLDER_ALL_REQUIRED` release at Enhanced Decision-Grade is still defective if one of its required holders accepted the risk being released. Where no separately eligible release holder exists, the release is not validly authorisable and the gate stays unsatisfied — an unavailable second holder is not an emergency and does not reach `decision.emergency_production_change`.

## Prerequisites

Every acceptance criterion is tested; `review.security` and `review.test_coverage` are `SATISFIED` for the criticality band, or `decision.exceptional_progression` has been exercised over each named unsatisfied one; open defects at or above the band's severity carry `decision.defect_deferral`; residual security risk carries `decision.security_risk_acceptance`; the rollback position is stated; and where the release includes them, `decision.production_database_migration` and `decision.production_infrastructure_change` are separately taken.

## Workflow / Handoff / Review References

`workflow.software_change_delivery` S6 (`HUMAN_GATE_REFERENCE`); `handoff.software_implementation_to_security_and_test_review` (upstream); informed by `review.security`, `review.test_coverage`, `review.code`, `review.architecture`.

## Required Evidence

Beyond the generic nineteen: the change set version; test evidence against each acceptance criterion; the security position and residual risk; open defects with severity and deferral status; the rollback position and its limits; the review statuses at decision time; and the environments the change touches.

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
