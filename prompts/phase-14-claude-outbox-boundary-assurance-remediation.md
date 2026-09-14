# Phase 14 — Claude targeted remediation after independent re-audit V5

Repository: `dgerman-code/AI-OS`
Branch: `spec/phase-14-implementation-specification`
Audited baseline that failed V5: `34a360d384ca8565048eac1dcc3e626d58c443f9`

## Mission

Remediate only the seven blockers identified by the independent V5 re-audit. Preserve all approved Phase 1–13 semantics, all Phase 14 PROPOSED status, all blocked authorities BA-1…BA-4, all open items OI-1…OI-11, and all inherited Phase 10/11 findings. Do not create or map any new Decision Right. Do not create runtime, DDL, migrations, provider SDK integrations, workers, queues, schedulers, secrets, IaC, or a PR.

This is specification + validator remediation only.

## Required blockers to close

### 1. External-call/outbox boundary must be crash-safe

Current V5 finding: `CLAIMED` means no call has occurred, `DISPATCHED` means the call has occurred, but no DB transition can be atomic with the external provider call. A crash after the provider call but before persisting `DISPATCHED` can leave an expired `CLAIMED` item that the current contract may re-dispatch.

Define an implementable state machine that does not infer non-occurrence from local state after an external-call boundary. You may introduce an explicit pre-call dispatch-intent / uncertain boundary state if needed, but do not invent vendor-specific machinery. Preserve the principle that timeout, connection reset, crash, or ambiguous provider response never proves no external effect.

Mandatory properties:
- stable `outbox_ref`, `model_invocation_ref`, `provider_attempt_ref`, provider idempotency key;
- no state that is considered safely re-dispatchable after the system could already have crossed the provider-call boundary unless receiver deduplication is guaranteed;
- every transition has a clear precondition and resulting state;
- crash points before call, at call boundary, after provider acceptance but before local persistence, after outcome persistence, and during reconciliation are all defined;
- successful stage 3/4 persistence must settle the operational dispatch/outbox state consistently;
- no distributed transaction and no exactly-once claim.

### 2. Replace invalid/redundant O4 with an implementable lease/concurrency mechanism

The V5 audit correctly notes that a PostgreSQL partial unique predicate using `lease_expires_at > now()` is not implementable as stated, and that uniqueness on `outbox_ref` is redundant with O1.

Redesign O1–O4 (or equivalent) so they are implementable with ordinary durable columns/constraints plus an atomic compare-and-swap or OCC predicate. The contract must guarantee at most one active claimant/lease owner according to the state row itself, without a time-dependent partial-index predicate.

Specify:
- claim owner service identity;
- lease/claim token;
- lease expiry semantics;
- OCC/fencing token or monotonic claim generation;
- exact atomic predicate for acquisition/renewal/reclaim;
- stale-owner write rejection;
- deterministic expired-claim recovery.

### 3. Specify every token-fenced outbox transition

V5 found only initial `PENDING → CLAIMED` to be precise. Make every transition implementable and token-fenced, including at minimum:
- pending/unclaimed → claimed;
- claimed → pre-call/dispatch-intent state if one is introduced;
- claim renewal where permitted;
- external-call boundary handling;
- observed-success / observed-failure / unknown-effect transitions;
- settlement;
- abandonment;
- expired-claim recovery/reclaim;
- reconciliation.

For each transition state exact reads, predicates, writes, fencing/claim token requirements, whether redispatch is allowed, and whether provider reconciliation is mandatory.

Bind stage 3/4 success to an exact operational transition to `SETTLED` (or equivalent terminal dispatch state).

### 4. Repair duplicate normative rule ID

There are two active `P-23` rules. Assign unique normative IDs and update every cross-reference. Add validator coverage for duplicate normative rule IDs across the active Phase 14 package, not only this specific number.

### 5. Remove stale routing/refusal prose everywhere active

Repair all active contradictions noted by V5:
- self-check prose that still describes only four routing branches and stale B3/B4 cardinalities;
- any router-contract phrase like “blocks or escalates” where the current contract is deterministically `BLOCKED` then `ESCALATED`;
- `implementation-sequencing.md` statement that a refused route leaves “no request and no event”; the required refusal execution event must remain visible and remain non-governance evidence.

Do not merely fix named lines. Search all active Phase 14 normative prose for logically equivalent stale forms.

### 6. Repair assurance-gate manifests

V5 says milestone gates omit remediation tests. Update the governing milestone / approval-gate manifests so every applicable current remediation test and positive control is required, including at least A48–A55 and P-A49 where they belong.

The manifest must derive from canonical assurance inventories rather than a stale hard-coded contiguous range. Suffixed IDs and non-contiguous IDs must remain supported. Orphan and missing IDs must fail.

### 7. Harden cross-document assurance against the six demonstrated escapes

The independent V5 nearby mutations that escaped were:
1. B3 missing run-state append in a nearby normative API location;
2. B4n missing inherited consequence in a nearby normative API location;
3. B1r advancing ordinal in nearby normative API prose;
4. refusal requiring equal total execution-event count in nearby assurance prose;
5. `RequestRouting` presented as current in nearby historical/current narrative;
6. unknown-effect retry automatically redispatching in a nearby Q31-like location.

Add substantive checks that derive/compare semantics across all active normative locations, not one canonical sentence. Add controlled mutation probes for each exact class of escape. The validator must reject contradictory duplicate normative prose even when the canonical table is still correct.

## Additional consistency requirements

- Routing B1/B1r/B2/B3/B4s/B4n semantics remain unchanged unless necessary to remove contradiction.
- Retry branch semantics remain unchanged unless necessary for consistency.
- Outbox rows remain operational, not governed, unless you can demonstrate a compelling approved-architecture reason otherwise. Prefer preserving the current Phase 10/11 classification.
- Execution/refusal events remain non-governance evidence and cannot satisfy gates, approval, authority, or progress.
- Preserve local governed-record one-audit-event-per-governed-mutation semantics.
- Preserve no distributed exactly-once claim.
- Preserve provider/runtime independence.
- Do not promote any Phase 14 artifact from PROPOSED.

## Validation requirements

After remediation, run and report:
- Phase 14 validator default, `--verbose`, and `--json`;
- Phase 14 mutation probes;
- Phase 12 unit suite;
- Phase 12 validator;
- Phase 11 validator, preserving inherited finding exactly;
- Phase 10 validator, preserving inherited findings exactly;
- Phase 9 validator;
- Phase 8 validator;
- governed example;
- blocked example;
- `git diff --check`;
- containment / byte-identity check for approved Phase 1–13 artifacts.

Add validator/probe coverage for:
- impossible time-dependent partial index returning;
- redundant lease uniqueness that cannot enforce active ownership;
- crash after provider call but before local post-call state persistence;
- stale claim token attempting settlement;
- reclaim that treats expired claim as proof no call occurred;
- missing settlement transition after successful stage 3/4 commit;
- duplicate normative rule IDs;
- stale routing cardinality prose;
- stale `RequestRouting` current-membership prose;
- stale refusal-event equality prose;
- unknown-effect auto-redispatch in any active normative location;
- incomplete milestone assurance manifests.

Every probe must be DETECTED by a named substantive check. Git-dependent failures do not count. Missing mutation targets must fail loudly.

## Commit / push

If and only if all required remediation and regressions pass:
- commit all remediation changes;
- push `spec/phase-14-implementation-specification`;
- do not create a PR.

Recommended commit message:
`docs: close Phase 14 outbox boundary and assurance blockers`

## Required report format

Return sections A–R:
A. Remediation summary
B. Baseline / containment
C. External-call boundary remediation
D. Lease / claim concurrency remediation
E. Token-fenced transition model
F. Rule-ID repair
G. Routing/refusal stale-prose cleanup
H. Assurance-gate manifest remediation
I. Cross-document validator hardening
J. Routing / retry consistency
K. Audit / provenance consistency
L. Validator / mutation results
M. Regression results
N. Files changed
O. Known limitations
P. Harness credibility
Q. Remaining blockers
R. Readiness verdict

If blockers remain, say so. Do not claim readiness unless Q = NONE.
