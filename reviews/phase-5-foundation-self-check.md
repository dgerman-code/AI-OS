# Phase 5 — Workflow Registry Foundation Self-Check

Status: PROPOSED — READY FOR INDEPENDENT PHASE 5 FOUNDATION AUDIT

Branch: `architecture/phase-5-workflow-registry`
Baseline: Phase 4 human-approved state at commit `8a0d8d18525cb1adf54fdf74f3fb625f5be6fe3d`

This is a **self**-check. It is not an independent audit and does not claim to be one — it is the producing pass testing its own output, which is exactly the kind of quality control the architecture it describes refuses to call review.

## Artifacts covered

| File | Purpose |
|---|---|
| `architecture/workflow-registry-design.md` | Workflow identity model, adjacency distinctions, composition model, participation vocabulary, transition semantics, criticality behaviour |
| `workflows/_standards/common-workflow-constraints.md` | 17 enforceable architecture rules inherited by every Workflow Card |
| `workflows/_templates/workflow-card-template.md` | Mandatory Workflow Card structure |
| `workflows/master-workflow-universe.md` | 9 families, 49 candidate Workflows, 7 deliberate exclusions, 8 flagged overlap groups |
| `workflows/exemplars/project-development-readiness.md` | Exemplar A |
| `workflows/exemplars/eu-grant-application-development.md` | Exemplar B |
| `workflows/exemplars/software-change-delivery.md` | Exemplar C |
| `workflows/exemplars/decision-grade-document-preparation.md` | Exemplar D |

---

## 1. Check results

| # | Check | Result | Evidence |
|---:|---|---|---|
| 1 | No Phase 3 Role Card changed | **PASS** | `git diff 8a0d8d1 -- roles/` empty |
| 2 | No Phase 4 approved architecture file materially changed | **PASS** | `git diff 8a0d8d1` empty over `skills/`, the three Phase 4 architecture files and the three Phase 4 review records |
| 3 | No Workflow grants professional authority | **PASS** | Canonical clause "grants no professional authority … gains nothing beyond its own Role Card" in all 4 cards; constraints §1 |
| 4 | No Workflow owns a human decision | **PASS** | All 4 cards carry `HUMAN_GATE_REFERENCE`, name the gates human decision rights, and state they are neither exercised nor satisfied |
| 5 | No Workflow defines independent reviewer identity | **PASS** | Constraints §5; all 4 cards state no stage performs or satisfies review |
| 6 | No Workflow self-promotes APPROVED/CANONICAL | **PASS** | All 4 cards state no artifact reaches `APPROVED` or `CANONICAL` through the Workflow |
| 7 | No Workflow widens Role-to-Skill compatibility | **PASS** | Constraints §3; every card's Activated Skills table states the Phase 4 basis per capability |
| 8 | Every exemplar has explicit trigger, entry/exit and completion semantics | **PASS** | `## Trigger`, `## Preconditions`, per-stage entry and exit criteria, `## Completion Criteria` present in all 4 |
| 9 | Every exemplar has exception/rework behaviour | **PASS** | `EXCEPTION_PATH`, `REWORK_LOOP` and `## Rework Rules` present in all 4 |
| 10 | Every exemplar preserves artifact ownership boundaries | **PASS** | Every artifact contribution and every output row attributes an owning Role |
| 11 | Project Development Lead does not absorb specialist conclusions | **PASS** | Explicit non-absorption clause plus the rule that a specialist artifact governs over the readiness assessment where they disagree |
| 12 | EU grant workflow cannot submit autonomously | **PASS** | "This Workflow cannot submit"; `decision.granting_authority_submission` preserved on the normal path and on the deadline-pressure exception path; no expedited route |
| 13 | Software workflow cannot release to production autonomously | **PASS** | "No workflow stage may authorize production release"; pipeline construction explicitly distinguished from release authority |
| 14 | Decision-grade document workflow cannot self-approve | **PASS** | "cannot self-approve"; `AI_SUGGESTION` adoption stated as a Role act, never a consequence of progression |
| 15 | Criticality changes depth, not Role identity | **PASS** | "**Role identity does not change**" in all 4 Criticality Scaling sections; design §6 carries the duplication test |
| 16 | No runtime/model/provider binding | **PASS** | No model, vendor, framework, queue, database or orchestrator named in any Phase 5 artifact; all 4 cards carry a Non-Runtime Statement |
| 17 | Master Workflow Universe is 30–50 candidates and avoids micro-workflows | **PASS** | 49 candidates across 9 families; 7 micro-, duplicate- or runtime-shaped candidates explicitly rejected with reasons |
| 18 | Workflow IDs are stable and provider-independent | **PASS** | 49 unique IDs; none encodes a vendor, version, organisation, person or scale band |
| 19 | Participation vocabulary consistent across template and exemplars | **PASS** | All 5 types defined in the design document and the template and used in all 4 exemplars; no undefined participation term anywhere; 0 RACI or approver-role terms |
| 20 | All Phase 5 artifacts remain PROPOSED | **PASS** | All 8 artifacts carry `Status: PROPOSED`; 0 `APPROVED` or `CANONICAL` |

**20/20 PASS.**

### Additional check not in the required list

**Referential integrity of every ID cited by the exemplars** — 0 unknown `role.<id>`, 0 unknown `decision.<id>`, 0 unknown `review.<id>`, 0 unknown `artifact.<id>`. Every identifier referenced across the four exemplar cards resolves to an existing entry in the approved Phase 3 Role Registry. This was added because a Workflow Card that cites a decision right or artifact that does not exist would pass every authority check above while being unusable.

### Honesty note on the checks themselves

The first run of this suite reported 14/20. Six failures were investigated individually:

- **Four were genuine content gaps** and were fixed in the cards, not in the checks: the EU grant card lacked a general no-authority clause; the project-development card did not name its gates as *human decision rights* in the authority section; three cards used inconsistent phrasing for the criticality/Role-identity rule; and the software-delivery card never used `CONSULTED_ROLE` at all, having typed the architect's deviation consultation at S3 as a contributing role, which was the wrong participation type for input that produces no artifact.
- **Two were defects in the checks**: check 18 flagged `workflow.large_project_readiness` and `workflow.small_project_readiness`, which appear only in the *rejected candidates* table as examples of what must not be created; and check 19 required all five participation types in every card, which is not the rule — the rule is that every term used is one of the five. Both checks were corrected to test the actual property.

No check was weakened to obtain a pass.

---

## 2. Architecture ambiguities

Stated rather than resolved. Each is a real question the foundation leaves open.

1. **How a composed Workflow is expressed.** `workflow.decision_grade_document_preparation` is designed to be composed into other Workflows rather than duplicated by them, but the foundation defines no composition primitive — no `INCLUDES`, no sub-workflow reference. Four exemplars were not enough to know whether composition needs its own primitive or whether stage-level referencing suffices.
2. **Partial ordering is asserted but not expressed formally.** Cards state in prose which stages may run in parallel. There is no notation for it. This is deliberate — a notation risks becoming the runtime DSL the phase prohibits — but it means parallelism is not machine-checkable.
3. **Where a Workflow's own version binds.** If a Workflow version changes mid-instance, the foundation does not say whether the instance continues on the old version or migrates. This is arguably a runtime question, but the answer constrains registry design.
4. **`COMPLETE_WITH_OPEN_ITEMS` has no severity model.** The outcome exists and requires open items to be named and carried, but nothing distinguishes a trivial open item from a gate-critical one except the criticality-band rules in individual cards. A shared severity vocabulary may be needed.
5. **Trigger expression.** Triggers are stated in prose. Whether the registry eventually needs a controlled trigger vocabulary — as the Skill Registry needed one for relationship types — is untested at four exemplars.
6. **The Document Owner Role parameterisation in Exemplar D.** It is the only exemplar with a variable lead Role. The foundation does not say whether parameterised Role slots are a general registry feature or a one-off for the generic document pattern.
7. **Interaction with System Control Profiles.** The design states that a Workflow Controller may later *select* a Workflow and that selection is not authorship. What "selection" may legitimately consider — and whether a control profile may narrow a Workflow at selection time — is not specified.

## 3. Likely overlap groups

Eight groups are flagged in `workflows/master-workflow-universe.md` §11 and are not resolved here. In summary:

1. The generic document pattern versus every document-producing Workflow — is composition real, or will the generic pattern become a mega-workflow?
2. Business case / strategic option appraisal / project definition and scoping.
3. Competitive bid / EU grant application / commercial proposal — three governed submissions under deadline.
4. Software change delivery / data platform change delivery — same shape, different terminal gate.
5. Bankability assessment / IFI appraisal readiness — possibly Pack activation rather than two Workflows.
6. Standalone risk cycle versus risk stages embedded everywhere.
7. Evidence base construction versus the generic document pattern's S1.
8. Grant periodic reporting / grant amendment — same Roles, same gate.

Resolving these requires more carded exemplars. The Phase 4 experience is directly relevant: overlap resolution driven by *actual mapping data* found real merges that inspection alone had not, and the equivalent here is participation and gate data across a wider exemplar set.

## 4. Deferred to Phase 6 — Handoff & Review

- **Review Profile identity and methodology.** Every `review.<id>` in every Phase 5 artifact is a *requirement reference* with no definition behind it. What each review covers, who is independent for it, its materiality and severity criteria, and when it is satisfied are all Phase 6.
- **What satisfies a review requirement.** Phase 5 states that producer quality control does not. It does not state what does.
- **Handoff semantics between Roles.** Phase 5 says a contribution is made and attributed; it does not define the handoff act, what accompanies it, or what the receiving Role may assume.
- **Review-triggered rework.** Rework loops are defined for internally detected failures. Rework triggered by an independent review's findings needs the review model first.
- **Reviewer independence against workflow participation.** Whether participating in a Workflow disqualifies a Role from reviewing its output is a Phase 6 question with a Phase 5 shadow: the constraints prohibit a stage from reviewing itself, but the general rule belongs to the Review Profile Registry.

## 5. Deferred to Phase 7 — Decision Rights / Human Approval

- **The Decision Rights Register itself.** Every `decision.<id>` referenced in Phase 5 is drawn from the approved Role Cards, but the register that defines each right — who holds it, how it is delegated, what evidence it requires, how it is recorded — is Phase 7.
- **Gate satisfaction semantics.** Phase 5 says a Workflow makes a decision *due* and never satisfies it. What satisfaction looks like, and how a Workflow instance observes it, is Phase 7.
- **Emergency and delegated authority.** The software exemplar routes emergency change to `decision.emergency_production_change` and states an emergency gate is still a gate. The actual emergency-authority model is Phase 7.
- **Decision reversal and its effect on completed Workflows.** Not addressed anywhere in Phase 5.
- **Who may cancel a Workflow instance.** Cancellation criteria are defined; cancellation *authority* is not.

## 6. Deferred to runtime phases

Instance state persistence, scheduling, assignment, notification, parallelism execution, retry, timeout, monitoring, model routing, agent binding, database schema, API surface and user interface. None is specified, implied or constrained by Phase 5 beyond the standing rule that a runtime validates against the registry rather than mutating it.

## 7. Standing statement

Every Phase 5 artifact is `PROPOSED`. Nothing in the Workflow Registry is APPROVED or CANONICAL, and inclusion in the Master Workflow Universe confers no approval on any Workflow. Four of 49 candidates are carded; the other 45 are one-sentence candidates that have not been validated, and card generation for them is not authorised by this record.

This self-check does not claim human approval and is not an independent audit.
