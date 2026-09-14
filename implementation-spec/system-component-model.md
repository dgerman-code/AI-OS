# System Component Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

## 1. Why components are drawn this way

The approved architecture is a set of separations. A component boundary that cuts across one of
those separations makes the separation unenforceable no matter how carefully the code inside is
written: a single service that both selects a model and sequences a workflow has merged
`ROUTER != ORCHESTRATOR` regardless of its internal class structure.

So the component boundaries below are drawn **on the separations**, not on convenience.

## 2. Components

| # | Component | Authoritative for | Never does |
|---:|---|---|---|
| C1 | **Definition Registry Service** | Serving approved definitions — Role Cards, Skill Cards, Workflow Definitions, Review Profiles, Decision Right Cards, Orchestrator Policies, Routing Policies, Model/Provider/Deployment Profiles — read from the Git-backed source of truth at a named version | Mutate a definition; approve one; decide which is "current" without a version |
| C2 | **Approval State Registry** | The machine-readable approval state of every governed baseline, artifact and registry version (`approval-state-registry.md`) | Create approval; infer it; approve by absence |
| C3 | **Scope Service** | Scope node identity, canonical path, ancestry queries, applicability resolution, sensitivity and residency binding (`scope-and-context-model.md`) | Grant access; widen a scope; infer an ancestor relationship from name similarity |
| C4 | **Knowledge & Canonical Service** | Knowledge items on four axes, conflict records, provenance, canonical records, promotion **preconditions** (`knowledge-and-canonical-model.md`) | Promote anything without a mapped Decision Right; convert an `AI_SUGGESTION` to another epistemic type; change an origin |
| C5 | **Review Service** | Review Requests, Review Instances, findings, independence-class evaluation, reviewer-eligibility evaluation (`decision-review-authority-model.md` §5) | Approve; satisfy a decision gate; relabel a review it did not perform |
| C6 | **Decision Authority Service** | Decision Rights resolution, holder eligibility, cardinality, `DECISION_RIGHT_SEPARATION`, Decision Record capture (`decision-review-authority-model.md`) | Decide; impersonate a holder; create a Right; widen a declared subject |
| C7 | **Router Service** | Candidate universe binding, eligibility filtering, preference ranking, Routing Decision production with the six-part reproducibility set (`model-router-runtime-contract.md`) | Sequence work; decide whether work is done; relax an eligibility constraint; create authority |
| C8 | **Model Invocation Gateway** | Executing a Model Invocation against the deployment a recorded Routing Decision selected, behind a provider-neutral adapter contract | Choose a model; retry an authority-bearing act; emit anything but `AI_GENERATED` / `AI_SUGGESTION` output |
| C9 | **Orchestrator Service** | Workflow Run and Work Item lifecycle, state transitions, gate detection, dispatch, waiting, retry classification, rework loops, escalation, execution events (`orchestrator-runtime-contract.md`) | Approve, review, canonicalise, accept risk, sign, create a Right, substitute for a human, infer competence, cross a scope |
| C10 | **Governed Record Store (PostgreSQL)** | Operational governance records, their lifecycle, lineage and queryable state, with durable uniqueness and optimistic concurrency (`persistence-and-transaction-model.md`) | Be the architecture's source; grant authority by a row or a policy |
| C11 | **Artifact & Object Store** | Bytes of files and large artifacts, immutable object versions, the staged commit protocol | Be the artifact registry; interpret content; adopt an orphan |
| C12 | **Audit & Provenance Service** | Audit events, provenance records, retention and legal holds (`audit-provenance-observability.md`) | Record authority; substitute for a Decision Record |
| C13 | **Observability Plane** | Operational runtime events, metrics, traces, correlation and causation identities | Produce governance evidence of any kind, ever |
| C14 | **Identity & Access Service** | Human identity references, service identities, credential lifecycle, authorization enforcement (`security-identity-access.md`) | Be authority; let an administrator substitute for a Decision Right |
| C15 | **Command/Query API** | The command and query surface, precondition validation, idempotency keys, error contracts (`api-command-contracts.md`) | Infer authority from an authenticated caller |
| C16 | **Outbox & Reconciliation Worker** | Draining staged external effects, recording external-effect uncertainty, driving reconciliation (`failure-recovery-race-model.md` §6) | Compensate on its own authority; retry a non-retryable governed act |

`C13` is deliberately at the bottom of no hierarchy and the top of none. It is the one component
whose output is **defined as having no governance meaning**, and it is drawn as a separate
component precisely so that nothing can accidentally read from it on a governed path.

## 3. Forbidden responsibility crossings

Each row is a build-time and review-time rule. A pull request that creates one of these is
rejected as an architecture violation, not debated as a design trade-off.

| # | Forbidden crossing | Invariant it would break |
|---:|---|---|
| F1 | C9 selects a model, a deployment or a provider | `ROUTER != ORCHESTRATOR` |
| F2 | C7 sequences work, activates a stage, or decides completion | `ROUTER != ORCHESTRATOR` |
| F3 | C9 writes a Review Instance, Decision Record or Canonical Record | Orchestrator is not reviewer, authority or promoter |
| F4 | C5 sets a gate to satisfied for a `DECISION` gate | `review != approval` |
| F5 | C6 satisfies a `REVIEW` gate | `DECISION RECORD != REVIEW INSTANCE` |
| F6 | C8 output is stored with any epistemic type other than `AI_SUGGESTION`, or any origin other than `AI_GENERATED` | `MODEL != KNOWLEDGE`, `MODEL != CANONICAL` |
| F7 | C13 output is read by C5, C6, C4, C9 or C15 on any path that satisfies a gate, evidences a decision, or promotes knowledge | `RUNTIME EVENT != AUDIT EVENT` |
| F8 | C12 output is treated as authority for the change it records | `AUDIT EVENT != DECISION RECORD` |
| F9 | C14 grants, widens or substitutes for a Decision Right; an admin, database owner, service role or RLS bypass stands in for a holder | `CREDENTIAL != HUMAN AUTHORITY` |
| F10 | C10 or C11 assigns, infers or overwrites a logical object identity, a version identity or an audit record | Phase 10 §2.1 seven-facet rule |
| F11 | C11 bytes become readable as an artifact without a committed C10 record | Orphan adoption; `FILE OBJECT != ARTIFACT` |
| F12 | C3 permits a scope crossing, or resolves an ancestor by string similarity rather than by path | Scope isolation |
| F13 | C4 promotes to `CANONICAL` without a mapped Decision Right and a recorded Decision Record | Canonical promotion authority |
| F14 | C1 serves a definition without a version, or serves an unapproved definition as approved | Registry versioning; C2 is the approval oracle |
| F15 | Any component treats a timeout, an expiry, a retry exhaustion, a confidence score, a ranking or an urgency flag as an outcome other than the approved one | Authority inference |

## 4. Component interaction on the governed path

```
   C15 Command/Query API
        │  (authenticated caller; carries NO authority)
        ▼
   C9 Orchestrator ──reads──► C1 Definitions @version ──asks──► C2 Approval State
        │                     C3 Scope (bind exactly one)
        │
        ├─ routing ──────────► C7 Router ──produces──► Routing Decision (6-part set)
        │                                                   │
        │                                                   ▼
        ├─ invocation ───────► C8 Gateway ──produces──► Model Result (AI_SUGGESTION)
        │
        ├─ review gate ──────► C5 Review Service ─────► Review Instance
        │
        ├─ decision gate ────► C6 Decision Authority ─► Decision Record  ◄── human only
        │
        └─ every governed write ─► C10 Store  ──►  C12 Audit  (separate record, separate write)
                                       │
                                       └── C11 Object Store via the staged commit protocol

   C13 Observability observes all of the above and is read by none of it.
```

The single most important property of this diagram: **every arrow that produces governance
meaning terminates in a typed governed record in C10, and no arrow terminates in C13.**

## 5. Deployment-neutrality of the component model

A component is a **responsibility boundary**, not a process, container or repository. A
conforming implementation may co-locate C1–C3 in one process, or split C9 into several, provided
no forbidden crossing in §3 becomes reachable. `deployment-topology-and-environments.md` states
the logical environment separation; it names no vendor, no orchestrator platform and no runtime.

## 6. Divergences from the Phase 12 reference implementation

Recorded rather than silently resolved. In each case the approved architecture is followed.

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | One `Orchestrator` object holds adapters for router, reviewers, decisions and model | C7, C5, C6 and C8 are separate components behind contracts | The MVP's single object is a demonstration; co-location at production scale makes F1–F5 reachable |
| D2 | `ExecutionEventLog` is documented in code as "Governance evidence" | An execution event is **coordination history and never governance evidence** | Phase 11 `orchestration/execution-audit-and-provenance.md` §1. Phase 13 finding M-2 |
| D3 | No audit-event record family distinct from the execution event | C12 is a separate component with its own record family | Phase 10 `storage/audit-provenance-model.md` §1 |
| D4 | No approval-state component | C2 exists | Phase 13 finding M-6 |
