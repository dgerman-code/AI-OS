# AI-OS Memory and Canonical Governance

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Depends on: approved Phase 3 Role Registry, Phase 4 Skill Registry, Phase 5 Workflow Registry, Phase 6 Handoff & Review architecture, Phase 7 Decision Rights architecture

## Purpose

Phase 2 listed twelve knowledge labels and governed none of them. Every phase since has leaned on that list: Phase 5 stages carry open items with knowledge states, Phase 6 reviews find `CONFLICT_DETECTED` and `UNKNOWN` and may not change them, Phase 7 states that a Decision Right may act on what to *do* about the state of knowledge and never on what that state *is* — and pointed at a canonical-promotion authority nobody had defined.

Phase 8 is where the thing all of them defer to acquires a definition. It governs **what the organisation knows, how that knowledge is stated, where it holds, and what makes it the organisation's position.** It builds no memory system.

## The separation this phase must preserve

```
SOURCE != EVIDENCE != MEMORY ITEM != KNOWLEDGE CLAIM != CANONICAL RECORD
      != DECISION RIGHT != DECISION RECORD != ARTIFACT != MODEL != RUNTIME
```

| Object | Is |
|---|---|
| **Source** | Raw material the entity holds. Cited, never promoted |
| **Evidence** | A located extraction from a source, bearing on a claim |
| **Memory item** | Something retained, of any class. **Retention is not assertion** |
| **Knowledge claim** | An assertion the entity makes, with an epistemic type and a governance state |
| **Canonical record** | The entity's governed position on a subject, for a scope, at a version |
| **Decision Right / Record** | Phase 7's. Authority to act, and evidence that authority was exercised |
| **Artifact** | A document or output. Expresses claims; **is not a claim** |
| **Model / runtime** | Implementation. Out of scope, and never a holder of anything |

### The governing rule

> **Memory is not truth. Evidence is not approval. Approval is not canonical promotion. And canonical status never arises from model confidence, retrieval rank, repetition, consensus among sources, or nobody having objected.**

Each clause names a real collapse. The last is the one an AI-native system is uniquely exposed to, because every mechanism it has for surfacing knowledge — similarity, ranking, frequency — is a mechanism for making something *look* established.

## 1. Component documents

| Document | Owns |
|---|---|
| `knowledge/knowledge-state-model.md` | Epistemic types, governance states, conflict flag, permitted transitions |
| `knowledge/scope-isolation-and-transfer.md` | The approved scope graph, the four applicability modes, isolation, governed transfer, ancestor fallback |
| `knowledge/memory-class-model.md` | The six memory classes and their boundaries |
| `knowledge/conflict-and-provenance-model.md` | Conflict taxonomy and resolution; provenance and lineage |
| `knowledge/canonical-promotion-governance.md` | The seven canonical acts; the two bounded authorities; Phase 7 integration |
| `knowledge/sensitivity-and-retention-model.md` | Sensitivity classes; item temporal facts versus use-context verdicts; end states; retention |
| `knowledge/_templates/` | Knowledge Record and Canonical Record semantic models |
| `knowledge/_standards/common-knowledge-governance-constraints.md` | The enforceable rules every record inherits |
| `knowledge/master-knowledge-governance-universe.md` | Inventory, upstream reference accounting, deferred work |

## 2. Four axes, held at once

A knowledge item is not one label. It carries an **epistemic type** (what it is), a **governance state** (how far governance has taken it), an **origin** (where it came from — permanent), and **zero or more conflict flags** — plus a scope, a memory class and a sensitivity classification. An approved assumption is `ASSUMPTION` + `APPROVED` and stays an assumption; that is the structural reason authority cannot quietly convert one kind of knowledge into another. Full model: `knowledge/knowledge-state-model.md`.

## 3. Canonical status, precisely

`CANONICAL` is a property of a **(claim version, scope)** pair: scoped, versioned, effective-dated, evidence-bound and revocable. It is **not** global, not permanent, not a claim of truth, and not a visibility level. It answers *what is the organisation's governed position here, now* — and nothing else.

## 4. What Phase 8 does not touch

**Approved Phase 3–7 semantics are unchanged.** Phase 8 adds a layer beneath them and rewrites none of it:

| Phase | Boundary preserved |
|---|---|
| 3 — Roles | Professional conclusions stay Role-owned. **Phase 8 grants no Role any authority**, and no knowledge state confers competence |
| 4 — Skills | Untouched |
| 5 — Workflows | A Workflow coordinates and satisfies no gate. **No Workflow promotes anything** |
| 6 — Reviews | A review may find, and may not approve. **Nothing in Phase 8 changes a review status**, and `REVIEWED` remains "examined", not "true" |
| 7 — Decision Rights | Authority acts on what to do, never on what is. **Phase 8 cards no Decision Right and grants none** |

Phase 8 resolves exactly one forward reference — the canonical-promotion authority Phases 6 and 7 both pointed at — and resolves it by **defining semantics and specifying the Phase 7 pass that must card it**, not by creating authority here. See `knowledge/canonical-promotion-governance.md` §7.

## 5. Human correction and AI contribution

1. **`AI_SUGGESTION` never becomes another epistemic type.** Not by acceptance, approval, review, editing or promotion. Where evidence or reasoning supports adoption, a **new linked knowledge item** is created with the type its own basis supports, and the proposal remains historically as what it was (`knowledge/knowledge-state-model.md` §2a). **Human acceptance is not an evidential basis.**
2. **A model may detect a conflict and propose an update.** Both are useful and neither is a promotion — raising a flag needs no authority, and clearing one does.
3. **Origin is permanent provenance, not a knowledge state.** Every item carries `HUMAN_ORIGIN`, `AI_ASSISTED`, `AI_GENERATED` or `EXTERNAL_ORIGIN`, and **nothing changes it** — not adoption, not editing, not promotion. An adopted claim carries its AI origin forever, and it is never absorbed into the editor's authorship.
4. **Correcting a canonical item creates a new linked version**, promoted, superseding the old. There is no in-place edit anywhere in this architecture.
5. **Rollback restores applicability through a new governed act.** It re-promotes the earlier content as a new version; it does not erase what happened in between, and the intervening versions remain readable.
6. **Administrator or user override does not bypass evidence, review or authority requirements.** There is no privileged path, and a system that has one has the requirements as decoration.

## 6. Artifacts and knowledge

An artifact is a document; a knowledge object is a claim. The relationship is many-to-many and is not identity.

1. **One document contains many claims in different states** — an approved report may carry facts, assumptions, an unresolved conflict and a stated unknown, simultaneously.
2. **An approved document is not wholly canonical.** Approving a document authorises reliance on the document for a purpose. It promotes nothing, and this is the single most common way unearned canonical status is acquired in practice.
3. **One canonical statement may appear in many artifacts**, at whatever version each was written against.
4. **Replacing an artifact rewrites no canonical history.** A new report supersedes a report; it supersedes no canonical statement.
5. **Deleting an artifact deletes no canonical or audit record.** They are different objects with different lifecycles.
6. **A generated document must cite the currently applicable canonical version** where the claim is one canonical governance covers — and must state where it has relied on something stale, assumed or conflicted.
7. **A downstream artifact carries open assumptions and conflicts explicitly**, in the artifact, at the point of reliance. Phase 5's open-item carry and Phase 6's finding carry are the same discipline applied to documents.

## 7. Stored, retrievable, selected, authoritative, canonical

Five different properties, and the distance between the first and the last is the whole of this section.

| Property | Means | Established by |
|---|---|---|
| **Stored** | It is retained | Retention |
| **Retrievable** | It can be found | Indexing |
| **Selected into context** | It is in front of the work right now | Selection — relevance, recency, similarity, any mechanism at all |
| **Authoritative for this task** | It is what the work must rely on | Scope applicability plus the task's own requirements |
| **Canonical for this scope** | It is the organisation's governed position | Governed promotion |

> **Retrieval rank, similarity score, relevance, recency or model confidence never determines authority or canonical status.**

Selection is a convenience mechanism and is permitted to be as clever as it likes. It has no governance meaning whatsoever: something surfaced first is not thereby more true, more current or more applicable, and something not surfaced is not thereby superseded. **An item's absence from a context window is not evidence about the item.** Equally, the authoritative item for a task may be one no retrieval mechanism surfaced — in which case the work is missing it, and the retrieval mechanism has not changed what the work required.

No retrieval design, ranking method, embedding, index or model routing is specified here or anywhere in Phase 8.

## 8. Non-runtime statement

This document and every artifact in `knowledge/` is declarative architecture. Nothing here implements or specifies a database schema, vector store, embedding model, retrieval pipeline, search ranking, API, user interface, notification, cache, storage engine, retention job, access-control mechanism, identity system, authentication, model routing, agent execution or orchestration. A later runtime **validates against** these semantics and does not mutate them.

## 9. Criticality and canonical rigour

Criticality bands are Phase 3's (`architecture/project-criticality-policy.md`) and are used, not rewritten. Higher criticality raises the **rigour required**, never the standard of truth: a claim does not become truer by being promoted under a stricter gate, and does not become false by being adequate under a lighter one.

| | Routine / Standard | Enhanced Review Candidate | Enhanced Decision-Grade |
|---|---|---|---|
| Evidence depth | Source cited | Source and located evidence | Located evidence, corroboration where the claim is load-bearing |
| Review independence | Producer review may suffice | Peer or cross-domain review | **Independent assurance review**, per Phase 6's classes |
| Provenance completeness | Gaps stated | Gaps stated and justified | **Chain complete or the omission explicitly justified per step** |
| Freshness | `STALE_BUT_USABLE` with disclosure | Disclosure plus a refresh plan | **Stale is blocking — refresh before use** |
| Conflict tolerance | Unresolved **material** conflict blocks; immaterial conflicts stay visible | Same rule; materiality assessed on the record | Same rule, **with a recorded, attributable materiality assessment required for every open conflict** — silence is not a finding of immateriality |
| Promotion gate | Promotion authority | Promotion authority | Promotion authority, with Phase 7 separation from any exception taken to reach it |
| Multi-authority | Not required | Not required | Where Phase 7 cardinality requires it — a Phase 7 determination, not one made here |

**Materiality, not count, is what blocks.** A conflict blocks canonical promotion or decision-grade use where **the claim or the decision depends on the contested point**. An immaterial conflict — a disagreement about something the statement does not rest on — stays visible and documented and blocks nothing, at any band. What criticality changes is the **tolerance and the burden**: at Enhanced Decision-Grade, every open conflict needs an explicit materiality assessment that is **attributable to a named eligible Role and reviewable**, and an unassessed conflict is treated as material until someone assesses it. Materiality is never inferred from retrieval ranking, model confidence, or nobody having raised it.

**Criticality changes depth, never identity or truth** — the same rule Phase 3 set for Roles, applied to knowledge.

## 10. Status

All Phase 8 artifacts are `PROPOSED`. Nothing is APPROVED or CANONICAL, no Decision Right is created, no Role gains anything, and inclusion here confers no authority on anyone.
