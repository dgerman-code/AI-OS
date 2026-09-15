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

| Material — changes the digest | Non-material — does not |
|---|---|
| `scope_ref` | `request_text` wording |
| `objective`, `deliverables` | `intent_id` |
| `primary_work_mode`, `secondary_work_modes` | Presentation, ordering of prose, summaries |
| `criticality` | Anything the user sees but the plan does not depend on |
| `execution_mode` | |
| Role, Skill, Review, Decision, Evidence requirements | |
| `workflow_ref` | |
| The stage graph — identities, roles, dependencies, gate flags | |

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
