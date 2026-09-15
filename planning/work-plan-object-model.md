# Work Plan Object Model

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. Seventeen records, and one question asked of each

For every planning record: what it is, whether it carries authority, where its truth lives, how it
is versioned, whether AI may create it, whether a human must approve it, whether it persists, and
whether it can affect execution directly.

**Rule OM-1 — every planning record is non-authoritative.** Without exception, at the foundation
stage, and until an approved rule says otherwise. A planning record informs; it establishes
nothing, satisfies nothing and authorises nothing.

## 2. The records

| # | Record | Purpose | Authority | Source of truth | AI may create | Human approval | Persisted | Affects execution directly |
|---:|---|---|---|---|---|---|---|---|
| 1 | `Request` | The user's words, verbatim | None — it is `SOURCE` | The user | No — it is **captured**, not created | No | Yes | No |
| 2 | `WorkIntent` | The structured reading | None — `AI_SUGGESTION` | The interpreter | **Yes** | No | Yes | No |
| 3 | `ScopeResolution` | The one governed scope, or a failure | None. `entitlement_status` is never `GRANTED` | The approved scope graph | **Yes** | No | Yes | No — intake re-checks |
| 4 | `WorkRequirementSet` | Deliverable, domains, acts, band, flags | None — `AI_SUGGESTION` | Derived; the criticality policy is authoritative for bands | **Yes** | No | Yes | No |
| 5 | `WorkflowMatchAssessment` | Candidates, fit, admissibility, outcome | None | The approved Workflow registry | **Yes** | No | Yes | No |
| 6 | `WorkPlan` | The instance-level composition | None. **Never a Workflow** | Itself, for one request | **Yes** | No — validation is not approval | Yes | No — via the handoff only |
| 7 | `PlanStage` | One stage of a plan | None | Its plan | **Yes** | No | Yes | No |
| 8 | `RoleRequirement` | A Role the work needs, and why | None. Confers nothing on the Role | The approved role registry | **Yes** | No | Yes | No |
| 9 | `SkillRequirement` | A Skill a Role needs activated | None | The approved skill registry and Phase 4 mappings | **Yes** | No | Yes | No |
| 10 | `ReviewRequirement` | A review the work will need | None. **Never satisfied here** | The approved Review Profile registry | **Yes** | No | Yes | No |
| 11 | `DecisionRequirement` | A Right the work will need exercised | None. **Never exercised here** | The approved Decision Right register | **Yes** | No | Yes | No |
| 12 | `EvidenceRequirement` | What must be held before a stage runs | None | Phase 8 | **Yes** | No | Yes | No |
| 13 | `ClarificationRequirement` | A question that must be answered | None | The clarification policy | **Yes** | No — the **answer** comes from a human | Yes | No — it blocks |
| 14 | `PlanningFinding` | Something the planner noticed | None | The planner | **Yes** | No | Yes | No |
| 15 | `PlanValidationResult` | The preflight verdict | None. Passing is not approval | The preflight checks | **Yes** | No | Yes | **Gates** the handoff |
| 16 | `PlannedWorkItemSpec` | A non-runtime description of the work a **validated** plan stage implies | None. **Never a `work_item.<id>`**, never a Task | Its validated plan stage | **Yes** | No | Yes | No — **inert**: no approved contract consumes it |
| 17 | `WorkflowCandidateSuggestion` | A pattern worth a human's attention | None. `PROPOSED`, permanently, until a human acts | The planner's observation | **Yes** | **Yes** — to become anything at all | Yes | **No** |

**Rule OM-2 — "affects execution directly" is `No` for sixteen of seventeen.** Only
`PlanValidationResult` touches execution, and only by **withholding** the handoff. Nothing in this
model starts anything.

## 3. Identity and versioning

**Rule OM-3 — planning identifiers are their own space.** `request.<id>`, `intent.<id>`,
`work_plan.<id>`, `plan_stage.<id>`, `planned_work_item_spec.<id>` and the rest. None is ever
minted in, written to, or resolved against a governed registry's namespace, and `work_plan.<id>` is never rendered as `workflow.<id>`.

**Rule OM-4 — planning records are immutable once complete; revision is a new version.** A plan
that changes after a clarification is `work_plan.<id>@v2` linked to `@v1`. Nothing is edited in
place, because a reviewer must be able to see what the system believed before the user corrected it.

**Rule OM-5 — every governed reference is recorded as ID **and** version, as a value.** The same
rule Phase 11 applies to run references. A plan that referenced "the current version" of a Workflow
would mean something different tomorrow.

**Rule OM-16 — `PlannedWorkItemSpec` is a planning record, and `work_item.<id>` is a runtime one.**

> `PLANNED WORK ITEM SPEC != WORK ITEM`

The Phase 11 `Work Item` is runtime state owned by a run (`orchestration/execution-run-model.md` §3,
row 6), and a **Task / Activity** is what the approved Workflow definition says is to be done,
unchanged by any run (§4 of the same document):

> `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`

Phase 15 writes before any run exists, so it cannot own a Work Item, cannot pre-create one, and
cannot hold one in a pre-runtime state; nor may it define a Task. A `PlannedWorkItemSpec` carries no
run reference, no assignment or execution status, no model, no routing action and no orchestration
semantics (`orchestrator-handoff-contract.md` HO-13), and there is **no transition** from a spec to
either of the other two.

**Rule OM-17 — the spec is inert with respect to execution, and this document claims nothing about
what consumes it.** The current boundary, stated exactly:

| Statement | Status |
|---|---|
| Phase 15 may produce a non-runtime `PlannedWorkItemSpec`, **only after plan validation**, where the architecture permits it (`intent-work-planning-architecture.md` PL-8, step 12) | True today |
| Some currently approved execution-basis contract consumes that record | **False.** None does |
| The record therefore does anything to execution | **No.** It is inert unless and until explicit downstream change control defines consumption semantics |
| MATCH depends on it | **No.** MATCH hands off through the approved Workflow-based intake path, on `workflow.<id>` @ version, and does not reference a spec |
| PO-4 and PO-12 are affected by its existence | **No.** Both remain explicit, fail-closed dependencies |

An earlier version of this rule described the approved Orchestrator handling the record at intake
and creating a runtime identity from it. That described behaviour nobody has approved, and it is
**withdrawn in full** — the table above replaces it, and nothing in this package restores it by
implication. A record that nothing consumes has caused nothing, which is the whole of its current
effect.

## 4. Lifecycle

| State | Means |
|---|---|
| `DRAFT` | Being derived |
| `AWAITING_CLARIFICATION` | One or more `ClarificationRequirement`s are open |
| `VALIDATED` | Preflight passed. **Not approved** |
| `BLOCKED` | A failure mode holds (`failure-and-escalation-model.md`) |
| `HANDED_OFF` | The trigger envelope was produced |
| `SUPERSEDED` | A later version replaced it |
| `ABANDONED` | The request was withdrawn or the plan was never completed |

**Rule OM-6 — `VALIDATED` is the strongest state a plan reaches, and it is not approval.** There is
no `APPROVED` state for a Work Plan, because nobody approves a Work Plan. Humans approve **acts**,
through Decision Rights, during the run.

## 5. Persistence

**Rule OM-7 — planning records persist, and persistence is not authority.** They are kept so that a
reviewer can reconstruct what the system understood and why. They are operational records in the
Phase 10/11 sense: they carry no authority, satisfy no gate, and are not governance evidence.

**Rule OM-8 — a planning record is never evidence for the work it planned.** The plan saying a fact
is needed does not supply it. The plan asserting a scope does not establish entitlement. The plan
naming a Right does not exercise it.

## 6. Knowledge typing inside planning

**Rule OM-9 — planner output is `AI_SUGGESTION` and stays there.** No planning step converts an
inference into a `FACT_CLAIM`, and no downstream use converts it either. Where a plan needs an
assertion, it records an `EvidenceRequirement` — *this must be established before S2 runs* — rather
than asserting it.

**Rule OM-10 — the eight epistemic types are used as Phase 8 defines them.** `SOURCE`, `EVIDENCE`,
`FACT_CLAIM`, `ASSUMPTION`, `CALCULATION`, `INFERENCE`, `AI_SUGGESTION`, `UNKNOWN`. The deprecated
label `FACT` is not used, and there is no transition between types: a supported claim is a **new
linked item** with its own basis.

**Rule OM-11 — a plan may not resolve its own `UNKNOWN`s.** An `UNKNOWN` is closed by evidence or
by a human, during the run or through clarification. It is not closed by the planner deciding the
likely answer, however confident.

## 7. Confidence

Six separate confidences, deliberately not aggregated:

| Confidence | About |
|---|---|
| `semantic` | How well the intent was read |
| `scope` | How sure the scope resolution is |
| `workflow_fit` | How well a candidate matches |
| `role_fit` | How well a Role requirement is derived |
| `risk_detection` | How sure a trigger determination is |
| `authority_resolution` | How sure the Right identification is |

**Rule OM-12 — there is no overall confidence.** Averaging them lets a strong semantic reading hide
a weak scope resolution, which is exactly the trade this architecture refuses.

**Rule OM-13 — confidence is never authority.** A confidence value may not, at any level:

| May not | Because |
|---|---|
| Grant or substitute for a Decision Right | Authority is held by people, not computed |
| Waive or satisfy a review | Reviews are satisfied by reviewers |
| Change a knowledge state | Types come from basis, not from certainty |
| Make a candidate Workflow approved | Approval is a governed act |
| Permit crossing a scope boundary | CS-4 |
| Substitute for missing evidence | An `EvidenceRequirement` is unmet until it is met |
| Override a constraint | MC-4 |

**Rule OM-14 — low confidence may trigger work; high confidence never grants permission.** Low
`scope` confidence may trigger clarification; low `semantic` confidence may trigger a restatement
back to the user; low `risk_detection` confidence routes conservatively (WC-6). High confidence of
any kind changes **nothing** about what is permitted. The asymmetry is deliberate and is the single
most important property of this model.

**Rule OM-15 — confidence is never displayed as authority.** A percentage next to a plan is a
statement about the planner, and the UX contract forbids presenting it as a statement about
whether the work is safe (`user-experience-contract.md` UX-7).

## 8. Non-Runtime Statement

This document is declarative architecture. It specifies no schema, database, API, serialisation
format, identifier generator, scoring implementation or storage mechanism, and binds no provider or
runtime technology.
