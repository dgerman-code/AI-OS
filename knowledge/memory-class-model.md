# Memory Class Model

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## 1. Architecture classes, not registry types

The six classes below are **architecture classes**, not first-class registry types. They classify what a knowledge item is *for*; they are not a registry of cards, they have no IDs, nothing is "registered as" a memory class, and no Role, Workflow, Handoff, Review or Decision Right references one.

The reason is deliberate. A registry type would invite runtime to implement **one store per class**, and the classes are not stores — they are governance postures over material that may sit anywhere. canonical status is not a place; it is a governance state a record holds.

## 2. The classes — six, after removing a duplicate

A memory class describes **retention and use character**: how long an item is kept, what it is for, and how it behaves over time. It says nothing about governance status.

| Class | Holds | Retention character | May hold canonical status? |
|---|---|---|---|
| `WORKING_MEMORY` | Short-lived task or workflow context — what is currently in hand | Ends with the task | **No** |
| `EPISODIC_MEMORY` | What happened: actions, events, exchanges, decisions taken | Retained; never re-opened | **No** — see §3 |
| `SEMANTIC_MEMORY` | Reusable claims, definitions, parameters, facts about the world | Retained, versioned | **Yes**, via governance state |
| `PREFERENCE_MEMORY` | How a person or organisation prefers to work — conventions, formats, defaults | Retained | **Never** — see §4 |
| `PROCEDURAL_MEMORY` | Governed methods, playbooks, instructions | Retained, versioned | **Yes**, as method — see §5 |
| `AUDIT_MEMORY` | The historical trail: evidence considered, reviews performed, decisions made, transitions taken | Append-only, permanent | **No** — it records, it does not assert |

**Class names are used in full, everywhere.** No shortened alias — `SEMANTIC`, `CANONICAL`, `AUDIT` on its own — appears in any model, template, exemplar or inventory, because a shortened name is one a runtime would have to guess at.

### `CANONICAL_MEMORY` was removed

The first Phase 8 draft listed a seventh class, `CANONICAL_MEMORY`, defined as "the records currently holding canonical status for a scope". The independent audit was right that this duplicates identity rather than adding a class:

1. **It restated the governance state.** Membership was exactly "governance state is `CANONICAL`", so the class carried no information the state did not.
2. **It duplicated Canonical Record identity.** The Canonical Record already *is* the object holding canonical status.
3. **It became undefined at the moment it mattered most.** When a record is superseded or retracted it leaves the class — and the model never said what it becomes, so a runtime would have to invent the answer for precisely the records whose history must not move.
4. **It made exemplars appear to mutate.** Records were written as `SEMANTIC` → `CANONICAL`, which reads as a class change where nothing about the item's retention character changed at all.

**The correction:** canonicality is a **governance state**, carried by a Canonical Record, and nothing else. A canonical claim is `SEMANTIC_MEMORY` with governance state `CANONICAL`; a canonical method is `PROCEDURAL_MEMORY` with governance state `CANONICAL`.

**The class does not change when the state does.** Promotion, supersession and retraction leave the memory class exactly where it was — which is the property the removed class lacked, and the reason historical identity now stays put:

| Event | Memory class | Governance state |
|---|---|---|
| Claim drafted | `SEMANTIC_MEMORY` | `DRAFT` |
| Promoted | `SEMANTIC_MEMORY` — **unchanged** | `CANONICAL` |
| Superseded by v2 | `SEMANTIC_MEMORY` — **unchanged** | `SUPERSEDED` |
| Retracted | `SEMANTIC_MEMORY` — **unchanged** | `RETRACTED` |

The count went from seven to six, and every reference was updated. It was not held at seven to protect a number.

## 3. Class rules

1. **Working memory cannot self-promote.** Nothing becomes durable because it was in context, was useful, was repeated across tasks, or was never contradicted. Promotion out of working memory is a governed act, every time.
2. **Working memory does not travel between scopes or tasks.** Its expiry is the task's end, and residue from a previous task is contamination, not continuity.
3. **Episodic memory does not imply ongoing validity.** That something was decided, said, or done is a durable fact *about the past*. It is not evidence that it still holds — and treating "we agreed this in March" as a current position is the most common way stale knowledge re-enters live work.
4. **Preference memory never overrides law, fact, evidence or canonical knowledge.** A preference governs presentation and convention. Where a preference and an evidenced claim disagree, the preference loses without a contest, and where a preference and a legal requirement disagree, the preference is void.
5. **Procedural memory grants no authority.** A playbook describing who approves something is a description of the governed arrangement, not a grant of the approval. Following a procedure does not make its follower a holder of any Decision Right.
6. **Canonical status is not a cache.** A canonical record is not a fast copy of something authoritative elsewhere, is not invalidated by a source refresh, and is never repopulated from a fetch. Canonical status changes only by governed promotion, supersession or retraction.
7. **Audit memory is append-oriented and history-preserving.** Corrections are appended and linked. Nothing in it is edited, and nothing in it is removed to make a record tidier.
8. **A memory class is not a governance status.** The class describes retention and use character; the status describes how far governance has taken the item. Neither is derivable from the other, and a governance act never changes the class.

## 4. Why preference memory is never canonical

Preference memory answers *how we like to work*; canonical memory answers *what the organisation's governed position is*. Promoting a preference would give a convention the standing of an evidenced position and let it be cited as one — the exact mechanism by which "we always use 8%" becomes an unexamined organisational parameter with nobody able to say where it came from.

Where a convention genuinely should bind — a standard discount rate, a required format — it is **not a preference**. It is a `SEMANTIC_MEMORY` parameter or a `PROCEDURAL_MEMORY` method, adopted through the governed route, with evidence or an explicit adopting decision behind it. The route exists; the shortcut is what is refused.

Personal-scope preference memory additionally never leaves its scope (`knowledge/scope-isolation-and-transfer.md` §7).

## 5. Why procedural memory may be canonical, and in what sense

A method can be canonical **as the method** — "this is the governed way this organisation does this, at this version, in this scope". That is a claim about the organisation's own arrangements, which the organisation is competent to settle, and it is evidence-bound in the ordinary way: the adopting decision is its evidence.

It is **not** canonical as a claim about the world, and canonicality of a method is never inherited by its outputs. A canonical valuation method does not make a valuation produced by it canonical; the output goes through its own promotion, on its own evidence.

## 6. Interaction with the state model

A memory class does not replace an epistemic type or a governance state, and does not overlap either. Every item carries all three plus an origin:

| Axis | Answers | Changed by |
|---|---|---|
| **Memory class** | What is it for, and how is it retained? | Rarely — and never by a governance act |
| **Epistemic type** | What kind of knowledge is it? | **Nothing.** A different type is a different, linked item |
| **Governance state** | How far has governance taken it? | Governed acts only |
| **Origin** (provenance) | Where did it come from — human, AI-assisted, AI-generated, external? | **Nothing. Permanent** |

An item in `SEMANTIC_MEMORY` may be `ASSUMPTION` + `APPROVED`; a `CANONICAL` record may be `INFERENCE` rather than `FACT_CLAIM`; and a canonical claim adopted from a model proposal carries `ORIGIN: AI_GENERATED` in its provenance forever. **No axis is derivable from another**, which is what makes each of them worth recording.

## 7. Status

`PROPOSED`. Defines no store, index, cache, TTL, eviction policy, embedding, retrieval mechanism or runtime.
