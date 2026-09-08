# Project Integration Coherence Review

Status: PROPOSED — Phase 6 exemplar Review Profile Card
Inherits: `standard.review.common_constraints@0.1`

## Identity
- Review Name: Project Integration Coherence Review
- Review ID: `review.project_integration_coherence`
- Version: 0.1
- Status: PROPOSED
- Review Family: Project / Investment
- Governance Owner: AI-OS architecture governance
- Inherits: `standard.review.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Nine specialist Roles each produce a defensible position, and the readiness assessment assembles them. This review checks the **space between** those positions: whether they contradict one another, whether one silently assumes what another denies, and whether the assembly cites them faithfully. It is the only review whose subject is the relationships rather than the contents.

It exists because no domain reviewer can perform it — each is bounded to its own domain, and the contradiction lives between two domains neither owns.

## Subject and Owning Role(s)

| Subject artifact / conclusion | Owning `role.<id>` |
|---|---|
| `artifact.development_readiness_assessment` | `role.project_development_lead` |
| the consistency relationships between the specialist artifacts it cites | no single Role — this is the review's reason to exist |

The specialist artifacts themselves remain owned and separately reviewed by their own Roles.

## Applicability / Trigger

Required where a readiness or integration position assembles conclusions from three or more separately owned workstreams. **Mandatory at Major / Systemic**, expected at Enhanced Decision-Grade.

## Required Evidence Package

The integration artifact at a stated version; every specialist artifact it cites, each at the version cited and with its own state; the consolidated assumption register; the open-item list with Phase 5 materiality classification; the record of any `CONFLICT_DETECTED` and its disposition.

## Independence Class

**`CROSS_DOMAIN_REVIEW`** by definition — the reviewer checks across domains and concludes on none of them. Escalates to `INDEPENDENT_ASSURANCE_REVIEW` at Major / Systemic, where the reviewer must also be outside the delivery line.

## Reviewer Eligibility

| `role.<id>` | Eligibility class | Scope basis in its Role Card | Dimension covered |
|---|---|---|---|
| `role.portfolio_programme_manager` | `FULL_PROFILE_REVIEWER_ELIGIBLE` | Owns interdependency logic and aggregated cross-workstream visibility — the whole of this Profile's satisfaction criteria | All |
| A second `role.project_development_lead` instance from outside this assignment | `FULL_PROFILE_REVIEWER_ELIGIBLE` | Owns integration of technical, commercial, financial, legal and ESG workstreams into a project case | All |
| `role.knowledge_evidence_steward` | `BOUNDED_REVIEW_CONTRIBUTOR` | Owns provenance and traceability, **not cross-workstream consistency** | Citation fidelity and traceability only |

Every eligible reviewer holds a cross-domain integrating surface. **None acquires authority in any domain by reviewing across them**, and the bounded contributor cannot satisfy the Profile on citation fidelity alone.

## Reviewer Instance Segregation

**`SEGREGATION_REQUIRED`.**

This is the most conservative declaration in the exemplar set and it is deliberate. This Profile's entire value is that it is a *second* perspective across positions that have each already been checked within their own domain. An instance that also satisfied one of those domain Profiles would carry its reading of that domain into the consistency check — and the contradiction this review exists to find is most likely to sit exactly where that reading is wrong. Concentrating both checks in one instance would defeat the purpose rather than economise on it.

## Review Dependencies

Each prerequisite is a **concrete** `review.<id>`, activated only where the corresponding position is actually cited. There is no category row: a dependency on "the applicable domain review" would not be testable.

| Prerequisite `review.<id>` | Required status | Activation condition | Bounded purpose |
|---|---|---|---|
| `review.engineering_technical` | `SATISFIED` | `artifact.feasibility_study` or `artifact.technical_basis_of_design` is cited **and** band is Enhanced Decision-Grade or above | The technical position is sound within its domain before consistency with other positions is assessed |
| `review.cost_estimate` | `SATISFIED` | `artifact.cost_estimate` is cited **and** band is Enhanced Decision-Grade or above | As above, for the cost basis |
| `review.financial_model` | `SATISFIED` | `artifact.financial_model` is cited **and** band is Enhanced Decision-Grade or above | As above, for the modelled position |
| `review.legal_compliance` | `SATISFIED` | `artifact.legal_analysis` is cited **and** band is Enhanced Decision-Grade or above | As above, for the legal position |
| `review.esg_safeguards` | `SATISFIED` | `artifact.es_impact_assessment` is cited **and** band is Enhanced Decision-Grade or above | As above, for the E&S position |
| `review.risk_quantification` | `SATISFIED` | `artifact.risk_quantification_analysis` is cited **and** band is Enhanced Decision-Grade or above | As above, for the quantified risk position |

Below Enhanced Decision-Grade the dependency does not activate: consistency checking has value on `DRAFT` positions and blocking it would remove the early warning it exists to give.

Where a required prerequisite is unsatisfied or `STALE`, this review is **`REVIEW_BLOCKED`** — it has found no defect, it cannot yet run. **Satisfaction of every domain review does not satisfy this one**: positions can each be individually sound and mutually contradictory, which is the whole reason this Profile exists.

## Reviewer Prohibitions

- The `role.project_development_lead` instance that assembled the assessment in this assignment;
- **any specialist Role whose own position is among those being checked for consistency** — it cannot adjudicate a contradiction it is party to;
- any Role that would need to conclude in a domain to identify the contradiction — if the check requires a domain conclusion, it belongs to that domain's review, not here;
- any reviewer whose independence rests only on model or runtime difference.

## Review Scope
### Checks
- every claim in the integration artifact is traceable to a specialist artifact at a cited version;
- no specialist conclusion is restated in the assembling Role's own voice, or altered in the restatement;
- positions are mutually consistent: no two cited artifacts assert incompatible facts, assumptions or constraints;
- an assumption material in one workstream is not silently contradicted in another;
- every `CONFLICT_DETECTED` between positions is recorded with both sides and an explicit disposition, not averaged or narrated away;
- the consolidated assumption register carries forward every material assumption from every workstream;
- open items are classified per Phase 5 §14A and none material was dropped in assembly.

### Does Not Check
- **any domain conclusion's correctness** — feasibility to `review.engineering_technical`, cost to `review.cost_estimate`, model to `review.financial_model`, legal to `review.legal_compliance`, E&S to `review.esg_safeguards`, risk to `review.risk_quantification`;
- whether the evidence under each position is traceable — `review.evidence_integrity_provenance`;
- whether the project is ready — `review.project_readiness` asks whether the evidence is sufficient; **this review asks only whether the positions contradict each other.** The two are adjacent and the boundary is deliberate;
- whether to proceed — a human decision.

## Method at Architecture Level

Pairwise consistency comparison across cited positions on shared facts, assumptions and constraints; citation-fidelity tracing from assembly back to source artifact; assumption-register reconciliation across workstreams.

## Finding Taxonomy Application

| Class | Example here |
|---|---|
| `NO_FINDING` | All claims trace; no contradictions; register complete |
| `OBSERVATION` | Two workstreams use different terminology for the same constraint without ambiguity |
| `MINOR_FINDING` | A citation to an artifact version superseded by a non-material revision |
| `MAJOR_FINDING` | A material assumption present in one workstream and absent from the consolidated register; a specialist conclusion restated with altered meaning |
| `CRITICAL_FINDING` | Two cited positions assert incompatible facts and the assembly presents a resolution neither Role made; a recorded `CONFLICT_DETECTED` removed without disposition |

## Satisfaction Criteria

`SATISFIED` when every claim traces faithfully, **every material contradiction between cited positions has been resolved by the Roles that own those positions**, and every material assumption and open item is carried.

### An unresolved material contradiction is an open finding

This is the load-bearing rule of this Profile, and the one an earlier revision got wrong.

A material contradiction between two cited positions is a `MAJOR_FINDING` or `CRITICAL_FINDING` and **remains an open review finding until the owning Roles resolve it**. While it remains unresolved the review status is `NOT_SATISFIED` or `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`.

**It cannot become `SATISFIED` because the contradiction is recorded, made visible, attributed to its owning Roles, escalated, or carried to a human gate.** Visibility is not resolution. Each of those acts is correct and necessary, and none of them satisfies this review.

A named external human `decision.<id>` may permit **Workflow progression** with the contradiction unresolved. Where it does:

- it does **not** close the finding;
- it does **not** satisfy this review — the status remains `NOT_SATISFIED` or `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`;
- it does **not** convert the contradiction into a minor or non-material item;
- the contradiction **remains open and is carried forward** into every subsequent stage and gate.

An unresolved `CRITICAL_FINDING` **can never be satisfied** — an assembly that resolves a specialist contradiction on its own authority is exactly the failure this review exists to catch. An unresolved `MAJOR_FINDING` blocks satisfaction, with **no conditional disposition permitted**: neither a missing material assumption nor an unreconciled contradiction is confinable.

**Satisfaction is not approval.** It does not make the integration artifact or any cited specialist position `REVIEWED`, `APPROVED` or `CANONICAL`, and it does not assert that the project is ready — only that the positions assembled do not contradict one another.

## Rework and Closure Requirements

A contradiction routes to **both** owning Roles, never to the assembling Role.

**Closure requires evidence that the owning domain Roles have actually reconciled or otherwise resolved the contradiction** against this Profile's criteria — a revised position from one or both, or a joint statement recording that the apparent conflict was a difference of scope rather than of substance. Carrying the contradiction to a decision-maker is **not** closure and never was: it is what the Workflow does with an open finding, not what disposes of one. Re-review is **mandatory** after any `CRITICAL` closure and after any `MAJOR` closure that changed a cited position.

**The integration reviewer must not settle the underlying specialist disagreement itself.** It identifies the contradiction, attributes it to the two owning Roles, and stops. A reviewer that adjudicates between two domain positions has taken authority in both domains, which `CROSS_DOMAIN_REVIEW` explicitly denies it — and would reproduce, one level up, precisely the failure this Profile exists to catch in the assembling Role.

Citation-fidelity findings route to the assembling Role and close on a corrected citation.

## Re-Review Triggers

A prior satisfaction becomes `STALE` when: any cited specialist artifact is revised or superseded; a new workstream position is added to the assembly; a material assumption changes in any cited workstream; or a conflict is newly recorded or disposed of.

## Criticality Scaling

| Band | Independence | Depth |
|---|---|---|
| Routine / Standard | `CROSS_DOMAIN_REVIEW`, advisory | Citation fidelity only |
| Enhanced Review Candidate | `CROSS_DOMAIN_REVIEW`, expected | Fidelity plus pairwise consistency on headline claims |
| Enhanced Decision-Grade | `CROSS_DOMAIN_REVIEW`, mandatory | Full pairwise consistency; register reconciled across all workstreams |
| Major / Systemic | `INDEPENDENT_ASSURANCE_REVIEW`, mandatory, reviewer outside the delivery line | Full, with no unrecorded contradiction permitted at exit |

## Workflow / Handoff References

Carried as a `REVIEW_REQUIRED_REFERENCE` at `workflow.project_development_readiness` S6, where the card already names it, and mandatory there at Major / Systemic.

## Decision Right Boundary

Informs `decision.stage_gate_progression`, `decision.project_definition_freeze` and `decision.business_case_approval`. It makes none of them, and it does not itself conclude that the project is ready.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no independence, severity or satisfaction change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, reviewer assignment, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
