# Exemplar 2 — A canonical promotion, and the four records it touches

Status: PROPOSED — Phase 10 exemplar storage record
Inherits: `standard.storage.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that promotion is recorded in one transaction across the objects that make it meaningful — and that storing the record is not what promoted it.

## What happened

A knowledge claim was promoted to canonical under Phase 8's governed path, on the authority of a Decision Record produced by an eligible human exercising a carded Phase 7 Right.

## The four records, committed as one transaction

| Domain | Record | Content |
|---|---|---|
| `knowledge` | `claim.settlement_basis_2026` version 4 | Status moves to canonical; version 4 is the promoted version |
| `knowledge` | Canonical history entry | Appended: version 4 is current canonical; version 3 is linked as superseded and **remains readable** |
| `decision` | `decision_record.dr.2026.0417` | **Append-only.** Names the Right exercised, the eligible human, the bounded effect and the expiry |
| `audit` | Audit event `ev.9c14` | Change class `transition`; subject `claim.settlement_basis_2026` v3 → v4; **field 7 carries `decision_record.dr.2026.0417`**; human identity and system identity as two separate fields |

**Consistency boundary 3** of `storage/versioning-and-lineage.md` §5: strong, one transaction. A promotion whose canonical version committed without its history entry would be canonical with no account of what it replaced; one whose Decision Record failed to commit would be an authority claim with no authority.

## What the storage layer did and did not do

| | |
|---|---|
| **Did** | Record the promotion, its authority reference, its lineage and its audit event, atomically |
| **Did not** | Cause the promotion. No column, grant, policy or service account promotes anything |
| **Did not** | Make version 4 true. Canonical is a governance status, not an assertion about the world |
| **Did not** | Remove version 3. It is superseded, linked, and readable as what it was when it was current |

## The reference that had to be a recorded value

`decision_record.dr.2026.0417` cites the claim as **`claim.settlement_basis_2026` version 4** — as a recorded value, not as a pointer to whatever is current.

Eleven months later the claim is at version 7. The Decision Record still reads version 4, which is what was decided about. A pointer would now read version 7 and would appear to say that a human approved something they never saw — the failure `storage/versioning-and-lineage.md` §7 exists to prevent, arriving quietly and looking like correctness.
