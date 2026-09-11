# Exemplar 4 — Conflicting external sources blocking canonical promotion

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** that conflict blocks promotion, that recency does not resolve it, and that the losing source survives the resolution.

## Identity
- Knowledge ID: `knowledge.regional_demand_baseline.project_alpha`
- Version: 1 — **candidate, not promoted**
- Subject: the regional demand baseline for the appraisal period
- Scope: `PROJECT/<alpha>`
- Memory class: `SEMANTIC_MEMORY`
- Origin: `HUMAN_ORIGIN`
- Sensitivity: `INTERNAL`

## Epistemic type / governance state
`FACT_CLAIM` + `REVIEWED`, carrying an open `SOURCE_CONFLICT` flag. It stops here.

## The conflict
Two external sources give materially different baselines: a national statistical release, and a sector association series published eighteen months later on a different definitional basis.

## What is not permitted as a resolution
- **Taking the later one.** Recency bears on currency, not correctness — and the later source is the one with the unexplained definitional change.
- **Taking the more authoritative publisher.** Authority is not evidence. The statistical office is not automatically right about a sector definition it does not use.
- **Averaging them.** Two incompatible definitions do not average into a third; the result is a number with no basis at all, which is worse than either input because it can no longer be traced.
- **Promoting with the conflict noted.** The conflict is **material** — the claim *is* the number, so the statement depends entirely on the contested point — and a material unresolved conflict blocks promotion outright (`standard.knowledge.common_constraints` §9). Noting it is not resolving it.

**Materiality here is a determination, not an impression**, and it is attributable: the Role that owns the demand position assessed it and the assessment is reviewable. Had the two sources disagreed about something the appraisal does not rest on, the conflict would stay visible and block nothing — at any criticality band.

## What the conflict actually is
On examination it is close to an `IDENTITY_CONFLICT`: the two series may not be measuring the same thing. That question is prior to which number is right, and answering "which is correct" first would merge two different quantities.

## Resolution route
A Role-owned professional conclusion — is this one quantity or two? — checked by review. **A Decision Right cannot perform this**, because it decides what the organisation does, never which source is accurate.

## After resolution
The prevailing interpretation is recorded **with its reasoning**. The set-aside series stays linked and readable, with the definitional difference stated. It is not deleted, downgraded or hidden — and if the appraisal is later challenged, the retained series is what shows the question was examined rather than missed.
