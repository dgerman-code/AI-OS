# Phase 5 — Foundation Remediation After Independent Audit

Status: `PROPOSED — READY FOR FINAL INDEPENDENT PHASE 5 FOUNDATION RE-AUDIT`

Branch: `architecture/phase-5-workflow-registry`
Foundation baseline audited: `17c95ac191c66a7f18cc13421480e44ef46a6af8`

The independent audit returned **PASS WITH CHANGES**: no HIGH findings, five MEDIUM. Architecture identity, phase boundary and the authority model passed and are untouched. This remediation is bounded to M1–M5 plus the universe carding boundary and the open-question dispositions.

No Role, Skill, Specialisation or Pack was added, removed or renamed. No Phase 3 Role Card and no approved Phase 4 artifact was modified. No runtime, database, orchestration, scheduling, model-routing, agent, API or UI element was introduced. No candidate was bulk-carded.

---

## M1 — Materiality-aware open-item progression

**Problem.** `COMPLETE_WITH_OPEN_ITEMS` had no materiality rule, so recording an item was indistinguishable from disposing of it. Any gate-critical `UNKNOWN`, `CONFLICT_DETECTED`, unresolved material `ASSUMPTION` or missing review could satisfy an exit merely by being named.

**Resolution.** A registry-wide two-value progression-materiality classification, applied in the architecture, the standard, the template and all four exemplar cards.

| Classification | Meaning |
|---|---|
| `NON_MATERIAL_TO_NEXT_STEP` | Resolving it could not change the next Stage's permitted work, any downstream conclusion, any review position, any gate's evidence basis, or the terminal conclusion |
| `MATERIAL_TO_NEXT_STEP_OR_GATE` | Any unresolved item that could change the next Stage's permitted work, a specialist conclusion relied on downstream, a required review position, a human gate's evidence basis, a transmitting act, or a terminal readiness conclusion |

Rules now enforced:

1. Every open item carried under `COMPLETE_WITH_OPEN_ITEMS` is classified; an unclassified item is a defect.
2. **A material item cannot support `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS`** for the progression it is material to. The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.
3. The **only** exception is a **named external human Decision Right** explicitly permitting progression with the item unresolved. The Workflow records the `decision.<id>`, the item **stays open and unresolved**, and the Workflow neither decides the waiver, defines its conditions, nor asserts it was granted.
4. A missing required `review.<id>` may be visible; **visibility does not satisfy it**. Absence blocks where the next Stage or gate depends on it, unless an external Decision Right governs proceeding without it.
5. `UNKNOWN`, `CONFLICT_DETECTED` and material `ASSUMPTION` are **never cleared by stage movement**.
6. This is progression materiality only, explicitly not a risk-severity taxonomy — severity belongs to the risk Roles' own methodologies.

Who holds such a Decision Right and what granting it means remains Phase 7; nothing here invents it.

**Exemplar D S4 — the specific defect named by the audit.** The card previously read that a gate-critical `UNKNOWN` "blocks progression to S5 **unless it is explicitly carried as a named open item that the decision-maker will see**". That clause made visibility a release mechanism, which is precisely the failure the rule now forbids. It now reads that the `UNKNOWN` blocks, that naming it does not release it, and that the only route past is a named external Decision Right with the item still open.

Every Stage in all four cards now carries an explicit `Open-Item Materiality` line, and each card carries a workflow-level `## Open-Item Materiality` section naming what is material at its terminal gate.

**Files:** `architecture/workflow-registry-design.md`, `workflows/_standards/common-workflow-constraints.md` (§14A), `workflows/_templates/workflow-card-template.md`, all four exemplar cards.

---

## M2 — Conditional activation separated from participation type

**Problem.** `CONSULTED_ROLE` was carrying two unrelated meanings — advisory participation, and conditional engagement. Roles typed consulted were in several cases producing and owning artifacts when triggered.

**Resolution.** Activation is now a **separate declared property**, not a participation type. No sixth type was added.

```
Activation: ALWAYS | CONDITIONAL(<objective trigger>)
```

The discriminator between the two contributing types is **ownership within the Stage**, never frequency:

- `CONTRIBUTING_ROLE` — produces bounded work, artifact content, an owned artifact, or an owned professional conclusion in that Stage;
- `CONSULTED_ROLE` — advisory or input-only; **owns and advances nothing in that Stage**.

A Role may be `CONTRIBUTING_ROLE` with `Activation: CONDITIONAL(...)`, and that is the **required** treatment for a triggered specialist that produces an owned artifact. The trigger must be an objective, testable condition. Conditional activation narrows participation and never widens Phase 4 compatibility or Role scope.

The participation table in the template gained an `Activation` column.

### Corrected exemplar assignments

| Card | Role | Was | Now |
|---|---|---|---|
| A | `role.sector_technical_expert` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(sector Specialisation exists and the technical basis depends on it)` — owns `artifact.sector_technical_opinion` |
| A | `role.asset_om_technical_operations_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(operating-cost or O&M basis required)` — owns `artifact.operating_cost_driver_definition` |
| A | `role.procurement_state_aid_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(procurement rules or State Aid exposure)` — owns two artifacts |
| A | `role.insurance_risk_transfer_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(insurance material to bankability or risk allocation)` — owns `artifact.insurance_programme_design` |
| B | `role.learning_vet_design_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(vocational-excellence or learning-design action)` — owns curriculum and assessment design |
| B | `role.monitoring_evaluation_learning_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(results framework or indicator set required)` |
| B | `role.legal_regulatory_lead` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(legal-framework, IP or contractual questions)` — owns `artifact.legal_analysis` |
| B | `role.data_protection_gdpr_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(personal data processed)` — owns the DPIA |
| B | `role.procurement_state_aid_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(State Aid or procurement exposure)` — owns `artifact.state_aid_assessment` |
| B | `role.institutional_communications_editorial_specialist` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(dissemination or communication content required)` — owns `artifact.dissemination_plan` |
| B | `role.sector_technical_expert` | `CONSULTED_ROLE` | **`CONSULTED_ROLE` retained**, `CONDITIONAL(material sector technical content)` — genuinely advisory here, owns nothing in S4 |
| B | `role.deliverables_reporting_specialist` | `CONSULTED_ROLE` | **`CONSULTED_ROLE` retained**, `CONDITIONAL(reporting schedule designed into the proposal)` — advisory, owns nothing in S3 |
| C | `role.ux_ui_information_architecture_specialist` | `CONTRIBUTING_ROLE`, trigger in prose | `CONTRIBUTING_ROLE`, `CONDITIONAL(user-facing surface altered)` |
| C | `role.data_database_architect`, `role.integration_api_engineer`, `role.full_stack_software_engineer`, `role.database_data_engineer` | trigger in prose | `CONTRIBUTING_ROLE`, `CONDITIONAL(...)` per layer |
| C | `role.solution_architect` at S3 | `CONSULTED_ROLE` | **`CONSULTED_ROLE` retained**, `CONDITIONAL(implementation deviates from the S2 design position)` — advisory, owns nothing in S3 |
| D | `role.research_market_intelligence_analyst` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(sources must be discovered)` — owns `artifact.research_evidence_pack` |
| D | `role.data_room_disclosure_manager` | `CONSULTED_ROLE` | `CONTRIBUTING_ROLE`, `CONDITIONAL(controlled disclosure process)` — owns `artifact.disclosure_log` |
| D | `role.institutional_communications_editorial_specialist` | `CONSULTED_ROLE` | **`CONSULTED_ROLE` retained**, `CONDITIONAL(institutional position or publication)` — advisory, owns nothing in S5 |

Twelve reclassifications, five deliberate retentions. Every retained `CONSULTED_ROLE` row now states explicitly that it owns and advances nothing in that Stage — the retention is an assertion, not an oversight.

**Files:** `architecture/workflow-registry-design.md`, `workflows/_standards/common-workflow-constraints.md` (§14B), `workflows/_templates/workflow-card-template.md`, all four exemplar cards.

---

## M3 — Software Change Delivery S3 security ownership defect

**Problem.** S3 advanced `artifact.security_control_implementation`, owned by `role.security_engineer`, while that Role did not participate in S3. The Stage was advancing an artifact whose owner was absent.

**Resolution — the preferred correction, not the removal.** `role.security_engineer` is added to S3 as `CONTRIBUTING_ROLE` with `Activation: CONDITIONAL(security-control implementation is in scope)`. Its S3 work is bounded to implementing the security controls that Role already owns, designed at S2.

Updated consistently: the top participation table (Stages now S2, S3, S4, S6, with per-Stage activation stated), the S3 participating-role list, the S3 activities line (control implementation now attributed to the Security Engineer explicitly), and the S3 artifact contribution ("owned **and produced here** by `role.security_engineer`").

**Phase 4 boundaries confirmed unchanged:** `role.security_engineer` remains excluded from `skill.quality_attribute_analysis` and from `skill_pack.supabase`. Nothing in this correction grants either, and the card restates both exclusions in the participation table and in the Activated Skills section. Adding a Role to a Stage is a participation change; it is not a capability change.

**Files:** `workflows/exemplars/software-change-delivery.md`.

---

## M4 — Declarative reusable Workflow composition

**Problem.** The architecture claimed the generic document Workflow was "composed into" other Workflows while the primitive model had no way to represent composition at all.

**Resolution.** One new declarative primitive, `WORKFLOW_REFERENCE` — the primitive table moves from 12 to 13.

Semantics, stated in the architecture and enforced in the standard (§14C):

1. It points at a stable `workflow.<id>`, optionally with a version constraint or reference policy, and **does not execute the child**. No call, scheduling, retry, nesting, call stack, state machine or database form.
2. The parent card states the reference's bounded purpose, expected inputs, expected outputs and the parent Stage(s) it relates to.
3. Referencing transfers **nothing** — not Role ownership, Skill compatibility, review identity, Decision Rights, gates or knowledge-state authority.
4. The child's gates and review requirements **cannot be silently dropped**; a parent relying on an output that requires a child gate keeps that dependency visible.
5. **Acyclicity is an architecture validation rule** — no direct or transitive self-reference. A cycle is a registry defect readable from the cards.
6. A reference may be optional or conditional only under a stated objective condition.

The template gained a `## Composed Workflow References` section.

### Does any parent exemplar reference the generic document Workflow?

**No — and that is a deliberate finding recorded on both cards, not an omission.**

`workflow.project_development_readiness` is the closest candidate: its S6–S7 produce a decision-grade document and map closely onto the child's S3–S5. But the child's S1 evidence base and S2 specialist contribution are satisfied by the parent's *own* S1 and S2–S5, spread across the whole pattern rather than sitting inside the segment that would carry the reference. That is a partial, overlapping fit — not a clean whole-child composition — and forcing a reference to make the new primitive look exercised would be exactly the false composition the instruction warns against.

Both cards state the reason. The Master Universe wording was corrected from "is intended to be *composed into* the others" to "**a candidate reusable pattern available through `WORKFLOW_REFERENCE`** where a parent's full preconditions and outputs match it". Whether the child should be decomposed so its document-production segment can be referenced independently is recorded as an open question for a wider exemplar set.

The remaining two exemplars carry an explicit `**None**` with their reasons: the EU grant package serves a submission gate rather than an approval gate; the software Workflow produces evidence and a readiness position rather than a prepared document, and its emergency path *routes to* `workflow.incident_response_and_recovery` rather than composing it.

**Files:** `architecture/workflow-registry-design.md`, `workflows/_standards/common-workflow-constraints.md` (§14C), `workflows/_templates/workflow-card-template.md`, all four exemplar cards, `workflows/master-workflow-universe.md`.

---

## M5 — Closed validation for parameterized Role slots

**Problem.** Exemplar D used a "Document Owner Role" and "Specialist Contributing Roles" as open placeholders. An unclosed slot is an authority hole.

**Resolution.** A **Role Slot Binding Rule** in the architecture (§4), the standard (§14D) and the template. Every slot declares: slot ID; allowed source (**approved `role.<id>` only**); the required ownership or interface condition; permitted participation type(s); required artifact-ownership relationship; and the Phase 4 capability validation rule.

Binding rules: exactly one concrete approved Role per slot occurrence unless a cardinality above one is declared; **wildcards prohibited** unless followed by testable eligibility constraints; **a slot cannot grant ownership** — the bound Role must already own the artifact or conclusion; every activated capability must independently pass Phase 4, and neither the Workflow nor the slot is evidence of compatibility; a slot cannot bind a System Control Profile, Review Profile, Decision Right, model or runtime identity; where no approved Role qualifies, the instance is **`BLOCKED` or invalid** and the slot is not widened.

### Exemplar D changes

Two named, closed slots replace the prose placeholders, with a full constraint table:

| Slot | Ownership condition | Participation | Cardinality |
|---|---|---|---|
| `SLOT.document_owner` | The Role Card lists the document artifact among its Output Artifact Interfaces **and** the subject falls inside its *Owns* clause | `LEAD_ROLE` only | exactly 1 |
| `SLOT.specialist_contributor` | The Role Card **owns the conclusion** the contributed section states; a Role whose card excludes it is ineligible however relevant it seems | `CONTRIBUTING_ROLE` only | 0..n, one per distinct specialist conclusion |

Every reference to the prose placeholders across the card was replaced with the bound-slot form, including in the Activated Skills table, the outputs table and the Authority / Review Boundary section, which now states that the bound Role owns the document **because its own Role Card already does — the slot selected it and conferred nothing**.

**Files:** `architecture/workflow-registry-design.md`, `workflows/_standards/common-workflow-constraints.md` (§14D), `workflows/_templates/workflow-card-template.md`, `workflows/exemplars/decision-grade-document-preparation.md`.

---

## Universe and carding boundary

The universe **remains 49 candidates**; nothing was deleted or merged. The independent audit's classification is recorded in a new section 10A: 29 VALID WORKFLOW, 8 needing boundary refinement, 10 likely Role or Skill in disguise pending a multi-Role test, 2 likely single-gate preparation patterns, 0 runtime concerns.

**The 20 candidates in the last three rows must not be carded** until each passes, with the result recorded against it: the Role-vs-Workflow test (§15), the multi-stage test (§16), an artifact-ownership test, and a composition test (§14C). The two single-gate candidates face the sharpest form of the multi-stage test — a pattern existing only to reach one gate is a gate reference, not a Workflow.

The eight overlap groups remain open and visible; group 1's wording was corrected in line with M4. Card generation for all uncarded candidates remains selective and assignment-driven, with the 20 carrying the additional prohibition.

---

## Open-question dispositions

| # | Question | Disposition |
|---:|---|---|
| 1 | Composition | **RESOLVED IN FOUNDATION** — declarative `WORKFLOW_REFERENCE`, acyclic, non-runtime, transferring nothing |
| 2 | Partial ordering | **SAFE TO DEFER WITH EXPLICIT RULE** — parallelism stays prose, and the prose must remain unambiguous and testable. A notation would risk becoming the runtime DSL this phase prohibits |
| 3 | Workflow version binding | **RUNTIME-PHASE CONCERN** — the registry still requires a version and a change record on every card, and constraints §12 still forbids silent authority drift across versions |
| 4 | Open-item materiality | **RESOLVED IN FOUNDATION** — shared two-value progression-materiality rule |
| 5 | Trigger vocabulary | **SAFE TO DEFER WITH EXPLICIT RULE** — triggers remain objective, testable prose; a controlled vocabulary is not adopted on four exemplars' evidence |
| 6 | Parameterized Role slots | **RESOLVED IN FOUNDATION** — closed Role Slot Binding Rule |
| 7 | System Control interaction | **RUNTIME-PHASE CONCERN** — selection may narrow only within registry-declared conditions and may never mutate or widen Workflow semantics |

---

## Validation

All 30 regression checks **PASS**, verified mechanically against baseline `17c95ac`.

| # | Check | Result |
|---:|---|---|
| 1 | Phase 3 Role Cards unchanged | PASS |
| 2 | Approved Phase 4 architecture/mappings unchanged | PASS |
| 3 | All Phase 5 artifacts remain PROPOSED | PASS |
| 4 | Registry separation statement unchanged | PASS |
| 5 | No Workflow grants professional authority | PASS |
| 6 | No Workflow grants or satisfies a human Decision Right | PASS |
| 7 | No Workflow defines independent reviewer identity/method | PASS |
| 8 | No Workflow self-promotes REVIEWED/APPROVED/CANONICAL | PASS |
| 9 | AI outputs remain AI_SUGGESTION/DRAFT until governed adoption | PASS |
| 10 | No Workflow widens Phase 4 capability compatibility | PASS |
| 11 | Material open items cannot pass without a named external Decision Right | PASS |
| 12 | `COMPLETE_WITH_OPEN_ITEMS` is not a generic gate-critical waiver | PASS |
| 13 | Conditional activation independent of participation type everywhere | PASS |
| 14 | Every artifact-producing Role in every Stage is LEAD or CONTRIBUTING | PASS |
| 15 | `CONSULTED_ROLE` produces no owned artifact/conclusion in its Stage | PASS |
| 16 | Software S3 security artifact has its owning Role participating | PASS |
| 17 | Security Engineer excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase` | PASS |
| 18 | `WORKFLOW_REFERENCE` declarative, acyclic, non-runtime, cannot drop child gates | PASS |
| 19 | Parameterized Role slots bind only to approved concrete Roles under closed rules | PASS |
| 20 | Slot binding cannot widen Role scope or Phase 4 compatibility | PASS |
| 21 | 49 candidate IDs remain unique | PASS |
| 22 | 7 deliberate exclusions remain sound | PASS |
| 23 | 20 audit-flagged candidates marked not safe to card yet | PASS |
| 24 | 8 overlap groups remain visible and open | PASS |
| 25 | No mass card generation performed | PASS |
| 26 | Four exemplars pass the corrected participation/materiality rules | PASS |
| 27 | Reference integrity; forward review/decision are explicit Phase 6/7 dependencies | PASS |
| 28 | No runtime/database/API/orchestrator/model implementation introduced | PASS |
| 29 | No PR created | PASS |
| 30 | Working tree clean after commit | PASS |

Check 27 detail: 0 invalid `role.*`, 0 invalid `skill.*` / `specialisation.*` / `skill_pack.*`, 0 invalid `artifact.*`. Every `review.*` and `decision.*` reference resolves to an approved Role Card and remains an explicit forward dependency on Phase 6 and Phase 7 respectively.

### Honesty note on the checks

The suite first reported 27/30. All three failures were investigated:

- **Check 8** was a genuine gap: the software card stated only that the readiness package does not become `APPROVED` at S6, and never carried the general no-promotion clause the other three cards carry. The clause was added to the card.
- **Check 19** was half genuine: the design document called the rule "Parameterized Role slots and their binding rule" while the standard called it the "Role Slot Binding Rule", and the template did not name it at all. The naming was made consistent across all three, which is what the finding asked for.
- **Check 24** was a defect in the check — a `findall` missing `re.MULTILINE`. All eight overlap groups were present throughout.

No check was weakened to obtain a pass.

---

## Standing statement

Every Phase 5 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. This record does not claim human approval and is not an independent audit — it is the producing pass reporting on its own remediation. Four of 49 candidates are carded; 45 remain unvalidated and 20 of those carry an explicit card-generation prohibition until they pass the four tests in section 10A of the Master Workflow Universe.
