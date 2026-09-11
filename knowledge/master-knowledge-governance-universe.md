# Master Knowledge Governance Universe

Status: PROPOSED — Phase 8 inventory
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## Purpose

The inventory of what Phase 8 governs, what it inherits, what it deliberately leaves alone, and what it hands on. **It is not a candidate universe of cards.** Phase 8 introduces no registry of knowledge objects to be carded, because knowledge records are instances produced by work — the registry analogue here is the *model*, not a card catalogue, and mass generation would produce fiction rather than architecture.

## 1. Governed vocabularies

| Vocabulary | Members | Owner document |
|---|---:|---|
| Epistemic types | 8 | `knowledge/knowledge-state-model.md` §2 |
| Origin values | 4 | `knowledge/knowledge-state-model.md` §2a |
| Governance states | 7 | `knowledge/knowledge-state-model.md` §3 |
| Conflict flag | 1 | `knowledge/knowledge-state-model.md` §4 |
| Conflict classes | 7 | `knowledge/conflict-and-provenance-model.md` §2 |
| Lineage types | 9 | `knowledge/conflict-and-provenance-model.md` §6 |
| Memory classes | **6** | `knowledge/memory-class-model.md` §2 |
| Sensitivity classes | 9 | `knowledge/sensitivity-and-retention-model.md` §1 |
| Item-level temporal fields | 7 | `knowledge/sensitivity-and-retention-model.md` §3 |
| Use-context freshness verdicts | 4 | `knowledge/sensitivity-and-retention-model.md` §3 |
| Applicability modes | 4 | `knowledge/scope-isolation-and-transfer.md` §2 |
| Canonical acts | 7, across 2 authorities (1 + 4 effect subtypes) | `knowledge/canonical-promotion-governance.md` §1 |
| Cross-scope mechanisms | 2 permitted, 1 prohibited | `knowledge/scope-isolation-and-transfer.md` §4 |
| Enforceable constraints | 29 | `knowledge/_standards/common-knowledge-governance-constraints.md` |

## 2. Artifacts

| File | Purpose |
|---|---|
| `architecture/memory-canonical-governance.md` | Master architecture; identity separation; artifact, retrieval and AI boundaries; criticality |
| `knowledge/knowledge-state-model.md` | The three axes and the transition rules |
| `knowledge/scope-isolation-and-transfer.md` | Scope, applicability, isolation, governed transfer |
| `knowledge/memory-class-model.md` | The six memory classes |
| `knowledge/conflict-and-provenance-model.md` | Conflict taxonomy and resolution; provenance and lineage |
| `knowledge/canonical-promotion-governance.md` | The canonical acts and the two bounded authorities |
| `knowledge/sensitivity-and-retention-model.md` | Sensitivity, freshness, end states, retention |
| `knowledge/_standards/common-knowledge-governance-constraints.md` | 28 inherited rules |
| `knowledge/_templates/knowledge-record-template.md` | Semantic Knowledge Record model |
| `knowledge/_templates/canonical-record-template.md` | Semantic Canonical Record model |
| `knowledge/exemplars/` × 8 | Worked cases, each proving one boundary |
| `knowledge/master-knowledge-governance-universe.md` | This inventory |
| `reviews/phase-8-foundation-self-check.md` | Self-check results and open questions |

## 3. Registry-type decision: memory classes are architecture classes

The **six** memory classes are **not** first-class registry types. They have no IDs, nothing is registered as one, and no Role, Skill, Workflow, Handoff, Review Profile or Decision Right references one. Reasoning is in `knowledge/memory-class-model.md` §1; the short form is that a registry type would invite a runtime to build seven stores, and the classes are governance postures, not stores.

**Reconsider this if and only if** a later phase needs to reference a memory class from a card — at which point it becomes a registry type by evidence rather than by anticipation.

## 4. What Phase 8 inherits and does not change

| Inherited | From | Phase 8's treatment |
|---|---|---|
| The context hierarchy | `architecture/context-hierarchy.md` (Phase 2) | **Reproduced verbatim** in `knowledge/scope-isolation-and-transfer.md` §1, with applicability, isolation and transfer semantics added around it. **Correction:** version 0.1 of this document claimed the hierarchy was unchanged while the Phase 8 scope document had in fact compressed it — dropping `INDEPENDENT BUSINESS / VENTURE`, `OPERATIONAL WORKSTREAM`, `PERMANENT FUNCTION / BUSINESS AREA` and the dual path by which a `PROJECT` may sit under a programme **or** directly under the organisation. **That claim was false.** The approved graph is now reproduced exactly and the approved file itself was never modified |
| The twelve knowledge labels | `architecture/context-hierarchy.md` | Every label keeps its spelling and meaning. Phase 8 says which **axis** each belongs to; it renames nothing |
| Criticality bands | `architecture/project-criticality-policy.md` (Phase 3) | Used, not rewritten. Bands change required rigour, never truth |
| Review semantics | Phase 6 | Referenced. **No review status is set, changed or interpreted by any Phase 8 artifact** |
| Decision Right semantics | Phase 7 | Referenced. **No card is created, no authority granted, no separation relationship declared** |

## 5. Upstream label mapping

| Upstream label | Phase 8 axis and name | Note |
|---|---|---|
| `FACT` | Epistemic type `FACT_CLAIM` | Renamed **only within Phase 8's own vocabulary**; upstream artifacts are untouched. The register holds claims; the world holds facts |
| `SOURCE`, `ASSUMPTION`, `CALCULATION`, `AI_SUGGESTION`, `UNKNOWN` | Epistemic types, same names | Unchanged |
| `DRAFT`, `REVIEWED`, `APPROVED`, `CANONICAL`, `SUPERSEDED` | Governance states, same names | Unchanged |
| `CONFLICT_DETECTED` | Conflict flag, same name | Reclassified from state to flag, so it can coexist with a state instead of replacing one |
| `AI_SUGGESTION` | Epistemic type, same name, **narrowed** | Still means what an upstream reader meant: an unadopted model proposal that may never become canonical automatically. Phase 8 adds that it **converts to no other type** — adoption creates a new linked item — and adds an **origin axis** alongside it so an adopted claim's AI origin stays recorded once the proposal is no longer the live item |
| — | `EVIDENCE`, `INFERENCE`, `REJECTED`, `RETRACTED` | **New in Phase 8.** Four gaps the flat list did not cover |
| — | Origin: `HUMAN_ORIGIN`, `AI_ASSISTED`, `AI_GENERATED`, `EXTERNAL_ORIGIN` | **New axis in Phase 8.** Permanent provenance; changes no upstream label |

## 6. Phase 7 canonical forward reference

| Upstream identifier | Phase 7 disposition | Phase 8 resolution |
|---|---|---|
| `decision.canonical_knowledge_promotion` | Candidate, deliberately uncarded | **Promotion** — and every canonical act with a successor: correction, renewal, scope widening, re-promotion. Supersession is its automatic effect |
| `decision.canonical_knowledge_status_change` | `DUPLICATE / OVERLAP`, consolidation deferred to Phase 8 | **Governed status downgrade** — four declared effect subtypes: `APPROVED_STATUS_WITHDRAWAL`, `CANONICAL_RETRACTION`, `SCOPE_OR_APPLICABILITY_NARROWING`, `EARLY_EXPIRY`. No successor exists in any act it covers |

**Correction to version 0.1:** the first Phase 8 draft bounded the second identifier to *canonical* withdrawal only, which silently dropped the approved upstream use. `roles/portfolio-programme-project/knowledge-evidence-steward.md` routes downgrade of material whose status derives from an explicit human **`APPROVED` or `CANONICAL`** decision to this ID. Both uses are now covered by the `APPROVED_STATUS_WITHDRAWAL` and `CANONICAL_RETRACTION` subtypes, and the Role Card was **not modified** — the Phase 8 proposal was.

The duplication is resolved by the **successor / no-successor** boundary, not by merging or renaming either. Both identifiers survive with upstream traceability intact. Carding is a **Phase 7 registry act**, specified exactly in `knowledge/canonical-promotion-governance.md` §7 and **not performed here** — until it runs, neither is exercisable and no canonical promotion can occur.

## 7. Deliberately not built

| Not built | Why |
|---|---|
| A candidate universe of knowledge objects | Knowledge records are instances of work, not registry entries. Generating them would be invention |
| Any Decision Right Card | Phase 7's registry, Phase 7's governance |
| Memory classes as registry types | §3 |
| A seventh `CANONICAL_MEMORY` class | Removed after the independent audit: it duplicated the `CANONICAL` governance state and Canonical Record identity, and was undefined after supersession or retraction. Canonicality is a governance state; the memory class does not change when it does |
| A retrieval, ranking, embedding or storage model | Out of scope by construction — and the whole of `architecture/memory-canonical-governance.md` §7 is about keeping it out |
| An access-control or IAM model | Sensitivity is metadata a runtime honours; the enforcement is not architecture's to design |
| A retention automation model | Semantics only. No job, schedule or sweep |
| An entity-resolution rule | Cross-scope identity is a governed conflict, never an inference the system makes |

## 8. Handed to later phases

1. **Phase 7 registry pass** — card both canonical authorities per `canonical-promotion-governance.md` §7, including the separation relationships.
2. **Workflow integration** — `workflow.canonical_knowledge_promotion_preparation` already exists as a Phase 5 candidate and prepares the promotion package. Nothing in Phase 8 cards or alters it.
3. **Role integration** — `role.knowledge_evidence_steward` (Phase 3, approved) already references both canonical identifiers and may not downgrade human-approved material. Phase 8 changes nothing about it and grants it nothing.
4. **Runtime** — storage, indexing, retrieval, access control, retention execution, identity. Validates against these semantics; does not mutate them.

## 9. Status

Every Phase 8 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL, and the eight exemplars are worked illustrations, not live knowledge records.
