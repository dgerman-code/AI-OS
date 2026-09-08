# Phase 6 — Handoff & Review Foundation Self-Check

Status: PROPOSED — READY FOR INDEPENDENT PHASE 6 FOUNDATION AUDIT

Branch: `architecture/phase-6-handoff-review`
Baseline: Phase 5 human-approval commit `97b02e897c86cfa059a453b8e26c166b6dd134d0`

This is a **self**-check by the producing pass. Under this phase's own architecture it is `PRODUCER_REVIEW` — internal quality control, which by `standard.review.common_constraints` §4 cannot satisfy an independent review requirement. It is named that way deliberately: the first thing the Phase 6 model should be able to classify is this document.

## Artifacts covered

| File | Purpose |
|---|---|
| `architecture/handoff-review-registry-design.md` | Handoff model, Review Profile model, independence classes, finding taxonomy, satisfaction semantics, rework, criticality |
| `reviews/_standards/common-review-constraints.md` | 19 enforceable review rules |
| `reviews/_templates/review-profile-card-template.md` | Mandatory Review Profile Card structure |
| `reviews/master-review-profile-universe.md` | 9 families, 34 candidates, 4 consolidation proposals, 6 overlap groups, all 44 existing references accounted for |
| `handoffs/_standards/common-handoff-constraints.md` | 16 enforceable handoff rules |
| `handoffs/_templates/handoff-card-template.md` | Mandatory Handoff Card structure |
| `reviews/exemplars/` × 6 | Review Profile exemplars |
| `handoffs/exemplars/` × 4 | Handoff exemplars |

---

## 1. Check results — 36 checks

| # | Check | Result | Evidence |
|---:|---|---|---|
| 1 | Phase 3 Role Cards unchanged | **PASS** | `git diff 97b02e8 -- roles/` empty |
| 2 | Approved Phase 4 architecture/mappings unchanged | **PASS** | `git diff` empty over `skills/` and the three Phase 4 architecture files |
| 3 | Approved Phase 5 Workflow architecture unchanged | **PASS** | `git diff` empty over `workflows/` and the Phase 5 design. Phase 6 references Phase 5 and alters nothing in it — no downstream edit proved necessary |
| 4 | All Phase 6 artifacts `PROPOSED` | **PASS** | 17 artifacts, all `PROPOSED` |
| 5 | Core identity separation preserved | **PASS** | 8-way separation stated in design §0 |
| 6 | Handoff never transfers professional ownership | **PASS** | Handoff constraints §1; retention stated per sender in all 4 cards |
| 7 | Receipt never implies review/approval/canonical | **PASS** | All 4 cards enumerate the four negations naming `REVIEWED`, `APPROVED`, `CANONICAL`; constraints §2–4 |
| 8 | Review Profile never creates a Decision Right | **PASS** | Review constraints §2; Decision Right Boundary section in all 6 |
| 9 | Review Profile never self-approves/canonicalizes | **PASS** | Review constraints §3; all 6 state satisfaction is not approval |
| 10 | Producer QC cannot satisfy independent review | **PASS** | Review constraints §4; `PRODUCER_REVIEW` exists as a named class precisely so it can be recognised as not independent |
| 11 | Independent reviewer cannot be producer in same assignment | **PASS** | Review constraints §7; Reviewer Prohibitions in all 6 |
| 12 | Independence cannot be manufactured by naming a Role | **PASS** | Review constraints §6; design §3.2(4) |
| 13 | Review satisfaction semantics explicit | **PASS** | 7 statuses in design §5.1; Satisfaction Criteria in all 6 |
| 14 | Review performed ≠ satisfied | **PASS** | `REVIEW_PERFORMED_WITH_OPEN_FINDINGS` is a distinct status; constraints §9 |
| 15 | Satisfied ≠ approval | **PASS** | Design §5.3; constraints §10 |
| 16 | Finding severity/materiality semantics explicit | **PASS** | Design §4.2; constraints §11; mapped to Phase 5 §14A |
| 17 | Critical finding blocks satisfaction | **PASS** | All 6 exemplars state it can never be satisfied; constraints §12 |
| 18 | Major finding handling explicit | **PASS** | All 6 state blocking and whether a bounded conditional disposition is permitted — 3 permit one, 3 permit none |
| 19 | Review cannot waive finding | **PASS** | Constraints §13; design §4.3 |
| 20 | Material change creates re-review/staleness | **PASS** | Re-Review Triggers in all 6; `STALE` status |
| 21 | Rework preserves finding/provenance/version history | **PASS** | Constraints §15; design §6; Rework and Closure in all 6 |
| 22 | Handoff package carries assumptions/conflicts/unknowns | **PASS** | `OPEN_ITEM_CARRY` with `CONFLICT_DETECTED` and `UNKNOWN` classes in all 4 |
| 23 | Handoff blocks/returns on material incompleteness | **PASS** | `RETURN_FOR_REWORK` and `HANDOFF_BLOCK` in all 4; constraints §8 |
| 24 | All 6 exemplar reviews have bounded scope/out-of-scope | **PASS** | 6/6 |
| 25 | All 6 exemplar reviews have reviewer eligibility/prohibitions | **PASS** | 6/6 |
| 26 | All 4 handoff exemplars have sender/receiver/subject/package/receipt/rework | **PASS** | 4/4 |
| 27 | Master Review Universe is 20–35 candidates | **PASS** | 34 standalone candidates |
| 28 | Duplicate Review IDs = 0 | **PASS** | 34 IDs, 34 unique |
| 29 | Universe flags overlaps/duplicates instead of mass-carding | **PASS** | 4 consolidation proposals and 6 overlap groups recorded, **none applied**; 6 of 34 carded |
| 30 | No runtime/database/API/orchestrator/model implementation | **PASS** | No model, vendor, framework, queue or schema anywhere; Non-Runtime Statement in all 10 cards and design §9 |
| 31 | No PR created | **PASS** | — |
| 32 | No Phase 6 artifact marked APPROVED/CANONICAL | **PASS** | 0 |
| 33 | Phase 5 forward `review.<id>` references classified | **PASS** | All 26 Phase 5 review references resolve to a standalone candidate Profile; none depends on a held or consolidation-proposed ID, so no Phase 5 card needed amendment |
| 34 | No Review Profile grants cross-domain conclusion authority | **PASS** | `CROSS_DOMAIN_REVIEW` explicitly cannot conclude on the domain it checks across; every out-of-scope list names the owning review |
| 35 | No Handoff or Review changes Role-to-Skill compatibility | **PASS** | Handoff constraints §10; design §8; 0 capability-granting statements |
| 36 | Criticality changes depth, not identity | **PASS** | Criticality Scaling in all 10 cards; design §7 prohibitions |

**36/36 PASS.**

### Additional check not in the required list

**Referential integrity across all 10 exemplar cards** — 0 invalid `role.<id>`, 0 invalid `artifact.<id>`, 0 invalid `decision.<id>`, 0 invalid `skill.<id>` / `specialisation.<id>` / `skill_pack.<id>`. Every identifier resolves to an approved Phase 3 or Phase 4 entry. Added because a card citing a non-existent artifact or decision right would pass every authority check above while being unusable.

### Honesty note on the checks

The suite first reported 31/36. All five failures were investigated and **all five were genuine content gaps**, fixed in the cards rather than in the checks:

- three Handoff cards stated the receipt negations incompletely, omitting `APPROVED` / `CANONICAL` by name where the fourth card named them;
- two Handoff cards carried no `CONFLICT_DETECTED` class in their open-item carry, and one carried no `UNKNOWN` class — a real omission, since a converging or diverging handoff is exactly where conflicting positions arrive;
- `review.project_integration_coherence` never stated that satisfaction is not approval, which `standard.review.common_constraints` §10 requires of every Profile;
- two other Profiles stated it only obliquely.

One check evidence line was also corrected: check 27's count regex did not match candidate rows carrying the exemplar marker, so it reported 28 standalone candidates where the file contains 34. The check passed either way; the reported figure was wrong and is now right.

No check was weakened.

---

## 2. Open architecture questions

Each classified. None hidden.

| # | Question | Disposition | Reasoning |
|---:|---|---|---|
| 1 | Does Review Profile composition/dependency need a first-class declarative reference? | **SAFE TO DEFER WITH EXPLICIT RULE** | The template's "any dependency on another review" field and the out-of-scope statement together express dependency adequately at six exemplars. A `REVIEW_REFERENCE` primitive analogous to Phase 5's `WORKFLOW_REFERENCE` may be warranted later; the rule until then is that a dependency is stated in prose and is testable. |
| 2 | May one Review Profile require another as prerequisite? | **SAFE TO DEFER WITH EXPLICIT RULE** | Two exemplars imply it — `review.project_integration_coherence` is meaningless before the domain reviews it checks across, and `review.security` consumes QA's security testing. The explicit rule for now: a Profile may name a prerequisite review, and where the prerequisite is `NOT_SATISFIED` the dependent review is `REVIEW_BLOCKED`, not failed. Formalising prerequisite chains needs a wider exemplar set. |
| 3 | May one reviewer instance satisfy multiple compatible Review Profiles? | **MUST RESOLVE IN PHASE 6 FOUNDATION** — **and it is not resolved.** | This is the one question the foundation should have answered and did not. It bears directly on independence: a single reviewer satisfying `review.architecture`, `review.security` and `review.data_architecture` on one change may be efficient and may also be a concentration that defeats the purpose. The foundation states eligibility per Profile and is silent on multi-Profile satisfaction by one instance. **Flagged as the primary gap for the independent audit.** |
| 4 | Should eligibility include organisational independence as well as Role/assignment independence? | **PHASE 7 CONCERN** | Organisational independence is about who employs and directs the reviewer, which is authority structure. Phase 6 defines independence relative to the *work*; who is organisationally separate is a decision-rights question. |
| 5 | One shared material-change rule for staleness, or Profile-specific triggers? | **SAFE TO DEFER WITH EXPLICIT RULE** | Currently Profile-specific, and the six exemplars show genuinely different triggers — a superseded legal source and a changed model input are not the same event. The rule until then: every Profile states its own triggers explicitly and a missing trigger section is a defect. A shared floor may emerge once more Profiles are carded. |
| 6 | Are Handoff Cards first-class registry entries, or reusable patterns embedded in Workflows? | **SAFE TO DEFER WITH EXPLICIT RULE** | Built here as first-class, because the same transfer recurs across Workflows and embedding would duplicate it. The rule: a Handoff is first-class where the transfer is reusable across more than one Workflow, and Phase 5 Workflow cards are unchanged and continue to reference neither. Whether Workflows should carry explicit handoff references is a later integration question. |
| 7 | How is review satisfaction later recorded and observed by a Workflow runtime? | **RUNTIME-PHASE CONCERN** | The registry defines what satisfaction *means* and what makes it stale. How an instance records who reviewed what, and how a Workflow observes the status, is execution. The standing rule holds: the runtime validates against these semantics and cannot redefine them. |
| 8 | How may a Phase 7 Decision Right permit exceptional progression without converting unsatisfied review into satisfied review? | **PHASE 7 CONCERN** — with a Phase 6 constraint already fixed | Phase 6 has done its half: a Decision Right may permit *progression* past an unsatisfied review, and the review **remains `NOT_SATISFIED`** — the Profile records the gate reference and never relabels its own status. What granting such a right means, who holds it and how it is exercised is entirely Phase 7. |

## 3. Additional findings surfaced during construction

1. **`review.security` may have no eligible reviewer.** On a single-security-engineer assignment, the only fully-qualified peer does not exist, and the Profile therefore resolves to `NOT_SATISFIED` with the Workflow blocked. This is the correct architectural answer and an uncomfortable operational one; it is recorded rather than softened.
2. **`role.security_engineer` is both sender and receiver** on `handoff.software_implementation_to_security_and_test_review`, under the approved Phase 5 M3 correction. The handoff card states explicitly that this produces a legitimate owned assessment and leaves `review.security` entirely unsatisfied.
3. **34 candidates sits at the top of the 20–35 target.** That is deliberate: forcing merges the evidence does not support would be the more damaging error, and four consolidation proposals plus six overlap groups are recorded instead of applied.

## 4. Standing statement

Every Phase 6 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. This record does not claim human approval and is not an independent audit — by this phase's own definitions it is `PRODUCER_REVIEW`. Six of 34 candidate Review Profiles are carded; 28 remain unvalidated one-line candidates and the 10 held IDs must not be carded at all until their consolidation or overlap question is decided.
