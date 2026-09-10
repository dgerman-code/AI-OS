# Phase 7 — Decision Rights Foundation Self-Check

Status: PROPOSED — READY FOR FINAL INDEPENDENT PHASE 7 FOUNDATION RE-AUDIT

**Updated after the independent Phase 7 audit returned FAIL (1 HIGH, 5 MEDIUM).** The remediation and its 60-check suite are recorded in `reviews/phase-7-foundation-audit-remediation.md`; this document is updated where the audit changed what it says, and the original 50-check results below stand as they were run.

Branch: `architecture/phase-7-decision-rights`
Baseline: Phase 6 human-approval commit `332750bf19e167d1ae0dd2f6350e9bf84731ddd4`

This is a **self**-check by the producing pass. Under Phase 6's own vocabulary it is `PRODUCER_REVIEW` — internal quality control, which cannot satisfy an independent review requirement.

## Artifacts covered

| File | Purpose |
|---|---|
| `architecture/decision-rights-registry-design.md` | Identity, 8 decision classes, effect model, holder eligibility, cardinality, delegation, revocation, evidence model, gate satisfaction, exceptional progression, risk/waiver, emergency, cancellation boundary, knowledge-state boundary, dependencies, **`DECISION_RIGHT_SEPARATION` (§15A)**, Human Approval Matrix |
| `decisions/_standards/common-decision-right-constraints.md` | 26 enforceable rules, including cross-Right separation |
| `decisions/_templates/decision-right-card-template.md` | Mandatory Decision Right Card structure, including the separation relationship table |
| `decisions/_templates/decision-record-template.md` | Semantic Decision Record model, 19 provable elements |
| `decisions/master-decision-right-universe.md` | 9 families, 35 candidates, all 95 upstream references classified into seven categories |
| `decisions/exemplars/` × 8 | Decision Right exemplars, each declaring its `DECISION_RIGHT_SEPARATION` relationships; every carded-to-carded relationship is declared from both ends |

---

## 1. Check results — 50 checks

**50/50 PASS.** Full results are reproduced by the validator; the summary below groups them.

| Group | Checks | Result |
|---|---|---|
| Upstream immutability (Phases 3, 4, 5, 6) | 1–4 | **PASS** — `git diff` empty over `roles/`, `skills/` + Phase 4 architecture, `workflows/` + Phase 5 design, `handoffs/` + `reviews/` + Phase 6 design |
| Status and identity separation | 5–7 | **PASS** — 14 artifacts `PROPOSED`; 9-way separation; Right ≠ Record stated in design, constraints §7 and the record template |
| No bound holders | 8–9 | **PASS** — 0 personal names; no model or agent may hold a Right by model identity alone |
| Authority does not come from competence | 10–13 | **PASS** — constraints §1–5, each with a named counter-example in a card |
| Card completeness | 14–17 | **PASS** — eligibility class, cardinality, delegation policy and revocation semantics on 8/8 |
| Record and gate semantics | 18–20 | **PASS** — 18/18 evidence elements; five gate conditions; requested ≠ satisfied |
| The five mandatory boundaries | 21–26 | **PASS** — review status untouched; items stay open; nothing erased; risk retained; law unwaivable; approval ≠ canonical |
| Canonical and emergency | 27–29 | **PASS** — distinct authority required and no carded Right claims it; four objective emergency triggers, short expiry, retrospective duty |
| Delegation and history | 30–36 | **PASS** — no widening, no cardinality bypass, re-delegation prohibited by default, history preserved, corrections supersede, cycles prohibited |
| Universe accounting | 37–39 | **PASS as run** — 35 candidates, **95/95 upstream references classified**. The duplicate count this group recorded as 0 was **wrong**: the audit found `decision.canonical_knowledge_status_change` duplicating `decision.canonical_knowledge_promotion`, and it is now classified `DUPLICATE / OVERLAP` (1), leaving 34 boundary-refinement entries. Re-tested in the remediation suite. |
| Exemplars and matrix | 40–41 | **PASS** — 8 cards; all 8 in the Human Approval Matrix |
| Scope hygiene | 42–44 | **PASS** — no DB/API/UI/runtime/orchestrator/model/agent; no PR; 0 APPROVED/CANONICAL |
| Boundary separations | 45–50 | **PASS** — conditional approvals carry conditions and expiry; email/meeting insufficient; release ≠ emergency; risk acceptance ≠ exception; publication ≠ canonical; submission ≠ compliance review |

### Additional check not in the required list

**Referential integrity across all 8 exemplars** — 0 invalid `role.<id>`, 0 invalid `artifact.<id>`, 0 invalid `review.<id>`. Every identifier resolves to an approved Phase 3 entry or a Phase 6 candidate Profile.

### Honesty note on the checks

The suite first reported 46/50, then 49/50. **All five failures were defects in the checks, not the content** — and each was replaced with a **stricter** test rather than a looser one, as the prompt requires:

- **Check 22** tested one card for one literal phrase. Replaced with a test requiring the rule in the design, the constraints, **and all eight cards** — each must either state that items remain open or explicitly disclaim the power.
- **Check 27** was case-sensitive against a table row. Replaced with a test that additionally requires **no carded Right to claim the canonical-promotion effect**.
- **Check 34** matched prose that was never written. Replaced with a test requiring the immutability rule **and** the linked-superseding-record mechanism in all three of design, constraints and record template.
- **Check 45** counted any *mention* of `APPROVE_WITH_CONDITIONS`, including `decision.granting_authority_submission` stating the outcome is **not permitted**. Replaced with a test that parses the outcome **table** and requires, for every card that actually permits the outcome, both an open-condition carry and a mandatory expiry in that row — and that every card mentioning it without permitting it says so.
- **Check 48** broke when a card's wording was normalised. Replaced with a test requiring **both directions in both cards**: risk acceptance denies progression and waiver; exceptional progression denies risk acceptance and waiver.

One content change was made during this: `decision.risk_acceptance`'s exceptional-progression disclaimer was normalised to the same form the other seven use, so the property is testable by one rule. The card's substance is unchanged and slightly strengthened.

No check was weakened.

---

## 2. Open architecture questions

| # | Question | Disposition | Reasoning |
|---:|---|---|---|
| 1 | Can organisational authority eligibility be fully registry-defined, or is it partly organisation-specific? | **RUNTIME / ORGANISATION-PHASE CONCERN** | The registry defines eligibility **classes** and the authority basis each requires. Which real body or office holds a class is the organisation's governing arrangement, and inventing it here would bind organisations this registry does not know. The explicit rule: a class without a mapped holder in a given organisation means the Right is unexercisable there, not that a lesser class may act. |
| 2 | May one human exercise multiple Decision Rights in the same chain? | **RESOLVED IN FOUNDATION** | Resolved by `DECISION_RIGHT_SEPARATION` (design §15A, constraints §25, card template, and declared relationships in all eight exemplars). One human may exercise multiple Rights in a chain **except** where a `SEPARATION_REQUIRED` relationship is active for the same governed subject — and then may not, regardless of holding both eligibility classes, delegating, or the second Right being multi-holder. The earlier disposition deferred this; the audit was right that the deferral left the hazard open. |
| 3 | Do some Decision Rights require mandatory separation of duties? | **RESOLVED IN FOUNDATION** | Yes, and they now declare it. Relationship-level separation declarations exist in the design, the constraints, the card template and every exemplar, with `SEPARATION_REQUIRED` as the criticality default across risk acceptance, exceptional progression, emergency authority and the final commitment, release, submission and publication Rights. The specific hazard this self-check flagged — one holder accepting a residual risk and then releasing the change carrying it — is closed from both ends and is stated verbatim in design §15A. |
| 4 | Do collective decisions need abstention and dissent semantics in the foundation? | **SAFE TO DEFER WITH EXPLICIT RULE** | Element 17 of the record model carries them where a body's constituting rules make them material. Whether the registry should *require* them is a governance-design question that belongs to the body's own constitution. |
| 5 | Should approval expiry be globally standardised or right-specific? | **SAFE TO DEFER WITH EXPLICIT RULE** | Right-specific, and the eight exemplars show genuinely different clocks — a contract commitment is version-bound, an emergency change is hours. The rule: **every Right states its own expiry or re-decision trigger, and a missing one is a defect.** |
| 6 | Should risk-acceptance authority use a shared risk-class ceiling model? | **RUNTIME / ORGANISATION-PHASE CONCERN** | The ceiling comes from the organisation's risk-appetite policy, which this universe classifies as executive policy **out of Phase 7 scope**. The registry consumes a ceiling; it does not set one. |
| 7 | Does canonical promotion belong here or in Phase 8? | **PHASE 8 CONCERN** | `decision.canonical_knowledge_promotion` is retained as a candidate because Phase 6 references it and the boundary rule needs it to exist. It is **deliberately uncarded**, and `decision.canonical_knowledge_status_change` is held for the same reason: carding either would presuppose the answer to a question Phase 8 owns. |
| 8 | Does Decision Right dependency need first-class composition or only prerequisites? | **SAFE TO DEFER WITH EXPLICIT RULE** | Prerequisites only, with the rule that **dual control uses cardinality inside one Right rather than chaining pseudo-decisions** — which removes the main pressure toward composition. |
| 9 | Is emergency retrospective ratification a new Decision Right or a dependency? | **SAFE TO DEFER WITH EXPLICIT RULE** | Currently an obligation carried as a condition of the emergency decision, with an expiry that escalates rather than lapsing. Whether the retrospective step is itself a Right needs the ratification's own effect to be settled first — it may be a review, not a decision. |
| 10 | Is reversal always a new Right, or an allowed outcome of the original? | **SAFE TO DEFER WITH EXPLICIT RULE** | The rule in force: **reversal requires a Right whose scope permits it** and is not an implied power of the Right that made the original decision. `decision.decision_reversal` was **deliberately not created** as a candidate, because creating it would presuppose the first half of the answer. |

## 3. Additional findings surfaced during construction

1. **Four of the eight requested exemplar IDs do not exist upstream.** Upstream IDs are preserved — `decision.stage_gate_progression`, `decision.granting_authority_submission`, `decision.contract_commitment` — and only `decision.exceptional_progression` is genuinely new. Renaming three approved artifacts to match a prompt would have been the silent normalization the universe section exists to prevent.
2. **95 upstream references reduce to 33 candidate Rights.** The other 62 are classified: 34 need boundary refinement, 10 are review gates in disguise, 8 are Role responsibilities, 4 are Workflow logic, 2 are IAM, 3 are executive policy, 1 duplicates another candidate. **The registry as inherited was roughly three times larger than the authority model needs**, which is the single most useful finding of this pass.
3. **Every commitment Right requires an authority class no Role holds.** Signatory and executive authority appear nowhere in the Role Registry — correctly, and it means there is a hard edge between doing the work and binding the entity that no amount of Role competence crosses.

## 4. Standing statement

Every Phase 7 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. This record does not claim human approval and is not an independent audit. Eight of 35 candidate Decision Rights are carded; 27 remain unvalidated one-line candidates — one of them, `decision.cancellation_or_termination`, **not cardable at all until bounded** — and the 62 classified references must not be carded until their classification is acted on by a governed pass.
