# Canonical Promotion Governance

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## Purpose

Phase 7 carded eight Decision Rights and deliberately carded neither canonical-governance candidate, recording that Phase 8 owns the question. Phase 7's universe classified `decision.canonical_knowledge_status_change` as `DUPLICATE / OVERLAP` with `decision.canonical_knowledge_promotion` and deferred consolidation here. This document resolves that forward reference.

**It creates no Decision Right Card and modifies no approved Phase 7 artifact.** Carding is a Phase 7 registry act; §7 states exactly what that pass must do.

## 1. The seven canonical acts

Canonical governance is often discussed as one thing. It is seven, and their prerequisites differ:

| # | Act | What it does |
|---:|---|---|
| 1 | **Promote** | A named version of a claim becomes canonical for a named scope, effective from a stated date |
| 2 | **Supersede** | A successor version replaces the operative effect of the current one, same subject, same scope |
| 3 | **Retract** | Canonical status is withdrawn with **nothing replacing it** |
| 4 | **Resolve a canonical conflict** | A conflict flag on a canonical record is cleared by a recorded resolution |
| 5 | **Correct** | An error in a canonical statement is fixed |
| 6 | **Change scope or applicability** | The scope in which a statement governs is widened or narrowed |
| 7 | **Expire / review** | A review-by point is reached and the item is renewed, allowed to lapse, or refreshed |

## 2. Five of the seven are not free-standing decisions

This is the finding that makes the duplicate-authority question answerable.

- **Supersession (2) is an automatic effect of promotion (1)**, not a decision of its own. Promoting version *n+1* of a subject for a scope supersedes version *n* for that scope, by definition — there is no state in which both are canonical, and no separate act is required. Any Right that could "supersede" independently would be a Right to leave a scope with no canonical position while pretending one was replaced.
- **Correction (5) is promotion of a corrected version** — a new version, promoted, superseding the erroneous one, with the correction reason recorded. There is no in-place edit and therefore no separate authority to define.
- **Conflict resolution (4) is a professional and review act**, not an authority act. Which evidence prevails is a Role conclusion checked by a Phase 6 review. Where the resolution changes the canonical position, the change happens through (1) or (3). A Decision Right cannot decide which source is accurate.
- **Widening scope (6) is promotion into the wider scope** — a distinct scope, a distinct promotion, its own evidence, per `scope-isolation-and-transfer.md` §2.
- **Renewal at a review point (7) is promotion of the same or a refreshed version** with a new effective period. Letting an item lapse is covered by §3 below.

What remains genuinely distinct is **promotion**, and **withdrawal that leaves a gap**.

## 3. Two bounded authorities

| | **Canonical promotion** | **Canonical status withdrawal** |
|---|---|---|
| Upstream identifier preserved | `decision.canonical_knowledge_promotion` | `decision.canonical_knowledge_status_change` |
| Subject | One named version of one claim, for one named scope | One canonical record, in one scope |
| Effect | It becomes the canonical statement from an effective date; any prior version for that scope is superseded automatically | Canonical status ends; **the scope is left with no canonical position on the subject**, and the record remains visible as `RETRACTED` |
| Also covers | Correction, renewal, scope widening, re-promotion after resolution — all are promotions | Narrowing scope so a statement no longer governs where it did; early expiry |
| Evidence shape | **Positive** — evidence sufficient to support the claim at this criticality band | **Negative** — a finding that the basis has failed, is unsound, or no longer holds |
| Characteristic risk | Adopting something unsupported | **Leaving a governed gap nobody notices** |
| Prerequisite review | The applicable Review Profiles `SATISFIED` for the band | A recorded finding, review or resolution establishing why the basis failed |

The boundary is drawn **differently from the two upstream names**: it is not "promotion versus any other status change", it is **"a successor exists" versus "no successor exists"**. That is what makes the two non-overlapping. Every act with a successor is a promotion; only withdrawal into a gap is the second authority. There is no act that both could perform.

Traceability for both upstream identifiers is preserved, and neither is renamed. `knowledge/master-knowledge-governance-universe.md` §6 records the mapping.

## 4. Promotion prerequisites

All eight must hold. They are cumulative, and each is checkable against the record.

1. The item is a **promotable epistemic type** — `FACT_CLAIM`, `CALCULATION`, `INFERENCE`, or a `PROCEDURAL_MEMORY` method. Never `ASSUMPTION`, `UNKNOWN`, `SOURCE`, `EVIDENCE` or `AI_SUGGESTION`.
2. Its governance state is `APPROVED`, reached by the ordinary route.
3. The applicable Review Profiles are `SATISFIED` for the criticality band, **or** exceptional progression has been separately exercised under Phase 7 over each named unsatisfied one.
4. **Provenance is complete to the band's depth**, with every omitted step explained.
5. **No unresolved conflict material to the claim** is outstanding.
6. The **version is named**, the **scope is named**, and the **effective-from is stated**.
7. Where a nearer or wider scope holds a statement on the same subject, the **relationship is declared** — override or coexistence — so no scope conflict is created by the promotion itself.
8. Uncertainty, limitations and applicability conditions are recorded **on the record**, not left in the supporting material.

## 5. What promotion authority cannot do

1. **It cannot create expertise.** The professional conclusion behind a canonical statement comes from an eligible Role and its review. Promotion adopts a conclusion; it does not reach one, and no holder becomes competent in a subject by being authorised to adopt positions about it.
2. **It cannot convert `UNKNOWN` into `FACT_CLAIM`.** Not knowing is a state of the evidence. Authority may decide to proceed without knowing; it cannot decide the answer.
3. **It cannot convert `ASSUMPTION` into `FACT_CLAIM`.** An assumption becomes a claim when evidence arrives, and then it is a new claim linked to the assumption it replaces.
4. **It cannot clear a conflict.** A material unresolved conflict blocks promotion; promoting anyway is not available as an override.
5. **It cannot promote "the current version" or "the document".** Promotion is version-specific and claim-specific; a document is not a unit of canonical status (`architecture/memory-canonical-governance.md` §6).
6. **It cannot promote globally.** Every promotion names one scope.
7. **It cannot promote on model confidence, retrieval rank, repetition, consensus among sources, or absence of objection.**
8. **It cannot edit anything.** Promotion adds a version and supersedes another; it changes no prior record's content.

## 6. What withdrawal authority cannot do

1. **It cannot delete, hide or erase.** `RETRACTED` is visible, with its reason, permanently.
2. **It cannot rewrite history.** Work performed in reliance on the statement while it was canonical was performed in reliance on a then-canonical statement, and remains so described.
3. **It cannot leave the gap unstated.** A retraction records what the scope now has no position on, and what depends on it — an unnoticed gap is the specific harm this authority carries.
4. **It cannot be used where a successor exists.** That is promotion.
5. **It cannot make the withdrawn statement false.** Withdrawal ends reliance; it is not a finding that the opposite is true.

## 7. Exact Phase 7 integration required (not performed here)

Phase 8 defines the semantics. A **Phase 7 registry pass** must then, under Phase 7's own governance:

1. Card `decision.canonical_knowledge_promotion` with the subject, effect and prerequisites of §3 and §4, and with supersession declared as an automatic effect of the `APPROVE` outcome rather than a separate act.
2. **Re-bound** `decision.canonical_knowledge_status_change` to withdrawal-into-a-gap per §3, and reclassify it in the Phase 7 universe from `DUPLICATE / OVERLAP` to a bounded candidate — resolving the duplication by **narrowing the second Right**, which is why neither identifier needs renaming or removing.
3. Declare the `DECISION_RIGHT_SEPARATION` relationships both Rights require. At minimum, `SEPARATION_REQUIRED` between canonical promotion and `decision.exceptional_progression` where the exception concerns an item material to the promotion — the person who excepted the unsatisfied review must not also be the one who adopts the result as the organisation's position.
4. Set holder eligibility, cardinality and delegation policy under Phase 7's model. Phase 8 states one boundary only, because it follows from the subject: **no class holds promotion authority by producing, owning, reviewing or retrieving the knowledge.**
5. Leave Phase 7's approved semantics otherwise untouched.

Until that pass runs, **both identifiers remain uncarded candidates conferring no authority**, and no canonical promotion is exercisable. Phase 8 does not invent the authority it describes.

## 8. Status

`PROPOSED`. Cards nothing, grants nothing, and implements nothing.
