# AI-OS Implementation Specification

Status: `PROPOSED` — Phase 14 implementation specification foundation
Version: 0.1

## 1. What this package is

This package turns the human-approved Phase 1–13 architecture into an implementation
specification detailed enough that a separate engineering team can build AI-OS **without
inventing governance semantics**.

It specifies components, identities, data contracts, schemas, constraints, transaction
boundaries, failure behaviour, security boundaries, observability, migration rules, test
strategy and build sequencing.

It builds nothing. There is no runtime, no migration, no deployed API, no provider SDK, no
secret, no credential, no database and no infrastructure in this package, and adding one is a
defect rather than progress.

## 2. Authority hierarchy

When two statements conflict, the higher row wins and the lower one is **defective**:

| # | Source | Status |
|---:|---|---|
| 1 | Human approval records in `reviews/phase-*-final-approval.md` | Authoritative governance decisions |
| 2 | Approved architecture — `architecture/`, `orchestration/`, `knowledge/`, `models/`, `storage/`, `decisions/`, `reviews/`, `roles/`, `skills/`, `workflows/`, `handoffs/` | Approved semantics |
| 3 | **This specification package** | Implementation detail **within** those boundaries |
| 4 | `implementation/phase-12/` reference implementation | Demonstration only |
| 5 | `validation/*.py` validators | Assurance tools |

Two consequences are load-bearing and are repeated throughout this package:

> **Phase 12 is a reference implementation, not a source of semantics.** Where the Phase 12
> reference implementation and the approved architecture differ, **the approved architecture
> wins** and this specification follows the architecture. Section 12 of each affected document
> records every such divergence explicitly rather than silently preferring the code.

> **A validator is an assurance tool and never governance authority.** A green validator is
> evidence that a check passed. It approves nothing, satisfies no gate, and creates no Right.

## 3. Approved baselines this package is written against

| Baseline | Commit | Record |
|---|---|---|
| Phase 3 — Role Registry | `f3cd318eb80d457a27e2f91218ce3cbb9a360e28` | `reviews/phase-3-final-approval.md` |
| Phase 4 — Skill Registry | `8ddacb2b2d2bc47e1a65099df575a0b16205d046` | `reviews/phase-4-final-approval.md` |
| Phase 5 — Workflow Registry | `adf45adf4ca33510a15281c5e776160d5720b859` | `reviews/phase-5-final-approval.md` |
| Phase 6 — Handoff & Review | `1c0f6cafbb43aa642aa0d10ccf4a9db22824c5fa` | `reviews/phase-6-final-approval.md` |
| Phase 7 — Decision Rights | `cedee2cfd1a959489585eb61acd975b4f7c65c84` | `reviews/phase-7-final-approval.md` |
| Phase 8 — Knowledge & Canonical | `516c91eb98ce89751b97d21c74553afaf7bed21b` | `reviews/phase-8-final-approval.md` |
| Phase 9 — Model Registry & Router | `a13fee667859bb8983d4f6a1f902f18fee0af083` | `reviews/phase-9-final-approval.md` |
| Phase 10 — Storage & Persistence | `b184b074c1de5416fcfc56036ee033f6e52fed46` | `reviews/phase-10-final-approval.md` |
| Phase 11 — Orchestrator | `b4cc549680c87e465931b5c4a6825e34f3c3ced6` | `reviews/phase-11-final-approval.md` |
| Phase 12 — MVP Foundation | `f5f8dd76ca8283eed969928b4ec1cd9f48f04dc7` | `reviews/phase-12-final-approval.md` |
| Phase 13 — System Architecture Review | `66927a9d535ed8de31157ca1b23c860a75448a8e` | `reviews/phase-13-final-approval.md` |

Approval caveats carried forward unchanged, and **not** rewritten by this package:

- Phase 11 is `APPROVED WITH VALIDATOR HARDENING DEFERRED`; its final audit remains
  `FAIL / NOT READY` and its harness credibility remains `MEDIUM`;
- Phase 12 harness credibility remains `MEDIUM-HIGH`, not `HIGH`;
- Phase 13 verdict remains `PASS WITH NON-BLOCKING NOTES`, blockers `NONE`,
  credibility `MEDIUM-HIGH`;
- the Phase 11 `159/160` and Phase 10 `145/147` inherited validator conditions are
  **not repaired from Phase 14**.

## 4. The governing invariants

Every document in this package is written to preserve these, and any statement in this package
that weakens one is a defect in this package:

```
ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE != ROUTER != ORCHESTRATOR != WORKFLOW
     != WORKFLOW RUN != TASK != HANDOFF != REVIEW PROFILE != REVIEW INSTANCE
     != DECISION RIGHT != DECISION RECORD != KNOWLEDGE != CANONICAL RECORD != ARTIFACT
     != STORAGE RECORD != RUNTIME EVENT != CREDENTIAL != HUMAN AUTHORITY
```

And, stated as enforcement rules rather than as prose:

1. `ROLE != AGENT INSTANCE` — competence attaches to a profile, never to a process.
2. `MODEL != ROLE` — a model is a replaceable execution runtime.
3. `ROUTER != ORCHESTRATOR` — eligibility and sequencing never merge.
4. `REVIEW PROFILE != REVIEW INSTANCE` — requesting a review never resembles satisfying one.
5. `DECISION RIGHT != DECISION RECORD` — holding authority is not exercising it.
6. `KNOWLEDGE != CANONICAL RECORD` — an assertion is not the organisation's position.
7. `ARTIFACT != STORAGE RECORD` — a file does not become true by being stored.
8. `RUNTIME EVENT != AUDIT EVENT` — **no operational log is governance evidence.**
9. `CREDENTIAL != HUMAN AUTHORITY` — possession of access is never permission to decide.
10. **Human authority is explicit and is never inferred** from model output, service identity,
    urgency, timeout, confidence, RLS, credentials, logs, routing, retries, seniority,
    administrative capability, or successful execution.

> **Fail closed.** Wherever the approved architecture fails closed, the implementation fails
> closed. Unassessed is restricted, never permissive. A missing Decision Right blocks; it is
> never read as permission. An absent applicability mode reads as `NON_INHERITABLE`. An
> unclassified retry class is non-retryable. An unassessed conflict is material.

## 5. Non-goals

This package does **not**:

- deploy, provision or configure anything;
- create production migrations, executable API code, infrastructure manifests or container
  definitions;
- introduce provider SDKs, live model calls, secrets, credentials, IAM bindings, queues,
  workers, schedulers, daemons or event buses;
- claim production readiness, and it never claims distributed exactly-once delivery or
  distributed transactions;
- create, widen, grant, infer or manufacture any Decision Right or human authority;
- promote any artifact to `APPROVED` or `CANONICAL`;
- modify any approved Phase 1–13 artifact;
- rewrite historical `Status:` fields to make a validator green.

All Phase 14 artifacts remain `PROPOSED` until independent audit and explicit human approval.

## 6. Document map

| # | Document | Owns |
|---:|---|---|
| 1 | `README.md` | Purpose, authority hierarchy, baselines, invariants, non-goals, map |
| 2 | `system-component-model.md` | Production components, responsibility ownership, forbidden crossings |
| 3 | `domain-identity-model.md` | Every governed identity, stable IDs, version identities, non-substitutability |
| 4 | `scope-and-context-model.md` | Path-based scope identity, ancestry, applicability, sensitivity, residency, transfer |
| 5 | `knowledge-and-canonical-model.md` | The four axes, versioning, conflict, freshness, canonical promotion hooks |
| 6 | `decision-review-authority-model.md` | Decision Rights/Records, holder resolution, SoD, review independence, missing-Right handling |
| 7 | `model-router-runtime-contract.md` | Routing request, eligibility, six-part reproducibility, Model Result lineage |
| 8 | `orchestrator-runtime-contract.md` | Runs, Work Items, states, gates, halted guard, atomic acts, retry, compensation, rework |
| 9 | `persistence-and-transaction-model.md` | Logical schema boundaries, transactions, uniqueness, OCC, append-only, object commit protocol |
| 10 | `audit-provenance-observability.md` | The six record families, correlation/causation, observability never authority |
| 11 | `api-command-contracts.md` | Command/query boundary, preconditions, idempotency, errors, no authority inference |
| 12 | `security-identity-access.md` | Human vs service identity, credentials, RLS boundary, secrets, isolation, admin limits |
| 13 | `approval-state-registry.md` | Machine-readable approval state, provenance, supersession, revocation |
| 14 | `migrations-versioning-compatibility.md` | Migration rules, destructive-migration blocking, compatibility |
| 15 | `failure-recovery-race-model.md` | Failures, retries, the ten races, unknown external effects, reconciliation, compensation |
| 16 | `deployment-topology-and-environments.md` | Logical environments and separation, no secrets or provider specifics |
| 17 | `test-and-assurance-strategy.md` | Nine test classes, invariant tests, approval-gate tests |
| 18 | `implementation-sequencing.md` | Build order, dependencies, milestones, stop/go gates |
| 19 | `open-items-and-blocked-authorities.md` | Deferred items, missing Decision Rights, unresolved production choices |
| 20 | `phase-14-self-check.md` | Completeness matrix against Phase 13 findings, invariant preservation, non-production status |

Assurance tool: `validation/phase_14_validation.py` — deterministic, standard library only.

## 7. How to read a specification table

Every persisted governed record in this package is specified with the same columns, so the
absence of a column is itself information:

| Column | Means |
|---|---|
| **Field** | Canonical field name |
| **Type** | Logical type, not a vendor type |
| **Null** | `NO` = required at insert; `YES` = genuinely optional, never "not yet filled in" |
| **Mut** | `IMM` = immutable after insert; `APP` = append-only linkage; `MUT` = mutable operational metadata that carries no governance meaning |
| **Notes** | Uniqueness, references, allowed writers, governance meaning |

`MUT` fields never carry governance meaning. If a field would change what a governed record
*means*, it is `IMM` and a change is a new version.
