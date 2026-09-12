# Exemplar 8 — Deprecated model retained in history, excluded from new routing

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All profile, provider and deployment identifiers below are architecture placeholders. **No claim is made about any real model or provider.**

**Proves:** that deprecation excludes a profile from **new** routing and removes **nothing** from the record.

## The historical decision
Routing Decision `rd.2025.appraisal.0731`, made eleven months ago: `model.legacy_analyst_g` v2 @ `deployment.tenant_internal_g`, under `routing_policy.analysis_standard` v3. It produced an economic appraisal still cited in a live business case.

`model.legacy_analyst_g` is now **`DEPRECATED`** — superseded by a successor and no longer evaluated.

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
