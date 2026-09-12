# Phase 11 — Targeted remediation: late Decision Record stale wording

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`

## Objective
Perform a single-defect remediation only. Do not redesign Phase 11.

The final approval re-audit found one remaining HIGH validator gap: the structured late-Decision race validator rejects `IGNORE_AS_STALE`, discarded/ignored/dropped/erased/voided wording, and the phrase `treated as stale`, but it still allows a late Decision Record to be characterised directly as stale, e.g. `The Decision Record stands but is stale`.

## Required change
Update the Phase 11 validator so the authoritative late-Decision race row fails if the Decision Record itself is characterised as stale in any direct semantic form, including at minimum:

- `is stale`
- `was stale`
- `becomes stale`
- `considered stale`
- `deemed stale`
- `marked stale`
- `treated as stale`
- `stale Decision Record`

The rule is semantic and narrow:

- a late Decision Record remains a valid authority-bearing governed historical fact;
- it may require `RECONCILE` and/or `ESCALATE` for current-state handling;
- it may not be ignored or discarded;
- it may not itself be reclassified as stale merely because the execution state changed;
- preserve the intentional asymmetry with late review results, where `IGNORE_AS_STALE` remains correct while the review result stays recorded against its Review Instance.

Do not alter the authoritative architecture row unless the row itself is defective. The audit says committed architecture content is correct; this is a validator coverage defect.

## Validation hardening
The validator must inspect the authoritative late-Decision race row directly. Do not rely on positive prose elsewhere.

Add deterministic regression coverage for at least these cases:

1. exact audit bypass: `The Decision Record stands but is stale` -> MUST FAIL;
2. `The Decision Record was deemed stale` -> MUST FAIL;
3. `stale Decision Record` -> MUST FAIL;
4. prior `IGNORE_AS_STALE` + discarded mutation -> MUST FAIL;
5. `voided` -> MUST FAIL;
6. remove `RECONCILE`/`ESCALATE` -> MUST FAIL;
7. valid late Decision wording: record stands/retained + `RECONCILE` and/or `ESCALATE` -> MUST PASS;
8. late review retains `IGNORE_AS_STALE` and remains recorded against Review Instance -> MUST PASS.

Prefer a structure-aware or bounded semantic pattern over a fragile one-off string match. Be fail-closed without banning unrelated words `stale` elsewhere in Phase 11.

## Scope and regression constraints
- Preserve all approved Phase 1–10 semantics.
- Do not touch the Phase 10 validator or Phase 10 approval record.
- Keep Phase 11 artifacts `PROPOSED`.
- No runtime, queue, worker, scheduler, event bus, state-machine service, SQL, migrations, Supabase deployment, API, SDK, RAG, agents, credentials, IAM or secrets.
- No PR.

## Required validation
Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected inherited condition: Phase 10 remains `145/147` because of the already-documented approval-record-only validator defect. Do not remediate it here.

Run all prior controlled probes plus the new stale-characterisation probes. Every negative mutation must produce non-zero exit for the intended reason; valid controls must remain zero.

## Commit / push
Commit exactly:

`docs: remediate Phase 11 stale Decision wording validation`

Push to:

`origin architecture/phase-11-orchestrator`

Verify remote HEAD equals the new commit and worktree is clean.

## Return exactly these sections

### A. REMEDIATION SUMMARY
### B. STALE-CHARACTERISATION RULE
### C. VALIDATOR REPAIR
### D. CONTROLLED PROBES
### E. VALIDATION
### F. REGRESSION
### G. FILES CHANGED
### H. COMMIT / PUSH
### I. NEXT STEP

Section I must be exactly one of:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`

or

`NOT READY — REMAINING BLOCKERS`
