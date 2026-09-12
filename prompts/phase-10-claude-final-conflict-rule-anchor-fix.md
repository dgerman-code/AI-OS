# Phase 10 — Final targeted remediation: anchor conflict outcomes at cell start

Repository: `dgerman-code/AI-OS`

Branch: `architecture/phase-10-github-supabase-storage`

Current remediated architecture baseline under review: `157cdd337c988b383aff0421aefd7f183611ce19`

Latest independent approval re-audit result: **FAIL — READY AFTER LISTED CHANGES**.

This is a **single-defect targeted remediation**. Do not redesign Phase 10.

## The only blocker to fix

The normative architecture says each source-of-truth matrix conflict-rule cell must **begin with** one or more declared conflict outcome tokens.

The current validator `conflict_rule_contract()` is too permissive: it extracts a valid token anywhere in the cell. Therefore a cell can begin with prose explicitly denying that a conflict rule exists and still pass if a valid token such as `AUTHORITY_WINS` appears later only as an example.

The final approval re-audit demonstrated this bypass.

## Required fix

1. Update `validation/phase_10_validation.py` so conflict-rule parsing is **anchored at the beginning of the normalized cell content**.
2. Permit one or more leading declared outcome tokens only in the syntax already supported by the normative architecture.
3. After the leading token(s), explanatory prose may follow.
4. Reject cells where:
   - prose appears before the first declared outcome token;
   - a valid outcome token appears only later in prose;
   - the cell begins with an unknown token;
   - the cell is empty;
   - last-write-wins or any undeclared outcome is introduced.
5. Add the exact adversarial bypass demonstrated by the audit as a deterministic regression probe: a long opening sentence saying no conflict-resolution rule exists, followed later by a valid token such as `AUTHORITY_WINS` merely as an example. The probe MUST fail with non-zero exit for the intended check.
6. Preserve the existing source-of-truth semantics, 24-row matrix, six authority tokens, nine conflict outcomes, and all prior remediations.
7. If the stronger parser exposes any current Phase 10 text that violates the already-approved normative rule, correct only that conformance defect; do not introduce new semantics.

## Validation required

Run:

```bash
python3 validation/phase_10_validation.py
python3 validation/phase_10_validation.py --verbose
python3 validation/phase_10_validation.py --json
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Then run controlled failure probes proving at minimum:

- the new audit bypass fails;
- prose-before-token fails;
- valid leading token + prose passes;
- empty conflict cell fails;
- unknown leading token fails;
- last-write-wins fails;
- all previous authority and source-of-truth probes still fail as intended;
- vacuous `or True` still fails.

Do not target a predetermined validation total. Report the derived total after the new check(s).

## Regression boundaries

Do not modify approved Phase 3–9 semantics or `reviews/phase-9-final-approval.md`.

Do not introduce:
- live Supabase connectivity;
- SQL DDL or live migrations;
- tables, buckets, RLS policies, service accounts, credentials or secrets;
- API/SDK/runtime/RAG/agents/orchestration;
- real Model/Provider/Deployment profiles;
- new Decision Rights or authority semantics.

All Phase 10 artifacts remain `PROPOSED`.

Do not create a PR.

## Commit / push

Commit exactly:

`docs: anchor Phase 10 conflict-rule validation`

Push to:

`origin architecture/phase-10-github-supabase-storage`

Verify remote HEAD equals the new commit and the worktree is clean.

## Required response

Return sections A–H exactly:

### A. FIX SUMMARY
State exactly what changed and confirm this was single-defect remediation only.

### B. CONFLICT-RULE PARSER
Describe the anchored grammar and why the prior bypass is now impossible.

### C. CONTROLLED FAILURE PROBES
Show the exact adversarial audit bypass plus the other required probes and their non-zero outcomes.

### D. VALIDATION
Report Phase 10 default/verbose/json results plus Phase 9 and Phase 8 regressions.

### E. REGRESSION
Confirm no Phase 3–9 semantic changes, no runtime/live infrastructure, Phase 10 still PROPOSED.

### F. FILES CHANGED
List only files changed in this remediation and why.

### G. COMMIT / PUSH
Return exact SHA, exact commit message, remote verification, clean worktree, no PR.

### H. NEXT STEP
Return exactly one of:
- `READY FOR FINAL PHASE 10 HUMAN-APPROVAL RE-AUDIT`
- `NOT READY — <reason>`

Do not claim human approval.