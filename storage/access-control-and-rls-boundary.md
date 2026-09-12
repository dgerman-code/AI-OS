# Access Control and the RLS Boundary

Status: PROPOSED — Phase 10 architecture candidate
Version: 0.1
Inherits: `standard.storage.common_constraints@0.1`

No live policy is implemented here. This document defines what authorisation is allowed to mean.

## 1. Enforcement is not authority

> **Row-level security decides whether an operation may touch a row. It never decides whether the act that operation records was authorised.**

Four collapses this prevents, each stated as a denial because each is a plausible shortcut:

| Denial | What it stops |
|---|---|
| **Role Card competence `!=` database permission** | A Role is a description of competence and accountability. Granting an identity write access to the `decision` domain does not make it competent, and describing a Role as competent grants it nothing |
| **Decision Right holder eligibility `!=` database role** | Eligibility to exercise a Right is Phase 7's, decided per Right and per holder. A database role that can insert a Decision Record row is a mechanism, not an eligibility |
| **Human signatory authority `!=` service account capability** | A service account may write the row that records a human decision. It never *is* the decision. The signing human is recorded as the human |
| **A model, provider or deployment gains no authority by holding a credential** | Possession of a token is possession of a token. Phase 9 already denies that capability confers authority; Phase 10 denies that access does |

A permission grant is therefore never evidence of authority in any audit, review or dispute. It is evidence that someone could perform an operation — which is exactly what a permission is for.

## 2. Seven access dimensions

Authorisation is evaluated over all seven. A policy that ignores any of them is under-specified.

| # | Dimension | Question |
|---:|---|---|
| 1 | **Organisation / scope** | Which Phase 2 context does this identity act within? |
| 2 | **Object class** | Which domain and object type is being touched? |
| 3 | **Sensitivity** | Does the identity's approved label set cover **every** label on the object? |
| 4 | **Operation type** | Read, append, transition, or administrative? |
| 5 | **Lifecycle state** | Is the object in a state this operation is defined for? |
| 6 | **Identity class** | Human, service account, or projector — and never interchangeable |
| 7 | **Purpose / use context** | What is it being accessed *for*? Access granted for one purpose is not access for another |

Dimension 3 is a **subset test** over label sets, exactly as in Phase 9 §3. There is no level, no ceiling and no ordering.

## 3. Deny by default, including for unknown

Two defaults, and the second is the one usually missing:

1. **Sensitive domains deny by default.** `decision`, `knowledge`, `audit` and any object carrying restricted labels are inaccessible unless a policy grants access explicitly.
2. **Unknown classification denies by default.** An object whose sensitivity, scope or residency is **unassessed** is treated as restricted. Unassessed is not "probably fine", and an architecture that treats absence of a label as absence of obligation has inverted the control.

Administrative operations, purge, hold release and mirror rebuild are denied to every identity that does not hold them explicitly, including to identities that hold every other operation.

## 4. Operations that no policy may grant

| Operation | Why it is unreachable |
|---|---|
| Update or delete an audit event | The `audit` domain has no such operation to grant |
| Amend a Decision Record | Append-only. A correction is a new record |
| Write to `registry_mirror` outside a rebuild | The mirror is a projection; a write to it is a defect by definition |
| Change a stable logical ID | Identity is immutable |
| Return a retracted object to use | `RETRACTED` is terminal |
| Set a canonical status directly | Promotion is a Phase 8 governed path, not a column update |

These are absent capabilities, not withheld ones. A backend that offers them is configured outside this architecture.

## 5. Identity classes

| Class | May | May never |
|---|---|---|
| **Human** | Exercise Rights, approve, sign, hold, release, authorise purge and restore | — |
| **Service account** | Execute governed write paths on behalf of a recorded act; read within its grants | Be recorded as the decider, approver, signatory or reviewer |
| **Projector** | Rebuild `registry_mirror` from an approved baseline | Write any other domain |
| **Analyst / read** | Read within its scope, class, labels and purpose | Write anything |

Every governed record names the **human or governed act** it records **and**, separately, the **system identity** that wrote it. Two fields, never one — because the audit question afterwards is usually which of the two is being claimed.

## 6. Where portable authorisation ends and the backend begins

| Portable — part of this architecture | Backend-specific — behind the adapter boundary |
|---|---|
| The seven dimensions and their evaluation order | The policy language they are expressed in |
| Deny-by-default for sensitive and unknown | How a session's context is supplied to the policy engine |
| The absent operations of §4 | Which mechanism makes them absent |
| Identity classes and their separation | How identities are authenticated |

Row-level security is the **current enforcement mechanism** for the relational store. The architecture above it must remain expressible if the mechanism changes — which is the test §6 exists to make checkable.

## 7. What this document does not do

It defines no policy, creates no role, grants no permission, names no account, and configures nothing. No live policy exists, and none may be created from this document without the Phase 7 authorisation that governs it.
