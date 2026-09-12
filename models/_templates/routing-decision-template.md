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

## 3. Candidate universe
| # | Element |
|---:|---|
| 10 | **Registry state reference** — a deterministic snapshot or registry version. **A timestamp alone reconstructs nothing** |
| 11 | **Candidate Universe Definition version** — the version of the enumeration rule |
| 12 | **Inclusion rule and routing scope** applied |
| 13 | **Pre-filter exclusions** — candidates outside the universe, with the rule that put them outside |
| 14 | **Enumerated candidate set** |
| 15 | **Omission reasons** for any registered candidate not enumerated |
| 16 | **Completeness result** — `CANDIDATE_UNIVERSE_COMPLETE` or `CANDIDATE_UNIVERSE_INCOMPLETE`, and on incomplete, the policy's declared block-or-escalate outcome |

The universe is bound **before** any filtering. "Where practical" is not a standard: a set nobody can reconstruct cannot be checked for accidental omission, and **a load failure must never silently shrink it** (`models/routing-precedence-and-fallback.md` §1).

## 4. Candidate assessment
| # | Element |
|---:|---|
| 17 | **Eligibility result per enumerated candidate, with the constraint that excluded each ineligible one** |
| 18 | **Availability class per candidate at evaluation time** — an `UNAVAILABLE` candidate is enumerated and excluded with availability named, never made to disappear |
| 19 | Declared fallback candidates, in order |

Element 17 is what makes the decision reviewable rather than merely reported: a record listing only the winner cannot be questioned, because the question is always *what else was there, and why not*.

## 5. Selection
| # | Element |
|---:|---|
| 20 | Selected **Model Profile stable ID** — `model.<id>` |
| 21 | **Registry Profile Version** — the version of the AI-OS record |
| 22 | **Underlying Model Release identity** — the originator's release identity that profile described **at that version** |
| 23 | **Provider Offering Mapping** reference and version |
| 24 | **Provider Profile version** |
| 25 | **Deployment Profile version** |
| 26 | `routing_policy.<id>` **and policy version**, and the **declared preference order** applied |
| 27 | Reason for selection — which preference or tie-break decided it |

Elements 20–25 are the **six-part reproducibility set**, and each is load-bearing. A stable ID names a lineage of records; a registry version names a record; **only the underlying release identity names the thing that actually ran.** Recording the first two without the third leaves the question open precisely when it matters — after a provider has changed something and the profile has moved on.

The mapping, provider and deployment versions complete it: the same release reached through a different mapping or a re-termed deployment is a different set of governance facts, even where the model is identical.

## 6. Acts, exceptions and outcomes
| # | Element |
|---:|---|
| 28 | **Act requirements** that applied, and the acts performed: human selection, acknowledgement, governance review |
| 29 | Fallback kind where this was a fallback: `EQUIVALENT_FALLBACK` / `DEGRADED_FALLBACK` / `HUMAN_SELECTION_FALLBACK` |
| 30 | **Where degraded on a preference or permitted band: the dimension on which it is weaker, and the acknowledgement** |
| 31 | **Where an eligibility constraint failed and was adjusted — the full case-B chain**: the original constraint; **the original ineligibility result**; the constraint's exceptionability class; the Phase 7 `decision.<id>` and Decision Record reference; the exact adjusted constraint and its bounded effect; the **expiry**; and the **re-evaluated** eligibility result |
| 32 | Outcome where nothing was eligible: `NO_ELIGIBLE_MODEL` / `BLOCKED_FOR_ROUTING`, with the unsatisfiable constraint and its exceptionability class named |

Element 30 is the anti-silent-degradation element. **A degraded fallback recorded as an ordinary selection is a defect in the record**, not a routing style.

Element 31 is the anti-retrospective-justification element. **A candidate that failed an eligibility constraint is never recorded as eligible under the original policy** (`models/routing-precedence-and-fallback.md` §5): the original result stands, the governed act is recorded, and eligibility is re-evaluated **against the adjusted context only**. Reversing that order turns a governance record into a justification written afterwards.

**Act requirements change no eligibility.** They withhold finalisation, and element 28 records whether they were met.

## 7. Time and lineage
| # | Element |
|---:|---|
| 33 | Timestamp and effective context (runtime) |
| 34 | Provenance and audit history — append-only |
| 35 | Supersedes / superseded-by, where a later decision replaced this one |

## Cross-Registry Governance References

Every `decision.<id>` and `review.<id>` appearing in a Routing Decision must **resolve to an approved Phase 7 or Phase 6 registry object**, or be explicitly marked **`FUTURE_GOVERNANCE_REFERENCE`** — unresolved, **non-executable**, and incapable of supporting any act recorded here.

**An unresolved governance ID must never appear as though already exercisable.** A decision citing a Right that does not exist has recorded no authority at all, and reads as though it had.

Where a review is conceptually required and no approved Profile matches, record **`REVIEW_PROFILE_NOT_BOUND_IN_PHASE_9`** and keep the path non-executable. Phase 9 binds to Phase 6 and Phase 7; it does not extend them.

## What a Routing Decision is not

- **not a Decision Record** — it selects a tool; Phase 7 governs authority;
- **not an approval of the work** the model then performed;
- **not evidence the output is correct** — output is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`;
- **not a review satisfaction** — routing has no effect on review status, in either direction;
- **not a change to reviewer independence** — model diversity is an execution control; adjusting it leaves Phase 6 reviewer independence exactly as it was;
- **not editable** — a correction is a new linked decision, and history is preserved through deprecation, retirement and provider disappearance alike.

## Non-Runtime Statement
This record is declarative architecture. It specifies no schema, storage, API, SDK, credential, endpoint, telemetry or runtime, and binds no person, organisation or provider.
