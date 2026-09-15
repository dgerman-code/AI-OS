# Intent & Work Planning Architecture

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1
Approved architecture basis: Phase 13 approval commit `2c4b90def9a60f8b384feef10f8428c5b437597c`
Inherits: every approved Phase 1–13 constraint, without exception

> **This is an architecture proposal.** It modifies no approved Phase 1–13 artifact, specifies no
> runtime, and confers no authority. Every Phase 15 artifact is `PROPOSED`.

## 1. The problem

AI-OS coordinates execution **once a governed Workflow has already been selected**. Everything
upstream of that selection is currently assumed: someone knows which Workflow applies, which Roles
it activates, which Reviews it carries and which Decision Rights gate it.

For the intended product that assumption fails. A user writes:

> "Review this partner email. They blame us for the delay. Check whether they are right and
> prepare a firm but professional response."

and must not be required to know — or to name — a Workflow ID, a Role ID, a Skill, a Review
Profile, a Decision Right, a Model Profile, a routing policy, a work-item structure, or anything
about the state machine. The system has to understand the request, work out what it implies, and
turn it into something the approved Orchestrator can accept.

**Phase 15 is that layer, and nothing more.** It sits strictly *before* the Orchestrator and hands
it a trigger the Orchestrator already knows how to validate.

## 2. Where the layer sits

```text
Natural-language Request
        │
        ▼
┌─────────────────────────────────────────────┐
│  Phase 15 — Intent & Work Planning Layer    │
│                                             │
│   P1 Request Interpreter                    │
│   P2 Context Resolver                       │
│   P3 Work Classifier                        │
│   P4 Workflow Planner                       │
│   P5 Governance Preflight                   │
└─────────────────────────────────────────────┘
        │
        ▼   VALIDATED WORKFLOW SELECTION or VALIDATED WORK PLAN
        │
        ▼   Trigger envelope satisfying orchestrator intake checks 1–7
┌─────────────────────────────────────────────┐
│  Approved Phase 11 Orchestrator             │
│  run creation · stage activation ·          │
│  assignment · routing requests · reviews ·  │
│  decision requests · waiting · retry ·      │
│  rework · block · escalate · complete       │
└─────────────────────────────────────────────┘
        │
        ▼
   Phase 9 Model Router → execution
```

**Rule PL-1 — the planner is not a second Orchestrator.** It creates no run, activates no stage,
makes no assignment, issues no routing request, satisfies no review, exercises no Decision Right,
performs no retry, and completes nothing. It produces a **proposal** and stops. Everything after
the handoff boundary is Phase 11's, unchanged.

**Rule PL-2 — the five functions are functions, not agents.** P1–P5 are stages of one deterministic
pipeline. None is a standing persona, none has a name a user addresses, none persists between
requests, and none may be described as an agent (`ROLE != AGENT INSTANCE`, and a planner function
is not even a Role).

## 3. The extended identity chain

Phase 15 adds four objects of its own — `Request`, `WorkIntent`, `WorkPlan` and
`PlannedWorkItemSpec` — and separates every link in the chain they extend:

> `REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK !=`
> `PLANNED WORK ITEM SPEC != WORK ITEM != ROLE != MODEL != ORCHESTRATOR != HUMAN AUTHORITY`

The three-way separation in the middle of that chain is the one the approved Phase 11 model
cares about most, so it is stated on its own as well:

> `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`

A **Task / Activity** is defined once in an approved Workflow definition and is unchanged by any
run (`orchestration/execution-run-model.md` §4). A **Work Item** is the run's instance of that
Task, created inside a run. A **`PlannedWorkItemSpec`** is neither: it is a Phase 15 planning
record written before any run exists, and it neither defines a Task nor is an instance of one.

| Object | Is | Is not |
|---|---|---|
| **Request** | What the user actually wrote, verbatim, at a point in time | An instruction the system has understood |
| **Work Intent** | The system's structured reading of that request | What the user meant — it is a reading, and it is `AI_SUGGESTION` |
| **Work Plan** | An instance-level composition for **this** request | A Workflow. See §4 |
| **Workflow** | An approved reusable registry pattern (Phase 5) | Anything Phase 15 may create |
| **Workflow Run** | One bounded execution (Phase 11) | Anything Phase 15 may create |
| **Task / Activity** | What an approved Workflow definition says is to be done, defined once and unchanged by any run (Phase 5) | Something Phase 15 may define, edit or create |
| **Planned Work Item Spec** | A Phase 15 planning record describing work a validated plan stage implies | A Task, a Work Item, or a Work Item in an earlier state. It has no run, no runtime state and no assignment |
| **Work Item** | The run's instance of a Task, created by Phase 11 inside a run | Anything Phase 15 may create, assign or hold |
| **Role** | An approved professional methodology profile | A persona the planner picks by vibe |
| **Model** | A replaceable runtime chosen by the Phase 9 Router | Anything Phase 15 may choose |
| **Orchestrator** | The coordinator of a run | Anything Phase 15 may act as |
| **Human authority** | A person holding a Decision Right | Anything a confidence score approximates |

**Rule PL-3 — a Work Plan never acquires Workflow identity.** It has its own identifier space
(`work_plan.<id>`), it is never written into the Workflow Registry, it is never referenced as
`workflow.<id>`, and no process promotes it. `planning/workflow-candidate-learning-boundary.md`
states the one permitted relationship: a **suggestion** a human may act on.

## 4. MATCH and COMPOSE

Two paths, and the planner must be able to say which one it took and why.

| Path | When | Result |
|---|---|---|
| **MATCH** | The request maps cleanly onto one approved Workflow, or an approved composition of them, and no governance conflict exists | A **workflow selection**: `workflow.<id>` @ version, with its own preconditions satisfied |
| **COMPOSE** | No approved Workflow fits, or every candidate carries a governance conflict | An **instance-level Work Plan** built from approved primitives: approved Roles, approved Skills, approved Review Profiles, approved Decision Rights, and Phase 8 knowledge requirements |

**Rule PL-4 — COMPOSE assembles approved primitives; it never invents one.** A composed plan may
arrange existing Roles into stages that no Workflow declares. It may not create a Role, a Skill, a
Review Profile, a Decision Right or a Workflow, and it may not weaken one. Where a required
primitive does not exist, the plan **fails closed** (`planning/failure-and-escalation-model.md`).

**Rule PL-5 — a composed plan is instance-level, permanently.** It is bound to one Request, one
scope and one point in time. Running it twice is two plans. Nothing in the system reads a Work Plan
as a reusable pattern, and no accumulation of similar plans changes that.

## 5. What the layer must never do

These are the constraints the rest of the package is written against. Each is stated once here and
enforced somewhere specific.

| # | Never | Enforced in |
|---:|---|---|
| N-1 | Invent a Role, Skill, Review Profile, Decision Right or Workflow | `role-skill-requirement-inference.md`, `governance-preflight.md` |
| N-2 | Turn a generated plan into an approved reusable Workflow | `workflow-candidate-learning-boundary.md` |
| N-3 | Select or exercise human authority | `governance-preflight.md` |
| N-4 | Treat confidence as authority | `work-plan-object-model.md` §7 |
| N-5 | Downgrade criticality, sensitivity, residency, materiality, review or decision requirements | `work-classification-and-criticality.md` |
| N-6 | Silently cross a scope boundary | `context-scope-resolution.md` |
| N-7 | Infer a missing Decision Right from business necessity | `governance-preflight.md` |
| N-8 | Convert AI output into approved or canonical knowledge | `work-plan-object-model.md` §6 |
| N-9 | Create a permanent autonomous agent | PL-2, `user-experience-contract.md` |
| N-10 | Choose a Model Profile | `orchestrator-handoff-contract.md` |
| N-11 | Instantiate a Phase 11 runtime `Work Item`, or any other runtime identity | `orchestrator-handoff-contract.md` HO-6, HO-13, HO-14; `work-plan-object-model.md` OM-16 |

## 6. The planning sequence

Deterministic and inspectable. Every step records what it concluded and on what basis.

| # | Step | Function | Output object |
|---:|---|---|---|
| 1 | Capture the request verbatim | P1 | `Request` |
| 2 | Derive the structured intent | P1 | `WorkIntent` |
| 3 | Resolve scope | P2 | `ScopeResolution` |
| 4 | Derive work requirements | P3 | `WorkRequirementSet` |
| 5 | Derive criticality and risk flags | P3 | flags on the `WorkRequirementSet` |
| 6 | Infer required Role / Skill capabilities | P4 | `RoleRequirement`, `SkillRequirement` |
| 7 | Search approved Workflow candidates | P4 | `WorkflowMatchAssessment` |
| 8 | Score and rank applicability | P4 | scores on the assessment |
| 9 | Select **or** compose | P4 | workflow selection, or `WorkPlan` + `PlanStage` set |
| 10 | Attach reviews, Decision Rights, evidence requirements, stop conditions and stage dependencies | P4 | `ReviewRequirement`, `DecisionRequirement`, `EvidenceRequirement` |
| 11 | Validate | P5 | `PlanValidationResult` |
| 12 | **Only then**, and only where the execution path is eligible to produce one, describe each **validated** stage's work | P5 | `PlannedWorkItemSpec` — **never** a `work_item.<id>` (N-11) |
| 13 | Hand off — **only** on a passing preflight, and only through a basis the approved downstream contract accepts | P5 | trigger envelope |

**Rule PL-8 — the sequence is acyclic, and step 12 is downstream of step 11.** A
`PlannedWorkItemSpec` is derived from a **validated** `PlanStage` (HO-6), so it cannot exist before
validation and it is never an input to the validation that must precede it. Nothing in steps 1–11
reads a spec, and no preflight check takes one as evidence. Eligibility is decided at step 12 and
nowhere earlier: where the execution path is not eligible to produce a specification at all, step 12
produces nothing and the plan is no less valid for it.

**Rule PL-6 — similarity never overrides a constraint.** A semantic score may rank candidates. It
may not override a Workflow precondition, a Role constraint, a Review Profile requirement, a
Decision Right, or a scope boundary. Ranking answers *which candidates are worth checking*;
checking answers *whether any of them may be used*, and only the second answer is binding.

## 7. Relationship to the approved handoff boundary

The Orchestrator's intake performs seven checks before any work is scheduled
(`architecture/orchestrator-architecture.md` §5). Phase 15's obligation is to make each of them
answerable, not to perform them:

| Intake check | What Phase 15 supplies |
|---|---|
| 1. Workflow definition resolves at a named version | A `workflow.<id>` @ version (MATCH). For COMPOSE, a validated `work_plan.<id>` whose stages each bind approved definitions — which is **not a Workflow definition**, so whether it is admissible at all is the Orchestrator's to decide and is open as PO-4 |
| 2. Orchestrator Policy resolves at a named version | The policy reference the plan assumes; the Orchestrator still resolves it |
| 3. Exactly one governed scope, and the originator may act in it | `ScopeResolution` with exactly one scope, or a blocking failure |
| 4. Sensitivity, handling and residency present or explicitly assessed | Carried from `ScopeResolution` and the request material; **unassessed is restricted** |
| 5. Criticality band resolves | The band from `work-classification-and-criticality.md` |
| 6. Not a duplicate under the same idempotency key | An idempotency key derived from the Request identity |
| 7. Every declared prerequisite reference resolves, or is declared `FUTURE_GOVERNANCE_REFERENCE` and therefore non-executable | The `EvidenceRequirement` set, each reference in exactly one of three states: **`RESOLVED`**, **`FUTURE_GOVERNANCE_REFERENCE`** (declared, non-executable), or **`UNKNOWN`** — and a plain `UNKNOWN` is a dangling reference, which **blocks**. `UNKNOWN` is never equivalent to `FUTURE_GOVERNANCE_REFERENCE` |

**Rule PL-7 — the Orchestrator re-checks everything.** Phase 15 supplying an answer does not
relieve intake of validating it. A planner that could satisfy an intake check by asserting it would
be a planner that can start a run, and PL-1 says it cannot.

## 8. Document map

| Artifact | Owns |
|---|---|
| `planning/intent-work-planning-architecture.md` | This document: the layer, its boundary, the identity chain, the sequence |
| `planning/request-intent-model.md` | `Request` and `WorkIntent`; what is inferred and what stays `UNKNOWN` |
| `planning/context-scope-resolution.md` | Scope inference and the separator boundary |
| `planning/work-classification-and-criticality.md` | Work class, criticality, risk flags, high-stakes detection |
| `planning/role-skill-requirement-inference.md` | Deriving Role and Skill requirements from semantics |
| `planning/workflow-matching-and-composition.md` | MATCH scoring, COMPOSE rules, the precedence of constraints over scores |
| `planning/work-plan-object-model.md` | The seventeen planning records, their authority status and lifecycle; the confidence model |
| `planning/clarification-policy.md` | Infer-when-safe; the five ambiguity classes |
| `planning/governance-preflight.md` | The validation gate before handoff |
| `planning/orchestrator-handoff-contract.md` | The trigger envelope and what crosses the boundary |
| `planning/failure-and-escalation-model.md` | The thirteen planning failure modes and their dispositions |
| `planning/workflow-candidate-learning-boundary.md` | Repeated-pattern suggestion, and why it never self-registers |
| `planning/user-experience-contract.md` | What the user sees and never has to choose |
| `planning/exemplars.md` | Six fully worked examples |
| `planning/open-items.md` | What Phase 15 deliberately leaves open |
| `planning/phase-15-self-check.md` | Producer self-check, limitations, harness credibility |
| `validation/phase_15_validation.py` | Cross-document assurance |
| `validation/phase_15_mutation_probes.py` | Controlled weakenings against that assurance |

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no LLM inference runtime, embedding or
semantic-search engine, planner service, vector store, provider integration, execution runtime,
agent framework, retrieval pipeline, user interface, database schema, migration, queue, worker,
scheduler, deployment or configuration, and it binds no model, provider or runtime technology.
