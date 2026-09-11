# Phase 8 — Memory and Canonical Governance Foundation Audit Remediation

Status: PROPOSED — READY FOR FINAL INDEPENDENT PHASE 8 RE-AUDIT

Branch: `architecture/phase-8-memory-canonical`
Foundation baseline: `3aea5890d81d0a954d8057d118facf54a365289d`
Phase 7 approval-record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`

The independent Codex foundation audit returned **FAIL** with five HIGH and three MEDIUM findings. This is a bounded architecture remediation. Every finding is addressed; unrelated Phase 8 concepts are not redesigned; **no approved Phase 3–7 artifact was modified**, and all upstream investigation was read-only.

**Every finding was genuine.** None is contested, and one of them (H1) makes a claim this foundation itself had asserted the opposite of.

---

## HIGH 1 — Scope hierarchy regression

**Finding.** Phase 8 omitted `INDEPENDENT BUSINESS / VENTURE` and `OPERATIONAL WORKSTREAM`, flattened `PROGRAMME / PORTFOLIO -> PROJECT`, and `master-knowledge-governance-universe.md` §4 claimed the hierarchy was unchanged.

**Status: RESOLVED.**

The approved graph in `architecture/context-hierarchy.md` is now **reproduced verbatim** in `knowledge/scope-isolation-and-transfer.md` §1, read from the approved file at the Phase 7 baseline. The first draft had lost four things, not two:

1. `INDEPENDENT BUSINESS / VENTURE`;
2. `OPERATIONAL WORKSTREAM`;
3. `PERMANENT FUNCTION / BUSINESS AREA`;
4. the dual path by which a `PROJECT` sits **either** under a programme/portfolio **or** directly under the organisation.

The fourth is the one with teeth: a project reachable by two paths has two different ancestor sets, so compressing the graph silently changes which statements are applicable to it — which is the entire subject of this document.

A per-node semantics table now distinguishes all eleven nodes, including the three pairs most easily merged: `OPERATIONAL WORKSTREAM` (organisation-level work ending at `TASK`) versus `WORKSTREAM` (inside a project); `PERMANENT FUNCTION / BUSINESS AREA` (a durable function) versus operational work; and `INDEPENDENT BUSINESS / VENTURE` as a **sibling of `ORGANISATION` under `GLOBAL`**, not a child of it — so nothing propagates between them in either direction.

The false claim in the universe is **corrected in place and labelled as false**, not quietly rewritten. The approved file itself was never modified.

**Validated by:** the harness reads the approved graph from `git show c72ef03:architecture/context-hierarchy.md` and requires a **line-for-line match** with the Phase 8 reproduction. Prose cannot satisfy it.

---

## HIGH 2 — Unbounded downward applicability

**Finding.** Every wider canonical statement was applicable to every descendant, and any named nearer statement could override it. No applicability modes; no protection for mandatory wider obligations.

**Status: RESOLVED.**

**Canonical status never inherits.** What may reach a descendant is *applicability*, and it propagates **only by the record's declared mode**:

| Mode | Propagates? | Descendant may hold a contrary statement? |
|---|---|---|
| `INHERITABLE_TO_DESCENDANTS` | Yes, unless a nearer statement declares a reasoned override | Yes, with a declared override |
| `CONDITIONALLY_APPLICABLE` | Only where the declared conditions hold | Outside the conditions the question does not arise |
| `NON_INHERITABLE` | No — governs its own scope only | Nothing to override |
| `MANDATORY_WIDER_CONSTRAINT` | Yes, and it **binds** | **No** — may be narrowed or detailed, never contradicted or relaxed |

**A mode is declared, never inferred**, and a record without one governs nothing beyond its own scope — the safe reading of a defective record is the narrow one.

An override must name what it overrides, at which version, the overridden record's mode, why it is governance-permissible, and the authority path relied on. **An override of a `MANDATORY_WIDER_CONSTRAINT` is not available at all**; a local exception requires a separately valid authority path, and where upstream provides none there is no exception — only a scope conflict and an unresolved obligation. A project cannot canonicalise its way out of a regulation.

**Ancestor fallback after local retraction is determined, never assumed:** a mandatory constraint **resumes automatically** (it never stopped binding — the local statement was only narrowing it); an inheritable statement **requires explicit revalidation**, because the finding strong enough to withdraw the local position is strong enough to be checked against the one beneath it; a conditional statement needs its **conditions re-checked**; and where there is none, **the scope has no position** and the retraction names the gap. **No wider statement resumes silently.**

Propagation stays downward only: nothing upward, nothing sideways, `PERSONAL` isolated, transfer still explicit, non-transitive, revalidated, and carrying neither canonical status nor Review satisfaction.

---

## HIGH 3 — Canonical identity duplication in memory classes

**Finding.** `CANONICAL_MEMORY` duplicated the `CANONICAL` governance state and Canonical Record identity, was undefined after supersession or retraction, and templates used shortened class names.

**Status: RESOLVED — the class was removed. Six classes remain.**

The audit was right on all three counts, and on a fourth the remediation found while fixing it:

1. membership was exactly "governance state is `CANONICAL`", so the class carried no information the state did not;
2. the Canonical Record already *is* the object holding canonical status;
3. a superseded or retracted record left the class with nowhere defined to go — undefined for precisely the records whose history must not move;
4. exemplars written as `SEMANTIC` → `CANONICAL` read as a class mutation where nothing about retention character had changed at all.

**Memory classes now describe retention and use character only.** Canonicality is a governance state carried by a Canonical Record. A canonical claim is `SEMANTIC_MEMORY` + `CANONICAL`; a canonical method is `PROCEDURAL_MEMORY` + `CANONICAL`; and **the class does not change when the state does** — through promotion, supersession and retraction alike, which is the property the removed class lacked.

Full names only, everywhere — model, templates, exemplars, inventory. The count went from seven to six and every reference was updated; it was not preserved at seven to protect a number.

---

## HIGH 4 — AI origin / epistemic type loophole

**Finding.** The architecture said a governed human act "moves" content out of `AI_SUGGESTION`, contradicting the rule that authority cannot change epistemic type.

**Status: RESOLVED.**

The contradiction was real, and it sat one section away from the rule it broke. A rule with an exception for the case it most needs to cover is not a rule.

**Disposition: `AI_SUGGESTION` remains an epistemic type, narrowed, and a separate permanent origin axis is added.** It stays because Phase 2's approved list carries it and Phase 3 Role Cards refer to unlabelled AI output; removing it would have broken upstream meaning to fix an internal one. It is narrowed to what it actually names — **an unadopted proposal** — while *where content came from* moves to the origin axis, where it belongs and where it can survive the proposal no longer being the live item.

**Origin:** `HUMAN_ORIGIN` · `AI_ASSISTED` · `AI_GENERATED` · `EXTERNAL_ORIGIN`. A permanent provenance fact. **Nothing changes it** — not adoption, editing, promotion or time.

**Adoption creates a new linked item and converts nothing:**

1. a **new knowledge item** is created with the epistemic type its own basis supports;
2. that type is justified by **evidence or reasoning** — **human acceptance is not an evidential basis**; a human agreeing with an unevidenced proposition produces an unevidenced proposition with an agreeing human attached;
3. the new item carries its AI origin **permanently** and links to the proposal;
4. the original `AI_SUGGESTION` **remains historically as what it was**, not rewritten or relabelled; its state may become `SUPERSEDED` or `REJECTED`;
5. the new item enters governance at `DRAFT` — **epistemic classification and governance approval stay separate acts, and neither performs the other.**

Made consistent across the architecture, state model, constraints, both templates, the provenance model, the universe and the exemplars. The provenance model's AI-lineage row still carried the old wording after the first pass and **the harness caught it** — see §Validation.

---

## HIGH 5 — Approved upstream forward reference narrowed

**Finding.** Phase 8 re-bounded `decision.canonical_knowledge_status_change` to canonical withdrawal only, while the approved Knowledge & Evidence Steward Role routes downgrades of both `APPROVED` and `CANONICAL` material to that ID. The `APPROVED` case was no longer covered.

**Status: RESOLVED.**

Upstream evidence, read at the Phase 7 baseline — `roles/portfolio-programme-project/knowledge-evidence-steward.md`, Role-Specific Authority Limits:

> "must not itself downgrade material whose current status derives from an explicit human **APPROVED / CANONICAL** decision; in that case it must raise `CONFLICT_DETECTED` / invalidation recommendation and route to `decision.canonical_knowledge_status_change`"

Phase 8 had created a broken forward reference while claiming to resolve one. The boundary is re-derived from that evidence as **successor promotion versus governed status downgrade**:

| | Promotion | Governed status downgrade |
|---|---|---|
| ID | `decision.canonical_knowledge_promotion` | `decision.canonical_knowledge_status_change` |
| Subject | One named version of one claim, for one scope | One existing governed status — **`APPROVED` or `CANONICAL`** — on one record in one scope |
| Effect subtypes | — | `APPROVED_STATUS_WITHDRAWAL` · `CANONICAL_RETRACTION` · `SCOPE_OR_APPLICABILITY_NARROWING` · `EARLY_EXPIRY` |
| Covers | Every act **with** a successor — correction, renewal, scope widening, re-promotion | Every act **without** a successor, at either status level |
| Evidence shape | Positive | Negative — a recorded finding that the basis failed |

**No overlap is possible:** an act either has a successor promotion or it does not, and none has both. A per-act table assigns all seven canonical acts plus conflict resolution and truth conversion to exactly one authority or to neither.

**Phase 7 carding recommendation:** one bounded Right for downgrade with the four declared subtypes, not four Rights — they share subject shape, evidence shape and characteristic risk. The counter-argument is recorded rather than dismissed: `APPROVED_STATUS_WITHDRAWAL` and `CANONICAL_RETRACTION` may warrant different holder eligibility, which is a **Phase 7 eligibility question**, and because each subtype is separately named, splitting later disturbs nothing. Phase 7 is also now directed to assess **promotion / transmitting-act concentration** on the same version rather than leave it unexamined.

No Decision Right is carded here, and the approved Role Card was not touched.

---

## MEDIUM 1 — Freshness axis ambiguity

**Finding.** Staleness was correctly use-specific, but the template required a single record-level "current freshness" value, and the stale exemplar used an undefined `STALE`.

**Status: RESOLVED — the axis is split.**

**Item-level temporal facts** (stored on the record): as-of date; last verified/refreshed; expected refresh interval; review-by; expiry; supersession/withdrawal state; refresh triggers. Plus one derived **age condition**, `PAST_REFRESH_INTERVAL`, replacing the undefined token — it says currency is unverified, not that the item is unusable and not that it is wrong.

**Use-context verdicts** (assessed per use, never stored): `CURRENT_FOR_USE` · `STALE_BUT_USABLE` · `STALE_AND_BLOCKING` · `EXPIRED_FOR_USE`.

The same item carries different verdicts for different tasks **at the same moment**. A single record-level field would have to pick one, be wrong for the other task, and then harden into a permanent label nobody re-examines.

**Review-by, expiry, refresh trigger and use verdict remain four distinct things** — collapsing any two is how "we reviewed it last year" becomes "it is fine to submit".

**Phase 6 is unaffected:** `STALE` remains an approved **review status** in `architecture/handoff-review-registry-design.md`, a different vocabulary about a different object. Phase 8 removes the token only from its own freshness model, and the harness asserts the Phase 6 status still exists.

---

## MEDIUM 2 — Criticality conflict rule inconsistent

**Finding.** Architecture §9 said any conflict bearing on an Enhanced Decision-Grade claim blocks, while everything else used **material** conflict. The former blocks immaterial disputes.

**Status: RESOLVED — normalised to materiality everywhere.**

One rule, in the architecture, the constraints, the promotion prerequisites, the conflict model and both templates: **an unresolved conflict blocks canonical promotion and decision-grade use where the claim or the decision depends on the contested point.** An immaterial conflict stays visible and documented and **blocks nothing, at any criticality band**.

**Materiality is a determination, not an impression**: stated on the record, **attributable to a named eligible Role, and reviewable** — never inferred from retrieval ranking, model confidence, source count or nobody having raised it.

Criticality changes the **tolerance and the burden, not the test**: at Enhanced Decision-Grade every open conflict requires an explicit materiality assessment, and an **unassessed** conflict is treated as material until one is made. That is a stronger default, not a different rule, and an irrelevant disagreement still blocks nothing.

---

## MEDIUM 3 — Self-check not reproducible

**Finding.** `116/116` was asserted in prose, with no committed validation logic, and presence-oriented checks missed the scope-tree, class/state, AI-transition, freshness and upstream-ID defects.

**Status: RESOLVED — the prose self-check is replaced by a committed harness.**

`validation/phase_8_validation.py`, with `validation/README.md` stating the convention. Python 3 standard library and `git` only; no network, no third-party packages; deterministic output; exit code 0 on full pass.

```
python3 validation/phase_8_validation.py
```

**95 checks. 95/95 PASS.** The old 116 figure is **not preserved** — it counted a different, weaker suite, and the count was replaced rather than protected.

Design rules, adopted directly from what the audit's criticism implied:

- **Discover, never enumerate.** Files come from walking the tree, so a new artifact is covered automatically and nothing passes by being absent from a hand-written list. The earlier suite's hand-built file dict is exactly how the `CANONICAL_MEMORY` alias in a template escaped it.
- **Compare against upstream, not against prose.** The scope-graph check reads the approved file **out of git at the Phase 7 baseline** and requires a line-for-line match. No wording could have satisfied it, and it would have caught H1 on the first run.
- **Parse structure where a string would do.** Class counts parse the class table; act coverage parses the act table; materiality is checked in five documents at once.
- **Never weaken a check.** Where a check was wrong it was replaced with a stricter one and the replacement recorded below.

---

## Validation evidence

**Command:** `python3 validation/phase_8_validation.py`
**Result:** `=== 95/95 PASS ===`, exit code 0.

Groups: scope-graph (6) · applicability (11) · memory-classes (6) · ai-origin (10) · decision-ids (8) · freshness (9) · materiality (7) · invariants (18) · regression (12) · exemplars (8).

### What the harness found that the prose self-check had missed

The first run returned **83/95**, and the failures were not all check defects:

1. **A real content loss.** The §2 rewrite of `memory-class-model.md` had **deleted its entire §3 Class rules section** — no self-promotion, episodic validity, preference precedence, procedural authority, cache and audit rules, all gone. The prose self-check would have reported success. The section is restored, with an eighth rule added (a memory class is not a governance status).
2. **A real missed edit.** Three constraint rewrites — §9 materiality, §15 applicability, §19 AI origin — had **silently failed to apply** because of a whitespace mismatch, leaving the standard asserting the pre-audit rules while every other document asserted the new ones. Caught, then applied.
3. **A real surviving defect.** `conflict-and-provenance-model.md` still carried "which governed human act moved it out of `AI_SUGGESTION`" in its lineage table — the exact wording H4 is about, in the one document the H4 edits had not covered. Fixed.

Three further failures were **check defects, each replaced with a stricter test**:

- the six-class check matched `| \`X_MEMORY\` |` anywhere in the file and caught a row of the state-transition table; it now **parses the class table itself**;
- the `CANONICAL_MEMORY` check flagged the universe's own record of the removal; it now distinguishes a **live declaration** from a documented removal, and additionally asserts the token is not in the declared class list;
- the ancestor-fallback check required a phrase the standard expressed differently; it now requires the rule in the **scope model, the standard and the canonical template**, and the scope model's wording was aligned so all three state it identically.

No check was weakened. **That the harness found three genuine defects the prose self-check had reported as passing is the substance of MEDIUM 3, not an incidental result.**

---

## Post-remediation regression checks

Re-tested, all passing: `CONFLICT_DETECTED` compatibility mapping explicit; artifact ≠ knowledge object; approved document ≠ wholly canonical; retrieval rank, relevance and model confidence ≠ authority; post-promotion material conflict visible with a governed use consequence; losing evidence and dissent retained; provenance surviving supersession, retraction and transfer; transformations lineage-bearing; preference never organisationally canonical by absorption, with the new-governed-record route open; procedural knowledge granting no authority; sensitivity orthogonal to canonicality and scope; canonical implying no visibility; retention-hold versus erasure left to legal authority; criticality raising rigour and not truth; `DRAFT`/`REVIEWED` → `CANONICAL` shortcuts absent; `UNKNOWN`/`ASSUMPTION` unpromotable by authority; transfer carrying neither canonical status nor Review satisfaction; no personal-to-organisational absorption; no in-place canonical overwrite.

---

## Files changed

| File | Purpose |
|---|---|
| `knowledge/scope-isolation-and-transfer.md` | Approved graph verbatim + per-node semantics (H1); four applicability modes, override rules, mandatory wider constraints, ancestor fallback (H2) |
| `knowledge/memory-class-model.md` | `CANONICAL_MEMORY` removed, six classes, class/state independence, §3 rules restored and extended (H3) |
| `knowledge/knowledge-state-model.md` | Origin axis, §2a no-conversion rule, four axes, forbidden shortcut 3 rewritten (H4) |
| `knowledge/canonical-promotion-governance.md` | Boundary re-derived from upstream, four effect subtypes, per-act table, Phase 7 carding recommendation and counter-argument (H5); materiality in prerequisite 5 (M2) |
| `knowledge/sensitivity-and-retention-model.md` | Item facts versus use verdicts, `PAST_REFRESH_INTERVAL`, Phase 6 compatibility note (M1) |
| `knowledge/conflict-and-provenance-model.md` | Materiality normalised and made attributable (M2); AI-lineage row rewritten (H4) |
| `knowledge/_standards/common-knowledge-governance-constraints.md` | §9 materiality, §15 applicability, §19 AI origin, new §28 item age ≠ use verdict (H2, H4, M1, M2) |
| `knowledge/_templates/knowledge-record-template.md` | Full class names, origin field, temporal facts replacing "current freshness", type-never-changes note (H3, H4, M1) |
| `knowledge/_templates/canonical-record-template.md` | Applicability mode, override requirements, ancestor-fallback determination, materiality assessment, class/state note (H2, H3, M2) |
| `knowledge/master-knowledge-governance-universe.md` | False hierarchy claim corrected in place; counts; AI mapping; decision-ID correction; removal recorded (H1, H3, H4, H5) |
| `knowledge/exemplars/` × 8 | Full class names, origin, applicability modes, ancestor fallback, item-facts/verdict split, attributable materiality |
| `validation/phase_8_validation.py` | **New** — 95-check reproducible harness (M3) |
| `validation/README.md` | **New** — harness conventions and non-runtime statement (M3) |
| `reviews/phase-8-foundation-self-check.md` | Replaced with a pointer to the harness and the corrected counts |
| `reviews/phase-8-foundation-audit-remediation.md` | This record |

**No approved Phase 3–7 file was modified.** Upstream investigation — the context hierarchy and the Steward Role Card — was read-only, via `git show` and `grep`.

---

## Deliberately deferred

1. **No Decision Right is carded.** Both canonical identifiers remain uncarded candidates conferring no authority; carding is a Phase 7 registry act, and **no canonical promotion is exercisable today**.
2. **Holder eligibility for either authority is not set** — Phase 7's, as it must be.
3. **Whether the four downgrade subtypes stay one Right or split** is a Phase 7 eligibility determination; Phase 8 recommends one and records the counter-argument.
4. **The exemplars remain eight worked illustrations**, not instances. Eight cases cannot exercise 95 rules.
5. **Runtime, storage, indexing, retrieval, access-control enforcement, identity and retention execution** remain out of scope.

---

## Open questions — re-adjudicated

The audit marked six as `MUST RESOLVE BEFORE HUMAN APPROVAL`. Each is answered with the **concrete architecture rule** that now resolves it, not a relabelling — and where the rule did not exist before this pass, it is named as new.

| # | Question | Disposition | The rule that resolves it |
|---:|---|---|---|
| 1 | Claim, record, or both? | **RESOLVED IN FOUNDATION** | Canonical status is a property of a **(claim version, scope)** pair carried by a Canonical Record — unchanged by this pass, and untouched by the audit |
| 2 | Multiple simultaneously valid scoped statements? | **RESOLVED IN FOUNDATION** *(rule added)* | **Yes, and now only under a declared applicability mode.** Two statements coexist where scopes do not overlap; where they do, the nearer must declare an override naming the wider record, its version, its mode and why the override is governance-permissible — and an override of a `MANDATORY_WIDER_CONSTRAINT` is unavailable. Undeclared overlap is a `SCOPE_CONFLICT`. The audit's objection was that this was unsafe over a flattened graph; the graph is restored verbatim and the modes make coexistence explicit rather than assumed |
| 3 | Cross-scope applicability / inheritance? | **RESOLVED IN FOUNDATION** *(rule added)* | **Canonical status never inherits.** Applicability propagates downward **only by declared mode**; a record without one governs nothing beyond its own scope; mandatory wider constraints bind and cannot be overridden locally; nothing propagates upward or sideways; and after local retraction **no wider statement resumes silently** |
| 4 | Normalise the two canonical Decision IDs? | **RESOLVED IN FOUNDATION** *(boundary re-derived)* | **Two Rights, on the successor / no-successor boundary**, derived from the approved Steward Role rather than from convenience. `..._promotion` takes every act with a successor; `..._status_change` takes every act without one, at **both `APPROVED` and `CANONICAL`** levels, through four declared effect subtypes. Non-overlap holds by construction. Carding remains a Phase 7 act, with the one-Right-with-subtypes recommendation and its counter-argument recorded |
| 5 | What types can become canonical? | **RESOLVED IN FOUNDATION** | `FACT_CLAIM`, `CALCULATION`, `INFERENCE`, and a `PROCEDURAL_MEMORY` method **as a method**. Never `SOURCE`, `EVIDENCE`, `ASSUMPTION`, `UNKNOWN`, `AI_SUGGESTION` or preference |
| 6 | Calculations when inputs change? | **RESOLVED IN FOUNDATION** | Inputs bound **by version**; supersession of any bound input fires the refresh trigger; the calculation becomes `PAST_REFRESH_INTERVAL`, **not false**, and **re-derivation** resolves it, never re-approval |
| 7 | Stale but not false? | **RESOLVED IN FOUNDATION** *(rule added)* | The axis is **split**: the record stores item-level temporal facts and the derived age condition `PAST_REFRESH_INTERVAL`; usability is a **per-use verdict** — `CURRENT_FOR_USE`, `STALE_BUT_USABLE`, `STALE_AND_BLOCKING`, `EXPIRED_FOR_USE` — assessed at the point of use and **never written back to the record**. The same item carries different verdicts for different tasks at the same moment. The audit's objection — that one record-level label could not represent this — is what the split removes |
| 8 | External evidence versus internal canonical? | **RESOLVED IN FOUNDATION** | A conflict flag is raised; the record stays canonical **and visibly in conflict**; where **material** it blocks decision-grade use until resolved. An unexamined newer source is a refresh trigger, not a conflict. Later is not superior |
| 9 | Retraction versus supersession? | **RESOLVED IN FOUNDATION** *(rule completed)* | Supersession has a successor and is the **automatic effect of promoting one**; retraction has none. The gap that retraction leaves must be **named**, and — the part missing before this pass — the **ancestor-fallback determination is mandatory and recorded**: automatic resumption only for a mandatory wider constraint, explicit revalidation for an inheritable one, re-checked conditions for a conditional one, or no position at all |
| 10 | What belongs to runtime / storage / IAM? | **PHASE 9+ / RUNTIME CONCERN** | Unchanged. Storage, indexing, retrieval, ranking, embeddings, access-control enforcement, identity, retention execution. The runtime validates against these semantics and does not mutate them |
| 11 | Preference or procedural memory canonical? | **RESOLVED IN FOUNDATION** | Procedural, yes — as the method, at a version, in a scope, with the adopting decision as its evidence. Preference, **never**: the route is to stop calling it a preference and adopt it as a method or parameter |
| 12 | Minimum evidence, Routine versus Decision-Grade? | **RESOLVED IN FOUNDATION** *(rule corrected)* | The band table in `architecture/memory-canonical-governance.md` §9 across six dimensions — and its conflict row, which the audit found overbroad, now carries the **single materiality rule**: a material conflict blocks, an immaterial one never does at any band, and Decision-Grade raises the **burden** by requiring an attributable materiality assessment for every open conflict. Rigour rises; the test does not change |

Five of the six the audit flagged are resolved by rules that **did not exist before this pass** (2, 3, 4, 7, 9). Question 12 is resolved by correcting a rule that existed and was inconsistent. None is resolved by relabelling.

---

## Status

**Phase 8 remains `PROPOSED`.** Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, and no approved Phase 3–7 artifact was modified. This record does not claim human approval and is not an independent audit; under Phase 6's vocabulary it is `PRODUCER_REVIEW`.

**Post-remediation audit baseline commit:** the commit carrying this record — the single commit `docs: remediate Phase 8 foundation after independent audit` on `architecture/phase-8-memory-canonical`.

A commit cannot contain its own SHA, so it is not written here rather than written wrongly. Resolve it with `git rev-parse HEAD` on this branch, or `git log -1 --format=%H --grep='remediate Phase 8 foundation'`. The re-audit baseline is that commit's tree, and the harness reproduces its result from it: `python3 validation/phase_8_validation.py` → `95/95 PASS`.
