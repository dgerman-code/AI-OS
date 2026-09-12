# Review Diversity and Criticality-Aware Routing

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Reviewer independence and model diversity are different things

Phase 6 established review independence at the **reviewer and Profile** level: `PRODUCER_REVIEW`, `PEER_REVIEW`, `CROSS_DOMAIN_REVIEW`, `INDEPENDENT_ASSURANCE_REVIEW`. Phase 9 adds diversity at the **model** level. They are orthogonal, and the four combinations all occur:

| | Model-homogeneous | Model-diverse |
|---|---|---|
| **Organisationally independent** | An independent assurance reviewer using the same model family as the producer — independent, and exposed to shared model failure modes | Both controls present |
| **Not organisationally independent** | Neither control | The producer re-running their own work on a different model — **model-diverse and not independent at all** |

> **`REVIEWER / REVIEW PROFILE INDEPENDENCE != MODEL DIVERSITY`**

**Phase 9 changes nothing in Phase 6.** It adds no independence class, removes none, and cannot make an unsatisfied review satisfied or a non-independent reviewer independent.

> **Reducing or excepting model diversity does not waive reviewer independence, and cannot.** They are two controls. A Phase 7 exception adjusting `MODEL_DIVERSITY_REQUIRED` reduces **execution diversity** and records that; the reviewer, the Review Profile and the independence class are **untouched by it**. Where a Review Profile requires both, both must be separately satisfied, and an exception affecting one leaves the other exactly as it was.

Nothing in Phase 9 can waive reviewer independence — not a routing choice, not an acknowledgement, not any Decision Right exercised over a routing constraint. Reviewer independence is waived, if ever, by Phase 6 and Phase 7 acting on the review itself. A model-diversity requirement is a **routing constraint**; a review independence class is a **review property**; satisfying one says nothing about the other, and the bottom-right cell above is where organisations most often believe otherwise.

## 2. Model diversity policy values

Declared by a Review Profile, a Workflow stage or a Routing Policy — never assumed:

| Value | Requires |
|---|---|
| `SAME_MODEL_ALLOWED` | Nothing. The reviewing task may use the same profile and version as the producing task |
| `DIFFERENT_MODEL_VERSION_REQUIRED` | A different version within the same family |
| `DIFFERENT_MODEL_FAMILY_REQUIRED` | A different model family |
| `DIFFERENT_PROVIDER_REQUIRED` | A different provider **and** therefore a different family |
| `HUMAN_ONLY_REVIEW_REQUIRED` | No model performs the review at all |
| `MODEL_DIVERSITY_NOT_APPLICABLE` | The task is not a review act, or no model is involved |

### What each is actually worth

**Diversity is a control against correlated failure**, and its value depends on which failure the review is meant to catch.

- `DIFFERENT_MODEL_VERSION_REQUIRED` addresses a defect fixed or introduced between versions. It is the **weakest** form: versions of one family share training lineage and typically share blind spots.
- `DIFFERENT_MODEL_FAMILY_REQUIRED` addresses shared blind spots — the class of error one lineage makes systematically and will not detect in its own output. **This is the form that earns its cost most often.**
- `DIFFERENT_PROVIDER_REQUIRED` additionally addresses provider-level concerns: an outage correlated across a provider's models, a contractual or data-handling concern, a supply concentration risk. **It does not add independence beyond family diversity on quality grounds**, which is why it is not a default.
- `HUMAN_ONLY_REVIEW_REQUIRED` is the only value that addresses failure modes **common to all current models**. It is the strongest and the most expensive, and no amount of model diversity substitutes for it.

**`DIFFERENT_PROVIDER_REQUIRED` is never a default.** Imposing it reflexively concentrates cost and shrinks the eligible set, often to one candidate — at which point the diversity requirement has produced a single point of failure, which is the opposite of what it was for.

## 3. Diversity is declared against a named prior selection

A diversity constraint is meaningless in the abstract: different **from what**? It is always evaluated against a **named prior Routing Decision** — normally the one that produced the artifact under review.

Where the prior decision is unknown or unrecorded, the constraint is **unsatisfiable, and routing blocks**. It is not treated as satisfied because nothing contradicts it. This is the concrete reason Phase 9 requires Routing Decisions to be retained: a diversity control over unrecorded history is not a control.

## 4. Criticality-aware routing

Criticality bands are Phase 3's (`architecture/project-criticality-policy.md`) and are **used, not redefined**.

| | Routine / Standard | Enhanced Review Candidate | Enhanced Decision-Grade |
|---|---|---|---|
| Capability evidence | Provider-declared may suffice where the claim is uncontested | Internal or external evidence on the load-bearing capabilities | **Internal evaluation evidence on every load-bearing capability**, within its freshness window |
| Evidence freshness | Stale usable with disclosure | Stale disclosed and scheduled for refresh | **Stale evidence is blocking** |
| Minimum classes | Policy's ordinary minima | Raised on the capabilities the task turns on | Raised, **plus** `MINIMUM_RELIABILITY_CLASS` where output feeds a decision |
| Availability | `UNKNOWN_AVAILABILITY` may be attempted under policy | Attempt recorded | **`UNKNOWN_AVAILABILITY` is not eligible** |
| Review diversity | Per Review Profile; often `SAME_MODEL_ALLOWED` | Per Review Profile | **`DIFFERENT_MODEL_FAMILY_REQUIRED` is the expected value for material independent review**, overridable only with a recorded justification |
| Degraded fallback | Declared, recorded | Declared, with human acknowledgement where material | **A governed exception under a Phase 7 Decision Right** |
| Human selection | Not required | Not required | Where the Workflow or Decision architecture requires it |

**"Expected value", not blanket rule.** Family diversity at Decision-Grade is the default a Review Profile must consciously depart from, with the departure recorded. Making it unconditional would tie a governance requirement to the state of the model market rather than to the risk in the work.

## 5. What criticality does not do

1. **It does not grant a model authority.** A Decision-Grade routing decision selects a tool. Authority is Phase 7's and is held by humans.
2. **It does not make output true.** Stronger evidence about the instrument is not evidence about the claim, and a Decision-Grade model's output enters Phase 8's governance as `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`, exactly as any other model's does.
3. **It does not make a review satisfied.** Routing has no effect on review status, in either direction.
4. **It does not mean "the largest model".** Higher criticality raises **evidence, freshness, reliability and independence** requirements. Scale is not a governance property, no model is globally strongest, and a model that is stronger on reasoning and weaker on instruction fidelity is the wrong choice for a task that turns on following constraints exactly.

## 6. Status

`PROPOSED`. Adds no Phase 6 class, changes no review status, grants no authority, implements nothing.
