# Phase 12 — Governed Evidence / Lineage Remediation

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-12-mvp`
Audit baseline: `56d88e6003e6f1994560595c6d49634f020fd3f1`

Status: REMEDIATION PROMPT ONLY. Do not open a PR. Do not modify Phase 1–11 architecture/orchestration/validators/approval records.

## Objective

Close the remaining nine structural blockers from the independent Phase 12 re-audit without changing approved Phase 1–11 semantics and without broadening MVP scope.

This is not a regex/NLP task. It is executable governance hardening. The invariant is:

> A governed act may change execution state only when the exact governed requirement, lineage, authority, adapter provenance, evidence object, and retained history needed by that act are already valid and recorded.

Never partially mutate state before validation completes.

## Required remediation

### 1. Construction-time type completeness
`enforce_reference_types()` currently protects governed references but not all mandatory governed fields. Extend construction-time validation so malformed governed objects cannot exist.

At minimum validate:
- Enum-typed fields such as `GateOutcome`, `RouterOutcome`, `GovernancePosture`, independence classes, retry classes, etc.;
- structured fields such as `ScopeBinding`;
- `Optional[T]`, tuples/frozensets/sequences where used;
- mandatory non-reference governed values;
- reject plain strings where Enum/structured types are required.

Explicit regression probes must include:
- `HumanWorkCompletion(... outcome="SATISFIED")` -> reject;
- `PrerequisiteEvidence(... outcome="SATISFIED")` -> reject;
- `RoutingRequest(... scope="...")` -> reject.

Do not implement blanket coercion.

### 2. Gate instance identity and repeated activation
A `GateRequirementRef` alone is not an instantiated gate identity.

Ensure each Gate Instance has a unique identity bound to at least:
- run;
- Work Item;
- requirement;
- gate kind.

Repeated activation of the same Task must create a second Work Item and separate Gate Instances without displacing the first.

Also prevent two Tasks in one Workflow Definition from accidentally aliasing instantiated gates merely because they reuse the same requirement id. Either enforce workflow-wide uniqueness for requirement identity or include task/work-item identity in instantiation keys. The outcome must preserve all gates independently.

Add tests proving:
- activate same gated Task twice -> two Work Items, two retained gate instances;
- satisfy only second -> first remains unsatisfied, completion blocked;
- two Tasks reuse same requirement id -> no displacement or silent alias.

### 3. Blocked / escalated run cannot progress through ordinary stage APIs
After `NO_APPLICABLE_DECISION_RIGHT`, a run in `BLOCKED` or `ESCALATED` / `AUTHORITY_ABSENT` must not be able to activate another declared stage until the governing unblock/reconciliation mechanism explicitly permits it.

`activate_stage()` and any equivalent public progression API must validate current phase/posture before mutation.

Add regression test for exact audit chain:
missing Right -> blocked/escalated -> attempt another stage -> reject; original gate remains retained.

### 4. Evidence-before-mutation transaction rule
Any continuing outcome must have complete valid evidence before changing:
- gate state;
- run phase;
- governance posture;
- governed record stores.

Specifically, a Decision adapter returning `SATISFIED` or `SATISFIED_WITH_OPEN_ITEMS` with `record is None` must fail before any state mutation.

Likewise, outcome on tuple/result must equal evidence object's own outcome.

Prefer a validate-then-commit sequence. If validation raises, observable run state and histories must be byte/value-equivalent to before the attempt.

Add tests asserting no partial commit.

### 5. `SATISFIED_WITH_OPEN_ITEMS` semantics are universal
For every gate kind and every public gate satisfaction path, `SATISFIED_WITH_OPEN_ITEMS` must apply `OPEN_ITEMS_CARRIED` posture consistently.

This includes:
- REVIEW;
- DECISION;
- HUMAN_WORK;
- GOVERNED_PREREQUISITE;
- externally supplied governed evidence via `satisfy_gate_with()`.

A run must not end `COMPLETED / GOVERNANCE_CLEAR` when its only satisfying outcome is `SATISFIED_WITH_OPEN_ITEMS`; expected completion is `COMPLETED_WITH_OPEN_ITEMS` if all other conditions permit.

### 6. Scope-transfer authorization must be retained, authoritative evidence
A well-shaped caller-created `ScopeTransferAuthorisation` must not be sufficient.

`transfer_scope()` must verify all of the following against source-run governed state/history:
- referenced Decision Record exists in source run retained decision history;
- Decision Record belongs to the exact source run/work item/requirement/right involved;
- authorizing human matches the Decision Record holder and approved holder set;
- authorization mechanism/version is one the source run recognizes as approved for the act;
- source scope exactly matches the immutable source binding;
- target authorization covers the complete target binding, including sensitivity/residency constraints, not just `ScopeRef`;
- no weakening of carried constraints unless the approved architecture explicitly permits it.

A fabricated authorization with no retained source Decision Record must fail.

Authorized transfer still creates a new execution; never mutate source-run scope.

### 7. Routing provenance and model-result lineage
Do not expose a public path that allows a caller to manufacture a Routing Decision and then merely "record" it.

A Routing Decision may enter governed history only as the direct result of invoking the configured RouterAdapter for the exact recorded Routing Request.

Required checks:
- `decided_by` equals configured RouterRef;
- RouterAdapter was actually called for that request;
- exact decision object/result returned by that call is what is recorded;
- request/run/work-item lineage matches;
- direct caller-manufactured lookalike is rejected.

If `record_routing_decision()` remains public, it must require provenance that cannot be fabricated through normal API use; otherwise make it internal.

For `ModelResult`, validate exact:
- run;
- Work Item;
- Routing Decision;
- model/model profile as applicable.

A model adapter returning a result for a foreign run/work item must be rejected before recording or progression.

### 8. Every gate satisfaction evidence object must be retained
If evidence is used to satisfy a gate, it must be appended to the corresponding governed append-only history before/atomically with applying the gate outcome.

`satisfy_gate_with()` must not create a state change without retained evidence.

Retain by own governed record identity, not Work Item id.

RecordStore must reject duplicate record identities rather than silently admitting ambiguous history.

Cover at minimum:
- ReviewInstance;
- DecisionRecord;
- HumanWorkCompletion;
- PrerequisiteEvidence;
- RoutingDecision and ModelResult where they are governance-relevant history.

Historical evidence needed to explain completion must remain reconstructable.

### 9. Adversarial and mutation credibility
Add tests for all audit variants above and strengthen the validator so it checks the behavior structurally, not by string matching only.

Required adversarial probes include at least:
1. malformed Enum field;
2. malformed ScopeBinding field;
3. repeated same Task activation with same requirement id;
4. cross-Task reused requirement id;
5. progression after missing authority;
6. continuing Decision outcome with no DecisionRecord;
7. no partial mutation on rejected evidence;
8. HumanWork `SATISFIED_WITH_OPEN_ITEMS`;
9. Prerequisite `SATISFIED_WITH_OPEN_ITEMS`;
10. fabricated full ScopeTransferAuthorisation;
11. fabricated RoutingDecision submitted through any public recording path;
12. configured Router mismatch;
13. foreign-lineage ModelResult;
14. externally supplied evidence satisfaction with missing history append;
15. duplicate record identity insertion.

Add controlled weakenings/mutations for load-bearing guards where practical. Mutation discipline should target the semantic guard, not exact implementation syntax.

## Preserve

Do not change protected Phase 1–11 files. Do not fix inherited Phase 11 159/160 or Phase 10 145/147 from Phase 12.

Keep MVP containment:
- standard library only;
- in-memory;
- no Supabase/SQL/migrations;
- no API server;
- no queue/worker/scheduler/event bus;
- no provider SDK/live LLM;
- no RAG/embeddings/agents;
- no credentials/secrets/deployment.

Do not implement true concurrency in this remediation.

## Validation expected

Run and report:

```text
python3 -m unittest discover -s implementation/phase-12/tests -v
python3 validation/phase_12_validation.py
python3 validation/phase_12_validation.py --verbose
python3 validation/phase_12_validation.py --json
python3 implementation/phase-12/examples/governed_run.py
python3 implementation/phase-12/examples/blocked_run.py
python3 validation/phase_11_validation.py
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Also demonstrate the specific audit bypasses now fail and that unsuccessful validation leaves run state/history unchanged.

## Files

Prefer modifying only Phase 12 implementation/tests/examples/README, `validation/phase_12_validation.py`, and `reviews/phase-12-foundation-self-check.md`.

If you believe an approved Phase 1–11 semantic change is necessary, STOP and report instead of editing it.

All Phase 12 artifacts remain `PROPOSED`.

Do not create a PR.

## Commit

Commit and push on `implementation/phase-12-mvp` with exact commit message:

`feat: harden Phase 12 governed evidence and lineage`

## Response format

Return exactly these sections:

A. REMEDIATION SUMMARY
B. CONSTRUCTION-TIME TYPE ENFORCEMENT
C. GATE INSTANCE / WORK-ITEM LINEAGE
D. BLOCKED-STATE / TRANSACTIONAL MUTATION RULE
E. EVIDENCE / OPEN-ITEMS SEMANTICS
F. SCOPE AUTHORIZATION PROVENANCE
G. ROUTING / MODEL PROVENANCE
H. APPEND-ONLY GOVERNED EVIDENCE HISTORY
I. ADVERSARIAL / MUTATION TESTS
J. VALIDATION / REGRESSION
K. FILES CHANGED
L. KNOWN LIMITATIONS
M. COMMIT / PUSH
N. NEXT STEP

N must be exactly:

`READY FOR INDEPENDENT PHASE 12 MVP RE-AUDIT V3`
