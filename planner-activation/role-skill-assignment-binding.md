# Role, Skill and Assignment Binding

Status: `PROPOSED` — Phase 16 candidate
Version: 0.1

## 1. Inference and assignability are different questions

**Rule RB-1 — the planner may infer a capability need; only the registry decides assignability.**
Inferring that work needs a communication-strategy conclusion is planning. Deciding that a
capability exists is the Role or Skill Registry's, and this phase reads those registries and
writes to neither.

**Rule RB-2 — an unregistered capability is non-assignable, and the plan blocks.** Not
substituted, not approximated by the nearest registered Role, not activated "pending
registration". `UNREGISTERED_CAPABILITY`, blocked, escalated.

**Rule RB-3 — a conclusion with no approved owner blocks the original request.** Where the
originally requested deliverable needs a conclusion the approved universe has no owner for, the
outcome is a block and an escalation. The system does not remove the conclusion, call the
remainder the deliverable and present it as the answer. A narrower deliverable is available only
if the user asks for one, as a new request.

## 2. The approved universe is read, never written

**Rule RB-4 — eligibility is declared evidence, never a slug or a mention.** The rule and its
evidence table live in `registry-eligibility-contract.md`; the short form is that an identity is
eligible only where a card declares it, the card carries a version and is not superseded, and a
human approval record covers that card class. The Role count is derived rather than hard-coded —
a phase that wrote "59" would still say 59 after something added a sixtieth — and it is
cross-checked against the approved universe in both directions.

**Rule RB-4a — assignability needs a compatible binding, not only a registered Skill.** A
registered Skill claimed for the wrong Role is an unassignable binding. Compatibility is read
from the Phase 4 Role-to-Skill **mapping** records, which state in terms that they are the sole
authoritative source for relationship type. `PROHIBITED_IN_CONTEXT` fails, and so does a pair
that appears in no mapping record: silence in the authoritative record is not permission. The
preflight blocks with `SKILL_ROLE_INCOMPATIBLE`.

**Rule RB-4b — every effective stage owner resolves.** A composed stage that is not a gate must
name an owner; that owner must be in the approved Role universe; and the plan must have declared
an owned conclusion for it. An owner appearing only inside a stage is an assignment nobody
declared and no approved registry was asked about. `STAGE_OWNER_UNRESOLVED`.

**Rule RB-4c — stage identity is unique before a basis is issued.** Duplicate stage ids used to
collapse into one another silently, taking the second stage's owner, artifact and dependencies
with them. Every planned work item spec is derived from stage identity, so a collision is not
cosmetic. `DUPLICATE_STAGE_IDENTITY`.

**Rule RB-5 — nothing here registers anything.** There is no write path, and the acceptance tests
assert that the approved Role universe is byte-identical before and after a planning attempt that
named an unregistered Role.

## 3. Separation of duties

**Rule RB-6 — author ≠ final critical reviewer, at identity level.** Not at Role level, not at
"different assignment" level: the same human identity may not both produce and finally review the
same work. The preflight blocks with `SOD_VIOLATION`.

**Rule RB-7 — a gate stage has no Role participation.** A gate is a point at which a human
decides, not work someone performs.

## 4. Non-Runtime Statement

This document is declarative architecture. It specifies no registry implementation, matcher,
index or storage mechanism, and binds no provider or runtime technology.
