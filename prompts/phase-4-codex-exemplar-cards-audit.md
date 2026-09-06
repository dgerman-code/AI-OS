# Codex Prompt — Phase 4 Exemplar Skill / Skill Pack Cards Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected HEAD: `1b7f417b5dc4fced6651f669191bb1beb6df855e`

Act as an independent senior architecture auditor.

Audit the 10 newly created exemplar Skill / Skill Pack Cards against the active Phase 4 architecture, mappings, templates and approved Phase 3 Role boundaries.

This is verification-only.
Do not modify files.
Do not commit.
Do not create a PR.
Do not create additional Skill / Specialisation / Skill Pack Cards.
Do not mark Phase 4 APPROVED or CANONICAL.
Do not introduce implementation, database, orchestration, model/router or agent-framework design.

## Read first

1. `architecture/skill-registry-design.md`
2. `architecture/role-to-skill-mapping-rules.md`
3. `skills/master-skill-universe.md`
4. `skills/_standards/common-skill-constraints.md`
5. `skills/_templates/skill-card-template.md`
6. `skills/_templates/skill-pack-template.md`
7. `skills/mappings/wave-1-exemplar-role-skill-mapping.md`
8. all 10 exemplar cards created in commit `1b7f417b5dc4fced6651f669191bb1beb6df855e`
9. every approved Phase 3 Role Card referenced by those exemplars
10. `reviews/phase-3-final-approval.md`

## Cards to audit

### Skills
- `skill.source_verification`
- `skill.requirement_traceability`
- `skill.quality_attribute_analysis`
- `skill.source_monitoring`
- `skill.lifecycle_cost_analysis`

### Skill Packs
- `skill_pack.life_programme`
- `skill_pack.project_finance_metrics`
- `skill_pack.supabase`
- `skill_pack.bid_proposal_management`
- `skill_pack.cove`

## Audit objectives

### 1. Template conformance
For each card verify:
- exact ID exists in Master Skill Universe;
- Status = PROPOSED;
- correct template type;
- inherits `standard.skill.common_constraints@0.1`;
- identity/version/governance fields are complete;
- no card-level relationship type or context trigger is declared authoritatively;
- compatible-role allowlist and mapping references are non-authoritative and consistent with Wave 1 mappings;
- no model/runtime identity is embedded.

### 2. Hidden Role / hidden authority test
For every Skill and Pack determine whether it:
- owns a professional conclusion;
- owns a first-class artifact;
- creates human approval power;
- creates review identity;
- silently absorbs another approved Role's methodology.

Any such condition is HIGH unless clearly constrained as support-only.

### 3. Role-owned artifact boundary
Check every exemplar contribution against approved Role Cards.

Verify that:
- named artifact IDs actually exist where asserted;
- owning Role IDs exist;
- the Skill/Pack contributes to but does not own the artifact;
- support-only language is sufficient where another Role owns the professional conclusion.

Flag any invented artifact ID, review ID or decision ID as HIGH.

### 4. Source Verification boundary
Verify `skill.source_verification` is strictly limited to provenance / authority / version / currency verification and does not become:
- factual truth determination;
- independent factual review;
- legal interpretation;
- canonical-knowledge promotion authority.

Check its allowlist is consistent with current mappings and approved Role Cards.

### 5. Requirement Traceability boundary
Verify `skill.requirement_traceability`:
- links requirements to sources, decisions, artifacts, implementation/tests where applicable;
- does not approve requirements;
- does not become independent compliance review;
- does not transfer Product, Legal, Architecture or Data authority.

Assess whether the chosen primary Skill Family is reasonable and non-authoritative.

### 6. Quality Attribute Analysis boundary
Verify `skill.quality_attribute_analysis`:
- may structure security/privacy/resilience/performance/availability dimensions;
- does not issue security accreditation or risk acceptance;
- does not make GDPR/lawful-basis/DPIA conclusions;
- does not replace `role.security_engineer` or `role.data_protection_gdpr_specialist`.

### 7. Source Monitoring boundary
Verify `skill.source_monitoring`:
- monitors governed source classes and detects changes;
- does not interpret policy/legal meaning by itself;
- does not modify canonical knowledge;
- does not perform knowledge-state transitions;
- does not publish externally.

### 8. Lifecycle Cost Analysis boundary
Verify `skill.lifecycle_cost_analysis` preserves the remediation rule:
- no authoritative CAPEX estimate;
- no authoritative OPEX estimate;
- no filling cost gaps with self-generated estimates;
- cost and O&M inputs remain specialist-owned;
- it only supports technical option comparison;
- no `decision.cost_estimate_acceptance` authority.

Any weakening is HIGH.

### 9. LIFE Programme Pack
Verify:
- Pack Class PROGRAMME;
- four normalized micro-capabilities are pack-internal and are not recreated as Skill IDs;
- controlled source/version/effective-date/call-specific invalidation architecture is explicit;
- no current LIFE facts were hard-coded without controlled-source architecture;
- external submission, budget approval, legal signature and human authority remain outside the Pack.

### 10. Project Finance Metrics Pack
Verify:
- DSCR / LLCR / PLCR are included appropriately;
- calculation/convention scope is coherent;
- `skill.project_finance_ratio_analysis` inclusion does not create duplicate activation problems;
- Funding & Bankability Architect and Project Finance / Transaction Specialist authority is not absorbed;
- lender engagement, financing terms acceptance, financial close and financial-model external reliance remain outside Pack authority.

### 11. Supabase Pack
Verify:
- Pack is technology context, not a Role;
- platform-specific architecture/implementation constraints are version/currency governed;
- no current vendor limit or feature fact is asserted as timeless without controlled-source linkage;
- activation does not grant production release/change/migration, technology-selection, security, GDPR, data architecture, integration or DevOps authority;
- no AI model/runtime binding exists.

### 12. Bid / Proposal Management Pack
Verify:
- it is only `skill_pack.bid_proposal_management`, not a hidden standalone Skill;
- it is a coherent composite bundle rather than a hidden Proposal Manager Role;
- no legal signature, commercial commitment, budget approval or submission authority is acquired;
- readiness checks are QC, not independent review;
- programme-specific rules remain in programme Packs.

### 13. CoVE Pack layering
Verify:
- CoVE -> Erasmus+ is one-way where applicable;
- Erasmus+ does not depend on CoVE;
- no cycle exists;
- more-specific/stricter precedence is correct;
- a more-specific Pack cannot permissively override a stricter base requirement;
- unresolved conflict becomes `CONFLICT_DETECTED`;
- dependency currency/invalidation propagation is explicit.

### 14. Controlled source and evidence integrity
Across all cards verify:
- AI-generated content is never a controlled source;
- source currency/version metadata are required where relevant;
- assumptions remain explicit;
- contradictions are escalated rather than silently reconciled;
- no Skill/Pack can promote itself to APPROVED or CANONICAL.

### 15. Review / decision references
Extract all `review.<id>` and `decision.<id>` used in the 10 cards and verify each against approved Phase 3 Role Cards or other existing approved architecture references.

Flag:
- invented IDs;
- wrong semantic reuse;
- any reference that gives authority to the Skill/Pack rather than expressing dependency.

### 16. Mapping-source integrity
Verify all 10 cards honor:

`Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger.`

Check there is no subtle reintroduction through:
- Typical Use;
- Activation Criteria;
- compatible-role narrative;
- Pack Applicability;
- prerequisites.

Activation/applicability may describe Pack-level conditions but must not become a second Role relationship registry.

### 17. Pack overlap / dependency integrity
For all five packs:
- no dependency cycle;
- duplicate effective activation rule is coherent;
- stricter/specific precedence is safe;
- no pack stack accumulates authority;
- unresolved overlap does not silently pick a permissive rule.

### 18. Specialisation model coverage
The current exemplar set contains no `Type: SPECIALISATION` card.

Assess whether this is:
- NON-BLOCKING and acceptable before Wave 2; or
- a blocker requiring one Specialisation exemplar before broad mapping/generation.

Do not create one; just decide.

### 19. PROHIBITED_IN_CONTEXT coverage
Wave 1 still has no live PROHIBITED_IN_CONTEXT mapping.

Assess whether this is:
- NON-BLOCKING and can be tested in Wave 2; or
- a blocker before further work.

Do not invent a prohibition just to exercise the type.

### 20. Micro-skill / over-cardification risk
Assess whether the five Skill exemplars validate the desired granularity or reveal pressure toward over-cardification.

Pay particular attention to whether the card format encourages too much artifact/decision detail for atomic reusable techniques.

### 21. Scale readiness
Given 205 Skills, 43 Specialisations, 21 Packs, determine whether the exemplar standard is now safe for:
- Wave 2 mapping of the remaining 48 Roles;
- additional selected exemplar cards;
- or mass generation.

Mass generation should be recommended only if architecture evidence strongly supports it.

## Required output

Return exactly these sections:

### A. FINAL VERDICT
Choose:
- PASS
- PASS WITH NON-BLOCKING NOTES
- PASS WITH CHANGES
- FAIL

### B. HIGH / CRITICAL FINDINGS
List only blocking architecture/authority/integrity issues.
If none: NONE.

### C. CARD-BY-CARD AUDIT
For each of the 10 cards:
- PASS
- PASS WITH NON-BLOCKING NOTE
- PASS WITH CHANGE REQUIRED
- FAIL
and a concise rationale.

### D. ROLE / AUTHORITY BOUNDARY
PASS / FAIL.
List any ownership leakage or invented artifact/review/decision reference.

### E. MAPPING-SOURCE INTEGRITY
PASS / FAIL.
List any card that creates a second relationship/trigger source.

### F. PACK DEPENDENCY / PRECEDENCE
PASS / FAIL.
Report cycles, overlap problems or authority accumulation if any.

### G. CONTROLLED SOURCE / KNOWLEDGE-STATE
PASS / FAIL.
List defects if any.

### H. SPECIALISATION COVERAGE
Choose:
- NON-BLOCKING — TEST IN WAVE 2
- ADD ONE EXEMPLAR BEFORE WAVE 2
- BLOCKER
Explain briefly.

### I. PROHIBITED_IN_CONTEXT COVERAGE
Choose:
- NON-BLOCKING — TEST IN WAVE 2
- ADD A REAL CASE BEFORE WAVE 2
- BLOCKER
Explain briefly.

### J. MICRO-SKILL / SCALE FINDINGS
Assess whether the 10 exemplars support scaling without registry explosion.

### K. NEXT-STEP VERDICT
Choose exactly one:
- GO TO WAVE 2 ROLE-TO-SKILL MAPPING
- GO TO ONE MORE EXEMPLAR ROUND
- GO AFTER LISTED CHANGES
- NO-GO

### L. MASS-GENERATION VERDICT
Choose exactly one:
- NOT YET — KEEP SELECTIVE
- SAFE FOR CONTROLLED BATCH GENERATION
- SAFE FOR MASS GENERATION

Do not edit anything.