# Codex Prompt — Phase 4 Wave 2 Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected HEAD: `5248888b42a11a1710d5df8e6c9dbc0edfee4e04`

Act as an independent senior architecture auditor.

Audit Wave 2 Role-to-Skill Mapping after completion of all 48 remaining approved Roles.

This is verification-only.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not create Skill / Specialisation / Skill Pack Cards.
Do not introduce implementation, model/runtime binding, orchestration, database schema, or agent-framework design.

## Read first

1. `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`
2. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
3. `architecture/skill-registry-design.md`
4. `architecture/role-to-skill-mapping-rules.md`
5. `skills/master-skill-universe.md`
6. `skills/_standards/common-skill-constraints.md`
7. all 10 exemplar Skill / Skill Pack Cards
8. every approved Phase 3 Role Card referenced by Wave 2
9. `reviews/phase-3-final-approval.md`
10. `architecture/project-criticality-policy.md`

## Audit goals

### 1. Scope / role identity integrity
Verify:
- exactly 48 Wave 2 Role subjects;
- 48 unique exact Role IDs taken from actual approved Role Cards;
- zero Wave 1 roles remapped as Wave 2 subjects;
- Wave 1 + Wave 2 = exactly 59 approved Roles;
- no missing or duplicate Role identity.

Any identity mismatch is HIGH.

### 2. Active reference integrity
Independently extract all active mappings from Wave 2 and verify:
- every `skill.<id>` exists in Master Skill Universe;
- every `specialisation.<id>` exists;
- every `skill_pack.<id>` exists;
- zero deprecated IDs reintroduced;
- Candidate Universe Gaps do not appear as active mappings.

### 3. Relationship taxonomy discipline
Audit all active mappings for correct use of:
- REQUIRED_CORE
- REQUIRED_FOR_CONTEXT
- OPTIONAL
- ALTERNATIVE
- PROHIBITED_IN_CONTEXT

Check especially:
- REQUIRED_CORE is truly intrinsic and sparse;
- every REQUIRED_FOR_CONTEXT has a concrete trigger;
- every ALTERNATIVE set has a clear choice-set name, cardinality and choice condition;
- every PROHIBITED_IN_CONTEXT has a defensible Role-scope, independence, regulatory, confidentiality or methodology basis;
- no relationship class is being used as a proxy for authority.

Flag any REQUIRED_CORE inflation as MEDIUM/HIGH depending severity.

### 4. Role authority boundary audit
For each of the 48 Roles compare mapping against the actual Role Card:
- Purpose
- Owns
- Does Not Own
- Professional Decision Right
- Output Artifact Interfaces
- Authority Limits
- Review Obligation
- Human Decision Gates
- Independence Constraints

A mapping must not:
- widen Role scope;
- transfer another Role's professional conclusion;
- create artifact ownership;
- create review identity;
- create human decision authority;
- bypass review/decision gates;
- turn support work into ownership.

### 5. High-risk boundary pairs
Audit these explicitly and report each PASS / ISSUE:
- Portfolio / Programme Manager vs Project / Delivery Lead
- Strategy / Business Analyst vs Research / Market Intelligence
- Supply Chain & Procurement Operations vs Procurement / State Aid
- EU Policy & Institutional Affairs vs Legal / Regulatory and EU Grants
- Programme / Partnership Manager vs Consortium / Partner Coordination
- EU Programme Implementation vs EU Grants & Programmes
- Grant Financial Compliance vs FP&A / Accounting / Financial DD
- MEL vs Data / Business Analytics
- Project Development Lead vs Technical / Feasibility and Funding / Bankability
- Sector Technical Expert vs Technical / Feasibility
- CAPEX / Cost Engineering vs Financial Modelling
- Asset O&M vs Operations / Service Delivery
- Economic / CBA vs Financial Modelling / Funding & Bankability
- Funding & Bankability vs Project Finance / Transaction
- IFI / DFI Preparation vs institution Packs and transaction ownership
- PPP / Concession vs Legal / Procurement / Project Finance
- Tax vs Accounting / Financial DD
- Insurance / Risk Transfer vs Enterprise / Project Risk
- Procurement / State Aid vs Legal / Regulatory
- ESG / E&S vs Enterprise Risk
- Integrity / Due Diligence vs component screening Skills
- Data Protection / GDPR vs Security and Solution Architecture
- UX / UI & IA vs Product Manager / BA
- Institutional Communications / Editorial vs Marketing / Growth
- Full-Stack vs Solution Architect / Integration / Platform
- Integration / API vs Solution Architect
- Platform / DevOps vs Security / Data / Integration
- Database / Data Engineer vs Data & Database Architect
- Data / Business Analytics vs FP&A / MEL / Research
- AI / Knowledge Systems vs Knowledge & Evidence Steward / Data Architect
- Security Engineer vs quality-attribute support techniques
- QA / Test Automation vs independent Review Profiles
- Data Room & Disclosure Manager vs Knowledge & Evidence Steward

### 6. Specialisation model audit
Wave 2 claims 36 active Specialisations across six classes.

Verify:
- each exists in the Universe;
- each is truly bounded context rather than hidden authority;
- Specialisation never adds artifact ownership, review identity, or decision rights;
- class assignment is coherent;
- no Specialisation is actually a hidden first-class Role or Pack.

Report counts by class from actual data.

### 7. Skill Pack activation audit
Independently identify all active Skill Packs and verify:
- Pack usage is appropriate vs direct Skill mapping;
- programme/institution/technology/method/composite Packs are used consistently;
- duplicate effective activation is resolved once under the stricter obligation;
- no Pack stack accumulates authority;
- no permissive override of stricter requirements;
- no circular dependency introduced.

### 8. Transitive Pack Compatibility
Apply the active Transitive Pack Compatibility Rule.

For every Pack-consuming Role:
- validate every carded Required Skill;
- validate every carded selectable Optional Skill;
- follow declared Pack layering/dependencies;
- confirm all carded component allowlists include the consuming Role or a governed compatibility rule permits it;
- report uncarded components as NOT YET VALIDATABLE, not PASS.

Specifically re-check all allowlist edits made in commit `5248888b...` and confirm only compatibility/mapping-reference prose changed, not authority/boundary sections.

### 9. Security Engineer avoided contradiction
Independently review the decision to **not** map `skill.quality_attribute_analysis` or `skill_pack.supabase` to `role.security_engineer`.

Determine whether this is architecturally correct.

Check:
- Security Engineer still has sufficient capabilities from the Universe for its Role Card scope;
- it does not need `quality_attribute_analysis` to perform specialist security ownership;
- platform constraints can legitimately arrive through architecture/data/platform outputs rather than direct Pack activation;
- no hidden gap was created by removing the mapping.

Classify as:
- CORRECT
- NON-BLOCKING GAP
- CHANGE REQUIRED

### 10. Project criticality behavior
Verify criticality is used only to increase:
- evidence depth;
- specialist engagement;
- contextual capability/Pack activation;
- review/decision rigor.

It must not create new Role identity or globally inflate REQUIRED_CORE.

### 11. PROHIBITED_IN_CONTEXT audit
Wave 2 claims 10 prohibitions across 8 Roles.

Audit each individually.

Pay special attention to:
- Asset O&M / `skill.opex_estimation`
- Software QA / implementation prohibitions
- Data Room / knowledge-state prohibition
- Supply Chain vs procurement/state-aid prohibitions
- Database Engineer vs metric definition

Check whether each prohibition is:
- genuinely necessary;
- correctly contextualized;
- not better represented as absence from mapping or support-only boundary.

Flag overuse of PROHIBITED_IN_CONTEXT.

### 12. ALTERNATIVE audit
Audit all 10 ALTERNATIVE sets.

Check:
- real substitutability exists;
- cardinality is appropriate;
- a set does not hide multiple simultaneously required capabilities;
- the condition is operationally decidable.

### 13. Cross-wave consistency
Verify:
- Wave 1 file is unchanged;
- no semantic contradiction between Wave 1 and Wave 2 mappings for shared Skills/Packs;
- earlier remediations remain intact, especially Technical/Feasibility CAPEX/OPEX boundary and source/quality-attribute boundaries;
- cross-role differences in relationship class are justified by Role context, not inconsistent taxonomy.

### 14. Universe gaps
Review the 8 Candidate Universe Gaps:
- `skill.governance_structure_design`
- `skill.editorial_multilingual_coordination`
- `skill.negotiation_preparation`
- `skill.variance_analysis`
- `skill.commissioning_readiness_assessment`
- `skill.defect_management`
- `skill.qa_response_control`
- `skill.accession_alignment_analysis`

For each choose:
- ADD TO UNIVERSE LATER
- REPRESENT WITH EXISTING SKILL/PACK
- ROLE-SPECIFIC PROSE — DO NOT ADD
- NEEDS SPLIT / FURTHER REVIEW

Do not edit the Universe.

### 15. Micro-skill / overlap pressure
Independently assess the claimed 94 of 265 used IDs being single-role-use.

Recompute from actual Wave 1 + Wave 2 mappings.

Review at least these overlap groups:
- market sizing / segmentation / demand
- risk identification / risk register design
- action tracking / milestone management / deliverable planning
- process design / process mapping / SOP design
- source discovery / source comparison
- capacity planning / resource planning
- evidence indexing / data room index design
- insurance gap analysis / insurance programme analysis
- ESG screening / ESG gap analysis
- security_control_design vs risk_control_design naming clarity
- requirement_traceability vs traceability_matrix_design

For each recommend:
- KEEP DISTINCT
- MERGE
- RENAME / CLARIFY BOUNDARY
- DEFER TO WAVE 3 REVIEW

### 16. Scale / maintainability
Assess whether 677 Wave 2 mapping entries plus Wave 1 demonstrate that the current architecture can scale to all 59 Roles without becoming unmaintainable.

Evaluate:
- mapping density;
- one-off capability rate;
- Pack reuse;
- contextual trigger complexity;
- Specialisation usefulness;
- amount of repeated support-only prose;
- likelihood of drift between mapping and Skill Card allowlists.

### 17. Statistical integrity
Independently recompute:
- total Wave 2 active mappings;
- relationship distribution;
- unique Skills;
- unique Specialisations;
- unique Skill Packs;
- REQUIRED_CORE min/max/average per Role;
- number of ALTERNATIVE sets;
- number of PROHIBITED_IN_CONTEXT mappings;
- top 20 reused IDs across Wave 1 + Wave 2;
- single-role-use count and percentage across Wave 1 + Wave 2;
- duplicate Pack/direct activation count.

Report discrepancies with Claude's stated numbers.

### 18. Mass-generation readiness
Explicitly decide whether the system is ready for:
- more mapping work;
- selective card generation;
- controlled batch card generation;
- mass card generation.

Do not recommend mass generation merely because validation passes.

## Required output

Return exactly:

### A. FINAL VERDICT
Choose:
- PASS
- PASS WITH NON-BLOCKING NOTES
- PASS WITH CHANGES
- FAIL

### B. CRITICAL / HIGH FINDINGS
If none: NONE.

### C. SCOPE / ID INTEGRITY
48-role and 59-role coverage verdict.

### D. RELATIONSHIP TAXONOMY
REQUIRED_CORE / RFC / OPTIONAL / ALTERNATIVE / PROHIBITED assessment and any misuse.

### E. HIGH-RISK ROLE BOUNDARIES
List each required boundary pair with PASS / ISSUE and concise reason.

### F. SPECIALISATION AUDIT
Counts by class, boundary verdict, and defects if any.

### G. PACK / TRANSITIVE COMPATIBILITY
Pack count, carded component PASS/FAIL, uncarded NOT YET VALIDATABLE, cycles/overlap/authority issues.

### H. SECURITY ENGINEER DECISION
Choose:
- CORRECT
- NON-BLOCKING GAP
- CHANGE REQUIRED
Explain briefly.

### I. PROHIBITED_IN_CONTEXT AUDIT
List all prohibitions as KEEP / CHANGE / REMOVE with rationale.

### J. ALTERNATIVE SET AUDIT
List all sets as PASS / CHANGE REQUIRED.

### K. UNIVERSE GAPS
Decision for all 8 candidate gaps.

### L. MICRO-SKILL / OVERLAP FINDINGS
Recommendations for the named overlap groups and any additional material ones.

### M. STATISTICAL RECHECK
Actual recomputed numbers and discrepancies, if any.

### N. CROSS-WAVE CONSISTENCY
PASS / FAIL and any conflict.

### O. SCALE / MAINTAINABILITY
Assessment of mapping architecture at 59-role coverage.

### P. NEXT-STEP VERDICT
Choose exactly one:
- GO TO WAVE 3 CROSS-DOMAIN NORMALIZATION AUDIT
- GO AFTER LISTED CHANGES
- NO-GO

### Q. CARD-GENERATION VERDICT
Choose exactly one:
- NOT YET — KEEP SELECTIVE
- SAFE FOR CONTROLLED BATCH GENERATION
- SAFE FOR MASS GENERATION

Do not edit anything.