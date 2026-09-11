# Exemplar 3 — Financial calculation with source lineage

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** what binding inputs by version does, and why a calculation can go stale without anyone touching it.

## Identity
- Knowledge ID: `knowledge.debt_service_cover_ratio.project_alpha`
- Version: 4
- Subject: minimum DSCR over the loan tenor under the base case
- Scope: `PROJECT/<alpha>`
- Memory class: `SEMANTIC_MEMORY` — **unchanged by promotion**
- Governance state: `CANONICAL` for the project scope
- Origin: `HUMAN_ORIGIN`
- Sensitivity: `CONFIDENTIAL`

## Epistemic type / governance state
`CALCULATION` + `CANONICAL`. A promoted calculation is still a calculation: as good as its inputs, its method, and nothing else.

## Bound inputs — the load-bearing part
| Input | Bound at | Type |
|---|---|---|
| Tariff assumption | v3 | `ASSUMPTION` |
| Capex estimate | v7 | `FACT_CLAIM`, quantity-surveyed |
| Financing terms | v2 | `FACT_CLAIM`, term-sheet evidenced |
| Availability profile | v5 | `INFERENCE` from operating data |

Each is bound **by version**, not by name. "The current tariff assumption" is not an input binding; it is a promise to be surprised later.

## Transformation lineage
Currency conversion at a stated rate and date; annualisation; real-to-nominal rebasing. Three steps, each recorded, because each is a point where one number silently becomes a different number and the difference is invisible in the result.

## What happens when an input changes
When tariff assumption v3 is superseded by v4, the refresh trigger fires and this record becomes **stale, not false** (`knowledge/sensitivity-and-retention-model.md` §3). Its value was correct on v3 and remains correctly derived from v3.

What resolves it is **re-derivation, not re-approval.** No authority can revalidate a calculation whose inputs have moved; approving it again would restate a number nobody recomputed. At Enhanced Decision-Grade the stale calculation is **blocking** — it cannot support a lender submission until re-derived.

## What promotion did not do
It did not make the DSCR true. It made it the project's governed figure, on those inputs at those versions, until one of them moves.
