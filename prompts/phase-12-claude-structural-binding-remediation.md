# Phase 12 — Structural Binding Remediation

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-12-mvp`
Target baseline: `b0aad05bfb39227e5f51ff2651b48fa82862981d`

## Mission

Remediate the **structural governance bypasses** found by the independent Phase 12 MVP audit. This is not prose-validator work. The findings are executable implementation defects in the MVP reference layer and must be fixed structurally.

Do **not** change approved Phase 1–11 architecture semantics. Do **not** edit protected Phase 1–11 architecture/orchestration/approval files to make tests pass. Do **not** add production infrastructure, live provider calls, Supabase, SQL migrations, queues, workers, schedulers, RAG, secrets, credentials or deployment configuration.

Keep Phase 12 artifacts `PROPOSED`. No PR.

## Audit findings to close

### 1. Enforce identity types in every governed object

Every governed dataclass/object field carrying a governed reference must validate its exact reference type at construction time, not only when a downstream method happens to call `require()`.

At minimum, invalid constructions like these must raise immediately:
- `ModelResult` with non-`WorkItemRef` / non-`ModelRef` fields;
- `RoutingDecision` with non-`WorkItemRef` or non-`RouterRef` identities;
- `GateState` with wrong work-item or evidence-reference types.

Audit every governed domain object, not only the three examples.

### 2. Bind workflow/run/task/work-item lineage structurally

The orchestrator must not trust caller-supplied replacement objects.

A `WorkflowRun` must bind to an immutable governed Workflow Definition/version and its declared Task definitions. Activating a stage must refer to a Task declared by that bound definition. Creating a Work Item must bind it immutably to the Task definition/version and run that created it.

An undeclared Task must not be activatable. A Task from another run/workflow/version must not be accepted.

Assignments, routing, reviews, decisions, retry, and completion checks must operate on that bound lineage.

### 3. Make governed run state non-bypassable

Public mutation of `phase`, `posture`, gate collections, scope binding, and governed histories must not allow bypassing orchestrator transitions.

Prefer immutable/frozen state objects or private state with read-only accessors plus controlled transition/update methods. The exact design is your choice, but this mutation must no longer work:
1. missing Right causes `ESCALATED / AUTHORITY_ABSENT`;
2. caller directly sets phase/posture/gates;
3. `complete()` succeeds.

Completion must derive from internally governed state that cannot be rewritten externally.

### 4. Represent gate requirements as independent governed objects

Do not key gates only by `(work_item, gate_kind)` if that collapses distinct requirements.

Each gate requirement needs its own stable identity and immutable bindings sufficient to validate evidence, including as applicable:
- run;
- Work Item;
- gate kind;
- Review Profile;
- Decision Right;
- Human Work requirement;
- Governed prerequisite identity;
- required independence/other constraint.

Two Decision gates on one Work Item must remain two separate requirements.

### 5. Validate gate evidence against exact requirement

Evidence must match the exact gate requirement, not merely have a vaguely compatible type.

Decision evidence must verify at least:
- exact run / Work Item;
- exact Decision Right;
- exact gate requirement;
- record outcome equals the governing outcome being applied;
- valid human holder/authority identity from the approved decision path.

Review evidence must verify exact Work Item, Review Profile, and independence requirement. A requested `INDEPENDENT` review cannot be satisfied by `NOT_INDEPENDENT` evidence.

`ReviewInstance` must not satisfy a HUMAN_WORK gate. `DecisionRecord` must not satisfy a GOVERNED_PREREQUISITE gate. Define explicit evidence contracts per gate kind.

Do not let tuple/adapter outcome override contradictory evidence-object outcome.

### 6. Bind Router output to exact Routing Request

A `RoutingDecision` passed to model invocation must be verifiably the recorded Router output for the exact request, exact run, and exact Work Item.

A caller-fabricated eligible RoutingDecision with arbitrary model, missing Router, or no preceding recorded request must fail.

The orchestrator may request routing but may not select a model itself. Preserve `ROUTER != ORCHESTRATOR`.

### 7. Bind retry class immutably

Retry eligibility must come from the governed Task/Work Item lineage, not from a caller-supplied Task argument at retry time.

A Work Item created from `NON_RETRYABLE_GOVERNED_ACT` must remain non-retryable even if a caller later presents a substitute Task claiming `SAFE_AUTOMATIC_RETRY`.

### 8. Approved mechanism and immutable scope semantics

Do not treat a bare `HandoffRef` or `ScopeTransferRef` identifier as proof that a crossing is approved.

Introduce a minimal governed evidence object or registry binding the approved mechanism to:
- source run/scope;
- target scope;
- mechanism identity/version;
- approval/governance provenance needed by the approved architecture.

A fabricated reference alone must fail.

Preserve one governed scope per execution. If approved Phase 11 semantics require scope change to create a new run/sub-run rather than mutating the original run binding, implement that. Do not mutate residency/sensitivity on the same run through `cross_scope()`.

### 9. Preserve governed history append-only

Do not overwrite prior Decision, Review, Routing, Model-result or other governed records by Work Item ID.

Use append-only collections or record stores with stable record identities. Event/provenance history must preserve enough value/version references to reconstruct what happened.

Repeated Decision execution must leave the earlier Decision Record standing in governed history. Late/repeated records may require reconciliation, but may not silently replace prior governed history.

Do not rely on an underscore-private mutable list as the sole append-only guarantee if callers can mutate it trivially. Strengthen the reference implementation boundary appropriately.

### 10. Add adversarial + mutation-resistant tests

Add executable tests for every blocker above. The test suite must prove the *relationships*, not only happy-path object creation.

At minimum include all independent audit bypasses:
- wrong reference types rejected at construction;
- undeclared Task activation rejected;
- foreign DecisionRecord cannot satisfy gate;
- two same-kind gates do not collapse;
- review independence mismatch rejected;
- tuple/record outcome mismatch rejected;
- ReviewInstance cannot satisfy HUMAN_WORK;
- DecisionRecord cannot satisfy GOVERNED_PREREQUISITE;
- fabricated RoutingDecision rejected before model invocation;
- retry-class substitution rejected;
- fabricated scope mechanism rejected;
- direct run-state mutation cannot bypass governance;
- repeated Decision records preserved append-only.

Add controlled weakenings/mutations for load-bearing guards where practical so removing each structural check causes at least one test/validation failure.

## Constraints

- Keep implementation minimal and readable; do not turn this into production infrastructure.
- Standard library only unless the repository already approved another dependency for Phase 12 (do not introduce one casually).
- No network.
- No hidden TODOs for any blocker above.
- If one audit finding conflicts with an approved Phase 1–11 semantic rule, stop and report the conflict instead of changing architecture.
- Protected upstream files remain byte-for-byte unchanged.
- Do not fix inherited Phase 11 `159/160` or Phase 10 `145/147` approval-record validator conditions from this Phase 12 remediation.

## Validation required before commit

Run and report:

```bash
python3 -m unittest discover -s implementation/phase-12/tests -v
python3 validation/phase_12_validation.py
python3 validation/phase_12_validation.py --verbose
python3 validation/phase_12_validation.py --json
python3 implementation/phase-12/examples/governed_run.py
python3 implementation/phase-12/examples/blocked_run.py
python3 validation/phase_11_validation.py
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Also execute explicit adversarial probes corresponding to every audit bypass listed above and show that each now fails/stops for the intended reason.

## Expected output

Return exactly these sections:

### A. REMEDIATION SUMMARY
### B. IDENTITY / CONSTRUCTION ENFORCEMENT
### C. WORKFLOW / TASK / WORK-ITEM BINDING
### D. RUN STATE / COMPLETION HARDENING
### E. GATE REQUIREMENT / EVIDENCE BINDING
### F. ROUTING / RETRY / SCOPE BINDING
### G. APPEND-ONLY HISTORY / RACE HANDLING
### H. ADVERSARIAL / MUTATION TESTS
### I. VALIDATION / REGRESSION
### J. FILES CHANGED
### K. KNOWN LIMITATIONS
### L. COMMIT / PUSH
### M. NEXT STEP

The expected next-step phrase, only if every blocker above is structurally closed, is:

`READY FOR INDEPENDENT PHASE 12 MVP RE-AUDIT`
