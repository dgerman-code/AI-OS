# Execution Run Model

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Definition and run are two objects

A **Workflow** is an approved definition in the repository (Phase 5). A **Workflow Run** is one bounded execution of it. The definition is immutable for the run's life: a run binds to `workflow.<id>` **at a named version**, and a later change to the definition produces a different run, never a mutation of this one.

The same rule governs the **Orchestrator Policy**, which is where coordination behaviour lives — retry classes permitted, gate timeouts, concurrency limits, escalation targets. **It is a separate object from the workflow definition**, versioned separately, and it may never change what a stage *means*, only how coordination around it behaves. A policy that could alter stage semantics would be a second, unreviewed workflow definition.

## 2. Fifteen runtime identity kinds

| # | Identity | Identifies | Scope of uniqueness |
|---:|---|---|---|
| 1 | **Orchestrator Policy Definition** — `orch_policy.<id>` @ version | The coordination rules in force | Governed; repository-authoritative |
| 2 | **Execution Run** — `run.<id>` | One bounded execution | Runtime |
| 3 | **Workflow Run binding** | The `workflow.<id>` **and version** this run executes | Recorded value |
| 4 | **Stage Instance** — `stage_inst.<id>` | One stage of one run | Runtime, within a run |
| 5 | **Activity Instance** — `activity_inst.<id>` | One activity within a stage instance | Runtime |
| 6 | **Work Item** — `work_item.<id>` | A unit of assignable work | Runtime |
| 7 | **Assignment Attempt** — `assign.<id>` | One attempt to bind a Role to a Work Item | Runtime |
| 8 | **Review Request** → **Review Instance reference** | The request, and the Phase 6 instance it created | Request runtime; instance governed |
| 9 | **Decision Request** → **Decision Record reference** | The request, and the Phase 7 record it created | Request runtime; record governed |
| 10 | **Model Invocation Request** → **Routing Decision reference** | The request, and the Phase 9 decision it produced | Request runtime; decision governed |
| 11 | **Handoff Instance reference** | The Phase 6 handoff this run moved through | Governed |
| 12 | **Human Intervention record** — `intervention.<id>` | One attributable human act on a run | Runtime record of a governed act |
| 13 | **Retry Attempt** — attempt ordinal within its parent | One re-execution of a classified step | Runtime |
| 14 | **Resume Point / Checkpoint** — `checkpoint.<id>` | A recorded point a run may resume from | Runtime |
| 15 | **Correlation / Causation identifiers** | Which events belong to one operation, and which caused which | Runtime |

> **A runtime identifier is never a governance identity.** Kinds 2 and 4–7 and 12–15 address executions; they are never quoted as the subject of a governed record. Where a run refers to something governed, it refers by **stable logical ID and version, recorded as values** — which is why kinds 8, 9, 10 and 11 are written as a *request* on one side and a *reference* on the other. Those are two objects, and merging them is how a request starts looking like an outcome.

## 3. What an Execution Run records

| Field group | Content | Mutability |
|---|---|---|
| **Identity** | `run.<id>`; parent run where this is a sub-run | Immutable |
| **Definition binding** | `workflow.<id>` @ version; `orch_policy.<id>` @ version | **Immutable for the run** |
| **Scope** | Exactly one governed scope, per Phase 2 | **Immutable.** A change is a new run |
| **Criticality** | The band, from Phase 3 | Immutable |
| **Sensitivity** | The **set** of Phase 8 labels, handling controls, residency constraints | Carried; narrowed only by governed reclassification |
| **Trigger** | Originator identity, trigger kind, idempotency key, intake validation result | Immutable |
| **State** | The four axes of `orchestration/state-machine-and-transitions.md` | Transitions only, each an execution event |
| **Progress** | Stage instances, activity instances, work items, assignment attempts | Append-only |
| **Governed references** | Review instances, Decision Records, Routing Decisions, handoffs, artifacts — each as ID **and version** | Append-only, **recorded as values** |
| **Open items** | Findings, conflicts and `UNKNOWN` states carried forward, each with the upstream rule permitting it | Append-only |
| **Checkpoints** | Resume points with the state and references valid at each | Append-only |
| **Correlation** | Correlation and causation identifiers | Immutable |

## 4. Task, Work Item and Assignment

Three objects that are routinely collapsed into one:

| Object | Owned by | What it is |
|---|---|---|
| **Task / Activity** | The Workflow definition (Phase 5) | What is to be done, defined once, unchanged by any run |
| **Work Item** | The run | An instance of that task needing someone or something to do it |
| **Assignment Attempt** | The run | One attempt to bind a Role — and, where permitted, a model execution — to that Work Item |

Reassignment creates a **new Assignment Attempt**, leaving the prior attempt recorded with its outcome. It does not edit the Work Item, and it never edits the Task: editing the Task would be rewriting the workflow definition from inside a run.

## 5. The Assignment Envelope — 12 fields

What an activation carries. It confers nothing not already carried by the Role, the Skill and the scope.

| # | Field | Content |
|---:|---|---|
| 1 | **Role ID** | `role.<id>` @ version — the profile activated, not a persona created |
| 2 | **Required skills / specialisations** | `skill.<id>` constraints the assignee must satisfy |
| 3 | **Scope** | The run's single governed scope; the assignment never widens it |
| 4 | **Task / activity reference** | The Phase 5 definition, by ID and version |
| 5 | **Criticality** | The band, which may raise requirements and never lowers them |
| 6 | **Required independence** | The Phase 6 class where this work feeds a review or assurance act |
| 7 | **Executor eligibility** | Human-only · model-executable · either — declared by the definition, never inferred |
| 8 | **Review restrictions** | Which reviews this assignee is **excluded** from as a consequence of doing this work |
| 9 | **Decision restrictions** | Which Rights this assignee may not exercise over this work |
| 10 | **Sensitivity and residency** | Carried from the run, narrowable, never widened |
| 11 | **Provenance** | Which stage, which dependency satisfaction, which policy rule produced this assignment |
| 12 | **Assignment reason** | Why this Role, recorded — so a later question about staffing has an answer |

**No seniority variants.** There is no junior, middle or senior form of a Role. Where work needs more capability, the requirement is expressed as a skill constraint, an independence class or a criticality band — all of which are governed — rather than as a rank, which is not.

Fields 8 and 9 exist because the orchestrator is the component that can see both sides: it knows who did the work and who is about to review it. **Recording the exclusion at assignment time is what makes the later independence check checkable** rather than a matter of someone noticing.

## 6. Sub-runs

A stage may spawn a **sub-run** — a bounded child execution with its own `run.<id>`, its own state, and the **same scope, sensitivity and residency** as its parent. A sub-run may narrow what it sees. It may not widen it, and it may not be used to reach a scope the parent could not reach: that would be a scope crossing wearing a different name.

The parent waits on the child as an ordinary dependency. A child's completion is a child's completion; it satisfies no gate the parent owes.
