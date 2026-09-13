# Phase 12 — MVP foundation producer self-check

Status: `PROPOSED`

Branch: `implementation/phase-12-mvp`

Base approval commit: `b8fba92e03a4bc29c8f1bb4d894fb9efb45586cb`

Human-approved Phase 11 architecture baseline: `b4cc549680c87e465931b5c4a6825e34f3c3ced6`

This is the producer's own account of what was built, what it proves, and what it does not.
It is not an independent audit.

---

> **Revision — structural binding remediation.** This document was updated after the
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
Ran 82 tests — OK

python3 validation/phase_12_validation.py            === 37/37 PASS ===   exit 0
python3 validation/phase_12_validation.py --verbose   === 37/37 PASS ===   exit 0
python3 validation/phase_12_validation.py --json      total 37, passed 37, 37 results

python3 implementation/phase-12/examples/governed_run.py   exit 0, run COMPLETED / GOVERNANCE_CLEAR
python3 implementation/phase-12/examples/blocked_run.py    exit 0, four governance stops and
                                                            ten structural bypasses refused
```

Validator groups: `structure` 4 · `containment` 6 · `domain` 7 · `assurance` 17 ·
`suite` 2 · `inventory` 1.

**Controlled weakenings: 20, each caught by both the test suite and the validator.** Every
load-bearing structural guard was removed in turn — construction-time reference enforcement,
the run-state boundary, the state token, task lookup, gate identity, each of the five evidence
bindings, both routing bindings, the retry-class binding, both scope-authorisation checks, the
record store's append-only behaviour, the event log's attribute guard, and both completion
conditions. None of them passed silently.

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
| 10 | Tests proved object creation, not relationships | 82 tests, including one class per finding, plus the 20 controlled weakenings above |

Two checks compare the implementation against the architecture **documents** rather than
against itself: the transition table is parsed from
`orchestration/state-machine-and-transitions.md` and reconciled row by row, and the separation
chain is parsed from `architecture/orchestrator-architecture.md`. An implementation that drifts
from the approved architecture fails without anyone editing the validator.

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
9. **The 20 controlled weakenings are run from a scratch harness, not committed.** They are
   reproducible by editing a guard and re-running the suite, and each is named in section 2,
   but the mutation runner itself is not part of the repository.

## 7. Statements this document does not make

- It does not claim an independent audit was performed.
- It does not claim exactly-once delivery anywhere.
- It does not claim the Phase 11 prose harness reached `HIGH` credibility.
- It does not claim anything about remote repository state.
- It does not claim Phase 12 is approved. All Phase 12 artifacts are `PROPOSED`.
