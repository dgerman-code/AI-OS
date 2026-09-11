# Codex Prompt — Final Independent Phase 8 Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-8-memory-canonical`
Audit baseline commit: `4a20429c94e4c881a303a58b7fd62289a4131c26`
Phase 7 approval-record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`
Original Phase 8 foundation baseline: `3aea5890d81d0a954d8057d118facf54a365289d`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 8 APPROVED or CANONICAL.

The prior independent Phase 8 audit returned `FAIL` with five HIGH and three MEDIUM findings. The remediation commit claims all eight are resolved and adds a deterministic validation harness reporting `95/95 PASS`.

Treat every remediation claim as untrusted until independently verified.

Read at minimum:
- `architecture/memory-canonical-governance.md`
- `architecture/context-hierarchy.md` from the approved upstream baseline as needed
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
- relevant approved Phase 3–7 artifacts, especially the Knowledge & Evidence Steward Role and Phase 7 Decision architecture.

## 1. Re-audit the exact prior findings

### H1 — Scope hierarchy regression
Verify the Phase 8 scope graph now exactly preserves approved upstream structure and terminology, including where applicable:
- GLOBAL;
- ORGANISATION;
- INDEPENDENT BUSINESS / VENTURE;
- PROGRAMME;
- PORTFOLIO;
- PRODUCT;
- PROJECT, including direct-under-organisation and programme/portfolio paths where upstream permits them;
- PERMANENT FUNCTION / BUSINESS AREA;
- OPERATIONAL WORKSTREAM;
- WORKSTREAM;
- TASK;
- PERSONAL as a separate scope family if that remains the model.

Do not accept prose claims. Compare against approved upstream source.
Report exact hierarchy/graph discrepancies count.

### H2 — Unbounded downward applicability
Verify four-mode applicability semantics or equivalent are now explicit and sufficient.

Required outcomes:
- canonical status never inherits;
- applicability propagates only by explicit declared mode and conditions;
- missing mode has a safe narrow interpretation;
- mandatory wider obligations cannot be overridden by local canonical statements;
- local exception requires a separately valid authority path where upstream allows it;
- no upward/sideways/PERSONAL leakage;
- transfer remains explicit, non-transitive, revalidated, and does not carry canonical or Review status;
- ancestor fallback after local retraction is explicit and mode-specific, with no silent fallback.

Stress-test law/regulation, contract, safety rule, binding governance standard, organisation policy, project exception, conditional programme parameter, and non-inheritable project parameter.
Report applicability leakage count.

### H3 — Canonical identity duplication
Verify `CANONICAL_MEMORY` is no longer an active memory class and that canonicality is represented only as governance state / Canonical Record status.

Verify the memory classes are semantically stable through promotion, supersession and retraction.
Check all templates/exemplars/universe for inconsistent aliases or residual active semantics.
Report duplication/alias count.

### H4 — AI origin/type transition loophole
Verify:
- origin is a separate permanent provenance axis;
- `AI_SUGGESTION` cannot be converted in place to another epistemic type by human acceptance, review, approval or authority;
- adoption creates a new linked item whose type is justified by its own evidence/reasoning;
- human acceptance alone is not evidence;
- original proposal remains historical;
- AI origin remains visible in successor lineage;
- all relevant architecture, templates, provenance rules and exemplars agree.

Explicitly adjudicate whether retaining `AI_SUGGESTION` as a narrowed epistemic type plus separate origin axis is coherent and upstream-compatible.
Report AI type-conversion loophole count.

### H5 — Approved upstream `decision.canonical_knowledge_status_change` meaning
Verify the remediation preserves the approved upstream use for material whose current status derives from explicit human `APPROVED` **or** `CANONICAL` decision.

Audit the proposed boundary:
- `decision.canonical_knowledge_promotion` = positive successor promotion;
- `decision.canonical_knowledge_status_change` = governed status downgrade/change without successor, covering at least `APPROVED_STATUS_WITHDRAWAL`, `CANONICAL_RETRACTION`, bounded scope/applicability narrowing, and early expiry where semantically justified.

Check:
- no upstream Role meaning is silently narrowed;
- no duplicate/unbounded authority is created;
- successor supersession remains an effect of successor promotion;
- truth conversion/conflict resolution remains outside Decision authority;
- Phase 8 does not itself card an executable Right;
- future Phase 7 carding/eligibility questions are explicitly bounded.

Report upstream semantic-regression count.

### M1 — Freshness-axis ambiguity
Verify item-level temporal facts are distinct from use-context usability verdicts.

Required:
- as-of / last-verified / refresh interval / review-by / expiry / refresh trigger remain item-level metadata;
- use-context verdict is evaluated per use and not persisted as the item's permanent truth;
- same item can yield different verdicts for different tasks at the same time;
- undefined bare `STALE` is absent from Phase 8 freshness vocabulary unless explicitly defined as a distinct item-age condition;
- Phase 6 Review status `STALE` remains unaffected and clearly separate;
- exemplar 8 and templates are consistent.

Report freshness-model ambiguity count.

### M2 — Criticality conflict-materiality inconsistency
Verify one normalized rule now governs all files:
- unresolved material conflict blocks canonical promotion / decision-grade use where the claim or decision depends on the contested point;
- immaterial conflicts remain visible but do not automatically block;
- Enhanced Decision-Grade requires explicit attributable materiality assessment for every open conflict;
- unassessed open conflict may default to material until assessed;
- materiality is not inferred from retrieval rank, model confidence, source count or silence.

Report rule discrepancy count across architecture, common constraints, promotion governance, conflict/provenance model, templates and exemplars.

### M3 — Self-check reproducibility
Independently inspect and, if execution is available, run:

`python3 validation/phase_8_validation.py`

Verify:
- deterministic exit code and reported total;
- file discovery is not merely a hard-coded allowlist where discovery is appropriate;
- upstream baseline checks actually read approved source rather than self-authored Phase 8 prose;
- tests cover the eight prior findings semantically enough to catch regression;
- tests do not merely assert string presence where opposite semantics could still pass;
- no test excludes remediation records in a way that hides live normative defects;
- prior test-defect fixes were stricter, not weaker.

Report exact result and credibility: HIGH / MEDIUM / LOW.

## 2. Recheck Phase 8 identity/state architecture

Verify exact separation remains intact:

`SOURCE != EVIDENCE != MEMORY ITEM != KNOWLEDGE CLAIM != CANONICAL RECORD != DECISION RIGHT != DECISION RECORD != ARTIFACT != MODEL != RUNTIME`

Verify the four-axis model after remediation:
- epistemic type;
- governance state;
- permanent origin/provenance axis;
- conflict flag(s).

Check compatibility mapping for upstream:
- `FACT` -> `FACT_CLAIM`;
- `CONFLICT_DETECTED` upstream state-like usage -> orthogonal conflict flag;
- `AI_SUGGESTION` upstream use -> narrowed proposal type + origin lineage;
- `APPROVED`, `CANONICAL`, `SUPERSEDED`, `UNKNOWN` semantics unchanged.

Any identity collapse or silent upstream semantic change is blocking.

## 3. Canonical semantics and simultaneous validity

Verify `CANONICAL` remains property of `(claim version, scope)` and not global truth.

Stress-test simultaneous active statements under:
- different scopes;
- conditional applicability;
- mandatory wider constraints;
- nearer-scope overrides;
- different effective periods;
- retraction with ancestor fallback;
- direct project under organisation vs project under programme/portfolio.

PASS only if incompatible active statements cannot silently coexist without declared override/conflict/applicability semantics.

## 4. Canonical promotion preconditions

Verify promotion remains version-specific, scope-specific, evidence-bound and competence/review/Decision-gated where required.

Check legitimate canonical candidates:
- FACT_CLAIM;
- CALCULATION;
- INFERENCE;
- approved method/policy/definition/parameter via appropriate epistemic type and governance route.

Verify personal preference itself is never promoted by absorption, but a new organisational method/policy/parameter can be created through governed adoption.

No Decision Right may create expertise or convert UNKNOWN/ASSUMPTION into FACT.

## 5. Conflict and post-promotion use

Verify conflict remains first-class and history-preserving.

Stress-test a canonical statement that later receives material contradictory evidence.

Architecture must make clear:
- canonical status may remain historically/currently recorded while conflicted;
- use may become blocked where material;
- resolution/review/refresh/retraction paths are explicit enough that downstream runtime does not invent policy;
- losing evidence/dissent remains attached;
- conflict never clears through silence/time/repetition.

## 6. Memory classes

Verify the final six classes:
- WORKING_MEMORY;
- EPISODIC_MEMORY;
- SEMANTIC_MEMORY;
- PREFERENCE_MEMORY;
- PROCEDURAL_MEMORY;
- AUDIT_MEMORY.

Check:
- classes describe retention/use character, not governance status;
- class does not mutate on canonical promotion/supersession/retraction;
- WORKING does not silently become durable organisational memory;
- EPISODIC does not imply current validity;
- PREFERENCE cannot override fact/law/evidence;
- PROCEDURAL does not grant authority;
- AUDIT append/history semantics do not silently defeat legal deletion obligations; legal conflicts remain external authority concerns.

## 7. Sensitivity / visibility / retention

Verify:
- sensitivity remains orthogonal to scope/canonicality;
- canonical does not imply visibility;
- declassification is governed;
- derived/aggregated records may retain/increase sensitivity;
- personal/confidential evidence can support a canonical statement without making evidence broadly visible;
- stale != false;
- expired != deleted;
- superseded != erased;
- retracted != forgotten;
- archived != gone;
- retention hold/deletion conflict is not silently solved by Phase 8.

## 8. Artifact/retrieval boundaries

Verify:
- artifact != claim;
- approved artifact != wholly canonical;
- artifact replacement/deletion does not rewrite knowledge history;
- generated decision-grade artifact uses currently applicable canonical versions where required;
- stored != retrievable != selected != authoritative-for-task != canonical-for-scope;
- retrieval rank, similarity, recency, relevance, freshness or model confidence cannot create authority;
- absence from context is not evidence of supersession/nonexistence.

Report retrieval-governance leakage count.

## 9. Eight exemplars

Audit all eight after remediation independently:
1. verified organisational fact;
2. project assumption;
3. financial calculation;
4. conflicting external sources;
5. superseded canonical parameter;
6. personal preference isolation;
7. retracted statement / ancestor fallback;
8. stale item / per-use verdict.

Return PASS/FAIL for each with a concise reason.

## 10. Open questions

Independently re-adjudicate all 12.

The prior audit marked #2, #3, #4, #7, #9, #12 as MUST RESOLVE BEFORE HUMAN APPROVAL.

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 9+ / RUNTIME CONCERN

Do not accept the producer's label without checking the actual rule.

## 11. Regression and non-runtime boundary

Verify against `c72ef0399b3c7c2f272711918803f7bc08c70084`:
- Phase 3 approved Role semantic/file changes = 0;
- Phase 4 approved Skill semantic/file changes = 0;
- Phase 5 approved Workflow semantic/file changes = 0;
- Phase 6 approved Handoff/Review semantic/file changes = 0;
- Phase 7 approved Decision semantic/file changes = 0;
- inherited approved context architecture files unchanged;
- upstream evidence inspection read-only;
- no runtime/DB/API/UI/RAG/embedding/model-router/agent/IAM implementation;
- all Phase 8 artifacts remain `PROPOSED`;
- no named real human or organisation assignment;
- no PR.

Validation tooling under `validation/` is allowed only if it is architecture/test tooling and not production runtime.

## 12. Human-approval threshold

Return `PASS` only if no material architecture issue remains.

Return `PASS WITH NON-BLOCKING NOTES` only if all remaining notes are genuinely Phase 9+/runtime or selective expansion concerns and cannot cause truth, authority, scope, provenance, conflict, or canonical misuse in the Phase 8 architecture.

Return `PASS WITH CHANGES` if another bounded Phase 8 correction is needed.

Return `FAIL` if any HIGH blocker remains or if upstream semantics/regression is unresolved.

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. PRIOR FINDINGS RE-AUDIT
For H1–H5 and M1–M3: RESOLVED / NOT RESOLVED + exact evidence and any residual issue.

### C. SCOPE GRAPH / APPLICABILITY
PASS / FAIL; graph discrepancy count; applicability leakage count; ancestor-fallback verdict.

### D. MEMORY / IDENTITY MODEL
PASS / FAIL; memory-class duplication/alias count; four-axis-model verdict.

### E. AI ORIGIN / EPISTEMIC MODEL
PASS / FAIL; type-conversion loophole count; explicit verdict on narrowed `AI_SUGGESTION` + permanent origin axis.

### F. CANONICAL DECISION INTEGRATION
PASS / FAIL; upstream semantic-regression count; final verdict on the two canonical Decision IDs and future carding boundary.

### G. FRESHNESS / CONFLICT MATERIALITY
PASS / FAIL; freshness ambiguity count; materiality-rule discrepancy count.

### H. CANONICAL SEMANTICS / CONFLICT USE
PASS / FAIL; simultaneous-validity findings; post-promotion material-conflict verdict.

### I. PROVENANCE / SENSITIVITY / RETENTION
PASS / FAIL; provenance-loss loophole count; visibility/deletion/retention findings.

### J. ARTIFACT / RETRIEVAL BOUNDARY
PASS / FAIL; retrieval-governance leakage count.

### K. EIGHT EXEMPLARS
Each PASS / FAIL with one concise reason.

### L. OPEN QUESTIONS
All 12 independent dispositions.

### M. VALIDATION HARNESS
Exact command/result if run; credibility HIGH / MEDIUM / LOW; any vacuous-test findings.

### N. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–7 changes, inherited context-architecture changes, Phase 8 status, runtime/PR status.

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