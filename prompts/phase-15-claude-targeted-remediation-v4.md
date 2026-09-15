# Phase 15 — Targeted Remediation V4 after Independent Architecture Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`
Failed audited baseline: `9f641ecb00cd28d9e7c443e4f16790075c3fcf0d`

This is a targeted remediation only.

Do not modify approved Phase 1–13 artifacts.
Do not modify Phase 14.
Do not create runtime code, migrations, queues, workers, provider bindings, deployment, secrets, IaC, or a PR.
All Phase 15 architecture artifacts remain `PROPOSED`.
Do not claim human approval.

The V4 independent re-audit returned `FAIL` with only two remaining blockers. Close those exact blockers and the associated second-location consistency gaps without weakening any previously repaired boundary.

## 1. Blocker: no-approved-owner summaries contradict F-14 / RS-12 / RS-13

Current governing semantics are already correct:

- if a required conclusion has **no approved owning Role**, this is `F-14 NO_APPROVED_ROLE_OWNS_CONCLUSION`;
- disposition for the original request is **BLOCK + escalate**;
- the system must not silently narrow the original request and present a constrained result as though it answered the original;
- a narrower result is permitted only after a **new user-originated linked Request** that explicitly changes the requested deliverable.

The independent V4 review found active second-location contradictions in:

- `planning/open-items.md` PO-1 summary;
- `planning/phase-15-self-check.md` wording about Example 2.

Remediate every active summary so it says exactly the same thing as the governing rules and Example 2.

Required invariant:

`NO APPROVED OWNER FOR A REQUIRED CONCLUSION -> BLOCK ORIGINAL REQUEST + ESCALATE`

A constrained/narrower plan may exist only for a new linked Request initiated by the user. It is never the automatic fallback for the blocked original request.

Search the entire Phase 15 package for stale phrases such as:

- constrained plan for no approved owner;
- constrained or blocked;
- narrower result as fallback;
- silently remove missing conclusion;
- proceed without the unowned conclusion.

Remove or correct all active contradictions, not only the two locations named by the reviewer.

## 2. Blocker: Example 2 criticality floor is below WC-3

The V4 review found Example 2 fires T-15/T-16 while value remains unresolved, yet the exemplar permits `Enhanced Review Candidate` unless contract value warrants a higher band.

This conflicts with governing rule WC-3:

- where project/value is unresolved and an approved escalation trigger fires, the planning floor must be at least **Enhanced Decision-Grade**;
- wording simplicity must never lower the floor;
- conservative planning is not the same as fabricating a factual trigger or value.

Fix Example 2 so the criticality treatment follows WC-3 exactly.

Do **not** reinterpret the approved criticality policy. Do not fabricate a contract value. Do not invent a new trigger. State that with T-15/T-16 fired and value unknown, the plan floor is at least `Enhanced Decision-Grade` until the governing value/risk information resolves otherwise under approved policy.

Then search every Phase 15 worked example, summary, table and self-check for any second-location statement that would permit a lower band merely because:

- the user request is simple;
- the wording is non-technical;
- no value is stated;
- the task looks like drafting/communication;
- the system is uncertain.

Any such statement must be corrected.

## 3. Non-blocking stale reporting from V4 review

The V4 audit also found stale reporting. Correct it while preserving architecture semantics:

- criticality document introduction says four fired EIB triggers while worked example now has three fired triggers plus conservative escalation;
- validator evidence references 15 planning documents / 53 checks in places where actual totals are 16 documents / 55 checks;
- Example 2 introduction simultaneously says priority is stated and no priority is stated; keep the actual RI-12 result (`primary_work_mode = UNKNOWN`, secondaries `{ANALYSIS, DRAFTING}`) and remove contradictory prose.

Do not turn these documentation fixes into new semantics.

## 4. Assurance hardening

The producer harness has repeatedly gone green while independent readers found active contradictions. Do not claim HIGH assurance.

Add checks/probes that specifically catch, in second locations, at minimum:

1. PO-1 or any summary says no-approved-owner may CONSTRAIN the original request;
2. self-check or exemplar summary says Example 2 original request produces a constrained result;
3. no-approved-owner conclusion is silently removed from original deliverable;
4. a simple/non-technical request lowers criticality below a fired-trigger floor;
5. unknown value with fired trigger permits a lower-than-WC-3 band;
6. Example 2 criticality wording differs from WC-3;
7. stale document/check counts drift again;
8. Example 2 priority prose contradicts its actual RI-12 result.

Also rerun adversarial classes that escaped V4. Do not merely place probes where current checks already look. Put them in fresh second locations.

If a new probe is REDUNDANT on first run, treat that as evidence about test quality, fix the check structurally where possible, and record it in `planning/phase-15-self-check.md` rather than hiding it.

## 5. Preserve all previously repaired boundaries

Reconfirm that remediation does not regress any of these:

- `REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK != PLANNED WORK ITEM SPEC != WORK ITEM != ROLE != MODEL != ORCHESTRATOR != HUMAN AUTHORITY`;
- Phase 15 never creates runtime Work Items;
- no approved Phase 11 contract is claimed to consume `PlannedWorkItemSpec`;
- specs remain inert until explicit downstream change control;
- MATCH does not depend on specs;
- COMPOSE remains non-executable under PO-4 / PO-12;
- primary mode is derived upstream only and Example 2 returns `UNKNOWN` with `{ANALYSIS, DRAFTING}`;
- unanswered C4 is `AWAITING_CLARIFICATION -> BLOCKED`, never automatic PREPARE;
- load-bearing uses original-deliverable evidence and reduced-deliverable admissibility is a separate post-determination basis;
- F-14 remains the no-approved-owner branch and is never routed through F-5/F-6;
- prerequisite tri-state remains `RESOLVED / FUTURE_GOVERNANCE_REFERENCE / UNKNOWN->BLOCK`;
- review requirements do not satisfy reviews;
- decision requirements do not exercise authority;
- Phase 15 does not perform Phase 11 intake;
- no partial handoff;
- repeated plans never self-register as Workflows.

## 6. Required verification

Run and report:

- Phase 15 validator default;
- Phase 15 validator `--verbose`;
- Phase 15 validator `--json`;
- Phase 15 mutation probes;
- Phase 12 unit suite: `157 tests`, if still applicable;
- Phase 12 validator;
- Phase 11 validator;
- Phase 10 validator;
- Phase 9 validator;
- Phase 8 validator;
- `git diff --check`;
- containment diff proving approved Phase 1–13 and Phase 14 unchanged.

Preserve inherited findings exactly; do not repair Phase 10/11 in this workstream.

## 7. Final report

Return A–R with at least:

A. remediation summary
B. failed baseline and new exact remediation SHA
C. no-owner disposition repair
D. Example 2 criticality floor repair
E. stale-reporting cleanup
F. confirmation of preserved RI-12/C4/load-bearing/spec boundaries
G. validator changes
H. mutation results, including any first-run REDUNDANT probes and why
I. inherited regression results
J. containment
K. changed files
L. PO-4 / PO-12 status
M. remaining technical blockers
N. open items
O. assurance credibility
P. blockers before independent re-audit
Q. no human approval claim
R. readiness verdict

The only acceptable positive readiness wording is:

`READY FOR INDEPENDENT PHASE 15 ARCHITECTURE RE-AUDIT V5`

Do not claim Phase 15 approved, production-ready, activation-ready, or COMPOSE executable.
