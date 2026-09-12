# Review, Decision and Human Gate Invocation

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Four gate kinds, kept apart

| Gate | Owned by | Satisfied by | The orchestrator's role |
|---|---|---|---|
| **Review gate** | Phase 6 | A Review Instance reaching `SATISFIED` under its Review Profile, by a reviewer meeting the declared independence class | **Detect that it applies; create the Review Request.** Nothing else |
| **Decision gate** | Phase 7 | A Decision Record produced by an eligible human exercising a **named, carded** Right | **Detect; create the Decision Request.** Nothing else |
| **Human work gate** | The workflow | A human completing requested work | Request and wait |
| **Governed-prerequisite gate** | Phases 8–10 | Evidence freshness, artifact integrity, scope and residency conditions being met | Evaluate against recorded state; block where unmet |

**Review and decision gates never merge.** A satisfied review is not authority to act, and an exercised Right is not a review having been done. Work that needs both needs both, and the orchestrator requests them as two objects with two references.

## 2. What the orchestrator may and may not do at a gate

| May | May not |
|---|---|
| Detect that a gate applies, from the definition and the governed state | Decide that a gate does not apply |
| Create the governed request with full context | Be the reviewer, decider or signatory |
| Name the applicable Review Profile or Decision Right from the definition | Substitute a different Profile or Right |
| Record the outcome by reference | Interpret the outcome into a different one |
| Escalate on expiry | Treat expiry as an outcome |
| Re-request after rework | Re-request until the answer changes |

The last row is a real failure mode and is therefore a rule: **re-requesting a gate is permitted only after a recorded change to the work**. Asking the same question of a different reviewer, unchanged, is reviewer shopping, and the orchestrator is the component best placed to do it accidentally.

## 3. Seven gate outcomes, none of which collapse

| Outcome | Meaning | Run effect |
|---|---|---|
| `SATISFIED` | The gate's requirement is met | Continue |
| `SATISFIED_WITH_OPEN_ITEMS` | Met, with items recorded and carried **where an upstream rule permits** | Continue; posture `OPEN_ITEMS_CARRIED` |
| `NOT_SATISFIED` | The requirement is not met | `REWORK_REQUIRED` or `BLOCKED`. **Never continuation** |
| `DEFER` | The gate declines to answer now | `WAITING` or `ESCALATED`. **Never `APPROVE`** |
| `ESCALATE` | The gate refers the question upward | `ESCALATED`. **Never `APPROVE`** |
| `EXPIRED` | The gate was not answered in the policy's window | `ESCALATED`, posture unchanged. **Never an approval** |
| `NO_APPLICABLE_DECISION_RIGHT` | No approved Phase 7 Right covers the act | `BLOCKED` **and** `ESCALATED`; posture `AUTHORITY_ABSENT` |

> **`DEFER`, `ESCALATE` and `EXPIRED` are not approvals**, and there is no configuration, criticality band, urgency level or policy setting under which they become one. A policy may set how long a gate waits; it may not set what happens to the answer.

## 4. When no Decision Right exists

The Phase 9 behaviour, unchanged: the orchestrator searches the approved Phase 7 register for a Right whose **declared subject covers this act**. Finding none, it records **`NO_APPLICABLE_DECISION_RIGHT`**, blocks, and escalates for governance design.

It does not:

- pick the nearest Right and read its subject more widely — widening a Right's declared subject is forbidden by the Right's own card;
- treat the absence as permission;
- ask a human to "approve it anyway", because a human without a Right has no Right either;
- continue and record the gap as an open item.

**Carding a Right is a Phase 7 act.** Phase 11 identifies the gap and has no power to fill it.

## 5. Independence, enforced where it is visible

The orchestrator knows who did the work, because it made the assignment. It therefore enforces the Phase 6 independence class **mechanically** at review request time:

- an assignee excluded by the Assignment Envelope's review restrictions (`orchestration/execution-run-model.md` §5, field 8) **cannot** be the reviewer;
- where the Profile declares `DIFFERENT_MODEL_FAMILY_REQUIRED`, the review's routing request carries the producing Routing Decision as the named prior selection, so Phase 9 can evaluate diversity against something real;
- where no eligible reviewer exists, the outcome is **`BLOCKED`**, not a relaxed class.

**Reviewer independence and model diversity remain two controls.** Satisfying one says nothing about the other, and the orchestrator's ability to check both does not merge them.

## 6. Human gates are not deadlines

A gate's waiting window is a **policy setting about when to escalate**, never about when to proceed. The only thing a window's expiry produces is an escalation to a named human or body, with the run's posture unchanged and the gate still unsatisfied.

This is stated plainly because the pressure runs the other way: a long-blocked run is expensive, everyone can see it, and "auto-approve after N days" is the single most natural thing to build into a coordinator. It is also the point at which the governance stops existing.
