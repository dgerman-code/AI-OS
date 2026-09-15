# Clarification Policy

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. The principle

> **Infer when safe; clarify only when ambiguity can materially change scope, authority, a
> professional conclusion, an irreversible action, or a governed outcome.**

Both halves matter. A system that asks about everything is unusable and trains users to click
through questions — including the one that mattered. A system that asks about nothing will
eventually send a contractual acceptance to the wrong counterparty.

## 2. Five classes of ambiguity

| Class | Name | Test | Disposition |
|---|---|---|---|
| **C1** | Safe default | A reasonable default exists, and being wrong costs a rewrite | **Infer.** Record the default and its basis; surface it as an assumption |
| **C2** | Recoverable ambiguity | Being wrong produces work that is discarded, with no external effect and no governed record | **Infer.** Surface prominently; make correction cheap |
| **C3** | Material ambiguity | Being wrong changes the deliverable, the professional conclusion, or which Roles own it | **Clarify** |
| **C4** | Authority ambiguity | Being wrong changes whether an act needs authority, which Right applies, or whether an irreversible act occurs | **Clarify, and block until answered** |
| **C5** | Scope ambiguity | Being wrong changes applicable knowledge, authority path, residency or sensitivity handling | **Clarify, and block until answered** (`context-scope-resolution.md` CS-7) |

**Rule CL-1 — the class is decided by consequence, not by confidence.** A 0.95-confidence reading
of an authority question is still C4. A 0.4-confidence reading of a tone preference is still C1.
Confidence may inform *how* the system presents an inference; it never changes the class.

**Rule CL-2 — C4 and C5 block.** They are not "ask and proceed on a default if no answer comes".
The plan sits in `AWAITING_CLARIFICATION` and, if unanswerable, becomes `BLOCKED`. The safe
direction is always the one that does less.

**Rule CL-3 — low confidence plus low consequence is not a question.** A C1 or C2 ambiguity is
inferred and surfaced, however uncertain. Asking would spend the user's attention on something that
cannot hurt them, and attention spent there is not available for C4.

## 3. What is never asked

**Rule CL-4 — never ask the user to choose an internal object.** Not a Workflow ID, a Role ID, a
Skill, a Review Profile, a Decision Right, a Model Profile, a routing policy or an orchestration
state. If the planner cannot determine which Workflow applies, the failure is the planner's, and
the resolution is COMPOSE or a block — not a menu.

The one exception: a user who **explicitly asks** to work at that level may. Offering it unprompted
is a violation; refusing it to a user who asked for it is unhelpful.

**Rule CL-5 — never ask a question whose answer the system will not use.** Every
`ClarificationRequirement` names the field it resolves and what changes once answered. A question
with no stated effect is a defect.

**Rule CL-6 — never ask a question the material already answers.** Clarification follows a genuine
attempt at inference, and the attempt is recorded.

## 4. How questions are formed

**Rule CL-7 — a question is about the user's world, not the system's.** Not *"which scope should I
use: `project.riverside` or `project.riverside_two`?"* but *"is this about the Riverside bridge
project or the Riverside depot expansion?"*

**Rule CL-8 — a question carries its consequence.** The user is told what changes: *"these have
different contracts, so the answer changes what we can say about liability."* A question without a
stated consequence gets answered carelessly.

**Rule CL-9 — questions are batched and minimal.** All open clarifications are presented together,
ordered by consequence, with C4 and C5 first. A single blocking question is asked alone.

**Rule CL-10 — the batch is bounded.** Where more than a handful of material questions are open,
the request is under-specified in a way that questioning will not fix, and the planner says so —
describing what it *could* plan if the user narrowed the request, and what would unlock the rest.
Describing is not doing: the narrower plan is produced only if the user asks for it, as a new linked
`Request` (RI-1, RS-13). A blocked request never becomes a narrower one on the planner's initiative,
whatever the reason for the block.

## 5. Assumptions are surfaced, not hidden

**Rule CL-11 — every C1 and C2 inference becomes a visible assumption.** The user sees what the
system decided on their behalf, in their own vocabulary, before work proceeds. An inference the
user cannot see is an inference they cannot correct.

**Rule CL-12 — an assumption is typed `ASSUMPTION` and stays there.** It is not a `FACT_CLAIM`, it
does not become one by going unchallenged, and the deliverable carries it as an assumption.

## 6. The answer is a new Request

**Rule CL-13 — a clarification answer is a linked `Request`, not an edit.** The original stands.
The plan revises to `@v2` and records what changed and why (`work-plan-object-model.md` OM-4). A
system that overwrote the original could not later show that it had misunderstood.

**Rule CL-14 — an answer resolves one field, not the class.** Answering *which* counterparty does
not answer whether the user wants the message **sent**. Each `ClarificationRequirement` closes
independently.

## 7. The `ClarificationRequirement` record

| Field | Content |
|---|---|
| `question` | In the user's vocabulary (CL-7) |
| `class` | `C1`…`C5` |
| `resolves_field` | The exact `WorkIntent` or `ScopeResolution` field |
| `consequence` | What changes once answered (CL-8) |
| `inference_attempted` | What the planner tried, and why it was insufficient (CL-6) |
| `blocking` | `true` for C4 and C5; `false` otherwise |
| `default_if_unanswered` | For C1 and C2 only. **Must be absent for C3, C4 and C5** |

**Rule CL-15 — `default_if_unanswered` on a blocking class is a validation failure.** A default for
a C4 question is precisely the thing the class exists to prevent, and
`governance-preflight.md` check G-7 fails a plan that carries one.

## 8. Worked classifications

| Request | Ambiguity | Class | Action |
|---|---|---|---|
| "Create a LinkedIn post about this news" | Tone and length unstated | **C1** | Infer a professional register; surface it |
| "Create a LinkedIn post about this news" | Posted under whose name — the entity's or the user's? | **C4** | Clarify. Publication under the entity's name is a governed act; under the user's it is not |
| "Prepare me for a meeting with EIB" | Which of two live projects | **C5** | Clarify and block |
| "Prepare a firm response" | How firm | **C2** | Infer; offer a firmer variant |
| "Check whether they are right" | Whether the user wants the answer, or wants it used in the reply | **C3** | Clarify — it changes the deliverable |
| "Send them confirmation that we accept the terms" | Which terms, which counterparty, and whether to actually send | **C4** ×3 | Clarify and block; **and** the Decision Right question blocks independently |

The second row is the one most systems get wrong: a LinkedIn post looks like a C1 request all the
way through, and the single question that matters — *whose name is on it* — is C4.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no dialogue manager, prompt, model,
interface, schema or storage mechanism, and binds no provider or runtime technology.
