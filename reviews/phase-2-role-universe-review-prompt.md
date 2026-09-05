# Phase 2 Independent Role Universe Review Prompt

Status: WORKING REVIEW INSTRUCTION

## Reviewer role
Act as an independent senior enterprise architect, operating-model architect and multi-agent systems reviewer. Review the AI-OS Master Role Universe as a professional capability architecture, not as a list of chatbot personas.

## Scope
Review `roles/master-role-universe.md` together with:
- `architecture/system-principles.md`
- `architecture/context-hierarchy.md`
- `architecture/capability-map.md`

Do not design database schemas, orchestration frameworks, APIs or implementation code.

## Objectives
1. Identify duplicate or substantially overlapping roles.
2. Identify roles that should become reusable skill packs rather than first-class roles.
3. Identify roles that are too broad and need separation.
4. Identify missing professional competencies required for:
   - general businesses across sectors;
   - EU-funded consortium projects such as Erasmus+/CoVE and EU social-dialogue projects;
   - €200m+ infrastructure/investment projects prepared to international advisory / IFI standards;
   - websites, SaaS, portals and internal digital products;
   - databases, data architecture, integrations and AI-enabled systems;
   - organisational operations, sales, marketing, HR and customer/service functions.
5. Check that the architecture can assemble multidisciplinary teams without hard-coding teams into roles.
6. Check separation of Delivery, Independent Assurance and Human Authority.
7. Check that ROLE != MODEL, ROLE != AGENT INSTANCE, and project context isolation remain intact.
8. Check whether reviewer roles are correctly modelled as independent profiles rather than duplicating author roles unnecessarily.
9. Stress-test the role universe against at least these scenarios:
   - €250m energy/infrastructure project for EIB/EBRD-style preparation;
   - Erasmus+/CoVE consortium implementation project;
   - EU social-dialogue/climate-adaptation project;
   - new commercial e-commerce business;
   - new institutional website + admin portal + Supabase/PostgreSQL backend;
   - data-heavy policy/intelligence platform with monitoring, evidence and knowledge graph requirements.

## Required output
Produce five sections only:

### A. KEEP AS FIRST-CLASS ROLES
For each role: role name + one-sentence reason.

### B. MERGE / RENAME
For each: current roles -> proposed role + rationale.

### C. CONVERT TO SKILL PACK / SPECIALISATION
For each: current role -> parent role + rationale.

### D. MISSING ROLES
Only roles whose absence creates a real professional capability or authority gap.

### E. PROPOSED MASTER ROLE UNIVERSE v1.0
Provide the final deduplicated list grouped by capability domain. Do not optimise for a small MVP yet.

## Review standard
Be conservative about creating roles. A separate first-class role is justified only when at least one is true:
- it requires a distinct professional methodology;
- it has a materially different authority boundary;
- it needs independent review separation;
- it recurrently produces a distinct professional artifact or decision-grade output.

Do not assume that a named technology, programme, institution, metric or sector deserves a separate role. Prefer skill packs for items such as EIB, EBRD, LIFE, Horizon Europe, Supabase, PostgreSQL, DSCR, solar energy, etc., unless the review demonstrates a genuine role-level boundary.

## Canonicality rule
Your output is a review recommendation only. Do not label any change DECIDED or CANONICAL. Human approval is required before changes to the Master Role Universe.
