# Exemplar 1 — Verified organisational fact promoted to canonical

Status: PROPOSED — Phase 8 exemplar knowledge record
Inherits: `standard.knowledge.common_constraints@0.1`

**Proves:** that promotion is possible, and what it costs. Every other exemplar is a case where one of these prerequisites fails.

## Identity
- Knowledge ID: `knowledge.entity_registered_legal_form.acme`
- Version: 2
- Subject: the registered legal form and registration number of the operating entity
- Scope: `ORGANISATION/<entity>` — the widest scope any exemplar here reaches
- Memory class: `SEMANTIC_MEMORY` — **unchanged by promotion, supersession or retraction**
- Governance state: `CANONICAL`
- Origin: `EXTERNAL_ORIGIN` — the register is outside the entity
- Applicability mode: `INHERITABLE_TO_DESCENDANTS`
- Sensitivity: `PUBLIC`

## Statement
The entity is registered in its jurisdiction under the stated legal form, with the stated registration number, effective from the stated date.

## Epistemic type / governance state
`FACT_CLAIM` + `CANONICAL`. The type does not change on promotion; it was a claim before and is a claim now, adopted.

## Why this one is promotable
The register is the authoritative source for its own contents, the claim is determinate, and the evidence is direct rather than derived. Corroboration adds little because the source *is* the fact — which is rarer than it looks, and is why this is exemplar 1 rather than a typical case.

## Provenance
`SOURCE` official register extract, dated and versioned → `EVIDENCE` located at the specific entries → `FACT_CLAIM` → `REVIEW` legal-compliance profile `SATISFIED` → promotion.

No step omitted. No transformation applied: the statement uses the register's own wording, because paraphrasing a legal form is a transformation and this record does not need one.

## Scope note
Canonical at `ORGANISATION`, with applicability mode `INHERITABLE_TO_DESCENDANTS`, and therefore **applicable** in every descendant scope — every programme, project, product, operational workstream and task beneath it — **because the mode says so**, not by default. Had the mode been `NON_INHERITABLE`, the identical record would govern at `ORGANISATION` alone. It is **not** applicable in an `INDEPENDENT BUSINESS / VENTURE`, which is a sibling of `ORGANISATION` under `GLOBAL` rather than a descendant of it — a venture with its own registration has its own answer, and nothing propagates sideways to tell it otherwise. It is not canonical *in* those scopes — they hold no record — and a project restating it in its own words creates a second claim to keep in step, which is why the discipline is to reference rather than restate.

## What promotion did not do
It did not make the entity's legal form true; the register did that. It did not authorise disclosure of anything else about the entity. It did not make the register extract canonical — a source is cited, never promoted.

## Freshness
Expectation: annual review-by, with a refresh trigger on any filed change. **Version 1 is `SUPERSEDED`, not deleted** — it recorded the position before the last change, and the work done under it was done correctly.
