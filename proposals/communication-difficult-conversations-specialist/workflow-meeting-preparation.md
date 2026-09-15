# Meeting / Call / Negotiation Communication Preparation — Workflow Candidate

Status: `PROPOSED`
Template: Workflow Card Template (Phase 5 standard candidate)
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: **Meeting / Call / Negotiation Communication Preparation**
- Workflow ID: `workflow.communication_meeting_preparation@0.1`
- Version: 0.1 · Status: PROPOSED
- Workflow Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands; S4 and S6 mandatory at high and critical
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Coordinate preparation for a live interaction — meeting, call, negotiation session or board
appearance — so that the participant enters with a fixed objective, a known boundary set, and a
clear statement of what may not be conceded in the room. Live interactions are the setting where
substantive positions are most often given away by accident.

## Trigger

`TRIGGER` — a scheduled or imminent live interaction within an assigned scope where
`communication_conflict_score >= 35`, or where the interaction concerns a disputed, contested or
high-stakes matter at any score.

## Preconditions

- `PRECONDITION` — the interaction is identified: participants, audience class, channel, time;
- `PRECONDITION` — a scope binding with sensitivity and disclosure labels exists;
- `PRECONDITION` — the stakes band is declared;
- `PRECONDITION` — every substantive domain in play has a named owning Role.

## Scope

### Covers
- objective fixing for the live interaction;
- position and boundary preparation;
- anticipated-move mapping and planned responses;
- the "lines not to cross" set;
- escalation and documentation plan for the interaction;
- post-interaction confirmation plan.

### Does Not Cover
- the substantive positions themselves;
- any authority to commit in the room;
- negotiation mandate setting (a human authority act);
- minutes as an official record;
- the interaction itself.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate)* | `LEAD_ROLE` | `ALWAYS` | S1–S6 | Prepares communication; gains no mandate and no authority to commit |
| **Substantive Owner Slot** | `CONTRIBUTING_ROLE` | `CONDITIONAL(a domain position is in play)` | S2, S4 | Owns the position; the brief cites it at its version |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `CONDITIONAL(dispute, contract or admission risk)` | S2, S4 | Owns admissions and reservations of rights |
| `role.project_finance_transaction_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(transaction terms in play)` | S2 | Owns the transaction position |
| `role.ppp_concession_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(concession or PPP terms in play)` | S2 | Owns the concession position |
| `role.institutional_affairs_stakeholder_specialist` | `CONSULTED_ROLE` | `CONDITIONAL(institutional counterparty)` | S3 | Owns the relationship position; advances no artifact here |

### Parameterized Role Slots

| Slot | Allowed source | Required ownership / interface condition | Permitted participation | Required artifact-ownership relationship | Phase 4 capability validation | Cardinality |
|---|---|---|---|---|---|---|
| **Substantive Owner Slot** | Approved Phase 3 Role universe | Already owns the position in play per its Role Card | `CONTRIBUTING_ROLE` | Retains ownership; the brief cites | Direct | `0..n` |

## Composed Workflow References

| Referenced Workflow | Version | Bounded purpose | Expected inputs | Expected outputs | Parent Stage(s) | Activation |
|---|---|---|---|---|---|---|
| `workflow.communication_boundary_setting@0.1` | pinned 0.1 | Produce the boundary set | Positions, constraints | Boundary formulations (`DRAFT`) | S3 | `ALWAYS` |
| `workflow.communication_refusal@0.1` | pinned 0.1 | Prepare a refusal for an anticipated ask | Anticipated ask, constraints | Refusal script (`DRAFT`) | S4 | `CONDITIONAL(a refusal is anticipated)` |

## Activated Skills / Packs

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `skill_pack.communication_difficult_conversations@0.1` *(candidate)* | `role.communication_difficult_conversations_specialist` *(candidate)* | Pending mapping record (`skill-pack.md` SP-1) |

## Inputs

| Input | Required knowledge state |
|---|---|
| Interaction details and participant list | `SOURCE` |
| Substantive positions in play | `DRAFT` minimum; `REVIEWED`/`APPROVED` where the interaction may commit |
| Prior correspondence and history | `SOURCE` |
| Constraints: `must_not_admit`, mandate limits, reservations | `SOURCE` |

## Stages

### Stage `S1` — Fix the objective and the success condition
- **Objective:** state what a good outcome of this interaction is, and what would make it a loss
- **Entry Criteria:** preconditions met
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` record the objective; `ACTIVITY` record the minimum acceptable outcome;
  `ACTIVITY` record what the interaction is explicitly **not** for
- **Artifact Contributions:** objective section of the Interaction Brief, owned by the lead
- **Knowledge-State Expectations:** an inferred objective is `ASSUMPTION`
- **Gate / Review References:** none
- **Exit Criteria:** objective, minimum outcome and non-purpose recorded
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`
- **Open-Item Materiality:** an unresolved objective is `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S2` — Assemble positions
- **Objective:** collect every substantive position the participant may be asked to state
- **Entry Criteria:** S1 complete
- **Participating Roles:** lead `LEAD_ROLE`; Substantive Owner Slot; conditional contributors
- **Activities:** `ACTIVITY` request each position at its version; `ACTIVITY` mark positions that
  are not yet settled as **not stateable in the room**; `ACTIVITY` raise `CONFLICT_DETECTED` on
  disagreement between owners
- **Artifact Contributions:** each position remains owned by its Role; the brief cites it
- **Knowledge-State Expectations:** an unsettled position is `UNKNOWN` and is flagged, never
  approximated
- **Gate / Review References:** none
- **Exit Criteria:** every in-play domain has a position or an explicit "not stateable" marker
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** a missing position in a domain that will certainly be raised is
  `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S3` — Build the boundary set and the lines not to cross
- **Objective:** fix in advance what will not be conceded, and how that is said
- **Entry Criteria:** S2 complete
- **Participating Roles:** lead `LEAD_ROLE`; `role.institutional_affairs_stakeholder_specialist`
  `CONSULTED_ROLE` where activated
- **Activities:** `ACTIVITY` formulate each boundary as self-directed action (`methodology-card.md`
  P-4); `ACTIVITY` list the admissions, commitments and characterisations that must not be made;
  `ACTIVITY` prepare the holding formulation for anything not yet settled
- **Artifact Contributions:** boundary set of the Interaction Brief
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** each boundary is stated, self-directed, and paired with a holding line
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S4` — Map anticipated moves and plan responses
- **Objective:** prepare for what the other side is likely to do, without predicting their motives
- **Entry Criteria:** S3 complete
- **Participating Roles:** lead `LEAD_ROLE`; conditional contributors
- **Activities:** `ACTIVITY` list anticipated asks, pressures and topic shifts as **observable
  moves**; `ACTIVITY` prepare a planned response per move, including "park it" and "not today";
  `ACTIVITY` prepare the refusal script where a refusal is anticipated
- **Artifact Contributions:** anticipated-move table of the Interaction Brief
- **Knowledge-State Expectations:** anticipated moves are `ASSUMPTION`; **no motive is attributed**
- **Gate / Review References:** none
- **Exit Criteria:** every anticipated move has a planned response
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

### Stage `S5` — Escalation and documentation plan
- **Objective:** decide in advance what gets escalated, what gets written down, and by whom
- **Entry Criteria:** S4 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` define the in-room escalation trigger and the exit line;
  `ACTIVITY` define the post-interaction written confirmation (`methodology-card.md` T-17);
  `ACTIVITY` define what must be recorded even if the interaction goes well
- **Artifact Contributions:** escalation and documentation plan of the Interaction Brief
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** trigger, exit line and confirmation plan recorded
- **Possible Outcomes:** `COMPLETE`

### Stage `S6` — Review the brief
- **Objective:** have someone other than the author check that the brief does not concede
- **Entry Criteria:** S5 complete
- **Participating Roles:** lead `LEAD_ROLE` as producer, ineligible to review
- **Activities:** `ACTIVITY` route to `review.communication_strategy@0.1` **whenever any RC-5 condition holds**; `ACTIVITY` route to
  `review.legal_compliance` where admissions are in scope
- **Artifact Contributions:** none
- **Knowledge-State Expectations:** satisfaction may support `REVIEWED`; the Workflow does not
  promote it
- **Gate / Review References:** `GATE_REFERENCE` `review.communication_strategy@0.1`;
  `review.legal_compliance`
- **Exit Criteria:** triggered reviews `SATISFIED`
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `BLOCKED`
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

## Branches / Exception Paths

- `BRANCH` **Unsettled position.** Where S2 finds a position the participant will be asked for and
  that is not settled, the brief carries a holding line and the matter is flagged for the owning
  Role rather than being guessed.
- `EXCEPTION_PATH` **The interaction may produce a commitment.** The brief states explicitly that
  any commitment requires the applicable `decision.<id>`, and that the participant's presence is
  not that authority. Preparation does not create a mandate.
- `EXCEPTION_PATH` **Interaction is brought forward.** Where time does not permit S6 at a band
  where it is mandatory, the instance is `BLOCKED` or `ESCALATED`; it does not proceed with the
  review skipped.

No exception path bypasses a review or gate reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` — S4 → S3 where a planned response would breach a boundary; S6 → S2/S3 on a review
finding. Prior brief versions and the finding are preserved.

## Open-Item Materiality

`MATERIAL_TO_NEXT_STEP_OR_GATE`: an unsettled position certain to be raised; an unsatisfied
mandatory review; an unresolved `CONFLICT_DETECTED` between owners. **None may support a `COMPLETE`
or `COMPLETE_WITH_OPEN_ITEMS` exit.** The outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.

**Rule MP-1 — authority and review satisfaction are separate, and neither cures the other.**
An earlier revision of this section allowed exit on any of the items above where a named external
human Decision Right permitted it. That is the same defect `workflow-difficult-interaction-response.md`
DIR-2 and `workflow-formal-escalation.md` FE-1 close, surviving in a second location. **None of the
items above is curable by a Decision Right**: a mandatory review is satisfied by a reviewer under its
Profile and by nothing else; an unresolved `CRITICAL_FINDING` is closed by the review that raised it;
an unresolved `CONFLICT_DETECTED` is resolved by the owning Roles; and a missing or stale substantive
conclusion is supplied by the Role that owns it. A decision to proceed anyway is a decision taken
*with the item open*, and it neither closes the item nor satisfies the review.

**Terminal progression requires both, separately:** every mandatory review `SATISFIED` under the
approved review contract, **and** every applicable Decision Right resolved. Satisfying one never
discharges the other. The only narrowly scoped exception DIR-2 allows is an unresolved **placeholder**
in a draft, decided on the record by the holder of the applicable Right; this Workflow produces no transmissible draft and carries no such item, so the exception never applies here. This Workflow
neither decides a waiver nor asserts one was granted.


## Completion Criteria

`COMPLETION_CRITERION` — the Interaction Brief exists, every in-play domain is covered or
explicitly marked not stateable, the boundary set is complete, and mandatory reviews are
`SATISFIED`. Complete is a coordination position, never an approval, and never a mandate.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the interaction is cancelled or postponed beyond the brief's validity;
the scope binding is revoked. The brief, its positions-at-version and any findings survive.

## Outputs / Resulting Artifact States

| Output | State | Owner |
|---|---|---|
| Interaction Brief | `DRAFT`, or `REVIEWED` where a review satisfied it | `role.communication_difficult_conversations_specialist` |
| Boundary set | `DRAFT` | as above |
| Refusal script, where prepared | `DRAFT` | as above |
| Positions cited | unchanged | each owning Role |

## Authority / Review Boundary

This Workflow does not set a negotiation mandate, does not authorise any commitment made in the
interaction, does not own any substantive position, does not satisfy any review it references, and
does not alter artifact ownership. Its specific leakage risk is **a brief being read as a
mandate**: a prepared line is a prepared line, not permission to say it where saying it would
commit the entity.

## Criticality Scaling

`LOW`/`MEDIUM`: S4 and S6 conditional. `HIGH`: both mandatory; every position must be cited at its
version. `CRITICAL`: additionally the boundary set is reviewed against the applicable Decision
Right boundaries, and the brief states the gate for every commitment it anticipates. Criticality
changes depth, not Role identity.

## Evidence / Traceability Requirements

The participant list and channel; each position at its version and owner; the boundary set and its
derivation; the anticipated-move assumptions; the escalation trigger; review findings and closure.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter authority, Role scope, gate
references or artifact ownership.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent
execution, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
