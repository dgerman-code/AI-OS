# Exemplar 6 — Provider outage causing an equivalent fallback

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that outage is a reason to **fall back within the eligible set**, never a reason to relax a constraint.

## Task context
Scheduled batch summarisation of meeting records. Criticality **Routine / Standard**. Material sensitivity `CONFIDENTIAL`. Preferred candidate: `model.compact_general_a` @ `deployment.tenant_internal_a`.

## What happened
At routing time the preferred deployment's availability class was **`UNAVAILABLE`**.

## Candidate assessment
| Candidate | Eligible? | Fallback kind |
|---|---|---|
| `model.compact_general_a` @ `deployment.tenant_internal_a` | **No** — `UNAVAILABLE` at stage 5 | — |
| `model.summariser_f` @ `deployment.tenant_internal_f` | **Yes** | **`EQUIVALENT_FALLBACK`** — meets every hard constraint; `STRONG` summarisation on current internal evaluation; not materially weaker on anything this task requires |
| `model.compact_general_a` @ `deployment.public_hosted_a` | **No** | **`PROHIBITED_FALLBACK`** — the same model, available, at a deployment whose maximum sensitivity is `INTERNAL` |

## Selection
`model.summariser_f` @ `deployment.tenant_internal_f`, recorded as `EQUIVALENT_FALLBACK`, with the preferred candidate's `UNAVAILABLE` status recorded as the reason.

## What this actually shows
The third row is the whole exemplar. **The preferred model was available** — through a deployment the task's sensitivity forbids. Under outage pressure that route is the obvious one, and it is not a lesser option: it is not an option.

**Availability is not capability, and it is not eligibility either.** The unavailability of compliant candidates is not evidence that a non-compliant one has become acceptable, and the fallback was assessed against the **original requirements**, not against what was reachable.

Had no equivalent candidate existed, the correct outcome would have been `BLOCKED_FOR_ROUTING` — exemplar 7 — and not the third row with an explanation attached.
