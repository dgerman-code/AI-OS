# Phase 8 — Memory and Canonical Governance Foundation Self-Check

Status: PROPOSED — READY FOR FINAL INDEPENDENT PHASE 8 RE-AUDIT

Branch: `architecture/phase-8-memory-canonical`
Phase 7 approval-record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`

This is a **self**-check by the producing pass. Under Phase 6's vocabulary it is `PRODUCER_REVIEW` — internal quality control, which cannot satisfy an independent review requirement.

## How this document changed

Version 0.1 of this file asserted **116/116 PASS** in prose, with no committed validation logic. The independent audit rated its credibility **LOW** and was right to: the figure was not reproducible from the repository, and the presence-oriented checks behind it had missed the scope-tree, memory-class, AI-transition, freshness and upstream-ID defects the audit went on to find.

**The prose self-check is replaced by a committed harness.** This file no longer carries results of its own; it points at the tooling that produces them.

## Running the check

```
python3 validation/phase_8_validation.py
```

Python 3 standard library and `git` only. No network, no third-party packages. Deterministic output; exit code 0 when every check passes. `--verbose` prints each check's evidence, `--json` emits machine-readable results. Conventions are in `validation/README.md`.

**Current result: `=== 95/95 PASS ===`.**

The earlier 116 figure is **not carried forward.** It counted a different and weaker suite, and preserving the number would have been preserving the problem. Accuracy over continuity.

| Group | Checks | Covers |
|---|---:|---|
| `scope-graph` | 6 | Line-for-line match against the approved hierarchy read out of git at the Phase 7 baseline; every node present and distinguished; the dual `PROJECT` path; venture/organisation siblinghood |
| `applicability` | 11 | Four modes; declared-not-inferred; mandatory wider constraints unoverridable; override requirements; ancestor fallback per mode; no upward or sideways propagation |
| `memory-classes` | 6 | Exactly six declared classes; no live `CANONICAL_MEMORY`; class unchanged by governance state; post-supersession classification; no shortened aliases anywhere |
| `ai-origin` | 10 | Origin axis; no type conversion by any actor; new-linked-item adoption; acceptance is not a basis; proposal preserved; upstream compatibility |
| `decision-ids` | 8 | The approved Steward route still resolves; four effect subtypes; non-overlap by construction; every canonical act assigned; nothing carded |
| `freshness` | 9 | Item facts versus use verdicts; `PAST_REFRESH_INTERVAL`; bare `STALE` gone while Phase 6's review status survives; verdicts never stored |
| `materiality` | 7 | One rule across five documents; no "any conflict blocks"; attributable and reviewable; Decision-Grade default |
| `invariants` | 18 | Shortcuts, authority conversion, transfer, absorption, retrieval, overwrite, provenance, transformations, preference, procedural, sensitivity, retention, criticality |
| `regression` | 12 | Phases 3–7 and inherited Phase 2/3 architecture unchanged since the baseline; all artifacts `PROPOSED`; inheritance; no runtime; no named parties; no PR |
| `exemplars` | 8 | Eight discovered on disk; full class names; no class mutation; applicability modes; the three remediated exemplar properties |

## What the harness caught that prose did not

On its first run it returned 83/95, and three of the failures were **genuine defects that the prose self-check had reported as passing**: an entire section of the memory-class model deleted by an edit; three constraint rewrites that had silently failed to apply, leaving the standard asserting pre-audit rules; and the old AI wording surviving in the provenance model. Details, and the three check defects replaced with stricter tests, are in `reviews/phase-8-foundation-audit-remediation.md`.

## Open questions and findings

Dispositions for all twelve open architecture questions, the remediation of every audit finding, and the deliberately deferred items are in `reviews/phase-8-foundation-audit-remediation.md`.

## Standing statement

Every Phase 8 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, and no approved Phase 3–7 artifact was modified. This record does not claim human approval and is not an independent audit.
