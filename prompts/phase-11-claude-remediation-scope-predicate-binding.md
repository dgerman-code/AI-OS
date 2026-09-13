# Phase 11 — Scope Predicate-Binding Remediation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`
Current candidate baseline: `0561a2d9d8a2be4d15e20e57f251edf9be39b204`

## Mode

Targeted validator remediation only.

Do **not** change Phase 11 architecture semantics. The committed architecture is correct; the remaining defect is validator enforcement in `no_implicit_scope_crossing()` / `scope_crossing_verdict()`.

Do not create a PR.

## Remaining blocker

Independent re-audit found that scope polarity is still not grammatically attached to the crossing predicate.

These forbidden permissions currently pass because `scope_crossing_verdict()` searches the whole pre-crossing subject region for any prohibitive token and immediately ALLOWs:

- `The orchestrator never waits and may cross a scope boundary.`
- `The run cannot be delayed but may cross a project boundary.`
- `No approval exists, but the orchestrator may cross a scope boundary.`
- `The run may not only log the event but may cross a project boundary.`

The prohibitive wording belongs to another predicate or clause. It must not negate a later permissive modal governing `cross`.

## Required semantic rule

The validator must determine the modality/polarity **attached to the crossing predicate itself**.

A prohibition is ALLOW only when the prohibitive modal governs the crossing verb, e.g.:

- `must not cross ...`
- `cannot cross ...`
- `may not cross ...`
- `is not permitted to cross ...`
- `never cross ...` when `never` directly governs the crossing predicate

A permission is REJECT unless it names an approved mechanism and does not waive it, e.g.:

- `may cross ...`
- `can cross ...`
- `could cross ...`
- `is permitted to cross ...`
- `is allowed to cross ...`

Unrelated prohibitive language earlier in the same sentence/clause must not change the polarity of a later permissive crossing predicate.

Do not solve this with another broad proximity or whole-subject search.

## Implementation requirement

Refactor the scope-crossing analysis so each crossing occurrence is evaluated from its **local modal phrase / predicate span**, not by searching the entire subject prefix.

A narrow deterministic standard-library implementation is sufficient. You do not need a general NLP parser, but the rule must be structurally anchored to the crossing predicate.

Possible acceptable approaches include:

- identify the modal phrase immediately governing the crossing verb;
- evaluate the nearest relevant auxiliary/modal sequence before `cross` within the same local clause;
- explicitly handle multiword forms such as `is not permitted to cross`, `is permitted to cross`, `may not cross`, `cannot cross`;
- split/limit contrastive clause regions so unrelated predicates before `but`, `and`, commas, or separate finite predicates do not leak polarity into `cross`.

Do not weaken existing approved-mechanism logic.

## Mandatory adversarial cases

The following must REJECT:

1. `The orchestrator never waits and may cross a scope boundary.`
2. `The run cannot be delayed but may cross a project boundary.`
3. `No approval exists, but the orchestrator may cross a scope boundary.`
4. `The run may not only log the event but may cross a project boundary.`
5. `The orchestrator does not pause and can cross a scope boundary.`
6. `The run is not blocked and is permitted to cross a project boundary.`
7. `The stage never retries, then may cross a scope boundary.`
8. `The run may cross a scope boundary without an approved mechanism.`
9. `The run can cross a project boundary.`
10. `The stage is permitted to cross a scope boundary.`

The following must ALLOW:

1. `The orchestrator must not cross a scope boundary.`
2. `The run cannot cross a project boundary.`
3. `The stage may not cross a scope boundary.`
4. `The orchestrator is not permitted to cross a project boundary.`
5. `The run never crosses a scope boundary.`
6. `The run may cross a scope boundary only through an approved scope transfer.`
7. `The stage can cross a project boundary through a Phase 6 handoff.`
8. `A cross-scope movement uses an approved mechanism or does not happen.`

Also add independent contrastive variants not copied from this list.

## Self-guard requirement

Add self-guards that prove the validator is binding polarity to the crossing predicate, not merely passing the examples.

At minimum:

- a mutation that restores whole-subject prohibitive search must fail the harness;
- a mutation that ignores permissive modality immediately attached to `cross` must fail;
- a mutation that treats `not only` as prohibiting a later `may cross` must fail;
- a mutation that drops approved-mechanism enforcement must fail;
- drive the **actual document scan**, not only the helper function, with synthetic violating and clean documents.

The prior malformed rendered-text remediation is already fully resolved. Do not alter it except where unavoidable for compilation/tests. Re-run its guards to ensure no regression.

## Full regression

Re-run all prior Phase 11 adversarial suites, including:

- rendered-text / malformed HTML
- stale Decision wording
- negation scope
- specimen fence
- late review / late Decision asymmetry
- authority
- state transitions
- missing Decision Right
- retry / replay / exactly-once
- cross-scope baseline cases
- logs-as-evidence
- Role/Agent collapse
- Router/Orchestrator collapse
- vacuity / `or True`

## Validation

Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected upstream if unchanged:

- Phase 10: `145/147` inherited approval-record-only condition
- Phase 9: `277/277 PASS`
- Phase 8: `119/119 PASS`

Phase 11 total may increase if a new self-guard is added. Update self-check counts only if they genuinely change.

## Regression constraints

Do not modify:

- substantive Phase 1–10 architecture;
- Phase 8/9/10 validators;
- Phase 9/10 approval records;
- Phase 11 architecture semantics under `orchestration/` or `architecture/`.

No runtime, SQL, migrations, Supabase deployment, API/SDK, queues/workers/scheduler/event bus, agents, RAG, credentials/IAM/secrets, or live assignments.

All Phase 11 architecture artifacts remain `PROPOSED`.

Prefer changing only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` if totals/descriptions change

If the blocker cannot be fixed without changing architecture semantics, STOP and report instead of committing.

## Commit

Commit exactly:

`docs: remediate Phase 11 scope predicate binding`

Push to:

`origin architecture/phase-11-orchestrator`

## Response

Return exactly sections A–I:

A. REMEDIATION SUMMARY  
B. SCOPE PREDICATE-BINDING RULE  
C. VALIDATOR REPAIR  
D. CONTROLLED PROBES  
E. VALIDATION  
F. REGRESSION  
G. FILES CHANGED  
H. COMMIT / PUSH  
I. NEXT STEP

Section I exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
