# Workflow Matching and Composition

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. Two outcomes, one decision procedure

The planner either **selects** an approved Workflow or **composes** an instance-level Work Plan. It
must always be able to say which, and why the other was not available.

## 2. Candidate search

**Rule MC-1 — search is over approved definitions only.** Candidates come from the approved
Workflow registry at named versions. A retired, superseded, proposed or draft Workflow is not a
candidate, and neither is a previous Work Plan.

**Rule MC-2 — search is recall; selection is check.** Any ranking mechanism — lexical, structural,
semantic — exists to produce a shortlist worth checking. Nothing is selected because it ranked
first.

## 3. Applicability assessment

Each shortlisted candidate is assessed on **both** axes, and they are not merged into one number:

| Axis | Question | Effect |
|---|---|---|
| **Fit** | Does this pattern coordinate the work the request implies? | Ranks candidates |
| **Admissibility** | Does every constraint the candidate carries hold for this request? | **Gates** candidates |

Admissibility is checked against the candidate's own card:

| # | Check | On failure |
|---:|---|---|
| A-1 | Trigger condition holds | Inadmissible |
| A-2 | Every precondition is satisfied or satisfiable within the plan | Inadmissible |
| A-3 | Every participating Role is available and entitled in the resolved scope | Inadmissible |
| A-4 | Every Role slot can bind a Role that already owns the relevant artifact | Inadmissible |
| A-5 | Every `REVIEW_REQUIRED_REFERENCE` resolves to an available Review Profile | Inadmissible |
| A-6 | Every `HUMAN_GATE_REFERENCE` resolves to an applicable Decision Right | Inadmissible |
| A-7 | The candidate's criticality applicability covers the derived band | Inadmissible |
| A-8 | The candidate does not require crossing the resolved scope boundary | Inadmissible |
| A-9 | Activated Skills are Phase 4-permissible for their Roles | Inadmissible |

**Rule MC-3 — inadmissible is not low-scoring.** An inadmissible candidate is removed, not ranked
down. A high fit score against an inadmissible candidate is a reason to record why it was rejected,
never a reason to relax a check.

**Rule MC-4 — a score never overrides a constraint.** This is the rule the whole section exists
for. No similarity score, confidence value, threshold, margin or aggregate may override a Workflow
precondition, a Role constraint, a Review Profile requirement, a Decision Right, or a scope
boundary. Where a score and a constraint disagree, the constraint wins, and the disagreement is
recorded.

## 4. Selection

**Rule MC-5 — MATCH requires exactly one admissible candidate with sufficient fit.** Where several
admissible candidates fit comparably well and the choice changes what is produced, reviewed or
authorised, that is a **material ambiguity**: the planner clarifies rather than picking the top of a
close ranking (`clarification-policy.md` C3).

**Rule MC-6 — a selected Workflow is used as written.** MATCH binds `workflow.<id>` @ version and
changes nothing about it. The planner does not drop a stage, skip a review, retime a gate or
substitute a Role. A pattern that needs modification is not a match — it is a COMPOSE input.

**Rule MC-7 — an approved composition of Workflows is still MATCH.** Where Phase 5 declares a
composition relationship, using it is selection, not composition, and it inherits the child's gates
exactly.

## 5. Composition

**Rule MC-8 — COMPOSE is a last resort with a recorded reason.** The `WorkflowMatchAssessment`
records every candidate considered and why each was rejected. "No Workflow matched" with no list
is not a finding.

**Rule MC-9 — composition assembles approved primitives only.** A `PlanStage` may reference:

- an approved Workflow, wholly, as a sub-pattern;
- an approved Role and its owned activity;
- an approved Skill or pack, Phase 4-permissibly attached to that Role;
- an approved Review Profile;
- an applicable approved Decision Right;
- Phase 8 knowledge and evidence requirements.

It may reference nothing else. There is no "custom stage", no free-form activity, and no inline
capability.

**Rule MC-10 — a composed plan carries at least what an equivalent Workflow would.** Composition is
not a route around rigor. Where a stage performs work that an approved Workflow would gate, the
composed stage carries that gate. Where the derived criticality band would escalate review in a
Workflow, it escalates here.

**Rule MC-11 — composition never lowers a floor.** Not a review requirement, not an independence
class, not a Decision Right, not a sensitivity or residency constraint, not a criticality band.

**Rule MC-12 — dependencies are explicit and acyclic.** Each stage declares entry criteria, exit
criteria and its dependencies. A cycle is `PLAN_VALIDATION_FAILED`.

## 6. The shape of a composed plan

A plan is a `WorkPlan` and an ordered set of `PlanStage`s. Illustrative — the shape, not a template
to instantiate:

```text
work_plan.<id>   scope: <one scope>   criticality: <band>   basis: <Request, WorkIntent>

 S1  evidence intake         role.knowledge_evidence_steward
                             evidence: the record, at its versions
                             exit: every claim the later stages rely on is linked to EVIDENCE

 S2  financial analysis      role.financial_modelling_specialist
                             depends: S1
                             review: review.financial_model  (criticality-escalated)

 S3  legal review            role.legal_regulatory_lead
                             depends: S1
                             owns: the legal position; nothing downstream may restate it

 S4  drafting                <owning substantive Role>
                             depends: S2, S3   carries S3's conclusion verbatim

 S5  independent review      review.<applicable>   author != reviewer

 S6  human decision          decision.<applicable>   ← the gate; no Role participates
```

**Rule MC-13 — the gate stage has no Role participation.** A gate is not work. It is a point at
which a human holding a Right decides, and modelling it as an assignable stage is how a gate
becomes a task somebody closes.

## 7. What a composed plan is not

**Rule MC-14 — it is not a Workflow, at any point, by any route.** It has its own identifier space,
is never written to the Workflow registry, is never referenced as `workflow.<id>`, and no
mechanism promotes it. Repetition does not promote it either
(`workflow-candidate-learning-boundary.md`).

**Rule MC-15 — it is instance-level and bound to one request.** One `Request`, one scope, one point
in time. Re-running the same request produces a **new** plan, and the two are separate records even
if identical.

**Rule MC-16 — it is not approved by being valid.** Passing `governance-preflight.md` means the
plan may be handed to the Orchestrator. It does not mean anyone approved the work, the conclusions,
or the acts the plan contemplates.

## 8. The `WorkflowMatchAssessment` record

| Field | Content |
|---|---|
| `candidates` | Every candidate considered, with its version |
| `fit_scores` | Per candidate; advisory, never binding |
| `admissibility` | Per candidate, per check A-1…A-9, with the failing check named |
| `outcome` | `MATCH` · `COMPOSE` · `AMBIGUOUS_MATCH` · `NO_MATCHING_WORKFLOW` |
| `selected` | `workflow.<id>` @ version, where `MATCH` |
| `rejection_reasons` | Why each rejected candidate was rejected (MC-8) |
| `constraint_overrides_attempted` | **Always empty.** The field exists so that a non-empty one is a validation failure, not a silent event |

**Rule MC-17 — `constraint_overrides_attempted` is a tripwire.** Its only permitted value is empty.
A planner implementation that ever populates it has done the thing MC-4 forbids, and
`governance-preflight.md` check G-9 fails the plan.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no matcher, ranker, embedding, index,
scoring implementation, schema or storage, and binds no provider or runtime technology.
