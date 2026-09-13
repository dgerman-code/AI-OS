# Phase 12 — MVP foundation

Status: `PROPOSED` (implementation-equivalent non-approved status).

Phase 12 is the first controlled *implementation* phase of AI-OS. Its claim is narrow and
deliberate:

> the approved Phase 1–11 governance model can be represented and executed in code without
> collapsing any of its boundaries.

Nothing here is a platform. It is a reference implementation small enough to read in one
sitting, whose value is that the rules are **structural** rather than described.

---

## Scope

* explicit typed domain objects for every governed identity the architecture separates;
* a reference orchestrator that coordinates and holds no authority of its own;
* provider and runtime boundaries behind adapters, with in-memory stubs;
* two synthetic workflows — one that completes under governance, one that is stopped by it;
* a deterministic test suite and a deterministic validator.

## Non-scope

None of the following is present, and `validation/phase_12_validation.py` fails if any of it
appears: production Supabase configuration, live database migrations, deployed APIs, cloud
queues or workers, schedulers or event buses, provider SDK coupling in governance objects,
secrets or credentials, live LLM calls, production IAM, RAG or embeddings, autonomous agents,
background daemons, deployment configuration.

The MVP runs in memory, offline, on the standard library.

## Architecture mapping

| Approved object or rule | Where it lives |
|---|---|
| The twenty-one-object separation chain | `domain.SEPARATION_CHAIN` — one frozen type per object, compared by type as well as id |
| Axis A — ten run phases | `domain.RunPhase`, moved only by `Orchestrator._transition` |
| Axis B — six terminal outcomes | `domain.TerminalOutcome` + `TERMINAL_REACHABLE_FROM` |
| Axis C — five wait reasons, never without a subject | `domain.WaitReason`; a `WAITING` transition with no named subject raises |
| Axis D — four governance postures | `domain.GovernancePosture` + `POSTURE_PERMITS_COMPLETION` |
| Approved transition table | `domain.ALLOWED_TRANSITIONS`, reconciled against `orchestration/state-machine-and-transitions.md` by the validator |
| Four gate kinds, seven outcomes, two of which continue | `domain.GateKind`, `GateOutcome`, `CONTINUING_GATE_OUTCOMES` |
| A gate requirement is an identified object, not a `(work_item, kind)` key | `domain.GateRequirement` carries a `GateRequirementRef`; `GateInstance` binds it to one run and one Work Item |
| One admissible evidence type per gate kind | `domain.EVIDENCE_CONTRACT` and `Orchestrator.validate_evidence` |
| `NO_APPLICABLE_DECISION_RIGHT` → BLOCKED + ESCALATED + `AUTHORITY_ABSENT` | `Orchestrator._apply_gate_outcome` |
| Seven retry classes; exactly-once claimed nowhere | `domain.RetryClass`, `AUTOMATICALLY_RETRYABLE`, `NEVER_AUTOMATICALLY_RETRYABLE` |
| Ten races, five outcomes, the late-review / late-Decision asymmetry | `domain.RaceOutcome` and `tests/test_invariants.py::TestLateResultAsymmetry` |
| `ROUTER != ORCHESTRATOR` | `RoutingRequest` and `RoutingDecision` are different types produced by different parties; the request carries no model |
| Model output is `AI_SUGGESTION` / `AI_GENERATED` | `domain.ModelResult`, which admits nothing else |
| One governed scope per execution; narrowing-only sub-runs | `domain.ScopeBinding.narrows_to`, `Orchestrator.open_sub_run` |
| Cross-scope movement needs an approved Phase 6 handoff or Phase 8 scope transfer | `domain.ScopeTransferAuthorisation` — mechanism at a version, source run and scope, target scope, authorising human and Decision Record — consumed by `Orchestrator.transfer_scope`, which creates a **new** execution rather than rewriting a binding |
| Execution history is append-only | `domain.ExecutionEventLog` and `domain.RecordStore` — the backing list lives in a closure, so there is no attribute to rewrite, and no governed record is replaced by Work Item id |
| Completion is not approval | `Orchestrator.complete` consults the posture and the open gates, never the operational result |

## How to run

```bash
# the governed workflow, twelve demonstrated behaviours
python3 implementation/phase-12/examples/governed_run.py

# four prohibited paths and where each stops
python3 implementation/phase-12/examples/blocked_run.py

# the invariant tests
python3 -m unittest discover -s implementation/phase-12/tests -v

# the Phase 12 validator
python3 validation/phase_12_validation.py
python3 validation/phase_12_validation.py --verbose
python3 validation/phase_12_validation.py --json
```

No environment variables, no configuration, no network.

## Nothing the caller passes is taken on trust

The independent MVP audit found that typed identities alone were not enough: the reference
layer still accepted whatever object a caller handed it. Every act is now checked against state
the orchestrator itself recorded.

| The caller offers | What is actually consulted |
|---|---|
| a `Task` | the Task the run's own bound definition declares, looked up by reference |
| a `WorkItem` | the Work Item this run created, with its lineage and retry class |
| a `GateRequirement` | the gate instance this run holds for that requirement id |
| a `DecisionRecord` | its run, Work Item, requirement, Right, outcome and the holder's standing in the approved decision path |
| a `ReviewInstance` | its run, Work Item, requirement, Profile and independence class |
| a `RoutingDecision` | identity membership in this run's own recorded Router output |
| a retry class | nothing — `retry()` takes no task argument; the class comes from the Work Item |
| a mechanism reference | nothing — a crossing needs a `ScopeTransferAuthorisation` naming this run, this scope and that target |
| an assignment to `run.phase` | nothing — governed run state is read-only from outside the orchestrator |

## What the orchestrator may not do

Each of these is a raise in `orchestrator.py`, not a convention: infer or manufacture approval;
act as reviewer, Decision Right holder or signatory; accept risk; canonicalise knowledge;
choose a model or relax a routing constraint; substitute a model result for a human gate; cross
a scope silently; rewrite recorded history; retry a non-replayable governed act automatically;
or treat operational success as governance completion.

## Known limitations

Recorded honestly in `reviews/phase-12-foundation-self-check.md`. In short: this is an
in-memory reference with no persistence, no concurrency, and stub adapters; the ten-race
concurrency table is represented as vocabulary and asymmetry rather than executed against real
contention; the Phase 11 natural-language validator gaps are addressed by moving the invariants
into structured checks here, not by further regex work there; and the run-state boundary is a
reference-implementation boundary, not an operating-system one — Python has no true privacy,
and the self-check says so plainly.
