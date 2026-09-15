# Phase 15 — Targeted Remediation After Independent Architecture Review

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`
Exact failed baseline: `f8ef2cf52a8581d87f05bfa0b8f822611b51fbda`

Mode: targeted architecture remediation only.

Do NOT modify approved Phase 1–13 artifacts.
Do NOT modify Phase 14.
Do NOT create runtime code, migrations, queues, workers, schedulers, provider integrations, deployment, IaC, secrets, or a PR.
Do NOT manufacture human approval.
All Phase 15 artifacts remain `PROPOSED`.

The independent review returned `FAIL`, `HIGH` credibility, with five blockers and a weak assurance harness. Close exactly those issues and adjacent contradictions without broad redesign.

## 1. Runtime Work Item ownership boundary

Current defect: Phase 15 says it may instantiate Phase 11 `Work Item` runtime identities before a run exists. This violates Phase 11 ownership.

Required remediation:
- Phase 15 must NOT instantiate a Phase 11 runtime `Work Item`.
- Introduce a distinct planning-stage object such as `PlannedWorkItemSpec` / `WorkItemSpecification` / equivalent clearly non-runtime identity.
- Preserve explicit identity separation, e.g. `PLANNED WORK ITEM SPEC != WORK ITEM`.
- The planning object may describe what Phase 11 later needs to instantiate a Work Item, but it has no runtime state, no run ownership, no assignment/execution status, no model selection, no routing action, and no orchestration semantics.
- Phase 11 remains solely responsible for runtime Work Item creation after a run exists.
- Update the handoff contract, object model, architecture summary, exemplars, validation and self-check consistently.
- Do not amend Phase 11 approved artifacts.

## 2. `work_mode` cardinality

Current contradiction: `request-intent-model.md` defines one enum value or UNKNOWN, while an exemplar uses both ANALYSIS and DRAFTING.

Required remediation:
- Choose one deterministic model and apply it everywhere.
- Preferred design: `primary_work_mode` as one enum + `secondary_work_modes` as a unique set of zero or more additional modes, if this preserves the architecture cleanly.
- Alternatively define `work_modes` as an ordered unique set, but then state how a primary/leading mode is derived where downstream logic requires one.
- Multi-part requests must be representable without free-form implementation inference.
- Update object schemas, exemplars, validation and mutation probes.

## 3. Deterministic F-5 / F-6 disposition

Current defect: CONSTRAIN versus BLOCK depends on whether a missing capability is “load-bearing,” but no normative predicate or record captures that.

Required remediation:
- Define an explicit, inspectable predicate for whether a missing Role/Skill/Review capability is load-bearing to the requested outcome.
- The predicate must derive from declared deliverables, owned professional conclusions, stage dependencies, and required gates/reviews — not confidence or convenience.
- Record the result in a first-class planning field/finding so the same inputs produce the same disposition.
- Example acceptable logic:
  - BLOCK if the unavailable capability owns a required professional conclusion, mandatory review, authority/gate prerequisite, or an upstream artifact required by every valid path to the requested deliverable.
  - CONSTRAIN only if a valid reduced deliverable remains that does not imply coverage of the unavailable capability and the omitted coverage is surfaced explicitly.
- F-5 and F-6 must each have one deterministic disposition from this predicate.
- No similar-role substitution.

## 4. Reconcile F-9 with G-11 / HO-2 / Phase 11 ownership

Current contradiction: F-9 says an affected stage blocks while unrelated later stages may proceed, but Phase 15 cannot operationally block/continue stages; G-11 treats unsatisfied requirements as a plan-level block; HO-2 forbids partial handoff.

Required remediation:
- Phase 15 must not perform stage execution or partial runtime progression.
- Define whether an unsatisfied evidence requirement results in:
  A) plan-level BLOCK before handoff, or
  B) a valid plan containing a declared future prerequisite that Phase 11 may wait on only if the approved Phase 11 semantics already permit such an unresolved prerequisite.
- Do not invent a partial-handoff mechanism.
- If current Phase 11 intake requires all declared prerequisites to resolve unless explicitly `FUTURE_GOVERNANCE_REFERENCE`, align Phase 15 to that approved rule.
- Preferred conservative outcome: required evidence that is necessary before the first executable dependent act blocks handoff; evidence legitimately deferred under an approved future-reference mechanism is represented as such, but Phase 15 itself does not “continue stages.”
- Make F-9, G-11, HO-2 and exemplars say exactly the same thing.

## 5. Self-check inventory count

Correct the stale statement “Ten open items” so it matches the canonical PO-1…PO-11 inventory. Prefer deriving the count in validation rather than hard-coding prose where possible.

## 6. PO-4 — preserve as explicit blocked implementation dependency

The independent review classified PO-4 as:

`APPROVABLE WITH EXPLICIT BLOCKED IMPLEMENTATION DEPENDENCY`

Preserve that classification.

Do NOT pretend COMPOSE is executable under current Phase 11 intake check 1.

State clearly:
- MATCH is executable in principle where it resolves an approved `workflow.<id>@version` and all other intake conditions are satisfied.
- COMPOSE produces a valid non-runtime Work Plan, but that plan cannot currently start a Phase 11 run solely as a Work Plan.
- Enabling Work Plan as an execution basis requires explicit Phase 11 change control or another approved mechanism.
- Never solve this by registering the instance-level Work Plan as a Workflow.

This is not a blocker to Phase 15 architecture approval if it remains explicit and fail-closed, but it IS a blocker to activation/execution of COMPOSE.

## 7. Criticality note cleanup

Non-blocking review note: the EIB meeting exemplar calls a meeting “submission-adjacent” under T-11 although T-11 is framed as an external submission.

Clarify the exemplar so it does not claim literal satisfaction of T-11 unless submission is actually contemplated. If rigor is raised conservatively, say it is criticality escalation / high-stakes treatment, not a false trigger match.

## 8. Assurance hardening — required

The independent review ran 16 second-location mutations and 12 escaped. Add substantive checks/probes for all escaped classes:

1. repeated plans auto-register an APPROVED Workflow;
2. high confidence bypasses C4;
3. sibling scope selected by string similarity;
4. unavailable Role replaced by similar Role;
5. future Difficult Conversations / Communication Strategy capability treated as approved;
6. ReviewRequirement treated as satisfied review;
7. DecisionRequirement treated as exercised Decision Right;
8. persisted planning record treated as governance evidence;
9. `AI_SUGGESTION` promoted to `FACT_CLAIM`;
10. planning-stage work item/spec selects a model;
11. Phase 15 performs a Phase 11 intake check instead of merely making it answerable;
12. COMPOSE bypasses intake check 1 / PO-4.

Also add probes for the five blockers being remediated:
- pre-run creation of runtime Work Item;
- contradictory singular/multi `work_mode`;
- nondeterministic load-bearing condition;
- partial stage continuation / partial handoff contradiction;
- stale open-item count.

Requirements for probes:
- mutate second or third active statements where possible, not only canonical owner tables;
- each required probe must be DETECTED by a named substantive check;
- report REDUNDANT/ERROR honestly;
- if the probe exposes a validator weakness, repair the validator and record that fact in self-check.

Do not claim HIGH harness credibility merely because all producer probes pass. Retain the explicit independent-review limitation.

## 9. Containment and regression

Run, at minimum:

- Phase 15 validator default / verbose / json;
- Phase 15 mutation probes;
- Phase 12 unit suite;
- Phase 12 validator;
- Phase 11 validator;
- Phase 10 validator;
- Phase 9 validator;
- Phase 8 validator;
- `git diff --check`;
- containment check proving approved Phase 1–13 unchanged and Phase 14 unchanged.

Inherited findings must remain exactly inherited:
- Phase 11: 159/160 unless independently changed by an upstream approved fix (do not fix here);
- Phase 10: 145/147 unless independently changed by an upstream approved fix (do not fix here).

## 10. Required final report

Return sections A–R.

At minimum include:
A. remediation summary
B. exact failed baseline + new immutable remediation SHA
C. runtime identity boundary / planned-work-item fix
D. WorkIntent cardinality fix
E. deterministic missing-capability disposition
F. evidence/prerequisite / handoff reconciliation
G. PO-4 status
H. criticality exemplar cleanup
I. validator changes
J. mutation results
K. inherited regressions
L. containment
M. changed files
N. remaining technical blockers
O. open items and their classifications
P. harness credibility
Q. readiness blockers
R. exact readiness verdict

If and only if all five blockers are closed, no new blocker is introduced, containment/regressions pass, and PO-4 remains explicit/fail-closed, end exactly with:

`READY FOR INDEPENDENT PHASE 15 ARCHITECTURE RE-AUDIT V2`

Otherwise end exactly with:

`NOT READY — REMAINING BLOCKERS`

Commit and push the remediation to the existing Phase 15 branch if all required checks complete. Do not create a PR.