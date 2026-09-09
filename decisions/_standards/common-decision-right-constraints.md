# Common Decision Right Constraints

Status: PROPOSED — Phase 7 standard candidate
Standard ID: `standard.decision.common_constraints`
Version: 0.1

Every Decision Right Card inherits this document by reference and does not repeat it. Where a card contradicts this standard, this standard governs and the card is defective.

## 1. A Decision Right grants no professional competence

Authority to decide is not ability to do. A holder approving a financial model does not thereby understand it, and the Right confers no methodology, no scope and no conclusion.

## 2. Role competence does not create Decision Right authority

Knowing how to do the work is not authority to commit to it. The two are separate objects and neither implies the other.

## 3. Workflow leadership does not create approval authority

`LEAD_ROLE` coordinates. It approves nothing, and reaching a gate as lead does not make the lead its holder.

## 4. Reviewer status does not create approval authority

Phase 6 denies reviewers approval power; this states the converse. Having satisfied a review is not having decided anything.

## 5. Artifact ownership does not automatically create commitment authority

The Role that owns an artifact does not thereby bind the entity to it externally. Ownership and commitment are different powers held under different bases.

## 6. Subject and effect must be bounded

Every Right declares what it decides about and what deciding does. A Right whose subject is a whole project, or whose effect is unqualified "approval", is not bounded and is defective.

## 7. A Decision Record is not a Decision Right

The Right is the type; the Record is the instance. A Right existing in the registry decides nothing.

## 8. A decision requested is not a decision made

A pending, tabled, circulated or awaited decision is an unmade one. The gate stays unsatisfied.

## 9. A meeting or an email is not a valid Decision Record

Correspondence and discussion are not authority. They constitute a record only where they are attributable to the Decision Right and carry the evidence the Right requires.

## 10. A Decision Right cannot make a Review `SATISFIED`

It may permit progression past an unsatisfied review where its scope includes that exception. The review's status is untouched, and no outcome relabels it.

## 11. A Decision Right cannot erase findings, risks, assumptions, `UNKNOWN` or conflicts

Authority acts on what to do about the world, not on what the world is. No outcome changes an epistemic state.

## 12. Exceptional progression keeps unresolved items open

The item remains visible, open and carried into every subsequent stage and gate. The Record names it.

## 13. Risk acceptance does not erase risk

Acceptance changes who carries the risk. The risk, its finding and its evidence basis remain recorded.

## 14. No Decision Right may waive law or regulation

A registry cannot create authority the legal order does not grant. A card purporting to is void, not merely defective.

## 15. Generic approval does not imply canonical promotion

`CANONICAL` requires a distinct promotion authority and is never inferred from an approval given for a bounded purpose.

## 16. Delegation cannot widen scope or bypass cardinality

A delegate cannot decide more than the delegator could, and delegation does not reduce a multi-holder requirement to one.

## 17. Revocation affects future exercise, not historical records

Removing a holder or ending a delegation invalidates what has not yet happened. It does not reverse, erase or invalidate a decision validly made.

## 18. Decision Records are immutable historical events

They are not edited. A correction is a **new Record linked to the prior one**, and both remain visible.

## 19. Urgency is not authority

An emergency creates conditions under which a pre-declared emergency Right may be exercised. It creates no authority where none was declared.

## 20. Emergency authority is bounded, temporary and retrospectively obligated

It carries a time limit, a maximum scope and a mandatory retrospective step. It does not become standing authority through use, and retrospective review does not rewrite the historical decision.

## 21. Cancellation retains history, evidence and open items

Stopping a path preserves the reason, the state, the findings, the artifacts, the prior decisions and any external commitments already given.

## 22. Decision dependencies transfer no authority or satisfaction

A prerequisite decision's outcome does not satisfy a dependent Right, contribute to it, or lower its requirements. Satisfaction is not transitive and cycles are prohibited.

## 23. Runtime validates against the registry; it does not mutate semantics

A later system may record holders, timestamps and delegation instances. It may not redefine what authority is, what satisfies a gate, or what an outcome does.

## 24. No model or agent may hold a Decision Right by model identity alone

A Decision Right is a **human** authority. No model, agent, orchestrator or automated process becomes a holder by being capable, by being trusted, or by being the thing that reached the gate.

## 25. Cross-Right separation cannot be bypassed

Where a Decision Right declares a `DECISION_RIGHT_SEPARATION` relationship as `SEPARATION_REQUIRED` and its objective activation condition holds, **the same human instance must not exercise both Rights for the same governed subject or context in the same decision chain.**

Eligibility is evaluated independently for each Right, and being eligible for both is not permission to exercise both. **Holding two eligibility classes does not bypass separation. Delegation does not bypass separation** — a delegate is the delegator's side of the pair for this purpose. **Within-Right cardinality does not satisfy cross-Right separation**: a multi-holder release does not cure one of those holders having accepted the risk being released.

Separation is relationship-level governance, declared card to card against a concrete `decision.<id>`. It is never inferred from a job title, a Role identity, a reporting line or seniority. `SAME_HOLDER_PERMITTED` applies only where a card declares it with an explicit defensible reason that preserves the independent-control purpose.

**Scarcity does not relax authority.** Where no separately eligible second holder is available, the second Right is not validly exercisable in that context and the gate stays unsatisfied. A Decision Record must be able to evidence which separation relationships were active and that they were observed.

This rule introduces no staffing algorithm, assignment engine or runtime scheduling of any kind.

---

## 26. Status discipline

All Phase 7 artifacts are `PROPOSED`. No Decision Right Card may set its own status to `APPROVED` or `CANONICAL`.
