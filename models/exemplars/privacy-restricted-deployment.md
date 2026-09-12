# Exemplar 4 — Privacy-sensitive task restricted to an approved deployment class

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that sensitivity eligibility is a property of the **deployment**, not the model — which is the mechanism that makes providers substitutable.

## Task context
Structured extraction from HR case files. Criticality **Enhanced Review Candidate**. Material sensitivity **`PERSONAL_DATA`**, with a residency requirement and `NO_TRAINING_ON_INPUT` required by the governing instrument.

## Requirements
`capability.structured_extraction` `STRONG`; `capability.document_analysis` `BASELINE`; `REQUIRED_DEPLOYMENT_CLASS` ∈ {`PRIVATE_CLOUD`, `LOCAL_INFERENCE`, `SOVEREIGN_REGION`}; `REQUIRED_RESIDENCY_OR_JURISDICTION`; `MAX_DATA_SENSITIVITY_ALLOWED` ≥ `PERSONAL_DATA`; `NO_TRAINING_ON_INPUT`.

## Candidate assessment — the same model, three deployments
| Candidate | Eligible? | Why |
|---|---|---|
| `model.extractor_e` @ `deployment.public_hosted_e` | **No** | Deployment maximum sensitivity `INTERNAL`; retention posture permits training on input |
| `model.extractor_e` @ `deployment.sovereign_region_e` | **Yes** | Maximum `PERSONAL_DATA`; in-jurisdiction; instrument forbids training on input |
| `model.extractor_e` @ `deployment.public_hosted_e2` | **No** | Provider's marketing states no training; **the instrument says nothing**. Unstated is **not satisfied** |
| `model.frontier_reasoning_b` @ `deployment.tenant_internal_a` | **No** | Deployment maximum `CONFIDENTIAL`, below `PERSONAL_DATA` |

## Selection
`model.extractor_e` @ `deployment.sovereign_region_e`.

## What this actually shows
**One model, three answers.** The capability claims are identical across all three rows; what differs is the deployment's approved maximum sensitivity, its jurisdiction, and what its governing instrument actually says. Sensitivity eligibility never touched the model at all.

The third row is the one worth dwelling on: a provider's public assurance is **not** an evidenced governance property. `NO_TRAINING_ON_INPUT` is satisfied by an instrument or it is unsatisfied, and a confident absence of a statement is still an absence.

**Routing moved nothing.** The case files stayed in their scope, at their classification, with their canonicality unchanged. Selecting a deployment is not a scope transfer (`knowledge/scope-isolation-and-transfer.md` §4).
