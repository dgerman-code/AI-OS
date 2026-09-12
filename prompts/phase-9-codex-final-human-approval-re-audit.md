# Codex Prompt — Final Phase 9 Human-Approval Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Audit baseline commit: `0ec2c26e8a262d06bf841fb718944f4573dcfbab`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 9 APPROVED or CANONICAL.

This is the final human-approval re-audit after conformance cleanup. The prior audit returned `READY AFTER LISTED CHANGES`. The cleanup claims all listed changes are complete, all nine exemplars now conform to Candidate Universe requirements, active counts are internally consistent, stage numbering is fixed, the self-check is current, and the validator reports `270/270 PASS` with eight targeted failure injections.

Treat every producer claim as untrusted until independently verified.

Read at minimum:
- `architecture/model-registry-router.md`
- `models/_standards/common-model-governance-constraints.md`
- all five templates under `models/_templates/`
- `models/model-capability-taxonomy.md`
- `models/model-lifecycle-and-versioning.md`
- `models/routing-constraint-model.md`
- `models/routing-precedence-and-fallback.md`
- `models/review-diversity-and-criticality.md`
- `models/evaluation-evidence-model.md`
- `models/master-model-routing-universe.md`
- all nine `models/exemplars/*.md`
- `reviews/phase-9-foundation-self-check.md`
- `reviews/phase-9-foundation-audit-remediation.md`
- `validation/phase_9_validation.py`
- `validation/README.md`
- relevant approved Phase 6, Phase 7 and Phase 8 artifacts needed to verify review, decision-right, sensitivity and scope references.

## 1. Re-audit the final cleanup blockers

Verify all are fully resolved:

1. Routing Decision inventory/cardinality says 35 everywhere active and normative.
2. Capability family count is 23 everywhere active and normative.
3. Negative-evidence applicability says eight dimensions everywhere active and normative.
4. Every one of the 9 exemplars contains a complete Candidate Universe Definition with all mandatory elements.
5. Every exemplar candidate count matches the actually assessed candidate set.
6. Exemplar 4 is exactly 5 declared / 5 assessed.
7. Exemplar 1 uses stage 6 for policy preferences and stage 7 only for deterministic tie-break.
8. Exemplar 8 preserves the complete six-part reproducibility identity set.
9. Current self-check contains no stale totals, no scalar-sensitivity wording, and no stale stage numbering.
10. Validator detects the above defects if reintroduced.

Report unresolved cleanup count.

## 2. Full architecture sanity pass

Even if cleanup passes, independently confirm no architecture regression remains in:
- Model/Role separation;
- Model/Profile/Provider/Deployment identity;
- Routing Policy vs Routing Decision vs Decision Right;
- Router vs Orchestrator;
- Candidate Universe reproducibility;
- multi-label sensitivity / privacy / residency;
- requirement kinds: eligibility constraint / preference / routing act requirement;
- exceptionability and non-waivable handling;
- governed exception ordering;
- reviewer independence vs model diversity;
- lifecycle exclusivity;
- negative evidence applicability;
- anti-lock-in/versioning;
- cross-registry governance references.

Any material regression in these areas blocks approval.

## 3. Candidate Universe exemplar conformance

For each of the nine exemplars, verify all 9 mandatory Candidate Universe elements are present and semantically valid:
- registry state reference;
- universe definition version;
- inclusion rule;
- routing scope;
- pre-filter exclusions;
- enumerated candidate set;
- omission reasons;
- completeness result;
- behaviour if incomplete.

Also verify:
- availability does not silently pre-filter unless policy explicitly allows it;
- candidate enumeration count equals evaluated count;
- producing family / lifecycle / sensitivity failures are recorded as in-universe exclusions where the exemplar claims so;
- `CANDIDATE_UNIVERSE_INCOMPLETE` remains distinct from `NO_ELIGIBLE_MODEL`.

Return PASS/FAIL per exemplar.

## 4. Stage map

Verify the active stage map is consistent everywhere:
- Stage 0 — bind Candidate Universe;
- Stage 1 — legality/governance;
- Stage 2 — sensitivity/handling/residency;
- Stage 3 — capability/modality/context/tools;
- Stage 4 — independence/diversity;
- Stage 5 — lifecycle/availability;
- Stage 6 — Routing Policy-owned preferences;
- Stage 7 — deterministic tie-break;
- Stage 8 — routing act requirements / finalisation.

Report stage-number contradiction count.

## 5. Inventory / counts

Derive counts independently from authoritative sources and compare with every current active numerical claim.

Expected producer claims to verify, not assume:
- capability families = 23;
- eligibility constraints = 27;
- preferences = 9;
- routing act requirements = 3;
- primary lifecycle states = 6;
- evidence classes = 6;
- negative-evidence applicability dimensions = 8;
- common governance constraints = 45;
- templates = 5;
- exemplars = 9;
- Routing Decision elements = 35.

Historical audit counts may remain only if clearly labelled historical, not current.

Report active inventory inconsistency count.

## 6. Cross-registry integrity

Verify every active `decision.<id>` and `review.<id>` in Phase 9:
- resolves to an approved Phase 7 / Phase 6 object; OR
- is explicitly marked `FUTURE_GOVERNANCE_REFERENCE` and non-executable.

Exemplar 9 must still resolve `review.security`, `review.code`, and its cited approved Decision Rights, and must end in `NO_APPLICABLE_DECISION_RIGHT` + block/escalation rather than inventing authority.

Report unresolved executable governance-reference count.

## 7. Capability-reference integrity

Verify every active `capability.<id>` used in Phase 9 resolves to one of the declared 23 capability families.

Historical removal notes are permitted if clearly non-active.

Report undeclared active capability-reference count.

## 8. Self-check quality

Audit `reviews/phase-9-foundation-self-check.md` as an active current producer artifact.

Verify:
- current totals match actual validator output;
- current group counts match actual validator groups if stated;
- current Routing Decision count = 35;
- current governance constraints count = 45;
- current capability families = 23;
- sensitivity language is multi-label, not scalar ceiling;
- stage numbering is current;
- old 141/204/219/239 totals appear only as historical progression, never as current status;
- no contradictory summary language remains.

## 9. Validation harness

Run if possible:
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_9_validation.py --verbose`
- `python3 validation/phase_9_validation.py --json`
- `python3 validation/phase_8_validation.py`

Verify:
- exact Phase 9 total;
- all expected results pass;
- Phase 8 remains 119/119;
- no vacuous checks;
- current validator discovers exemplars dynamically;
- candidate-universe checks are per-exemplar and cannot pass merely because one exemplar is well-formed;
- candidate declared/evaluated mismatch is detected;
- stage 6/7 contradiction is detected;
- stale current self-check totals are detected;
- stale active normative counts are detected;
- seven-vs-eight evidence-dimension regression is detected;
- vacuous `or True`-style condition is detected;
- no local validator claims remote PR state.

If feasible, perform at least one controlled failure probe. Do not modify committed files permanently.

Return credibility HIGH / MEDIUM / LOW.

## 10. Nine exemplars

Audit all 9 independently and return PASS/FAIL with one concise reason each.

Approval requires all nine to PASS.

## 11. Open questions

Re-adjudicate all 17 Phase 9 questions.

Expected only if evidence supports it:
- 1–15 RESOLVED IN FOUNDATION;
- 16 PHASE 11+;
- 17 PHASE 10+.

Any authority/privacy/independence ambiguity still unresolved blocks approval.

## 12. Upstream / non-runtime regression

Compare against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`.

Require:
- Phase 3 Role changes = 0;
- Phase 4 Skill changes = 0;
- Phase 5 Workflow changes = 0;
- Phase 6 Handoff/Review changes = 0;
- Phase 7 Decision changes = 0;
- Phase 8 Knowledge/Canonical semantic changes = 0;
- `validation/phase_8_validation.py` unchanged in this cleanup;
- all Phase 9 artifacts remain PROPOSED;
- no runtime/SDK/API/secrets/DB/UI/RAG/agent/orchestrator implementation;
- no real vendor/model/provider/deployment profiles;
- no Phase 9 PR.

## 13. Approval threshold

Return `PASS` only if no material architecture or conformance issue remains.

Return `PASS WITH NON-BLOCKING NOTES` only if all remaining notes are genuinely Phase 10+/Phase 11+/runtime/card-population concerns and cannot cause identity, eligibility, privacy, authority, review-control, reproducibility or routing-conformance misuse.

Return `PASS WITH CHANGES` if another bounded Phase 9 correction is still required.

Return `FAIL` if any approval blocker remains or if the validator still gives materially false confidence.

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. FINAL CLEANUP RE-AUDIT
Each of the 10 cleanup blockers: RESOLVED / NOT RESOLVED.

### C. ARCHITECTURE SANITY
PASS / FAIL; material regression count.

### D. CANDIDATE UNIVERSE CONFORMANCE
PASS / FAIL; per-exemplar completeness and mismatch findings.

### E. STAGE MAP
PASS / FAIL; contradiction count.

### F. INVENTORY / COUNTS
PASS / FAIL; independently derived counts; inconsistency count.

### G. CROSS-REGISTRY / CAPABILITY INTEGRITY
PASS / FAIL; unresolved governance refs; undeclared capability refs.

### H. SELF-CHECK QUALITY
PASS / FAIL; stale-current-claim count.

### I. VALIDATION HARNESS
Exact commands/results; credibility HIGH / MEDIUM / LOW; failure-probe result; material coverage gaps if any.

### J. NINE EXEMPLARS
Each PASS / FAIL with one concise reason.

### K. OPEN QUESTIONS
All 17 independent dispositions.

### L. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–8 changes; Phase 9 status; runtime/profile/PR status.

### M. REMAINING BLOCKERS
If none: NONE.

### N. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 9
- READY AFTER LISTED CHANGES
- NOT READY

### O. EXPANSION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED MODEL/PROVIDER CARDING
- SAFE FOR CONTROLLED BATCH MODEL/PROVIDER CARDING
- SAFE FOR MASS MODEL/PROVIDER CARDING

Do not modify anything.