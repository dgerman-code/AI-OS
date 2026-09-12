# Orchestrator Architecture

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`
Phase 10 human-approved baseline: `eb789263b4dcc7c4a966a19359522173c57ac8ec`
Phase 10 approved architecture baseline: `b184b074c1de5416fcfc56036ee033f6e52fed46`

Phase 11 answers one bounded question: **how does AI-OS coordinate an execution from trigger to completion without any approved boundary moving.** It adds no governance semantics. Where it appears to, that is a defect.

## 1. What the orchestrator is

A **coordination control plane**. It reads approved definitions and current governed state, instantiates bounded execution records, activates already-defined stages, requests governed acts from the phases that own them, waits, records, and escalates.

It is the one component in AI-OS positioned to see everything at once, which is exactly why it is given no authority over anything. A coordinator that could approve would be the shortest path around every gate in the architecture.

| It may | It may never |
|---|---|
| Read approved definitions and governed state | Invent authority |
| Instantiate execution records | Infer approval from completion |
| Activate defined workflow stages | Infer competence from model output |
| Request role-capable work | Turn a model result into a reviewed, approved or canonical result |
| Submit a routing request | Choose a provider endpoint where a Routing Policy applies |
| Request reviews and Decision Right exercise | Self-satisfy a review or self-exercise a Right |
| Pause while waiting on humans or prerequisites | Treat a timeout as approval |
| Carry open items forward **where upstream semantics permit** | Silently resolve findings, conflicts or `UNKNOWN` states |
| Record execution state and correlation metadata | Rewrite governed history |
| Retry **where retry is explicitly safe** | Replay an authority-bearing act |
| Escalate where continuation is not allowed | Lower sensitivity, residency or materiality constraints |
| Narrow what a stage sees | **Never** cross a scope boundary, and never widen where material may go |
| — | **Never** use operational logs as governance evidence |

## 2. The identity boundary

> **`ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE != ROUTER != ORCHESTRATOR != WORKFLOW != WORKFLOW RUN != TASK != HANDOFF != REVIEW PROFILE != REVIEW INSTANCE != DECISION RIGHT != DECISION RECORD != KNOWLEDGE != CANONICAL RECORD != ARTIFACT != STORAGE RECORD != RUNTIME EVENT != CREDENTIAL != HUMAN AUTHORITY`**

Twenty-one objects. The collapses Phase 11 is most exposed to, each denied with its consequence:

| Denial | What collapsing it would destroy |
|---|---|
| `ROLE != AGENT INSTANCE` | Roles would become persistent personas with memory and standing, and competence would attach to a process instead of to a profile |
| `ROUTER != ORCHESTRATOR` | Sequencing and eligibility would merge; a coordinator could pick a model to make a stage pass |
| `WORKFLOW != WORKFLOW RUN` | A definition would be mutable by running it, and two runs would not be comparable |
| `TASK != WORK ITEM` | The unit of definition and the unit of assignment would merge, and reassignment would rewrite the workflow |
| `REVIEW PROFILE != REVIEW INSTANCE` | Requesting a review would look like satisfying one |
| `DECISION RIGHT != DECISION RECORD` | The authority and its exercise would merge; holding a Right would be exercising it |
| `RUNTIME EVENT != AUDIT EVENT` | Operational logs would become governance evidence, which is **not** what they are |
| `ORCHESTRATOR != HUMAN AUTHORITY` | The control plane would become the signatory, which is the failure this entire phase is arranged to prevent |
| `CREDENTIAL != HUMAN AUTHORITY` | Possession of access would become permission to decide — denied in Phase 10 for storage and again here for execution |

## 3. What Phase 11 inherits and does not touch

| Inherited | From | Treatment |
|---|---|---|
| Context hierarchy and scope graph | Phase 2 | Every execution binds to exactly one scope. **No boundary is redefined and none is crossed without an approved mechanism** |
| Criticality bands and Enhanced Decision-Grade Project Mode | Phase 3 | Used, not redefined. Criticality may **raise** rigour and never lowers an approved requirement |
| Roles and Skills | Phases 3–4 | Activated, never instantiated as agents. **No Role Card or Skill Card is modified; no seniority variants are created** |
| Workflow stage semantics — completion, block, rework, escalation, cancellation | Phase 5 | Preserved exactly. Phase 11 schedules them; it does not redefine what they mean |
| Handoff and Review semantics, reviewer independence | Phase 6 | Requested, never satisfied by the requester. **No independence class is added or weakened** |
| Decision Rights and append-only decision history | Phase 7 | Requested. **No Right is carded, granted, substituted or inferred**, and absence blocks |
| Sensitivity, freshness, origin, `AI_SUGGESTION`, terminal `RETRACTED`, scope transfer | Phase 8 | Carried unchanged through every stage, handoff, routing request and retry |
| Model/Provider/Deployment identity, Routing Policies, Routing Decisions, the six-part reproducibility set | Phase 9 | Referenced by recorded value. **Routing is requested, never performed** |
| Source-of-truth matrix, storage identity, audit model, failure outcomes | Phase 10 | Used as the persistence layer. Execution records are `DB`-authoritative operational records; **nothing governed is relocated** |

## 4. Inventory

| Vocabulary | Members | Owner document |
|---|---|---|
| Identity chain objects | **21** | This document §2 |
| Runtime identity kinds | **15** | `orchestration/execution-run-model.md` §2 |
| Run phases (non-terminal) | **10** | `orchestration/state-machine-and-transitions.md` §2 |
| Terminal outcomes | **6** | `orchestration/state-machine-and-transitions.md` §3 |
| Wait reasons | **5** | `orchestration/state-machine-and-transitions.md` §4 |
| Governance postures | **4** | `orchestration/state-machine-and-transitions.md` §5 |
| Dependency kinds | **8** | `orchestration/scheduling-and-dependency-model.md` §2 |
| Dispatch kinds | **6** | `orchestration/scheduling-and-dependency-model.md` §1 |
| Assignment envelope fields | **12** | `orchestration/execution-run-model.md` §5 |
| Gate kinds | **4** | `orchestration/human-gate-and-decision-invocation.md` §1 |
| Gate outcomes | **7** | `orchestration/human-gate-and-decision-invocation.md` §3 |
| Retry classes | **7** | `orchestration/retry-replay-idempotency.md` §1 |
| Race cases | **10** | `orchestration/concurrency-and-race-governance.md` §2 |
| Race outcomes | **5** | `orchestration/concurrency-and-race-governance.md` §1 |
| Failure distinctions | **7** | `orchestration/failure-escalation-recovery.md` §1 |
| Stop conditions | **12** | `orchestration/failure-escalation-recovery.md` §4 |
| Intervention acts | **6** | `orchestration/manual-intervention-boundary.md` §2 |
| Execution event fields | **13** | `orchestration/execution-audit-and-provenance.md` §2 |
| History kinds | **8** | `orchestration/execution-audit-and-provenance.md` §1 |
| Adapter boundaries | **5** | `orchestration/provider-runtime-independence.md` §2 |
| Common orchestrator constraints | **30** | `orchestration/_standards/common-orchestrator-governance-constraints.md` |
| Templates | **3** | `orchestration/_templates/` |
| Exemplars | **6** | `orchestration/exemplars/` |

## 5. Trigger intake and validation

An execution begins with a **Trigger**, and a trigger is a request, not a start. Intake validates, in this order, before any work is scheduled:

| # | Check | Failure outcome |
|---:|---|---|
| 1 | The Workflow definition resolves at a named version in the approved baseline | **BLOCK** |
| 2 | The Orchestrator Policy resolves at a named version | **BLOCK** |
| 3 | Exactly one governed scope is named and the trigger's originator may act in it | **BLOCK** |
| 4 | Sensitivity labels, handling controls and residency constraints are present or explicitly assessed | **BLOCK** — unassessed is restricted, never permissive |
| 5 | Criticality band resolves | **BLOCK** |
| 6 | The trigger is not a duplicate of a live run under the same idempotency key | **IGNORE_AS_STALE**, recorded |
| 7 | Every declared prerequisite artifact, evidence or decision reference resolves, or is declared `FUTURE_GOVERNANCE_REFERENCE` and therefore non-executable | **BLOCK** on a dangling reference |

A trigger failing any check produces a **recorded refusal**, not a run that fails later. The distinction matters because a run that started and then blocked has already consumed assignments, routing requests and possibly external effects.

## 6. Human control

Three things belong to humans and to no coordination process:

1. **Exercising a Decision Right** — by an eligible human, recorded as a Decision Record under Phase 7.
2. **Satisfying a review** — by a reviewer meeting the Profile's independence class under Phase 6.
3. **Intervening in an execution** — resume, pause, cancel, reassign, supply evidence, request rework, each attributable and bounded (`orchestration/manual-intervention-boundary.md`).

Four things no orchestration act reaches: **the truth of produced content** · **a review's outcome** · **a canonical promotion** · **an authority Phase 7 did not card**.

## 7. Reproducibility

A historical execution must reconstruct what it used. Every governed reference in an execution record is the **stable logical ID and version, written as a recorded value** — the Phase 10 §7 rule, applied to execution. A Routing Decision reference carries Phase 9's six-part reproducibility set by reference to the decision that holds it, never by re-resolving the profile as it stands today.

**Determinism is bounded and stated.** Given the same definitions, versions, inputs and governed state, the orchestrator's own decisions — which stage is next, which dependency is unmet, which gate applies, which retry class a failure falls into — are deterministic. What is **not** deterministic, and is not claimed to be, is the content a model produces, the outcome a human reaches, or the timing of an external system.

## 8. Not built in Phase 11

| Not built | Why |
|---|---|
| Any live orchestrator, queue, worker, scheduler, state-machine service or event bus | Architecture phase |
| Any SQL, migration, table, bucket or policy | Phase 10 defines the persistence governance; deployment follows approval |
| Any provider SDK, model API call or prompt-as-runtime | Phase 9 defines routing semantics; execution is not implemented |
| Agents, personas or standing instances | `ROLE != AGENT INSTANCE` |
| RAG, embeddings or a retrieval system | A consumer of this architecture, not part of it |
| Secrets, credentials, IAM or service accounts | Phase 10, and none are created there either |
| A production retry engine or auto-failover | The **classification** of what may be retried is defined; the mechanism is not |
| Billing, telemetry backends, CI/CD, UI | Out of scope by construction |
| Real Decision Right assignments, or real Model/Provider/Deployment profiles | Phases 7 and 9 did not create them and Phase 11 does not |
