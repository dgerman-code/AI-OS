# Criticality, Review and Authority Binding

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

## 1. Criticality

**Rule CR-1 — the approved policy is the policy.** Bands come from the approved project
criticality policy. This phase re-thresholds nothing and invents no trigger.

**Rule CR-2 — criticality raises and never lowers.** No wording, no silence, no absence of a
stated value and no planner uncertainty lowers a band. Where value is unknown **and** an approved
trigger fires, the floor is at least `ENHANCED_DECISION_GRADE`.

**Rule CR-3 — an unresolved band blocks.** `criticality = None` is a determinate finding. The
preflight blocks with `CRITICALITY_UNRESOLVED`; it never reads the absence as `ROUTINE`.

## 2. Review

**Rule CR-4 — at `ENHANCED_DECISION_GRADE` and above, an independent review requirement is not
waivable by planning.** A plan at those bands that declares no mandatory review blocks. The
planner may add a requirement; it may never remove one.

**Rule CR-5 — a Review Profile must be approved to be required.** An unapproved profile is not a
review requirement, and naming one blocks rather than creating it.

**Rule CR-6 — planning never satisfies a review.** A planning result arriving with
`satisfied=True` is refused by exception. A review is satisfied by a reviewer, through
`SubmitReviewInstance`, under its Profile's own eligibility and independence rules.

## 3. Authority

**Rule CR-7 — resolve first, then fail closed.** For every act the plan contemplates, the
applicable approved Right is searched for and resolved **before** any absence is recorded.
Reporting a missing authority without having looked trains users to ignore the finding.

**Rule CR-8 — a missing Right blocks, with no alternative branch.** Not a warning, not a
downgrade, not an escalation that proceeds in parallel. `NO_APPLICABLE_DECISION_RIGHT` stops it.

**Rule CR-9 — planning never exercises a Right, and neither does the Execution Basis.**
`ExecutionBasis.exercise()` raises. Exercise happens during the run, by a human, through
`ExerciseDecisionRight`.

**Rule CR-10 — business necessity is not an authority.** Not urgency, not seniority, not a
deadline, not the user's insistence, not the observation that a similar act was authorised before.

## 4. What a Decision Right does not cure

**Rule CR-11 — authority and review satisfaction are separate governance objects.** An exercised
Right does not satisfy an unsatisfied review, does not close an unresolved critical finding, and
does not supply a missing substantive conclusion. Terminal progression requires **both**,
separately — the same rule the approved Phase 14 and Communication Specialist contracts state.

## 5. Non-Runtime Statement

This document is declarative architecture. It specifies no implementation, schema or storage
mechanism, and binds no provider or runtime technology.
