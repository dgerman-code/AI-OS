# Phase 8 — Memory and Canonical Governance Foundation Self-Check

Status: PROPOSED — READY FOR INDEPENDENT PHASE 8 FOUNDATION AUDIT

Branch: `architecture/phase-8-memory-canonical`
Start baseline: Phase 7 human-approval record `c72ef0399b3c7c2f272711918803f7bc08c70084`
Approved Phase 7 architecture baseline: `cedee2cfd1a959489585eb61acd975b4f7c65c84`

This is a **self**-check by the producing pass. Under Phase 6's own vocabulary it is `PRODUCER_REVIEW` — internal quality control, which cannot satisfy an independent review requirement.

## Artifacts covered

| File | Purpose |
|---|---|
| `architecture/memory-canonical-governance.md` | Master architecture: identity separation, three axes, canonical definition, correction/AI rules, artifact relationship, the five retrieval properties, criticality, non-runtime |
| `knowledge/knowledge-state-model.md` | 8 epistemic types, 7 governance states, conflict flag, transitions, 10 forbidden shortcuts |
| `knowledge/scope-isolation-and-transfer.md` | Hierarchy, applicability, isolation, governed transfer, 4 contamination directions, `PERSONAL` |
| `knowledge/memory-class-model.md` | 7 memory classes as architecture classes |
| `knowledge/conflict-and-provenance-model.md` | 7 conflict classes, resolution rules, required chain, 9 lineage types |
| `knowledge/canonical-promotion-governance.md` | 7 canonical acts, 2 bounded authorities, the Phase 7 integration specification |
| `knowledge/sensitivity-and-retention-model.md` | 9 sensitivity classes, freshness controls, 4 end states, retention holds |
| `knowledge/_standards/common-knowledge-governance-constraints.md` | 28 enforceable rules |
| `knowledge/_templates/` × 2 | Knowledge Record and Canonical Record semantic models |
| `knowledge/exemplars/` × 8 | Worked cases, each proving one boundary |
| `knowledge/master-knowledge-governance-universe.md` | Inventory, label mapping, deferred work |

---

## 1. Check results — 116 checks

**116 / 116 PASS.**

| Group | Checks | Result |
|---|---|---|
| Identity separation | 1–6 | **PASS** — 9-way chain; every object defined; memory ≠ truth, evidence ≠ approval, approval ≠ promotion; source and evidence never promotable |
| State model | 7–20 | **PASS** — three axes held simultaneously; 8 types, 7 states, conflict as a flag; 10 forbidden shortcuts; `UNKNOWN` and `ASSUMPTION` unpromotable by authority; AI confidence is no state |
| Canonical semantics | 21–28 | **PASS** — scoped, versioned, effective-dated, a (claim version, scope) pair; never from confidence, rank, repetition or silence; 8 cumulative prerequisites; no document-level promotion |
| Promotion authority | 29–34 | **PASS** — creates no expertise, cannot clear a conflict; 7 acts, 5 of them not free-standing; 2 bounded authorities; both upstream identifiers preserved and **neither carded here** |
| Conflict | 35–41 | **PASS** — 7 classes; conflict is not an error; later ≠ superior, authority ≠ evidence; reasoning recorded, losing evidence retained; material conflict blocks promotion |
| Provenance | 42–47 | **PASS** — required chain; omissions explained; 9 lineage types; no silent loss; inputs bound by version; AI contribution always visible |
| Scope and isolation | 48–56 | **PASS** — applicability down, authority never, nothing up or sideways; nearest-scope-wins with named override; silent copy prohibited; transfer carries neither status nor review satisfaction; 4 contamination directions closed |
| Memory classes | 57–62 | **PASS** — 7 classes as architecture classes with the decision justified; no self-promotion; preference never canonical; canonical memory is not a cache |
| Lifecycle and sensitivity | 63–70 | **PASS** — 4 end states distinguished; staleness decided by use; 9 sensitivity classes, orthogonal, carried through lineage; retention hold outranks |
| Artifact, retrieval, AI | 71–80 | **PASS** — artifact ≠ knowledge object; approved document ≠ canonical; five properties separated; rank never authority; absence is not evidence; no override path |
| Criticality | 81–83 | **PASS** — Phase 3 bands used not rewritten; depth changes, truth does not |
| Upstream immutability and hygiene | 84–95 | **PASS** — `git diff` empty over Phases 3, 4, 5, 6, 7 and the inherited Phase 2/3 architecture; no Role authority, no review-status change, no card created; all artifacts `PROPOSED`; no PR |
| Non-runtime | 96–100 | **PASS** — no DB/API/embedding/retrieval/IAM; statements in architecture and both templates; no named person or organisation |
| Exemplars | 101–110 | **PASS** — 8 exemplars, each testing its own boundary |
| Inheritance and templates | 111–116 | **PASS** — every knowledge file inherits the standard; 28 constraints; templates cover the full record models and forbid in-place edits |

### Honesty note on the checks

The suite first reported 114/116, then 115/116. **All three failures were defects in the checks, not the content**, and each was replaced with a stricter test:

- **Check 25** matched a sentence with the bold markers inside it — twice, in two different documents. Replaced with a test that **strips emphasis before matching and requires all four denials in both the state model and the architecture**, rather than one prose string in one file. Two of the three failures were this one defect surfacing in sequence.
- **Check 111** required every knowledge document to inherit the standard, and the standard cannot inherit itself. It also scanned a hand-built list rather than the filesystem. Replaced with a test that **walks every file on disk**, excludes only the standard, and additionally requires the standard to declare the exact ID the others inherit — so a new file cannot slip past it.

No check was weakened, and **no content changed as a result of any of them**.

---

## 2. Open architecture questions

| # | Question | Disposition | Reasoning |
|---:|---|---|---|
| 1 | Is canonical status attached to a claim, a record, or both? | **RESOLVED IN FOUNDATION** | To a **(claim version, scope)** pair, carried by a Canonical Record. The record is the container and the identity; the status is a property of the pair. This is why promoting "the document" is impossible and why one subject can hold different statuses in different scopes. |
| 2 | Can one canonical subject have multiple simultaneously valid scoped statements? | **RESOLVED IN FOUNDATION** | Yes, in non-overlapping scopes, and yes for an ancestor/descendant pair where the nearer one **declares the override**. Overlapping statements with no declared relationship are a `SCOPE_CONFLICT`, not a permitted arrangement. |
| 3 | How is canonicality inherited across scopes? | **RESOLVED IN FOUNDATION** | It is not inherited; it is **applicable** downward, nearest-scope-wins, and never upward or sideways. Applicability and authority are separated precisely so that being inside a scope confers nothing. |
| 4 | Should the two canonical Decision Rights normalize to one or several? | **RESOLVED IN FOUNDATION** | **Two bounded Rights**, on a boundary drawn differently from the two upstream names: *a successor exists* (promotion — including correction, renewal and scope widening, with supersession as an automatic effect) versus *no successor exists* (withdrawal into a gap). No act is performable by both. Carding is a **Phase 7 registry act**, specified exactly and deliberately not performed here. |
| 5 | What types can become canonical? | **RESOLVED IN FOUNDATION** | `FACT_CLAIM`, `CALCULATION`, `INFERENCE`, and `PROCEDURAL_MEMORY` methods **as methods**. Never `SOURCE`, `EVIDENCE`, `ASSUMPTION`, `UNKNOWN`, `AI_SUGGESTION` or preference. A canonical method does not make its outputs canonical. |
| 6 | How are calculations handled when inputs later change? | **RESOLVED IN FOUNDATION** | Inputs are bound **by version**; supersession of any bound input fires the refresh trigger and the calculation becomes **stale, not false**. Re-derivation resolves it — **not re-approval**, because authority cannot revalidate a number nobody recomputed. |
| 7 | What happens when a canonical item is stale but not false? | **RESOLVED IN FOUNDATION** | It stays canonical and becomes `STALE_BUT_USABLE` or `STALE_AND_BLOCKING` **according to the use**, not the item. At Enhanced Decision-Grade, stale is blocking. |
| 8 | What happens when external evidence conflicts with internal canonical knowledge? | **RESOLVED IN FOUNDATION** | A conflict flag is raised; the record stays canonical **and visibly in conflict**, and becomes blocking for decision-grade use until resolved. A newer external source is a refresh trigger, and is not a conflict until someone establishes incompatibility. Later is not superior. |
| 9 | When is retraction different from supersession? | **RESOLVED IN FOUNDATION** | Supersession has a successor and is automatic. Retraction has none and **leaves a governed gap that must be named**. Calling a retraction a supersession implies a position the scope no longer holds. |
| 10 | What belongs in runtime/storage/IAM rather than Phase 8? | **PHASE 9+ / RUNTIME CONCERN** | Storage, indexing, retrieval, ranking, embeddings, access-control enforcement, identity, retention execution. Phase 8 states what a runtime must honour; the runtime validates against these semantics and does not mutate them. |
| 11 | Should preference or procedural memory ever be canonical? | **RESOLVED IN FOUNDATION** | Procedural, yes — as the governed method, at a version, in a scope, with the adopting decision as its evidence. Preference, **never**: the legitimate route is to stop calling it a preference and adopt it as a method or parameter through the governed act. |
| 12 | Minimum evidence standard, Routine versus Decision-Grade? | **RESOLVED IN FOUNDATION** | The band table in `architecture/memory-canonical-governance.md` §9: six dimensions — evidence depth, review independence, provenance completeness, freshness, conflict tolerance, promotion gate. **Rigour rises; truth does not.** |

**Nothing is classified `MUST RESOLVE BEFORE HUMAN APPROVAL`.** That is a claim the independent audit should test hardest: Phase 7's self-check flagged its own separation gap as an open question and shipped 50/50, and the audit was right to reject that. The corresponding candidate here is question 4 — see §4 below for where this foundation is most likely to be wrong.

## 3. Producer-review threshold

The prompt's ten conditions, each answered against the artifacts rather than asserted:

| Condition | Position |
|---|---|
| No identity collapse | 9-way chain, with each object separately defined and each collapse named where it typically occurs |
| No silent cross-scope leakage | Reference or governed transfer only; silent copy is a defect, not a mechanism; four contamination directions closed by name |
| No path for AI, model or retrieval rank to self-canonicalize | `AI_SUGGESTION` is a type a model cannot move; the five retrieval properties are separated; confidence has **no representation in the model at all** |
| No authority-only truth conversion | Epistemic type is a separate axis that no governance act touches; `UNKNOWN` and `ASSUMPTION` are unpromotable by authority in three documents |
| No conflict silently erased | Flags cleared only by recorded resolution; losing evidence retained and readable |
| No canonical version silently overwritten | Correction is a new promoted version; canonical records are never edited in place |
| Phase 7 canonical forward references resolved or bounded | Resolved semantically, bounded in authority: both identifiers keep traceability, **neither is carded**, and the exact Phase 7 pass is specified |
| Provenance and history preserved | Provenance survives every transition; four end states each preserve content |
| Phase 3–7 architecture unchanged | Verified by `git diff` against the Phase 7 approval baseline, not by inspection |
| All self-checks pass | 116/116 |

## 4. Where this foundation is most likely to be wrong

Recorded for the audit rather than left to be discovered:

1. **Question 4 is the load-bearing judgement.** The claim that supersession, correction, renewal and scope widening are all *promotions* is what makes two Rights non-overlapping. If any one of them turns out to need its own evidence shape, the boundary moves and the Phase 7 pass specification in `canonical-promotion-governance.md` §7 is wrong with it.
2. **The three-axis model is a departure**, even though it renames nothing upstream. Reclassifying `CONFLICT_DETECTED` from a state to a flag is the specific change an auditor should test against every upstream use of the term.
3. **Withdrawal authority is defined but its holder class is not.** Phase 8 states one boundary — no class holds promotion authority by producing, owning, reviewing or retrieving the knowledge — and leaves eligibility, cardinality and delegation to Phase 7, as it must. That is a deliberate gap, and it means **no canonical promotion is exercisable today**.
4. **The exemplars are worked illustrations, not instances.** They demonstrate boundaries; they validate no real knowledge, and eight cases cannot exercise 116 rules.

## 5. Standing statement

Every Phase 8 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, and no approved Phase 3–7 artifact was modified. This record does not claim human approval and is not an independent audit.
