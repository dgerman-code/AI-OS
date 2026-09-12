# Model Lifecycle, Versioning and Provider Independence

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Lifecycle states

Registry-level status of a Model Profile. **Not task eligibility.**

| State | Meaning |
|---|---|
| `CANDIDATE` | Known to the registry; not assessed. Routable to nothing |
| `EVALUATING` | Under assessment. Routable only where a policy explicitly permits evaluation traffic |
| `ELIGIBLE` | Assessed and admitted to the registry. **May be routed to where a policy's constraints are also met** |
| `PREFERRED` | Eligible, and ranked first by `PREFER_LIFECYCLE_PREFERRED` where nothing else decides |
| `RESTRICTED` | Eligible only for bounded contexts the restriction names |
| `DEPRECATED` | Excluded from **new** routing; historical decisions stand |
| `SUSPENDED` | Excluded from new routing **immediately**, pending investigation. A temporary state with an owner |
| `RETIRED` | Permanently excluded from new routing; historical decisions stand |

## 2. Lifecycle status is not task eligibility

> **Registry status is a gate, not a grant.** `ELIGIBLE` means "admitted to the registry", never "usable for this task".

A profile is routable to a specific task only when it is `ELIGIBLE` or `PREFERRED` (or `RESTRICTED` within its restriction) **and** every hard constraint of the task is met. Three consequences stated plainly:

1. **A globally `ELIGIBLE` model can be prohibited for a particular task** — by sensitivity, residency, capability, diversity or an explicit prohibition. This is the ordinary case, not an exception.
2. **A `PREFERRED` model is not mandatory.** Preference ranks the eligible set; where policy disqualifies it, it is not in the set to be ranked, and preferring it anyway would be a soft value overriding a hard constraint.
3. **A `RESTRICTED` model is not a lesser `ELIGIBLE` one.** Outside its named contexts it is ineligible, not disfavoured.

## 3. Deprecation and history

**Deprecation excludes a profile from new routing. It removes nothing.**

| Concern | Rule |
|---|---|
| Existing Routing Decisions | **Preserved intact**, naming the profile and version actually used |
| The Model Profile record | Retained at its final version, with the lifecycle change and its reason |
| Work already produced | Unaffected. It was produced under the profile that was then eligible |
| Re-running the work | A **new** Routing Decision under current policy, which will select something else |

A Routing Decision naming a now-retired profile is **correct history, not a stale record.** Deleting or rewriting it would destroy the only account of what actually performed the work — and the question "what produced this?" is asked precisely when something has gone wrong, which is after the model has usually been retired.

`SUSPENDED` differs from `DEPRECATED` in intent and reversibility: suspension is an **urgent, temporary** exclusion pending investigation, and it may end in restoration, restriction or retirement. Deprecation is a planned, one-way wind-down.

## 4. Versioning

Three versioned things, and confusing them is how reproducibility is lost:

| Versioned object | Changes when |
|---|---|
| **Model Profile version** | The registry's description of the model changes — new claims, new evidence, new limitations, a provider version change |
| **Provider / Deployment Profile version** | Terms, posture, residency, availability commitments or deployment class change |
| **Routing Policy version** | The rules change — constraints, preferences, accepted evidence classes, tie-break |

**A Routing Decision names all three, by version.** Naming a profile without its version reproduces nothing, because the thing behind the name has moved.

**A provider version change is a profile version change**, even where nothing else moves — the underlying thing is different and every claim about it is now evidence about the previous one until re-verified.

## 5. Provider independence and anti-lock-in

Phase 9's central practical purpose: **the vendor must be replaceable without rewriting Role, Skill, Workflow, Handoff, Review, Decision or Knowledge architecture.**

### Stable internal identifiers

```
model.<stable_snake_case_name>
provider.<stable_snake_case_name>
deployment.<stable_snake_case_name>
routing_policy.<stable_snake_case_name>
capability.<stable_snake_case_name>
```

An ID must not contain a marketing name, a version number, a price, a date, a region code or an infrastructure detail. These change; the identity must not. A profile *about* a specific provider product may carry the provider reference in its ID where that is the deliberate intent — `model.vendor_x_reasoning_v2` — but that is a **provider-specific profile**, knowingly created, not the default shape.

### Aliases

A Model Profile carries **aliases**: the provider's display names and API identifiers as they have been over time, each with the period it applied.

**A rename is an alias addition, never an identity change.** When a provider renames a product, the stable ID does not move, historical Routing Decisions stay valid, and nothing upstream is rewritten. The alias list is how a human finds the record from the name they know, and it is metadata — **no routing constraint is ever expressed against an alias**, because an alias can be reassigned by someone outside the organisation.

### What upper architecture may name

| Layer | May reference | Must not reference |
|---|---|---|
| Role Card | Capability requirements, or a `routing_policy.<id>` | A model, provider, or vendor name |
| Workflow stage | Capability, modality, context and tooling requirements | A model or provider |
| Review Profile | A diversity policy value | A model or provider |
| Routing Policy | Capabilities, classes, providers, deployments, model families | — |
| Routing Decision | Exact profiles and versions used | — |

**No Role says "this Role is model X".** A Role is a professional profile; a model is a replaceable execution capability; the Role Registry states this already (`architecture/registry-separation.md` §2), and Phase 9 is what makes it hold in practice rather than in aspiration.

### Model pinning is exceptional and governed

Pinning a specific profile for a task is permitted only with a **recorded justification, a named owner, and an expiry or review-by**. An unexpiring pin is lock-in acquired one task at a time, and the expiry is what forces the question to be asked again.

## 6. Incidents and restriction

| Trigger | Typical consequence |
|---|---|
| Incorrect capability assumption | Claim corrected; evidence refreshed; `RESTRICTED` if load-bearing |
| Provider incident | Availability change; `SUSPENDED` if recurring or unexplained |
| Data-handling concern | `SUSPENDED` or `RESTRICTED`; deployment eligibility reassessed; `NO_TRAINING_ON_INPUT` re-verified |
| Safety concern | `RESTRICTED` for bounded contexts, or `SUSPENDED` |
| Severe quality regression | Evidence refresh trigger; `RESTRICTED` or `SUSPENDED` pending re-evaluation |
| Outage | Availability class change — **not a lifecycle change**, unless it recurs |
| Policy violation | `SUSPENDED`, then a governed determination |

**An incident is negative evidence and is recorded as such** (`models/evaluation-evidence-model.md` §2), not averaged away against positive claims. **A route prohibition may be bounded** — a model restricted from personal data remains eligible for everything else.

**Historical Routing Decisions are preserved through every one of these.** No incident rewrites what was selected before it was known.

## 7. Status

`PROPOSED`. Names no provider, builds no incident system, implements nothing.
