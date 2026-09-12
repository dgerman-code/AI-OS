# Exemplar 3 — The effect landed, the record did not

Status: PROPOSED — Phase 11 exemplar execution run
Inherits: `standard.orchestration.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that a multi-system step has no distributed transaction, that the declared commit order makes the interruption detectable, and that neither half is ever completed by inventing the other.

## The run

`run.2026.evidence_pack.0208` · `workflow.evidence_assembly` @ v2 · scope `project.zeta` · sensitivity {`CONFIDENTIAL`, `PERSONAL_DATA`}.

## The step

Stage 4 produced an evidence bundle and stored it. The step is multi-system, so it declares a commit order, a reconciliation owner and a compensating outcome.

| Step | Declared order | Outcome |
|---:|---|---|
| 1 | Upload the object | **Succeeded** |
| 2 | Verify the returned content hash | **Succeeded** |
| 3 | Commit the artifact metadata record | **Failed** — the database was unavailable across the commit |
| 4 | Record the execution event referencing the artifact | Never reached |

## The resulting state, named

**An orphaned object.** Not an artifact, not a partial artifact — bytes no record refers to. Nothing reads an object the registry does not know about, so the upload was never visible to anything, and the run did not proceed on the assumption that it had worked.

Run state: `RUNNING` → **`RETRY_PENDING`**, then `RUNNING` after a class-2 retry.

## What reconciliation did, and did not

| Finding | Action | Why not otherwise |
|---|---|---|
| Object present, no artifact record | **`RECONCILE`** → quarantine, then expire under its class | Adoption by a later record would attach provenance, producer, scope and labels nobody asserted — and they would then look asserted |
| Nothing else | Nothing | There is no record to repair, so there is no repair |

The retry was class 2, `RETRY_REQUIRING_REVALIDATION`: preconditions, evidence freshness, scope, sensitivity **and assignment eligibility** were re-checked before re-execution rather than assumed from the first attempt. It produced a **new** upload and a **new** artifact record, committed in the declared order. The new object's hash equals the orphan's, and that changes nothing — a matching hash is a deduplication hint, not an identity claim.

## The variant that would have escalated instead

Had step 1 been an **external** effect rather than an internal upload — a notification sent, a filing submitted — the orphan could not be quarantined, because it is not ours to quarantine. That path is `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT`: the run would have **`BLOCKED`** and **`ESCALATED`**, and recovery would be **compensation** — a new, recorded, separately-authorised act — rather than a retry.

## What this shows

The commit order is chosen so that the common interruption produces the **invisible** failure rather than the **visible-and-wrong** one. Had metadata been committed first, the same outage would have left an artifact record with no bytes: still detectable, but visible in the meantime as a real artifact that things could cite.
