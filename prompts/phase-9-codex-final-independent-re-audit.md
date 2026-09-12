# Codex Prompt — Final Independent Phase 9 Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Audit baseline commit: `69a119f59c8fc1687944ed27df594dc809aadf78`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`
Original Phase 9 foundation baseline: `212f42e4453033d63b761fe6c19c63538ce772d8`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 9 APPROVED or CANONICAL.

The prior independent audit returned `FAIL` with 5 HIGH and 7 MEDIUM findings. The remediation commit claims all 12 are resolved and the Phase 9 validation harness reports `204/204 PASS` while Phase 8 remains `119/119 PASS`.

Treat every remediation claim as untrusted until independently verified.

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
- relevant approved Phase 3–8 sources, especially Phase 6 review independence, Phase 7 Decision Rights, Phase 8 sensitivity/scope/canonical governance.

## 1. Re-audit exact prior HIGH findings

### H1 — Model Profile identity granularity
Verify the six-layer stack is explicit and coherent:
- Model Family;
- Underlying Model Release;
- Model Profile;
- Registry Profile Version;
- Provider Offering Mapping;
- Deployment Profile.

Required:
- registry profile version != underlying model release/version;
- marketing alias never defines identity;
- one Model Profile may map to multiple provider/deployment combinations only with evidence they expose the same underlying release;
- materially different provider behavior must become a distinct profile/variant, not ambiguous mapping;
- historical Routing Decision preserves exact profile version + provider/deployment mapping;
- data-handling posture is not duplicated as a Model Profile property.

Report identity ambiguity count.

### H2 — Candidate universe reproducibility
Verify every Routing Decision binds a Candidate Universe Definition before filtering/ranking.

Required semantics:
- deterministic registry-state/snapshot reference;
- universe definition version;
- inclusion/enumeration rule;
- routing scope;
- enumerated candidate set;
- explicit pre-universe exclusions vs in-universe ineligibility;
- omission reason;
- completeness result;
- runtime load failure => `CANDIDATE_UNIVERSE_INCOMPLETE` or equivalent;
- availability does not silently remove a candidate from the universe;
- incomplete universe blocks/escalates according to policy.

Reject “where practical” or equivalent weak language.

### H3 — Phase 8 sensitivity compatibility
Verify scalar/ordinal “maximum sensitivity” logic is fully removed from normative Phase 9.

Required:
- sensitivity is handled as a multi-label set/policy compatibility model;
- every applicable Phase 8 label must be explicitly supported;
- obligations for all labels must be met simultaneously;
- prohibited labels override support;
- unknown support != supported;
- no label outranks another unless Phase 8 explicitly says so;
- compound cases such as `PERSONAL_DATA + PRIVILEGED` work correctly.

Report scalar-sensitivity leakage count.

### H4 — Residency/jurisdiction semantics
Verify Deployment Profile can explicitly represent:
- exact jurisdictions;
- region/residency class;
- allowed jurisdictions;
- prohibited jurisdictions;
- mapping between region class and exact jurisdictions;
- cross-border processing posture;
- `UNKNOWN_RESIDENCY` or equivalent;
- evidence/source/review-by.

Required precedence:
- unknown never satisfies a hard residency requirement;
- prohibited outranks allowed;
- provider-level claims constrain but do not replace deployment evidence;
- broad region class and exact jurisdiction are not silently interchangeable.

### H5 — Fallback vs eligibility vs governed exception
Verify the architecture cleanly separates:
A. ordinary eligible fallback;
B. governed exception-adjusted requirement context followed by re-evaluation;
C. non-waivable failure -> block.

Required:
- candidate failing original eligibility constraint is recorded as ineligible;
- valid Phase 7 Decision Right/Record, where allowed, adjusts a bounded requirement context first;
- then eligibility is re-evaluated;
- original result/history preserved;
- candidate is never called eligible under the original failed policy;
- non-waivable failures remain blocked.

Audit Exemplar 9 especially.

## 2. Re-audit all prior MEDIUM findings

### M1 — Exceptionability taxonomy
Verify hard/eligibility constraints have explicit exceptionability semantics equivalent to:
- `ABSOLUTELY_NON_WAIVABLE`;
- `GOVERNED_EXCEPTION_POSSIBLE`;
- `OPERATOR_CONFIGURABLE_WITHIN_POLICY`.

Check:
- exceptionability derives from source/policy context, not generic hard-constraint label;
- specific named Phase 7 Right must cover the specific constraint class;
- unknown exceptionability defaults to non-waivable;
- law/regulation/privacy/security/contract prohibitions are not magically made exceptionable by existence of a Decision Right;
- human acknowledgement alone never changes eligibility.

### M2 — Negative evidence applicability
Verify negative evidence precedence is bounded by at least:
- exact release/profile version;
- provider/deployment context where relevant;
- capability/evaluation dimension;
- task/domain context;
- materiality/severity;
- evidence quality;
- freshness/effective period;
- remediation/resolution status.

Check stale/irrelevant/low-quality negative evidence does not dominate indefinitely.
Check current severe incidents can restrict immediately.
Check conflicting evidence produces governed conflict state rather than averaging.

### M3 — Lifecycle exclusivity
Verify exactly one primary lifecycle state at a time.
Check whether `PREFERRED` and `RESTRICTED` were correctly removed from primary state and represented as orthogonal designation/annotation.
Verify transition behavior, terminal `RETIRED`, and historical preservation.

### M4 — Act requirements vs eligibility constraints
Verify three semantic kinds exist and are non-overlapping:
- ELIGIBILITY_CONSTRAINT;
- PREFERENCE;
- ROUTING_ACT_REQUIREMENT.

`HUMAN_SELECTION_REQUIRED` must not be in the candidate-filter set.

### M5 — Fixed precedence vs policy-owned soft preferences
Verify:
- hard/governance stages are globally fixed;
- soft preference ordering is versioned Routing Policy-owned;
- no preference can restore an ineligible candidate;
- reliability can become a hard minimum where criticality/risk requires it;
- no hidden global “reliability always before cost” rule remains.

### M6 — Reviewer independence vs model diversity
Verify no Phase 9 artifact states or implies that reducing model-family diversity waives/reduces Phase 6 reviewer independence.
Where both controls apply, they remain separate.

### M7 — Privacy-sensitive suitability capability overlap
Verify `capability.privacy_sensitive_suitability` or equivalent governance-overlapping capability was removed or narrowed so it no longer duplicates provider/deployment eligibility.

### M8 — Data-handling posture ownership
Verify one authoritative read path:
- Model Profile: intrinsic technical characteristics only;
- Provider: contractual/default posture and constraints;
- Deployment: effective deployment-specific posture;
- routing reads effective deployment posture after provider constraints.

Report duplicated-source-of-truth count.

## 3. Candidate universe stress tests

Stress-test:
- registered candidate not loaded by runtime;
- candidate unavailable at decision time;
- globally prohibited provider;
- stale profile;
- deployment with unknown availability;
- candidate outside inclusion rule by design;
- candidate omitted accidentally.

PASS only if the record can distinguish all seven cases without runtime inventing semantics.

## 4. Sensitivity / residency stress tests

Stress-test at least:
- PERSONAL_DATA only;
- PRIVILEGED only;
- PERSONAL_DATA + PRIVILEGED;
- TRADE_SECRET + THIRD_PARTY_RESTRICTED;
- supported one label but unknown another;
- allowed region but prohibited exact jurisdiction;
- exact jurisdiction known, region class unknown;
- unknown residency;
- cross-border conditional processing.

PASS only if no scalar ordering or silent implication is needed.

## 5. Model/provider/deployment stress tests

Stress-test:
- same underlying release via two providers;
- same provider alias renamed;
- silent provider backend change;
- deployment-only data handling change;
- provider-wide contractual change;
- provider-specific behavior materially diverges from nominal same release;
- registry metadata correction with no underlying model change.

Verify each case has a deterministic identity/version consequence.

## 6. Requirement taxonomy / exception stress tests

Stress-test:
- legal prohibition;
- binding contract prohibition;
- unsupported sensitivity label;
- minimum reasoning class;
- model-family diversity requirement;
- max cost class;
- human-selection act requirement;
- required acknowledgement;
- provider prohibition.

For each determine whether it is:
- eligibility constraint;
- preference;
- act requirement;
plus exceptionability class.

Architecture must not imply all hard constraints are waiver-capable.

## 7. Routing Decision sufficiency

Audit the claimed 31 elements.

Verify the record supports reconstruction of:
- task context;
- role/workflow context;
- criticality;
- candidate universe definition;
- candidate set;
- per-candidate eligibility;
- exclusion reasons;
- profile/provider/deployment versions;
- Routing Policy version;
- preference order;
- availability state/time;
- fallback status;
- original failed requirements if exception path used;
- Phase 7 Decision Right/Record reference;
- adjusted requirement context;
- re-evaluation result;
- human act requirement completion;
- provenance/history.

Flag any runtime-invented missing semantic.

## 8. Review diversity / criticality

Verify Phase 9 still preserves:
`REVIEWER / REVIEW PROFILE INDEPENDENCE != MODEL DIVERSITY`.

Check:
- different model version != different model family;
- different provider not default;
- Decision-Grade does not impose blanket family/provider diversity outside explicit Review/Policy context;
- model diversity never upgrades review independence;
- same reviewer using another model is still non-independent if Phase 6 says so.

## 9. Router vs Orchestrator

Verify zero orchestration leakage.
Phase 9 must not decide task creation, ordering, parallelism, retry strategy, replanning, Role assignment or whether work should occur.

Fallback selection for a bounded task is allowed; workflow retry/replanning logic is not.

## 10. Evaluation / freshness boundary

Verify Phase 9 still owns evidence semantics only, not evaluation runtime/methodology.
Check provider terms change, incident, new release, quality regression and deployment change all trigger review appropriately.

## 11. Anti-lock-in

Verify stable IDs and alias semantics do not accidentally prohibit semantically necessary deployment differentiation.

Check:
- marketing rename != identity change;
- deployment region/jurisdiction differences may create distinct Deployment Profiles;
- profile IDs do not embed transient provider product names unless intentionally provider-specific mapping IDs;
- historical decisions preserve exact versions.

## 12. Nine exemplars

Audit all 9 independently.

Return PASS/FAIL for each with concise reason.

Extra scrutiny:
- #1 multi-label/privacy-safe eligibility;
- #4 unknown label support is ineligible;
- #5 modality non-waivable semantics;
- #6 unavailable candidate remains in universe;
- #7 multi-label no-eligible path;
- #9 original ineligibility -> governed exception -> adjusted context -> re-evaluation, with reviewer independence untouched.

## 13. Open questions

Independently re-adjudicate all 17 Phase 9 questions.

The prior audit marked #1, #7, #10, #13 as MUST RESOLVE BEFORE HUMAN APPROVAL.

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 10+
- PHASE 11+
- RUNTIME CONCERN

Do not accept producer labels without checking actual normative rules.

## 14. Validation harness

Run if possible:
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_9_validation.py --verbose`
- JSON mode if supported.

Also run:
- `python3 validation/phase_8_validation.py`

Verify:
- Phase 9 exact result total;
- non-zero exit on injected failure if feasible;
- no vacuous checks;
- semantic parsing rather than phrase-presence where material;
- candidate-universe checks cannot be bypassed by missing optional fields;
- sensitivity checks detect forbidden scalar/ordinal language;
- exception checks detect “eligible before exception” contradiction;
- lifecycle parser checks exactly one primary state;
- act requirements cannot appear in eligibility table;
- soft-order checks detect reintroduction of global reliability-before-cost;
- no local validator claims remote PR state;
- Phase 8 remains 119/119.

Return credibility HIGH / MEDIUM / LOW.

## 15. Inventory / counts

Audit `models/master-model-routing-universe.md`.
Verify actual counts for:
- capability families;
- lifecycle states;
- common constraints;
- requirement kinds;
- eligibility constraints/preferences/act requirements;
- evidence classes;
- templates;
- exemplars;
- decision fields if counted.

Report inventory inconsistency count.

## 16. Regression / non-runtime

Compare against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`.

Require:
- Phase 3 Role semantic/file changes = 0;
- Phase 4 Skill changes = 0;
- Phase 5 Workflow changes = 0;
- Phase 6 Handoff/Review changes = 0;
- Phase 7 Decision changes = 0;
- Phase 8 Knowledge/Canonical semantic changes = 0;
- Phase 8 validation remains unchanged in this remediation;
- all Phase 9 artifacts remain PROPOSED;
- no runtime/SDK/API/secrets/DB/UI/RAG/agent/orchestrator implementation;
- no real vendor/model/provider/deployment profiles;
- no PR on Phase 9 branch.

## 17. Approval threshold

Return `PASS` only if no material architecture issue remains.

Return `PASS WITH NON-BLOCKING NOTES` only if all notes are genuinely Phase 10+/11+/runtime or controlled-carding concerns and cannot cause identity, eligibility, privacy, scope, authority, exception, provenance or review-control misuse.

Return `PASS WITH CHANGES` if another bounded Phase 9 correction is required.

Return `FAIL` if any HIGH blocker remains or if validation gives materially false confidence.

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. PRIOR FINDINGS RE-AUDIT
For H1–H5 and M1–M8: RESOLVED / NOT RESOLVED + exact evidence and any residual issue.

### C. MODEL IDENTITY / OBJECT MODEL
PASS / FAIL; identity ambiguity count; duplicated data-handling source count.

### D. CANDIDATE UNIVERSE
PASS / FAIL; reproducibility verdict; omission/incomplete-universe loophole count.

### E. SENSITIVITY / PRIVACY / RESIDENCY
PASS / FAIL; scalar-sensitivity leakage count; multi-label compatibility verdict; residency ambiguity count.

### F. REQUIREMENT TAXONOMY / EXCEPTIONABILITY
PASS / FAIL; hard/soft/act ambiguity count; non-waivable/exceptionable ambiguity count.

### G. FALLBACK / GOVERNED EXCEPTION
PASS / FAIL; pre-exception eligibility contradiction count; history-preservation verdict.

### H. EVIDENCE / LIFECYCLE
PASS / FAIL; negative-evidence applicability ambiguity count; lifecycle-state ambiguity count.

### I. PRECEDENCE / ROUTING POLICY
PASS / FAIL; fixed-hard-stage vs policy-owned-soft-order verdict; hidden global-order findings.

### J. REVIEW DIVERSITY / CRITICALITY
PASS / FAIL; reviewer-independence/model-diversity leakage count; Decision-Grade blanket-rule findings.

### K. ROUTING DECISION MODEL
PASS / FAIL; missing semantic fields; reproducibility verdict.

### L. ROUTER / ORCHESTRATOR
PASS / FAIL; orchestration leakage count.

### M. NINE EXEMPLARS
Each PASS / FAIL with one concise reason.

### N. OPEN QUESTIONS
All 17 independent dispositions.

### O. VALIDATION HARNESS
Exact commands/results; credibility HIGH / MEDIUM / LOW; vacuous/discovery findings; Phase 8 harness result.

### P. INVENTORY / COUNTS
PASS / FAIL; inconsistency count and details.

### Q. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–8 changes, Phase 9 status, runtime/profile/PR status.

### R. REMAINING BLOCKERS
If none: NONE.

### S. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 9
- READY AFTER LISTED CHANGES
- NOT READY

### T. EXPANSION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED MODEL/PROVIDER CARDING
- SAFE FOR CONTROLLED BATCH MODEL/PROVIDER CARDING
- SAFE FOR MASS MODEL/PROVIDER CARDING

Do not modify anything.