# Phase 6 — Foundation Remediation After Independent Audit

Status: `PROPOSED — READY FOR FINAL INDEPENDENT PHASE 6 FOUNDATION RE-AUDIT`

Branch: `architecture/phase-6-handoff-review`
Audited foundation baseline: `cd3f3fcd25a20a1bb0a24c556681079209deb5b0`

The independent audit returned **FAIL** with three HIGH and three MEDIUM findings. Upstream Phase 3/4/5 immutability, the Handoff identity model, `review.security`, `review.legal_compliance`, reference integrity and the non-runtime boundary all passed and are unchanged except where a finding required it.

This is one bounded consolidated remediation covering H1–H3 and M1–M3. No Role, Skill, Workflow or Decision Right was created or modified; no consolidation was applied; no additional Profile or Handoff was carded.

---

## H1 — Project Integration Coherence satisfaction and closure loophole

**Defect.** The Profile could be read as satisfied or closed when a contradiction was merely *recorded*. Two phrases did it: satisfaction required that "no **unrecorded** contradiction exists", implying a recorded one was acceptable; and closure required that the owning Roles "either reconcile their positions **or** that the contradiction is carried explicitly as an open item to the decision-maker". The second branch closed a finding by describing it.

**Correction.**

Satisfaction now requires that **every material contradiction has been resolved by the Roles that own those positions**. A new subsection states the rule directly:

- a material contradiction is a `MAJOR_FINDING` or `CRITICAL_FINDING` and **remains an open review finding until the owning Roles resolve it**;
- while unresolved, status is `NOT_SATISFIED` or `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`;
- it **cannot become `SATISFIED` because it is recorded, made visible, attributed, escalated, or carried to a human gate** — each of those acts is correct and necessary, and none satisfies the review. *Visibility is not resolution.*

A named external `decision.<id>` may permit **Workflow progression** with the contradiction unresolved. Four explicit negations now attach to that route: it does not close the finding; it does not satisfy the review; it does not convert the contradiction into a minor or non-material item; the contradiction remains open and is carried forward.

Closure now requires **evidence that the owning domain Roles have actually reconciled or otherwise resolved** the contradiction — a revised position, or a joint statement that the apparent conflict was a difference of scope rather than substance. Re-review is mandatory after any `CRITICAL` closure and after any `MAJOR` closure that changed a cited position.

Added explicitly: **the integration reviewer must not settle the underlying specialist disagreement itself.** It identifies, attributes to both owning Roles, and stops. A reviewer that adjudicates has taken authority in both domains, which `CROSS_DOMAIN_REVIEW` denies it — reproducing one level up the exact failure this Profile exists to catch in the assembling Role.

---

## H2 — EU Programme Compliance "record it and continue" loopholes

**Defect.** Three dimensions treated *visibility* as sufficient: "every rulebook requirement is addressed, **or its gap is explicit**"; "every eligibility condition has an **evidenced status**"; "every factual claim is verified **or marked**".

**Correction.** Satisfaction is now a four-row table separating what supports it from what is an open finding, with the governing statement that **recording, marking or making something visible satisfies none of them**.

| Dimension | Supports satisfaction | Open finding |
|---|---|---|
| **Rulebook requirements** | Requirement met; or **verified not applicable** with evidence and rationale | Unmet, unresolved, or recorded as a gap — normally `MAJOR_FINDING` |
| **Eligibility conditions** | Assessed and **satisfied**; or **verified not applicable** where programme rules genuinely permit N/A | Unmet, `UNKNOWN`, unassessed, or evidenced as not-satisfied — `CRITICAL_FINDING` where asserted satisfied without basis |
| **Factual claims** | Material claim **verified** against required evidence; or claim explicitly identified as **non-material** and permitted by these criteria | Material claim marked, flagged or recorded but still unverified |
| **Cost eligibility** | Assessed against programme rules, budget internally consistent | Any budget line with unassessed eligibility |

The load-bearing distinction is stated in prose as well: **verified not applicable** is finished work with evidence behind it; an **unresolved gap** is absent work with a note attached. The earlier revision conflated them, and an evidenced status is now explicitly *a record, not a pass*.

The Decision Right boundary is restated: a human gate may permit progression with an open finding; it does not close the finding and does not change the review's status.

---

## H3 — Reviewer eligibility must not widen upstream Role scope

**Defect.** Eligibility lists named Roles whose approved scope covers only one dimension of a Profile without saying so, letting partial expertise read as full-Profile authority. `review.eu_programme_compliance` was the clearest case: it declared the financial-compliance Role "eligible for the rest" of the package once its own assessment was excluded, which is scope widening by declaration.

**Correction — a registry-wide rule**, in design §3.3, constraints §7A and the template:

| Class | Meaning |
|---|---|
| `FULL_PROFILE_REVIEWER_ELIGIBLE` | Approved Role scope already covers **every** satisfaction criterion and professional conclusion the Profile requires |
| `BOUNDED_REVIEW_CONTRIBUTOR` | Scope covers one dimension; may contribute a bounded check and **cannot satisfy the whole Profile** |

Five normative rules: full-Profile eligibility requires full scope; **partial expertise does not aggregate into full Profile authority**; Phase 6 never widens Role scope; Profile wording cannot make a Role eligible by declaration; and where no Role is fully eligible the Profile remains `NOT_SATISFIED` — cross-role authority is never invented by aggregation.

Every eligibility list in all six exemplars was converted to a table declaring the class, the Role Card scope basis, and the dimension covered. **All six were audited, not only the three the audit named.**

| Profile | Full-Profile eligible | Bounded contributors |
|---|---|---|
| `review.evidence_integrity_provenance` | A second Knowledge & Evidence Steward instance | Accounting & Financial DD (reconciliation and financial-evidence consistency); Data Room & Disclosure Manager (provenance and package integrity of a disclosure set) |
| `review.financial_model` | A second Financial Modelling Specialist instance | Accounting & Financial DD (reconciliation, tie-out, evidence consistency, due diligence); Funding & Bankability (whether outputs support the bankability use) |
| `review.legal_compliance` | A second Legal & Regulatory Lead instance | Procurement/State Aid, Data Protection, Tax — each to its own perimeter |
| `review.project_integration_coherence` | Portfolio/Programme Manager; a second Project Development Lead from outside the assignment | Knowledge & Evidence Steward (citation fidelity and traceability only) |
| `review.eu_programme_compliance` | A second EU Grants & Programmes Specialist instance | EU Programme Implementation (rulebook conformity); Grant Financial Compliance (budget and cost eligibility only); Deliverables/Reporting (reporting-schedule conformity) |
| `review.security` | A second Security Engineer instance who neither designed nor implemented the controls | Solution Architect (control-to-architecture consistency); Data Protection (controls implementing a DP obligation) |

Each Profile's Reviewer Prohibitions now also names its bounded contributors as **prohibited satisfiers** — prohibited from full-Profile satisfaction, not from contributing.

Two corrections the audit called out specifically: the Data Room Manager is bounded to provenance and package integrity and no longer implies capability over evidential-quality criteria its Role Card excludes; the Accounting & DD Role is bounded to reconciliation and tie-out on the financial model, with full satisfaction resting solely with the Role whose scope includes financial modelling methodology.

---

## M1 — Multi-Profile reviewer-instance rule

**Resolved in the foundation.** This was the gap the foundation pass itself flagged as its primary unresolved question.

A single reviewer instance may satisfy multiple Profiles only where all seven hold, **for each Profile, each subject, each artifact version and each assignment**: eligibility passes separately; independence passes separately; satisfaction of one grants nothing to another; the reviewer does not review its own output from another Profile where that output is the second review's subject or evidence; **no Profile declares `SEGREGATION_REQUIRED`**; no declared dependency or conflict condition requires separate instances; and combining Profiles creates no cross-domain authority by accumulation.

New declared field on every Profile:

```
Reviewer Instance Segregation: ALLOWED_IF_INDEPENDENTLY_ELIGIBLE | SEGREGATION_REQUIRED
```

**Default for decision-grade and high-criticality work covering interdependent domains is `SEGREGATION_REQUIRED`.** The reasoning is concentration: where two Profiles check different aspects of one interdependent subject, a single reviewer's blind spot propagates into both and the second review stops being a second look.

Applied to all six with a reason:

| Profile | Declaration | Reason |
|---|---|---|
| `review.evidence_integrity_provenance` | `ALLOWED_IF_INDEPENDENTLY_ELIGIBLE` | Checks the evidence base *underneath* conclusions rather than any conclusion; no blind spot propagates between it and a domain Profile |
| `review.legal_compliance` | `ALLOWED_IF_INDEPENDENTLY_ELIGIBLE` | Its bounded contributors carry their own Profiles, and a bounded perimeter contribution cannot substitute for this Profile's conclusion |
| `review.financial_model` | `SEGREGATION_REQUIRED` at Enhanced Decision-Grade and above | Its inputs are separately reviewed; one instance satisfying both would let a single reading of an assumption pass twice as two independent checks |
| `review.eu_programme_compliance` | `SEGREGATION_REQUIRED` at Enhanced Decision-Grade and above | One instance also satisfying the evidence Profiles would check the claims and the evidence under them with one reading |
| `review.project_integration_coherence` | **`SEGREGATION_REQUIRED`** | The most conservative declaration, deliberately: the contradiction it hunts sits exactly where a domain reading is wrong, so an instance carrying that reading in would defeat the purpose |
| `review.security` | **`SEGREGATION_REQUIRED`** | Concentration most defeats the purpose here; combined with already narrow eligibility this makes the Profile demanding, which is the point |

No staffing algorithm, assignment logic or human allocation is defined.

---

## M2 — Declarative Review Profile dependency model

**Resolved in the foundation** with one bounded primitive, `REVIEW_DEPENDENCY`, in design §3.5, constraints §7C, the template and four exemplars.

A declaration names a **concrete prerequisite `review.<id>`** — never a category — with a required status, an objective activation condition where conditional, and a bounded purpose. Eight normative rules: an unsatisfied, `STALE` or missing prerequisite gives **`REVIEW_BLOCKED`, not failed**; **satisfaction is not transitive**; the dependency transfers nothing; self-dependency is prohibited; transitive cycles are prohibited as an architecture validation rule; conditional triggers must be objective; the dependency executes nothing and adds no runtime semantics; and the dependent Profile still evaluates its own evidence and criteria independently.

Usage across the six — dependencies were **not** manufactured for symmetry:

| Profile | Dependencies |
|---|---|
| `review.project_integration_coherence` | **Six concrete prerequisites**, each activated only where the corresponding position is actually cited and the band is Enhanced Decision-Grade or above. Below that band the dependency does not activate, because consistency checking has value on `DRAFT` positions and blocking it would remove the early warning it exists to give |
| `review.financial_model` | `review.cost_estimate` and `review.evidence_integrity_provenance`, both at Enhanced Decision-Grade and above |
| `review.security` | `review.architecture`, where the change alters the architecture position at Enhanced Decision-Grade and above |
| `review.evidence_integrity_provenance` | **None** — it is a prerequisite for others; a foundation check waiting on the conclusions built atop it would be inverted |
| `review.legal_compliance` | **None** — performable on a stated, attributed factual basis; making the evidence Profiles prerequisites would block a check that can run |
| `review.eu_programme_compliance` | **None** — an unverified material claim is an open finding *here*; making `review.factual_evidence` a prerequisite would convert a finding this Profile is designed to raise into a blocker preventing it from raising anything |

---

## M3 — Closed Handoff sender eligibility

**Defect.** `handoff.application_content_to_compliance_review` named "each conditionally activated specialist Role" — not a closed, testable sender set.

**Resolved by Option A, explicit enumeration**, as the prompt preferred. The card is a known grant-application handoff and its source structure showed no genuine reusable-slot need, so a slot would have been the more complex and less honest answer.

Seven senders enumerated, each with its objective activation trigger, its exact package contribution and what it retains: EU Grants & Programmes (`ALWAYS`); Legal & Regulatory; Data Protection; Procurement/State Aid; Institutional Communications; Learning/VET Design; Monitoring, Evaluation & Learning (each `CONDITIONAL` on a stated condition).

Every trigger is the same objective condition the approved Phase 5 `workflow.eu_grant_application_development` participation table already declares — **the Handoff narrows to that set and widens nothing.** The card states that a Role not in the table cannot send, and `RETURN_FOR_REWORK` now triggers on a section attributed to a Role outside the enumerated set.

`handoff.software_implementation_to_security_and_test_review` already carried an enumerated five-sender table but introduced it with wording that could read as open; it now states the set is closed. The other two handoffs were already closed.

---

## Universe and consolidation constraints

Counts unchanged: **9 families, 34 standalone candidates, 6 exemplar Review Profiles, 4 exemplar Handoffs, 6 overlap groups open.** No additional carding.

**None of the four proposed consolidations is applied**, and the independent audit's constraint against each is now recorded in the universe file so a later pass starts from the constraint rather than the proposal:

- `grant_compliance → eu_programme_compliance` — not safe without proving all grant contexts are EU-programme contexts; a national, foundation or bilateral donor rulebook would be left with no Profile;
- `ifi_appraisal_readiness → bankability` — may lose IFI-specific safeguard, procurement and institutional-compliance scope; the proposal assumed the scope was identical and the audit found it is not;
- `ppp_structure → commercial_structure` — may collapse public-interest, procurement, legal and value-for-money review into a commercial mega-review, breaching the bounded-scope rule;
- `financial_evidence → factual_evidence` — plausible **only if** financial reconciliation requirements remain explicit; a trigger alone does not carry reconciliation and tie-out.

Three of the four are materially weaker as proposals than when first recorded, and the fourth is conditional. They are proposals **under constraint**, not a queue of pending merges.

---

## Open-question dispositions after remediation

Updated in `reviews/phase-6-foundation-self-check.md`, which previously showed 1–3 as deferred or unresolved:

| # | Question | Disposition |
|---:|---|---|
| 1 | First-class Review Profile dependency reference | **RESOLVED IN FOUNDATION** — bounded `REVIEW_DEPENDENCY` |
| 2 | One Profile requiring another as prerequisite | **RESOLVED IN FOUNDATION** — same mechanism; `REVIEW_BLOCKED`, non-transitive |
| 3 | One reviewer instance satisfying multiple Profiles | **RESOLVED IN FOUNDATION** — seven per-Profile conditions plus the segregation field on all six |
| 4 | Organisational independence in eligibility | **SAFE TO DEFER WITH EXPLICIT RULE** — assignment-level independence stays mandatory; organisational structures not invented here |
| 5 | Shared vs Profile-specific staleness | **SAFE TO DEFER WITH EXPLICIT RULE** — Profile-specific triggers remain normative |
| 6 | Handoff Cards first-class vs embedded | **SAFE TO DEFER WITH EXPLICIT RULE** — first-class only for reusable governed transfer semantics |
| 7 | Runtime observation of review satisfaction | **RUNTIME-PHASE CONCERN** |
| 8 | Exceptional progression via Decision Rights | **PHASE 7 CONCERN**, with the standing Phase 6 rule fixed: progression never converts unsatisfied review to satisfied |

---

## Regression validation

**All 50 checks PASS**, verified mechanically against baseline `cd3f3fc`.

Upstream immutability: `git diff` empty over `roles/`, over `skills/` and the three Phase 4 architecture files, and over `workflows/` and the Phase 5 design. Handoff receipt and ownership semantics unchanged — the handoff standard and template are byte-identical to the audited baseline. `review.security`'s single-producing-engineer case remains safe and is reinforced by `SEGREGATION_REQUIRED`; `review.legal_compliance`'s analysis-not-opinion boundary is intact. Reference integrity: 0 invalid `role.`, `artifact.`, `decision.` or capability references. No `decision.<id>` is defined, granted or exercised anywhere — all remain forward references to Phase 7. No runtime, database, API, UI, orchestrator, model or agent element introduced.

### Honesty note

The suite first reported 47/50. Three failures were investigated:

- **Check 24 was a genuine defect.** `review.project_integration_coherence` declared its prerequisite as "the domain review applicable to each cited position", listing examples — a category, which M2 explicitly prohibits and which is not testable. It is now **six concrete prerequisite rows**, each with its own activation condition tied to a specific cited artifact.
- **Check 46 was a genuine gap.** The audit's four consolidation constraints were not recorded anywhere. They are now a table in the universe file.
- **Check 12 was a check artifact.** It forbade the literal phrase "eligible for the rest", which now survives only *inside the note recording its removal*. The check was made stricter, not weaker: it now requires both that the phrase does not appear as an assertion and that the correction note explaining its removal is present.

One further check-mechanics correction: check 46's string match was case-sensitive against text that begins the sentence with a capital. No check was weakened to obtain a pass.

---

## Standing statement

Every Phase 6 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. This record does not claim human approval and is not an independent audit — under this phase's own definitions it is `PRODUCER_REVIEW`. Six of 34 candidate Review Profiles are carded and four Handoffs; no additional carding was performed.
