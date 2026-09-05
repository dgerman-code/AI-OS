# Phase 4 — Skill / Specialisation Registry Architecture

Status: PROPOSED — Phase 4 foundation

## Purpose

Define the architecture for reusable skills, specialisations and skill packs that can be attached to approved professional roles and assignments without creating duplicate role identities or embedding model/runtime choices into professional capability definitions.

Phase 4 starts from the approved Phase 3 Role Registry. The Role Registry remains authoritative for first-class professional methodology, professional ownership boundaries and role identity.

## Core Rule

**ROLE != SKILL != SKILL PACK != MODEL**

- A **Role** owns a distinct professional methodology, recurring professional output or materially distinct authority boundary.
- A **Skill** is a reusable capability or technique that helps one or more roles perform work.
- A **Specialisation** is a bounded domain, sector, framework, technology, programme or method-specific extension to one or more roles.
- A **Skill Pack** is a curated, versioned bundle of skills, methods, references, controls and assignment requirements that can be activated together.
- A **Model** is only runtime and is not part of skill identity.

## 1. Skill

A Skill is the smallest reusable capability unit that is meaningful across assignments.

Examples:
- requirements elicitation;
- stakeholder mapping;
- tariff modelling;
- source verification;
- API contract design;
- project scheduling;
- cost-estimate reconciliation;
- accessibility testing;
- sensitivity analysis.

A Skill:
- does not own a first-class professional decision boundary;
- does not independently create a new role identity;
- may be shared across multiple roles;
- may have proficiency, evidence and applicability metadata;
- may be mandatory or optional for a specific role assignment.

## 2. Specialisation

A Specialisation narrows a role or set of roles to a bounded professional context.

Typical specialisation classes:
- sector: solar, BESS, water, waste, transport, industrial, health, real estate;
- programme / framework: Erasmus+, CoVE, LIFE, Horizon Europe;
- institution / financing framework: EIB, EBRD, World Bank, IFC, BGK, InvestEU, Ukraine Facility;
- technology: Supabase, PostgreSQL, Vercel;
- method / metric: DSCR, LLCR, PLCR, tariff modelling, affordability;
- operating context: municipal, regulated infrastructure, cross-border, public procurement.

A Specialisation must not become a first-class Role merely because it is commercially important, technically complex or project-specific.

## 3. Skill Pack

A Skill Pack is a versioned bundle used when one capability needs to travel as a coherent package.

A Skill Pack may contain:
- required skills;
- optional skills;
- methods / standards;
- controlled references;
- evidence requirements;
- assignment prerequisites;
- jurisdiction / programme / technology applicability;
- expiry / refresh rules;
- compatible Role IDs;
- incompatible or restricted contexts;
- links to Review Profile requirements where applicable;
- links to Decision Rights only as workflow/assignment dependencies, never as authority owned by the skill pack.

A Skill Pack must not:
- self-approve outputs;
- create a new human authority;
- override a Role Card;
- change canonical knowledge on its own;
- bind to a specific AI model as part of identity;
- silently widen a role's Professional Scope.

## 4. Classification Test — Role or Skill?

Treat a capability as a **Role** only if at least one approved Role Registry justification applies:
- distinct professional methodology;
- materially different authority boundary;
- recurring standalone professional artifact or decision-grade output;
- independent review separation that cannot be represented cleanly by a Review Profile.

Otherwise default to:
- Skill;
- Specialisation; or
- Skill Pack.

Complexity, prestige, price, sector importance and project size alone are not sufficient reasons to create a Role.

## 5. Skill Taxonomy

Phase 4 should use a layered taxonomy:

`SKILL FAMILY -> SKILL -> SPECIALISATION / PACK -> ROLE ASSIGNMENT`

Suggested Skill Families:
1. Research & Evidence
2. Strategy & Analysis
3. Stakeholder & Institutional
4. Project / Programme Delivery
5. Commercial & Market
6. Finance & Economics
7. Legal / Compliance / Procurement
8. ESG / Risk / Integrity
9. Technical / Engineering
10. Product / UX / Content
11. Software / Integration / Platform
12. Data / Analytics / AI
13. Documentation / Knowledge / Disclosure
14. Sales / Marketing / Customer
15. Operations / Supply Chain / People

These are capability families, not new professional Role domains.

## 6. Role-to-Skill Relationship

A Role Card may reference skills and skill packs, but the Role remains authoritative for:
- Professional Scope;
- Professional Decision Right;
- authority limits;
- required review;
- human decision gates;
- output artifact ownership.

A skill or pack may only refine *how* the role performs the assigned work, not *what authority* the role has.

Relationship types:
- REQUIRED_CORE
- REQUIRED_FOR_CONTEXT
- OPTIONAL
- ALTERNATIVE
- PROHIBITED_IN_CONTEXT

## 7. Assignment Model

Skills should be activated per assignment rather than permanently attached to a running agent.

Conceptually:

`ROLE PROFILE + ASSIGNMENT ATTRIBUTES + SKILL SET + SPECIALISATION PACKS + WORKFLOW CONTEXT`

The assignment determines which subset of the registry is active.

Examples:
- `role.financial_modelling_specialist` + `skill_pack.project_finance_metrics` + `specialisation.bess`;
- `role.eu_grants_programmes_specialist` + `skill_pack.life_programme`;
- `role.data_database_architect` + `skill_pack.postgresql` + `skill_pack.supabase`;
- `role.research_market_intelligence_analyst` + `skill_pack.labour_market_skills_intelligence`.

## 8. Versioning and Currency

Skills and packs must be versionable independently from roles.

Each versioned pack should eventually define:
- Pack ID;
- version;
- status;
- owner / governance owner;
- effective date;
- expiry or review date where relevant;
- applicable jurisdictions / frameworks / technology versions;
- controlled-source references;
- compatible Role IDs;
- supersedes / superseded-by links.

Fast-changing specialisations such as EU programmes, IFI procedures, regulatory frameworks and technology stacks require explicit currency controls.

## 9. Evidence and Methodology Boundary

A skill pack may point to methodology and controlled references, but:
- AI-generated content is not a controlled source;
- pack activation does not promote assumptions to facts;
- external standards and legal / programme rules require version/effective-date metadata;
- conflicting controlled sources must be escalated under the same knowledge-state principles as Role Cards.

## 10. Review and Decision Separation

Skill Registry must not absorb Review Profile Registry or Decision Rights Register.

A skill may declare that a particular type of use normally requires:
- a review class;
- an external validation step;
- a licensed professional;
- a human decision gate.

But the authoritative references remain:
- `review.<id>` in Review Profile Registry;
- `decision.<id>` in Decision Rights Register.

## 11. Initial Approved Skill / Specialisation Candidates from Phase 3

The following were explicitly kept outside the Role Registry and are Phase 4 starting candidates:
- Bid / Proposal Management
- Labour Market & Skills Intelligence
- Change Management / Adoption
- Technical Writing / Documentation
- Version Control / Document Configuration
- Erasmus+
- CoVE
- LIFE
- Horizon Europe
- EIB
- EBRD
- World Bank
- IFC
- BGK
- InvestEU
- Ukraine Facility
- Supabase
- PostgreSQL
- Vercel
- solar
- BESS
- water
- waste
- transport
- industrial
- health
- real estate
- DSCR
- LLCR
- PLCR
- tariff modelling
- affordability

This is a seed list, not the final registry.

## 12. Phase 4 Deliverables

Phase 4 should produce, in order:
1. Skill Registry principles and taxonomy;
2. Skill Card / Skill Pack standard;
3. initial Master Skill Universe;
4. Role-to-Skill mapping rules;
5. first versioned skill / specialisation packs;
6. cross-role reuse and duplication audit;
7. independent Phase 4 architecture review;
8. human approval.

No database schema, orchestration implementation or model router should be designed in this phase.

## Phase 4 Boundary

Phase 4 answers:
- what reusable capability exists;
- how it is classified;
- which roles may use it;
- what context makes it required;
- what controlled methodology / source package accompanies it.

Phase 4 does not answer:
- which AI model executes it;
- which agent framework runs it;
- which workflow activates it;
- who gives final human approval;
- how it is stored in a production database.