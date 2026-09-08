# Granting Authority Submission

Status: PROPOSED — Phase 7 exemplar Decision Right Card
Inherits: `standard.decision.common_constraints@0.1`

## Identity
- Decision Name: Granting Authority Submission
- Decision ID: **`decision.granting_authority_submission`**
- Version: 0.1
- Status: PROPOSED
- Decision Family: Programme / Grant / Submission
- Decision Class: `COMMITMENT_DECISION`
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.decision.common_constraints@0.1`
- Supersedes / Superseded By: none

**Upstream ID preserved.** The prompt named this exemplar `decision.grant_submission`; upstream uses `decision.granting_authority_submission`, at `workflow.eu_grant_application_development` S6 and in three Role Cards. The longer name is also the more accurate one — it names the recipient, which is what makes the act a transmitting one.

## Decision Subject

Submission of **one** governed application, report, claim or amendment package, at a stated version, to a named granting authority under a named call or agreement.

## Decision Effect

Transmits the package externally. This is **irreversible in substance**: what the authority has received cannot be unreceived, and everything the package asserts becomes an assertion the entity has made to a funder.

## Allowed Outcomes and Their Effects

| Outcome | Workflow progression | Handoff eligibility | External action | Review status | Knowledge state | Conditions / open items | Expiry |
|---|---|---|---|---|---|---|---|
| `APPROVE` | S6 exits; the submission occurs | n/a — terminal | **Package transmitted to the authority** | Unchanged | None | Open items retained in the record of what was submitted | Version-bound |
| `REJECT` | Blocked; do-not-submit | n/a | None | Unchanged | None | Retained | n/a |
| `DEFER` | Not permitted; gate unsatisfied | n/a | None | Unchanged | None | Retained | n/a |

**`APPROVE_WITH_CONDITIONS` is not permitted.** A submission cannot be conditional: the package either goes or it does not, and a condition attached after transmission binds nobody at the receiving end.

## Holder Eligibility

| Eligibility class | Authority basis required | Why not a lesser class |
|---|---|---|
| `LEGAL_ENTITY_SIGNATORY_AUTHORITY` | Authority to bind the entity externally | A submission makes assertions the entity is answerable for |
| `EXECUTIVE_AUTHORITY` | Where the governing arrangement places grant submission within executive authority below a stated value | Proportionality for small actions |
| `PROJECT_OR_PROGRAMME_SPONSOR_AUTHORITY` | **Only jointly**, never alone | The sponsor wants the grant; wanting it is not authority to bind |

**`role.eu_grants_programmes_specialist` is not eligible.** It owns the package, leads the workflow and knows the call better than any holder will — and none of that is authority to bind the entity. The Phase 5 card already states the workflow cannot submit; this states who can.

## Cardinality

`SINGLE_HOLDER` where signatory authority alone suffices under the governing arrangement; **`MULTI_HOLDER_ALL_REQUIRED`** where co-financing exposure, consortium coordination or a value threshold requires both signatory and sponsor authority. One person holding both classes is **one holder, not two**.

## Delegation Policy

**`DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`.**

Delegable only within `LEGAL_ENTITY_SIGNATORY_AUTHORITY`, for a named call, for a stated period, with a value ceiling where the arrangement sets one. **Re-delegation prohibited.** Delegation never reduces a `MULTI_HOLDER_ALL_REQUIRED` requirement to one, and a deadline is not a constraint that permits delegation the arrangement does not.

## Revocation and Supersession

Revocation ends future exercise. **It cannot recall a submitted package** — the external act stands. A later submission of a revised package supersedes the earlier one *as the operative submission* only where the authority's own rules permit resubmission; the original remains in the record either way. Withdrawal, where the authority permits it, is a separate external act requiring its own exercise of this Right.

## Prerequisites

The package exists at a stated version; the rulebook version relied on is **current at decision time**; `review.eu_programme_compliance` is `SATISFIED`, or `decision.exceptional_progression` has been exercised over each named unsatisfied element; every eligibility condition has an evidenced status; required partners are confirmed under `decision.partner_commitment`; and `decision.consortium_decision_confirmation` is taken where the consortium's arrangement requires it.

## Workflow / Handoff / Review References

`workflow.eu_grant_application_development` S6 (`HUMAN_GATE_REFERENCE`); `handoff.application_content_to_compliance_review` (downstream); informed by `review.eu_programme_compliance`, `review.factual_evidence`, `review.evidence_integrity_provenance`.

## Required Evidence

Beyond the generic eighteen: the package version submitted; the rulebook version and its currency confirmation date; the compliance matrix status; the eligibility condition status list; partner confirmation status; every unverified claim remaining in the package; and the review status at decision time.

## Open Item, Finding and Risk Handling

Open items **remain open after submission** and become open items of the submitted package. A finding recorded before submission is a finding about what was submitted, and it does not close by the package leaving.

## Expiry / Re-Decision Trigger

The decision is bound to the package version. Any change to the package after decision and before transmission **voids the decision** and requires a new one. Where the authority permits resubmission, each submission is its own decision.

## Exceptional Progression Rule

**Not within this Right.** Submitting with an unsatisfied compliance review requires `decision.exceptional_progression` first, exercised over each named element. **Deadline pressure is not a basis for this Right at all** — the Phase 5 card states a missed deadline is an acceptable outcome where the alternative is an ungated submission, and this Right does not soften that.

## Risk / Waiver Boundary

Accepts **no** risk and waives **no** requirement. It does not waive an eligibility condition, cure an unverified claim, or excuse a rulebook requirement — and it cannot waive the granting authority's own rules, which are not the entity's to waive.

## Emergency Rule

**None.** There is no emergency grant submission. A deadline is foreseeable by definition.

## Knowledge-State Effect

**None.** The package does not become `APPROVED` or `CANONICAL` by being submitted.

## Out-of-Scope Authority

This Right does **not**: satisfy or relabel `review.eu_programme_compliance` — the Phase 6 Profile's status is untouched; assert that any eligibility condition is met; commit a partner (`decision.partner_commitment`); approve the budget (`decision.budget_approval`); accept a grant award, which is a separate act on receipt; bind the entity to implementation obligations before an agreement is executed; or authorise any other external transmission.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version.

## Non-Runtime Statement

This card is declarative architecture. It specifies no database schema, API, interface, notification, workflow runtime, model routing, agent execution, signature, identity, authentication or authorisation mechanism, and binds no person, organisation, job title, provider or runtime identity.
