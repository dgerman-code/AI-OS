# Phase 11 — Claude Targeted Remediation: Markdown Inline Formatting Bypass

Repository: `dgerman-code/AI-OS`

Branch: `architecture/phase-11-orchestrator`

Current approved-for-remediation baseline to build on:
`bafad72b1a290139a9ca5650ee2755979ccd1957`

## Mode

TARGETED REMEDIATION ONLY.

Do not redesign Phase 11. Do not modify substantive architecture semantics. Do not create runtime, SQL, migrations, APIs, SDKs, queues, workers, schedulers, agents, RAG, credentials, IAM, secrets or deployment artifacts. Do not touch the Phase 10 validator or approval record. Keep all Phase 11 architecture artifacts `PROPOSED`. Do not create a PR.

## Independent re-audit finding to close

The final human-approval re-audit found that inline-code, negation-scope and specimen-fence defects are resolved, but one Markdown-formatting bypass remains in the Phase-11-wide stale-Decision invariant.

The following forbidden architecture assertions currently pass validation because emphasis/strikethrough markers can split the governed subject `Decision Record`:

- `The Decision *Record* is stale.`
- `The Decision _Record_ is stale.`
- `The Decision ~~Record~~ is stale.`

This is a validator/harness defect, not an architecture defect.

## Required semantic rule

Formatting is not semantics.

Any prose assertion that characterises a Decision Record as stale MUST be rejected regardless of supported Markdown inline formatting around or within its semantic tokens.

At minimum the validator must treat these as semantically equivalent and reject them:

- `The Decision Record is stale.`
- `The Decision *Record* is stale.`
- `The Decision _Record_ is stale.`
- `The Decision **Record** is stale.`
- `The Decision ~~Record~~ is stale.`
- `The *Decision Record* is stale.`
- `The _Decision Record_ is stale.`
- `The ~~Decision Record~~ is stale.`
- `The Decision Record is *stale*.`
- `The Decision Record is _stale_.`
- `The Decision Record is ~~stale~~.`
- Mixed forms that split multiple tokens, e.g. `The *Decision* _Record_ is ~~stale~~.`

The same invariant continues to apply across the already-fixed inline-code cases.

## Positive controls that MUST remain valid

Do not over-normalise semantic content or create false positives. At minimum preserve:

- `The Decision Record is not stale.`
- formatting variants of attached negation, e.g. `The *Decision Record* is not _stale_.`
- stale evidence unrelated to a Decision Record;
- late-review `IGNORE_AS_STALE` while retained against its Review Instance;
- explicit `stale-specimen` fences where already permitted in review records;
- ordinary Markdown formatting that does not make a stale-Decision assertion.

## Implementation requirements

1. Fix the normalisation path so all supported Markdown inline-formatting markers relevant to committed Phase 11 Markdown cannot split or hide semantic tokens.
2. Preserve enclosed text; remove/bridge formatting markers only. Never delete semantic content.
3. At minimum cover:
   - backticks / inline code;
   - `*...*` emphasis;
   - `_..._` emphasis;
   - `**...**` strong emphasis;
   - `__...__` strong emphasis;
   - `~~...~~` strikethrough.
4. Handle mixed/nested formatting conservatively enough that formatting cannot provide a bypass.
5. Preserve the explicit `stale-specimen` semantic fence; do not convert ordinary Markdown into an exemption.
6. Do not reintroduce proximity-based negation suppression, line-wide denial suppression, or code-span deletion.
7. Do not alter the authoritative late-Decision architecture row merely to satisfy the validator.

If you discover that the current shared `plain()` normaliser is used broadly and changing it would risk unrelated validators, prefer a narrowly scoped semantic normalisation helper for this invariant rather than a broad risky rewrite. Architecture correctness is more important than convenience.

## Self-guard requirements

Extend the committed validator so future regressions are caught without editing architecture documents.

Add self-guard cases covering, at minimum:

- `*Record*`
- `_Record_`
- `**Record**`
- `__Record__`
- `~~Record~~`
- formatted whole subject (`*Decision Record*`, `_Decision Record_`, `~~Decision Record~~`)
- formatted predicate (`*stale*`, `_stale_`, `~~stale~~`)
- mixed formatting across subject and predicate;
- existing inline-code variants;
- positive attached-negation formatting controls.

A weakening that stops normalising any one of those supported marker classes must cause a non-zero validator exit.

## Controlled probes

After repair, run and revert mutations proving:

1. `The Decision *Record* is stale.` -> non-zero
2. `The Decision _Record_ is stale.` -> non-zero
3. `The Decision **Record** is stale.` -> non-zero
4. `The Decision __Record__ is stale.` -> non-zero
5. `The Decision ~~Record~~ is stale.` -> non-zero
6. `The *Decision Record* is stale.` -> non-zero
7. `The Decision Record is *stale*.` -> non-zero
8. mixed formatted subject + stale predicate -> non-zero
9. formatted attached negation (`The *Decision Record* is not _stale_.`) -> PASS
10. unrelated stale evidence with formatting -> PASS
11. late-review `IGNORE_AS_STALE` retained against Review Instance -> PASS
12. explicit allowed review specimen fence -> PASS

Then rerun all prior controlled suites already used in Phase 11 remediation:

- stale-wording probes;
- contrastive-negation probes;
- inline-code probes;
- specimen-fence probes;
- code-span deletion regression;
- broad specimen regression;
- broad negation regression;
- twelve foundation probes;
- vacuity / `or True` probe.

Every negative mutation must fail for the intended reason and be reverted.

## Validation required

Run:

- `python3 validation/phase_11_validation.py`
- `python3 validation/phase_11_validation.py --verbose`
- `python3 validation/phase_11_validation.py --json`
- `python3 validation/phase_10_validation.py`
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_8_validation.py`

Phase 10's inherited 145/147 approval-record-only defect must remain unchanged and must NOT be fixed in this task.

## Regression requirements

Confirm explicitly:

- no substantive Phase 1–10 architecture changes;
- no Phase 8/9/10 validator changes;
- no Phase 9/10 approval-record changes;
- no `orchestration/` or `architecture/` content changes unless strictly unavoidable — and if any are changed, STOP and report instead of committing;
- no runtime/infrastructure introduced;
- all Phase 11 architecture artifacts remain `PROPOSED`;
- no PR created.

## Commit / push

Commit exactly:

`docs: remediate Phase 11 Markdown formatting validation`

Push to:

`origin architecture/phase-11-orchestrator`

## Required response format

Return sections exactly A–I:

### A. REMEDIATION SUMMARY
### B. MARKDOWN-FORMATTING SEMANTIC RULE
### C. VALIDATOR REPAIR
### D. CONTROLLED PROBES
### E. VALIDATION
### F. REGRESSION
### G. FILES CHANGED
### H. COMMIT / PUSH
### I. NEXT STEP

Section I must say `READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT` only if the remediation is committed, pushed, the working tree is clean, and all required checks/probes pass.