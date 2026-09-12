# Phase 11 — Claude Targeted Remediation Prompt: Negation Scope in Late Decision Staleness Validation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`

## Mode

TARGETED REMEDIATION ONLY.

Do not redesign Phase 11. Do not alter approved Phase 1–10 semantics. Do not add runtime, SQL, APIs, SDKs, queues, workers, schedulers, agents, secrets, credentials, IAM, Supabase deployment, RAG, or infrastructure. Do not create a PR.

All Phase 11 artifacts remain `PROPOSED`.

## Audit baseline and defect

The final human-approval re-audit of baseline:

`7b61d1125485b49f9d9f05282506f698b76367a4`

returned `FAIL` with exactly one remaining HIGH validator defect.

The committed architecture is correct. The validator's negation suppression is too broad.

This invalid sentence currently bypasses both stale-characterisation checks:

`The Decision Record stands and is not optional but is stale`

The problem is that `NEGATION_BEFORE` treats any nearby `not`, `never`, `neither`, `nor`, or `no longer` as negating the stale predicate, even when the negation grammatically belongs to another predicate.

The Phase-11-wide check also uses a line-wide denial suppression (`DENIAL_MARKER`) that can hide a later positive stale characterisation on the same line.

## Required semantic rule

A late Decision Record is an authority-bearing governed historical fact that occurred.

It:

- stands / is retained in governed history;
- may require `RECONCILE` and/or `ESCALATE` for current-state handling;
- may not use `IGNORE_AS_STALE`;
- may not be discarded, ignored, dropped, erased, voided, or characterised as stale itself.

The late-review asymmetry must remain intact:

- a late review result may use `IGNORE_AS_STALE`;
- it must remain recorded against its Review Instance.

## Required validator repair

Repair only the stale-characterisation validation logic so that negation suppresses a stale match **only when the negation is grammatically attached to the stale predicate itself**.

Examples that MUST PASS:

- `The Decision Record is not stale.`
- `The Decision Record was not stale.`
- `The Decision Record is never stale.` only if the validator can unambiguously treat `never` as directly modifying the stale predicate.
- unrelated prose about stale evidence elsewhere in Phase 11.
- late review `IGNORE_AS_STALE` while the result remains recorded against its Review Instance.

Examples that MUST FAIL:

- `The Decision Record stands and is not optional but is stale.`
- `The Decision Record is not optional and is stale.`
- `The Decision Record is not ignored but is stale.`
- `The Decision Record is neither optional nor revocable but is stale.`
- `The Decision Record is no longer pending but is stale.`
- `The Decision Record is never discarded, but is stale.`
- the same contrastive forms when inserted elsewhere in a Phase 11 artifact.

Do not implement a generic line-wide denial exemption. Remove or narrowly avoid any `DENIAL_MARKER` behavior for this specific rule if it can suppress a later positive stale predicate.

Prefer a bounded predicate-aware approach over larger NLP machinery. The repair must remain deterministic, standard-library-only and easy to audit.

## Self-check requirements

The validator must directly inspect the authoritative late-Decision race row and Phase-11-wide content as before.

Add explicit regression cases that distinguish:

1. **direct negation of stale** — should pass;
2. **unrelated earlier negation + later positive stale predicate** — must fail;
3. **late-review `IGNORE_AS_STALE`** — must remain allowed;
4. **stale evidence unrelated to a Decision Record** — must remain allowed.

The harness must fail if the negation logic is weakened back to proximity-based suppression.

## Controlled probes

Run all existing Phase 11 controlled probes plus, at minimum, these new probes individually and revert each mutation:

Negative probes — each must produce non-zero exit:

- authoritative row → `The Decision Record stands and is not optional but is stale`
- authoritative row → `The Decision Record is not ignored but is stale`
- authoritative row → `The Decision Record is neither optional nor revocable but is stale`
- authoritative row → `The Decision Record is no longer pending but is stale`
- authoritative row → `The Decision Record is never discarded, but is stale`
- Phase-11-wide insertion of at least two of the same contrastive forms

Positive controls — each must produce zero exit:

- `The Decision Record is not stale`
- retained/standing + `RECONCILE` and/or `ESCALATE`, with no stale characterisation
- stale evidence unrelated to a Decision Record
- late-review `IGNORE_AS_STALE`, still recorded against its Review Instance

Also rerun all previously required foundation and late-Decision probes.

## Validation

Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected inherited condition:

- Phase 10 remains `145/147` because of the already documented approval-record-only validator defect.
- Do NOT modify Phase 10 validator or `reviews/phase-10-final-approval.md`.

Phase 9 must remain `277/277 PASS`.
Phase 8 must remain `119/119 PASS`.

Update Phase 11 self-check totals if the validator test count changes.

## Regression boundary

Confirm no substantive Phase 1–10 architecture, approval record, or validator changes.

No Phase 11 architecture redesign. If architecture content is already correct, do not edit it merely to satisfy the validator.

No runtime/infrastructure implementation.

## Commit / push

Commit exactly:

`docs: remediate Phase 11 negation scope validation`

Push to:

`origin architecture/phase-11-orchestrator`

Do not create a PR.

## Required output

Return sections A–I exactly:

### A. REMEDIATION SUMMARY
State that this was a single-defect validator remediation and whether any architecture semantics changed.

### B. NEGATION-SCOPE RULE
Explain the precise rule: only negation attached to the stale predicate suppresses the stale characterisation.

### C. VALIDATOR REPAIR
Describe the implementation and how line-wide / proximity-based denial suppression was removed or narrowed.

### D. CONTROLLED PROBES
Report all new contrastive-negation probes, prior stale probes, foundation probes, and positive controls with exit behavior.

### E. VALIDATION
Report Phase 11 normal/verbose/json totals and Phase 10/9/8 results.

### F. REGRESSION
Confirm no Phase 1–10 semantic changes, no runtime/infrastructure, Phase 11 still PROPOSED, no PR.

### G. FILES CHANGED
List exactly the changed files and why.

### H. COMMIT / PUSH
Provide exact SHA, exact commit message, push status, local/remote HEAD equality, working-tree state.

### I. NEXT STEP
Return exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
