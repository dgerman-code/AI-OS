# Common Handoff Constraints

Status: PROPOSED — Phase 6 standard candidate
Standard ID: `standard.handoff.common_constraints`
Version: 0.1

Every Handoff Card inherits this document by reference and does not repeat it. Where a Handoff Card contradicts this standard, this standard governs and the card is defective.

## 1. A Handoff does not transfer professional ownership

The sending Role continues to own its artifact and its conclusion after transfer. The receiver takes custody of a package for a bounded next activity. Ownership moves only where the sending Role Card already defines a legitimate ownership transition — and then it is the Role Card's transition, coordinated here, not created here.

## 2. Receipt acknowledgement is not agreement with the conclusion

A receiver may accept a package as complete and still consider the conclusion wrong. Accepting the package says the package is usable; it says nothing about whether the work is right.

## 3. Receipt acknowledgement is not review satisfaction

However carefully a receiver inspects a package, inspecting it is not performing an independent review. A `review.<id>` is satisfied by an eligible reviewer under a Review Profile, never by a receiving Role acknowledging a transfer.

## 4. Receipt acknowledgement is not approval or canonicalization

Receipt moves nothing to `REVIEWED`, `APPROVED` or `CANONICAL`. The subject holds whatever governed state it held before transfer.

## 5. The sender cannot omit material assumptions, conflicts or unknowns

Every `ASSUMPTION` the conclusion rests on, every `CONFLICT_DETECTED` bearing on it, and every material `UNKNOWN` travels with the package, classified. A package that presents a conclusion without the uncertainty it rests on is materially incomplete, however polished.

## 6. The receiver cannot silently reinterpret missing inputs as assumptions

Where an input the receiver needs is absent, the receiver returns the package or blocks. Inventing a placeholder value and labelling it an assumption manufactures a basis the sending Role never provided and no Role owns.

## 7. The package must preserve provenance and version identity

The subject's version, its sources and their verification status, and the identity of the artifact version being transferred all travel with it. A package that cannot say which version it carries cannot support anything downstream.

## 8. A materially incomplete package blocks or returns for rework

Completeness is assessed against the package definition. Where a required element is missing and is material to the receiver's next activity, the outcome is `HANDOFF_BLOCK` or `RETURN_FOR_REWORK` — never acceptance with a note.

## 9. Required review and gate references cannot be bypassed by handoff

Where a Handoff carries a `REVIEW_REFERENCE` that must be `SATISFIED` before transfer, or a `DECISION_REFERENCE` gating it, transferring anyway is not an option. Urgency is not a bypass, and a handoff is never a route around a gate that the Workflow path carries.

## 10. A Handoff may narrow but cannot widen Role or Skill applicability

A Handoff may require more of a sender or receiver than the general case. It cannot make a Role competent where its card excludes it, and it cannot make a capability compatible where the approved Phase 4 records do not. The Handoff is never evidence of compatibility.

## 11. A rejected handoff preserves history and reason

`RETURN_FOR_REWORK` records what was returned, why, and against which package version. A returned package is not deleted and the return is not erased by a later successful transfer.

## 12. Re-handoff after rework identifies the superseded package

The new package states which prior package it supersedes and what changed. A receiver must be able to see that it is looking at the second attempt and what the first one lacked.

## 13. Criticality increases package and evidence depth, not Role identity

Higher criticality may demand more evidence, more provenance, more checkpoints and stricter state requirements. It never changes who owns what, and it never creates a Handoff identity that duplicates an existing one at a different depth.

## 14. Runtime executes handoffs but cannot redefine their semantics

A later runtime may transport packages, record acknowledgements and notify Roles. It may not redefine what receipt means, what completeness requires, or when a transfer is blocked.

---

## 15. Handoff-vs-Review boundary

A Handoff checks **package completeness and transfer readiness**. A Review checks **substantive quality, compliance, integrity or assurance** under a Review Profile. A handoff rejection is a transfer failure, **not** a review finding, unless a Review Profile explicitly says that condition is one.

## 16. Status discipline

All Phase 6 artifacts are `PROPOSED`. No Handoff Card may set its own status to `APPROVED` or `CANONICAL`.
