# Phase 12 — Claude Remediation: Halted-Run, Atomic Commit, Provenance, and Harness Credibility

Status: PROPOSED

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-12-mvp`
Target remediation baseline: `a8a27b6eaa4ae3789a076e2f62ba06ee750c93de`

## Objective

Remediate ONLY the remaining blockers from the independent Phase 12 MVP re-audit v3. Do not redesign Phase 1–11 architecture. Do not introduce production infrastructure. Do not create a PR.

The audit found that the Phase 12 reference implementation is substantially stronger, but still NOT READY because five load-bearing control families remain incomplete:

1. halted-run refusal is not applied consistently across all normal mutation/progression APIs;
2. validate-before-commit is not atomic when a later governed-store insertion fails;
3. Routing Decision origin is still caller-assertable through an internal-but-callable recording path;
4. scope-transfer mechanism approval is not bound to the exact Decision Right / authorized act;
5. ModelResult lacks stable record identity and selected Model Profile lineage;
6. mutation/adversarial assurance is not committed and harness credibility remains LOW.

The implementation must preserve the approved architecture and MVP boundaries. In-memory, single-process, standard-library-only remains acceptable.

## Non-negotiable invariants

### 1. One common halted-run guard

Create one central guard used by every normal API that can mutate governed state/history or progress execution.

At minimum apply it to:
- stage activation;
- assignment;
- routing request / route;
- routing-decision recording if any such path still exists;
- model invocation / model-result recording;
- review request / review execution;
- decision request / decision execution;
- external gate satisfaction;
- human-work recording;
- prerequisite recording;
- retry / replay dispatch;
- completion;
- any other public or semipublic orchestration method that can mutate governed state/history.

If run phase is `BLOCKED` or `ESCALATED`, or governance posture is `AUTHORITY_ABSENT`, no such API may progress or append governed history unless the operation is the explicitly governed recovery path.

`unblock()` (or equivalent governed recovery operation) must be the ONLY path that can restore progression after such halt. It must require retained, validated human intervention / authority evidence and must not clear or bypass unresolved prohibitive gates.

The audit specifically demonstrated that retry, review, decision, prerequisite, assignment, routing, and model paths could continue after missing authority. Add direct tests for every normal API.

### 2. Truly atomic validate-then-commit

No governed act may partially mutate phase, posture, gate outcome, record stores, or event log if any validation or append step fails.

The current defect: duplicate evidence identity can raise `AppendOnlyError` only AFTER phase/event mutation.

Refactor so that ALL failure-prone checks occur before any state mutation, including:
- evidence lineage validation;
- adapter result validation;
- duplicate record-id checks;
- record-store capacity/identity checks;
- gate-instance existence/state checks;
- transition validity;
- outcome validity;
- history insertion preflight;
- event construction validity.

Recommended pattern:
- prepare a complete immutable `CommitPlan` / `GovernedMutationPlan` in memory;
- preflight every append and transition against current state without mutating;
- only after all checks pass, apply record appends + gate/state/posture/event changes as one reference-level transaction;
- if this MVP cannot guarantee rollback after an exception, structure the apply phase so it contains no remaining expected validation failures.

Add snapshot-based adversarial tests proving that a duplicate record identity, malformed evidence, bad adapter result, or conflicting history append leaves ALL governed state/history/event counts bit-for-bit equivalent to the pre-call snapshot.

### 3. Router-origin provenance must not be caller-assertable

The audit reproduced a caller-created `RoutingDecision` accepted through `_record_routing_decision()` without Router invocation.

There must be no callable orchestration path by which a caller can inject a Routing Decision merely by matching the configured `RouterRef` and request identifiers.

Use one of these structural approaches:
- keep routing and recording inside one method that invokes the configured Router and records exactly the returned object; or
- use an unforgeable reference-implementation capability/token produced only by the adapter boundary and verified during recording.

Do NOT rely on leading underscore naming as a security/governance boundary.

Required proof:
- caller-created matching RoutingDecision is rejected;
- configured Router invocation count remains authoritative;
- recorded decision is exactly the object returned by the configured Router;
- no public/semipublic method can bypass that provenance check.

### 4. Scope-transfer approval must bind mechanism + version + exact Right + authorized act

Current registry approval is too coarse: mechanism/version/source/target only. The audit showed a retained unrelated Decision Right could authorize a registered crossing.

The mechanism registry / authorization contract must bind at least:
- mechanism identity;
- mechanism version;
- source scope binding;
- target scope binding;
- exact Decision Right required for this transfer class/act;
- authorized act/purpose (e.g. `scope_transfer` or explicit governed action id);
- if useful, workflow/run or policy class where architecture requires it.

`ScopeTransferAuthorisation` must be corroborated against:
- retained Decision Record in source run;
- exact source run/work item/gate requirement;
- exact Decision Right named by the approved mechanism policy;
- human holder of that Right;
- exact source and target bindings;
- sensitivity/residency constraints;
- mechanism version and approved act.

Add negative tests where everything matches except the Decision Right or authorized act; both must fail without mutation.

### 5. ModelResult needs stable identity and Model Profile lineage

Add a stable governed reference for model-result records, e.g. `ModelResultRef`, and include it in `ModelResult`.

A ModelResult must retain and validate at least:
- result ref;
- run;
- work item;
- routing decision;
- selected model;
- selected model profile;
- output origin/canonicality;
- payload/value as already modeled.

`invoke_model()` must verify the result matches the exact recorded Routing Decision including BOTH model and Model Profile selected by the Router.

Append it to a `RecordStore` with duplicate identity rejection.

Required tests:
- duplicate ModelResultRef rejected without any state/history/event mutation;
- foreign model profile rejected;
- same model but wrong profile rejected;
- result from foreign run/work item/routing decision rejected;
- retained result reconstructs the selected model/profile lineage.

### 6. Committed adversarial / mutation assurance

The re-audit explicitly rejected a scratch-only mutation runner and rated harness credibility LOW.

Commit the mutation/adversarial runner under Phase 12, e.g.:
`implementation/phase-12/tests/test_mutation_guards.py`
or a deterministic script under `validation/`.

It must be runnable from the repository without manual source editing and must exercise representative weakening of the load-bearing guards above.

At minimum include mutations/probes for:
- removing common halted-run guard;
- allowing retry after `AUTHORITY_ABSENT`;
- permitting evidence append failure after phase/event mutation;
- allowing caller-injected RoutingDecision;
- removing exact Decision Right binding from scope mechanism approval;
- removing authorized-act binding;
- removing ModelResult stable-id duplicate check;
- removing Model Profile lineage verification;
- allowing duplicate governed evidence identity;
- allowing an externally failed validation to leave a partial mutation.

Each controlled weakening must be detected by either the unit suite or Phase 12 validator, preferably both. Do not claim a mutation is effective if an independent redundant guard makes it observationally inert; classify it honestly.

The runner itself must be committed and the Phase 12 validator must verify its presence and execute or independently verify its assertions.

## Harness and documentation cleanup

Fix inconsistent self-check counts (65 / 118 / 121). The self-check must report only current, reproducible totals.

Update:
- `implementation/phase-12/README.md`
- `reviews/phase-12-foundation-self-check.md`
- `validation/phase_12_validation.py`

Do not change approved Phase 1–11 architecture/orchestration/validators/approval records.

## Required adversarial tests

In addition to existing tests, independently add tests that reproduce the exact v3 findings:

- After missing Decision Right -> `ESCALATED / AUTHORITY_ABSENT`, EACH normal mutation/progression API rejects and leaves snapshots unchanged.
- `retry()` cannot resume halted run.
- review/decision/human-work/prerequisite/assignment/routing/model APIs cannot resume halted run.
- duplicate evidence identity cannot change phase/posture/gate/event count before failing.
- fabricated RoutingDecision with correct request/router identifiers but no Router invocation is rejected.
- unrelated Decision Right cannot authorize an otherwise registered scope crossing.
- wrong authorized-act token cannot authorize crossing.
- ModelResult with duplicate result identity rejected atomically.
- ModelResult with wrong model profile rejected.
- all successful governed evidence remains reconstructable from append-only stores.

## Acceptance criteria

Before reporting READY FOR RE-AUDIT V4, ALL must hold:

- unit tests: all PASS;
- Phase 12 validator default/verbose/JSON: all PASS;
- governed example: exit 0;
- blocked example: exit 0;
- committed mutation/adversarial harness: all expected weakenings detected;
- harness credibility self-assessment: HIGH only if supported by committed executable evidence;
- Phase 11 remains the inherited 159/160 condition only;
- Phase 10 remains inherited 145/147 only;
- Phase 9 277/277 PASS;
- Phase 8 119/119 PASS;
- protected Phase 1–11 files unchanged;
- all Phase 12 artifacts remain PROPOSED;
- no PR.

## Files you may modify

Only Phase 12 implementation/assurance files, expected primarily:
- `implementation/phase-12/domain.py`
- `implementation/phase-12/orchestrator.py`
- `implementation/phase-12/adapters.py`
- `implementation/phase-12/examples/*`
- `implementation/phase-12/tests/*`
- `implementation/phase-12/README.md`
- `validation/phase_12_validation.py`
- `reviews/phase-12-foundation-self-check.md`

Do not touch approved Phase 1–11 architecture semantics.

## Report format

Return exactly sections A–N:

A. REMEDIATION SUMMARY
B. COMMON HALTED-RUN GUARD
C. ATOMIC VALIDATE-THEN-COMMIT
D. ROUTER-ORIGIN PROVENANCE
E. SCOPE RIGHT / ACT PROVENANCE
F. MODEL RESULT IDENTITY / PROFILE LINEAGE
G. APPEND-ONLY HISTORY
H. ADVERSARIAL / MUTATION HARNESS
I. TESTS / VALIDATION
J. REGRESSION
K. FILES CHANGED
L. KNOWN LIMITATIONS
M. COMMIT / PUSH
N. NEXT STEP

The final line may say `READY FOR INDEPENDENT PHASE 12 MVP RE-AUDIT V4` only if the acceptance criteria above are actually met.

Commit with message:
`feat: close Phase 12 halted atomic provenance gaps`

Push to `implementation/phase-12-mvp`. Do not create a PR.
