# Phase 14 — Claude Remediation: Transaction Completeness, Approval Recording, Assurance Consistency

Repository: `dgerman-code/AI-OS`
Branch: `spec/phase-14-implementation-specification`
Target baseline to remediate: `c771d05dd86f019fc33e4aa12a3884f359db2cd0`

## Mission

Remediate ONLY the remaining blockers from the independent Phase 14 implementation-specification re-audit v2. Preserve all approved Phase 1–13 semantics and all Phase 14 fixes already accepted by the re-audit. Do not broaden scope, invent Decision Rights, add runtime/DDL/migrations/provider integrations, or create a PR.

All Phase 14 artifacts remain `PROPOSED`.

Use this governing rule throughout:

> A conforming engineering team must be able to implement every governed act and every assurance test without inventing missing semantics or reconciling contradictory contracts themselves.

## Exact blockers to close

### 1. Fix A12 so it matches the repaired terminal contract

The current test strategy still treats `TerminateRun` as though it accepts a human intervention and expects `FOREIGN_RUN_LINEAGE`. That contradicts the repaired system-only termination semantics.

Required correction:
- `CancelRun` remains a human act requiring a valid `HumanInterventionRecord`.
- `TerminateRun` remains system-initiated and requires a named breached/at-risk constraint, with no human intervention and no synthesised human identity.
- Replace A12 with an adversarial test that attacks the actual TerminateRun contract, for example:
  - missing named constraint;
  - caller attempting to provide/smuggle a human intervention where the command contract does not accept one;
  - missing/incorrect system actor identity;
  - termination attempted from an unreachable state.
- The expected result must be failure with full observational equality and no fabricated human provenance.
- Add a companion positive control showing valid constraint-driven termination succeeds without a human intervention.

### 2. Make the transaction table exhaustive over the full governed-command catalogue

The API catalogue defines governed commands that change governed state. The persistence transaction model currently claims exhaustive coverage but lists only 17 acts.

Required correction:
- Define one canonical machine-readable or validator-parsable governed-command inventory owned by the specification.
- Every state-changing governed command in `api-command-contracts.md` MUST have exactly one matching transaction-contract row (or an explicit alias mapping where multiple API names are semantically one governed act).
- Cover the currently omitted acts at minimum:
  - `RecordIntervention`
  - `ResumeRun`
  - `UnblockRun`
  - `SupplyGateEvidence`
  - `CreateKnowledgeItem`
  - `AdoptAISuggestion`
  - `RaiseConflict`
  - `ApplyConsequentStatusChange`
  - `CompleteRun`
  - and any other state-changing command present in the API catalogue.
- Each transaction row must specify: read set, validation/preflight set, OCC/concurrency check, exact governed writes, exact audit-event count, execution-event count, durable constraints used, and pre-commit refusal behavior.
- Blocked commands that always fail closed must explicitly state zero governed writes / zero audit writes and their refusal event semantics.
- The validator MUST derive the API command set and transaction-row set and require exact coverage (no omissions, no extra undeclared governed acts, no duplicate coverage unless explicitly aliased).

### 3. Reconcile approval-state recording authority, bootstrap transcription, nullable provenance, and pointer write

The current `RecordApprovalState` contract is contradictory: API class `H` implies a pre-existing mapped Decision Right/Decision Record, while the approval-state registry says transcription/recording itself does not create approval and bootstrap may legitimately have nullable Right/DecisionRecord lineage.

Required correction: distinguish at least TWO acts, without inventing authority.

A. `TranscribeApprovalState` (or equivalent precise name)
- Purpose: mechanical transcription of an already-existing authoritative human approval record into the machine-readable registry.
- It creates NO approval and exercises NO Decision Right merely by transcription.
- Source approval record is mandatory and must be resolvable/verifiable.
- `decision_right_ref` / `decision_record_ref` may be nullable exactly where the authoritative historical source did not record them.
- Bootstrap must be a bounded, reviewable migration/transcription process, not a generic runtime privilege.
- If there is no authoritative source record, fail closed as PROPOSED / not approved.

B. `RecordNewApprovalState` (or equivalent)
- Purpose: persist the result of a NEW governed approval/revocation/supersession act after that act has already satisfied the applicable Decision Right semantics.
- This path must carry the applicable Right/DecisionRecord provenance where required.

For BOTH acts:
- The persistence contract must write the immutable approval-state history row AND atomically create/move the `approval_state_current` pointer in the same transaction.
- Audit cardinality must follow one audit event per governed-record mutation.
- The API catalogue, persistence table, approval-state registry, security/authority model, migration/bootstrap section, and self-check must all agree.
- Do not allow a service/admin/authenticated caller to manufacture approval by calling a recording API.

### 4. Reconcile the durable uniqueness count everywhere

The specification now has U1–U21 (21 constraints), but implementation milestones still say 20.

Required correction:
- Replace stale milestone/count language with the actual inventory.
- Better: make validation derive the count from the canonical uniqueness table and verify every referenced milestone/checkpoint against that value, rather than hardcoding 21 in multiple places.
- Ensure no stale “20 durable uniqueness constraints” remains where it means the whole inventory.

### 5. Correct A17 canonical-promotion test semantics

Current A17 is internally contradictory because it says a mapped Right is mocked in while also expecting refusal because no Right is mapped.

Required correction:
Split the intent into unambiguous cases, for example:
- A17a: with current approved universe where no applicable canonical-promotion Right is mapped, `PromoteToCanonical` MUST refuse `NO_APPLICABLE_DECISION_RIGHT` with zero mutation.
- A17b: a synthetic future-spec fixture MAY test that merely presenting an arbitrary/non-applicable Right or forged Decision Record cannot satisfy BA-1. This must NOT claim that a valid mapped Right exists in current architecture.
- If testing future behavior after a hypothetical governed Phase 7 change, label it explicitly as non-current and do not use it as evidence that BA-1 is currently resolved.

Validator should catch contradictory test setup/expectation language where feasible through structured test metadata rather than prose matching.

### 6. Define insert-time `record_version_before` audit semantics

The audit-event schema currently requires both `record_version_before` and `record_version_after` non-null, but inserts have no prior record version.

Required correction:
Choose one explicit schema contract and apply it consistently. Preferred semantics:
- `record_version_before` is nullable ONLY for INSERT/create mutations where no prior governed record exists;
- `record_version_after` is mandatory for successful writes;
- for UPDATE/state-transition/pointer-move/supersession operations, both before and after are mandatory;
- for DELETE/destruction, if ever authorized in future, define the pair explicitly now (e.g. before mandatory, after nullable) but BA-3 remains blocked and no destructive path is enabled.
- mutation kind must be an explicit enum (`INSERT`, `UPDATE`, `SUPERSEDE`, `POINTER_MOVE`, etc.) sufficient to validate nullability rules.
- no audit event exists for a refused transaction.

Make the API/audit/persistence/test strategy agree.

## Assurance hardening required

The re-audit found that the validator missed cross-document contradictions despite 74/74 and 19/19 mutation probes.

Add committed adversarial/mutation coverage for at least:
1. A12 regressing to human-intervention termination semantics.
2. A governed API command missing from the transaction table.
3. A transaction-table row not represented in the governed API catalogue.
4. `RecordApprovalState` collapsed back into a single ambiguous authority class.
5. Transcription allowed to create approval without authoritative source provenance.
6. Approval history written without current-pointer update in the same transaction.
7. Uniqueness count mismatch between canonical inventory and milestones.
8. Contradictory A17 current-vs-hypothetical Right setup.
9. Audit INSERT event requiring non-null `record_version_before`.
10. Audit cardinality mismatch after adding the newly covered governed acts.

Mutation targets must fail loudly if not found. Classifications must be derived from execution, not comments. Do not count git/containment failures as substantive detection.

The validator should include cross-document exact-set checks where possible, especially:
- governed API command set == governed transaction act coverage set (modulo explicit aliases);
- uniqueness inventory count == milestone/checkpoint references;
- terminal command contract == adversarial test metadata;
- approval command classes == approval-state registry semantics;
- audit mutation kind == version-before/version-after nullability matrix.

## Regression / containment

Run and report:
- Phase 14 validator default / verbose / JSON;
- Phase 14 mutation/adversarial probes;
- Phase 12 unit suite;
- Phase 12 validator;
- Phase 11 validator (preserve inherited 159/160 exactly; do not repair here);
- Phase 10 validator (preserve inherited 145/147 exactly; do not repair here);
- Phase 9 validator;
- Phase 8 validator;
- governed and blocked Phase 12 examples.

Confirm protected Phase 1–13 artifacts are byte-identical to Phase 13 approval baseline `2c4b90def9a60f8b384feef10f8428c5b437597c`.

No runtime, migration, DDL, SDK, secret, provider integration, queue, worker, scheduler, daemon, infrastructure, or PR.

## Required report

Return sections A–R:
A. Remediation summary
B. Baseline / containment
C. A12 terminal-test correction
D. Governed-command / transaction completeness
E. Approval-state recording / bootstrap contract
F. Audit cardinality after full command coverage
G. Uniqueness inventory reconciliation
H. A17 canonical-promotion test correction
I. Audit record-version semantics
J. API / authority consistency
K. Persistence / transaction consistency
L. Validator / mutation hardening
M. Validation / regression results
N. Files changed
O. Known limitations
P. Harness credibility
Q. Remaining blockers
R. Readiness verdict

Only if all blockers are substantively closed, end exactly with:

`READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION RE-AUDIT V3`

Do not approve Phase 14 yourself.
