# Phase 14 — Claude Redispatch, Fencing and Assurance Remediation

## Role
You are acting as the implementation-specification remediation engineer for AI-OS Phase 14.

This is a targeted remediation pass only. Do not redesign approved Phase 1–13 architecture. Do not add runtime code, DDL, migrations, SDK integrations, workers, queues, schedulers, secrets, IaC, or a PR.

## Repository / branch
Repository: `dgerman-code/AI-OS`
Branch: `spec/phase-14-implementation-specification`

## Exact remediation baseline
Audit/remediation target baseline:

`28d663203876c41cc264108b33c7ce91c61ab4ce`

The latest independent V6 audit returned `FAIL / NOT READY — REMAINING BLOCKERS` with six remaining blockers. Remediate only those blockers plus directly necessary validator/mutation coverage. Preserve all accepted prior remediation semantics.

## Non-negotiable containment
- Phase 1–13 approved artifacts must remain byte-identical.
- All Phase 14 specification artifacts remain `PROPOSED`.
- Create no Decision Right and map no new authority.
- BA-1…BA-4 and OI-1…OI-11 remain unchanged unless a wording correction is required to preserve the same meaning.
- Do not alter inherited Phase 10 `145/147` or Phase 11 `159/160` findings.
- Do not create a PR.

# V6 blockers to close

## 1. Redispatch after crossed external-call boundary has no executable transition path
The current spec allows conditional redispatch under PO-14 / PO-19 after `boundary_crossed=true` when either:
- a recorded provider deduplication guarantee makes retry safe; or
- reconciliation proves `CONFIRMED_NOT_APPLIED`.

But T1–T10 provide no token-fenced transition/ownership path that makes such an item dispatchable again.

### Required remediation
Choose one coherent design and encode it everywhere:

Preferred direction: preserve conditional redispatch but make it an explicit governed/operational state-machine path.

Define an explicit transition (or small explicit transition sequence) that:
- starts only from the exact crossed-boundary state(s) where redispatch has become proven safe;
- requires a durable recorded safe-precondition, never inference from timeout/absence;
- reacquires ownership with a new fencing generation/token;
- preserves the same stable provider idempotency key;
- makes the redispatchable state unambiguous;
- prevents any stale claimant from dispatching or settling;
- states exact before/after state, reads, predicates, writes, token requirements, redelivery permission, and reconciliation requirement;
- distinguishes the provider-dedup-guarantee path from the `CONFIRMED_NOT_APPLIED` reconciliation path if their evidence requirements differ.

If you instead remove conditional redispatch, then remove it consistently from PO-14, PO-19, failure/recovery prose, retry semantics, API, persistence, assurance, examples and tests. Do not leave dormant wording.

No path may ever interpret lease expiry, timeout, missing evidence or absence of a result as proof that the external effect did not occur.

## 2. Reconcile F-9a / F-9d / PO-8 with T6 and PO-14 / PO-19
Current active prose conflicts:
- F-9a says expired attempt lease is always unknown;
- T6 safely returns expired `CLAIMED`, `boundary_crossed=false` to `PENDING`;
- F-9d says `boundary_crossed=true` is never redispatched;
- PO-14/PO-19 permit conditional redispatch;
- PO-8 says `CLAIMED` is the only safely redispatchable state.

### Required remediation
Make the vocabulary precise:
- before boundary crossed: expired ownership may be recovered without asserting any external attempt;
- after boundary crossed: default is uncertainty/reconciliation, never optimistic replay;
- conditional redispatch after boundary is allowed only through the exact explicit safe transition designed under blocker 1;
- distinguish "safe initial dispatch/reclaim before call" from "safe redispatch after proof/dedup guarantee" so PO-8 cannot be read as contradicting later safe redispatch.

Every active location must agree.

## 3. Correct T10 exact state and ownership predicates
Current T10 permits `PENDING` or `CLAIMED` → `SETTLED` but does not require the exact source-state predicate and, for `CLAIMED`, current ownership / `claim_token`.

### Required remediation
Specify T10 as an exact transition contract:
- enumerate permitted source states separately if their predicates differ;
- if leaving `CLAIMED`, require current `claim_generation`, `claim_token`, claimant identity and any OCC/version predicate required by the protocol;
- stale claimant must update zero rows and cannot settle;
- if `PENDING` retirement is allowed without a claimant, explain the exact reason and predicate;
- do not use a single ambiguous row if two distinct transitions are clearer.

Add independent mutation coverage for stale-token settlement and wrong-source-state settlement.

## 4. O5 claims durable monotonic generation but is only `CHECK (claim_generation >= 0)`
That CHECK enforces non-negativity only; it does not enforce monotonic increase or non-reuse across updates.

### Required remediation
Do not claim a SQL CHECK enforces historical monotonicity.

Choose an honest classification:
- O5 may remain an ordinary row-level domain constraint enforcing only nonnegative generation; and
- monotonic increment / no token reuse must be an exact transition precondition enforced by CAS/OCC in every ownership-changing transition;

or define another implementable database mechanism if you can specify it without inventing unsupported runtime/DDL.

The prose, constraint table, transition table and validator must all state exactly what is actually enforceable. Never describe a row CHECK as a cross-version monotonic guarantee.

## 5. Remove active `O1–O4` / `O1–O5` contradiction
`api-command-contracts.md` currently contains both forms.

### Required remediation
Identify one canonical operational-constraint inventory and make every active reference match it. Historical prose must be clearly historical if retained and must not look current.

The validator must derive the inventory and reject any active second-location count/range drift.

## 6. Assurance must catch second-location semantic contradictions and blockquoted normative definitions
Independent V6 mutations detected only 5/14; 9 escaped. The validator also reports 373 normative IDs while independent derivation finds 374 because blockquoted Rule P-14a is missed.

### Required remediation
Harden assurance structurally, not by matching one preferred sentence.

At minimum add substantive checks and mutation probes for these escaped classes:
- B3 second-location statement drops required run-state append;
- B4n second-location statement drops inherited run-state consequence;
- B1r second-location statement consumes/increments the ordinal;
- stale/concurrent writer prose weakens fencing or allows same generation/token reuse;
- provider idempotency key is regenerated in an active second location;
- outbox is reclassified as governed in an active second location;
- refusal observational equality is expanded to total execution-event equality;
- stale command/transaction counts appear in active non-canonical prose;
- unknown external effect auto-redispatches without the explicit safe precondition;
- blockquoted normative rule definitions are included in rule-ID derivation.

The validator must:
- parse active prose across all Phase 14 documents, not only canonical tables;
- distinguish historical/deprecated text only through explicit bounded markers, not nearby wording accidents;
- derive normative rule IDs including blockquotes;
- reject duplicate definitions and unresolved references;
- compare second-location routing/retry/outbox assertions against their owning canonical contracts;
- fail if an active narrative weakens an invariant even when the canonical table is correct.

Add controlled mutation probes for every escaped V6 class and prove they are detected by named substantive checks, not containment/git-dependent checks.

# Additional consistency requirements

## External-effect safety vocabulary
Keep these concepts non-substitutable:
- ownership/lease expiry;
- fencing generation/token;
- provider idempotency key;
- provider-side deduplication guarantee;
- local `boundary_crossed` state;
- observed provider outcome;
- reconciliation result;
- permission to redispatch.

One must not imply another.

## No false exactly-once claim
The design may use at-least-once delivery with idempotency/fencing, but must not assert distributed exactly-once or distributed transactions.

## Operational vs governed
The outbox remains operational unless you explicitly justify and consistently change the classification everywhere. Do not accidentally create audit events for operational claim transitions while keeping prior governance semantics elsewhere.

# Required validation / regression
Run and report:
- Phase 14 validator default / `--verbose` / `--json`;
- Phase 14 mutation probes;
- Phase 12 unit suite;
- Phase 12 validator;
- Phase 11 validator;
- Phase 10 validator;
- Phase 9 validator;
- Phase 8 validator;
- governed example;
- blocked example;
- `git diff --check`;
- containment verification against Phase 13 approval baseline `2c4b90def9a60f8b384feef10f8428c5b437597c`.

Record inherited Phase 10/11 failures exactly and do not repair them.

# Commit requirement
When all six V6 blockers are closed and regressions pass:
- commit the remediation;
- push `spec/phase-14-implementation-specification`;
- do not create a PR.

Use a concise commit message such as:

`docs: close Phase 14 redispatch fencing and assurance blockers`

Return the exact full remediation commit SHA.

# Required report
Return sections A–R:

A. Remediation summary
B. Baseline / containment
C. Crossed-boundary redispatch model
D. Failure/recovery vocabulary reconciliation
E. T10 / settlement fencing
F. O5 enforceability correction
G. Operational-constraint inventory reconciliation
H. Cross-document assurance hardening
I. Rule-ID parsing / blockquote coverage
J. External-effect safety invariants
K. Audit / provenance consistency
L. Validator / mutation hardening
M. Regression results
N. Files changed
O. Known limitations
P. Harness credibility
Q. Remaining blockers
R. Readiness verdict

Only if every blocker is actually closed, use the exact final readiness line:

`READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION RE-AUDIT V7`

Otherwise return `NOT READY — REMAINING BLOCKERS` and list them precisely.
