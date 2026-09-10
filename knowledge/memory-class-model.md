# Memory Class Model

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## 1. Architecture classes, not registry types

The seven classes below are **architecture classes**, not first-class registry types. They classify what a knowledge item is *for*; they are not a registry of cards, they have no IDs, nothing is "registered as" a memory class, and no Role, Workflow, Handoff, Review or Decision Right references one.

The reason is deliberate. A registry type would invite runtime to implement seven stores, and the classes are not stores — they are governance postures over material that may sit anywhere. `CANONICAL_MEMORY` is not a place; it is the set of records holding canonical status for a scope.

## 2. The classes

| Class | Holds | Lifetime | May be canonical? |
|---|---|---|---|
| `WORKING_MEMORY` | Short-lived task or workflow context — what is currently in hand | The task | **No** |
| `EPISODIC_MEMORY` | What happened: actions, events, exchanges, decisions taken | Retained | **No** — see §3 |
| `SEMANTIC_MEMORY` | Reusable claims, definitions, parameters, facts about the world | Retained, versioned | **Yes** |
| `PREFERENCE_MEMORY` | How a person or organisation prefers to work — conventions, formats, tone, defaults | Retained | **Never** — see §4 |
| `PROCEDURAL_MEMORY` | Governed methods, playbooks, instructions — how something is to be done | Retained, versioned | **Yes**, as method — see §5 |
| `CANONICAL_MEMORY` | The records currently holding canonical status for a scope | Versioned, superseded, never overwritten | **Is** canonical |
| `AUDIT_MEMORY` | The historical trail: evidence considered, reviews performed, decisions made, transitions taken | Append-oriented, permanent | **No** — it records, it does not assert |

## 3. Class rules

1. **Working memory cannot self-promote.** Nothing becomes durable because it was in context, was useful, was repeated across tasks, or was never contradicted. Promotion out of working memory is a governed act, every time.
2. **Working memory does not travel between scopes or tasks.** Its expiry is the task's end, and residue from a previous task is contamination, not continuity.
3. **Episodic memory does not imply ongoing validity.** That something was decided, said, or done is a durable fact *about the past*. It is not evidence that it still holds — and treating "we agreed this in March" as a current position is the most common way stale knowledge re-enters live work.
4. **Preference memory never overrides law, fact, evidence or canonical knowledge.** A preference governs presentation and convention. Where a preference and an evidenced claim disagree, the preference loses without a contest, and where a preference and a legal requirement disagree, the preference is void.
5. **Procedural memory grants no authority.** A playbook describing who approves something is a description of the governed arrangement, not a grant of the approval. Following a procedure does not make its follower a holder of any Decision Right.
6. **Canonical memory is not a cache.** It is not a fast copy of something authoritative elsewhere, it is not invalidated by a source refresh, and it is never repopulated from a fetch. Its contents change only by governed promotion, supersession or retraction.
7. **Audit memory is append-oriented and history-preserving.** Corrections are appended and linked. Nothing in it is edited, and nothing in it is removed to make a record tidier.

## 4. Why preference memory is never canonical

Preference memory answers *how we like to work*; canonical memory answers *what the organisation's governed position is*. Promoting a preference would give a convention the standing of an evidenced position and let it be cited as one — the exact mechanism by which "we always use 8%" becomes an unexamined organisational parameter with nobody able to say where it came from.

Where a convention genuinely should bind — a standard discount rate, a required format — it is **not a preference**. It is a `SEMANTIC_MEMORY` parameter or a `PROCEDURAL_MEMORY` method, adopted through the governed route, with evidence or an explicit adopting decision behind it. The route exists; the shortcut is what is refused.

Personal-scope preference memory additionally never leaves its scope (`knowledge/scope-isolation-and-transfer.md` §7).

## 5. Why procedural memory may be canonical, and in what sense

A method can be canonical **as the method** — "this is the governed way this organisation does this, at this version, in this scope". That is a claim about the organisation's own arrangements, which the organisation is competent to settle, and it is evidence-bound in the ordinary way: the adopting decision is its evidence.

It is **not** canonical as a claim about the world, and canonicality of a method is never inherited by its outputs. A canonical valuation method does not make a valuation produced by it canonical; the output goes through its own promotion, on its own evidence.

## 6. Interaction with the state model

A memory class does not replace an epistemic type or a governance state. Every item carries all three: an item in `SEMANTIC_MEMORY` may be `ASSUMPTION` + `APPROVED`, and an item in `CANONICAL_MEMORY` is by definition `CANONICAL` but may still be `INFERENCE` rather than `FACT_CLAIM`. The class says what the item is for; the type says what it is; the state says how far governance has taken it.

## 7. Status

`PROPOSED`. Defines no store, index, cache, TTL, eviction policy, embedding, retrieval mechanism or runtime.
