# Exemplar 2 — Project assumption that remains non-canonical

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** that an assumption stays an assumption through review and approval, and that no amount of governance converts it.

## Identity
- Knowledge ID: `knowledge.grid_connection_date.project_alpha`
- Version: 1
- Subject: the date grid connection is assumed available for the project's programme
- Scope: `PROJECT/<alpha>`
- Memory class: `SEMANTIC_MEMORY`
- Origin: `HUMAN_ORIGIN`
- Sensitivity: `CONFIDENTIAL`

## Statement
Grid connection is **assumed** available from the stated date, for programme and financial-model purposes.

## The four axes, on one item

| Axis | Value |
|---|---|
| Epistemic type | `ASSUMPTION` |
| Governance state | `APPROVED` |
| Origin | `HUMAN_ORIGIN` — the date came from the programme team's judgement, not from a model |
| Conflict flags | None |

`ASSUMPTION` + `APPROVED`, held simultaneously — **this is the case the four-axis model exists for.** A single-label model would force the item to choose, and whichever it chose would lose the other half: "approved" hides that it is an assumption, "assumption" hides that reliance was authorised.

Origin matters here even though nothing in this item came from a model. Had the date been a model's suggestion, it would have been `AI_SUGGESTION` and **could not have become an `ASSUMPTION` by anyone accepting it** — adoption would have created a new linked item carrying `ORIGIN: AI_GENERATED` permanently (`knowledge/knowledge-state-model.md` §2a).

## What happened, exactly
The operator has issued no dated commitment. The date is adopted so that the programme and the model can proceed, which is a legitimate governed act. A review examined the basis and was `SATISFIED` — meaning **the assumption is well-characterised**, its sensitivity is quantified, and its failure consequence is stated. It does not mean the date is right.

An approval then authorised reliance **for the financial model and programme only**. That is what `APPROVED` bought: a bounded purpose.

## Why it cannot be promoted
`ASSUMPTION` is not a promotable type (`knowledge/canonical-promotion-governance.md` §4.1). No promotion authority exists that could convert it, no seniority overrides that, and no repetition across three model versions and two board packs changes it. It becomes a `FACT_CLAIM` when the operator issues a dated commitment — and then as a **new claim linked to this assumption**, not a relabelling of it.

## Where it must travel
Every artifact relying on the date **carries the assumption explicitly at the point of reliance** (`architecture/memory-canonical-governance.md` §6.7). A model output whose sensitivity to this date is not disclosed has lost the assumption, and the loss is invisible in the output.

## The failure this exemplar names
The assumption's disappearance is never a decision anyone makes. It happens when the date has been in the model long enough that everyone has stopped seeing it as an input.
