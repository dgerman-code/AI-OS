# Exemplar 6 — Resumed after six weeks, into constraints that had moved

Status: PROPOSED — Phase 11 exemplar execution run
Inherits: `standard.orchestration.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that a resume compares rather than assumes — definitions, freshness, assignments and classification are all re-checked at the point of use, and a run resumes into the constraints that hold **now**.

## The run

`run.2026.regulatory_filing.0019` · `workflow.regulatory_filing` @ v8 · scope `project.iota` · criticality **Enhanced Decision-Grade**.

Paused at stage 6 on 3 February by `intervention.0455` — the counterparty needed time. Resumed on 17 March by `intervention.0781`.

## What the checkpoint recorded, and what resume compared

| Check | At the checkpoint | At resume | Outcome |
|---|---|---|---|
| **Workflow definition** | `workflow.regulatory_filing` @ v8 | v9 now approved | **Stays on v8.** The newer version is recorded as a **notice**, not applied — upgrading mid-run would mean the execution ran neither version |
| **Orchestrator Policy** | `orch_policy.filing` @ v2 | v2 | Unchanged |
| **Evidence freshness** | `CURRENT_FOR_USE` | **`STALE_AND_BLOCKING`** at this band | **`BLOCKED`** |
| **Artifact integrity** | Present, hash verified | Present, hash verified | Continue |
| **Assignment eligibility** | Valid | The stage-7 reviewer had since performed related work on the same subject | **Invalidated and re-attempted**, recorded |
| **Sensitivity classification** | {`CONFIDENTIAL`} | **{`CONFIDENTIAL`, `THIRD_PARTY_RESTRICTED`}** after a governed reclassification | Constraints tightened; the stage-5 Routing Decision would **not** be eligible today |

## What happened

Run: `PAUSED` → **`BLOCKED`**, posture `GATE_UNSATISFIED`, wait reason recorded with its subject — the stale evidence reference.

Three consequences, none of them automatic:

1. **The evidence must be refreshed** through Phase 8's governed path. Freshness is **use-specific and evaluated at the point of use**: the same evidence was legitimately current in February and is blocking in March, and nothing cached the February verdict.
2. **The stage-7 assignment was invalidated**, not honoured on the grounds that it was valid when made. A new Assignment Attempt was created; the prior attempt remains recorded with its outcome.
3. **The stage-5 output is re-evaluated against the new labels.** The reclassification added `THIRD_PARTY_RESTRICTED`, whose obligations arise from someone else's terms. The deployment used in February supported {`CONFIDENTIAL`} — **support for one label implies support for no other**, and the subset test fails today. Re-running stage 5 requires a fresh routing request under the current constraints.

## What did not happen

- **The run did not resume into February's constraints.** A resume is not a time machine; it is the reintroduction of stale state into the present.
- **The stage-5 output was not grandfathered.** "It was compliant when produced" is true and is not a reason to continue using it under obligations that now apply.
- **The newer workflow version was not silently adopted**, and the older one was not silently declared stale.

## What this shows

Long duration is not a special case needing special rules — it is the ordinary case with enough elapsed time for the ordinary rules to bite. **Everything a resume checks is something the architecture already required to be checked at the point of use**; the six weeks only make it visible.
