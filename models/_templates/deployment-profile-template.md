# Deployment Profile Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Deployment Profile** is a conceptual target through which a model is reached. It is the object that carries **residency, the supported sensitivity label set and the effective data-handling posture** — which is why provider substitution is possible without touching the architecture above.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Deployment ID: `deployment.<stable_snake_case_name>`
- Profile version:
- Provider reference: `provider.<id>`
- Model Profiles reachable here: `model.<id>` list
- Deployment class: `PUBLIC_HOSTED` / `ENTERPRISE_TENANT` / `PRIVATE_CLOUD` / `LOCAL_INFERENCE` / `SOVEREIGN_REGION` / other declared class
- Primary lifecycle state: `CANDIDATE` / `EVALUATING` / `ELIGIBLE` / `DEPRECATED` / `SUSPENDED` / `RETIRED` — **exactly one**; `PREFERRED` and restrictions are annotations
- Status: PROPOSED

**No URL, hostname, credential, key, region code, infrastructure configuration or network detail appears in this template or in any profile using it.**

## Residency and Jurisdiction

Residency belongs **primarily here**, not to a Model Profile: the same model reached through two deployments is processed in two places.

| Field | Content |
|---|---|
| **Exact jurisdiction(s)** | The named legal orders under which processing occurs |
| **Region / residency class** | `SOVEREIGN` / `REGIONAL_BLOC` / `PRIVATE_TENANT` / `LOCAL_ONLY` / `GLOBAL_UNSPECIFIED` |
| **Class-to-jurisdiction mapping** | The explicit mapping, where a class is to satisfy a requirement stated over exact jurisdictions. **Without it, the two are not interchangeable** |
| **Cross-border processing** | `FORBIDDEN` / `CONDITIONAL` (state the conditions) / `ALLOWED` — assessed **separately** from the primary jurisdiction |
| **`UNKNOWN_RESIDENCY`** | Where not established. **Never satisfies a residency requirement**, and is never read as "probably fine" |
| **Evidence and review-by** | What establishes each of the above, and when it is re-checked |

The **task** declares its allowed and prohibited jurisdiction sets; **prohibited outranks allowed**, and a jurisdiction in both is prohibited and a defect to correct. **Provider-level regional claims constrain what this deployment may claim but never substitute for deployment-specific evidence.**

## Supported and Prohibited Sensitivity Classes

Phase 8 defines **no total order** over its sensitivity classes — an item may carry several, and `PERSONAL_DATA`, `PRIVILEGED` and `THIRD_PARTY_RESTRICTED` each carry obligations independent of every other. **There is no "maximum".** This section therefore declares **sets**, not a ceiling.

| Field | Content |
|---|---|
| **`SUPPORTED_SENSITIVITY_CLASSES`** | Each Phase 8 label this deployment is **explicitly approved** to handle, with **what approved it**. A label not listed is **unsupported** |
| **`PROHIBITED_SENSITIVITY_CLASSES`** | Labels this deployment must never handle, whatever else it supports. **Prohibition wins over support** |
| **Handling controls per supported label** | The obligations each label imposes here — retention limits, logging suppression, no-training, deletion rights, sub-processing limits — since supporting a label without meeting its obligations is not support |
| **Unassessed labels** | Named explicitly. **Unknown support is not support** |

Eligibility is a **subset test with obligations**: every applicable label explicitly supported, every obligation satisfied, no prohibition triggered. `PERSONAL_DATA + PRIVILEGED` requires **both** regimes; support for `TRADE_SECRET` implies nothing about `PERSONAL_DATA`.

**The same model behind two deployments has two different answers**, and that is the property that makes the registry substitutable.

## Effective Data-Handling Posture

The **authoritative** retention, training-on-input, logging and tenancy posture for this deployment — **evidenced by the governing instrument**, and **the posture routing reads** (`models/routing-constraint-model.md` §3.4).

This may be **more** restrictive than the provider-level default freely. It may be **less** restrictive **only where the provider-level instrument explicitly permits it and that permission is evidenced here**; an unevidenced relaxation is a defect, and the provider-level constraint governs.

**Unstated is not satisfied** — an absent statement never satisfies `REQUIRED_DATA_HANDLING_POSTURE`.

## Availability Expectation
The ordinary expectation. Current availability is a runtime observation, recorded on a Routing Decision, **never stored here as fact**.

## Deployment-Level Prohibited Contexts
Uses this deployment must not serve, whatever the model or provider allows.

## Freshness
Review-by and refresh triggers, including `DEPLOYMENT_CHANGE` and `PROVIDER_TERMS_CHANGE`.

## Non-Runtime Statement
This profile is declarative architecture. It specifies no address, credential, network path, infrastructure configuration or runtime.
