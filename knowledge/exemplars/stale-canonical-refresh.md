# Exemplar 8 — Stale canonical item requiring refresh before decision-grade use

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** that staleness is a property of the use, not the item, and that stale is not false.

## Identity
- Canonical ID: `knowledge.construction_cost_index.organisation`
- Version: 6 — `CANONICAL`, `STALE`
- Subject: the construction cost index basis used for estimate escalation
- Scope: `ORGANISATION/<entity>`
- Sensitivity: `INTERNAL`

## Status
Canonical, current version, **past its freshness expectation**. Its review-by date has passed and the publisher has issued a newer series the entity has not yet adopted.

## The same item, two answers
| Use | Freshness verdict |
|---|---|
| Internal orientation, early-stage sizing, sensitivity ranges | `STALE_BUT_USABLE` — usable, **with the staleness disclosed at the point of use** |
| Enhanced Decision-Grade: a lender submission, a board investment paper, an external commitment | `STALE_AND_BLOCKING` — **refresh before use** |

Nothing about the index changed between those two rows. **The use changed** (`architecture/memory-canonical-governance.md` §9). At Enhanced Decision-Grade stale is blocking; at Routine it is a disclosure obligation.

## Stale is not false
The index is not wrong. Its **currency is unverified** — nobody has checked whether the newer series moves it, and the difference may be immaterial. Treating staleness as falsity discards correct knowledge exactly as reliably as treating it as currency accepts wrong knowledge, and an organisation that does the former loses its institutional memory a little at a time.

## Nor is it in conflict
The newer published series is **not** a `SOURCE_CONFLICT` until someone establishes that it says something incompatible. An unexamined newer source is a refresh trigger, not a contradiction — and raising it as a conflict would block work that nothing yet contradicts.

## What refresh is
Re-derivation against the current series, then **promotion of version 7**, superseding version 6 automatically. It is not re-approval of version 6: authority cannot make an unverified figure current, and approving it again would restate a number nobody re-checked.

If the newer series turns out to leave the basis unchanged, version 7 is promoted anyway — same content, new evidence, new effective period. **A refreshed statement is a new version even when the number does not move**, because what changed is what is known about it.
