# Codex Prompt — Independent Phase 6 Handoff & Review Foundation Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-6-handoff-review`
Foundation baseline commit: `cd3f3fcd25a20a1bb0a24c556681079209deb5b0`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 6 APPROVED or CANONICAL.

This is an independent architecture audit of the Phase 6 Handoff & Review foundation.

Read at minimum:
- `architecture/handoff-review-registry-design.md`
- `reviews/_standards/common-review-constraints.md`
- `reviews/_templates/review-profile-card-template.md`
- `reviews/master-review-profile-universe.md`
- all six files in `reviews/exemplars/`
- `handoffs/_standards/common-handoff-constraints.md`
- `handoffs/_templates/handoff-card-template.md`
- all four files in `handoffs/exemplars/`
- `reviews/phase-6-foundation-self-check.md`
- approved Phase 3 Role architecture, approved Phase 4 Skill architecture/mappings, and approved Phase 5 Workflow architecture only as needed for regression / reference / authority verification.

The producing self-check reports 36/36 PASS but explicitly leaves one issue classified `MUST RESOLVE IN PHASE 6 FOUNDATION`: whether one reviewer instance may satisfy multiple compatible Review Profiles. Treat that as an open architecture finding to adjudicate independently, not as an assumed blocker or assumed non-blocker.

## 1. Identity and phase boundary

Verify the separation:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != MODEL != RUNTIME`

Check that:
- Handoff is transfer/coordination architecture, not ownership transfer, review, approval, Role identity, or runtime transport;
- Review Profile is reusable review architecture, not a reviewer instance, Decision Right, Role, Skill, Workflow, or runtime agent;
- no Phase 6 object expands Role professional scope or Phase 4 capability compatibility;
- no Phase 6 object creates or exercises a human Decision Right;
- no Phase 6 artifact defines runtime assignment, persistence, scheduling, database schema, API, UI, model routing, or agent binding;
- approved Phase 3/4/5 artifacts were not materially changed.

## 2. Handoff authority and ownership audit

Stress-test the architecture, standard, template, and all four Handoff exemplars.

Verify:
- Handoff never transfers professional ownership merely by transfer;
- `RECEIVED` never implies agreement with a conclusion;
- `RECEIVED` never implies `REVIEWED`, `APPROVED`, or `CANONICAL`;
- `RECEIVED` never satisfies a review requirement;
- material assumptions, `UNKNOWN`, `CONFLICT_DETECTED`, open findings, source/version provenance, and superseded inputs cannot disappear during transfer;
- receiver cannot invent missing assumptions or silently repair incomplete upstream reasoning;
- materially incomplete packages block or return for rework;
- review / Decision Right references carried by the Handoff cannot be bypassed;
- chained handoffs do not accumulate authority;
- re-handoff preserves package history and prior/superseded versions.

Report any phrase that could reasonably be read as acceptance = endorsement or ownership transfer.

## 3. Review independence model

Audit all four independence classes:
- `PRODUCER_REVIEW`
- `PEER_REVIEW`
- `CROSS_DOMAIN_REVIEW`
- `INDEPENDENT_ASSURANCE_REVIEW`

Verify:
- producer QC is explicitly non-independent and never satisfies an independent-review requirement;
- independence is an assignment/work relationship, not a label applied by prose;
- the reviewer is not the producer/author of the reviewed subject in the same assignment where independence is required;
- Workflow participation cannot manufacture reviewer independence;
- cross-domain review checks interfaces/consistency only and does not substitute for domain review;
- independent assurance adds real separation rather than merely renaming peer review;
- model-family diversity is not treated as reviewer independence;
- unavailable eligible reviewer leads to unsatisfied/block/rework/escalation, never lowering the requirement.

Pay particular attention to `review.security`, because the same Security Engineer Role may own security design/implementation/assessment in the producing assignment. Verify the Review Profile does not create an impossible or circular eligibility model, and that it handles "no eligible independent reviewer available" safely.

## 4. Review scope and professional authority

For each of the six exemplar Review Profiles, verify:
- bounded subject/artifact scope;
- owning Role(s) named;
- explicit purpose;
- explicit out-of-scope boundaries;
- no neighbouring domain conclusion is absorbed;
- required evidence package and traceability are sufficient for the stated review purpose;
- the Profile cannot override the producer Role's domain conclusion outside its review remit;
- Profile satisfaction is not professional approval or business/policy decision authority.

Specifically stress-test:
- evidence integrity vs truth/substantive correctness;
- financial model integrity vs ownership/validity of source assumptions;
- legal compliance review vs formal legal opinion / legal Decision Right;
- project integration coherence vs settling specialist disagreement;
- EU programme compliance vs producer QC and grant submission authority;
- security review vs producing Security Engineer work and security-risk acceptance.

## 5. Finding taxonomy and materiality

Audit:
- `NO_FINDING`
- `OBSERVATION`
- `MINOR_FINDING`
- `MAJOR_FINDING`
- `CRITICAL_FINDING`

Verify:
- finding severity is distinct from Phase 5 workflow open-item materiality;
- unresolved `CRITICAL_FINDING` cannot be `SATISFIED` and blocks/reworks/escalates;
- unresolved `MAJOR_FINDING` cannot be casually carried forward; any bounded exception is explicit and cannot itself waive the finding;
- `MINOR_FINDING` / observation treatment cannot bypass materiality at the next step/gate;
- a Review Profile cannot waive its own finding;
- any exceptional progression with unresolved material/major findings requires a named external Decision Right while review status remains unsatisfied where applicable;
- review findings cannot silently change artifact knowledge states.

Identify any loophole equivalent to "record the finding and continue."

## 6. Review status and satisfaction semantics

Audit these states:
- `NOT_STARTED`
- `IN_REVIEW`
- `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`
- `SATISFIED`
- `NOT_SATISFIED`
- `REVIEW_BLOCKED`
- `STALE` / `SUPERSEDED`

Verify:
- performed != satisfied;
- satisfied != approved/canonical;
- Workflow progress cannot itself cause `SATISFIED`;
- only a later eligible reviewer instance applying the Profile can produce satisfaction;
- missing prerequisite/evidence can result in `REVIEW_BLOCKED` rather than a false negative substantive finding;
- material change after satisfaction causes staleness/re-review where the Profile says so;
- Decision Right exceptional progression does not convert `NOT_SATISFIED` into `SATISFIED`.

## 7. Review rework and closure

Verify that review-triggered rework is declarative and preserves:
- original finding;
- severity;
- affected artifact/version;
- owning Role;
- response/remediation evidence;
- closure rationale;
- new artifact/version;
- re-review outcome where required.

Check:
- revisiting a Workflow Stage does not itself close a finding;
- the producer cannot self-close a finding that requires independent re-review;
- closure does not erase previous failure history;
- review does not schedule runtime work.

## 8. Handoff vs Review boundary

Verify the two models remain separate in architecture and all exemplars:
- Handoff checks transfer/package completeness;
- Review checks substantive quality/compliance/assurance;
- receiving a package is not review;
- rejecting a package is not automatically a review finding;
- Review may consume a Handoff package;
- Handoff may require a Review Profile to already be `SATISFIED`;
- neither model silently absorbs the other.

## 9. Multi-profile reviewer-instance question — REQUIRED ADJUDICATION

The self-check classifies this as `MUST RESOLVE IN PHASE 6 FOUNDATION` but leaves it unresolved:

> May one reviewer instance satisfy multiple compatible Review Profiles on the same assignment/change?

Audit this independently and choose one disposition:
- BLOCKER NOW
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- RUNTIME/ASSIGNMENT-PHASE CONCERN

Then state the **minimal architecture rule** required.

At minimum consider:
- one reviewer could legitimately perform multiple compatible scoped reviews if independently eligible for each;
- one person satisfying `review.architecture`, `review.security`, `review.data_architecture`, and other profiles could create concentration risk or destroy intended separation;
- a single reviewer instance must not inherit cross-domain professional authority by accumulation;
- satisfying multiple Profiles must require eligibility and independence to be evaluated separately for each Profile/subject;
- Profiles with explicit segregation-of-review requirements must prohibit same-instance satisfaction;
- decision-grade / high-criticality work may require separation even when one person is technically eligible;
- the foundation must not defer so far that reviewer independence semantics become ambiguous or unsafe.

If you judge it resolvable with one generic rule, state that rule precisely. Do not invent runtime assignment algorithms.

## 10. Review Profile dependencies/composition

Audit whether Phase 6 needs first-class declarative dependencies between Review Profiles now.

The architecture currently surfaces open questions about:
- Profile composition;
- one Profile requiring another as prerequisite.

Determine whether current "dependency on another review" prose is sufficient for foundation approval or whether a bounded primitive/reference rule is required to prevent ambiguity/cycles.

If dependency is permitted, verify at minimum:
- dependency must point to `review.<id>`;
- unsatisfied prerequisite means dependent review is `REVIEW_BLOCKED`, not substantively failed;
- dependency cannot imply satisfaction transitivity;
- no cycles / self-dependency;
- parent/dependent Profile does not inherit another Profile's scope or authority.

## 11. Handoff registry identity question

The self-check says Handoff Cards are currently first-class entries but whether they should instead be embedded Workflow patterns is deferred.

Assess whether this is safe for foundation approval.

PASS if first-class Handoff identity is sufficiently justified by reuse, versioning, auditability, and stable transfer semantics without causing registry explosion.

Flag if the four exemplars reveal that Handoffs are merely one-off Stage glue or duplicate Workflow semantics.

## 12. Review Universe quality

Independently assess the claimed universe:
- 9 families;
- 34 candidate Review Profiles;
- 44 existing `review.<id>` references accounted for;
- 4 proposed consolidations;
- 6 unresolved overlap groups;
- 6 exemplar Review Profiles.

For each candidate conceptually classify as one of:
- VALID REVIEW PROFILE
- LIKELY REVIEW PROFILE BUT NEEDS BOUNDARY REFINEMENT
- METHOD / CHECK / QC IN DISGUISE
- ROLE / PROFESSIONAL CONCLUSION IN DISGUISE
- DECISION RIGHT / APPROVAL IN DISGUISE
- DUPLICATE / OVERLAPPING PROFILE
- RUNTIME / ASSIGNMENT CONCERN

You do not need to create cards. Audit for profile explosion and mega-review collapse.

Evaluate the four proposed consolidations and six overlap groups. Do not force merges without evidence, but identify any pair/group that must be resolved before human approval or before additional carding.

## 13. Reference integrity

Verify all concrete references in the 10 exemplar cards:
- `role.*`
- `artifact.*`
- `skill.*`
- `specialisation.*`
- `skill_pack.*`
- `review.*`
- `decision.*`
- `workflow.*` / Stage references where used

Distinguish:
- valid approved upstream IDs;
- valid Phase 6 candidate/profile IDs;
- deliberate Phase 7 forward Decision references;
- invalid/undefined references.

Do not treat a deliberate future Decision Right reference as existing human authority.

## 14. Criticality scaling

Verify criticality:
- increases evidence depth, review type/intensity, independence depth, closure evidence, handoff checkpoints, and re-review requirements;
- does not change Role identity;
- does not create duplicate Handoff/Review Profile identities merely for project size;
- does not turn a reviewer into a Decision Right holder;
- does not make satisfaction equal approval.

## 15. Upstream regression / non-runtime boundary

Verify:
- Phase 3 Role changes = 0;
- approved Phase 4 architecture/mapping changes = 0;
- approved Phase 5 Workflow semantic changes = 0 or only explicit non-semantic downstream references if any;
- all Phase 6 artifacts remain `PROPOSED`;
- no DB/API/UI/runtime/orchestrator/model/agent implementation;
- no PR.

## 16. Open architecture questions — dispositions

For all eight questions listed in `reviews/phase-6-foundation-self-check.md`, return exactly one disposition:
- BLOCKER NOW
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 7 CONCERN
- RUNTIME-PHASE CONCERN

The eight questions are:
1. first-class Review Profile composition/dependency reference;
2. one Profile requiring another as prerequisite;
3. one reviewer instance satisfying multiple compatible Profiles;
4. organisational independence eligibility;
5. shared vs Profile-specific staleness rule;
6. Handoff Cards first-class vs embedded patterns;
7. runtime recording/observation of review satisfaction;
8. exceptional progression via Phase 7 Decision Rights while review remains unsatisfied.

Do not inherit the producer's dispositions automatically.

## 17. Approval threshold

Use a strict threshold:
- FAIL if reviewer independence can be manufactured, self-review can satisfy independent review, satisfaction can imply approval, Handoff receipt can imply endorsement/ownership, critical findings can silently pass, or unresolved foundation ambiguity makes scaling unsafe;
- PASS WITH CHANGES if architecture is sound but bounded corrections are required before human approval;
- PASS WITH NON-BLOCKING NOTES if only Phase 7/runtime/future selective refinements remain;
- PASS only if no material finding remains.

Do not recommend mass Review Profile or Handoff card generation merely because the foundation passes.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. HIGH / MEDIUM FINDINGS
List findings with severity and exact affected files/sections.

### C. IDENTITY / PHASE BOUNDARY
PASS / FAIL + explanation.

### D. HANDOFF MODEL
PASS / FAIL + authority/ownership/receipt/rework findings.

### E. REVIEW INDEPENDENCE
PASS / FAIL + independence findings.

### F. REVIEW SCOPE / AUTHORITY
PASS / FAIL + findings across six exemplars.

### G. FINDING / SATISFACTION SEMANTICS
PASS / FAIL + finding severity, review-status, stale/re-review findings.

### H. MULTI-PROFILE REVIEWER INSTANCE
Disposition + minimal architecture rule + whether it blocks approval.

### I. REVIEW DEPENDENCY / COMPOSITION
PASS / FAIL + whether a bounded dependency primitive/rule is needed now.

### J. HANDOFF IDENTITY
PASS / FAIL + first-class-vs-embedded finding.

### K. REVIEW UNIVERSE
Counts, duplicate/overlap findings, consolidation findings, required changes if any.

### L. EXEMPLAR AUDIT
Six Review Profiles and four Handoffs, each PASS / FAIL with concise finding.

### M. REFERENCE INTEGRITY
Existing / Phase 6 candidate / Phase 7 forward / invalid counts and findings.

### N. OPEN QUESTIONS DISPOSITION
All eight questions with one allowed disposition each.

### O. REMAINING BLOCKERS
If none: NONE.

### P. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 6 FOUNDATION
- READY AFTER LISTED CHANGES
- NOT READY

### Q. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.