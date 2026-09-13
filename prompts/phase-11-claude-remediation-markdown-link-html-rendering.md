# Phase 11 — Targeted Validator Remediation: Markdown Link / Inline HTML Rendering

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`

## Context

The latest independent approval re-audit found one remaining MEDIUM validator defect. The committed Phase 11 architecture semantics are correct, but the stale-Decision invariant can still be bypassed when Markdown links or inline HTML split the rendered subject.

Required audited baseline for this remediation:

`88a2b60656b55d2caa6d33a59314cd238e2be51e`

Do not redesign Phase 11. This is a single-defect validator remediation only.

## Defect to remediate

The validator correctly normalizes inline code, `*`, `_`, `**`, `__`, and `~~`, but these rendered-equivalent assertions currently pass:

- `The Decision [Record](#term) is stale.`
- `The Decision <em>Record</em> is stale.`
- `The Decision <code>Record</code> is stale.`

Formatting/rendering must not alter the semantic reading of the governed phrase `Decision Record` or the stale predicate.

## Required semantic rule

For this invariant, the validator must evaluate **rendered semantic text**, not raw Markdown delimiters.

A prose assertion that characterises a Decision Record as stale must be rejected regardless of supported inline presentation wrappers.

At minimum, normalisation must preserve visible/semantic text while removing or bridging:

- existing inline code markers;
- `*`, `_`, `**`, `__`, `~~`;
- Markdown inline links `[visible text](target)` — preserve `visible text`, discard only link destination syntax;
- inline HTML tags that wrap text, including at minimum `<em>...</em>`, `<strong>...</strong>`, `<code>...</code>`, `<span>...</span>` — preserve inner text, remove tags only.

Do not treat formatting itself as an exemption.

The only exemption remains the explicit `stale-specimen` fence in allowed review records. Do not widen it.

Do not alter the shared general `plain()` helper unless strictly necessary. Prefer a narrowly-scoped semantic normalizer for this invariant, as already established.

## Required negative probes

All must fail validation when inserted as assertions in Phase 11 architecture prose:

1. `The Decision [Record](#term) is stale.`
2. `The [Decision Record](#term) is stale.`
3. `The Decision Record is [stale](#status).`
4. `The Decision <em>Record</em> is stale.`
5. `The Decision <strong>Record</strong> is stale.`
6. `The Decision <code>Record</code> is stale.`
7. `The Decision <span>Record</span> is stale.`
8. `The <em>Decision</em> <code>Record</code> is <strong>stale</strong>.`
9. A mixed Markdown+HTML+inline-code form that renders to `The Decision Record is stale.`

Also test the authoritative late-Decision race-row reading path with at least one link-wrapped and one HTML-wrapped variant. Those must fail too.

## Positive controls

These must continue to pass:

- `The Decision Record is not stale.`
- formatted attached negation, e.g. `The <em>Decision Record</em> is not <code>stale</code>.`
- unrelated stale evidence;
- benign Markdown links / inline HTML that do not assert a stale Decision Record;
- late-review `IGNORE_AS_STALE`, still recorded against its Review Instance;
- explicit `stale-specimen` fence in an allowed review record;
- controlled vocabulary such as `IGNORE_AS_STALE`, `NON_RETRYABLE_GOVERNED_ACT`, `GOVERNANCE_CLEAR` survives the invariant-specific normalization unchanged.

## Self-guard requirements

Do not only add phrase examples. Guard the reading path itself.

Add deterministic self-tests proving that:

- Markdown links preserve visible text and drop only destination syntax;
- inline HTML tags are removed while inner text is preserved;
- nested/mixed wrappers cannot split `Decision Record` or `stale`;
- both the Phase-11-wide scan and `race_row_cells()` consume the same semantic-normalized text path;
- restoring raw Markdown reading for either path fails the harness;
- removing link normalization fails the harness;
- removing inline-HTML normalization fails the harness;
- widening specimen treatment to ordinary formatting fails the harness.

Use Python standard library only. No external Markdown/HTML parser dependency.

## Regression requirements

Re-run all prior Phase 11 negative/positive suites, including:

- stale wording;
- contrastive negation;
- inline-code;
- emphasis / strong / strikethrough;
- specimen fences;
- authoritative-row reading-path weakening;
- code-span deletion weakening;
- broad-negation weakening;
- vacuity / `or True` probe;
- foundation adversarial probes.

Also run:

- `python3 validation/phase_11_validation.py`
- `python3 validation/phase_11_validation.py --verbose`
- `python3 validation/phase_11_validation.py --json`
- `python3 validation/phase_10_validation.py` — expected inherited `145/147`; do not repair here
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_8_validation.py`

## Hard boundaries

Do NOT:

- change Phase 1–10 architecture semantics;
- change Phase 10 validator;
- change Phase 9/10 approval records;
- redesign Phase 11 architecture;
- alter Decision Right semantics;
- introduce runtime, SQL, migrations, Supabase deployment, API, SDK, queues, workers, scheduler, agents, RAG, secrets, credentials, IAM, or live assignments;
- create a PR.

All Phase 11 architecture artifacts remain `PROPOSED`.

If any `orchestration/` or `architecture/` content would need semantic alteration to make the validator pass, STOP and report instead of committing.

## Files expected to change

Prefer only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` only if totals/group counts or self-check description must change

## Commit / push

Commit exactly:

`docs: remediate Phase 11 rendered-text validation`

Push to:

`origin architecture/phase-11-orchestrator`

No PR.

## Required response format

Return exactly these sections:

### A. REMEDIATION SUMMARY
### B. RENDERED-TEXT SEMANTIC RULE
### C. VALIDATOR REPAIR
### D. CONTROLLED PROBES
### E. VALIDATION
### F. REGRESSION
### G. FILES CHANGED
### H. COMMIT / PUSH
### I. NEXT STEP

Section I must be exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
