# Phase 14 — Targeted remediation: routing lifecycle, retry refusal, external-effect staging, audit nullability, assurance inventory

You are working in repository `dgerman-code/AI-OS` on branch `spec/phase-14-implementation-specification`.

This is a **targeted remediation pass** after independent re-audit V3 of exact Phase 14 baseline:

`5799aadbdbbcffb77545e655e3cbf44184fd0f35`

The V3 audit verdict was `FAIL / NOT READY — REMAINING BLOCKERS` with seven blockers. Close those blockers **without changing approved Phase 1–13 semantics**, without creating any new Decision Right, without changing blocked authorities BA-1…BA-4, and without introducing runtime code, migrations, DDL, provider SDKs, secrets, queues, workers, schedulers, IaC, or live integrations.

All Phase 14 artifacts must remain `PROPOSED`.

## Hard containment

Do not modify approved Phase 1–13 artifacts. The only permitted edits are under:

- `implementation-spec/`
- `validation/phase_14_validation.py`
- `validation/phase_14_mutation_probes.py`

Do not modify historical audit/approval records. Do not create a PR.

## Blocker 1 — Routing Request lifecycle contradiction

V3 found three incompatible statements:

- `RequestRouting` persists a Routing Request independently;
- `route()` also writes the Routing Request with the Routing Decision;
- M-13 says the Routing Request remains prospective until Router output fully validates, and malformed Router output leaves **no Routing Request**.

Choose one architecture-faithful lifecycle and make **every document** agree. Preserve Phase 11/12 semantics: caller must not be able to inject a Routing Decision; malformed Router output must not leave a committed decision-like artifact; validation-before-commit must hold.

The resulting contract must state precisely:

- whether `RequestRouting` creates a durable governed Routing Request or only a non-governed/prospective envelope;
- when the stable Routing Request identity becomes durable;
- what `route()` reads and writes;
- behavior when Router answer is invalid, incomplete, blocked, or no-eligible;
- exact governed writes and audit-event counts for every branch;
- whether a valid non-selection routing outcome still records the request and decision, and why;
- exact uniqueness/idempotency behavior.

Do not paper over this with prose aliases. The canonical API inventory and transaction table must encode one lifecycle.

## Blocker 2 — Retry class-4/class-6 refusal path

V3 found that O-20 requires forbidden class-4/class-6 retry to halt/escalate, while the transaction row says `Nothing written`.

Specify exact branch semantics for **every retry class**, especially non-retryable governed acts and unknown external-effect cases.

For each branch define:

- preconditions;
- run phase/posture before and after;
- exact governed records written;
- exact audit-event count;
- execution-event count;
- whether a retry-dispatch record exists;
- whether an escalation/block record exists;
- atomicity boundary;
- duplicate/idempotency behavior;
- prohibition on treating compensation as retry.

The transaction table must be branch-complete rather than giving one ambiguous row for `Retry`.

## Blocker 3 — `InvokeModel` versus mandatory outbox/external-effect protocol

V3 found that `InvokeModel` currently looks like one local transaction that writes Model Invocation + Model Result even though a model call is an external effect.

Reconcile this with the approved Phase 10/11 rules: no fake distributed transaction; unknown external effects stop and reconcile; outbox/staged intent; compensation is separate; exactly-once is not claimed.

Specify the external-effect state machine for model invocation. At minimum distinguish:

1. local intent/preparation commit;
2. external provider call;
3. observed provider response / timeout / unknown effect;
4. local result or uncertainty recording;
5. reconciliation path where external outcome is uncertain.

Define stable identities and linkage for invocation intent, provider attempt, Model Result, and any uncertainty/reconciliation record without collapsing them.

State exact transaction boundaries, writes, audit counts, retry classes, and what happens after crash at every boundary. A model timeout must never be treated as proof that no external effect occurred.

Do not claim distributed exactly-once or a distributed transaction.

## Blocker 4 — audit version nullability contradiction

The field-level Audit Event schema says `record_version_after` is always non-null, while the mutation-kind matrix correctly requires it `NULL` for `DESTROY`.

Make the **field table and matrix identical in semantics**. Explicitly specify conditional nullability for both `record_version_before` and `record_version_after` by mutation kind.

The schema prose, transaction model, test strategy, validator and probes must all use the same rule.

BA-3 remains blocked; defining DESTROY semantics must not make it executable.

## Blocker 5 — stale counts and stale structural descriptions

V3 found stale prose in `phase-14-self-check.md` describing:

- twenty uniqueness constraints instead of 21;
- eleven or seventeen governed acts instead of 35;
- thirty adversarial tests even though the inventory is now larger.

Remove stale numeric/word-form claims from **all Phase 14 documents**, not just the known lines.

Prefer derived language such as “the canonical U1–U21 inventory” or validator-derived counts where practical. Where a count is intentionally stated, it must be parsed/checked against the canonical inventory.

Search for both digits and English word forms (`twenty`, `eleven`, `seventeen`, `thirty`, etc.) and for stale ranges (`A1–A30`, `P1–P8`) that may be normative.

## Blocker 6 — M20 / G-R incomplete assurance gates

V3 found that M20 and G-R still require only old ranges A1–A30 and P1–P8 and therefore could allow completion without running the new remediation tests.

Create **canonical machine-readable/parseable assurance inventories** for:

- all adversarial cases;
- all positive controls;
- all cross-document invariant checks required for Phase 14 acceptance.

M20, G-R, the self-check and the validator must derive/verify the complete current inventory rather than hard-code a stale prefix range.

If test IDs are non-contiguous or have suffixes such as A12a/A12b, the inventory must support them exactly.

## Blocker 7 — validator hardening for localized/word-form drift

The independent audit mutated a localized milestone count and the validator still passed because another correct count survived elsewhere.

Harden the validator so that it checks **all normative count-bearing locations**, not “at least one correct occurrence”. It must detect:

- numeric drift (`20` vs `21`);
- word-form drift (`twenty` vs `twenty-one`, etc.) where normative prose states a count;
- stale command-count statements;
- stale adversarial/positive-control ranges;
- stale milestone/gate inventories.

Do not solve this by brittle global substring banning alone. Prefer parsing canonical tables/IDs and checking each normative reference against the derived value/set.

## Required new adversarial/mutation probes

Extend `validation/phase_14_mutation_probes.py` with load-bearing probes that independently weaken at least these cases:

1. persist Routing Request in both `RequestRouting` and `route()`;
2. allow malformed Router output to leave a committed request when the chosen lifecycle forbids that;
3. class-4 retry writes nothing instead of block/escalate;
4. class-6 unknown external effect automatically retries;
5. model invocation claims local atomicity across provider call;
6. timeout is treated as proof of no external effect;
7. `record_version_after` forced non-null for DESTROY;
8. stale uniqueness count written as digits in one normative gate;
9. stale uniqueness count written as words in one normative gate;
10. stale governed-act count in self-check/milestone;
11. M20 omits one current adversarial test ID;
12. G-R omits one positive control;
13. validator accepts an orphan assurance ID not present in canonical inventory.

Each probe must:

- mutate a real load-bearing target;
- fail loudly if the target cannot be found;
- be classified from execution;
- be detected by a named substantive check;
- not receive credit from containment/git-dependent failures.

Add more probes if needed.

## Cross-document exactness checks

At minimum the validator must now establish:

- canonical governed-command set == transaction-contract set;
- routing lifecycle statements in API, router contract, orchestrator contract and transaction model are compatible;
- retry-class branch semantics are represented in persistence and failure/recovery docs;
- external-effect/model-invocation staging is compatible across API, orchestrator, persistence, failure/recovery, audit and test strategy;
- U1–U21 canonical inventory == every normative uniqueness-count reference;
- canonical adversarial inventory == every normative assurance-gate requirement;
- canonical positive-control inventory == every normative assurance-gate requirement;
- Audit Event field nullability == mutation-kind matrix.

## BA-1 non-blocking note

V3 made one non-blocking note: BA-1 prose should explicitly cover governed downgrade of `APPROVED` material consistent with Phase 8. You may make this clarification **only if it does not create or map a new Right** and BA-1 remains fail-closed. Do not broaden scope beyond that clarification.

## Validation/regression

Run and report at least:

- `validation/phase_14_validation.py`
- `validation/phase_14_validation.py --verbose`
- `validation/phase_14_validation.py --json`
- `validation/phase_14_mutation_probes.py`
- Phase 12 full unit suite
- Phase 12 validator
- Phase 11 validator (preserve inherited 159/160 exactly; do not repair from Phase 14)
- Phase 10 validator (preserve inherited 145/147 exactly; do not repair from Phase 14)
- Phase 9 validator
- Phase 8 validator
- governed and blocked Phase 12 examples

Verify approved Phase 1–13 artifacts remain byte-identical to the Phase 13 approval state.

## Final report

Return sections A–R:

A. Remediation summary
B. Baseline / containment
C. Routing lifecycle remediation
D. Retry refusal branch remediation
E. Model invocation / external-effect staging
F. Audit version-nullability remediation
G. Canonical counts / inventory cleanup
H. Assurance-gate inventory remediation
I. Validator localized-drift hardening
J. Cross-document consistency
K. BA/open-items preservation
L. Validator / mutation hardening
M. Validation / regression results
N. Files changed
O. Known limitations
P. Harness credibility
Q. Remaining blockers
R. Readiness verdict

Do not claim `HIGH` harness credibility merely because checks increased. Do not declare production readiness.

Only if every V3 blocker is actually closed, end with exactly:

`READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION RE-AUDIT V4`

Otherwise end with:

`NOT READY — REMAINING BLOCKERS`
