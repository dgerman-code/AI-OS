# Security Review

Status: PROPOSED — Phase 6 exemplar Review Profile Card
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: Security Review
- Review ID: `review.security`
- Version: 0.1
- Status: PROPOSED
- Review Family: Product / Software / Data / Security
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

`role.security_engineer` designs the threat model, designs the controls, and — under the approved Phase 5 correction — implements the security controls it owns. That concentration is correct for ownership and **fatal for self-assessment**: the Role that designed and built a control cannot be the one that independently validates it. This review is the check that separation is preserved.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.security_control_assessment` | `role.security_engineer` |
| `artifact.security_control_implementation` | `role.security_engineer` |
| the threat model and residual-risk statement | `role.security_engineer` |

## Applicability / Trigger

Required where a change touches a security-relevant surface, processes personal or regulated data, alters an authorisation model, or exposes an external interface. **Mandatory at Enhanced Review Candidate and above**; at Routine, a recorded screening by the owning Role is required and is explicitly `PRODUCER_REVIEW`, not this review.

## Required Evidence Package

The threat model at a stated version; the control design; the control implementation record; the validation evidence per control; the residual risk statement; the architecture position the controls sit on (`artifact.solution_architecture_specification`); the security test scope and results where security testing was performed.

## Independence Class

`PEER_REVIEW` at Enhanced Review Candidate; **`INDEPENDENT_ASSURANCE_REVIEW` at Enhanced Decision-Grade and above**, and always where security accreditation is in prospect.

## Reviewer Eligibility

- A second `role.security_engineer` instance that neither designed nor implemented the controls in this assignment — the primary and usually only fully-qualified peer;
- `role.solution_architect` for `CROSS_DOMAIN_REVIEW` of whether the controls are consistent with the adopted architecture — **this class cannot conclude on control adequacy**, which is the security domain's own;
- `role.data_protection_gdpr_specialist` where the controls implement a data-protection obligation, bounded to that obligation.

The narrowness of this eligibility list is deliberate and is the finding worth carrying forward: for a single-security-engineer assignment there may be **no eligible reviewer**, in which case the review is `NOT_SATISFIED` and the Workflow blocks, reworks or escalates. **An unavailable reviewer does not lower the requirement.**

## Reviewer Prohibitions

- The `role.security_engineer` instance that designed or implemented the controls in this assignment — the central prohibition of this Profile;
- `role.software_qa_test_automation_specialist` over control adequacy: it executes security testing **within a scope the Security Engineer defines**, which makes its testing an input to this review, never a substitute for it;
- the implementing engineers (`role.full_stack_software_engineer`, `role.integration_api_engineer`, `role.database_data_engineer`, `role.platform_devops_engineer`) over controls in the code or environments they built;
- **any reviewer whose claim to independence is a different model or runtime** — this Profile states it explicitly because security is where the substitution is most tempting.

## Review Scope
### Checks
- the threat model covers the change's actual surface, including surfaces introduced by the change;
- each identified threat has a designed control, an accepted residual risk, or an explicit `UNKNOWN`;
- each designed control is implemented as designed;
- each implemented control is validated, or its non-validation is explicit — not silently absent;
- the residual risk statement is complete and characterised, not merely non-empty;
- controls are consistent with the adopted architecture position;
- security testing scope matches the threat model it claims to exercise.

### Does Not Check
- **general architecture soundness** — `review.architecture`;
- **data model and migration soundness** — `review.data_architecture`;
- **whether tests cover the acceptance criteria** — `review.test_coverage`; this review checks security test *scope against the threat model*, which is a different question;
- code quality generally — `review.code`;
- data-protection legal conclusions — `review.data_protection`;
- accessibility — `review.accessibility`;
- **whether to accept the residual risk** — `decision.security_risk_acceptance`, a human right;
- **whether to accredit** — `decision.security_accreditation`, a human right.

## Method at Architecture Level

Independent threat-surface reconstruction, control-to-threat coverage mapping, design-to-implementation conformity checking, and validation-evidence assessment. Not a penetration test, not a re-implementation, and not a re-run of the QA suite.

## Finding Taxonomy Application

| Class | Example here |
|---|---|
| `NO_FINDING` | Threat surface covered; controls implemented as designed and validated; residual risk characterised |
| `OBSERVATION` | A control documented in a non-standard place without ambiguity |
| `MINOR_FINDING` | A validated control whose evidence lacks a timestamp |
| `MAJOR_FINDING` | A designed control not implemented; an implemented control not validated; a residual risk stated but not characterised |
| `CRITICAL_FINDING` | A threat surface introduced by the change and absent from the threat model; a control validated by the Role that implemented it and presented as independent; a residual risk omitted entirely |

## Satisfaction Criteria

`SATISFIED` when the threat model covers the actual surface, every threat has a control or an explicit accepted residual, every designed control is implemented and validated, and the residual risk statement is complete — **and when the reviewer met the eligibility constraints above.** Satisfaction by an ineligible reviewer is not satisfaction; it is a `CRITICAL_FINDING` against the process.

An unresolved `CRITICAL_FINDING` **can never be satisfied**. An unresolved `MAJOR_FINDING` blocks satisfaction; this Profile permits a **bounded conditional disposition** only where the control is confined to a surface the release does not expose, that confinement is independently verified, and **`decision.security_risk_acceptance`** governs any progression. The Profile references that right and does not exercise it.

**Satisfaction is not approval.** It is not accreditation, not risk acceptance, and not authorisation to release.

## Rework and Closure Requirements

All findings route to `role.security_engineer` for design and control defects, and to the implementing Role for conformity defects — with the security engineer retaining the assessment. Closure requires the implemented or corrected control plus validation evidence produced independently of the implementer. **Re-review is mandatory** after every `CRITICAL` closure and every `MAJOR` closure, without exception: a security finding closed without re-review is not closed.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: the change's surface alters; a control is modified; the architecture position changes; a new threat class becomes applicable; or a dependency with a security-relevant interface is updated.

## Criticality Scaling

| Band | Independence | Depth |
|---|---|---|
| Routine / Standard | Recorded `PRODUCER_REVIEW` screening — **explicitly not this review** | Screening only |
| Enhanced Review Candidate | `PEER_REVIEW`, mandatory | Coverage mapping and conformity check |
| Enhanced Decision-Grade | `INDEPENDENT_ASSURANCE_REVIEW`, mandatory | Above, plus independent threat-surface reconstruction and validation-evidence assessment |
| Major / Systemic | As above; accreditation position required; no `MAJOR` conditional disposition permitted | Full |

## Workflow / Handoff References

Carried as a `REVIEW_REQUIRED_REFERENCE` at `workflow.software_change_delivery` S2, S4 and S6. Required `SATISFIED` before transfer on `handoff.software_implementation_to_security_and_test_review`'s onward step to release readiness at Enhanced Decision-Grade and above.

## Decision Right Boundary

Informs `decision.security_risk_acceptance`, `decision.security_accreditation`, `decision.production_release` and `decision.emergency_production_change`. It makes none of them, and satisfaction authorises no release.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no independence, severity or satisfaction change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
