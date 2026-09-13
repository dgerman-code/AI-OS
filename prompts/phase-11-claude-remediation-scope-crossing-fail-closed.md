# Phase 11 — Scope Crossing Fail-Closed Remediation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`

Current candidate baseline:
`04065b0df558477d592cf66bcb7e5b32ac1de264`

## MODE

REMEDIATION ONLY.

Do not change Phase 11 architecture semantics.
Do not modify substantive Phase 1–10 architecture.
Do not modify Phase 8/9/10 validators or Phase 9/10 approval records.
No runtime, SQL, migration, Supabase deployment, API, SDK, queue, worker, scheduler, event bus, agent, RAG, credential, IAM, secret, live assignment, or PR.

Phase 11 remains `PROPOSED`.

## AUDIT FINDING TO FIX

The current scope validator still relies on enumerating permission/prohibition phrasings.

Two classes remain:

### False negatives — unauthorized crossing can pass

Examples that currently pass because the permission phrase falls into `NEUTRAL` and then borrows a mechanism from a neighbouring clause:

- `An approved mechanism exists, and the orchestrator is hereby permitted to cross a scope boundary.`
- `A Phase 6 handoff is discussed, but the run has permission to cross a scope boundary.`

### False positives — genuine prohibitions fail

Examples:

- `The run must under no circumstances cross a project boundary.`
- `The run is forbidden to cross a project boundary.`
- `The run can't cross a project boundary.`

The remaining problem is not architecture semantics. It is that the validator still tries to fully classify English modal wording before deciding whether scope crossing is governed.

## REQUIRED DESIGN CHANGE

Do **not** add another ever-growing list of permissive phrases and then keep the existing `NEUTRAL` borrowing rule.

Make the scope validator **fail closed** around the actual governance invariant:

> Any clause that positively asserts, permits, authorizes, or describes a scope crossing must name an approved Phase 6 / Phase 8 crossing mechanism in that crossing clause. A clause that explicitly prohibits the crossing may stand without naming a mechanism. A mechanism mentioned only in a neighbouring clause or elsewhere in the sentence cannot satisfy the crossing clause.

This means the validator does not need to recognize every possible English permission synonym in order to remain safe.

### Enforcement rule

For each detected crossing occurrence:

1. Determine the crossing's own clause.
2. If the crossing clause is an explicit prohibition of that crossing predicate, ALLOW.
3. Otherwise, require an approved mechanism in the crossing's own clause.
4. If the clause explicitly dispenses with / waives / lacks that mechanism, REJECT even if a mechanism is named elsewhere.
5. Never allow a crossing merely because a mechanism appears in a neighbouring clause or earlier sentence fragment.
6. Unknown / unrecognized modal wording must therefore fail closed unless the crossing clause itself names the approved mechanism.

The diagnostic classifier may still return labels such as PROHIBITED / PERMITTED / NEUTRAL / UNKNOWN, but **UNKNOWN must not become a permissive escape hatch**.

## PROHIBITION ATTACHMENT

You still need a robust predicate-local prohibition detector so genuine prohibitions are not false positives.

It must cover at minimum these attached forms:

- `must not cross`
- `must never cross`
- `must under no circumstances cross`
- `cannot cross`
- `can't cross`
- `can not cross`
- `may not cross`
- `may never cross`
- `shall not cross`
- `will not cross`
- `would not cross`
- `is not permitted to cross`
- `is not allowed to cross`
- `is forbidden to cross`
- `is prohibited from crossing`
- `is barred from crossing`
- `never crosses`

Unrelated prohibitive wording elsewhere in the sentence must not attach to the crossing predicate.

Examples that MUST still be REJECTED unless their own crossing clause names an approved mechanism:

- `The orchestrator never waits and may cross a scope boundary.`
- `The run cannot be delayed but may cross a project boundary.`
- `No approval exists, but the orchestrator may cross a scope boundary.`
- `The run may not only log the event but may cross a project boundary.`

## REQUIRED FALSE-NEGATIVE PROBES

The following must be rejected if the crossing clause itself does not name an approved mechanism:

- `An approved mechanism exists, and the orchestrator is hereby permitted to cross a scope boundary.`
- `A Phase 6 handoff is discussed, but the run has permission to cross a scope boundary.`
- `The run is authorized to cross a project boundary.`
- `The stage has authority to cross a scope boundary.`
- `The orchestrator is free to cross a project boundary.`
- `The run is entitled to cross a scope boundary.`
- `The stage may lawfully cross a project boundary.`
- an unfamiliar/unsupported permission paraphrase chosen by you, without mechanism in its own clause.

The purpose is to prove that an unrecognized permission phrase cannot fall into a permissive `NEUTRAL` branch.

## REQUIRED TRUE-PROHIBITION CONTROLS

These must be accepted as prohibitions without requiring a mechanism:

- `The run must under no circumstances cross a project boundary.`
- `The run is forbidden to cross a project boundary.`
- `The run can't cross a project boundary.`
- `The run is prohibited from crossing a project boundary.`
- `The run is barred from crossing a project boundary.`
- `The run may never cross a project boundary.`

## REQUIRED GOVERNED-CROSSING CONTROLS

These must be accepted because the crossing's own clause names its mechanism:

- `The run may cross a project boundary through an approved scope transfer.`
- `The stage may cross the scope boundary via a Phase 6 handoff.`
- `A cross-scope movement uses an approved mechanism or does not happen.`

These must be rejected because the mechanism belongs to another clause:

- `An approved mechanism exists, and the orchestrator may cross a scope boundary.`
- `The orchestrator may cross a scope boundary, and an approved mechanism is recorded elsewhere.`
- `A Phase 6 handoff is available, but the stage is allowed to cross a project boundary.`

## SELF-GUARDS

Do not guard only phrase examples.

Add self-guards proving the enforcement structure:

1. unknown/unrecognized crossing modality without mechanism in its own clause is REJECTED;
2. an approved mechanism in a neighbouring clause cannot satisfy the crossing clause;
3. attached prohibition can exempt only that same crossing predicate;
4. unrelated prohibition before a later crossing cannot exempt it;
5. weakening the own-clause mechanism requirement fails the harness;
6. weakening predicate-local prohibition attachment fails the harness;
7. reverting UNKNOWN/NEUTRAL to sentence-wide mechanism borrowing fails the harness;
8. the real document scan is exercised, not only helper functions.

## REGRESSION

Re-run all prior Phase 11 suites, including:

- malformed/rendered text
- stale Decision wording
- late review / late Decision asymmetry
- negation-scope
- specimen fence
- state machine
- authority
- missing Decision Right
- retry/replay/exactly-once
- logs-as-evidence
- Role/Agent separation
- Router/Orchestrator separation
- cross-scope historical probes
- vacuity / `or True`

## VALIDATION

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

Phase 11 total may increase if a genuinely new self-guard is added. If so, update the Phase 11 self-check honestly.

## FILE SCOPE

Prefer changing only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` only if totals/descriptions genuinely change

If a correct fix would require changing Phase 11 architecture semantics, STOP and report instead of committing.

## COMMIT

Commit exactly:

`docs: remediate Phase 11 fail-closed scope crossing validation`

Push to:

`origin architecture/phase-11-orchestrator`

Do not create a PR.

## RESPONSE

Return exactly sections A–I:

A. REMEDIATION SUMMARY
B. FAIL-CLOSED SCOPE-CROSSING RULE
C. VALIDATOR REPAIR
D. CONTROLLED PROBES
E. VALIDATION
F. REGRESSION
G. FILES CHANGED
H. COMMIT / PUSH
I. NEXT STEP

Section I exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
