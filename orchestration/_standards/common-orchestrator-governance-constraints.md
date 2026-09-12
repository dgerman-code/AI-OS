# Common Orchestrator Governance Constraints

Status: PROPOSED — Phase 11 standard candidate
Standard ID: `standard.orchestration.common_constraints`
Version: 0.1

Every Phase 11 artifact inherits this document by reference and does not repeat it. Where anything in `orchestration/` contradicts this standard, this standard governs and the contradicting artifact is defective.

## 1. The orchestrator is a control plane, not an authority
It coordinates. It decides **when a governed thing is requested**, never **what the governed thing concludes**. Every question of the second kind belongs to the phase that owns it.

## 2. Coordination is not competence
Activating a Role does not make anything competent to perform it. A Role is a reusable profile with declared competence and accountability; an assignment is an activation of that profile for bounded work, and it confers nothing the profile did not already carry.

## 3. An assignment is not an agent
No execution creates a persistent persona, identity, memory or standing. A Role is not instantiated into a being; it is bound to a Work Item and released.

## 4. Completion is not approval
A stage that finished is a stage that finished. Approval is a governed act with a named authority, and no quantity of finished work becomes one.

## 5. Absence of a Decision Right is not permission
Where no approved Phase 7 Right covers an act, the outcome is **block and escalate** — the Phase 9 rule, unchanged. The orchestrator identifies the gap and has no power to fill it.

## 6. A timeout is never an approval
A review, decision or human gate that expires produces an **expiry**, which is a reason to escalate. Silence is not assent, and a deadline is not a signatory.

## 7. `DEFER` and `ESCALATE` never collapse into `APPROVE`
Each is a distinct governed outcome. An orchestrator that treats any of them as permission to continue has substituted its own judgement for the gate's.

## 8. The orchestrator never self-satisfies a gate
It may detect that a gate applies and create the governed request. It may not be the reviewer, the decider, the signatory or the promoter, in any configuration, for any criticality, under any urgency.

## 9. A model result is a model result
It is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED` under Phase 8, exactly as it would be from any other model. It is never a review outcome, never a decision, never canonical, and never evidence that a Role's work was done well.

## 10. Confidence is not authority
No score, probability or self-assessment produced by a model alters eligibility, satisfies a requirement or authorises an act. Phase 9 denies this for routing; Phase 11 denies it for execution.

## 11. The orchestrator is not the Router
It may submit a routing request. The Routing Decision is Phase 9's, made under the applicable Routing Policy, and the orchestrator neither chooses an endpoint nor rewrites a constraint.

## 12. Governed history is never rewritten
Execution events, Decision Records, review findings, routing history, canonical history and Phase 10 audit events are append-only. A correction is a new appended record naming what it corrects.

## 13. An execution record is not a governed artifact
It records that something happened. Whether the something was right, approved or canonical is recorded elsewhere, and a run's success says nothing about any of the three.

## 14. An operational log is never governance evidence
It may be truncated, sampled, rotated and discarded. Nothing that must survive is kept only there, and nothing governed cites it — the Phase 10 rule, unchanged.

## 15. A runtime identifier is not a governance identity
Run IDs, stage instance IDs, attempt numbers and correlation IDs address executions. Governed references are by **stable logical ID and version**, recorded as values.

## 16. Every execution binds to exactly one governed scope
Bound at intake, before any work. The orchestrator never crosses an organisation, programme, portfolio, project, product, workstream or `PERSONAL` boundary, and a crossing that looks convenient is the failure this rule exists to prevent.

## 17. A cross-scope movement uses an approved mechanism or does not happen
Phase 8's scope transfer and Phase 6's handoff are the mechanisms. There is no orchestrator-level shortcut, and coordination convenience is never a transfer.

## 18. No failure path weakens a constraint
Outage, urgency, retry exhaustion, cancellation, a missed deadline and an incomplete recovery never make a non-compliant model, deployment, storage location, reviewer or scope acceptable.

## 19. Sensitivity and residency are carried, never relaxed
Phase 8 labels and Phase 9/10 residency travel with the work through every stage, handoff, routing request and retry. The orchestrator may narrow what a stage sees; it may never widen where material may go.

## 20. Retry is not repetition of an authority-bearing act
A Decision Record, approval, signature, external publication, contract commitment, risk acceptance, purge or destructive migration is **performed once**. Replay of such an act is a defect, not a recovery.

## 21. Exactly-once is not claimed
Across an orchestrator, a database, object storage and any external system, exactly-once delivery is not achievable and is not asserted. What is provided is **idempotent-at-least-once for replayable steps** and **at-most-once by governed record for authority-bearing acts**, and the difference is stated rather than blurred.

## 22. An external side effect is not replayable
Once something has left the system, no retry un-sends it. A step with an external side effect is non-replayable by classification, and recovery from it is **compensation**, which is a new act, not a rollback.

## 23. Rollback is not compensation
Rollback restores a prior state and is available only inside a single transactional boundary. Compensation is a new, recorded, separately-authorised act that counteracts an effect that cannot be undone. Calling one the other hides which of them actually happened.

## 24. A dependency graph is acyclic
Rework is expressed as a **bounded loop construct** with a declared maximum and an escalation on exhaustion. A hidden cycle is a defect, and an unbounded one is a system that never stops.

## 25. Stale results are recorded, never applied
A review, decision or model result arriving after supersession, cancellation or reclassification is recorded against the instance that requested it and **does not** change the current run's state.

## 26. Two claimants on one Work Item is a block
Not a race to be won. Concurrency conflicts on governed state are resolved by version-pinned writes that fail rather than overwrite, per Phase 10.

## 27. Manual intervention is attributable and bounded
Every human act on an execution names the human, the reason, the scope of the act and its effect. An administrator's ability to perform an action is not authority to authorise one.

## 28. Reproducibility is by recorded reference
A historical execution reconstructs which definitions and versions it used, because it recorded the stable IDs and versions as values. A pointer resolving to current state answers a question nobody asked.

## 29. The orchestrator is provider-independent
Workflow semantics, state, dependency and gate semantics are portable. Whatever engine, queue or scheduler eventually executes them sits behind a declared adapter boundary and carries no governance meaning.

## 30. Phase 11 changes no approved semantics
It coordinates Phases 1–10. Where a coordination design would require an approved semantic to change, the design is wrong, and the change is a matter for the phase that owns the semantic.
