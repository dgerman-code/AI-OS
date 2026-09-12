# Provider and Runtime Independence

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. The architecture is not an engine

Everything in Phase 11 is expressed in terms of **workflow semantics, state, dependencies, gates and governed references**. None of it names a queue, a worker pool, a scheduler, a temporal engine, a state-machine service or an event bus — not because one will not eventually exist, but because the governance must survive replacing it.

**The test, stated so it can be applied:** if the execution engine were replaced tomorrow, would any governance semantic in Phases 1–11 change? If yes, the semantic has leaked into the engine and is defective.

## 2. Five adapter boundaries

| Surface | Portable — part of this architecture | Engine-specific, behind the boundary |
|---|---|---|
| **Execution engine** | Run, stage and activity semantics; the four state axes; transitions | Work distribution, worker pools, leases, heartbeats |
| **Scheduling** | Dependency kinds and satisfaction rules; the scheduled-versus-requested distinction | Timers, cron mechanics, backoff curves |
| **Messaging** | Idempotency keys, correlation and causation identifiers, at-least-once classification | Brokers, topics, delivery mechanics, ordering guarantees |
| **Persistence** | Phase 10's source-of-truth matrix and audit model, unchanged | Connection handling, pooling, client libraries |
| **Observability** | The execution event and its 13 fields | Metrics backends, tracing systems, log shipping |

## 3. What may never sit behind a boundary

An adapter boundary isolates a **mechanism**. It never isolates a **meaning**:

- no engine decides whether a gate applies;
- no queue decides whether a retry is safe — the step's declared retry class does;
- no broker's delivery guarantee becomes a governance guarantee, which is why exactly-once is denied in `orchestration/retry-replay-idempotency.md` §2 rather than delegated to a vendor's claim;
- no scheduler decides stage order — the workflow definition does;
- no observability backend becomes evidence, because an operational log is not evidence.

## 4. Determinism, bounded honestly

**Deterministic**, given the same definitions, versions, inputs and governed state: which stage is next; which dependency is unmet; which gate applies; which retry class a failure falls into; which race outcome applies; which stop condition fires.

**Not deterministic, and not claimed to be**: the content a model produces; the outcome a human reaches; the timing or availability of an external system; the wall-clock interleaving of independent activities.

The line matters because a claim of end-to-end determinism would be false, and the parts that *are* deterministic are exactly the parts an auditor needs to be able to re-derive.

## 5. No engine in this repository

Phase 11 creates no orchestrator, no queue, no worker, no scheduler, no event bus, no state-machine service, no SQL, no migration, no API, no SDK, no agent and no secret. It defines what such a thing would have to honour, and the validator scans every Phase 11 artifact to confirm none of it was written.
