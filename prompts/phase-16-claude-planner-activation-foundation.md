# Phase 16 — Planner Activation & Execution-Basis Integration

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-16-planner-activation`

## Human-approved inputs

Phase 14 implementation specification approval commit:

`35a4c01be450e07b13ed52ca78e9834752261a45`

Human-approved Phase 14 architecture/specification baseline:

`ba9e3feebc25418b8f858c62e63bb0ec466b9a21`

Phase 15 intent & work-planning approval commit:

`72870de11857140c056bfe1e482ca6cd82940d74`

Human-approved Phase 15 architecture baseline:

`2301b66c39a218e966587731eee2f7472501f39c`

Phase 13 approval remains an ancestor of both lines.

## First action — establish the Phase 16 integration baseline

The Phase 16 branch was created from the Phase 14 approval commit. Before designing Phase 16, merge the exact Phase 15 approval commit into this branch with a normal non-squash merge so both approved histories remain visible and attributable.

Requirements:

- merge exact commit `72870de11857140c056bfe1e482ca6cd82940d74`;
- preserve both approval records unchanged;
- do not rewrite, rebase, squash, or cherry-pick approved history;
- if there is any semantic conflict in approved content, STOP and report it rather than silently choosing one side;
- do not create a PR.

After the merge, print the exact integration-baseline SHA. All Phase 16 work must descend from that merge commit.

## Objective

Phase 16 turns the approved Phase 15 natural-language planning architecture into an executable planning handoff that can feed the approved Phase 11 Orchestrator under the Phase 14 implementation contracts.

The target path is:

`Natural-language request`
→ `Intent understanding`
→ `Context / scope resolution`
→ `Objective + deliverable definition`
→ `Work classification + criticality`
→ `Role / Skill inference`
→ `Workflow MATCH or COMPOSE`
→ `Work Plan`
→ `Governance preflight`
→ `Execution Basis`
→ `Phase 11 Orchestrator intake`
→ `Model Router / execution`

This phase must close the two Phase 15 downstream obligations that intentionally remained open:

- **PO-4** — composed Work Plans must receive a governed execution basis before they can execute;
- **PO-12** — downstream change control must distinguish an instance-level Work Plan from a reusable Workflow definition and govern later promotion/change correctly.

## Core principle

The planner may infer, compose and propose. It may not silently create authority, canonical status, approved Workflow definitions, approved Roles, approved Skills, Decision Rights, or production execution permission.

`COMPOSE` remains non-executable until Phase 16 produces a valid governed Execution Basis.

`MATCH` may proceed only through an already-approved Workflow and only after the same preflight / authority / review / scope checks required by the approved architecture.

## Scope of Phase 16

Design and specify the minimum implementation-ready bridge from Phase 15 planner outputs to Phase 11/14 execution contracts.

Create a focused Phase 16 package under a new directory such as:

`planner-activation/`

Do not redesign Phase 1–15.

### Required contracts

At minimum define:

1. **Planner Output Contract**
   - exact machine-readable shape of the planning result;
   - intent, scope, objective, deliverables, classification, criticality, inferred roles, inferred skills, workflow mode, reviews, authority requirements, evidence/knowledge requirements, tasks and dependencies;
   - explicit unknown/ambiguous fields;
   - provenance to the originating user request;
   - no model-specific fields in the canonical planner contract.

2. **Workflow Resolution Contract**
   - exact `MATCH` vs `COMPOSE` semantics;
   - MATCH must name an approved Workflow identity/version;
   - COMPOSE creates an instance-level Work Plan only;
   - no composed plan becomes a reusable Workflow automatically;
   - repeated patterns may create only a `PROPOSED` workflow-candidate record.

3. **Execution Basis Contract**
   - define the governed object that authorises an otherwise valid Work Plan to enter Orchestrator intake;
   - exact fields, lineage, status lifecycle and fail-closed rules;
   - must bind request, scope, Work Plan version, approved Workflow where MATCH, role/skill bindings, required reviews, applicable Decision Rights, criticality, evidence requirements and implementation-spec version;
   - must distinguish `VALIDATED`, `EXECUTABLE`, `BLOCKED`, `SUPERSEDED` or equivalent states without inventing authority;
   - must not itself exercise a Decision Right;
   - must become invalid/stale when material planning inputs change.

4. **Planner → Orchestrator Handoff Contract**
   - exact mapping into the approved Phase 11 / Phase 14 Orchestrator command/intake model;
   - define what becomes a Workflow Run, Work Items, Gate Instances, scope binding, review requests, decision requests, model-routing requests and knowledge references;
   - no caller-injected governed records;
   - no bypass of Phase 14 command contracts.

5. **Change-Control Contract**
   - close PO-12;
   - distinguish edits to an instance Work Plan from changes to an approved Workflow definition;
   - define material vs non-material planner changes;
   - material change must invalidate or supersede the Execution Basis and require re-preflight;
   - promotion of a recurring composed pattern to a Workflow must remain `PROPOSED` until separately governed and approved.

6. **Clarification / Ambiguity Contract**
   - preserve the Phase 15 rule: infer when safe; clarify only when ambiguity can materially change scope, authority, professional conclusion, irreversible action or governed outcome;
   - exact planner state for `CLARIFICATION_REQUIRED`;
   - no Orchestrator activation while required clarification is unresolved.

7. **Criticality / Review / Authority Binding**
   - preserve the approved project-criticality floor and Enhanced Decision-Grade mode;
   - resolve mandatory Review Profiles and Decision Rights as requirements, not as things the planner may grant;
   - missing approved owner/right/profile must block and escalate, not be improvised.

8. **Role / Skill / Assignment Binding**
   - planner may infer candidate role/skill needs;
   - executable assignment must resolve only against approved registries and eligibility rules;
   - unregistered candidate capabilities remain non-assignable;
   - preserve identity-level SoD and author ≠ final critical reviewer.

9. **Idempotency / Versioning / Replay**
   - planning requests and Execution Basis issuance must have durable identity/version semantics compatible with Phase 14;
   - same request/version must not create duplicate governed execution lineage;
   - material replan creates a new linked version, never mutation of historical governed records.

10. **Observability / Audit / Provenance**
    - define which planning events are operational versus governed;
    - preserve separation between evidence, audit, execution events and authority;
    - retain provenance from user request → planning interpretation → Work Plan → Execution Basis → Orchestrator Run.

## Minimum runtime slice

This phase is not only prose architecture. Produce the smallest executable/reference implementation needed to prove the bridge works end-to-end at specification/MVP level without production deployment.

At minimum include:

- typed/domain models for Planner Output, Work Plan and Execution Basis;
- a deterministic preflight validator;
- a handoff builder that converts an executable planning result into the Orchestrator intake shape without bypassing approved contracts;
- a small in-memory/reference store or fixtures for version/lineage checks if needed;
- positive and blocked examples;
- unit tests for the critical planner→execution invariants.

Do **not** add live external model calls, secrets, Supabase production writes, deployment code or production UI.

## Mandatory acceptance scenarios

Implement and test at least these cases:

1. simple MATCH request → approved Workflow → valid Execution Basis → Orchestrator intake;
2. COMPOSE request → valid instance Work Plan → governed Execution Basis → Orchestrator intake without creating a Workflow definition;
3. COMPOSE request with missing required Decision Right → BLOCKED;
4. high-criticality request with required independent review unresolved → BLOCKED;
5. ambiguity materially affecting scope → `CLARIFICATION_REQUIRED`, no activation;
6. inferred unregistered Role/Skill → BLOCKED / escalation, never auto-register;
7. material replan after Execution Basis issuance → prior basis stale/superseded, no execution on old basis;
8. non-material presentation-only change → does not create a new governed plan version;
9. duplicate same request/version → idempotent reuse, no duplicate execution lineage;
10. repeated COMPOSE pattern → may emit only a PROPOSED Workflow candidate, never auto-promote;
11. MATCH against unapproved/stale Workflow version → BLOCKED;
12. author assigned as final critical reviewer → SoD failure;
13. missing required evidence / stale knowledge condition → BLOCKED where the approved contract requires it;
14. valid MATCH with all gates resolved → handoff contains no synthetic approval/authority objects;
15. planner attempts to inject a fully formed Decision Record or Review Instance → rejected.

## Governance boundaries

Do not:

- edit approved Phase 1–15 artifacts;
- edit Phase 14 approval record or approved baseline content except by reference;
- edit approved registries;
- create or approve Decision Rights;
- silently register Roles, Skills, Workflows or Review Profiles;
- change the approved 59-role universe through this phase;
- activate the separately approved Communication Specialist package;
- claim production readiness;
- create a PR.

## Assurance

Create a focused Phase 16 validator and a mutation/negative-test fixture. Keep it useful rather than enormous.

The validator must at least detect:

- COMPOSE becoming executable without an Execution Basis;
- Execution Basis exercising authority itself;
- planner-created Decision Right / approval / Review Instance;
- material plan changes that fail to invalidate the prior basis;
- unapproved Workflow accepted under MATCH;
- unregistered Role/Skill accepted for executable assignment;
- SoD violation;
- clarification-required request entering execution;
- duplicate request creating duplicate run lineage;
- Work Plan being silently promoted to reusable Workflow;
- caller-injected governed records in handoff;
- stale/mismatched scope or version lineage.

Do not spend time chasing exhaustive mutation perfection. The user explicitly wants to accelerate toward a working system. Architecture/runtime blockers matter; prose-only validator gaps are debt unless they expose a real contradiction.

## Required outputs

Produce:

A. Integration baseline and ancestry verification
B. Phase 16 package file list
C. Planner Output contract
D. MATCH / COMPOSE contract
E. Execution Basis contract
F. Planner → Orchestrator handoff mapping
G. PO-4 closure
H. PO-12 closure
I. Clarification / criticality / authority / review rules
J. Reference implementation summary
K. Acceptance-test results
L. Validator / mutation results
M. Containment statement
N. Remaining blockers
O. Verdict

If the package is coherent and all directly blocking tests pass, end exactly with:

`READY FOR INDEPENDENT PHASE 16 PLANNER ACTIVATION REVIEW`

Otherwise end with:

`NOT READY — PHASE 16 BLOCKERS REMAIN`
