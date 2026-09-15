# Phase 16 Targeted Remediation — Remaining B1/B3/B4/B5 Survivors

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-16-planner-activation`

This is a TARGETED REMEDIATION only.

Do not redesign Phase 16. Do not reopen B2. Do not modify approved Phase 1–15 artifacts, registries, approval records, Phase 14/15 histories, or the Communication Specialist package. Do not create or map Decision Rights. Do not create a PR.

The exact immutable baseline reviewed by Codex was:

`2197fd37da466726b103501e7d74bbdd920e8463`

The independent closure review found exactly four remaining blocker families. Fix all four in one pass and perform an exhaustive second-location sweep for the same defect classes.

## B1 — Skill eligibility must fail closed at individual-card approval

Problem: `implementation/phase-16/registries.py` currently treats Phase 4 architecture approval as if it approved six individual Skill cards. The Phase 4 approval record explicitly denies mass promotion.

Required outcome:

1. Skill eligibility must be based on authoritative declared Skill identity + explicit individual/exemplar-card approval evidence, not architecture-level phase approval alone.
2. If the repository lacks sufficient approval evidence for an individual Skill card, that Skill must be ineligible / unresolved, not approved by inference.
3. Preserve fail-closed behavior for the whole Skill eligibility view where evidence cannot be established consistently.
4. Do not manufacture new approvals or alter existing approval records.
5. Add positive and negative tests proving:
   - approved exemplar Skill identity resolves only when its approval evidence really covers it;
   - architecture-level approval alone is insufficient;
   - candidate / mentioned / superseded / unapproved Skills remain ineligible.
6. Sweep all Skill eligibility helpers, caches, docs, examples and validation assumptions for second-location inference from Phase 4 architecture approval.

## B3 — only successful preflight may produce an issuable basis

Problem: the store can seal and issue an arbitrary caller-constructed `ExecutionBasis`, including one fabricated after preflight blocked.

Required outcome:

1. A basis may become issued/EXECUTABLE only from a successful Phase 16 preflight result produced by the actual preflight path.
2. Introduce an unforgeable-in-process provenance/capability/token/result binding sufficient for this reference implementation so caller construction alone cannot satisfy issuance.
3. Store issuance must validate that provenance against the exact PlannerOutput / preflight result / basis payload and reject:
   - fabricated bases;
   - blocked preflight results;
   - missing provenance;
   - provenance from another request/plan/basis;
   - altered basis payloads;
   - reused provenance.
4. Do not convert this into authority or approval. The provenance only proves successful Phase 16 preflight.
5. `build_trigger` must remain impossible for any never-validly-issued basis.
6. Add a direct regression test reproducing the Codex attack: CRITICAL plan lacks mandatory review → preflight BLOCKED → fabricated matching basis → issuance MUST REFUSE → trigger MUST NOT build.
7. Sweep examples, store helpers, lifecycle methods and docs for any path that can mark/accept/issue an EXECUTABLE basis without successful preflight provenance.

## B4a — parser must never convert boundary/exclusion prose into positive mapping

Problem: the Role/Skill mapping parser carries a prior relationship into `### Boundaries` and misreads explicit `not mapped` prose as `ALTERNATIVE` mapping. Example: `skill.lifecycle_cost_analysis` is wrongly accepted for CAPEX / Cost Engineering despite explicit exclusion.

Required outcome:

1. Mapping parsing must be section-aware and positive-evidence-only.
2. Boundary, exclusion, negative, superseded, example/counterexample and narrative text must never create a positive mapping.
3. Encountering a boundary/exclusion section must reset any carried parser state that could cause positive inheritance.
4. Explicit `not mapped`, `prohibited`, `not assigned`, `does not map`, or equivalent negative statements must override/deny, never map.
5. Add direct tests for `skill.lifecycle_cost_analysis` against CAPEX / Cost Engineering and at least several nearby negative/boundary examples.
6. Add positive controls proving real authoritative mappings still resolve.
7. Sweep all parser branches and docs for state leakage across sections.

## B4b — owned conclusions must be substantive, not just Role membership

Problem: `preflight.py` accepts an empty `owned_conclusion` as long as the Role is registered.

Required outcome:

1. Every load-bearing Role requirement must carry a non-empty, non-whitespace substantive owned conclusion.
2. The owned conclusion must be part of the effective binding checked before basis issuance.
3. Blank / whitespace / missing / placeholder-only values must BLOCK with a named reason.
4. If there is an authoritative Role-owned-conclusion vocabulary/contract, validate compatibility without inventing a new registry. If no such authoritative mapping exists, require a substantive declared conclusion and preserve it exactly as planner provenance rather than claiming canonical Role ownership semantics not present upstream.
5. Add tests showing blank/whitespace owned conclusions cannot reach issuance or trigger construction.

## B5 — runtime faults must be RUNNER_ERROR, never semantic DETECTED

Problem: `phase_16_validation.py` catches arbitrary runtime exceptions and turns them into normal failed checks; the mutation classifier then counts them as DETECTED.

Required outcome:

1. Distinguish semantic validator failure from validator/runtime infrastructure failure.
2. A deliberate unexpected `RuntimeError`, import failure, path failure, timeout, crash, malformed validator output, or other infrastructure/runtime fault must classify as `RUNNER_ERROR`, never `DETECTED`.
3. Only a cleanly executed validator that returns a semantic FAIL attributable to the planted mutation may count as `DETECTED`.
4. Pristine copied control must still pass before probes are counted.
5. `--json` must remain valid JSON and must expose enough structured status to distinguish PASS / semantic FAIL / RUNNER_ERROR.
6. Add a direct probe that injects a `RuntimeError` into preflight and assert `RUNNER_ERROR`.
7. Do not hide errors by broad exception-to-check conversion.

## Required assurance

After remediation run and report:

- Phase 16 unit suite;
- `python3 validation/phase_16_validation.py`;
- `python3 validation/phase_16_validation.py --json`;
- `python3 validation/phase_16_mutation_probes.py --json`;
- executable and blocked examples;
- `git diff --check`;
- final clean worktree.

For mutation accounting, report exact counts for DETECTED / ESCAPED / REDUNDANT / RUNNER_ERROR. Do not present a green ratio that counts runtime failures as detections.

Add fresh targeted tests/probes for every one of the four blocker families above, including the direct fabricated-basis bypass and the direct runtime-error classification case.

## Containment

Changes must remain inside:

- `planner-activation/`
- `implementation/phase-16/`
- `validation/phase_16_validation.py`
- `validation/phase_16_mutation_probes.py`

Do not modify approved upstream artifacts or registry source records.

## Commit / push

When all checks are complete:

1. commit the remediation;
2. push it to `implementation/phase-16-planner-activation`;
3. do not create a PR;
4. return the exact remediation SHA and confirm the final worktree is clean.

## Required output

Return sections A–L:

A. SUMMARY
B. BASELINE / HEAD / REMEDIATION SHA
C. CHANGED FILES
D. B1 CLOSURE
E. B3 CLOSURE
F. B4 CLOSURE
G. B5 CLOSURE
H. TARGETED TESTS
I. VALIDATOR / MUTATION RESULTS
J. CONTAINMENT
K. REMAINING BLOCKERS
L. VERDICT

If all four blocker families are closed, end with exactly:

`READY FOR FINAL SHORT PHASE 16 SURVIVOR CLOSURE REVIEW`

Otherwise list the remaining blocker(s) precisely. 
