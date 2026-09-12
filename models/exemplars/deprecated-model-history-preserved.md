# Exemplar 8 — Deprecated model retained in history, excluded from new routing

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that deprecation excludes a profile from **new** routing and removes **nothing** from the record.

## The historical decision
Routing Decision `rd.2025.appraisal.0731`, made eleven months ago: `model.legacy_analyst_g` v2 @ `deployment.tenant_internal_g`, under `routing_policy.analysis_standard` v3. It produced an economic appraisal still cited in a live business case.

The decision's **six-part reproducibility identity set** — elements 20–25 of `models/_templates/routing-decision-template.md` — as it was recorded then and as it stands today, unaltered:

| Part | Value recorded in 2025 |
|---|---|
| **Model Profile stable ID** | `model.legacy_analyst_g` |
| **Registry Profile Version** | v2 |
| **Underlying Model Release identity** | `release.legacy_analyst_g.2024-11` — the originator release that profile described **at v2** |
| **Provider Offering Mapping** | `offering.legacy_analyst_g.standard` v1 |
| **Provider Profile version** | `provider.g` v5 |
| **Deployment Profile version** | `deployment.tenant_internal_g` v3 |

`model.legacy_analyst_g` is now **`DEPRECATED`** — superseded by a successor and no longer evaluated. **Deprecation changes no cell of that table**, and it is the third row that makes the record answer the question people actually ask afterwards: not which of our records was used, but which thing ran.

## Candidate universe

Bound before any filtering or ranking, per `models/routing-precedence-and-fallback.md` §1 — for **today's** decision. The 2025 universe is part of the 2025 record and is not re-derived here.

| Element | Value |
|---|---|
| **Registry state reference** | `reg.snapshot.2026-09-11T07:00Z#4480` |
| **Universe definition version** | `cud.analysis_standard` v5 |
| **Inclusion rule** | Every registered Model Profile in **any** primary lifecycle state, paired with the internally-approved deployment classes. Lifecycle is **not** an enumeration filter: a `DEPRECATED` profile is enumerated and excluded at stage 5, so the record shows that the prior selection was considered and why it is no longer routable. **Availability pre-enumeration: no** |
| **Routing scope** | All registered profiles × internally-approved deployment classes × the internal provider allowlist |
| **Pre-filter exclusions** | `NONE` |
| **Enumerated candidate set** | **2**: `model.legacy_analyst_g` v2; `model.midsize_analyst_d` |
| **Omission reasons** | `NONE` — every registered candidate inside the scope is enumerated, the deprecated prior selection included |
| **Completeness result** | **`CANDIDATE_UNIVERSE_COMPLETE`** |
| **Behaviour if incomplete** | Policy `routing_policy.analysis_standard` v7 declares **`BLOCK`** on `CANDIDATE_UNIVERSE_INCOMPLETE` |

## The new decision
Re-running the appraisal on updated inputs, today:

| Candidate | Eligible? | Why |
|---|---|---|
| `model.legacy_analyst_g` v2 | **No** | Lifecycle `DEPRECATED` — excluded at stage 5 from all new routing |
| `model.midsize_analyst_d` | **Yes** | `STRONG` on the required capabilities, current evidence |

New decision: `model.midsize_analyst_d`, **linked to** `rd.2025.appraisal.0731` as the prior selection for the same subject.

## What survives, and why it must
| | Status |
|---|---|
| `rd.2025.appraisal.0731` | **Intact**, naming `model.legacy_analyst_g` **v2** and `routing_policy.analysis_standard` **v3** |
| The Model Profile record | **Retained** at its final version, with the deprecation and its reason |
| The 2025 appraisal | **Unaffected.** It was produced under a profile that was then eligible |
| The new appraisal | A new decision under current policy, which selects something else |

Deleting the old decision — or "tidying" it to the successor profile — would destroy the only account of what actually produced the 2025 appraisal. **That question is asked precisely when something turns out to be wrong, which is usually after the model has been retired.** A record that updates itself to name whatever is current answers the question only while nobody needs to ask it.

This is also why versions are named rather than profiles alone: `model.legacy_analyst_g` without `v2` would point at a lineage, not at the thing that ran.
