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

## 3. Two bounded authorities, derived from upstream evidence

The first Phase 8 draft bounded the second authority to **canonical** withdrawal only. The independent audit was right that this silently narrowed an approved upstream meaning. The evidence, read at the Phase 7 approval baseline:

> `roles/portfolio-programme-project/knowledge-evidence-steward.md`, Role-Specific Authority Limits — the Steward "must not itself downgrade material whose current status derives from an explicit human **APPROVED / CANONICAL** decision; in that case it must raise `CONFLICT_DETECTED` / invalidation recommendation and route to `decision.canonical_knowledge_status_change`".

So the approved upstream use covers downgrade of **`APPROVED` material as well as `CANONICAL` material**. A boundary that covered only canonical retraction would have left the Steward's `APPROVED` route pointing at an authority that no longer claimed it — a broken forward reference created by Phase 8 rather than resolved by it.

The boundary is therefore **successor promotion versus governed status downgrade**, which preserves both upstream uses and still creates no overlap:

| | **Canonical promotion** | **Governed status downgrade** |
|---|---|---|
| Upstream identifier preserved | `decision.canonical_knowledge_promotion` | `decision.canonical_knowledge_status_change` |
| Subject | One named version of one claim, for one named scope | One existing **governed status** — `APPROVED` or `CANONICAL` — on one record, in one scope |
| Effect | It becomes the canonical statement from an effective date; any prior canonical version for that scope is superseded automatically | The status ends or narrows. **Nothing takes its place**, and the record stays visible at the state the downgrade leaves it in |
| Declared effect subtypes | — | `APPROVED_STATUS_WITHDRAWAL` · `CANONICAL_RETRACTION` · `SCOPE_OR_APPLICABILITY_NARROWING` · `EARLY_EXPIRY` |
| Also covers | Correction, renewal, scope **widening**, re-promotion after resolution — every act with a successor | Every act **without** a successor, at either governed status level |
| Evidence shape | **Positive** — evidence sufficient to support the claim at this band | **Negative** — a recorded finding that the basis has failed, is unsound, or no longer holds |
| Characteristic risk | Adopting something unsupported | **Leaving a governed gap nobody notices** |

**The two cannot overlap, by construction:** every act either has a successor promotion or it does not, and no act has both. Correction is promotion; retraction is downgrade; there is nothing in between.

Traceability for both upstream identifiers is preserved and neither is renamed. `knowledge/master-knowledge-governance-universe.md` §6 records the mapping.

### Every act accounted for

| Act | Authority | Note |
|---|---|---|
| Promote a claim to `CANONICAL` | Promotion | §4 prerequisites |
| Supersede via successor version | Promotion | Automatic effect; never a free-standing act |
| Correct a canonical statement | Promotion | A corrected version, promoted |
| Widen scope | Promotion | A distinct scope, its own promotion |
| Renew at a review point | Promotion | Same or refreshed version, new effective period |
| **Downgrade `APPROVED` material** | **Status downgrade** — `APPROVED_STATUS_WITHDRAWAL` | **The approved Steward route.** Reliance for the declared purpose ends; the record stays at `REVIEWED` or `DRAFT` as the finding warrants |
| **Retract `CANONICAL` with no successor** | **Status downgrade** — `CANONICAL_RETRACTION` | Leaves a gap, which must be named, with ancestor fallback determined per `knowledge/scope-isolation-and-transfer.md` §2 |
| Narrow scope or applicability | **Status downgrade** — `SCOPE_OR_APPLICABILITY_NARROWING` | Withdrawal from scopes where it governed; widening is promotion |
| Expire early | **Status downgrade** — `EARLY_EXPIRY` | Ends currency ahead of the declared point |
| Resolve a conflict | **Neither** | A Role conclusion checked by review. Any resulting status change then uses one of the two above |
| Convert `UNKNOWN` or `ASSUMPTION` into a fact | **Neither — and no authority does this** | Evidence does, as a new linked item |

### One Right with effect subtypes, or several — the Phase 7 determination

**Recommendation to the Phase 7 pass: one bounded Right for downgrade, with the four declared effect subtypes above** — not four Rights. The four share a subject shape (an existing governed status on one record in one scope), an evidence shape (a negative finding), and the characteristic risk (an unnoticed gap), and Phase 7's own model already expresses varying consequence through declared outcome effects rather than through multiplying Rights.

The countervailing argument is recorded rather than dismissed: `APPROVED_STATUS_WITHDRAWAL` and `CANONICAL_RETRACTION` may warrant different holder eligibility, since withdrawing a bounded approval is a lesser act than withdrawing the organisation's position. **That is a Phase 7 eligibility question, not a Phase 8 identity question** — and if Phase 7 concludes the eligibility classes differ enough, splitting the subtypes into two Rights remains open without disturbing anything here, because each subtype is already separately named.

## 4. Promotion prerequisites

All eight must hold. They are cumulative, and each is checkable against the record.

1. The item is a **promotable epistemic type** — `FACT_CLAIM`, `CALCULATION`, `INFERENCE`, or a `PROCEDURAL_MEMORY` method. Never `ASSUMPTION`, `UNKNOWN`, `SOURCE`, `EVIDENCE` or `AI_SUGGESTION`.
2. Its governance state is `APPROVED`, reached by the ordinary route.
3. The applicable Review Profiles are `SATISFIED` for the criticality band, **or** exceptional progression has been separately exercised under Phase 7 over each named unsatisfied one.
4. **Provenance is complete to the band's depth**, with every omitted step explained.
5. **No unresolved conflict material to the claim** is outstanding — materiality being an attributable, reviewable assessment, and at Enhanced Decision-Grade an unassessed open conflict counts as material until assessed.
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

## 6. What status-downgrade authority cannot do

1. **It cannot delete, hide or erase.** `RETRACTED` is visible, with its reason, permanently.
2. **It cannot rewrite history.** Work performed in reliance on the statement while it was canonical was performed in reliance on a then-canonical statement, and remains so described.
3. **It cannot leave the gap unstated.** A retraction records what the scope now has no position on, and what depends on it — an unnoticed gap is the specific harm this authority carries.
4. **It cannot be used where a successor exists.** That is promotion — at either status level.
5. **It cannot make the withdrawn statement false.** Withdrawal ends reliance; it is not a finding that the opposite is true.
6. **It cannot rewrite the Steward's route.** The approved Phase 3 Role raises `CONFLICT_DETECTED` and routes; it does not downgrade. Nothing here gives it the power it is denied, and nothing here removes the route it is given.

## 7. Exact Phase 7 integration required (not performed here)

Phase 8 defines the semantics. A **Phase 7 registry pass** must then, under Phase 7's own governance:

1. Card `decision.canonical_knowledge_promotion` with the subject, effect and prerequisites of §3 and §4, and with supersession declared as an automatic effect of the `APPROVE` outcome rather than a separate act.
2. **Bound** `decision.canonical_knowledge_status_change` to governed status downgrade per §3 — **covering `APPROVED` material as well as `CANONICAL`**, with the four declared effect subtypes — and reclassify it in the Phase 7 universe from `DUPLICATE / OVERLAP` to a bounded candidate. The duplication is resolved by the successor/no-successor boundary, not by removing either identifier, and the approved Knowledge & Evidence Steward route to this ID **must still resolve after carding**.
3. Declare the `DECISION_RIGHT_SEPARATION` relationships both Rights require. At minimum, `SEPARATION_REQUIRED` between canonical promotion and `decision.exceptional_progression` where the exception concerns an item material to the promotion — the person who excepted the unsatisfied review must not also be the one who adopts the result as the organisation's position.
4. Decide whether the four downgrade subtypes stay in one Right or split, on the eligibility argument in §3 — Phase 8 recommends one Right with subtypes and records the counter-argument.
5. **Assess concentration between promotion of a version and any transmitting act on the same version** — publication, submission or release. Phase 8 does not assert this separation as mandatory; it asserts that Phase 7 must reach a determination rather than leave it unexamined, because adopting a statement as the organisation's position and putting that same version outside the entity are close enough to be taken in one breath.
6. Set holder eligibility, cardinality and delegation policy under Phase 7's model. Phase 8 states one boundary only, because it follows from the subject: **no class holds promotion authority by producing, owning, reviewing or retrieving the knowledge.**
7. Leave Phase 7's approved semantics otherwise untouched.

Until that pass runs, **both identifiers remain uncarded candidates conferring no authority**, and no canonical promotion is exercisable. Phase 8 does not invent the authority it describes.

## 8. Status

`PROPOSED`. Cards nothing, grants nothing, and implements nothing.
