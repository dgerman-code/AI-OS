# Communication Specialist — Targeted Remediation V1

Repository: `dgerman-code/AI-OS`
Branch: `proposal/communication-difficult-conversations-specialist`
Failed audit baseline: `0c02b5e4a8916b58161bcc0cf074447c5b53fe9b`

## Objective

Perform one targeted remediation pass for the independent Communication Specialist package re-audit. Fix only the four remaining blocking defects and directly related stale reporting/assurance gaps. Do not redesign the package, do not expand scope, and do not create a PR.

All package artifacts must remain `PROPOSED`. Do not modify approved Phase 1–15 artifacts, approved registries, Decision Rights, or Phase 14. Do not register or approve the candidate Role, Skills, mappings, workflows, Review Profiles, or methodology. Do not claim activation or production readiness.

## Blocker 1 — conflicting external-authority routing

The governing Decision Right analysis correctly treats `decision.external_publication` as applying to release outside the entity under the entity's name, including private correspondence. Submission and contractual-commitment rights are additive where applicable.

Fix every active second-location contradiction, especially:
- `review-profile-communication-strategy.md` public/otherwise routing language;
- `workflow-difficult-interaction-response.md` public/otherwise split.

Required invariant everywhere:

`external release under entity name -> decision.external_publication`

Privacy/publicity is not a discriminator. `decision.submission` and `decision.contract_commitment` may apply in addition, never instead merely because the communication is private.

Do not create `decision.communication_send` or revive `decision.external_high_stakes_communication_send`.

## Blocker 2 — mandatory-review bypass on non-transmitting paths

Reconcile all paths with RC-5 / RC-5a and the Role Card.

Two known defects:
1. `workflow-thread-diagnostics.md` currently says no review is required because nothing is transmissible, while the diagnostic interface requires independent review when `high_stakes_communication = true`.
2. `workflow-difficult-interaction-response.md` currently skips S6–S10 on non-response, which can skip mandatory review even when RC-5 fires.

Required invariant:
- Review applicability is determined by RC-5 conditions, not by whether an external transmission occurs.
- A read-only diagnostic may have Decision Right `NOT_APPLICABLE` for transmission while still requiring independent professional review.
- Non-response does not waive mandatory review of the strategy/diagnostic where RC-5 fires.
- Self-review remains prohibited.

Do not make review mandatory where RC-5 does not fire.

## Blocker 3 — overbroad unresolved-item exception

Known active defects:
- `workflow-difficult-interaction-response.md`
- `workflow-formal-escalation.md`

They currently permit terminal progression with unresolved CRITICAL findings or unsatisfied required review through a generic named-human-Decision-Right exception.

Required invariant:
- Decision authority and review satisfaction are separate.
- A named/exercised Decision Right cannot cure an unsatisfied mandatory review.
- Unresolved CRITICAL review findings cannot be treated as satisfied.
- Terminal progression is allowed only when all mandatory review conditions are satisfied under the approved review contract and all applicable Decision Rights are separately resolved.

Narrow or remove the exception. Do not weaken fail-closed behavior.

## Blocker 4 — exact filter schema mismatch

`conversation-diagnostics-contract.md` claims exact structural identity with the owner filter contract but uses case-different keys such as `GOAL` / `NEXT_STEP`, while `communication-control-filter.md` uses lowercase `goal` / `next_step`.

Choose one exact canonical serialized schema and make all active contracts agree. Prefer the owner document's current canonical field names unless another approved package rule clearly governs. If any display labels are uppercase, distinguish display labels from JSON keys explicitly.

Add validation that compares exact ordered/canonical key sets where appropriate, not only counts/namespaces.

## Stale reporting / assurance cleanup

Fix only directly relevant drift found by the audit:
- evaluation narrative still describing 36 scenarios when current suite is E1–E44;
- self-check/document totals/open-item counts where demonstrably stale;
- validator evidence-vacuity message reporting 20 checks when the actual completed validator has 22 or the new post-remediation total.

Do not spend time chasing broad mutation-coverage perfection. The user explicitly wants to accelerate. The producer harness is a supporting control, not the approval criterion.

## Required validation

Run and report:
- communication package validator: default, `--verbose`, `--json`;
- committed package mutation probes;
- Phase 8 validator;
- Phase 9 validator;
- Phase 10 validator (preserve inherited `145/147` unless independently changed upstream — do not repair here);
- Phase 11 validator (preserve inherited `159/160` unless independently changed upstream — do not repair here);
- `git diff --check`;
- ancestry-aware containment from the branch merge-base, demonstrating no approved registry / Phase 1–15 / Phase 14 artifact modification.

Add targeted checks/probes only for the four blocker classes and their obvious second locations. Avoid another large assurance expansion.

## Manual closure checklist

Before declaring ready, manually verify all of the following across active package text:
1. private external correspondence under entity name always resolves `decision.external_publication`;
2. additive rights remain additive, never replacements;
3. withdrawn send Right remains withdrawn;
4. high-stakes read-only diagnostic can require review even with no transmission Right;
5. non-response cannot bypass RC-5 mandatory review;
6. self-review remains prohibited;
7. Decision Right cannot substitute for review satisfaction;
8. unresolved CRITICAL findings cannot be waved through by authority;
9. filter/diagnostic JSON keys are exactly consistent;
10. candidate Role/Skills/mappings remain unregistered and non-activatable;
11. OG-1/OG-2 remain human decisions recorded, not package approval;
12. Jefferson Fisher attribution/disclaimer boundary remains unchanged.

## Output

Return a concise report with:
A. Summary
B. Failed baseline and new remediation SHA
C. Blocker 1 closure
D. Blocker 2 closure
E. Blocker 3 closure
F. Blocker 4 closure
G. Stale-reporting cleanup
H. Validation results
I. Inherited failures
J. Containment
K. Remaining blockers
L. Verdict

If and only if all four blockers are closed and no new blocker is introduced, end exactly with:

`READY FOR SHORT INDEPENDENT COMMUNICATION SPECIALIST BLOCKER-CLOSURE REVIEW`
