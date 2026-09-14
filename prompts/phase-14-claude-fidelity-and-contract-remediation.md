# Phase 14 — Claude Fidelity & Contract Remediation

Repository: `dgerman-code/AI-OS`
Branch: `spec/phase-14-implementation-specification`

## Mission

Remediate ONLY the blockers found by the independent Phase 14 implementation-specification audit of exact baseline:

`7530f5cd9bd8258095784f8d7c24e54234c2036b`

Do not redesign approved Phase 1–13 semantics. Do not create new Decision Rights. Do not introduce runtime code, migrations, DDL, SDKs, infrastructure, secrets, credentials, workers, queues, schedulers, provider integrations, or production implementation.

All Phase 14 artifacts remain `PROPOSED`.

No PR.

## Source-of-truth order

1. Human approval records in `reviews/phase-*-final-approval.md`.
2. Approved Phase 1–13 architecture.
3. Phase 14 implementation specification.
4. Phase 12 reference implementation.
5. Validators.

Where Phase 14 conflicts with approved architecture, Phase 14 is wrong and must be corrected.

## Required remediation — seven blockers

### 1. Phase 9 Model Profile identity compatibility

Restore exact compatibility with the approved Phase 9 model identity scheme.

Audit finding:
- Approved Phase 9 Model Profile stable identity is `model.<stable_snake_case_name>`.
- Phase 14 introduced incompatible `model_profile.<name>` and separately allocated `model.<name>` to `ModelRef`.
- This creates either identity drift or collapse of `MODEL != MODEL PROFILE`.

Requirements:
- Read the approved Phase 9 documents and use their exact identity semantics.
- Do not invent a new prefix to make the specification aesthetically cleaner.
- Preserve `MODEL != MODEL PROFILE != PROVIDER != ENDPOINT != DEPLOYMENT` exactly as Phase 9 defines them.
- Reconcile any Phase 14 `ModelRef` concept with the approved identity stack; if the approved architecture does not define an independent stable `ModelRef` in the way Phase 14 assumes, remove or rename the Phase 14 construct rather than changing Phase 9 semantics.
- Update all affected schema tables, API contracts, transaction tables, examples, identity inventory, reproducibility set, tests and validator rules consistently.

### 2. Routing Decision / Model Result lineage

Audit finding:
- Phase 14 Model Result validation requires equality to a Routing Decision `model_ref` that the Routing Decision schema does not contain.

Requirements:
- Make the recorded Routing Decision and Model Result lineage internally complete and exactly consistent with approved Phase 9/11 semantics.
- The Model Result must be verifiable against fields actually persisted on the Routing Decision.
- Preserve the full six-part routing reproducibility set required by the approved architecture.
- Do not add a field merely to satisfy the validator if it is not part of the approved semantic model.
- Add exact cross-document validation of the Routing Decision schema versus Model Result lineage checks.

### 3. Restore Phase 8 conflict-resolution semantics

Audit finding:
- Approved Phase 8 treats generic conflict resolution as a professional Role conclusion checked by review; it does not itself require a Decision Right unless a resulting governed status/canonical change separately requires one.
- Phase 14 incorrectly makes `ResolveConflict` an authority-bearing `H` command and thereby invents an unlisted authority dependency.

Requirements:
- Restore the exact Phase 8 distinction between:
  - professional resolution/conclusion about a conflict;
  - review of that conclusion;
  - any subsequent governed status or canonical-state change requiring a separately mapped Right.
- `ResolveConflict` must not itself manufacture or require a generic Decision Right unless the approved Phase 8/7 model explicitly says so.
- If a later status transition needs authority, model it as a separate governed act.
- Update API, transaction, knowledge, authority, tests, open-items and validator documents consistently.

### 4. Preserve CANCELLED / TERMINATED asymmetry

Audit finding:
- Approved Phase 11 distinguishes `CANCELLED` as a human act from `TERMINATED` as the system stopping work that would breach a constraint.
- Approved Phase 12 permits termination without a human intervention.
- Phase 14 collapsed `CancelRun / TerminateRun`, requires human authentication/intervention for both and therefore either blocks required termination or fabricates human provenance.

Requirements:
- Separate cancellation and constraint-driven termination contracts.
- Cancellation: human-governed act, intervention/provenance as approved.
- Termination: system-enforced stop when continuing would breach a constraint; no invented human intervention is required.
- Still record exact system identity, cause, runtime event/audit records as applicable, and preserve immutable terminal semantics.
- Ensure the API, transaction table, actor/provenance model, audit model, tests and failure/recovery model all reflect the asymmetry.

### 5. Reconcile audit-event cardinality and transaction semantics

Audit finding:
- Rule V-6/API text says exactly one audit event per governed record write.
- Audit event schema references one governed record.
- Transaction tables sometimes emit one audit event for multiple governed writes and sometimes none.

Requirements:
- Define one precise, implementable rule and apply it everywhere.
- Default interpretation to preserve unless approved architecture contradicts it: each persisted governed-record mutation has its own same-transaction audit event linked to that exact governed record; one higher-level governed act may therefore produce multiple audit events plus one execution/runtime event.
- Distinguish act-level correlation/causation from record-level audit cardinality.
- Enumerate every multi-record governed act and show the exact audit rows produced.
- Do not group multiple governed-record changes behind one audit event unless approved Phase 10 explicitly authorizes such grouping.
- Cover insert, append, state transition, supersession, scope-transfer writes, review/decision gate records and canonical-related blocked hooks.
- Add validator checks that compare transaction-table governed writes to required audit-event rows.

### 6. Fix approval-state current-row uniqueness (U19)

Audit finding:
- Persistence spec uses nonexistent approval status `ACTIVE`.
- Approval-state schema uses `APPROVED` and leaves `APPROVED_WITH_CONDITIONS` current-row uniqueness unresolved.

Requirements:
- Derive the exact approval-state vocabulary from authoritative approval records/spec semantics.
- Remove nonexistent `ACTIVE` unless it is explicitly defined in approved architecture.
- Define precisely what makes an approval-state row "current" independently of approval semantic status if necessary.
- The uniqueness rule must cover every operative state without conflating approval status with row-currentness.
- Prefer an explicit immutable version/history model plus one enforceable current-pointer/current-marker rule if consistent with approved semantics.
- Update U19, approval registry schema, migration/versioning text, transaction model, tests and validator consistently.

### 7. Reconcile Rule I-1 and correct Phase 4 baseline/OI-12

#### 7a. Rule I-1

Audit finding:
- Phase 14 says every persisted governed reference is a stable-ID/version pair while its own inventory includes runtime-instance references that are intentionally unversioned.

Requirements:
- Distinguish versioned governed definitions/profiles from unversioned immutable runtime-instance identities.
- State the exact categories that require a version pair and those that require only stable immutable record identity.
- Preserve reproducibility without inventing versions for instance records.
- Update identity model, schema conventions and validator.

#### 7b. Phase 4 baseline / OI-12

The authoritative Phase 4 approval record already identifies baseline:

`8ddacb2b2d2bc47e1a65099df575a0b16205d046`

Requirements:
- Correct Phase 14 baseline tables to use that SHA.
- Remove false OI-12.
- Do not request a new human decision for something already resolved by the approval record.
- Add validator coverage that reads the Phase 4 approval record and verifies the cited baseline rather than hard-coding a contradictory statement.

## Validator hardening — mandatory

The audit rated Phase 14 harness credibility `MEDIUM` because 8/9 materially contradictory mutations were accepted. This remediation must materially harden `validation/phase_14_validation.py`.

At minimum add non-vacuous checks for:

1. exact Phase 9 Model Profile identity compatibility;
2. Routing Decision schema ↔ Model Result lineage consistency;
3. exact Phase 8 conflict-resolution authority boundary;
4. CANCELLED / TERMINATED actor and intervention asymmetry;
5. audit-event-per-governed-record-write cardinality across transaction tables;
6. U19/current approval-row consistency and valid status vocabulary;
7. exact Phase 4 approved baseline citation;
8. exact ordered identity-chain equality;
9. origin-axis completeness;
10. self-review identity inequality;
11. separator-boundary ancestry rule;
12. approval registry may record but never create approval;
13. operational/runtime events can never satisfy governance evidence;
14. no `ON CONFLICT DO NOTHING` exception for governed uniqueness;
15. no admin substitution for missing destructive-migration Right.

Add a committed Phase 14 adversarial/mutation assurance fixture or equivalent deterministic test mechanism. It must:
- weaken each load-bearing rule intentionally;
- fail loudly if the mutation target is not found;
- independently demonstrate the validator detects the weakening;
- classify any genuinely redundant mutation honestly;
- never modify Phase 1–13 artifacts.

Do not claim `HIGH` harness credibility merely because the validator count increases. Report the evidence and limitations honestly.

## Open items and blocked authorities

Keep BA-1…BA-4 fail-closed and unchanged in authority meaning:
- canonical promotion/status change;
- re-parenting / unregistered cross-scope acts;
- governed-content destruction;
- destructive production migration.

Do not create any new Decision Right.

After correcting false OI-12, preserve the remaining open items with the audit classification:
- implementation preconditions: OI-1, OI-2, OI-3, OI-4, OI-6, OI-8;
- production/organisational engineering deferrals: OI-5, OI-7, OI-9, OI-10, OI-11.

If you discover that one of these actually requires an architectural human decision before Phase 14 approval, report it explicitly; do not silently choose.

## Required regressions

Run and report:

```bash
python3 validation/phase_14_validation.py
python3 validation/phase_14_validation.py --verbose
python3 validation/phase_14_validation.py --json
python3 -m unittest discover -s implementation/phase-12/tests -v
python3 validation/phase_12_validation.py
python3 validation/phase_11_validation.py
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
python3 implementation/phase-12/examples/governed_run.py
python3 implementation/phase-12/examples/blocked_run.py
```

The inherited Phase 11 `159/160` and Phase 10 `145/147` findings must remain reported exactly and must not be repaired from Phase 14.

Verify byte-for-byte that approved Phase 1–13 artifacts are unchanged.

## Required final report

Return sections A–R:

A. REMEDIATION SUMMARY
B. BASELINE / CONTAINMENT
C. MODEL PROFILE IDENTITY REMEDIATION
D. ROUTING / MODEL RESULT LINEAGE
E. CONFLICT-RESOLUTION SEMANTICS
F. CANCELLATION / TERMINATION SEMANTICS
G. AUDIT CARDINALITY / TRANSACTION MODEL
H. APPROVAL-STATE UNIQUENESS
I. IDENTITY VERSIONING RULE
J. PHASE 4 BASELINE / OI-12
K. VALIDATOR / ADVERSARIAL HARDENING
L. BLOCKED AUTHORITIES / OPEN ITEMS
M. VALIDATION / REGRESSION RESULTS
N. FILES CHANGED
O. KNOWN LIMITATIONS
P. HARNESS CREDIBILITY
Q. REMAINING BLOCKERS
R. READINESS VERDICT

Expected implementation commit message:

`docs: remediate Phase 14 fidelity and contract blockers`

Do not create a PR.

Only if every audit blocker is actually closed and no new blocker is introduced, end exactly:

`READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION RE-AUDIT V2`
