# Codex Prompt — Independent Phase 9 Model Registry / Router Foundation Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Audit baseline commit: `212f42e4453033d63b761fe6c19c63538ce772d8`
Phase 8 human-approval record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 9 APPROVED or CANONICAL.

The producer reports 27 files, 141/141 deterministic checks PASS, no Phase 3–8 semantic regressions, no real vendor/model profiles, and readiness for independent foundation audit. Treat every producer claim as untrusted until independently verified.

Read at minimum:
- `architecture/model-registry-router.md`
- `models/_standards/common-model-governance-constraints.md`
- `models/_templates/model-profile-template.md`
- `models/_templates/provider-profile-template.md`
- `models/_templates/deployment-profile-template.md`
- `models/_templates/routing-policy-template.md`
- `models/_templates/routing-decision-template.md`
- `models/model-capability-taxonomy.md`
- `models/model-lifecycle-and-versioning.md`
- `models/routing-constraint-model.md`
- `models/routing-precedence-and-fallback.md`
- `models/review-diversity-and-criticality.md`
- `models/evaluation-evidence-model.md`
- `models/master-model-routing-universe.md`
- all `models/exemplars/*.md`
- `reviews/phase-9-foundation-self-check.md`
- `validation/phase_9_validation.py`
- `validation/README.md`
- relevant approved Phase 3–8 artifacts needed for regression, especially Role, Review, Decision Right, criticality and Phase 8 sensitivity/scope rules.

Audit architecture, not prose style.

## 1. Identity separation

Verify:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != KNOWLEDGE != MODEL PROFILE != MODEL CAPABILITY != ROUTING POLICY != ROUTING DECISION != PROVIDER != DEPLOYMENT/ENDPOINT != RUNTIME`

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

Report identity-collapse loophole count.

## 2. Model / provider / deployment object model

Audit whether the three-object separation is coherent.

Stress-test:
- same model family through two providers;
- same model version through public and private deployments;
- one provider with multiple models;
- provider terms change without model version change;
- deployment residency changes without provider identity change;
- model capability unchanged while deployment sensitivity allowance changes.

PASS only if runtime would not need to invent whether a property belongs to model, provider, or deployment.

Explicitly assess whether “one Model Profile = one model one version” is coherent enough, including provider-specific variants and provider-hosted aliases.

## 3. Model capability taxonomy

Audit the 24 capability families and four claim classes.

Check:
- capability families are sufficiently non-overlapping;
- `NOT_CLAIMED != NOT_CAPABLE` is consistently applied;
- limitations and prohibited contexts can narrow/override positive capability claims;
- no claim class implies guaranteed quality;
- no single global “best model” concept exists;
- model size/provider prestige cannot substitute for capability evidence.

Flag any missing capability dimension that would force runtime to invent a material governance concept later.

## 4. Capability evidence model

Audit the six evidence classes.

Verify:
- provider declaration is not treated as proof;
- external benchmark is distinct from internal evaluation;
- observed production evidence is future/runtime evidence, not architecture execution;
- known limitation/incident can override or restrict positive evidence in its dimension;
- confidence cannot make an ineligible candidate eligible;
- evidence freshness/review-by semantics reuse Phase 8 correctly;
- provider term changes can affect deployment/privacy suitability without rewriting capability truth.

Critically test the statement “negative evidence outweighs positive in its dimension”. Determine whether it is sufficiently bounded by recency/materiality/context/version, or whether one stale/low-quality negative observation could permanently dominate stronger evidence.

## 5. No composite score / ranking semantics

Audit the prohibition on a single composite score.

Verify architecture still allows deterministic preference ordering without secretly recreating a composite score through opaque weighting.

Check whether:
- dimension-specific thresholds and precedence are enough;
- confidence ranking has bounded meaning;
- tie-breaking is deterministic but not governance-significant;
- “reliability before cost” is correctly encoded.

Flag any hidden scoring path that can override hard constraints.

## 6. Lifecycle model

Audit states:
`CANDIDATE`, `EVALUATING`, `ELIGIBLE`, `PREFERRED`, `RESTRICTED`, `DEPRECATED`, `SUSPENDED`, `RETIRED` or their exact final forms.

Verify:
- lifecycle != task-specific eligibility;
- `PREFERRED` never forces use;
- `RESTRICTED` semantics are explicit;
- `DEPRECATED` does not erase historical Routing Decisions;
- `SUSPENDED`/`RETIRED` behavior for new routing is clear;
- transitions are coherent and history-preserving.

Check whether a model can be both `PREFERRED` and `RESTRICTED`, or whether states are exclusive. If exclusivity is intended, verify it is explicit.

## 7. Hard constraints vs soft preferences

Audit the constraint taxonomy and ensure each constraint has an unambiguous hard/soft role.

Required:
- hard constraint filters;
- soft preference ranks only eligible candidates;
- unknown constraint blocks rather than gets ignored;
- no accumulation of preferences restores an ineligible candidate;
- cost/latency cannot override legality/privacy/capability/independence/criticality;
- HUMAN_SELECTION_REQUIRED is modeled as an act requirement rather than eligibility distortion.

Report hard/soft ambiguity count.

## 8. Routing precedence

Audit the eight-stage precedence order.

Verify no contradiction among:
- legality/governance;
- sensitivity/privacy/residency;
- capability/modality/context/tooling;
- independence/diversity;
- lifecycle/availability;
- reliability;
- latency/cost;
- tie-break.

Critically test whether “reliability before cost” is always correct or should be policy-dependent within an eligible set. If policy may choose differently, determine whether current architecture over-hard-codes a preference order that should itself be versioned policy.

Do not fail merely because a different order is conceivable; fail if current order conflicts with the claimed reusable Routing Policy abstraction.

## 9. Routing Policy vs Routing Decision

Verify:
- Policy = reusable versioned rule set;
- Decision = task-instance selection record;
- neither is a Phase 7 Decision Right;
- Routing Decision cannot approve work, accept risk, satisfy review, promote knowledge or grant authority.

Audit the 24 claimed required Routing Decision elements for sufficiency.

Required evidence should support reconstruction of:
- task context;
- required capabilities;
- constraints;
- candidate set;
- eligibility result and exclusion reason;
- selected model/provider/deployment versions;
- policy version;
- diversity requirement;
- availability context;
- fallback/degradation status;
- human involvement/exception refs;
- provenance/audit history.

Flag missing semantic fields that runtime would otherwise need to invent.

## 10. Candidate-set completeness

Producer says a Routing Decision records each candidate and why it was eligible/ineligible.

Audit what defines the candidate universe.

Stress-test:
- candidate omitted accidentally;
- candidate unavailable at routing time;
- provider prohibited globally;
- model profile stale;
- deployment unknown availability;
- candidate existed in registry but not loaded into runtime.

Determine whether “candidate set where practical” is too weak for auditability. If full registry enumeration is not required, architecture must define a reproducible bounded candidate-universe rule.

This is potentially material.

## 11. Model-family diversity vs reviewer independence

Verify:
`REVIEWER / REVIEW PROFILE INDEPENDENCE != MODEL DIVERSITY`.

Check all four combinations:
- independent reviewer + same model family;
- independent reviewer + different family;
- non-independent reviewer + different family;
- non-independent reviewer + same family.

Verify:
- model diversity never upgrades Phase 6 independence;
- Phase 9 does not create/alter Review statuses;
- different provider is not default;
- different version is weaker than different family where architecture claims so;
- diversity requirement is measured against a named producer Routing Decision;
- missing predecessor Routing Decision blocks where diversity is mandatory.

Critically assess whether `DIFFERENT_MODEL_FAMILY_REQUIRED` at Decision-Grade is truly a policy option rather than an implicit blanket default.

## 12. Criticality integration

Verify approved criticality bands are reused, not redefined.

Check higher criticality raises routing rigor through evidence freshness, capability/reliability requirements, privacy/deployment constraints and review diversity where justified.

Criticality must not:
- create authority;
- make output true;
- automatically require the largest/most expensive model;
- rewrite Role/Review semantics.

Flag any blanket Decision-Grade requirement not tied to explicit policy/review context.

## 13. Fallback semantics

Audit:
- EQUIVALENT_FALLBACK;
- DEGRADED_FALLBACK;
- PROHIBITED_FALLBACK;
- HUMAN_SELECTION_FALLBACK;
- BLOCK / NO_ELIGIBLE_MODEL.

Required:
- every fallback rechecked against original hard requirements;
- no chained degradation drift;
- no outage-based relaxation of hard constraints;
- degraded fallback explicitly records weakened dimension;
- degraded fallback still satisfies every hard constraint unless a separately valid governed exception exists;
- no “best available” path when nothing is eligible.

Critically test relationship between “degraded fallback still satisfies every hard constraint” and “governed exception under Phase 7”. If a hard constraint is actually waived by exception, the selected candidate is not eligible under the original policy. Architecture must distinguish exception-adjusted requirements from ordinary fallback without semantic contradiction.

## 14. Human control / exceptions

Audit ordinary human choice vs governed exception.

Verify humans may:
- select among eligible candidates;
- require stronger/different family/provider;
- prohibit candidate;
- acknowledge declared degraded fallback where allowed;
- block execution.

Verify humans may not:
- bypass law/privacy/security/contract constraints by ordinary override;
- waive review independence merely by routing selection;
- make output true/canonical;
- rewrite routing history.

Critical issue: identify which hard constraints are absolutely non-waivable versus potentially exceptionable under a Phase 7 Decision Right. Architecture must not imply every hard constraint can be exceptioned.

If no taxonomy exists, determine whether one is required before human approval.

## 15. Privacy / sensitivity / residency

Audit Phase 8 integration.

Verify:
- task/data sensitivity comes from Phase 8;
- deployment carries max allowed sensitivity/residency/retention/training posture;
- sensitivity classification does not directly name provider;
- provider suitability requires explicit evidence/policy;
- `NO_TRAINING_ON_INPUT`: unknown/not-declared != satisfied;
- routing does not move knowledge across scope boundaries;
- PERSONAL / organisational separation remains intact;
- routing changes neither canonicality nor visibility;
- no IAM implementation leaks into Phase 9.

Critically test whether comparing “maximum sensitivity” by simple ordinal ordering is valid across all Phase 8 sensitivity classes, since some classes may be orthogonal (e.g. privileged/legal vs trade secret vs personal data). If architecture assumes a total order where Phase 8 defines categories, this may be a blocker.

## 16. Residency / jurisdiction semantics

Verify deployment eligibility can represent:
- exact jurisdiction;
- region class;
- allowed list;
- prohibited list;
- sovereign/private deployment requirement;
- unknown residency.

Check that region/residency is not accidentally stored only as provider-level property where deployment-specific variation matters.

## 17. Availability semantics

Audit `AVAILABLE`, `DEGRADED`, `UNAVAILABLE`, `UNKNOWN_AVAILABILITY`.

Verify availability != capability.

Check:
- unknown availability handling by criticality;
- whether “unknown is ineligible on Enhanced Decision-Grade” is architecture policy or should be Routing Policy choice;
- availability evidence is runtime-observed and timestamped conceptually;
- Phase 9 does not build monitoring.

## 18. Anti-lock-in

Audit stable internal IDs, aliases, versioning and historical reproducibility.

Verify:
- no real provider/model names in architecture artifacts except historical/source references if any;
- alias rename never changes identity;
- constraints never bind against alias accidentally;
- model pinning is exceptional, justified, owned and time-bounded;
- provider/product rename does not rewrite history;
- historical Routing Decisions preserve exact profile versions.

Critically assess the rule “stable IDs without dates/regions/versions”. Some deployment IDs may need region/deployment distinction as identity. Verify the anti-lock-in rule does not prohibit semantically necessary stable differentiation.

## 19. Evaluation boundary

Verify Phase 9 owns evaluation evidence semantics, not the evaluation engine/methodology.

Check:
- 11 evaluation dimensions remain dimension-specific;
- no single score becomes authority;
- internal/external/provider evidence remain distinguishable;
- review-detection quality distinct from generation capability;
- evaluation freshness and incident triggers exist;
- runtime evaluation service is not implemented.

## 20. Model freshness / drift

Verify model/provider/deployment/routing-policy changes trigger review appropriately.

Stress-test:
- model alias rename only;
- silent provider backend change;
- provider terms update;
- new model version;
- safety incident;
- quality regression;
- deployment-region change.

Check whether the architecture can represent “same vendor product name, materially changed behavior” without losing version identity.

## 21. Role-to-model boundary

Verify no Role Card is rewritten to vendor/model identity.

Preferred chain should remain:
`ROLE PROFILE + ASSIGNMENT ATTRIBUTES + SKILL SET + WORKFLOW CONTEXT + TASK CRITICALITY -> MODEL REQUIREMENTS -> ROUTING POLICY -> ELIGIBLE MODEL SET -> ROUTING DECISION`.

Check model pinning is exceptional and bounded.

## 22. Router vs Orchestrator boundary

Verify Phase 9 does not decide:
- what tasks exist;
- task ordering;
- parallelism;
- retries/replanning;
- which Role owns work;
- whether work should occur.

Those belong to Workflow/Phase 11.

Flag any orchestration leakage in fallback/retry language.

## 23. Provider / deployment first-class objects

Audit whether Provider and Deployment should indeed be first-class registry objects.

PASS only if their distinct governance properties justify separation and no material duplication creates contradictory sources of truth.

## 24. Synthetic exemplars

Audit all 9 exemplars.

For each report PASS/FAIL and concise reason.

Check exemplars do not smuggle in unnamed-but-obviously-real vendor claims as architecture truth.

Specific stress points:
- low-cost model wins only among eligible candidates;
- high-criticality example does not equate small/large size with evidence quality;
- independent review keeps reviewer and model diversity separate;
- privacy example places sensitivity at deployment layer;
- vision example filters rather than ranks incapable model;
- outage example preserves constraints;
- no-eligible example blocks;
- deprecated-model example preserves historical decision;
- degraded fallback example does not confuse human acknowledgement with authority to waive a hard constraint.

## 25. Master universe / counts

Audit `models/master-model-routing-universe.md`.

Verify all active counts match actual files/taxonomies/templates/constraints/lifecycle states/evidence classes/exemplars.

Look for stale prose from earlier iterations.

Report inventory inconsistency count.

## 26. Validation harness

Run if possible:
`python3 validation/phase_9_validation.py`

Inspect `--verbose` and `--json` if feasible.

Verify:
- actual result count;
- no vacuous checks (`or True`, tautologies, unreachable fail branches, cosmetic hard-coded pass counts);
- checks discover files where appropriate;
- anti-vendor check does not produce false confidence by banning only a tiny known list;
- runtime check does not misclassify architecture terminology as implementation or vice versa;
- regression checks truly compare against Phase 8 approval baseline;
- no local check falsely claims remote PR state;
- exemplars/templates are semantically discovered rather than selected by optional fields whose absence is itself a defect.

Return credibility HIGH / MEDIUM / LOW.

## 27. Phase 8 harness modification

Producer changed `validation/phase_8_validation.py` to account for the Phase 8 approval record.

Verify:
- this is tooling-only, not Phase 8 semantic change;
- the revised check is stricter/correct, not weakened to permit architecture artifacts to self-approve;
- Phase 8 still passes its own harness;
- no approved Phase 8 knowledge files changed.

## 28. Open questions

Independently adjudicate all 17 Phase 9 questions.

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 10+
- PHASE 11+
- RUNTIME CONCERN

Pay strongest attention to:
- Model Profile identity granularity;
- provider/deployment first-class status;
- review diversity requirements;
- human direct selection;
- hard constraint exceptionability;
- fallback vs exception;
- privacy/residency representation;
- evaluation ownership boundary;
- Router vs Orchestrator boundary.

No authority/privacy/independence ambiguity may be deferred silently.

## 29. Regression / non-runtime

Compare against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`.

Required:
- Phase 3 approved Role semantic/file changes = 0;
- Phase 4 Skill changes = 0;
- Phase 5 Workflow changes = 0;
- Phase 6 Handoff/Review changes = 0;
- Phase 7 Decision changes = 0;
- Phase 8 Knowledge/Canonical semantic changes = 0;
- validation-only Phase 8 change correctly bounded;
- all Phase 9 artifacts remain PROPOSED;
- no runtime/provider SDK/API/secrets/DB/UI/orchestrator implementation;
- no real model/provider/deployment profile cards;
- no PR for Phase 9 branch.

## 30. Blocker policy

Treat as blocking before human approval if any of the following exist:
- Role/Model collapse;
- Router/Orchestrator collapse;
- Routing Decision/Decision Right collapse;
- model/provider/deployment ambiguity that runtime must invent;
- hard constraints can be overridden by preferences;
- cost/latency can override governance;
- privacy/residency model is semantically invalid;
- candidate universe is not auditable enough to reproduce routing;
- silent fallback/degradation path;
- reviewer independence confused with model diversity;
- human ordinary override can waive mandatory hard constraints;
- exception semantics do not distinguish non-waivable vs waivable constraints;
- no-eligible-model path silently chooses “best available”;
- provider lock-in leaks into higher architecture;
- Phase 3–8 semantic regression;
- validation harness gives materially false confidence.

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. HIGH / MEDIUM FINDINGS
All HIGH and MEDIUM findings with exact files/sections. If none: NONE.

### C. IDENTITY / OBJECT MODEL
PASS / FAIL; identity-collapse count; model/provider/deployment ambiguity count.

### D. CAPABILITY / EVIDENCE
PASS / FAIL; capability-taxonomy gaps; evidence-model ambiguities; negative-evidence finding.

### E. LIFECYCLE / VERSIONING
PASS / FAIL; lifecycle contradictions; anti-lock-in/versioning findings.

### F. CONSTRAINTS / PRECEDENCE
PASS / FAIL; hard/soft ambiguity count; precedence-policy findings.

### G. ROUTING DECISION / CANDIDATE UNIVERSE
PASS / FAIL; missing record semantics; candidate-universe reproducibility verdict.

### H. CRITICALITY / REVIEW DIVERSITY
PASS / FAIL; reviewer-independence/model-diversity leakage count; Decision-Grade findings.

### I. FALLBACK / HUMAN EXCEPTION
PASS / FAIL; silent-degradation count; hard-constraint exceptionability verdict.

### J. PRIVACY / SENSITIVITY / RESIDENCY
PASS / FAIL; Phase 8 sensitivity compatibility verdict; residency/deployment findings.

### K. AVAILABILITY / FRESHNESS / EVALUATION
PASS / FAIL; ambiguity counts/findings.

### L. ROUTER / ORCHESTRATOR BOUNDARY
PASS / FAIL; orchestration leakage count.

### M. NINE EXEMPLARS
Each PASS / FAIL with one concise reason.

### N. OPEN QUESTIONS
All 17 independent dispositions.

### O. VALIDATION HARNESS
Exact command/result if run; credibility HIGH / MEDIUM / LOW; vacuous-test or discovery findings.

### P. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–8 changes, Phase 8 harness-only change, Phase 9 status, runtime/profile/PR status.

### Q. REMAINING BLOCKERS
If none: NONE.

### R. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 9
- READY AFTER LISTED CHANGES
- NOT READY

### S. EXPANSION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED MODEL/PROVIDER CARDING
- SAFE FOR CONTROLLED BATCH MODEL/PROVIDER CARDING
- SAFE FOR MASS MODEL/PROVIDER CARDING

Do not modify anything.