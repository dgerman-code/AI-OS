# Failure and Escalation Model

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. Fourteen planning failure modes

Every one has exactly one disposition. A failure mode with two possible outcomes is a failure mode
that will be resolved by whoever is in a hurry.

| # | Mode | Disposition | Why |
|---:|---|---|---|
| F-1 | `NO_VALID_SCOPE` | **BLOCK** + escalate | No governed scope resolves; every later step would be ungoverned |
| F-2 | `AMBIGUOUS_SCOPE` | **CLARIFY**, blocking; **BLOCK** if unanswerable | Choosing changes applicable knowledge, authority, residency or sensitivity (CS-7) |
| F-3 | `NO_MATCHING_WORKFLOW` | **COMPOSE** | Not an error. It is the ordinary trigger for the COMPOSE path |
| F-4 | `PLAN_COMPOSITION_REQUIRED` | **COMPOSE** | An admissible candidate exists but does not cover the work |
| F-5 | `REQUIRED_ROLE_UNAVAILABLE` — an **approved** owning Role exists and is unavailable, unmapped or not activatable | **BLOCK** where `load_bearing = LOAD_BEARING`; otherwise **CONSTRAIN** with the gap stated | The predicate is `role-skill-requirement-inference.md` §6a (LB-0…LB-6), evaluated against the **originally requested** deliverable; RS-9, RS-10. Where **no** approved Role owns the conclusion, the mode is F-14, not this one |
| F-6 | `REQUIRED_SKILL_UNAVAILABLE` — an **approved** Skill exists and is not activatable | **BLOCK** where `load_bearing = LOAD_BEARING`; otherwise **CONSTRAIN** with the gap stated | The same predicate, on the same original-deliverable basis, applied to the Skill's Role (RS-8, §6a) |
| F-7 | `REVIEW_PROFILE_UNAVAILABLE` | **BLOCK** + escalate | An unreviewable deliverable at a band that requires review is not shippable |
| F-8 | `NO_APPLICABLE_DECISION_RIGHT` | **BLOCK** + escalate | GP-4. There is no alternative branch |
| F-9 | `EVIDENCE_REQUIREMENT_UNSATISFIED` | **BLOCK the plan**, before handoff | §2a. Phase 15 has no stages to block, and no partial handoff exists (HO-2, G-11) |
| F-10 | `CRITICALITY_UNRESOLVED` | **BLOCK** | Never defaults to Routine (WC-2) |
| F-11 | `CONFLICTING_REQUIREMENTS` | **ESCALATE** | Two governed requirements cannot both be met; a planner may not choose between them |
| F-12 | `UNSAFE_INFERENCE` | **CLARIFY**, blocking; **BLOCK** if unanswerable | The planner would have to guess about scope, authority or an irreversible act |
| F-13 | `PLAN_VALIDATION_FAILED` | **BLOCK** | Preflight failed; §5 of the preflight document names the locus |
| F-14 | `NO_APPROVED_ROLE_OWNS_CONCLUSION` | **BLOCK** + escalate | The originally requested deliverable needs a conclusion the approved universe has **no owner** for. Distinct from F-5: no approved owner exists, so there is no load-bearing determination to make (`role-skill-requirement-inference.md` §6b, RS-12) |

**Rule FE-1 — `RECOMMENDATION_ONLY` is an outcome, not a fallback.** Where the user asked for a
recommendation (`execute_or_prepare = RECOMMEND`), the plan produces one and no act is contemplated.
It is **not** a degraded mode a blocked plan silently drops into: converting "send this" into
"here's what you could send" without saying so is a silent scope change.

## 2. Disposition semantics

| Disposition | Means | Never means |
|---|---|---|
| **CLARIFY** | A `ClarificationRequirement` opens; the plan waits | The planner picks the likely answer if no reply comes |
| **BLOCK** | No handoff. The plan is `BLOCKED` with the mode recorded | A warning attached to a plan that proceeds |
| **ESCALATE** | A governance question is raised to a human, naming what is missing | The plan continues while someone looks at it |
| **COMPOSE** | Take the COMPOSE path | Relax a constraint to make MATCH work |
| **CONSTRAIN** | Proceed with a narrower plan that **states what it does not cover** | Proceed quietly with a gap |

**Rule FE-2 — a blocked plan is a result, delivered.** The user is told what is blocked, why, and
what would unblock it — in their own vocabulary, not as an error code. A block the user cannot act
on is a dead end wearing a status.

**Rule FE-3 — escalation names the gap, not the inconvenience.** "No approved Role owns
communication strategy for contested interactions" is an escalation. "This is taking too long" is
not.

**Rule FE-4 — no disposition is reachable by confidence.** A high-confidence planner does not get a
lighter disposition, and a low-confidence one does not get a heavier one. Dispositions follow the
mode (OM-13).

## 2a. F-9, and why it is plan-level

The first version of this document disposed of F-9 per stage: hold the one that lacks its evidence
and let the rest go on. That was wrong twice over. Phase 15 can never hold a single stage, because
stage activation is Phase 11's (HO-1, PL-1); and it can never let some stages go on, because no
partial handoff exists (HO-2). A rule that has Phase 15 continuing or halting stages describes a
second Orchestrator.

The disposition is therefore plan-level, and it has two branches decided by the approved Phase 11
prerequisite semantics rather than by Phase 15's preference:

| The unsatisfied `EvidenceRequirement` is | Outcome | Basis |
|---|---|---|
| Required before the **first executable dependent act** of the plan | **BLOCK the plan.** No envelope is produced | The plan cannot start; handing it over would hand over a run that must immediately wait or fail |
| Legitimately deferred, and declarable under the approved mechanism as `FUTURE_GOVERNANCE_REFERENCE` | The plan stays valid and the reference is carried in `prerequisite_refs` **as** `FUTURE_GOVERNANCE_REFERENCE`, which the approved intake check 7 already accepts and which marks the dependent act **non-executable** | `architecture/orchestrator-architecture.md` §5 check 7 |

**Rule FE-11 — Phase 15 neither continues nor halts a stage, in any failure mode.** It produces a
whole plan or no plan. Where the approved Phase 11 semantics permit an unresolved prerequisite, the
plan represents it exactly as Phase 11 defines it and lets Phase 11 do the waiting; where they do
not, the plan blocks before the handoff. There is no third behaviour, and no Phase 15 rule may be
written as *"stage X blocks while stage Y proceeds"*.

**Rule FE-13 — a prerequisite reference is `RESOLVED`, `FUTURE_GOVERNANCE_REFERENCE`, or
blocking.** There is no fourth state and no passable `UNKNOWN`: an unresolved, dangling or
unclassified reference blocks, and is never relabelled as a declared future reference to get past
the handoff (`orchestrator-handoff-contract.md` HO-15).

**Rule FE-12 — a `FUTURE_GOVERNANCE_REFERENCE` is not a satisfied requirement.** It is a declared,
non-executable dependency. It does not make the evidence available, does not permit the dependent
act, and is never used to move a blocking requirement out of the way of a handoff.

## 3. Combination

**Rule FE-5 — the strictest disposition wins.** Where several modes hold, the plan takes the
strictest: BLOCK beats CLARIFY beats CONSTRAIN beats COMPOSE. Every mode is recorded, not just the
governing one, because the user needs to know everything that is wrong rather than the first thing.

**Rule FE-6 — F-8 is never softened by another mode.** A missing Decision Right blocks whatever
else is true. In particular it is not converted into a CONSTRAIN by removing the act from the
plan's description while leaving it in the user's expectation — if the act is removed, the plan says
so in terms the user will read (`user-experience-contract.md` UX-5).

## 4. What the planner escalates to

**Rule FE-7 — escalation is to a human, through the product, and it is not an approval request.**
It raises a governance question — a missing Role owner, an unavailable Review Profile, a Decision
Right the register does not carry. Answering it is a governance act elsewhere, not a click in the
plan.

**Rule FE-8 — the planner never escalates to itself.** There is no retry loop that re-plans on the
same inputs hoping for a different reading. A failure mode is resolved by new information — a
clarification answer, a governance change, a resolved reference — and new information means a new
`Request` and a new plan version.

## 5. What is never a failure mode

**Rule FE-9 — `NO_MATCHING_WORKFLOW` is not an error.** It is the normal state for most real
requests, and the COMPOSE path exists for it. A system that treated it as a failure would push its
users back toward naming Workflows.

**Rule FE-10 — a user's request being unusual is not a failure.** The failure modes are about
governance completeness, not about whether the request fits a familiar pattern.

## 6. Non-Runtime Statement

This document is declarative architecture. It specifies no error-handling implementation, retry
mechanism, notification channel, schema or storage, and binds no provider or runtime technology.
