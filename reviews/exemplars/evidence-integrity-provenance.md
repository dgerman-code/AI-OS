# Evidence Integrity and Provenance Review

Status: PROPOSED — Phase 6 exemplar Review Profile Card
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: Evidence Integrity and Provenance Review
- Review ID: `review.evidence_integrity_provenance`
- Version: 0.1
- Status: PROPOSED
- Review Family: Evidence / Factual Integrity
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Decision-grade work rests on an evidence base whose integrity nobody checks unless someone is required to. This review verifies that the evidence base under a conclusion is traceable, correctly versioned, correctly state-labelled, and honest about its gaps — **without checking whether the conclusion drawn from it is right.**

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.evidence_integrity_record` | `role.knowledge_evidence_steward` |
| `artifact.evidence_gap_conflict_report` | `role.knowledge_evidence_steward` |
| the assumption register and source-verification record of the reviewed work product | the Role owning that work product |

`role.knowledge_evidence_steward` is the producer of the first two and is therefore **ineligible** to satisfy this review over its own records in the same assignment.

## Applicability / Trigger

Required where a work product will be relied on for a decision that is costly to reverse, or transmitted externally. Advisory at Routine / Standard; **mandatory at Enhanced Decision-Grade and above** under `architecture/project-criticality-policy.md`.

## Required Evidence Package

The evidence integrity record; the gap and conflict report; the assumption register with basis and owner per entry; source verification records with provenance and effective date; version identity of every artifact relied on; the traceability record linking claims to sources. An incomplete package produces `REVIEW_BLOCKED`, not a finding.

## Independence Class

`PEER_REVIEW` at Enhanced Review Candidate; **`INDEPENDENT_ASSURANCE_REVIEW` at Enhanced Decision-Grade and above.**

## Reviewer Eligibility

- A second `role.knowledge_evidence_steward` instance that did not produce the evidence records under review — the natural peer;
- `role.accounting_financial_due_diligence_specialist` where the evidence base is predominantly financial and its Role Card evidence-discipline scope applies;
- `role.data_room_disclosure_manager` where the evidence base is a disclosure set and provenance is its owned surface.

Eligibility is checked against the producing assignment: whoever built the record cannot review it.

## Reviewer Prohibitions

- The `role.knowledge_evidence_steward` instance that produced the evidence records in this assignment;
- any Role that authored a conclusion resting on this evidence base — it would be reviewing the foundation of its own claim;
- the Workflow stage lead where that Role assembled the evidence base;
- any reviewer whose only claim to independence is a different model or runtime.

## Review Scope
### Checks
- every material `FACT` traces to a verified source with provenance and effective date;
- every `ASSUMPTION` is registered with a basis and a named owner, and is not presented as fact;
- every `CALCULATION` traces to its inputs and stated method;
- version identity is unambiguous and superseded inputs are flagged, not silently used;
- gaps are recorded as `UNKNOWN` rather than omitted;
- conflicts are recorded as `CONFLICT_DETECTED` with both positions, not resolved by preference;
- knowledge-state labels are applied consistently and no state was promoted by workflow progression.

### Does Not Check
- **whether the domain conclusion is correct** — that is the domain review: `review.engineering_technical`, `review.financial_model`, `review.legal_compliance`, `review.esg_safeguards` or the applicable other;
- **whether the facts are true in the world** — this review verifies traceability to a verified source, not the source's correctness;
- whether the analytical method was appropriate — `review.analytical_method`;
- whether the document is fit for its audience — `review.factual_evidence` for claim substantiation, or the applicable publication review.

## Method at Architecture Level

Structured tracing from claim to source and back, sampling at Routine and exhaustive at Enhanced Decision-Grade, plus a register completeness check and a state-label consistency pass.

## Finding Taxonomy Application

| Class | Example here |
|---|---|
| `NO_FINDING` | Every material claim traces; registers complete; states consistent |
| `OBSERVATION` | A citation format inconsistency that does not impair traceability |
| `MINOR_FINDING` | A non-material fact lacking an effective date |
| `MAJOR_FINDING` | A material `FACT` with no verified source, or an `ASSUMPTION` presented as a fact |
| `CRITICAL_FINDING` | A knowledge state promoted without a governed transition; a superseded input used silently; a recorded conflict removed without disposition |

## Satisfaction Criteria

`SATISFIED` when every material claim traces, the assumption register is complete with owners, gaps and conflicts are visible, and no state was promoted outside a governed transition.

An unresolved `CRITICAL_FINDING` **can never be satisfied**. An unresolved `MAJOR_FINDING` blocks satisfaction; this Profile permits **no** conditional disposition, because a conclusion resting on an unsourced material fact is not a lesser defect at any criticality. Unresolved `MINOR_FINDING`s may remain open only where each is `NON_MATERIAL_TO_NEXT_STEP` per Phase 5 §14A.

**Satisfaction is not approval.** It does not make the evidence base or anything resting on it `APPROVED` or `CANONICAL`.

## Rework and Closure Requirements

`MAJOR` and `CRITICAL` route to the Role owning the affected claim, not to the evidence steward — the steward records provenance, it does not manufacture the missing source. Closure requires the source, the corrected label, or the removal of the claim, plus a closure rationale. Re-review is **mandatory** after any `CRITICAL` closure and after any `MAJOR` closure that changed a material claim.

Closure preserves the original finding, its severity, the response evidence, the rationale, and both artifact versions.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: a source is superseded; a material assumption changes or is resolved; a new material claim is added; a conflict is recorded or disposed of; or the artifact version relied on changes materially.

## Criticality Scaling

| Band | Independence | Depth |
|---|---|---|
| Routine / Standard | `PEER_REVIEW`, advisory | Sampling |
| Enhanced Review Candidate | `PEER_REVIEW`, expected | Material claims exhaustively |
| Enhanced Decision-Grade | `INDEPENDENT_ASSURANCE_REVIEW`, mandatory | Every claim traced individually; closure evidence required |
| Major / Systemic | As above, plus mandatory re-review on any material change | Full |

Criticality changes independence depth and evidence rigour. It does not change the review's identity, and no second Profile is created for larger projects.

## Workflow / Handoff References

Carried as a `REVIEW_REQUIRED_REFERENCE` at `workflow.project_development_readiness` S6, `workflow.eu_grant_application_development` S5, and `workflow.decision_grade_document_preparation` S3–S4. Required `SATISFIED` before transfer on `handoff.technical_commercial_cost_to_financial_model` at Enhanced Decision-Grade.

## Decision Right Boundary

Informs `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change`. It makes none of them, and satisfaction is not approval. Where a document proceeds to a transmitting act, the applicable transmitting-act gate is unaffected by this review's status.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no independence, severity or satisfaction change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
