# Codex Prompt — Independent Phase 7 Decision Rights Foundation Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-7-decision-rights`
Foundation baseline commit: `1db348c90fb7f6ba9d78b4c346ae1e4a9a05c0e4`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 7 APPROVED or CANONICAL.

This is an independent architecture audit of the Phase 7 Decision Rights / Human Approval Matrix foundation.

Read at minimum:
- `architecture/decision-rights-registry-design.md`
- `decisions/_standards/common-decision-right-constraints.md`
- `decisions/_templates/decision-right-card-template.md`
- `decisions/_templates/decision-record-template.md`
- `decisions/master-decision-right-universe.md`
- all eight `decisions/exemplars/*.md`
- `reviews/phase-7-foundation-self-check.md`
- approved Phase 3 Role, Phase 4 Skill, Phase 5 Workflow, and Phase 6 Handoff/Review artifacts only as needed for regression/reference/authority verification.

The producer self-check reports 50/50 PASS but explicitly leaves one issue classified `MUST RESOLVE IN PHASE 7 FOUNDATION`: separation of duties across related Decision Rights. Treat that as an open architecture finding to adjudicate independently, not as an assumed blocker or non-blocker.

## 1. Identity / phase boundary

Verify:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != DECISION RECORD != MODEL != RUNTIME`

PASS only if:
- Decision Right is a reusable bounded human authority definition, not a Role/reviewer/Workflow/model/runtime permission;
- Decision Record is a concrete decision instance/evidence record, not the Right itself;
- Phase 7 does not expand Role competence or Phase 4 capability scope;
- no Decision Right creates a professional conclusion;
- no named human, organisation, provider/model, runtime identity, IAM permission, DB/API/UI is bound;
- approved Phase 3/4/5/6 artifacts are unchanged.

## 2. Decision subject/effect boundedness

Audit the architecture, template and all eight exemplar cards.

Verify:
- every Decision Right has a bounded subject;
- every Decision Right has a bounded effect;
- no generic “approve project / approve anything” semantics exist;
- each allowed outcome has an explicit effect on Workflow, Handoff, external act, Review status, knowledge state, conditions/open items, and expiry/re-decision where relevant;
- `APPROVE_WITH_CONDITIONS` never closes conditions by mere recording;
- `DEFER` / `ESCALATE` do not falsely satisfy a gate;
- rejection/cancellation semantics are not smuggled into unrelated Rights without explicit bounded effect.

## 3. Holder eligibility and authority leakage

Audit all holder eligibility classes and exemplar usage.

Verify:
- Role competence != Decision Right authority;
- Workflow LEAD_ROLE != approval authority;
- reviewer != Decision Right holder by virtue of reviewing;
- artifact owner != external commitment authority;
- holder eligibility derives from authority basis, not subject-matter expertise alone;
- if no eligible holder exists, decision remains unmade;
- legal entity signatory authority is required where a Right binds the entity externally;
- governance-body authority is not treated as one member acting alone;
- no exemplar silently maps an upstream Role directly to a Decision Right merely because the Role owns the work.

Report any authority-leakage count.

## 4. Cardinality / collective authority

Verify four cardinality modes are safe:
- `SINGLE_HOLDER`
- `MULTI_HOLDER_ALL_REQUIRED`
- `MULTI_HOLDER_THRESHOLD`
- `GOVERNANCE_BODY_DECISION`

Check:
- cardinality cannot be bypassed by delegation;
- one human cannot count twice under two labels in one decision instance;
- threshold semantics are declarative/testable;
- absent required holders means decision not made;
- governance-body decision is not equivalent to one officer acting alone;
- multi-holder rules do not become runtime voting logic.

## 5. Delegation / revocation / supersession

Audit:
- `NON_DELEGABLE`
- `DELEGABLE_WITHIN_ELIGIBILITY`
- `DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`

Verify:
- delegation transfers only declared Decision Right scope;
- delegation never widens subject/effect;
- delegation cannot bypass cardinality or holder-class requirements;
- default re-delegation is prohibited unless explicitly permitted;
- delegation expiry/revocation affects future exercise only;
- revoked delegation does not erase historical valid decisions;
- decision correction uses a new linked Decision Record, not mutation;
- supersession/reversal retain historical records and require explicit authority.

## 6. Decision Record / gate satisfaction

Audit the 18-element Decision Record model and gate semantics.

PASS only if:
- a gate is satisfied only by an attributable valid Decision Record under an existing Decision Right;
- holder/cardinality/prerequisite/evidence/outcome requirements are all required;
- request/meeting/email is not sufficient by itself;
- invalid/missing authority => gate unsatisfied;
- `DEFER`, `ESCALATE`, `REJECT` do not satisfy positive gate unless explicitly defined otherwise;
- exceptional path is explicit and auditable;
- open findings/reviews/risks at decision time are preserved in the record;
- Decision Record semantics remain architecture-level, not DB schema.

Identify any “meeting/email = approval” loophole count.

## 7. Review / knowledge-state boundary

Verify:
- Decision Right may permit progression while Review remains `NOT_SATISFIED`, but cannot change it to `SATISFIED`;
- Decision Right may accept risk but cannot erase risk/finding;
- generic approval cannot make artifact `CANONICAL`;
- `UNKNOWN` cannot become FACT;
- `ASSUMPTION` cannot become FACT;
- `CONFLICT_DETECTED` cannot be declared resolved by authority alone;
- `AI_SUGGESTION` cannot become canonical without governed human decision plus required controls;
- canonical promotion remains correctly deferred/bounded relative to Phase 8.

## 8. Exceptional progression

Stress-test `decision.exceptional_progression` and generic rules.

PASS only if:
- one concrete unresolved item/finding/risk is named;
- the scope is one bounded progression point/context, not a blanket waiver;
- unresolved item remains open downstream;
- review status remains unchanged;
- consequences/conditions are recorded;
- expiry/revisit trigger is present where applicable;
- no fictional resolution occurs;
- `APPROVE` without conditions is disallowed if the card intentionally requires conditions, and the rationale is coherent;
- Decision Right cannot waive mandatory law/regulation.

Report any “permit progression = resolve issue” loophole count.

## 9. Risk acceptance / waiver boundary

Audit `decision.risk_acceptance` and shared rules.

Verify:
- risk acceptance is distinct from progression approval;
- risk acceptance is distinct from process waiver;
- risk remains recorded after acceptance;
- acceptance scope/class is bounded;
- expiry/review trigger exists where relevant;
- law/regulation cannot be waived;
- Review finding remains a finding;
- acceptance does not itself authorize release/submission/publication/contractual commitment unless a separate Right exists.

## 10. Emergency authority

Stress-test `decision.emergency_production_change` and generic emergency architecture.

PASS only if:
- emergency trigger is objective and bounded;
- urgency/deadline alone is not authority;
- bypassable and non-bypassable prerequisites are explicit;
- emergency authority is pre-defined, not invented during the incident;
- emergency use is temporary;
- skipped reviews remain skipped/open and are not retroactively satisfied;
- retrospective obligations are mandatory;
- historical emergency decision is not rewritten by retrospective review;
- emergency Right remains distinct from ordinary `decision.production_release`.

## 11. Cancellation / termination / reversal

Audit architecture and universe handling.

Verify:
- Workflow cannot create its own cancellation authority;
- cancellation/termination preserves history, open items, prior decisions and commitments;
- reversal is not implied automatically by the original Right unless explicitly permitted;
- pause/suspend/reject/rework/cancel are not conflated;
- `decision.cancellation_or_termination` architecture gap candidate is bounded enough to remain a valid candidate rather than a universal kill-switch.

## 12. Decision dependencies

Audit whether current bounded prerequisite model is sufficient.

If dependencies are allowed, verify:
- concrete `decision.<id>` prerequisite;
- required prior outcome/status declared;
- authority and satisfaction are non-transitive;
- no authority transfer;
- direct/transitive cycles prohibited;
- no runtime call-stack semantics;
- multi-holder/dual-control is modeled with cardinality where appropriate, not chains of pseudo-decisions.

## 13. Separation-of-duties across related Decision Rights — REQUIRED ADJUDICATION

The producer self-check flags this as the principal unresolved foundation issue.

Question:
> May the same human exercise multiple Decision Rights in one related decision chain when those Rights are intended as independent controls?

Example hazard:
- the same holder accepts residual risk under `decision.risk_acceptance` and then authorizes `decision.production_release` for the same change carrying that risk.

Audit independently and choose one disposition:
- BLOCKER NOW
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- RUNTIME/ORGANISATION-PHASE CONCERN

Then state the **minimal architecture rule** required.

At minimum consider:
- some Rights may legitimately be exercised by the same human;
- some paired Rights should require `SEPARATION_REQUIRED` or equivalent;
- separation should be declared at Decision Right relationship level, not inferred from job title;
- one Right's holder eligibility must not create eligibility for another;
- same-person use must be evaluated per decision instance/context;
- multi-holder cardinality inside one Right does not solve separation **between** two Rights;
- decision-grade/high-criticality or external-commitment chains may need stronger defaults;
- do not invent runtime staffing algorithms.

If you judge this resolvable with a small registry rule/property, specify it precisely.

## 14. Human Approval Matrix consistency

Audit all eight exemplar rows.

Verify consistency among:
- Decision Right ID;
- class;
- subject;
- holder eligibility;
- cardinality;
- delegation;
- upstream trigger;
- required review state;
- external commitment flag;
- exceptional progression flag;
- risk acceptance flag;
- knowledge-state effect.

Report matrix/card discrepancies count.

## 15. Decision Universe quality

Independently assess:
- 9 families;
- 35 candidate Rights;
- 95 upstream `decision.<id>` references accounted for;
- 33 candidates preserving upstream IDs;
- 2 architecture-gap candidates;
- 34 `LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT`;
- 10 Review/quality gates in disguise;
- 8 Role responsibilities in disguise;
- 4 Workflow progression logic in disguise;
- 2 runtime/IAM in disguise;
- 3 executive-policy items outside Phase 7.

For each candidate conceptually classify as:
- VALID DECISION RIGHT
- LIKELY DECISION RIGHT NEEDS BOUNDARY REFINEMENT
- REVIEW / QUALITY GATE IN DISGUISE
- ROLE RESPONSIBILITY IN DISGUISE
- WORKFLOW PROGRESSION LOGIC IN DISGUISE
- RUNTIME / IAM IN DISGUISE
- EXECUTIVE POLICY / ORGANISATIONAL POLICY
- DUPLICATE / OVERLAP

Do not mass-card. Identify any candidate that is dangerously broad or actually a review/runtime/role responsibility.

## 16. Exemplar audit

Audit each of the eight exemplar Decision Rights independently:
1. `decision.exceptional_progression`
2. `decision.stage_gate_progression`
3. `decision.granting_authority_submission`
4. `decision.external_publication`
5. `decision.contract_commitment`
6. `decision.risk_acceptance`
7. `decision.production_release`
8. `decision.emergency_production_change`

For each verify:
- bounded subject/effect;
- holder eligibility;
- cardinality;
- delegation;
- prerequisites;
- evidence;
- outcome effects;
- review/knowledge-state boundaries;
- out-of-scope authority;
- expiry/re-decision;
- no authority leakage.

## 17. Reference integrity

Verify all concrete references in the eight exemplar cards:
- `role.*`
- `artifact.*`
- `review.*`
- `workflow.*`
- `handoff.*`
- `decision.*`

Classify as:
- valid approved upstream IDs;
- valid Phase 7 candidate IDs;
- deliberate Phase 8 forward canonical-governance references if any;
- invalid/undefined.

Invalid concrete refs must be 0.

## 18. Upstream / non-runtime regression

Verify:
- Phase 3 Role changes = 0;
- approved Phase 4 architecture/mapping changes = 0;
- approved Phase 5 Workflow semantic changes = 0;
- approved Phase 6 Handoff/Review semantic changes = 0;
- all Phase 7 artifacts remain `PROPOSED`;
- no DB/API/UI/runtime/orchestrator/model/agent/IAM implementation;
- no named human/organisation assignment;
- no PR.

## 19. Open architecture questions — dispositions

For all ten producer questions, return exactly one:
- BLOCKER NOW
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 8 CONCERN
- RUNTIME/ORGANISATION-PHASE CONCERN

Questions:
1. organisational authority eligibility fully registry-defined vs organisation-specific;
2. one human exercising multiple Rights in one chain;
3. mandatory separation of duties between some Rights;
4. abstention/dissent semantics;
5. global vs Right-specific approval expiry;
6. shared risk-class ceiling model;
7. canonical promotion here vs Phase 8;
8. first-class Decision Right composition vs bounded prerequisites;
9. emergency retrospective ratification as new Right vs review/dependency;
10. reversal as new Right vs outcome of original Right.

Do not inherit producer dispositions automatically.

## 20. Approval threshold

Use a strict threshold:
- FAIL if authority can be inferred from Role/reviewer/workflow ownership, Decision Right can alter truth/review status, delegation/cardinality can be bypassed, gate can be satisfied without valid authority/evidence, emergency/risk/exception semantics allow fictional resolution, or separation-of-duties ambiguity makes high-criticality use unsafe;
- PASS WITH CHANGES if architecture is fundamentally sound but bounded corrections are required before human approval;
- PASS WITH NON-BLOCKING NOTES if only Phase 8/runtime/organisation-specific refinements remain;
- PASS if no material issue remains.

Do not recommend mass Decision Right card generation merely because foundation passes.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. HIGH / MEDIUM FINDINGS
List severity + exact files/sections.

### C. IDENTITY / PHASE BOUNDARY
PASS / FAIL + explanation.

### D. SUBJECT / EFFECT BOUNDEDNESS
PASS / FAIL + loophole count.

### E. HOLDER / CARDINALITY / DELEGATION
PASS / FAIL + authority-leakage/cardinality/delegation findings.

### F. DECISION RECORD / GATE SATISFACTION
PASS / FAIL + invalid gate-satisfaction loophole count.

### G. REVIEW / KNOWLEDGE-STATE BOUNDARY
PASS / FAIL + findings.

### H. EXCEPTION / RISK / EMERGENCY
PASS / FAIL + findings for all three domains.

### I. SEPARATION OF DUTIES
Disposition + minimal architecture rule + whether it blocks approval.

### J. DECISION DEPENDENCY / REVERSAL / CANCELLATION
PASS / FAIL + findings.

### K. HUMAN APPROVAL MATRIX
PASS / FAIL + discrepancy count.

### L. DECISION UNIVERSE
Counts, classifications, overlaps/broad candidates, required changes if any.

### M. EXEMPLAR AUDIT
Eight Decision Rights, each PASS / FAIL with concise finding.

### N. REFERENCE INTEGRITY
Existing upstream / Phase 7 / Phase 8 forward / invalid counts.

### O. OPEN QUESTIONS DISPOSITION
All ten questions with one allowed disposition each.

### P. REMAINING BLOCKERS
If none: NONE.

### Q. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 7 FOUNDATION
- READY AFTER LISTED CHANGES
- NOT READY

### R. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.