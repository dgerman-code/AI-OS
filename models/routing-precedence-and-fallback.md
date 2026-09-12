# Routing Precedence, Fallback and Availability

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Precedence

Eligibility is determined in stages. **Each stage filters the set the next stage sees**, so a later stage can never restore what an earlier one excluded — which is the mechanism, not merely the policy, that stops cost from outranking legality.

| # | Stage | Kind | Effect |
|---:|---|---|---|
| 1 | **Legality and governance** — statutory, regulatory, contractual and organisational prohibitions | Hard | Excludes |
| 2 | **Sensitivity, privacy and residency** — deployment class, jurisdiction, retention posture, maximum sensitivity | Hard | Excludes |
| 3 | **Required capability, modality, context and tooling** | Hard | Excludes |
| 4 | **Independence and diversity** where the task is a review or assurance act | Hard | Excludes |
| 5 | **Lifecycle and availability** — registry status and current availability class | Hard | Excludes |
| 6 | **Quality and reliability preference** | Soft | Ranks |
| 7 | **Latency and cost preference** | Soft | Ranks |
| 8 | **Deterministic tie-break** | Mechanical | Selects |

**Stages 1–5 are hard and cannot be reordered.** Stages 6 and 7 rank only what survives them. Stage 7 sits **after** stage 6 deliberately: within the eligible set, reliability outranks cheapness, so a policy cannot make a less reliable model win by weighting cost — because there is no weighting, only order.

> **Cost and latency preference can never override legality, confidentiality, residency, required capability, review independence, or a criticality requirement.** They operate on a set from which every violation of those has already been removed.

### Deterministic tie-break

Where stages 1–7 leave more than one candidate indistinguishable, selection is made by a **declared deterministic rule stated in the Routing Policy** — for example: the profile with the fresher accepted capability evidence; then the one with fewer limitations bearing on the task; then the lowest stable profile ID in lexical order.

A tie-break is **deterministic and recorded**, never random and never "whichever responded first". Two identical tasks under one policy version select the same candidate, which is what makes a Routing Decision reviewable rather than merely reported.

## 2. Availability

Availability is a **runtime observation** that Phase 9 gives semantics to and does not measure. No probe, monitor, health check or telemetry is defined here.

| Class | Meaning |
|---|---|
| `AVAILABLE` | Believed reachable and serving |
| `DEGRADED` | Reachable with reduced service — slower, rate-limited, partially functional |
| `UNAVAILABLE` | Not serving |
| `UNKNOWN_AVAILABILITY` | Not established |

**Availability is not capability.** An unavailable model has lost none of its claims and gained no limitation; an available one has gained no competence. They are separate properties and a routing record states both.

> **`UNKNOWN_AVAILABILITY` is never silently treated as `AVAILABLE` in high-criticality routing.** At Enhanced Decision-Grade an unknown-availability candidate is **not eligible** at stage 5 until availability is established; at lower bands a policy may permit an attempt, and the decision records that it did so on unknown availability.

Treating unknown as available is the single most attractive shortcut here, because it usually works. The band where it usually works is not the band that matters.

## 3. Fallback

A fallback is **another selection from the eligible set**, made because the first choice cannot be used. **It is never an exemption from the constraints.**

| Kind | Meaning | Permitted when |
|---|---|---|
| `EQUIVALENT_FALLBACK` | A different candidate that satisfies **every** hard constraint and is not materially weaker on the capabilities this task requires | Freely, and recorded |
| `DEGRADED_FALLBACK` | Satisfies every hard constraint but is **materially weaker** on a required capability, freshness or reliability | Only where the policy declares it, only **explicitly**, and with acknowledgement per §4 |
| `PROHIBITED_FALLBACK` | Would breach a hard constraint | **Never.** Not under outage, deadline, cost pressure or absence of alternatives |
| `HUMAN_SELECTION_FALLBACK` | The choice is put to a human among eligible candidates | Where the policy requires it, or where the alternative would be a degraded fallback above the acknowledgement threshold |
| `BLOCK` | No selection is made | Whenever no candidate satisfies every hard constraint |

### The rules that make fallback safe

1. **A fallback satisfies every hard constraint or it is not a fallback.** A candidate that breaches privacy, residency, capability, independence or criticality requirements is not a lesser option; it is not an option.
2. **There is no "best available".** If nothing is eligible, the answer is `NO_ELIGIBLE_MODEL` and the task is `BLOCKED_FOR_ROUTING`.
3. **No silent degradation.** A degraded fallback is **declared as degraded**, names the dimension on which it is weaker, and appears in the Routing Decision as a degraded selection. A degraded fallback recorded as an ordinary selection is a defect in the record, not a routing style.
4. **Degradation does not compound unnoticed.** Each fallback is assessed against the original requirements, never against the previous fallback — otherwise a chain of individually small steps arrives somewhere no single step would have been allowed to go.
5. **Outage is a reason to fall back, never a reason to relax a constraint.** The unavailability of the compliant candidates is not evidence that a non-compliant one has become acceptable.

## 4. Degraded fallback and acknowledgement

| Materiality of the degradation | Requirement |
|---|---|
| Immaterial to the task's purpose | Declared and recorded; ordinary operator selection suffices |
| Material to the task's purpose | **Explicit human acknowledgement**, recorded in the Routing Decision, naming what is weaker and what that risks |
| Material at Enhanced Decision-Grade, or touching review independence, privacy or a Decision-Grade input | **A governed exception under an upstream Phase 7 Decision Right.** Operator acknowledgement is not sufficient |

**Materiality is assessed against the work, not against the model.** A weaker vision claim is immaterial to a text task and disqualifying to a document task, and the same substitution is therefore a different act in each.

## 5. Blocking is a legitimate outcome

`BLOCKED_FOR_ROUTING` is a **correct result**, not a failure of the router. It means the work as specified requires something the available registry cannot lawfully or capably provide, and it hands that fact to the humans who can change the requirements, the registry, the deployment or the timetable.

The alternatives it exists to refuse are: routing to an ineligible model; quietly weakening a requirement until something fits; treating a preference as the constraint that was really meant; and reporting success on work that was performed by something unqualified to perform it.

## 6. Status

`PROPOSED`. Defines no failover service, no health check, no retry policy, no circuit breaker and no runtime.
