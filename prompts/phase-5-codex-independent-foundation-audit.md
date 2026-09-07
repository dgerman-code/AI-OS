# Codex Prompt — Independent Phase 5 Workflow Registry Foundation Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-5-workflow-registry`
Foundation baseline commit: `17c95ac191c66a7f18cc13421480e44ef46a6af8`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 5 APPROVED or CANONICAL.

This is an independent architecture audit of the Phase 5 Workflow Registry foundation.

Read at minimum:
- `architecture/workflow-registry-design.md`
- `workflows/_standards/common-workflow-constraints.md`
- `workflows/_templates/workflow-card-template.md`
- `workflows/master-workflow-universe.md`
- all four files in `workflows/exemplars/`
- `reviews/phase-5-foundation-self-check.md`
- approved Phase 3 Role architecture and approved Phase 4 Skill Registry artifacts only as needed for compatibility / authority verification

## 1. Workflow identity and phase boundary
Verify that:
- `ROLE != SKILL != WORKFLOW != REVIEW PROFILE != DECISION RIGHT != MODEL != RUNTIME` is consistently enforced;
- Workflow is coordination/state-transition architecture, not a hidden Role, Skill, Review Profile, approval right, System Control Profile or runtime program;
- no workflow can expand Role scope, Skill compatibility, authority, review independence or decision rights;
- Phase 5 does not implement runtime, orchestration, persistence, model routing, database schema or agent binding;
- Phase 3 Role Cards and approved Phase 4 architecture were not altered.

## 2. Authority leakage audit
Stress-test every exemplar and the common standard for hidden authority transfer.

Check specifically that:
- Workflow Lead means coordination only;
- stage completion never implies `REVIEWED`, `APPROVED` or `CANONICAL`;
- `HUMAN_GATE_REFERENCE` references an external right rather than defining/awarding one;
- `REVIEW_REQUIRED_REFERENCE` does not define reviewer identity or independence;
- external submission, production release, legal commitment, financial commitment, grant submission and other hard-to-reverse acts preserve human gates;
- exception/emergency paths never bypass gates;
- AI outputs remain `AI_SUGGESTION` / `DRAFT` until governed action changes state;
- unresolved `CONFLICT_DETECTED`, `UNKNOWN`, or material assumptions cannot silently disappear through workflow progress.

Report every phrase that could reasonably be read as granting authority even if another section tries to disclaim it.

## 3. Workflow composition model
Audit the 12 primitives and the seven-stage-question requirement.

Determine whether the foundation can represent, without runtime semantics:
- sequential flow;
- conditional branching;
- parallel work;
- rework;
- exceptions;
- termination/cancellation;
- completion with open items;
- nested or reusable workflow composition.

Pay special attention to the foundation's declared open question about composition. Decide whether composition is:
- a BLOCKER for Phase 5 foundation approval;
- a REQUIRED CHANGE before approval;
- safely DEFERRED to a later Phase 5 refinement / runtime phase.

Do the same for partial-order notation, trigger vocabulary, workflow version binding, open-item severity, parameterized Role identity, and System Control Profile interaction.

Do not treat an explicitly deferred runtime concern as a defect unless the architecture already needs that semantic to remain coherent.

## 4. Participation vocabulary
Audit `LEAD_ROLE`, `CONTRIBUTING_ROLE`, `CONSULTED_ROLE`, `REVIEW_REQUIRED_REFERENCE`, `HUMAN_GATE_REFERENCE`.

Verify:
- the five concepts are mutually understandable and sufficient at foundation level;
- none smuggles RACI-style Accountable/Approver semantics into a Role;
- contributing vs consulted is applied consistently in all exemplars;
- a Role may lead coordination without owning every conclusion;
- participation statements do not override Role Cards or artifact ownership.

## 5. Workflow universe quality
Independently assess all 49 candidates and 7 rejected candidates.

Classify each candidate conceptually as one of:
- VALID WORKFLOW
- LIKELY WORKFLOW BUT NEEDS BOUNDARY REFINEMENT
- SKILL / METHOD IN DISGUISE
- ROLE / SYSTEM CONTROL IN DISGUISE
- SINGLE GATE / SOP / EVENT, NOT WORKFLOW
- RUNTIME / IMPLEMENTATION CONCERN
- DUPLICATE / OVERLAPPING WORKFLOW

You do not need to create 49 cards. But audit the universe for systemic over-fragmentation and duplication.

For the 8 overlap groups:
- identify whether the overlap is acceptable taxonomy breadth, or likely duplicate identity;
- identify any pair/group that must be resolved before human approval;
- do not force premature merges if evidence is insufficient.

## 6. Exemplar stress tests
Audit each exemplar independently:

A. `workflow.project_development_readiness`
- specialist conclusions remain with specialist Roles;
- integrator does not rewrite or settle specialist disagreement;
- readiness aggregation does not become an approval right;
- criticality only changes depth/controls, not Role identity.

B. `workflow.eu_grant_application_development`
- deadline pressure cannot remove evidence/review/human gates;
- rule/call-version change causes valid rework;
- grant submission authority is external;
- Pack activation does not become a programme-specific workflow identity explosion.

C. `workflow.software_change_delivery`
- build/test/deploy workflow does not authorize production release;
- Security Engineer boundaries from Phase 4 remain intact;
- emergency release remains gated;
- DevOps / engineering coordination does not become decision authority.

D. `workflow.decision_grade_document_preparation`
- generic document workflow remains composable and does not absorb domain methodology;
- `FACT`, `ASSUMPTION`, `CALCULATION`, `AI_SUGGESTION` boundaries are preserved;
- parameterized Document Owner Role does not create an unconstrained dynamic Role loophole;
- traceability/evidence stewardship remains separate from domain conclusion ownership.

## 7. State and completion semantics
Audit the distinction between:
- workflow-instance progress outcome; and
- knowledge/artifact governance state.

Check `COMPLETE_WITH_OPEN_ITEMS` closely.

Determine whether the absence of an explicit severity model creates a dangerous loophole whereby material blockers could be labeled open items and workflow declared complete.

If current per-card criticality rules are sufficient, say so. If not, state the minimal architecture rule required.

## 8. Reference integrity
Recompute / verify all identifiers referenced by exemplars:
- `role.*`
- `skill.*`
- `specialisation.*`
- `skill_pack.*`
- `review.*`
- `decision.*`
- `artifact.*`

Distinguish:
- valid existing registry IDs;
- deliberate forward references reserved for Phase 6/7;
- truly undefined/invalid references.

Forward reference is not automatically a defect if Phase 5 explicitly treats it as an external unresolved registry dependency and does not fabricate its semantics.

## 9. Granularity and maintainability
Assess whether:
- 49 candidates / 9 families is a maintainable foundation;
- workflow identity is stable enough not to explode per project size, sector, EU programme, model, customer, or tool;
- criticality and Pack activation are correctly treated as context/depth modifiers rather than new workflow identity where appropriate;
- the four exemplar cards are enough for foundation approval without mass card generation.

## 10. Open architecture questions
For each of the seven open questions in the self-check, return exactly one disposition:
- BLOCKER NOW
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- RUNTIME-PHASE CONCERN
- PHASE 6 CONCERN
- PHASE 7 CONCERN

Provide one-sentence rationale for each.

## 11. Approval threshold
Use a strict threshold:
- FAIL if there is authority leakage, registry identity confusion, phase-boundary breach, or an unresolved architectural ambiguity that makes Workflow Cards unsafe to scale;
- PASS WITH CHANGES if the foundation is sound but bounded textual/rule corrections are required;
- PASS WITH NON-BLOCKING NOTES if only future refinements remain;
- PASS only if no material finding remains.

Do not recommend mass card generation merely because the foundation passes.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. HIGH / MEDIUM FINDINGS
List findings with severity and exact affected files/sections.

### C. IDENTITY / PHASE BOUNDARY
PASS / FAIL + explanation.

### D. AUTHORITY LEAKAGE
PASS / FAIL + every material authority concern.

### E. COMPOSITION / STATE SEMANTICS
PASS / FAIL + dispositions for composition, partial order, version binding, trigger vocabulary, open-item severity, parameterization, System Control interaction.

### F. PARTICIPATION MODEL
PASS / FAIL + findings.

### G. WORKFLOW UNIVERSE
Counts, duplicate/overlap findings, rejected-candidate quality, any required universe changes.

### H. EXEMPLAR AUDIT
A / B / C / D each PASS / FAIL with concise findings.

### I. REFERENCE INTEGRITY
Existing IDs / deliberate forward refs / invalid refs counts and findings.

### J. OPEN QUESTIONS DISPOSITION
All seven questions with one allowed disposition each.

### K. REMAINING BLOCKERS
If none: NONE.

### L. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 5 FOUNDATION
- READY AFTER LISTED CHANGES
- NOT READY

### M. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.