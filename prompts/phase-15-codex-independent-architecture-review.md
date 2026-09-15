# Phase 15 — Independent Architecture Review

## Repository / branch / exact baseline

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`

AUDIT / REVIEW ONLY.

Do not modify files.
Do not commit.
Do not create a PR.
Do not promote any Phase 15 artifact.
Do not manufacture human approval.

Audit exact baseline:

`f8ef2cf52a8581d87f05bfa0b8f822611b51fbda`

The later review-prompt commit is not part of the audited architecture and must be excluded.

Before substantive review:
1. print the exact audited SHA;
2. verify it equals `f8ef2cf52a8581d87f05bfa0b8f822611b51fbda`;
3. use a clean detached worktree;
4. if the SHA differs, STOP with `BASELINE MISMATCH`.

---

# Review objective

Independently determine whether Phase 15 safely closes the gap between a natural-language user request and the approved Phase 11 Orchestrator **without** creating a second Orchestrator, inventing authority, turning instance plans into Workflow Registry objects, weakening scope/knowledge/criticality controls, or forcing users to understand internal architecture.

The intended product behavior is:

```text
Natural-language Request
  -> Work Intent
  -> Scope Resolution
  -> Work Classification / Criticality
  -> Role / Skill Requirements
  -> Workflow MATCH or instance-level COMPOSE
  -> Reviews / Decision Rights / Evidence Requirements
  -> Work Items
  -> Governance Preflight
  -> Phase 11-compatible Trigger
  -> Approved Orchestrator
```

The user should normally not need to name Workflow IDs, Role IDs, Skills, Review Profiles, Decision Rights, Model Profiles, or routing policies.

---

# Mandatory architecture invariants

Verify, do not assume:

1. `REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK != WORK ITEM != ROLE != MODEL != ORCHESTRATOR != HUMAN AUTHORITY`.
2. Phase 15 functions are not persistent agents/personas.
3. MATCH binds an existing approved Workflow at version; COMPOSE creates only an instance-level Work Plan.
4. A Work Plan can never silently become a Workflow Registry object.
5. A repeated plan may produce only a `PROPOSED` Workflow candidate suggestion, never auto-registration/approval.
6. Planner confidence never grants authority, waives review, changes knowledge state, crosses scope, or substitutes for evidence.
7. Criticality can only increase rigor, never lower approved requirements.
8. Role/Skill inference cannot invent missing or unapproved capabilities or use similarity as authority.
9. Review Profiles and Decision Rights are resolved by reference; missing applicable authority fails closed.
10. Model selection remains Phase 9 Router responsibility.
11. Phase 15 does not execute orchestration semantics owned by Phase 11.
12. Governance preflight is not approval.
13. Phase 8 epistemic types remain separate and there is no epistemic-type mutation.
14. Scope separator boundaries cannot be crossed by guess or string similarity.
15. The UX hides internal object selection by default and asks clarification only where consequence justifies it.

---

# Required review dimensions

## A. Baseline / containment

Verify exact baseline and clean worktree.
Confirm approved Phase 1–13 artifacts are unchanged.
Confirm no Phase 14 file changed.
Confirm all Phase 15 artifacts remain `PROPOSED`.
Confirm no runtime, DDL, migrations, provider bindings, queues, workers, schedulers, secrets, IaC, deployment, or PR exists.

Also inspect the deliberate path deviation: the primary architecture document is under `planning/`, not `architecture/`, because adding a file under `architecture/` would trip the inherited Phase 12 containment validator. Determine whether this is a safe repository-governance workaround, a documentation-structure defect, or a blocker.

## B. Identity and layer separation

Audit every first-class planning object and every place where Work Plan, Workflow, Workflow Run, Task, Work Item, Role, Model, Orchestrator, Decision Right, Review Profile, knowledge, and human authority are discussed.

Look for semantic collapse even if IDs remain distinct.

## C. Request / Intent semantics

Review the `Request` and `WorkIntent` model.
Check that the original natural-language request remains source material and that structured interpretation is non-authoritative.
Check EXECUTE vs PREPARE ambiguity, reversible vs irreversible action, external transmission, commitments, audience/channel, deadline, and `UNKNOWN` handling.

## D. Clarification policy

Audit C1–C5 and the principle: infer when safe; clarify only when ambiguity materially changes scope, authority, professional conclusion, irreversible action, or governed outcome.

Specifically test:
- high confidence cannot downgrade C4/C5;
- C4/C5 never receive defaults;
- C1/C2 do not become needless blocking questions;
- C3 behavior is coherent;
- user is never forced to select internal architecture objects;
- clarification answers revise records append-only rather than overwriting history.

## E. Context / scope resolution

Verify the reproduced scope graph against approved Phase 2/8 semantics.
Check both PROJECT parent paths.
Check separator-boundary handling, cross-scope reference vs copy, one-request/one-scope rule, entitlement deferral, and material ambiguity.

Attempt nearby attacks such as prefix/string similarity between sibling projects, same counterparty across two scopes, and session context overriding an explicitly referenced artifact scope.

## F. Work classification / criticality

Verify all inherited high-stakes triggers and that planning cannot lower criticality.
Check that conservatism is represented as planning posture rather than fabricated fact.
Check apparently simple tasks that become high-stakes because of IFI/DFI, PPP, public actors, legal commitment, external institutional communication, sanctions/AML, data/cyber, etc.

## G. Role / Skill inference

Verify requirement inference is grounded in approved compatibility/ownership, not persona or semantic similarity alone.
Check missing/unapproved Role/Skill behavior.
Check co-activation and domain ownership.
Check that a communication request with legal consequences does not let the communication capability alter legal conclusions.

Where the package references a future Difficult Conversations & Communication Strategy capability, verify it remains future/conditional and cannot activate until governed/approved.

## H. Workflow matching vs dynamic composition

Audit the MATCH and COMPOSE boundary in depth.

Verify:
- MATCH uses an approved Workflow at a named version;
- similarity/ranking never overrides explicit preconditions, scope, role constraints, reviews, or rights;
- COMPOSE uses approved primitives only;
- PlanStage does not acquire Workflow semantics by accumulation;
- gates have no fake Role participation;
- partial/conditional composition is represented honestly;
- repeated plans cannot self-register.

## I. Work Plan object model

Audit all proposed first-class records: Request, WorkIntent, ScopeResolution, WorkRequirementSet, WorkflowMatchAssessment, WorkPlan, PlanStage, RoleRequirement, SkillRequirement, ReviewRequirement, DecisionRequirement, EvidenceRequirement, ClarificationRequirement, PlanningFinding, PlanValidationResult, WorkflowCandidateSuggestion, or equivalents.

For each, check purpose, authority status, lifecycle, versioning, persistence, AI-creation permission, human-approval requirement, and whether it may directly affect execution.

Look for any record that accidentally becomes authoritative merely because it is persisted.

## J. Review / Decision Right planning

Verify Phase 15 only resolves requirements and references.
It must not exercise, grant, satisfy, invent, or infer a Right from business necessity.

Test distinctions among:
- prepare only;
- review required;
- Decision Right required;
- executable non-authority-bearing action;
- transmission blocked.

Missing applicable authority must fail closed.

## K. Knowledge / evidence planning

Verify SOURCE, EVIDENCE, FACT_CLAIM, ASSUMPTION, CALCULATION, INFERENCE, AI_SUGGESTION, UNKNOWN remain separate.
No type mutation.
No planning need may upgrade an assumption or AI suggestion into a fact claim.
Evidence requirements must be able to block or constrain downstream work.

## L. Work Item generation

Verify Work Items are derived only from validated plan stages and approved definitions.
Check required fields and deterministic downstream handoff information.
Check that Work Item generation does not itself perform orchestration, assignment, routing, review satisfaction, or authority exercise.

## M. Orchestrator handoff / PO-4

This is the highest-priority architecture question.

The approved Phase 11 intake check 1 expects a Workflow definition resolving at a named version. Phase 15 allows COMPOSE, where a Work Plan is explicitly **not** a Workflow.

Independently analyze all viable interpretations.
At minimum evaluate:

A. Phase 11 trigger can name a composed instance plan through an already-approved generic execution Workflow / envelope mechanism without changing Workflow identity.
B. Phase 11 intake semantics need a governed extension so a validated Work Plan can be a distinct trigger basis alongside a Workflow definition.
C. Register the Work Plan as a Workflow.

C must be rejected if it violates Phase 15/Phase 5 identity rules.

Determine whether A is already supported by approved semantics, whether B requires an explicit future change-control to Phase 11, or whether there is another safe architecture. Classify PO-4 as one of:
- BLOCKER BEFORE PHASE 15 APPROVAL;
- APPROVABLE WITH EXPLICIT BLOCKED IMPLEMENTATION DEPENDENCY;
- SAFE NON-BLOCKING OPEN ITEM.

Do not resolve this by silently rewriting approved Phase 11 semantics.

## N. Failure / escalation model

Audit all failure modes and exact dispositions.
Check there is no ambiguous overlap where one condition can both continue and block.
Check `NO_MATCHING_WORKFLOW` vs `PLAN_COMPOSITION_REQUIRED` distinction.
Check unavailable Role/Skill/Review/Right behavior.
Check constrained-plan behavior explicitly states uncovered work.

## O. UX contract

Verify the normal user experience satisfies the product goal:
- system understands ordinary language;
- user sees what AI understood and intends to produce;
- only material clarifications are asked;
- human approval points are visible;
- internal IDs remain hidden by default but inspectable for governance/admin/debug.

Look for any architecture path that would force ordinary users to understand Roles, Workflows, Decision Rights, or Router internals.

## P. Assurance / validator / mutation credibility

Run:

```bash
python3 validation/phase_15_validation.py
python3 validation/phase_15_validation.py --verbose
python3 validation/phase_15_validation.py --json
python3 validation/phase_15_mutation_probes.py --json
```

Also run inherited validators/tests as appropriate, at minimum Phase 8, 9, 10, 11, and 12, and confirm inherited findings remain exactly inherited.

Do not trust the committed Phase 15 harness by itself.
Derive key inventories independently from source text.

Perform at least 16 independent second-location/adversarial mutations or equivalent semantic probes, including:
1. Work Plan renamed/described as Workflow in a secondary document;
2. repeated pattern auto-registers an approved Workflow;
3. high confidence bypasses C4 clarification;
4. blocking clarification gains a default;
5. sibling scope chosen by string similarity;
6. planner lowers criticality after a "simple" user wording;
7. unavailable Role substituted with a similar approved Role;
8. future communication capability treated as already approved;
9. similarity score overrides a Workflow precondition;
10. ReviewRequirement treated as satisfied review;
11. DecisionRequirement treated as exercised Right;
12. persisted planning record treated as governance evidence/approval;
13. AI_SUGGESTION promoted to FACT_CLAIM without linked evidence;
14. Work Item chooses a model directly;
15. Phase 15 performs one of Phase 11's seven intake checks rather than making it answerable;
16. COMPOSE path reaches Orchestrator with no valid interpretation of intake check 1 / PO-4.

Report detected vs escaped probes honestly.

---

# Open items PO-1…PO-11

Review every open item individually and classify each as exactly one of:

- `BLOCKER BEFORE PHASE 15 APPROVAL`
- `REQUIRED CHANGE-CONTROL BEFORE ACTIVATION`
- `SAFE TO DEFER TO IMPLEMENTATION`
- `SAFE TO DEFER TO ORGANISATIONAL CONFIGURATION`
- `DOCUMENTATION / REPOSITORY GOVERNANCE ONLY`

Pay special attention to PO-4 and PO-11.

---

# Required output format

Return exactly sections A–R:

## A. FINAL VERDICT
`PASS` | `PASS WITH NON-BLOCKING NOTES` | `FAIL`

## B. BASELINE / CONTAINMENT VERIFICATION

## C. IDENTITY / LAYER-SEPARATION REVIEW

## D. REQUEST / INTENT / CLARIFICATION REVIEW

## E. CONTEXT / SCOPE REVIEW

## F. CLASSIFICATION / CRITICALITY REVIEW

## G. ROLE / SKILL INFERENCE REVIEW

## H. WORKFLOW MATCH / COMPOSITION REVIEW

## I. PLANNING OBJECT-MODEL REVIEW

## J. REVIEW / DECISION-RIGHT REVIEW

## K. KNOWLEDGE / EVIDENCE REVIEW

## L. ORCHESTRATOR HANDOFF / PO-4 REVIEW

## M. FAILURE / UX / LEARNING-BOUNDARY REVIEW

## N. OPEN ITEMS PO-1…PO-11

## O. REGRESSION / ASSURANCE RESULTS

## P. REVIEW CREDIBILITY
`LOW` | `MEDIUM` | `MEDIUM-HIGH` | `HIGH`

## Q. REMAINING BLOCKERS
Use `NONE` only if there are genuinely no blockers before human architecture approval.

## R. READINESS VERDICT

If ready for human architecture approval, the final line must be exactly:

`READY FOR HUMAN APPROVAL OF PHASE 15 INTENT & WORK PLANNING ARCHITECTURE`

Otherwise the final line must be exactly:

`NOT READY — REMAINING BLOCKERS`

Do not create any approval record. Do not modify the repository.
