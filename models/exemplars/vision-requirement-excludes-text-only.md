# Exemplar 5 — Vision requirement makes a text-only candidate ineligible

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that a modality requirement is a **hard constraint**, and that no strength elsewhere compensates for it.

## Task context
Extracting figures from scanned engineering drawings. Criticality **Enhanced Review Candidate**. Material sensitivity `CONFIDENTIAL`.

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
