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

**Current result: `=== 119/119 PASS ===`.** Normal, `--verbose` and `--json` modes all report the same total; exit code 0 on pass, non-zero on any failure.

Neither the earlier 116 nor the 95 figure is carried forward. Each counted a different and weaker suite, and preserving a number would have been preserving the problem. Accuracy over continuity.

**Scope boundary.** These 119 are **offline, deterministic checks over committed content**. Remote repository state — open pull requests, branch protection, review state — is **not provable offline and is not claimed**; it is checked separately against the GitHub API and reported in `reviews/phase-8-foundation-audit-remediation.md`.

| Group | Checks | Covers |
|---|---:|---|
| `scope-graph` | 6 | Line-for-line match against the approved hierarchy read out of git at the Phase 7 baseline; every node present and distinguished; the dual `PROJECT` path; venture/organisation siblinghood |
| `applicability` | 11 | Four modes; declared-not-inferred; mandatory wider constraints unoverridable; override requirements; ancestor fallback per mode; no upward or sideways propagation |
| `personal-isolation` | 9 | Leakage scan across every normative document; separate scope family; association is not ancestry; nothing crosses automatically; reference or transfer only; mandatory constraints do not cross sideways; four stress tests |
| `memory-classes` | 6 | Exactly six declared classes; no live `CANONICAL_MEMORY`; class unchanged by governance state; post-supersession classification; no shortened aliases |
| `ai-origin` | 10 | Origin axis; no type conversion by any actor; new-linked-item adoption; acceptance is not a basis; proposal preserved; upstream compatibility |
| `decision-ids` | 8 | The approved Steward route still resolves; four effect subtypes; non-overlap by construction; every canonical act assigned; nothing carded |
| `state-transitions` | 6 | Transition table parsed for rewinds; rewind phrasing scanned across normative text; withdrawn-level metadata in five documents; new-linked-item rule |
| `freshness` | 9 | Item facts versus use verdicts; `PAST_REFRESH_INTERVAL`; bare `STALE` gone while Phase 6's review status survives; verdicts never stored |
| `materiality` | 7 | One rule across five documents; no "any conflict blocks"; attributable and reviewable; Decision-Grade default |
| `inventory` | 6 | Contiguous constraint numbering; counts derived from files and compared to the universe's claims; stale axis and class claims scanned in normative text |
| `invariants` | 18 | Shortcuts, authority conversion, transfer, absorption, retrieval, overwrite, provenance, transformations, preference, procedural, sensitivity, retention, criticality |
| `regression` | 13 | Phases 3–7 and inherited architecture unchanged; all artifacts `PROPOSED`; inheritance; no runtime; no named parties; harness read-only; no vacuous checks; no local PR action |
| `exemplars` | 10 | Eight discovered on disk; full class names; no class mutation; canonical discovery by Identity block; exactly one declared mode each; exemplar 2 and 3 fixes |

## What the harness caught that prose did not

In the first remediation it returned 83/95 on its first run, and three failures were **genuine defects the prose self-check had reported as passing**: a deleted section of the memory-class model; three constraint rewrites that had silently failed to apply; and the old AI wording surviving in the provenance model.

In the second remediation the strengthened suite caught three of **its own new checks** being wrong, and each was replaced with a stricter correct test rather than relaxed — a transition check that treated legitimate promotion as a rewind, a mode check that counted prose mentions as declarations, and a canonical-discovery regex that missed three exemplars. Full detail is in `reviews/phase-8-foundation-audit-remediation.md`.

## Open questions and findings

Dispositions for all twelve open architecture questions, the remediation of every audit finding, and the deliberately deferred items are in `reviews/phase-8-foundation-audit-remediation.md`.

## Standing statement

Every Phase 8 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, and no approved Phase 3–7 artifact was modified. This record does not claim human approval and is not an independent audit.
