# Observability, Audit and Provenance

Status: `PROPOSED` — Phase 16 candidate. Approves nothing, registers nothing.

Requirement 10 of the Phase 16 scope. Two questions: which planning events are operational and
which are governed, and how provenance survives the whole path from a sentence a person typed
to a run the Orchestrator created.

## 1. Operational versus governed

The distinction is not about importance. It is about whether losing the record changes what is
true about authority.

| | Operational event | Governed record |
|---|---|---|
| Purpose | Observability, debugging, cost, latency, planner quality | Establishing what was decided, by whom, under what authority |
| If lost | The system is harder to operate | The governance record is incomplete; authority cannot be reconstructed |
| Written by | The planner, freely | Only the approved Phase 14 command that owns it |
| Mutable | Yes, may be sampled, truncated, aggregated or dropped | No — append-only |

### Phase 16 planning events, classified

| Event | Class | Note |
|---|---|---|
| `planner.intent_parsed` | Operational | P1 output; a planner-quality signal |
| `planner.scope_resolved` | Operational | The **resolved scope** it names is, however, material |
| `planner.classification_assigned` | Operational | Criticality is material; the event about it is not the record of it |
| `planner.mode_selected` (MATCH/COMPOSE) | Operational | |
| `planner.clarification_raised` / `.resolved` | Operational | The blocking *state* is carried by the planner output, not by the event |
| `planner.work_plan_drafted` | Operational | |
| `planner.preflight_run` | Operational | Includes each gate's outcome; useful and not authoritative |
| **`activation.basis_issued`** | **Governed** | The basis itself is the governed record |
| **`activation.basis_stale`** / **`.superseded`** | **Governed** | A status transition on a governed record |
| **`activation.trigger_accepted`** | **Governed** | It mints the `run_lineage` that makes duplicate execution detectable |
| `activation.trigger_rejected` | Operational | Nothing was written, so nothing must be remembered for authority |
| `activation.workflow_candidate_proposed` | Operational | A `PROPOSED` candidate is an observation, not a status grant |

Three governed records in the whole phase — basis issue, basis status transition, trigger
acceptance — and none of them is an approval, a decision, a review outcome or a run.

## 2. What Phase 16 must never emit

| # | Never |
|---:|---|
| OB-1 | An event that reads as an approval, an authorisation or a sign-off |
| OB-2 | An event that a downstream consumer could treat as satisfying a Review Requirement |
| OB-3 | An event that records a Decision Right as exercised |
| OB-4 | A "basis approved" event. A basis is *issued*, never approved; `is_approval` is a declared `false` field on the object |
| OB-5 | An evidence claim. Planning observes; it does not produce evidence for a professional conclusion |
| OB-6 | A record that overwrites a prior governed record rather than appending a new one |

OB-5 restates the approved separation: **evidence, audit, execution events and authority are
four different things.** Planner telemetry is none of them. A preflight that found a Review
Requirement is not evidence that the review happened; it is the reason the requirement is in the
basis, unsatisfied, waiting for the party that actually holds it.

## 3. The provenance chain

Every governed object in the path carries the reference of the one before it, so the chain is
reconstructable in both directions from any point:

```text
request.<id>
  └─ intent.<id>                         provenance: request_id
      └─ work_plan.<id>@<v>              provenance: intent_id, request_id, scope_id
          │                              (MATCH also: workflow.<id>@<version>)
          └─ execution_basis.<request>.<n>
              │   binds: request_id, scope_id, work_plan ref + version,
              │          planning_digest, implementation_spec_version,
              │          role/skill bindings, review requirements,
              │          decision requirements, criticality, evidence requirements
              │   links: supersedes → execution_basis.<request>.<n-1>
              └─ trigger (CreateWorkflowRun)
                  │   carries: basis ref, idempotency_key, planned work item specs
                  └─ run_lineage.<key>
                      └─ workflow_run.<id>      created by the ORCHESTRATOR, not here
```

Four properties of that chain, each testable:

| # | Property |
|---:|---|
| PR-1 | Every link is a reference, never a copy. No stage re-states what an earlier stage owns |
| PR-2 | The basis is bound to `planning_digest`, so "which plan was this basis for" has an exact answer, not a narrative one |
| PR-3 | `implementation_spec_version` is on the basis, so a later spec change is detectable rather than assumed compatible |
| PR-4 | The chain crosses into the Orchestrator exactly once, at the trigger, and the crossing is a command submission — not a write |

## 4. What provenance does not buy

Provenance says what happened and in what order. It does not make any of it authorised.

An `EXECUTABLE` basis with a complete provenance chain, a resolved scope, bound roles and a
correctly computed digest still carries `ReviewRequirement(satisfied=False)` and
`DecisionRequirement(exercised=False)` wherever the approved architecture requires them. The
chain records that those requirements were identified. Nothing in this package can record them
as met, and `ExecutionBasis.satisfy_review()` and `.exercise()` raise rather than let a caller
try.
