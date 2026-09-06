# Claude Code Prompt — Phase 4 Exemplar Skill / Skill Pack Cards

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected starting HEAD: `31d8c3f19fd6f0a12ec37c6fd0fee15e45181bc8`

The independent final re-check returned PASS with:
- B1 RESOLVED
- B2 RESOLVED
- B3 RESOLVED
- no active deprecated IDs
- all seven stress tests PASS
- no remaining blockers
- verdict: GO TO EXEMPLAR SKILL CARDS

This is an APPLY task.

Create only a small, representative exemplar set of Skill / Specialisation / Skill Pack Cards. Do NOT mass-generate the full 205 Skills / 43 Specialisations / 21 Packs.

Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not alter approved Phase 3 Role Cards.
Do not create Review Profile Registry or Decision Rights Register.
Do not introduce model/runtime bindings, orchestration, database schema, or implementation code.

## Read first

1. `architecture/skill-registry-design.md`
2. `architecture/role-to-skill-mapping-rules.md`
3. `skills/master-skill-universe.md`
4. `skills/_standards/common-skill-constraints.md`
5. `skills/_templates/skill-card-template.md`
6. `skills/_templates/skill-pack-template.md`
7. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
8. the approved Role Cards for every compatible role referenced by the cards you create
9. `reviews/phase-3-final-approval.md`
10. historical Phase 4 audit/remediation prompts for context only; do not treat them as active registry authority

## Objective

Create a deliberately small exemplar set that stress-tests:
- cross-role reusable generic Skills;
- support-only boundaries;
- Specialisation representation;
- programme Pack currency/version behavior;
- method Pack behavior;
- technology Pack behavior;
- pack dependency/layering;
- duplicate-activation handling;
- Role-owned artifact boundary;
- evidence and knowledge-state controls;
- model/runtime independence.

## Required exemplar set

Create exactly these 10 cards:

### Skills
1. `skill.source_verification`
2. `skill.requirement_traceability`
3. `skill.quality_attribute_analysis`
4. `skill.source_monitoring`
5. `skill.lifecycle_cost_analysis`

### Skill Packs
6. `skill_pack.life_programme`
7. `skill_pack.project_finance_metrics`
8. `skill_pack.supabase`
9. `skill_pack.bid_proposal_management`
10. `skill_pack.cove`

Do not create additional cards unless strictly required as a dependency placeholder. If a dependency card does not yet exist, reference the declared Pack/Skill ID in the universe without creating it and explain this in validation.

## Folder / filename convention

Use clear stable paths under `skills/`.

Recommended:
- `skills/research-evidence/source-verification.md`
- `skills/legal-compliance-procurement/requirement-traceability.md` OR another primary family that best matches the current taxonomy after inspection
- `skills/software-integration-platform-security/quality-attribute-analysis.md`
- `skills/research-evidence/source-monitoring.md`
- `skills/technical-engineering/lifecycle-cost-analysis.md`
- `skills/packs/programmes/life-programme.md`
- `skills/packs/methods/project-finance-metrics.md`
- `skills/packs/technology/supabase.md`
- `skills/packs/composite/bid-proposal-management.md`
- `skills/packs/programmes/cove.md`

If current repository naming conventions imply a better folder slug, follow them consistently and report the chosen convention.

## Card conformance rules

Every card must conform to the active template and inherit:
`standard.skill.common_constraints@0.1`

Every card status must remain:
`PROPOSED`

### Identity
Every Skill card must define:
- name
- exact ID
- Type
- primary family
- secondary family tags only where useful
- version
- governance owner
- supersedes / superseded-by

Every Pack must define:
- Pack Name
- exact Pack ID
- Type: Skill Pack
- Pack Class
- contributing families
- included specialisations where applicable
- version
- effective/review/invalidation rules

Do not invent a governance body that does not exist. Use a neutral governance owner such as `AI-OS Skill Registry Governance — human-controlled` if no narrower approved owner exists.

## Canonical mapping-source rule

Critical:

Role-to-Skill mapping records are the sole authoritative source for:
- relationship type;
- context trigger;
- alternative choice condition.

Cards may only provide:
- compatible-role allowlists;
- canonical mapping references;
- advisory Typical Use.

Do NOT write REQUIRED_CORE / REQUIRED_FOR_CONTEXT / OPTIONAL / ALTERNATIVE / PROHIBITED_IN_CONTEXT as card-level role relationships.

## Role compatibility

Build compatible-role allowlists from approved Role Cards and the Wave 1 mapping, not from guesswork.

At minimum:

### `skill.source_verification`
Must support the current Wave 1 mapped Roles where applicable, including:
- Research / Market Intelligence Analyst
- EU Grants & Programmes Specialist
- Legal & Regulatory Lead
- Knowledge & Evidence Steward

Define boundary carefully so it verifies provenance, authority, currency and version but does not become independent factual review, legal opinion, or evidence-governance authority.

### `skill.requirement_traceability`
Use compatible Roles from current mappings, including EU Grants / Legal / Product / Data / Architecture where actually supported by Role Cards.

Boundary: links requirements to sources, decisions, artifacts and tests; does not itself approve requirements or perform independent review.

### `skill.quality_attribute_analysis`
Compatible with Solution Architect and other roles only where Role Cards support use.

Explicitly include selectable dimensions such as:
- security
- privacy
- resilience
- performance
- availability

Boundary: it structures and allocates quality requirements; it does not replace Security Engineer or Data Protection / GDPR Specialist conclusions.

### `skill.source_monitoring`
Define recurring monitoring of governed source classes and change detection.

Boundary: monitoring detects and flags change; it does not promote knowledge state, publish policy/legal conclusions, or automatically rewrite canonical knowledge.

### `skill.lifecycle_cost_analysis`
Treat as support-only for Technical / Feasibility Lead where mapped.

Explicitly state:
- cost and O&M inputs are specialist-owned;
- this Skill may compare lifecycle implications of technical options;
- it may never create authoritative CAPEX/OPEX estimates or cost acceptance conclusions.

Preserve ownership of CAPEX / Cost Engineering and Asset O&M / Technical Operations roles.

## Pack-specific requirements

### 1. `skill_pack.life_programme`
Pack Class: PROGRAMME.

Must include as pack-internal controlled capabilities, not standalone Skill IDs:
- eligibility analysis;
- work-package logic;
- programme budget logic;
- submission requirement mapping.

Must model:
- controlled source / call guide version;
- call-specific effective date;
- submission deadline / annex / portal constraints as versioned controlled content;
- compatibility with EU Grants & Programmes Specialist and other roles only where supported;
- pack expiry/invalidation when call rules or official guidance change.

Do not hard-code current external LIFE facts from web research. This card defines architecture and controlled-source requirements, not current call content.

### 2. `skill_pack.project_finance_metrics`
Pack Class: METHOD.

Must include at minimum:
- `specialisation.dscr`
- `specialisation.llcr`
- `specialisation.plcr`

May reference `skill.project_finance_ratio_analysis` if still active in the universe.

Boundary:
- provides governed metric definitions, calculation conventions, sensitivity / covenant-analysis methods;
- does not grant Funding & Bankability or Project Finance transaction authority;
- does not own lender commitments or financing approval.

### 3. `skill_pack.supabase`
Pack Class: TECHNOLOGY.

Must define platform-specific capability constraints without binding any Role to a model/runtime.

Must cover architecture-level controlled topics such as:
- database / relational platform use where relevant;
- auth / storage / API / security constraints where applicable;
- version/service-limit currency;
- deployment / integration assumptions;
- data/confidentiality and production-boundary constraints.

Boundary:
- activation does not authorize production change;
- does not replace Security Engineer, Data Protection, Data Architect, DevOps or Integration ownership.

Do not use live web research to populate current platform limits; specify that controlled source references must be refreshed from authoritative vendor documentation when the Pack is instantiated or updated.

### 4. `skill_pack.bid_proposal_management`
Pack Class: COMPOSITE.

This Pack replaces any standalone `skill.bid_proposal_management` concept.

Must define coherent reusable bundle for formal competitive bid/proposal processes, potentially spanning:
- opportunity qualification;
- requirements / compliance matrix;
- contribution planning;
- deliverable schedule;
- narrative coordination;
- evidence / claim substantiation;
- submission-readiness quality control.

Boundary:
- does not replace programme-specific Packs such as LIFE / Erasmus+ / Horizon;
- does not own legal signature, pricing approval, budget approval or external submission authority;
- submission readiness QC is not independent review.

### 5. `skill_pack.cove`
Pack Class: PROGRAMME.

Must explicitly declare one-directional conditional layering over `skill_pack.erasmus_plus` where the CoVE action operates under Erasmus+ rules.

Must state:
- CoVE adds action-specific rules/logic on top of applicable Erasmus+ requirements;
- Erasmus+ does not depend on CoVE;
- no circular dependency;
- more-specific CoVE constraints prevail where stricter / more specific;
- unresolved inconsistency -> `CONFLICT_DETECTED`.

Do not populate current CoVE programme facts from outside research; define controlled-source/version architecture only.

## Evidence and knowledge-state requirements

All 10 cards must explicitly preserve:
- SOURCE / FACT / ASSUMPTION / CALCULATION / AI_SUGGESTION / DRAFT / REVIEWED / APPROVED / CANONICAL / SUPERSEDED / CONFLICT_DETECTED / UNKNOWN semantics where relevant;
- AI-generated content is not a controlled source;
- the Skill/Pack cannot execute a knowledge-state transition;
- contradictions or stale authoritative sources escalate rather than resolve silently.

## Review / decision boundary

Do not invent new review IDs or decision IDs.

Where a current approved Role Card or mapping already references a review/decision dependency, the Skill/Pack may reference it as a dependency only.

If no confirmed ID exists, write `none at Skill/Pack level; resolved by consuming Role/workflow` rather than inventing one.

Every card must state that quality-control techniques do not discharge independent review obligations.

## Proficiency

Use only:
- AWARENESS
- WORKING
- ADVANCED
- EXPERT

Do not use FOUNDATION or any other scale.

Proficiency never creates authority, credential, licensing or regulated authorisation.

## Validation before commit

Run and report all of the following:

1. Exactly 10 exemplar cards created.
2. No approved Phase 3 Role Card modified.
3. All 10 cards Status = PROPOSED.
4. All 10 inherit `standard.skill.common_constraints@0.1`.
5. No card independently declares a role relationship type or trigger.
6. All compatible Role IDs exist in approved Role Registry.
7. All referenced Skill / Specialisation / Skill Pack IDs exist in `skills/master-skill-universe.md`, except explicitly permitted dependency references that are declared in the universe but do not yet have cards.
8. No active deprecated ID is reintroduced.
9. No `skill.integrity_due_diligence`.
10. No standalone `skill.bid_proposal_management`.
11. `skill.lifecycle_cost_analysis` preserves specialist-owned cost-input boundary.
12. `skill.quality_attribute_analysis` preserves Security and Data Protection Role ownership.
13. LIFE programme micro-capabilities are pack-internal, not new standalone Skill IDs.
14. CoVE dependency direction is CoVE -> Erasmus+, never reverse.
15. No circular pack dependency among created Packs.
16. Duplicate-activation rule is present in every Pack where included Skills may also be individually mapped.
17. No Pack claims to satisfy licensing, competence, review-independence or human authority.
18. No model/runtime binding introduced.
19. No Review Profile Registry or Decision Rights Register created.
20. No Skill / Pack marked APPROVED or CANONICAL.
21. Proficiency vocabulary only AWARENESS / WORKING / ADVANCED / EXPERT.
22. AI-generated content is not used as controlled source.
23. Every card has explicit Role-owned artifact / contribution boundary or an explicit explanation of why contribution is method-level and artifact ownership remains with consuming Roles.
24. Every evaluation/readiness/validation/check technique is explicitly QC, not independent review.

Also report any template defect discovered while authoring exemplars. Do not silently modify templates unless the defect blocks correct card creation; if blocking, stop and report instead of improvising a competing structure.

## Commit / Push

If all mandatory validation passes:

Commit exactly:
`docs: add Phase 4 exemplar Skill and Skill Pack cards`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required final output

Return exactly:

### A. EXEMPLAR CARDS CREATED
List all 10 paths and IDs.

### B. CONFORMANCE
Summarize template and common-constraint conformance.

### C. ROLE / AUTHORITY BOUNDARIES
Report lifecycle-cost, quality-attribute, source-verification, and Pack authority boundaries.

### D. PACK MODEL
Report LIFE internal components, Project Finance Metrics composition, Supabase boundaries, Bid/Proposal boundaries, CoVE->Erasmus+ dependency.

### E. VALIDATION
Report checks 1–24 PASS / FAIL.

### F. TEMPLATE DEFECTS
If none: NONE.

### G. COMMIT / PUSH
Commit SHA and push result.

### H. REMAINING NON-BLOCKING ITEMS
Only items not required for exemplar-card completion.

If any mandatory check fails, do not claim completion.