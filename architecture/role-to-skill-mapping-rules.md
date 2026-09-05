# Phase 4 — Role-to-Skill Mapping Rules

Status: PROPOSED — Phase 4 working baseline

## Purpose

Define how approved Role Profiles may consume reusable Skills, Specialisations and Skill Packs without creating duplicate role identities, widening professional authority, or hard-coding workflow and runtime behavior.

This document is downstream from:
- the approved Phase 3 Role Registry;
- `architecture/skill-registry-design.md`;
- `skills/master-skill-universe.md`;
- `skills/_templates/skill-card-template.md`;
- `skills/_templates/skill-pack-template.md`.

## Core Principle

**A mapping grants capability applicability, not authority.**

A Role-to-Skill mapping may state that a Skill or Skill Pack is required, contextually required, optional, alternative or prohibited for an assignment.

A mapping must never:
- expand the Role's Professional Scope;
- create a new Professional Decision Right;
- transfer artifact ownership from another Role;
- bypass Review Profile requirements;
- bypass Human Decision Rights;
- create a new first-class Role;
- bind a Role to an AI model or runtime;
- imply that possession of a skill is evidence of competence, licensing or authority.

## 1. Mapping Entity Types

Mappings may connect an approved `role.<id>` to:
- `skill.<id>`;
- `specialisation.<id>`;
- `skill_pack.<id>`.

A mapping must always preserve the type boundary.

Examples:
- `role.financial_modelling_specialist` -> `skill.cash_flow_modelling`;
- `role.financial_modelling_specialist` -> `skill_pack.project_finance_metrics`;
- `role.sector_technical_expert` -> `specialisation.bess`;
- `role.eu_grants_programmes_specialist` -> `skill_pack.life_programme`.

## 2. Relationship Types

Only the following relationship classes are permitted.

### REQUIRED_CORE
The capability is normally intrinsic to competent execution of the Role across most assignments.

Use sparingly. It must not merely duplicate the Role Card's Core Skills wording without adding a reusable registry linkage.

### REQUIRED_FOR_CONTEXT
The capability becomes mandatory when a defined assignment condition is true.

Examples:
- BESS project -> `specialisation.bess`;
- LIFE call -> `skill_pack.life_programme`;
- lender-facing project-finance model -> `skill_pack.project_finance_metrics`;
- Supabase-backed product -> `skill_pack.supabase` for relevant architecture / engineering assignments.

A contextual mapping must define the trigger clearly enough that later workflow logic can resolve it without guessing.

### OPTIONAL
The capability may improve or extend execution but is not required for a valid assignment.

Optional must not be used as a catch-all for weakly related capabilities.

### ALTERNATIVE
One of several capabilities or packs may satisfy the same assignment need depending on context.

Alternative mappings must state the choice condition.

Example:
- database architecture may use PostgreSQL, another relational platform or a different approved pack depending on the selected technology context.

### PROHIBITED_IN_CONTEXT
The capability or pack must not be activated for a Role in a defined context because it creates conflict, unsafe authority mixing, incompatible methodology or data / licensing restrictions.

This relationship is exceptional and requires an explicit rationale.

## 3. Scope Boundary Test

Before creating a mapping, apply this test:

1. Does the Role already own the professional output or methodology surface in its approved Role Card?
2. Does the Skill merely refine how that owned work is performed?
3. Does the mapping avoid transferring responsibility from another approved Role?
4. Does the mapping leave Review and Human Decision authority untouched?

If #1 is no, the mapping is invalid unless the capability is merely supportive and the Role is not being represented as owner of the resulting professional conclusion.

## 4. Core Skill vs Registry Skill

Role Cards may contain prose Core Skills. Phase 4 registry mapping does not require every phrase in Core Skills to become a separate `skill.<id>`.

Create registry items only where they are reusable and independently meaningful.

Examples:
- `stakeholder synthesis` may map to broader `skill.stakeholder_mapping`, `skill.position_mapping` and `skill.consultation_design` depending on the Role;
- `system-level structural reasoning` does not automatically require its own Skill if adequately represented by `skill.solution_decomposition` and `skill.quality_attribute_analysis`;
- `professional judgement` must not become a generic registry Skill.

The Skill Registry is a reusable capability catalogue, not a tokenized decomposition of Role Card prose.

## 5. Mapping Direction

Canonical mapping direction is:

`ROLE -> SKILL / SPECIALISATION / SKILL_PACK`

Reverse discovery may later be derived:

`SKILL -> COMPATIBLE ROLES`

But reverse discovery must not become an independent source of authority.

The approved Role Card always wins where a conflict exists.

## 6. Context Triggers

A `REQUIRED_FOR_CONTEXT` mapping should reference one or more trigger classes.

Allowed conceptual trigger classes:
- sector;
- programme / call;
- institution / funder;
- jurisdiction;
- technology stack;
- project criticality;
- financing structure;
- public / private counterparty type;
- regulated activity;
- data classification;
- publication / external-use context;
- assignment artifact type.

Examples:

`role.eu_grants_programmes_specialist` + `skill_pack.life_programme`
- relationship: REQUIRED_FOR_CONTEXT
- trigger: programme = LIFE

`role.data_database_architect` + `skill_pack.postgresql`
- relationship: REQUIRED_FOR_CONTEXT
- trigger: selected relational platform = PostgreSQL

`role.financial_modelling_specialist` + `skill_pack.project_finance_metrics`
- relationship: REQUIRED_FOR_CONTEXT
- trigger: financing structure = project finance OR lender-facing debt model

`role.sector_technical_expert` + `specialisation.bess`
- relationship: REQUIRED_FOR_CONTEXT
- trigger: sector technology = BESS

## 7. Criticality Interaction

Project criticality changes mapping depth, not Role identity.

For Enhanced Decision-Grade or Major / Systemic work, mapping may require:
- more context-specific Skills / Packs;
- tighter currency controls;
- stronger evidence prerequisites;
- broader specialist coverage;
- additional review references defined elsewhere.

Do not create a `major_project_skill` or `large_project_role` merely because project size is high.

The project-criticality policy remains authoritative.

## 8. Skill Pack Precedence

A Skill Pack may include Skills and Specialisations that would otherwise be mapped individually.

Where a Pack is activated:
- do not duplicate the same capability as a separate mandatory mapping unless the individual mapping has independent meaning;
- Pack constraints apply in addition to Role constraints;
- Role constraints prevail if the Pack attempts to widen authority;
- Pack version and currency rules apply to the assignment.

Example:

If `skill_pack.life_programme` already includes programme eligibility interpretation, call-structure analysis and submission-calendar controls, do not also create separate REQUIRED_FOR_CONTEXT mappings for every micro-capability unless another role reuses them independently.

## 9. Multi-Role Reuse

A Skill should be mapped to multiple Roles where genuinely reusable.

Examples:
- `skill.source_verification` may apply to Research / Market Intelligence, EU Policy, Legal, Accounting / FDD, Knowledge & Evidence and others;
- `skill.stakeholder_mapping` may apply to Institutional Affairs, Programme / Partnership, Sales / BD and Project Development;
- `skill.sensitivity_analysis` may apply to Strategy, Financial Modelling, Commercial & Demand, Economic / CBA and Risk;
- `skill.requirement_traceability` may apply to Legal / Regulatory, Procurement / State Aid, Product / BA and Programme Implementation.

Reuse is desirable. Duplicate Skill IDs differentiated only by Role are not.

Bad:
- `skill.financial_modelling_source_verification`
- `skill.legal_source_verification`
- `skill.policy_source_verification`

Preferred:
- `skill.source_verification` with role-specific assignment context.

## 10. Role Boundary Collision Rules

A mapping is invalid if it causes one Role to appear to own another Role's professional conclusion.

Examples:

### Financial Modelling Specialist
May use:
- `skill.capex_modelling`;
- `skill.opex_modelling`;
- `skill.project_finance_ratio_analysis`.

Must not gain Technical / Feasibility ownership merely because it consumes technical assumptions.

### Project / Delivery Lead
May use:
- `skill.project_scheduling`;
- `skill.dependency_mapping`;
- `skill.multidisciplinary_integration`.

Must not gain Legal, Financial, Technical or ESG professional conclusion authority through skill mapping.

### Product Manager / Business Analyst
May use:
- `skill.requirements_elicitation`;
- `skill.process_mapping`;
- `skill.acceptance_criteria_design`.

Must not gain Solution Architecture or Security authority through technology packs.

### Knowledge & Evidence Steward
May use:
- `skill.source_verification`;
- `skill.evidence_mapping`;
- `skill.evidence_indexing`.

Must not become the substantive author or reviewer of every professional conclusion whose evidence it governs.

## 11. Review and Decision References

Mappings themselves do not own `review.<id>` or `decision.<id>`.

A Skill or Skill Pack may declare review / decision dependencies in its own card, but Role-to-Skill mappings should only indicate that the relevant Pack is active.

The consuming workflow later resolves:
- applicable Role Card obligations;
- active Pack constraints;
- Review Profile references;
- Human Decision Rights.

No mapping may suppress a required review because a Skill Pack was activated.

## 12. Proficiency

Proficiency is an assignment attribute, not a new Role or Skill identity.

Suggested future proficiency states:
- FOUNDATION
- WORKING
- ADVANCED
- EXPERT

Phase 4 does not yet define scoring, credentialing or automatic proficiency inference.

The system must not infer regulated professional authorisation from proficiency labels.

## 13. Currency and Version Matching

Where a mapped Skill Pack is version-sensitive, the assignment must resolve a current Pack version.

Examples:
- EU programme calls;
- IFI procedures;
- legal / regulatory frameworks;
- Supabase / PostgreSQL / Vercel platform behavior;
- financial-methodology packs when standards change.

A stale Pack must not silently satisfy `REQUIRED_FOR_CONTEXT`.

## 14. Mapping Record — Conceptual Minimum

A future mapping record should be able to express:
- Mapping ID;
- Role ID;
- Capability ID;
- Capability Type;
- Relationship Type;
- Context Trigger;
- Rationale;
- Minimum Proficiency if applicable;
- Effective Version / Pack Version rule;
- Status;
- Supersedes / Superseded By.

This is an architecture contract only, not a database schema.

## 15. Mapping Validation Rules

Every mapping must pass:

1. referenced Role ID exists in approved Role Registry;
2. referenced Skill / Specialisation / Pack exists in current Skill Registry baseline;
3. relationship type is one of the five allowed types;
4. REQUIRED_FOR_CONTEXT has an explicit trigger;
5. ALTERNATIVE has a choice condition;
6. PROHIBITED_IN_CONTEXT has a rationale;
7. mapping does not widen Role authority;
8. mapping does not create duplicate Role identity;
9. mapping does not bind a model/runtime;
10. mapping does not bypass Review or Decision Rights;
11. version-sensitive Pack has currency logic;
12. no duplicate mapping exists for same Role + Capability + trigger without a stated override.

## 16. Initial Mapping Strategy for 59 Roles

Do not attempt exhaustive Role-to-Skill mapping in one pass.

Use three waves:

### Wave 1 — Core exemplar mapping
Map 8–12 representative Roles spanning different domains.

Recommended exemplar Roles:
- `role.project_delivery_lead`
- `role.research_market_intelligence_analyst`
- `role.eu_grants_programmes_specialist`
- `role.technical_feasibility_lead`
- `role.financial_modelling_specialist`
- `role.legal_regulatory_lead`
- `role.product_manager_business_analyst`
- `role.solution_architect`
- `role.data_database_architect`
- `role.knowledge_evidence_steward`
- `role.sales_business_development_specialist`

### Wave 2 — Domain completion
Map remaining Roles by approved capability domain, checking for Skill reuse and duplicate creation.

### Wave 3 — Cross-domain audit
Audit high-frequency Skills, Pack activation, authority boundaries and contextual triggers across all 59 Roles.

## 17. Exemplar Stress Tests

Before mass mapping, test at least:

A. €50m+ BESS / infrastructure project
B. €7m municipal / IFI project with ESG and procurement triggers
C. Erasmus+ / CoVE programme implementation
D. LIFE project-preparation proposal
E. commercial e-commerce business
F. institutional website + Supabase/PostgreSQL
G. policy / intelligence platform with evidence lineage

For each test, verify:
- correct Roles remain unchanged;
- context activates the right Skills / Packs;
- no Skill Pack becomes a hidden Role;
- no authority boundary changes;
- Pack currency can be resolved;
- reuse occurs without duplicate skill creation.

## 18. Phase 4 Mapping Completion Criterion

Role-to-Skill mapping architecture is ready for approval when:
- all 59 approved Roles can be mapped without changing Role identity;
- all mappings use the controlled relationship types;
- no mapping widens authority;
- Skill reuse is demonstrable across domains;
- programme / institution / technology Packs activate by explicit context;
- no unresolved duplicate Skill families remain;
- independent review finds no hidden Role proliferation or authority leakage.

Until Phase 4 human approval, all mappings and taxonomy remain PROPOSED.