# Clarification and Ambiguity Contract

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

## 1. The rule Phase 15 set, carried without amendment

**Infer when safe. Clarify when the ambiguity can materially change scope, authority, a
professional conclusion, an irreversible action or a governed outcome.**

**Rule CA-1 — asking is not free, and neither is not asking.** A question spent on something that
cannot hurt the user is attention unavailable for one that can. A question not asked about scope
or authority is a governed outcome decided by the system.

## 2. The blocking state

**Rule CA-2 — `CLARIFICATION_REQUIRED` produces no Execution Basis at all.** Not a blocked one, not
a draft one: none. There is nothing for a caller to pick up, retry against, or read as partial
progress, and `build_trigger` therefore has nothing to be handed.

**Rule CA-3 — a blocking clarification carries no default.** A `default_if_unanswered` on a
blocking class is refused by exception, not merely blocked: a default on a blocking question is
the system answering a question it declared it could not answer.

**Rule CA-4 — the answer is a new linked request.** It is not an edit to the original, and it is
not an automatic fallback to a smaller act. Where the user afterwards asks for something narrower,
that is a decision they made, recorded as a new request and a new plan version.

## 3. What never resolves an ambiguity

| Never | Because |
|---|---|
| High confidence | Confidence is a statement about the planner, not about what is permitted |
| Convenience, urgency or a deadline | None of them is evidence about scope or authority |
| Choosing the safer-looking act | `PREPARE` instead of `EXECUTE` is a **different act**, chosen by the system without being told |
| Asking the model what it thinks | The ambiguity is in the request, not in the reading |

## 4. Non-Runtime Statement

This document is declarative architecture. It specifies no interface, prompt, channel or storage
mechanism, and binds no provider or runtime technology.
