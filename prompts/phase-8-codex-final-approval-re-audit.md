# Codex Prompt — Final Phase 8 Approval Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-8-memory-canonical`
Final remediation baseline: `516c91eb98ce89751b97d21c74553afaf7bed21b`
Phase 7 approval-record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 8 APPROVED or CANONICAL.

This is the final approval-readiness audit for Phase 8 — Memory / Canonical Governance.

Two prior independent audits found material defects. The current baseline claims all remaining blockers are resolved, the deterministic validation harness reports `119/119 PASS`, and Phase 8 is `READY FOR FINAL PHASE 8 APPROVAL RE-AUDIT`.

Treat all producer claims as untrusted until independently verified.

Read at minimum:
- `architecture/memory-canonical-governance.md`
- approved upstream context hierarchy at the Phase 7 baseline
- `knowledge/_standards/common-knowledge-governance-constraints.md`
- `knowledge/_templates/knowledge-record-template.md`
- `knowledge/_templates/canonical-record-template.md`
- `knowledge/knowledge-state-model.md`
- `knowledge/memory-class-model.md`
- `knowledge/scope-isolation-and-transfer.md`
- `knowledge/conflict-and-provenance-model.md`
- `knowledge/canonical-promotion-governance.md`
- `knowledge/sensitivity-and-retention-model.md`
- `knowledge/master-knowledge-governance-universe.md`
- all eight `knowledge/exemplars/*.md`
- `reviews/phase-8-foundation-self-check.md`
- `reviews/phase-8-foundation-audit-remediation.md`
- `validation/phase_8_validation.py`
- `validation/README.md`
- relevant approved Phase 3–7 artifacts, especially Knowledge & Evidence Steward and Phase 7 Decision Rights architecture.

## 1. Final blocker verification

### 1.1 PERSONAL / scope-family isolation
Verify:
- `PERSONAL / AD-HOC INITIATIVE` is a sibling scope family, not an ORGANISATION descendant;
- no organisational canonical statement propagates into PERSONAL by applicability/inheritance;
- no PERSONAL item propagates into organisational scope by absorption;
- no canonical state, Review satisfaction, authority, or applicability mode crosses that family boundary automatically;
- explicit reference/use is distinguished from inherited applicability;
- `MANDATORY_WIDER_CONSTRAINT` does not flow sideways into PERSONAL merely because a person belongs to an organisation;
- cross-family use requires explicit task selection/reference or governed transfer.

Required counts:
- sideways applicability leakage = 0;
- PERSONAL absorption leakage = 0.

### 1.2 Governance-state withdrawal consistency
Verify one coherent transition model across:
- `knowledge-state-model.md`;
- `canonical-promotion-governance.md`;
- common constraints;
- Knowledge Record template;
- Canonical Record template;
- universe.

Required semantics:
- no `APPROVED -> REVIEWED` rewind;
- no `APPROVED -> DRAFT` rewind;
- no `CANONICAL -> APPROVED` rewind;
- withdrawn `APPROVED` material goes to `RETRACTED` with withdrawn-level metadata `APPROVED`;
- retracted canonical material goes to `RETRACTED` with withdrawn-level metadata `CANONICAL`;
- revised claim is a new linked item/version beginning a new lifecycle;
- history remains intact.

Report transition contradiction count.

### 1.3 Active universe consistency
Verify live normative inventory accurately states:
- four axes;
- six memory classes;
- actual common-constraint count;
- no active `seven stores/classes` wording;
- no stale pre-remediation counts or aliases;
- no old AI-conversion wording;
- no old freshness wording.

Historical remediation text may mention prior counts if clearly historical and non-normative.

Report active inventory inconsistency count.

### 1.4 Exemplars 2 and 3
Verify:
- project assumption exemplar now uses four axes and remains non-canonical;
- financial calculation exemplar declares exactly one applicability mode;
- that mode is valid and appropriately bounded for the project-specific calculation;
- source-input versioning and re-derivation semantics remain intact.

Then verify all eight exemplars independently.

## 2. Validation harness credibility

Run if possible:

`python3 validation/phase_8_validation.py`

Also inspect `--verbose` and `--json` behavior if feasible.

Verify:
- result total matches the committed harness;
- exit code is non-zero on failure conditions;
- no unconditional pass constructs (`or True`, tautological checks, unreachable failure branches, hard-coded counters disconnected from discovered tests);
- PERSONAL isolation checks are semantic enough to catch organisational-to-PERSONAL propagation wording;
- state-transition checks compare actual permitted transitions against status-change effects;
- inventory counts are derived from source where practical;
- canonical exemplars are detected by semantic state, not by a field whose absence can hide them;
- local validator does not falsely claim to prove remote open-PR state;
- offline-vs-external verification boundary is explicit.

Return harness credibility HIGH / MEDIUM / LOW.

If external GitHub state is available, independently verify:
- branch HEAD;
- whether a PR exists for `architecture/phase-8-memory-canonical`;
- distinguish unrelated repository PRs from PRs on this branch.

Do not mark Phase 8 failed merely because an unrelated old PR exists elsewhere in the repository.

## 3. Identity and four-axis model

Verify exact separation:

`SOURCE != EVIDENCE != MEMORY ITEM != KNOWLEDGE CLAIM != CANONICAL RECORD != DECISION RIGHT != DECISION RECORD != ARTIFACT != MODEL != RUNTIME`

Verify four orthogonal knowledge axes:
- epistemic type;
- governance state;
- permanent origin/provenance;
- conflict flags.

Check:
- `AI_SUGGESTION` remains a narrowed proposal type, not origin;
- AI origin remains separate/permanent;
- adoption creates a new linked typed item;
- human acceptance is not evidence;
- `CONFLICT_DETECTED` compatibility mapping to upstream semantics remains safe;
- no authority changes epistemic truth type.

## 4. Scope graph and applicability

Compare Phase 8 scope graph against approved upstream baseline.

Require graph discrepancy count = 0.

Audit applicability modes:
- `INHERITABLE_TO_DESCENDANTS`;
- `CONDITIONALLY_APPLICABLE`;
- `NON_INHERITABLE`;
- `MANDATORY_WIDER_CONSTRAINT`;
-or exact semantic equivalents.

Verify:
- canonical status never inherits;
- applicability only propagates within valid descendant relationships in the same scope family;
- no upward flow;
- no sideways flow;
- mandatory wider constraints cannot be locally overridden without separate valid authority path;
- missing applicability mode has safe narrow interpretation;
- ancestor fallback after local retraction is explicit and mode-specific.

## 5. Canonical Decision integration

Verify final architecture for:
- `decision.canonical_knowledge_promotion`;
- `decision.canonical_knowledge_status_change`.

Required:
- upstream APPROVED and CANONICAL uses both preserved;
- promotion = positive successor path;
- status change = bounded no-successor downgrade/withdrawal path;
- `APPROVED_STATUS_WITHDRAWAL` transition now matches state model;
- `CANONICAL_RETRACTION` transition matches state model;
- scope/applicability narrowing and early expiry are bounded and do not create truth conversion;
- no duplicate authority;
- conflict resolution remains professional/review work, not Decision authority;
- Phase 8 cards no executable Right itself;
- future Phase 7 carding boundary remains explicit.

Report upstream semantic-regression count.

## 6. Canonical semantics

Verify canonicality remains:
- property of `(claim version, scope)`;
- scoped;
- versioned;
- effective-dated;
- evidence-bound;
- revocable/supersedable without history loss;
- not equal to global truth;
- not equal to visibility;
- not inherited as canonical state.

Stress-test simultaneous-validity cases:
- wider and narrower scope statements;
- conditional applicability;
- mandatory wider constraint plus local detail;
- retraction + ancestor fallback;
- sibling scope families including PERSONAL;
- direct project-under-organisation and programme/portfolio paths.

No incompatible statements may silently coexist without declared override/conflict/applicability semantics.

## 7. Memory classes

Verify final active classes are exactly:
- WORKING_MEMORY;
- EPISODIC_MEMORY;
- SEMANTIC_MEMORY;
- PREFERENCE_MEMORY;
- PROCEDURAL_MEMORY;
- AUDIT_MEMORY.

Check:
- no active `CANONICAL_MEMORY` semantics;
- class does not mutate when governance state changes;
- WORKING does not self-promote to durable organisational memory;
- EPISODIC does not imply present validity;
- PREFERENCE cannot override fact/law/evidence;
- PROCEDURAL grants no authority;
- AUDIT preserves history while legal deletion conflicts remain external governance concerns.

## 8. Freshness / conflict / provenance

Verify:
- item-level temporal facts are separate from use-context verdicts;
- bare undefined `STALE` is absent from Phase 8 freshness vocabulary;
- Phase 6 Review `STALE` remains separate;
- unresolved material conflicts block canonical promotion/decision-grade use where depended upon;
- immaterial conflicts remain visible but non-blocking;
- Enhanced Decision-Grade requires attributable materiality assessment for every open conflict;
- unassessed open conflict may default to material until assessed;
- provenance preserves direct/derived evidence, transformations, AI contribution, human edits, supersession, retraction, transfer;
- no silent provenance loss.

Report freshness ambiguity count and provenance-loss loophole count.

## 9. Sensitivity / retention / artifact / retrieval

Verify:
- sensitivity is orthogonal to scope/canonicality;
- canonical does not imply visibility;
- declassification is governed;
- derived/aggregated data can retain or increase sensitivity;
- artifact != knowledge claim;
- approved artifact != wholly canonical;
- replacing/deleting artifact does not rewrite canonical/audit history;
- stored != retrievable != selected != authoritative-for-task != canonical-for-scope;
- retrieval rank, similarity, recency, relevance, freshness, model confidence do not create authority;
- context absence is not evidence of supersession/nonexistence;
- stale != false;
- expired != deleted;
- superseded != erased;
- retracted != forgotten;
- retention hold/deletion conflicts remain governance/legal concerns, not silently resolved.

Report retrieval-governance leakage count.

## 10. Open questions

Independently re-adjudicate all 12 original Phase 8 open questions.

Questions #2, #3, #4 must receive special attention because prior audits repeatedly found them unresolved.

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 9+ / RUNTIME CONCERN

Human approval is not ready if #2, #3, or #4 remains materially unresolved.

## 11. Regression / non-runtime

Verify against `c72ef0399b3c7c2f272711918803f7bc08c70084`:
- Phase 3 approved Role changes = 0;
- Phase 4 approved Skill changes = 0;
- Phase 5 approved Workflow changes = 0;
- Phase 6 approved Handoff/Review changes = 0;
- Phase 7 approved Decision changes = 0;
- inherited approved context architecture changes = 0;
- upstream investigation read-only;
- all Phase 8 artifacts remain `PROPOSED`;
- no runtime/DB/API/UI/RAG/embedding/model-router/agent/IAM implementation;
- no real named holder assignment;
- no PR created for Phase 8 branch.

Validation tooling is allowed as architecture/test tooling only.

## 12. Approval threshold

Return `PASS` only if no material architecture issue remains.

Return `PASS WITH NON-BLOCKING NOTES` only if all notes are genuinely deferred/runtime/expansion matters and cannot cause scope, truth, authority, provenance, conflict, or canonical misuse.

Return `PASS WITH CHANGES` if one more bounded correction is required.

Return `FAIL` if any material architecture blocker remains.

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. FINAL BLOCKER RE-AUDIT
For PERSONAL leakage, withdrawal transition, active inventory, exemplars 2/3, and validation credibility: RESOLVED / NOT RESOLVED with exact evidence.

### C. SCOPE / PERSONAL ISOLATION
PASS / FAIL; scope-graph discrepancy count; sideways applicability leakage count; PERSONAL absorption leakage count; ancestor-fallback verdict.

### D. IDENTITY / FOUR-AXIS MODEL
PASS / FAIL; identity-collapse count; AI type-conversion loophole count; upstream compatibility verdict.

### E. GOVERNANCE-STATE MODEL
PASS / FAIL; transition contradiction count; exact APPROVED-withdrawal and CANONICAL-retraction destination semantics.

### F. CANONICAL DECISION INTEGRATION
PASS / FAIL; upstream semantic-regression count; final disposition of the two canonical Decision IDs; future carding boundary.

### G. CANONICAL SEMANTICS
PASS / FAIL; simultaneous-validity findings; applicability/inheritance verdict.

### H. MEMORY CLASSES
PASS / FAIL; active class count; duplication/alias count.

### I. FRESHNESS / CONFLICT / PROVENANCE
PASS / FAIL; freshness ambiguity count; materiality discrepancy count; provenance-loss loophole count.

### J. SENSITIVITY / ARTIFACT / RETRIEVAL
PASS / FAIL; retrieval-governance leakage count; visibility/retention findings.

### K. EIGHT EXEMPLARS
Each PASS / FAIL with one concise reason.

### L. OPEN QUESTIONS
All 12 independent dispositions.

### M. VALIDATION HARNESS
Exact command/result; credibility HIGH / MEDIUM / LOW; vacuous-test findings; local-vs-external scope verdict.

### N. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–7 changes, inherited context changes, Phase 8 status, runtime status, Phase 8 branch PR status.

### O. REMAINING BLOCKERS
If none: NONE.

### P. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 8
- READY AFTER LISTED CHANGES
- NOT READY

### Q. EXPANSION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED EXPANSION
- SAFE FOR CONTROLLED BATCH EXPANSION
- SAFE FOR MASS EXPANSION

Do not modify anything.