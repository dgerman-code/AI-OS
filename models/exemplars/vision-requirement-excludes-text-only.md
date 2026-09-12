# Exemplar 5 — Vision requirement makes a text-only candidate ineligible

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that a modality requirement is an **eligibility constraint** — `ABSOLUTELY_NON_WAIVABLE`, because no decision makes a text-only model read an image — and that no strength elsewhere compensates for it.

## Task context
Extracting figures from scanned engineering drawings. Criticality **Enhanced Review Candidate**. Material sensitivity `CONFIDENTIAL`.

## Candidate universe

Bound before any filtering or ranking, per `models/routing-precedence-and-fallback.md` §1.

| Element | Value |
|---|---|
| **Registry state reference** | `reg.snapshot.2026-09-11T12:00Z#4485` |
| **Universe definition version** | `cud.document_extraction` v1 |
| **Inclusion rule** | Every `ROUTABLE` Model Profile paired with the deployment classes approved for `CONFIDENTIAL` material. **Modality is not an enumeration filter**: text-only profiles are enumerated and excluded at stage 3, so the record shows what the modality requirement removed. **Availability pre-enumeration: no** |
| **Routing scope** | Routable profiles × `CONFIDENTIAL`-approved deployment classes × the internal provider allowlist |
| **Pre-filter exclusions** | Deployment classes not approved for `CONFIDENTIAL` material, by the inclusion rule |
| **Enumerated candidate set** | **3**: `model.frontier_reasoning_b` v6; `model.vision_specialist_c` @ `deployment.tenant_internal_c`; `model.midsize_analyst_d` |
| **Omission reasons** | `NONE` — every registered candidate inside the scope is enumerated |
| **Completeness result** | **`CANDIDATE_UNIVERSE_COMPLETE`** |
| **Behaviour if incomplete** | Policy `rp.document_extraction` v1 declares **`BLOCK`** on `CANDIDATE_UNIVERSE_INCOMPLETE` |

## Requirements
`REQUIRED_MODALITY` image input; `capability.vision` `STRONG`; `capability.document_analysis` `STRONG`; `capability.structured_extraction` `BASELINE`.

## Candidate assessment
| Candidate | Eligible? | Why |
|---|---|---|
| `model.frontier_reasoning_b` v6 | **No** | Text-only. `SPECIALISED` on advanced reasoning, `SPECIALISED` on structured extraction, `NOT_CLAIMED` on vision — **and the modality is absent, so the rest is unreachable** |
| `model.vision_specialist_c` @ `deployment.tenant_internal_c` | **Yes** | Image input; `SPECIALISED` vision; `STRONG` document analysis on internal evaluation |
| `model.midsize_analyst_d` | **No** | Text-only |

## Selection
`model.vision_specialist_c` @ `deployment.tenant_internal_c`.

## What this actually shows
The excluded candidate is the strongest general model in the registry, and it is **ineligible** — not disfavoured, not ranked last. There is no ranking it appears in, because stage 3 removed it.

Two distinctions this makes concrete:

- **`NOT_CLAIMED` is not a low score.** Nobody has asserted the text-only model fails at vision; it has no vision input at all, and the modality constraint settles the matter before any claim is consulted.
- **No aggregate compensates.** A composite score would have ranked the frontier model first on the strength of two `SPECIALISED` claims, and a composite is exactly what `models/evaluation-evidence-model.md` §3 refuses to define.

The task is not "analysis"; it is "analysis of images". A requirement stated in the capability vocabulary catches that. A requirement stated as "use a strong model" does not.
