# Open Items

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

> Recorded, not resolved. Each is something Phase 15 deliberately does not settle, with the reason
> it is not settleable here.

| # | Item | Why it is open | Who settles it |
|---:|---|---|---|
| **PO-1** | **No approved Role owns communication strategy for contested interactions.** A candidate exists on a separate proposal branch and is not approved | Phase 15 may not create a Role (N-1). Until one is approved, plans needing that conclusion are constrained or blocked (RS-9) | Role Registry change control |
| **PO-2** | **The Work Plan is not in any approved storage domain.** Phase 10 defines ten data domains; none of them is "planning" | Adding a domain is a Phase 10 change, not a Phase 15 one | Phase 10 change control |
| **PO-3** | **The Orchestrator Policy a composed plan assumes is unspecified.** `workflow_ref` carries its own policy binding; a `work_plan_ref` does not obviously inherit one | Phase 11 owns policy binding; inventing a default here would be inventing coordination behaviour | Phase 11 governance |
| **PO-4** | **Whether a composed Work Plan is an admissible `execution_basis` at all.** The approved intake check 1 says "the Workflow definition resolves at a named version". A Work Plan is not a Workflow definition | This is the load-bearing compatibility question of the whole phase, and it is a Phase 11 question. §2 below | Phase 11 governance |
| **PO-5** | **Criticality bands are stated as "typically"** in the approved policy. Deterministic band derivation needs a rule the policy does not give | Re-thresholding an approved policy is not a Phase 15 act (WC-1) | Phase 3 policy governance |
| **PO-6** | **No approved mechanism records planner provenance.** `planning_provenance` crosses the handoff boundary with nowhere defined to live | Follows PO-2 | Phase 10 change control |
| **PO-7** | **Review Profiles and Decision Rights are candidate universes, largely uncarded.** Preflight checks G-8 and G-10 resolve against registers that are mostly proposals | Carding is Phase 6 and Phase 7 work | Phase 6 / Phase 7 change control |
| **PO-8** | **Confidence has no defined production method.** The model says what confidence may never do; it does not say how it is computed | Deliberate. Specifying a computation would specify an inference runtime, which §13 of the commissioning prompt excludes | A later phase, or never |
| **PO-9** | **Repeated-pattern detection has no defined threshold.** `workflow-candidate-learning-boundary.md` says what a suggestion may not do, not when one is emitted | Deliberate, and low-risk: a suggestion is inert (WL-3), so the threshold cannot cause harm | A later phase |
| **PO-10** | **The clarification-answer channel is unspecified.** CL-13 says an answer is a new linked `Request`; how it is collected is a product question | Out of scope: no UI is specified | Product design |
| **PO-11** | **The architecture document's final home.** It sits in `planning/` because adding a file under `architecture/` degrades the approved Phase 12 containment check (self-check §2a) | Whether system-level Phase 15 material belongs in `architecture/` is a repository-convention question, and moving it there requires the Phase 12 check to be amended first | Phase 12 / repository governance |

## 2. PO-4 in full, because it decides whether this phase is buildable

The approved Orchestrator intake check 1 reads: *"The Workflow definition resolves at a named
version in the approved baseline — failure outcome BLOCK."*

A composed Work Plan is, by construction, **not** a Workflow definition. Three readings are
available, and Phase 15 takes none of them:

| Reading | Consequence |
|---|---|
| **A** — intake check 1 is satisfied only by a `workflow.<id>` | The COMPOSE path cannot reach the Orchestrator at all. Phase 15's MATCH half works; its COMPOSE half is architecture with no execution route |
| **B** — intake check 1 is satisfied by any resolvable execution basis, and a validated Work Plan is one | Requires an approved Phase 11 change stating so, with its own conditions |
| **C** — a composed plan must first be registered as a Workflow | **Prohibited.** That is exactly what `workflow-candidate-learning-boundary.md` forbids, and taking this reading would make the system self-register patterns |

**Reading C is excluded here**; it is the failure mode this phase is built to prevent. Between A and
B, Phase 15 does not choose, because choosing B would be amending an approved Phase 11 check from a
proposal branch — and `planning/intent-work-planning-architecture.md` PL-7 says the Orchestrator
re-checks everything precisely so that a planner cannot satisfy an intake check by assertion.

**Until PO-4 is settled, the honest position is:** the MATCH path is complete and compatible; the
COMPOSE path is specified and **not yet executable**. `orchestrator-handoff-contract.md` field 1
carries `execution_basis` so that the distinction is explicit in the envelope rather than discovered
at intake.

## 3. What is deliberately not open

Stated so that a reviewer does not read silence as uncertainty:

| Not open | Because |
|---|---|
| Whether a Work Plan may become a Workflow | It may not. WL-1 |
| Whether confidence may grant authority | It may not. OM-13 |
| Whether the planner may select a model | It may not. N-10, HO-4 |
| Whether a missing Decision Right may be inferred | It may not. GP-5 |
| Whether scope may be crossed on high confidence | It may not. CS-4 |
| Whether the planner may act as an Orchestrator | It may not. PL-1 |

## 4. Non-Runtime Statement

This document is declarative architecture. It specifies no implementation and binds no provider or
runtime technology.
