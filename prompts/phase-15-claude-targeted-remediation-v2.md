# Phase 15 — Targeted Remediation V2 after Independent Architecture Re-audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-15-intent-work-planning`
Failed audited baseline: `fa9447dedc8077783ab61f116988371128de8476`
Independent review verdict: `FAIL`, credibility `HIGH`.

This is a **targeted remediation only**. Do not redesign Phase 15 beyond what is necessary to close the review blockers and the escaped second-location mutations. Do not modify approved Phase 1–13 artifacts. Do not modify Phase 14. Do not create runtime code, migrations, queues, workers, schedulers, provider integrations, deployment, IaC, secrets, or a PR. All Phase 15 artifacts remain `PROPOSED`. Do not manufacture human approval.

The exact review to remediate is the V2 independent architecture re-audit of baseline `fa9447dedc8077783ab61f116988371128de8476`.

## 1. Mandatory blockers to close

Close **all six** remaining blockers exactly and consistently across every active location.

### Blocker 1 — restore `TASK != WORK ITEM`

The approved Phase 11 ownership distinction must be preserved exactly:

- `TASK` / `ACTIVITY` belongs to the Workflow definition / coordination pattern;
- runtime `WORK ITEM` belongs to a Workflow Run;
- `PlannedWorkItemSpec` is a Phase 15 planning object and is neither of those.

Fix every Phase 15 statement that groups “Task / Work Item” together or implies both are created inside a run.

The Phase 15 identity chain must explicitly preserve at least:

`TASK != PLANNED WORK ITEM SPEC != WORK ITEM`.

Do not alter the approved Phase 11 files.

### Blocker 2 — stop claiming current Phase 11 consumes `PlannedWorkItemSpec`

`PlannedWorkItemSpec` is a proposed Phase 15 planning object. No approved Phase 11 contract currently defines it as an intake object.

Therefore Phase 15 must **not** state as current behavior that Phase 11:

- reads `PlannedWorkItemSpec`;
- revalidates `PlannedWorkItemSpec` at intake;
- instantiates a Work Item from it;
- derives runtime identity directly from it.

Replace those claims with the correct governance boundary:

- Phase 15 may produce `PlannedWorkItemSpec` as non-runtime planning output;
- it may be included in a proposed handoff envelope only where an approved execution-basis contract permits it;
- the exact future translation / consumption semantics require explicit Phase 11 change control or another separately approved execution-basis mechanism;
- until then, COMPOSE remains non-executable under PO-4;
- MATCH continues to hand off through the approved Workflow-based intake path only.

This change must not silently resolve PO-4.

### Blocker 3 — reorder `PlannedWorkItemSpec` generation

The current planning sequence creates `PlannedWorkItemSpec` before requirements and validation, while HO-6 says it derives only from a validated PlanStage.

Make the sequence deterministic and acyclic.

Required ordering principle:

1. derive intent / scope / classification / requirements;
2. build candidate Work Plan and PlanStages;
3. attach Role / Skill / Review / Decision / Evidence requirements and dependencies;
4. run governance preflight / plan validation appropriate to Phase 15;
5. only then produce `PlannedWorkItemSpec` from the **validated planning stage**, if and only if the relevant execution path is eligible to produce such a specification;
6. only then build any handoff envelope permitted by the approved downstream basis.

Do not make `PlannedWorkItemSpec` a validation input for the same validation that is required before it can exist.

### Blocker 4 — remove circular `primary_work_mode` derivation

`WorkIntent` is upstream of PlanStage construction. Therefore `primary_work_mode` must not depend on downstream PlanStage dependency order.

Define a deterministic upstream derivation rule using only information available at Request / WorkIntent interpretation time, such as:

- explicitly requested end result(s);
- requested act versus analysis/advice/drafting/monitoring/decision support;
- direct grammatical / semantic target of the request;
- explicit execution verbs;
- stated deliverable priority;
- if more than one mode is requested and no earlier deterministic priority resolves the primary, set `primary_work_mode = UNKNOWN` and carry all applicable modes in `secondary_work_modes` or an equivalent clearly defined representation without inventing an arbitrary primary.

Do not derive upstream intent fields from downstream planning objects.

Retain the repaired cardinality:

- exactly one `primary_work_mode` enum value or `UNKNOWN`;
- `secondary_work_modes` is unique, may be empty, and never duplicates the primary.

### Blocker 5 — fix original-deliverable load-bearing semantics and RS-9

The current load-bearing example is circular because it first removes the missing communication-strategy conclusion, then calls the reduced output the declared deliverable, then concludes the missing capability was not load-bearing.

Make the rule explicit:

- LB-a and all load-bearing tests are evaluated against the **original requested / declared deliverable before any constraint-induced reduction**;
- only after `NOT_LOAD_BEARING` is independently established may LB-2 validate a reduced deliverable;
- a reduced deliverable can never be used as evidence that the removed capability was non-load-bearing.

Also reconcile RS-9:

- where a required professional conclusion has **no approved Role owner**, that branch is `BLOCK` for any plan that still requires that conclusion;
- F-5/F-6 apply only to an approved owning Role / Skill requirement that exists but is unavailable, unmapped, or otherwise not activatable;
- do not route the no-approved-owner case through F-5 as `NOT_LOAD_BEARING` unless the original requested deliverable is independently shown not to require that conclusion at all.

Update the difficult-partner-communication exemplar accordingly. If the future Difficult Conversations / Communication Strategy owner is unapproved and the user explicitly requests communication strategy, the architecture must not pretend that conclusion is available. The plan may only produce a narrower result if the original requested deliverable permits that narrowing under the non-circular predicate; otherwise it blocks.

### Blocker 6 — fix prerequisite reference handling

Two active handoff locations currently permit prerequisite references to be “resolved or explicitly `UNKNOWN`.” That conflicts with approved Phase 11 intake check 7.

Replace this everywhere with the exact approved distinction:

1. **resolved prerequisite reference** → eligible to proceed, subject to the rest of the intake contract;
2. **`FUTURE_GOVERNANCE_REFERENCE`** → allowed as a declared future reference and therefore non-executable until satisfied;
3. **plain `UNKNOWN`, unresolved, dangling, or otherwise unclassified prerequisite** → BLOCK / no executable handoff.

Plain `UNKNOWN` is never equivalent to `FUTURE_GOVERNANCE_REFERENCE`.

Use the same semantics in:

- `planning/intent-work-planning-architecture.md`;
- `planning/orchestrator-handoff-contract.md`;
- governance preflight and failure model where relevant;
- exemplars and self-check if they restate the rule.

## 2. Preserve PO-4 exactly

The independent review classified PO-4 as:

`APPROVABLE WITH EXPLICIT BLOCKED IMPLEMENTATION DEPENDENCY`

Preserve that classification.

Required meaning:

- MATCH may in principle create a Phase 11-compatible trigger only when an approved `workflow.<id>@version` is resolved and all other intake conditions are answerable;
- COMPOSE may create a valid non-runtime Work Plan;
- a Work Plan **cannot currently start a Phase 11 run as a Work Plan**;
- enabling COMPOSE execution requires explicit Phase 11 change control or another separately approved execution-basis mechanism;
- never solve this by registering the instance-level Work Plan as a Workflow;
- do not claim `PlannedWorkItemSpec` already bridges the gap.

PO-4 is not an architecture-approval blocker while this dependency remains explicit and fail-closed. It remains a blocker before activation / execution of COMPOSE.

## 3. Assurance hardening — mandatory escaped classes

The V2 independent review found 4/21 second-location mutations still escaped. Add **substantive second-location checks and probes** for all four, not merely phrase checks on the owner rule:

1. `PlannedWorkItemSpec` described as a runtime Work Item;
2. load-bearing result based on urgency / confidence / convenience instead of the normative predicate;
3. F-9 permits Phase 15 to continue / stop runtime stages;
4. `primary_work_mode` omitted, duplicated in `secondary_work_modes`, or derived from downstream PlanStages.

The validator must also gain direct cross-document checks for the six blockers above, including:

- `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`;
- no active claim that approved Phase 11 currently consumes `PlannedWorkItemSpec`;
- generation order: PlanStage requirements + validation before spec generation;
- primary-mode derivation only from upstream Request/Intent information;
- load-bearing evaluation against original requested/declared deliverable before any reduction;
- RS-9 no-approved-owner branch distinct from F-5/F-6;
- prerequisite tri-state of RESOLVED / FUTURE_GOVERNANCE_REFERENCE / BLOCKING UNKNOWN;
- PO-4 classification preserved and COMPOSE remains non-executable.

Do not claim the harness proves the architecture. Preserve the self-check's explicit limitations and record any redundant or escaped probes encountered while repairing it.

## 4. Required regression / containment checks

Run and report, at minimum:

```bash
python3 validation/phase_15_validation.py
python3 validation/phase_15_validation.py --verbose
python3 validation/phase_15_validation.py --json
python3 validation/phase_15_mutation_probes.py --json
python3 validation/phase_12_validation.py
python3 validation/phase_11_validation.py
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
git diff --check
```

Preserve inherited results rather than "repairing" them inside Phase 15:

- Phase 11 inherited finding: 159/160;
- Phase 10 inherited findings: 145/147;
- Phase 9: 277/277;
- Phase 8: 119/119;
- Phase 12: 55/55.

Verify all approved Phase 1–13 artifacts are unchanged and no Phase 14 file is modified.

## 5. Files likely affected

Inspect all active Phase 15 files, but likely changes include:

- `planning/intent-work-planning-architecture.md`
- `planning/request-intent-model.md`
- `planning/role-skill-requirement-inference.md`
- `planning/work-plan-object-model.md`
- `planning/orchestrator-handoff-contract.md`
- `planning/governance-preflight.md`
- `planning/failure-and-escalation-model.md`
- `planning/exemplars.md`
- `planning/open-items.md`
- `planning/phase-15-self-check.md`
- `validation/phase_15_validation.py`
- `validation/phase_15_mutation_probes.py`

Do not touch approved architecture files to make the new Phase 15 model fit.

## 6. Commit / readiness rules

If and only if the remediation is internally coherent and all required regressions have been run:

- commit the remediation on `architecture/phase-15-intent-work-planning`;
- push it;
- do not create a PR;
- do not create approval records;
- do not promote any Phase 15 artifact from `PROPOSED`.

The final report must use sections A–R and must include:

A. remediation summary
B. failed baseline and exact new remediation SHA
C. Task / PlannedWorkItemSpec / Work Item separation
D. `PlannedWorkItemSpec` downstream-contract boundary
E. corrected generation order
F. corrected WorkIntent / primary-mode derivation
G. corrected load-bearing / RS-9 semantics
H. corrected prerequisite reference semantics
I. PO-4 status
J. assurance / validator changes
K. mutation results, including first-run redundancies if any
L. inherited regressions
M. containment
N. remaining technical blockers
O. open items / deferred change-control items
P. harness credibility
Q. blockers before independent re-audit
R. readiness verdict

The only acceptable final readiness line, **only if all six blockers are genuinely closed**, is:

`READY FOR INDEPENDENT PHASE 15 ARCHITECTURE RE-AUDIT V3`

Otherwise finish with:

`NOT READY — REMAINING BLOCKERS`
