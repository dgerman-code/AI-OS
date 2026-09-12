# Deployment Profile Template

Status: PROPOSED — Phase 9 standard candidate
Template Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

A **Deployment Profile** is a conceptual target through which a model is reached. It is the object that carries **residency, maximum sensitivity and retention posture** — which is why provider substitution is possible without touching the architecture above.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Deployment ID: `deployment.<stable_snake_case_name>`
- Profile version:
- Provider reference: `provider.<id>`
- Model Profiles reachable here: `model.<id>` list
- Deployment class: `PUBLIC_HOSTED` / `ENTERPRISE_TENANT` / `PRIVATE_CLOUD` / `LOCAL_INFERENCE` / `SOVEREIGN_REGION` / other declared class
- Status: PROPOSED

**No URL, hostname, credential, key, region code, infrastructure configuration or network detail appears in this template or in any profile using it.**

## Residency and Jurisdiction
Where processing occurs and under which legal order. This is what `REQUIRED_RESIDENCY_OR_JURISDICTION` tests.

## Maximum Approved Data Sensitivity
The highest Phase 8 sensitivity class approved for this deployment — `PUBLIC` / `INTERNAL` / `CONFIDENTIAL` / `RESTRICTED` / `PERSONAL_DATA` / `PRIVILEGED` / `TRADE_SECRET` / `SECURITY_SENSITIVE` / `THIRD_PARTY_RESTRICTED` — with **what approved it**.

This is what `MAX_DATA_SENSITIVITY_ALLOWED` tests. **The same model behind two deployments has two different answers**, and that is the property that makes the registry substitutable.

## Retention and Training Posture
Whether submitted content is retained, for how long, and whether it may be used for training — **evidenced by the governing instrument**. This is what `NO_TRAINING_ON_INPUT` tests, and **unstated is not satisfied**.

## Availability Expectation
The ordinary expectation. Current availability is a runtime observation, recorded on a Routing Decision, **never stored here as fact**.

## Deployment-Level Prohibited Contexts
Uses this deployment must not serve, whatever the model or provider allows.

## Freshness
Review-by and refresh triggers, including `DEPLOYMENT_CHANGE` and `PROVIDER_TERMS_CHANGE`.

## Non-Runtime Statement
This profile is declarative architecture. It specifies no address, credential, network path, infrastructure configuration or runtime.
