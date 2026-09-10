# Sensitivity, Retention and Freshness Model

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

This file carries §9 and §10 of the Phase 8 scope — lifecycle controls and restricted-knowledge handling — kept separate from `scope-isolation-and-transfer.md` because sensitivity is an **independent axis**, not a scope, and conflating the two is how "confidential" comes to mean "belongs to that project".

## 1. Sensitivity classes

Metadata-level handling classes. What a runtime must later honour; not an access-control design.

| Class | What it marks |
|---|---|
| `PUBLIC` | Already outside the entity, or intended to be |
| `INTERNAL` | Ordinary internal material |
| `CONFIDENTIAL` | Restricted to those with a working need |
| `RESTRICTED` | Highly sensitive; handling constrained beyond need-to-know |
| `PERSONAL_DATA` | Identifies or relates to an identifiable person; carries obligations independent of every other class here |
| `PRIVILEGED` | Legally privileged; **privilege can be lost by handling**, which no other class on this list can be |
| `TRADE_SECRET` | Commercially sensitive, deriving value from not being known |
| `SECURITY_SENSITIVE` | Disclosure of which would weaken a control |
| `THIRD_PARTY_RESTRICTED` | Held under someone else's terms — the entity's own classification does not govern it |

An item may carry several. Where classes conflict, the **most restrictive handling applies**, and a restriction arising from `THIRD_PARTY_RESTRICTED` or `PRIVILEGED` cannot be relaxed by an internal decision at all.

## 2. Sensitivity is orthogonal to everything else

| Axis | Answers |
|---|---|
| Sensitivity | How may this be handled? |
| Scope | Where does this govern? |
| Governance state | How far has governance taken it? |
| Memory class | What is it for? |

**Canonical status implies no visibility.** A `RESTRICTED` canonical statement is the organisation's governed position *and* narrowly handled, and neither property softens the other. Nor does the converse hold: being widely visible confers no status, and a `PUBLIC` classification is not an approval, a review or a promotion.

Sensitivity is **not** a scope. Two projects' confidential material is not one pool because both are confidential.

Classification is **carried through the whole lineage**. Evidence extracted from a `PERSONAL_DATA` source is `PERSONAL_DATA`; a summary of privileged material is privileged; and an aggregate can be more sensitive than its parts. Declassification is a governed act with a reason, never a side effect of quotation, summarisation, aggregation or reuse.

## 3. Freshness and staleness

| Control | Meaning |
|---|---|
| **Freshness expectation** | How long this kind of item is expected to remain current — declared on the record, not inferred |
| `FRESH` | Within the expectation |
| `STALE_BUT_USABLE` | Past it, still usable, **with the staleness disclosed at the point of use** |
| `STALE_AND_BLOCKING` | Past it, and not usable for the current purpose until refreshed |
| **Review-by** | A date at which the item must be re-examined |
| **Expiry** | A date after which it no longer carries its status |
| **Refresh trigger** | An event that fires staleness before any date — a bound input superseded, a source reissued, a conflict raised, a scope condition changed |

**What makes staleness blocking is the use, not the item.** The same canonical figure may be `STALE_BUT_USABLE` for internal orientation and `STALE_AND_BLOCKING` for a decision-grade external submission. The band decides (`architecture/memory-canonical-governance.md` §9), and a decision-grade use of a stale canonical item requires refresh first.

**Stale is not false.** A stale item is one whose currency is unverified; it has not been contradicted, and treating staleness as falsity discards correct knowledge as reliably as treating it as currency accepts wrong knowledge.

## 4. End states, four different things

| | What it means | What survives |
|---|---|---|
| **Superseded** | A successor version governs now | Content intact, readable, linked to its successor |
| **Expired** | The status lapsed at a stated point | Everything — expiry ends currency, not existence |
| **Retracted** | Withdrawn from reliance, with a reason, no successor | Everything, plus the reason and the resulting gap |
| **Archived** | Moved out of active use | Everything — archival is a handling change, not a status |

**stale ≠ false. expired ≠ deleted. superseded ≠ erased. retracted ≠ forgotten. archived ≠ gone.**

## 5. Retention holds and deletion eligibility

- A **retention hold** — legal, contractual, regulatory or funder-imposed — makes an item ineligible for deletion **regardless of every other lifecycle control**. Expiry, supersession, retraction and archival all leave the hold intact.
- **Deletion eligibility is a conclusion, not a default.** An item becomes eligible only when no hold applies, no obligation requires it, and nothing canonical or audit-bearing depends on it.
- **Audit memory and the provenance of canonical statements are not deletion candidates** in the ordinary course. Deleting the evidence trail of a decision destroys the decision's accountability while leaving the decision in place.
- **`PERSONAL_DATA` may carry an erasure obligation that runs the other way**, and where an erasure duty and a retention hold both apply the conflict is a governed matter for legal authority — **not one this architecture resolves, and not one a runtime may resolve by policy default**.

No retention job, schedule, sweep or lifecycle automation is specified here.

## 6. Status

`PROPOSED`. Defines no access control, no encryption, no classification engine, no retention automation and no runtime.
