# Routing Decision Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Routing Decision** records that **one task instance** selected one execution candidate, and why. It is an instance; the Routing Policy is the type.

**A Routing Decision is not a Decision Record.** It approves no work, accepts no risk, satisfies no review, promotes no knowledge and creates no authority — however senior the person who made the selection. It is a **semantic record model**, not a schema.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## 1. Task context
| # | Element |
|---:|---|
| 1 | Task / work item reference |
| 2 | Role and activity context — **the Role that owns the work, never a model acting as one** |
| 3 | Criticality band, from `architecture/project-criticality-policy.md` |
| 4 | Material data sensitivity, from Phase 8 |

## 2. Requirements applied
| # | Element |
|---:|---|
| 5 | Required capabilities, with the class required for each |
| 6 | Required modality, context class, tool use and structured output |
| 7 | Prohibited conditions — providers, deployments, families, contexts |
| 8 | Diversity requirement and **the named prior Routing Decision** it was evaluated against |
| 9 | Cost, latency, privacy and residency constraints applied, and whether each was hard or soft |

## 3. Candidate assessment
| # | Element |
|---:|---|
| 10 | Candidate set considered |
| 11 | **Eligibility result per candidate, with the constraint that excluded each ineligible one** |
| 12 | Declared fallback candidates, in order |

Element 11 is what makes the decision reviewable rather than merely reported: a record listing only the winner cannot be questioned, because the question is always *what else was there, and why not*.

## 4. Selection
| # | Element |
|---:|---|
| 13 | Selected `model.<id>` **and profile version** |
| 14 | Selected `provider.<id>` and `deployment.<id>`, **with versions** |
| 15 | `routing_policy.<id>` **and policy version** |
| 16 | Reason for selection — which preference or tie-break decided it |
| 17 | Availability class of the selected candidate **at selection time**, including `UNKNOWN_AVAILABILITY` where that is what it was |

Elements 13–15 are what make the selection reproducible after the model behind the name has changed or gone. **A name without a version reproduces nothing.**

## 5. Exceptions and human involvement
| # | Element |
|---:|---|
| 18 | Human selection, requirement or prohibition, where one occurred |
| 19 | Fallback kind where this was a fallback: `EQUIVALENT_FALLBACK` / `DEGRADED_FALLBACK` / `HUMAN_SELECTION_FALLBACK` |
| 20 | **Where degraded: the dimension on which it is weaker, the acknowledgement, and the Phase 7 exception reference where one was required** |
| 21 | Outcome where nothing was eligible: `NO_ELIGIBLE_MODEL` / `BLOCKED_FOR_ROUTING`, with the unsatisfiable constraint named |

Element 20 is the anti-silent-degradation element. **A degraded fallback recorded as an ordinary selection is a defect in the record**, not a routing style.

## 6. Time and lineage
| # | Element |
|---:|---|
| 22 | Timestamp and effective context (runtime) |
| 23 | Provenance and audit history — append-only |
| 24 | Supersedes / superseded-by, where a later decision replaced this one |

## What a Routing Decision is not

- **not a Decision Record** — it selects a tool; Phase 7 governs authority;
- **not an approval of the work** the model then performed;
- **not evidence the output is correct** — output is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`;
- **not a review satisfaction** — routing has no effect on review status, in either direction;
- **not editable** — a correction is a new linked decision, and history is preserved through deprecation, retirement and provider disappearance alike.

## Non-Runtime Statement
This record is declarative architecture. It specifies no schema, storage, API, SDK, credential, endpoint, telemetry or runtime, and binds no person, organisation or provider.
