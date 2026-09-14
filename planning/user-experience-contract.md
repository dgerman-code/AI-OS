# User Experience Contract

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. The obligation

A user writes what they want in ordinary language. They should never have to learn the architecture
to get work done — and they should never be unable to find out what it did.

Those two obligations pull in opposite directions, and this document is where the tension is
resolved rather than averaged.

## 2. What the user normally sees

| # | Surface | Content |
|---:|---|---|
| 1 | **What I understood** | The objective and deliverable in the user's own vocabulary, not field names |
| 2 | **What I plan to produce** | The deliverable and the shape of the work — "check the record, get a legal read, then draft" |
| 3 | **What I assumed** | Every C1 and C2 inference, visibly, before work proceeds (CL-11) |
| 4 | **What I don't know** | The material `UNKNOWN`s |
| 5 | **Questions that matter** | Only C3, C4 and C5 — ordered by consequence, blocking ones first (CL-9) |
| 6 | **Where a human decides** | Each point where a Decision Right is required, in plain terms |
| 7 | **Progress, blockers, results** | During the run |

**Rule UX-1 — the plan is shown as work, not as objects.** "A legal read on whether the contract
puts the delay on us" — not `RoleRequirement{role_ref: role.legal_regulatory_lead}`.

**Rule UX-2 — assumptions are shown before work, not after.** An assumption surfaced in a footnote
under a finished deliverable was never correctable.

## 3. What the user is never required to choose

**Rule UX-3 — none of these is ever required input:** a Workflow ID, a Role ID, a Skill ID, a
Review Profile ID, a Decision Right ID, a Model Profile, a routing policy, an orchestration state,
a work-item structure, a scope path string, or a confidence threshold.

**Rule UX-4 — a user who asks for that level gets it.** Offering internal objects unprompted
violates UX-3; refusing them to a user who explicitly wants to work at that level is unhelpful.
The default is hidden; the door is not locked.

## 4. What must always be visible

**Rule UX-5 — a removed or blocked act is stated, in terms the user will read.** Where the planner
drops an act it cannot authorise, or downgrades `EXECUTE` to `PREPARE`, the user is told **before**
they rely on it: *"I've drafted this but not sent it — sending it needs approval from someone who
holds the authority to accept terms."* Quietly producing a draft for a user who asked for a send is
the single most damaging thing this layer can do, because the user believes the act happened.

**Rule UX-6 — a block is delivered as an answer.** What is blocked, why, and what would unblock it.
Never an error code, never a silent empty result.

**Rule UX-7 — confidence is never displayed as safety.** A confidence value may appear in an
inspection view as a statement about the planner. It may not appear next to a plan as though it
said something about whether the work is sound, and it may never be presented as a reason the user
need not read an assumption (OM-15).

**Rule UX-8 — where a human gate exists, the user knows before the work starts.** Discovering at the
end that the deliverable cannot be sent wastes the work and the user's expectation.

## 5. Inspection

**Rule UX-9 — everything is inspectable.** Governance, admin and debug views may show the full
planning record: the `WorkIntent` fields, the scope resolution basis, the candidates considered and
rejected, the requirement derivations, the preflight check results, the confidence values. Nothing
is hidden from inspection; it is hidden from the **default** surface.

**Rule UX-10 — the inspection view is not an editing view.** Reading the planning record does not
let anyone change a governed outcome from it. A view that let an admin flip a preflight check would
be an authority path wearing a debug label.

## 6. What the product must not imply

**Rule UX-11 — no persona.** The layer has no name the user addresses, no personality, no
first-person identity beyond ordinary system voice, and no continuity that would make it feel like
a colleague who remembers. `ROLE != AGENT INSTANCE`, and a planner function is not even a Role.

**Rule UX-12 — no implied authority.** The product never says a deliverable is "approved", "ready
to send", "cleared" or "final" on the strength of planning. Those words describe governed outcomes
that only humans and reviews produce.

**Rule UX-13 — no implied certainty.** An inferred field is presented as an inference. A plan
presented with the confidence of a fact is a plan the user will not check.

**Rule UX-14 — no memory across scopes.** The product does not carry material, tone or conclusions
from one scope's request into another's, and it does not offer to. Cross-scope reuse is a governed
transfer, not a convenience (`knowledge/scope-isolation-and-transfer.md` §4).

## 7. The test this contract has to pass

A user with no knowledge of AI-OS writes three sentences about a partner dispute. They should get:
work that is actually useful; a short list of assumptions they can correct; at most one or two
questions, each obviously worth answering; and a clear statement of what needs someone's approval
before it goes anywhere.

They should not get: a menu of Workflows, a request to pick a Role, a confidence percentage
presented as reassurance, a draft that quietly went unsent, or a finished deliverable resting on an
assumption they never saw.

## 8. Non-Runtime Statement

This document is declarative architecture. It specifies no interface, component, layout, interaction
implementation, framework or storage mechanism, and binds no provider or runtime technology.
