# Claude Code Prompt — Phase 3 Mass Role Card Generation

Status: WORKING EXECUTION INSTRUCTION — NOT CANONICAL

You are working inside the repository `dgerman-code/AI-OS` on branch `architecture/phase-3-role-registry`.

Your task is to generate the remaining missing Professional Delivery Role Cards for Phase 3, using the approved Master Role Universe and the current Role Card Standard.

Do not redesign the architecture.
Do not add new first-class roles.
Do not remove approved roles.
Do not merge roles.
Do not change role names or IDs unless an inconsistency with the approved Master Role Universe is purely clerical and you explicitly report it rather than silently changing architecture.
Do not design database schemas, orchestration frameworks, APIs or implementation code.
Do not mark any newly generated Role Card as APPROVED or CANONICAL.

## Governing files — read these first

1. `roles/master-role-universe.md`
2. `roles/_templates/role-card-template.md`
3. `roles/_standards/common-role-constraints.md`
4. `architecture/system-principles.md`
5. `architecture/context-hierarchy.md`
6. `architecture/registry-separation.md`
7. `architecture/project-criticality-policy.md`

Then inspect all existing role cards and use the strongest current examples as style / architecture references, especially:

- Project / Delivery Lead
- Knowledge & Evidence Steward
- Financial Modelling Specialist
- EU Grants & Programmes Specialist
- Legal & Regulatory Lead
- Data & Database Architect
- Product Manager / Business Analyst
- Monitoring, Evaluation & Learning Specialist
- Sales / Business Development Specialist

The template and standards override older wording in any example if they conflict.

## Core architectural rules

Preserve these distinctions strictly:

- ROLE != MODEL
- ROLE != AGENT INSTANCE
- Role != Skill / Specialisation
- Role != Review Profile
- Role != Human Decision Authority
- Delivery / Assurance / Authority remain separate
- Methodology is versioned outside the model
- Seniority is an assignment attribute, not a separate role
- Role Cards define professional identity, interfaces and limits; workflows bind producers to consumers
- Do not hard-code teams into Role Cards
- Do not put named upstream/downstream role lists into handoff sections
- Use role IDs only where an adjacent/boundary relationship is materially useful
- Human approval is expressed only through `decision.<id>` references
- Independent review is expressed only through `review.<id>` references
- AI output never becomes APPROVED or CANONICAL automatically

## Project scale / criticality rule

Apply `architecture/project-criticality-policy.md`.

- €50m+ total investment / enterprise / transaction value automatically enters Enhanced Decision-Grade Project Mode.
- Projects below €50m may also require Enhanced Decision-Grade treatment when complexity / risk triggers apply.
- Do not treat project value as the sole risk criterion.
- Scale and criticality change assignment depth, review obligations, minimum knowledge state, skill packs and decision gates; they do NOT create new role identities.

Role Cards must therefore remain usable for:
- routine / low-complexity work;
- smaller but complex / regulated / external-decision projects;
- €50m+ Enhanced Decision-Grade projects;
- major / systemic projects.

## Generation scope

1. Read `roles/master-role-universe.md` and build the authoritative list of approved professional roles.
2. Recursively inspect `roles/` and identify which approved roles already have current Role Cards.
3. Do NOT duplicate or overwrite existing current reference cards unless the template requires a small mechanical conformance fix. If you believe an existing reference card needs substantive architectural change, report it and leave it unchanged.
4. Generate one Markdown Role Card for each approved role that does not yet have a current card.
5. Place files in capability-domain folders using existing repository naming conventions.
6. If a required domain folder does not yet exist, create it using a concise kebab-case domain name consistent with the repository.

## Role Card conformance requirements

Every generated card must follow `roles/_templates/role-card-template.md` exactly and inherit the current version of `standard.role.common_constraints`.

Every card must include, as applicable:

- Identity
- Profile Level: CORE / EXTENDED
- version and status
- Methodology Owner
- versioned `Inherits`
- Purpose
- Professional Scope: Owns / Does Not Own
- Professional Decision Right
- Context Breadth Limit
- Typical Input Interfaces using artifact / information classes, not named teammates
- Minimum Input Knowledge State
- Output Artifact Interfaces
- Required Methodologies
- Core Skills
- Evidence, Source & Knowledge-State Requirements
- Role-Specific Authority Limits
- Input Acceptance Rules
- Review Obligation with `review.<id>` only
- Human Decision Gates with `decision.<id>` only
- Mandatory Assignment Attributes
- optional Adjacent / Boundary Roles using `role.<id>` only
- Incompatible Assignments / Independence Constraints
- Escalation Conditions
- Completion Criteria
- optional advisory Failure Modes to Avoid
- Extended Regulated / Decision-Grade Profile when `Profile Level: EXTENDED`

## Output artifact rules

For each material artifact, define:

- Artifact Type / ID
- Description
- Default Knowledge State
- Evidence / Source Linkage Required
- Independent Review Required
- Decision Right Reference, where applicable
- Reversibility at Creation
- Transmitting Act
- Reversibility after Transmitting Act
- Validity / Expiry / Refresh Rule

Do not confuse creation of a draft with the external act of sending, submitting, publishing, filing, deploying or making a binding commitment.

## Minimum input knowledge-state rules

Do not allow a decision-grade output to be constructed from materially unverified inputs merely because they exist.

Each card must state:
- minimum state for ordinary output;
- minimum state for decision-grade output;
- what happens if the minimum is not met.

Use `RETURNED_FOR_REWORK`, preliminary / non-decision-grade output, or an equivalent explicit controlled behaviour.

## Profile-level guidance

Use CORE where the role normally produces reversible, internal, non-regulated outputs.

Use EXTENDED where the role regularly handles one or more of:
- regulated / licensed domains;
- external submission or binding commitment;
- production changes;
- financing / investment decision-grade work;
- sensitive legal / personal / commercial / inside information;
- material public-sector / IFI / lender / regulator exposure;
- high-stakes irreversible or costly-to-reverse outcomes.

Do not make every role EXTENDED by default.

## Skill / specialisation discipline

Do not create separate roles for named programmes, institutions, technologies, sectors or metrics.

Treat items such as the following as skill packs / specialisations unless already approved as roles:
- EIB
- EBRD
- World Bank
- IFC
- InvestEU
- Ukraine Facility
- LIFE
- Horizon Europe
- Erasmus+
- CoVE
- Supabase
- PostgreSQL
- Vercel
- DSCR / LLCR / PLCR
- solar
- BESS
- water
- waste
- transport
- health
- real estate
- Bid / Proposal Management
- Labour Market & Skills Intelligence
- Change Management / Adoption
- Technical Writing / Documentation
- Version Control / Document Configuration

## High-stakes boundaries

Where relevant, make explicit what professional conclusion a role may issue and what it must not claim.

Examples:
- Financial Modelling may conclude the model is internally consistent and passes defined checks, but not that the project is bankable.
- Legal may produce draft legal / regulatory analysis, but not impersonate licensed counsel or issue a binding opinion where human authorisation is required.
- Technical roles may assess feasibility within assigned evidence and methodology, but not issue statutory certifications unless authorised professionals do so.
- Grant roles may prepare eligibility / compliance / application analysis, but not bind the applicant or submit externally without a decision right.
- Software / data roles may design or implement changes, but production deployment / destructive migration gates remain human-controlled where required.

## Naming and ID discipline

- Role names must match `roles/master-role-universe.md` exactly.
- Role IDs must be stable, concise and unique: `role.<snake_case_name>`.
- Review IDs use `review.<id>`.
- Decision IDs use `decision.<id>`.
- Artifact IDs use `artifact.<id>`.
- Do not invent human names or organisation-specific approvers in Role Cards.

## Quality checks before finishing

Perform a repository-wide conformance audit after generation.

Check at minimum:

1. Every approved role in the Master Role Universe has exactly one current Role Card.
2. No unapproved first-class Role Card was created.
3. No duplicate role IDs exist.
4. All cards declare Profile Level.
5. All cards declare Methodology Owner.
6. All cards inherit the current common standard version.
7. All cards have Professional Decision Right.
8. All cards have Context Breadth Limit.
9. All cards have Minimum Input Knowledge State.
10. All material output interfaces include creation/transmission reversibility fields.
11. No free-text human approver replaces a `decision.<id>` reference.
12. No review methodology is embedded where a `review.<id>` reference should be used.
13. No hard-coded named upstream/downstream teams appear in handoff logic.
14. Adjacent role references, if any, use `role.<id>`.
15. No card silently grants authority to promote material to APPROVED / CANONICAL.
16. No card creates Senior / Junior / Lead / Principal variants as separate role identities.
17. Existing reference cards remain intact unless changed only for mechanical conformance.

## Required final report

After making the file changes, produce a concise report with exactly these sections:

### A. GENERATED
- number of new Role Cards
- list of created file paths

### B. EXISTING / PRESERVED
- list of current reference cards left unchanged
- list of any cards mechanically conformed, with exact change type

### C. CONFORMANCE CHECK
Report PASS / FAIL for each of the 17 quality checks above.

### D. ISSUES REQUIRING HUMAN / ARCHITECTURE REVIEW
Only unresolved issues that cannot be safely resolved without changing approved architecture.

### E. TOTAL ROLE REGISTRY COVERAGE
State:
- approved roles in Master Role Universe
- current Role Cards present
- missing cards
- duplicate IDs
- unapproved cards

Do not mark Phase 3 complete.
Do not mark the generated cards APPROVED.
Stop after generation and conformance report so the repository can receive an independent Codex consistency audit.