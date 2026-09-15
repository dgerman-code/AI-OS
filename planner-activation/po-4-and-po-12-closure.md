# PO-4 and PO-12 — What Phase 16 Closes, and What It Does Not

Status: `PROPOSED` — Phase 16 candidate. Approves nothing, registers nothing.

Phase 15 left two obligations open on purpose, because closing either one meant changing
something downstream that Phase 15 held no authority over. This document states exactly what
Phase 16 proposes in each case, what that proposal depends on, and what is still open
afterwards. It is written to be checkable rather than reassuring: a closure that depends on an
approval nobody has given is named as a dependency, not reported as done.

---

## Part 1 — PO-4

### 1.1 What PO-4 actually said

A composed Work Plan is not a Workflow definition. The approved Phase 11 intake check 1
resolves a Workflow definition. So on the COMPOSE path there was nothing for check 1 to
resolve, and the COMPOSE path was specified and **not executable**.

Note the shape of the problem. It was never "COMPOSE is unsafe". It was "COMPOSE has no
governed object to present at the door".

### 1.2 What Phase 16 proposes

The **Execution Basis** — `execution-basis-contract.md` — is that object.

| Property | Statement |
|---|---|
| What it authorises | Entry to intake. Nothing else |
| What it binds | Request, scope + ancestry, Work Plan ref and version, approved Workflow ref and version where MATCH, `planning_digest`, `implementation_spec_version`, role and skill bindings, review requirements, decision requirements, criticality, evidence requirements |
| What it declares | `is_approval = false`, `is_authority = false` — as fields, so no consumer can read `EXECUTABLE` as either |
| Lifecycle | `DRAFT` → `VALIDATED` → `EXECUTABLE`, or `BLOCKED`; `STALE` on material change; `SUPERSEDED` on reissue |
| What it refuses | `exercise()` and `satisfy_review()` raise. They are not unimplemented; they are refusals |

On the COMPOSE path, intake check 1 then resolves the `work_plan.<id>@<v>` named by an
`EXECUTABLE` basis, in place of a `workflow.<id>@<version>`. On the MATCH path nothing changes:
check 1 resolves the approved Workflow exactly as before, and the basis merely accompanies it.

### 1.3 What that closure depends on — stated plainly

**Adopting the Execution Basis as an admissible answer to approved intake check 1 on the
COMPOSE path is a change to how an approved contract is satisfied.** Phase 16 cannot make that
change; it can only propose it. Approving this package is what would settle it.

Until that approval:

| # | State |
|---:|---|
| D-1 | The Execution Basis is `PROPOSED`. Every basis this package's implementation issues is a proposal-grade record |
| D-2 | `EXECUTABLE` means *intake may accept this*, and never *this is approved to run* |
| D-3 | The Orchestrator still performs all seven intake checks independently and may refuse. A refusal after an `EXECUTABLE` basis is the design working |
| D-4 | If Phase 16 review rejects the basis as an answer to check 1, PO-4 reverts to open and COMPOSE reverts to non-executable. Nothing in this package has been relied upon in the meantime |

### 1.4 What remains open after PO-4 closure

| # | Open item |
|---|---|
| **PO-16-A** | In-flight runs. Phase 16 guarantees no *new* execution starts from stale planning. A run the Orchestrator already created, whose basis later goes `STALE`, is the Orchestrator's to handle; no approved contract says what it does |
| **PO-16-B** | The COMPOSE-path check-1 resolution above is a proposal against an approved contract, and needs the Phase 11 owner's acceptance, not only Phase 16 approval |
| **PO-16-C** | `sensitivity` and `residency` default to `UNASSESSED` in the reference handoff. Intake check 4 is answerable but the *answer quality* depends on an upstream classification Phase 16 does not perform |

---

## Part 2 — PO-12

### 2.1 What PO-12 actually said

No approved contract defined what a downstream consumer does with a planning record, or how an
instance-level Work Plan differs from a reusable Workflow definition under change control.

### 2.2 What Phase 16 proposes

`change-control-contract.md` and `workflow-resolution-contract.md` together, on three axes:

**Axis 1 — the two objects never merge.**

| | Instance Work Plan | Approved Workflow |
|---|---|---|
| Identity | `work_plan.<id>@<v>` | `workflow.<id>@<version>` |
| Created by | Planning, per request | The approved registry, before planning ran |
| Reusable | No | Yes |
| Changed by | A replan | Governed change to an approved definition, outside this phase |

`WorkPlan.__post_init__` raises if a plan id would be rendered in the `workflow.` space. A Work
Plan never acquires Workflow identity — by construction, not by convention.

**Axis 2 — material versus non-material change.**

Material fields are enumerated and hashed. `PlannerOutput.material_digest()` is a sha256 over
the canonicalised material fields; a presentation-only edit yields the same digest, and
therefore no new governed plan version and no new basis (acceptance scenario 8). A material
change yields a different digest, which makes every live basis for that request `STALE` and
forces re-preflight (acceptance scenario 7).

The digest is the mechanism, not a description of one. Staleness is not a judgement call.

**Axis 3 — promotion stays a proposal.**

A repeated COMPOSE shape may emit a workflow candidate with `status = "PROPOSED"`,
`is_approved = false`, `is_matchable = false`. The reference store has **no method that
registers a Workflow and none that sets a candidate to APPROVED** — again by construction.
Promotion is a separately governed act this phase does not perform and cannot perform.

### 2.3 What that closure depends on

| # | Dependency |
|---:|---|
| D-5 | The material-field list is a Phase 16 proposal. If review judges a field mis-classified, the digest changes meaning and the staleness behaviour changes with it |
| D-6 | Promotion governance — who may approve a candidate, under what Review Profile — is **not** specified here and is not Phase 16's to specify |

### 2.4 What remains open after PO-12 closure

| # | Open item |
|---|---|
| **PO-16-D** | The promotion pathway itself. Phase 16 guarantees a candidate stays `PROPOSED`; it does not define how one would ever stop being `PROPOSED` |
| **PO-16-E** | Change control for an approved Workflow definition remains wholly outside this phase, as it must |

---

## Part 3 — Honest summary

| Obligation | Phase 16 status |
|---|---|
| PO-4 | **Closure proposed**, mechanism implemented and tested, contingent on D-1…D-4 |
| PO-12 | **Closure proposed**, mechanism implemented and tested, contingent on D-5…D-6 |

Neither is closed by this package alone. Both are closed by this package *plus* the approval
this package is being submitted for. Five new open items — PO-16-A through PO-16-E — are
created by the proposal and are recorded here rather than left to be discovered.
