# Governance Preflight

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. What preflight is

The last gate inside Phase 15. A plan that passes may be handed to the Orchestrator. A plan that
fails is not handed over in a reduced form — there is no partial handoff.

**Rule GP-1 — passing preflight is not approval.** It means the plan is internally coherent and
governance-complete enough to be *offered* to the Orchestrator, which then validates it again
independently (`planning/intent-work-planning-architecture.md` PL-7). Nobody has approved the
work, the conclusions, or the acts.

## 2. The checks

| # | Check | On failure |
|---:|---|---|
| **G-1** | Exactly one governed scope is resolved; `entitlement_status` is `TO_BE_CHECKED_AT_INTAKE` | **BLOCK** — `NO_VALID_SCOPE` or `AMBIGUOUS_SCOPE` |
| **G-2** | Every `WorkIntent` field is present as a value or an explicit `UNKNOWN` (RI-3) | **BLOCK** — an unconsidered field is a planner defect |
| **G-3** | The criticality band resolves | **BLOCK** — `CRITICALITY_UNRESOLVED`. Never defaults to Routine |
| **G-4** | Sensitivity, handling and residency are present or explicitly `UNASSESSED`, and `UNASSESSED` is treated as restricted | **BLOCK** |
| **G-5** | Every `RoleRequirement` resolves to an approved, available Role; every fired conditional requirement is met (RS-6); every unavailable Role records `load_bearing` **and** `load_bearing_basis` (LB-3) | **BLOCK** — `REQUIRED_ROLE_UNAVAILABLE` where the determination is `LOAD_BEARING`, or a recorded constrained plan (RS-10). A missing determination is itself a **BLOCK** |
| **G-6** | Every `SkillRequirement` resolves to an approved Skill with a Phase 4 basis; no candidate Skill is activated (RS-8); every unavailable Skill records `load_bearing` **and** `load_bearing_basis` (LB-3) | **BLOCK** — `REQUIRED_SKILL_UNAVAILABLE` where the determination is `LOAD_BEARING`. A missing determination is itself a **BLOCK** |
| **G-7** | No blocking `ClarificationRequirement` is open; none carries a `default_if_unanswered` (CL-15) | **BLOCK** |
| **G-8** | Every `ReviewRequirement` names an approved Review Profile, and **none is marked satisfied** | **BLOCK** — `REVIEW_PROFILE_UNAVAILABLE`, or a planner defect if satisfaction was asserted |
| **G-9** | `constraint_overrides_attempted` is empty (MC-17) | **BLOCK** — the planner did the thing MC-4 forbids |
| **G-10** | Every contemplated act has its `DecisionRequirement` resolved to an **applicable approved** Right, or the act is removed from the plan | **BLOCK** — `NO_APPLICABLE_DECISION_RIGHT`. §3 |
| **G-11** | Every `EvidenceRequirement` names what must hold, with its epistemic type; none asserts an unestablished claim (OM-9); any requirement unsatisfied before the first executable dependent act is unmet, and any legitimately deferred one is declared `FUTURE_GOVERNANCE_REFERENCE` (FE-11, FE-12) | **BLOCK the plan** — `EVIDENCE_REQUIREMENT_UNSATISFIED`. Plan-level, never per-stage: preflight has no stages to block and there is no partial handoff (HO-2) |
| **G-12** | The plan is acyclic and every stage declares entry and exit criteria (MC-12) | **BLOCK** — `PLAN_VALIDATION_FAILED` |
| **G-13** | No stage requires crossing the resolved scope boundary (CS-4) | **BLOCK** |
| **G-14** | No plan element names a Model Profile, a provider or a routing decision (N-10) | **BLOCK** — model selection is Phase 9's |
| **G-15** | The plan is `work_plan.<id>`, is not written to the Workflow registry, and is not referenced as `workflow.<id>` (MC-14) | **BLOCK** |
| **G-16** | No confidence value is used as a basis for any of G-1, G-5, G-8, G-10 or G-13 (OM-13) | **BLOCK** |
| **G-17** | The gate stage, where one exists, has no Role participation (MC-13) | **BLOCK** |
| **G-18** | Every inherited floor — criticality, sensitivity, residency, review, decision — is at or above what the approved inputs require (MC-11, WC-10) | **BLOCK** |

**Rule GP-2 — a failed check is recorded with its evidence.** The `PlanValidationResult` names the
check, the element that failed it, and what would satisfy it. "Validation failed" with no locus is
not a result.

## 3. Authority resolution

**Rule GP-3 — resolve first, then fail closed.** For every act the plan contemplates, the planner
**searches for and resolves** the applicable approved Right before recording any absence. Reporting
a missing authority without having looked is as wrong as proceeding without one, and it trains
users to ignore the finding.

**Rule GP-4 — a missing Right blocks. There is no alternative branch.** Not a warning, not a
downgrade to "prepare only" unless the user asked for that, not an escalation that proceeds in
parallel. `NO_APPLICABLE_DECISION_RIGHT` stops the act.

**Rule GP-5 — business necessity is not an authority.** Not urgency, not seniority, not a deadline,
not the user's insistence, not a high confidence that the act is obviously fine, and not the
observation that a similar act was authorised before.

**Rule GP-6 — the five act postures.** A plan involving an external act states exactly which:

| Posture | Means |
|---|---|
| `PREPARING_ONLY` | Content is produced; no external act is planned |
| `REQUESTING_REVIEW` | A Review Profile will be invoked during the run |
| `REQUESTING_DECISION` | A named Decision Right will be requested during the run |
| `EXECUTING_NON_AUTHORITY_ACT` | An act that requires no Right — and the plan says why not |
| `BLOCKED_FROM_TRANSMISSION` | An act is contemplated and no applicable Right resolves |

**Rule GP-7 — `EXECUTING_NON_AUTHORITY_ACT` carries its justification.** An act asserted to need no
authority must say which acts it is **not**: not a release outside the entity under its name, not a
submission, not a commitment, not a disclosure of controlled information. An unjustified assertion
of this posture is a G-10 failure.

## 4. What preflight never does

**Rule GP-8 — it never satisfies a review.** `ReviewRequirement` records that a review will be
needed. Validation does not perform it, and a plan that marked one satisfied is defective.

**Rule GP-9 — it never exercises a Right.** It resolves *which* Right applies. The exercise happens
during the run, by a human.

**Rule GP-10 — it never grants entitlement.** Scope entitlement is decided by the approved access
boundary at intake.

**Rule GP-11 — it never converts a knowledge type.** An `EvidenceRequirement` stays a requirement
until met.

**Rule GP-12 — it never relaxes on a re-run.** A plan that failed and was revised is re-validated in
full. There is no "previously checked" shortcut, because the revision is what changed.

**Rule GP-14 — every preflight outcome is plan-level.** A check passes or fails for the plan. No
check produces a per-stage verdict, no check holds one stage while releasing another, and no check
emits a partial envelope — because activating and holding stages is Phase 11's and Phase 15 has no
run to act on (HO-2, FE-11).

## 5. The `PlanValidationResult` record

| Field | Content |
|---|---|
| `outcome` | `PASSED` · `FAILED` |
| `checks` | G-1…G-18, each `PASS` · `FAIL` · `NOT_APPLICABLE` with a reason |
| `failures` | The failed check, the element, and what would satisfy it (GP-2) |
| `act_posture` | One of the five (GP-6) |
| `constrained` | Whether the plan is constrained, and what it does not cover (RS-10) |
| `is_approval` | **`false`**, always. Declared rather than omitted, so that no consumer can read a pass as one |

**Rule GP-13 — `NOT_APPLICABLE` carries a reason.** A check marked inapplicable without one is
indistinguishable from a check that was skipped.

## 6. Non-Runtime Statement

This document is declarative architecture. It specifies no validator implementation, schema, API or
storage mechanism, and binds no provider or runtime technology.
