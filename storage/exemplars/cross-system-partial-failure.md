# Exemplar 3 — A partial write across two systems, and the reconciliation that is not a repair

Status: PROPOSED — Phase 10 exemplar storage record
Inherits: `standard.storage.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that an object upload and a database transaction are two acts, that the declared commit order makes the failure detectable, and that neither half is ever completed by inventing the other.

## What happened

An evidence document was uploaded for a review. The upload succeeded. The metadata transaction did not: the database was unavailable for ninety seconds, spanning the commit.

| Step | Declared order | Outcome |
|---:|---|---|
| 1 | Upload the object | **Succeeded** — `bkt.governed.eu` / `project-beta/evidence/` / `obj.3ad81f` @ version 1 |
| 2 | Verify the returned content hash | **Succeeded** — matched |
| 3 | Commit the artifact metadata record | **Failed** — failure mode 1, database unavailable |

## The resulting state, named

**An orphaned object.** Not an artifact, not a partial artifact, not an artifact pending metadata — bytes that no record refers to. Because nothing reads an object the registry does not know about (standard §18), the upload was never visible to anything.

## What the reconciliation sweep did

| Finding | Action | Why not otherwise |
|---|---|---|
| Object present, no artifact record references it | **QUARANTINE**, then expire under its class | It is failure mode 2. The object is **never adopted by a later record**: adoption would attach provenance, producer, scope and labels that nobody asserted, and they would then look asserted |
| Nothing else | Nothing | There is no record to repair, so there is no repair |

**The writer retried.** The retry produced a **new** upload and a **new** artifact record, committed together in the declared order. The retried artifact's content hash equals the orphan's, and that changes nothing: a matching hash is a deduplication hint, not an identity claim (`storage/artifact-object-model.md` §4).

## The failure that would have been worse

Had the commit order been reversed — metadata first, object after — the failure would have produced an **artifact record with no bytes**, which is failure mode 3: still detectable, but detectable only by a sweep or a read, and visible in the meantime as a real artifact. The chosen order makes the common interruption produce the invisible failure rather than the visible-and-wrong one.

## What was not done

- The metadata was not committed "as soon as the database returned", because by then it would have been a record asserting a state nobody had verified.
- The orphan was not linked to the retried record.
- No distributed transaction was attempted across the two systems, because there is none to attempt (standard §17), and a design that implied one would have been a claim the architecture cannot honour.
