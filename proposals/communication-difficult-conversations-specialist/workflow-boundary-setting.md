# Boundary Setting — Workflow Candidate

Status: `PROPOSED`
Template: Workflow Card Template (Phase 5 standard candidate)
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: **Boundary Setting**
- Workflow ID: `workflow.communication_boundary_setting@0.1`
- Version: 0.1 · Status: PROPOSED
- Workflow Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands; S4 mandatory at high and critical
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Coordinate the formulation of a boundary — a stated limit on what the user will and will not do —
so that it is enforceable by the user alone, does not overstate authority, and does not silently
become a threat or a commitment.

## Trigger

`TRIGGER` — a boundary issue is classified material in a Conversation Diagnostic, or an assignment
explicitly requests a boundary formulation.

## Preconditions

- `PRECONDITION` — the behaviour, request or pattern the boundary responds to is identified in the
  record;
- `PRECONDITION` — the user's actual authority over the boundary's subject is known;
- `PRECONDITION` — any contractual or programme obligation constraining the boundary is supplied.

## Scope

### Covers
- deciding whether a boundary is the right instrument;
- formulating it as self-directed action;
- stating its consequence, where one is factual and within the user's own authority;
- placing it in the escalation ladder.

### Does Not Cover
- whether the user has the underlying right to impose the limit (a legal or contractual question);
- whether a stated consequence may lawfully be applied;
- the decision to apply a consequence;
- the transmitting act.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate)* | `LEAD_ROLE` | `ALWAYS` | S1–S4 | Formulates the boundary; establishes no entitlement to it |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the boundary rests on a contractual right, or a consequence is stated)` | S2, S4 | Owns whether the right exists and whether the consequence is available |
| `role.people_organisation_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the counterparty is an employee or the matter is a people matter)` | S2, S4 | Owns the employment position |
| `role.programme_partnership_manager` | `CONSULTED_ROLE` | `CONDITIONAL(the counterparty is a consortium partner)` | S2 | Owns the partnership position; advances no artifact here |

## Activated Skills / Packs

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `skill_pack.communication_difficult_conversations@0.1` *(candidate)* | `role.communication_difficult_conversations_specialist` *(candidate)* | Pending mapping record (`skill-pack.md` SP-1) |

## Inputs

| Input | Required knowledge state |
|---|---|
| The behaviour, request or pattern at issue | `SOURCE` |
| The user's authority over the subject | `FACT_CLAIM` linked to `EVIDENCE` where evidenced; `UNKNOWN` otherwise |
| Contractual / programme obligations in force | `APPROVED` or cited at version |
| Relationship context and stakes | `SOURCE` |

## Stages

### Stage `S1` — Test whether a boundary is the right instrument
- **Objective:** avoid setting a boundary where a clarification, a redirect or a decision is what
  is actually needed
- **Entry Criteria:** preconditions met
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` identify what is actually being asked of the user; `ACTIVITY` test the
  alternatives — clarify, redirect, refuse, escalate, do nothing; `ACTIVITY` record why a boundary
  is or is not the instrument
- **Artifact Contributions:** instrument-selection note, owned by the lead
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** the instrument is chosen with a recorded reason
- **Possible Outcomes:** `COMPLETE`, `CANCELLED` (a boundary is not the instrument)
- **Open-Item Materiality:** none material at this stage

### Stage `S2` — Establish the authority basis
- **Objective:** know whether the user can actually hold the line before writing it
- **Entry Criteria:** S1 chose a boundary
- **Participating Roles:** lead `LEAD_ROLE`; conditional contributors
- **Activities:** `ACTIVITY` determine whether the boundary is within the user's own action alone;
  `ACTIVITY` where it rests on a contractual or employment right, obtain that conclusion from its
  owning Role; `ACTIVITY` where a consequence is contemplated, obtain whether it is available
- **Artifact Contributions:** the authority basis remains owned by the contributing Role
- **Knowledge-State Expectations:** an unverified entitlement is `UNKNOWN`; the boundary is then
  narrowed to what the user can do alone
- **Gate / Review References:** none
- **Exit Criteria:** the basis is established, or the boundary is narrowed to self-action only
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** a stated consequence with no established availability is
  `MATERIAL_TO_NEXT_STEP_OR_GATE` — it is removed or the instance blocks

### Stage `S3` — Formulate
- **Objective:** write the boundary so that it holds without requiring agreement
- **Entry Criteria:** S2 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` express as self-directed action — what the user will and will not do
  (`methodology-card.md` P-4); `ACTIVITY` remove commands directed at the other party;
  `ACTIVITY` state the consequence only where S2 established it, factually and without accusation
  (T-14); `ACTIVITY` add the narrower alternative where one exists (T-13); `ACTIVITY` verify the
  formulation makes no admission and no commitment beyond its own terms
- **Artifact Contributions:** Boundary formulation (`DRAFT`), owned by the lead
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** the boundary is self-directed, unambiguous, and carries no unestablished
  consequence
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S4` — Place in the ladder and review
- **Objective:** know what comes next if the boundary is ignored, and have someone check it
- **Entry Criteria:** S3 complete
- **Participating Roles:** lead `LEAD_ROLE` as producer, ineligible to review; conditional
  contributors as reviewers where eligible
- **Activities:** `ACTIVITY` place the boundary on the escalation ladder — clarify → boundary →
  deadline → formal escalation (T-21); `ACTIVITY` state what the next step is and who takes it;
  `ACTIVITY` route to `review.communication_strategy@0.1` **whenever any RC-5 condition holds** and, where a consequence or contractual
  right is stated, `review.legal_compliance`. A boundary carrying a consequence satisfies
  **RC-5.3**, so the communication review is mandatory at **every** band for such a boundary
- **Artifact Contributions:** ladder placement note
- **Knowledge-State Expectations:** satisfaction may support `REVIEWED`; not promoted here
- **Gate / Review References:** `GATE_REFERENCE` `review.communication_strategy@0.1`;
  `review.legal_compliance`
- **Exit Criteria:** ladder placement recorded; triggered reviews `SATISFIED`
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `BLOCKED`
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

## Branches / Exception Paths

- `BRANCH` **Not the instrument.** S1 may terminate the instance where clarification or a decision
  is what is needed. That is a correct outcome, not a failure.
- `BRANCH` **Narrowed boundary.** Where S2 cannot establish an entitlement, the boundary is
  narrowed to self-action and the entitlement question is escalated to its owning Role.
- `EXCEPTION_PATH` **The boundary would be a threat.** Where the contemplated consequence is not
  available to the user, or is disproportionate, the instance is `BLOCKED` and escalated. A
  consequence the user cannot bring about is a threat, and `methodology-card.md` S-3 puts it out
  of scope.
- `EXCEPTION_PATH` **Transmission requested.** Setting a boundary is not sending one. Transmission
  re-enters `workflow.communication_difficult_interaction_response@0.1` at its S11 gate.

No exception path bypasses a review or gate reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` — S3 → S2 where formulation reveals an unestablished entitlement; S4 → S3 on a review
finding. Prior formulations and findings are preserved.

## Open-Item Materiality

`MATERIAL_TO_NEXT_STEP_OR_GATE`: an unestablished consequence; an unverified contractual basis; an
unsatisfied mandatory review. None may support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit
absent a named external human Decision Right permitting progression, whose reference is then
recorded with the item left open.

## Completion Criteria

`COMPLETION_CRITERION` — a self-directed boundary exists, its basis is established or it has been
narrowed, its ladder position is recorded, and mandatory reviews are `SATISFIED`. Complete is a
coordination position, never an approval, and never a determination that the user is entitled to
the limit.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the underlying request is withdrawn; the relationship ends; the scope
binding is revoked. The instrument-selection note, the formulation and any findings survive.

## Outputs / Resulting Artifact States

| Output | State | Owner |
|---|---|---|
| Boundary formulation | `DRAFT`, or `REVIEWED` where satisfied | `role.communication_difficult_conversations_specialist` |
| Instrument-selection note | `DRAFT` | as above |
| Ladder placement note | `DRAFT` | as above |
| Authority basis cited | unchanged | owning Role |

## Authority / Review Boundary

This Workflow does not determine that the user is entitled to the limit; does not determine that a
consequence may lawfully be applied; does not decide to apply one; does not own the employment,
contractual or partnership position; does not satisfy any review it references; and does not
transmit. Its specific leakage risk is **a well-formed boundary being mistaken for an established
right** — the formulation is communication work, and S2's basis is someone else's conclusion.

## Criticality Scaling

`LOW`/`MEDIUM`: S4 review conditional. `HIGH`: S4 mandatory; the authority basis must be cited at
version. `CRITICAL`: additionally `review.legal_compliance` is mandatory wherever a consequence is
stated. Criticality changes depth, not Role identity.

## Evidence / Traceability Requirements

The behaviour at issue and its source; the instrument-selection reasoning; the authority basis at
version and its owner; the formulation history; the ladder placement; review findings and closure.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter authority, Role scope, gate
references or artifact ownership.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent
execution, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
