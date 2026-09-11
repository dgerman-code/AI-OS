# Common Knowledge Governance Constraints

Status: PROPOSED — Phase 8 standard candidate
Standard ID: `standard.knowledge.common_constraints`
Version: 0.1

Every Phase 8 record, template and model inherits this document by reference and does not repeat it. Where anything in `knowledge/` contradicts this standard, this standard governs and the contradicting item is defective.

## 1. Memory is not truth
Retention asserts nothing. That something is held, remembered, repeated or frequently retrieved says nothing about whether it is so.

## 2. Evidence is not approval
Evidence bears on a claim. It does not adopt it, and a well-evidenced claim nobody adopted carries no reliance.

## 3. `REVIEWED` does not mean true
A review applies a stated methodology and records findings. A reviewed assumption is a well-examined assumption.

## 4. `APPROVED` does not mean `CANONICAL`
Approval authorises reliance for a declared purpose. Canonical promotion adopts a statement as the organisation's position for a scope. Neither implies the other.

## 5. Canonical status is scoped, versioned and time-bound
`CANONICAL` is a property of a (claim version, scope) pair with an effective date. There is no global, permanent or unversioned canonical status.

## 6. Canonical status never arises from confidence, rank, repetition or silence
Not from model confidence, retrieval relevance, similarity, recency, agreement across sources, reuse, or the absence of objection. It arises from a governed promotion and from nothing else.

## 7. An epistemic type is never changed by authority
`ASSUMPTION`, `UNKNOWN`, `INFERENCE`, `CALCULATION`, `AI_SUGGESTION` and `FACT_CLAIM` describe what a piece of knowledge is. No approval, promotion, seniority or override converts one into another; only evidence does, and then as a new linked item.

## 8. `UNKNOWN` cannot be closed by authority
Authority may decide what to do about not knowing. It cannot decide the answer.

## 9. An unresolved material conflict blocks canonical promotion and decision-grade use
A conflict blocks where **the claim or the decision depends on the contested point**; an immaterial conflict stays visible and documented and **blocks nothing, at any criticality band**. Materiality is **stated, attributable to a named eligible Role, and reviewable** — never assumed, and never inferred from retrieval ranking, model confidence or the absence of objection. At Enhanced Decision-Grade every open conflict requires an explicit materiality assessment, and an unassessed open conflict is treated as material until one is made. Promotion is never available as an override of an outstanding material conflict.

## 10. Conflict is preserved and is cleared only by recorded resolution
Never by time, re-assertion, a newer source, model agreement, promotion, or nobody objecting. The losing evidence is retained and remains readable.

## 11. Later is not automatically superior, and authority is not evidence
Recency bears on currency, not correctness. A Decision Right may decide what the organisation does about a conflict; it cannot decide which source is accurate.

## 12. No silent provenance loss
An unrecoverable lineage step is recorded as unknown, never omitted. Provenance survives every transition, version, supersession, retraction and transfer.

## 13. No silent overwrite anywhere
Corrections create new linked versions. Canonical records, resolutions, decisions and audit entries are never edited in place, and rollback restores applicability through a new act without erasing what happened.

## 14. Nothing crosses a scope boundary without a governed act
Reference or governed transfer only. A transfer carries neither canonical status nor review satisfaction, is never transitive, and states what was revalidated and what was not.

## 15. Applicability propagates only by declared mode; authority never flows; nothing goes up or sideways
**Canonical status never inherits.** Applicability propagates downward only according to the record's declared mode — `INHERITABLE_TO_DESCENDANTS`, `CONDITIONALLY_APPLICABLE`, `NON_INHERITABLE` or `MANDATORY_WIDER_CONSTRAINT` — and a record with no declared mode governs nothing beyond its own scope. A `MANDATORY_WIDER_CONSTRAINT` **cannot be overridden by a nearer scope**: law, regulation, contract, safety rules and binding governance standards may be narrowed or detailed locally, never contradicted or relaxed, and a local exception requires a **separately valid authority path** — where none exists there is no exception. Any other override must name what it overrides, at which version, and why it is governance-permissible. After a local retraction **no wider statement resumes silently**: a mandatory constraint resumes automatically because it never stopped binding; everything else requires explicit revalidation or re-checked conditions. Scope membership confers no authority.

## 16. Personal scope never becomes organisational knowledge by absorption
Preference memory is never canonical. Personal-scope content reaches an organisational scope only by governed transfer producing a new organisationally-owned record.

## 17. Same name is not same entity
Cross-scope entity resolution is an identity conflict to be governed, never an inference the system makes for itself.

## 18. Withdrawal is terminal and never rewinds a state
A withdrawn approval or a retracted canonical statement becomes **`RETRACTED`, with the withdrawn level — `APPROVED` or `CANONICAL` — recorded as metadata**. There is no `APPROVED` → `REVIEWED`, no `CANONICAL` → `APPROVED`, and no other reverse transition on the governance axis: the approval or promotion **happened**, work relied on it while it stood, and relabelling the item to an earlier state would assert otherwise. A revised claim is a **new linked item starting at `DRAFT`**.

## 19. An artifact is not a knowledge object
A document contains claims in several states. Approving a document promotes nothing, replacing a document rewrites no canonical history, and deleting one deletes no canonical or audit record.

## 20. `AI_SUGGESTION` converts to no other epistemic type, and origin is permanent
No model, agent or automated process moves its own output along the governance axis. **And no actor of any kind — human, reviewer, approver or authority — converts `AI_SUGGESTION` into another epistemic type.** Adoption creates a **new linked item** whose type is justified by its own evidence or reasoning: **human acceptance is not an evidential basis**. The proposal remains historically as what it was. **Origin** — `HUMAN_ORIGIN`, `AI_ASSISTED`, `AI_GENERATED`, `EXTERNAL_ORIGIN` — is a permanent provenance fact on a separate axis; nothing changes it, and it survives every version, transfer, promotion and rewrite.

## 21. Retrieval is not authority
Stored, retrievable, selected, authoritative and canonical are five different properties. Selection mechanisms carry no governance meaning, and an item's absence from context is not evidence about the item.

## 22. Canonical status implies no visibility, and sensitivity implies no status
Sensitivity is an orthogonal axis, is carried through the whole lineage, and is not a scope. Declassification is a governed act, never a side effect of quotation, summary or aggregation.

## 23. stale ≠ false; expired ≠ deleted; superseded ≠ erased; retracted ≠ forgotten
Four distinct end conditions, each preserving content, each with a different meaning for reliance.

## 24. A retention hold outranks every other lifecycle control
Deletion eligibility is a conclusion, never a default. Audit memory and the provenance of canonical statements are not ordinary deletion candidates.

## 25. Promotion authority creates no expertise
The professional conclusion behind a canonical statement is Role-owned and review-checked. Adopting a conclusion is not reaching one.

## 26. Phase 8 grants no authority and changes no upstream status
It cards no Decision Right, gives no Role a power, satisfies no review, changes no review status, and leaves approved Phase 3–7 semantics as they are.

## 27. No override path exists
Administrator, owner or user override does not bypass evidence, review or authority requirements. A requirement with a privileged exception is not a requirement.

## 28. Runtime validates against this architecture; it does not mutate it
A later system may store, index, retrieve and enforce. It may not redefine what knowledge is, what makes it canonical, or what a state means.

## 29. Item age is not a use verdict

Item-level temporal facts — as-of date, last verified, refresh interval, review-by, expiry — are properties of the record. **Usability is a property of the use**: the same item may be `CURRENT_FOR_USE` for one task and `STALE_AND_BLOCKING` for another at the same moment. A use verdict is never stored as a permanent label on the record.

---

## 30. Status discipline
All Phase 8 artifacts are `PROPOSED`. No Phase 8 record may set its own status to `APPROVED` or `CANONICAL`, and no exemplar is a live knowledge record.
