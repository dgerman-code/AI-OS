# Knowledge and Canonical Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 finding **M-1**.

## 1. The governing rule

> **Memory is not truth. Evidence is not approval. Approval is not canonical promotion. And
> canonical status never arises from model confidence, retrieval rank, repetition, consensus
> among sources, or nobody having objected.**

Every mechanism an AI-native system has for surfacing knowledge — similarity, ranking,
frequency, recency — is a mechanism for making something *look* established. The four axes
below exist so that looking established is never the same as being the organisation's position.

## 2. Four axes, held simultaneously

A knowledge item is **not one label**. It carries four independent axes plus a scope, a memory
class and a sensitivity classification. The implementation stores each axis in its own column.
Collapsing any two into one column is a defect, and is exactly the Phase 12 shortcut this
document replaces.

### 2.1 Axis 1 — Epistemic type (what it is)

| Value | Meaning | Promotable to `CANONICAL`? |
|---|---|---|
| `SOURCE` | Raw material as received — a document, dataset, statement, filing, message. A thing the entity holds, not an assertion it makes | **No** — cited, never promoted |
| `EVIDENCE` | A specific extraction from a source, bound to its location in that source, supporting or contradicting a claim | **No** — evidence supports promotion, it is not promoted |
| `FACT_CLAIM` | An assertion about the world, offered as true and evidence-bound. Named `FACT_CLAIM`, not `FACT`, because the register holds claims and the world holds facts | **Yes** |
| `ASSUMPTION` | A position adopted without sufficient evidence, deliberately and visibly | **No** |
| `CALCULATION` | A value derived by a stated method from stated inputs at stated versions | **Yes**, with input bindings |
| `INFERENCE` | A conclusion drawn from evidence by reasoning rather than observation | **Yes**, where the reasoning is Role-owned and reviewed |
| `AI_SUGGESTION` | **An unadopted proposal.** Names the item's unadopted-proposal character, not its origin | **No** — and it never becomes another type |
| `UNKNOWN` | A determinate, named gap: the question is asked, the answer is not held | **No** |

Upstream Phase 2 `FACT` maps to `FACT_CLAIM`. The mapping is recorded, and no upstream artifact
is edited.

### 2.2 Axis 2 — Governance state (how far governance has taken it)

| Value | Meaning |
|---|---|
| `DRAFT` | In preparation. Carries no reliance |
| `REVIEWED` | A Phase 6 Review Profile was performed and `SATISFIED`. **`REVIEWED` does not mean true** — it means a stated methodology was applied and its findings recorded |
| `APPROVED` | A bounded Phase 7 approval Decision Right was exercised **for a declared purpose**. Reliance extends to that purpose and no further |
| `CANONICAL` | The organisation's governed position on a subject, **for a named scope, at a named version, from an effective date** |
| `SUPERSEDED` | A later governed version replaced this one's operative effect. Content remains intact and readable |
| `RETRACTED` | Withdrawn from reliance **and still visible**, with reason and the level withdrawn from recorded. The single terminal state for every withdrawal. Not deletion |
| `REJECTED` | Considered and refused — the claim was not adopted. Distinct from `RETRACTED`, which withdraws something previously adopted |

### 2.3 Axis 3 — Origin (permanent provenance)

| Value | Meaning |
|---|---|
| `HUMAN_ORIGIN` | Produced by a person |
| `AI_ASSISTED` | Produced by a person with model assistance |
| `AI_GENERATED` | Produced by a model or automated process |
| `EXTERNAL_ORIGIN` | Received from outside the entity |

**Rule K-1 — origin is immutable.** Nothing changes it — not adoption, not editing, not review,
not approval, not promotion. An adopted claim carries its AI origin forever and is **never
absorbed into the editor's authorship**. The column is `IMM`, and there is no command in
`api-command-contracts.md` that writes it after insert.

### 2.4 Axis 4 — Conflict (orthogonal flag set)

Zero or more conflict flags, each a link to a conflict record. Conflict is **orthogonal**: a
`CANONICAL` item may carry an open conflict, and an item with no conflict flag is not thereby
true.

Conflict classes, from `knowledge/conflict-and-provenance-model.md`:

`SOURCE_CONFLICT` · `CLAIM_CONFLICT` · `VERSION_CONFLICT` · `SCOPE_CONFLICT` ·
`TEMPORAL_CONFLICT` · `AUTHORITY_CONFLICT` · `IDENTITY_CONFLICT`

### 2.5 The orthogonality rule, stated as a constraint

**Rule K-2.** An approved assumption is `ASSUMPTION` + `APPROVED` and **stays an assumption**.
No combination of the four axes is collapsed, derived, or defaulted from another. Specifically:

- there is no column, view or API field that merges epistemic type and governance state;
- there is no column that merges epistemic type and origin;
- `CANONICAL` is a governance state, never an epistemic type;
- `AI_SUGGESTION` is an epistemic type, never an origin.

This rule exists because Phase 2 held a single flat list of twelve labels and Phase 8 replaced
it with four axes precisely to stop authority quietly converting one kind of knowledge into
another. The Phase 12 reference implementation reintroduced the collapse in a two-valued
`Canonicality` enum; this specification does not inherit it.

## 3. `AI_SUGGESTION` never converts

**Rule K-3.** No human, model, reviewer, editor or authority converts `AI_SUGGESTION` into
another epistemic type by status change, acceptance, review, editing or approval. **There is no
transition.** The state machine in §6 contains no edge out of `AI_SUGGESTION` on the epistemic
axis, and the implementation must make that edge unrepresentable rather than merely unused.

Adoption works like this, and only like this:

1. a **new knowledge item** is created, with the epistemic type its own basis supports —
   `FACT_CLAIM` if evidence supports a claim, `INFERENCE` if reasoning does, `ASSUMPTION` if
   neither does but the position is adopted anyway, `CALCULATION` if it is derived;
2. the new item is linked to the proposal it came from;
3. the new item carries `AI_GENERATED` or `AI_ASSISTED` origin **permanently**;
4. the original `AI_SUGGESTION` **remains, historically, as what it was** — not rewritten, not
   relabelled, not deleted. Its governance state may become `SUPERSEDED` or `REJECTED`.

**Rule K-4 — human acceptance is not an evidential basis.** A record whose only support for a
`FACT_CLAIM` is "a person accepted the AI's proposal" fails the promotion preconditions in §7.
This is checked, not assumed: the adopted item's evidence links must resolve to `EVIDENCE`
items, and an adoption link to an `AI_SUGGESTION` does not count as one.

## 4. Persisted record — `knowledge_item`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `knowledge_ref` | `KnowledgeRef` | NO | IMM | Logical item identity, stable across versions |
| `item_version` | int | NO | IMM | PK with `knowledge_ref`; monotonic; **no in-place edit anywhere** |
| `epistemic_type` | enum §2.1 | NO | IMM | Never changes within a version; never changes across versions of the same item |
| `governance_state` | enum §2.2 | NO | APP | Changes only by a recorded transition (§6) |
| `origin` | enum §2.3 | NO | IMM | Rule K-1 |
| `scope_path` | `ScopePath` | NO | IMM | Exactly one |
| `memory_class` | enum §5 | NO | IMM | |
| `sensitivity_labels` | label set | NO | APP | Carried through every transfer and use |
| `subject_key` | text | NO | IMM | What the item is *about*; the unit `CANONICAL` is unique on |
| `statement` | text | NO | IMM | The assertion itself |
| `evidence_links` | set of `KnowledgeRef` | YES | APP | Must resolve to `EVIDENCE` items |
| `source_links` | set of `KnowledgeRef` | YES | APP | Must resolve to `SOURCE` items |
| `derivation` | structured | YES | IMM | Required for `CALCULATION`: method, inputs, input versions |
| `reasoning` | text | YES | IMM | Required for `INFERENCE` |
| `adopted_from` | `KnowledgeRef` | YES | IMM | Set on an item adopted from an `AI_SUGGESTION`; never satisfies `evidence_links` |
| `conflict_flags` | set of `ConflictRef` | YES | APP | Orthogonal |
| `freshness_policy` | structured | YES | IMM | Refresh interval and basis |
| `asserted_at` | timestamp | NO | IMM | |
| `effective_from` / `effective_to` | timestamp | NO / YES | IMM / APP | Temporal validity, distinct from record time |
| `supersedes` / `superseded_by` | `KnowledgeRef`+version | YES | APP | Lineage links, append-only |
| `retraction` | structured | YES | APP | Reason and **level withdrawn from**; required when state is `RETRACTED` |
| `created_by_*` | identity stamps | NO | IMM | Separate human and system identity columns |

Constraints:
`PRIMARY KEY (knowledge_ref, item_version)`;
`UNIQUE (knowledge_ref, item_version)`;
check: `epistemic_type = 'CALCULATION' → derivation IS NOT NULL`;
check: `epistemic_type = 'INFERENCE' → reasoning IS NOT NULL`;
check: `governance_state = 'RETRACTED' → retraction IS NOT NULL`;
check: `governance_state = 'CANONICAL' → epistemic_type IN ('FACT_CLAIM','CALCULATION','INFERENCE')`;
check: epistemic type is identical across all versions of one `knowledge_ref` (enforced by a
trigger-equivalent constraint or by an immutable `epistemic_type` column on a parent
`knowledge_identity` table — the second is preferred because it makes K-3 structural).

**Rule K-5 — no in-place edit.** Correcting an item creates a **new linked version**. There is
no `UPDATE` of `statement`, `epistemic_type`, `origin`, `derivation`, `reasoning`,
`subject_key` or `scope_path` anywhere in this specification.

## 5. Memory classes

From `knowledge/memory-class-model.md`, used unchanged:

| Class | Retention | Promotable? |
|---|---|---|
| `WORKING_MEMORY` | Ends with the task | No |
| `EPISODIC_MEMORY` | Retained; never re-opened | No |
| `SEMANTIC_MEMORY` | Retained, versioned | **Yes**, via governance state |
| `PREFERENCE_MEMORY` | Retained | **Never** |
| `PROCEDURAL_MEMORY` | Retained, versioned | **Yes**, as method |
| `AUDIT_MEMORY` | Append-only, permanent | No — it records, it does not assert |

**Rule K-6.** `PREFERENCE_MEMORY` is never promotable to any governance state above `DRAFT`.
How someone prefers to work is not a claim about the world, and an implementation that lets a
preference become `CANONICAL` has made a convention into a position.

## 6. Governance-state transitions

Permitted transitions on the governance axis. The epistemic axis has **no** transitions.

| From | Permitted to | Requires |
|---|---|---|
| `DRAFT` | `REVIEWED`, `REJECTED`, `RETRACTED` | A Review Instance `SATISFIED` for `REVIEWED` |
| `REVIEWED` | `APPROVED`, `REJECTED`, `RETRACTED`, `DRAFT` (new version) | A Decision Record under a bounded approval Right for `APPROVED` |
| `APPROVED` | `CANONICAL`, `SUPERSEDED`, `RETRACTED` | §7 preconditions **and** a mapped promotion Right for `CANONICAL` |
| `CANONICAL` | `SUPERSEDED`, `RETRACTED` | A new promoted version for `SUPERSEDED`; a retraction record otherwise |
| `SUPERSEDED` | `RETRACTED` | A retraction record |
| `RETRACTED` | — | Terminal |
| `REJECTED` | — | Terminal |

**Rule K-7.** `REVIEWED` is not reachable from `APPROVED` or `CANONICAL` by "re-review": a new
review produces a new Review Instance against the same item version, and any change of position
is a new item version. Governance states never travel backwards on one version.

**Rule K-8 — rollback.** Restoring an earlier position **re-promotes the earlier content as a
new version** through the ordinary governed act. It does not erase what happened in between, and
the intervening versions remain readable.

## 7. Canonical promotion — preconditions and the blocked authority

`CANONICAL` is a property of a **(claim version, scope)** pair: scoped, versioned,
effective-dated, evidence-bound and revocable. It is **not** global, not permanent, not a claim
of truth, and not a visibility level.

### 7.1 Preconditions, all of which must hold

| # | Precondition |
|---:|---|
| 1 | Epistemic type is promotable (§2.1) |
| 2 | Governance state is `APPROVED` |
| 3 | An applicability mode is **declared** (never inferred) |
| 4 | Evidence links resolve, at the versions recorded, and are `EVIDENCE` items |
| 5 | No **material** unresolved conflict on the contested point (§8) |
| 6 | Freshness is `CURRENT_FOR_USE`, or `STALE_BUT_USABLE` with disclosure where the criticality band permits — at Enhanced Decision-Grade, **stale is blocking** |
| 7 | The criticality band's review independence requirement is satisfied by a Review Instance of the required class |
| 8 | A scope and an effective date are named |
| 9 | **A Decision Record exists, made by an eligible human under a mapped canonical-promotion Decision Right** |

### 7.2 Precondition 9 is currently unsatisfiable — and that is the correct behaviour

`decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change` exist
in `decisions/master-decision-right-universe.md` as **uncarded candidates**. Phase 8
`knowledge/canonical-promotion-governance.md` §7 defines the semantics and **specifies the
Phase 7 pass that must card the Right**, deliberately creating no authority.

Therefore:

> **The `PROMOTE_TO_CANONICAL` operation is specified, and is
> `BLOCKED / UNIMPLEMENTABLE UNTIL RIGHT IS MAPPED`.**

The implementation builds the enforcement hook — the precondition check, the Decision Record
lookup, the Canonical Record writer — and the hook **refuses every call** with
`NO_APPLICABLE_DECISION_RIGHT` until a Phase 7 governed change cards the Right. Phase 14 does
**not** create the Right, does not name a placeholder Right, and does not provide a
configuration flag that bypasses precondition 9. See
`open-items-and-blocked-authorities.md` BA-1.

### 7.3 `canonical_record`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `canonical_ref` | `CanonicalRecordRef` | NO | IMM | |
| `canonical_version` | int | NO | IMM | PK with `canonical_ref` |
| `knowledge_ref` + `item_version` | ref pair | NO | IMM | The exact promoted claim version |
| `scope_path` | `ScopePath` | NO | IMM | |
| `subject_key` | text | NO | IMM | |
| `applicability_mode` | enum | NO | IMM | `NOT NULL`; declared, never inferred |
| `conditions` | structured | YES | IMM | Required when mode is `CONDITIONALLY_APPLICABLE` |
| `effective_from` / `effective_to` | timestamp | NO / YES | IMM / APP | |
| `promotion_decision_record` | `DecisionRecordRef` | NO | IMM | **`NOT NULL`.** The whole of precondition 9 |
| `evidence_snapshot` | set of ref+version | NO | IMM | Recorded values |
| `supersedes` / `superseded_by` | ref+version | YES | APP | |
| `status` | `ACTIVE` \| `SUPERSEDED` \| `RETRACTED` | NO | APP | |

Constraint: `UNIQUE (subject_key, scope_path, canonical_version)` and a partial unique index
enforcing **at most one `ACTIVE` canonical record per `(subject_key, scope_path)`**.

**Rule K-9.** Promotion writes a *new* `canonical_record` version and marks the prior one
`SUPERSEDED` in the same transaction. Nothing is overwritten and nothing is deleted.

## 8. Conflict handling

**Rule K-10 — materiality, not count, is what blocks.** A conflict blocks canonical promotion
or decision-grade use **where the claim or the decision depends on the contested point**. An
immaterial conflict — a disagreement about something the statement does not rest on — stays
visible and documented and blocks nothing, at any band.

**Rule K-11 — unassessed is material.** An unassessed conflict is treated as material until
someone assesses it. At Enhanced Decision-Grade every open conflict needs an explicit materiality
assessment that is **attributable to a named eligible Role and reviewable**; silence is not a
finding of immateriality.

**Rule K-12.** Materiality is never inferred from retrieval ranking, model confidence, source
count, or nobody having raised it. There is no automatic conflict resolution path in this
specification for any conflict class, and `IDENTITY_CONFLICT` in particular has none.

`conflict_record` fields: `conflict_ref`, `conflict_class`, `subject_key`, `scope_path`,
`sides` (each a knowledge ref+version), `raised_by_*`, `raised_at`, `materiality_assessment`
(nullable; structured, carrying the assessing Role and the reasoning),
`resolution` (nullable; structured, carrying the governed act that resolved it), `status`
(`OPEN` | `ASSESSED_IMMATERIAL` | `RESOLVED` | `ESCALATED`).

**Rule K-13.** Raising a flag needs no authority. **Clearing one does.** A model may detect a
conflict and propose an update; both are useful and neither is a promotion.

## 9. Freshness

| Verdict | Meaning |
|---|---|
| `CURRENT_FOR_USE` | Adequate for this use |
| `STALE_BUT_USABLE` | Past its refresh interval, usable for this use, **with the staleness disclosed at the point of use** |
| `STALE_AND_BLOCKING` | Past its refresh interval and not usable for this use until refreshed |

**Rule K-14.** Freshness is a verdict about an **item in a use context**, not a property of the
item alone. The same item may be `CURRENT_FOR_USE` for one task and `STALE_AND_BLOCKING` for
another at the same instant, and the implementation computes and **records** the verdict per
use, never caching it on the item.

## 10. Stored, retrievable, selected, authoritative, canonical

Five different properties. The distance between the first and the last is the whole of this
section, and the implementation must keep them in five different mechanisms.

| Property | Established by | Implementation locus |
|---|---|---|
| **Stored** | Retention | C10 row exists |
| **Retrievable** | Indexing | Any index, of any cleverness |
| **Selected into context** | Selection — relevance, recency, similarity, any mechanism at all | Retrieval layer |
| **Authoritative for this task** | Scope applicability plus the task's own requirements | C3 + C4 applicability resolution |
| **Canonical for this scope** | Governed promotion | `canonical_record` with `promotion_decision_record` |

**Rule K-15.** Retrieval rank, similarity score, relevance, recency or model confidence **never
determines authority or canonical status.** Selection is a convenience mechanism, permitted to
be as clever as it likes, with **no governance meaning whatsoever**. Something surfaced first is
not thereby more true, more current or more applicable; something not surfaced is not thereby
superseded; **an item's absence from a context window is not evidence about the item.**

**Rule K-16.** No retrieval design, ranking method, embedding, index or vector store is
specified here, and none may appear on a governed path. A retrieval component may read C4; C4
never reads a retrieval score.

## 11. Artifacts and knowledge

| # | Rule |
|---:|---|
| 1 | One document contains many claims in different states, simultaneously |
| 2 | **An approved document is not wholly canonical.** Approving a document authorises reliance on it for a purpose; it promotes nothing |
| 3 | One canonical statement may appear in many artifacts, at whatever version each was written against |
| 4 | Replacing an artifact rewrites no canonical history |
| 5 | Deleting an artifact deletes no canonical or audit record |
| 6 | A generated document must cite the currently applicable canonical version, and must state where it relied on something stale, assumed or conflicted |
| 7 | A downstream artifact carries open assumptions and conflicts explicitly, **at the point of reliance** |

The relationship between artifact and knowledge is **many-to-many and is not identity**; it is
persisted as an explicit link table, never as a foreign key on either side.

## 12. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `Origin = {AI_GENERATED, HUMAN_AUTHORED}` | The four approved origins, spelled `HUMAN_ORIGIN`, `AI_ASSISTED`, `AI_GENERATED`, `EXTERNAL_ORIGIN` | Phase 8 §2a. `HUMAN_AUTHORED` is not an approved value and `AI_ASSISTED` / `EXTERNAL_ORIGIN` were inexpressible |
| D2 | `Canonicality = {AI_SUGGESTION, CANONICAL}` — one axis mixing an epistemic type and a governance state | Two separate axes, §2.1 and §2.2 | Phase 8 §1; Phase 13 M-1 |
| D3 | No conflict, freshness, memory class, applicability or canonical record | §2.4, §5, §8, §9, §7.3 | Phase 8 in full |
| D4 | No canonical promotion path at all | Specified **and blocked** at precondition 9 | Phase 8 §7; authority is not invented |
