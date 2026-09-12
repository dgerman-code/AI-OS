# Execution Run Template

Status: PROPOSED — Phase 11 template candidate
Inherits: `standard.orchestration.common_constraints@0.1`

Synthetic values only. A runtime identifier here is **never** a governance identity.

## Identity and bindings
- **Run ID**: `run.<id>` · parent run where this is a sub-run
- **Workflow**: `workflow.<id>` @ **version** — immutable for this run
- **Orchestrator Policy**: `orch_policy.<id>` @ **version** — immutable for this run
- **Scope**: exactly one governed scope. **A change is a new run**
- **Criticality**: the Phase 3 band

## Material
- **Sensitivity labels**: a **set** of Phase 8 classes. Not a level, not a ceiling, not ordered
- **Required handling controls**: per label
- **Residency constraints**: allowed jurisdictions; cross-border posture

## Trigger
- Originator identity · trigger kind · **idempotency key** · intake validation result

## State — four axes
- **Run phase** (1 of 10) · **Terminal outcome** (absent until terminal, then 1 of 6) · **Wait reason** (only while `WAITING`, with its named subject) · **Governance posture** (1 of 4, always)

## Progress
- Stage instances · activity instances · work items · assignment attempts — **append-only**

## Governed references — recorded as values, never pointers
- Review Requests → Review Instances @ version
- Decision Requests → Decision Records @ version
- Model Invocation Requests → `rd.<id>` Routing Decisions
- Handoff Instances · artifacts @ version

## Open items
- Each carried item, with **the named upstream rule permitting it to be carried**

## Checkpoints
- Resume points, each recording state **and the governed references valid at that point**

## Audit
- Execution events · correlation and causation identifiers

## What this run is not
- Not an approval. **Completion is not approval**
- Not evidence that produced content is correct, reviewed or canonical
- Not a grant of authority to anyone who appears in it
