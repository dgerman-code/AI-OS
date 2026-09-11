# Codex Prompt — Independent Phase 8 Memory / Canonical Governance Foundation Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-8-memory-canonical`
Audit baseline commit: `3aea5890d81d0a954d8057d118facf54a365289d`
Phase 7 human-approval record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 8 APPROVED or CANONICAL.

This is an **independent architecture audit** of the Phase 8 foundation produced after Phase 7 human approval.

The producer reports 20 files, 116/116 self-check PASS, no Phase 3–7 semantic changes, no runtime implementation, and readiness for independent audit. Treat all producer claims as untrusted until verified.

Read at minimum:

- `architecture/memory-canonical-governance.md`
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
- approved Phase 3–7 artifacts as necessary for regression and forward-reference validation.

Audit the architecture, not prose quality.

---

## 1. Identity separation

Verify the architecture preserves:

`SOURCE != EVIDENCE != MEMORY ITEM != KNOWLEDGE CLAIM != CANONICAL RECORD != DECISION RIGHT != DECISION RECORD != ARTIFACT != MODEL != RUNTIME`

PASS only if:
- each identity has a distinct semantic purpose;
- no object silently acquires another object's authority/state;
- artifact approval cannot make contained claims canonical;
- memory retention cannot imply truth;
- evidence cannot imply adoption/approval;
- Decision Right cannot manufacture professional truth;
- canonical record is not equivalent to source/evidence/artifact;
- model/runtime cannot own or self-promote governance state.

Report identity-collapse loophole count.

---

## 2. Three-axis knowledge model

Audit the proposed split into:
- epistemic type;
- governance state;
- conflict flag(s).

Verify whether the split is coherent and complete.

Stress-test:
- `ASSUMPTION + APPROVED`;
- `FACT_CLAIM + DRAFT + CONFLICT_DETECTED`;
- `CALCULATION + CANONICAL`;
- `INFERENCE + CANONICAL`;
- `AI_SUGGESTION + REVIEWED`;
- `UNKNOWN + APPROVED`;
- `RETRACTED + CONFLICT_DETECTED`;
- `SUPERSEDED + CONFLICT_DETECTED`.

Check whether any state/type combination becomes semantically impossible, contradictory, or authority-leaking.

Pay special attention to the producer's decision to move `CONFLICT_DETECTED` out of the governance-state list into an orthogonal flag. Determine whether this preserves all Phase 2–7 semantics or creates incompatibility with upstream references that treated it as a state-like label.

Required disposition:
- PASS;
- MUST CHANGE BEFORE HUMAN APPROVAL;
- SAFE WITH EXPLICIT COMPATIBILITY MAPPING.

---

## 3. Epistemic-type transitions

Audit the claim that epistemic type is never changed by authority and changes only through evidence as a new linked item.

Verify:
- `UNKNOWN` cannot be authority-promoted to `FACT_CLAIM`;
- `ASSUMPTION` cannot become `FACT_CLAIM` by approval, age, reuse, repetition or promotion;
- `AI_SUGGESTION` cannot become FACT merely by human acceptance;
- evidence-based reclassification creates a new linked knowledge item/version rather than silently relabeling history;
- calculations/inferences remain distinguishable from facts even when canonical.

Flag any path that conflates acceptance with truth.

---

## 4. Governance-state transitions

Audit permitted and forbidden transitions among:

`DRAFT`, `REVIEWED`, `APPROVED`, `CANONICAL`, `SUPERSEDED`, `RETRACTED`, `REJECTED`.

Check:
- whether `APPROVED` and `CANONICAL` are clearly non-equivalent;
- whether direct `DRAFT -> CANONICAL` is prohibited or conditionally governed;
- whether `REVIEWED -> CANONICAL` has a mandatory promotion act rather than implicit promotion;
- whether `SUPERSEDED` and `RETRACTED` are terminal or can become applicable again only through a new linked record;
- whether `REJECTED` is historically preserved;
- whether rollback creates new history rather than mutating old state;
- whether governance transitions are claim-version-specific and scope-specific.

Report transition loophole count.

---

## 5. Canonical semantics

Audit the definition:

`CANONICAL = property of (claim version, scope)`.

PASS only if canonicality is:
- scoped;
- versioned;
- effective-dated;
- evidence-bound;
- revocable/supersedable without history loss;
- not equivalent to global truth;
- not equivalent to visibility;
- not inherited as canonical status across scopes.

Stress-test whether multiple simultaneously valid canonical statements can coexist for:
- different scopes;
- different time periods;
- different conditions;
- overlapping scopes;
- the same subject under different semantic types.

Identify any ambiguity that could create two active incompatible canonical statements without a declared conflict/override relation.

---

## 6. Scope hierarchy and applicability

Audit:

`GLOBAL -> ORGANISATION -> PROGRAMME / PORTFOLIO / PRODUCT -> PROJECT -> WORKSTREAM -> TASK`

with `PERSONAL` as a separate scope family.

The producer states applicability may flow downward while authority never flows, and a nearer canonical statement overrides a wider one if the override is named.

Stress-test hard:
- organisation policy vs project exception;
- project assumption vs organisation fact;
- programme parameter reused in two projects;
- same-name entity in two organisations;
- personal preference affecting organisational artifact generation;
- project-local canonical statement becoming visible in sibling project;
- global standard whose applicability is conditional rather than universal;
- product and project scopes that are not strict parent/child in real organisations.

Required checks:
- no upward leakage;
- no sideways leakage;
- no PERSONAL -> organisational absorption;
- applicability inheritance is not mistaken for canonical inheritance;
- nearer-scope override cannot silently contradict mandatory wider-scope law/policy;
- cross-scope transfer requires explicit governed act;
- transfer is non-transitive;
- transfer carries neither canonical status nor Review satisfaction;
- revalidation requirement is explicit.

Pay special attention to whether the phrase **“applicability flows down”** is too broad. If some canonical items must be non-inheritable or conditionally inheritable, determine whether the architecture already supports that or needs an explicit applicability mode/property.

This is a potential blocker; adjudicate explicitly.

---

## 7. Canonical promotion and Phase 7 forward references

Audit the resolution of:
- `decision.canonical_knowledge_promotion`;
- `decision.canonical_knowledge_status_change`.

Producer proposes two bounded authority patterns:
- promotion where a successor/positive position exists;
- status withdrawal/retraction where no successor exists.

Verify:
- upstream traceability for both IDs is preserved;
- duplicate authority is not reintroduced under different names;
- supersession is an effect of successor promotion, not a free-standing kill authority;
- correction is successor promotion, not in-place edit;
- scope expansion is a new scope-specific promotion;
- conflict resolution is professional/review work and does not by itself exercise Decision authority;
- refresh/revalidation does not silently create canonical status;
- withdrawal/retraction cannot silently imply the opposite fact;
- no executable Right is accidentally created by Phase 8 architecture alone;
- required future Phase 7 carding is explicit and bounded.

Critically audit the proposed required separation:
`decision.canonical_knowledge_promotion` vs `decision.exceptional_progression`.

Determine whether this is sufficient, too broad, too narrow, or missing other required separation relationships (for example conflict-resolution reviewer vs canonical promoter, source owner vs promoter, retraction vs successor promotion, or promotion vs artifact publication).

Do not invent separation unless control rationale requires it.

---

## 8. Promotion preconditions

Verify all promotion preconditions are sufficient and non-circular.

At minimum test:
- source/evidence sufficiency;
- provenance completeness;
- material conflict status;
- Role competence for professional conclusion;
- Review requirement;
- Decision Right requirement;
- scope identity;
- exact version identity;
- freshness for intended use;
- criticality-dependent rigor.

Check whether a claim can become canonical with:
- no direct source but defensible inference;
- a calculation dependent on assumptions;
- a policy/methodology that is normative rather than factual;
- third-party statement adopted as organisational position;
- stale evidence that is still historically correct;
- unresolved non-material conflict.

Flag any blanket rule that incorrectly blocks legitimate canonical policy/methodology/parameters or permits weak evidence for load-bearing facts.

---

## 9. Types eligible for canonicality

Producer indicates canonicalization may apply to `FACT_CLAIM`, `CALCULATION`, `INFERENCE`, and procedural method as method; `PREFERENCE` is never canonical.

Audit whether this type boundary is coherent.

Specifically test:
- organisational policies;
- definitions;
- approved methodologies;
- operational parameters;
- legal interpretations;
- financial model outputs;
- planning assumptions;
- user preferences;
- organisational conventions/preferences.

Determine whether `PREFERENCE` being **never canonical** is correctly scoped to personal preference memory only, or whether it accidentally prevents an organisation from governing a convention/standard that originated as a preference.

PASS only if the architecture clearly provides a governed path to reclassify/adopt such a convention as a policy/method/parameter without pretending the personal preference itself became canonical.

---

## 10. Conflict model

Audit all seven reported conflict classes:
- source;
- claim;
- version;
- scope;
- temporal;
- authority;
- identity.

Verify:
- conflict is first-class and preserved;
- later != automatically better;
- higher authority != automatically truer evidence;
- unresolved material conflict blocks promotion;
- losing evidence/history remains attached;
- dissent can remain visible;
- resolution records rationale;
- conflict does not clear through silence/repetition/time;
- conflict discovered after promotion is visible without silent de-canonicalization.

Stress-test the last rule: if a canonical statement becomes materially contradicted after promotion, can it remain canonical and conflicted indefinitely while still being consumed as authoritative? The architecture must distinguish:
- still canonical but use-blocked;
- still canonical and usable with warning;
- retraction required;
- refresh/review required.

If post-promotion material conflict has no clear usage/gate consequence, treat as a potential blocker.

---

## 11. Provenance and lineage

Verify the lineage model can trace:

`SOURCE -> EVIDENCE -> CLAIM/CALCULATION/INFERENCE -> REVIEW -> DECISION (where required) -> CANONICAL VERSION`

Audit:
- direct evidence;
- derived evidence;
- transformation lineage;
- calculation lineage;
- human edits;
- AI contribution;
- external sources;
- artifact relationships;
- unknown/missing lineage steps.

Check that:
- unknown provenance is recorded as unknown rather than omitted;
- transformations such as currency conversion, rebasing, rounding and aggregation are lineage-bearing operations;
- AI contribution remains visible after human editing;
- lineage survives supersession/retraction/transfer;
- a downstream statement cannot silently cite a moving target such as “current tariff assumption” instead of a versioned source.

Report provenance-loss loophole count.

---

## 12. Memory classes

Audit the seven architecture classes:
- WORKING;
- EPISODIC;
- SEMANTIC;
- PREFERENCE;
- PROCEDURAL;
- CANONICAL;
- AUDIT.

Verify the producer's decision to keep them architecture classes rather than registry types.

Check:
- no hidden storage architecture is implied;
- classes are not mutually exclusive when they should not be;
- `CANONICAL` as memory class does not duplicate governance state in a confusing way;
- `AUDIT` append-oriented semantics are coherent with legal correction/deletion obligations;
- `EPISODIC` does not imply present validity;
- `PROCEDURAL` does not grant authority;
- `WORKING` cannot silently become durable organisational memory;
- `PREFERENCE` cannot override fact/law/evidence.

Potential issue to adjudicate explicitly: does naming a `CANONICAL` memory class create identity duplication with `CANONICAL` governance state/canonical record, or is the distinction clean enough?

---

## 13. Freshness, staleness, expiry, supersession, retraction, archival

Audit lifecycle distinctions.

Verify at minimum:
- stale != false;
- expired != deleted;
- superseded != erased;
- retracted != forgotten;
- archived != gone;
- retention hold can block ordinary deletion;
- deletion eligibility is explicit, not default;
- audit/provenance retention preserves accountability;
- legal conflicts around erasure/retention are deferred to proper authority, not silently resolved here.

Stress-test whether “staleness depends on use” is represented at the right layer. Determine whether staleness belongs partly to the item and partly to the use-context, and whether the architecture prevents contradictory permanent labels on the same item.

Check whether `review-by`, expiry and refresh triggers are sufficiently separate.

---

## 14. Sensitivity / visibility boundary

Audit the nine sensitivity classes and their relationship to scope and canonicality.

PASS only if:
- sensitivity is orthogonal to canonicality;
- canonical does not imply visible;
- scope does not imply access permission;
- declassification is governed;
- derived/aggregated data may retain or increase sensitivity;
- third-party restrictions survive citation/summary/aggregation where required;
- personal/confidential evidence can support a canonical statement without forcing the evidence itself to become broadly visible.

Do not require IAM implementation.

---

## 15. Artifact / knowledge boundary

Verify:
- one artifact may contain heterogeneous claims/states;
- approved artifact != canonical artifact wholesale;
- canonical knowledge can appear in multiple artifacts;
- artifact replacement does not rewrite canonical history;
- artifact deletion does not automatically delete knowledge/audit history;
- generated decision-grade artifacts must use currently applicable canonical versions where required;
- open assumptions/conflicts remain visible at point of reliance.

Stress-test partial-document approval and mixed canonical/non-canonical content.

---

## 16. Retrieval / RAG boundary

Audit the five properties:
- stored;
- retrievable;
- selected into context;
- authoritative for task;
- canonical for scope.

PASS only if no retrieval/ranking mechanism can create authority.

Verify:
- absence from context != evidence of absence/supersession;
- top-ranked != canonical;
- fresh != true;
- relevant != authoritative;
- canonical-but-not-retrieved remains required where task governance says so;
- architecture remains retrieval-engine-agnostic.

Report retrieval-governance leakage count.

---

## 17. AI / human correction boundary

Verify:
- AI can propose but cannot self-promote;
- AI can raise a conflict flag but cannot clear one without governed resolution;
- human edit preserves AI/source lineage;
- admin override cannot bypass evidence/review/authority;
- canonical correction creates new version;
- rollback creates a new governed applicability act;
- no hidden “trusted admin” shortcut exists.

Check whether a human adopting an AI-authored claim requires a new epistemic item/type or whether lineage + governance state is enough. Flag ambiguity if AI_SUGGESTION as epistemic type would otherwise remain forever even after evidence-supported human adoption.

This is an important conceptual test: does `AI_SUGGESTION` describe origin or epistemic nature? If origin, it may belong in provenance rather than epistemic type. Adjudicate explicitly.

---

## 18. Criticality rigor

Audit use of existing criticality bands.

Verify higher criticality increases:
- evidence depth;
- review independence;
- provenance completeness;
- freshness rigor;
- conflict tolerance;
- promotion gate rigor;
- authority/cardinality where Phase 7 requires.

But verify criticality does **not**:
- change truth;
- change identity;
- change the same claim's epistemic type;
- create authority by itself.

Check whether blanket rule “any conflict bearing on the claim blocks” at Enhanced Decision-Grade is too broad for clearly immaterial disputes.

---

## 19. Canonical-record semantic model

Audit required fields and semantic sufficiency.

Verify the Canonical Record can preserve:
- stable ID;
- subject identity;
- scope;
- exact statement;
- semantic type;
- evidence refs;
- provenance;
- author/contributor origin;
- Review refs/status;
- Decision refs where required;
- effective date;
- expiry/review-by;
- version;
- supersession links;
- conflict links;
- uncertainty/limitations;
- applicability conditions;
- status;
- promotion/change/retraction reason;
- governance-owner class;
- audit history;
- sensitivity metadata;
- freshness/use constraints if required.

Flag any missing field that would force runtime to invent governance semantics later.

---

## 20. Exemplars

Audit all eight exemplars independently:

1. verified organisational fact promoted to canonical;
2. project assumption remaining non-canonical;
3. financial calculation with lineage;
4. conflicting external sources blocking promotion;
5. superseded canonical parameter;
6. personal preference not leaking to organisational canonical knowledge;
7. retracted canonical statement with history preserved;
8. stale canonical item requiring refresh before decision-grade use.

For each report PASS/FAIL and concise reason.

Check exemplar consistency against architecture, not merely whether the prose sounds plausible.

---

## 21. Open questions — independent disposition

Independently adjudicate all 12 producer questions.

Producer claims 11/12 are `RESOLVED IN FOUNDATION`, only runtime/storage/IAM is deferred.

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 9+ / RUNTIME CONCERN

Pay strongest attention to:
1. canonical status attached to claim/record/both;
2. multiple valid scoped statements;
3. cross-scope applicability/inheritance;
4. normalization of the two canonical Decision IDs;
5. eligible canonical semantic types;
6. calculations after input changes;
7. stale-but-not-false handling;
8. external evidence vs internal canonical conflict;
9. retraction vs supersession;
11. preference/procedural canonicality;
12. minimum evidence by criticality.

If even one is materially unresolved in a way that permits authority/truth/scope leakage, mark it MUST RESOLVE BEFORE HUMAN APPROVAL.

---

## 22. Upstream compatibility and regression

Verify exact changes from Phase 7 human-approval record baseline.

Required:
- Phase 3 Role semantic changes = 0;
- Phase 4 Skill architecture/mapping changes = 0;
- Phase 5 Workflow semantic changes = 0;
- Phase 6 Handoff/Review semantic changes = 0;
- Phase 7 Decision Rights semantic changes = 0;
- no approved upstream file silently edited;
- no Role authority leakage;
- no Review-state rewrite;
- no Decision Right creation inside Phase 8;
- no runtime/DB/API/UI/RAG/embedding/model-router/agent/IAM implementation;
- all Phase 8 artifacts remain `PROPOSED`;
- no PR.

Audit especially compatibility mappings for earlier labels:
- `FACT` vs `FACT_CLAIM`;
- `CONFLICT_DETECTED` state-like upstream usage vs Phase 8 flag;
- `APPROVED`, `CANONICAL`, `SUPERSEDED`, `UNKNOWN`, `AI_SUGGESTION`.

No approved upstream semantic meaning may be silently changed just because Phase 8 refines the model.

---

## 23. Universe / completeness

Audit `knowledge/master-knowledge-governance-universe.md`.

Verify all major governance concepts are accounted for and classifications are non-overlapping enough to be usable.

Look for missing first-class concepts such as:
- applicability mode/inheritance behavior;
- evidence sufficiency;
- revalidation requirement;
- canonical gap/open-position state after retraction;
- use-block after material conflict;
- governed adoption of external statement;
- entity identity resolution;
- lineage incompleteness;
- deletion/retention legal hold conflict.

Do not demand a registry card for every concept; determine whether architecture coverage is sufficient.

---

## 24. Self-check quality

Inspect `reviews/phase-8-foundation-self-check.md` and the underlying validation logic if present.

Verify:
- 116/116 claim is reproducible in principle;
- tests are not vacuous/string-presence-only where semantic validation is claimed;
- the three producer-reported test defects were replaced by stricter checks rather than weakened;
- all required files are discovered from filesystem/registry rather than hard-coded where appropriate;
- no known architecture concern was marked PASS merely because it was listed as an open question.

Report self-check credibility as HIGH / MEDIUM / LOW.

---

## 25. Blocker policy

Treat as blocking before human approval if any of the following exist:

- silent cross-scope leakage;
- canonical inheritance ambiguity that can cause wrong-scope authority;
- AI/model/retrieval path to self-canonicalization;
- approval/authority path that changes epistemic truth state;
- unresolved material conflict can be silently ignored for canonical use;
- canonical record can be silently overwritten;
- Phase 7 Decision Right normalization creates duplicate or unbounded authority;
- upstream Phase 3–7 semantics are changed without explicit reapproval;
- identity duplication makes memory class / governance state / canonical record ambiguous in a way runtime would have to invent;
- provenance can be lost silently;
- personal data/preferences can silently become organisational canonical knowledge;
- post-promotion material conflict has no governed use consequence;
- a “resolved” open question actually contains an unresolved authority/truth/scope loophole.

---

# Required final output

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. HIGH / MEDIUM FINDINGS
List all HIGH and MEDIUM findings with exact files/sections and why they matter. If none: NONE.

### C. IDENTITY / THREE-AXIS MODEL
PASS / FAIL; identity-collapse count; disposition of `CONFLICT_DETECTED`; disposition of `AI_SUGGESTION` as epistemic type vs provenance-origin concern.

### D. STATE / TYPE TRANSITIONS
PASS / FAIL; illegal shortcut count; any ambiguous reclassification paths.

### E. SCOPE / ISOLATION / APPLICABILITY
PASS / FAIL; leakage count; explicit verdict on whether “applicability flows down” is sufficiently bounded or needs an applicability-mode refinement.

### F. CANONICAL SEMANTICS
PASS / FAIL; version/scope/time/conflict handling; simultaneous-validity findings.

### G. CANONICAL PROMOTION / PHASE 7 INTEGRATION
PASS / FAIL; final disposition of the two canonical Decision IDs; missing/overbroad separation relationships if any.

### H. CONFLICT / PROVENANCE
PASS / FAIL; post-promotion material-conflict handling; provenance-loss loophole count.

### I. MEMORY CLASSES
PASS / FAIL; explicit verdict on `CANONICAL` memory class duplication risk and PREFERENCE/PROCEDURAL boundaries.

### J. FRESHNESS / RETENTION / SENSITIVITY
PASS / FAIL; lifecycle ambiguities and visibility/confidentiality boundary.

### K. ARTIFACT / RETRIEVAL / AI BOUNDARIES
PASS / FAIL; retrieval-governance leakage count; AI-origin/adoption finding.

### L. CRITICALITY
PASS / FAIL; any overbroad or under-rigorous rule.

### M. CANONICAL RECORD MODEL
PASS / FAIL; missing semantic fields if any.

### N. EIGHT EXEMPLARS
Each PASS / FAIL with one concise reason.

### O. OPEN QUESTIONS
All 12 independent dispositions.

### P. UPSTREAM / NON-RUNTIME REGRESSION
Phase 3–7 changes, Phase 8 status, runtime/PR status, compatibility-mapping findings.

### Q. SELF-CHECK CREDIBILITY
HIGH / MEDIUM / LOW + concise reason.

### R. REMAINING BLOCKERS
If none: NONE.

### S. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 8
- READY AFTER LISTED CHANGES
- NOT READY

### T. NEXT CARDING / EXPANSION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED EXPANSION
- SAFE FOR CONTROLLED BATCH EXPANSION
- SAFE FOR MASS EXPANSION

Do not modify anything.