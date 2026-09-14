# Phase 15 Self-Check

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

> **This is a producer self-check.** The party that wrote an architecture is the last party who
> should certify it. What follows records what was checked and what was found; it approves nothing
> and replaces no independent review.

## 1. Non-production status

| Claim | Status |
|---|---|
| Any Phase 15 artifact is `APPROVED` or `CANONICAL` | **No.** All 16 documents are `PROPOSED` |
| Any approved Phase 1–13 artifact is modified | **No.** The branch adds files; it changes none |
| Any Phase 14 file is modified | **No** |
| Any runtime, migration, SDK, queue, worker, scheduler, IaC or secret is created | **No** |
| Any Decision Right, Role, Skill, Review Profile or Workflow is created | **No** |
| Any human approval is claimed | **No** |
| Anything here has been executed | **No.** No planner exists, and no exemplar is a fixture |

## 2. Completeness against the commissioning prompt

| Required | Artifact | Present |
|---|---|:---:|
| Architecture | `planning/intent-work-planning-architecture.md` | ✓ |
| Request / intent model | `planning/request-intent-model.md` | ✓ |
| Context / scope resolution | `planning/context-scope-resolution.md` | ✓ |
| Work classification / criticality | `planning/work-classification-and-criticality.md` | ✓ |
| Role / Skill inference | `planning/role-skill-requirement-inference.md` | ✓ |
| Workflow matching / composition | `planning/workflow-matching-and-composition.md` | ✓ |
| Work Plan object model | `planning/work-plan-object-model.md` | ✓ |
| Clarification policy | `planning/clarification-policy.md` | ✓ |
| Governance preflight | `planning/governance-preflight.md` | ✓ |
| Orchestrator handoff | `planning/orchestrator-handoff-contract.md` | ✓ |
| Failure / escalation | `planning/failure-and-escalation-model.md` | ✓ |
| Learning boundary | `planning/workflow-candidate-learning-boundary.md` | ✓ |
| UX contract | `planning/user-experience-contract.md` | ✓ |
| Exemplars | `planning/exemplars.md` | ✓ — six, fully worked |
| Open items | `planning/open-items.md` | ✓ |
| Self-check | `planning/phase-15-self-check.md` | ✓ |
| Validator | `validation/phase_15_validation.py` | ✓ |
| Mutation probes | `validation/phase_15_mutation_probes.py` | ✓ |

### 2a. One deviation from the recommended filenames, and why

The commissioning prompt recommended `architecture/intent-work-planning-architecture.md`. The
document is at **`planning/intent-work-planning-architecture.md`** instead.

Adding **any** file under `architecture/` changes the result of the **approved Phase 12
validator**, whose containment check treats every path under `architecture/` and `orchestration/`
as inherited material that this branch must leave untouched — tracked or untracked, added or
modified. Placing the document there took Phase 12 from `55/55` to `54/55`, and a proposal branch
that degrades an approved validator's result has modified approved architecture in the only sense
that check cares about.

The prompt permits filename adjustment where coherence requires it. Keeping an approved
validator's result intact is the stronger obligation, and the whole package now sits in one
directory, which is arguably more coherent anyway. Phase 12 is back to `55/55`.

## 3. The prohibitions, and where each is enforced

| # | Never | Enforced by | Checked by |
|---:|---|---|---|
| N-1 | Invent a governed primitive | RS-3, MC-9 | `the planner invents no Role, Skill, Review Profile, Right or Workflow` |
| N-2 | Turn a plan into a Workflow | WL-1, WL-2, WL-4, MC-14 | `a Work Plan never acquires Workflow identity` |
| N-3 | Select or exercise human authority | GP-4, GP-9 | `the planner never grants, exercises or substitutes for authority` |
| N-4 | Treat confidence as authority | OM-13, OM-14 | `confidence never grants authority, waives review or crosses scope` |
| N-5 | Downgrade an inherited requirement | WC-2, WC-10, MC-11 | `no inherited criticality, sensitivity or review floor is lowered` |
| N-6 | Silently cross a scope boundary | CS-4, CS-5, CS-7 | `scope is never crossed by inference, similarity or confidence` |
| N-7 | Infer a missing Decision Right | GP-5 | `a missing applicable Decision Right fails closed` |
| N-8 | Convert AI output into approved knowledge | OM-9, OM-11, RI-11 | `generated planning knowledge stays correctly typed` |
| N-9 | Create a permanent autonomous agent | PL-2, UX-11 | Structural: no persona is specified anywhere |
| N-10 | Choose a Model Profile | HO-4, HO-8, G-14 | `the planner never selects a Model Profile` |

## 4. Identifier integrity — checked, not asserted

Every `role.<id>`, `skill.<id>`, `review.<id>`, `decision.<id>` and `workflow.<id>` cited anywhere
in the package is resolved against the approved registries on this branch. **There are no
unresolved identifiers.** The package cites 20 approved Roles, 5 approved Workflows, and the
Review Profiles and Decision Rights the exemplars name. It creates none.

This is the check that would catch the most plausible failure of a planning layer: describing a
capability instead of naming one, and then having no way to tell that the capability does not exist.

## 5. What this self-check did **not** check

1. **Whether the architecture is correct.** Whether the five functions are the right five, whether
   the sixteen records are the right sixteen, whether the five ambiguity classes carve the space
   correctly, and whether the eighteen preflight checks are the right eighteen are questions for an
   independent review.
2. **Whether the COMPOSE path can execute.** Open item **PO-4** is unresolved and is load-bearing:
   the approved intake check 1 requires a Workflow definition, and a Work Plan is not one. The
   MATCH path is compatible with the approved Orchestrator; **the COMPOSE path is specified and not
   yet executable**, and this phase deliberately does not amend an approved Phase 11 check to make
   it so.
3. **Whether inference is achievable.** The architecture says what an interpreter must produce and
   what it may never do. Whether any system can derive those fields reliably from ordinary language
   is an empirical question no document settles.
4. **Whether the criticality triggers fire correctly.** The sixteen triggers are transcribed from
   the approved policy. Whether a planner would detect them in real requests is untested.
5. **Whether the user experience works.** UX-contract compliance is checkable; whether the result
   is usable is not, and no user has seen it.

## 6. Known limitations

- **Ten open items**, one of which (PO-4) determines whether half this phase is buildable at all.
  It is stated in full rather than resolved, because resolving it would mean amending an approved
  Phase 11 check from a proposal branch.
- **The package names a capability gap it cannot fill.** No approved Role owns communication
  strategy for contested interactions (PO-1), so `exemplars.md` Example 2 produces a *constrained*
  plan. That is the architecture working, and it is also a real functional limit.
- **Confidence has no production method** (PO-8). The model specifies what confidence may never do
  and leaves how it is computed undefined — deliberately, since specifying it would specify an
  inference runtime this phase excludes.
- **Planning records have nowhere approved to live** (PO-2, PO-6). Phase 10's ten data domains do
  not include planning, and adding one is a Phase 10 act.
- **Nothing has been executed.** Every exemplar is worked on paper. No fixture exists.

## 7. Harness credibility

**Not high, and the reasons are specific rather than modest.**

1. **The validator and the architecture were written by the same party in the same pass.** It tests
   the architecture against the constraints its author was already trying to satisfy, which is the
   weakest possible form of assurance.
2. **Text-consistency checks cannot test an architecture.** Every check here reads documents. None
   executes a planner, because there is no planner. A package can be perfectly self-consistent and
   architecturally wrong, and this harness would report `PASS`.
3. **The prior phases of this repository establish a pattern worth stating.** In Phases 12–14 a
   green validator repeatedly coexisted with blockers an independent reader found — including, in
   two rounds, defects the harness's own author had introduced in the previous round. There is no
   reason to expect Phase 15's first harness to be better than Phase 14's fifth.
4. **The probes test the checks, not the architecture.** A high detection rate means the checks are
   load-bearing against the weakenings the same author thought to write. It says nothing about the
   weakenings nobody thought of, and those are the ones independent reviewers keep finding.

**Results are reported in §8 exactly as executed**, including any probe that came back redundant on
its first run.

## 8. Validation results

| Run | Result |
|---|---|
| `validation/phase_15_validation.py` | **32/32 PASS** on default, `--verbose` and `--json` |
| `validation/phase_15_mutation_probes.py` | **28 probes, 28 DETECTED, 0 REDUNDANT, 0 ERROR** |
| Phase 8 validator | `119/119 PASS` |
| Phase 9 validator | `277/277 PASS` |
| Phase 10 validator | `145/147 PASS` — **inherited**, unchanged |
| Phase 11 validator | `159/160 PASS` — **inherited**, unchanged |
| Phase 12 validator | `55/55 PASS` |
| `git diff --check` | clean |
| Containment | only `planning/`, `prompts/` and `validation/phase_15_*` differ from the merge base |

**One probe was `REDUNDANT` on its first run**, and it exposed a weakness in the checks rather
than in the architecture: the clarification check verified the *record table* constraining
`default_if_unanswered`, while the probe rewrote the *rule* that makes a default on a blocking
class a failure and left the table intact. Checking one of a pair is not checking the pair. It is
fixed, and it is recorded here rather than quietly repaired, because a fixture whose first-run
misses are invisible proves whatever its author wanted it to.

**Three validator defects were also found by running it**, before any probe: the identity-chain
check read one line of a blockquote that wraps and reported the tail of the chain as missing; the
object-model check looked for "Yes" in a column whose one affirmative cell reads "**Gates** the
handoff"; and a corrective-frame pattern lacked the word *nothing*, so "high confidence changes
nothing about what is permitted" read as a permission. Each is the same class of error — a check
that tested the shape it expected rather than the shape the document has.

## 9. Readiness

This package is ready for an **independent architecture review**, not for approval. The two
questions a reviewer should press hardest:

1. **PO-4** — is a validated Work Plan an admissible execution basis for the approved Orchestrator,
   and if not, what is the COMPOSE path for?
2. **Whether the planning layer can stay a planning layer.** Every pressure on a system like this
   pushes it toward re-planning mid-run, remembering across requests, and turning repeated patterns
   into registry entries. The boundaries here are structural (HO-11, HO-12, WL-4) precisely because
   policy boundaries erode — and a reviewer should check whether they are structural enough.

## 10. Non-Runtime Statement

This document is declarative architecture. It specifies no implementation and binds no provider or
runtime technology.
