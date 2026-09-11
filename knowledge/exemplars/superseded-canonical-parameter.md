# Exemplar 5 — Superseded canonical project parameter

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** that supersession is an effect of promoting a successor, not an act of its own, and that the superseded version stays intact.

## Identity
- Canonical ID: `knowledge.design_capacity.project_alpha`
- Versions: 1 `SUPERSEDED` → 2 `CANONICAL`
- Subject: the project's design capacity
- Scope: `PROJECT/<alpha>`
- Memory class: `SEMANTIC_MEMORY` — **unchanged across both versions and the supersession**
- Applicability mode: `NON_INHERITABLE` — a design capacity governs this project and propagates to nothing
- Origin: `HUMAN_ORIGIN`
- Sensitivity: `CONFIDENTIAL`

## What happened
Version 1 was promoted on the feasibility-stage technical basis. The detailed design changed the figure. Version 2 was promoted on the new technical basis, with a new effective-from — **and version 1 became `SUPERSEDED` at that moment, automatically.**

**Nobody decided to supersede version 1.** There is no such decision in this architecture (`knowledge/canonical-promotion-governance.md` §2): a scope cannot hold two canonical statements on one subject, so promoting the successor is the supersession. A separate power to supersede would be a power to leave the scope with no position while appearing to replace one.

## What survives
Version 1 keeps its content, its evidence, its effective period and its provenance, and stays readable. This matters concretely: the cost estimate, the grid application and the permit submission prepared against version 1 were prepared against the then-canonical figure. They were **correct at the time**, and version 1 is what demonstrates that. Erasing it would make every one of those documents look like an error.

## What supersession did not do
It did not make version 1 false — it was a sound figure on the feasibility basis. It did not update the artifacts citing it; each carries the version it was written against, and bringing them forward is separate work. It did not change any assumption or finding that fed version 1.

## The refresh cascade
Every record binding design capacity as an input — the cost model, the yield calculation, the connection application — has its refresh trigger fired by this promotion. They become **stale, not wrong**, and each is re-derived on its own timetable and its own criticality band.
