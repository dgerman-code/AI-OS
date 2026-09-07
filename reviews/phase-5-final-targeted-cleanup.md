# Phase 5 — Final Targeted Cleanup

Status: `PROPOSED — READY FOR FINAL HUMAN-APPROVAL RE-AUDIT`

Branch: `architecture/phase-5-workflow-registry`
Remediated baseline re-audited: `e32d87f40ec6c5ae83d2abcc566f739e6118dbaf`

The final independent re-audit returned **FAIL** for two narrowly bounded areas: residual M1 wording loopholes in terminal-stage and deadline-pressure prose, and seven participation-table inconsistencies under M2. M3, M4, M5, regression, phase boundaries, universe boundaries and authority leakage all passed and are untouched.

This cleanup changes **prose only**. No semantics were redesigned: `WORKFLOW_REFERENCE`, the Role Slot Binding Rule, the M3 Security Engineer correction, the participation vocabulary, universe counts, overlap groups and carding boundaries are unchanged.

---

## 1. Terminal review / materiality phrases corrected

The loophole was a single recurring formula used as **entry and completion sufficiency**:

> "required reviews satisfied **or their absence explicitly recorded**"

Under it, a missing required review could satisfy an exit merely by being written down — the same failure the M1 rule forbids for open items, surviving in the review clause.

Six occurrences corrected, three entry criteria and three completion criteria:

| File | Location | Was | Now |
|---|---|---|---|
| `project-development-readiness.md` | S7 entry | "required reviews for the criticality band satisfied or their absence explicitly recorded" | required reviews **satisfied under the Phase 6 review semantics**; recording absence is not sufficient; absence gives `BLOCKED` / `REWORK_REQUIRED` / `ESCALATED` unless a named external `decision.<id>` permits progression, and the review then **remains unsatisfied and open** |
| `project-development-readiness.md` | Completion Criteria | "every required review either satisfied or its absence recorded" | every required review **satisfied under the Phase 6 review semantics**; completion with one outstanding requires a named external `decision.<id>`, and the review remains unsatisfied and open |
| `eu-grant-application-development.md` | S6 entry | "required reviews satisfied or their absence explicitly recorded" | as above |
| `eu-grant-application-development.md` | Completion Criteria | "required reviews satisfied or their absence recorded" | as above, with every carried open item classified |
| `software-change-delivery.md` | S6 entry | "required reviews satisfied or their absence explicitly recorded" | as above |
| `software-change-delivery.md` | Completion Criteria | "required reviews satisfied or their absence recorded" | as above, naming `review.security` and `review.test_coverage` explicitly |

In every corrected passage the Workflow **does not** say the review was satisfied, waived by the Workflow, or no longer required. Who holds the permitting Decision Right and how waiver authority is granted remains Phase 7; nothing here invents it.

---

## 2. Deadline-path corrections — all four exemplars

Every exception path keyed on deadline, release-date or schedule pressure was rewritten to state the materiality rule **on the path itself**, so the exemplar cannot be read as admitting the contrary even though the generic constraint already forbids it.

| File | Path | Correction |
|---|---|---|
| `project-development-readiness.md` | gate deadline pressure | `COMPLETE_WITH_OPEN_ITEMS` available **only when every carried item affecting the progression is `NON_MATERIAL_TO_NEXT_STEP`** |
| `eu-grant-application-development.md` | deadline pressure | same, with the material classes named: unmet eligibility condition, unverified claim, unconfirmed required partner, missing required review |
| `software-change-delivery.md` | release-date pressure | same, with the material classes named: untested criterion, unvalidated control, open defect at or above severity, missing required review |
| `decision-grade-document-preparation.md` | deadline pressure | same, with the material classes named: gate-critical `UNKNOWN`, unresolved `CONFLICT_DETECTED`, unverified source under a material `FACT`, missing required review |

All four now state, explicitly and identically in substance:

1. `COMPLETE_WITH_OPEN_ITEMS` requires **every** carried item affecting that progression to be `NON_MATERIAL_TO_NEXT_STEP`;
2. any `MATERIAL_TO_NEXT_STEP_OR_GATE` item gives `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`;
3. progression with a material item unresolved is possible **only** through a named external human `decision.<id>` explicitly permitting it;
4. the item then **remains open and carried forward** — the Workflow neither resolves nor downgrades it, and does not treat a missing review as satisfied or waived;
5. **deadline pressure is not such a Decision Right** and removes no review requirement and no human gate.

### One further loophole of the same family, found and closed

Not listed in the prompt, but the same defect: `decision-grade-document-preparation.md` carried an exception path reading

> "**material `CONFLICT_DETECTED` unresolved:** `ESCALATED`, **or carried as an explicit open item to the decision-maker**"

That second branch let a *material* conflict release the progression by being made visible — precisely the reading the re-audit rejected elsewhere. It now reads `BLOCKED` or `ESCALATED`, states that carrying the conflict as a visible open item does **not** release the progression, and confines that route to a named external `decision.<id>` with the conflict remaining open.

---

## 3. Participation table reconciliation — seven discrepancies

The M2 semantics were correct and were not changed. Only the top-level tables and per-stage lists were reconciled.

The root cause in two cards was **aggregate phrasing**: a stage listed its participants collectively ("every `CONTRIBUTING_ROLE` from S2–S5 re-engaged", "implementing engineers") rather than by ID, so the per-stage lists and the top-level stage columns could not be checked against each other.

### Project Development Readiness — four discrepancies

S6 re-engages every contributing Role but named none. The S6 participating-role list now names all twelve explicitly, and the four conditional Roles gained S6 in the top-level table:

| Role | Stage list was | Now | Activation |
|---|---|---|---|
| `role.sector_technical_expert` | S2 | **S2, S6** | `CONDITIONAL(sector Specialisation exists and the technical basis depends on it)` — unchanged |
| `role.asset_om_technical_operations_specialist` | S3 | **S3, S6** | `CONDITIONAL(operating-cost or O&M basis required)` — unchanged |
| `role.procurement_state_aid_specialist` | S3 | **S3, S6** | `CONDITIONAL(procurement rules or State Aid exposure)` — unchanged |
| `role.insurance_risk_transfer_specialist` | S5 | **S5, S6** | `CONDITIONAL(insurance material to bankability or risk allocation)` — unchanged |

None was converted to `ALWAYS`. The S6 text states that each conditional Role is re-engaged **under the same trigger that activated it earlier**, and that a Role not activated in its originating Stage is not activated at S6 either.

### EU Grant Application Development — two discrepancies

| Role | Issue | Resolution |
|---|---|---|
| `role.consortium_partner_coordination_specialist` | Participates in S6 but the table listed S2, S3, S5 | **S6 added** to the stage list |
| `role.grant_financial_compliance_budget_specialist` | Table listed S4; S4 does not include it | **S4 removed** from the stage list — the preferred resolution. S4 is narrative content assembly with legal, DPIA, State Aid and dissemination contributions; it does not require this Role to contribute an owned artifact, so the Role was **not** added merely to make the table match |

### Software Change Delivery — one discrepancy

| Role | Issue | Resolution |
|---|---|---|
| `role.data_database_architect` | Table listed S2, S3; S3 does not include it | **S3 removed** — the preferred resolution. Both its artifacts are S2 *design* artifacts; S3 migration implementation belongs to `role.database_data_engineer`. The boundary note now says so. No artificial S3 participation was added for symmetry |

S5 additionally named its defect-remediation participants collectively as "implementing engineers"; they are now named by ID under the same conditional triggers that activated them at S3. This resolved the residual S5 column mismatches for the three engineering Roles without changing any activation condition.

**Result: 0 discrepancies in all four cards**, verified mechanically by comparing each top-level stage column against the IDs actually named in each stage's participating-role list.

---

## 4. Validation

All 27 checks **PASS**, verified against baseline `e32d87f`.

| # | Check | Result |
|---:|---|---|
| 1 | No required-review absence satisfies entry/completion merely by being recorded | PASS |
| 2 | Every deadline-pressure `COMPLETE_WITH_OPEN_ITEMS` path limited to `NON_MATERIAL_TO_NEXT_STEP` items | PASS |
| 3 | Material items on deadline paths block/rework/escalate unless a named external Decision Right permits | PASS |
| 4 | Missing reviews stay unresolved; no wording says the Workflow satisfied or waived review | PASS |
| 5 | All four exemplar cards remain `PROPOSED` | PASS |
| 6 | Phase 3 Role Cards unchanged | PASS |
| 7 | Approved Phase 4 architecture/mappings unchanged | PASS |
| 8 | M3 Security Engineer S3 intact | PASS |
| 9 | Security Engineer exclusions from `skill.quality_attribute_analysis` and `skill_pack.supabase` intact | PASS |
| 10 | `WORKFLOW_REFERENCE` semantics unchanged | PASS |
| 11 | Role Slot Binding Rule semantics unchanged | PASS |
| 12 | Consulted-role artifact/conclusion mismatch count remains 0 | PASS |
| 13 | Project top-level vs per-stage participation discrepancy count = 0 | PASS |
| 14 | EU Grant top-level vs per-stage participation discrepancy count = 0 | PASS |
| 15 | Software top-level vs per-stage participation discrepancy count = 0 | PASS |
| 16 | Decision-Grade Document top-level vs per-stage participation discrepancy count = 0 | PASS |
| 17 | Conditional activation triggers objective and unchanged except stage-list reconciliation | PASS |
| 18 | No authority leakage introduced | PASS |
| 19 | No new Workflow cards created | PASS |
| 20 | Candidate universe remains 49 unique IDs | PASS |
| 21 | Rejected candidates remain 7 | PASS |
| 22 | Audit-flagged blocked-from-carding candidates remain 20 | PASS |
| 23 | Overlap groups remain 8 | PASS |
| 24 | Exemplar cards remain 4 | PASS |
| 25 | No runtime/database/API/orchestrator/model implementation introduced | PASS |
| 26 | No PR created | PASS |
| 27 | Working tree clean after commit | PASS |

Checks 10 and 11 are verified structurally: `architecture/workflow-registry-design.md` and `workflows/_standards/common-workflow-constraints.md` are **byte-identical** to the remediated baseline, and no added or removed line in Exemplar D touches a slot declaration.

### Honesty note

The suite first reported 26/27. Check 11 failed because it counted the string `SLOT` anywhere in the file's diff output, including an unchanged **context** line that git prints around the one modified line. The M5 semantics were in fact untouched. The check was corrected to inspect only added and removed lines, which is what it was meant to test. No check was weakened.

---

## Standing statement

Every Phase 5 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. This record does not claim human approval and is not an independent audit — it is the producing pass reporting on its own cleanup. Four of 49 candidates are carded; 45 remain unvalidated and 20 of those carry an explicit card-generation prohibition.
