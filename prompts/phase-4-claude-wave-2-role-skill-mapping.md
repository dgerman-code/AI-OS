# Claude Code Prompt — Phase 4 Wave 2 Role-to-Skill Mapping

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected starting HEAD: `63ebc4ae4d27af23f1028ea608f5849734f4026f`

Independent re-check result:
- FINAL VERDICT: PASS WITH NON-BLOCKING NOTES
- ALLOWLIST REMEDIATION: PASS
- TRANSITIVE PACK COMPATIBILITY: PASS
- AUTHORITY BOUNDARY: PASS
- REMAINING TESTABLE INCOMPATIBILITIES: NONE
- COVERAGE LIMITATION: NON-BLOCKING
- REMAINING BLOCKERS: NONE
- NEXT STEP: GO TO WAVE 2 ROLE-TO-SKILL MAPPING
- MASS GENERATION: NOT YET — KEEP SELECTIVE

This is an APPLY task for **Wave 2 mapping only**.

Do not mass-generate Skill, Specialisation or Skill Pack Cards.
Do not create new first-class Roles.
Do not modify approved Phase 3 Role Cards.
Do not create Review Profile Registry or Decision Rights Register.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not introduce model/runtime bindings, orchestration, database schema or implementation code.

## Read first

1. `architecture/skill-registry-design.md`
2. `architecture/role-to-skill-mapping-rules.md`
3. `skills/master-skill-universe.md`
4. `skills/_standards/common-skill-constraints.md`
5. `skills/_templates/skill-card-template.md`
6. `skills/_templates/skill-pack-template.md`
7. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
8. all 10 existing exemplar Skill / Skill Pack Cards
9. `reviews/phase-3-final-approval.md`
10. every approved Phase 3 Role Card for the remaining 48 roles listed below

## Scope: exactly the remaining 48 approved Roles

Do not remap the 11 Wave 1 exemplar Roles except where a cross-reference is needed for reuse analysis.

Map exactly these 48 Roles:

1. Portfolio / Programme Manager
2. Strategy & Business Analyst
3. Marketing / Growth Specialist
4. Operations / Service Delivery Specialist
5. People / Organisation Specialist
6. Customer / CRM Specialist
7. Supply Chain & Procurement Operations Specialist
8. EU Policy & Institutional Affairs Specialist
9. EU Enlargement / Governance Specialist
10. Institutional Affairs & Stakeholder Specialist
11. Programme / Partnership Manager
12. EU Programme Implementation & Grant Management Specialist
13. Consortium / Partner Coordination Specialist
14. Grant Financial Compliance / Budget Specialist
15. Deliverables / Reporting Specialist
16. Learning / VET Design Specialist
17. Social Dialogue Specialist
18. Monitoring, Evaluation & Learning Specialist
19. Project Development Lead
20. Sector Technical Expert
21. Commercial & Demand Specialist
22. CAPEX / Cost Engineering Specialist
23. Asset O&M / Technical Operations Specialist
24. Economic / CBA Specialist
25. FP&A / Management Finance Specialist
26. Funding & Bankability Architect
27. Project Finance / Transaction Specialist
28. IFI / DFI Project Preparation Specialist
29. PPP / Concession Specialist
30. Tax Specialist
31. Accounting / Financial Due Diligence Specialist
32. Insurance / Risk Transfer Specialist
33. Procurement / State Aid Specialist
34. ESG / E&S Specialist
35. Enterprise / Project Risk Specialist
36. Integrity / Due Diligence Specialist
37. Data Protection / GDPR Specialist
38. UX / UI & Information Architecture Specialist
39. Institutional Communications / Editorial Specialist
40. Full-Stack Software Engineer
41. Integration / API Engineer
42. Platform / DevOps Engineer
43. Database / Data Engineer
44. Data / Business Analytics Specialist
45. AI / Knowledge Systems Engineer
46. Security Engineer
47. Software QA / Test Automation Specialist
48. Data Room & Disclosure Manager

## Critical precondition: exact Role IDs

Do not infer Role IDs from names.

For all 48 roles:
- read the actual Role Card;
- extract the exact `Role ID:`;
- verify 48 unique Role IDs;
- use only those exact IDs in Wave 2.

If any named Role Card is missing or its identity conflicts with the approved 59-role baseline, STOP and report instead of guessing.

## Deliverable

Create one new file:

`skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

Do not rewrite Wave 1.

The Wave 2 file must be `Status: PROPOSED` and must state clearly:

> Role-to-Skill mapping records are the sole authoritative source for relationship type, context trigger and alternative choice condition. Mapping grants capability applicability, never professional authority.

## Mapping vocabulary

Use only:
- `REQUIRED_CORE`
- `REQUIRED_FOR_CONTEXT`
- `OPTIONAL`
- `ALTERNATIVE`
- `PROHIBITED_IN_CONTEXT`

Rules:

### REQUIRED_CORE
Use sparingly.
A capability is REQUIRED_CORE only when it is intrinsic to competent execution of the Role across most ordinary assignments.

Do not turn every item in a Role Card's prose `Core Skills` section into a registry REQUIRED_CORE mapping.

### REQUIRED_FOR_CONTEXT
Every entry MUST have an explicit trigger.
Valid trigger classes include:
- sector;
- programme / call / framework;
- institution / financing route;
- jurisdiction;
- technology;
- project criticality;
- financing structure;
- counterparty;
- regulated activity;
- data classification;
- publication / external use;
- artifact / workflow condition.

### OPTIONAL
Use for useful but genuinely non-essential capabilities.

### ALTERNATIVE
Every ALTERNATIVE set must:
- name the choice set;
- state the choice condition;
- explain whether one-of, at-least-one-of or mutually exclusive applies.

### PROHIBITED_IN_CONTEXT
Use only where a real, defensible restriction exists from:
- Role scope;
- licensing / authorisation;
- independence;
- confidentiality / data classification;
- jurisdiction;
- methodology conflict;
- workflow safety.

Do **not** invent a prohibition just to exercise the type.
If no genuine case exists, state that explicitly in the validation report.

## Registry reference rules

### Active mappings may reference only IDs already present in `skills/master-skill-universe.md`

Allowed entity namespaces:
- `skill.<id>`
- `specialisation.<id>`
- `skill_pack.<id>`

Do not invent active mapping IDs.

If a genuinely missing reusable capability is discovered:
- do NOT create a new Skill Card;
- do NOT silently add it to an active mapping;
- list it in a final section `Candidate Universe Gaps — NOT ACTIVE MAPPINGS` with proposed ID, reason, likely family/class, and affected Roles.

The active mapping section must remain free of unresolved references.

## Specialisation test required in Wave 2

The independent audit explicitly said the Specialisation model should be tested in Wave 2.

Use existing `specialisation.<id>` entries from the Master Skill Universe where they are genuinely applicable.

Requirements:
- include at least one real active Specialisation mapping if the Universe and Role Cards support it;
- prefer several meaningful examples across distinct classes such as SECTOR / INSTITUTION / TECHNOLOGY / JURISDICTION / METRIC / OPERATING_CONTEXT where they exist;
- do not create Specialisation Cards in this step;
- do not force a mapping solely for test coverage.

Report which Specialisation IDs were exercised and why they remain bounded context rather than authority.

## Skill Pack use

Use existing `skill_pack.<id>` where the Pack is the correct reusable unit, especially for:
- programmes;
- IFIs / institutions;
- technologies;
- project finance methods;
- labour-market/skills context;
- bid/proposal context;
- technical writing/documentation;
- version control/document configuration;
- change/adoption.

Do not explode Pack contents into duplicate mandatory direct mappings unless a Skill has independent meaning outside the Pack.

Where a direct Skill and a Pack would activate the same capability, apply the duplicate-effective-activation rule.

## Transitive Pack Compatibility

Apply `standard.skill.common_constraints` §6.1a.

For every Pack mapped to a Role:
- validate every Required Skill that currently has a Skill Card against the consuming Role;
- validate every selectable Optional Skill that currently has a Skill Card against the consuming Role;
- traverse currently declared Pack dependencies/layering;
- if an existing Skill/Pack Card allowlist must be widened purely for compatibility with a valid new Wave 2 mapping, update that allowlist in the same commit;
- such allowlist widening confers compatibility only, never relationship type or trigger;
- do not modify the capability's authority/boundary sections unless a genuine contradiction is discovered; if contradiction exists, STOP and report instead of widening.

For Pack components without cards, report them as `NOT YET VALIDATABLE`, not as PASS.

## Existing exemplar-card allowlist synchronization

The 10 exemplar cards may be edited only when Wave 2 creates a valid direct or transitive compatibility requirement for a new Role.

If edited:
- preserve all authority, artifact, review, decision, evidence and knowledge-state boundary sections byte-identically where possible;
- change only compatible-role allowlist / mapping-reference / explanatory compatibility prose;
- never put relationship type or trigger in the card.

## Role boundary discipline

For every mapping, check the approved Role Card's:
- Purpose;
- Owns;
- Does Not Own;
- Professional Decision Right;
- Output Artifact Interfaces;
- Authority Limits;
- Review Obligation;
- Human Decision Gates;
- Independence Constraints.

A Skill / Specialisation / Pack must never:
- widen Role scope;
- transfer another Role's professional conclusion;
- create artifact ownership;
- create independent review identity;
- create human approval authority;
- bypass a specific `review.<id>` or `decision.<id>`;
- convert support work into ownership.

Where a capability touches another Role's methodology, write an explicit `Support-only boundary` note in the Wave 2 role section.

## Specific high-risk boundary checks

Pay particular attention to:

- Portfolio / Programme Manager vs Project / Delivery Lead;
- Strategy / Business Analyst vs Research / Market Intelligence;
- Supply Chain & Procurement Operations vs Procurement / State Aid;
- EU Policy / Institutional Affairs vs Legal / Regulatory and EU Grants;
- Programme / Partnership Manager vs Consortium Coordination;
- EU Programme Implementation vs EU Grants & Programmes;
- Grant Financial Compliance vs FP&A / Accounting / Financial DD;
- MEL vs Data / Business Analytics;
- Project Development Lead vs Technical / Feasibility and Funding / Bankability;
- Sector Technical Expert vs Technical / Feasibility;
- CAPEX / Cost Engineering vs Financial Modelling;
- Asset O&M vs Operations / Service Delivery;
- Economic / CBA vs Financial Modelling / Funding & Bankability;
- Funding & Bankability vs Project Finance / Transaction;
- IFI / DFI Preparation vs institution Packs and transaction ownership;
- PPP / Concession vs Legal / Procurement / Project Finance;
- Tax vs Accounting / Financial DD;
- Insurance / Risk Transfer vs Enterprise / Project Risk;
- Procurement / State Aid vs Legal / Regulatory;
- ESG / E&S vs Enterprise Risk;
- Integrity / Due Diligence vs source verification / screening component skills;
- Data Protection / GDPR vs Security and Solution Architecture;
- UX/UI/IA vs Product Manager / BA;
- Institutional Communications / Editorial vs Marketing / Growth;
- Full-Stack vs Solution Architect / Integration / Platform;
- Integration/API vs Solution Architect;
- Platform/DevOps vs Security / Data / Integration;
- Database/Data Engineer vs Data & Database Architect;
- Data/Business Analytics vs FP&A / MEL / Research;
- AI/Knowledge Systems vs Knowledge & Evidence Steward / Data Architect;
- Security Engineer vs quality-attribute support techniques;
- QA/Test Automation vs independent Review Profiles;
- Data Room & Disclosure Manager vs Knowledge & Evidence Steward.

## Project criticality

Use `architecture/project-criticality-policy.md`.

Criticality may increase:
- required depth;
- evidence quality;
- review dependency;
- specialist engagement;
- contextual Skill/Pack activation.

Criticality must NOT create a new Role identity or turn OPTIONAL into REQUIRED_CORE globally.

## Cross-role reuse and anti-proliferation

After mapping all 48 roles, compute:
- total active mapping entries;
- counts by relationship type;
- number of unique Skills;
- number of unique Specialisations;
- number of unique Skill Packs;
- top 20 most reused capability IDs;
- number and percentage of capability IDs used by only one Role across Wave 1 + Wave 2;
- candidate near-duplicates / micro-skills surfaced by mapping;
- Pack-vs-direct duplication cases.

Do not automatically delete or merge additional universe entries in this step.
List them for Wave 3 audit.

## Wave 1 preservation

Wave 1 is a reviewed exemplar baseline.
Do not rewrite its mappings in this step.

If Wave 2 exposes a contradiction with Wave 1:
- do not silently fix Wave 1;
- record it under `Cross-Wave Conflict Findings`;
- classify severity;
- leave remediation to a separate governed step.

## Required file structure

`skills/mappings/wave-2-domain-completion-role-skill-mapping.md` must contain:

1. Status / scope / canonical-source statement
2. Exact Role ID verification table for all 48 roles
3. Mapping sections for each role
4. For each role:
   - REQUIRED_CORE
   - REQUIRED_FOR_CONTEXT with trigger
   - OPTIONAL
   - ALTERNATIVE sets if any
   - PROHIBITED_IN_CONTEXT if any genuine case
   - activated Specialisations / Packs
   - support-only / ownership boundaries
   - short rationale for sparse core
5. Cross-role reuse summary
6. Specialisation coverage summary
7. Pack activation and transitive compatibility summary
8. Candidate Universe Gaps — NOT ACTIVE MAPPINGS
9. Micro-skill / overlap candidates for Wave 3 audit
10. Cross-Wave Conflict Findings
11. Validation summary

## Validation before commit

Run and report all of these checks:

1. Exactly 48 Wave 2 Role names are present.
2. Exactly 48 unique Role IDs, each verified from an actual approved Role Card.
3. Zero Wave 1 Roles accidentally remapped as Wave 2 subjects.
4. Every active `skill.<id>` exists in Master Skill Universe.
5. Every active `specialisation.<id>` exists in Master Skill Universe.
6. Every active `skill_pack.<id>` exists in Master Skill Universe.
7. Zero unresolved candidate IDs inside active mappings.
8. Every REQUIRED_FOR_CONTEXT entry has an explicit trigger.
9. Every ALTERNATIVE set has an explicit choice condition and cardinality.
10. Every PROHIBITED_IN_CONTEXT entry, if any, has a concrete safety/scope basis.
11. REQUIRED_CORE remains sparse; report per-role count and flag >8 for manual review rather than assuming it is valid.
12. No mapping widens approved Role authority.
13. No mapping transfers artifact ownership or another Role's professional conclusion.
14. No mapping creates review identity or human decision authority.
15. No model/runtime binding.
16. No Phase 3 Role Card modified.
17. No Skill / Specialisation / Pack Card created.
18. Any existing exemplar-card edits are allowlist/mapping-reference compatibility edits only.
19. All currently carded Pack components pass transitive compatibility for every newly mapped Pack-consuming Role.
20. Uncarded Pack components are reported as NOT YET VALIDATABLE.
21. No circular Pack dependency introduced.
22. Duplicate-effective-activation cases are identified and handled once under the stricter obligation.
23. At least one genuine Specialisation mapping is present if supported; otherwise explain why none exists.
24. PROHIBITED_IN_CONTEXT is not fabricated; report actual count.
25. No active deprecated ID is reintroduced.
26. All mapping artifacts remain PROPOSED / working.
27. Candidate Universe Gaps are excluded from active mappings.
28. Cross-Wave conflicts are reported rather than silently editing Wave 1.
29. Cross-role reuse statistics are computed from actual mapping data, not estimates.
30. The mapping file is sufficient for an independent Wave 2 audit without reading Claude's console history.

## Commit / Push

If all mandatory validation passes:

Commit exactly:
`docs: add Phase 4 Wave 2 role-to-skill mapping`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. WAVE 2 MAPPING CREATED
Path, 48-role coverage and mapping counts.

### B. ROLE ID VERIFICATION
48/48 result and any identity issue.

### C. RELATIONSHIP DISTRIBUTION
Counts for REQUIRED_CORE / REQUIRED_FOR_CONTEXT / OPTIONAL / ALTERNATIVE / PROHIBITED_IN_CONTEXT.

### D. SPECIALISATION / PACK COVERAGE
Specialisation IDs exercised, Pack IDs exercised, and why they remain context rather than authority.

### E. TRANSITIVE PACK COMPATIBILITY
Carded components PASS/FAIL; uncarded components NOT YET VALIDATABLE; any allowlist-only edits.

### F. ROLE / AUTHORITY BOUNDARIES
High-risk boundary results and any support-only notes.

### G. UNIVERSE GAPS / MICRO-SKILL FINDINGS
Candidate gaps excluded from active mappings and overlap candidates for Wave 3.

### H. CROSS-WAVE CONFLICTS
If none: NONE.

### I. VALIDATION
Checks 1–30 PASS / FAIL.

### J. COMMIT / PUSH
Commit SHA and push result.

### K. NEXT-STEP READINESS
Choose:
- READY FOR INDEPENDENT WAVE 2 AUDIT
- NOT READY

Do not claim Phase 4 approval or readiness for mass generation.