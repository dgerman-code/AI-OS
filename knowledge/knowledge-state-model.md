# Knowledge State Model

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## Purpose

Phases 2 through 7 wrote a flat list of knowledge labels — `FACT`, `SOURCE`, `ASSUMPTION`, `CALCULATION`, `AI_SUGGESTION`, `DRAFT`, `REVIEWED`, `APPROVED`, `CANONICAL`, `SUPERSEDED`, `CONFLICT_DETECTED`, `UNKNOWN` — and governed none of them. The list works as a vocabulary and fails as a model, for one reason: **the labels are not the same kind of thing.** `ASSUMPTION` says what a piece of knowledge *is*. `APPROVED` says how far through governance it has *come*. `CONFLICT_DETECTED` says something is *wrong with it* and says nothing about either. Treating them as one enumeration forces a false choice — an approved assumption has to pick a label and lose the other half of its meaning.

Phase 8 resolves this **without renaming anything upstream**. Every label above keeps its spelling and its meaning; this document says which axis it belongs to.

## 1. Three axes, held simultaneously

Every knowledge item carries **exactly one epistemic type**, **exactly one governance state**, and **zero or more conflict flags**.

```
EPISTEMIC TYPE   what this knowledge is        (never changed by authority)
GOVERNANCE STATE how far governance has come   (changed only by governed acts)
CONFLICT FLAG    what is unresolved about it   (cleared only by resolution)
```

An approved assumption is `ASSUMPTION` + `APPROVED`, and remains an assumption. This is the single most important structural claim in Phase 8, because the failure it prevents — approval quietly converting an assumption into a fact — is the failure the whole registry chain exists to prevent.

## 2. Epistemic types

| Type | Meaning | May reach `CANONICAL`? |
|---|---|---|
| `SOURCE` | Raw material as received — a document, dataset, statement, filing, message. Not an assertion the entity makes; a thing the entity holds. | **No** — a source is cited, never promoted |
| `EVIDENCE` | A specific extraction from a source, bound to its location in that source, supporting or contradicting a claim | **No** — evidence supports promotion, it is not promoted |
| `FACT_CLAIM` | An assertion about the world, offered as true and evidence-bound. **Named `FACT_CLAIM`, not `FACT`,** because the register holds claims; the world holds facts | **Yes** |
| `ASSUMPTION` | A position adopted **without sufficient evidence**, deliberately and visibly, so downstream work can proceed | **No** |
| `CALCULATION` | A value derived by a stated method from stated inputs at stated versions | **Yes**, with input bindings |
| `INFERENCE` | A conclusion drawn from evidence by reasoning rather than observation, where the reasoning is the load-bearing part | **Yes**, where the reasoning is Role-owned and reviewed |
| `AI_SUGGESTION` | Content originating from a model or automated process, of any of the above shapes, **before** any governed human act | **No** — see §6 |
| `UNKNOWN` | A determinate, named gap: the question is asked, the answer is not held | **No** |

Upstream `FACT` maps to `FACT_CLAIM`. No upstream artifact is edited; the mapping is recorded in `knowledge/master-knowledge-governance-universe.md` §5.

**`AI_SUGGESTION` is a type, not a confidence level.** A model's confidence, score, ranking, or repetition across outputs is **not a knowledge state, not an epistemic type, and not evidence**. It has no representation in this model at all.

## 3. Governance states

| State | Meaning |
|---|---|
| `DRAFT` | In preparation. Carries no reliance. |
| `REVIEWED` | A Phase 6 Review Profile was performed and `SATISFIED`. **`REVIEWED` does not mean true** — it means a stated methodology was applied and its findings recorded. A reviewed assumption is a well-examined assumption. |
| `APPROVED` | A bounded Phase 7 approval Decision Right was exercised **for a declared purpose**. Reliance extends to that purpose and no further. |
| `CANONICAL` | The organisation's governed position on a subject, **for a named scope, at a named version, from an effective date**. See §5. |
| `SUPERSEDED` | A later governed version replaced this one's operative effect. The content remains intact and readable. |
| `RETRACTED` | The item is withdrawn from reliance **and remains visible**, with the reason recorded. Not deletion, not erasure, not forgetting. |
| `REJECTED` | Considered and refused — the claim was not adopted. Distinct from `RETRACTED`, which withdraws something previously adopted. |

**`APPROVED` does not automatically mean `CANONICAL`.** Approval authorises reliance for a purpose; canonical promotion adopts a statement as the organisation's position for a scope. Every phase since Phase 3 asserted this boundary; Phase 8 is where it becomes a transition rule rather than a sentence.

## 4. Conflict flag

`CONFLICT_DETECTED` is a **flag carried alongside** the type and state, not a state that replaces them. A canonical record with a detected conflict is still `CANONICAL` and is **visibly in conflict** — which is the honest representation, and the one that lets a reader see both that the organisation has a position and that the position is contested. Taxonomy and resolution semantics are in `knowledge/conflict-and-provenance-model.md`.

A conflict flag is cleared **only by a recorded resolution**. It is never cleared by time, by re-assertion, by the arrival of a newer source, or by promotion.

## 5. What `CANONICAL` is, exactly

`CANONICAL` is a property of a **(claim version, scope)** pair, carried by a Canonical Record. It is:

- **scoped** — canonical in `PROJECT/alpha` is not canonical in `PROJECT/beta`, nor at `ORGANISATION`;
- **versioned** — a canonical statement is always a specific version, and promotion is version-specific;
- **time-bound** — it has an effective-from, and may have a review-by or expiry;
- **evidence-bound** — it carries the evidence that supported promotion, at the versions relied on;
- **revocable** — by supersession or retraction, both of which preserve history.

It is **not** global, not permanent, not a statement that the claim is true, and not a visibility level.

## 6. Permitted transitions

Governance-state transitions, with what each requires:

| From | To | Requires |
|---|---|---|
| `DRAFT` | `REVIEWED` | A Phase 6 Review Profile performed and `SATISFIED` |
| `DRAFT` | `REJECTED` | A governed refusal, with reason |
| `REVIEWED` | `APPROVED` | A bounded approval Decision Right, for a declared purpose |
| `REVIEWED` | `REJECTED` | As above |
| `APPROVED` | `CANONICAL` | Canonical promotion authority **plus** the evidence, review, scope, version and conflict prerequisites of `knowledge/canonical-promotion-governance.md` |
| `CANONICAL` | `SUPERSEDED` | Promotion of a successor version for the **same subject and scope** — automatic, and never a free-standing decision |
| `CANONICAL` | `RETRACTED` | Canonical status-withdrawal authority, with a recorded reason and the resulting gap declared |
| `APPROVED` / `REVIEWED` / `DRAFT` | `RETRACTED` | Withdrawal of an adopted item at its own level of adoption |
| any | `CONFLICT_DETECTED` flag raised | Evidence of conflict. **Raising a flag needs no authority; clearing one does.** |

### Forbidden shortcuts

Each of these is a defect wherever it appears, not a policy choice:

1. `DRAFT` → `CANONICAL` — skipping review and approval.
2. `REVIEWED` → `CANONICAL` — review satisfaction is not adoption.
3. `AI_SUGGESTION` → any governance state **without a governed human act**. A model cannot move its own output along this axis.
4. `UNKNOWN` → `FACT_CLAIM` **by authority**. Authority may decide what to do about not knowing; it cannot decide the answer. Closing an `UNKNOWN` requires evidence.
5. `ASSUMPTION` → `FACT_CLAIM` **by authority, approval, promotion, age, or reuse**. It requires evidence sufficient to support the claim — and then it is a *new* `FACT_CLAIM` linked to the assumption it replaces, not a relabelling.
6. `CONFLICT_DETECTED` → cleared without a recorded resolution.
7. `CANONICAL` → `CANONICAL` for the same scope by **editing in place**. A correction is a new version, promoted, superseding the old.
8. `SUPERSEDED` or `RETRACTED` → deleted, hidden, or overwritten.
9. `REJECTED` → `APPROVED` without a new governed act on new grounds.
10. Any transition **caused by retrieval, ranking, relevance, confidence, repetition or absence of objection.**

## 7. What no state transition can do

No transition on this model changes **what the world is**. Every transition changes what the organisation has *done about* what it holds — examined it, adopted it, relied on it, withdrawn it. The epistemic type axis exists precisely so that this remains visible after every governance act: an approved assumption is still an assumption, a canonical inference is still an inference, and a promoted calculation is still only as good as the inputs it names.

## 8. Status

`PROPOSED`. This model governs no runtime, specifies no storage, and confers no authority.
