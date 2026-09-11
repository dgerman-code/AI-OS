# Exemplar 8 — Stale canonical item requiring refresh before decision-grade use

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** that staleness is a property of the use, not the item, and that stale is not false.

## Identity
- Canonical ID: `knowledge.construction_cost_index.organisation`
- Version: 6 — governance state `CANONICAL`, item condition `PAST_REFRESH_INTERVAL`
- Memory class: `SEMANTIC_MEMORY`
- Applicability mode: `INHERITABLE_TO_DESCENDANTS`
- Origin: `EXTERNAL_ORIGIN`
- Subject: the construction cost index basis used for estimate escalation
- Scope: `ORGANISATION/<entity>`
- Sensitivity: `INTERNAL`

## Item-level temporal facts — what the record stores

| Field | Value |
|---|---|
| As-of date | The index basis date |
| Last verified / refreshed | At version 6's promotion |
| Expected refresh interval | Per the publisher's release cycle |
| Review-by | **Passed** |
| Expiry | None declared |
| Supersession / withdrawal | None — this is the current version |
| Refresh trigger fired | The publisher issued a newer series |
| Derived condition | **`PAST_REFRESH_INTERVAL`** |

`PAST_REFRESH_INTERVAL` is an **age condition, not a usability verdict**: the currency is unverified. **The record stores no usability label at all**, which is what lets the next section be true.

## The same item, two answers
## The same item, two verdicts, at the same moment

| Use | Use-context verdict |
|---|---|
| Internal orientation, early-stage sizing, sensitivity ranges | `STALE_BUT_USABLE` — usable, **with the staleness disclosed at the point of use** |
| Enhanced Decision-Grade: a lender submission, a board investment paper, an external commitment | `STALE_AND_BLOCKING` — **refresh before use** |

Both verdicts are live **simultaneously**, for two tasks running the same week. Nothing about the index changed between the rows; **the use changed** (`architecture/memory-canonical-governance.md` §9).

This is why neither verdict is written back to the record. A single record-level "current freshness" field would have to pick one and would then be **wrong for the other task** — and whichever it picked would harden into a permanent item label that nobody re-examines. Item facts live on the record; verdicts live at the point of use.

## Stale is not false
The index is not wrong. Its **currency is unverified** — nobody has checked whether the newer series moves it, and the difference may be immaterial. Treating staleness as falsity discards correct knowledge exactly as reliably as treating it as currency accepts wrong knowledge, and an organisation that does the former loses its institutional memory a little at a time.

## Nor is it `EXPIRED_FOR_USE`

No expiry was declared, so no use reaches that verdict. **Review-by, expiry, refresh trigger and use verdict are four distinct things**: the review-by passing is what produced `PAST_REFRESH_INTERVAL`; the publisher's release is what fired the refresh trigger; neither is an expiry, and neither is by itself a verdict about any use.

## Nor is it in conflict
The newer published series is **not** a `SOURCE_CONFLICT` until someone establishes that it says something incompatible. An unexamined newer source is a refresh trigger, not a contradiction — and raising it as a conflict would block work that nothing yet contradicts.

## What refresh is
Re-derivation against the current series, then **promotion of version 7**, superseding version 6 automatically. It is not re-approval of version 6: authority cannot make an unverified figure current, and approving it again would restate a number nobody re-checked.

If the newer series turns out to leave the basis unchanged, version 7 is promoted anyway — same content, new evidence, new effective period. **A refreshed statement is a new version even when the number does not move**, because what changed is what is known about it.
