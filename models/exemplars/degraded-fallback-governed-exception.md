# Exemplar 9 — The governed exception that is not available

Status: PROPOSED — Phase 9 exemplar Routing Decision
Inherits: `standard.model.common_constraints@0.1`

**Illustrative and synthetic.** All **model, provider and deployment** identifiers below are architecture placeholders. **No claim is made about any real model or provider.** Every `review.<id>` and `decision.<id>` below is a **real approved registry object**, cited as it actually exists.

**Proves:** that a candidate failing an eligibility constraint is **never called eligible** until a governed act changes the requirement — **and that today no such act is available**, because no approved Phase 7 Decision Right covers a model-capability threshold. The correct outcome is therefore **`BLOCKED_FOR_ROUTING`**.

**Rewritten twice.** Its first version called a `BASELINE` candidate eligible while `STRONG` was required, then reached for a Phase 7 exception — contradictory. Its second version fixed the sequence but **invented** a model-capability-threshold exception Right and a software-security-change Review Profile, neither of which exists in any approved registry. Those invented names are deliberately not reproduced here in code form: a `decision.<id>` or `review.<id>` string is a concrete registry reference, and writing one that resolves to nothing is the defect itself. The re-audit was right on both counts: **a correct sequence over invented registry objects is not a governed path, it is a diagram of one.**

## Task context
Code review of a security-relevant change, feeding a release gate. Criticality **Enhanced Decision-Grade**.

Two **separate** controls apply:

| Control | Source | Value |
|---|---|---|
| Reviewer independence | **Phase 6**, `review.security` (approved) | `INDEPENDENT_ASSURANCE_REVIEW` |
| Model diversity | **Phase 9**, Routing Policy `rp.decision_grade_code_review` v4 | `DIFFERENT_MODEL_FAMILY_REQUIRED` against `rd.2026.change.0918` |

`review.code` and `review.security` both inform the gate; the release gate itself is `decision.production_release` (approved, Phase 7).

## Candidate universe
Registry state `reg.snapshot.2026-09-12T08:00Z#4491`; universe definition `cud.decision_grade_code_review` v2. Enumerated: 4. **`CANDIDATE_UNIVERSE_COMPLETE`.**

## Step 1 — evaluation under the current policy

| Candidate | Eligible? | Excluded by |
|---|---|---|
| `model.reviewer_h` @ `deployment.tenant_internal_h` | **No** | Primary state `SUSPENDED` — `LIFECYCLE_ROUTABLE` fails |
| `model.midsize_analyst_d` @ `deployment.tenant_internal_d` | **No** | **`REQUIRED_CAPABILITY` `capability.code_review` `STRONG` — claim is `BASELINE`** |
| `model.frontier_reasoning_b` @ `deployment.tenant_internal_b` | **No** | Same family as the producer — `MODEL_DIVERSITY_REQUIRED` fails |
| `model.compact_general_a` @ `deployment.tenant_internal_a` | **No** | `capability.code_review` `NOT_CLAIMED` |

**Result: `NO_ELIGIBLE_MODEL`.** Recorded, and **never overwritten** by anything that follows.

## Step 2 — exceptionability, and the search for a Right that covers it

| Failed constraint | Exceptionability class | A named approved Right covering this class? |
|---|---|---|
| `LIFECYCLE_ROUTABLE` (`SUSPENDED`) | `ABSOLUTELY_NON_WAIVABLE` | Not applicable — nothing reaches it |
| `capability.code_review` `STRONG` | `GOVERNED_EXCEPTION_POSSIBLE` **in principle** | **None.** See below |
| `MODEL_DIVERSITY_REQUIRED` | `GOVERNED_EXCEPTION_POSSIBLE` **in principle** | **None** |

The approved Phase 7 registry carries **eight** carded Decision Rights: `decision.stage_gate_progression`, `decision.exceptional_progression`, `decision.granting_authority_submission`, `decision.external_publication`, `decision.contract_commitment`, `decision.risk_acceptance`, `decision.production_release`, `decision.emergency_production_change`.

**None of them covers a model-capability threshold or a model-diversity requirement**, and the nearest candidate is instructive rather than usable:

- **`decision.exceptional_progression`** permits progression past *one named unresolved item* at *one progression point*. Its subject is a **governed work item** — an open finding, an unsatisfied review — not a **routing requirement**. Reading it as authority to lower a capability threshold would widen its declared subject, which its own card forbids: it "does not permit progression past a second item", and it authorises no external act or substitution of any kind.
- **`decision.production_release`** governs the release, not what reviewed it, and explicitly accepts no risk and waives no review.

Under `models/routing-constraint-model.md` §5.3, **"a Decision Right exists" is not a basis**: *this* Right must cover *this* constraint class, and **unknown or unrecognised exceptionability defaults to `ABSOLUTELY_NON_WAIVABLE`.** No such Right exists, so no adjustment is available.

## Step 3 — the governance boundary, reached and recorded

The search of §2 has an outcome, and it is a recorded one rather than an absence:

> **`NO_APPLICABLE_DECISION_RIGHT`** — no approved Phase 7 Right covers either adjustable constraint class.

Routing outcome: **`BLOCKED_FOR_ROUTING`**, with **`ESCALATED_FOR_GOVERNANCE_DESIGN`** attached — the block is not merely a refusal, it is a referral of a specific gap to the phase that owns it. This is **case C** of `models/routing-precedence-and-fallback.md` §5, for all four candidates.

**Both review references resolve.** `review.security` and `review.code` are approved Phase 6 Profiles, checked against the registry rather than assumed; no `REVIEW_PROFILE_NOT_BOUND_IN_PHASE_9` marker is needed here, and none is used. Had no approved Profile matched, that marker — not a plausible-sounding name — is what this exemplar would carry.

The Routing Decision records: the four ineligibility results; each failed constraint's exceptionability class; **`NO_APPLICABLE_DECISION_RIGHT`**; **`BLOCKED_FOR_ROUTING` / `ESCALATED_FOR_GOVERNANCE_DESIGN`**; and the three things that could change the answer — the suspension resolving, a stronger diverse-family profile entering the registry, or **a Phase 7 pass carding a Right for this constraint class**.

The third is explicitly **a Phase 7 governance extension**. Phase 9 identifies the gap and has no power to fill it; a Right comes into existence through Phase 7's own carding governance or not at all.

## What case B would have required, and why it was not reached

Case B is fully defined and entirely unavailable here. It would have required, in order: the ineligibility recorded (done); an exceptionability class of `GOVERNED_EXCEPTION_POSSIBLE` (satisfied in principle for two constraints); **a named, valid, approved Phase 7 Decision Right whose scope covers that class** (absent); its exercise by an eligible human producing a Decision Record with a bounded, expiring effect (unreachable); an adjusted routing context (unreachable); and re-evaluation against it (unreachable).

**The chain stops at the third step, and stopping there is the architecture working.** Inventing a Right to complete the illustration was the defect the re-audit caught — and it is the same defect at a larger scale that the whole exceptionability model exists to prevent: **treating the existence of a governance mechanism as the existence of the authority.**

## What is untouched, whatever happens next

| | Effect |
|---|---|
| **Reviewer independence** | **Untouched, and unreachable.** `review.security` remains `INDEPENDENT_ASSURANCE_REVIEW`. **No routing act, acknowledgement, or Right exercised over a routing constraint waives it** — model diversity and reviewer independence are two controls |
| `model.reviewer_h`'s suspension | Untouched. `ABSOLUTELY_NON_WAIVABLE` |
| Whether the reviews are `SATISFIED` | **Phase 6's question**, decided by findings. Routing does not reach it |
| The release gate | `decision.production_release` is unaffected by any of this, and its own prerequisites are unchanged |

## Three acts, and none of them available here

1. **Operator choice** — selecting among eligible candidates. There were none.
2. **Acknowledgement** — recording that someone knows about a degradation on a **preference**. **Adjusts no requirement**, and the shortfall here was an eligibility constraint.
3. **Governed exception** — a named approved Right adjusting a named adjustable constraint, before re-evaluation. **No such Right exists.**

What remains is what the architecture offers when nothing is eligible: **a block, a named reason, and a decision for humans** — resolve the suspension, admit a stronger diverse-family profile, or card a Right through Phase 7's own governance. Each is deliberate. **The one outcome refused is the work quietly proceeding on an instrument nothing authorised.**
