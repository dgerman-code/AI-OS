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

| `role.<id>` | Eligibility class | Scope basis in its Role Card | Dimension covered |
|---|---|---|---|
| A second `role.eu_grants_programmes_specialist` instance that did not author this package | `FULL_PROFILE_REVIEWER_ELIGIBLE` | Owns call fit, application logic and the application package — the whole of this Profile's satisfaction criteria | All |
| `role.eu_programme_implementation_grant_management_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns obligation mapping and donor-rule interpretation against an executed agreement; **does not own pre-award call fit or application logic** | Rulebook-conformity dimension |
| `role.grant_financial_compliance_budget_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns cost eligibility and grant budget structure; **does not own rulebook conformity, application logic or narrative claims** | Budget, cost-eligibility and financial-compliance criteria only, **and only where it did not produce the eligibility assessment in this assignment** |
| `role.deliverables_reporting_specialist` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns deliverable and reporting schedule design | Reporting-schedule conformity only |

**Only the first row may satisfy this Profile.** An earlier revision said the financial-compliance Role was "eligible for the rest" of the package once its own assessment was excluded — that was scope widening by declaration, since its Role Card covers neither rulebook conformity nor application logic. It is now bounded to its own criteria, as are the other two contributors, and **their contributions do not aggregate** into full-Profile satisfaction.

## Reviewer Prohibitions

- The `role.eu_grants_programmes_specialist` instance that authored the package;
- `role.grant_financial_compliance_budget_specialist` over its own eligibility assessment in the same assignment, and over the whole Profile in any case — it is a bounded contributor, never a satisfier;
- any `BOUNDED_REVIEW_CONTRIBUTOR` above, as a **satisfier of this Profile**;
- any Role that authored a narrative section, over that section;
- the Workflow stage lead of `workflow.eu_grant_application_development`;
- any reviewer whose independence rests only on model or runtime difference.

**The S5 compliance cycle inside `workflow.eu_grant_application_development` is producer quality control and does not satisfy this review** — the workflow card states this and this Profile confirms it.

## Reviewer Instance Segregation

**`SEGREGATION_REQUIRED` at Enhanced Decision-Grade and above**; `ALLOWED_IF_INDEPENDENTLY_ELIGIBLE` below it.

At decision-grade, an instance satisfying this Profile and also `review.factual_evidence` or `review.evidence_integrity_provenance` over the same package would check the claims and the evidence under them with one reading — and an unverified material claim is precisely the failure mode both are meant to catch independently. Below that band the exposure is proportionate and same-instance satisfaction is permitted where each Profile's eligibility and independence pass separately.

## Review Dependencies

**None required.** This Profile assesses conformity to a rulebook at a bound version and can do so on a package whose claims are not yet independently verified — an unverified material claim is an open finding *here*, not a reason this review cannot run. Making `review.factual_evidence` a prerequisite would convert a finding this Profile is designed to raise into a blocker preventing it from raising anything.

## Review Scope
### Checks
- **every rulebook requirement is either met, or verified not applicable with evidence and a rationale.** A requirement recorded as an explicit gap is an **open finding**, not a checked item;
- **every eligibility condition is assessed against the bound rulebook version and is either satisfied, or verified not applicable where the programme rules genuinely permit N/A.** A condition that is unmet, `UNKNOWN`, unassessed, or evidenced as not-satisfied is an **open finding** — an evidenced status is a record, not a pass;
- cost eligibility is assessed against the programme's own rules and the budget is internally consistent;
- **every material factual claim is verified against the required evidence.** A claim merely marked, flagged or recorded while still unverified is an **open finding**; a claim explicitly identified as non-material may be handled under the bounded rule in Satisfaction Criteria;
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

`SATISFIED` requires all four of the following. **Recording, marking or making something visible satisfies none of them** — visibility is how an open finding is carried, not how it is disposed of.

| Dimension | Supports satisfaction | Open finding — review **not** satisfied |
|---|---|---|
| **Rulebook requirements** | Requirement **met**; or **verified not applicable** with evidence and a stated rationale | Requirement unmet, unresolved, or recorded as a gap. Normally `MAJOR_FINDING` |
| **Eligibility conditions** | Condition **assessed and satisfied**; or **verified not applicable** where the programme rules genuinely permit N/A | Condition unmet, `UNKNOWN`, unassessed, or evidenced as not-satisfied. Normally `MAJOR_FINDING`, and `CRITICAL_FINDING` where asserted satisfied without basis |
| **Factual claims** | Material claim **verified** against the required evidence; or claim **explicitly identified as non-material** and permitted by these criteria | Material claim marked, flagged or recorded but still unverified. Normally `MAJOR_FINDING` |
| **Cost eligibility** | Assessed against the programme rules, budget internally consistent | Any budget line with unassessed eligibility |

The distinction that carries the most weight here is **verified not applicable** against **unresolved gap**. The first is a finished piece of work with evidence behind it and may support satisfaction. The second is an absence of work with a note attached, and may not. An earlier revision of this card conflated them by treating "its gap is explicit" as sufficient; it is not, and never was.

An unresolved `CRITICAL_FINDING` **can never be satisfied**. An unresolved `MAJOR_FINDING` blocks satisfaction; this Profile permits **no** conditional disposition, because an unaddressed rulebook requirement is not confinable — the granting authority assesses the whole package.

A named external human `decision.<id>` may permit **progression** with an open finding — that is the submission decision's to take. It does not close the finding and does not change this review's status.

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
