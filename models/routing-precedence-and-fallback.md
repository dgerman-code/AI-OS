# Routing Precedence, Fallback and Availability

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. The candidate universe comes first

Filtering presupposes a set to filter. The first draft said a Routing Decision records the candidate set "where practical" — which the audit correctly identified as unauditable: a set nobody can reconstruct cannot be checked for **accidental omission**, and accidental omission is the failure that leaves no trace.

**Every Routing Decision binds to a Candidate Universe Definition before any filtering or ranking occurs.**

### 1.1 What the definition states

| Element | Content |
|---|---|
| **Registry state reference** | A deterministic reference to the registry as it stood — a snapshot identifier, registry version, or equivalent. **Not a timestamp alone**, which does not reconstruct anything |
| **Universe definition version** | The version of the enumeration rule itself |
| **Inclusion rule** | How candidates are enumerated: which profile states, which deployment classes, which provider context |
| **Routing scope** | The bound — e.g. routable profiles × approved deployment classes × the applicable provider allowlist context |
| **Pre-filter exclusions** | Candidates **outside the universe**, with the rule that put them outside |
| **Enumerated candidate set** | Every candidate inside the universe |
| **Omission reasons** | For any registered candidate not enumerated, **why** |
| **Completeness result** | `CANDIDATE_UNIVERSE_COMPLETE` or `CANDIDATE_UNIVERSE_INCOMPLETE` |

### 1.2 Outside the universe versus ineligible inside it

Two different exclusions, and collapsing them is how a shrinking universe hides:

- **Pre-filter exclusion** — the candidate was never in scope. A profile for a deployment class this organisation does not use is outside the universe by the inclusion rule, and its absence is explained by that rule.
- **Hard-constraint exclusion** — the candidate **was** in the universe, was evaluated, and failed a constraint. It appears in the record with the constraint that excluded it.

A candidate that quietly appears in neither list is the defect this section exists to make impossible.

### 1.3 Availability does not remove a candidate from the universe

**Availability is a property of a candidate and a result of evaluating it, not a reason for it to disappear.** An `UNAVAILABLE` candidate is enumerated, evaluated, and excluded at stage 5 **with availability named as the reason** — so the record shows that a compliant option existed and was unreachable, which is a materially different fact from no compliant option existing.

A policy may define pre-enumeration availability filtering, but **only explicitly**, in the inclusion rule, where it can be read.

### 1.4 A shrinking universe is an error, never a silent success

> **A registry load failure, partial fetch, timeout or unreachable source must never silently shrink the universe.**

Where a registered candidate cannot be enumerated for any reason other than the inclusion rule, the universe is **`CANDIDATE_UNIVERSE_INCOMPLETE`**, and the policy declares what follows: **block**, or **escalate** for human selection. It never proceeds as though the missing candidates did not exist.

This matters because the failure mode is invisible from the inside. A router that enumerated three of five candidates and selected the best of three produces a record that looks exactly like a correct decision — **unless the universe was bound first and its completeness recorded.**

### 1.5 A bounded universe is permitted; an unexplainable one is not

The universe need not be the whole registry. It must be **reproducible and explainable**: given the same registry state reference and the same universe definition version, the same enumeration results. That is the whole requirement, and "where practical" does not meet it.

---

## 2. Precedence

Eligibility is then determined in stages over the enumerated universe. **Each stage filters the set the next stage sees**, so a later stage can never restore what an earlier one excluded — the mechanism, not merely the policy, that stops cost from outranking legality.

| # | Stage | Kind | Ownership |
|---:|---|---|---|
| 0 | **Candidate universe binding** (§1) | Precondition | Policy declares the rule; the rule is fixed once declared |
| 1 | **Legality and governance** — statutory, regulatory, contractual and organisational prohibitions | Eligibility | **Globally fixed order** |
| 2 | **Sensitivity, handling and residency** — label support, handling controls, posture, jurisdiction | Eligibility | **Globally fixed order** |
| 3 | **Required capability, modality, context and tooling** | Eligibility | **Globally fixed order** |
| 4 | **Independence and diversity** where the task is a review or assurance act | Eligibility | **Globally fixed order** |
| 5 | **Lifecycle and availability** | Eligibility | **Globally fixed order** |
| 6 | **Preferences, in the policy's declared order** | Preference | **Owned by the versioned Routing Policy** |
| 7 | **Deterministic tie-break** | Mechanical | Policy declares the rule |
| 8 | **Act requirements** — human selection, acknowledgement, governance review | Finalisation | Policy declares which apply |

### 2.1 What is globally fixed, and what the policy owns

The first draft fixed reliability above cost globally while the policy template claimed to own preference ordering. The audit was right that both could not hold.

> **Stages 1–5 are globally fixed and cannot be reordered by any policy.** They are the governance stages, and their order is the architecture.

> **Stage 6 is owned by the versioned Routing Policy**, which declares an **ordered, lexicographic** list of preferences from `models/routing-constraint-model.md` §6. A policy may rank reliability above cost, or cost above reliability, where the work's risk permits.

Three bounds on that freedom:

1. **No preference ordering can restore an ineligible candidate.** Stage 6 operates on what stages 1–5 left.
2. **Where risk requires reliability, it is expressed as an eligibility constraint, not a preference.** `MINIMUM_RELIABILITY_CLASS` at stage 3 is how criticality makes reliability non-negotiable — and that is the correct mechanism, because a preference is always negotiable by definition.
3. **Ordering is lexicographic, not weighted.** No composite score, no tuned weights: a later preference decides only what an earlier one left tied. Opaque scoring is what lets a large enough cost weighting quietly outrank everything else.

### 2.2 Deterministic tie-break

Where stages 1–6 leave more than one candidate indistinguishable, selection is made by a **declared deterministic rule stated in the Routing Policy** — for example: fresher accepted capability evidence; then fewer applicable limitations; then lowest stable profile ID in lexical order.

A tie-break is **deterministic and recorded**, never random and never "whichever responded first". Two identical tasks under one policy version, against one registry state, select the same candidate — which is what makes a Routing Decision reviewable rather than merely reported.

## 3. Availability

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

## 4. Fallback

A fallback is **another selection from the eligible set**, made because the first choice cannot be used. **It is never an exemption from the constraints.**

| Kind | Meaning | Permitted when |
|---|---|---|
| `EQUIVALENT_FALLBACK` | A different candidate that satisfies **every** hard constraint and is not materially weaker on the capabilities this task requires | Freely, and recorded |
| `DEGRADED_FALLBACK` | Satisfies **every eligibility constraint** but is **materially weaker on a dimension the policy treats as a preference or as an explicitly permitted degradation band** | Only where the policy declares it, only **explicitly**, and with acknowledgement per §6 |
| `PROHIBITED_FALLBACK` | Would breach an eligibility constraint | **Never.** Not under outage, deadline, cost pressure or absence of alternatives |
| `HUMAN_SELECTION_FALLBACK` | The choice is put to a human among eligible candidates | Where the policy requires it, or where the alternative would be a degraded fallback above the acknowledgement threshold |
| `BLOCK` | No selection is made | Whenever no candidate satisfies every eligibility constraint |

### The rules that make fallback safe

1. **A fallback satisfies every eligibility constraint or it is not a fallback.** A candidate that breaches privacy, residency, capability, independence or criticality requirements is not a lesser option; it is not an option. **A candidate failing an eligibility constraint is never called eligible** — see §5.
2. **There is no "best available".** If nothing is eligible, the answer is `NO_ELIGIBLE_MODEL` and the task is `BLOCKED_FOR_ROUTING`.
3. **No silent degradation.** A degraded fallback is **declared as degraded**, names the dimension on which it is weaker, and appears in the Routing Decision as a degraded selection. A degraded fallback recorded as an ordinary selection is a defect in the record, not a routing style.
4. **Degradation does not compound unnoticed.** Each fallback is assessed against the original requirements, never against the previous fallback — otherwise a chain of individually small steps arrives somewhere no single step would have been allowed to go.
5. **Outage is a reason to fall back, never a reason to relax a constraint.** The unavailability of the compliant candidates is not evidence that a non-compliant one has become acceptable.

## 5. Three distinct cases, and the one the first draft confused

The first draft's ninth exemplar called a candidate eligible while a required capability class was unmet, then reached for a Phase 7 exception because the requirement was unmet. **The audit was right that this is contradictory**: a candidate is not eligible under a policy whose constraint it fails, and no later act makes it retroactively so.

The three cases are kept apart:

### A. Ordinary eligible fallback

The candidate **satisfies every eligibility constraint of the current policy.** It may be equivalent, or weaker on a dimension that is a **preference** or an **explicitly declared permitted degradation band** — never weaker on an eligibility constraint, because then it is not in case A at all.

Recorded as `EQUIVALENT_FALLBACK` or `DEGRADED_FALLBACK`, with the weaker dimension named. **No governed exception is involved**, because no requirement was unmet.

### B. Exception-adjusted re-evaluation

The candidate **fails an eligibility constraint** of the current policy. Then, in order:

1. **The candidate is ineligible.** The evaluation records that, with the constraint that excluded it. Nothing about that result is later rewritten.
2. **The constraint's exceptionability class is checked** (`models/routing-constraint-model.md` §5). If `ABSOLUTELY_NON_WAIVABLE`, this is case C and stops here.
3. **A named, valid Phase 7 Decision Right whose scope covers that constraint class is exercised by a human**, producing a Decision Record with a bounded, expiring effect.
4. **That governed act creates an exception-adjusted routing context** — a bounded requirement set differing from the policy's only in the named, adjusted constraint.
5. **Eligibility is re-evaluated against the adjusted set.** Only now may a candidate be eligible, and it is eligible **under the adjusted context**, never under the original policy.

The Routing Decision preserves **all** of: the original constraint; the original ineligibility result; the Decision Right and Decision Record reference; the exact adjusted constraint and its bounded effect; the re-evaluated eligibility result; and the expiry. **No part of the original routing history is rewritten** — the record shows a requirement that was unmet and a human who changed the requirement, which is the honest account.

> **A candidate is never called eligible before the governing act changes the applicable requirement set.** Order matters, and reversing it converts a governance record into a justification written afterwards.

### C. Non-waivable constraint failure

No exception path exists — the constraint is `ABSOLUTELY_NON_WAIVABLE`, or no Right covers its class, or none was exercised. The result stays **`NO_ELIGIBLE_MODEL` / `BLOCKED_FOR_ROUTING`**, and no acknowledgement, seniority or urgency changes it.

### The distinction in one line

| | Requirement met? | Governed act? | Candidate eligible? |
|---|---|---|---|
| **A** | Yes, all of them | No | Yes, under the policy |
| **B** | No — then adjusted | **Yes, before re-evaluation** | Yes, **under the adjusted context only** |
| **C** | No, and unadjustable | Not available | **No. Blocked** |

## 6. Degraded fallback and acknowledgement

| Materiality of the degradation | Requirement |
|---|---|
| Immaterial to the task's purpose | Declared and recorded; ordinary operator selection suffices |
| Material to the task's purpose | **Explicit human acknowledgement**, recorded in the Routing Decision, naming what is weaker and what that risks |
| The weaker dimension is an **eligibility constraint**, not a preference | **This is not a degraded fallback at all — it is case B of §5**, and requires the governed act *before* re-evaluation. Operator acknowledgement is not sufficient and is not the mechanism |

**Acknowledgement records that someone knows; it adjusts no requirement** (`models/routing-constraint-model.md` §5.3). Where a requirement must change, only a Phase 7 act changes it.

**Materiality is assessed against the work, not against the model.** A weaker vision claim is immaterial to a text task and disqualifying to a document task, and the same substitution is therefore a different act in each.

## 7. Blocking is a legitimate outcome

`BLOCKED_FOR_ROUTING` is a **correct result**, not a failure of the router. It means the work as specified requires something the available registry cannot lawfully or capably provide, and it hands that fact to the humans who can change the requirements, the registry, the deployment or the timetable.

The alternatives it exists to refuse are: routing to an ineligible model; quietly weakening a requirement until something fits; treating a preference as the constraint that was really meant; and reporting success on work that was performed by something unqualified to perform it.

## 8. Status

`PROPOSED`. Defines no failover service, no health check, no retry policy, no circuit breaker and no runtime.
