# Model Profile Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Model Profile** describes one execution capability, at one version, with claims, evidence and limitations. It is a **semantic record model**, not a vendor API schema: no request format, parameter set, credential, endpoint address or SDK is specified or implied.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity — the stack, layers 1 to 4

Per `models/model-lifecycle-and-versioning.md` §0. The four layers a Model Profile carries; layers 5 and 6 are the Provider's and the Deployment's.

- **Model Family:** `family.<stable_name>` — the lineage, used by diversity constraints
- **Underlying Model Release:** the originator's release identity for the thing being profiled. **Recorded, never used as the registry ID**
- **Model Profile ID:** `model.<stable_snake_case_name>` — no marketing name, version number, price, date or region
- **Registry Profile Version:** `v<n>` — the version of **this AI-OS record**, which is **not** the underlying model version and moves independently of it
- Display name: the human-facing name
- Aliases: provider display names and API identifiers, each with the period it applied. **Metadata only — no constraint is ever expressed against an alias, and an alias never defines identity**
- **Provider offering mappings:** the `provider.<id>` / `deployment.<id>` combinations that expose **this same underlying release**, each with the evidence that it is the same release. Where a provider's exposure is materially different and cannot be evidenced as the same release, **it belongs to a distinct Model Profile, not to this list**
- Primary lifecycle state: `CANDIDATE` / `EVALUATING` / `ELIGIBLE` / `DEPRECATED` / `SUSPENDED` / `RETIRED` — **exactly one**
- Routing designation: `PREFERRED`, or none — an annotation, not a state
- Restriction annotations: zero or more, each naming the contexts it excludes and why — annotations, not states
- Status: PROPOSED

## Capability Claims

| `capability.<id>` | Class | Evidence class(es) | Confidence | As-of | Review-by |
|---|---|---|---|---|---|

Classes are `NOT_CLAIMED` / `BASELINE` / `STRONG` / `SPECIALISED`. **`NOT_CLAIMED` is an absence of assertion, not a finding of incapacity.** A claim is a claim: it carries evidence, and evidence never makes it true.

## Modalities
Input and output modalities supported. A modality not listed is not supported for routing purposes.

## Context Characteristics
Context capacity **class**, and any difference between what is accepted and what is used well — the distinction `capability.long_context_analysis` exists to capture.

## Tool Use / Structured Output
Claims for `capability.tool_calling`, `capability.structured_tool_use` and `capability.structured_generation`, with the class and its evidence. State whether conformance holds under unusual input or only typical input.

## Safety and Compliance Constraints
Declared **behavioural** constraints intrinsic to the model. **Not contractual or data-handling properties** — those belong to Provider and Deployment.

## Data Handling — not recorded here

**None. By rule.** Retention, training-on-input, logging, residency and approved sensitivity labels are **Provider and Deployment governance properties**, and routing reads the **effective deployment posture** (`models/routing-constraint-model.md` §3.4).

A generic retention or no-training promise on a Model Profile is a **defect**, not a convenience: it creates a second source of truth for a question the deployment already answers, and the two will diverge.

Intrinsic *technical* characteristics that happen to bear on privacy — a model that cannot retain state across calls, say — are recorded above as behavioural constraints, with evidence, and they are never a substitute for deployment posture.

## Deployment Class Applicability
Which deployment classes this release is available through. This states **availability**, not approval: whether a given deployment may handle given material is the Deployment Profile's answer.

## Semantic Bands
- Cost class: `COST_LOW` / `COST_MEDIUM` / `COST_HIGH` / `COST_PREMIUM`
- Latency class: `LATENCY_INTERACTIVE` / `LATENCY_STANDARD` / `LATENCY_SLOW` / `LATENCY_BATCH`
- Availability class expectation: the ordinary expectation, **not a live reading**

**No prices, rates, token costs or measured latencies.** Bands only.

## Evaluation Evidence References
Per dimension, referencing `models/evaluation-evidence-model.md` §3. **No composite score.**

## Known Limitations
Observed or declared weaknesses, failure modes, and the conditions under which claims do not hold. A limitation **narrows** a claim.

## Prohibited Contexts
Bounded uses this profile must not be routed to, whatever its claims say. A prohibition **overrides** a claim.

## Freshness
As-of date; last verified; expected refresh interval; review-by; refresh triggers fired. **Use-context verdicts are assessed at routing time and never stored here** (Phase 8 §3).

## Supersedes / Superseded By
With the reason. **Supersession removes nothing**: historical Routing Decisions naming this version stay valid.

## Non-Runtime Statement
This profile is declarative architecture. It specifies no SDK, API, credential, endpoint, parameter, billing integration or runtime, and confers no authority on any model, provider or process.
