# Phase 11 — Targeted remediation: inline-code stale Decision bypass

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`

## Context

The final human-approval re-audit reports that all prior negation-scope findings are resolved and the committed Phase 11 architecture is correct. One MEDIUM validator defect remains:

The Phase-11-wide stale-Decision invariant can be bypassed because the validator removes inline code spans before matching. As a result, prose assertions such as:

- `The Decision Record is `stale`.`
- `The Decision `Record` is stale.`

incorrectly pass the Phase 11 validator.

Inline code formatting does **not** itself prove that text is a quoted, denied, hypothetical or rejected specimen.

## Task

Perform a **single-defect validator remediation only**. Do not redesign or edit Phase 11 architecture semantics.

Repair `validation/phase_11_validation.py` so that the Phase-11-wide invariant still detects a stale characterisation of a Decision Record when Markdown inline-code formatting splits or wraps relevant words.

### Required rule

Formatting is not semantics.

A prose assertion that a Decision Record is stale must be rejected whether the relevant tokens are plain text or wrapped/split by inline Markdown code spans.

The validator must reject at minimum:

- `The Decision Record is stale.`
- `The Decision Record is `stale`.`
- `The Decision `Record` is stale.`
- `The `Decision Record` is stale.`
- `The `Decision` `Record` is `stale`.`
- `The Decision Record was deemed `stale`.`
- `This is a stale `Decision Record`.`

The validator must still allow genuinely non-assertive specimens when they are explicitly marked as such by surrounding semantics, not merely because they are in code formatting. Do **not** rely on deleting all inline code spans.

Preserve all earlier guarantees:

- late Decision Record stands in governed history;
- current-state handling requires `RECONCILE` and/or `ESCALATE`;
- late Decision Record itself may not be characterised as stale;
- direct predicate-attached negation such as `Decision Record is not stale` remains valid;
- unrelated earlier negation must not suppress a later positive stale characterisation;
- late review keeps the intentional `IGNORE_AS_STALE` asymmetry and remains recorded against its Review Instance;
- stale evidence unrelated to a Decision Record remains valid;
- authoritative late-Decision race-row rules remain unchanged;
- architecture content under `orchestration/` and `architecture/` must remain byte-for-byte unchanged unless an unavoidable validator-only reference update is required (prefer none).

## Implementation constraints

- Fix the validator, not the architecture.
- Remove or narrow the `prose_only()` / inline-code deletion behaviour for this invariant so formatting cannot hide an assertion.
- If you normalize Markdown for matching, normalize formatting markers while preserving the semantic text.
- Add deterministic self-guard cases proving that inline-code formatting cannot bypass either the row-scoped or Phase-11-wide stale-Decision detection.
- The self-guard must fail if the old `QUOTED_SPECIMEN`-style deletion behaviour is reintroduced.
- Python standard library only.
- Do not change Phase 10 validator or approval files.
- Do not add runtime, SQL, Supabase deployment, APIs, SDKs, queues, workers, schedulers, agents, RAG, credentials, IAM, secrets or live assignments.
- All Phase 11 artifacts remain `PROPOSED`.
- Do not create a PR.

## Controlled probes

Run and report at least the following negative probes, reverting each mutation after execution:

1. Phase-wide prose: `The Decision Record is `stale`.` → non-zero.
2. Phase-wide prose: `The Decision `Record` is stale.` → non-zero.
3. Phase-wide prose: `The `Decision Record` is stale.` → non-zero.
4. Phase-wide prose: `The `Decision` `Record` is `stale`.` → non-zero.
5. Phase-wide prose: `The Decision Record was deemed `stale`.` → non-zero.
6. Phase-wide prose: `This is a stale `Decision Record`.` → non-zero.
7. Re-run all previous contrastive-negation probes → non-zero.
8. Re-run all previous stale-wording probes → non-zero.
9. Re-run all twelve foundation probes → non-zero.
10. Reintroduce the old inline-code deletion behaviour or equivalent semantic weakening → self-guard must fail.

Positive controls must still pass:

- `The Decision Record is not stale.`
- retained Decision Record + `RECONCILE` + `ESCALATE` without stale characterisation;
- unrelated stale evidence;
- late review `IGNORE_AS_STALE`, retained against Review Instance;
- inline code that is not making a stale-Decision assertion.

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

The Phase 10 result may remain the known inherited `145/147` approval-record-only condition. Do not remediate Phase 10 here.

## Documentation

Append a concise targeted remediation record to the existing Phase 11 remediation review file or create a narrowly named review record if cleaner. Do not rewrite prior audit history.

## Commit / push

Commit exactly:

`docs: remediate Phase 11 inline-code stale validation`

Push to:

`origin architecture/phase-11-orchestrator`

No PR.

## Return format

Return exactly these sections:

### A. REMEDIATION SUMMARY
### B. INLINE-CODE SEMANTIC RULE
### C. VALIDATOR REPAIR
### D. CONTROLLED PROBES
### E. VALIDATION
### F. REGRESSION
### G. FILES CHANGED
### H. COMMIT / PUSH
### I. NEXT STEP

Section I must state either:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`

or clearly identify the remaining blocker.
