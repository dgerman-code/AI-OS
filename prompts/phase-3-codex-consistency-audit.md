# Codex Prompt — Phase 3 Independent Consistency Audit

Status: WORKING REVIEW INSTRUCTION — NOT CANONICAL

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-3-role-registry`

Act as an independent senior architecture auditor and repository consistency reviewer.

Your task is to audit the completed Phase 3 Role Registry after mass generation. Do not generate new Role Cards, do not redesign the architecture, do not approve or canonicalize Phase 3, and do not change any files unless explicitly instructed in a later turn.

## Read first

1. `roles/master-role-universe.md`
2. `roles/_templates/role-card-template.md`
3. `roles/_standards/common-role-constraints.md`
4. `architecture/system-principles.md`
5. `architecture/context-hierarchy.md`
6. `architecture/registry-separation.md`
7. `architecture/project-criticality-policy.md`
8. all current Role Cards recursively under `roles/`

## Audit objectives

Independently verify the registry at architecture level, not just syntax level.

### 1. Registry coverage and identity
- exactly 59 approved professional roles exist;
- each approved role has exactly one current Role Card;
- no unapproved first-class roles exist;
- Role Names match the Master Role Universe;
- Role IDs are unique, stable and conventionally named;
- identify any legacy ID that deviates from `role.<snake_case_role_name>` and assess whether it should remain for stability or be renamed now.

### 2. Role boundaries
Test every card for leakage across these boundaries:
- Role vs Skill / Specialisation;
- Role vs Review Profile;
- Role vs Human Decision Right;
- Role vs System Control;
- Delivery vs Assurance vs Authority;
- adjacent-role overlap that could create conflicting ownership.

Flag any role that behaves like a super-agent, duplicates another role materially, or claims conclusions beyond its professional methodology.

### 3. High-stakes decision boundaries
Stress-test relevant roles for:
- investment / financing;
- legal / regulatory;
- technical / engineering;
- ESG / E&S;
- tax / accounting;
- procurement / State Aid;
- data / security / production deployment;
- grants / public funding;
- external communications and publication.

Confirm that decision-grade conclusions, external submission, binding commitments and production changes remain gated by `decision.<id>` and/or independent review where required.

### 4. Knowledge-state and evidence integrity
Check that cards consistently distinguish SOURCE, FACT, ASSUMPTION, CALCULATION, DRAFT, REVIEWED, APPROVED, CANONICAL, SUPERSEDED, CONFLICT_DETECTED and UNKNOWN where relevant.

Flag:
- decision-grade outputs built from insufficient input states;
- cards that could silently promote AI output to APPROVED or CANONICAL;
- cards that allow contradiction resolution without escalation;
- cards with weak source-currency / effective-date controls in regulated or externally governed domains.

### 5. Review Profile reference audit
Extract every unique `review.<id>` used across all 59 cards.

Then:
- group semantically overlapping review IDs;
- identify likely duplicates / near-duplicates;
- identify ambiguous or overly broad IDs;
- recommend a normalized Review Profile Registry candidate list;
- do not create the registry yet.

Pay special attention to examples such as:
- `review.financial_evidence`
- `review.factual_evidence`
- similarly named legal / finance / technical / integration / publication reviews.

### 6. Decision Rights reference audit
Extract every unique `decision.<id>` used across all 59 cards.

Then:
- group semantically overlapping decision IDs;
- identify duplicates / near-duplicates;
- distinguish external communication, publication, submission, commitment, deployment and production-change rights;
- recommend a normalized Decision Rights Register candidate list;
- preserve human-only authority.

Pay special attention to examples such as:
- `decision.production_release`
- `decision.production_infrastructure_change`
- `decision.production_database_migration`

Do not collapse materially distinct decision rights just to reduce count.

### 7. Capability-domain and folder placement
Check whether each role's folder and `Capability Domain` align with Master Role Universe v1.1.

Explicitly assess:
- `Institutional Communications / Editorial Specialist` under Digital Product / Software / Data;
- `roles/project-development-technical-commercial/`;
- `roles/knowledge-documentation-disclosure/`.

For each issue, distinguish:
- genuine architecture inconsistency;
- awkward but acceptable approved placement;
- purely naming / tooling concern.

Do not reclassify roles automatically.

### 8. Project criticality policy consistency
Check that cards remain usable across:
- Routine / Standard work;
- Enhanced Review Candidate work;
- Enhanced Decision-Grade work;
- Major / Systemic work.

Verify the architecture correctly treats €50m+ as an automatic Enhanced Decision-Grade trigger while still allowing smaller projects to escalate based on complexity / risk.

Flag any role that hardcodes the wrong threshold or treats project size as the sole trigger.

### 9. Cross-role interface quality
Check:
- Typical Input Interfaces are artifact / information classes, not named teammates;
- Adjacent / Boundary Roles use `role.<id>`;
- handoff logic is workflow-agnostic;
- artifact interfaces do not imply workflow ownership that belongs elsewhere;
- minimum-input-state and output-state logic is coherent across likely producer/consumer chains.

Stress-test at least these chains:

A. €50m+ infrastructure / energy project preparation
B. €7m municipal / IFI project with procurement and ESG complexity
C. Erasmus+/CoVE programme implementation
D. commercial e-commerce business
E. institutional website + admin + Supabase/PostgreSQL
F. policy / intelligence platform with evidence lineage

### 10. Conformance re-check
Independently re-run the 17 conformance checks from:
`prompts/phase-3-claude-code-mass-role-card-generation.md`

Do not rely on Claude's prior PASS result.

## Required output

Return exactly these sections:

### A. EXECUTIVE VERDICT
One of:
- PASS
- PASS WITH CHANGES
- FAIL

State whether Phase 3 Role Registry is architecturally ready for human approval after listed changes.

### B. CRITICAL ISSUES
Only issues that make the registry unsafe, inconsistent or architecturally wrong.

For each:
- severity: CRITICAL / HIGH
- file(s)
- exact issue
- why it matters
- recommended correction

### C. IMPORTANT NORMALIZATION ITEMS
For each:
- severity: MEDIUM / LOW
- file(s)
- issue
- recommendation

Must include a position on:
1. `role.sales_business_development`
2. Institutional Communications / Editorial domain placement
3. new domain folder slugs

### D. REVIEW PROFILE ID NORMALIZATION
Provide:
- all unique `review.<id>` values found;
- overlap groups;
- proposed normalized candidate IDs;
- mapping: current -> proposed.

### E. DECISION RIGHTS ID NORMALIZATION
Provide:
- all unique `decision.<id>` values found;
- overlap groups;
- proposed normalized candidate IDs;
- mapping: current -> proposed.

### F. ROLE-BOUNDARY FINDINGS
List only genuine overlap / authority / methodology problems.
If none, say NONE.

### G. STRESS-TEST RESULTS
For each scenario A–F:
- PASS / PASS WITH ISSUE / FAIL
- one-paragraph explanation

### H. 17-CHECK CONFORMANCE
Report each check independently as PASS / FAIL with concise evidence.

### I. GO / NO-GO FOR PHASE 3 APPROVAL
Choose one:
- GO
- GO AFTER LISTED CHANGES
- NO-GO

Then list the minimum changes required before human approval.

## Constraints

- Advisory review only.
- Do not write or modify files.
- Do not create PRs or commits.
- Do not mark any role, registry or phase APPROVED / CANONICAL.
- Do not invent new first-class roles unless the audit reveals a genuine architecture gap that cannot be represented as a skill, review profile, system-control profile or decision right.
- Prefer precise normalization over role proliferation.