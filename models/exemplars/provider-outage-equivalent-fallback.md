# Exemplar 6 — Provider outage causing an equivalent fallback

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that outage is a reason to **fall back within the eligible set**, never a reason to relax a constraint.

## Task context
Scheduled batch summarisation of meeting records. Criticality **Routine / Standard**. **Material sensitivity labels: `CONFIDENTIAL` + `PERSONAL_DATA`** (the records name attendees). Preferred candidate: `model.compact_general_a` @ `deployment.tenant_internal_a`.

## Candidate universe

Bound before any filtering or ranking, per `models/routing-precedence-and-fallback.md` §1.

| Element | Value |
|---|---|
| **Registry state reference** | `reg.snapshot.2026-09-11T06:00Z#4479` |
| **Universe definition version** | `cud.batch_summarisation` v1 |
| **Inclusion rule** | Every `ROUTABLE` Model Profile paired with every registered deployment of that profile. **Availability pre-enumeration: no** — unavailable candidates are enumerated and evaluated, so an outage is visible in the record rather than absent from it |
| **Routing scope** | Routable profiles × all registered deployments × the internal provider allowlist |
| **Pre-filter exclusions** | `NONE` |
| **Enumerated candidate set** | **3**: `model.compact_general_a` @ `deployment.tenant_internal_a` (**`UNAVAILABLE`**, and enumerated anyway); `model.summariser_f` @ `deployment.tenant_internal_f`; `model.compact_general_a` @ `deployment.public_hosted_a` |
| **Omission reasons** | `NONE`. In particular, **no candidate was omitted for being unavailable** — availability is a candidate property evaluated at stage 5, never a reason to disappear from the universe (`models/routing-precedence-and-fallback.md` §1.3) |
| **Completeness result** | **`CANDIDATE_UNIVERSE_COMPLETE`** |
| **Behaviour if incomplete** | Policy `rp.batch_summarisation` v2 declares **`BLOCK`** on `CANDIDATE_UNIVERSE_INCOMPLETE`. An outage and a failed registry read look alike from inside the router, and one of them must never be routed through |

## What happened
At routing time the preferred deployment's availability class was **`UNAVAILABLE`**.

## Candidate assessment
| Candidate | Eligible? | Fallback kind |
|---|---|---|
| `model.compact_general_a` @ `deployment.tenant_internal_a` | **No** — supports both labels, but `UNAVAILABLE` at stage 5 | — |
| `model.summariser_f` @ `deployment.tenant_internal_f` | **Yes** | **`EQUIVALENT_FALLBACK`** — supports {`CONFIDENTIAL`, `PERSONAL_DATA`} with handling controls met for each; meets every other eligibility constraint; `STRONG` summarisation on current internal evaluation; not materially weaker on anything this task requires |
| `model.compact_general_a` @ `deployment.public_hosted_a` | **No** | **`PROHIBITED_FALLBACK`** — the same model, available, at a deployment supporting {`PUBLIC`, `INTERNAL`}: **neither required label** |

## Selection
`model.summariser_f` @ `deployment.tenant_internal_f`, recorded as `EQUIVALENT_FALLBACK`, with the preferred candidate's `UNAVAILABLE` status recorded as the reason.

## What this actually shows
The third row is the whole exemplar. **The preferred model was available** — through a deployment the task's sensitivity forbids. Under outage pressure that route is the obvious one, and it is not a lesser option: it is not an option.

**Availability is not capability, and it is not eligibility either.** The unavailability of compliant candidates is not evidence that a non-compliant one has become acceptable, and the fallback was assessed against the **original requirements**, not against what was reachable.

Note also what the first row is **not**: it was enumerated, evaluated, and excluded **with availability named**. Had the policy dropped unavailable candidates before enumeration, the record would have shown two candidates and no outage — the same selection, with the reason for it invisible.

This is **case A** of `models/routing-precedence-and-fallback.md` §5: the chosen candidate satisfies every eligibility constraint, so no governed exception arises. Nothing here was excepted.

Had no equivalent candidate existed, the correct outcome would have been `BLOCKED_FOR_ROUTING` — exemplar 7 — and not the third row with an explanation attached.
