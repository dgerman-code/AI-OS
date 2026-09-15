# Planner Output Contract

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

> Creates nothing, approves nothing, and confers no authority. This is the shape of a planning
> result, not a permission to act on one.

## 1. What a Planner Output is

The Phase 15 planning result, made machine-readable so that a preflight can judge it
deterministically. It is `AI_SUGGESTION` throughout: a reading of a request, not a finding about
the world (`planning/request-intent-model.md` RI-2).

**Rule PC-1 — the canonical contract carries no model-specific field.** No model, Model Profile,
provider, prompt, temperature, token budget or routing hint appears in it, and the reference
implementation raises on an attempt to add one. Model selection belongs to the Phase 9 Router,
after the Orchestrator creates a routing request — several governed steps downstream of here.

## 2. The fields

| Field | Type | Notes |
|---|---|---|
| `request_id` | id | Provenance root. Every later object links back to it |
| `request_text` | verbatim text | `SOURCE`. Never edited, summarised in place or replaced by its reading (RI-1) |
| `intent_id` | id | The structured reading, `AI_SUGGESTION` |
| `scope_ref` | one governed scope | Exactly one. Not a list, not a guess |
| `scope_ancestry` | ordered tuple | The declared path from the root. A scope with no ancestry is ambiguous, not resolved |
| `objective` | text | What the user is trying to achieve |
| `deliverables` | tuple | The declared outputs, **before** any constraint-induced narrowing (Phase 15 LB-0) |
| `primary_work_mode` | one enum value **or** `UNKNOWN` | Derived from upstream material only (RI-12, RI-13) |
| `secondary_work_modes` | unique set | Never contains the primary; complete where the primary is `UNKNOWN` |
| `criticality` | band **or** `None` | `None` is a determinate finding and **blocks**; it never defaults to `ROUTINE` |
| `execution_mode` | `MATCH` \| `COMPOSE` | §3 of `workflow-resolution-contract.md` |
| `role_requirements` | tuple | Approved `role.<id>` or an explicit "no approved owner" |
| `skill_requirements` | tuple | Approved `skill.<id>`, each naming the Role it activates for |
| `review_requirements` | tuple | Requirements. `satisfied` is present and **always false** here |
| `decision_requirements` | tuple | Requirements. `exercised` is present and **always false** here |
| `evidence_requirements` | tuple | Each in the tri-state of §4 |
| `clarifications` | tuple | Blocking or not; a blocking one carries no default |
| `work_plan` | `WorkPlan` \| `None` | COMPOSE only |
| `workflow_ref` | `workflow.<id>@<version>` \| `None` | MATCH only |
| `orchestrator_policy_ref` | id@version | The policy the plan assumes; the Orchestrator still resolves it |
| `unknown_fields` | tuple | Explicit `UNKNOWN`s, carried forward rather than silently absent |
| `injected_governed_records` | tuple | Always refused. Present so the refusal can name what was attempted |

**Rule PC-2 — `MATCH` and `COMPOSE` fields are mutually exclusive.** A MATCH result carries no
`work_plan`; a COMPOSE result carries no `workflow_ref`. An object carrying both has collapsed
two identities, and the constructor refuses it.

**Rule PC-3 — `UNKNOWN` is a value, never an absence.** A field that was never considered is a
defect in the planner, not an `UNKNOWN`, and the preflight fails a plan whose criticality is
`None` rather than reading it as `ROUTINE`.

## 3. Requirements are requirements

**Rule PC-4 — a requirement is never the thing it requires.** A `ReviewRequirement` is not a
satisfied review; a `DecisionRequirement` is not an exercised Right; an `EvidenceRequirement` is
not evidence. The preflight **raises** — it does not merely block — on a planning result that
arrives with `satisfied=True` or `exercised=True`, because that is not a plan that failed a
check, it is a caller claiming an act that only an approved Phase 14 command performs.

## 4. Prerequisite tri-state

| State | Means | At intake |
|---|---|---|
| `RESOLVED` | The reference resolves at an ID and version | Eligible |
| `FUTURE_GOVERNANCE_REFERENCE` | A declared future reference | Permitted; the dependent act is non-executable |
| `UNKNOWN` | Not held, and not classifiable as a declared deferral | **Dangling. Blocks** |

**Rule PC-5 — `UNKNOWN` is never relabelled as a deferral**, and a `FUTURE_GOVERNANCE_REFERENCE`
required before the first executable act blocks as well. This is the approved Phase 14 / Phase 15
semantics, carried without amendment.

## 5. Provenance

**Rule PC-6 — every object links back to the request.** `request_id` → `intent_id` →
`work_plan_ref` → `execution_basis_ref` → the trigger's `planning_provenance`. A reader can
reconstruct what the system understood and why, which is what makes a wrong reading auditable
rather than invisible.

## 6. Non-Runtime Statement

This document is declarative architecture. It specifies no parser, classifier, model, prompt,
schema migration, API or storage mechanism, and binds no provider or runtime technology.
