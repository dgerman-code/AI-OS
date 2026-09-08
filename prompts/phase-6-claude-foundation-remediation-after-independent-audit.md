# Claude Code Prompt — Phase 6 Foundation Remediation After Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-6-handoff-review`
Audited foundation baseline: `cd3f3fcd25a20a1bb0a24c556681079209deb5b0`
Independent audit prompt commit currently on branch: `f406567eb44131e7acd2268b0e24c05fce1992f3`

The independent Phase 6 audit returned **FAIL** with three HIGH and three MEDIUM findings. Upstream Phase 3/4/5 immutability, the core Handoff identity model, `review.security`, `review.legal_compliance`, reference integrity, and non-runtime boundaries otherwise passed.

This is one **bounded consolidated remediation**. Fix H1–H3 and M1–M3 only, plus any wording directly required for consistency. Do not redesign Phase 6 broadly.

Do not modify approved Phase 3 Role Cards.
Do not modify approved Phase 4 architecture/mappings.
Do not modify approved Phase 5 Workflow semantics.
Do not create or exercise Decision Rights.
Do not implement runtime/database/API/UI/orchestrator/model/agent logic.
Do not create a PR.
Do not mark Phase 6 APPROVED or CANONICAL.
Do not bulk-card additional Review Profiles or Handoffs.

All Phase 6 artifacts remain `PROPOSED`.

---

# H1 — Project Integration Coherence satisfaction/closure loophole

Affected:
- `reviews/exemplars/project-integration-coherence.md`
  - Satisfaction Criteria
  - Rework and Closure Requirements

Current defect: the Profile can be read as satisfied/closed when a contradiction is merely recorded or carried to a decision-maker, despite unresolved `MAJOR_FINDING` / `CRITICAL_FINDING` semantics.

Required correction:

1. An unresolved material contradiction remains an **open review finding**.
2. While such a contradiction remains unresolved:
   - review status is `NOT_SATISFIED` or `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`;
   - it cannot become `SATISFIED` merely because the contradiction is recorded, visible, attributed, escalated, or carried to a human gate.
3. A named external human `decision.<id>` may permit **Workflow progression** with the contradiction unresolved, but:
   - it does not close the finding;
   - it does not satisfy the review;
   - it does not convert the contradiction into a minor/non-material item;
   - the contradiction remains open and carried forward.
4. Closure requires evidence that the owning domain Roles have actually reconciled or otherwise resolved the contradiction according to the Profile criteria, followed by required re-review where applicable.
5. The integration reviewer must not settle the underlying specialist disagreement itself.

Remove every phrase equivalent to "record/carry/escalate the contradiction and count the review satisfied/closed."

---

# H2 — EU Programme Compliance “record it and continue” loopholes

Affected:
- `reviews/exemplars/eu-programme-compliance.md`
  - Review Scope
  - Satisfaction Criteria

Correct three ambiguous classes:

## Rulebook requirements
Distinguish:
- **verified not applicable** with evidence and rationale -> may support satisfaction;
- **unmet / unresolved requirement** -> open finding, normally `MAJOR_FINDING`, review not satisfied.

Merely recording a requirement as a gap is never sufficient.

## Eligibility conditions
Distinguish:
- eligibility condition assessed and **satisfied** -> may support satisfaction;
- eligibility condition verified **not applicable** where the programme rules genuinely permit N/A -> may support satisfaction;
- eligibility condition unmet, unknown, unassessed, or evidenced as `not-satisfied` -> review not satisfied.

Do not treat “evidenced status” by itself as success.

## Factual claims
Distinguish:
- material claim verified against required evidence -> may support satisfaction;
- claim explicitly identified as non-material and permitted by Profile criteria -> bounded handling allowed;
- material claim merely “marked,” flagged, or recorded but still unverified -> open finding; review not satisfied.

No wording may permit a material unresolved rule, eligibility condition, or claim to satisfy the Profile by visibility alone.

Decision Right boundary remains: a human gate may permit progression without changing review status.

---

# H3 — Reviewer eligibility must not widen upstream Role scope

Affected at minimum:
- `reviews/exemplars/evidence-integrity-provenance.md`
- `reviews/exemplars/financial-model.md`
- `reviews/exemplars/eu-programme-compliance.md`
- and template/standards if needed to establish the generic rule.

Add a registry-wide distinction between:

1. **FULL_PROFILE_REVIEWER_ELIGIBLE**
2. **BOUNDED_REVIEW_CONTRIBUTOR / CROSS_DOMAIN_REVIEW_ONLY**

Names may be refined, but semantics must be explicit.

Generic rule:

- A Role may satisfy an entire Review Profile only if its **approved Role scope already covers every satisfaction criterion and professional conclusion required by that Profile**.
- Partial expertise does not aggregate into full Profile authority automatically.
- A Role whose approved scope covers only one dimension may contribute a bounded `CROSS_DOMAIN_REVIEW` or evidence/reconciliation check for that dimension, but **cannot satisfy the whole Profile**.
- Phase 6 never widens Role scope.
- Profile wording cannot make a Role eligible by declaration alone.
- If no approved Role/assignment instance is fully eligible, the Profile remains unsatisfied unless the Profile explicitly requires a multi-reviewer composition that is itself governed by declared bounded contribution rules. Do not invent cross-role authority by aggregation.

Apply specifically:

## `review.evidence_integrity_provenance`
- `role.data_room_disclosure_manager` must not be presented as capable of satisfying epistemic/evidential-quality criteria excluded by its Role Card.
- If useful, retain it only for bounded provenance/disclosure/package integrity dimensions.
- Any accounting/financial evidence specialist must likewise be bounded to reconciliation/evidence dimensions unless its Role Card covers the entire Profile.

## `review.financial_model`
- `role.accounting_financial_due_diligence_specialist` must be explicitly **partial-scope only** for reconciliation, accounting tie-out, evidence consistency, or due-diligence dimensions unless upstream Role scope actually covers full financial-model integrity.
- Full Profile satisfaction must remain with an independently eligible Role whose approved scope includes financial modelling methodology.

## `review.eu_programme_compliance`
- `role.grant_financial_compliance_budget_specialist` remains bounded to budget/cost-eligibility/financial-compliance criteria.
- Remove any phrase equivalent to “eligible for the rest” unless upstream Role scope actually covers the complete Profile.
- Other specialist Roles must remain bounded to their own compliance dimensions.

Audit all six exemplars for the same defect, not only the three named by Codex.

---

# M1 — Multi-Profile reviewer-instance rule

Resolve this in Phase 6 foundation before human approval.

Add a generic normative rule to:
- `architecture/handoff-review-registry-design.md`
- `reviews/_standards/common-review-constraints.md`
- `reviews/_templates/review-profile-card-template.md`
- `reviews/phase-6-foundation-self-check.md`

Required semantics:

A single reviewer instance **may** satisfy multiple Review Profiles only if all of the following are independently true **for each Profile, subject, artifact version, and assignment**:

1. reviewer eligibility passes separately for each Profile;
2. independence passes separately for each Profile;
3. satisfaction of one Profile grants no eligibility, authority, scope, or satisfaction for another;
4. the reviewer does not review its own output from another Profile where that output becomes subject/evidence of the second review;
5. no Profile involved declares `SEGREGATION_REQUIRED`;
6. no declared inter-profile dependency or conflict-of-interest condition requires separate instances;
7. combining Profiles does not create cross-domain professional authority by accumulation.

Add a Review Profile field/property equivalent to:

`Reviewer Instance Segregation: ALLOWED_IF_INDEPENDENTLY_ELIGIBLE | SEGREGATION_REQUIRED`

For decision-grade/high-criticality work covering **interdependent domains**, default to `SEGREGATION_REQUIRED` unless the Profile explicitly and defensibly states that same-instance review preserves required separation.

Do not define staffing algorithms or human assignments. This is architecture eligibility only.

Apply the field to all six exemplar Profiles with a reasoned value.

Be conservative for `review.project_integration_coherence` and `review.security` where concentration of assurance would defeat the purpose.

---

# M2 — Declarative Review Profile dependency model

Resolve before human approval.

Add one bounded declarative dependency concept, without runtime execution semantics.

Suggested primitive/property:

`REVIEW_DEPENDENCY`

A dependency declaration must include:

- concrete prerequisite `review.<id>`;
- required prerequisite status (normally `SATISFIED`);
- objective activation condition if conditional;
- bounded purpose of the dependency.

Normative rules:

1. An unsatisfied, `STALE`, or missing required prerequisite causes the dependent review to be `REVIEW_BLOCKED`, not substantively failed.
2. Satisfaction is **not transitive**. A satisfied prerequisite does not satisfy the dependent Profile.
3. Dependency transfers no scope, reviewer eligibility, authority, findings, professional conclusion, or satisfaction.
4. Direct self-dependency is prohibited.
5. Transitive cycles are prohibited as an architecture validation rule.
6. Conditional dependencies use objective/testable triggers only.
7. Dependency does not execute another review and creates no scheduling/call-stack/runtime semantics.
8. A dependent Profile must still evaluate its own evidence and satisfaction criteria independently.

Update:
- architecture;
- common review constraints;
- review template;
- exemplars where a real dependency already exists or is semantically justified.

Do **not** force artificial dependencies into every exemplar. `None` with reason is valid.

---

# M3 — Closed Handoff sender eligibility

Affected:
- `handoffs/exemplars/application-content-to-compliance-review.md`

Current defect: “each conditionally activated specialist Role” is not a closed, testable sender set.

Fix with one of these two bounded approaches, preferring the simpler honest one:

## Option A — Explicit enumeration
Enumerate every possible sender `role.<id>` that this Handoff permits, with its objective activation trigger and exact artifact/package contribution.

## Option B — Closed Handoff Role Slot
Only if enumeration would be structurally wrong, add a **closed Handoff Role Slot** rule analogous in strictness to Phase 5 Role Slot Binding:
- slot has stable ID/name;
- permitted source = approved concrete `role.<id>` only;
- eligibility derives from declared Role-owned artifact/interface;
- objective activation condition;
- cardinality;
- cannot grant ownership or capability;
- cannot bind Review Profile, Decision Right, System Control, model, runtime identity;
- no eligible Role => package incomplete / `HANDOFF_BLOCK`, never wildcard widening.

Do not use an unbounded phrase such as “any relevant specialist.”

Given the current card is a known grant-application handoff, **prefer explicit enumeration** unless the actual source structure demonstrates a genuine reusable slot need.

---

# Universe / consolidation constraints

Do not apply the four proposed consolidations in this remediation.

Record the independent audit constraints in the universe or remediation record:

- `grant_compliance -> eu_programme_compliance`: not safe without proving all grant contexts are EU-programme contexts;
- `ifi_appraisal_readiness -> bankability`: may lose IFI-specific safeguard/procurement/institutional-compliance scope;
- `ppp_structure -> commercial_structure`: may collapse public-interest/procurement/legal/value-for-money review into a commercial mega-review;
- `financial_evidence -> factual_evidence`: plausible only if financial reconciliation requirements remain explicit.

Keep:
- 9 families;
- 34 standalone candidate IDs unless a direct defect forces otherwise;
- 6 exemplar Review Profiles;
- 4 exemplar Handoffs;
- 6 overlap groups visible/open.

No additional carding.

---

# Open-question dispositions after remediation

Update the Phase 6 self-check so these are no longer falsely shown unresolved:

1. First-class Review Profile dependency reference -> **RESOLVED IN FOUNDATION** via bounded `REVIEW_DEPENDENCY`.
2. One Profile requiring another as prerequisite -> **RESOLVED IN FOUNDATION** via dependency semantics.
3. One reviewer instance satisfying multiple compatible Profiles -> **RESOLVED IN FOUNDATION** via per-Profile eligibility/independence + segregation rule.
4. Organisational independence eligibility -> **SAFE TO DEFER WITH EXPLICIT RULE**. Phase 6 assignment-level independence remains mandatory; organisational authority/delegation structures are not invented here.
5. Shared vs Profile-specific staleness -> **SAFE TO DEFER WITH EXPLICIT RULE**; Profile-specific triggers remain normative for now.
6. Handoff Cards first-class vs embedded -> **SAFE TO DEFER WITH EXPLICIT RULE**; first-class cards are used only for reusable governed transfer semantics, while one-off stage glue stays Workflow prose.
7. Runtime observation/recording of review satisfaction -> **RUNTIME-PHASE CONCERN**.
8. Exceptional progression via Decision Rights while review remains unsatisfied -> **PHASE 7 CONCERN**, with standing Phase 6 rule that progression never converts unsatisfied review to satisfied.

---

# Required remediation record

Create:

`reviews/phase-6-foundation-audit-remediation.md`

Status:

`PROPOSED — READY FOR FINAL INDEPENDENT PHASE 6 FOUNDATION RE-AUDIT`

Record:
- H1–H3 exact corrections;
- M1–M3 exact corrections;
- files changed;
- open-question disposition updates;
- universe/consolidation constraints;
- regression validation results.

---

# Validation — minimum 36 checks

Run at least these checks and add more if useful:

1. H1 unresolved material contradiction cannot support `SATISFIED`.
2. H1 Decision Right exceptional progression does not close finding.
3. H1 integration reviewer cannot settle domain disagreement.
4. H2 unresolved rulebook gap cannot support `SATISFIED`.
5. H2 unmet/unknown eligibility cannot support `SATISFIED`.
6. H2 unverified material claim cannot support `SATISFIED`.
7. Verified N/A is distinct from unresolved gap.
8. Full-profile reviewer eligibility requires upstream Role scope covering all satisfaction criteria.
9. Partial-scope reviewer/contributor cannot satisfy whole Profile.
10. Evidence Integrity/Data Room eligibility is bounded correctly.
11. Financial Model/Accounting-Due-Diligence eligibility is bounded correctly.
12. EU Programme financial-compliance specialist is bounded correctly.
13. All six exemplar reviewer eligibility tables pass the no-scope-widening rule.
14. Multi-Profile rule exists in architecture.
15. Multi-Profile rule exists in common constraints.
16. Multi-Profile field exists in template.
17. All six exemplars declare segregation semantics.
18. Eligibility/independence evaluated separately per Profile/subject/version/assignment.
19. Satisfaction of one Profile does not grant anything to another.
20. Same reviewer cannot review own output from another Profile where independence would be compromised.
21. `SEGREGATION_REQUIRED` blocks same-instance satisfaction.
22. High-criticality interdependent-domain default separation is explicit.
23. `REVIEW_DEPENDENCY` exists declaratively.
24. Dependency targets concrete `review.<id>`.
25. Unsatisfied/stale prerequisite -> `REVIEW_BLOCKED`.
26. Satisfaction is non-transitive.
27. Dependency transfers no authority/scope/eligibility/findings/satisfaction.
28. Direct/transitive dependency cycles prohibited.
29. Dependency adds no runtime execution semantics.
30. Application-compliance Handoff sender set is explicit or closed-bound.
31. No wildcard/unbounded sender phrase remains.
32. Handoff ownership semantics unchanged and safe.
33. `RECEIVED` semantics unchanged and safe.
34. `review.security` single-producing-Security-Engineer case remains safe.
35. `review.legal_compliance` boundaries remain intact.
36. Phase 3 Role changes = 0.
37. Approved Phase 4 architecture/mapping changes = 0.
38. Approved Phase 5 Workflow semantic changes = 0.
39. All Phase 6 artifacts remain `PROPOSED`.
40. No runtime/database/API/UI/orchestrator/model/agent implementation.
41. Candidate Review Profiles remain 34 unless explicitly justified otherwise.
42. Review families remain 9.
43. Exemplar Review Profiles remain 6.
44. Exemplar Handoffs remain 4.
45. Existing overlap groups remain visible/open.
46. Proposed consolidations remain unapplied.
47. Invalid concrete refs = 0.
48. Phase 7 `decision.*` refs remain forward references, not authority definitions.
49. No new professional authority granted by Phase 6.
50. No PR created.

Do not weaken a test to make it pass. If a test is wrong, document why and replace it with a stricter correct test.

---

# Commit / push

If and only if the remediation is complete and all validation checks pass, commit exactly:

`docs: remediate Phase 6 foundation after independent audit`

Push to:

`origin architecture/phase-6-handoff-review`

Do not create a PR.

---

# Required final output

Return exactly:

### A. H1 PROJECT INTEGRATION COHERENCE
Exact correction and resulting satisfaction/closure semantics.

### B. H2 EU PROGRAMME COMPLIANCE
Exact correction for requirements, eligibility, and claims.

### C. H3 REVIEWER ELIGIBILITY
Full-profile vs partial-scope rule and all exemplar corrections.

### D. M1 MULTI-PROFILE REVIEWER INSTANCE
Final normative rule and six exemplar segregation declarations.

### E. M2 REVIEW DEPENDENCY
Final declarative dependency model and any exemplar usage.

### F. M3 HANDOFF SENDER BINDING
Exact resolution and sender set/binding.

### G. UNIVERSE / OPEN QUESTIONS
Counts, consolidation constraints, updated dispositions.

### H. REGRESSION
Upstream immutability, authority, Handoff receipt/ownership, security/legal boundaries, runtime boundary.

### I. VALIDATION
PASS/FAIL count and any honesty notes.

### J. FILES CHANGED
Exact files and purpose.

### K. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, PR status.

### L. NEXT STEP
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 6 FOUNDATION RE-AUDIT
- NOT READY

Do not claim Phase 6 approval.