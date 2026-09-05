# Codex Prompt — Phase 4 Wave 1 Skill Registry Independent Audit

Status: WORKING REVIEW INSTRUCTION — NOT CANONICAL

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`

Act as an independent senior architecture auditor.

Your task is to review the Phase 4 Skill / Specialisation Registry foundation, Master Skill Universe v0.1, mapping rules, and Wave 1 exemplar role-to-skill mapping before any mass Skill Card generation.

This is audit-only.
Do not modify files.
Do not create commits or PRs.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not invent implementation architecture, database schema, agent framework, or model bindings.

## Read first

1. `architecture/skill-registry-design.md`
2. `architecture/role-to-skill-mapping-rules.md`
3. `skills/master-skill-universe.md`
4. `skills/_standards/common-skill-constraints.md`
5. `skills/_templates/skill-card-template.md`
6. `skills/_templates/skill-pack-template.md`
7. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
8. `roles/master-role-universe.md`
9. the approved Phase 3 Role Cards for the 11 Wave 1 exemplar roles
10. `reviews/phase-3-final-approval.md`

## Audit objectives

### 1. Registry type integrity
Verify the architecture consistently distinguishes:
- Role
- Skill
- Specialisation
- Skill Pack
- Review Profile
- Decision Right
- Model/runtime

Flag any Skill, Specialisation or Skill Pack that behaves like a hidden Role, Review Profile, Decision Right, workflow, or model binding.

### 2. Master Skill Universe quality
Audit the proposed universe for:
- duplicate or near-duplicate Skills;
- micro-skills that should be merged;
- broad catch-all Skills that should be split;
- context items incorrectly represented as Skills instead of Specialisations/Packs;
- capabilities that belong inside an existing Skill Pack instead of becoming standalone IDs;
- obvious missing reusable capability classes required by the 59 approved roles.

Do not optimize for the smallest possible count. Optimize for reusable capability clarity.

### 3. Explicit normalization review of Wave 1 candidates
Resolve each of these six candidates:
- `skill.eligibility_analysis`
- `skill.work_package_logic_design`
- `skill.budget_logic_analysis`
- `skill.submission_requirement_mapping`
- `skill.bid_proposal_management`
- `skill.security_constraint_allocation`

For each choose exactly one:
- KEEP AS SKILL
- MAP TO EXISTING SKILL
- MOVE INTO SKILL PACK
- RENAME / RECLASSIFY
- REMOVE

Provide exact target ID where applicable.

Pay special attention to whether:
- Bid / Proposal Management should remain a cross-family Skill Pack rather than a standalone Skill;
- EU call eligibility, budget logic, work-package logic and submission requirements belong inside EU programme packs;
- security constraint allocation is a reusable architecture Skill or better represented by existing quality-attribute / regulatory constraint skills.

### 4. Wave 1 mapping correctness
Audit all 11 exemplar roles.

For every mapping verify:
- referenced Role exists;
- referenced Skill/Specialisation/Pack exists or is explicitly identified as a normalization candidate;
- relationship type is appropriate;
- REQUIRED_FOR_CONTEXT has a sufficiently explicit trigger;
- no mapping widens Professional Scope;
- no mapping transfers another Role's artifact/conclusion ownership;
- no mapping bypasses review or human authority;
- no technology/programme/sector pack becomes a hidden professional Role.

### 5. REQUIRED_CORE discipline
Check whether REQUIRED_CORE is being used too broadly.

A Skill should be REQUIRED_CORE only where it is genuinely intrinsic to competent execution of the Role across most assignments.

Flag mappings that should be OPTIONAL or REQUIRED_FOR_CONTEXT instead.

### 6. Pack vs individual Skill duplication
Check whether a Role activates a Pack and also redundantly requires the same capabilities individually.

Flag unnecessary double activation.

Preserve individual mappings only where the Skill has independent reuse or meaning outside the Pack.

### 7. Cross-role reuse
Assess whether Wave 1 demonstrates real reuse rather than role-specific cloning.

Identify:
- highest-reuse skills;
- suspicious role-specific one-offs;
- candidate generic Skills that should replace domain-prefixed duplicates before mass generation.

### 8. Skill family structure
Assess the 15 Skill Families for:
- overlap;
- gaps;
- ambiguous ownership;
- whether family taxonomy is stable enough for Phase 4.

Do not turn Skill Families into Role domains or authority domains.

### 9. Specialisation semantics
Check whether Specialisations are used consistently for:
- sector;
- programme / institutional context;
- technology context;
- metric / modelling method;
- operating context.

Identify any item currently classed as Specialisation that should instead be Skill Pack or Skill, and vice versa.

### 10. Skill Pack semantics
Check whether each proposed Pack represents a coherent bundle with independent version/currency value.

Explicitly review:
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
- Project Finance Metrics
- Labour Market & Skills Intelligence
- Change Management / Adoption
- Technical Writing / Documentation
- Version Control / Document Configuration
- Bid / Proposal Management

Classify each as:
- KEEP AS PACK
- BETTER AS SPECIALISATION
- BETTER AS SKILL
- NEEDS SPLIT

### 11. Role boundary stress tests
Stress-test the mapping architecture against:

A. €50m+ BESS infrastructure / energy project
B. €7m municipal / IFI project with ESG and procurement complexity
C. Erasmus+ / CoVE programme implementation
D. LIFE project-preparation proposal
E. commercial e-commerce business
F. institutional website + Supabase/PostgreSQL/Vercel
G. policy / intelligence platform with evidence lineage

For each verify:
- Role set remains unchanged by Skill activation;
- contextual Packs activate cleanly;
- no hidden authority transfer;
- no duplication pressure creates unnecessary Roles;
- version/currency-sensitive Packs can be governed independently.

### 12. Scale test
Estimate whether the current taxonomy can scale from Wave 1 to all 59 Roles without exploding into hundreds of low-value micro-skills.

Give:
- PASS
- PASS WITH CHANGES
- FAIL

Explain what structural controls are necessary before mass generation.

### 13. Template and standards audit
Check the Skill Card and Skill Pack templates for missing fields or dangerous ambiguity.

At minimum assess:
- identity/version/status;
- family/type;
- definition/purpose;
- applicability;
- compatible Role IDs;
- relationship compatibility;
- prerequisites;
- methodology/reference links;
- evidence/source requirements;
- version/currency;
- authority limits;
- review/decision dependency boundary;
- model/runtime independence;
- supersedes/superseded-by;
- completion or competence criteria where appropriate.

Do not add credentialing or automatic scoring architecture unless strictly necessary to correct a boundary defect.

## Required output

Return exactly these sections:

### A. EXECUTIVE VERDICT
Choose:
- PASS
- PASS WITH CHANGES
- FAIL

State whether Phase 4 is ready to proceed to exemplar Skill Card / Skill Pack creation.

### B. CRITICAL / HIGH ISSUES
Only architecture or safety issues.
For each:
- severity
- file(s)
- issue
- why it matters
- recommended correction

If none: NONE.

### C. MASTER SKILL UNIVERSE NORMALIZATION
Provide:
- duplicate groups;
- merge candidates;
- split candidates;
- missing reusable capability classes;
- exact proposed ID changes.

### D. SIX WAVE 1 NORMALIZATION DECISIONS
For each of the six candidate IDs give exactly one disposition and rationale.

### E. SKILL PACK CLASSIFICATION
Classify every pack listed in objective 10 and explain only where a change is recommended.

### F. WAVE 1 ROLE MAPPING AUDIT
For each of the 11 exemplar roles:
- PASS / PASS WITH ISSUE / FAIL
- exact mapping issues if any.

### G. REQUIRED_CORE AUDIT
List mappings that should change from REQUIRED_CORE to another relationship type.
If none: NONE.

### H. CROSS-ROLE REUSE FINDINGS
Identify good reuse and problematic one-off patterns.

### I. FAMILY TAXONOMY REVIEW
PASS / PASS WITH CHANGES / FAIL and exact family changes if any.

### J. TEMPLATE / STANDARD FINDINGS
List exact required changes to:
- common skill constraints;
- skill card template;
- skill pack template.

If none: NONE.

### K. STRESS-TEST RESULTS
A–G with PASS / PASS WITH ISSUE / FAIL.

### L. SCALE VERDICT
PASS / PASS WITH CHANGES / FAIL.

### M. GO / NO-GO
Choose:
- GO TO EXEMPLAR SKILL CARDS
- GO AFTER LISTED CHANGES
- NO-GO

List the minimum required changes before the next Phase 4 step.

## Constraints

- Audit only.
- Do not edit repository files.
- Do not generate mass Skill Cards.
- Do not create new first-class Roles.
- Do not create Review Profile Registry or Decision Rights Register.
- Do not bind any Skill or Pack to a specific model.
- Preserve approved Phase 3 Role boundaries.
- Prefer reusable generic capabilities over role-prefixed duplicates.
- Prefer Skill Packs where versioned programme/institution/technology context is the true reusable unit.