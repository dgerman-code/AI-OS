# Exemplar 5 — An act nobody is authorised to perform

Status: PROPOSED — Phase 11 exemplar execution run
Inherits: `standard.orchestration.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders. Every `decision.<id>` below is a real approved registry object, cited as it actually exists.

**Proves:** that the absence of a Decision Right is a block and an escalation, never an inference — and that the orchestrator, which can see the whole run and the whole register, has no power to close the gap.

## The run

`run.2026.dataset_retire.0064` · `workflow.dataset_retirement` @ v1 · scope `project.theta` · criticality **Enhanced Decision-Grade**.

Stage 5 is a **physical purge** of a superseded dataset's payload — destructive, irreversible, and governed. Retry class: `NON_RETRYABLE_GOVERNED_ACT`.

## The search for a Right

The approved Phase 7 register carries **eight** carded Decision Rights: `decision.stage_gate_progression`, `decision.exceptional_progression`, `decision.granting_authority_submission`, `decision.external_publication`, `decision.contract_commitment`, `decision.risk_acceptance`, `decision.production_release`, `decision.emergency_production_change`.

**None of them covers the destruction of governed content**, and the nearest candidates are instructive rather than usable:

- **`decision.risk_acceptance`** accepts a risk. It authorises no act, destroys nothing, and reading it as permission to purge would substitute accepting a consequence for authorising a cause.
- **`decision.exceptional_progression`** permits progression past one named unresolved item at one progression point. Its subject is a **governed work item**, not a dataset, and widening its declared subject is forbidden by its own card.

## The outcome

**`NO_APPLICABLE_DECISION_RIGHT`** → run **`BLOCKED`** and **`ESCALATED`**, governance posture **`AUTHORITY_ABSENT`**.

Recorded: the act requested, the constraint class, each Right considered and why it does not reach, and the specific gap — **no approved Right covers destruction of governed content**. The escalation goes to Phase 7's carding governance, not to a senior person.

## Five things that did not happen

1. **The nearest Right was not stretched.** Widening a declared subject is the defect, not a workaround for it.
2. **The absence was not read as permission.** An act nobody is authorised to perform is not an act everybody may perform.
3. **No human was asked to "approve it anyway."** A human without a Right has no Right either; seniority is not authority in this architecture.
4. **It was not carried as an open item.** `AUTHORITY_ABSENT` permits no completion, and `COMPLETED_WITH_OPEN_ITEMS` requires an upstream rule permitting each item — there is none for an unauthorised destructive act.
5. **It was not retried.** Retry re-executes a step; a block is an unmet constraint, and no number of attempts produces a Right.

## What is still true

The dataset is **untouched**. Its Phase 10 retention class, any legal hold, and its audit history are unchanged. The superseded version remains readable as what it was. Nothing was lost by blocking, which is the asymmetry worth noticing: **the cost of stopping here is a delay, and the cost of guessing is unrecoverable.**

## What would unblock it

A Phase 7 pass carding a Right whose declared subject covers destruction of governed content, exercised afterwards by an eligible human. That is **a Phase 7 governance extension**. Phase 11 identified the gap and has no power to fill it — and an orchestrator that could would be the single largest authority in the system.
