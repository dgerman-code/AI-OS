# EU Programme Compliance Review

Status: PROPOSED — Phase 6 exemplar Review Profile Card
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: EU Programme Compliance Review
- Review ID: `review.eu_programme_compliance`
- Version: 0.1
- Status: PROPOSED
- Review Family: Programme / Grant
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

A governed submission is checked against an external rulebook at a bound version, under a deadline, by people who also wrote it. This review verifies conformity to the rulebook **independently of the producing team** — and exists precisely because the deadline makes producer self-checking most tempting at the moment it is least reliable.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.eu_application_package` | `role.eu_grants_programmes_specialist` |
| `artifact.cost_eligibility_assessment` | `role.grant_financial_compliance_budget_specialist` |
| `artifact.grant_budget_structure` | `role.grant_financial_compliance_budget_specialist` |

## Applicability / Trigger

Required before any submission to a granting authority, and for post-award conformity checks against an executed agreement. **Mandatory at Enhanced Review Candidate and above**; advisory only for a single-applicant action with immaterial co-financing exposure.

## Required Evidence Package

The package at a stated version; the call rulebook and annexes at the bound version with currency confirmed; the compliance matrix with each requirement mapped to content; the eligibility condition list with satisfied / not-satisfied / `UNKNOWN` status per condition; the cost eligibility assessment; partner confirmation status; source verification for factual claims.

Rulebook currency is a **package precondition**: a package prepared against a superseded rulebook version produces `REVIEW_BLOCKED`, not a finding.

## Independence Class

`PEER_REVIEW` at Enhanced Review Candidate; **`INDEPENDENT_ASSURANCE_REVIEW` at Enhanced Decision-Grade and above.**

## Reviewer Eligibility

- A second `role.eu_grants_programmes_specialist` instance that did not author this package;
- `role.eu_programme_implementation_grant_management_specialist`, whose Role Card owns obligation mapping and donor-rule interpretation — eligible for the rulebook-conformity dimension;
- `role.grant_financial_compliance_budget_specialist` for cost eligibility specifically, **provided it did not produce the eligibility assessment in this assignment**;
- `role.deliverables_reporting_specialist` for reporting-schedule conformity specifically — bounded to that dimension.

## Reviewer Prohibitions

- The `role.eu_grants_programmes_specialist` instance that authored the package;
- `role.grant_financial_compliance_budget_specialist` over its own eligibility assessment in the same assignment — eligible for the rest, ineligible for that;
- any Role that authored a narrative section, over that section;
- the Workflow stage lead of `workflow.eu_grant_application_development`;
- any reviewer whose independence rests only on model or runtime difference.

**The S5 compliance cycle inside `workflow.eu_grant_application_development` is producer quality control and does not satisfy this review** — the workflow card states this and this Profile confirms it.

## Review Scope
### Checks
- every rulebook requirement is addressed, or its gap is explicit;
- eligibility conditions are assessed against the bound rulebook version, with `UNKNOWN` where unestablished rather than assumed satisfied;
- cost eligibility is assessed against the programme's own rules and the budget is internally consistent;
- every factual claim in the package is verified or marked;
- work packages trace to intervention logic and to budget lines;
- partner composition meets the call's stated composition requirements, or the gap is explicit;
- the rulebook version relied on is current at review date.

### Does Not Check
- **whether the proposal is good** — competitiveness, quality of the intervention logic and likelihood of award are outside this review entirely;
- **legal, IP or contractual conclusions** — `review.legal_compliance`;
- **data-protection conclusions** — `review.data_protection`;
- **State Aid conclusions** — `review.procurement_state_aid`;
- MEL methodology — `review.mel_methodology`; curriculum and assessment design — `review.learning_design_quality`;
- evidence provenance under the claims — `review.evidence_integrity_provenance`;
- whether to submit — `decision.granting_authority_submission`, a human right this review does not touch.

## Method at Architecture Level

Independent requirement-by-requirement reconstruction of the compliance matrix from the rulebook, eligibility condition re-assessment, budget arithmetic and eligibility re-check, and claim-level verification sampling scaled by criticality.

## Finding Taxonomy Application

| Class | Example here |
|---|---|
| `NO_FINDING` | Every requirement addressed; eligibility established; budget consistent |
| `OBSERVATION` | A formatting deviation the rulebook does not mandate |
| `MINOR_FINDING` | A cross-reference error that does not affect conformity |
| `MAJOR_FINDING` | A rulebook requirement unaddressed; a budget line whose eligibility is unassessed; an unverified factual claim |
| `CRITICAL_FINDING` | An eligibility condition asserted as satisfied without basis; preparation against a superseded rulebook version; a partner presented as confirmed who is not |

## Satisfaction Criteria

`SATISFIED` when every rulebook requirement is addressed or its gap explicit, every eligibility condition has an evidenced status, cost eligibility is assessed, and every factual claim is verified or marked.

An unresolved `CRITICAL_FINDING` **can never be satisfied**. An unresolved `MAJOR_FINDING` blocks satisfaction; this Profile permits **no** conditional disposition, because an unaddressed rulebook requirement is not confinable — the granting authority assesses the whole package.

**Deadline pressure does not affect satisfaction criteria.** An unsatisfied review at the deadline means the review is unsatisfied; whether to submit regardless is a human decision under `decision.granting_authority_submission`, and taking it does not convert this review to `SATISFIED`.

## Rework and Closure Requirements

Findings route to the Role owning the affected content — package content to the grants specialist, eligibility and budget to the compliance specialist, specialist sections to their owners. Closure requires the corrected content and, for eligibility findings, the evidence establishing the condition. **Re-review is mandatory** after any `CRITICAL` closure and after any `MAJOR` closure touching eligibility or budget.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: the rulebook version changes; the package content changes materially; a partner's confirmation status changes; the budget changes; or the call deadline is extended with a rulebook revision.

## Criticality Scaling

| Band | Independence | Depth |
|---|---|---|
| Routine / Standard | `PEER_REVIEW`, advisory | Compliance matrix completeness |
| Enhanced Review Candidate | `PEER_REVIEW`, mandatory | Matrix reconstructed; eligibility re-assessed |
| Enhanced Decision-Grade | `INDEPENDENT_ASSURANCE_REVIEW`, mandatory | Above, plus claim-by-claim verification and full budget eligibility re-check |
| Major / Systemic | As above, plus mandatory re-review on any package change after satisfaction | Full |

## Workflow / Handoff References

Carried as a `REVIEW_REQUIRED_REFERENCE` at `workflow.eu_grant_application_development` S3 and S5. Required `SATISFIED` before transfer on `handoff.application_content_to_compliance_review`'s downstream submission-readiness step.

## Decision Right Boundary

Informs `decision.granting_authority_submission`, `decision.budget_approval` and `decision.consortium_decision_confirmation`. It makes none of them. **Satisfaction is not approval**: it does not authorise submission and does not make the package `REVIEWED`, `APPROVED` or `CANONICAL`.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no independence, severity or satisfaction change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
