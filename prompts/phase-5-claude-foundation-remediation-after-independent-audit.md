# Claude Code Prompt — Phase 5 Foundation Remediation After Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-5-workflow-registry`
Current branch HEAD includes the independent audit prompt commit `6a441238cd78828617d06326728a256d8549690a`.
Foundation baseline audited: `17c95ac191c66a7f18cc13421480e44ef46a6af8`.

The independent audit returned **PASS WITH CHANGES** with no HIGH findings and five MEDIUM findings. The architecture identity, phase boundary and authority model passed. This remediation must be **narrow and bounded**: fix the listed foundation defects only.

Do not modify Phase 3 Role Cards.
Do not modify approved Phase 4 architecture or mappings.
Do not add, remove or rename Roles, Skills, Specialisations or Packs.
Do not implement runtime, database, orchestration, scheduling, model routing, agents, APIs or UI.
Do not create a PR.
Do not mark Phase 5 APPROVED or CANONICAL.
Do not bulk-card the 45 uncarded Workflow candidates.
Do not resolve all eight overlap groups in this pass unless one of the changes below directly requires a wording clarification.

## Audit findings to remediate

### M1 — Materiality-aware open-item progression

Problem: `COMPLETE_WITH_OPEN_ITEMS` has no shared materiality rule. A gate-critical `UNKNOWN`, `CONFLICT_DETECTED`, unresolved material `ASSUMPTION`, missing required review, or other item material to the next Stage / terminal gate must not satisfy exit merely because it is recorded.

Apply a registry-wide rule in:
- `architecture/workflow-registry-design.md`
- `workflows/_standards/common-workflow-constraints.md`
- `workflows/_templates/workflow-card-template.md`

Required semantics:
1. Every open item used with `COMPLETE_WITH_OPEN_ITEMS` must be classified at least as **NON_MATERIAL_TO_NEXT_STEP** or **MATERIAL_TO_NEXT_STEP_OR_GATE**. Do not create a broad risk-severity taxonomy; this is only progression materiality.
2. `MATERIAL_TO_NEXT_STEP_OR_GATE` includes any unresolved item that could change the next Stage's permitted work, a specialist conclusion relied on downstream, a required review position, a human gate's evidence basis, a transmitting act, or a terminal readiness conclusion.
3. A material item cannot support `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` for the affected progression. Default outcome must be `BLOCKED`, `REWORK_REQUIRED`, or `ESCALATED`.
4. The only exception is where a **named external human Decision Right** explicitly permits proceeding with that unresolved material item. The Workflow records the gate reference and the item remains unresolved/open; the Workflow does not decide the waiver and does not relabel the item resolved.
5. A missing required `review.<id>` can be visible, but visibility does not satisfy the review. If the next Stage or gate requires that review, absence blocks progression unless an external Decision Right explicitly governs proceeding without it.
6. `UNKNOWN`, `CONFLICT_DETECTED`, and material `ASSUMPTION` are never cleared by stage movement.

Correct all four exemplar cards so their Stage exit/completion/exception language is consistent with the shared rule. Specifically correct Exemplar D S4: remove any implication that a gate-critical `UNKNOWN` may advance merely because it is named for the decision-maker.

Do not invent who holds a Decision Right or what its approval semantics are; Phase 7 still owns that.

### M2 — Conditional activation must be separate from participation type

Problem: `CONSULTED_ROLE` currently mixes two concepts: advisory participation and conditional/triggered activation. Several Roles typed as consulted actually produce/own artifacts when triggered.

Correct the participation architecture in:
- `architecture/workflow-registry-design.md`
- `workflows/_standards/common-workflow-constraints.md`
- `workflows/_templates/workflow-card-template.md`
- affected exemplar cards

Required model:
1. Keep the three Role participation types:
   - `LEAD_ROLE`
   - `CONTRIBUTING_ROLE`
   - `CONSULTED_ROLE`
2. Define **conditional activation as a separate property**, not a participation type. Use a simple declarative field/qualifier such as `Activation: ALWAYS | CONDITIONAL(<objective trigger>)`. Do not add a sixth Role participation type.
3. `CONTRIBUTING_ROLE`: produces bounded work, artifact content, an owned artifact, or an owned professional conclusion.
4. `CONSULTED_ROLE`: advisory/input-only participation; it does not own or advance an artifact/conclusion within that Stage.
5. A Role may be `CONTRIBUTING_ROLE` and conditionally activated. This is the required treatment for triggered specialists that produce owned artifacts.
6. Triggered participation must use an objective condition and must not widen Phase 4 compatibility or Role scope.

Reconcile all four exemplar cards. At minimum audit/correct:
- Project Development Readiness S2, S3, S5
- EU Grant Application Development S3, S4
- Decision-Grade Document Preparation S1, S5

Examples of the intended result:
- a Sector Technical Expert who produces `artifact.sector_technical_opinion` when sector materiality applies = `CONTRIBUTING_ROLE`, Activation `CONDITIONAL(sector materiality)`;
- a genuinely advisory architect consulted on deviation, with no artifact contribution in that Stage = `CONSULTED_ROLE`, Activation `CONDITIONAL(deviation)`.

Update the global Participating Roles tables and per-Stage participation consistently.

### M3 — Software Change Delivery S3 security ownership defect

Problem: S3 advances `artifact.security_control_implementation`, owned by `role.security_engineer`, while Security Engineer does not participate in S3.

Preferred correction:
- add `role.security_engineer` as `CONTRIBUTING_ROLE` in S3 with `Activation: CONDITIONAL(security-control implementation is in scope)`;
- keep implementation responsibility bounded to security controls owned by that Role;
- do not give Security Engineer `skill.quality_attribute_analysis` or `skill_pack.supabase`;
- update the top participation table, S3 participating roles, activities, artifact contribution and any traceability text consistently.

If repo Role ownership makes that impossible, remove `artifact.security_control_implementation` and the corresponding activity from S3 and explain why. Do not fabricate ownership.

### M4 — Declarative reusable Workflow composition

Problem: the architecture claims `workflow.decision_grade_document_preparation` is composed into other Workflows, but the primitive model has no way to represent that.

Add **one declarative non-runtime composition primitive**. Recommended name: `WORKFLOW_REFERENCE`.

Required semantics:
1. `WORKFLOW_REFERENCE` points to a stable `workflow.<id>` and optionally a version constraint/reference policy, but does not execute it.
2. The parent card must state the bounded purpose of the reference, expected inputs, expected outputs, and which parent Stage(s) it relates to.
3. Referencing a child Workflow does not transfer Role ownership, Skill compatibility, review identity, Decision Rights, gates, or knowledge-state authority.
4. The child Workflow's gates/review requirements cannot be silently dropped by the parent. If the parent relies on an output that requires a child gate/review, that dependency remains visible.
5. No nested runtime scheduling semantics, retry semantics, call stack, state-machine execution or database representation are introduced.
6. Avoid recursion/cycles at registry level: a Workflow must not directly or transitively reference itself. State this as an architecture validation rule.
7. Composition may be optional/conditional only under a stated objective condition.

Update:
- architecture primitive table (12 → 13 primitives)
- common constraints with a composition rule
- Workflow Card template with a `## Composed Workflow References` section or equivalent
- `workflow.decision_grade_document_preparation` to describe its role as reusable child pattern without claiming magical composition
- at least one parent exemplar should contain a concrete `WORKFLOW_REFERENCE` only if the fit is semantically honest and does not require redesign. Prefer Project Development Readiness's document-preparation segment if appropriate. If the current parent exemplars do not cleanly compose the whole child Workflow, explicitly state that they do not yet reference it and revise the Master Universe wording from "is composed" to "is a candidate reusable pattern available through WORKFLOW_REFERENCE where its full preconditions/outputs match". Do not force a false composition.

The goal is representability, not proving every overlap now.

### M5 — Closed validation for parameterized Role slots

Problem: Exemplar D uses Document Owner Role and Specialist Contributing Role slots, but registry-wide validation rules do not close the binding.

Add a declarative **Role Slot Binding Rule** in architecture/standard/template.

Required semantics:
1. Any parameterized Role slot must declare:
   - slot ID/name;
   - allowed source = approved `role.<id>` only;
   - required ownership/interface condition;
   - permitted participation type(s);
   - any required artifact-ownership relationship;
   - capability validation rule against approved Phase 4 mappings.
2. At instance binding, the slot resolves to exactly one concrete approved `role.<id>` per slot occurrence unless the slot explicitly declares cardinality >1.
3. Wildcards like "any Role" are prohibited unless followed by explicit machine/audit-testable eligibility constraints derived from the Role Card/approved registries.
4. A slot cannot grant ownership: the bound Role must already own the relevant artifact/conclusion in its Role Card.
5. Every Skill/Specialisation/Pack activated for a bound Role must independently pass Phase 4 compatibility. The Workflow/slot is never evidence of compatibility.
6. A slot cannot bind a System Control Profile, Review Profile, Decision Right, model or runtime identity.
7. If no approved Role satisfies the slot constraints, the Workflow instance is `BLOCKED` / invalid for that assignment; do not widen the slot.

Update Exemplar D so the Document Owner and Specialist slots have explicit closed binding constraints. Keep it generic, but not unconstrained.

## Workflow universe finding handling

The independent audit classified:
- 29 VALID WORKFLOW
- 8 LIKELY WORKFLOW BUT NEEDS BOUNDARY REFINEMENT
- 10 LIKELY ROLE OR SKILL IN DISGUISE PENDING MULTI-ROLE TEST
- 2 LIKELY SINGLE-GATE PREPARATION PATTERN
- 0 runtime concerns among active candidates

Do **not** mass-delete or merge candidates in this remediation. Instead:
1. add a concise audit-status annotation or review note to `workflows/master-workflow-universe.md` indicating that 20 candidates require boundary validation before carding;
2. explicitly prohibit card generation for those 20 until they pass Role-vs-Workflow, multi-stage, artifact-ownership and composition tests;
3. keep the 8 overlap groups open for selective validation;
4. retain 49 as the candidate universe unless a direct contradiction discovered during remediation forces a change.

## Open-question dispositions to record

Update `reviews/phase-5-foundation-self-check.md` or create `reviews/phase-5-foundation-audit-remediation.md` so the seven questions now have clear disposition after remediation:

1. Composition — RESOLVED IN FOUNDATION via declarative `WORKFLOW_REFERENCE`.
2. Partial ordering — SAFE TO DEFER WITH EXPLICIT RULE; prose must remain unambiguous/testable.
3. Workflow version binding — RUNTIME-PHASE CONCERN; registry still requires version/change record.
4. Open-item materiality — RESOLVED IN FOUNDATION via shared materiality rule.
5. Trigger vocabulary — SAFE TO DEFER WITH EXPLICIT RULE; triggers remain objective/testable prose.
6. Parameterized Role slots — RESOLVED IN FOUNDATION via closed Role Slot Binding Rule.
7. System Control interaction — RUNTIME-PHASE CONCERN; selection may narrow only within registry-declared conditions and may never mutate/widen Workflow semantics.

## Regression requirements

After changes, independently verify:
1. Phase 3 Role Cards unchanged.
2. Approved Phase 4 architecture/mappings unchanged.
3. All Phase 5 artifacts remain `PROPOSED`.
4. `ROLE != SKILL != WORKFLOW != REVIEW PROFILE != DECISION RIGHT != MODEL != RUNTIME` unchanged.
5. No Workflow grants professional authority.
6. No Workflow grants or satisfies a human Decision Right.
7. No Workflow defines independent reviewer identity/method.
8. No Workflow self-promotes `REVIEWED`, `APPROVED`, or `CANONICAL`.
9. AI outputs remain `AI_SUGGESTION`/`DRAFT` until governed adoption/transition.
10. No Workflow widens Phase 4 capability compatibility.
11. Material open items cannot pass an affected exit/gate without a named external Decision Right explicitly permitting progression.
12. `COMPLETE_WITH_OPEN_ITEMS` cannot be used as a generic gate-critical waiver.
13. Conditional activation is independent of participation type everywhere.
14. Every artifact-producing Role in every exemplar Stage is `LEAD_ROLE` or `CONTRIBUTING_ROLE`, not merely `CONSULTED_ROLE`.
15. `CONSULTED_ROLE` produces no owned artifact/conclusion in the Stage where it is consulted.
16. Software S3 security artifact has the owning Security Engineer participating, or the artifact/activity is removed consistently.
17. Security Engineer remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase`.
18. `WORKFLOW_REFERENCE` is declarative, acyclic, non-runtime and cannot drop child gates/reviews/ownership.
19. Parameterized Role slots bind only to approved concrete Roles under closed eligibility rules.
20. Slot binding cannot widen Role scope or Phase 4 compatibility.
21. 49 candidate IDs remain unique (unless an explained direct correction is unavoidable).
22. 7 deliberate exclusions remain sound.
23. 20 audit-flagged boundary-validation candidates are marked not safe to card yet.
24. 8 overlap groups remain visible/open.
25. No mass card generation performed.
26. Four exemplars each pass the corrected participation/materiality rules.
27. Reference integrity: zero invalid concrete `role.*`, `skill.*`, `specialisation.*`, `skill_pack.*`, `artifact.*` references; forward `review.*` / `decision.*` remain explicit Phase 6/7 dependencies.
28. No runtime/database/API/orchestrator/model implementation introduced.
29. No PR created.
30. Working tree clean after commit.

Create a remediation record:
`reviews/phase-5-foundation-audit-remediation.md`

Status:
`PROPOSED — READY FOR FINAL INDEPENDENT PHASE 5 FOUNDATION RE-AUDIT`

The record must list M1–M5 and show exactly how each was resolved, including files changed and the 30 validation results.

## Commit / push

If and only if all 30 checks pass, commit exactly:

`docs: remediate Phase 5 foundation after independent audit`

Push to:
`origin architecture/phase-5-workflow-registry`

Do not create a PR.

## Required output

Return exactly:

### A. M1 MATERIALITY RULE
What changed and how gate-critical open items now behave.

### B. M2 PARTICIPATION MODEL
How participation type and conditional activation are separated; list corrected exemplar assignments.

### C. M3 SECURITY S3
Exact correction and confirmation of Phase 4 Security boundaries.

### D. M4 WORKFLOW COMPOSITION
New declarative primitive/rules and whether any concrete parent exemplar references the generic document Workflow.

### E. M5 ROLE SLOT VALIDATION
Closed binding rules and Exemplar D changes.

### F. UNIVERSE / CARDING BOUNDARY
49-candidate status, the 20 audit-flagged candidates, overlap groups, card-generation restriction.

### G. OPEN QUESTIONS
All seven with updated disposition.

### H. REGRESSION / VALIDATION
Checks 1–30 PASS / FAIL.

### I. FILES CHANGED
Exact files and concise purpose.

### J. COMMIT / PUSH
Commit SHA, message, push result, remote HEAD and PR status.

### K. NEXT STEP
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 5 FOUNDATION RE-AUDIT
- NOT READY

Do not claim Phase 5 approval.