# Phase 16 — Planner Activation & Execution-Basis Integration

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1
Integration baseline: the merge of the approved Phase 14 line and the approved Phase 15 line
Phase 14 approval: `35a4c01be450e07b13ed52ca78e9834752261a45` (baseline `ba9e3feebc25418b8f858c62e63bb0ec466b9a21`)
Phase 15 approval: `72870de11857140c056bfe1e482ca6cd82940d74` (baseline `2301b66c39a218e966587731eee2f7472501f39c`)

> **Nothing in this package is approved.** It creates no Decision Right, registers no Role,
> Skill, Workflow or Review Profile, exercises no authority, satisfies no review, and claims no
> production, deployment or activation readiness. Every artifact here is `PROPOSED`.

## 1. What Phase 16 is

Phase 15 specified a planning layer and left two obligations open on purpose, because closing
them meant changing something downstream that Phase 15 did not hold authority over:

| Open item | What it said |
|---|---|
| **PO-4** | A composed Work Plan is not a Workflow definition, so the approved intake check 1 has nothing to resolve. The COMPOSE path was specified and **not executable** |
| **PO-12** | No approved contract defined what a downstream consumer does with a planning record, or how an instance Work Plan differs from a reusable Workflow definition under change control |

Phase 16 is the bridge that closes both. It defines the **Execution Basis** — the governed
object that lets a valid plan *enter* Orchestrator intake — and the change-control contract that
keeps an instance-level plan from drifting into a reusable definition.

The whole path, with the new link in bold:

```text
natural-language request → intent → scope → objective & deliverables → classification
   → role / skill inference → MATCH or COMPOSE → Work Plan → governance preflight
   → **EXECUTION BASIS** → Phase 11 Orchestrator intake → Model Router → execution
```

## 2. The one thing the Execution Basis does, and the several it does not

It authorises **entry to intake**. That is all.

| It does | It does not |
|---|---|
| Bind a request, a scope, a plan version and an implementation-spec version into one governed object | Approve the work, the plan or any act |
| Make the seven approved intake checks answerable | Perform any of them — the Orchestrator still validates all seven and may refuse |
| Carry review requirements | Satisfy a review |
| Carry Decision Right requirements | Exercise a Right |
| Carry role and skill bindings against approved registries | Register, widen or create a capability |
| Become `STALE` when material planning inputs change | Survive a material replan |

`is_approval` and `is_authority` are declared `false` **as fields**, not merely omitted, so that
no consumer can read an `EXECUTABLE` basis as either.

## 3. Package map

| Artifact | Owns |
|---|---|
| `planner-output-contract.md` | The machine-readable planning result, field by field |
| `workflow-resolution-contract.md` | MATCH vs COMPOSE, and why neither promotes anything |
| `execution-basis-contract.md` | The governed object, its fields, lifecycle and fail-closed rules |
| `planner-orchestrator-handoff.md` | The exact mapping into the approved Phase 11 / Phase 14 intake |
| `change-control-contract.md` | Material vs non-material change; PO-12 |
| `clarification-and-ambiguity-contract.md` | Infer when safe; clarify when it matters; never activate while open |
| `criticality-review-authority-binding.md` | Floors, requirements, and what planning may never grant |
| `role-skill-assignment-binding.md` | Inference vs assignability; SoD |
| `idempotency-versioning-replay.md` | Durable identity, lineage, and no duplicate execution lineage |
| `observability-audit-provenance.md` | Operational vs governed events; end-to-end provenance |
| `po-4-and-po-12-closure.md` | What is closed, what it depends on, and what remains open |
| `phase-16-self-check.md` | Producer self-check, limits, and honest assurance credibility |

Reference implementation: `implementation/phase-16/` — domain model, preflight, handoff
builder, in-memory store, two runnable examples and the acceptance tests.
Assurance: `validation/phase_16_validation.py`, `validation/phase_16_mutation_probes.py`.

## 4. What this phase must never do, and where each is enforced

| # | Never | Enforced in |
|---:|---|---|
| A-1 | Make COMPOSE executable without an Execution Basis | `execution-basis-contract.md`; `preflight.py` |
| A-2 | Let an Execution Basis exercise authority | `ExecutionBasis.exercise()` raises |
| A-3 | Create a Decision Record, approval or Review Instance | `preflight.py` G-1, G-7, G-8 |
| A-4 | Let a material plan change leave a live basis standing | `store.invalidate_on_material_change` |
| A-5 | Accept an unapproved or stale Workflow under MATCH | `preflight.py` G-11 |
| A-6 | Make an unregistered Role or Skill assignable | `preflight.py` G-5, G-6 |
| A-7 | Let an author be the final critical reviewer | `preflight.py` G-10 |
| A-8 | Activate while a blocking clarification is open | `preflight.py` G-2 |
| A-9 | Create duplicate execution lineage for one request version | `handoff.idempotency_key`, `store.record_trigger` |
| A-10 | Promote a Work Plan to a reusable Workflow | `WorkPlan.__post_init__`; the store has no registration path |
| A-11 | Carry a caller-injected governed record into a trigger | `handoff.FORBIDDEN_IN_TRIGGER` |
| A-12 | Hand off on a stale or mismatched scope or version | `handoff.build_trigger` digest check |

## 5. Non-Runtime Statement

This package specifies no live model call, no provider integration, no secret, no database
migration, no production storage configuration, no deployment, no queue, no worker, no scheduler
and no production interface. The reference implementation is in-memory, standard library only,
and runs no network operation.
