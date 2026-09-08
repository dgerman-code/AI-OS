# External Publication

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: External Publication
- Decision ID: `decision.external_publication`
- Version: 0.1
- Status: PROPOSED
- Decision Family: Publication / Disclosure / Canonical Promotion
- Decision Class: `COMMITMENT_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

## Decision Subject

Release of **one** content item, at a stated version, to an audience outside the entity, under the entity's name.

## Decision Effect

Makes the content externally available and attributes it to the entity. Publication is **practically irreversible**: retraction removes availability, not the fact of having published.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE` | Publication step completes | n/a | **Content published under the entity's name** | Unchanged | None | Retained against the published version | Version-bound |
| `APPROVE_WITH_CONDITIONS` | Completes on conditions being met **before** release | n/a | Publication only once conditions are met | Unchanged | None | Conditions open, owned, and **pre-release** | **Mandatory** |
| `REJECT` | Blocked | n/a | None | Unchanged | None | Retained | n/a |
| `DEFER` | Not permitted | n/a | None | Unchanged | None | Retained | n/a |

Conditions here are **pre-release** only. A condition that would have to be satisfied after publication is not a condition; it is an unmanaged exposure.

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `LEGAL_ENTITY_SIGNATORY_AUTHORITY` | Authority to make statements binding on the entity | Published content is an assertion the entity is answerable for |
| `EXECUTIVE_AUTHORITY` | Executive authority over external communication | Proportionate for routine content within an approved position |
| `FUNCTIONAL_AUTHORITY` | Communications function authority, **only** for content wholly within an already-approved institutional position | Content that establishes a new position is not routine |

`role.institutional_communications_editorial_specialist` owns editorial standards and is **not** eligible: owning the standard is not authority to publish against it.

## Cardinality

`SINGLE_HOLDER` for routine content within an approved position; **`MULTI_HOLDER_ALL_REQUIRED`** where the content states a new institutional position, makes a commercial claim, or discloses information about a third party — communications authority plus the functional authority owning the substance.

## Delegation Policy

**`DELEGABLE_WITHIN_ELIGIBILITY`**, bounded to a content class and a period. **Re-delegation prohibited.** Not delegable where cardinality is `MULTI_HOLDER_ALL_REQUIRED`.

## Revocation and Supersession

Revocation ends future exercise; it retracts nothing already published. A later publication decision may supersede an earlier one **as the current position**; the earlier publication remains a historical fact and its record stands. Retraction is a **new decision**, not an undoing of the old one.

## Prerequisites

Content exists at a stated version; every material claim is substantiated; `review.factual_evidence` is `SATISFIED` where the content makes factual assertions, and `review.commercial_claims` where it makes commercial ones; publication-requirements validation is complete — **which is explicitly not independent review**; and third-party information carries `decision.disclosure_authorisation` separately.

## Workflow / Handoff / Review References

`workflow.decision_grade_document_preparation` S5; `workflow.external_publication_preparation`; informed by `review.factual_evidence`, `review.institutional_position`, `review.commercial_claims`, `review.accessibility` where the surface is user-facing.

## Required Evidence

Beyond the generic eighteen: the content version published; substantiation for each material claim; the review statuses at decision time; the audience and channel; and any third-party information with its separate disclosure authorisation.

## Open Item, Finding and Risk Handling

An open finding on published content **remains open and becomes a finding about published content**, which is a materially worse position than the same finding pre-release. This Right does not close it, and the escalation in consequence is recorded.

## Expiry / Re-Decision Trigger

Bound to the content version. Any change after decision and before release voids the decision. Re-decision is required where the underlying position changes, a substantiating source is superseded, or a claim becomes inaccurate with time.

## Exceptional Progression Rule

**Not within this Right.** Publishing with an unsatisfied review requires `decision.exceptional_progression` first. Publication is the archetypal case where visibility is not resolution: an unverified claim published is an unverified claim, more widely.

## Risk / Waiver Boundary

Accepts **no** risk and waives **no** requirement. It cannot waive a regulatory disclosure obligation, a contractual confidentiality obligation, or a third party's rights over their own information.

## Emergency Rule

**None.** Urgent communications remain publications and use this Right.

## Knowledge-State Effect

**None. Publication is not canonical promotion.** Content the world can read is not thereby the entity's canonical position — that requires `decision.canonical_knowledge_promotion` and its own prerequisites. The two are kept separate because organisations routinely treat the published version as the true one, which is exactly the inference this boundary denies.

## Out-of-Scope Authority

This Right does **not**: promote anything to `CANONICAL`; authorise disclosure of third-party or controlled information (`decision.disclosure_authorisation`); authorise data transmission (`decision.external_data_transmission`); make a claim true; satisfy any review; commit the entity contractually; or bind the entity to anything the content merely describes.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
