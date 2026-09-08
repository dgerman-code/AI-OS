# Master Review Profile Universe

Status: PROPOSED — Phase 6 candidate universe
Version: 0.1
Inherits: `standard.review.common_constraints@0.1`

## Purpose

A bounded candidate universe of reusable Review Profiles. This is a **candidate list for audit**, not an approved registry.

The universe is built from a specific evidence base rather than invented: **44 distinct `review.<id>` references already exist** across the approved Phase 3 Role Cards and the approved Phase 5 Workflow cards, 26 of them load-bearing in Phase 5. Every one of the 44 is accounted for below — either as a standalone candidate Profile, or in a consolidation or overlap group with a stated proposed disposition.

**Nothing upstream is changed by this document.** The Phase 3 and Phase 5 references are approved and remain exactly as they are; a proposed consolidation here is a proposal for a later governed pass, not an applied merge.

## Scale

- **9 families**
- **34 standalone candidate Review Profiles**
- **10 existing IDs held** in consolidation or overlap groups, not carded
- **6 carded exemplars** (marked ✎)
- **44 existing references, 100% accounted for**

Target range was 20–35 candidates; 34 sits at the top of it, which is a deliberate choice: the alternative was to force merges the evidence does not yet support, and §8 of the standard makes over-merging the more dangerous error than over-splitting.

---

## 1. Evidence / Factual Integrity

| ID | Purpose |
|---|---|
| `review.factual_evidence` | Verify that stated facts are traceable to verified sources and that assumptions are not presented as facts. |
| `review.evidence_integrity_provenance` ✎ | Verify provenance, version identity, chain of evidence and knowledge-state discipline across an evidence base. |
| `review.analytical_method` | Verify that the analytical method applied is appropriate to the question and correctly executed, independently of the domain conclusion. |

## 2. Project / Investment

| ID | Purpose |
|---|---|
| `review.project_readiness` | Verify that a readiness position is supported by the workstream evidence it claims. |
| `review.project_integration_coherence` ✎ | Verify that separately owned specialist positions are mutually consistent and that contradictions between them are surfaced rather than reconciled. |
| `review.engineering_technical` | Verify the technical basis, option comparison and design assumptions within the engineering domain. |
| `review.operational_feasibility` | Verify that a proposed configuration is operable and maintainable as designed. |

## 3. Finance / Economics

| ID | Purpose |
|---|---|
| `review.financial_model` ✎ | Verify model integrity, assumption traceability and calculation soundness before reliance. |
| `review.cost_estimate` | Verify estimate basis, method, contingency rationale and completeness against the defined scope. |
| `review.bankability` | Verify a bankability position against stated lender or investor requirements. |
| `review.economic_appraisal` | Verify economic appraisal methodology, comparator basis and sensitivity treatment. |
| `review.tax_analysis` | Verify tax position analysis and its stated authority basis. |

## 4. Legal / Compliance / Procurement

| ID | Purpose |
|---|---|
| `review.legal_compliance` ✎ | Verify that a legal or regulatory analysis is correctly grounded, current, and correctly bounded as analysis rather than opinion. |
| `review.procurement_state_aid` | Verify procurement route and State Aid analysis against the applicable regime. |
| `review.data_protection` | Verify data-protection analysis, lawful-basis reasoning and DPIA completeness. |
| `review.commercial_structure` | Verify commercial or contractual structure analysis, including risk-allocation coherence. |

## 5. ESG / Risk / Integrity

| ID | Purpose |
|---|---|
| `review.esg_safeguards` | Verify E&S assessment against the named safeguard standard and its categorisation basis. |
| `review.risk_quantification` | Verify risk quantification method, data basis and treatment of unquantifiable residual risk. |
| `review.integrity_due_diligence` | Verify integrity and sanctions screening scope, method and escalation handling. |
| `review.insurance_adequacy` | Verify insurance programme adequacy against contractual and lender requirements. |

## 6. Programme / Grant

| ID | Purpose |
|---|---|
| `review.eu_programme_compliance` ✎ | Verify a governed submission against the applicable programme rulebook at its bound version. |
| `review.mel_methodology` | Verify monitoring, evaluation and learning methodology and indicator design. |
| `review.learning_design_quality` | Verify curriculum, learning-outcome and assessment design quality. |

## 7. Product / Software / Data / Security

| ID | Purpose |
|---|---|
| `review.architecture` | Verify solution architecture decisions, quality-attribute reasoning and constraint handling. |
| `review.data_architecture` | Verify data model, migration design and data-quality treatment. |
| `review.security` ✎ | Verify threat model, control design and control validation, independently of the implementing Roles. |
| `review.code` | Verify implementation against the adopted design position and applicable standards. |
| `review.test_coverage` | Verify that test evidence covers the acceptance criteria it claims to cover. |
| `review.product_requirements_quality` | Verify requirement clarity, testability and traceability. |
| `review.accessibility` | Verify accessibility conformance of a user-facing surface against the applicable standard. |

## 8. Documentation / Publication / Disclosure

| ID | Purpose |
|---|---|
| `review.institutional_position` | Verify that published institutional content states the institution's position accurately and within mandate. |
| `review.commercial_claims` | Verify that external commercial claims are substantiated and correctly qualified. |

## 9. Cross-Workstream / Decision-Grade Assurance

| ID | Purpose |
|---|---|
| `review.strategic_analysis` | Verify strategic option framing, criteria design and comparability of options. |
| `review.portfolio_prioritisation_coherence` | Verify that a portfolio ranking follows its stated criteria and evidence. |

---

## 10. Consolidation proposals — 4 existing IDs

Each is an existing approved reference judged **too granular or duplicative** as a standalone Profile. **None is merged here.** These are proposals for a later governed pass, and every one of the four remains a valid reference in the Role Card or Workflow that carries it until such a pass runs.

| Existing ID | Proposed disposition | Reasoning |
|---|---|---|
| `review.grant_compliance` | Into `review.eu_programme_compliance`, with a post-award trigger | Same purpose — conformity to a programme rulebook at a bound version — applied at a different lifecycle stage. Stage is a trigger, not a review identity. |
| `review.ifi_appraisal_readiness` | Into `review.bankability`, with an institution-specific trigger | Institution specificity is Pack context under the approved Phase 4 model. Every IFI would otherwise generate its own Profile. |
| `review.ppp_structure` | Into `review.commercial_structure`, with a PPP trigger | PPP is a structure variant, not a distinct review purpose; the checks are risk allocation, payment mechanism and value-for-money coherence in both cases. |
| `review.financial_evidence` | Into `review.factual_evidence`, with a financial-evidence trigger | Both verify that stated figures trace to verified sources. The domain is the trigger; the review method is the same. |

## 11. Overlap groups — 6 existing IDs, unresolved

Recorded now so a later audit does not rediscover them. **None is resolved in Phase 6.**

1. **`review.design_quality` / `review.accessibility` / `review.product_requirements_quality`** — three checks on the same user-facing surface at different altitudes. Accessibility is plainly distinct (conformance to an external standard); design quality may be a method inside requirements quality, or may be its own assurance. `review.design_quality` is **held**, the other two are carded candidates.
2. **`review.sourcing_and_commitment` / `review.customer_commitment_exposure`** — both verify exposure created by a commitment, one supplier-side and one customer-side. Possibly one Profile with a direction trigger; possibly two, because the counterparty risk profile differs. Both **held**.
3. **`review.partnership_governance` / `review.commercial_structure`** — partnership governance design overlaps structure review where the partnership is contractual. `review.partnership_governance` is **held**; `review.commercial_structure` is a carded candidate.
4. **`review.organisational_change_impact`** — **held** pending a prior question: whether this is an independent review or a conclusion the People & Organisation Role owns outright. If the latter, it is not a Review Profile at all.
5. **`review.ai_system_evaluation`** — **held** pending whether it is a distinct Profile or a composition of `review.architecture`, `review.security` and `review.analytical_method` applied to an AI subject.
6. **`review.project_readiness` / `review.project_integration_coherence`** — both carded as candidates and one is a carded exemplar, but their boundary needs testing: readiness asks *is the evidence sufficient*, coherence asks *do the positions contradict each other*. Adjacent, and the exemplar states its own out-of-scope against the other.

## 12. Accounting for all 44 existing references

| Disposition | Count |
|---|---:|
| Standalone candidate Profile | 34 |
| Consolidation proposal (§10) | 4 |
| Held in an overlap group (§11) | 6 |
| **Total existing `review.<id>` references** | **44** |

All 26 `review.<id>` references load-bearing in the approved Phase 5 Workflow cards resolve to a **standalone candidate Profile**. No Phase 5 workflow depends on a held or consolidation-proposed ID, so no Phase 5 card needs amendment and none was amended.

## 13. Carding discipline

**6 of 34 are carded** as exemplars. The other 28 are one-line candidates and are explicitly **not** validated. The 10 held IDs must not be carded at all until their consolidation or overlap question is decided.

Card generation for the remaining 28 follows the same selective, assignment-driven discipline Phase 4 and Phase 5 adopted. Mass generation is not authorised by this document.

## 14. Status

Every entry is `PROPOSED`. Inclusion here confers no approval on any Review Profile.
