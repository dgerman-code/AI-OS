# Common Review Constraints

Status: PROPOSED — Phase 6 standard candidate
Standard ID: `standard.review.common_constraints`
Version: 0.1

Every Review Profile Card inherits this document by reference and does not repeat it. Where a Review Profile Card contradicts this standard, this standard governs and the card is defective.

## 1. Review grants no professional authority

Performing or being eligible for a review grants a Role nothing beyond its own Role Card. A reviewer does not acquire the producing Role's methodology, scope or conclusions by examining them, and does not acquire authority in the reviewed domain by being competent to check it.

## 2. A Review Profile cannot create a Decision Right

A Profile may reference a `decision.<id>`. It may not create one, name a holder, define delegation, or state what exercising it means. Phase 7 owns all of that.

## 3. A Review Profile cannot approve or canonicalize an artifact

The most a review can support is a governed transition to `REVIEWED`, and only where a separately governed knowledge-state rule permits it. `APPROVED` and `CANONICAL` are unreachable from any review outcome.

## 4. Producer quality control cannot satisfy independent review

`PRODUCER_REVIEW` is internal QC. It has a name so it can be recorded, not so it can be counted. Where a requirement declares `PEER_REVIEW`, `CROSS_DOMAIN_REVIEW` or `INDEPENDENT_ASSURANCE_REVIEW`, no amount of producer self-checking satisfies it.

## 5. Reviewer eligibility must be independently checkable

Eligibility is stated so that it can be tested against the producing assignment and the Workflow participation record — who produced the subject, who led the stage, who owns the conclusion. A constraint that cannot be checked against those facts is not an eligibility rule.

## 6. Independence cannot be declared by prose

Neither a Review Profile nor a Workflow makes a Role independent by saying it is. Independence is the **absence of a producing relationship** to the subject in that assignment instance, and it is established by that absence, never by assertion.

## 7. A reviewer cannot review a conclusion it produced in the same assignment

Owning the same class of conclusion on another assignment is normal and is what makes a competent peer reviewer. Owning **this** conclusion, in **this** assignment instance, is disqualifying.

## 7A. Full-Profile eligibility requires full Role scope

Every Reviewer Eligibility entry declares one of two classes:

- **`FULL_PROFILE_REVIEWER_ELIGIBLE`** — the Role's approved scope already covers **every** satisfaction criterion and professional conclusion the Profile requires;
- **`BOUNDED_REVIEW_CONTRIBUTOR`** — the Role's approved scope covers one dimension; it contributes a bounded check and **cannot satisfy the whole Profile**.

**Partial expertise does not aggregate into full Profile authority.** Two bounded contributors covering the Profile's dimensions between them do not produce a full-Profile satisfaction unless the Profile explicitly declares a multi-reviewer composition with individually governed bounded contributions.

**Phase 6 never widens Role scope**, and Profile wording cannot make a Role eligible by declaration — eligibility is checked against the Role Card. Where no Role is fully eligible, the Profile remains `NOT_SATISFIED`; cross-role authority is never invented by aggregation.

A Role listed in an eligibility table without a class is a defect.

## 7B. Multi-Profile reviewer instances

One reviewer instance may satisfy more than one Profile only where, **for each Profile, subject, artifact version and assignment**, all seven hold: eligibility passes separately; independence passes separately; satisfaction of one grants nothing to another; the reviewer does not review its own output from another Profile where that output is the second review's subject or evidence; **no Profile declares `SEGREGATION_REQUIRED`**; no declared dependency or conflict condition requires separate instances; and combining Profiles creates no cross-domain authority by accumulation.

Every Profile declares `Reviewer Instance Segregation: ALLOWED_IF_INDEPENDENTLY_ELIGIBLE | SEGREGATION_REQUIRED`. **The default for decision-grade or high-criticality work spanning interdependent domains is `SEGREGATION_REQUIRED`**, unless the Profile states defensibly why same-instance review preserves the separation it depends on.

This is architecture eligibility. It defines no staffing, assignment or allocation logic.

## 7C. `REVIEW_DEPENDENCY`

A Profile may declare a dependency on a **concrete prerequisite `review.<id>`**, with a required status (normally `SATISFIED`), an objective activation condition where conditional, and a bounded purpose.

An unsatisfied, `STALE` or missing prerequisite makes the dependent review **`REVIEW_BLOCKED`**, not failed. **Satisfaction is not transitive**, and a dependency transfers no scope, eligibility, authority, findings, conclusion or satisfaction. Direct self-dependency and transitive cycles are prohibited as architecture validation rules. A dependency executes nothing and adds no runtime semantics, and the dependent Profile still evaluates its own evidence and criteria independently.

`None` with a reason is valid; dependencies are not manufactured for symmetry.

## 8. Review scope must be bounded

Every Profile states what it checks and what it explicitly does not. Universal mega-reviews are prohibited: no Profile may absorb technical, financial, legal, ESG, security and evidence-integrity review. The out-of-scope statement must name the neighbouring review that covers what this one does not.

## 9. Review performed is not review satisfied

A complete, competent review that leaves open findings is `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`, not `SATISFIED`. The distinction may not be elided in card prose.

## 10. Review satisfied is not human approval

`SATISFIED` is a requirement status. It may permit a Workflow Stage or Handoff requirement to be treated as met. It does not approve the artifact and does not touch any human Decision Right.

## 11. Finding severity is not workflow open-item materiality

Severity is a review assessment of how bad a defect is. Materiality (Phase 5 `standard.workflow.common_constraints` §14A) is whether progression may continue. A Profile states how its findings map to materiality; it does not assume the two are the same scale.

## 12. Critical and major unresolved findings block satisfaction

An unresolved `CRITICAL_FINDING` **cannot be review-satisfied under any Profile**. An unresolved `MAJOR_FINDING` normally blocks satisfaction; a Profile may permit a bounded conditional disposition, and any exceptional progression then requires a **named external human Decision Right**, which the Profile references and does not grant.

## 13. A review cannot waive its own findings

Downgrading, closing without remediation, or declaring a finding acceptable are not review acts. A review assesses and records; disposition of an unremediated finding is a human decision outside this registry.

## 14. Material change can invalidate a prior review

Where the subject changes materially after review, the prior satisfaction becomes `STALE` and no longer supports progression. Each Profile states its own material-change triggers.

## 15. Rework preserves the original finding and its provenance

Remediation does not overwrite history. The original finding, its severity as assessed, the response, the evidence, the closure rationale, the prior and new artifact versions, and any re-review outcome are all preserved.

## 16. Review-triggered rework does not silently close findings

A Workflow returning to a Stage does not close anything. Closure is an explicit act with evidence, and it is recorded against the finding it closes.

## 17. Version change cannot silently alter independence, severity or satisfaction semantics

A new Profile version may refine wording, method and evidence expectations. Where it changes the independence class, the finding taxonomy application, or the satisfaction criteria, that is a governance change stated explicitly in the card's change record — never an editorial one.

## 18. Runtime validates against the registry, it does not mutate it

A later runtime may record who reviewed what and when. It may not redefine what independence means, what satisfies a review, or how severity maps to progression. Where a runtime cannot express a rule here, that is a runtime limitation to report, not a licence to weaken the rule.

---

## 19. Status discipline

All Phase 6 artifacts are `PROPOSED`. No Review Profile Card may set its own status to `APPROVED` or `CANONICAL`.
