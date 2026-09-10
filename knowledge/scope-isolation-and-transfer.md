# Scope, Isolation and Governed Transfer

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## Purpose

`architecture/context-hierarchy.md` (Phase 2, approved) states the hierarchy. It does not say what a scope *does* to knowledge. This document does, and it does so without implementing identity, permission or access control.

## 1. Scope hierarchy

```
GLOBAL
 └── ORGANISATION
      ├── PERMANENT FUNCTION / BUSINESS AREA
      ├── PROGRAMME / PORTFOLIO   ──┐
      ├── PRODUCT / PLATFORM      ──┤
      └── PROJECT                 ──┴── WORKSTREAM ── TASK
```

`PERSONAL` is a **separate scope family**, not a level of this tree:

```
PERSONAL (per human)
 └── WORKSTREAM / TASK
```

Scope identity is a path — `ORGANISATION/acme`, `PROJECT/alpha`, `PERSONAL/<human>` — and is **structural, never a name match**: two projects called "Phase 2" in different programmes are two scopes, and the registry never resolves them to each other by string similarity. Same-name disambiguation is by path, always.

## 2. Inheritance: applicability flows down, authority does not

Two things are routinely conflated and are kept apart here.

| | Direction | Rule |
|---|---|---|
| **Applicability** | Downward only | A canonical statement at `ORGANISATION` is **applicable** in every descendant scope unless a nearer scope holds its own canonical statement on the same subject |
| **Authority** | Never flows | Being inside a scope confers no authority over it. Authority is Phase 7's, is held by eligibility class, and is not derived from scope membership |

**Nearest-scope-wins.** Where an ancestor and a descendant both hold a canonical statement on the same subject, the descendant's governs *inside* the descendant, and the ancestor's continues to govern everywhere else. This is an override, not a contradiction, and the descendant record **must name the ancestor statement it overrides** — an unnamed override is a scope conflict (see `knowledge/conflict-and-provenance-model.md`).

**Nothing flows upward, ever.** A project's canonical statement is not the organisation's position. A workstream cannot canonicalise for its project. The most common real failure this prevents: a parameter agreed inside one project quietly becoming "what the organisation assumes" because nobody said otherwise.

**Nothing flows sideways.** Sibling projects, sibling programmes and two organisations share nothing by default.

## 3. Visibility is not authority, and neither is either one applicability

Three separate questions, routinely answered as one:

- **Visible?** — may a reader see it (a sensitivity and runtime question);
- **Applicable?** — does it govern in this scope (this document);
- **Authoritative for this task?** — is it what the current work must rely on (`architecture/memory-canonical-governance.md` §7).

An item can be visible and not applicable, applicable and not currently relied on, and — the case worth naming — **canonical in a scope a reader cannot see**. Canonical status implies no visibility, and visibility implies no applicability.

## 4. Cross-scope reference: reference, never copy

A scope may **reference** knowledge from another scope. It may not **absorb** it.

| Mechanism | What it does | Status of the result |
|---|---|---|
| `SCOPE_REFERENCE` | Cites another scope's item at a named version, in place | The item stays where it is, under its own scope's governance. The citing scope gains no canonical statement |
| `GOVERNED_TRANSFER` | Proposes an item for adoption into another scope | Produces a **new candidate record in the receiving scope**, requiring the receiving scope's own review and promotion |
| silent copy | — | **Prohibited.** Not a mechanism; a defect |

A `SCOPE_REFERENCE` carries the source scope path and the referenced version. When that version is superseded or retracted, the reference does not silently follow it: the citing record's freshness trigger fires and the citing scope decides.

## 5. Governed transfer and revalidation

**Knowledge from one organisation, project or personal scope does not become canonical or presumed applicable in another scope without an explicit governed transfer and revalidation.**

A transfer records, at minimum:

1. the source scope path, item identity and **exact version**;
2. the receiving scope path;
3. the reason the item is expected to hold in the receiving scope;
4. **what was revalidated, and what was not** — carried forward as open items where not;
5. the receiving scope's own review outcome;
6. the receiving scope's own promotion decision, where canonical status is sought;
7. what changes in the receiving context could invalidate it.

Rules:

- **A transfer never carries canonical status with it.** An item canonical in the source arrives in the receiver as a candidate with strong provenance and no status.
- **A transfer never carries review satisfaction with it.** The source's review satisfied the source's requirements.
- **Transfer is not transitive.** A → B → C requires two transfers, each revalidated; C may not cite A's original review as its basis.
- **Provenance survives transfer intact.** The receiving record's lineage begins at the original source, not at the transfer.
- **A transfer that cannot say what was revalidated has not revalidated anything.**

## 6. Contamination: the four directions that must not happen

| Contamination | Example | Prevented by |
|---|---|---|
| **Personal → organisational** | A human's working convention, note or preference becoming an organisational position | §7 below; preference memory is never canonical |
| **Project → project** | A parameter from one client's project applied to another's because the subject looked the same | §4 — no silent copy; §2 — nothing flows sideways |
| **Project → organisation** | A project-specific figure becoming "the company's number" by reuse | §2 — nothing flows upward |
| **Organisation → organisation** | Anything at all crossing between two client organisations | §4 — reference or governed transfer only, and confidentiality classes may forbid even that |

Two same-named subjects in different scopes are **different subjects until a governed act says otherwise.** Entity resolution across scopes is an identity conflict (`conflict-and-provenance-model.md` §2), not an inference the system may make on its own.

## 7. `PERSONAL` scope

`PERSONAL` is separated from the organisational tree because its content is a different kind of thing: how a person prefers to work, what they are drafting, what they have not yet shared.

- **Personal-scope knowledge is never canonical for any organisational scope**, at any level, by any route short of a governed transfer that produces a new organisationally-owned record with its own evidence and review.
- **Preference memory is never canonical anywhere** — see `knowledge/memory-class-model.md` §4.
- **Personal scope does not inherit downward into organisational scopes**, and organisational canonical statements are applicable to work done in personal scope without becoming personal property.
- A personal item that ought to be organisational is **transferred, with attribution**, not adopted by absorption.

## 8. Context switching

When work moves between scopes, the applicable canonical set changes with it. Three rules:

1. **Applicability is recomputed at the new scope**, never inherited from the previous task's context.
2. **Working memory does not travel.** What was in context for the previous task is not in context for the next one by default (`memory-class-model.md` §2).
3. **An item carried across deliberately is carried as a reference or a transfer**, with the scope change recorded — never as an unmarked residue of the previous context.

## 9. What this document does not do

It defines no permission model, no access-control rule, no tenancy mechanism, no partitioning strategy, no identity system and no storage layout. Scope is a **governance boundary**; a later runtime enforces it and does not redefine it. Sensitivity classification is a separate axis entirely (`knowledge/sensitivity-and-retention-model.md`) and is not a scope.

## 10. Status

`PROPOSED`. Confers no authority and implements nothing.
