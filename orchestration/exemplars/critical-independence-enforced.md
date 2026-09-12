# Exemplar 2 — A critical project where independence is two controls, not one

Status: PROPOSED — Phase 11 exemplar execution run
Inherits: `standard.orchestration.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that reviewer independence and model diversity are separate requirements, that the orchestrator enforces both mechanically because it is the component that can see both, and that it relaxes neither when no eligible party is available.

## The run

`run.2026.valuation.0117` · `workflow.valuation_assurance` @ v4 · scope `project.epsilon` · criticality **Enhanced Decision-Grade** · sensitivity {`CONFIDENTIAL`}.

Two separate controls apply:

| Control | Source | Value |
|---|---|---|
| Reviewer independence | **Phase 6**, `review.assurance` | `INDEPENDENT_ASSURANCE_REVIEW` |
| Model diversity | **Phase 9**, `routing_policy.decision_grade` @ v5 | `DIFFERENT_MODEL_FAMILY_REQUIRED` |

## Stage 2 — production

Routing request submitted with the stage's declared constraints. Router returned `rd.2026.val.0301`, selecting a profile in family `family.analyst_d`. The Assignment Envelope recorded:

- field 8, **review restrictions**: the producing assignee is excluded from `review.assurance` on this artifact;
- field 6, **required independence**: the downstream review's class, carried forward.

## Stage 3 — the review, and two checks that are not the same check

| Check | Mechanism | Result |
|---|---|---|
| **Reviewer independence** | The producing assignee is excluded by the envelope; the candidate reviewer is a different person meeting `INDEPENDENT_ASSURANCE_REVIEW` | Satisfied |
| **Model diversity** | The review's routing request carries `rd.2026.val.0301` as the **named prior selection**, so Phase 9 evaluates `DIFFERENT_MODEL_FAMILY_REQUIRED` against something real | Satisfied — `rd.2026.val.0318`, family `family.reasoning_b` |

**Neither produced the other.** Had the same family reviewed, the review would still have been independent — and exposed to whatever that lineage systematically fails to notice. Had the producer re-run their own work on a different family, it would have been model-diverse and not independent at all.

## The moment the constraint bit

At the first attempt, the only reviewer available with the required independence class was the person who had performed related work on the same subject earlier in the programme — which the envelope's review restrictions recorded.

The outcome was **`BLOCKED`**, wait reason recorded, escalated to name a reviewer.

It was **not**:

- a relaxed independence class, because criticality may raise requirements and never lowers them;
- a "closest available" reviewer, because there is no partial independence;
- a decision for the orchestrator, which can see the conflict precisely because it made both assignments, and which has no authority to resolve it.

## What this shows

The orchestrator is the only component positioned to check both controls at once, and that is exactly why it is given authority over neither. **Seeing a conflict and being allowed to resolve it are different things**, and a coordinator that could relax a class to unblock itself would relax it every time the alternative was waiting.
