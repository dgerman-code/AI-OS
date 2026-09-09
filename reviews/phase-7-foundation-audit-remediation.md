# Phase 7 — Decision Rights Foundation Audit Remediation

Status: PROPOSED — READY FOR FINAL INDEPENDENT PHASE 7 FOUNDATION RE-AUDIT

Branch: `architecture/phase-7-decision-rights`
Foundation baseline: `1db348c90fb7f6ba9d78b4c346ae1e4a9a05c0e4`
Phase 6 human-approval baseline: `332750bf19e167d1ae0dd2f6350e9bf84731ddd4`
Independent audit prompt commit: `5c0517fda7edf123ef3781d8031ab85073308a72`

The independent Phase 7 foundation audit returned **FAIL** with one HIGH and five MEDIUM findings. This remediation is **strictly bounded to those six blockers**. Phase 7 was not redesigned, no Decision Rights were mass-carded, and every artifact remains `PROPOSED`.

---

## 1. Finding H1 — Cross-Right separation of duties was undefined

**Audit disposition:** MUST RESOLVE BEFORE HUMAN APPROVAL.
**Status: RESOLVED.**

The gap was real and the foundation self-check had already flagged it as its own primary open question: cardinality governed separation *within* one decision and nothing governed it *across* related decisions. One human could accept a residual risk and then authorise the release carrying it while satisfying every rule in the document.

### What was added

A relationship-level declarative model, `DECISION_RIGHT_SEPARATION`, now exists in all four required places:

| File | What it carries |
|---|---|
| `architecture/decision-rights-registry-design.md` | New **§15A** — declaration shape, ten normative rules, criticality defaults, and the hazard stated verbatim |
| `decisions/_standards/common-decision-right-constraints.md` | New **§25**, inherited by every card (status discipline renumbered to §26) |
| `decisions/_templates/decision-right-card-template.md` | Mandatory **Decision Right Separation** section with the five-column relationship table |
| `reviews/phase-7-foundation-self-check.md` | Artifact coverage and open questions 2 and 3 updated to `RESOLVED IN FOUNDATION` |

Each relationship row declares five things: a **concrete `decision.<id>`**; an **objective, testable activation condition**; the mode `SEPARATION_REQUIRED` or `SAME_HOLDER_PERMITTED`; the **bounded subject/context**; and the **reason**.

### Normative rules now in force

1. Where `SEPARATION_REQUIRED` is active, the same human instance must not exercise both Rights for the same governed subject or context in the same decision chain.
2. Eligibility is evaluated independently per Right; being eligible for both is not permission to exercise both.
3. Holding two eligibility classes does not bypass separation.
4. Delegation does not bypass separation — a delegate is the delegator's side of the pair.
5. Within-Right cardinality does not satisfy cross-Right separation.
6. Separation is relationship-level governance, never inferred from job title, Role identity, reporting line or seniority.
7. `SAME_HOLDER_PERMITTED` only where a card declares it with a defensible reason that preserves the control purpose. **Silence is neither permission nor prohibition**, and an undeclared relationship is not evidence that separation was considered.
8. No staffing algorithm, assignment engine, rota or runtime scheduling is created.
9. **Scarcity does not relax authority** — no separately eligible holder means the second Right is not validly exercisable and the gate is unsatisfied.
10. A Decision Record must be able to evidence compliance; **element 19** of the record model now carries it.

### Criticality defaults applied

`SEPARATION_REQUIRED` is the default for decision-grade and high-criticality external-commitment chains between risk acceptance and a final release/submission/publication/commitment Right on the same subject; between exceptional progression and the downstream final act over a material item; and between emergency authority and the ordinary authority that ratifies or normalises it. No card overrides a default to `SAME_HOLDER_PERMITTED`.

### Exemplar relationships declared

| Card | `SEPARATION_REQUIRED` against | `SAME_HOLDER_PERMITTED` against |
|---|---|---|
| `decision.risk_acceptance` | `production_release`, `contract_commitment`, `granting_authority_submission`, `external_publication` | `security_risk_acceptance`, `exceptional_progression` |
| `decision.production_release` | `risk_acceptance`, `security_risk_acceptance`, `exceptional_progression`, `emergency_production_change`, `defect_deferral` | — |
| `decision.exceptional_progression` | `production_release`, `granting_authority_submission`, `external_publication`, `contract_commitment`, `stage_gate_progression` | `risk_acceptance` |
| `decision.granting_authority_submission` | `risk_acceptance`, `exceptional_progression` | — |
| `decision.external_publication` | `risk_acceptance`, `exceptional_progression` | — |
| `decision.contract_commitment` | `risk_acceptance`, `exceptional_progression` | — |
| `decision.emergency_production_change` | `production_release`, `security_risk_acceptance` | — |
| `decision.stage_gate_progression` | `exceptional_progression`, `risk_acceptance` | — |

Every relationship is declared **from both ends** where both Rights are carded, so a reader of either card sees it. Relationships were kept conservative: none was manufactured to fill a matrix cell.

The one `SAME_HOLDER_PERMITTED` pair with a substantive argument is `risk_acceptance` ↔ `exceptional_progression`: these are two aspects of one accountability for proceeding with a known problem rather than an independent control pair, and splitting them would fragment accountability without adding a check. The independent control is preserved downstream, where separation from the final commitment Right **is** required. Stated explicitly, as §15A rule 7 requires, rather than left to silence.

### The hazard, closed exactly

> The same human must not both accept the residual risk under `decision.risk_acceptance` and authorise `decision.production_release` for the same change carrying that risk, where the separation relationship is active.

Present verbatim in design §15A and declared as `SEPARATION_REQUIRED` in both cards.

---

## 2. Finding M1 — Production release `APPROVE_WITH_CONDITIONS` timing contradiction

**Status: RESOLVED.**

The defect was genuine: the outcome table said the change goes live "once conditions met" while the prose permitted post-release monitoring conditions. Those imply different gate timing, and the ambiguity is exactly the one that lets a material blocker travel through a gate under the word "condition".

`decisions/exemplars/production-release.md` now separates the two classes explicitly:

| | Pre-release condition | Post-release obligation |
|---|---|---|
| What it is | Must be true **for the release to be authorised** | Owed about a change **already live** |
| Effect on the gate | **The gate is not satisfied and the change is not live until met** | None — the gate was satisfied without it |
| Where it may be open | Only before deployment | Only after deployment |
| If it fails | The release is not authorised; the decision is re-taken | The declared re-decision, escalation or rollback path triggers |

Five rules the card now holds itself to: both classes may appear only if **named separately**; any material pre-release condition is met before gate satisfaction and before the change is live; a post-release obligation may remain open only where it does not invalidate release readiness, is explicitly classified, is carried into the Decision Record, and has a named owner and expiry or revisit trigger; failure of a post-release obligation triggers the declared path and **does not retroactively invalidate the release or pretend the decision never existed**; and `APPROVE_WITH_CONDITIONS` cannot move a material pre-release blocker past the gate — that is exceptional progression, requiring `decision.exceptional_progression` held by a separated holder.

The outcome-table row was rewritten to match. The phrase "Live once conditions met" and the free-standing "monitoring conditions may be post-release" wording are gone.

**Human Approval Matrix:** the production-release row's required-review semantics (`review.security`, `review.test_coverage` `SATISFIED`) were already consistent with pre-release gating and needed no change; its cardinality was corrected under M5.

---

## 3. Finding M2 — Universe count/classification mismatch

**Status: RESOLVED.**

The audit was right: the boundary-refinement list contained 35 rows against a declared target of 34, and no duplicate/overlap category existed at all.

`decision.canonical_knowledge_status_change` is now classified **`DUPLICATE / OVERLAP`** with `decision.canonical_knowledge_promotion`. Both are canonical-governance concepts over the same subject — the governed status of a knowledge artifact — differing only in whether the transition is framed as promotion or as status change. Distinguishing them requires the canonical state model itself, which **Phase 8 owns**. Neither identifier is merged, renamed or removed; both remain accounted for; **consolidation and normalization are deferred to Phase 8 canonical governance**, and carding either now would presuppose the answer to open question 7.

Resulting accounting, all verified by parsing the document rather than by reading its prose:

| | Count |
|---|---:|
| Families | 9 |
| Candidate Rights | 35 |
| — upstream-ID candidates | 33 |
| — architecture-gap candidates | 2 |
| LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT | 34 |
| REVIEW / QUALITY GATE IN DISGUISE | 10 |
| ROLE RESPONSIBILITY IN DISGUISE | 8 |
| WORKFLOW PROGRESSION LOGIC IN DISGUISE | 4 |
| RUNTIME PERMISSION / IAM IN DISGUISE | 2 |
| EXECUTIVE POLICY — OUT OF PHASE 7 SCOPE | 3 |
| DUPLICATE / OVERLAP | 1 |
| Classified subtotal | 62 |
| **Upstream references accounted for** | **95 / 95** |

A per-category count table was added to §11 so the totals are checkable at a glance instead of by counting rows. No cards were generated.

---

## 4. Finding M3 — `decision.cancellation_or_termination` too broad

**Status: RESOLVED — and the concept is now explicitly not cardable.**

The audit's characterisation was accurate: as written the entry spanned pre-commitment cancellation and post-commitment termination across any governed path, which makes it a universal kill-switch.

It is **not carded**, and it is now marked **`NOT CARDABLE UNTIL BOUNDED`** in `decisions/master-decision-right-universe.md` §9, with the explicit statement that it **confers no authority, is not an exercisable Right, and must not be referenced as one**. `architecture/decision-rights-registry-design.md` §13 carries the same boundary under the heading *"There is no universal cancellation authority in this registry"*.

Both documents state why these are likely two bounded authority patterns rather than one: pre-commitment cancellation stops an internal governed path with sunk effort as its consequence class and sponsor or executive authority as its likely basis; post-commitment termination affects legal, contractual, regulatory and financial obligations owed to third parties, with signatory or governance-body authority and materially heavier evidence. A single Right spanning both would be eligible to whoever holds the weaker basis and able to end an external obligation on an internal evidence standard.

The upstream architectural need is preserved by recording the placeholder rather than by inventing authority. A future governed pass may split it — plausibly into a governed-path cancellation Right and an external-commitment termination Right — and **no final ID is created here for either**, because inventing one now would be exactly the silent normalization the universe's §12 exists to prevent.

**One downstream consequence, fixed:** `decisions/exemplars/project-readiness-progression.md` had cited `decision.cancellation_or_termination` as the route for withdrawing a project past a gate. That reference would have resolved to something not exercisable. The card now states that no such Right is bounded in the registry yet, that the placeholder confers nothing, and that the withdrawal therefore has no valid authority today — the gap recorded rather than papered over.

Counts are unaffected: the entry remains a candidate, so families stay 9 and candidates stay 35. §11 now distinguishes **candidacy from carding readiness** — 34 of the 35 are bounded enough for a governed pass to card; this one is not.

---

## 5. Finding M4 — Three undefined code-form alias IDs

**Status: RESOLVED.**

The audit's reasoning is accepted without reservation: a code-form `decision.*` string is a concrete registry reference, and calling it a "prompt alias" does not make it resolve. Three such strings appeared in exemplar prose and three more in the universe's §12 table.

All are replaced with plain-language labels carrying no backticks and no `decision.` prefix:

| Removed code-form string | Replaced by | Actual registry ID (unchanged) |
|---|---|---|
| `decision.project_readiness_progression` | "a project-readiness progression exemplar" | `decision.stage_gate_progression` |
| `decision.grant_submission` | "a grant-submission exemplar" | `decision.granting_authority_submission` |
| `decision.contractual_commitment` | "a contractual-commitment exemplar" | `decision.contract_commitment` |

Each of the three cards now states explicitly that **no second identifier exists for that Right** and that the requested wording is a description, not an alias. The universe §12 table was retitled from "Prompt name" to "Requested in plain words" for the same reason.

**No stable ID was renamed to match prompt wording**, in either direction — that was the original reason for preserving them and it has not changed.

**Invalid or undefined concrete Decision references across the eight exemplar cards: 0**, verified by extracting every `decision.<id>` token from every card and resolving it against the universe.

---

## 6. Finding M5 — Human Approval Matrix cardinality mismatch

**Status: RESOLVED, and the audit's specific finding generalised.**

The audit found the `decision.exceptional_progression` row describing all-required only across domains while the card also requires `MULTI_HOLDER_ALL_REQUIRED` at a terminal gate. The default correction applies: **matrix → card**, and the card was not weakened.

Auditing all eight rows against their cards for the same defect found the matrix's compressed shorthand ("Single → all-required on exposure") losing content in **four** rows, not one:

| Row | Matrix said | Card says | Fix |
|---|---|---|---|
| `exceptional_progression` | "Single, or all-required across domains" | also `MULTI_HOLDER_ALL_REQUIRED` **at a terminal gate** | terminal-gate condition added |
| `granting_authority_submission` | "all-required on exposure" | co-financing exposure, **consortium coordination or a value threshold** | all three named |
| `external_publication` | "for new positions or claims" | also **third-party disclosure** | third-party disclosure added |
| `production_release` | "Single → all-required at Enhanced Decision-Grade" | also **`GOVERNANCE_BODY_DECISION` where accreditation applies** | body case added |

The remaining four rows were correct in substance but written in prose shorthand rather than the vocabulary the cards use. All eight now state the actual cardinality tokens, so the alignment is machine-checkable instead of a matter of reading. A line was added stating that **where matrix and card diverge, the card governs and the matrix is defective.**

Delegation policy, external-commitment flag, exceptional-progression flag, risk-acceptance flag and knowledge-state effect were audited across all eight rows on the same basis. No discrepancies were found in those five dimensions.

**Discrepancy count after remediation across all eight rows and all six dimensions: 0.**

A fifth authority-gap note was added below the matrix recording that every commitment and release Right now carries at least one `SEPARATION_REQUIRED` relationship.

---

## 7. Open architecture question dispositions

| # | Question | Disposition |
|---:|---|---|
| 1 | Organisational authority eligibility | `RUNTIME / ORGANISATION-PHASE CONCERN` |
| 2 | One human exercising multiple Rights in one chain | **`RESOLVED IN FOUNDATION`** via `DECISION_RIGHT_SEPARATION` |
| 3 | Mandatory separation between some Rights | **`RESOLVED IN FOUNDATION`** via relationship-level separation declarations |
| 4 | Abstention / dissent | `SAFE TO DEFER WITH EXPLICIT RULE` |
| 5 | Global vs Right-specific expiry | `SAFE TO DEFER WITH EXPLICIT RULE` |
| 6 | Shared risk-class ceiling | `RUNTIME / ORGANISATION-PHASE CONCERN` |
| 7 | Canonical promotion | `PHASE 8 CONCERN` |
| 8 | First-class composition vs bounded prerequisites | `SAFE TO DEFER WITH EXPLICIT RULE` |
| 9 | Emergency retrospective ratification model | `SAFE TO DEFER WITH EXPLICIT RULE` |
| 10 | Reversal model | `SAFE TO DEFER WITH EXPLICIT RULE` |

Questions 2 and 3 are claimed resolved **because the rules are implemented**, not because the disposition was updated: separation exists in the design, the constraints, the card template and all eight exemplars, and checks 1–16 test each of those locations independently.

---

## 8. Upstream regression checks

| Scope | Result |
|---|---:|
| Phase 3 Role Cards (`roles/`) | **0 changes** |
| Phase 4 architecture and mappings | **0 changes** |
| Phase 5 Workflow semantics | **0 changes** |
| Phase 6 Handoff / Review semantics | **0 changes** |

Verified by `git diff` against the Phase 6 human-approval baseline `332750b` plus a clean-tree check, not by inspection.

Boundaries re-tested and unchanged: a Decision Right still cannot make a Review `SATISFIED`; risk acceptance still permits no progression; emergency authority still satisfies nothing retroactively; generic approval still does not imply `CANONICAL`; a requested decision, a meeting and an email still do not satisfy a gate; a correction is still a new linked Decision Record rather than a mutation. Every artifact remains `PROPOSED`; no runtime, database, API, UI, orchestrator, model, agent or IAM logic was introduced; no real person or organisation is bound; no PR was created.

---

## 9. Validation

**60 checks run. 60 / 60 PASS.**

| Group | Checks | Result |
|---|---|---|
| H1 — separation model exists, is declarative and cannot be bypassed | 1–13 | **PASS** |
| H1 — the three named hazard pairs are closed | 14–16 | **PASS** |
| M1 — pre-release vs post-release semantics | 17–21 | **PASS** |
| M2 — universe counts and canonical duplicate disposition | 22–30 | **PASS** |
| M3 — cancellation/termination bounded and not carded | 31–34 | **PASS** |
| M4 — alias cleanup, stable IDs, reference integrity | 35–39 | **PASS** |
| M5 — matrix/card alignment across all eight rows and six dimensions | 40–46 | **PASS** |
| Upstream immutability and scope hygiene | 47–54 | **PASS** |
| Standing boundary regressions | 55–60 | **PASS** |

### Honesty notes

- **No check was weakened.** Where the prompt's wording allowed a shallow test, the implemented test is stricter than the wording requires. Checks 23, 26, 27 and 30 **parse the universe document and count rows** rather than matching a declared number, so a heading that disagrees with its own table fails. Check 39 extracts every `decision.<id>` token from every card and resolves it. Checks 41–46 compare each matrix cell against the corresponding section of the corresponding card, so the matrix cannot pass by restating itself.
- **Check 51 failed on its first run** and the failure was correct: it requires every Phase 7 artifact including this remediation record to carry `Status: PROPOSED`, and this file did not yet exist. It passes now that it does. No other check failed at any point in this remediation.
- **The self-check's earlier universe result is now marked wrong in place.** Its group 37–39 recorded "0 duplicates", which the audit disproved. Rather than quietly restating the number, `reviews/phase-7-foundation-self-check.md` records what that group asserted, that it was wrong, and where it is re-tested. A self-check that silently absorbs an audit finding is worth less than one that shows where it was wrong.
- **The self-check flagged H1 itself, as open question 3, and still shipped 50/50.** That is the honest reading of what happened: the check suite tested what the documents said, and the documents did not claim to have solved separation. The audit was right that a foundation cannot ship a known unclosed concentration hazard as an open question. This remediation closes it rather than re-flagging it.

---

## 10. Files changed

| File | Purpose of the change |
|---|---|
| `architecture/decision-rights-registry-design.md` | **§15A** `DECISION_RIGHT_SEPARATION` (H1); §8 evidence element **19** (H1 rule 10); §13 cancellation/termination bounding (M3); §17 matrix cardinality alignment across all eight rows and a fifth authority-gap note (M5) |
| `decisions/_standards/common-decision-right-constraints.md` | **§25** cross-Right separation; status discipline renumbered §26 (H1) |
| `decisions/_templates/decision-right-card-template.md` | Mandatory separation relationship table; nineteen generic evidence elements (H1) |
| `decisions/_templates/decision-record-template.md` | **§9** and element 19 — separation compliance provable in the record (H1) |
| `decisions/master-decision-right-universe.md` | `DUPLICATE / OVERLAP` category and canonical duplicate disposition (M2); per-category count table (M2); cancellation placeholder bounded and marked not cardable (M3); §12 alias table de-coded (M4) |
| `decisions/exemplars/risk-acceptance.md` | Separation relationships, five required and one permitted (H1) |
| `decisions/exemplars/production-release.md` | Separation relationships (H1); pre-release vs post-release condition semantics (M1) |
| `decisions/exemplars/exceptional-progression.md` | Separation relationships including the reasoned `SAME_HOLDER_PERMITTED` pair (H1) |
| `decisions/exemplars/grant-submission.md` | Separation relationships (H1); alias removed (M4) |
| `decisions/exemplars/external-publication.md` | Separation relationships (H1) |
| `decisions/exemplars/contractual-commitment.md` | Separation relationships (H1); alias removed (M4) |
| `decisions/exemplars/emergency-production-change.md` | Separation relationships paying for `SINGLE_HOLDER` cardinality (H1) |
| `decisions/exemplars/project-readiness-progression.md` | Separation relationships (H1); alias removed (M4); cancellation reference corrected (M3) |
| `reviews/phase-7-foundation-self-check.md` | Open questions 2 and 3 to `RESOLVED IN FOUNDATION`; artifact coverage; the wrong duplicate count marked wrong in place |
| `reviews/phase-7-foundation-audit-remediation.md` | This record |

---

## 11. Remaining deferred matters

Recorded so the re-audit does not have to rediscover them:

1. **`decision.cancellation_or_termination` remains unbounded.** A governed pass must bound or split it; until then there is no valid authority for withdrawing a project past a gate, and `decision.stage_gate_progression` says so rather than pointing at a placeholder.
2. **Canonical governance is Phase 8's.** `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change` are both retained, both uncarded, and their consolidation deferred.
3. **27 of 35 candidates remain uncarded one-line entries**, one of them not cardable at all. No mass carding is authorised by this remediation.
4. **The 62 classified upstream references stay classified and uncarded** until a governed pass acts on the classification.
5. **Separation relationships exist only between carded Rights.** Where a relationship names an uncarded candidate — `decision.security_risk_acceptance`, `decision.defect_deferral` — it binds the carded end today and will need declaring from the other end when that Right is carded.
6. **Eligibility-class-to-organisation mapping remains out of scope**, as do the risk-appetite ceiling and every runtime concern. Separation says when two decisions may not share a human; it never says who the humans are.

## 12. Status

Every Phase 7 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL, this record does not claim human approval, and under Phase 6's own vocabulary it remains `PRODUCER_REVIEW` — it cannot satisfy an independent review requirement. Inclusion in this registry confers authority on no one.
