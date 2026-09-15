# Phase 15 — Independent Architecture Re-Audit V4

## Repository / branch

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`

AUDIT / REVIEW ONLY.

Do not modify files.
Do not commit.
Do not create a PR.
Do not manufacture human approval.

Audit the exact immutable baseline:

`9f641ecb00cd28d9e7c443e4f16790075c3fcf0d`

Do **not** audit this later prompt commit.

Before substantive review:

1. print the exact audited SHA;
2. verify it equals `9f641ecb00cd28d9e7c443e4f16790075c3fcf0d`;
3. use a clean detached worktree;
4. verify Phase 13 approval commit `2c4b90def9a60f8b384feef10f8428c5b437597c` is an ancestor;
5. verify approved Phase 1–13 artifacts are byte-identical to their approved state;
6. verify Phase 14 files are unchanged;
7. verify all Phase 15 architecture artifacts remain `PROPOSED`;
8. if the audited SHA differs, STOP with `BASELINE MISMATCH`.

## Primary audit objective

Determine whether the Phase 15 architecture is now internally coherent and approvable as architecture for:

`Natural-language Request → Intent Understanding → Scope Resolution → Work Classification → Role/Skill Requirement Inference → Workflow MATCH or instance-level COMPOSE → Review / Decision / Evidence Requirements → Governance Preflight → approved Orchestrator handoff`

The user must not need to choose internal IDs, roles, workflows, models, routing policies, review profiles, or decision rights in normal use.

A PASS must mean that the architecture preserves all approved upstream boundaries while making natural-language intent planning explicit and fail-closed.

## Mandatory review areas

### 1. Identity and ownership separation

Independently verify at least:

`REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK != PLANNED WORK ITEM SPEC != WORK ITEM != ROLE != MODEL != ORCHESTRATOR != HUMAN AUTHORITY`

Confirm:
- Task / Activity belongs to the Workflow definition, not to a run;
- Work Item is a runtime identity owned by a run;
- `PlannedWorkItemSpec` is a non-runtime planning record and neither Task nor Work Item;
- Phase 15 never creates `work_item.<id>`;
- no Phase 15 planning record acquires runtime identity by persistence, validation or handoff.

### 2. PlannedWorkItemSpec / Phase 11 boundary

This is a critical V3 remediation target.

Derive the current contract independently from the active documents.

Required result:
- Phase 15 may produce `PlannedWorkItemSpec` only after plan validation;
- no currently approved execution-basis contract consumes it;
- it is inert with respect to execution today;
- no current Phase 11 behavior may be claimed to read, revalidate, translate or instantiate from it;
- MATCH does not depend on it;
- COMPOSE remains non-executable until PO-4 / PO-12 or another governed mechanism is approved;
- the existence of the spec must not act as a bridge around intake check 1.

Reject any active second-location text that contradicts this, including tables, record inventories, examples, summaries, open-item prose or self-checks.

### 3. Request / WorkIntent derivation

Verify `primary_work_mode` and `secondary_work_modes` are deterministic and upstream-only.

Specifically test the unprioritised analysis-plus-drafting request used in Example 2.

The normative RI-12 logic and Example 2 must prescribe the same result.

If neither mode is privileged by request-level evidence, the architecture must not arbitrarily promote one using plan-stage order, dependency order, sentence order, salience or implementation convenience.

Verify the `UNKNOWN` case is represented consistently and secondary modes carry the complete applicable set where required.

### 4. Clarification policy / unanswered C4

This is another critical V3 remediation target.

Verify that unresolved authority ambiguity follows the clarification policy exactly:
- C4 → `AWAITING_CLARIFICATION`;
- if unanswerable → `BLOCKED`;
- no automatic downgrade to PREPARE;
- no default that converts EXECUTE ambiguity into a preparation-only act;
- a later preparation-only request must be a new linked Request or equivalent user-originated revision, not a planner fallback.

Check owner rules and all second locations, including examples and UX prose.

### 5. Role / Skill ownership and no-owner branch

Verify:
- requirement inference derives from approved ownership / compatibility, not semantic resemblance;
- a similar Role cannot substitute for an unavailable or missing owner;
- candidate/future communication capability is not treated as approved;
- `NO_APPROVED_ROLE_OWNS_CONCLUSION` remains distinct from `REQUIRED_ROLE_UNAVAILABLE`;
- no-approved-owner remains BLOCK + escalation under F-14 / RS-12 / RS-13;
- F-5/F-6 cannot be used to CONSTRAIN around a conclusion for which no approved Role exists.

### 6. Load-bearing determination

This is a critical V3 remediation target.

Independently derive the predicate and record semantics.

Required distinctions:
- determination is made against the originally requested / declared deliverable before any reduction;
- `load_bearing_basis` contains only pre-reduction evidence: requested result, approved ownership, review/gate dependencies and pre-reduction plan requirements;
- `NOT_LOAD_BEARING` must be a positive finding with a complete basis, not a residual/default class;
- `reduced_deliverable_basis` may be written only after independent `NOT_LOAD_BEARING` and proves only that the reduced output is admissible;
- `reduced_deliverable_basis` must never prove the determination itself;
- when `LOAD_BEARING`, no reduced-deliverable basis should be required or used to soften the outcome.

Reject any schema row, example, preflight check, failure disposition or self-check that collapses these two evidentiary roles.

### 7. Scope / criticality / confidence safeguards

Verify:
- separator/sibling scope boundaries cannot be crossed by similarity or naming proximity;
- session context is not decisive alone;
- material scope ambiguity blocks/clarifies;
- confidence does not change ambiguity class or authority;
- criticality may only rise, never fall because wording appears simple;
- conservative escalation is not represented as factual trigger satisfaction.

### 8. Workflow MATCH / COMPOSE boundary

Verify:
- MATCH resolves an approved `workflow.<id>@version` unchanged;
- admissibility dominates similarity;
- COMPOSE creates an instance-level Work Plan only;
- Work Plan never becomes Workflow identity;
- repeated patterns produce only inert `PROPOSED` candidate suggestions;
- no registry mutation, self-registration or auto-approval exists;
- human gate stages carry no Role participation;
- COMPOSE remains non-executable under current Phase 11 intake semantics unless separately approved change control exists.

### 9. Evidence / prerequisite / preflight / handoff

Verify the strict prerequisite states everywhere they appear:
- `RESOLVED` → eligible subject to other checks;
- `FUTURE_GOVERNANCE_REFERENCE` → declared future reference, dependent act non-executable;
- plain `UNKNOWN` → dangling reference, BLOCK.

Reject any active wording equivalent to `resolved or UNKNOWN`.

Verify:
- Phase 15 performs governance preflight, not Phase 11 intake checks;
- Phase 15 must not create partial handoff envelopes;
- F-9 does not continue/block runtime stages;
- runtime stage control remains Phase 11-owned;
- no preflight check depends on a `PlannedWorkItemSpec` that is only generated after validation.

### 10. Review / Decision Right / knowledge semantics

Verify:
- ReviewRequirement != satisfied review;
- DecisionRequirement != exercised Decision Right;
- missing applicable authority blocks;
- planner never grants entitlement, authority or approval;
- persistence does not create governance evidence;
- all eight Phase 8 epistemic types remain separate;
- `AI_SUGGESTION`, `ASSUMPTION`, `SOURCE`, `UNKNOWN` are not promoted by silence, validation, confidence, persistence or downstream need.

### 11. UX requirement

Verify that the user can express ordinary needs in natural language and that Phase 15, not the user, resolves internal architecture objects.

The default UX must not require the user to choose:
- Role IDs;
- Skill IDs;
- Workflow IDs;
- Review Profile IDs;
- Decision Right IDs;
- Model Profiles;
- routing policies;
- orchestration internals.

Clarification questions must be in user/world vocabulary and only material ambiguities should block.

### 12. Open items / approval boundary

Independently inventory and classify all open items.

In particular:
- PO-4: COMPOSE execution-basis dependency;
- PO-12: downstream `PlannedWorkItemSpec` consumption dependency.

Assess whether each is:
- architecture blocker before Phase 15 approval;
- required change control before activation;
- safe implementation deferment;
- documentation/repository-governance only.

Do not let a fail-closed implementation dependency become a silent execution capability.

## Assurance review

Run all available committed checks from the exact audited baseline:

- `python3 validation/phase_15_validation.py`
- `python3 validation/phase_15_validation.py --verbose`
- `python3 validation/phase_15_validation.py --json`
- `python3 validation/phase_15_mutation_probes.py --json`
- Phase 12 unit suite under `implementation/phase-12/tests`
- Phase 12 validator
- Phase 11 validator
- Phase 10 validator
- Phase 9 validator
- Phase 8 validator
- `git diff --check`

Preserve inherited Phase 10 / Phase 11 findings exactly and do not repair them.

Do not trust a green producer harness as evidence of correctness.

## Independent inventories

Derive independently at least:
- Phase 15 architecture document count;
- PROPOSED document count;
- normative rule IDs and duplicates;
- planning record count;
- clarification class count;
- preflight check count;
- failure-mode count;
- open-item count;
- cited Role IDs;
- cited Workflow IDs;
- cited Review IDs;
- cited Decision Right IDs;
- unresolved governed identifiers.

Flag stale reporting even if non-blocking.

## Independent adversarial second-location mutations

Plant fresh mutations in temporary copies only; do not edit the repository.

Use locations not obviously targeted by the producer's latest probes. Test at least these classes:

1. Work Plan described as Workflow.
2. Repeated plans auto-register or auto-approve a Workflow.
3. High confidence bypasses C4/C5.
4. Blocking clarification gains a default.
5. Sibling scope selected by string similarity.
6. Simple wording lowers criticality.
7. Similar Role substitutes for an unavailable owner.
8. Future communication capability treated as approved.
9. Similarity overrides Workflow admissibility/precondition.
10. ReviewRequirement treated as a satisfied review.
11. DecisionRequirement treated as exercised authority.
12. Persisted planning record treated as governance evidence.
13. `AI_SUGGESTION` promoted to `FACT_CLAIM`.
14. PlannedWorkItemSpec selects model/provider/routing.
15. Phase 15 performs a Phase 11 intake check.
16. COMPOSE bypasses intake check 1 / PO-4.
17. PlannedWorkItemSpec described as runtime Work Item.
18. Load-bearing result based on urgency/confidence/convenience.
19. F-9 controls runtime stages.
20. Partial handoff envelope permitted.
21. Primary work mode omitted or duplicated in secondary set.
22. Task described as a run-created identity.
23. Approved Phase 11 described as consuming PlannedWorkItemSpec.
24. Spec generated before plan validation.
25. Governance preflight depends on a spec.
26. Primary mode derived from PlanStage or dependency order.
27. Reduced deliverable used to prove NOT_LOAD_BEARING.
28. No-owner branch routed through F-5/F-6 CONSTRAIN.
29. Plain `UNKNOWN` prerequisite treated as admissible.
30. PlannedWorkItemSpec used as a bridge for COMPOSE without change control.
31. `load_bearing_basis` accepts reduced-deliverable evidence.
32. `reduced_deliverable_basis` is required before NOT_LOAD_BEARING is independently established.
33. RI-12 normative worked example and Example 2 return different primary modes.
34. Unanswered C4 automatically degrades to PREPARE.
35. A later preparation-only path is created without a new linked Request/user decision.
36. OM/object inventory implies current execution influence for PlannedWorkItemSpec despite no approved consumer.
37. MATCH execution path is made dependent on PlannedWorkItemSpec.
38. A no-approved-owner conclusion is silently removed and the reduced deliverable returned as the answer to the original request.
39. Criticality is lowered because the request sounds simple/non-technical.
40. Review satisfaction or Decision Right exercise is inferred from plan validation/preflight success.

Report each mutation as DETECTED / ESCAPED / ERROR and give an independent total.

## Review credibility

State separately:
- confidence in the baseline-specific architectural findings;
- confidence in the producer validator/mutation harness.

Do not call the producer harness HIGH merely because it is green.

## Required output

Return sections A–R exactly:

A. FINAL VERDICT
B. BASELINE / CONTAINMENT VERIFICATION
C. IDENTITY / LAYER-SEPARATION REVIEW
D. REQUEST / INTENT MODEL REVIEW
E. SCOPE / CLARIFICATION / CRITICALITY REVIEW
F. ROLE / SKILL INFERENCE REVIEW
G. LOAD-BEARING / FAILURE-DETERMINISM REVIEW
H. WORKFLOW MATCH / COMPOSITION REVIEW
I. PLANNING OBJECT-MODEL REVIEW
J. REVIEW / DECISION-RIGHT / AUTHORITY REVIEW
K. KNOWLEDGE / EVIDENCE REVIEW
L. ORCHESTRATOR HANDOFF / PO-4 / PO-12 REVIEW
M. UX / LEARNING-BOUNDARY / FAILURE REVIEW
N. OPEN ITEMS / INVENTORIES
O. REGRESSION / ASSURANCE / ADVERSARIAL RESULTS
P. REVIEW CREDIBILITY
Q. REMAINING BLOCKERS
R. READINESS VERDICT

## Verdict discipline

Return `PASS` or `PASS WITH NON-BLOCKING NOTES` only if all material architecture contradictions are closed.

If the only remaining issues are explicitly fail-closed activation/change-control dependencies such as PO-4 / PO-12 and they do not create active contradictions, classify them accurately rather than treating them automatically as architecture blockers.

For approval readiness, require:
- A = `PASS` or `PASS WITH NON-BLOCKING NOTES`;
- Q = `NONE`;
- no active contradiction between owner and second-location documents;
- no hidden current-consumption claim for `PlannedWorkItemSpec`;
- no circular load-bearing proof;
- no C4 fallback to PREPARE;
- no mismatch between RI-12 and Example 2.

If approval-ready, end R with exactly:

`READY FOR HUMAN PHASE 15 ARCHITECTURE APPROVAL`

Otherwise end with:

`NOT READY — REMAINING BLOCKERS`
