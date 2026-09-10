# Claude Code Prompt — Phase 8 Memory / Canonical Governance Foundation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-8-memory-canonical`
Start baseline: Phase 7 human-approval record commit `c72ef0399b3c7c2f272711918803f7bc08c70084`
Approved Phase 7 architecture baseline: `cedee2cfd1a959489585eb61acd975b4f7c65c84`

Build the **Phase 8 Memory / Canonical Governance foundation**.

This is architecture and registry work only.

Do NOT implement runtime memory, vector DB, embeddings, Supabase schemas, APIs, UI, retrieval pipelines, agents, model routing, storage engines, search ranking, access-control code, or orchestration.
Do NOT modify approved Phase 3–7 semantics except where Phase 8 must resolve explicit forward references from those phases.
Do NOT create a PR.
Do NOT mark Phase 8 APPROVED or CANONICAL.
All new Phase 8 artifacts must be `PROPOSED`.

---

# 1. Core identity separation

Make the following separation explicit and normative:

`SOURCE != EVIDENCE != MEMORY ITEM != KNOWLEDGE CLAIM != CANONICAL RECORD != DECISION RIGHT != DECISION RECORD != ARTIFACT != MODEL != RUNTIME`

At minimum distinguish:

- raw/source material;
- extracted evidence;
- remembered context;
- asserted claim;
- derived inference;
- approved canonical statement;
- canonical subject/record;
- superseded canonical statement;
- conflicting information;
- unresolved/unknown information;
- temporary working context;
- personal/user preference memory;
- organisation/project/workstream/task-scoped knowledge;
- external/public evidence.

Normative rule: **memory is not truth, evidence is not approval, approval is not canonical promotion, and canonical status never arises from model confidence or repetition.**

---

# 2. Scope hierarchy and isolation

Use and refine the existing context hierarchy:

`GLOBAL -> ORGANISATION -> PROGRAMME / PORTFOLIO / PRODUCT -> PROJECT -> WORKSTREAM -> TASK`

Where needed, allow `PERSONAL` as a separate scope family that must never silently leak into organisation/project canonical knowledge.

Define:
- scope identity;
- inheritance direction;
- visibility versus authority;
- parent/child reuse rules;
- cross-scope reference rules;
- contamination prevention;
- same-name entity disambiguation;
- context switching rules;
- explicit import/reference versus silent copying.

Critical rule:

**Knowledge from one organisation/project/user scope must not become canonical or presumed applicable in another scope without an explicit governed transfer/revalidation step.**

Do not turn this into IAM implementation.

---

# 3. Knowledge-state model

Phase 8 must own the knowledge-state lifecycle that earlier phases intentionally referenced but did not govern.

At minimum support these states or their exact semantic equivalents:

- `SOURCE`
- `EVIDENCE`
- `FACT_CLAIM`
- `ASSUMPTION`
- `CALCULATION`
- `INFERENCE`
- `AI_SUGGESTION`
- `DRAFT`
- `REVIEWED`
- `APPROVED`
- `CANONICAL`
- `SUPERSEDED`
- `CONFLICT_DETECTED`
- `UNKNOWN`
- `REJECTED`
- `RETRACTED`

Do not mechanically reuse earlier labels if their meaning is ambiguous. Define every state.

Important:
- `REVIEWED` does not mean true;
- `APPROVED` does not automatically mean `CANONICAL`;
- `CANONICAL` is scoped and versioned, not globally true forever;
- `SUPERSEDED` preserves history;
- `RETRACTED` is not deletion;
- `CONFLICT_DETECTED` must remain visible until resolved by evidence/governance;
- `UNKNOWN` cannot be promoted by authority alone;
- AI confidence is never a knowledge state.

Define permitted state transitions and forbidden shortcuts.

---

# 4. Canonical knowledge object

Define a semantic Canonical Knowledge Record/Object model.

It must minimally preserve:

- stable canonical ID;
- subject/entity identity;
- scope;
- statement/claim;
- semantic type;
- source/evidence references;
- provenance chain;
- author/contributor origin;
- review status and relevant Review Profile refs;
- decision/approval refs where required;
- effective-from;
- expiry/review-by if applicable;
- version;
- supersedes/superseded-by linkage;
- conflict links;
- uncertainty/limitations;
- applicable context/conditions;
- canonical status;
- reason for promotion/change/retraction;
- responsible governance owner class (not named person);
- audit history.

This is a semantic record model, not a DB schema.

---

# 5. Canonical promotion governance

Resolve the Phase 7 forward-reference area around:

- `decision.canonical_knowledge_promotion`
- `decision.canonical_knowledge_status_change`

Do not casually keep two overlapping executable Rights.

Required architecture outcome:

1. Determine whether there is one bounded Decision Right with multiple permitted effects, or more than one genuinely distinct Right.
2. Preserve upstream traceability for both prior identifiers.
3. Avoid duplicate authority.
4. Define exactly what authority is required to:
   - promote to `CANONICAL`;
   - supersede a canonical statement;
   - retract canonical status;
   - resolve a canonical conflict;
   - correct a canonical record;
   - change scope/applicability;
   - expire/review a canonical item.
5. A professional conclusion needed for promotion must still come from an eligible Role/Review process; the Decision Right itself cannot manufacture expertise.
6. A Decision Right cannot convert unsupported `UNKNOWN`, `ASSUMPTION`, or unresolved conflict into FACT merely by approval.
7. Canonical promotion must be version-specific and evidence-bound.

If a final Decision Right Card is not justified yet, keep it as a bounded candidate and document exact future Phase 7/8 integration instead of inventing authority.

---

# 6. Conflict model

Define first-class conflict governance.

At minimum distinguish:

- source conflict;
- claim conflict;
- version conflict;
- scope conflict;
- temporal conflict;
- authority conflict;
- identity/entity-resolution conflict.

Rules:
- conflict is not automatically an error;
- later source != automatically superior source;
- higher authority != automatically truer evidence;
- conflict resolution must record why one interpretation prevailed;
- unresolved conflict blocks canonical promotion where material;
- minority/dissent evidence may remain attached after a resolution;
- resolution must not erase the losing evidence/history.

---

# 7. Provenance and lineage

Define required provenance from source to canonical output.

A downstream canonical statement must be traceable through:

`SOURCE -> EVIDENCE -> CLAIM / CALCULATION / INFERENCE -> REVIEW -> DECISION (if required) -> CANONICAL VERSION`

Not every item needs every step, but every omitted step must be explainable by item type/risk level.

Define:
- direct evidence;
- derived evidence;
- calculation lineage;
- transformation lineage;
- citation/reference lineage;
- human edit lineage;
- AI-generated contribution lineage;
- external-source lineage;
- artifact-to-knowledge linkage.

No silent provenance loss.

---

# 8. Memory classes

Define conceptual memory classes without implementing storage.

At minimum consider:

- `WORKING_MEMORY` — short-lived task/workflow context;
- `EPISODIC_MEMORY` — prior actions/events/decisions;
- `SEMANTIC_MEMORY` — reusable facts/claims/definitions;
- `PREFERENCE_MEMORY` — user/org preferences and conventions;
- `PROCEDURAL_MEMORY` — governed methods/playbooks/instructions;
- `CANONICAL_MEMORY` — approved scoped source of truth;
- `AUDIT_MEMORY` — immutable historic evidence/decision trail.

Decide whether these are first-class registry types or architecture classes only.

Rules:
- working memory cannot self-promote;
- preference memory cannot override law/fact/canonical evidence;
- episodic memory does not imply ongoing validity;
- procedural memory does not grant authority;
- canonical memory is not a cache;
- audit memory is append-oriented and history-preserving.

---

# 9. Retention, freshness, staleness, expiry

Define semantic lifecycle controls:

- freshness expectation;
- stale-but-usable;
- stale-and-blocking;
- expiry;
- review-by;
- refresh trigger;
- supersession;
- archival;
- retraction;
- legal/contractual retention hold concept;
- deletion eligibility concept.

Do not implement retention jobs.

Critical distinction:

**stale != false; expired != deleted; superseded != erased; retracted != forgotten.**

---

# 10. Sensitive / restricted knowledge boundary

Architecture only: define metadata-level handling classes for knowledge whose use must be restricted.

At minimum support concepts for:

- public;
- internal;
- confidential;
- restricted/highly sensitive;
- personal data;
- privileged/legal;
- trade secret/commercially sensitive;
- security-sensitive;
- third-party-restricted.

Do not design IAM. Define only what downstream runtime/storage must later honor.

Canonical status must not imply broader visibility.

---

# 11. Artifact / knowledge relationship

Define relationship between documents/artifacts and knowledge objects.

Rules:
- a document can contain multiple claims of different states;
- an approved document is not automatically entirely canonical;
- canonical knowledge may be represented in multiple artifacts;
- artifact replacement does not silently rewrite canonical history;
- artifact deletion does not necessarily delete canonical/audit records;
- generated documents must cite/use the currently applicable canonical version where required;
- downstream artifact may carry open assumptions/conflicts explicitly.

---

# 12. Human correction and AI suggestions

Define safe correction flow:

- AI suggestion remains `AI_SUGGESTION` until governed transition;
- AI may detect conflicts or propose updates but cannot self-canonicalize;
- human edits must retain provenance;
- correction of a canonical item creates a new linked version/record, not silent overwrite;
- rollback means restore applicability through a new governed action, not erase intervening history;
- admin/user override does not bypass mandatory evidence/review/authority rules.

---

# 13. Reuse and retrieval boundary

Architecture only.

Define the distinction between:
- being stored;
- being retrievable;
- being selected into context;
- being authoritative for the current task;
- being canonical for the current scope.

Critical rule:

**retrieval rank or model relevance score must never determine authority or canonical status.**

Do not implement RAG or model routing.

---

# 14. Criticality and canonical rigor

Use existing project/decision criticality ideas without rewriting them.

Define how higher criticality changes:
- required evidence depth;
- review independence;
- provenance completeness;
- freshness threshold;
- conflict tolerance;
- canonical promotion gate;
- dual/multi-authority requirements where applicable.

Criticality must increase rigor, not change truth.

---

# 15. Required artifacts

Create at minimum:

1. `architecture/memory-canonical-governance.md`
2. `knowledge/_standards/common-knowledge-governance-constraints.md`
3. `knowledge/_templates/knowledge-record-template.md`
4. `knowledge/_templates/canonical-record-template.md`
5. `knowledge/knowledge-state-model.md`
6. `knowledge/memory-class-model.md`
7. `knowledge/scope-isolation-and-transfer.md`
8. `knowledge/conflict-and-provenance-model.md`
9. `knowledge/canonical-promotion-governance.md`
10. `knowledge/master-knowledge-governance-universe.md`
11. `reviews/phase-8-foundation-self-check.md`

You may add a small number of additional architecture files only if clearly necessary.

Do not mass-generate cards.

---

# 16. Exemplar set

Create a small controlled exemplar set, not a mass universe.

At minimum include examples for:

1. verified organisational fact promoted to canonical;
2. project assumption that remains non-canonical;
3. financial calculation with source lineage;
4. conflicting external sources blocking canonical promotion;
5. superseded canonical project parameter;
6. user preference memory that must not leak into organisational canonical knowledge;
7. retracted canonical statement preserving history;
8. stale canonical item requiring refresh before decision-grade use.

Use template-based exemplar records or worked examples. Keep them `PROPOSED`.

---

# 17. Required self-check

Build a repeatable self-check with at least 60 checks.

It must verify at least:

- identity separation;
- memory != canonical;
- evidence != truth/approval;
- approved != canonical;
- canonical is scoped/versioned;
- state transition legality;
- UNKNOWN/ASSUMPTION cannot be authority-promoted into FACT without evidence;
- conflict preservation;
- provenance completeness;
- no silent overwrites;
- scope isolation;
- personal-to-org contamination prevention;
- cross-project contamination prevention;
- transfer/revalidation semantics;
- artifact != knowledge object;
- approved artifact != all-canonical;
- AI suggestion cannot self-promote;
- rollback preserves history;
- stale/expired/superseded/retracted semantics differ;
- sensitive classification != canonical status;
- retrieval relevance != authority;
- canonical promotion Decision Right cannot create expertise;
- Phase 7 separation-of-duties remains intact;
- no Role authority leakage;
- no Review status rewrite;
- no runtime implementation;
- Phase 3–7 approved semantics unchanged;
- all Phase 8 artifacts PROPOSED;
- no PR.

If a test is wrong, document it and replace it with a stricter correct test. Never weaken tests just to pass.

---

# 18. Open architecture questions

Explicitly identify and disposition at least these:

1. Is canonical status attached to a claim, a record, or both?
2. Can one canonical subject have multiple simultaneously valid scoped statements?
3. How is canonicality inherited across scopes, if at all?
4. Should `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change` normalize to one Right or multiple bounded Rights?
5. What types can become canonical: facts only, or also approved policies, parameters, definitions, methodologies?
6. How are calculations handled when source inputs later change?
7. What happens when a canonical item becomes stale but not false?
8. What happens when external evidence conflicts with internal canonical knowledge?
9. When is retraction different from supersession?
10. What belongs in runtime/storage/IAM rather than Phase 8 architecture?
11. Should preference/procedural memory ever be canonical?
12. What is the minimum evidence standard for Routine vs Decision-Grade canonical promotion?

For each classify:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 9+ / RUNTIME CONCERN

---

# 19. Final producer review threshold

Do not claim readiness merely because files exist.

Foundation is producer-ready for independent audit only if:

- no identity collapse exists;
- no silent cross-scope leakage exists;
- no path allows AI/model/retrieval ranking to self-canonicalize;
- no authority-only truth conversion exists;
- no conflict can be silently erased;
- no canonical version can be silently overwritten;
- the Phase 7 canonical Decision forward references are coherently resolved or explicitly bounded;
- provenance and history are preserved;
- Phase 3–7 approved architecture is unchanged;
- all self-checks pass.

---

# 20. Commit / push

If and only if the foundation and self-check pass, commit exactly:

`docs: add Phase 8 Memory and Canonical Governance foundation`

Push to:

`origin architecture/phase-8-memory-canonical`

Do not create a PR.

---

# Required final output

Return exactly:

### A. FOUNDATION SUMMARY
What was created and governing principles.

### B. IDENTITY / STATE MODEL
Exact separations and knowledge states.

### C. SCOPE / ISOLATION
Hierarchy, inheritance, transfer and contamination rules.

### D. CANONICAL GOVERNANCE
Promotion, supersession, retraction, correction and Decision Right integration.

### E. MEMORY CLASSES
Final classes and boundaries.

### F. CONFLICT / PROVENANCE
Conflict taxonomy and lineage rules.

### G. RETENTION / FRESHNESS / SENSITIVITY
Lifecycle and restricted-knowledge semantics.

### H. ARTIFACT / RETRIEVAL / AI BOUNDARIES
Artifact, retrieval and AI suggestion rules.

### I. EXEMPLARS
Eight exemplar outcomes and what each proves.

### J. OPEN QUESTIONS
All 12 dispositions.

### K. REGRESSION
Phase 3–7 immutability and non-runtime status.

### L. VALIDATION
PASS/FAIL count and honesty notes.

### M. FILES CHANGED
Exact files and purpose.

### N. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, PR status.

### O. NEXT STEP
Choose exactly one:
- READY FOR INDEPENDENT PHASE 8 FOUNDATION AUDIT
- NOT READY

Do not claim Phase 8 approval.