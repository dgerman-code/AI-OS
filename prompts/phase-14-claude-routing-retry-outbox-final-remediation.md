# Phase 14 — Claude Final Routing / Retry / Outbox Remediation

Repository: `dgerman-code/AI-OS`
Branch: `spec/phase-14-implementation-specification`

## Scope

Target exact audited baseline:

`bf19b56d00443bc14a910f6c88fdf6979b311303`

Independent V4 verdict on this baseline: `FAIL` / `NOT READY FOR HUMAN APPROVAL OF PHASE 14 IMPLEMENTATION SPECIFICATION`.

This is a targeted remediation only. Preserve all approved Phase 1–13 semantics. Do not create, widen, map, or infer any Decision Right. Do not edit approved Phase 1–13 artifacts. All Phase 14 artifacts remain `PROPOSED`. No PR.

## Required blocker closure

Close all seven V4 blockers exactly, and prove each with cross-document validation plus mutation/adversarial probes.

### 1. Routing B1/B3/B4 transactional state semantics

Reconcile `api-command-contracts.md` §5.4, `model-router-runtime-contract.md` §5.2/§7, and `persistence-and-transaction-model.md` §7.2.

Requirements:
- Keep the single durable routing lifecycle: prospective envelope is non-governed; `route()` is the durable writer.
- B1 malformed/invalid answer on a first submission writes no governed routing record and one refusal execution event only.
- Explicitly define malformed/invalid answer after an already-durable prior submission: preserve the existing Routing Request, create no new decision, do not advance ordinal, and define exact execution-event/refusal behavior.
- For B3 valid non-selection and the equivalent B4 re-submission non-selection branch, include every required atomic run-state consequence in the transaction contract: run phase, governance posture, wait reason/subject where applicable, escalation/block state, exact governed-write count, exact audit-event count, exact execution-event count.
- The transaction must not allow a durable non-selection decision while the run remains eligible to continue.
- Preserve Phase 11’s same-request / every-decision-recorded semantics and U6 submission-ordinal uniqueness.

### 2. Retry R2 / R2f / R4 / R6 / RX complete posture semantics

Reconcile `api-command-contracts.md` §5.6, `orchestrator-runtime-contract.md`, `failure-recovery-race-model.md`, and the persistence transaction table.

For every retry branch, including R2, R2f, R4, R6, RX, specify:
- before phase;
- after phase;
- before posture;
- after posture;
- wait reason / escalation state when relevant;
- exact governed writes;
- exact audit-event count;
- exact execution-event count;
- whether dispatch occurs;
- whether a retry-attempt/dispatch record is created.

R4/R6/RX must make their halted/escalated posture explicit in the exact writes, not only prose. Preserve that compensation is a separate governed act and that unknown external effect is never auto-replayed.

### 3. Implementable outbox lease / claim / deduplication protocol

Reconcile `persistence-and-transaction-model.md` §§7.1 and 9, `api-command-contracts.md` §5.5, `failure-recovery-race-model.md` §6, and any relevant component/security sections.

Specify a complete provider-call outbox protocol without introducing a concrete vendor or production implementation:
- stable outbox record identity;
- durable uniqueness constraint(s);
- linkage to ModelInvocationRef and ProviderAttemptRef;
- claim state vocabulary;
- atomic claim/lease acquisition precondition;
- claimant service identity;
- lease owner and lease expiry;
- compare-and-swap / OCC token semantics;
- no concurrent valid lease for the same dispatch item;
- redelivery after expired lease;
- stable provider idempotency key;
- receiver-side deduplication assumption where available;
- behavior where provider-side deduplication is unavailable;
- crash before claim, after claim/before dispatch, after dispatch/before outcome, after outcome/before persistence;
- durable `ATTEMPTED_OUTCOME_UNKNOWN` path and reconciliation;
- exact conditions for safe redispatch versus mandatory reconciliation/block.

Do not claim distributed transaction or exactly-once delivery.

### 4. Resolve outbox audit classification contradiction

Choose one consistent classification and apply it everywhere.

If outbox rows are operational records, they must not be counted as governed mutations/audit events under P-14d. If they are governed records, P-14d and the record-family model must change consistently. Prefer preserving the approved Phase 10/11 distinction that operational delivery plumbing is not governance evidence/authority unless the architecture requires otherwise.

Then derive stage-1 exact governed-write and audit counts from that classification and update API, persistence, audit/provenance, self-check, validator and tests consistently.

### 5. Stage 3 / Stage 4 transaction boundary contradiction

`api-command-contracts.md` §5.5 currently cannot simultaneously say stages 3 and 4 are one transaction and define a crash state after stage 3 before stage 4.

Choose one coherent contract:
- either outcome + Model Result are one local transaction, with no committed crash window between them; or
- they are separate durable transactions, with explicit idempotent recovery, exact record identities, OCC, audits and no duplicate Model Result.

The resulting crash table, transaction table, API contract, failure/recovery model and assurance tests must agree exactly.

### 6. Refusal-event observational equality semantics

Reconcile `orchestrator-runtime-contract.md` Rule O-25, `test-and-assurance-strategy.md` §3, B1 and blocked-command contracts.

Define observational equality precisely:
- refused/failed pre-commit acts must preserve governed state and governed-history counts;
- an explicitly specified refusal execution event MAY be appended where the contract requires one;
- such a refusal event must never count as governance evidence, gate evidence, approval, authority, or state progress;
- tests must compare governed state/history for equality while separately asserting the allowed refusal event.

Remove any language that simultaneously requires total execution-event-count equality and one required refusal event.

### 7. Self-check / count drift and validator honesty

Fix `implementation-spec/phase-14-self-check.md` active stale claims: removed `RequestRouting`, 35 command/row counts, and any other outdated inventory totals.

The current canonical inventories must be parsed, not hard-coded from stale prose. Validator must detect every normative count-bearing occurrence in relevant Phase 14 documents, including:
- leading and trailing numeric forms;
- word-form counts (`thirty-six`, `thirty six`, etc. where applicable);
- command counts;
- act counts;
- transaction branch counts;
- uniqueness counts;
- assurance inventory totals;
- obsolete command names such as removed `RequestRouting` where the text claims current inventory membership.

Add a committed mutation probe that reproduces the exact V4 miss: change only the self-check’s current command/row count and reintroduce `RequestRouting`, while leaving canonical inventories correct. The mutation must be detected by a named substantive check.

## Validator / mutation requirements

Do not merely add string-presence checks. Add cross-document checks that parse the owning inventories/contracts and compare independently derived structures.

At minimum add controlled weakenings for:
1. B3 decision durable but no run-state halt/escalation write;
2. B4 non-selection re-submission missing run-state consequence;
3. malformed answer after durable request incorrectly increments submission ordinal;
4. R2f missing posture;
5. R4/R6/RX missing explicit halted posture write;
6. outbox missing stable identity/uniqueness;
7. two concurrent active leases allowed;
8. lease expiry incorrectly treated as proof no provider effect occurred;
9. outbox counted as governed mutation while classified operational;
10. impossible crash window between same-transaction stage 3 and 4;
11. refused act test requires execution-event equality while contract requires a refusal event;
12. stale self-check 35/35 plus removed `RequestRouting` surviving.

Every probe must be `DETECTED` by the intended named check. Missing probe target is `ERROR`, never skipped. Do not count git/containment failures as substantive mutation detection.

## Regression / containment

Run and report:
- Phase 14 validator default / verbose / JSON;
- Phase 14 mutation harness;
- Phase 12 unit suite;
- Phase 12 validator;
- Phase 11 validator, preserving inherited `159/160` exactly;
- Phase 10 validator, preserving inherited `145/147` exactly;
- Phase 9 validator;
- Phase 8 validator;
- governed example;
- blocked example;
- `git diff --check`;
- containment / byte-identity check for approved Phase 1–13 artifacts.

Do not repair Phase 10/11 inherited findings from Phase 14.

## Deliverable

After remediation, commit and push the exact remediation baseline on `spec/phase-14-implementation-specification`.

Do NOT create a PR.

Return sections A–R with:
- exact full remediation commit SHA;
- changed-file list;
- blocker-by-blocker closure evidence;
- exact derived inventory counts;
- validator totals;
- mutation totals;
- regression totals;
- harness credibility without overclaiming;
- remaining blockers;
- final verdict exactly one of:
  - `READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION RE-AUDIT V5`
  - `NOT READY — REMAINING BLOCKERS`

Do not claim human approval or production readiness.