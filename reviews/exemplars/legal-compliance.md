# Legal and Regulatory Compliance Review

Status: PROPOSED — Phase 6 exemplar Review Profile Card
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: Legal and Regulatory Compliance Review
- Review ID: `review.legal_compliance`
- Version: 0.1
- Status: PROPOSED
- Review Family: Legal / Compliance / Procurement
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

A legal analysis is easy to over-read: a bounded analysis of an obligation set gets cited downstream as though it settled the question. This review verifies that the analysis is correctly grounded, current, and **correctly bounded as analysis rather than opinion** — the last of which is the boundary most often lost in transit.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.legal_analysis` | `role.legal_regulatory_lead` |
| `artifact.contract_review_note` | `role.legal_regulatory_lead` |
| regulatory perimeter statements within a wider work product | `role.legal_regulatory_lead` |

## Applicability / Trigger

Required where a legal or regulatory position is relied on outside the legal workstream, or is transmitted externally. **Mandatory at Enhanced Decision-Grade and above**, and whenever the analysis bears on a transmitting act or a commitment gate.

## Required Evidence Package

The analysis at a stated version; the legal sources relied on with their currency confirmed and effective dates; the factual basis supplied by other Roles and its state; the stated jurisdiction and scope; the explicit statement of what the analysis does not conclude.

## Independence Class

`PEER_REVIEW` at Enhanced Review Candidate; **`INDEPENDENT_ASSURANCE_REVIEW` at Enhanced Decision-Grade**, and always where the analysis supports an external transmitting act.

## Reviewer Eligibility

- A second `role.legal_regulatory_lead` instance that did not author this analysis;
- `role.procurement_state_aid_specialist` for the procurement and State Aid perimeter specifically — bounded to that perimeter;
- `role.data_protection_gdpr_specialist` for data-protection reasoning specifically — bounded to that reasoning;
- `role.tax_specialist` for tax-adjacent reasoning specifically — bounded to that reasoning.

The three specialist eligibilities are **scope-bounded**: each may satisfy this review only over the part of the analysis inside its own owned domain, never over the analysis as a whole.

## Reviewer Prohibitions

- The `role.legal_regulatory_lead` instance that authored the analysis in this assignment;
- any Role supplying the factual basis, over the legal conclusions drawn from its facts;
- any Role seeking to rely on the analysis for a commitment it owns — the party wanting the answer does not review the answer;
- any reviewer whose independence rests only on model or runtime difference.

## Review Scope
### Checks
- the legal sources relied on are current at a stated effective date and correctly cited;
- the jurisdiction and regulatory perimeter are correctly identified and stated;
- the factual basis is attributed to the Role that supplied it and its state is labelled;
- reasoning follows from the sources and the facts as stated;
- the analysis is **correctly bounded** — it does not read as, and is not presented as, a formal legal opinion;
- uncertainty and unsettled points are stated rather than smoothed;
- any dependency on another specialist's conclusion is explicit.

### Does Not Check
- **whether the underlying facts are true** — factual basis is owned by the supplying Roles and reviewed under `review.factual_evidence` and `review.evidence_integrity_provenance`;
- **procurement route or State Aid conclusions in substance** — `review.procurement_state_aid`;
- **data-protection conclusions in substance** — `review.data_protection`;
- tax positions — `review.tax_analysis`;
- commercial or risk-allocation soundness — `review.commercial_structure`;
- whether to accept the legal risk — a human decision, not a review.

## Method at Architecture Level

Source-currency verification, perimeter reconstruction, reasoning trace from source and fact to stated conclusion, and a boundary check that the artifact's own scope limitation matches how it will be relied on.

## Finding Taxonomy Application

| Class | Example here |
|---|---|
| `NO_FINDING` | Sources current, perimeter correct, reasoning traceable, boundary intact |
| `OBSERVATION` | A citation style inconsistency |
| `MINOR_FINDING` | A source cited without an effective date where currency is not in doubt |
| `MAJOR_FINDING` | Reliance on a superseded source; a perimeter omission; a factual basis used without attribution or state |
| `CRITICAL_FINDING` | The analysis reads as a formal legal opinion the Role Card excludes; a jurisdiction misidentified; a conclusion drawn on a regulatory question outside the stated perimeter |

## Satisfaction Criteria

`SATISFIED` when sources are current and correctly cited, the perimeter is correct, reasoning traces, and the analysis is bounded as analysis.

An unresolved `CRITICAL_FINDING` **can never be satisfied** — a bounded analysis that reads as an opinion is a scope breach, not a quality defect. An unresolved `MAJOR_FINDING` blocks satisfaction; this Profile permits a **bounded conditional disposition** only where the finding is confined to a perimeter segment the relying decision does not touch, that confinement is stated, and a **named external Decision Right** governs any reliance regardless.

**Satisfaction is not approval, and is emphatically not a legal opinion.**

## Rework and Closure Requirements

`MAJOR` and `CRITICAL` route to `role.legal_regulatory_lead`, or to the supplying Role where the defect is in the factual basis. Closure requires the corrected analysis at a new version and, for a boundary breach, an explicit re-statement of scope. **Re-review is mandatory** after any `CRITICAL` closure.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: a relied-on legal source changes or is superseded; the factual basis changes materially; the jurisdiction or perimeter changes; or the analysis is put to a reliance materially wider than the one reviewed.

## Criticality Scaling

| Band | Independence | Depth |
|---|---|---|
| Routine / Standard | `PEER_REVIEW`, advisory | Source currency and boundary check |
| Enhanced Review Candidate | `PEER_REVIEW`, expected | Full reasoning trace |
| Enhanced Decision-Grade | `INDEPENDENT_ASSURANCE_REVIEW`, mandatory | Full trace plus independent perimeter reconstruction |
| Major / Systemic | As above, plus mandatory re-review on any source change | Full |

## Workflow / Handoff References

Carried as a `REVIEW_REQUIRED_REFERENCE` at `workflow.project_development_readiness` S3 and S6, `workflow.eu_grant_application_development` S4, and `workflow.software_change_delivery` where a contractual constraint applies.

## Decision Right Boundary

Informs `decision.contract_commitment`, `decision.risk_acceptance`, `decision.legal_external_use` and `decision.formal_legal_opinion`. It makes none of them. In particular, satisfaction does **not** convert the analysis into a formal legal opinion — that remains a separate act under `decision.formal_legal_opinion`.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no independence, severity or satisfaction change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
