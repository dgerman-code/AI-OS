# Codex Prompt — Final Independent Phase 6 Foundation Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-6-handoff-review`
Audit baseline commit: `1c0f6cafbb43aa642aa0d10ccf4a9db22824c5fa`

AUDIT ONLY.
Do not modify files.
Do not commit.
Do not create a PR.
Do not mark Phase 6 APPROVED or CANONICAL.

This is the final independent re-audit after the consolidated remediation of the prior six blockers: H1–H3 and M1–M3.

Read at minimum:
- `architecture/handoff-review-registry-design.md`
- `reviews/_standards/common-review-constraints.md`
- `reviews/_templates/review-profile-card-template.md`
- `reviews/master-review-profile-universe.md`
- all six `reviews/exemplars/*.md`
- `handoffs/_standards/common-handoff-constraints.md`
- `handoffs/_templates/handoff-card-template.md`
- all four `handoffs/exemplars/*.md`
- `reviews/phase-6-foundation-self-check.md`
- `reviews/phase-6-foundation-audit-remediation.md`
- approved Phase 3/4/5 artifacts only as needed for reference and regression verification.

## 1. Re-audit H1 — Project Integration Coherence

PASS only if all are true:
- unresolved material contradiction remains an open `MAJOR_FINDING` / `CRITICAL_FINDING` as applicable;
- review status remains `NOT_SATISFIED` or `REVIEW_PERFORMED_WITH_OPEN_FINDINGS` while unresolved;
- recording, visibility, attribution, escalation, or carrying to a decision-maker cannot produce `SATISFIED` or closure;
- external named `decision.<id>` may permit progression only, without closing the finding or satisfying the review;
- integration reviewer cannot settle the underlying specialist disagreement;
- closure requires actual resolution by the owning domain Roles plus required re-review evidence.

Report exact remaining loophole count.

## 2. Re-audit H2 — EU Programme Compliance

PASS only if:
- verified N/A is clearly distinct from unresolved gap;
- unmet/unresolved rulebook requirement cannot satisfy the Profile;
- unmet/unknown/unassessed/not-satisfied eligibility cannot satisfy the Profile;
- unverified material factual claim cannot satisfy the Profile merely because it is marked/recorded/visible;
- any non-material claim exception is explicit and bounded;
- Decision Right exceptional progression does not change review status.

Report exact remaining "record it and continue" loophole count.

## 3. Re-audit H3 — Reviewer eligibility and Role-scope boundaries

Verify registry-wide distinction between:
- `FULL_PROFILE_REVIEWER_ELIGIBLE`
- `BOUNDED_REVIEW_CONTRIBUTOR`

PASS only if:
- full-Profile eligibility requires approved Role scope covering every satisfaction criterion/professional conclusion of the Profile;
- bounded contributors cannot satisfy the entire Profile;
- partial expertise does not aggregate into full authority unless a specifically governed multi-reviewer model exists;
- Profile prose cannot widen upstream Role scope;
- all six exemplar Review Profiles classify every reviewer/contributor explicitly;
- evidence integrity: Data Room and Accounting roles are bounded correctly;
- financial model: Accounting/FDD and Bankability roles are bounded correctly;
- EU programme compliance: financial-compliance specialist is bounded to cost/budget dimensions only;
- legal/security/integration exemplar eligibility remains within upstream Role scope.

Report any overbroad eligibility count.

## 4. Re-audit M1 — Multi-Profile reviewer-instance rule

PASS only if the architecture, common constraints, template, and six exemplars consistently implement:
- eligibility evaluated separately per Profile, subject, artifact version, assignment;
- independence evaluated separately per Profile;
- satisfaction of one Profile grants nothing to another;
- reviewer cannot review its own output from another Profile where independence is compromised;
- `Reviewer Instance Segregation` field exists and uses only declared values;
- `SEGREGATION_REQUIRED` prevents same-instance satisfaction;
- decision-grade/high-criticality interdependent-domain default is separation unless explicitly justified otherwise;
- combined review cannot create cross-domain authority by accumulation;
- no staffing/runtime assignment algorithm is introduced.

Audit all six exemplar segregation declarations for internal consistency, especially `review.project_integration_coherence`, `review.security`, `review.financial_model`, and `review.eu_programme_compliance`.

## 5. Re-audit M2 — Review dependency model

PASS only if `REVIEW_DEPENDENCY` is a bounded declarative primitive/rule with:
- concrete prerequisite `review.<id>`;
- required prerequisite status;
- objective activation condition if conditional;
- bounded purpose;
- missing/unsatisfied/STALE prerequisite => `REVIEW_BLOCKED`, not substantive failure;
- no transitive satisfaction;
- no transfer of scope, reviewer eligibility, authority, findings, professional conclusion, or satisfaction;
- self-dependency prohibited;
- transitive cycles prohibited;
- no runtime execution/scheduling semantics;
- dependent Profile still applies its own criteria independently.

Check every exemplar dependency declaration. `None` with reason is valid. Flag any generic category dependency rather than concrete `review.<id>`.

## 6. Re-audit M3 — Handoff sender binding

For `handoffs/exemplars/application-content-to-compliance-review.md` verify:
- sender set is closed and explicitly enumerated;
- every sender is a concrete approved `role.<id>`;
- each conditional sender has an objective activation trigger;
- each sender's exact package contribution is declared;
- each sender retains Role-owned professional ownership;
- no unbounded phrases remain such as "each relevant specialist" or equivalent;
- Role outside set cannot send on that Handoff;
- no Phase 4/5 scope is widened.

Also confirm the software implementation handoff sender set is explicitly closed.

## 7. Handoff model regression

Verify prior PASS areas remain intact:
- Handoff never transfers professional ownership;
- `RECEIVED` != endorsement/agreement;
- `RECEIVED` != `REVIEWED` / `APPROVED` / `CANONICAL`;
- receipt never satisfies review;
- missing/materially incomplete package blocks or returns for rework;
- assumptions, `UNKNOWN`, `CONFLICT_DETECTED`, findings, provenance/version history are preserved;
- chained handoffs do not accumulate authority;
- review/Decision references cannot be bypassed.

## 8. Review independence regression

Verify:
- `PRODUCER_REVIEW` cannot satisfy independent review;
- peer/cross-domain/independent-assurance distinctions remain meaningful;
- model-family diversity is not independence;
- unavailable eligible reviewer leaves requirement unsatisfied;
- `review.security` single-producing-Security-Engineer case remains safe;
- no reviewer becomes independent merely by Profile/Workflow declaration.

## 9. Finding / satisfaction / rework regression

Verify:
- finding severity != workflow progression materiality;
- unresolved `CRITICAL_FINDING` cannot satisfy review;
- unresolved `MAJOR_FINDING` cannot be carried as satisfied by visibility alone;
- `REVIEW_PERFORMED_WITH_OPEN_FINDINGS` != `SATISFIED`;
- `SATISFIED` != approval/canonical;
- material change can make review `STALE`;
- rework preserves original finding, severity, version, remediation evidence, closure rationale and re-review outcome;
- revisiting a Workflow stage cannot silently close a finding;
- Decision Right exceptional progression cannot relabel unsatisfied review as satisfied.

## 10. Scope/authority across six exemplar Review Profiles

Audit each separately:
1. `review.evidence_integrity_provenance`
2. `review.financial_model`
3. `review.legal_compliance`
4. `review.project_integration_coherence`
5. `review.eu_programme_compliance`
6. `review.security`

PASS only if each has:
- bounded subject;
- bounded review purpose;
- explicit out-of-scope;
- no neighbouring professional conclusion absorbed;
- reviewer eligibility constrained by upstream Role scope;
- satisfaction not equated with professional/business/human approval.

## 11. Universe / consolidation / carding boundary

Verify counts remain:
- families: 9
- standalone candidate Review Profiles: 34
- exemplar Review Profiles: 6
- exemplar Handoffs: 4
- overlap groups: 6

Verify:
- four consolidation proposals remain unapplied;
- their audit caveats are recorded;
- no new carding occurred;
- no mass-generation recommendation is implied by foundation status.

## 12. Reference integrity

Count and classify concrete references across all 10 exemplar cards:
- existing approved upstream IDs;
- Phase 6 candidate/profile IDs;
- deliberate Phase 7 forward `decision.*` refs;
- invalid/undefined refs.

Invalid concrete refs must be 0.

## 13. Upstream / phase-boundary regression

Verify:
- Phase 3 Role changes = 0;
- approved Phase 4 architecture/mapping changes = 0;
- approved Phase 5 Workflow semantic changes = 0;
- all Phase 6 artifacts remain `PROPOSED`;
- no Decision Right is defined, granted, assigned, or exercised;
- no runtime/database/API/UI/orchestrator/model/agent implementation;
- no PR created as part of this path.

## 14. Open architecture question dispositions

Verify current dispositions are coherent:
1. Review dependency reference — RESOLVED IN FOUNDATION
2. Profile prerequisite review — RESOLVED IN FOUNDATION
3. Multi-Profile reviewer instance — RESOLVED IN FOUNDATION
4. Organisational independence — SAFE TO DEFER WITH EXPLICIT RULE
5. Shared vs Profile-specific staleness — SAFE TO DEFER WITH EXPLICIT RULE
6. Handoff first-class vs embedded — SAFE TO DEFER WITH EXPLICIT RULE
7. Runtime observation/recording of review satisfaction — RUNTIME-PHASE CONCERN
8. Exceptional progression via Decision Rights while review remains unsatisfied — PHASE 7 CONCERN

Flag any question that is marked resolved but remains materially ambiguous.

## Approval threshold

- PASS if H1–H3 and M1–M3 are fully remediated and no regression exists.
- PASS WITH NON-BLOCKING NOTES if only the explicitly deferred organisational-independence, staleness refinement, Handoff reuse, Phase 7, or runtime matters remain.
- PASS WITH CHANGES if a bounded Phase 6 correction is still required before human approval.
- FAIL if any satisfaction loophole, reviewer scope widening, unsafe multi-Profile accumulation, unbounded dependency/sender model, authority leakage, or phase-boundary regression remains.

Do not modify anything.

Return exactly:

### A. FINAL VERDICT
PASS / PASS WITH NON-BLOCKING NOTES / PASS WITH CHANGES / FAIL

### B. H1 PROJECT INTEGRATION COHERENCE
PASS / FAIL + exact remaining loophole count.

### C. H2 EU PROGRAMME COMPLIANCE
PASS / FAIL + exact remaining record-it-and-continue loophole count.

### D. H3 REVIEWER ELIGIBILITY
PASS / FAIL + overbroad full-Profile eligibility count.

### E. M1 MULTI-PROFILE REVIEWER INSTANCE
PASS / FAIL + segregation consistency findings.

### F. M2 REVIEW DEPENDENCY
PASS / FAIL + invalid/generic dependency count + cycle findings.

### G. M3 HANDOFF SENDER BINDING
PASS / FAIL + unbounded sender-set count.

### H. HANDOFF / REVIEW REGRESSION
Handoff ownership/receipt, independence, finding/satisfaction/rework status.

### I. SIX EXEMPLAR REVIEW PROFILES
Each PASS / FAIL with concise finding.

### J. FOUR EXEMPLAR HANDOFFS
Each PASS / FAIL with concise finding.

### K. UNIVERSE / CARDING BOUNDARY
Report 9 / 34 / 6 / 4 / 6 and consolidation/card-generation status.

### L. REFERENCE INTEGRITY
Existing / Phase 6 / Phase 7 forward / invalid counts.

### M. OPEN QUESTIONS
All eight dispositions + any remaining ambiguity.

### N. REMAINING BLOCKERS
If none: NONE.

### O. HUMAN APPROVAL VERDICT
Choose exactly one:
- READY FOR HUMAN APPROVAL OF PHASE 6
- READY AFTER LISTED CHANGES
- NOT READY

### P. CARD-GENERATION VERDICT
Choose exactly one:
- KEEP EXEMPLAR-ONLY
- SAFE FOR SELECTIVE CONTROLLED CARDING
- SAFE FOR CONTROLLED BATCH CARDING
- SAFE FOR MASS CARD GENERATION

Do not modify anything.