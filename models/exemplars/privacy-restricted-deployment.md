# Exemplar 4 — Privacy-sensitive task restricted to an approved deployment class

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that sensitivity eligibility is a **multi-label subset test** on the **deployment**, not a comparison against a ceiling — and that this is the mechanism making providers substitutable.

## Task context
Structured extraction from HR case files held under a works-council agreement. Criticality **Enhanced Review Candidate**.

**Material sensitivity labels: `PERSONAL_DATA` + `CONFIDENTIAL` + `THIRD_PARTY_RESTRICTED`.** Three labels, three independent obligation sets. Phase 8 orders none of them.

## Candidate universe
Registry state `reg.snapshot.2026-09-11T00:00Z#4471`; universe definition `cud.restricted_processing` v1. Enumerated: 4. **`CANDIDATE_UNIVERSE_COMPLETE`.**

## Requirements
`capability.structured_extraction` `STRONG`; `capability.document_analysis` `BASELINE`; `REQUIRED_DEPLOYMENT_CLASS` ∈ {`PRIVATE_CLOUD`, `LOCAL_INFERENCE`, `SOVEREIGN_REGION`}; `REQUIRED_JURISDICTION` with an allowed set of two named jurisdictions and cross-border `FORBIDDEN`; **`SUPPORTED_SENSITIVITY_CLASSES` ⊇ {`PERSONAL_DATA`, `CONFIDENTIAL`, `THIRD_PARTY_RESTRICTED`}**; `REQUIRED_HANDLING_CONTROLS` per label; `REQUIRED_DATA_HANDLING_POSTURE` = no training on input, logging suppressed.

**Exceptionability:** every one of these is `ABSOLUTELY_NON_WAIVABLE`. The labels arrive from statute, from a works-council agreement and from `THIRD_PARTY_RESTRICTED` — which Phase 8 says cannot be relaxed by an internal decision at all. **No Phase 7 Right adjusts any of them.**

## Candidate assessment — the same model, three deployments
| Candidate | Eligible? | Why |
|---|---|---|
| `model.extractor_e` @ `deployment.public_hosted_e` | **No** | Supports {`PUBLIC`, `INTERNAL`} — none of the three required labels |
| `model.extractor_e` @ `deployment.sovereign_region_e` | **Yes** | Supports all three, **each explicitly approved**; handling controls met per label; in the allowed jurisdiction set with cross-border `FORBIDDEN`; effective posture forbids training and suppresses logging |
| `model.extractor_e` @ `deployment.public_hosted_e2` | **No** | Provider's marketing states no training; **the governing instrument says nothing**. Unstated is **not satisfied** |
| `model.extractor_e` @ `deployment.private_cloud_e3` | **No** | Supports {`CONFIDENTIAL`, `TRADE_SECRET`, `PERSONAL_DATA`} — **`THIRD_PARTY_RESTRICTED` is unassessed**. Unknown support is not support |
| `model.frontier_reasoning_b` @ `deployment.tenant_internal_a` | **No** | Supports {`INTERNAL`, `CONFIDENTIAL`}; `PERSONAL_DATA` **prohibited** by its own profile |

## Selection
`model.extractor_e` @ `deployment.sovereign_region_e`.

## What this actually shows
**One model, four answers.** The capability claims are identical across every `model.extractor_e` row; what differs is which labels each deployment is approved for, its jurisdiction, and what its governing instrument actually says. Sensitivity eligibility never touched the model at all.

Two rows carry the lesson the old version of this exemplar got wrong:

- **The fourth row** would have passed a ceiling test. A deployment supporting `PERSONAL_DATA` looks like the strictest of the three it supports, and under a "maximum sensitivity" model it would have been eligible — while being **unassessed for `THIRD_PARTY_RESTRICTED`**, whose obligations come from someone else's terms entirely. **Support for one label implies support for no other**, and no label outranks another by being "higher", because there is no higher.
- **The third row** shows a provider's public assurance is **not** an evidenced governance property. The posture routing reads is the **effective deployment posture** evidenced by the instrument, and a confident absence of a statement is still an absence.

**Routing moved nothing.** The case files stayed in their scope, at their classification, with their canonicality unchanged. Selecting a deployment is not a scope transfer (`knowledge/scope-isolation-and-transfer.md` §4).
