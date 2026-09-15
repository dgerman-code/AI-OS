# Workflow Candidate Learning Boundary

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. The temptation, stated plainly

The planner composes an instance-level Work Plan for a request no Workflow covers. Next month it
composes a near-identical one. Then a third. The obvious move — and the wrong one — is to write the
pattern into the Workflow registry so the fourth request matches.

That move would let a system create its own governed reusable patterns by repetition. It is
prohibited, entirely, by every route.

## 2. The boundary

**Rule WL-1 — a Work Plan never becomes a Workflow.** Not automatically, not on a threshold, not on
a confidence value, not on a human clicking "looks good" in a planning view, and not by any process
this phase specifies. The only thing repetition may produce is a **suggestion**.

**Rule WL-2 — the system never writes to a governed registry.** Phase 15 has no registry-mutation
capability of any kind: it cannot create, amend, version, retire or approve a Workflow, Role, Skill,
Review Profile or Decision Right. Registry change is a governed act performed by people through
Phase 5–7 change control.

**Rule WL-3 — a suggestion is `PROPOSED` and inert.** A `WorkflowCandidateSuggestion` confers
nothing, is matched against by nothing, is not a candidate in `workflow-matching-and-composition.md`
§2, and has no effect on any plan. It is a document a human may read.

**Rule WL-4 — self-approval is impossible by construction, not by policy.** There is no state
transition from `PROPOSED` to anything within Phase 15, and no actor inside the layer has authority
over a registry object. A rule that merely forbade self-approval would be a rule an implementation
could violate; the absence of a mechanism is stronger.

## 3. What a suggestion contains

| Field | Content |
|---|---|
| `suggestion_ref` | `workflow_candidate.<id>` — deliberately **not** `workflow.<id>` |
| `status` | `PROPOSED`. The only permitted value |
| `observed_plans` | The `work_plan.<id>`s that prompted it, each at its version |
| `common_structure` | The stages, Roles, reviews and gates the plans shared |
| `divergences` | Where the plans differed — often the more informative half |
| `scope_span` | Which scopes the plans came from, because a pattern inside one project is not a reusable pattern |
| `granularity_assessment` | Whether it meets the Phase 5 granularity rule, or is a single skill invocation wearing a prefix |
| `governance_questions` | What a human would have to settle: Role ownership, review independence, gate placement |
| `is_approved` | **`false`**, declared rather than omitted |
| `is_matchable` | **`false`**, declared rather than omitted |

**Rule WL-5 — a suggestion carries the divergences, not only the similarities.** Three plans that
agree on six stages and disagree on where the human gate sits are **not** evidence of a reusable
pattern; they are evidence of a question. A suggestion that averaged them away would be proposing a
gate placement nobody chose.

**Rule WL-6 — a suggestion states what it does not know.** The Phase 5 granularity rule exists
because near-identical patterns proliferate and micro-workflows masquerade as coordination. A
suggestion that cannot say which side of that line it falls on says so.

## 4. Why repetition is weak evidence

**Rule WL-7 — three similar plans may mean three similar requests from one person in one month.**
Frequency is not reusability. A pattern that recurs because one user has one recurring task is a
habit; a reusable Workflow serves work the organisation will do repeatedly, across scopes and
people. `scope_span` exists to make that visible.

**Rule WL-8 — the plans that got blocked matter as much as the plans that ran.** A pattern derived
only from plans that validated would encode a survivorship bias: the shape that happened to pass,
rather than the shape the work needs. A suggestion records blocked plans with the same structure.

## 5. What a human does with one

Nothing happens inside Phase 15. A human may take the suggestion into Phase 5 workflow change
control as **input material**, where it goes through candidate assessment, granularity review,
overlap analysis against the existing universe, Role and review design, and approval — exactly as
any other Workflow candidate would.

**Rule WL-9 — the suggestion carries no procedural weight there either.** Having been machine-
generated makes it neither more nor less likely to be right, and it earns no shortcut through the
approval path.

## 6. What this boundary protects

Without it, the system would accumulate governed patterns that no one designed, whose Role
ownership nobody assigned, whose review independence nobody checked, and whose human gates were
placed by whatever the first few instances happened to do. It would do this gradually, plausibly,
and with every individual step looking reasonable — which is precisely why the boundary is
structural rather than procedural.

## 7. Non-Runtime Statement

This document is declarative architecture. It specifies no pattern-detection implementation,
clustering method, threshold, storage or registry mechanism, and binds no provider or runtime
technology.
