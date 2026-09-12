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
- Primary lifecycle state: `CANDIDATE` / `EVALUATING` / `ELIGIBLE` / `DEPRECATED` / `SUSPENDED` / `RETIRED` — **exactly one**; `PREFERRED` and restrictions are annotations
- Status: PROPOSED

## Provider Offering Mappings

Layer 5 of the identity stack. For each `model.<id>` this provider exposes:

| `model.<id>` | Provider catalogue name and aliases | Underlying release exposed | Evidence it is the same release | Materially different behaviour? |
|---|---|---|---|---|

**A mapping is bounded, not a registry object**: it has no lifecycle, no capability claims and no governance properties of its own. Where the answer to the last column is yes and cannot be evidenced away, the exposure is **a distinct Model Profile**, not a mapping — a runtime must never have to guess whether a provider variant is the same release, a different release, or a renamed catalogue entry.

**A silent backend change** — the exposure changes without a release change the consumer can see — fires `PROVIDER_VERSION_CHANGE` and forces this mapping to be reviewed.

## Contractual and Data-Handling Posture — provider level
References to the governing instrument, and what it establishes about retention, training on input, sub-processing, logging and incident notification. **References the instrument; does not restate it as fact.** Where no instrument exists, that is what this section records.

**This is the provider-level default and constraint**, not the effective posture. A deployment beneath it may be **more** restrictive freely; it may be **less** restrictive only where this instrument explicitly permits it and the deployment evidences it. Routing reads the deployment's effective posture (`models/routing-constraint-model.md` §3.4), and where the two disagree without evidenced permission, **the provider-level constraint governs and the deployment record is defective**.

## Supported Deployment and Residency Classes
Which deployment classes and jurisdictions this provider offers. Each becomes a Deployment Profile in its own right.

## Availability and Commercial Constraints
Service commitments, capacity limits, regional restrictions, contractual minima — as governance properties, **not as prices or live metrics**.

## Provider-Level Prohibited Contexts
Uses no model through this provider may be routed to, whatever an individual Model Profile claims. **A provider-level prohibition overrides every model-level claim beneath it.**

## Concentration and Substitutability
What proportion of the eligible registry depends on this provider, and what remains eligible without it. **A diversity requirement satisfied only by this provider is a concentration, not a control.**

## Freshness
Review-by and refresh triggers, including `PROVIDER_TERMS_CHANGE` — which can invalidate a `REQUIRED_DATA_HANDLING_POSTURE` constraint without touching a single capability claim.

## Non-Runtime Statement
This profile is declarative architecture. It specifies no credential, endpoint, contract text, billing integration or runtime, and endorses no provider.
