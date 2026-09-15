# Phase 14 Targeted Remediation — V7 Blockers B1/B2

Repository: `dgerman-code/AI-OS`
Branch: `spec/phase-14-implementation-specification`

## Purpose

Apply one **targeted remediation only** for the two HIGH blockers returned by the independent Phase 14 V7 re-audit of exact architecture baseline:

`46a7a891727a5ee3a3c3e90c83ef7d0d7531c33c`

The later V7 audit-prompt commit is prompt-only and is not the architecture baseline.

Do not redesign Phase 14. Do not reopen already-passing areas. Do not touch approved Phase 1–13 artifacts. Do not modify Phase 14 scope beyond what is necessary to close B1 and B2 plus directly related second-location contradictions and assurance coverage.

Do not create a PR.

## Independent audit findings to close

### B1 — HIGH: contradictory external delivery / replay contract

The active contract currently contains contradictory statements:

- `implementation-spec/api-command-contracts.md` Q-26 claims external **at-least-once** delivery where the provider deduplicates;
- `implementation-spec/persistence-and-transaction-model.md` PO-17 explicitly defines an **at-most-once-per-dispatch-item** guarantee across the external-effect boundary;
- conditional redispatch wording survives in active Q-24, T5/T7 summaries, §9.6 and possibly other second locations.

The intended architecture is already established and must be made consistent everywhere:

1. A dispatch item / dispatch key that may have crossed the provider boundary is **never redispatched as the same dispatch item/key**.
2. Provider idempotency / deduplication is defence-in-depth only; it does **not** license same-item crossed-boundary replay.
3. `UNKNOWN` / ambiguous external effect requires reconciliation, never blind replay.
4. After `CONFIRMED_NOT_APPLIED`, continuation is a **new governed provider attempt** with a new attempt identity, new dispatch item identity, and new provider idempotency key, linked to prior lineage.
5. The Phase 14 guarantee must be described consistently as **at-most-once dispatch per dispatch item/key**. Do not claim end-to-end exactly-once or external at-least-once delivery.
6. Reconciliation may determine no effect occurred and permit a new governed attempt; that is not redispatch of the old item.

### B2 — HIGH: governed writes assigned to a no-governed-write retry class

The active contract currently assigns `SAFE_AUTOMATIC_RETRY` to stages 1/3/4/5 even though those commands explicitly write governed records.

This contradicts the approved Phase 11 definition of that class: **no governed record is written**.

Do not widen or redefine the approved class.

Remediate by making retry classification compatible with approved Phase 11 semantics:

1. Identify every affected Stage 1/3/4/5 command and its actual governed writes.
2. Do not classify any command that writes governed records as `SAFE_AUTOMATIC_RETRY`.
3. Use the already-approved retry classes / semantics that fit durable governed-write commands, including durable request identity / deduplication / replay-safe command handling where appropriate.
4. Preserve deterministic command identity and durable deduplication so client/network retry does not duplicate governed records.
5. Distinguish **re-executing a command handler safely because the prior governed write is durably deduplicated** from the Phase 11 class `SAFE_AUTOMATIC_RETRY`.
6. Do not equate “not authority-bearing” with “not governed.”
7. Keep refusal / wait / escalation behavior fail-closed where the retry class or prior outcome cannot be established.

## Required exhaustive consistency sweep

Do not patch only the two cited lines.

After remediation, sweep all active Phase 14 documents for semantic second locations of both blocker families.

### B1 sweep terms / concepts

Search conceptually for all active statements involving:

- at-least-once;
- at-most-once;
- exactly-once;
- redispatch / replay / retry after external dispatch;
- provider deduplication / idempotency;
- unknown external effect;
- `CONFIRMED_NOT_APPLIED`;
- same dispatch item / same key;
- new provider attempt / new identity / new key;
- T5 / T7 / T10 / T11;
- Q-24 / Q-26;
- PO-8 / PO-14 / PO-14a / PO-14b / PO-17 / PO-19;
- crash / recovery summaries.

Every active location must agree with the owner contract.

### B2 sweep terms / concepts

Search conceptually for all active statements involving:

- `SAFE_AUTOMATIC_RETRY`;
- governed writes;
- request / decision / review / knowledge / scope / audit records;
- stages 1/3/4/5;
- retry class tables;
- API command retries;
- orchestrator retry handling;
- durable deduplication / command identity;
- “safe”, “automatic”, “idempotent”, “replay-safe”, “network retry”.

No active statement may imply that a governed-write command belongs to a class whose contract says no governed record is written.

## Hard boundaries

- Do not modify approved Phase 1–13 artifacts.
- Do not rewrite approved Phase 11 retry-class definitions.
- Do not modify Phase 15 or the Communication Specialist package.
- Do not create or approve Decision Rights.
- Do not infer human approval.
- Do not claim production/runtime readiness.
- Keep all Phase 14 implementation-spec artifacts `PROPOSED`.
- Do not introduce runtime code, migrations, infrastructure, provider integrations or secrets.
- Do not create a PR.

## Assurance changes

Update the Phase 14 validator / mutation fixture only as necessary to make these two blocker families observable in **second locations**, not just owner definitions.

At minimum add adversarial probes that fail when:

1. Q-26 reintroduces external at-least-once delivery;
2. Q-24 conditionally permits same-item crossed-boundary redispatch;
3. T5 or T7 reintroduces conditional redispatch of the old dispatch item/key;
4. a crash/recovery summary says provider dedup permits crossed-item replay;
5. `CONFIRMED_NOT_APPLIED` continuation reuses the old identity/key;
6. a Stage 1/3/4/5 governed-write command is labelled `SAFE_AUTOMATIC_RETRY`;
7. a second-location table classifies any governed-write command as no-governed-write retry;
8. prose equates “not authority-bearing” with “safe automatic retry”.

Avoid checks that pass merely because a corrective rule exists somewhere else. Validate the active local statement / row / classification being weakened.

## Regression checks

Run and report:

- `python3 validation/phase_14_validation.py`
- `python3 validation/phase_14_validation.py --verbose`
- `python3 validation/phase_14_validation.py --json`
- `python3 validation/phase_14_mutation_probes.py --json`
- Phase 12 unit suite
- Phase 12 validator
- Phase 11 validator
- Phase 10 validator
- Phase 9 validator
- Phase 8 validator
- governed example
- blocked example
- `git diff --check`

Preserve inherited Phase 10/11 findings as inherited. Do not repair them here.

## Manual closure checklist

Before committing, verify all of the following against active text, not only validators:

### B1

- Q-24 agrees with PO-17;
- Q-26 agrees with PO-17;
- T5/T7 summaries agree with PO-17;
- §9.6 and crash/recovery prose agree with PO-17;
- same crossed dispatch item/key is never redispatched;
- provider dedup does not license replay;
- unknown effect reconciles;
- `CONFIRMED_NOT_APPLIED` creates a new governed attempt / identity / key;
- no active external at-least-once or exactly-once guarantee survives.

### B2

- Stages 1/3/4/5 are classified according to actual governed-write behavior;
- no governed-write command is `SAFE_AUTOMATIC_RETRY`;
- approved Phase 11 class semantics are unchanged;
- durable request identity / deduplication semantics are explicit for replay-safe client/network retry;
- all second-location retry tables/prose agree.

## Commit

If and only if both blockers are closed and regressions pass, commit the remediation to the same branch.

Do not create a PR.

## Required report

Return exactly:

A. SUMMARY
B. STARTING BASELINE / BRANCH HEAD / FINAL SHA
C. CHANGED FILES
D. B1 — EXTERNAL DELIVERY / REPLAY CLOSURE
E. B1 — EXHAUSTIVE SECOND-LOCATION SWEEP
F. B2 — RETRY CLASSIFICATION CLOSURE
G. B2 — EXHAUSTIVE SECOND-LOCATION SWEEP
H. ASSURANCE CHANGES
I. VALIDATION / MUTATION RESULTS
J. REGRESSION RESULTS
K. CONTAINMENT
L. REMAINING BLOCKERS
M. VERDICT

The only acceptable positive final line is:

`READY FOR SHORT INDEPENDENT PHASE 14 B1/B2 CLOSURE REVIEW`

Do not claim Phase 14 approval readiness yet.