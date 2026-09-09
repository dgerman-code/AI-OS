# Master Decision Right Universe

Status: PROPOSED — Phase 7 candidate universe
Version: 0.1
Inherits: `standard.decision.common_constraints@0.1`

## Purpose

A bounded candidate universe of Decision Rights, built from evidence rather than invention.

**95 distinct `decision.<id>` references already exist** across the approved Phase 3 Role Cards and the approved Phase 5 and Phase 6 architecture — written over four phases by cards that could reference a gate and could not define one. Every one of the 95 is classified below. Nothing upstream is renamed, removed or normalized by this document: the references are approved and remain exactly as they are, and every consolidation here is a **proposal for a later governed pass**.

## Scale

- **9 families**
- **35 candidate Decision Rights** — 33 preserving an upstream ID, 2 filling an architecture gap with no upstream equivalent
- **62 upstream references classified into the other seven categories**
- **8 carded exemplars** (marked ✎)
- **95 upstream references, 100% accounted for**

The two architecture-gap entries are `decision.exceptional_progression` and `decision.cancellation_or_termination`. Both are gaps Phase 5 and Phase 6 pointed at without naming: both wrote *"a named external human `decision.<id>` may permit progression"* with no such ID existing anywhere, and Phase 5 defined cancellation criteria while explicitly leaving cancellation **authority** undefined.

They are not in the same condition. `decision.exceptional_progression` is bounded and carded. **`decision.cancellation_or_termination` is a placeholder marked `NOT CARDABLE UNTIL BOUNDED`**: it names a real architectural need, confers no authority, and is not an exercisable Right — see §9.

---

## 1. Workflow / Progression

| ID | Decision subject |
|---|---|
| `decision.stage_gate_progression` ✎ | Permit or refuse movement past a defined stage gate on the evidence presented. |
| `decision.exceptional_progression` ✎ NEW | Permit progression with a named unresolved item or unsatisfied review, without resolving it. |

## 2. Project / Investment / Readiness

| ID | Decision subject |
|---|---|
| `decision.project_definition_freeze` | Fix the project definition as the basis all downstream workstreams build on. |
| `decision.feasibility_acceptance` | Accept a feasibility position for reliance in downstream work. |
| `decision.technical_basis_freeze` | Fix the technical basis of design as the basis for cost and modelling. |
| `decision.cost_estimate_acceptance` | Accept a cost estimate for reliance in modelling and appraisal. |
| `decision.business_case_approval` | Approve a business case for the decision it was prepared to support. |
| `decision.investment_or_financing_use` | Authorise use of a prepared position for an investment or financing purpose. |

## 3. Programme / Grant / Submission

| ID | Decision subject |
|---|---|
| `decision.granting_authority_submission` ✎ | Submit a governed application or report to a granting authority. |
| `decision.grant_amendment_commitment` | Commit to a grant amendment request against an executed agreement. |
| `decision.grant_financial_claim` | Submit a financial claim under an executed grant agreement. |
| `decision.consortium_decision_confirmation` | Confirm a consortium-level decision on behalf of the participant. |

## 4. Financial / Commercial / Contractual Commitment

| ID | Decision subject |
|---|---|
| `decision.contract_commitment` ✎ | Bind the entity to a contractual obligation. |
| `decision.financial_close` | Declare financial close on a financing transaction. |
| `decision.financing_terms_acceptance` | Accept financing terms as binding on the entity. |
| `decision.budget_approval` | Approve a budget or budget structure as authorised expenditure. |
| `decision.supplier_award` | Award a contract to a selected supplier. |
| `decision.partner_commitment` | Commit the entity to a partnership or consortium participation. |

## 5. Legal / Compliance / Risk Acceptance

| ID | Decision subject |
|---|---|
| `decision.risk_acceptance` ✎ | Accept a declared residual risk within a bounded risk class. |
| `decision.security_risk_acceptance` | Accept a declared residual security risk within a bounded class. |
| `decision.lawful_basis_adoption` | Adopt a lawful basis for a personal-data processing activity. |
| `decision.formal_legal_opinion` | Issue, or authorise reliance on, a formal legal opinion. |
| `decision.state_aid_route_adoption` | Adopt a State Aid route for an intervention. |

## 6. Publication / Disclosure / Canonical Promotion

| ID | Decision subject |
|---|---|
| `decision.external_publication` ✎ | Release content externally under the entity's name. |
| `decision.disclosure_authorisation` | Authorise disclosure of controlled information to a named recipient class. |
| `decision.external_data_transmission` | Authorise transmission of data outside the entity. |
| `decision.canonical_knowledge_promotion` | Promote a knowledge artifact to CANONICAL status. |

## 7. Product / Software / Security / Release

| ID | Decision subject |
|---|---|
| `decision.production_release` ✎ | Release a change into production. |
| `decision.production_database_migration` | Execute a migration against production data. |
| `decision.production_infrastructure_change` | Change production infrastructure or environment configuration. |
| `decision.security_accreditation` | Accredit a system or change against a security standard. |
| `decision.architecture_adoption` | Adopt an architecture position as the basis for implementation. |

## 8. Emergency / Exception

| ID | Decision subject |
|---|---|
| `decision.emergency_production_change` ✎ | Permit a time-critical production change under declared emergency conditions. |
| `decision.defect_deferral` | Defer remediation of a known defect past a release gate. |

## 9. Cancellation / Termination / Reversal

| ID | Decision subject |
|---|---|
| `decision.cancellation_or_termination` NEW — **NOT CARDABLE UNTIL BOUNDED** | Placeholder for the cancellation/termination authority Phase 5 left undefined. **Confers no authority, is not an exercisable Right, and must not be referenced as one.** |

**This candidate is not a valid bounded Right and is not ready for carding.** As written it spans pre-commitment cancellation of an internal governed path and post-commitment termination of an obligation already given to a third party — a universal kill-switch bounded by nothing, eligible to whoever holds the weaker of the two authority bases.

| | Pre-commitment cancellation | Post-commitment termination |
|---|---|---|
| What it stops | An internal governed path — a Workflow, a stage, a preparation effort | An obligation already owed to a counterparty, funder, regulator or lender |
| Consequence class | Sunk effort; open items retained | Legal, contractual, regulatory, financial and reputational exposure |
| Likely eligibility | Sponsor or executive authority over the path | Signatory or governance-body authority, on the instrument's own terms |
| Evidence | State at cancellation, open items, reason | The above, plus the instrument, its termination provisions and the liabilities crystallised |

Holder eligibility and evidence differ materially, which is what makes this two authority patterns rather than one. **A future governed pass may split it** — plausibly into a governed-path cancellation Right and an external-commitment termination Right — and this document deliberately creates **no final ID for either**, because inventing one now would be exactly the silent normalization §12 exists to prevent. The upstream architectural need is preserved by recording it here; nothing is carded, and `architecture/decision-rights-registry-design.md` §13 states the same boundary.

---

## 10. Classification of the remaining 62 upstream references

Per the required taxonomy. **No reference is renamed, merged or removed by this classification** — each remains valid and in force in the Role Card or architecture that carries it. A classification is a finding about what the reference *is*, recorded for a later governed pass to act on.

### LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT — 34

Real authority, insufficiently bounded to card. Most are overlaps whose boundary has not been drawn, or selections whose status as authority rather than professional recommendation is unsettled.

| Upstream `decision.<id>` | Finding |
|---|---|
| `decision.commercial_commitment` | Overlaps contract_commitment; the boundary between a commercial and a contractual commitment is not yet drawn. |
| `decision.customer_commitment` | Commitment direction differs from supplier_award; may be one Right with a counterparty trigger. |
| `decision.purchase_commitment` | Threshold and delegation semantics undefined against budget_approval and supplier_award. |
| `decision.land_or_site_commitment` | A real bounded commitment, but its authority basis (property, legal entity) needs stating. |
| `decision.marketing_budget_commitment` | May be budget_approval at a lower threshold rather than its own Right. |
| `decision.insurance_placement` | Placement binds externally; boundary against insurance_programme_adoption unclear. |
| `decision.insurance_programme_adoption` | Adoption versus placement is an approval/commitment split not yet drawn. |
| `decision.es_action_plan_commitment` | Commits the entity to E&S actions; boundary against contract_commitment unclear where lender-required. |
| `decision.service_level_commitment` | External commitment with an operational subject; scope and holder basis need stating. |
| `decision.partnership_agreement_terms` | Terms acceptance versus partner_commitment is an unresolved two-step. |
| `decision.funding_strategy_adoption` | Adoption of a strategy may be an internal approval rather than a commitment. |
| `decision.risk_allocation_adoption` | Adopting an allocation may be an approval of a position rather than acceptance of risk. |
| `decision.tax_position_adoption` | Adopting a tax position has external consequence; authority basis needs stating. |
| `decision.operating_model_change` | Bounded subject unclear — model design approval or organisational change? |
| `decision.organisational_change` | Overlaps operating_model_change and workforce_communication. |
| `decision.ai_system_adoption` | A real adoption decision; prerequisite review dependencies not yet settled. |
| `decision.data_retention_policy_change` | Policy-setting rather than case decision; may belong to a policy family. |
| `decision.ifi_submission` | Almost certainly the same shape as granting_authority_submission with an institution trigger. |
| `decision.legal_filing_or_representation` | External binding act; boundary against formal_legal_opinion unclear. |
| `decision.legal_external_use` | Authorising external use of a legal analysis; overlaps formal_legal_opinion and external_publication. |
| `decision.partnership_composition` | Composition selection precedes partner_commitment; may be one Right with two stages. |
| `decision.financial_model_external_reliance` | Authorising external reliance is bounded and real; overlaps investment_or_financing_use. |
| `decision.lender_engagement` | Engagement may be a commitment or merely a Role act; not yet distinguishable. |
| `decision.financing_route_selection` | Selection may be a recommendation the Role owns rather than a separate authority. |
| `decision.procurement_route_selection` | Same question as financing_route_selection. |
| `decision.commercial_structure_selection` | Same question; may be an approval of a recommended structure. |
| `decision.technology_selection` | May be architecture_adoption at a component granularity. |
| `decision.delivery_model_selection` | May be a Role-owned recommendation adopted under a broader approval. |
| `decision.om_model_selection` | Same question. |
| `decision.counterparty_acceptance` | Real bounded acceptance; overlaps due_diligence_reliance and integrity escalation. |
| `decision.integrity_escalation` | Escalation obligation with a decision component; the two need separating. |
| `decision.breach_notification` | Regulatory act under a deadline; may be an obligation rather than a discretionary Right. |
| `decision.regulatory_reporting` | Same question — obligation versus authority. |
| `decision.workflow_scope_approval` | Scope approval sits between Workflow logic and a genuine approval authority. |

### DUPLICATE / OVERLAP — 1

One upstream reference duplicates the substance of a candidate already in this universe. **Neither identifier is merged, renamed or removed** — both remain accounted for, and consolidation is deferred to the phase that owns the subject.

| Upstream `decision.<id>` | Duplicates | Finding |
|---|---|---|
| `decision.canonical_knowledge_status_change` | `decision.canonical_knowledge_promotion` | Both are canonical-governance concepts over the same subject — the governed status of a knowledge artifact — differing only in whether the transition is framed as promotion or as status change. Distinguishing them requires the canonical state model itself, which **Phase 8 owns**. Carding or merging either now would presuppose the answer to open question 7, so both identifiers stay recorded, both stay uncarded, and **consolidation or normalization is deferred to Phase 8 canonical governance.** |

### REVIEW / QUALITY GATE IN DISGUISE — 10

A Phase 6 Review Profile already covers the substance. Carding these would create an authority that adds nothing to the review it duplicates.

| Upstream `decision.<id>` | Finding |
|---|---|
| `decision.design_acceptance` | `review.design_quality` covers the substance; acceptance adds no distinct authority. |
| `decision.dpia_acceptance` | `review.data_protection` covers it; the distinct act is lawful_basis_adoption. |
| `decision.economic_appraisal_acceptance` | `review.economic_appraisal` covers the substance. |
| `decision.es_assessment_acceptance` | `review.esg_safeguards` covers it; the distinct act is es_action_plan_commitment. |
| `decision.demand_basis_acceptance` | `review.factual_evidence` and the demand Role's own conclusion cover it. |
| `decision.learning_assessment_approval` | `review.learning_design_quality` covers the substance. |
| `decision.results_framework_approval` | `review.mel_methodology` covers the substance. |
| `decision.metric_definition_adoption` | A methodology choice the owning Role makes, checked by review, not decided by authority. |
| `decision.due_diligence_reliance` | Reliance follows from review satisfaction plus counterparty_acceptance. |
| `decision.external_mel_use` | Use follows external_publication or external_data_transmission plus review satisfaction. |

### ROLE RESPONSIBILITY IN DISGUISE — 8

An act the owning Role performs under its own Role Card, gated where external by a Right that already exists. Not a separate authority.

| Upstream `decision.<id>` | Finding |
|---|---|
| `decision.institutional_engagement` | Engagement is the Institutional Affairs Role's owned activity, not a gate. |
| `decision.workforce_communication` | Communication execution is the People & Organisation Role's owned surface. |
| `decision.joint_text_adoption` | Adoption of a joint text is a Role-owned negotiation output, gated by partner_commitment. |
| `decision.curriculum_adoption` | The Learning/VET Role owns curriculum design; external adoption is a client act. |
| `decision.external_commercial_communication` | Marketing Role's owned act, gated by external_publication where it is public. |
| `decision.institutional_position_release` | Editorial Role's owned act, gated by external_publication. |
| `decision.external_reporting_release` | Reporting Role's owned act, gated by external_publication or a submission Right. |
| `decision.formal_tax_opinion` | Parallel to formal_legal_opinion; a Role-issued professional instrument. |

### WORKFLOW PROGRESSION LOGIC IN DISGUISE — 4

Stage exit conditions or scope definitions that Phase 5 already governs. No distinct human authority is demonstrated.

| Upstream `decision.<id>` | Finding |
|---|---|
| `decision.product_scope_approval` | Scope acceptance is a Workflow stage exit plus review; distinct authority not demonstrated. |
| `decision.release_scope_approval` | Subsumed by production_release; scope is part of what is released. |
| `decision.portfolio_prioritisation` | A ranking recommendation the Portfolio Role owns; adoption is an executive act. |
| `decision.api_contract_publication` | A release act subsumed by production_release where the contract ships with a change. |

### RUNTIME PERMISSION / IAM IN DISGUISE — 2

Identity and permission management, or a regulated processing category. Neither is a governance decision class, and both are explicitly out of scope for this registry.

| Upstream `decision.<id>` | Finding |
|---|---|
| `decision.data_room_access_grant` | Access granting is identity and permission management, not a governance decision class. |
| `decision.automated_decision_making` | Names a regulated processing category, not an authority to decide something. |

### EXECUTIVE POLICY — OUT OF PHASE 7 SCOPE — 3

Standing policy-setting rather than a bounded case decision. `risk_appetite_setting` in particular sets the ceiling that `decision.risk_acceptance` operates under, which makes it a policy input to this registry rather than an entry in it.

| Upstream `decision.<id>` | Finding |
|---|---|
| `decision.strategic_direction` | Standing executive policy-setting, not a bounded case decision. |
| `decision.risk_appetite_setting` | Sets the ceiling risk_acceptance operates under; policy, not a case Right. |
| `decision.working_capital_policy` | Standing financial policy. |

---

## 11. Accounting

| Disposition | Count |
|---|---:|
| Standalone candidate Decision Right (upstream ID preserved) | 33 |
| Standalone candidate filling an architecture gap (no upstream ID) | 2 |
| **Total candidate Decision Rights** | **35** |
| Classified into the seven non-candidate categories | 62 |
| **Total upstream `decision.<id>` references** | **95** |

The 62 classified references, by category:

| Category | Count |
|---|---:|
| LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT | 34 |
| REVIEW / QUALITY GATE IN DISGUISE | 10 |
| ROLE RESPONSIBILITY IN DISGUISE | 8 |
| WORKFLOW PROGRESSION LOGIC IN DISGUISE | 4 |
| RUNTIME PERMISSION / IAM IN DISGUISE | 2 |
| EXECUTIVE POLICY — OUT OF PHASE 7 SCOPE | 3 |
| DUPLICATE / OVERLAP | 1 |
| **Total** | **62** |

Of the 35 candidates, **34 are bounded enough to be carded by a governed pass** and one — `decision.cancellation_or_termination` — is **not cardable until bounded**. Carding readiness and candidacy are different things, and the count reflects that.

Every one of the 45 `decision.<id>` references load-bearing in the approved Phase 5 and Phase 6 cards resolves either to a standalone candidate here or to a classified reference whose gate remains valid. **No Phase 5 or Phase 6 card requires amendment and none was amended.**

## 12. Naming normalizations proposed, not applied

The Phase 7 prompt described four exemplars using wording that is not a registry identifier. Upstream IDs are **preserved**, and the divergence is recorded rather than resolved by silent renaming. **None of the requested wordings is an alias**: no second `decision.<id>` exists for any of these Rights, and the plain-language column below is description, not reference.

| Requested in plain words | Actual registry ID | Disposition |
|---|---|---|
| project readiness progression | **`decision.stage_gate_progression`** | The upstream ID is used in `workflow.project_development_readiness` S7 and in the Portfolio Role Card. Renaming would break two approved artifacts to gain nothing. |
| grant submission | **`decision.granting_authority_submission`** | Used in `workflow.eu_grant_application_development` S6 and three Role Cards. The longer name is also the more accurate one — it names the recipient, which is what makes the act a transmitting one. |
| contractual commitment | **`decision.contract_commitment`** | Used across several Role Cards. Purely orthographic difference. |
| exceptional progression | **`decision.exceptional_progression`** — created as new | No upstream equivalent exists. This is a genuine architecture gap, not a rename. |

## 13. Carding discipline

**8 of 35 are carded** as exemplars. The other 27 are one-line candidates and are explicitly **not** validated — and one of those 27, `decision.cancellation_or_termination`, is **not cardable at all until it is bounded and probably split**. The 62 classified references must not be carded until their classification is acted on by a governed pass, and the two canonical-governance identifiers are held for Phase 8 in either direction.

Card generation for the remaining candidates follows the same selective, assignment-driven discipline Phases 4, 5 and 6 adopted. Mass generation is not authorised by this document.

## 14. Status

Every entry is `PROPOSED`. Inclusion here confers authority on no one.
