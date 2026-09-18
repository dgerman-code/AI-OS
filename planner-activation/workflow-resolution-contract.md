# Workflow Resolution Contract — MATCH and COMPOSE

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

## 1. Two paths, and the difference that matters

| Path | Binds | Creates |
|---|---|---|
| **MATCH** | An approved `workflow.<id>` **at its approved version**, unchanged | Nothing. The definition already exists |
| **COMPOSE** | An instance-level `work_plan.<id>@<version>` built from approved primitives | A plan bound to one request, one scope, one moment |

**Rule WR-1 — MATCH binds; it never edits.** The planner may not add a stage, remove a gate,
relax a precondition or substitute a Role in an approved Workflow. A Workflow that does not fit
is not matched — it is a reason to COMPOSE.

**Rule WR-2 — MATCH requires the approved version, not merely an approved identity.** A
`workflow.<id>` bound at a version that is not the approved one is **not** a binding, and the
preflight blocks with `WORKFLOW_VERSION_STALE`. An identity without a version blocks likewise.

**Rule WR-2a — MATCH requirements come from the selected Workflow, not from the planner payload.**
Before a MATCH can issue an Execution Basis, the preflight resolves the selected approved Workflow
card at the bound version and checks its mandatory requirement set against the proposed
`PlannerOutput`. The planner payload is a proposal; omission from it is never evidence that the
Workflow does not require something. Every concrete `ALWAYS` participating Role, explicit
`REVIEW_REQUIRED_REFERENCE`, explicit `HUMAN_GATE_REFERENCE`, and artifact precondition represented
by the Phase 16 contract must be present in the corresponding planner requirement family. An
omission is fail-closed and the MATCH produces no basis.

An `ALWAYS` parameterised Role slot is also mandatory. Where the current `PlannerOutput` contract
cannot prove the slot's binding, ownership or cardinality constraints, the preflight fails closed
rather than treating any semantically plausible Role as an implicit binding. This targeted rule
adds no slot registry and no new Role. Conditional Role bindings remain governed by their trigger
conditions and are not silently promoted to `ALWAYS`.

`Activated Skills / Packs` entries in the current exemplar Workflow cards are explicitly labelled
**references only**. They therefore remain subject to the existing Phase 4/Phase 16 eligibility
path when actually activated and are not incorrectly promoted into unconditional mandatory
requirements merely because they are listed in that reference section.

**Rule WR-3 — COMPOSE assembles approved primitives and invents none.** Approved Roles, approved
Skills, approved Review Profiles, approved Decision Rights, Phase 8 knowledge requirements. Where
a required primitive does not exist, the plan **fails closed**.

## 2. A Work Plan is not a Workflow, by construction

**Rule WR-4 — the identifier spaces are disjoint and the constructor enforces it.**
`WorkPlan.__post_init__` raises on any identifier outside `work_plan.`, and raises on one that
begins `workflow.`. This is not a convention a later pass could quietly break; it is a refusal in
the type.

**Rule WR-5 — there is no write path to the registry.** The reference store has no method that
registers a Workflow and none that sets a candidate to `APPROVED`. Self-promotion is impossible
because there is nothing to call, not because a rule forbids calling it.

**Rule WR-6 — a composed plan is instance-level, permanently.** Bound to one Request, one scope
and one point in time. Running the same request tomorrow produces a second plan, and the two are
separate records even if identical.

## 3. Repeated patterns

**Rule WR-7 — a repeated COMPOSE shape may emit exactly one thing: a `PROPOSED` candidate.**

| Field | Value |
|---|---|
| `status` | `PROPOSED` — the only permitted value |
| `observed_plans` | The plans that produced the observation, at their versions |
| `is_approved` | `false` |
| `is_matchable` | `false` |

**Rule WR-8 — a candidate is inert.** It is not matched against, influences no plan, and cannot
become a Workflow inside Phase 16. A human may take it into Phase 5 change control as input
material, where it earns no shortcut for having been machine-generated.

## 4. The gate stage

**Rule WR-9 — a gate stage has no Role participation.** A gate is not work: it is a point at
which a human decides. A composed plan whose gate stage names a Role is refused by the preflight.

## 5. Plan shape

**Rule WR-10 — a composed plan is acyclic and every dependency resolves.** The preflight walks
the stage graph iteratively and blocks on a cycle or a dangling dependency. A plan the
Orchestrator could not schedule is not a plan that should reach it.

**Rule WR-11 — stage identity is unique before a basis is issued.** Duplicate stage ids used to
collapse into one another silently: two stages with the same id became one, and the second
stage's owner, artifact and dependencies simply disappeared. Every planned work item spec is
derived from stage identity, so a collision is not cosmetic. `DUPLICATE_STAGE_IDENTITY`.

**Rule WR-12 — every effective stage owner resolves.** A non-gate stage must name an owner; the
owner must be in the approved Role universe; and the plan must have declared an owned conclusion
for it. An owner appearing only inside a stage is an assignment nobody declared and no approved
registry was asked about. `STAGE_OWNER_UNRESOLVED`. The Role and Skill eligibility rules the
check resolves against are in `registry-eligibility-contract.md`.

## 6. Non-Runtime Statement

This document is declarative architecture. It specifies no scoring implementation, index,
embedding, matcher or storage mechanism, and binds no provider or runtime technology.