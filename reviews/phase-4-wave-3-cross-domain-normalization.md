# Phase 4 — Wave 3 Cross-Domain Normalization

Status: PROPOSED — READY FOR INDEPENDENT PHASE 4 REVIEW

Scope: a single consolidated normalization pass over the Skill Registry across all 59 approved Roles, performed after the Wave 2 remediation re-audit returned PASS WITH NON-BLOCKING NOTES with no remaining blockers.

This record is self-contained. An independent auditor should be able to validate every decision below from this file plus the repository, without reference to any working history.

Nothing here is APPROVED or CANONICAL. Mass card generation remains prohibited.

---

## 1. Audit-trail correction — Project Development Lead

The Wave 2 re-audit confirmed that removing `skill_pack.bid_proposal_management` from `role.project_development_lead` was correct, and separately found that the permanent explanation for it was factually too broad.

**The overstatement.** The record said the Role Card "carries no bidding, tendering, proposal or governed-submission surface: its owned artifacts are internal preparation documents". Both halves are false on the Role Card:

- `artifact.project_definition_document` carries `Transmitting Act: submission where issued to lenders, investors or authorities`, COSTLY_TO_REVERSE afterwards;
- `artifact.development_readiness_assessment` carries `Transmitting Act: submission`, COSTLY_TO_REVERSE afterwards;
- the Extended profile names external submissions — permit applications, lender and investor submissions, land and connection agreements — and requires tender deadlines and permitting windows to be captured.

**The corrected distinction, now in the mapping record.** The Role does transmit externally and does track tender deadlines. What it does not own is a **formal competitive response-to-solicitation process**: bid/no-bid qualification, a compliance matrix built from a solicitation, multi-author narrative coordination, and submission-readiness control against evaluation criteria. That is the Pack's subject and it belongs to `role.sales_business_development_specialist` and `role.eu_grants_programmes_specialist`.

**Mapping decision unchanged.** The Pack remains unmapped to this Role, and the cascade removing the Role from the `skill.source_verification` and `skill.requirement_traceability` allowlists stands.

Why this mattered enough to fix: a false statement in a permanent audit trail is load-bearing for future readers. "No governed-submission surface" could be used to conclude the Role has no external act at all, which would be materially wrong given two COSTLY_TO_REVERSE submissions and `decision.land_or_site_commitment`.

---

## 2. Candidate Universe Gap decisions — 8 of 8 resolved

No candidate remains ambiguous.

| Candidate | Decision | Rationale |
|---|---|---|
| `skill.negotiation_preparation` | **ADD AS REUSABLE SKILL** | Named in the Core Skills prose of four approved Role Cards — Programme / Partnership Manager, Supply Chain & Procurement Operations, Project Development Lead, Project Finance / Transaction — and bounded identically in all four as preparation within delegated limits. Four consumers with a common bound is the clearest reuse case in the gap list. Added to Strategy & Analysis, mapped to those four Roles, and carded (see section 7) because its authority boundary is its whole point. |
| `skill.variance_analysis` | **ADD AS REUSABLE SKILL** | FP&A owns "variance analysis and driver explanation" outright; Grant Financial Compliance owns budget reallocation analysis, which is the same method against grant execution. Two consumers. Distinct from `skill.financial_evidence_reconciliation`, which ties figures to records rather than explaining deviation by driver. Added to Finance & Economics. |
| `skill.defect_management` | **ADD AS REUSABLE SKILL** | Software QA owns "defect identification, reproduction and severity characterisation" with no registry entry, leaving its core at two capabilities and under-representing the Role. Distinct from defect *correction*, which is implementation. Second consumer in Full-Stack, which reproduces defects before correcting them. Added to Software / Integration / Platform / Security. |
| `skill.editorial_multilingual_coordination` | **REPRESENT WITH EXISTING** | `skill.editorial_quality_control` supplies the coordination method and `specialisation.multilingual_content` supplies the bounded context. Both are already mapped to both affected Roles, so no mapping change was needed. Adding a third ID would have split one capability across two entries. |
| `skill.governance_structure_design` | **ROLE-SPECIFIC PROSE — DO NOT ADD** | Joint governance design across partner organisations is genuinely owned by Programme / Partnership Manager and genuinely distinct from `skill.role_responsibility_mapping`, which allocates responsibilities inside one organisation. But it has exactly one consumer: PPP / Concession owns contract term architecture, not partnership governance bodies. Adding a single-consumer Skill would worsen the very over-cardification pressure Wave 3 exists to reduce. The existing approximation — `skill.role_responsibility_mapping` plus `skill.decision_criteria_design` — is retained and its limitation is recorded here. **Re-open when a second consumer appears.** |
| `skill.commissioning_readiness_assessment` | **ROLE-SPECIFIC PROSE — DO NOT ADD** | Single consumer (Asset O&M). `skill.delivery_readiness_assessment` is the delivery-management technique and does not carry operational acceptance content, so this is not a merge; it is a capability whose reuse case has not appeared. Carried by `skill.om_strategy_design` and `skill.asset_performance_analysis`, both mapped. |
| `skill.qa_response_control` | **ROLE-SPECIFIC PROSE — DO NOT ADD** | Single consumer (Data Room & Disclosure Manager), which already holds five core capabilities covering the document-control surface. Q&A consistency across competing parties is carried by `skill.disclosure_tracking` plus `skill.action_tracking`. |
| `skill.accession_alignment_analysis` | **SPLIT / REFRAME BEFORE ADDING** | Decomposes into method plus context. The method is already present — `skill.regulatory_mapping` for the acquis perimeter, `skill.capability_gap_analysis` for administrative capacity, `skill.institutional_mapping` for competence, all mapped to EU Enlargement / Governance. What is missing is the bounded context. **Proposed normalized shape: `specialisation.eu_accession_context`, class JURISDICTION**, bounding negotiating chapters, screening stages and the acquis structure. **Not activated**: it is not in the Universe and appears in no mapping. A future governed decision may add it. |

**Net: 3 added, 1 represented with existing, 3 kept as role-specific prose, 1 reframed and deferred.**

---

## 3. Overlap / micro-skill normalization — 14 of 14 groups resolved

Merges are governed changes: each has one surviving ID, migrated mappings and a tombstone in the Universe deprecation register.

| # | Group | Outcome | Detail |
|---|---|---|---|
| 1 | market sizing / segmentation / demand analysis | **KEEP DISTINCT — clarify** | Three methods with different inputs and error modes; all multi-Role (2, 5, 4 consumers). Boundaries written into the Universe. |
| 2 | risk identification / risk register design | **KEEP DISTINCT — clarify** | Elicitation (14 Roles) versus designing the register instrument — taxonomy, scales, aggregation — which is the methodology surface owned by Enterprise / Project Risk. Merging on name similarity is exactly what the normalization rules forbid. |
| 3 | action tracking / milestone management / deliverable planning | **KEEP DISTINCT — clarify** | Three tracked objects with different cadence and completion semantics; 8, 7 and 5 consumers. |
| 4 | process design / process mapping / SOP design | **KEEP DISTINCT — clarify** | Designing a target process, documenting an existing one, and writing the operating procedure are separately commissioned; 4, 4 and 3 consumers. |
| 5 | source discovery / comparison / verification / monitoring / change detection | **KEEP DISTINCT — clarify** | Five distinct operations on sources. `skill.source_discovery` is single-consumer because most Roles are given their source set rather than assembling it — a consumer count, not a duplication. |
| 6 | capacity planning / resource planning | **MERGE** | Survivor `skill.capacity_planning` (7 consumers). Both consumers of the retired ID already held the survivor, so the merge migrated cleanly with no capability lost. |
| 7 | evidence indexing / data room index design | **KEEP DISTINCT — clarify** | The second carries phased-release and access-tier structure the first does not, and maps to a Role-owned artifact. The difference is structural, not just destination. |
| 8 | insurance gap analysis / insurance programme analysis | **MERGE** | Survivor `skill.insurance_programme_analysis`. Gap analysis is a step inside programme analysis, both were single-consumer at the same Role, and both were added in the same Wave 1 remediation. |
| 9 | ESG screening / environmental & social gap analysis | **KEEP DISTINCT — clarify** | Triage and categorisation versus assessment against a named safeguard standard; screening has a second consumer in IFI / DFI. |
| 10 | `security_control_design` vs `risk_control_design` | **KEEP DISTINCT — clarify** | Technical security controls in a system versus risk-management controls over a process. Different families, different methods; the collision is only in the names. IDs preserved — a rename would have cost tombstones and migrations to fix a readability problem that a scope note fixes. |
| 11 | `requirement_traceability` vs `traceability_matrix_design` | **MERGE** | Survivor `skill.requirement_traceability`. Decisive evidence: the survivor's own Skill Card already lists "matrix granularity design proportionate to criticality" among its Methods. The two were one capability under two IDs. Both consumers were Wave 1 Roles — see section 3.1. |
| 12 | source monitoring vs change detection | **KEEP DISTINCT — clarify** | Watching a defined set on a cadence versus analysing what differs between two versions. Roles that need both hold both. |
| 13 | privacy-impact / security-control support mappings | **KEEP DISTINCT — clarify** | Every mapping of `skill.privacy_impact_analysis`, `skill.threat_modelling` and `skill.security_control_validation` outside its owning Role already carries a support-only boundary note naming the Role that retains the conclusion. Verified across both waves; no change required. |
| 14 | **Specialisation IDs naming methods** (surfaced by reuse data) | **MERGE ×2** | `specialisation.affordability` → `skill.affordability_analysis`; `specialisation.tariff_modelling` → `skill.tariff_analysis`. Both were Skills wearing a Specialisation namespace: they name what a practitioner does, not a context the work sits in. Both had a single consumer that already held the surviving Skill. This is the strongest data-driven finding of Wave 3 and it motivated the classification semantics in section 6. |

### 3.1 Governed cross-wave correction (merge 11)

Both consumers of `skill.traceability_matrix_design` were Wave 1 Roles, so this merge required the one change Wave 3 makes to the reviewed Wave 1 baseline. It is recorded in the Wave 1 file itself and here:

- **Data & Database Architect** — the retired ID was OPTIONAL and the Role already held the survivor as REQUIRED_CORE. The optional entry was removed; no relationship changed.
- **Knowledge & Evidence Steward** — the retired ID was its only traceability route, so it migrated to `skill.requirement_traceability` at the same REQUIRED_FOR_CONTEXT relationship with its trigger unchanged. The Role Card basis is direct: it owns provenance and evidence-lineage integrity. This required adding the Role to the survivor's allowlist, done in the same change.

No other Wave 1 Role subject, relationship type or trigger was altered. Wave 1's own reuse statistics were corrected to match.

---

## 4. Single-role over-cardification

Recomputed from actual mappings across all 59 Roles.

| | Before Wave 3 | After Wave 3 |
|---|---:|---:|
| Capability IDs in active use | 265 | 263 |
| Used by exactly one Role | 95 | 92 |
| Percentage | 35.8% | 35.0% |

The movement is deliberately small. Wave 3 did not rewrite mappings to reduce a percentage; it resolved the cases where the evidence was strong. Three retirements removed single-consumer duplicates, three additions were made where the Role Card evidence justified them, and two of the three additions arrive with two consumers each.

**Classification of the 92 remaining single-role capabilities.** The dominant pattern is that a single-consumer capability is usually *correct*: it belongs to a Role that exists precisely because no one else does that work.

| Class | Count | Examples and reasoning |
|---|---:|---|
| VALID REUSABLE BUT CURRENTLY SINGLE-CONSUMER | ~46 | `skill.source_discovery`, `skill.fact_extraction`, `skill.business_case_structuring`, `skill.capex_estimation`, `skill.opex_estimation`, `skill.design_basis_definition`, `skill.critical_path_analysis`, `skill.project_scheduling`. Genuinely reusable techniques whose second consumer has not yet been mapped. No action. |
| ROLE-SPECIFIC TECHNIQUE — SHOULD NOT BE FIRST-CLASS SKILL | ~8 | Candidates rather than conclusions: `skill.knowledge_graph_design`, `skill.prompt_method_design` and `skill.ai_guardrail_design` are all single-consumer inside AI / Knowledge Systems and may be one capability; `skill.sanctions_screening` sits very close to `skill.counterparty_screening`. **Deliberately not merged in Wave 3** — each would need its own Role-boundary review and the evidence is not yet decisive. Flagged for a future governed decision. |
| PACK-INTERNAL CANDIDATE | ~6 | The five `skill.disclosure_*` and data-room capabilities cluster on one Role and would travel together as a disclosure Pack if one is ever created. No Pack exists, so no action now. |
| SPECIALISATION CANDIDATE | 0 | Wave 3 moved in the opposite direction: two Specialisations were found to be Skills, not the reverse. |
| NEEDS MORE CONSUMERS BEFORE CARDING | 17 (all Specialisations) | 17 of the 92 are single-consumer Specialisations — sector, sales and context entries used by exactly one Role. They are legitimate bounded contexts, but none should be carded until a second consumer or an assignment demands it. |

**Interpretation for the next audit.** 35% single-consumer is not by itself a defect at this stage: 48 of the 59 Roles were mapped only in Wave 2, so many capabilities have had exactly one opportunity to be reused. The figure is a watch metric, and the right time to act on it is when real assignments — not mappings — fail to reuse.

---

## 5. Pack versus direct activation

All duplicate direct-Skill-plus-Pack cases across both waves were re-examined.

| Role | Capability | Pack | Outcome |
|---|---|---|---|
| EU Programme Implementation | `skill.source_verification` | life_programme / cove | **Retained.** Direct REQUIRED_CORE is stricter than the Pack's requirement and applies outside any programme Pack. Activates once under the stricter obligation. |
| EU Programme Implementation | `skill.requirement_traceability` | life_programme / cove | **Retained.** Obligation traceability applies to any grant agreement, not only Pack-covered programmes. |
| EU Programme Implementation | `skill.source_monitoring` | life_programme / cove | **Retained.** Direct mapping is REQUIRED_FOR_CONTEXT; where the Pack is active its REQUIRED obligation is stricter and governs. |
| Funding & Bankability, Project Finance / Transaction, PPP / Concession | `skill.project_finance_ratio_analysis` | project_finance_metrics | **Retained.** Ratio analysis has meaning without the full metrics Pack. Watch item: if no assignment needs it Pack-free, the direct mappings should go. |
| Learning / VET Design | `skill.learning_outcome_design` | cove | **Retained.** Direct REQUIRED_CORE is stricter than the Pack's optional selection. |

No Pack-internal capability is redundantly exposed as a direct mandatory mapping, no Pack widens authority, and no relationship type or trigger has moved into a Pack Card. All five cases resolve to one activation under the stricter obligation, per `standard.skill.common_constraints` 6.1b.

---

## 6. Specialisation normalization

**Classification semantics added to the Universe.** A Specialisation bounds a *context*; it never names a *method*. The test: does the identifier answer *where or under what rules the work applies*, or *what the practitioner does*? An entry answering the second is a Skill in the wrong namespace.

**Reclassifications.** `specialisation.admin_console` and `specialisation.institutional_website` move from TECHNOLOGY to **OPERATING_CONTEXT**. Neither binds a platform or version; both describe a product kind and audience. Reserving TECHNOLOGY for entries that actually bind a platform keeps the class meaningful — `specialisation.relational_data_platform` is the genuine TECHNOLOGY case.

**Hidden Skills found and retired.** `specialisation.affordability` and `specialisation.tariff_modelling` failed the test above: both name methods. Merged into `skill.affordability_analysis` and `skill.tariff_analysis` (section 3, group 14).

**Audit for other defects.** All 34 remaining active Specialisations were checked against the four failure modes:

- *hidden Skill* — none beyond the two retired;
- *hidden Pack* — none. `specialisation.eu_grant_delivery` and `specialisation.infrastructure_project_preparation` are the broadest, but each bounds a delivery context rather than bundling capabilities;
- *hidden Role* — none. No Specialisation carries a conclusion, artifact or decision right;
- *too broad to be bounded context* — none disqualifying. `specialisation.multi_partner_programme_delivery` and `specialisation.public_sector_strategy` are broad but name real operating contexts.

Six classes are exercised by direct Wave 2 mappings after the group-14 merges retired the two METRIC-named entries: SECTOR, JURISDICTION, INSTITUTION, PROGRAMME, TECHNOLOGY and OPERATING_CONTEXT. METRIC remains a valid and used class, exercised by `specialisation.dscr`, `specialisation.llcr` and `specialisation.plcr` as components of `skill_pack.project_finance_metrics` rather than through a direct mapping — a distinction worth stating, since a class can be live in the registry without appearing in a direct-mapping table.

---

## 7. Selective carding — 2 of a maximum 3

Two cards created, both PROPOSED, both under the section 7 criteria.

**`specialisation.bess` — `skills/specialisations/sector/bess.md`.** The `Type: SPECIALISATION` template path had no instance, so the safe-Specialisation-representation decision from the Wave 1 remediation was untested architecture. BESS is the right exemplar: SECTOR is the most-used class, and the card has four mapped consumers across Wave 1 and Wave 2. It demonstrates that a Specialisation narrows applicability while adding no capability and no authority, and it carries the reclassification warning that catches drift into method description.

**`skill.negotiation_preparation` — `skills/strategy-analysis/negotiation-preparation.md`.** A newly added Skill whose authority boundary cannot safely be left implicit. A capability named "negotiation", mapped to four Roles none of which may commit the organisation, is exactly the entry that drifts into implied mandate. The card states that preparation confers no mandate to negotiate, concede or commit; names the human decision right gating each consuming Role's commitment; and states that no proficiency level converts preparation into mandate.

**No third card.** `skill.variance_analysis` and `skill.defect_management` have boundaries adequately expressed by their Universe entries and mapping-level support-only notes. Creating cards for them would have been generation, not normalization.

---

## 8. Compatibility and authority validation

Five paths, run across Wave 1 and Wave 2 against every existing card.

| Path | Direction | Result |
|---|---|---|
| direct Role → Skill | forward | **0 conflicts** |
| direct Role → Specialisation (carded) | forward | **0 conflicts** — first time this path has been testable, now that a Specialisation card exists |
| direct Role → Skill Pack | forward | **0 conflicts** |
| transitive Pack → component Skill | forward | **0 conflicts** |
| allowlist entry → mapping basis | **reverse** | **0 orphans** |

Coverage honesty: 235 Skills, 16 Packs and 31 Pack components have no card and are **NOT YET VALIDATABLE**, not passes. Zero conflicts means zero among what is checkable.

**Authority boundaries.** Every normalization decision was tested against the nine prohibitions. No merge collapsed two authority boundaries: merges 6, 8 and 11 joined capabilities owned by the same Role at the same authority level, and merges in group 14 replaced a Specialisation with a Skill already held by the same consumer. No Role scope widened, no professional conclusion transferred, no artifact ownership created, no review identity created, no human decision authority created, no gate bypassed, no support work converted to ownership.

**Preserved decisions, re-verified:** Security Engineer remains excluded from `skill.quality_attribute_analysis` and `skill_pack.supabase`; `skill.lifecycle_cost_analysis` remains support-only to Technical / Feasibility Lead with its card untouched; the Project Development Lead bid/proposal removal stands with corrected prose.

---

## 9. Statistics after Wave 3

| | Before | After |
|---|---:|---:|
| Universe Skills declared | 205 | 205 |
| Universe Specialisations declared | 43 | 41 |
| Universe Packs declared | 21 | 21 |
| Wave 2 active mapping entries | 673 | 676 |
| REQUIRED_CORE / RFC / OPTIONAL / ALTERNATIVE / PROHIBITED | 187 / 228 / 192 / 56 / 10 | 188 / 230 / 192 / 56 / 10 |
| Capability IDs in active use (both waves) | 265 | 263 |
| Single-role capabilities | 95 (35.8%) | 92 (35.0%) |
| Cards | 10 | 12 |

Universe Skills stayed at 205 because three additions offset three retirements; Specialisations fell by two through the group-14 merges.

---

## 10. Remaining non-blocking notes

1. **Card coverage remains the dominant limitation.** 12 cards against 267 declared capabilities. Every "zero conflicts" result is bounded by that.
2. **Eight single-consumer capabilities flagged but not merged** — the AI / Knowledge Systems cluster and `skill.sanctions_screening` versus `skill.counterparty_screening`. Evidence is suggestive, not decisive; each needs a Role-boundary review.
3. **`skill.governance_structure_design` deferred**, not dismissed. Re-open when a second consumer appears.
4. **`specialisation.eu_accession_context` proposed and not activated.** Wave 3's only unactivated proposal.
5. **Disclosure capability cluster** would travel together as a Pack if one is created.
6. **35% single-role use** is a watch metric, not yet a defect; 48 of 59 Roles have had one mapping opportunity.
7. **`skill.project_finance_ratio_analysis`** direct mappings retained across three Roles alongside the Pack; revisit if no Pack-free assignment appears.

---

## 11. Standing statement

Every decision above is PROPOSED. Nothing in the Skill Registry is APPROVED or CANONICAL. Mass generation of Skill, Specialisation or Skill Pack Cards remains prohibited and is not recommended by this record: the single-role distribution and the 235 uncarded Skills both argue for continued selective carding driven by real assignments.
