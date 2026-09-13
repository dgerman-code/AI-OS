# Phase 12 — MVP foundation producer self-check

Status: `PROPOSED`

Branch: `implementation/phase-12-mvp`

Base approval commit: `b8fba92e03a4bc29c8f1bb4d894fb9efb45586cb`

Human-approved Phase 11 architecture baseline: `b4cc549680c87e465931b5c4a6825e34f3c3ced6`

This is the producer's own account of what was built, what it proves, and what it does not.
It is not an independent audit.

---

> **Revision 5 — late-failure atomicity.** The v4 re-audit found four ordinary governed
> acts that still mutated before their last fallible check: the assignment attempt counter,
> `pause`, the scope-transfer authorisation event, and the Routing Request in `route()`. All
> four now validate everything fallible first and commit afterwards; section 4e records them.
>
> **Revision 4 — halted-run, atomic commit, provenance and committed mutation assurance.**
> The v3 re-audit rated the implementation substantially stronger but NOT READY, on five
> load-bearing families plus harness credibility. All are closed; section 4d records them. The
> mutation runner is now **committed and executed by the validator**, so the credibility claim
> rests on evidence in the repository rather than on a scratch file.
>
> **Revision 3 — governed evidence and lineage hardening.** The independent re-audit found
> nine further structural blockers on the remediated baseline. All nine are closed; section 4c
> records them. The governing rule is now: *a governed act may change execution state only when
> the exact requirement, lineage, authority, adapter provenance, evidence object and retained
> history needed by that act are already valid and recorded* — validate first, commit second,
> and never partially.
>
> **Revision 2 — structural binding remediation.** This document was updated after the
> independent Phase 12 MVP audit found ten structural governance bypasses in the reference
> layer. All ten are closed; sections 2, 4a and 6 below record the current state, and section
> 4b records what the audit found and how each finding was answered.

## 1. What was built

A minimal, offline, standard-library reference implementation of the approved control model:

| File | Responsibility |
|---|---|
| `implementation/phase-12/domain.py` | Governed identities as distinct types; the four state axes; gate, retry and race vocabularies; append-only event log |
| `implementation/phase-12/orchestrator.py` | The reference coordinator. Every Axis A move goes through one validated function |
| `implementation/phase-12/adapters.py` | Router, reviewer desk, decision authority and model execution, behind protocols with in-memory stubs |
| `implementation/phase-12/examples/governed_run.py` | One workflow that reaches `COMPLETED` under governance |
| `implementation/phase-12/examples/blocked_run.py` | Four prohibited paths and where each stops |
| `implementation/phase-12/tests/test_invariants.py` | 65 deterministic invariant and transition tests |
| `validation/phase_12_validation.py` | Structure, containment and assurance validator |
| `implementation/phase-12/README.md` | Scope, non-scope, architecture mapping, how to run |

The design rule throughout: **make the denied collapses unrepresentable rather than
discouraged.** A `RoleRef` and an `AgentInstanceRef` carrying the same string are unequal, and
`require()` raises rather than coercing.

## 2. Exact results

```
python3 -m unittest discover -s implementation/phase-12/tests
Ran 145 tests — OK

python3 validation/phase_12_validation.py            === 52/52 PASS ===   exit 0
python3 validation/phase_12_validation.py --verbose   === 52/52 PASS ===   exit 0
python3 validation/phase_12_validation.py --json      total 52, passed 52, 52 results

python3 implementation/phase-12/examples/governed_run.py   exit 0, run COMPLETED / GOVERNANCE_CLEAR
python3 implementation/phase-12/examples/blocked_run.py    exit 0, four governance stops and
                                                            twenty-two structural bypasses refused
```

Validator groups: `structure` 4 · `containment` 6 · `domain` 7 · `assurance` 29 ·
`suite` 5 · `inventory` 1.

**Controlled weakenings: 16, committed and executed.**
`implementation/phase-12/tests/test_mutation_guards.py` removes each load-bearing guard from
the module **source in memory**, executes a fresh copy of the implementation, and re-runs the
scenario that guard protects. Nothing on disk is edited, so the runner is reproducible from a
clean checkout and runs as part of the ordinary suite. The Phase 12 validator both checks that
the harness is committed and re-derives every classification itself, so a weakening that
quietly stopped biting is a validator failure rather than a stale comment.

Fifteen of the sixteen are classified `DETECTED` — removing the guard changes observable
governed behaviour. One is classified `REDUNDANT` and says so in the file: removing the Model
Result identity **preflight** changes nothing observable, because nothing has mutated between
the preflight and the append, so the store's own identity check still refuses. That store check
is itself weakened separately, and is detected.

Three earlier redundancies were removed rather than explained: the stage activation path
refuses a halted run in exactly one place; the authorisation-coverage check is exercised by
source-run and target-binding mismatches that no other check catches; and "a continuing outcome
with no record" raises its own `MissingEvidenceError`, so the guard is load-bearing by type

## 3. Regression

| Validator | Result | Note |
|---|---|---|
| Phase 11 | `159/160 PASS` | **Inherited.** Reproduced at the base approval commit `b8fba92` before any Phase 12 work. The single failure is the Phase 11 approval record's own sentence *"without distributed exactly-once claims"* tripping the Phase 11 exactly-once scan — an approval-record-only condition, not repaired from Phase 12 |
| Phase 10 | `145/147 PASS` | Inherited approval-record-only condition, unchanged and not repaired |
| Phase 9 | `277/277 PASS` | |
| Phase 8 | `119/119 PASS` | |

`architecture/`, `orchestration/`, the Phase 8–11 validators and `reviews/phase-11-final-approval.md`
are byte-for-byte unchanged since the base approval commit; the Phase 12 validator asserts this
rather than claiming it.

## 4a. What the structured layer enforces

| Approved rule | Enforcement |
|---|---|
| Role ID cannot be used where an Agent Instance ID is required | `require()` raises `IdentityError` on the type |
| Model Profile cannot satisfy a Review Instance or Decision Record field | constructor raises |
| A Decision Record requires an explicit human authority | constructor raises on any other reference kind |
| Router output cannot set a gate state | `satisfy_gate_with` accepts only the gate kind's own evidence type |
| Evidence must answer the exact requirement | run, Work Item, requirement id, Profile or Right, independence class, holder standing, and the evidence's own outcome are all checked |
| A fabricated Routing Decision cannot reach a model | model invocation requires identity membership in this run's recorded Router output |
| Lineage cannot be substituted | Tasks are looked up in the run's bound definition; Work Items, gates and retry classes come from what the run recorded |
| Governed run state cannot be set from outside | `WorkflowRun.__setattr__` raises; mutation needs the token the creating orchestrator holds |
| Missing Decision Right cannot transition to a continuing state | outcome → BLOCKED + ESCALATED + `AUTHORITY_ABSENT`, and **no Decision Record is produced at all** |
| A model result cannot mutate canonical state | `ModelResult` admits only `AI_GENERATED` / `AI_SUGGESTION`, and `satisfies_gate()` is `False` |
| Cross-scope transition requires an approved transfer or handoff | only `HandoffRef` or `ScopeTransferRef` are accepted; anything else blocks |
| Terminal completion requires a permitted posture | `POSTURE_PERMITS_COMPLETION` is empty for `GATE_UNSATISFIED` and `AUTHORITY_ABSENT` |
| Retries cannot replay a non-replayable governed act | classes 4 and 6 escalate and dispatch nothing |
| Execution history is append-only | write and delete raise `AppendOnlyError` |
| Timeout is not approval | `EXPIRED` escalates and is not in `CONTINUING_GATE_OUTCOMES` |

### 4b. The ten audit findings, and how each was closed

| # | Finding | Answer |
|---|---|---|
| 1 | Identity types were only checked where a downstream method called `require()` | `enforce_reference_types()` runs in every governed object's `__post_init__`, driven by the declared annotations; a required reference slot also refuses `None` |
| 2 | The orchestrator trusted caller-supplied replacement objects | A run binds the `WorkflowDefinition` object; `activate_stage` takes a `TaskRef` and looks it up; a `WorkItem` carries workflow, version, task, run, role, capability and retry class |
| 3 | Public mutation of phase, posture, gates and scope bypassed the transitions | `WorkflowRun` exposes read-only properties; `__setattr__` raises `StateAccessError`; state moves only through the creating orchestrator's token |
| 4 | Gates keyed by `(work_item, kind)` collapsed distinct requirements | `GateRequirement` has a `GateRequirementRef`; `GateInstance` binds it to one run and Work Item; two Decision gates stay two |
| 5 | Evidence was accepted on a vaguely compatible type | `EVIDENCE_CONTRACT` gives one admissible type per gate kind, and `validate_evidence` checks every binding including the holder's standing and the adapter tuple against its own record |
| 6 | Router output was not bound to a request | `RoutingRequest` has an identity and is recorded; a decision must `answers()` it; model invocation requires identity membership in the recorded store |
| 7 | Retry class came from a caller-supplied Task | `retry()` has no task parameter; the class is read from the Work Item's lineage |
| 8 | A bare mechanism reference proved a crossing was approved | `ScopeTransferAuthorisation` binds mechanism-at-version, source run and scope, target scope, human authority and Decision Record; the crossing creates a **new** execution and rewrites no binding |
| 9 | Governed records were overwritten by Work Item id | `RecordStore` is append-only with the backing list in a closure; repeated Decision and Review records both stand |
| 10 | Tests proved object creation, not relationships | 145 tests, including one class per finding, plus the committed weakenings above |

### 4c. The nine re-audit findings, and how each was closed

| # | Finding | Answer |
|---|---|---|
| 1 | Construction-time validation covered references only | `enforce_field_types()` validates **every** declared field: Enums by exact type, structured values such as `ScopeBinding` by class, tuples and frozensets element by element, `Optional` distinguished from required, and a plain `str` refused wherever an Enum or a structured value is declared. No coercion anywhere. A sweep test asserts every governed dataclass calls it |
| 2 | A `GateRequirementRef` is not an instantiated gate identity | `GateInstance` carries a `GateInstanceRef` and its own `kind`; the run keys gates by instance identity, so activating one gated Task twice yields two Work Items and two retained gates, and two Tasks reusing a requirement id do not alias |
| 3 | A blocked or escalated run could progress through ordinary APIs | Stage activation plus assignment, routing, model invocation, review/decision/human-work/prerequisite gates, external evidence satisfaction and retry all refuse from `BLOCKED`/`ESCALATED` and under `AUTHORITY_ABSENT`; leaving those states is `unblock()`, which needs a recorded human act and refuses while any gate stands resolved against continuation |
| 4 | State moved before validation completed | Every governed act is validate-then-commit: the adapter is asked, the answer is validated in full, and `_commit_gate` applies the result. A refusal leaves axes, gate outcomes, all five record stores and the event count identical — asserted by a `snapshot()` helper in four tests. A continuing Decision outcome with no record raises `MissingEvidenceError` before anything moves |
| 5 | `SATISFIED_WITH_OPEN_ITEMS` applied only on the review path | Every satisfaction path funnels through `_apply_gate_outcome`, so all four gate kinds and `satisfy_gate_with()` carry `OPEN_ITEMS_CARRIED`, and such a run completes only as `COMPLETED_WITH_OPEN_ITEMS` |
| 6 | A well-shaped authorisation was sufficient | `transfer_scope` corroborates every clause against the source run's retained history: the Decision Record must be retained and must answer the exact run, Work Item, requirement and Right with a continuing outcome; the authorising human must be that record's author and hold the Right; the mechanism at its version must be approved by the configured registry for that exact Right (no registry approves nothing); the complete source and target bindings must match; and sensitivity may not widen nor residency change |
| 7 | A caller could manufacture a Routing Decision and record it | There is no recording method — `route()` invokes the configured Router and directly records exactly the object it returned; `decided_by` must equal the configured `RouterRef`; and a `ModelResult` must carry its own record identity and answer this run, Work Item, Routing Decision, model and Model Profile before it is recorded |
| 8 | Evidence could satisfy a gate without being retained | `_commit_gate` retains the evidence in its governed store as part of the same commit, keyed by the record's own identity; `RecordStore` refuses a duplicate identity; and `run.evidence_for(gate)` reconstructs what explained a completion |
| 9 | Adversarial and mutation credibility | 145 tests, 22 executable bypass probes in `examples/blocked_run.py`, and the committed weakening harness |

Two checks compare the implementation against the architecture **documents** rather than
against itself: the transition table is parsed from
`orchestration/state-machine-and-transitions.md` and reconciled row by row, and the separation
chain is parsed from `architecture/orchestrator-architecture.md`. An implementation that drifts
from the approved architecture fails without anyone editing the validator.

### 4d. The v3 re-audit findings, and how each was closed

| Family | Answer |
|---|---|
| Halted-run refusal applied in one place only | `_require_progressible()` is the one guard, called by every ordinary API — stage activation, assignment, routing request, route, model invocation, review, decision, external gate satisfaction, human work, prerequisite, retry, intervention, pause, sub-run, scope transfer and completion. It also refuses a terminal run. Stopping a halted run (CANCELLED, TERMINATED) stays permitted, because stopping is always permitted; only completing is governed |
| `unblock()` must be the only way back | It is the only method that does not call the guard, and it earns that by being harder: a validated human intervention naming this run, no gate still standing against continuation, and every fallible check preflighted before the first mutation |
| Validate-then-commit not atomic | Every fallible check now precedes the first mutation: evidence appends through `RecordStore.validate_add`, the whole planned phase sequence through `_preflight_phases`, and the Model Result identity before the model result is recorded. Four snapshot tests assert bit-for-bit equality of axes, gate outcomes, every record store and the event count after a refusal |
| Routing origin caller-assertable | There is no recording path at all: `route()` asks the configured Router and records exactly the object returned, and the validator asserts that neither `record_routing_decision` nor `_record_routing_decision` exists on the orchestrator |
| Mechanism approval too coarse | An approval binds mechanism, version, both complete bindings, the **exact Decision Right** and the **authorised act**. An unrelated Right and a mismatched act are each refused, without mutation |
| ModelResult lacked identity and profile lineage | `ModelResultRef` is part of `ModelResult`, alongside the selected `model_profile`; `invoke_model` verifies both against the recorded Routing Decision and preflights the identity before recording |
| Harness credibility LOW | The weakening runner is committed at `implementation/phase-12/tests/test_mutation_guards.py`, runs in the ordinary suite, and the validator re-derives every classification independently |

### 4e. The v4 re-audit findings, and how each was closed

| Finding | Answer |
|---|---|
| The assignment attempt counter moved before the Agent Instance reference was validated, so a refused assignment consumed an attempt | `assign()` computes the attempt number as a local, constructs the `Assignment` (which is what validates the Agent Instance) and preflights the store insert; only then does it write the counter, append the record and log the event. There is no decrement-on-exception anywhere: the design is validate-then-commit, not mutate-then-rollback |
| A second `pause()` on an already-PAUSED run appended the intervention and its event before the transition refused | Intervention validation is split into a read-only `_validate_intervention()` and a commit-only `_record_intervention()`, shared with `unblock()` so the two paths cannot diverge. `pause()` validates, preflights the store insert, preflights the transition, and only then commits. `_preflight_phases` gained `allow_noop`, so a preflight is never more permissive than the commit it stands in for: `_ensure_phase` callers tolerate "already there", `_transition` callers do not |
| A scope transfer appended `scope:transfer_authorised` before the target run was known creatable | `_preflight_run_creation()` holds every condition that can refuse a run creation — governed definition, run-reference type, run-identity collision against this orchestrator's issued references, complete target binding, and the narrowing rule with its authorisation exemption. `_create_run()` calls it and then only commits, and `transfer_scope()` calls the same helper before it records anything. One definition of the conditions, two call sites, no divergent semantics |
| `route()` recorded the Routing Request before the Router's answer was validated | The request is built prospectively by `_build_routing_request()` and recorded nowhere. The Router is asked with that exact object, the answer is fully validated, both store inserts and the phase plan are preflighted, and request, decision and both events commit as one act. `request_routing()` remains a governed act in its own right, and `route()` no longer goes through it. No caller-injectable Routing Decision path was reintroduced |

Four named regression tests hold these: `test_invalid_assignment_does_not_increment_attempt_or_append_history`,
`test_second_pause_failure_is_atomic`, `test_invalid_target_definition_transfer_is_atomic` and
`test_malformed_router_answer_leaves_no_request_or_event`, with nearby variants for a
wrong-Role assignment, a repeated intervention identity, a colliding target run identity, and
a Router answer that is well-formed but answers another request or comes from another Router.
Each compares the full observable state — axes, gate outcomes, every governed record store and
the execution-event count — before and after the refusal. The validator loads the four by name
through `unittest` rather than by grep, so a renamed or commented-out test fails it. Four new
weakenings move each mutation back in front of its check and are classified `DETECTED`.

## 5. Deferred Phase 11 validator hardening

Phase 11 was approved with four natural-language attachment items deferred. Phase 12's answer
is to stop relying on the text layer for them where a structured object can carry the rule:

| Deferred item | Phase 12 position |
|---|---|
| same-subject pronoun attachment after controlled connectors (`... but it is ...`) | **Structurally moot here.** In the implementation a Role and an Agent Instance cannot be equated by any sentence; the collapse is a type error. The text-layer gap remains in the Phase 11 prose scanner and is not re-opened |
| contrastive `although` / `though` hiding a later identity collapse | **Text-layer only, unchanged.** Recorded as a known limitation below |
| false positives for genuinely new bare/proper-name subjects after coordinators | **Text-layer only, unchanged** |
| restoring HIGH harness credibility | **Partially addressed.** Credibility moves to structured checks and executable tests for the implementation; the Phase 11 prose harness's own credibility is unchanged at `MEDIUM` and this document does not claim otherwise |

No further natural-language regex expansion was attempted, per the Phase 12 instruction. The
approved invariants are enforced at the structured-data boundary instead. **This changes no
approved architecture semantics**: the architecture already states these rules; Phase 12 only
changes where they are checked.

## 6. Known limitations

Each of these is an MVP limitation, not an architecture defect.

1. **In-memory only.** No persistence, no Phase 10 storage adapter, no version-pinned write.
   The concurrency table's `BLOCK`-on-version-conflict cases therefore cannot be *executed*
   here; `RaceOutcome` and the late-review / late-Decision asymmetry are represented and tested
   as vocabulary and as record-standing behaviour, not against real contention.
2. **Single-threaded, single-run.** No dispatch concurrency, no scheduler, no dependency graph
   beyond one task per definition in the examples. Stage ordering and bounded rework loops are
   modelled only as far as the state machine requires.
3. **Stub adapters.** The Router, reviewer desk and decision desk return recorded fixtures.
   They prove the *shape* of the boundary — request and decision are different objects by
   different parties — not the behaviour of a real Phase 9 router or a real reviewer.
4. **No live model call, by design.** `StubModel` returns a fixed string. A real provider would
   add nothing to the claim being made and would couple governance objects to a vendor.
5. **Compensation is named, not implemented.** Class 6 recovery is "a new act, separately
   authorised"; Phase 12 stops the run and escalates rather than modelling the compensating
   act.
6. **`SUPERSEDED` and run-supersession linking** are in the state model but not exercised by an
   example.
7. **The run-state boundary is a reference-implementation boundary, not an operating-system
   one.** `WorkflowRun.__setattr__` raises and the mutable state sits behind a token, but
   Python has no true privacy: `object.__setattr__` and name-mangled attribute access still
   exist for anyone determined to reach them. The claim made here is that no *ordinary* caller
   path can set governed state, and that every orchestrator act consults state the orchestrator
   recorded. A production implementation would put this boundary in a process or a database,
   not in a class.
8. **The `inventory` self-check counts this document's stated total**, not its prose. A wrong
   description here would not fail the validator; a wrong number would.
9. **The weakening harness is committed and runs in-process.** It executes copies of the
   implementation with guards removed; it does not fork, sandbox or time-limit them. A
   weakening that hung rather than failing would hang the suite.
10. **One weakening is honestly classified `REDUNDANT`**, and one earlier finding remains so:
   removing the `AUTHORITY_ABSENT` posture check in the halted guard changes nothing
   observable today, because that posture is only ever set together with `ESCALATED`. Both are
   kept as defence for future paths and are recorded rather than claimed.

## 6a. Harness credibility, self-assessed

**MEDIUM-HIGH, and the gap is named.** What supports it: 145 committed tests; 22 executable
bypass probes; a committed weakening runner whose fifteen detected weakenings are re-derived by
the validator; and two checks that compare the implementation against the architecture
*documents* rather than against itself. What holds it back from HIGH: this is a single-process
in-memory reference with no persistence and no concurrency, so a whole class of governed
behaviour — version-pinned writes, real contention, the ten-race table — is represented rather
than executed. A producer self-assessment is also not an audit.

## 7. Statements this document does not make

- It does not claim an independent audit was performed.
- It does not claim exactly-once delivery anywhere.
- It does not claim the Phase 11 prose harness reached `HIGH` credibility.
- It does not claim anything about remote repository state.
- It does not claim Phase 12 is approved. All Phase 12 artifacts are `PROPOSED`.
