# Change-Control Contract — instance plans, definitions, and what a change invalidates

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

## 1. Two objects, two change-control regimes

| Object | Changed by | Governed by |
|---|---|---|
| **Work Plan** — `work_plan.<id>@v` | Replanning one request | This contract. A new version, linked to the old |
| **Workflow definition** — `workflow.<id>@v` | Phase 5 registry change control | Not this phase, and not reachable from here |

**Rule CC-1 — editing an instance plan is not editing a definition, and cannot become one.**
There is no operation in this package that writes to the Workflow registry. A replan produces
`work_plan.<id>@v2`; it never produces `workflow.<id>@v2`.

## 2. Material versus non-material

**Rule CC-2 — materiality is a computed property, not a judgement.** A change is material where
it changes the digest of the plan's material fields:

| Material — changes the digest | Not digested, and why |
|---|---|
| `scope_ref` **and `scope_ancestry`** | `request_text` — presentation. A reworded request is not a new plan |
| `objective`, `deliverables` | `request_id` and `intent_id` — **identity**, bound exactly and separately by EB-2e. Folding them into a hash would hide a cross-request reuse behind a digest mismatch instead of naming it |
| `primary_work_mode`, `secondary_work_modes` | `injected_governed_records` — refused outright, before any digest is taken |
| `criticality` | |
| `execution_mode` | |
| Role, Skill, Review, Decision, Evidence requirements | |
| **`clarifications`, including each one's blocking flag and its default** | |
| `workflow_ref` | |
| The whole Work Plan — stage identities, owners, dependencies, gate flags **and each stage's `expected_artifact`** | |
| **`orchestrator_policy_ref`** | |
| **`unknown_fields`** — the declared open items, which the trigger carries | |

**Rule CC-2a — a new planner field cannot be silently non-material.** Every declared field of
`PlannerOutput` is classified as material, presentation-only, identity or refused, and the module
refuses to load if one is unclassified. The five families in bold above were originally missing:
each was read downstream, so a change to any of them left an issued basis standing that no longer
described the plan, and none of them changed the digest.

**Rule CC-3 — a material change invalidates every live basis for that request.** The store marks
them `STALE`, and `build_trigger` refuses a digest mismatch independently. Two mechanisms, because
one of them will eventually be bypassed by a caller in a hurry.

**Rule CC-4 — a non-material change creates no new governed version.** The digest is unchanged,
`issue()` returns the existing basis, and the history stays one entry long. A reworded request is
not a new plan, and treating it as one would fill governed history with noise that hides the real
versions.

## 3. Re-preflight

**Rule CC-5 — a material change requires the full preflight again, not a delta.** Every check
runs: scope, criticality, capability registration, review floor, Rights, prerequisites, SoD, mode
and plan shape. There is no "previously checked" shortcut, because the change is what changed.

**Rule CC-6 — supersession is append-only.** The prior basis stays in `SUPERSEDED`, carrying the
reference of its replacement, and the new one carries `supersedes`. Nothing is deleted and no
version is edited in place.

## 4. Promotion — the PO-12 half

**Rule CC-7 — a recurring composed pattern may reach only `PROPOSED`.** The store emits a
workflow-candidate record with `is_approved=false` and `is_matchable=false`. There is no method
that changes either, and none that registers the candidate.

**Rule CC-8 — promotion is a separate governed act, elsewhere.** Taking a candidate into the
Workflow registry is Phase 5 change control: its own review, its own approval, its own version.
This phase supplies input material to that act and performs no part of it.

**Rule CC-9 — a candidate that has been observed many times is still a candidate.** Frequency is
not approval, and a count is not a governance argument.

## 5. Non-Runtime Statement

This document is declarative architecture. It specifies no diffing implementation, storage,
migration or versioning engine, and binds no provider or runtime technology.
