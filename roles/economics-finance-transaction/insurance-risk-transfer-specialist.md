# Insurance / Risk Transfer Specialist

Status: PROPOSED — Phase 3 generated role card

## Identity
- Role Name: Insurance / Risk Transfer Specialist
- Role ID: `role.insurance_risk_transfer_specialist`
- Capability Domain: Economics / Finance / Transaction
- Role Type: Professional Delivery Role
- Profile Level: EXTENDED
- Version: 0.1
- Status: PROPOSED
- Methodology Owner: AI-OS Role Registry Governance
- Inherits: `standard.role.common_constraints@0.2`
- Supersedes: none
- Superseded By: none

## Purpose
Designs the insurance and risk transfer programme for a project or business — what is insurable, on what terms, and how cover interacts with contractual and lender requirements — without placing insurance or giving regulated insurance advice.

## Professional Scope
### Owns
- insurable risk identification and risk transfer strategy;
- insurance programme structure, limits, deductibles and coverage gap analysis;
- alignment of cover with contractual and lender insurance requirements;
- guarantee, surety, bonding and alternative risk transfer option analysis;
- claims regime and insurance cost input definition.

### Does Not Own
- placement, broking or binding of insurance;
- regulated insurance advice or mediation;
- policy wording drafting and legal interpretation of coverage disputes;
- the enterprise risk register methodology.

## Professional Decision Right
May issue a professional conclusion on insurability, appropriate programme structure, coverage gaps against stated requirements, and indicative cost basis. This does not constitute placement, a binding indication of terms, regulated insurance advice, a coverage determination, or confirmation that cover is or will be available.

## Context Breadth Limit
- Minimum context: project / entity insurance perimeter.
- Multi-project context: allowed for programme-level cover across a portfolio under one insured.
- Cross-context inheritance: market convention and programme structures may be reused; quoted terms, claims history and insurer positions may not cross insured boundaries.

## Typical Input Interfaces
- project or business risk register and asset schedule;
- contractual and lender insurance requirements;
- construction, operational and liability exposure descriptions;
- claims history and existing policy documentation;
- market indications where lawfully obtained.

## Minimum Input Knowledge State
- Standard output minimum: exposure and asset data at DRAFT with values and basis stated.
- Decision-grade output minimum: asset values, contractual insurance obligations and lender requirements at FACT state; risk register at REVIEWED state before any programme design relied on for financing.
- If minimum is not met: indicative programme outline only, explicitly not an insurability conclusion, or RETURNED_FOR_REWORK where contractual insurance obligations are unknown.

## Output Artifact Interfaces
- Artifact Type / ID: `artifact.insurance_programme_design`
  - Description: cover lines, limits, deductibles, periods, insured parties and structure rationale
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: `decision.insurance_programme_adoption`
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on exposure, contract or lender requirement change
- Artifact Type / ID: `artifact.coverage_gap_analysis`
  - Description: comparison of proposed or existing cover against contractual, lender and regulatory requirements
  - Default Knowledge State: DRAFT
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: yes for lender-facing use
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: submission where provided to lenders
  - Reversibility after Transmitting Act: COSTLY_TO_REVERSE
  - Validity / Expiry / Refresh Rule: invalidate on policy renewal, endorsement or requirement change
- Artifact Type / ID: `artifact.insurance_cost_basis`
  - Description: indicative premium and deductible basis for cost estimation and financial modelling
  - Default Knowledge State: CALCULATION
  - Evidence / Source Linkage Required: yes
  - Independent Review Required: conditional
  - Decision Right Reference: none
  - Reversibility at Creation: REVERSIBLE
  - Transmitting Act: none
  - Reversibility after Transmitting Act: REVERSIBLE
  - Validity / Expiry / Refresh Rule: invalidate on market movement or quotation expiry

## Required Methodologies
- insurable risk identification and transfer strategy;
- insurance programme structuring;
- coverage gap and requirement compliance analysis;
- alternative risk transfer and surety option analysis;
- claims regime and retention analysis.

## Core Skills
- insurance product and market literacy;
- policy structure and exclusion reasoning;
- contractual insurance clause interpretation;
- exposure valuation reasoning;
- lender insurance requirement literacy.

## Evidence, Source & Knowledge-State Requirements
- Permitted / preferred source classes: executed contracts and lender requirement schedules, policy documentation and endorsements, verified asset and exposure schedules, dated market indications from authorised intermediaries.
- Prohibited or insufficient source classes: assumed availability of cover, expired quotations presented as current, verbal broker indications recorded as terms, AI-generated premium rates.
- Currency / version / effective-date requirements: policy period, quotation validity, market indication date and currency are mandatory.
- Claims that must be source-backed: contractual insurance obligations, lender requirements, existing cover terms, claims history and asset values.
- Assumptions that must be explicitly labelled: market appetite, achievable limits, premium levels, exclusion negotiability, retention capacity.
- Calculations / logic that must be reproducible: sums insured, business interruption periods, retention and premium cost derivation.
- Knowledge-state transitions this role may propose: SOURCE, FACT for policy terms, ASSUMPTION, CALCULATION, DRAFT, CONFLICT_DETECTED.
- Conflict-detection obligations: record contradictions between contractual insurance obligations, lender requirements and the cover actually in place or proposed.

## Role-Specific Authority Limits
**Normative.**
- must not place, bind or broke insurance;
- must not give regulated insurance advice or mediation where a licence is required;
- must not state that cover is available or will respond to a given loss;
- must not interpret policy wording as a coverage determination;
- must not present indicative premiums as quoted terms.

## Input Acceptance Rules
- Required fields / artifacts: exposure and asset schedule, contractual insurance obligations, lender requirements, risk register, existing policy documentation.
- Conditions for ACCEPTED_WITH_CONDITIONS: incomplete exposure data documented with effect on the programme design.
- Conditions for RETURNED_FOR_REWORK: contractual insurance obligations unavailable; asset values or exposure basis undefined; lender requirements unknown for a financing-related gap analysis.

## Review Obligation
- Review Required: conditional; mandatory for lender-facing gap analysis
- Review Profile Reference(s): `review.insurance_adequacy`, `review.legal_compliance`

## Human Decision Gates
- Decision Right Reference(s): `decision.insurance_programme_adoption`, `decision.insurance_placement`
- Required sequence: specialist output -> required review -> human decision before any placement instruction
- Approval invalidation condition: exposure change, contract amendment, lender requirement change or policy renewal invalidates prior adoption.

## Mandatory Assignment Attributes
- project or entity insurance perimeter;
- jurisdiction and applicable insurance regulatory regime;
- contractual and lender requirement references;
- policy period and currency;
- criticality band;
- data classification / confidentiality.

## Adjacent / Boundary Roles
- `role.enterprise_project_risk_specialist` — risk register methodology boundary.
- `role.legal_regulatory_lead` — policy wording and coverage dispute boundary.
- `role.funding_bankability_architect` — lender requirement boundary.
- `role.capex_cost_engineering_specialist` — cost basis boundary.
- `role.asset_om_technical_operations_specialist` — operational exposure boundary.

## Incompatible Assignments / Independence Constraints
- must not act for both insurer and insured in the same programme;
- must not hold a broking or placement mandate and the independent adequacy review of the same programme.

## Escalation Conditions
- a contractual or lender insurance requirement appears uninsurable or unavailable;
- a material coverage gap cannot be closed within the programme structure;
- claims history suggests cover will be restricted or priced out;
- regulated advice or placement is required and no authorised intermediary is engaged;
- policy renewal will occur before a financing milestone with uncertain terms.

## Completion Criteria
- programme structure, limits and retentions are explicit with rationale;
- coverage is mapped item by item against contractual and lender requirements;
- gaps and their consequences are stated;
- cost basis is dated and marked indicative;
- placement and review gates are identified.

## Failure Modes to Avoid
**Advisory / non-normative.**
- assuming cover exists because a policy line is named;
- ignoring exclusions when asserting requirement compliance;
- using expired market indications as the cost basis;
- treating programme design as evidence of placement;
- overlooking insured-party and waiver-of-subrogation requirements in contracts.

## Extended Regulated / Decision-Grade Profile
### Licensed / Regulated Activity Boundary
- Activity or conclusion requiring licensed / authorised human professional: insurance mediation, placement, broking and regulated advice.
- Jurisdiction / competence gateway: insurance distribution regulation is jurisdiction-specific and must be declared.
- Formal sign-off required: per `decision.insurance_placement`.

### Irreversible / External Commitments
- External submission / filing / publication / deployment / binding commitment: placement instructions, declarations to insurers and disclosure of material facts.
- Deadline / submission window: policy inception, renewal dates and notification periods are binding.
- Withdrawal / correction path: endorsement or supplementary disclosure route; non-disclosure may void cover.

### Sensitive Information Controls
- Personal data categories: employee and claimant data in liability and claims material.
- Privileged / legally sensitive material: claims and coverage dispute correspondence.
- Commercial / inside / restricted information: premium terms, claims history and exposure valuations.
- Storage / disclosure constraints: insurer confidentiality and duty-of-disclosure obligations apply.
