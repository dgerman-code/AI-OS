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

- `role.portfolio_programme_manager`, whose Role Card owns interdependency logic and aggregated visibility across constituent work;
- a second `role.project_development_lead` instance from outside this assignment;
- `role.knowledge_evidence_steward` for the citation-fidelity and traceability dimension specifically — bounded to that dimension.

Every eligible reviewer holds a cross-domain integrating surface. **None acquires authority in any domain by reviewing across them.**

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

`SATISFIED` when every claim traces faithfully, no unrecorded contradiction exists between cited positions, and every material assumption and open item is carried.

An unresolved `CRITICAL_FINDING` **can never be satisfied** — an assembly that resolves a specialist contradiction on its own authority is exactly the failure this review exists to catch. An unresolved `MAJOR_FINDING` blocks satisfaction, with **no conditional disposition permitted**: a missing material assumption is not confinable.

**Satisfaction is not approval.** It does not make the integration artifact or any cited specialist position `REVIEWED`, `APPROVED` or `CANONICAL`, and it does not assert that the project is ready — only that the positions assembled do not contradict one another.

## Rework and Closure Requirements

A contradiction routes to **both** owning Roles, not to the assembling Role — the lead may not adjudicate between them, and closure requires that the owning Roles either reconcile their positions or that the contradiction is carried explicitly as an open item to the decision-maker. Citation-fidelity findings route to the assembling Role. **Re-review is mandatory** after any `CRITICAL` closure.

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
