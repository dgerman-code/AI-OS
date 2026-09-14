# Scope and Context Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 finding **M-5**.

## 1. The approved scope graph

Reproduced from `architecture/context-hierarchy.md` (Phase 2, approved) and
`knowledge/scope-isolation-and-transfer.md` §1, **exactly as approved**, not summarised:

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

Four properties are load-bearing and an implementation that loses any of them is defective:

1. `INDEPENDENT BUSINESS / VENTURE` is a **sibling** of `ORGANISATION` under `GLOBAL`, not a
   child of it.
2. `PERSONAL / AD-HOC INITIATIVE` is a **third top-level branch**, a separate scope family.
3. `PROJECT` may sit **either** under `PROGRAMME / PORTFOLIO` **or** directly under
   `ORGANISATION` (and under an independent business).
4. `OPERATIONAL WORKSTREAM` ends at `TASK` with **no project above it**, and is not a
   `WORKSTREAM`.

## 2. Node kinds

| Kind | Permitted parents | Is not |
|---|---|---|
| `GLOBAL` | — (root, exactly one) | An organisation |
| `ORGANISATION` | `GLOBAL` | `GLOBAL`, or any other organisation |
| `INDEPENDENT_BUSINESS` | `GLOBAL` | A programme or product of an organisation |
| `PERSONAL_INITIATIVE` | `GLOBAL` | Any organisational node |
| `PERMANENT_FUNCTION` | `ORGANISATION` | `OPERATIONAL_WORKSTREAM` — a function is not work |
| `PROGRAMME_PORTFOLIO` | `ORGANISATION` | A project; and is not always present above one |
| `PRODUCT_PLATFORM` | `ORGANISATION`, `INDEPENDENT_BUSINESS` | A project, which ends |
| `PROJECT` | `ORGANISATION`, `PROGRAMME_PORTFOLIO`, `INDEPENDENT_BUSINESS` | A workstream |
| `OPERATIONAL_WORKSTREAM` | `ORGANISATION` | A project workstream |
| `WORKSTREAM` | `PROJECT`, `PRODUCT_PLATFORM`, `INDEPENDENT_BUSINESS`, `PERSONAL_INITIATIVE` | `OPERATIONAL_WORKSTREAM` |
| `TASK` | `WORKSTREAM`, `OPERATIONAL_WORKSTREAM`, `PROJECT`, `PRODUCT_PLATFORM`, `INDEPENDENT_BUSINESS`, `PERSONAL_INITIATIVE` | Everything above it |

**Rule S-1.** The parent kind of every node is validated against this table at insert. A node
whose parent kind is not listed is rejected. This table is the whole graph; there is no
"other" kind and no free-form nesting.

## 3. Scope identity — node identity and path identity are two things

> **Scope identity is a path, and the path is the whole ancestry.**
> `ORGANISATION/acme/PROGRAMME/north/PROJECT/alpha` and `ORGANISATION/acme/PROJECT/alpha` are
> **two different scopes** even where the project name matches, because their ancestor sets
> differ. Same-name disambiguation is by path, always, and **never by string similarity**.

| Concept | Type | Stable across a re-parent? | Used for |
|---|---|---|---|
| **Scope node identity** | `ScopeNodeRef` = `scope_node.<uuid>` | Yes | Referencing the node itself |
| **Canonical scope path** | `ScopePath`, a normalised string | **No** | Applicability, isolation, ancestry, every governance question |

### 3.1 Canonical path representation

```
<KIND>/<slug>[/<KIND>/<slug>]*
```

Normalisation rules, applied at write and enforced by a check constraint:

| # | Rule |
|---:|---|
| P-1 | Segments alternate `KIND` then `slug`; the path always begins at a top-level kind (`ORGANISATION`, `INDEPENDENT_BUSINESS`, `PERSONAL_INITIATIVE`) or is exactly `GLOBAL` |
| P-2 | `KIND` is upper snake case from §2; `slug` is lower snake case, 1–128 chars, `[a-z0-9_-]` |
| P-3 | Separator is `/`; no leading, trailing or repeated separator; no `.` or `..` segment |
| P-4 | The path is **stored, not derived at read time**, and is recomputed only by the governed re-parent act (§3.3) |
| P-5 | `(parent_path, kind, slug)` is unique; a sibling collision is a `BLOCK`, never a silent suffix |
| P-6 | Comparison is **exact segment-wise equality**. No case folding, no Unicode folding, no fuzzy matching, no `LIKE` matching anywhere on a governance path |

### 3.2 Ancestry queries

The persisted `scope_path` plus a persisted `depth` supports the four queries the architecture
needs, each with an exact definition:

| Query | Definition | Governance use |
|---|---|---|
| `ancestors_of(p)` | The ordered list of proper prefixes of `p` at kind boundaries, nearest first | Applicability resolution; ancestor fallback |
| `is_descendant_of(a, d)` | `d` starts with `a` **and** the next character in `d` is the separator | Propagation of `INHERITABLE_TO_DESCENDANTS` |
| `nearest_statement(p, subject)` | The applicable record on `subject` at the deepest ancestor of `p` (or `p` itself) | Override resolution |
| `common_ancestor(p, q)` | The longest shared prefix at a kind boundary; `GLOBAL` if none | Detecting a sibling crossing |

**Rule S-2 — the prefix trap.** `is_descendant_of` must test the separator boundary. A naive
prefix test makes `ORGANISATION/acme_holdings` a descendant of `ORGANISATION/acme`, which is
a cross-organisation leak produced by string handling. This is specified as a mandatory test
case in `test-and-assurance-strategy.md`.

**Rule S-3 — no sibling inheritance.** Nothing flows between two top-level branches, or between
two organisations, or between an organisation and a personal scope, **in either direction**, by
any mechanism short of a governed transfer (§7). Sibling inheritance is not merely discouraged;
there is no query in this specification that returns it.

### 3.3 Re-parenting

Re-parenting a node changes the scope path of the node and every descendant, which changes what
is applicable to them. It is therefore a **governed act**, not an administrative edit:

1. it requires a mapped Decision Right — and **no approved Right currently covers it**, so
   re-parenting is `UNIMPLEMENTABLE UNTIL RIGHT IS MAPPED` (see
   `open-items-and-blocked-authorities.md` BA-2);
2. the prior path is retained as a `scope_path_history` row, append-only, so historical records
   remain interpretable;
3. every Canonical Record whose applicability changes is flagged for revalidation; none silently
   changes applicability.

## 4. Persisted record — `scope_node`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `scope_node_ref` | `ScopeNodeRef` | NO | IMM | PK. `scope_node.<uuid>` |
| `kind` | enum §2 | NO | IMM | |
| `slug` | text | NO | IMM | P-2 |
| `parent_ref` | `ScopeNodeRef` | YES | IMM | `NULL` only for `GLOBAL`; FK; parent kind validated by S-1 |
| `scope_path` | text | NO | APP | Unique. Recomputed only by §3.3; prior values in `scope_path_history` |
| `depth` | int | NO | APP | Derived with `scope_path`; consistency enforced by constraint |
| `display_name` | text | NO | MUT | Carries no governance meaning |
| `sensitivity_labels` | set of §5 classes | NO | APP | Declared, never inferred; changes are append-only with reason |
| `residency` | residency constraint | NO | APP | Declared; `UNASSESSED` is restricted, never permissive |
| `lifecycle_state` | `ACTIVE` \| `DORMANT` \| `CLOSED` \| `TOMBSTONED` | NO | MUT | `CLOSED`/`TOMBSTONED` still resolve for historical reads |
| `created_*`, `closed_*` | audit stamps | NO/YES | IMM | |

Constraints: `UNIQUE(scope_path)`; `UNIQUE(parent_ref, kind, slug)`; check on §2 parent kind;
check that `depth = segment_count(scope_path) / 2` (with `GLOBAL` at depth 0).

## 5. Sensitivity and residency

Sensitivity classes, from `knowledge/sensitivity-and-retention-model.md`, used unchanged and
**never reordered into a ranking**:

`PUBLIC` · `INTERNAL` · `CONFIDENTIAL` · `RESTRICTED` · `PERSONAL_DATA` · `PRIVILEGED` ·
`TRADE_SECRET` · `SECURITY_SENSITIVE` · `THIRD_PARTY_RESTRICTED`

**Rule S-4 — unordered multi-label set.** Sensitivity is a *set of labels*, not a level. There
is no ceiling to compare. Narrowing is **subset containment**; widening is anything else. An
implementation that sorts these into a severity integer has invented an ordering the
architecture does not have, and will eventually compare `PRIVILEGED` against `PERSONAL_DATA`
as though one dominated the other.

**Rule S-5 — three labels carry obligations no comparison can discharge.** `PERSONAL_DATA`
carries obligations independent of every other class; `PRIVILEGED` **can be lost by handling**,
which no other class can; `THIRD_PARTY_RESTRICTED` is held under someone else's terms, so the
entity's own classification does not govern it. Each is carried explicitly through every
narrowing, transfer, routing request and artifact.

**Rule S-6 — residency.** Residency is an explicit constraint value, not a preference and not a
default. A binding with residency `UNASSESSED` is treated as **restricted**: no routing
candidate, no deployment and no storage location satisfies it until it is assessed.

## 6. Scope binding, narrowing and sub-runs

**Rule S-7 — one governed scope per execution.** A Workflow Run binds exactly one
`ScopeBinding` at intake. The binding is **immutable**. A change of scope is a new run.

A `ScopeBinding` is the triple *(scope path, sensitivity label set, residency)*.

**Rule S-8 — narrowing.** `A.narrows_to(B)` is true **only** when all hold:

1. `B.scope_path == A.scope_path` **or** `is_descendant_of(A.scope_path, B.scope_path)`;
2. `B.sensitivity ⊆ A.sensitivity`;
3. `B.residency == A.residency`.

Anything else is widening and is refused. In particular a change of residency is never a
narrowing, and adding a label is never a narrowing.

**Rule S-9 — sub-runs.** A sub-run may narrow what it sees and may not widen it, and **may not
be used to reach a scope the parent could not reach** — that would be a scope crossing wearing a
different name. A sub-run that names a non-descendant path is refused even when its sensitivity
set is smaller.

## 7. Cross-scope transfer

**Rule S-10.** A cross-scope movement uses an approved mechanism or **does not happen**. The
mechanisms are Phase 8's scope transfer and Phase 6's handoff. There is no orchestrator-level
shortcut, and coordination convenience is never a transfer.

Two distinct things are governed separately and must not be conflated:

| | **Execution scope crossing** | **Knowledge scope transfer** |
|---|---|---|
| Moves | Work, into a **new** execution bound to the target scope | A knowledge item's applicability into a receiving scope |
| Source binding | Never rewritten | Never rewritten |
| Carries | Nothing from the source run's stores | The item, as a candidate |
| Record | `scope_transfer_authorisation` + a new run | `knowledge_transfer` record |
| Owner | C9 with C6 authorisation | C4 with C6 authorisation |

### 7.1 `scope_transfer_authorisation` — required bindings

A crossing is authorised only by a record binding **all** of:

| # | Binding |
|---:|---|
| 1 | Approved mechanism reference **and its version** |
| 2 | Complete source `ScopeBinding` |
| 3 | Complete target `ScopeBinding` |
| 4 | The Work Item the crossing is for |
| 5 | The Gate Requirement the authorisation answers |
| 6 | The **exact** `decision.<id>` relied on |
| 7 | The **authorised act** the mechanism is registered for |
| 8 | The authorising `HumanAuthorityRef` |
| 9 | The `DecisionRecordRef` — which **must be found in the source run's own retained decision history**, not merely named |

A well-shaped object a caller constructed is evidence of nothing. Element 9 is what makes the
difference, and it is validated by lookup, not by comparison of fields.

### 7.2 `knowledge_transfer` — required content

From `knowledge/scope-isolation-and-transfer.md` §5, carried in full:

| # | Recorded |
|---:|---|
| 1 | Source scope path, item identity and **exact version** |
| 2 | Receiving scope path |
| 3 | The reason the item is expected to hold in the receiving scope |
| 4 | **What was revalidated, and what was not** — the latter carried forward as open items |
| 5 | The receiving scope's own review outcome |
| 6 | The receiving scope's own promotion decision, where canonical status is sought |
| 7 | What changes in the receiving context could invalidate it |

Rules, unchanged: a transfer **never carries canonical status** — an item canonical in the
source arrives as a candidate with strong provenance and no status; a transfer **never carries
review satisfaction**; transfer is **not transitive** — A→B→C requires two transfers, each
revalidated, and C may not cite A's review; **provenance survives intact** — the receiving
record's lineage begins at the original source, not at the transfer; and a transfer that cannot
say what was revalidated **has not revalidated anything** and is rejected at write.

## 8. Applicability modes and ancestor fallback

Every Canonical Record declares **exactly one** mode. Modes are non-overlapping, and
**a mode is declared, never inferred**.

| Mode | Propagates to descendants? | May a descendant hold a contrary statement? |
|---|---|---|
| `INHERITABLE_TO_DESCENDANTS` | Yes, unless a nearer statement declares an override | Yes — with a declared, reasoned override |
| `CONDITIONALLY_APPLICABLE` | Only where the declared conditions are satisfied in the descendant scope | Yes; outside the conditions the question does not arise |
| `NON_INHERITABLE` | No. Governs its own scope only | Not applicable |
| `MANDATORY_WIDER_CONSTRAINT` | Yes, **and it binds** | **No.** A descendant may narrow or add local detail; never contradict, relax or override |

**Rule S-11 — fail closed on a missing mode.** A record whose mode is absent is defective, and
the safe reading of a defective record is `NON_INHERITABLE`: it governs nothing beyond its own
scope until the mode is stated. The column is `NOT NULL`; the rule governs legacy and imported
rows.

### 8.1 Ancestor fallback after local retraction — no silent fallback

| Wider statement's mode | On local retraction with no successor |
|---|---|
| `MANDATORY_WIDER_CONSTRAINT` | **Resumes automatically** — it never stopped binding |
| `INHERITABLE_TO_DESCENDANTS` | **Requires explicit revalidation** before reliance |
| `CONDITIONALLY_APPLICABLE` | Applies **only if** its conditions are re-checked and hold now |
| `NON_INHERITABLE`, or none | **The scope has no position.** The retraction record names the gap |

**Rule S-12.** The retraction record states which row applied and what was determined. **No
wider statement resumes silently.** The implementation therefore computes fallback as a
*recorded determination*, never as a read-time query result: a read that would silently return a
wider statement after a local retraction returns "no position" until a determination exists.

## 9. Contamination directions that must not happen

| Contamination | Prevented by |
|---|---|
| Organisation → organisation | S-3 sibling rule; transfer only, and confidentiality classes may forbid even that |
| Organisation → personal | S-3; the two are different top-level families |
| Personal → organisation | S-3; a personal position is not an organisational one |
| Project → unrelated project | Path ancestry; a common ancestor is not applicability |

**Rule S-13.** An item carried across deliberately is carried as a **reference or a transfer**,
with the scope change recorded — never as an unmarked residue of a previous context.

## 10. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `ScopeRef` is a flat opaque id; `narrows_to` requires `scope == scope` | Path identity with ancestry; narrowing permits a descendant path | Phase 8 §1; Phase 13 M-5 |
| D2 | No applicability modes, no ancestor fallback | §8 in full | Phase 8 `scope-isolation-and-transfer.md` |
| D3 | Sensitivity is a bare `frozenset[str]` | The nine approved classes, with S-5 obligations carried | Phase 8 sensitivity model |
| D4 | No knowledge transfer record | §7.2 | Phase 8 §5 |
