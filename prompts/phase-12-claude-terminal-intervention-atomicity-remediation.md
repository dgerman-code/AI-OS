# Phase 12 — Claude Terminal Intervention Atomicity Remediation

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-12-mvp`

## Mission

Remediate the remaining Phase 12 MVP blocker identified by independent re-audit V5 at baseline `25b6811fdd011e17eab7d49a037349439ff832d0`.

This is a narrow remediation. Do not redesign Phase 12. Do not change approved Phase 1–11 architecture semantics. Do not touch inherited Phase 11 `159/160` or Phase 10 `145/147` validator conditions.

The only blocking family is terminal-path intervention provenance and atomicity, especially cancellation.

## Independent audit finding to close

The V5 audit found that ordinary completion/cancellation paths are not uniformly validate-before-commit:

- a `HumanInterventionRecord` naming another run can be accepted, retained, and used to reach `CANCELLED`;
- a string or arbitrary object can be appended to the intervention store before later attribute access fails;
- therefore malformed or foreign completion interventions can cause both provenance bypass and partial governed mutation;
- committed tests and mutation harness do not currently cover this terminal path;
- mutation documentation counts are inconsistent with the executable manifest.

All other V5 areas passed and must remain intact: assignment atomicity, pause atomicity, scope-transfer atomicity, route atomicity, halted-run governance, Router provenance, model/profile lineage, scope Right/act provenance, retry/completion gating, append-only history on ordinary paths, and containment.

## Required remediation

### 1. One intervention validation contract

Use a single read-only intervention validation path for every API that consumes a `HumanInterventionRecord`, including at minimum:

- `pause()`;
- `unblock()`;
- ordinary intervention recording;
- terminal paths such as cancellation / termination / other completion outcomes that accept an intervention.

The validation contract must reject, before any mutation:

- wrong object type;
- missing/invalid stable intervention identity;
- duplicate stable identity;
- foreign run lineage;
- invalid human authority reference;
- any other governed field mismatch already required by the domain model.

Do not create a terminal-specific weaker validator.

### 2. Validate before any terminal mutation

For cancellation, termination, or any terminal completion path that accepts an intervention, every refusal-capable check must run before:

- appending intervention history;
- appending an event;
- changing phase;
- changing posture;
- setting terminal outcome;
- mutating gates or any other governed store.

The required pattern is:

`construct/receive -> validate type/lineage/identity -> validate_add/preflight -> preflight terminal/phase plan -> commit history + events + terminal state`

No rollback-on-exception implementation. Use validate-then-commit.

### 3. Atomic failure invariant

For every malformed/foreign/duplicate terminal intervention, snapshot the full observable governed state before the call and require exact equality afterwards, including at least:

- phase;
- terminal outcome;
- governance posture;
- wait reason if present;
- gate outcomes;
- intervention history;
- all other record stores;
- event count/content;
- attempt counters and run-created references where applicable.

### 4. Cross-run provenance

A `HumanInterventionRecord` naming run B must never be usable to cancel, terminate, complete, pause, or unblock run A.

The record must remain absent from run A history after refusal.

### 5. Stable identity / append-only semantics

Duplicate intervention identity must be rejected before any dependent mutation on all paths, including cancellation/termination.

Append-only semantics must hold consistently across ordinary and terminal paths.

### 6. Terminal-path coverage

Add committed adversarial tests covering at minimum:

- foreign-run intervention supplied to cancellation;
- string/non-`HumanInterventionRecord` supplied to cancellation;
- arbitrary object supplied to cancellation;
- duplicate intervention identity supplied to cancellation;
- malformed human authority reference if construction/API permits it;
- valid cancellation still succeeds;
- valid termination (if distinct) still succeeds;
- no valid terminal path regresses.

If there are multiple terminal methods or terminal outcomes sharing one helper, test at least one negative and one positive case through each distinct supported public path.

### 7. Mutation harness

Extend `implementation/phase-12/tests/test_mutation_guards.py` with controlled weakening(s) that recreate the V5 blocker, for example:

- move terminal intervention append before validation;
- bypass foreign-run lineage validation on completion;
- bypass duplicate-identity preflight on terminal intervention.

Each weakening must be non-vacuous and classified from executable behavior. Missing mutation target must fail loudly.

Fix the producer self-check / README mutation counts so they exactly match the executable manifest. Do not claim more DETECTED mutations than actually exist.

### 8. Validator

Extend `validation/phase_12_validation.py` so it independently verifies:

- malformed and foreign cancellation interventions cause zero observable mutation;
- duplicate terminal intervention identity is atomic;
- the named regression tests exist and execute through `unittest`, not merely grep;
- mutation manifest counts and documented counts agree;
- a controlled weakening of terminal intervention validation is detected.

Avoid fragile source-string-only assertions where behavioral checks are possible.

## Required regression preservation

Keep byte-identical all protected Phase 1–11 artifacts and validators relative to the already-approved baseline where required by existing Phase 12 validation.

Do not repair inherited:

- Phase 11 `159/160`;
- Phase 10 `145/147`.

Phase 9 must remain `277/277`; Phase 8 must remain `119/119`.

Phase 12 artifacts remain `PROPOSED`.

Do not create a PR.

## Scope constraints

Remain an in-memory, standard-library reference implementation.

Do not add:

- Supabase or database integration;
- SQL or migrations;
- queues/workers/schedulers/event buses;
- provider SDKs or live LLM calls;
- secrets/IAM/deployment;
- agents/daemons;
- production persistence;
- distributed transaction or exactly-once claims.

Do not expand this remediation into production infrastructure.

## Required validation commands

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

Also run the committed mutation/adversarial harness exactly as the repository defines it.

## Required output

Return sections A–N:

A. REMEDIATION SUMMARY  
B. TERMINAL INTERVENTION VALIDATION  
C. CANCELLATION / TERMINATION ATOMICITY  
D. CROSS-RUN PROVENANCE  
E. APPEND-ONLY / DUPLICATE IDENTITY  
F. TESTS ADDED  
G. MUTATION HARNESS  
H. VALIDATOR CHANGES  
I. VALIDATION RESULTS  
J. UPSTREAM REGRESSION  
K. FILES CHANGED  
L. KNOWN LIMITATIONS  
M. COMMIT / PUSH  
N. NEXT STEP

If and only if the V5 blocker is genuinely closed and all required regressions pass, end section N with exactly:

`READY FOR INDEPENDENT PHASE 12 MVP RE-AUDIT V6`

Do not claim Phase 12 APPROVED or CANONICAL.