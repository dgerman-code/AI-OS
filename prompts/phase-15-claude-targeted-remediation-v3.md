# Phase 15 — Targeted Remediation V3 after Independent Re-Audit V3

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`
Failed audited baseline: `9b95c3e0025a4ca63c9ec425b68fddea68fa10de`
Independent review verdict: `FAIL`
Review credibility: `HIGH` for baseline-specific findings; validator assurance `LOW`.

## Mission

Remediate ONLY the four remaining blocking contradictions from the independent V3 re-audit, plus directly necessary assurance/reporting updates. Preserve all accepted Phase 15 semantics, especially the natural-language-to-governed-plan UX, Work Plan != Workflow, P1-P5 functions-not-agents, no invented authority, and fail-closed COMPOSE boundaries.

Do not modify approved Phase 1–13 artifacts. Do not modify any Phase 14 file. Do not create runtime code, migrations, DDL, workers, queues, provider bindings, secrets, deployment, IaC, or a PR. All Phase 15 architecture artifacts remain `PROPOSED`. Do not manufacture human approval.

## Blocker 1 — remove invented current Phase 11 consumption from the object model

The handoff contract now correctly says no approved Phase 11 contract consumes `PlannedWorkItemSpec`, but `planning/work-plan-object-model.md` still contradicts it.

Required correction:

- Remove every active statement in OM-16 and the planning-record inventory/row that says or implies current approved Phase 11 reads, revalidates, translates, instantiates, or otherwise consumes `PlannedWorkItemSpec`.
- State the current boundary exactly:
  - Phase 15 may produce a non-runtime `PlannedWorkItemSpec` only after plan validation where the Phase 15 architecture permits it;
  - no currently approved execution-basis contract consumes that record;
  - therefore the record is inert with respect to execution unless and until explicit downstream change control defines consumption semantics;
  - PO-4 and PO-12 remain explicit fail-closed dependencies;
  - MATCH continues to use the approved Workflow-based intake path and must not depend on `PlannedWorkItemSpec`.
- Preserve `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`.
- Do not solve the gap by calling the spec a Workflow, Task, Work Item, trigger, or approved execution basis.

Add cross-document validator checks that reject any active current-behaviour claim that approved Phase 11 consumes the spec, including reversed word order and table-row variants.

## Blocker 2 — make load-bearing determination non-circular everywhere

The V3 audit found that LB-0/LB-6 are correct, but LB-3 and the `RoleRequirement` schema still prescribe the reduced deliverable as `load_bearing_basis`, contradicting the rule that reduction is only a consequence after the determination.

Required correction:

Define two distinct concepts/fields if needed, for example:

- `load_bearing_basis`: evidence drawn ONLY from the original requested/declared deliverable, approved ownership, review/gate dependencies, and pre-reduction plan requirements;
- `reduced_deliverable_basis` / `constrained_output_basis`: recorded only AFTER an independent `NOT_LOAD_BEARING` result, used solely to prove that a coherent reduced deliverable survives.

Normative requirements:

1. `LOAD_BEARING` / `NOT_LOAD_BEARING` is always decided against the original requested deliverable before any narrowing.
2. A surviving reduced deliverable can never be evidence for the load-bearing determination.
3. `NOT_LOAD_BEARING` must have a positive original-deliverable basis; it is not a default residual category.
4. The reduced-deliverable field, if present, is post-determination admissibility evidence only.
5. `NO_APPROVED_ROLE_OWNS_CONCLUSION` remains F-14 and blocks. Do not route it back through F-5/F-6.
6. The difficult-partner exemplar continues to BLOCK the original request because communication strategy is requested in terms and has no approved owner.

Update schema/table text, LB rules, preflight checks, examples, self-check, validator and probes consistently.

## Blocker 3 — make `primary_work_mode` normative example agree with RI-12

The V3 audit found a direct contradiction: RI-12 still includes an example/prescription that yields `ANALYSIS` for an unprioritised analysis + drafting request, while Example 2 correctly yields `UNKNOWN` under the ordered tests.

Required correction:

- Make RI-12 itself match the ordered upstream-only algorithm now used by Example 2.
- For a request like “check whether they are right and prepare a response” where two end-results are requested without stated priority and tests 1–4 do not resolve one primary, the normative result must be:
  - `primary_work_mode = UNKNOWN`
  - `secondary_work_modes = {ANALYSIS, DRAFTING}` (complete applicable set)
- Remove any stale example or prose that deterministically picks ANALYSIS merely because analytical work happens to precede drafting or feels semantically central.
- Never use downstream PlanStage/dependency structure to resolve primary mode.
- Preserve the ACTION case for explicit execution verbs with applicable external/commitment conditions.

Add a validator assertion and mutation probe that target the normative RI-12 example itself, not only the exemplar file.

## Blocker 4 — unanswered C4 must BLOCK, never silently degrade to PREPARE

The V3 audit found RI-6 contradicts CL-2 by saying unresolved EXECUTE/PREPARE ambiguity on an irreversible/authority-sensitive act can degrade to PREPARE.

Required correction:

- Align RI-6 with CL-2 exactly: unresolved C4 ambiguity -> `AWAITING_CLARIFICATION`, and if unavailable/unanswerable -> `BLOCKED`.
- No default `PREPARE`, no implicit narrowing, no “safe fallback” that changes the requested act.
- If the user later asks for preparation-only, that is a NEW linked Request / revised WorkIntent, not an automatic fallback of the blocked request.
- Preserve the architecture principle: infer when safe; clarify/block where ambiguity changes authority or irreversible action.

Add cross-document checks so a future active statement like “if unanswered, treat as PREPARE” fails even if CL-2 remains correct elsewhere.

## Non-blocking stale reporting to clean while touching the package

The V3 audit identified stale reporting. Correct these without changing governance semantics:

- eighteen preflight checks -> current actual count;
- thirteen failure modes -> current actual count;
- stale EIB-trigger count;
- stale Example 2 “constrained result” references;
- incorrect statement that no separate Phase 12 unit suite exists.

Derive counts where practical instead of hard-coding duplicate prose.

## Assurance hardening

The independent V3 review detected only 22/30 second-location mutations; eight escaped. Extend assurance specifically to catch these classes in independent second locations:

1. simple wording lowers criticality;
2. ReviewRequirement treated as satisfied review;
3. PlannedWorkItemSpec described as runtime Work Item;
4. F-9 lets Phase 15 continue/control runtime stages;
5. Task described as run-created identity;
6. spec generated before validation;
7. no-approved-owner routed to F-5 CONSTRAIN;
8. plain UNKNOWN prerequisite treated as admissible.

Do not implement brittle single-sentence matching only. Prefer structural/cross-document invariants and table-row parsing where feasible. Also add probes for the four V3 blockers above in second locations.

Do not claim HIGH assurance. Preserve the self-check's explicit history that two previous green producer harnesses coexisted with blocking contradictions.

## Required execution

Run and report, at minimum:

- `python3 validation/phase_15_validation.py`
- `python3 validation/phase_15_validation.py --verbose`
- `python3 validation/phase_15_validation.py --json`
- `python3 validation/phase_15_mutation_probes.py --json`
- Phase 12 unit suite (157 tests, if unchanged and available)
- Phase 12 validator
- Phase 11 validator
- Phase 10 validator
- Phase 9 validator
- Phase 8 validator
- `git diff --check`
- containment diff proving approved Phase 1–13 and Phase 14 unchanged

Inherited Phase 10/11 findings must remain inherited; do not repair them here.

## Completion criteria

Before committing, verify all of the following manually, not only through the validator:

- object model no longer claims current approved Phase 11 consumes `PlannedWorkItemSpec`;
- PO-4 and PO-12 remain explicit and fail-closed;
- load-bearing basis and reduced-deliverable admissibility are separate, non-circular concepts;
- RI-12 and Example 2 return the same `UNKNOWN + {ANALYSIS,DRAFTING}` result for the same unprioritised request shape;
- unresolved C4 ambiguity blocks and never auto-degrades to PREPARE;
- no approved owner remains F-14 BLOCK;
- prerequisite tri-state remains `RESOLVED / FUTURE_GOVERNANCE_REFERENCE / UNKNOWN->BLOCK`;
- no runtime Stage control moved into Phase 15;
- all Phase 15 artifacts remain PROPOSED;
- no PR.

If all blockers are closed, commit and push to `architecture/phase-15-intent-work-planning` and return the full immutable remediation SHA.

Return a concise A–R report. The exact final line must be:

`READY FOR INDEPENDENT PHASE 15 ARCHITECTURE RE-AUDIT V4`

If any blocker remains, end instead with:

`NOT READY — REMAINING BLOCKERS`
