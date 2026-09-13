# Phase 12 — Claude Final Atomicity Remediation

## Role
Act as the senior implementation engineer responsible for the Phase 12 in-memory MVP reference implementation.

This is a **targeted remediation only**. Do not redesign the architecture, broaden scope, add production infrastructure, change Phase 1–11 artifacts, or turn this into another general hardening pass.

## Repository / branch
- Repository: `dgerman-code/AI-OS`
- Branch: `implementation/phase-12-mvp`
- Required starting baseline: `77690e931d3d297dab58342771de0547a099cf81`

If branch HEAD is not a descendant of that baseline, stop and report the discrepancy.

## Audit source of truth
The independent V4 re-audit found only the following blocking family: **late-failure atomicity**. Sections C, E, F, G, H, I, M, O all passed. Do not reopen passing areas except where strictly necessary to fix the four atomicity defects below.

The required invariant is:

> If an ordinary governed act fails, then phase, posture, terminal state, Work Item counters, gate outcomes, governed record stores, and execution-event history must remain observationally identical to their pre-call state.

This applies not only to known duplicate-record cases but to every fallible validation step in the affected call path.

## The four exact blockers to close

### 1. Assignment attempt counter mutates before validation
Current failure reproduced by audit:
- assignment begins;
- Work Item attempt count moves `0 -> 1`;
- invalid `agent_instance` then raises `IdentityError`.

Required behavior:
- construct and fully validate the proposed `Assignment` and every referenced identity/lineage constraint first;
- preflight any append/record operation first;
- only after all validation passes may the Work Item attempt counter increment and the assignment/history/event be committed;
- an invalid assignment must leave attempt count, history, events and all run axes byte-for-byte/observationally unchanged.

Do not hide the problem by decrementing on exception. The design must be validate-then-commit, not mutate-then-rollback.

### 2. Repeated `pause()` partially commits before invalid transition
Current failure:
- run is already PAUSED;
- second `pause()` records intervention and event;
- invalid `PAUSED -> PAUSED` transition then fails.

Required behavior:
- validate intervention lineage/type;
- preflight record identity insertion;
- preflight the entire intended transition sequence;
- only then append intervention/event and transition;
- calling `pause()` when no legal transition exists must leave run state, stores and events unchanged.

Prefer one explicit commit point. Do not depend on exception cleanup.

### 3. Scope transfer logs authorization before target-run validation
Current failure:
- source authorization is valid;
- `scope:transfer_authorised` is appended;
- target definition/run creation later raises `LineageError`.

Required behavior:
- before recording any transfer authorization or event, validate **all** source-side and target-side conditions required for successful creation of the target execution;
- this includes target `WorkflowDefinition`, run identity suitability, target scope compatibility and every `_create_run` condition that can fail;
- only once both source authorization and prospective target-run construction are known valid may the transfer authorization event and new run be committed.

If useful, introduce a pure/preflight helper that validates prospective run creation without mutation, then let `_create_run` commit after preflight. Do not duplicate validation semantics in divergent paths.

A failed transfer must not append `scope:transfer_authorised`, create a partial run, or mutate source state/history.

### 4. `route()` retains Routing Request/event when Router answer is malformed
Current failure:
- `route()` records a Routing Request and `routing:requested` event;
- configured Router returns malformed/invalid `RoutingDecision`;
- validation rejects it;
- request/event remain.

For the purposes of this Phase 12 MVP and the V4 audit standard, `route()` is one governed act and must be atomic.

Required behavior:
- build a **prospective/transient** Routing Request without committing it;
- invoke the configured Router with that exact object;
- fully validate the returned `RoutingDecision` against router identity, request identity, run, Work Item and all existing routing constraints;
- preflight both request and decision record-store insertions and any event writes;
- only after the answer is valid commit the request, the decision, and their events as one logical act;
- malformed Router output must leave routing request history, routing decision history, events, run axes and Work Item state unchanged.

Important distinction:
- if there is an explicit standalone API whose successful purpose is merely to create/record a routing request, it may remain a separate governed act;
- but `route()` itself must not call a mutating request-recording API before Router-answer validation.

Do not reintroduce any caller-injectable Routing Decision path. V4 Section E already passed and must stay passed.

## Atomicity implementation guidance

Use the existing Phase 12 pattern where possible:
- `_require_progressible()` for halted/terminal protection;
- `RecordStore.validate_add()` for duplicate preflight;
- `_preflight_phases()` for transition preflight;
- explicit prospective object construction before mutation;
- one small commit section after all fallible checks.

If a helper both validates and mutates today, split it into a pure/preflight portion and a commit portion rather than adding rollback logic.

Do **not** introduce a generic transaction framework, persistence abstraction, database, locks, snapshots-as-runtime-rollback, decorators, or speculative production machinery. This remains a small standard-library in-memory reference implementation.

## Required adversarial tests

Add committed tests that independently reproduce all four V4 failures and assert complete observational non-mutation.

At minimum:

1. `test_invalid_assignment_does_not_increment_attempt_or_append_history`
   - invalid `AgentInstanceRef`/wrong governed type or invalid assignment lineage;
   - snapshot before/after identical;
   - attempt remains zero.

2. `test_second_pause_failure_is_atomic`
   - pause once successfully;
   - snapshot;
   - second pause fails;
   - snapshot unchanged, including interventions/events.

3. `test_invalid_target_definition_transfer_is_atomic`
   - valid retained Decision Record + valid mechanism/Right/act authorization;
   - invalid target definition/run construction;
   - failure with source snapshot unchanged and no target run committed.

4. `test_malformed_router_answer_leaves_no_request_or_event`
   - configured Router is actually called;
   - returns malformed answer (choose a structurally meaningful wrong run/work-item/request/router field);
   - `route()` fails;
   - routing requests, decisions, events and run state unchanged.

Use the same snapshot vocabulary as the audit where practical: axes, counters, gates, governed stores, event count/content.

Also add nearby variants so this is structural, not probe-specific:
- assignment duplicate-record failure after all identity validation;
- pause duplicate intervention identity;
- target run-ref collision or other target-run preflight failure;
- Router answer with valid type but wrong request identity.

## Mutation harness

Extend the **committed** mutation/adversarial harness so at least the following weakenings are non-vacuously detected:
- assignment counter increment moved before validation;
- pause intervention append moved before transition preflight;
- transfer authorization event emitted before target preflight;
- route request committed before Router-answer validation.

Mutation targets must fail loudly if source text/pattern is not found. Keep honest `DETECTED` / `REDUNDANT` classification; do not label an actually redundant mutation as detected.

Do not make `HIGH` a magic textual claim. The independent re-audit decides credibility. Your job is to make the committed evidence strong enough.

## Validator / self-check

Update `validation/phase_12_validation.py` and `reviews/phase-12-foundation-self-check.md` to:
- include the four new atomicity tests;
- verify they are in the ordinary committed test suite;
- verify the relevant mutation scenarios execute;
- keep one current, internally consistent test count only;
- preserve inherited Phase 11 `159/160` and Phase 10 `145/147` facts exactly as inherited;
- do not modify upstream validators or approval records.

Do not add brittle source-string checks where executable behavior can be tested.

## Regression requirements

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

Expected upstream facts remain:
- Phase 11: inherited `159/160` approval-record wording condition;
- Phase 10: inherited `145/147` approval-record status conditions;
- Phase 9: `277/277`;
- Phase 8: `119/119`.

Verify protected Phase 1–11 files are unchanged from `b8fba92e03a4bc29c8f1bb4d894fb9efb45586cb`.

## Scope constraints

Allowed to change only what is needed in Phase 12 implementation/assurance, expected mainly:
- `implementation/phase-12/orchestrator.py`
- `implementation/phase-12/domain.py` only if truly required
- `implementation/phase-12/adapters.py` only if required for malformed Router test fixture semantics
- `implementation/phase-12/tests/test_invariants.py`
- `implementation/phase-12/tests/test_mutation_guards.py`
- `implementation/phase-12/examples/blocked_run.py` if useful
- `implementation/phase-12/README.md`
- `validation/phase_12_validation.py`
- `reviews/phase-12-foundation-self-check.md`

Do not modify Phase 1–11 architecture/orchestration/validators/approval records.
Do not add live providers, DB, SQL, migrations, queues, workers, schedulers, event buses, secrets, deployment or UI.
Do not create a PR.
All Phase 12 artifacts remain `PROPOSED`.

## Required final report

Return exactly these sections:

### A. REMEDIATION SUMMARY
### B. ASSIGNMENT ATOMICITY
### C. PAUSE ATOMICITY
### D. SCOPE-TRANSFER ATOMICITY
### E. ROUTING ATOMICITY
### F. ADVERSARIAL / MUTATION COVERAGE
### G. TESTS / VALIDATION
### H. REGRESSION
### I. FILES CHANGED
### J. KNOWN LIMITATIONS
### K. COMMIT / PUSH
### L. NEXT STEP

In `K`, provide the exact implementation commit SHA and commit message and confirm branch push / clean worktree / no PR.

In `L`, use exactly:

`READY FOR INDEPENDENT PHASE 12 MVP RE-AUDIT V5`

Commit implementation with a concise message such as:

`feat: close Phase 12 final atomicity gaps`
