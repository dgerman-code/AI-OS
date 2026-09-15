# Idempotency, Versioning and Replay

Status: `PROPOSED` — Phase 16 candidate. Approves nothing, registers nothing.

Requirement 9 of the Phase 16 scope. This document owns the durable-identity rules that keep
one request from acquiring two execution lineages, and keep a replan from rewriting history.

## 1. The identifiers, and what each one is not

| Identifier | Created by | Never |
|---|---|---|
| `request.<id>` | The originating user request | Reused for a different request that merely looks the same |
| `intent.<id>` | Phase 15 P1 | Given Work Plan identity |
| `work_plan.<id>@<v>` | Phase 15 COMPOSE, or MATCH's instance record | Rendered as `workflow.<id>` — see `workflow-resolution-contract.md` |
| `workflow.<id>@<version>` | The approved registry, before Phase 15 ever ran | Created, widened or versioned by planning |
| `execution_basis.<request>.<n>` | Phase 16 preflight | Created by a caller, or edited after issue |
| `run_lineage.<key>` | The store, on the first accepted trigger for an idempotency key | Created twice for one key |
| `workflow_run.<id>` | The **Orchestrator**, under the approved Phase 14 command | Created by Phase 16 |

The extended identity chain from the approved Phase 15 architecture holds unchanged here:

```text
REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK
        != PLANNED WORK ITEM SPEC != WORK ITEM != ROLE != MODEL
        != ORCHESTRATOR != HUMAN AUTHORITY
```

Phase 16 adds exactly one new object to that chain's vicinity — the Execution Basis — and it is
not an authority, not an approval and not a run. It sits between the Work Plan and intake.

## 2. Basis version semantics

A basis is versioned **per request**, not per plan and not globally.

| Rule | Statement |
|---|---|
| IV-1 | `version` starts at 1 for the first basis issued for a request |
| IV-2 | A later basis for the same request takes `previous.version + 1` and sets `supersedes` to the previous basis's ref |
| IV-3 | "Previous" means the **most recently issued** basis for that request, whatever its status — including `STALE` and `BLOCKED` |
| IV-4 | A basis is never edited after issue. `STALE`, `SUPERSEDED` and `BLOCKED` are status transitions on an otherwise immutable record |
| IV-5 | A superseded basis stays readable. Superseding is not deletion; governed history is append-only |

IV-3 is not cosmetic. An earlier draft of the reference store read the *live* basis when
versioning. The moment a basis went `STALE`, the replacement restarted at version 1 with no
`supersedes` link, and the lineage of the replan was simply gone from the record. That is
precisely the history a governed record may not lose, so the store now reads
`latest_basis()` — `implementation/phase-16/store.py`.

## 3. Idempotent reuse

Two things are idempotent, and they are idempotent on different keys.

**Basis issue** is idempotent on `(request_id, planning_digest)`. Re-running preflight on
unchanged material planning inputs returns the existing live basis rather than issuing a second
one. `planning_digest` is `PlannerOutput.material_digest()` — a sha256 over the canonicalised
material fields listed in `change-control-contract.md`, so a presentation-only edit produces
the same digest and therefore the same basis (acceptance scenario 8).

**Trigger acceptance** is idempotent on the handoff idempotency key:

```text
idempotency_key = sha256( scope_id | request_id | material_digest )
```

`ActivationStore.record_trigger` returns `(lineage_id, created)`. A repeat under the same key
returns the first lineage and `created=False`. No second `run_lineage` is minted, and the
builder emits no second `CreateWorkflowRun` (acceptance scenario 9).

The key deliberately excludes the basis version. A basis reissued for the same material inputs
is the same planning state; it must not buy a second lineage.

This is the Phase 16 side of the at-most-once discipline the approved Phase 14 specification
requires across the provider boundary (PO-17, Q-26, P-9x, O-21a). Phase 16 does not restate
those rules and does not weaken them: the trigger is a command submission, and the Orchestrator
remains the sole creator of the run.

## 4. Replay and retry

| Situation | Phase 16 behaviour |
|---|---|
| Same request, same digest, basis live | Return the existing basis; no new lineage |
| Same request, non-material change | Same digest, so the above applies; no new governed plan version |
| Same request, material change | New digest → prior live basis `STALE` → re-preflight → basis v+1 linked by `supersedes` |
| Trigger submitted twice, same key | One lineage, `created=False` on the repeat |
| Trigger rejected (basis not `EXECUTABLE`, or digest mismatch) | Nothing recorded; nothing to replay |

Phase 16 defines **no automatic retry class of its own**. Whether a failed downstream submission
may be retried is decided by the approved Phase 14 retry classification, not here. A Phase 16
trigger that was accepted has already written a lineage record, so it does not satisfy the
approved "no governed record written" condition for `SAFE_AUTOMATIC_RETRY`; re-submission after
acceptance is a `RETRY_REQUIRING_REVALIDATION` case in the approved sense, and revalidation
means re-reading the basis status and digest before resubmitting.

## 5. What a material replan may never do

| # | Never |
|---:|---|
| IV-6 | Mutate a historical basis, trigger record or lineage |
| IV-7 | Reuse a superseded basis ref for the new basis |
| IV-8 | Execute on a `STALE` basis — `build_trigger` refuses any basis not `EXECUTABLE` |
| IV-9 | Carry a digest that disagrees with the planner output it claims to describe — `build_trigger` recomputes and compares |
| IV-10 | Silently rebase an in-flight run. Phase 16 stops at the trigger; what an already-created run does about a superseded basis is the Orchestrator's, and is named as an open dependency in `po-4-and-po-12-closure.md` |

IV-10 is a real limit, not a formality. Phase 16 can guarantee that no **new** execution starts
from stale planning. It cannot reach into a run the Orchestrator already created.
