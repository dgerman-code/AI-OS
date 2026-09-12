# Exemplar 3 — Independent assurance requiring a different model family

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that model diversity and reviewer independence are **two controls**, and that satisfying one says nothing about the other.

## Task context
Independent assurance review of a financial model. Phase 6 independence class **`INDEPENDENT_ASSURANCE_REVIEW`**. Review Profile declares **`DIFFERENT_MODEL_FAMILY_REQUIRED`**. Criticality **Enhanced Decision-Grade**.

## Candidate universe

Bound before any filtering or ranking, per `models/routing-precedence-and-fallback.md` §1.

| Element | Value |
|---|---|
| **Registry state reference** | `reg.snapshot.2026-09-11T04:00Z#4476` |
| **Universe definition version** | `cud.independent_assurance` v2 |
| **Inclusion rule** | Every `ROUTABLE` Model Profile version paired with the internally-approved deployment classes. **The producing family is not pre-excluded**: family diversity is an eligibility constraint evaluated at stage 4, so the producer's family is enumerated and then excluded with the constraint named. **Availability pre-enumeration: no** |
| **Routing scope** | Routable profile versions × internally-approved deployment classes × the internal provider allowlist |
| **Pre-filter exclusions** | `NONE` |
| **Enumerated candidate set** | **4**: `model.frontier_reasoning_b` v5; `model.frontier_reasoning_b` v6; `model.midsize_analyst_d`; `model.compact_general_a` |
| **Omission reasons** | `NONE` — every registered candidate inside the scope is enumerated |
| **Completeness result** | **`CANDIDATE_UNIVERSE_COMPLETE`** |
| **Behaviour if incomplete** | Policy `rp.independent_assurance` v4 declares **`ESCALATE`** on `CANDIDATE_UNIVERSE_INCOMPLETE`: a diversity requirement assessed over a partial set could report diversity that does not exist, so a human decides rather than the router proceeding |

## The named prior selection
Routing Decision `rd.2026.model_build.0412` — the producing task used `model.frontier_reasoning_b` v5, family `family.reasoning_b`. **Without that record the diversity constraint would be unsatisfiable and routing would block**, because "different from what?" has no answer.

## Candidate assessment
| Candidate | Eligible? | Why |
|---|---|---|
| `model.frontier_reasoning_b` v5 | **No** | Same family as the producer. Excluded at **stage 4** |
| `model.frontier_reasoning_b` v6 | **No** | Different *version*, same family. Version diversity is the weakest form and **is not what was required** |
| `model.midsize_analyst_d` | **Yes** | Family `family.analyst_d`; `STRONG` on `capability.code_review`, on current internal evaluation — the dimension this task actually turns on, which is not the same as the dimension that produced the artifact |
| `model.compact_general_a` | **No** | Reasoning class below the band minimum |

## Selection
`model.midsize_analyst_d`, satisfying family diversity and the band's evidence requirements.

## The two controls, kept apart
The reviewer is **organisationally independent** because Phase 6 says who may review and under which class. The model is **family-diverse** because Phase 9 says a different lineage must run it. Both are present here, and **neither produced the other**:

- had the same family been used, the review would still be `INDEPENDENT_ASSURANCE_REVIEW` — independent, and exposed to whatever that lineage systematically fails to notice;
- had the producer re-run their own work on a different family, it would be model-diverse and **not independent at all**.

**Routing changed nothing about the review's status.** Whether it is `SATISFIED` is Phase 6's question, decided by findings, and no model selection reaches it.

**Why family and not provider:** `DIFFERENT_PROVIDER_REQUIRED` would have left exactly one eligible candidate here — a diversity requirement producing a single point of failure. It was not imposed, and the policy records that.
