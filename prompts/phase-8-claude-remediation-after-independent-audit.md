# Claude Code Prompt — Phase 8 Remediation After Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-8-memory-canonical`
Foundation baseline: `3aea5890d81d0a954d8057d118facf54a365289d`
Phase 7 approval-record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`

The independent Codex foundation audit returned **FAIL**.

This is a bounded architecture remediation pass. Fix the audit findings without redesigning unrelated Phase 8 concepts and without changing approved Phase 3–7 semantics.

Do NOT implement runtime, DB, API, UI, RAG, embeddings, model routing, agents, IAM, retention jobs, or storage engines.
Do NOT create a PR.
Do NOT mark Phase 8 APPROVED or CANONICAL.
All Phase 8 artifacts remain `PROPOSED`.

## Independent-audit blockers to remediate

### 1. Restore the approved scope hierarchy exactly

Audit finding: Phase 8 omitted `INDEPENDENT BUSINESS / VENTURE` and `OPERATIONAL WORKSTREAM`, and flattened the approved `PROGRAMME / PORTFOLIO -> PROJECT` relationship.

Required action:
- inspect approved pre-Phase8 architecture at/before `c72ef0399b3c7c2f272711918803f7bc08c70084`;
- identify the exact previously approved context/scope graph and terminology;
- restore it without reinterpretation;
- include `INDEPENDENT BUSINESS / VENTURE` and `OPERATIONAL WORKSTREAM` where the approved architecture requires them;
- preserve distinct semantics for organisation, independent business/venture, programme, portfolio, product, project, operational workstream, workstream, task, and personal scope where applicable;
- correct every Phase 8 statement that claimed the hierarchy was unchanged if that statement was factually false.

Do not invent a new hierarchy merely to satisfy the names above. The approved upstream architecture is authoritative.

### 2. Replace unconditional downward applicability with an explicit applicability model

Audit finding: current wording makes every wider canonical statement automatically applicable to every descendant and allows any nearer statement to override it.

Add an explicit semantic applicability/inheritance mode to canonical knowledge. At minimum support clear equivalents of:
- `INHERITABLE` — may apply to descendants subject to conditions;
- `CONDITIONAL` — applies only where declared applicability conditions are satisfied;
- `NON_INHERITABLE` — does not automatically apply to descendants;
- `MANDATORY_WIDER_CONSTRAINT` — descendant scopes may narrow/add local detail but may not contradict or override the wider obligation unless an explicitly authorized upstream exception mechanism exists.

You may choose better names, but the semantics must be explicit and non-overlapping.

Rules:
- canonical status itself never “inherits”;
- applicability may propagate only according to the item's explicit applicability mode and conditions;
- nearer scope does not automatically override a mandatory wider law, regulation, policy, contract, safety rule, governance standard, or equivalent binding constraint;
- local exception requires a separately valid authority path if upstream architecture permits one;
- descendant override must identify what is overridden and why it is legally/governance-permissible;
- no upward or sideways propagation;
- `PERSONAL` remains isolated;
- transfer remains explicit, non-transitive, revalidated, and carries neither canonical status nor Review satisfaction.

Define ancestor fallback after local retraction: when a narrower canonical statement is retracted without successor, state whether an otherwise-applicable wider canonical statement resumes, remains blocked, or requires explicit revalidation according to applicability mode/conditions. No silent fallback.

Update templates and exemplars as needed.

### 3. Remove canonical identity duplication from memory classes

Audit finding: `CANONICAL_MEMORY` duplicates the `CANONICAL` governance state / Canonical Record identity and becomes undefined after supersession/retraction.

Required action:
- remove `CANONICAL_MEMORY` as a memory class OR redefine the memory-class model so there is no semantic duplication;
- preferred direction: memory classes describe retention/use character, while canonicality remains governance state / Canonical Record status only;
- a record that was canonical and later becomes `SUPERSEDED` or `RETRACTED` must still have an unambiguous memory/retention class without changing historical identity;
- normalize class naming across model, templates, exemplars, and universe; no shortened aliases that runtime would need to guess.

If reducing from seven to six memory classes is architecturally cleaner, do so and update all counts/references transparently. Do not preserve a bad class merely to keep a previous count.

### 4. Fix `AI_SUGGESTION` origin/type semantics

Audit finding: current wording lets a governed human act “move” content out of `AI_SUGGESTION`, conflicting with the rule that authority cannot change epistemic type.

Resolve this explicitly.

Required model:
- AI origin belongs in provenance/origin metadata;
- an AI-produced proposition may initially be represented as an AI-originated proposal/suggestion, but human acceptance alone cannot change its epistemic nature into FACT/INFERENCE/etc.;
- if evidence/reasoning supports adoption, create a **new linked knowledge item/version** with the appropriate epistemic type (`FACT_CLAIM`, `INFERENCE`, `ASSUMPTION`, `CALCULATION`, etc.);
- preserve the AI-origin contribution in lineage;
- the old AI suggestion/proposal remains historical and is not rewritten;
- governance approval and epistemic reclassification remain separate acts;
- no human, model, reviewer, or authority can convert `AI_SUGGESTION` into `FACT_CLAIM` by status change alone.

Decide whether `AI_SUGGESTION` should remain an epistemic type at all. If it is fundamentally an origin/provenance condition rather than a knowledge nature, normalize the model accordingly and provide an explicit compatibility mapping for earlier Phase 2–7 references so no upstream semantics are silently broken.

This decision must be internally consistent across:
- `architecture/memory-canonical-governance.md`;
- `knowledge/knowledge-state-model.md`;
- common constraints;
- Knowledge Record template;
- Canonical Record template;
- provenance model;
- universe;
- exemplars;
- self-check.

### 5. Preserve approved upstream meaning of `decision.canonical_knowledge_status_change`

Audit finding: Phase 8 narrowed that upstream ID to canonical withdrawal only, while the approved Knowledge & Evidence Steward Role routes downgrades of both `APPROVED` and `CANONICAL` material to that Decision ID.

Required action:
- inspect the approved upstream references to `decision.canonical_knowledge_status_change` at/before the Phase 7 approval baseline;
- preserve the approved `APPROVED`-material use;
- do not silently rewrite the approved Role semantics;
- do not create an executable Decision Right in Phase 8;
- refine the Phase 8 proposal so both prior upstream references remain representable without duplicate/unbounded authority.

A likely acceptable architecture is to distinguish **governed status downgrade/change** from **canonical successor promotion**, but you must derive the final boundary from upstream evidence, not from this prompt alone.

Explicitly account for:
- downgrade/removal of `APPROVED` status;
- withdrawal/retraction of `CANONICAL` status without successor;
- successor promotion causing supersession;
- correction via successor version;
- scope/applicability change;
- no authority-only truth conversion.

Record whether Phase 7 will later need one bounded Right with effect subtypes or multiple genuinely distinct Rights. Preserve stable upstream IDs and traceability.

### 6. Separate item freshness facts from use-context usability

Audit finding: staleness is correctly described as use-specific, but templates require one singular “current freshness” value and exemplar 8 uses undefined `STALE`.

Required model:
- distinguish **item-level temporal metadata** from **use-context assessment**.

At minimum define item-level fields such as:
- observed/as-of date;
- last verified/refreshed date;
- expected refresh/review interval or review-by;
- expiry if applicable;
- supersession/withdrawal state.

And a separate use-context verdict such as:
- `CURRENT_FOR_USE`;
- `STALE_BUT_USABLE`;
- `STALE_AND_BLOCKING`;
- `EXPIRED_FOR_USE` or equivalent where needed.

Do not make these exact names mandatory if a better model exists.

Rules:
- the same item may be usable for one task and blocking for another at the same time;
- the use verdict is not a permanent record-level truth label;
- undefined plain `STALE` must disappear unless formally defined as an item-age condition distinct from use verdict;
- `review-by`, expiry, refresh trigger, and use verdict must remain distinct.

Update stale exemplar accordingly.

### 7. Reconcile conflict materiality at Enhanced Decision-Grade

Audit finding: architecture says “any conflict bearing on the claim blocks,” while other rules say **material** conflict blocks.

Normalize to one rule:
- unresolved **material** conflict blocks canonical promotion/use where the decision/task depends on the contested point;
- immaterial conflicts remain visible and documented but do not automatically block;
- criticality may lower the materiality tolerance / require explicit materiality assessment and stronger review, but does not make every irrelevant disagreement blocking;
- materiality determination must be attributable and reviewable, not silently inferred by retrieval/model confidence.

Update architecture, common constraints, promotion prerequisites, conflict model, templates, exemplars, and self-check as needed.

### 8. Make the self-check reproducible and semantic

Audit finding: `116/116` was not reproducible; no committed validation implementation existed, and presence-oriented checks missed major architecture defects.

Required action:
- create a committed, repeatable Phase 8 validation harness under an appropriate repository path, following existing project conventions if any;
- it may be a script/test file, but it must remain architecture-validation tooling, not runtime implementation;
- it must be runnable locally and return deterministic PASS/FAIL;
- do not hard-code only the known files where filesystem discovery is more correct;
- include semantic cross-file validations where feasible rather than mere string presence;
- document exact command(s) used and exact totals;
- ensure the self-check report can be independently reproduced from the repository.

The new harness must detect at least:
1. approved scope graph compatibility;
2. applicability mode presence and mandatory-wider constraint protection;
3. no canonical memory-class duplication;
4. AI adoption/new-linked-item rule;
5. preservation of upstream `decision.canonical_knowledge_status_change` references/meaning;
6. item freshness vs use-context distinction;
7. conflict-materiality consistency;
8. no silent `DRAFT/REVIEWED/APPROVED -> CANONICAL` shortcut;
9. no authority conversion of `UNKNOWN`/`ASSUMPTION` to `FACT_CLAIM`;
10. no cross-scope transfer carrying canonical or Review status;
11. no personal-to-org absorption;
12. no retrieval/ranking authority leakage;
13. no in-place canonical overwrite;
14. provenance preservation;
15. all Phase 8 artifacts remain `PROPOSED`;
16. Phase 3–7 approved files/semantics unchanged;
17. no runtime implementation;
18. no PR.

If previous “116 checks” cannot be honestly reproduced after redesign, replace the count with the actual new deterministic test count. Accuracy matters more than preserving 116.

---

## Required post-remediation architecture checks

In addition to the eight findings above, re-test these non-blocking areas to ensure no regression:

- `CONFLICT_DETECTED` compatibility mapping remains explicit and safe;
- artifact != knowledge object;
- approved document != wholly canonical;
- retrieval rank/relevance/freshness/model confidence != authority;
- post-promotion material conflict remains visible and has a governed use consequence;
- losing conflict evidence/dissent remains retained;
- provenance survives supersession/retraction/transfer;
- transformations (currency conversion, rounding, aggregation, rebasing) remain lineage-bearing;
- PREFERENCE cannot become organisational canonical by absorption;
- a convention that originated as preference may become a new governed policy/method/parameter record;
- PROCEDURAL knowledge does not grant authority;
- sensitivity remains orthogonal to canonicality and scope;
- canonical does not imply visibility;
- retention hold vs deletion/legal erasure conflict remains a legal-authority concern, not silently resolved;
- criticality increases rigor, not truth or authority;
- all eight exemplars remain coherent after updates.

---

## Open-question disposition after remediation

Re-adjudicate all 12 Phase 8 open questions.

The independent audit marked these as MUST RESOLVE BEFORE HUMAN APPROVAL:
- #2 multiple simultaneously valid scoped statements;
- #3 cross-scope applicability/inheritance;
- #4 normalization of canonical Decision IDs;
- #7 stale-but-not-false handling;
- #9 retraction vs supersession;
- #12 minimum evidence by criticality.

Do not simply relabel them RESOLVED. Show the concrete architecture rule that resolves each.

Question #10 remains `PHASE 9+ / RUNTIME CONCERN` unless remediation reveals otherwise.

---

## Required remediation record

Create:

`reviews/phase-8-foundation-audit-remediation.md`

It must contain:
- each HIGH/MEDIUM finding;
- exact remediation;
- files changed;
- validation evidence;
- any deliberately deferred issue;
- explicit statement that Phase 8 remains `PROPOSED`;
- exact post-remediation audit baseline commit once committed.

---

## Regression boundary

Prove from git diff against `c72ef0399b3c7c2f272711918803f7bc08c70084` that:
- approved Phase 3 Role files/semantics changed = 0;
- approved Phase 4 Skill files/semantics changed = 0;
- approved Phase 5 Workflow files/semantics changed = 0;
- approved Phase 6 Handoff/Review files/semantics changed = 0;
- approved Phase 7 Decision files/semantics changed = 0;
- any upstream reference investigation is read-only;
- only Phase 8 architecture, exemplars, validation tooling, and review evidence are modified.

No reapproval of prior phases is implied.

---

## Commit / push

If and only if all remediation checks pass, commit exactly:

`docs: remediate Phase 8 foundation after independent audit`

Push to:

`origin architecture/phase-8-memory-canonical`

Do not create a PR.

---

# Required final output

Return exactly:

### A. REMEDIATION SUMMARY
All HIGH/MEDIUM findings and final status.

### B. SCOPE GRAPH
Exact restored approved hierarchy/graph and evidence source; confirm upstream compatibility.

### C. APPLICABILITY MODEL
Final modes, override rules, mandatory wider-constraint rule, ancestor fallback after retraction.

### D. MEMORY CLASS MODEL
Final classes and how canonical duplication was removed.

### E. AI ORIGIN / EPISTEMIC MODEL
Final `AI_SUGGESTION` disposition, linked-item adoption rule, provenance behavior.

### F. CANONICAL DECISION INTEGRATION
Final semantics of `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change`, including approved-material downgrade coverage and future Phase 7 carding boundary.

### G. FRESHNESS MODEL
Item-level fields vs use-context verdicts; confirm undefined `STALE` removed or formally defined.

### H. CONFLICT MATERIALITY
Single normalized rule and Decision-Grade behavior.

### I. OPEN QUESTIONS
All 12 dispositions with one-line justification each.

### J. EXEMPLARS
Eight exemplar PASS/FAIL after remediation.

### K. VALIDATION HARNESS
Exact committed file(s), exact command, exact PASS/FAIL total, and how the former non-reproducible self-check was replaced.

### L. REGRESSION
Phase 3–7 diffs/semantic changes, Phase 8 status, runtime status, PR status.

### M. FILES CHANGED
Exact files and purpose.

### N. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, clean-tree status, PR status.

### O. NEXT STEP
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 8 RE-AUDIT
- NOT READY

Do not claim Phase 8 approval.