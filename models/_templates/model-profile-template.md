# Model Profile Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Model Profile** describes one execution capability, at one version, with claims, evidence and limitations. It is a **semantic record model**, not a vendor API schema: no request format, parameter set, credential, endpoint address or SDK is specified or implied.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Model Profile ID: `model.<stable_snake_case_name>` — no marketing name, version number, price, date or region in the ID
- Display name: the human-facing name
- Aliases: provider display names and API identifiers, each with the period it applied. **Metadata only — no constraint is ever expressed against an alias**
- Profile version:
- Provider reference: `provider.<id>`
- Model family: the lineage this belongs to, used by family-diversity constraints
- Provider version / release identifier: as the provider states it
- Lifecycle status: `CANDIDATE` / `EVALUATING` / `ELIGIBLE` / `PREFERRED` / `RESTRICTED` / `DEPRECATED` / `SUSPENDED` / `RETIRED`
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
Declared behavioural constraints, and any compliance property claimed for the model itself as distinct from its deployment.

## Data Handling Posture
Retention, training-on-input and logging posture **as declared, with the source of the declaration**. Where it varies by deployment, the deployment governs and this section says so. **Unstated is not satisfied** — an absent statement never satisfies `NO_TRAINING_ON_INPUT`.

## Deployment Class Applicability
Which deployment classes this profile is available through: hosted provider / private hosted / local / sovereign / other declared class.

## Region and Residency Applicability
Where relevant. Residency is a **deployment** property; this section records which deployments carry which.

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
