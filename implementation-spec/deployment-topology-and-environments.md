# Deployment Topology and Environments

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

> **This document creates no infrastructure, no manifest, no container definition, no pipeline,
> no secret and no cloud resource.** It specifies **logical** environments and the governance
> properties that must hold across them. No vendor, hosting platform, orchestration system,
> region or product is named as a requirement.

## 1. Logical environments

| Environment | Holds governed records? | Real external effects? | Approval state required? |
|---|---|---|---|
| `DEV` | **No** — synthetic only | No | No |
| `TEST` | **No** — synthetic only | No | No |
| `STAGING` | **No** — synthetic or de-identified only | **No** | Schema version yes; definitions yes |
| `PRODUCTION` | **Yes** | Yes, through the outbox | Yes, for every version plane |

**Rule E-1 — governed records exist in exactly one environment.** `PRODUCTION` holds the
organisation's governed records. No other environment holds a real Decision Record, Review
Instance, Canonical Record, Routing Decision or Artifact — not a copy, not a subset, not a
"refreshed from prod" snapshot.

**Rule E-2 — no downward data flow.** Production governed data is never copied into a lower
environment. Lower environments are seeded with synthetic data. This is not a data-hygiene
preference: a Decision Record in `STAGING` is a governed act in a place where it can be deleted,
and the moment that exists, "it was only staging" becomes an available explanation.

**Rule E-3 — no upward code flow without approval.** An application version reaches
`PRODUCTION` only where its schema-compatibility declaration and its schema version carry an
approval state (`migrations-versioning-compatibility.md` §6).

**Rule E-4 — lower environments perform no external effects.** The outbox drain in `DEV`,
`TEST` and `STAGING` writes to a recording stub, never to a real provider, recipient, publication
surface or counterparty. An environment that can publish is a production environment, whatever
it is called.

## 2. Separation properties that must hold

| # | Property |
|---:|---|
| 1 | Separate databases. Not separate schemas in one database, and never separate rows distinguished by an `env` column |
| 2 | Separate object storage namespaces |
| 3 | Separate credentials, with no credential valid in more than one environment |
| 4 | Separate identity-provider tenants or realms; a `HumanAuthorityRef` in `TEST` is not the same person-reference as in `PRODUCTION` |
| 5 | Separate observability stores |
| 6 | No network path from a lower environment to production data stores |
| 7 | Separate approval-state registries; a `TEST` approval state has no meaning in production |

**Rule E-5 — an `env` column is prohibited on governed tables.** A shared table distinguished by
an environment flag means one query mistake is a cross-environment leak, and it makes RLS carry a
load it was never meant to carry.

## 3. Deployment topology — logical

```
   Command/Query API (C15)
        │
        ├── Orchestrator (C9)       ── Router (C7) ── Model Invocation Gateway (C8) ──► provider adapters
        ├── Review (C5)                                        │
        ├── Decision Authority (C6)                            └── recording stub in DEV/TEST/STAGING
        ├── Knowledge (C4) ── Scope (C3)
        ├── Definition Registry (C1) ── Approval State (C2)   ◄── Git, read-only
        │
        ├── Governed Record Store (C10, PostgreSQL)
        ├── Artifact/Object Store (C11)
        ├── Audit & Provenance (C12)
        └── Outbox & Reconciliation (C16)

   Identity & Access (C14) mediates every inbound call.
   Observability (C13) receives from all; is read by none of them.
```

**Rule E-6 — co-location is permitted; crossing is not.** Components may share a process, a
container or a host. What may not happen is a forbidden responsibility crossing
(`system-component-model.md` §3) becoming reachable because two components share an address
space. Where components are co-located, the crossings are enforced by module boundaries and by
database grants, and the static checks in `test-and-assurance-strategy.md` §8 verify it.

**Rule E-7 — the outbox drain is the only component permitted an outbound effect**, and only
for rows whose authorisation reference is present.

## 4. Configuration

**Rule E-8 — configuration never carries governance.** No environment variable, config file,
feature flag or launch parameter may:

- grant, widen, substitute for or bypass a Decision Right;
- change an approved vocabulary;
- relax a uniqueness constraint, a gate requirement or an independence requirement;
- enable a `--force`, `skip_checks` or `as_admin` path, because none exists;
- declare something approved.

Configuration carries endpoints, pool sizes, timeouts, log levels and the environment name. That
is the whole of its remit.

**Rule E-9 — a timeout is configuration; what a timeout *means* is not.** An expiry produces
`EXPIRED` → `ESCALATED`, never an approval, whatever its value is set to.

## 5. Scaling and availability

**Rule E-10 — horizontal scaling must not weaken any governed property.** Every governed
invariant in this specification is enforced by a database constraint or a version-pinned write,
precisely so that running *n* instances of a component changes nothing about correctness. An
invariant that holds only because one process is running is a defect — which is exactly what
Phase 13 found about the Phase 12 in-memory uniqueness store.

**Rule E-11 — no leader election is required for correctness.** Where a singleton process is
convenient (the reconciliation sweep), it is convenient only; the sweep is idempotent and
concurrent execution is safe.

**Rule E-12 — availability is never a governance argument.** An outage does not create
authority, relax a constraint, permit a substitution or justify a retry of a non-retryable act.
`orchestration/_standards` constraint: outage, urgency, retry exhaustion, cancellation, a missed
deadline and an incomplete recovery **never** make a non-compliant model, deployment, storage
location, reviewer or scope acceptable.

## 6. Residency

**Rule E-13.** Residency constraints bind deployment topology: a storage location, a model
deployment and a backup destination each satisfy the residency of the data they touch, or they
are not used. `UNASSESSED` residency satisfies nothing.

**Rule E-14.** Residency is a property of the data's scope binding, not of the environment. A
production environment spanning regions must still refuse a placement that violates a binding.

## 7. What is deliberately not specified

Cloud provider · region names · container runtime · orchestration platform · service mesh ·
CI/CD product · secret manager product · IaC language · network topology · instance sizing ·
autoscaling policy · DNS · certificates.

All of these are production-engineering choices made after this specification is approved, under
their own review. Naming one here would make the architecture depend on it.
