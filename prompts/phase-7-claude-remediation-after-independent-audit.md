# Claude Code Prompt — Phase 7 Foundation Remediation After Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-7-decision-rights`
Foundation baseline: `1db348c90fb7f6ba9d78b4c346ae1e4a9a05c0e4`
Independent audit prompt commit on branch: `5c0517fda7edf123ef3781d8031ab85073308a72`

The independent Phase 7 audit returned **FAIL** with one HIGH and five MEDIUM findings.

This remediation must be **strictly bounded** to the six audit blockers below. Do not redesign Phase 7 broadly.

Do not modify approved Phase 3 Role Cards.
Do not modify approved Phase 4 architecture/mappings.
Do not modify approved Phase 5 Workflow semantics.
Do not modify approved Phase 6 Handoff/Review semantics.
Do not implement DB/API/UI/runtime/orchestrator/model/agent/IAM logic.
Do not bind real people or organisations.
Do not create a PR.
Do not mark Phase 7 APPROVED or CANONICAL.
Do not mass-card Decision Rights.

All Phase 7 artifacts remain `PROPOSED`.

---

# Finding H1 — Cross-Right separation of duties is undefined

Audit disposition: **MUST RESOLVE BEFORE HUMAN APPROVAL**.

Add a relationship-level declarative model named exactly or equivalently:

`DECISION_RIGHT_SEPARATION`

It must exist in:
- `architecture/decision-rights-registry-design.md`
- `decisions/_standards/common-decision-right-constraints.md`
- `decisions/_templates/decision-right-card-template.md`
- `reviews/phase-7-foundation-self-check.md`

## Required declaration semantics

A Decision Right may declare one or more relationship rows with:

- concrete related `decision.<id>`;
- objective activation condition;
- separation mode:
  - `SEPARATION_REQUIRED`
  - `SAME_HOLDER_PERMITTED`
- bounded subject/context to which the relation applies;
- reason for the separation/permitted-sharing rule.

## Normative rules

1. Where `SEPARATION_REQUIRED`, **the same human instance must not exercise both Decision Rights for the same governed subject/context and decision chain**.
2. Eligibility is evaluated independently for each Right.
3. Holding two eligibility classes does not bypass separation.
4. Delegation does not bypass separation.
5. Within-Right cardinality does not satisfy cross-Right separation.
6. Separation is relationship-level governance, not a property inferred from job title or Role identity.
7. Same-person exercise may be permitted only where the relationship explicitly declares `SAME_HOLDER_PERMITTED` and doing so does not undermine the independent-control purpose.
8. This model creates no staffing algorithm, assignment engine or runtime scheduling semantics.
9. If a required-separated second eligible holder is unavailable, the second Decision Right is not validly exercisable for that context; authority is not relaxed.
10. A Decision Record later must be able to evidence compliance with applicable separation relationships.

## Criticality default

For **decision-grade/high-criticality external-commitment chains**, default to `SEPARATION_REQUIRED` between:

- `decision.risk_acceptance` and a final release/submission/publication/contractual-commitment Right when both concern the same unresolved risk/subject;
- `decision.exceptional_progression` and the downstream final commitment/release/submission/publication Right where the exceptional progression concerns an unresolved item material to that final act;
- emergency exception authority and ordinary ratification/release authority where independence of retrospective control would otherwise be defeated.

A card may override that default to `SAME_HOLDER_PERMITTED` only with an explicit defensible reason and only where the control purpose is preserved.

## Apply to exemplars

At minimum add relationships where applicable to:
- `decision.risk_acceptance`
- `decision.production_release`
- `decision.exceptional_progression`
- `decision.granting_authority_submission`
- `decision.external_publication`
- `decision.contract_commitment`
- `decision.emergency_production_change`

Be conservative. Do not manufacture irrelevant relationships.

The exact high-risk case must be closed:

> The same human must not both accept the residual risk under `decision.risk_acceptance` and authorize `decision.production_release` for the same change carrying that risk, where the separation relationship is active.

---

# Finding M1 — Production release `APPROVE_WITH_CONDITIONS` timing contradiction

Affected:
- `decisions/exemplars/production-release.md`
  - Allowed Outcomes and Their Effects
  - following explanatory prose

Current defect:
- the table says the change becomes live once conditions are met;
- prose also permits post-release monitoring conditions;
- these imply different gate timing.

Resolve by explicitly distinguishing **pre-release conditions** from **post-release obligations**.

Required semantics:

1. `APPROVE_WITH_CONDITIONS` may include both classes only if they are named separately.
2. Any **pre-release condition** that is material to release authorization must be satisfied **before the production-release gate is satisfied and before deployment becomes live**.
3. A **post-release obligation** may remain open after release only if:
   - it does not invalidate release readiness;
   - it is explicitly classified as post-release;
   - it is carried into the Decision Record;
   - it has an owner/trigger/expiry or revisit criterion at the architecture level;
   - failure later triggers the declared re-decision/escalation/rollback path rather than retroactively claiming the original decision never existed.
4. The phrase “conditions are met” must not ambiguously include post-release obligations.
5. `APPROVE_WITH_CONDITIONS` cannot be used to smuggle an unresolved material pre-release blocker through the gate.

Update the Human Approval Matrix if needed so its required-review/gate semantics stay aligned.

---

# Finding M2 — Universe count/classification mismatch

Affected:
- `decisions/master-decision-right-universe.md` §10 and related summary/count tables.

Independent audit found:
- actual `LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT`: 35
- required/declared target: 34
- `DUPLICATE / OVERLAP`: 0 actual, 1 required

Required correction:

Reclassify:

`decision.canonical_knowledge_status_change`

as:

`DUPLICATE / OVERLAP`

with:

`decision.canonical_knowledge_promotion`

Rationale:
- both are Phase 8-bound canonical-governance concepts;
- keep both upstream identifiers accounted for;
- do **not** silently merge or rename them;
- record that consolidation/normalization is deferred to Phase 8 canonical governance.

Resulting exact universe accounting must be:
- 9 families
- 35 candidate Rights
- 33 upstream-ID candidates
- 2 architecture-gap candidates
- 34 `LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT`
- 10 Review/quality gates in disguise
- 8 Role responsibilities in disguise
- 4 Workflow progression logic in disguise
- 2 Runtime/IAM in disguise
- 3 Executive-policy items
- 1 `DUPLICATE / OVERLAP`
- all 95 upstream references still accounted for

No mass carding.

---

# Finding M3 — `decision.cancellation_or_termination` is too broad

Affected:
- `decisions/master-decision-right-universe.md`
- `architecture/decision-rights-registry-design.md` if the architecture currently suggests one universal cancellation/termination right.

Current defect:
- combines pre-commitment cancellation and post-commitment termination across any governed path;
- risks becoming a universal kill-switch.

Do **not** card it in this remediation.

Required correction:

1. Reclassify the current architecture-gap concept so it is **not treated as a valid bounded Right ready for carding**.
2. State explicitly that cancellation and termination are likely separate bounded authority patterns because:
   - pre-commitment cancellation may stop an internal governed path;
   - post-commitment termination may affect legal, contractual, regulatory, financial or external obligations;
   - holder eligibility and evidence can differ materially.
3. Preserve the upstream architectural need without inventing one universal `decision.cancellation_or_termination` authority.
4. Preferred disposition:
   - `LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT`, or
   - split proposal recorded as unresolved overlap/boundary work.
5. If you preserve the placeholder ID, mark it **NOT CARDABLE UNTIL BOUNDED** and state it confers no authority.
6. Do not create replacement cards now.

A future bounded split could use separate concepts such as governed-path cancellation versus external-commitment termination, but do not silently create final IDs unless supported by existing registry evidence.

---

# Finding M4 — Three undefined code-form alias IDs

Affected exemplar prose contains:
- `decision.project_readiness_progression`
- `decision.grant_submission`
- `decision.contractual_commitment`

These are not defined candidate IDs; calling them “prompt aliases” is not enough because code-form `decision.*` strings are concrete registry references.

Required correction:

Replace those code-form aliases with plain-language labels or explicitly non-ID formatting.

Map conceptually to the actual exemplar IDs without introducing new registry identities:
- project readiness progression -> actual `decision.stage_gate_progression`
- grant submission -> actual `decision.granting_authority_submission`
- contractual commitment -> actual `decision.contract_commitment`

Rules:
- no undefined `decision.*` alias may remain in exemplar prose;
- if explaining original prompt terminology, use prose such as “the requested project-readiness progression exemplar” without backticks or `decision.` prefix;
- do not rename actual stable IDs merely to match the prompt.

After remediation, invalid/undefined concrete Decision references across exemplar cards must be 0.

---

# Finding M5 — Human Approval Matrix cardinality mismatch

Affected:
- Human Approval Matrix section/file for `decision.exceptional_progression`
- `decisions/exemplars/exceptional-progression.md`

Audit finding:
- matrix describes all-required only across domains;
- card also requires `MULTI_HOLDER_ALL_REQUIRED` at a terminal gate.

Required correction:

Make matrix and card exactly consistent.

The matrix must express the card’s actual rule, including the terminal-gate condition.

Do not weaken the card to match the matrix unless a stronger reason is discovered. Default correction is matrix → card semantics.

Audit all eight matrix rows for the same type of discrepancy.

Required discrepancy count after remediation: 0.

---

# Open architecture question updates

Update `reviews/phase-7-foundation-self-check.md` dispositions:

1. organisational authority eligibility -> `RUNTIME / ORGANISATION-PHASE CONCERN`
2. one human exercising multiple Rights in one chain -> `RESOLVED IN FOUNDATION` through `DECISION_RIGHT_SEPARATION`
3. mandatory separation between some Rights -> `RESOLVED IN FOUNDATION` through relationship-level separation declarations
4. abstention/dissent -> `SAFE TO DEFER WITH EXPLICIT RULE`
5. global vs Right-specific expiry -> `SAFE TO DEFER WITH EXPLICIT RULE`
6. shared risk-class ceiling -> `RUNTIME / ORGANISATION-PHASE CONCERN`
7. canonical promotion -> `PHASE 8 CONCERN`
8. first-class composition vs bounded prerequisites -> `SAFE TO DEFER WITH EXPLICIT RULE`
9. emergency retrospective ratification model -> `SAFE TO DEFER WITH EXPLICIT RULE`
10. reversal model -> `SAFE TO DEFER WITH EXPLICIT RULE`

Do not claim 2–3 resolved unless separation rules are actually implemented in design, constraints, template and affected exemplars.

---

# Required remediation record

Create:

`reviews/phase-7-foundation-audit-remediation.md`

Status:

`PROPOSED — READY FOR FINAL INDEPENDENT PHASE 7 FOUNDATION RE-AUDIT`

Record:
- all six audit findings;
- exact fixes;
- files changed;
- separation-of-duties model and exemplar relationships;
- production-release timing correction;
- universe count correction;
- cancellation/termination reclassification/bounding;
- alias cleanup;
- matrix alignment;
- upstream regression checks;
- remaining deferred matters.

---

# Validation — minimum 50 checks

Run at least these checks:

1. `DECISION_RIGHT_SEPARATION` exists in architecture.
2. Separation rule exists in common constraints.
3. Separation section/property exists in card template.
4. Separation supports only concrete `decision.<id>` relationships.
5. Separation activation condition is objective/testable.
6. Separation supports `SEPARATION_REQUIRED`.
7. Separation supports `SAME_HOLDER_PERMITTED`.
8. Same human cannot exercise both Rights where active separation required.
9. Dual eligibility labels cannot bypass separation.
10. Delegation cannot bypass separation.
11. Within-Right cardinality cannot substitute for cross-Right separation.
12. No staffing/runtime algorithm introduced.
13. Decision Record evidence model can prove separation compliance.
14. `risk_acceptance` vs `production_release` same-subject hazard is closed.
15. `exceptional_progression` vs downstream final commitment/release relationship is governed where applicable.
16. Emergency/ordinary related-authority separation is governed where applicable.
17. Production release distinguishes pre-release conditions from post-release obligations.
18. Material pre-release condition blocks gate satisfaction until met.
19. Post-release obligation may remain only under explicit bounded semantics.
20. No ambiguous “conditions met” wording remains.
21. `APPROVE_WITH_CONDITIONS` cannot bypass material pre-release blocker.
22. Universe families = 9.
23. Candidate Rights = 35.
24. Upstream-ID candidates = 33.
25. Architecture-gap candidates = 2 unless explicitly and transparently reclassified while total remains coherent.
26. Boundary-refinement entries = 34.
27. Duplicate/overlap entries = 1.
28. `canonical_knowledge_status_change` is duplicate/overlap with `canonical_knowledge_promotion`.
29. Both canonical IDs remain accounted for and deferred to Phase 8.
30. All 95 upstream references remain accounted for.
31. `cancellation_or_termination` is not presented as a universal valid kill-switch.
32. `cancellation_or_termination` is NOT CARDABLE UNTIL BOUNDED or equivalently constrained.
33. Pre-commit cancellation vs post-commit termination distinction is explicit.
34. No new cancellation/termination cards created.
35. Undefined alias `decision.project_readiness_progression` absent.
36. Undefined alias `decision.grant_submission` absent.
37. Undefined alias `decision.contractual_commitment` absent.
38. Actual stable exemplar IDs remain unchanged.
39. Invalid/undefined concrete Decision refs across exemplars = 0.
40. Exceptional-progression matrix cardinality matches card.
41. All eight matrix rows match corresponding card cardinality.
42. All eight matrix rows match delegation policy.
43. All eight matrix rows match external-commitment flag.
44. All eight matrix rows match exceptional-progression flag.
45. All eight matrix rows match risk-acceptance flag.
46. All eight matrix rows match knowledge-state effect.
47. Phase 3 Role changes = 0.
48. Approved Phase 4 architecture/mapping changes = 0.
49. Approved Phase 5 Workflow semantic changes = 0.
50. Approved Phase 6 Handoff/Review semantic changes = 0.
51. All Phase 7 artifacts remain PROPOSED.
52. No DB/API/UI/runtime/orchestrator/model/agent/IAM implementation.
53. No named human/organisation assignment.
54. No PR created.
55. Review `NOT_SATISFIED` boundary unchanged.
56. Risk acceptance still does not itself permit progression/release.
57. Emergency authority still cannot retroactively satisfy skipped review.
58. Generic approval still does not imply CANONICAL.
59. Decision requested/meeting/email still does not satisfy gate.
60. Decision correction still uses a new linked Decision Record, not mutation.

Do not weaken a test to make it pass. If a test is genuinely wrong, document why and replace it with a stricter correct test.

---

# Commit / push

If and only if remediation is complete and validation passes, commit exactly:

`docs: remediate Phase 7 foundation after independent audit`

Push to:

`origin architecture/phase-7-decision-rights`

Do not create a PR.

---

# Required final output

Return exactly:

### A. H1 CROSS-RIGHT SEPARATION
Final model, defaults, exemplar relationships and closed hazards.

### B. M1 PRODUCTION RELEASE CONDITIONS
Exact pre-release vs post-release semantics.

### C. M2 UNIVERSE CLASSIFICATION
Exact counts and canonical duplicate/overlap disposition.

### D. M3 CANCELLATION / TERMINATION
Final bounded/reclassified status and carding boundary.

### E. M4 REFERENCE INTEGRITY
Alias cleanup and final invalid-ref count.

### F. M5 HUMAN APPROVAL MATRIX
Exact correction and discrepancy count across all eight rows.

### G. OPEN QUESTIONS
Updated dispositions for all ten.

### H. REGRESSION
Phase 3–6 immutability, authority/review/risk/emergency/canonical boundaries, non-runtime status.

### I. VALIDATION
PASS/FAIL count and honesty notes.

### J. FILES CHANGED
Exact files and purpose.

### K. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, PR status.

### L. NEXT STEP
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 7 FOUNDATION RE-AUDIT
- NOT READY

Do not claim Phase 7 approval.