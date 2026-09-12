# Model Router Invocation Boundary

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. `ROUTER != ORCHESTRATOR`

Two questions, two components:

| Question | Answered by |
|---|---|
| What work happens, in what order, by which Role, and whether it is done | **The orchestrator** |
| Which execution capability is eligible and preferred for this bounded work | **The Router**, under Phase 9 |

The orchestrator submits a **Model Invocation Request**. The Router produces a **Routing Decision**. These are two objects, and the request is never recorded as though it were the decision.

## 2. What the request carries and what it may not

| Carries | May not carry |
|---|---|
| The activity and its declared capability requirements | A chosen model, provider or deployment |
| Scope, criticality, sensitivity labels, residency constraints | A relaxed version of any of them |
| The applicable `routing_policy.<id>` @ version, from the definition | A different policy chosen for convenience |
| The required independence class and the named prior selection, where diversity applies | A request to ignore diversity |
| The producing context needed for the candidate universe | A pre-filtered candidate set |

> **The orchestrator does not choose an endpoint where a Routing Policy applies**, and it does not rewrite a routing constraint. A coordinator that could adjust the constraints would be choosing the model with extra steps.

## 3. What comes back

A Routing Decision, or a refusal. Both are recorded, and the refusals are the important half:

| Router outcome | Run effect |
|---|---|
| A Routing Decision naming an eligible candidate | Continue; record the decision by reference |
| `NO_ELIGIBLE_MODEL` → `BLOCKED_FOR_ROUTING` | Run `BLOCKED`. **No fallback outside the eligible set** |
| `CANDIDATE_UNIVERSE_INCOMPLETE` handled per policy | `BLOCKED` or `ESCALATED` as that policy declares |
| `NO_APPLICABLE_DECISION_RIGHT` → `BLOCKED_FOR_ROUTING` / `ESCALATED_FOR_GOVERNANCE_DESIGN` | Run `BLOCKED` **and** `ESCALATED`, posture `AUTHORITY_ABSENT` |

**A block from the Router is a block.** It is not a signal to retry with different constraints, to try another policy, or to ask a human to override — the last of which would be asking a human to exercise an authority nobody has.

## 4. Recording, by reference and by value

An execution records, for each model-assisted step:

- the **Model Invocation Request** ID (runtime);
- the **Routing Decision** reference — `rd.<id>`, **as a recorded value**;
- the outcome class;
- the produced content's Phase 8 classification: `AI_SUGGESTION`, `ORIGIN: AI_GENERATED`.

The execution does **not** re-resolve the model profile at read time. Phase 9's six-part reproducibility set lives in the Routing Decision, and the execution's job is to name which decision it used — so that a question asked a year later reaches what actually ran rather than what the profile says today.

## 5. Retry across models

The failure mode this section exists for: a stage fails, the orchestrator retries, and the retry routes to a different model family — quietly satisfying a diversity constraint that was meant to compare **different work**, or quietly violating one that required sameness.

The rules:

1. A retry of a **failed invocation** re-submits the **same request**. The Router re-evaluates under the same policy and may legitimately return a different decision; that is Phase 9's judgement, recorded.
2. A retry **never** alters the request's constraints, independence class or named prior selection to make a different candidate eligible.
3. Where the stage feeds a review with a diversity requirement, **every** attempt's Routing Decision is recorded, and the diversity check evaluates against the decision that produced the **artifact under review** — not against the last attempt that happened to run.
4. Repeated routing blocks are **not** a retry loop. After the policy's attempt limit the run `ESCALATES`, because the constraint is not going to change by being asked again.

## 6. A model result is not a completed review

Stated once, because it is the collapse that would make everything else decorative:

**A model producing output completes an activity, not a gate.** The output enters Phase 8 as `AI_SUGGESTION`. It becomes reviewed when a reviewer meeting the Profile's independence class satisfies the review; it becomes authorised when an eligible human exercises a Right; it becomes canonical through Phase 8's promotion path. **No confidence score, self-assessment, agreement between two models, or absence of detected problems substitutes for any of the three.**
