# Codex Prompt — Final Phase 9 Approval Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Final remediation baseline: `4ffbcc79109ea140385841fc62c41798d8ee6566`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 9 APPROVED or CANONICAL.

This is the final approval-readiness audit for Phase 9 — Model Registry / Router.

Two independent audit rounds previously returned FAIL. The current remediation baseline claims that all remaining blockers are resolved, the Phase 9 deterministic validation harness reports `239/239 PASS`, Phase 8 remains `119/119 PASS`, and Phase 9 is `READY FOR FINAL PHASE 9 APPROVAL RE-AUDIT`.

Treat every producer/remediation claim as untrusted until independently verified.

Read at minimum:
- `architecture/model-registry-router.md`
- `models/_standards/common-model-governance-constraints.md`
- all files under `models/_templates/`
- `models/model-capability-taxonomy.md`
- `models/model-lifecycle-and-versioning.md`
- `models/routing-constraint-model.md`
- `models/routing-precedence-and-fallback.md`
- `models/review-diversity-and-criticality.md`
- `models/evaluation-evidence-model.md`
- `models/master-model-routing-universe.md`
- all `models/exemplars/*.md`
- `reviews/phase-9-foundation-self-check.md`
- `reviews/phase-9-foundation-audit-remediation.md`
- `validation/phase_9_validation.py`
- `validation/README.md`
- relevant approved Phase 3–8 registry artifacts needed to resolve cross-registry IDs.

---

## 1. Re-audit the final five blockers from the previous audit

### 1.1 Underlying Model Release vs Registry Profile Version

Verify there is now exactly one coherent rule everywhere normative:

- one Model Profile identity is bound to one underlying model release;
- Registry Profile Version versions the AI-OS record about that same underlying release;
- metadata/evidence corrections may increment Registry Profile Version without changing Model Profile identity;
- deployment/provider contractual or residency changes do not automatically change Model Profile identity;
- a materially changed underlying release requires a new Model Profile identity linked by supersedes/superseded-by;
- if sameness of the release cannot be demonstrated after provider backend change, architecture requires new identity or explicit identity conflict, never silent profile-version increment;
- marketing alias rename never changes identity by itself;
- Routing Decision preserves stable model ID, Registry Profile Version, Underlying Model Release identity, Provider Offering Mapping, Provider Profile version, and Deployment Profile version.

Stress-test these five cases:
1. marketing alias rename only;
2. provider contract/data-handling change only;
3. provider silently changes backend behavior and release sameness cannot be proven;
4. deployment region/residency changes only;
5. AI-OS corrects evidence/metadata only.

Report identity/version contradiction count.

### 1.2 Cross-registry governance integrity

Verify every active `decision.<id>` and `review.<id>` in Phase 9 does one of exactly two things:

- resolves to an approved Phase 7 / Phase 6 object; or
- is explicitly marked `FUTURE_GOVERNANCE_REFERENCE` / equivalent non-executable marker.

Required:
- unresolved IDs are never treated as exercisable;
- no plausible-sounding fabricated Review Profile or Decision Right is permitted;
- lack of applicable approved Right produces `NO_APPLICABLE_DECISION_RIGHT` or equivalent and routing blocks/escalates for governance design;
- carding a missing Right is explicitly a Phase 7 action, never performed by Phase 9;
- conceptually-needed review with no approved profile is marked non-bound/non-executable rather than invented.

Independently resolve the references used by Exemplar 9 against approved Phase 6 and Phase 7 registries.

If `review.security`, `review.code`, `decision.production_release`, or any other referenced ID is not actually approved/resolvable, mark FAIL.

Report unresolved active governance reference count.

### 1.3 Removed capability cleanup

Verify:
- `capability.privacy_sensitive_suitability` has no active normative use;
- every active `capability.<id>` reference across Phase 9 resolves to a declared capability family/token;
- removed tokens may appear only in clearly historical/remediation prose, never as active rule/example semantics.

Report undeclared active capability reference count.

### 1.4 Active inventory / counts

Independently derive and verify all active counts, including at minimum:
- capability families;
- eligibility constraints;
- preferences;
- routing act requirements;
- primary lifecycle states;
- evidence classes;
- common constraints;
- templates;
- exemplars;
- Routing Decision elements.

Check every active place where those counts are stated.

Also verify headings/cardinality prose such as “two things this architecture cannot express” matches actual listed cardinality.

Report inventory inconsistency count.

### 1.5 Validation harness coverage

Audit whether the current harness materially checks:
- identity/release/profile-version consistency;
- cross-registry Decision/Review ID resolution;
- undeclared capability references;
- derived active inventory counts;
- stale active prose counts;
- exemplar 9 governance integrity;
- Phase 3–8 regression;
- Phase 9 PROPOSED status;
- non-runtime boundary.

Run if possible:
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_9_validation.py --verbose`
- JSON mode if supported;
- `python3 validation/phase_8_validation.py`

Perform a failure injection or equivalent inspection if feasible to confirm non-zero failure behavior.

Return validation credibility HIGH / MEDIUM / LOW.

---

## 2. Full identity/object-model audit

Verify separation:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != KNOWLEDGE != MODEL PROFILE != MODEL CAPABILITY != ROUTING POLICY != ROUTING DECISION != PROVIDER != DEPLOYMENT != RUNTIME`

Required:
- MODEL != ROLE;
- MODEL != AGENT INSTANCE;
- MODEL != AUTHORITY;
- MODEL != REVIEWER IDENTITY;
- MODEL != KNOWLEDGE SOURCE BY DEFAULT;
- MODEL != CANONICAL KNOWLEDGE;
- MODEL != PROVIDER != DEPLOYMENT;
- ROUTER != ORCHESTRATOR;
- ROUTING DECISION != DECISION RIGHT.

Report identity-collapse count.

---

## 3. Candidate Universe Definition

Verify every Routing Decision binds a reproducible universe before filtering/ranking.

Required:
- deterministic registry-state/snapshot reference;
- universe definition version;
- inclusion rule;
- routing scope;
- enumerated candidate set;
- omission reasons;
- completeness result;
- `CANDIDATE_UNIVERSE_INCOMPLETE` or equivalent when load/enumeration is incomplete;
- availability does not silently remove candidates;
- outside-universe exclusion is distinct from in-universe ineligibility;
- accidental omission is detectable.

Stress-test unloaded, unavailable, globally prohibited, stale, unknown-availability, intentionally out-of-scope, accidentally omitted candidates.

Report candidate-universe loophole count.

---

## 4. Sensitivity / privacy / residency

Verify Phase 8 sensitivity is used exactly as multi-label/orthogonal semantics, never an invented total order.

Required:
- all applicable labels must be explicitly supported;
- all per-label handling obligations must be met;
- prohibited classes override support;
- unknown support != supported;
- compound labels accumulate obligations;
- routing does not change scope, canonicality or visibility.

Residency must represent:
- exact jurisdictions;
- region classes;
- region-to-jurisdiction mapping;
- allowed/prohibited sets;
- cross-border posture;
- unknown residency;
- evidence/review-by.

Report scalar-sensitivity leakage count and residency ambiguity count.

---

## 5. Requirement taxonomy and exceptionability

Verify exactly distinct semantic kinds:
- ELIGIBILITY_CONSTRAINT;
- PREFERENCE;
- ROUTING_ACT_REQUIREMENT.

Verify exceptionability semantics:
- ABSOLUTELY_NON_WAIVABLE;
- GOVERNED_EXCEPTION_POSSIBLE;
- OPERATOR_CONFIGURABLE_WITHIN_POLICY.

Required:
- act requirement never masquerades as filter;
- preference never restores ineligible candidate;
- unknown exceptionability defaults non-waivable;
- Phase 7 Right cannot create legal authority where none exists;
- only a specific applicable approved Right may adjust a governed-exception constraint;
- ordinary human acknowledgement never changes eligibility.

Report taxonomy ambiguity count and exceptionability ambiguity count.

---

## 6. Fallback / governed exception

Verify three-case model:
A. ordinary fallback satisfies all eligibility constraints;
B. candidate initially ineligible, specific approved Phase 7 act adjusts bounded requirement context, then re-evaluation occurs;
C. non-waivable/no applicable Right => block.

Required:
- original ineligibility preserved;
- no retrospective relabelling;
- no silent degradation;
- no “best available” path when no candidate qualifies;
- each fallback assessed against original requirements or explicitly adjusted governed context;
- model diversity and reviewer independence remain separate controls.

Audit Exemplar 9 especially.

---

## 7. Evidence / lifecycle

Verify negative evidence applicability is bounded by:
- release/profile version;
- provider/deployment context;
- capability/evaluation dimension;
- domain/task context;
- materiality/severity;
- evidence quality;
- freshness/effective period;
- remediation status.

Verify conflict creates governed evidence conflict rather than blind averaging.

Lifecycle:
- exactly six mutually exclusive primary states if that is the final model;
- `PREFERRED` is not a primary lifecycle state;
- restrictions are annotations, not competing primary states;
- `RETIRED` terminal;
- history preserved.

Report ambiguity counts.

---

## 8. Precedence / Routing Policy

Verify:
- stages 1–5 are globally fixed hard/governance stages;
- stage 6 soft preference order belongs to the versioned Routing Policy;
- no hidden global “reliability always before cost” remains;
- if risk requires minimum reliability, it is represented as eligibility constraint;
- lexicographic soft preferences do not become a hidden composite score;
- deterministic tie-break is governance-neutral.

---

## 9. Review diversity / criticality

Verify:
`REVIEWER / REVIEW PROFILE INDEPENDENCE != MODEL DIVERSITY`.

Required:
- different version != different family;
- different provider not default;
- Decision-Grade family diversity is policy/review-context dependent, not blanket global law;
- same reviewer using another model does not become independent;
- reducing model diversity does not alter Phase 6 reviewer independence.

Report leakage count.

---

## 10. Routing Decision model

Verify actual required element count and whether the record supports reconstruction of:
- task/Role/Workflow context;
- criticality;
- Candidate Universe Definition;
- candidate set and per-candidate eligibility;
- exclusion reasons;
- six-part reproducibility identity set;
- Routing Policy version and preference order;
- availability state/time;
- fallback/degradation;
- act requirements;
- original failed constraint;
- approved Decision Right/Record where applicable;
- adjusted requirement context;
- re-evaluation result;
- provenance/history.

Report missing semantic field count.

---

## 11. Router / Orchestrator boundary

Verify zero orchestration leakage.
Phase 9 must not decide task creation, task order, retries/replanning, concurrency, Role assignment, or whether work occurs.

---

## 12. Anti-lock-in / provider independence

Verify:
- marketing aliases do not define identity;
- provider rename does not rewrite history;
- deployment region differences may produce distinct Deployment Profiles where semantically needed;
- no real vendor product is hard-coded into higher architecture;
- historical Routing Decisions preserve exact versions/mappings;
- model pinning remains exceptional and bounded.

---

## 13. All nine exemplars

Audit each independently.

Return PASS/FAIL + concise reason for all 9.

Extra scrutiny:
- #3 uses only declared capability IDs;
- #4 compound privacy labels and unknown support;
- #6 unavailable candidate remains enumerated;
- #7 no-eligible path blocks;
- #9 contains no invented governance object and correctly stops at `NO_APPLICABLE_DECISION_RIGHT` / block if no approved Right exists.

---

## 14. Open questions

Independently adjudicate all 17 Phase 9 questions.

Questions #1 and #10 previously remained blockers and must receive special scrutiny.

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 10+
- PHASE 11+
- RUNTIME CONCERN

Human approval is not ready if #1 or #10 remains materially unresolved.

---

## 15. Inventory / stale prose scan

Search active normative Phase 9 text for stale statements of:
- 24 capability families;
- 24/22 eligibility or “hard” constraints where actual current count differs;
- 8 preferences where actual current count differs;
- 33/43 common constraints where actual current count differs;
- 31 Routing Decision elements if actual current count differs;
- removed capability IDs;
- any cardinality heading mismatch.

Historical remediation prose may mention old numbers only if clearly historical.

Report active stale-prose count.

---

## 16. Regression / non-runtime

Compare against Phase 8 approval record `00fb92e1b2dd1209ee2f69550c5962158b881e3e`.

Require:
- Phase 3 Role changes = 0;
- Phase 4 Skill changes = 0;
- Phase 5 Workflow changes = 0;
- Phase 6 Handoff/Review changes = 0;
- Phase 7 Decision changes = 0;
- Phase 8 Knowledge/Canonical semantic changes = 0;
- Phase 8 validator unchanged in the final remediation;
- all Phase 9 artifacts remain PROPOSED;
- no runtime/SDK/API/secrets/DB/UI/RAG/agent/orchestrator implementation;
- no real model/provider/deployment profiles;
- no PR on Phase 9 branch.

---

## 17. Approval threshold

Return `PASS` only if no material architecture issue remains.

Return `PASS WITH NON-BLOCKING NOTES` only if every note is genuinely Phase 10+/11+/runtime/controlled-carding and cannot cause identity, authority, privacy, eligibility, exception, review, provenance or auditability misuse.

Return `PASS WITH CHANGES` if another bounded Phase 9 correction is required.

Return `FAIL` if any material blocker remains or validation gives materially false confidence.

---

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. FINAL BLOCKER RE-AUDIT
For each of the final five blockers: RESOLVED / NOT RESOLVED + exact evidence.

### C. MODEL IDENTITY / VERSIONING
PASS / FAIL; identity/version contradiction count; six-part reproducibility verdict.

### D. CROSS-REGISTRY GOVERNANCE INTEGRITY
PASS / FAIL; unresolved active `decision.*` count; unresolved active `review.*` count; Exemplar 9 governance verdict.

### E. CAPABILITY TAXONOMY
PASS / FAIL; undeclared active capability reference count; removed-token leakage count.

### F. INVENTORY / COUNTS
PASS / FAIL; inconsistency count; derived current counts.

### G. CANDIDATE UNIVERSE
PASS / FAIL; reproducibility verdict; omission/incomplete-universe loophole count.

### H. SENSITIVITY / PRIVACY / RESIDENCY
PASS / FAIL; scalar-sensitivity leakage count; multi-label compatibility verdict; residency ambiguity count.

### I. REQUIREMENT TAXONOMY / EXCEPTIONABILITY
PASS / FAIL; requirement-kind ambiguity count; exceptionability ambiguity count.

### J. FALLBACK / GOVERNED EXCEPTION
PASS / FAIL; pre-exception eligibility contradiction count; non-waivable handling verdict; history-preservation verdict.

### K. EVIDENCE / LIFECYCLE
PASS / FAIL; negative-evidence ambiguity count; lifecycle ambiguity count.

### L. PRECEDENCE / ROUTING POLICY
PASS / FAIL; hard-stage/soft-order boundary verdict; hidden global-order findings.

### M. REVIEW DIVERSITY / CRITICALITY
PASS / FAIL; reviewer-independence/model-diversity leakage count; blanket-rule findings.

### N. ROUTING DECISION MODEL
PASS / FAIL; actual required element count; missing semantic field count; reproducibility verdict.

### O. ROUTER / ORCHESTRATOR
PASS / FAIL; orchestration leakage count.

### P. NINE EXEMPLARS
Each PASS / FAIL with one concise reason.

### Q. OPEN QUESTIONS
All 17 independent dispositions.

### R. VALIDATION HARNESS
Exact commands/results; credibility HIGH / MEDIUM / LOW; vacuous/discovery findings; Phase 8 harness result.

### S. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–8 changes; Phase 9 status; runtime/profile/PR status.

### T. REMAINING BLOCKERS
If none: NONE.

### U. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 9
- READY AFTER LISTED CHANGES
- NOT READY

### V. EXPANSION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED MODEL/PROVIDER CARDING
- SAFE FOR CONTROLLED BATCH MODEL/PROVIDER CARDING
- SAFE FOR MASS MODEL/PROVIDER CARDING

Do not modify anything.