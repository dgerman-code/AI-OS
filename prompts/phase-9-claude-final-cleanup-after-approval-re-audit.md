# Claude Code Prompt — Final Phase 9 Cleanup After Approval Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Audited content baseline: `4ffbcc79109ea140385841fc62c41798d8ee6566`
Prompt-only branch HEAD at audit time: `e3c2793c9a7042a8a746974c1c08bc95b111f476`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

The final approval re-audit returned `FAIL`, but all deep architecture blockers are resolved. Remaining issues are bounded consistency/conformance/validation defects.

This pass must fix **only** the listed remaining blockers. Do not redesign Phase 9.

Do NOT modify approved Phase 3–8 semantics.
Do NOT implement runtime, SDKs, APIs, DB, UI, RAG, agents, orchestrator, telemetry or storage.
Do NOT create real provider/model/deployment cards.
Do NOT create a PR.
Keep all Phase 9 artifacts `PROPOSED`.

## 1. Fix all active normative counts and cardinalities

The audit found these active normative defects:
- Routing Decision inventory says 31 but actual template has 35 elements;
- active prose says 24 capability dimensions/families where actual declared capability families are 23;
- negative-evidence applicability prose says seven dimensions while the table lists eight;
- current common constraints count is 45;
- verify all related active counts against authoritative tables rather than hand-maintained numbers.

Required current derived counts:
- capability families: 23;
- eligibility constraints: 27;
- preferences: 9;
- routing act requirements: 3;
- primary lifecycle states: 6;
- evidence classes: 6;
- negative-evidence applicability dimensions: 8;
- common constraints: 45;
- templates: 5;
- exemplars: 9;
- Routing Decision elements: 35.

Search all active Phase 9 normative files and review/self-check files for stale numbers. Historical remediation notes may preserve prior counts only when clearly historical/non-normative and not presented as current.

## 2. Bring all nine exemplars into Candidate Universe conformance

The Candidate Universe Definition is mandatory before filtering/ranking. Every exemplar must include all mandatory universe elements, not a partial prose approximation.

For each exemplar, include explicitly:
- deterministic registry-state/snapshot reference;
- Candidate Universe Definition version/reference;
- inclusion/enumeration rule;
- routing scope;
- explicit pre-filter exclusions (or `NONE` with reason);
- enumerated candidate set;
- omission reasons (or `NONE`);
- completeness result;
- policy behavior if completeness fails.

Specific defects to fix:
- Exemplars 2, 3, 8: add full Candidate Universe Definition;
- Exemplars 1, 4, 5, 6, 7, 9: complete all missing mandatory universe fields;
- Exemplar 4: resolve the 4-versus-5 contradiction so declared candidate count exactly matches assessed candidates;
- availability must remain an evaluated candidate property, not a reason to disappear from the universe;
- exemplar 8 historical decision must preserve the complete six-part reproducibility identity set where the decision format requires it.

Do not invent vendor facts. Synthetic IDs remain synthetic.

## 3. Fix stage numbering contradiction

Normative architecture defines:
- stages 1–5 = fixed eligibility filtering;
- stage 6 = Routing Policy-owned lexicographic preferences;
- stage 7 = deterministic tie-break after preferences.

Fix Exemplar 1 and any current self-check text that still says cost preference occurs at stage 7.

Cost/latency preference belongs to stage 6 when it is a preference.
Stage 7 is only deterministic tie-break after stage-6 preference evaluation.

Search all active Phase 9 files for contradictory stage numbering.

## 4. Clean the producer self-check

The audit found 14 stale numerical claims and scalar-sensitivity wording in the current producer self-check.

Update `reviews/phase-9-foundation-self-check.md` so it describes the current architecture only.

Requirements:
- current validation count only;
- current group totals only;
- 35 Routing Decision elements;
- 45 common constraints;
- 23 capability families;
- no stale 24-family wording;
- no stale 141/141, 204/204 or other prior-pass totals presented as current;
- no scalar `maximum sensitivity` language;
- stage 6/7 numbering correct;
- Candidate Universe mandatory fields accurately represented.

Historical audit/remediation records may preserve prior results as history; the current self-check must not.

## 5. Fix negative-evidence dimension count

In `models/evaluation-evidence-model.md` and anywhere else active:
- the applicability model has exactly 8 dimensions;
- prose and table must agree;
- validator must derive/verify the count from the authoritative table.

## 6. Strengthen validation harness so these defects fail

Current 239/239 PASS gave false confidence on conformance it claimed to cover.

Strengthen `validation/phase_9_validation.py` to detect at minimum:

### Inventory/count consistency
- derive Routing Decision element count from numbered template rows and assert every current active inventory/self-check claim agrees;
- derive capability family count from taxonomy and assert every current active count claim agrees;
- derive negative-evidence dimension count from its authoritative table and assert prose/count claims agree;
- derive common-constraint count from headings/table and assert active inventory/self-check claims agree;
- derive exemplar count and template count;
- scan both digit and word-form numeric claims where relevant;
- include current producer self-check in consistency scans instead of excluding it.

### Candidate Universe exemplar conformance
For every exemplar, require all mandatory Candidate Universe elements:
- snapshot/state reference;
- definition version/reference;
- inclusion rule;
- routing scope;
- pre-filter exclusions;
- enumerated set;
- omission reasons;
- completeness result;
- incomplete-universe behavior.

Require declared candidate cardinality to equal evaluated candidate cardinality.
This must catch Exemplar 4-style 4-versus-5 mismatches.

### Stage numbering
- assert normative stage map: 1–5 fixed filtering, 6 preferences, 7 tie-break;
- detect any exemplar/self-check claim putting cost preference at stage 7.

### Scalar sensitivity language
- continue scanning normative files;
- also scan current producer self-check for active scalar ceiling/maximum/at-or-above logic.

### Routing Decision historical conformance
- for exemplar 8 or any exemplar representing a historical Routing Decision, verify the six-part reproducibility set is represented where applicable.

### Existing checks must remain
Preserve:
- cross-registry governance ID resolution;
- Model Profile identity/version consistency;
- undeclared capability reference checks;
- no runtime implementation;
- Phase 3–8 regression = 0;
- all Phase 9 artifacts PROPOSED;
- local validator does not claim remote PR state.

Do not keep 239 cosmetically. Report the actual resulting deterministic count.

Run:
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_9_validation.py --verbose`
- `python3 validation/phase_9_validation.py --json`
- controlled failure injection if supported;
- `python3 validation/phase_8_validation.py`

Phase 8 must remain `119/119 PASS` and unchanged.

## 7. Re-audit all nine exemplars after edits

Each must be PASS against the final Phase 9 architecture.

Explicitly verify:
1. Routine drafting — full Candidate Universe + cost at stage 6;
2. High-criticality reasoning — full Candidate Universe;
3. Independent assurance — full Candidate Universe;
4. Privacy-restricted deployment — candidate cardinality exact and full universe;
5. Vision — full universe and non-waivable modality rule;
6. Outage — unavailable candidate remains enumerated;
7. No eligible model — full universe and compound labels;
8. Deprecated model — full universe and six-part historical identity set;
9. Governance gap — full universe, approved review refs only, `NO_APPLICABLE_DECISION_RIGHT`, block/escalate.

## 8. Update remediation/self-check evidence

Update existing Phase 9 remediation/self-check documentation to record this final cleanup accurately.
Do not rewrite historical audit verdicts.

State clearly:
- this pass fixes conformance/count/validation defects only;
- no new governance semantics introduced;
- Phase 9 remains PROPOSED;
- human approval is still pending final re-audit.

## 9. Regression boundary

Prove against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`:
- Phase 3 changes = 0;
- Phase 4 = 0;
- Phase 5 = 0;
- Phase 6 = 0;
- Phase 7 = 0;
- Phase 8 Knowledge/Canonical semantics = 0;
- Phase 8 validator unchanged in this pass;
- no runtime implementation;
- no real model/provider/deployment profiles;
- no PR.

## 10. Commit / push

If and only if all checks pass, commit exactly:

`docs: finalize Phase 9 conformance after approval re-audit`

Push to:

`origin architecture/phase-9-model-registry-router`

Do not create a PR.

# Required final output

Return exactly:

### A. CLEANUP SUMMARY
Each remaining blocker and status.

### B. INVENTORY / COUNTS
All final derived counts and inconsistency count.

### C. CANDIDATE UNIVERSE CONFORMANCE
Nine exemplars and mandatory-universe compliance.

### D. STAGE NUMBERING
Final 1–7 map and contradiction count.

### E. SELF-CHECK CLEANUP
Stale claims removed and current values.

### F. VALIDATION
Exact commands/results, deterministic total, injected failure result, Phase 8 result, credibility self-assessment.

### G. NINE EXEMPLARS
Each PASS/FAIL with one concise reason.

### H. REGRESSION
Phase 3–8 changes, Phase 9 status, runtime/profile/PR status.

### I. FILES CHANGED
Exact files and purpose.

### J. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, clean-tree status.

### K. NEXT STEP
Choose exactly one:
- READY FOR FINAL PHASE 9 HUMAN-APPROVAL RE-AUDIT
- NOT READY

Do not claim Phase 9 approval.