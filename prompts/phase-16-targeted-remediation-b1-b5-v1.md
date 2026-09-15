# Phase 16 Targeted Remediation — B1–B5

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-16-planner-activation`

IMPLEMENTATION / REMEDIATION ONLY.

Do not create a PR.
Do not modify approved Phase 1–15 artifacts, registries, approval records, or Phase 14/15 validators.
Do not create or exercise any Decision Right.
Do not claim production readiness.

## Exact starting baseline

Start from the Phase 16 candidate audited at:

`2271bf2ef72d4563a17f71e9827a718095572405`

The independent review returned exactly five blockers. Remediate these blocker families exhaustively in one pass. Do not redesign unrelated architecture.

## B1 — authoritative registry eligibility

Problem: mention-based parsing invents approval eligibility.

Required outcome:
- stop deriving Role IDs by display-name slugging;
- use authoritative declared IDs from approved sources;
- distinguish approved entries from mentions, candidates, examples, prose references, and uncarded IDs;
- for MATCH, Review Profiles, Decision Rights and Roles, require explicit approval evidence and version/scope evidence where applicable;
- uncarded or unresolved identities fail closed;
- preserve the approved 59-role universe exactly;
- add positive and negative tests for the three misparsed Role IDs called out by review and for uncarded workflow/review/right examples.

Do not silently promote or register anything.

## B2 — material digest completeness

Problem: `material_digest()` omits load-bearing validation/handoff inputs.

Required outcome:
- include every load-bearing input whose change can alter preflight, basis issuance, handoff, authority/review/evidence requirements, or planned-stage semantics;
- specifically include blocking/non-blocking clarifications and their consequence/default semantics, scope ancestry, orchestrator policy reference, stage `expected_artifact`, and any effective binding used by preflight/handoff;
- preserve only explicitly presentation-only exclusions;
- changing any load-bearing field after issuance must make the old basis unusable and require re-preflight/reissuance;
- add direct tests for each omitted field family.

## B3 — basis integrity and issuance

Problem: mutable stored bases and weak trigger integrity allow tampering, cross-request reuse, and never-issued bases.

Required outcome:
- make issued Execution Basis payload effectively immutable, or store immutable snapshots and never expose mutable authoritative state;
- require trigger construction to verify issued-basis existence, exact basis version, exact request/intent identity, planning digest, implementation-spec version, scope, execution mode, workflow/work-plan binding, policy binding, criticality, false authority/approval flags, and status `EXECUTABLE`;
- refuse cross-request reuse even where material digests happen to match;
- refuse never-issued/fabricated bases;
- preserve lineage for STALE/SUPERSEDED/reissued bases;
- add direct tamper/fabrication/cross-request tests.

## B4 — effective composition bindings and uniqueness

Problem: duplicate stage IDs, unregistered stage owners, and unchecked Skill-to-Role bindings pass preflight.

Required outcome:
- stage IDs must be unique before basis issuance;
- every effective stage owner must resolve to an approved Role eligible for the intended participation/owned conclusion;
- every Skill requirement must resolve to an approved Skill and be compatible with its referenced Role according to authoritative mappings;
- unresolved/invalid bindings fail closed before basis issuance;
- planned-spec IDs must remain unique by construction;
- add negative tests for duplicate stage IDs, unregistered owners, wrong-role Skill binding, and unresolved Skill/Role IDs.

## B5 — mutation harness validity

Problem: fixture omits required dependencies and arbitrary nonzero exits are counted as semantic detection.

Required outcome:
- temporary-copy fixture must include all required read-only upstream dependencies;
- pristine copied control must PASS before any mutation result is counted;
- distinguish `DETECTED`, `ESCAPED`, `REDUNDANT`, and `RUNNER_ERROR`;
- arbitrary import/path/runtime failure must be `RUNNER_ERROR`, never `DETECTED`;
- `--json` must emit valid JSON only;
- rerun all committed probes from a valid copied control and report honest totals;
- add at least the review’s escaped semantic cases as probes where practical, but do not chase broad unrelated coverage.

## Required verification

Run and report:
- Phase 16 validator default and `--json`;
- Phase 16 mutation probes `--json` with pristine-copy control;
- Phase 16 unit suite;
- executable and blocked examples;
- `git diff --check`;
- containment against approved upstream artifacts;
- final clean worktree.

Also run a focused semantic sweep across the Phase 16 package for second-location variants of B1–B4. Do not rely only on exact strings.

## Output

Return sections A–M:

A. SUMMARY
B. BASELINE / HEAD / REMEDIATION SHA
C. CHANGED FILES
D. B1 CLOSURE
E. B2 CLOSURE
F. B3 CLOSURE
G. B4 CLOSURE
H. B5 CLOSURE
I. TARGETED TESTS
J. VALIDATOR / MUTATION RESULTS
K. CONTAINMENT
L. REMAINING BLOCKERS
M. VERDICT

If all five blocker families are closed, use exactly:

`READY FOR SHORT INDEPENDENT PHASE 16 B1-B5 CLOSURE REVIEW`

Do not declare Phase 16 approved.
