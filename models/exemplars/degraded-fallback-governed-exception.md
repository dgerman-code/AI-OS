# Exemplar 9 — Exception-adjusted re-evaluation, and what an exception does not reach

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that a candidate failing an eligibility constraint is **never called eligible** until a governed act changes the requirement — and that adjusting model diversity **does not touch reviewer independence**.

**This exemplar was rewritten after the independent audit.** Its first version called a `BASELINE` candidate eligible while `STRONG` was required, then reached for a Phase 7 exception because the requirement was unmet. That is contradictory, and it also said that dropping model-family diversity waives review independence, which conflates two controls. Both are corrected below, and the correction is the lesson.

## Task context
Code review of a security-relevant change, feeding a release gate. Criticality **Enhanced Decision-Grade**. Review Profile `review.software_security_change` declares **two separate controls**: Phase 6 independence class `INDEPENDENT_ASSURANCE_REVIEW`, **and** Phase 9 `DIFFERENT_MODEL_FAMILY_REQUIRED` against the producing decision `rd.2026.change.0918`.

## Candidate universe
Registry state `reg.snapshot.2026-09-12T08:00Z#4491`; universe definition `cud.decision_grade_code_review` v2. Enumerated: 4. **`CANDIDATE_UNIVERSE_COMPLETE`.**

## What happened
The only candidate satisfying both family diversity and `capability.code_review` `STRONG` on current internal evaluation became **`SUSPENDED`** after an incident. The remaining diverse-family candidate claims `capability.code_review` at **`BASELINE`**.

## Step 1 — evaluation under the current policy

| Candidate | Eligible? | Excluded by |
|---|---|---|
| `model.reviewer_h` @ `deployment.tenant_internal_h` | **No** | Primary lifecycle state `SUSPENDED` — `LIFECYCLE_ROUTABLE` fails, `ABSOLUTELY_NON_WAIVABLE` |
| `model.midsize_analyst_d` @ `deployment.tenant_internal_d` | **No** | **`REQUIRED_CAPABILITY` `capability.code_review` `STRONG` — claim is `BASELINE`** |
| `model.frontier_reasoning_b` @ `deployment.tenant_internal_b` | **No** | Same family as the producer — `MODEL_DIVERSITY_REQUIRED` fails |
| `model.compact_general_a` @ `deployment.tenant_internal_a` | **No** | `capability.code_review` `NOT_CLAIMED` |

**Result: `NO_ELIGIBLE_MODEL`.** Four candidates, none eligible. **This result is recorded and is never overwritten**, whatever happens next.

## Step 2 — exceptionability, before anything else

| Failed constraint | Class | Adjustable? |
|---|---|---|
| `LIFECYCLE_ROUTABLE` (`SUSPENDED`) | `ABSOLUTELY_NON_WAIVABLE` | **No** |
| `capability.code_review` `STRONG` | `GOVERNED_EXCEPTION_POSSIBLE` — the policy names `decision.model_capability_threshold_exception` as covering minimum-capability thresholds | **Yes, by that Right** |
| `MODEL_DIVERSITY_REQUIRED` | `GOVERNED_EXCEPTION_POSSIBLE` | Yes in principle — **not taken here**, see below |

Two of the four failures are unadjustable on their face. The question is therefore narrow: is there a named Right covering *this* constraint class? "A Decision Right exists" would not be a basis.

## Step 3 — the governed act

A human holding `decision.model_capability_threshold_exception` exercises it, producing a Decision Record with a **bounded, expiring** effect: for **this review only**, the minimum `capability.code_review` class is `BASELINE`, expiring when the suspension resolves or in fourteen days, whichever is sooner.

**This creates an exception-adjusted routing context** — the policy's requirement set, differing in exactly one named constraint.

## Step 4 — re-evaluation against the adjusted context

| Candidate | Eligible **under the adjusted context**? |
|---|---|
| `model.midsize_analyst_d` @ `deployment.tenant_internal_d` | **Yes** — every constraint of the adjusted set is met |
| The other three | **No** — their failures were untouched by the adjustment |

Selected: `model.midsize_analyst_d`, **eligible under the adjusted context only**, never under the original policy.

## What the Routing Decision records

The original constraint; **the original ineligibility result**; the exceptionability class; the `decision.model_capability_threshold_exception` reference and its Decision Record; the exact adjusted constraint and its bounded effect; the expiry; and the re-evaluated result. **Nothing is rewritten.** The record says a requirement was unmet, a human changed the requirement within their authority, and the work then proceeded — which is what happened.

## What the exception did **not** reach

| | Effect |
|---|---|
| `model.reviewer_h`'s suspension | **Untouched.** `ABSOLUTELY_NON_WAIVABLE`; no Right reaches it |
| **Reviewer independence** | **Untouched, and unreachable.** The review is still `INDEPENDENT_ASSURANCE_REVIEW` under Phase 6, performed by an independent reviewer. **No routing act waives it** |
| Model-family diversity | **Untouched — it was never adjusted.** The selected candidate satisfies it |
| Whether the review is `SATISFIED` | **Phase 6's question**, decided by findings. Routing does not reach it |
| The strength of the review | **Unchanged by the exception.** A weaker instrument was authorised; the exception records the cost, it does not pay it |

The first version of this exemplar said that dropping family diversity would "waive an independence control". **It would not, and cannot.** Model-family diversity is an **execution** control: reducing it reduces protection against correlated model failure and nothing else. **Reviewer independence is an organisational property of who reviews** — Phase 6's, waived if ever by Phase 6 and Phase 7 acting on the review itself, never by a routing choice, an acknowledgement, or any Right exercised over a routing constraint. Where a Review Profile requires both, they are **two controls**, and an exception to one leaves the other exactly as it was.

## Three acts, still kept apart

1. **Operator choice** — selecting among eligible candidates. Here there were none, so there was nothing to choose.
2. **Acknowledgement** — recording that someone knows about a degradation on a **preference**. It **adjusts no requirement**, and would have been useless here: the shortfall was an eligibility constraint.
3. **Governed exception** — a named Right adjusting a named adjustable constraint, **before** re-evaluation.

The available alternative throughout was **`BLOCKED_FOR_ROUTING` until the suspension resolves** — and it remains the right answer whenever no Right covers the failed constraint, which is most of the time.
