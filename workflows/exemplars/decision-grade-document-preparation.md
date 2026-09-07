# Decision-Grade Document Preparation

Status: PROPOSED — Phase 5 exemplar Workflow Card
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: Decision-Grade Document Preparation
- Workflow ID: `workflow.decision_grade_document_preparation`
- Version: 0.1
- Status: PROPOSED
- Workflow Family: Knowledge / Documentation / Disclosure
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands. The criticality driver is the weight of the decision the document supports and whether it leaves the organisation.
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose

A decision-grade document is one a human will rely on to make a decision they cannot easily unmake. This Workflow is the **generic reusable pattern** for producing one: sources through evidence, evidence through drafting and specialist contribution, drafting through traceability and review requirement, to a human approval gate.

It is deliberately generic and deliberately **not** a universal mega-workflow. It carries no domain conclusions of its own.

**This card is a candidate reusable child pattern, available to a parent Workflow through `WORKFLOW_REFERENCE`** where that parent's preconditions and outputs match this card's in full. It is not automatically composed into anything: a parent that references it says so in its own `## Composed Workflow References` section, states the bounded purpose and the parent Stages involved, and keeps this card's gates and review requirements visible.

**No current exemplar references it, and that is an accurate finding rather than an omission.** `workflow.project_development_readiness` is the closest candidate — its S6–S7 map onto this card's S3–S5 — but that parent satisfies this card's S1 evidence base and S2 specialist contribution in its own earlier stages, so the fit is partial and overlapping rather than a clean whole-child composition. Whether this pattern should be decomposed so its document-production segment can be referenced independently needs a wider exemplar set than four.

### What it is not

It is not a substitute for the domain workflow that produces the conclusions. If this pattern is being used to produce a feasibility position, a legal analysis or a financial model, it is being misused: those are owned elsewhere and this pattern only assembles, traces and prepares.

## Composed Workflow References

**None.** This Workflow references no child pattern; it is itself the candidate child described above. Self-reference, direct or transitive, is prohibited as a registry defect under `standard.workflow.common_constraints` §14C.

## Trigger

`TRIGGER` — a document is required that a named human decision will rely on, where the reliance is material and the decision is identified.

## Preconditions

- `PRECONDITION` — the decision the document supports is named, with its `decision.<id>` where one exists.
- `PRECONDITION` — the document's owning Role is identified; a document with no owning Role cannot be prepared under this pattern.
- `PRECONDITION` — the intended audience and whether the document will be transmitted externally are stated.
- `PRECONDITION` — criticality band determined.

## Scope
### Covers
- source identification, acquisition and verification;
- separation of `FACT`, `ASSUMPTION` and `CALCULATION`;
- drafting and specialist section contribution;
- requirement and claim traceability;
- gap and conflict surfacing;
- review requirement identification;
- preparation to the point the approval decision becomes due.

### Does Not Cover
- **any domain conclusion** — every substantive conclusion is owned by the Role whose card owns it;
- **approval of the document** — a human decision right;
- **promotion to `APPROVED` or `CANONICAL`** — governed elsewhere;
- **independent review** — a requirement is referenced, never performed here;
- **external transmission** — a separate transmitting-act gate;
- canonical-status change — `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change` are human.

## Participating Roles

Role identity is parameterised through two declared slots. The slots are **closed**, not open placeholders: their binding constraints are stated below and an instance that cannot satisfy them is `BLOCKED`, not accommodated by widening the slot.

| Role ID / Slot | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| **Slot `SLOT.document_owner`** (binds one approved `role.<id>`) | `LEAD_ROLE` | `ALWAYS` | S1–S5 | Owns the document artifact per its own Role Card. Leading grants nothing further, and does **not** grant the specialist conclusions the document cites. |
| `role.knowledge_evidence_steward` | `CONTRIBUTING_ROLE` | `ALWAYS` | S1, S3, S4, S5 | Owns evidence integrity, provenance, source verification, the gap/conflict position and knowledge-state metadata. Owns **no** substantive conclusion in the document. |
| **Slot `SLOT.specialist_contributor`** (binds zero or more approved `role.<id>`) | `CONTRIBUTING_ROLE` | `CONDITIONAL(the document makes a claim whose conclusion the Document Owner's Role Card does not own)` | S2, S3 | Each owns its own section's conclusion. Contribution is by reference and attribution; the Document Owner does not absorb it. |
| `role.research_market_intelligence_analyst` | `CONTRIBUTING_ROLE` | `CONDITIONAL(sources must be discovered rather than supplied)` | S1 | Owns `artifact.research_evidence_pack`. Contributing rather than consulted **because it owns an artifact** when activated. |
| `role.institutional_communications_editorial_specialist` | `CONSULTED_ROLE` | `CONDITIONAL(the document is an institutional position or will be published)` | S5 | **Advisory only in this Stage** — it applies editorial standards to a document it does not own and advances no artifact here. Owns no substantive conclusion. |
| `role.data_room_disclosure_manager` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the document enters a controlled disclosure process)` | S5 | Owns `artifact.disclosure_log`. Contributing rather than consulted **because it owns an artifact** when activated. |

### Parameterized Role Slots

| Slot | Allowed source | Required ownership / interface condition | Permitted participation | Required artifact-ownership relationship | Phase 4 capability validation | Cardinality |
|---|---|---|---|---|---|---|
| `SLOT.document_owner` | An approved `role.<id>` from the Phase 3 Role Registry. No other identity type is admissible. | The Role's own Role Card must list the document artifact among its **Output Artifact Interfaces**, and the document's subject must fall inside that Role's *Owns* clause. | `LEAD_ROLE` only. | The bound Role **must already own** the document artifact under its Role Card. The slot selects an owner; it never creates one. | Every Skill, Specialisation or Pack activated for the bound Role must independently pass the approved Phase 4 mapping records — directly or under the Transitive Pack Compatibility Rule. Neither this Workflow nor the slot is evidence of compatibility. | Exactly **1** per instance. |
| `SLOT.specialist_contributor` | An approved `role.<id>` from the Phase 3 Role Registry. | The Role's Role Card must *own* the conclusion the contributed section states. A Role whose card excludes that conclusion is ineligible regardless of how relevant it seems. | `CONTRIBUTING_ROLE` only. A specialist that owns nothing in the Stage is not bound to this slot; it participates as a named `CONSULTED_ROLE` instead. | The bound Role must already own the artifact carrying its contributed conclusion. Contribution is by attribution and citation, never by transfer. | As above, per bound Role. | **0..n** — one binding per distinct specialist conclusion the document carries. |

Closing rules, applied to both slots:

- **No wildcards.** "Any Role", "an appropriate Role" and equivalents are prohibited. The eligibility conditions above are testable against the Role Card and the approved registries.
- **A slot cannot grant ownership.** If no approved Role already owns the document or the conclusion, the instance is **`BLOCKED` or invalid for that assignment** — the slot is not widened to make the assignment fit, and ownership is not fabricated.
- **A slot cannot bind** a System Control Profile, a Review Profile, a Decision Right, a model or a runtime identity.
- Binding resolves to exactly one concrete `role.<id>` per slot occurrence, per the cardinality column.

## Activated Skills / Packs

References only; instance Roles activate only what Phase 4 already permits them.

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `skill.source_verification` | `role.knowledge_evidence_steward` | direct (Wave 1) |
| `skill.source_monitoring` | `role.knowledge_evidence_steward` | direct (Wave 1) |
| `skill.requirement_traceability` | `role.knowledge_evidence_steward` | direct (Wave 1, migrated in Wave 3) |
| `skill.evidence_mapping`, `skill.evidence_gap_analysis` | `role.knowledge_evidence_steward` | direct |
| `skill.knowledge_state_metadata_management` | `role.knowledge_evidence_steward` | direct |
| `skill.document_structuring`, `skill.technical_writing` | the Role bound to `SLOT.document_owner`, where its Phase 4 mapping permits | per the bound Role's mapping record — validated at binding, never assumed |
| `skill.publication_requirements_validation` | per the mapping record for the publishing Role | direct; explicitly **not** independent review |

The Role bound to `SLOT.document_owner` activates document-production capability **only** where its own Phase 4 mapping already allows it. This pattern does not confer `skill.document_structuring` on a Role that Phase 4 has not mapped it to, and a binding that would require such a conferral fails — the instance is `BLOCKED` rather than the slot widened.

## Inputs

| Input | Required state |
|---|---|
| Named decision the document supports | stated, with `decision.<id>` where one exists |
| Candidate sources | `SOURCE`; provenance and currency to be established at S1 |
| Existing specialist artifacts to be cited | any governed state; `SUPERSEDED` inputs must be flagged, never silently cited |
| Prior version of the document, where one exists | any; supersession relationship recorded |

## Stages

### Stage `S1` — Source and evidence base
- **Objective:** establish what is actually known, and with what authority, before a single claim is drafted.
- **Entry Criteria:** preconditions satisfied.
- **Participating Roles:** the Role bound to `SLOT.document_owner` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`), `role.research_market_intelligence_analyst` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(sources must be discovered rather than supplied)`).
- **Activities:** source discovery where triggered; **source verification** — provenance, authority, version and effective date; evidence mapping; evidence gap analysis; conflict identification between sources.
- **Artifact Contributions:** `artifact.research_evidence_pack` (owned by `role.research_market_intelligence_analyst` where engaged); `artifact.evidence_integrity_record` and `artifact.evidence_gap_conflict_report` (owned by `role.knowledge_evidence_steward`).
- **Knowledge-State Expectations:** verified sources are `SOURCE` with provenance recorded. **Unverifiable material is `UNKNOWN` and stays `UNKNOWN`** — it is not promoted by being useful. Contradictory sources produce `CONFLICT_DETECTED`, which is carried, not resolved by preference.
- **Gate / Review References:** none at this stage.
- **Exit Criteria:** every source verified or explicitly marked unverified; gaps named; conflicts recorded with both positions.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `CANCELLED`.
- **Open-Item Materiality:** an unverifiable source that any material claim will rest on is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S3. A source relevant only to background context is `NON_MATERIAL_TO_NEXT_STEP` and is carried.

### Stage `S2` — Structure and specialist contribution
- **Objective:** establish the document's structure and obtain each specialist section **from the Role that owns it**, bound through `SLOT.specialist_contributor`.
- **Entry Criteria:** S1 exited; the decision the document supports is confirmed unchanged.
- **Participating Roles:** the Role bound to `SLOT.document_owner` (`LEAD_ROLE`), Roles bound to `SLOT.specialist_contributor` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL` per the slot table).
- **Activities:** document structuring against the decision's information needs; specialist section contribution; identification of which claims require a specialist and which the owner may make.
- **Artifact Contributions:** the document artifact (owned by the Role bound to `SLOT.document_owner`); specialist sections contributed **by attribution** — each remains the contributing Role's conclusion, cited rather than restated.
- **Knowledge-State Expectations:** `DRAFT`. **AI-generated content enters as `AI_SUGGESTION`** and remains so until a named Role adopts it as its own `DRAFT`. No quantity of drafting, no number of revisions and no stage advancement performs that adoption.
- **Gate / Review References:** none at this stage; specialist sections may carry their own `review.<id>` requirements inherited from their owning Role Cards.
- **Exit Criteria:** structure addresses the decision's information needs; every claim requiring a specialist has one; no unattributed specialist conclusion in the draft.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** a claim requiring a specialist conclusion that no bound `SLOT.specialist_contributor` Role supplies is `MATERIAL_TO_NEXT_STEP_OR_GATE` — the Document Owner may not supply it, so the claim is removed or the progression blocks.

### Stage `S3` — Fact, assumption and calculation separation
- **Objective:** make the document's epistemic structure visible — which statements are established, which are assumed, and which are derived.
- **Entry Criteria:** S2 exited.
- **Participating Roles:** the Role bound to `SLOT.document_owner` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`), Roles bound to `SLOT.specialist_contributor` (`CONTRIBUTING_ROLE`, for their own sections).
- **Activities:** classify every material statement as `FACT`, `ASSUMPTION` or `CALCULATION`; build the assumption register; trace each `CALCULATION` to its inputs and method; trace each `FACT` to its verified source.
- **Artifact Contributions:** assumption register within the document artifact; `artifact.evidence_integrity_record` updated (owned by `role.knowledge_evidence_steward`).
- **Knowledge-State Expectations:** the three classes remain **separable in the finished document** and are not merged into undifferentiated narrative. An assumption presented as a fact is a defect, not a style choice.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.factual_evidence`, `review.evidence_integrity_provenance`.
- **Exit Criteria:** every material statement classified; every `FACT` traced to a verified source; every `ASSUMPTION` in the register with its basis and its owner; every `CALCULATION` traced to inputs and method.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** an unclassified material statement, an `ASSUMPTION` with no recorded basis or owner, or a `CALCULATION` whose inputs cannot be traced is `MATERIAL_TO_NEXT_STEP_OR_GATE` toward S4 and S5.

### Stage `S4` — Traceability and coherence
- **Objective:** confirm the document does what the decision needs, and surface what it does not establish.
- **Entry Criteria:** S3 exited.
- **Participating Roles:** the Role bound to `SLOT.document_owner` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`).
- **Activities:** requirement traceability — each information need of the decision to the content that addresses it; orphan and gap analysis; internal contradiction check; consolidation of open items and unresolved assumptions.
- **Artifact Contributions:** traceability record within the document artifact; `artifact.evidence_gap_conflict_report` updated.
- **Knowledge-State Expectations:** an internal contradiction is `CONFLICT_DETECTED` and blocks or branches. A gate-critical `UNKNOWN` **blocks progression to S5**. Naming it as an open item the decision-maker will see does **not** release it — visibility is not disposal, and under `standard.workflow.common_constraints` §14A a `MATERIAL_TO_NEXT_STEP_OR_GATE` item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit. The only route past it is a **named external human Decision Right** that explicitly permits proceeding with it unresolved; that reference is recorded and the item stays open.
- **Gate / Review References:** `REVIEW_REQUIRED_REFERENCE` → `review.evidence_integrity_provenance`; and the domain review applicable to the document's subject, inherited from the owning Role Card.
- **Exit Criteria:** every information need traced or its gap named; no unrecorded contradiction; open items and unresolved assumptions consolidated and visible.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `REWORK_REQUIRED`, `ESCALATED`.
- **Open-Item Materiality:** a gate-critical `UNKNOWN` and any unresolved `CONFLICT_DETECTED` are `MATERIAL_TO_NEXT_STEP_OR_GATE` and **cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit**. The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED` unless a named external human Decision Right explicitly permits proceeding with the item unresolved.

### Stage `S5` — Review requirement and approval preparation
- **Objective:** identify what review the document requires, and present it so the human decision can be taken — including taken negatively.
- **Entry Criteria:** S4 exited.
- **Participating Roles:** the Role bound to `SLOT.document_owner` (`LEAD_ROLE`), `role.knowledge_evidence_steward` (`CONTRIBUTING_ROLE`), `role.institutional_communications_editorial_specialist` (`CONSULTED_ROLE`, `Activation: CONDITIONAL(institutional position or publication)`, advisory only) and `role.data_room_disclosure_manager` (`CONTRIBUTING_ROLE`, `Activation: CONDITIONAL(controlled disclosure process)`).
- **Activities:** identify the applicable `review.<id>` requirements from the owning and contributing Role Cards and the criticality band; record which are satisfied and which are not; publication-requirements validation where the document will be published; assemble the approval package with open items, unresolved assumptions and scope limitations stated **at the front**.
- **Artifact Contributions:** the document artifact finalised as `DRAFT` or `REVIEWED`; `artifact.disclosure_log` where controlled disclosure applies.
- **Knowledge-State Expectations:** the document is `DRAFT`, or `REVIEWED` where a governed review has occurred. **It does not become `APPROVED` or `CANONICAL` by reaching this stage, by any stage outcome, or by completion.**
- **Gate / Review References:** `HUMAN_GATE_REFERENCE` → the instance's named approval decision right; plus `decision.external_publication`, `decision.disclosure_authorisation`, `decision.external_data_transmission` or `decision.institutional_position_release` where the document is transmitted; plus `decision.canonical_knowledge_promotion` where canonical status is sought. Each is preserved under `standard.workflow.common_constraints` §8.
- **Exit Criteria:** the approval decision is due, with review status, open items, unresolved assumptions and scope limitations in front of the decision-maker.
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `BLOCKED`, `ESCALATED`, `CANCELLED`.
- **Open-Item Materiality:** any item bearing on the evidence basis of the named approval decision, or on a transmitting act where the document leaves the organisation, is `MATERIAL_TO_NEXT_STEP_OR_GATE`. A missing required `review.<id>` is material where the gate depends on it; its visibility does not satisfy it.

## Branches / Exception Paths

- `BRANCH` — **external transmission:** the applicable transmitting-act gate joins the S5 gate set, and publication-requirements validation becomes mandatory.
- `BRANCH` — **canonical status sought:** `decision.canonical_knowledge_promotion` joins the gate set and `artifact.canonical_promotion_package` is prepared. Preparing the package is not promoting anything.
- `BRANCH` — **no specialist content:** S2's specialist thread reduces; S3's separation and S4's traceability do **not** reduce.
- `BRANCH` — **document supersedes a prior version:** the supersession relationship is recorded and the prior version's state history preserved.
- `EXCEPTION_PATH` — **source found unverifiable at S3 or S4:** returns to S1 as `REWORK_REQUIRED`, or the dependent claim is removed. It is not retained as a `FACT` on the basis that it is probably right.
- `EXCEPTION_PATH` — **specialist declines to support a claim:** the claim is removed or attributed as unsupported. The Document Owner does not supply the missing conclusion.
- `EXCEPTION_PATH` — **material `CONFLICT_DETECTED` unresolved:** `BLOCKED` or `ESCALATED`. Because the conflict is material it is `MATERIAL_TO_NEXT_STEP_OR_GATE`, so **carrying it as an open item visible to the decision-maker does not release the progression** — that route exists only where a **named external human `decision.<id>`** explicitly permits proceeding with it unresolved, and the conflict then remains open and carried forward. It is never narrated away and never averaged.
- `EXCEPTION_PATH` — **deadline pressure:** `COMPLETE_WITH_OPEN_ITEMS` at S5 is available **only when every carried item affecting the approval gate is `NON_MATERIAL_TO_NEXT_STEP`**. Any `MATERIAL_TO_NEXT_STEP_OR_GATE` item — a gate-critical `UNKNOWN`, an unresolved `CONFLICT_DETECTED`, an unverified source under a material `FACT`, a missing required review — gives `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`. Progression with a material item unresolved is possible **only** through a **named external human `decision.<id>`** explicitly permitting it, and that item then **remains open and carried forward**; this Workflow neither resolves nor downgrades it, and does not treat a missing review as satisfied or waived. **Deadline pressure is not such a Decision Right**: it never drops the review requirement or the approval gate.

No exception path bypasses any gate or review reference on the normal path.

## Rework Rules

`REWORK_LOOP` targets: S4 → S2/S3 on a traceability or coherence failure; S3 → S1 on a verification failure; S5 → S3/S4 where review requirement identification exposes a gap.

Across every loop, prior document versions, their knowledge states, source verification records, the assumption register history, conflict records and the reason for rework are preserved. **A rework loop may not be used to remove an inconvenient recorded assumption or conflict.**

## Open-Item Materiality

For this Workflow's terminal gate, `MATERIAL_TO_NEXT_STEP_OR_GATE` covers: any gate-critical `UNKNOWN`; any unresolved `CONFLICT_DETECTED`; any `ASSUMPTION` material to the decision that has no recorded basis or owner; any unverified source under a material `FACT`; any specialist conclusion the document relies on but no bound Role supplies; and any missing `review.<id>` the gate or the criticality band depends on.

**A material item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit at the progression it is material to.** The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`. Making an item visible to the decision-maker is **not** a route past this rule — that was the specific defect the independent audit found at S4, and it is corrected.

The only exception is a **named external human Decision Right** explicitly permitting progression with that item unresolved. The gate reference is recorded, the item **remains open and unresolved**, and this Workflow neither decides the waiver nor asserts it was granted. Phase 7 owns that semantics.

## Completion Criteria

`COMPLETION_CRITERION` — S5 exited with the approval decision due; every `FACT` traced to a verified source; every `ASSUMPTION` registered with its basis and owner; every `CALCULATION` traced; every specialist conclusion attributed to its owning Role; every open item, unresolved assumption and scope limitation visible; review requirements identified with their status.

**Completion is not approval.** The document is prepared; the decision is a human act on the far side of the gate.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the decision the document supports is withdrawn or taken by other means; the evidence base proves insufficient in a way no rework repairs; or a human decision stops preparation.

On cancellation, the draft, sources, verification records, assumption register, conflict records and gate history are retained.

## Outputs / Resulting Artifact States

| Artifact | Owning Role | State at completion |
|---|---|---|
| the document artifact (instance-specific) | the Role bound to `SLOT.document_owner` | `DRAFT` or `REVIEWED` |
| specialist sections | the Roles bound to `SLOT.specialist_contributor` | their own governed states, unchanged by this Workflow |
| `artifact.evidence_integrity_record` | `role.knowledge_evidence_steward` | `DRAFT` or `REVIEWED` |
| `artifact.evidence_gap_conflict_report` | `role.knowledge_evidence_steward` | `DRAFT` |
| `artifact.canonical_promotion_package` where sought | `role.knowledge_evidence_steward` | `DRAFT` |

**No artifact reaches `APPROVED` or `CANONICAL` through this Workflow.** That is the point of the pattern.

## Authority / Review Boundary

- **This Workflow cannot self-approve.** No stage, outcome or completion state approves the document or promotes its knowledge state. `DRAFT -> REVIEWED -> APPROVED -> CANONICAL` occurs only under the governed rule that permits it, and never by stage movement.
- **AI output does not escape `AI_SUGGESTION` through this Workflow.** Adoption is an act by a named Role, not a consequence of progression.
- The Role bound to `SLOT.document_owner` owns the document **because its own Role Card already does** — the slot selected it, and conferred nothing. It does **not** own the specialist conclusions the document cites, and may not restate them as its own.
- `role.knowledge_evidence_steward` owns evidence integrity and **no substantive conclusion**. Verifying a source is not endorsing the claim built on it.
- No stage performs an independent review. `skill.publication_requirements_validation` is explicitly not independent review, per its own Skill Card.
- Every transmitting act retains its gate, and every gate referenced above is a **human decision right** held outside this Workflow.
- **Participation in this Workflow grants no professional authority.** A Role gains nothing beyond its own Role Card by participating, including at `LEAD_ROLE`.

## Criticality Scaling

| Band | Effect |
|---|---|
| Routine / Standard | Internal, low-reliance document: S3 separation required but the assumption register may be lightweight; review references advisory. |
| Enhanced Review Candidate | Material internal reliance or limited external audience: assumption register mandatory; `review.factual_evidence` expected; S4 traceability claim-by-claim. |
| Enhanced Decision-Grade | External reliance, financing, regulatory or board audience: full S1–S5 mandatory; `review.factual_evidence` and `review.evidence_integrity_provenance` mandatory; every `FACT` individually source-traced; transmitting-act gate explicit. |
| Major / Systemic | As above, plus no `COMPLETE_WITH_OPEN_ITEMS` exit at S5 for any decision-critical `UNKNOWN` or unresolved `CONFLICT_DETECTED`. |

Criticality changes evidence depth, traceability granularity and review intensity. **Role identity does not change**, and criticality does not create a second document Workflow.

## Evidence / Traceability Requirements

Source verification record for every cited source; provenance chain for every `FACT`; assumption register with basis, owner and current status for every `ASSUMPTION`; input and method trace for every `CALCULATION`; attribution for every specialist conclusion; conflict record with disposition; rework history; review requirement status; gate record.

## Versioning / Change Control

Version 0.1 — initial exemplar. No prior version, therefore no authority, Role scope, gate or artifact-ownership change to declare.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent execution, model routing, database schema, API, interface or automation code, and binds no model, provider or runtime technology.
