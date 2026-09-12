# Routing Constraint Model

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Two kinds of constraint, and the rule between them

| Kind | What it does | Failure to meet it |
|---|---|---|
| **Hard eligibility constraint** | **Filters** the candidate set | The candidate is **ineligible**. Not disfavoured — ineligible |
| **Soft preference** | **Ranks** candidates already eligible | The candidate ranks lower and stays eligible |

> **A soft preference may never override a hard constraint, and no accumulation of preferences ever makes an ineligible candidate eligible.**

Ranking happens **only inside the eligible set**. A model excluded by a hard constraint is not in the ranking at all, so no weighting, scoring or aggregation can reach it — which is the structural reason cost cannot buy its way past privacy.

## 2. Hard eligibility constraints

| Constraint | Satisfied when |
|---|---|
| `REQUIRED_CAPABILITY` | The profile claims the named capability at or above the required class, on evidence the policy accepts |
| `REQUIRED_MODALITY` | The profile supports the named input and output modalities |
| `REQUIRED_CONTEXT_CLASS` | The profile's context class meets the minimum |
| `REQUIRED_TOOL_USE` | The profile claims tool calling at the required class |
| `REQUIRED_STRUCTURED_OUTPUT` | The profile claims schema adherence at the required class |
| `REQUIRED_DEPLOYMENT_CLASS` | The deployment is of the required class |
| `REQUIRED_RESIDENCY_OR_JURISDICTION` | The deployment sits in the required jurisdiction |
| `MAX_DATA_SENSITIVITY_ALLOWED` | The **deployment's** approved maximum sensitivity is at or above the task's material sensitivity |
| `PROVIDER_ALLOWED` / `PROVIDER_PROHIBITED` | The provider is on the allow list / is not on the prohibit list |
| `MODEL_ALLOWED` / `MODEL_PROHIBITED` | As above, at profile level |
| `MODEL_FAMILY_ALLOWED` / `MODEL_FAMILY_PROHIBITED` | As above, at family level |
| `MINIMUM_REASONING_CLASS` | The reasoning claim meets the minimum |
| `MINIMUM_RELIABILITY_CLASS` | The reliability claim meets the minimum |
| `MINIMUM_CONTEXT_CAPACITY_CLASS` | The context class meets the minimum |
| `MODEL_DIVERSITY_REQUIRED` | The candidate differs from a named prior selection at the required level (`models/review-diversity-and-criticality.md`) |
| `PROVIDER_DIVERSITY_REQUIRED` | The candidate's provider differs from a named prior selection's — **only where justified, never a default** |
| `HUMAN_SELECTION_REQUIRED` | A human selected from the eligible set. **No automatic selection satisfies this**; it does not filter candidates, it requires an act |
| `NO_EXTERNAL_PROVIDER` | The deployment class is internal, private or local — where justified |
| `NO_TRAINING_ON_INPUT` | The deployment's declared retention and training posture forbids training on submitted content |
| `MAX_COST_CLASS` | The cost class is at or below the bound — **hard only where a task policy declares it so** (§4) |
| `MAX_LATENCY_CLASS` | As above |

### Four that are commonly misread

- **`MAX_DATA_SENSITIVITY_ALLOWED` is a property of the deployment, not of the model.** The same model family behind two deployments has two different answers, and that is the point: it is what lets a provider change without the architecture changing.
- **`NO_TRAINING_ON_INPUT` is a declared governance property, evidenced by contract or deployment policy.** It is never assumed from a provider's marketing, a default setting, or the absence of a statement. Unstated is **not satisfied**.
- **`HUMAN_SELECTION_REQUIRED` is not a filter.** Every candidate may pass it and the constraint still be unsatisfied, because what it requires is a human act. Where no human selects, routing **blocks**.
- **`PROVIDER_DIVERSITY_REQUIRED` is never a default.** It is the strongest diversity constraint and the easiest to impose reflexively; it applies only where a policy states the justification.

## 3. Soft preferences

| Preference | Ranks toward |
|---|---|
| `PREFER_HIGHER_CAPABILITY_EVIDENCE` | Stronger or fresher evidence on the capabilities the task requires |
| `PREFER_LOWER_COST_CLASS` | Cheaper |
| `PREFER_LOWER_LATENCY_CLASS` | Faster |
| `PREFER_HIGHER_RELIABILITY_CLASS` | More reliable on constrained output |
| `PREFER_LIFECYCLE_PREFERRED` | Profiles the registry marks `PREFERRED` |
| `PREFER_FRESHER_EVALUATION` | More recent capability evidence |
| `PREFER_FEWER_KNOWN_LIMITATIONS` | Fewer limitations bearing on this task |
| `PREFER_EXISTING_DEPLOYMENT` | A deployment already approved for this context |

**A preference states a direction, not a weight.** Weights would make the outcome depend on tuning rather than on policy, and would let a sufficiently large cost weighting outrank reliability inside the eligible set — which §4 of `models/routing-precedence-and-fallback.md` forbids by ordering preferences instead.

## 4. When cost or latency becomes hard

`MAX_COST_CLASS` and `MAX_LATENCY_CLASS` are **preferences by default**. They become hard constraints only where a **task policy declares a bound** — an interactive task that is useless above a latency class, a bulk task with a stated budget ceiling.

Even then:

1. **A hard cost or latency bound never displaces a governance, privacy, residency, capability, independence or criticality constraint.** It filters within what those allow.
2. **Where a cost or latency bound leaves no eligible candidate, routing blocks.** It does not relax the bound, and it does not relax anything else to fit inside it. A budget that cannot buy a compliant model has not discovered a cheaper compliant model; it has discovered that the work costs more than the budget.
3. **The cheapest eligible model is not automatically preferred, and the most expensive is not automatically best** (`models/master-model-routing-universe.md` §4).

## 5. Where constraints come from

| Source | Typical constraints |
|---|---|
| Task or Workflow stage | Required capabilities, modality, context class, tool use, structured output, latency |
| Data sensitivity (Phase 8) | `MAX_DATA_SENSITIVITY_ALLOWED`, `REQUIRED_DEPLOYMENT_CLASS`, `NO_TRAINING_ON_INPUT`, residency |
| Review Profile (Phase 6) | `MODEL_DIVERSITY_REQUIRED`, occasionally `PROVIDER_DIVERSITY_REQUIRED`, `HUMAN_SELECTION_REQUIRED` |
| Criticality band (Phase 3) | Minimum classes, evidence freshness, `HUMAN_SELECTION_REQUIRED` at the top band where policy says so |
| Organisational policy | Provider allow and prohibit lists, deployment classes, `NO_EXTERNAL_PROVIDER` |
| Legal or contractual obligation | Residency, retention posture, prohibited providers |

**Constraints are declared by the governance that owns the concern, and merged by the Routing Policy.** The Router does not invent a constraint, and it does not drop one it does not understand: **an unrecognised constraint blocks routing** rather than being ignored, because the alternative is a silent grant of everything the constraint was meant to prevent.

## 6. Conflicting constraints

Where two hard constraints cannot both be met, the result is **`NO_ELIGIBLE_MODEL`** and the conflict is reported. It is never resolved by:

- dropping the constraint that is harder to satisfy;
- preferring the one declared more recently, or by a more senior source;
- treating a prohibition as a preference;
- selecting the candidate that violates the fewest constraints.

**There is no partial eligibility.** A candidate meets every hard constraint or it is not a candidate, and "closest fit" is not a concept this model contains.

## 7. Status

`PROPOSED`. Implements no matcher, no engine, no scoring function and no runtime.
