# Orchestrator Policy Template

Status: PROPOSED — Phase 11 template candidate
Inherits: `standard.orchestration.common_constraints@0.1`

Coordination behaviour only. **This policy may never change what a stage means** — that is the Workflow definition's, and a policy that could would be a second, unreviewed definition.

## Identity
- **Policy ID**: `orch_policy.<id>` @ version — governed, repository-authoritative
- **Scope of applicability**: which governed scopes and criticality bands this policy governs

## Dispatch
- **Concurrency limits**: per run, per scope, per assignee. A limit may **delay** a dispatch; it may never **skip** one
- **Priority rule** among ready work items — deterministic, recorded

## Gates
- **Waiting window before escalation**, per gate kind. **This is when to escalate, never when to proceed**
- **Escalation target** per gate kind — a named human or body
- **On expiry**: `ESCALATED`, posture unchanged. **There is no auto-approve setting, and none may be added**

## Retry
- **Permitted retry classes** and attempt limits per class
- **On exhaustion**: `ESCALATED`. Never `FAILED`-and-continue, never silent continuation
- `NON_RETRYABLE_GOVERNED_ACT` and `NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT` are **never** retried automatically, and this policy cannot make them retryable

## Rework
- **Maximum iterations** per declared loop
- **On exhaustion**: `ESCALATED`

## Races
- Which of `BLOCK` · `IGNORE_AS_STALE` · `SUPERSEDE` · `RECONCILE` · `ESCALATE` applies to each of the ten cases, where the architecture leaves a choice. **Where it does not, this policy restates nothing and overrides nothing**

## Checkpoints
- Where checkpoints are taken; what each records

## What this policy cannot declare
- That a gate outcome other than `SATISFIED` permits continuation
- That a timeout approves anything
- That a Decision Right may be substituted, widened or inferred
- That a review may be re-requested without a recorded change to the work
- That a scope, sensitivity label or residency constraint may be widened
- That an authority-bearing act may be replayed
- That exactly-once is guaranteed — it is **not**, anywhere in this architecture
