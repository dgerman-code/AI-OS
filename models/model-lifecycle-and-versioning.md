# Model Lifecycle, Versioning and Provider Independence

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 0. The identity stack

The audit found the first draft did not sufficiently distinguish underlying model version, provider-hosted variant, provider alias, registry profile version and the provider/deployment relationship. **Runtime must never have to guess whether a provider-specific variant is the same underlying model, a different release, or merely a renamed catalogue entry.** Six layers, no overlap:

| # | Layer | Is | Identified by |
|---:|---|---|---|
| 1 | **Model Family** | A lineage, used for grouping and diversity constraints | `family.<stable_name>` |
| 2 | **Underlying Model Release** | The thing whose behaviour is being profiled — the release identity as the originator versions it | The originator's release identity, recorded, **never used as the registry ID** |
| 3 | **Model Profile** | The AI-OS governed record describing **one underlying model release** | `model.<stable_snake_case_name>` |
| 4 | **Registry Profile Version** | The version of the **AI-OS record**, not of the model | `v<n>` on the profile |
| 5 | **Provider Offering Mapping** | A provider's exposure of that release — its catalogue name, aliases and any provider-specific behaviour | A bounded mapping **inside the Provider Profile**, not a separate registry object |
| 6 | **Deployment Profile** | The concrete target: class, tenant, region, residency, supported handling labels, effective posture | `deployment.<stable_snake_case_name>` |

### Why Provider Offering is a mapping, not a seventh object

It has no independent lifecycle, no capability claims of its own, and no governance properties that are not already the Provider's or the Deployment's. It is the answer to *what does this provider call this release, and does anything about their exposure of it differ* — a bounded mapping, with an unambiguous outcome, held where the provider's other facts are held.

### Identity rules

1. **Registry profile version is not the underlying model version.** The record may be revised — new evidence, a new limitation, a corrected claim — while the model is unchanged; and the model may change while the record has not yet caught up, which is precisely what a refresh trigger is for.
2. **One Model Profile may map to several provider/deployment combinations** where they genuinely expose **the same underlying release**, evidenced.
3. **Where provider-specific behaviour is materially different and cannot be evidenced as the same release**, it is **a distinct Model Profile** — or an explicitly named provider-specific variant profile with its own ID. It is never left as an ambiguous mapping under a shared profile.
4. **A provider marketing alias never defines Model Profile identity.** Aliases are metadata; identity is the stable internal ID; no constraint is ever expressed against an alias.
5. **Model Profile carries no provider-specific governance property.** Retention, training, logging, residency and approved handling labels belong to Provider and Deployment (`models/routing-constraint-model.md` §3.4). A generic retention promise on a Model Profile is a defect.
6. **A historical Routing Decision preserves both the exact Model Profile version and the provider/deployment mapping used.** Either alone under-determines what ran.
7. **A silent provider backend change triggers review.** Where the exposure changes without a release change the consumer can see, `PROVIDER_VERSION_CHANGE` fires; depending on materiality the outcome is a new mapping version, a new profile version, or — where the same release can no longer be evidenced — a distinct profile.

## 1. Lifecycle states

Registry-level status of a Model Profile. **Not task eligibility.**

**Exactly one primary lifecycle state at a time.** The states are mutually exclusive, and two never coexist — the audit was right that this was not said, and that a runtime would otherwise have to invent whether `PREFERRED` and `RESTRICTED` can be held together.

| State | Meaning | Routable to new work? |
|---|---|---|
| `CANDIDATE` | Known to the registry; not assessed | **No** |
| `EVALUATING` | Under assessment | Only where a policy explicitly permits evaluation traffic |
| `ELIGIBLE` | Assessed and admitted to the registry | **Yes, where the policy's constraints are also met** |
| `DEPRECATED` | Wound down, planned and one-way | **No.** Historical decisions stand |
| `SUSPENDED` | Excluded immediately pending investigation; temporary, with an owner | **No.** Historical decisions stand |
| `RETIRED` | Permanently excluded | **No.** Historical decisions stand |

Six states, down from eight. `PREFERRED` and `RESTRICTED` were removed **as lifecycle states** because neither is one:

| Was a state | Is now | Why |
|---|---|---|
| `PREFERRED` | A **routing preference designation** — an annotation read by `PREFER_LIFECYCLE_PREFERRED` at stage 6 | Preference is a ranking property, not an admission property. As a lifecycle state it collided with `ELIGIBLE`, which every preferred profile also is |
| `RESTRICTED` | A **restriction annotation** — zero or more bounded exclusions, each naming the contexts it excludes and why | A restriction is contextual by nature. As a lifecycle state it forced one global answer to a question whose answer is per-context |

**Annotations are orthogonal to the state and to each other.** A profile is `ELIGIBLE`, may carry the `PREFERRED` designation, and may carry any number of restriction annotations — with no ambiguity, because only one of the three is a state.

### Transitions

| From | To | On |
|---|---|---|
| `CANDIDATE` | `EVALUATING` | Assessment begins |
| `EVALUATING` | `ELIGIBLE` | Assessment admits it |
| `EVALUATING` | `RETIRED` | Assessment rejects it |
| `ELIGIBLE` | `SUSPENDED` | An incident or concern, urgently |
| `ELIGIBLE` | `DEPRECATED` | A planned wind-down |
| `SUSPENDED` | `ELIGIBLE` | Investigation clears it — possibly with new restriction annotations |
| `SUSPENDED` | `DEPRECATED` / `RETIRED` | Investigation does not clear it |
| `DEPRECATED` | `RETIRED` | The wind-down completes |

**`RETIRED` is terminal.** Restoring a retired profile is a **new profile** with its own evidence, not a state change — the evidence that retired it does not un-apply.

**No transition touches history.** Every state change affects new routing only; existing Routing Decisions name the profile and version they used, permanently.

## 2. Lifecycle status is not task eligibility

> **Registry status is a gate, not a grant.** `ELIGIBLE` means "admitted to the registry", never "usable for this task".

A profile is routable to a specific task only when its **primary state permits new routing**, **no restriction annotation excludes this context**, and **every eligibility constraint of the task is met**. Three consequences stated plainly:

1. **A globally `ELIGIBLE` model can be prohibited for a particular task** — by sensitivity, residency, capability, diversity or an explicit prohibition. This is the ordinary case, not an exception.
2. **The `PREFERRED` designation is not mandatory.** It ranks within the eligible set; where policy disqualifies the profile, it is not in the set to be ranked, and preferring it anyway would be a preference overriding an eligibility constraint.
3. **A restriction annotation is not a weaker eligibility.** Inside the contexts it excludes, the profile is **ineligible** — not disfavoured — and outside them the annotation says nothing.

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
| **Registry Profile Version** | **The AI-OS record changes** — a new claim, new evidence, a new limitation, a corrected field, a new mapping. **The underlying release is the same one** |
| **Provider / Deployment Profile version** | Terms, posture, residency, availability commitments or deployment class change |
| **Routing Policy version** | The rules change — constraints, preferences, accepted evidence classes, tie-break |

**A Routing Decision names all three, by version, plus the provider offering mapping used.** Naming a profile without its version reproduces nothing.

### A changed underlying release is a different Model Profile, not a new version of this one

§0 rule 2 says a Model Profile describes **one underlying model release**. That rule is exact, and the versioning rule follows from it rather than qualifying it:

> **A registry profile version never absorbs a change of the underlying release.** Bumping the version records that *the record* changed. It cannot record that *the thing* changed, because the profile's identity is the release it describes.

| What changed | Consequence |
|---|---|
| A claim, a piece of evidence, a limitation, a field, a mapping | **New Registry Profile Version.** Same profile, same release |
| **The underlying release**, by any route — a new provider version, a silent backend change, any exposure that can no longer be evidenced as the same release | **A different Model Profile**, with its own stable ID, linked to its predecessor. **Never a version bump on the existing one** |
| Uncertainty about which of the two happened | **Treated as a changed release** until evidence establishes otherwise, and the existing profile is `SUSPENDED` pending that evidence |

The last row is the operative one. Provider version changes are often opaque from outside, and the safe reading is the one that does not quietly leave historical Routing Decisions pointing at a profile whose subject has moved underneath them. A version bump in that situation would make every prior decision naming `model.x v3` ambiguous about what actually ran — which is the precise failure versioning exists to prevent.

**`PROVIDER_VERSION_CHANGE` therefore fires an identity review, not a version bump.** The review's outcome is one of the three rows above; it is never assumed to be the first.

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
| Incorrect capability assumption | Claim corrected; evidence refreshed; a **restriction annotation** if load-bearing |
| Provider incident | Availability change; `SUSPENDED` if recurring or unexplained |
| Data-handling concern | `SUSPENDED`, or a restriction annotation; **deployment** posture reassessed and re-evidenced |
| Safety concern | A **restriction annotation** for bounded contexts, or `SUSPENDED` |
| Severe quality regression | Evidence refresh trigger; a restriction annotation or `SUSPENDED` pending re-evaluation |
| Outage | Availability class change — **not a lifecycle change**, unless it recurs |
| Provider-specific behavioural divergence | Mapping review; a new mapping version, a new profile version, or a **distinct profile** where the same release can no longer be evidenced (§0 rule 7) |
| Policy violation | `SUSPENDED`, then a governed determination |

**An incident is negative evidence and is recorded as such** (`models/evaluation-evidence-model.md` §2), not averaged away against positive claims — and its effect is bounded by its **applicability** (§2a there), so an incident in one context does not silently disqualify unrelated ones. **A route prohibition may be bounded** — a model restricted from personal data remains eligible for everything else.

**Historical Routing Decisions are preserved through every one of these.** No incident rewrites what was selected before it was known.

## 7. Status

`PROPOSED`. Names no provider, builds no incident system, implements nothing.
