# Provider Profile Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Provider Profile** describes the organisation operating one or more deployments. It is **separate from model identity**: one family may exist through several providers, and one provider may expose many models.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Provider ID: `provider.<stable_snake_case_name>`
- Display name and aliases, with periods
- Profile version:
- Provider type / class: e.g. commercial model provider / cloud platform reseller / internal operator / open-weights host
- Lifecycle status: `CANDIDATE` / `EVALUATING` / `ELIGIBLE` / `PREFERRED` / `RESTRICTED` / `DEPRECATED` / `SUSPENDED` / `RETIRED`
- Status: PROPOSED

## Contractual and Data-Handling Posture
References to the governing instrument, and what it establishes about retention, training on input, sub-processing, logging and incident notification. **References the instrument; does not restate it as fact.** Where no instrument exists, that is what this section records.

## Supported Deployment and Residency Classes
Which deployment classes and jurisdictions this provider offers. Each becomes a Deployment Profile in its own right.

## Availability and Commercial Constraints
Service commitments, capacity limits, regional restrictions, contractual minima — as governance properties, **not as prices or live metrics**.

## Provider-Level Prohibited Contexts
Uses no model through this provider may be routed to, whatever an individual Model Profile claims. **A provider-level prohibition overrides every model-level claim beneath it.**

## Concentration and Substitutability
What proportion of the eligible registry depends on this provider, and what remains eligible without it. **A diversity requirement satisfied only by this provider is a concentration, not a control.**

## Freshness
Review-by and refresh triggers, including `PROVIDER_TERMS_CHANGE` — which can invalidate a `NO_TRAINING_ON_INPUT` constraint without touching a single capability claim.

## Non-Runtime Statement
This profile is declarative architecture. It specifies no credential, endpoint, contract text, billing integration or runtime, and endorses no provider.
