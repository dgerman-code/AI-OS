# AI-OS Workflow Registry Design

Status: PROPOSED — Phase 5 architecture candidate
Version: 0.1
Depends on: approved Phase 3 Role Registry, approved Phase 4 Skill / Specialisation / Pack Registry

## Purpose

The Workflow Registry stores reusable, provider-independent **coordination patterns**: how work moves from a trigger to a completion position across Roles, capabilities, artifacts, knowledge states, gates and exception paths.

It exists because coordination is a real, reusable, governable object — and because coordination is exactly the place where authority tends to leak. A sequence that says "then the plan is approved" quietly manufactures an approval. A stage that says "the lead signs off the technical position" quietly transfers a specialist conclusion. The registry's job is to make coordination reusable **without** letting it become authority.

## The separation this registry must preserve

```
ROLE  !=  SKILL  !=  WORKFLOW  !=  REVIEW PROFILE  !=  DECISION RIGHT  !=  MODEL  !=  RUNTIME
```

A Workflow **coordinates work**. It does not become a Role, does not own a professional conclusion, does not grant review independence, does not grant human authority, and does not itself make information canonical.

The Workflow Registry sits **downstream** of the Role Registry and the Skill Registry. It consumes their identities; it cannot amend them. Where a Workflow and a Role Card disagree, the Role Card governs and the Workflow is defective.

---

## 1. Workflow identity model

A **Workflow** is a reusable governed coordination pattern. A Workflow Card specifies:

| Element | What it fixes |
|---|---|
| Triggering condition | What causes this pattern to become applicable |
| Required inputs / preconditions | What must exist before the pattern can start |
| Ordered or partially ordered stages | The coordination shape, including what may run in parallel |
| Stage-entry criteria | What must be true to enter a stage |
| Stage-exit criteria | What must be true to leave it |
| Participating Role IDs | Which approved Roles take part, and in what participation type |
| Applicable Skill / Specialisation / Pack references | Which Phase 4 capabilities are expected to be active — by reference only |
| Artifact inputs / contributions / outputs | Which Role-owned artifacts the pattern reads and which it advances |
| Knowledge-state expectations | The states inputs must hold and outputs are expected to reach |
| Gate references | Which human decision rights and review requirements sit on the path |
| Exception / rollback / rework paths | What happens when the normal path fails |
| Completion criteria | What "this workflow finished" means |
| Termination / cancellation criteria | What "this workflow stopped without completing" means |
| Criticality-sensitive depth | How the pattern deepens as criticality rises |
| Version / status / governance owner | Change control |

### A Workflow must NOT

1. own professional methodology that belongs to a Role;
2. own a first-class professional conclusion;
3. create artifact ownership where a Role Card already defines it;
4. create a Review Profile or a reviewer identity;
5. create or grant a Decision Right;
6. turn AI output into `APPROVED` or `CANONICAL` by itself;
7. select or bind an AI model as identity;
8. execute itself.

Each prohibition is restated as an enforceable rule in `workflows/_standards/common-workflow-constraints.md`, which every Workflow Card inherits.

### Workflow ID convention

```
workflow.<stable_snake_case_name>
```

The ID must be stable across versions and free of anything that is not the coordination pattern itself. Do **not** encode into the stable ID:

- an organisation, client or department;
- a model vendor, model name or agent framework;
- a temporary project or campaign name;
- an individual person;
- a version number;
- a runtime technology or deployment target.

`workflow.eu_grant_application_development` is a valid ID. `workflow.acme_horizon_2026_claude_pipeline_v2` encodes four things that will change while the coordination pattern does not.

Renaming a Workflow's display name does not change its ID. Retiring a Workflow tombstones its ID; the ID is never reused for a different pattern.

---

## 2. Workflow versus adjacent concepts

This section is the disambiguation test. If a proposed Workflow is better described by the right-hand column, it does not belong in this registry.

### Workflow vs Role

| Role | Workflow |
|---|---|
| Professional methodology and ownership boundary | Coordination and order of work among Roles |
| Owns conclusions, artifacts and a decision-right interface | Owns none of these; references them |
| Exists whether or not any particular sequence runs | Exists only as a pattern of participation |

A Workflow that starts accumulating methodology, owned artifacts and a professional conclusion is a Role wearing a Workflow ID. Escalate it under the Role-vs-Workflow test in the constraints document.

### Workflow vs Skill

| Skill | Workflow |
|---|---|
| A reusable capability or technique | When and in what sequence capabilities and Roles participate |
| Applies within one Role's execution | Spans Roles and stages |
| Governed by Phase 4 mapping records | Governed by this registry, subordinate to those records |

A single skill invocation is not a Workflow. "Verify these sources" is a Skill; "prepare a decision-grade document" is a Workflow.

### Workflow vs Project Plan

| Project plan | Workflow |
|---|---|
| Assignment-specific | Reusable registry pattern |
| Carries dates, named people, resources, budget | Carries none of these |
| Instantiated once, then diverges from every other plan | Identical wherever the pattern applies |

A Workflow is what a project plan is an *instance* of. Dates, resource loading and named individuals belong to the instance, never to the registry entry.

### Workflow vs SOP

| SOP | Workflow |
|---|---|
| Operating instruction or procedure, usually organisation-specific | Governed cross-Role coordination pattern |
| Tells one team how to perform steps | Tells the system which Roles participate, in what order, under which gates |
| May be prescriptive about tools and formats | Provider- and tool-independent |

A Workflow **may reference** an SOP as a controlled source for a stage's activities. It is not itself an SOP, and importing an SOP wholesale into a Workflow Card is a common way to smuggle organisation-specific instruction into a reusable registry.

### Workflow vs Checklist

| Checklist | Workflow |
|---|---|
| A verification list | A stateful coordination path |
| Flat; every item independent | Has progression, branches, gates and rework loops |
| Answers "did we do these things?" | Answers "where are we, what may happen next, and what blocks it?" |

A Workflow may *contain* checklist-shaped exit criteria. A checklist with no progression, no participation model and no gate is not a Workflow.

### Workflow vs Review Profile

| Review Profile | Workflow |
|---|---|
| Independent review identity and methodology | Coordination pattern |
| Defines reviewer independence, scope, materiality and severity | May state that a review is required and reference its ID |
| Reserved for a later phase | Phase 5 |

A Workflow may carry a `REVIEW_REQUIRED_REFERENCE` pointing at a `review.<id>`. It may **not** define who is independent, what the review method is, or when a review is satisfied. Writing "the lead reviews the output" into a stage creates a fake reviewer identity and is prohibited.

### Workflow vs Decision Right

| Decision Right | Workflow |
|---|---|
| Human authority | Coordination pattern |
| Held by a person under the Decision Rights Register | Referenced by a Workflow as a gate |
| Can be exercised, delegated or withheld | Can be neither exercised nor satisfied by a Workflow |

A Workflow may carry a `HUMAN_GATE_REFERENCE` pointing at a `decision.<id>`. Reaching that point in the Workflow is not the decision; it is the moment the decision becomes due.

### Workflow vs Orchestrator

| Orchestrator / runtime | Workflow Registry |
|---|---|
| Executes, schedules, retries, assigns and monitors instances | Declares the pattern |
| Later implementation phase | Phase 5 architecture |
| Must validate against the registry | Must not be mutated by the runtime |

The registry is declarative. Nothing in Phase 5 schedules, queues, routes, assigns a model, calls an API or persists an instance.

---

## 3. Workflow composition model

The composition model is deliberately small and human-readable. It is **not** a runtime DSL: there is no execution semantics, no expression language, no state machine serialization format and no scheduling primitive.

### Primitives

| Primitive | Meaning |
|---|---|
| `TRIGGER` | The condition that makes this Workflow applicable to an assignment |
| `PRECONDITION` | What must already be true or already exist before the Workflow may start |
| `STAGE` | A bounded segment of coordination with its own entry and exit criteria |
| `ACTIVITY` | Bounded work performed inside a Stage by a participating Role |
| `ARTIFACT_CONTRIBUTION` | A named contribution to a Role-owned artifact; never a transfer of ownership |
| `STATE_EXPECTATION` | The knowledge state an input must hold, or an output is expected to reach |
| `GATE_REFERENCE` | A pointer to a `decision.<id>` human gate or a `review.<id>` review requirement |
| `BRANCH` | A conditional divergence in the path, with a stated condition |
| `EXCEPTION_PATH` | The route taken when the normal path cannot proceed |
| `REWORK_LOOP` | A governed return to an earlier Stage, preserving provenance |
| `COMPLETION_CRITERION` | What must be true for the Workflow to be complete |
| `TERMINATION_CONDITION` | What causes the Workflow to stop without completing |
| `WORKFLOW_REFERENCE` | A declarative pointer to another Workflow used as a reusable child pattern; it names, it does not execute |

### Every Stage must answer seven questions

1. **Why does this stage exist?** — its objective, in one sentence, distinct from every other stage.
2. **Which Role(s) participate?** — by approved `role.<id>`, with a participation type.
3. **What may they contribute?** — activities and artifact contributions, bounded by each Role Card.
4. **What must be true to enter?** — entry criteria, including required knowledge states.
5. **What must be true to exit?** — exit criteria, testable rather than aspirational.
6. **What artifact/state changes are expected?** — which artifacts advance and to which state.
7. **Which gate or review reference may block progression?** — the `decision.<id>` / `review.<id>` pointers on this stage.

A stage that cannot answer all seven is either not a stage or is hiding an authority transfer in the gap.

### `WORKFLOW_REFERENCE` — declarative composition

Some coordination patterns are genuinely reusable inside others. `workflow.decision_grade_document_preparation` is the clearest case: its shape recurs wherever a decision-grade document is produced. Without a way to say so, the registry either duplicates the pattern into every parent — which guarantees drift — or claims a composition it has no means of expressing.

`WORKFLOW_REFERENCE` is that means, and it is **declarative only**:

1. It points at a stable `workflow.<id>`, optionally with a version constraint or reference policy. **It does not execute the child.** There is no call, no scheduling, no retry, no nesting semantics, no call stack, no state-machine representation and no database form.
2. The parent card states the reference's **bounded purpose**, its **expected inputs**, its **expected outputs**, and **which parent Stage or Stages** it relates to.
3. Referencing a child transfers nothing: not Role ownership, not Skill compatibility, not review identity, not Decision Rights, not gates, not knowledge-state authority. The child's Roles remain the child's; the parent gains no capability by pointing.
4. The child's gates and review requirements **cannot be silently dropped**. Where the parent relies on an output the child produces only past a child gate or review, that dependency stays visible in the parent card.
5. **Acyclicity is an architecture validation rule.** A Workflow must not reference itself directly or transitively. A cycle is a registry defect, detectable by reading the cards, not a runtime problem to be handled at execution.
6. A reference may be optional or conditional only under a stated objective condition, declared like any other conditional activation.

Composition is **representability, not obligation**. A parent that does not cleanly compose the whole child says so; it does not force a reference to look tidy.

### Ordering

Stages are **partially ordered** by default. A Workflow Card states which stages are strictly sequential and which may proceed in parallel. Strict sequence must be justified by a real dependency — an input that does not exist yet, or a gate that must precede the next act — not by drafting convenience. Over-serialised workflows manufacture bottlenecks that the professional work does not have.

---

## 4. Workflow participation relationships

Five participation types. Three describe Role participation; two are explicitly **not** Role relationships and are named that way to stop them being read as one.

| Type | Applies to | Meaning |
|---|---|---|
| `LEAD_ROLE` | a `role.<id>` | Coordinates the Stage or Workflow. Gains **no** authority beyond its own Role Card. |
| `CONTRIBUTING_ROLE` | a `role.<id>` | Contributes bounded work or artifact content within its own Role Card scope. |
| `CONSULTED_ROLE` | a `role.<id>` | Provides professional input when a stated trigger applies; not present in every instance. |
| `REVIEW_REQUIRED_REFERENCE` | a `review.<id>` | **Not a Role relationship.** Points at a review requirement to be defined by the later Review Profile Registry. |
| `HUMAN_GATE_REFERENCE` | a `decision.<id>` | **Not a Role relationship.** Points at a human decision right in the Decision Rights Register. |

### Activation is a separate property, not a participation type

Participation type answers **what a Role does** in a Stage. It does not answer **whether the Role is engaged at all** in a given instance. Those are orthogonal questions, and collapsing them is how a triggered specialist who owns an artifact ends up typed as merely "consulted".

Activation is therefore declared as its own qualifier:

```
Activation: ALWAYS | CONDITIONAL(<objective trigger>)
```

| | `Activation: ALWAYS` | `Activation: CONDITIONAL(...)` |
|---|---|---|
| `CONTRIBUTING_ROLE` | Always produces bounded work or an owned artifact here | Produces an owned artifact **when the trigger applies** — the required treatment for triggered specialists |
| `CONSULTED_ROLE` | Always gives advisory input here | Gives advisory input when the trigger applies |

The discriminator between `CONTRIBUTING_ROLE` and `CONSULTED_ROLE` is **ownership within the Stage**, never frequency:

- **`CONTRIBUTING_ROLE`** — produces bounded work, artifact content, an owned artifact, or an owned professional conclusion in that Stage.
- **`CONSULTED_ROLE`** — advisory or input-only; **owns and advances nothing in that Stage**.

A Sector Technical Expert who produces `artifact.sector_technical_opinion` when sector materiality applies is a `CONTRIBUTING_ROLE` with `Activation: CONDITIONAL(sector materiality)`. An architect consulted on a deviation who produces no artifact in that Stage is a `CONSULTED_ROLE` with `Activation: CONDITIONAL(deviation from the design position)`.

No sixth participation type may be added to express conditionality, and the trigger inside `CONDITIONAL(...)` must be an **objective, testable condition** — not a judgement that the Role would be useful. Conditional activation narrows participation; it never widens Phase 4 compatibility or Role scope.

### Why not RACI

RACI is rejected as a mechanical model because its "A" — Accountable / Approver — is precisely the thing this architecture refuses to let a coordination pattern create. In RACI practice, someone is made Accountable for every activity, and that role then reads as an approver even when no human decision right exists and no Role Card grants the conclusion. The result is a fake approver Role invented by the coordination layer.

The vocabulary above has no "A". Approval is not a participation type at all: it is a `HUMAN_GATE_REFERENCE`, and it points outside the Workflow.

### Workflow lead is not workflow ownership

**A Role may be workflow lead without owning all conclusions or artifacts in the workflow.** This is the single most important rule in this section, and the one the exemplars stress-test hardest. `role.project_development_lead` leads `workflow.project_development_readiness` and integrates its workstreams; it does not thereby acquire the feasibility conclusion, the cost estimate, the financial model, the legal analysis or the E&S assessment. Each of those remains owned, and remains reviewable, under its own Role Card.

Lead means: coordinates sequence, convenes participation, integrates contributions, maintains the open-item position, and raises escalations. It does not mean: concludes, approves, overrides or absorbs.

### Parameterized Role slots — the Role Slot Binding Rule

A few coordination patterns are genuinely Role-agnostic: the shape of preparing a decision-grade document is the same whether a legal, financial or technical Role owns the document. Such a pattern may declare a **parameterized Role slot** rather than naming a concrete Role.

A slot is a hole in the pattern, and an unclosed hole is an authority leak. Every slot therefore declares, in the card itself:

1. **slot ID / name**;
2. **allowed source** — approved `role.<id>` only;
3. the **required ownership or interface condition** the bound Role must already satisfy;
4. **permitted participation type(s)**;
5. any **required artifact-ownership relationship**;
6. the **capability validation rule** against the approved Phase 4 mappings.

Binding rules:

- At instance binding a slot resolves to **exactly one concrete approved `role.<id>` per slot occurrence**, unless the slot explicitly declares a cardinality greater than one.
- Wildcards — "any Role", "whichever Role is appropriate" — are **prohibited** unless immediately followed by eligibility constraints testable against the Role Card and the approved registries.
- **A slot cannot grant ownership.** The bound Role must already own the relevant artifact or conclusion under its own Role Card. Binding selects an owner; it never creates one.
- Every capability activated for a bound Role must independently pass Phase 4 compatibility. **The Workflow and the slot are never evidence of compatibility.**
- A slot cannot bind a System Control Profile, a Review Profile, a Decision Right, a model or a runtime identity.
- Where no approved Role satisfies the constraints, the instance is `BLOCKED` or invalid for that assignment. The slot is not widened to make an assignment fit.

### Participation is bounded by Phase 4

A Workflow may reference Skills, Specialisations and Packs for a participating Role only where the approved Phase 4 mapping records already make that Role compatible. A Workflow **cannot** widen compatibility. If a Workflow appears to need a Role to use a capability Phase 4 does not allow it, that is a Phase 4 mapping question, raised as a finding — never resolved inside the Workflow Card.

---

## 5. Stage transition semantics

### Stage completion is not approval

Completing a Stage means the Stage's exit criteria are satisfied. It does not mean the work is approved, reviewed, accepted or canonical. A Workflow that treats stage advancement as approval has manufactured authority.

### Knowledge states are not inferred from movement

The transitions

```
DRAFT -> REVIEWED -> APPROVED -> CANONICAL
```

**cannot be inferred solely from stage movement.** A Workflow may require a knowledge state as an entry or exit condition — "this stage may not be entered until the demand study is `REVIEWED`" is legitimate. A Workflow may **not** itself promote a state unless the underlying governed human or review rule permits that promotion, and the promotion is then attributable to that rule, not to the Workflow.

`SUPERSEDED` behaves the same way: a Workflow may detect that an input has been superseded and must branch or block on it, but the supersession itself is a governed act elsewhere.

### Blocking and branching states

`CONFLICT_DETECTED` and `UNKNOWN` must be able to block or branch a Workflow wherever they are **material** to the stage's exit criteria or to a downstream gate. A Workflow that can advance past a material `CONFLICT_DETECTED` without either resolving it or explicitly carrying it as an open item is defective.

**Critical unresolved assumptions must not disappear merely because a workflow advances.** An assumption that was material at Stage 2 is still material at Stage 6 unless it was resolved, and the Workflow must carry it forward in its open-item position rather than letting stage advancement quietly retire it. This is the failure mode that produces confident final documents built on forgotten `ASSUMPTION` inputs.

### Generic stage outcomes

Every Stage resolves to exactly one of six outcomes. These are **workflow-instance progression outcomes, not knowledge states**, and must never be written into an artifact's state field.

| Outcome | Meaning |
|---|---|
| `COMPLETE` | Exit criteria satisfied; no open items material to the next stage |
| `COMPLETE_WITH_OPEN_ITEMS` | Exit criteria satisfied; named open items carried forward explicitly |
| `BLOCKED` | Cannot proceed; a precondition, input, gate or unresolved conflict prevents exit |
| `REWORK_REQUIRED` | Output insufficient; a governed return to this or an earlier stage is required |
| `ESCALATED` | Raised beyond the Workflow — an authority, scope, resource or integrity question the pattern cannot resolve |
| `CANCELLED` | Stopped deliberately; the assignment or Workflow is discontinued |

`COMPLETE_WITH_OPEN_ITEMS` exists deliberately. Without it, coordination pressure forces a binary choice between blocking on every loose end and declaring a clean `COMPLETE` that is not true. The open items must be named, carried and visible at every subsequent stage and at every gate.

### Open-item materiality

Naming an open item is not disposing of it. Without a materiality rule, `COMPLETE_WITH_OPEN_ITEMS` becomes a universal waiver: anything can pass any exit as long as it is written down. **Every open item carried under `COMPLETE_WITH_OPEN_ITEMS` is classified**, at minimum, as one of two values:

| Classification | Meaning |
|---|---|
| `NON_MATERIAL_TO_NEXT_STEP` | Resolving it could not change the next Stage's permitted work, any downstream conclusion, any review position, any gate's evidence basis, or the terminal conclusion. |
| `MATERIAL_TO_NEXT_STEP_OR_GATE` | Any unresolved item that could change the next Stage's permitted work, a specialist conclusion relied on downstream, a required review position, a human gate's evidence basis, a transmitting act, or a terminal readiness conclusion. |

This is **progression materiality only**. It is not a risk-severity taxonomy, it does not rank importance, and it must not be extended into one — risk severity belongs to the risk Roles and their own methodologies.

**A `MATERIAL_TO_NEXT_STEP_OR_GATE` item cannot support `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` for the progression it is material to.** The default outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.

The **only** exception is a **named external human Decision Right** that explicitly permits proceeding with that unresolved material item. Where it applies:

- the Workflow records the `decision.<id>` gate reference;
- the item **remains unresolved and open** — it is not relabelled resolved, downgraded, or removed from the carry-forward;
- the Workflow does not decide the waiver, does not define its conditions and does not assert that it was granted.

Who holds that Decision Right and what its approval semantics are is Phase 7. Phase 5 only records that such a right is the sole route past a material item.

A missing required `review.<id>` may be **visible**, but visibility does not satisfy the review. Where the next Stage or a gate requires that review, its absence blocks progression unless an external Decision Right explicitly governs proceeding without it.

`UNKNOWN`, `CONFLICT_DETECTED` and a material `ASSUMPTION` are **never cleared by stage movement** — not by advancing, not by being named, and not by being carried into a later stage's open-item list.

---

## 6. Criticality behaviour

The Workflow Registry inherits `architecture/project-criticality-policy.md` in full, including the automatic Enhanced Decision-Grade trigger at €50m and the sub-threshold complexity triggers.

### What criticality may increase

- evidence depth and source-verification rigour;
- the number of specialist contributions required;
- mandatory stage depth — stages that are optional at Routine become mandatory;
- required reviews and gate references;
- traceability granularity;
- exception-handling rigour;
- rework requirements before a gate may be reached.

### What criticality must NOT do

**Criticality must not create a new Workflow identity merely because a project is larger.** A €60m project and a €6m project of the same professional shape run the *same* Workflow at different depths. Splitting them into `workflow.small_project_readiness` and `workflow.large_project_readiness` duplicates the coordination pattern, guarantees the two copies drift, and encodes a monetary threshold into a stable ID.

Criticality also must not change Role identity. The same Role Registry is reused at every band; what changes is which Roles are triggered, how deep their contribution must be, and how many gates sit on the path.

### The duplication test

Prefer **one Workflow with criticality-conditioned depth** over duplicate Workflows, unless the professional process is *genuinely different* — different Roles owning different conclusions, a different artifact set, or a different gate structure that is not merely "more of the same gates".

A useful discriminator: if the two candidate Workflows would have the same Stage objectives and differ only in how much evidence each Stage demands, they are one Workflow. If they would have different Stage objectives — a competitive tender versus a negotiated award, say — they are two.

---

## 7. Relationship to the other registries

| Registry | Direction | What the Workflow Registry may do |
|---|---|---|
| Role Registry (Phase 3, approved) | upstream | Reference `role.<id>`; reference Role-owned artifacts; respect every Owns / Does Not Own boundary |
| Skill Registry (Phase 4, approved) | upstream | Reference `skill.<id>`, `specialisation.<id>`, `skill_pack.<id>` **only within existing Phase 4 compatibility**; never widen it |
| Review Profile Registry (later phase) | downstream | Reference `review.<id>` as a requirement; never define independence or method |
| Decision Rights Register (later phase) | downstream | Reference `decision.<id>` as a gate; never own, satisfy or bypass it |
| System Control Profiles | adjacent | A Workflow Controller may later *select* a Workflow; selection is not authorship and does not amend the registry |
| Model Registry / runtime | out of scope | No binding of any kind |

## 8. Change control

- Workflow Cards are versioned. The stable `workflow.<id>` does not change across versions.
- A version change must not silently alter authority, Role scope, gate references or artifact ownership. Any change touching those must be stated explicitly in the card's change record and is a governance change, not an editorial one.
- Retired Workflows are tombstoned with the reason and the surviving pattern, following the deprecation-register convention established in Phase 4.
- Runtime implementation must later **validate against** this registry. It must not mutate registry semantics to fit an execution engine.

## 9. Non-runtime statement

This document, and every artifact in `workflows/`, is declarative architecture. Nothing here implements or specifies orchestration, scheduling, queueing, agent execution, model routing, database schema, API surface, user interface or automation code. No model, provider or runtime technology is named as a binding. Execution design is a later phase and is subordinate to this registry.

## 10. Status

All Phase 5 artifacts are `PROPOSED`. Nothing in this document is APPROVED or CANONICAL, and inclusion in this registry confers no approval on any Workflow.
