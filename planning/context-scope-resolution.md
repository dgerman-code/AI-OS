# Context and Scope Resolution

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. What this resolves, and why it is first

Every governed act happens in exactly one scope. Scope decides which knowledge is applicable, which
authority path exists, which sensitivity and residency constraints bind, and what a Role is even
allowed to see. Resolve it wrong and every later step is wrong in a way that looks right.

The Orchestrator's intake check 3 requires **exactly one** governed scope and an originator
entitled to act in it. Phase 15's job is to produce that scope or to fail visibly.

## 2. The scope graph, as approved

Reproduced from `architecture/context-hierarchy.md`, approved at Phase 2 and unchanged through the
Phase 13 baseline. It is not summarised, compressed or reinterpreted here:

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

**Rule CS-1 — a project has two possible parents, and which one it has matters.** A `PROJECT` may
sit under a `PROGRAMME / PORTFOLIO` **or** directly under the `ORGANISATION`. Those are different
ancestor sets, so they are different applicable-knowledge sets. A resolver that assumed one path
would silently change which statements govern the work. Phase 8 records that a compressed graph
loses exactly this, and Phase 15 does not repeat it.

**Rule CS-2 — `PERSONAL / AD-HOC INITIATIVE` and `INDEPENDENT BUSINESS / VENTURE` are separate
families, not branches of the organisation.** Organisational canonical material is not applicable
inside them by descent, and personal material is not applicable to organisational work. Resolving a
request into the wrong family is a contamination event, not a mis-filing.

## 3. Resolution inputs

| Input | Weight |
|---|---|
| A scope the user named explicitly | Decisive, subject to entitlement |
| A scope implied by a referenced artifact whose own scope is recorded | Strong |
| A counterparty, project or instrument that resolves to exactly one scope | Strong |
| The session's active context, where the product maintains one | Moderate, and never decisive alone |
| The user's default or home scope | Weak; a tiebreak only where nothing else is material |
| Similarity to past requests | **Not an input.** See CS-5 |

**Rule CS-3 — an inferred scope carries its basis.** `ScopeResolution` records which inputs
produced the candidate, in order, so a reviewer can see why this scope and not the neighbouring
one. A resolution with no recorded basis is invalid.

## 4. The separator boundary

**Rule CS-4 — never cross a boundary by guess.** Two scopes that look adjacent in a path are not
adjacent in governance. The resolver may narrow *within* a resolved branch on evidence. It may not
move sideways between projects, programmes, ventures, products, or families on a similarity
judgement, on a shared word in a name, or on a shared counterparty.

**Rule CS-5 — string proximity is not ancestry.** `project.riverside` and `project.riverside_two`
share a prefix and share nothing else. A scope path is a structured identity with declared parents,
and prefix matching over it is prohibited — the same rule Phase 8 applies to canonical applicability
and Phase 10 applies to row-level access predicates.

**Rule CS-6 — one request, one scope.** Where a request genuinely spans scopes, that is not one
plan with two scopes; it is either a plan in one scope that **references** material from another
through a governed reference, or two plans. Cross-scope reference is reference, never copy
(`knowledge/scope-isolation-and-transfer.md` §4), and the planner may not fold two scopes into one
run to make a request convenient.

## 5. When clarification is mandatory

**Rule CS-7 — material scope ambiguity is always clarified, whatever the confidence.** Where two or
more scopes are plausible **and** choosing between them changes any of:

| Changes | Why it is material |
|---|---|
| Which knowledge is applicable | The work would rest on statements that do not govern it |
| Which authority path exists | A Decision Right available in one scope may not exist in the other |
| Residency constraints | Data may not lawfully be processed where the other scope permits |
| Sensitivity handling | Material may be disclosed to an audience the other scope's labels forbid |
| Which Roles are entitled to act | An assignment may be invalid |

then the resolution is **`AMBIGUOUS_SCOPE`** and the planner clarifies. A high semantic confidence
does not substitute: confidence is a statement about the model, and this is a question about
governance (`work-plan-object-model.md` §7).

**Rule CS-8 — where clarification is unavailable, the planner blocks.** It does not pick the more
likely scope and proceed. `NO_VALID_SCOPE` and `AMBIGUOUS_SCOPE` are both blocking outcomes in
`failure-and-escalation-model.md`; neither degrades into a best guess.

## 6. Entitlement

**Rule CS-9 — resolving a scope is not being allowed into it.** The resolver produces a candidate;
whether the originator may act there is an access question answered by the approved Phase 10
boundary and re-checked by orchestrator intake. A planner that treated its own resolution as
entitlement would have granted access by inference.

**Rule CS-10 — unassessed is restricted.** Where sensitivity, handling or residency for the
resolved scope is not established, the `ScopeResolution` records it as unassessed and the plan is
constrained accordingly. Absence of a label is never absence of an obligation
(`storage/access-control-and-rls-boundary.md` §2).

## 7. The `ScopeResolution` record

| Field | Content |
|---|---|
| `scope_ref` | Exactly one resolved scope, or `UNRESOLVED` |
| `scope_family` | `ORGANISATION` · `INDEPENDENT_BUSINESS` · `PERSONAL` |
| `node_kind` | The graph node kind, from §2 |
| `ancestor_path` | The full declared ancestry, because a project's parent is not assumable (CS-1) |
| `candidates_considered` | Every candidate, with the inputs that suggested it |
| `basis` | The ordered inputs that produced the resolution (CS-3) |
| `confidence` | Scope confidence, advisory only |
| `sensitivity` | Labels, or `UNASSESSED` |
| `residency` | Constraints, or `UNASSESSED` |
| `entitlement_status` | `TO_BE_CHECKED_AT_INTAKE` — never `GRANTED` |
| `outcome` | `RESOLVED` · `AMBIGUOUS_SCOPE` · `NO_VALID_SCOPE` |

**Rule CS-11 — `entitlement_status` has one permitted value at planning time.** The planner cannot
write `GRANTED`, because it is not the component that grants.

## 8. Worked resolutions

| Request fragment | Resolution | Why |
|---|---|---|
| "…about this municipal infrastructure project" with one project in session context | `RESOLVED` to that project, ancestry recorded | One candidate, explicit context |
| "…the partner email" where the counterparty appears in two projects | **`AMBIGUOUS_SCOPE`** | Choosing changes applicable contract terms and authority |
| "Create a LinkedIn post about this news" from a personal context | `RESOLVED` to the personal family — **and** flagged, because publication under the entity's name would be organisational | The act's audience may not match the request's origin |
| "Send them confirmation…" with no resolvable counterparty | **`NO_VALID_SCOPE`** | An unresolved counterparty on a committing act cannot be scoped |

The third row is the one worth reading twice: the **origin** of a request and the **scope of the act
it proposes** are different questions, and a resolver that answers only the first will route an
organisational publication through a personal scope.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no resolver implementation, index, search
mechanism, schema or storage, and binds no provider or runtime technology.
