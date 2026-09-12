# Phase 11 — Orchestrator Architecture Foundation Prompt

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`
Starting baseline: Phase 10 human approval commit `eb789263b4dcc7c4a966a19359522173c57ac8ec`
Phase 10 approved architecture baseline: `b184b074c1de5416fcfc56036ee033f6e52fed46`

## Mission

Create the **PROPOSED Phase 11 Orchestrator Architecture foundation** for AI-OS.

Phase 11 answers a bounded question:

> How does AI-OS coordinate an execution from trigger to completion while preserving all previously approved boundaries around roles, workflows, handoffs, review, decisions, knowledge, model routing, storage, human authority, provenance, scope and failure handling?

This is an architecture/governance phase. It is **not** runtime implementation.

## Non-negotiable inherited separations

Preserve all approved Phase 1–10 semantics. At minimum, explicitly preserve:

`ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE != ROUTER != ORCHESTRATOR != WORKFLOW != WORKFLOW RUN != TASK != HANDOFF != REVIEW PROFILE != REVIEW INSTANCE != DECISION RIGHT != DECISION RECORD != KNOWLEDGE != CANONICAL RECORD != ARTIFACT != STORAGE RECORD != RUNTIME EVENT != CREDENTIAL != HUMAN AUTHORITY`

The orchestrator:

- does not become a Role;
- does not become an agent persona;
- does not become the Model Router;
- does not become a Decision Right holder;
- does not approve, waive, canonicalize, sign, publish or accept risk by itself;
- does not convert model confidence into authority;
- does not silently resolve material findings, conflicts, UNKNOWN states, or stale evidence;
- does not redefine Phase 5 Workflow semantics;
- does not redefine Phase 6 Handoff/Review semantics;
- does not redefine Phase 7 Decision Rights;
- does not redefine Phase 8 knowledge/canonical governance;
- does not redefine Phase 9 Model Registry/Router semantics;
- does not redefine Phase 10 source-of-truth/storage semantics.

## Scope boundary

### In scope

Define the architecture for:

1. Orchestrator identity and responsibility boundary.
2. Workflow-run / execution-run identity.
3. Trigger intake and validation.
4. Scope binding and context isolation.
5. Stage/activity scheduling semantics.
6. Dependency handling.
7. Role assignment activation without turning roles into agents.
8. Skill/specialisation capability checks.
9. Review and human-gate activation.
10. Decision Right gate invocation.
11. Model-router invocation boundary.
12. Handoff package movement.
13. State-machine transitions.
14. Pause / resume / retry / timeout / cancellation / termination / rework / escalation semantics.
15. Idempotency and duplicate-run handling.
16. Concurrency and race-condition governance.
17. Long-running execution semantics.
18. Partial failure and compensation boundaries.
19. Event/correlation/audit requirements.
20. Recovery/replay/resume rules.
21. Manual intervention boundaries.
22. Orchestrator policy vs workflow definition separation.
23. Execution determinism / reproducibility requirements.
24. Provider/runtime independence.
25. Validation harness and synthetic exemplars.

### Explicitly out of scope

Do **not** implement or design concrete production runtime infrastructure:

- no live orchestrator;
- no queue, worker, scheduler, temporal engine, state machine service or event bus implementation;
- no Supabase schema/table/RLS deployment;
- no SQL DDL or migrations;
- no provider SDK;
- no model API calls;
- no agents;
- no prompts-as-runtime;
- no RAG/embedding system;
- no secrets/credentials;
- no billing/telemetry backend;
- no CI/CD deployment;
- no UI;
- no IAM implementation;
- no production retry engine;
- no auto-failover implementation;
- no real Decision Right assignments;
- no real Model/Provider/Deployment profiles;
- no PR.

## Required architectural position

The orchestrator is a **coordination control plane**, not a source of truth for governed semantics.

It may:

- read approved definitions and current governed state;
- instantiate bounded execution records;
- activate already-defined workflow stages;
- request role-capable work;
- invoke the model router where a model execution is permitted;
- request reviews;
- request Decision Right exercise;
- pause while waiting on humans or governed prerequisites;
- carry open items forward only where upstream semantics permit;
- record execution state and correlation metadata;
- retry only where retry is explicitly safe;
- escalate where continuation is not allowed.

It may **not**:

- invent authority;
- infer approval from completion;
- infer role competence from model output;
- turn a model result into a reviewed/approved/canonical result;
- rewrite governed history;
- lower sensitivity/residency constraints;
- weaken materiality rules;
- bypass required review or decision gates;
- auto-accept risk;
- silently substitute one Decision Right for another;
- silently substitute one Review Profile for another;
- silently substitute one model/deployment where Phase 9 constraints disallow it;
- silently downgrade from governed artifact to runtime state;
- use operational logs as governance evidence.

## Required architecture artifacts

Create a coherent Phase 11 package. Use clear file names under `orchestration/`, `architecture/`, `reviews/`, and `validation/`.

At minimum include:

1. `architecture/orchestrator-architecture.md`
2. `orchestration/_standards/common-orchestrator-governance-constraints.md`
3. `orchestration/execution-run-model.md`
4. `orchestration/state-machine-and-transitions.md`
5. `orchestration/scheduling-and-dependency-model.md`
6. `orchestration/human-gate-and-decision-invocation.md`
7. `orchestration/model-router-invocation-boundary.md`
8. `orchestration/retry-replay-idempotency.md`
9. `orchestration/concurrency-and-race-governance.md`
10. `orchestration/failure-escalation-recovery.md`
11. `orchestration/manual-intervention-boundary.md`
12. `orchestration/execution-audit-and-provenance.md`
13. `orchestration/provider-runtime-independence.md`
14. three templates under `orchestration/_templates/`
15. at least five synthetic exemplars under `orchestration/exemplars/`
16. `reviews/phase-11-foundation-self-check.md`
17. `validation/phase_11_validation.py`
18. update `validation/README.md`

You may add supporting documents if genuinely useful, but avoid architecture sprawl.

## Required identity model

Define stable identities for at least:

- Orchestrator Policy Definition
- Execution Run
- Workflow Run binding
- Stage Instance
- Activity Instance
- Work Item
- Assignment Attempt
- Review Request / Review Instance reference
- Decision Request / Decision Record reference
- Model Invocation Request / Routing Decision reference
- Handoff Instance reference
- Human Intervention record
- Retry Attempt
- Resume Point / Checkpoint
- Correlation / Causation identifiers

The architecture must make explicit that runtime instance identifiers are not governance identifiers.

## Scope and context isolation

Preserve the approved scope graph and state how every execution binds to one explicit governed scope.

The orchestrator must never silently cross:

- organisation boundaries;
- project boundaries;
- programme/portfolio boundaries;
- product/service boundaries;
- operational workstream boundaries;
- PERSONAL scope boundaries.

Any cross-scope transfer must use an explicit approved boundary mechanism inherited from previous phases.

## State machine

Define a finite, explicit execution state model. Avoid one giant status enum if orthogonal axes are more correct.

At minimum address:

- CREATED
- VALIDATING
- READY
- RUNNING
- WAITING_FOR_DEPENDENCY
- WAITING_FOR_REVIEW
- WAITING_FOR_DECISION
- WAITING_FOR_HUMAN
- PAUSED
- RETRY_PENDING
- REWORK_REQUIRED
- BLOCKED
- ESCALATED
- COMPLETED
- COMPLETED_WITH_OPEN_ITEMS where upstream semantics permit
- CANCELLED
- TERMINATED
- FAILED
- SUPERSEDED / STALE only if semantically justified

Do not conflate workflow-stage completion with approval.

## Dependency semantics

Define dependency types such as:

- hard prerequisite;
- review prerequisite;
- decision prerequisite;
- data/evidence prerequisite;
- artifact prerequisite;
- external-system prerequisite;
- timing prerequisite;
- conditional branch prerequisite.

A dependency graph must be acyclic unless a bounded rework loop is explicitly modeled as a loop construct rather than hidden cycle.

## Scheduling semantics

Define what the orchestrator is allowed to schedule and what it may only request.

Distinguish:

- scheduling a machine-executable activity;
- requesting human work;
- requesting review;
- requesting Decision Right exercise;
- invoking the router;
- waiting for external events.

Human authority must never be represented as merely another worker queue.

## Role activation

Roles remain reusable profiles, not persistent agents.

Define an assignment envelope that can bind:

- role ID;
- required skill/specialisation constraints;
- scope;
- task/activity;
- criticality;
- required independence;
- human vs model-executable eligibility;
- review/decision restrictions;
- provenance and assignment reason.

Do not create junior/middle/senior role variants.

## Model router boundary

The orchestrator may submit a routing request; the router makes a Routing Decision under Phase 9.

The orchestrator must not:

- choose a provider endpoint directly when routing policy applies;
- rewrite routing constraints;
- equate model result with completion of governed review;
- retry by silently switching model families where independence constraints would be violated.

Define how routing decisions are recorded and referenced in execution history.

## Review and Decision Right invocation

Review and decision gates must remain separate.

The orchestrator may detect that a gate is required and create/request the corresponding governed instance.

It cannot:

- self-satisfy a review;
- self-exercise a Decision Right;
- mark a finding resolved merely because work continued;
- turn a gate timeout into an implicit approval;
- collapse DEFER/ESCALATE into APPROVE;
- treat absence of a Decision Right as permission.

If no applicable Decision Right exists, preserve Phase 9/7 behavior: block/escalate rather than invent one.

## Retry, replay, idempotency

Define explicit categories:

- safe automatic retry;
- retry requiring revalidation;
- retry requiring human acknowledgement;
- non-retryable governed act;
- replayable read-only step;
- non-replayable external side effect;
- exactly-once not guaranteed vs idempotent-at-least-once semantics.

Never claim global exactly-once unless the architecture can actually prove it.

Decision Records, approvals, signatures, external publication, contract commitments, risk acceptance, purge, destructive migration and other authority-bearing acts must never be duplicated by blind replay.

## Concurrency and race governance

Address at minimum:

- duplicate trigger;
- double stage start;
- concurrent edits to governed state;
- stale assignment result;
- review result arriving after supersession;
- decision result arriving after cancellation;
- two workers claiming same work item;
- model result arriving after run reclassification;
- resumed run vs late retry;
- human intervention vs automated continuation race.

Define which events BLOCK, which are ignored as stale, which become superseded, and which require reconciliation.

## Failure, pause, cancellation and termination

Preserve the Phase 5 distinction between completion, block, rework, escalation and cancellation.

Define explicit semantics for:

- PAUSE vs BLOCK;
- CANCEL vs TERMINATE;
- RETRY vs REWORK;
- ESCALATE vs HUMAN REVIEW;
- FAIL vs BLOCKED;
- SUPERSEDE vs CANCEL;
- compensation vs rollback.

No failure handling may silently weaken governance constraints.

## Manual intervention

Define a first-class Human Intervention Record.

Manual intervention must be attributable and bounded. It may:

- resume;
- pause;
- cancel;
- reassign;
- approve a permitted operational exception where a valid Decision Right exists;
- supply missing evidence;
- request rework.

It must not create authority merely because an administrator performed it.

## Audit and provenance

Define append-only execution-event requirements and their relationship to Phase 10 audit events.

Keep separate:

- operational runtime event;
- execution event;
- audit event;
- Decision Record;
- Review result;
- Routing Decision;
- knowledge provenance;
- Git architecture history.

A historical execution must reconstruct which governed definitions and versions it used.

## Human control / stop conditions

Define when the orchestrator must stop and wait for a human or governed authority.

Examples:

- missing applicable Decision Right;
- material unresolved conflict;
- review NOT_SATISFIED;
- stale/expired blocking evidence;
- scope mismatch;
- sensitivity/residency violation;
- destructive action without authority;
- ambiguous identity/version;
- failed integrity check;
- unknown model eligibility;
- cancellation/termination race;
- external side-effect uncertainty.

## Criticality

Inherit project criticality and Enhanced Decision-Grade Project Mode.

The orchestrator may enforce stricter review/segregation/reproducibility requirements for critical work, but may not reduce approved requirements for lower-criticality work without an explicit policy basis.

## Exemplars

Create at least five synthetic exemplars covering distinct hard cases. Include at minimum:

1. A normal multi-stage workflow with model-assisted work, review, and human decision gate.
2. A critical project where reviewer/model independence matters.
3. A partial failure after object creation but before governed metadata completion.
4. A cancellation racing with a late model/review result.
5. A missing Decision Right that must block/escalate instead of being inferred.

Prefer 6–8 exemplars if useful, but keep them synthetic and PROPOSED.

## Validation harness

Create a deterministic offline validator in `validation/phase_11_validation.py`.

It must:

- parse structures, not merely search strings;
- derive inventory counts from source artifacts;
- fail on stale counts;
- fail on collapsed identities;
- fail if orchestrator can approve/review/canonicalize/accept risk;
- fail if router and orchestrator collapse;
- fail if role and agent instance collapse;
- fail if a missing Decision Right can default to continuation;
- fail if review timeout implies approval;
- fail if retry can replay authority-bearing acts blindly;
- fail if scope crossing is implicit;
- fail if operational logs become governance evidence;
- fail if sensitive/residency constraints may be weakened;
- fail if exactly-once is asserted without bounded proof;
- fail if replay/late-result race handling is absent;
- fail if the validator contains obvious vacuity such as `or True`;
- preserve Phase 10, Phase 9 and Phase 8 validators as regressions.

Add controlled adversarial probes and report them in the self-check. Include at least ten mutations that are expected to produce non-zero exit.

## Open questions classification

Maintain an explicit table of unresolved questions with exactly one of:

- `RESOLVED IN FOUNDATION`
- `SAFE TO DEFER WITH EXPLICIT RULE`
- `MUST RESOLVE BEFORE HUMAN APPROVAL`
- `PHASE 12+`
- `IMPLEMENTATION DETAIL`

Do not hide authority, privacy, scope, replay, side-effect, decision or human-control ambiguity behind `implementation detail`.

## Self-check and readiness

The producer self-check must explicitly state that it is not independent review.

Do not claim Phase 11 approved.

Do not create a PR.

End with one of:

- `READY FOR INDEPENDENT PHASE 11 FOUNDATION AUDIT`
- `NOT READY`

## Validation/regression commands

Run at minimum:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

## Commit and push

Commit exactly:

`docs: add Phase 11 Orchestrator foundation`

Push to:

`origin architecture/phase-11-orchestrator`

No PR.

## Required final response

Return sections **A–R exactly**:

### A. PHASE 11 FOUNDATION SUMMARY
### B. ORCHESTRATOR BOUNDARY
### C. EXECUTION-RUN / IDENTITY MODEL
### D. SCOPE / CONTEXT ISOLATION
### E. STATE MACHINE
### F. SCHEDULING / DEPENDENCIES
### G. ROLE / SKILL ACTIVATION
### H. MODEL ROUTER INVOCATION
### I. REVIEW / DECISION / HUMAN GATES
### J. RETRY / REPLAY / IDEMPOTENCY
### K. CONCURRENCY / RACE GOVERNANCE
### L. FAILURE / RECOVERY / MANUAL INTERVENTION
### M. AUDIT / PROVENANCE
### N. OPEN QUESTIONS
### O. VALIDATION
### P. REGRESSION
### Q. COMMIT / PUSH
### R. NEXT STEP
