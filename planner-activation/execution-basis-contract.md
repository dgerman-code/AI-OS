# Execution Basis Contract

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

> The Execution Basis is the object Phase 16 adds. It creates no authority. It is `PROPOSED`,
> like everything in this package, and approving Phase 16 is what would make it operative.

## 1. What it is, in one sentence

**A governed record that binds one request, one scope, one plan version and one
implementation-spec version, and whose `EXECUTABLE` status means the Orchestrator's intake may
*accept the trigger* — nothing more.**

## 2. What it is not

| Not | Because |
|---|---|
| An approval | `is_approval` is a declared field and is `false`, always |
| An authority | `is_authority` is a declared field and is `false`, always. `exercise()` raises |
| A satisfied review | `satisfy_review()` raises. Reviews are satisfied by reviewers, through `SubmitReviewInstance` |
| A Workflow definition | For COMPOSE it names a `work_plan.<id>@v`, which is not a definition and never becomes one |
| A run | It produces a **trigger**. A trigger is a request, not a start |
| A permission to perform any act | Every gate the plan names still stands |

**Rule EB-1 — the basis authorises entry, and entry is not execution.** After intake accepts, the
Orchestrator still activates stages, requests reviews, requests decisions and routes. Each is a
separate approved Phase 14 command, and each can refuse.

## 3. Fields

| Field | Content |
|---|---|
| `basis_id`, `version` | `execution_basis.<id>@<n>`. Version increments on supersession, never in place |
| `request_id`, `intent_id` | Provenance to the originating request |
| `scope_ref`, `scope_ancestry` | Exactly one governed scope, with its declared ancestry |
| `execution_mode` | `MATCH` or `COMPOSE` |
| `workflow_ref` | `workflow.<id>@<version>` — **MATCH only** |
| `work_plan_ref` | `work_plan.<id>@<version>` — **COMPOSE only** |
| `criticality` | The resolved band |
| `role_bindings`, `skill_bindings` | Approved identifiers only |
| `review_requirements` | Requirements. Unsatisfied, by definition |
| `decision_requirements` | Requirements. Unexercised, by definition |
| `evidence_requirements` | `(reference, state)` in the tri-state |
| `orchestrator_policy_ref` | The policy the plan assumes |
| `implementation_spec_version` | The Phase 14 baseline this basis was issued against |
| `planning_digest` | The staleness mechanism — §5 |
| `supersedes` | The prior basis this one replaces, where there is one |
| `status` | §4 |
| `is_approval`, `is_authority` | `false`, declared rather than omitted |

## 4. Lifecycle

| Status | Means |
|---|---|
| `DRAFT` | Being assembled |
| `VALIDATED` | Preflight passed. **Not approval, and not yet a trigger** |
| `EXECUTABLE` | Intake may accept a trigger built from it |
| `BLOCKED` | A preflight condition failed; no trigger exists |
| `STALE` | Material planning inputs changed after issuance |
| `SUPERSEDED` | A later version replaced it |

**Rule EB-2 — only `EXECUTABLE` produces a trigger.** `build_trigger` raises on any other status,
including `STALE`. There is no "proceed with a warning".

**Rule EB-3 — `VALIDATED` → `EXECUTABLE` is the whole of what Phase 16 adds.** It is one
transition, and it says intake **may accept**. A reader who takes it for approval has read the
two declared `false` fields and disbelieved them.

## 5. Staleness — the mechanism, not the intention

**Rule EB-4 — the basis is bound to a digest of the plan's material fields.** Scope, objective,
deliverables, work modes, criticality, execution mode, role / skill / review / decision / evidence
requirements, the workflow reference and the stage graph. Request wording, intent identifier and
presentation are **excluded**: a reworded request is not a new plan.

**Rule EB-5 — a material change makes every live basis for that request `STALE`.** Not "should";
the store does it, and `build_trigger` re-computes the digest and refuses a mismatch. A basis
cannot be used against inputs it was not issued against, even by a caller who wants to.

**Rule EB-6 — supersession is append-only.** The prior basis stays readable in `SUPERSEDED`,
carrying the reference of the one that replaced it. Governed history is not edited, and a stale
basis keeps its place in the lineage rather than being dropped from it.

## 6. Fail-closed rules

| Condition | Outcome |
|---|---|
| A blocking clarification is open | `CLARIFICATION_REQUIRED`. **No basis is created at all** |
| Criticality does not resolve | `BLOCKED`. Never `ROUTINE` by default |
| An act has no applicable approved Right | `BLOCKED` — `NO_APPLICABLE_DECISION_RIGHT` |
| The band requires an independent review and none is required by the plan | `BLOCKED` |
| A Role or Skill is not in the approved registry | `BLOCKED` — non-assignable |
| A required conclusion has no approved owner | `BLOCKED` + escalate |
| MATCH names an unapproved Workflow or a version that is not the approved one | `BLOCKED` |
| A prerequisite is a plain `UNKNOWN` | `BLOCKED` — dangling |
| Author and final critical reviewer are one identity | `BLOCKED` — SoD |
| A caller supplies a pre-formed governed record | **Refused**, by exception, naming what was attempted |

## 7. Non-Runtime Statement

This document is declarative architecture. It specifies no database schema, migration, storage
engine, transport or deployment, and binds no provider or runtime technology.
