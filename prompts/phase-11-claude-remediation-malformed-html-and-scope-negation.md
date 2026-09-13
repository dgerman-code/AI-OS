# Phase 11 — targeted remediation: malformed rendered-text opener + scope-negation validator

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`
Baseline defect audit: `0695b1be013e9933c5a36cefef8590a6f2befb1d`

Mode: TARGETED REMEDIATION ONLY. Do not redesign Phase 11 architecture. Keep all active Phase 11 architecture artifacts `PROPOSED`. Do not modify substantive Phase 1–10 architecture, Phase 8/9/10 validators, or Phase 9/10 approval records. No runtime, SQL, migrations, API/SDK, queues/workers/schedulers/event bus, agents, RAG, secrets/IAM, deployment, live assignments, or PR.

The independent audit found exactly two validator blockers. Fix both and nothing else.

## Blocker 1 — malformed HTML opener can consume visible content in full-document path

The committed architecture is correct. The validator is not.

A malformed opener such as a partial `<em` token placed before visible text can be interpreted by the full-document rendering path as part of a later tag because `_tag_closes()` scans too far forward for a closing `>`.

Required semantic rule:

- malformed presentation syntax must never hide visible semantic content;
- the bounded race-row path and full-document path must produce equivalent rendered semantic text for the same malformed sample;
- a malformed opener must be neutralised locally, not allowed to consume arbitrarily later text;
- do not regress correctly handled quoted attributes, comments, entities, nested Markdown links, emphasis, inline code, specimen fences, or controlled vocabulary.

Implement this structurally. Do not add a phrase-specific regex patch.

Add self-guards that fail if:

1. a malformed opener before visible words is allowed to consume later content in a full document;
2. the same malformed sample yields different semantic text through document and race-row paths;
3. quoted `>` or `<` inside a valid attribute is misclassified as malformed;
4. an unterminated comment or opener drops visible words after the marker.

Required negative probes include at least two malformed-opener placements in full architecture prose and at least one through `race_row_cells()`.

## Blocker 2 — scope-crossing guard misreads negation

The architecture correctly requires an approved Phase 6/8 mechanism for cross-scope movement. The validator incorrectly treats the phrase `approved mechanism` as sufficient even when the sentence says the orchestrator may cross scope *without* an approved mechanism.

Fix `no_implicit_scope_crossing()` so negated/contrastive permission does not pass by substring coincidence.

Required rule:

- an explicit statement allowing cross-scope movement without the approved mechanism must fail;
- merely containing the words `approved mechanism` is not enough;
- direct prohibitions such as `must not cross ... without an approved mechanism` remain allowed;
- legitimate architecture wording describing approved scope-transfer/handoff mechanisms remains allowed.

Prefer bounded deterministic clause/predicate-aware matching over generic substring checks.

Add self-guards covering at minimum:

- `may cross ... without an approved mechanism` => reject;
- `can cross ... without an approved mechanism` => reject;
- `is permitted to cross ... without an approved mechanism` => reject;
- `must not cross ... without an approved mechanism` => allow;
- `cannot cross ... without an approved mechanism` => allow;
- legitimate approved Phase 6/8 crossing wording => allow.

## Regression requirements

Re-run all previous Phase 11 adversarial suites, including:

- stale-wording variants;
- unrelated-negation and attached-negation controls;
- inline code;
- emphasis/strong/strikethrough;
- Markdown inline and reference links;
- inline HTML, comments, entities, quoted attributes, nested link destinations;
- specimen fence restrictions;
- authoritative-row reading path;
- malformed rendered-text cases;
- cross-scope mutations;
- foundation probes including timeout-as-approval, WAITING→COMPLETED, completion without governance clear, missing Decision Right continuation, governed-act autoretry, exactly-once, log-as-evidence, Role/agent collapse, Router/Orchestrator collapse, and vacuous `or True`.

Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected upstream only if independently reproduced:

- Phase 10: `145/147` inherited approval-record-only condition;
- Phase 9: `277/277 PASS`;
- Phase 8: `119/119 PASS`.

Update Phase 11 totals and self-check only if they genuinely change.

Preferred changed files only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` if needed.

If either blocker cannot be fixed without changing architecture semantics, STOP and report instead of committing.

Commit exactly:

`docs: remediate Phase 11 malformed rendering and scope validation`

Push to `origin/architecture/phase-11-orchestrator`. No PR.

Return exactly sections A–I:

A. REMEDIATION SUMMARY
B. MALFORMED RENDERED-TEXT RULE
C. SCOPE-NEGATION RULE
D. VALIDATOR REPAIR / CONTROLLED PROBES
E. VALIDATION
F. REGRESSION
G. FILES CHANGED
H. COMMIT / PUSH
I. NEXT STEP

Section I exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
