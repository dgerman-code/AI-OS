# Scope, Isolation and Governed Transfer

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## Purpose

`architecture/context-hierarchy.md` (Phase 2, approved) states the hierarchy. It does not say what a scope *does* to knowledge. This document does, and it does so without implementing identity, permission or access control.

## 1. Scope graph — the approved hierarchy, restored verbatim

The authoritative graph is `architecture/context-hierarchy.md`, approved at Phase 2 and unchanged through the Phase 7 approval baseline `c72ef03`. It is reproduced here **exactly as approved**, not summarised or reinterpreted:

```text
GLOBAL
│
├── ORGANISATION
│   ├── PERMANENT FUNCTION / BUSINESS AREA
│   ├── PROGRAMME / PORTFOLIO
│   │   └── PROJECT
│   │       └── WORKSTREAM
│   │           └── TASK
│   ├── PROJECT
│   │   └── WORKSTREAM
│   │       └── TASK
│   ├── PRODUCT / PLATFORM
│   │   └── WORKSTREAM
│   │       └── TASK
│   └── OPERATIONAL WORKSTREAM
│       └── TASK
│
├── INDEPENDENT BUSINESS / VENTURE
│   └── PROJECT / PRODUCT / WORKSTREAM / TASK
│
└── PERSONAL / AD-HOC INITIATIVE
    └── WORKSTREAM / TASK
```

The first Phase 8 draft compressed this into a single organisational chain and **lost four things**: `INDEPENDENT BUSINESS / VENTURE`, `OPERATIONAL WORKSTREAM`, the fact that `PROJECT` may sit **either** under a programme/portfolio **or** directly under the organisation, and `PERMANENT FUNCTION / BUSINESS AREA`. The independent audit was right, and it was right about the consequence as well as the omission: a project reachable by two different paths has two different sets of ancestors, so a compressed graph silently changes which statements are applicable to it.

### Distinct semantics of each node

| Node | What it is | Not to be conflated with |
|---|---|---|
| `GLOBAL` | Above any organisation — knowledge true of the world, not of an entity | `ORGANISATION` |
| `ORGANISATION` | One legal or operating entity | `GLOBAL`, and any other organisation |
| `PERMANENT FUNCTION / BUSINESS AREA` | A durable internal function — finance, legal, security. Persists across projects | `OPERATIONAL WORKSTREAM`, which is work, not a function |
| `PROGRAMME / PORTFOLIO` | A governed grouping of projects | A project; and a programme is **not** always present above one |
| `PROJECT` | A bounded endeavour — **reachable under a programme/portfolio, directly under the organisation, or under an independent business** | A workstream |
| `PRODUCT / PLATFORM` | A durable product line | A project, which ends |
| `OPERATIONAL WORKSTREAM` | Continuing operational work directly under the organisation, **ending at `TASK` with no project above it** | A project workstream |
| `WORKSTREAM` | A strand of work inside a project, product or venture | `OPERATIONAL WORKSTREAM` |
| `TASK` | One unit of work | Everything above it |
| `INDEPENDENT BUSINESS / VENTURE` | A venture **at the same level as `ORGANISATION`, not inside it** | A programme or product of the organisation |
| `PERSONAL / AD-HOC INITIATIVE` | A person's own scope, a **third top-level branch** | Any organisational node |

**`INDEPENDENT BUSINESS / VENTURE` and `ORGANISATION` are siblings under `GLOBAL`.** Nothing flows between them, in either direction, by any mechanism short of governed transfer — and the sibling rule of §2 is what makes that structural rather than a matter of care.

**Scope identity is a path, and the path is the whole ancestry.** `ORGANISATION/acme/PROGRAMME/north/PROJECT/alpha` and `ORGANISATION/acme/PROJECT/alpha` are two different scopes even where the project name matches, because their ancestor sets differ. Same-name disambiguation is by path, always, and never by string similarity.

## 2. Applicability, not inheritance

**Canonical status never inherits.** A statement canonical in one scope is canonical in that scope and nowhere else, ever. What may reach a descendant scope is **applicability** — whether the statement governs work done there — and applicability propagates **only according to the statement's own declared applicability mode**.

The first Phase 8 draft said every wider canonical statement was applicable to every descendant and that any nearer statement overrode it. The audit was right that this is two defects: it propagates by default rather than by declaration, and it lets a local statement override a binding obligation it has no power to touch.

### The four applicability modes

Every Canonical Record declares exactly one. They are non-overlapping.

| Mode | Propagates to descendants? | May a descendant scope hold a contrary statement? |
|---|---|---|
| `INHERITABLE_TO_DESCENDANTS` | **Yes**, to every descendant, unless a nearer statement declares an override | **Yes** — with a declared, reasoned override |
| `CONDITIONALLY_APPLICABLE` | **Only where the declared conditions are satisfied** in the descendant scope. Where they are not, it simply does not apply — which is not an override and needs no one's permission | Yes, and outside the conditions the question does not arise |
| `NON_INHERITABLE` | **No.** It governs its own scope only. A descendant needing a position on the subject must establish its own | Not applicable — there is nothing to override |
| `MANDATORY_WIDER_CONSTRAINT` | **Yes, and it binds.** Law, regulation, a contractual obligation, a safety rule, a binding governance standard, a funder condition | **No.** A descendant may **narrow it or add local detail**; it may not contradict, relax or override it |

**A mode is declared, never inferred.** A record whose mode is absent is defective, and the safe reading of a defective record is `NON_INHERITABLE` — it governs nothing beyond its own scope until the mode is stated.

### Override rules

Where a descendant scope holds a statement contrary to an applicable wider one, the descendant record must state:

1. **what it overrides** — the wider record, by identity and version;
2. **the wider statement's applicability mode** — and an override of `MANDATORY_WIDER_CONSTRAINT` is **not available at all**;
3. **why the override is permissible** — in governance or legal terms, not merely as a local preference;
4. **the authority path relied on**, where the upstream architecture provides one.

An undeclared contrary statement is a `SCOPE_CONFLICT`, not an override. **An override that names nothing has overridden nothing.**

### Mandatory wider constraints

A `MANDATORY_WIDER_CONSTRAINT` is not overridden by proximity, by seniority, by local circumstance, or by a local canonical statement. **A local exception requires a separately valid authority path** — one that upstream architecture actually provides — and where none exists, there is no exception, only a scope conflict and an unresolved obligation. A project cannot canonicalise its way out of a regulation, and this architecture does not offer it a mechanism that looks like one.

### Ancestor fallback after local retraction — no silent fallback

When a narrower canonical statement is retracted with no successor, what happens to an otherwise-applicable wider statement is **determined and recorded**, never assumed:

| Wider statement's mode | On local retraction |
|---|---|
| `MANDATORY_WIDER_CONSTRAINT` | **Resumes automatically** — it never stopped binding; the local statement was only narrowing it, and removing the narrowing leaves the obligation |
| `INHERITABLE_TO_DESCENDANTS` | **Requires explicit revalidation** before the scope may rely on it. It was displaced by a statement now withdrawn on a finding, and that finding may bear on the wider statement too |
| `CONDITIONALLY_APPLICABLE` | Applies **only if its conditions are re-checked and hold** in the scope as it now stands |
| `NON_INHERITABLE`, or no wider statement | **The scope has no position.** The retraction record names the gap |

The retraction record states which of these applies and what was determined. **No wider statement resumes silently.** **A wider statement quietly resuming, unexamined, is exactly the silent fallback this rule forbids** — the local statement was retracted for a reason, and a reason strong enough to withdraw a position is strong enough to be checked against the position beneath it.

### Authority still never flows

| | Direction | Rule |
|---|---|---|
| **Applicability** | Downward only, by declared mode | Per the table above |
| **Authority** | **Never flows** | Being inside a scope confers no authority over it. Authority is Phase 7's, held by eligibility class, never derived from scope membership |

**Nothing flows upward, ever.** A project's canonical statement is not the organisation's position, and a workstream cannot canonicalise for its project. The most common real failure this prevents: a parameter agreed inside one project quietly becoming "what the organisation assumes" because nobody said otherwise.

**Nothing flows sideways.** Sibling projects, sibling programmes, an organisation and an independent venture, and two organisations share nothing by default.

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
