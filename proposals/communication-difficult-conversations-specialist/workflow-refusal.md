# Refusal — Workflow Candidate

Status: `PROPOSED`
Template: Workflow Card Template (Phase 5 standard candidate)
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: **Refusal**
- Workflow ID: `workflow.communication.refusal@0.1`
- Registry-normalised alternative (open item **OG-1**): `workflow.communication_refusal@0.1`
- Version: 0.1 · Status: PROPOSED
- Workflow Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands; S2 and S5 mandatory at high and critical
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Coordinate the production of a clear "no" that is unambiguous, minimally justified, and does not
concede by accident — and that expresses a refusal **decision someone else has made**, since
deciding to refuse is frequently an authority act rather than a communication act.

## Trigger

`TRIGGER` — a request has been received or is anticipated, the response posture is to decline, and
the refusal must be communicated.

## Preconditions

- `PRECONDITION` — the request is identified precisely, including what exactly is being declined;
- `PRECONDITION` — **the refusal decision exists and is attributed** — either it is within the
  user's own action alone, or it is a decision made by whoever holds the authority to make it;
- `PRECONDITION` — any obligation that would make refusal a breach is supplied by its owning Role.

## Scope

### Covers
- stating the refusal unambiguously;
- selecting the minimum sufficient rationale;
- deciding whether to offer a narrower alternative;
- preserving the relationship where that is an objective;
- preserving optionality for anything not yet decided.

### Does Not Cover
- the decision to refuse;
- whether refusing breaches an obligation;
- the consequences of refusal;
- renegotiation of the underlying terms;
- the transmitting act.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate)* | `LEAD_ROLE` | `ALWAYS` | S1, S3–S5 | Expresses a refusal; never makes one |
| **Refusal Decision Owner Slot** | `CONTRIBUTING_ROLE` | `CONDITIONAL(the refusal is not within the user's own action alone)` | S2 | Owns the decision to refuse; supplies it, and retains it |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `CONDITIONAL(refusal may breach an obligation, or the request is legally sensitive)` | S2, S5 | Owns whether refusal is available and what may be said about why |
| `role.programme_partnership_manager` | `CONSULTED_ROLE` | `CONDITIONAL(the requester is a partner or consortium member)` | S3 | Owns the relationship position; advances no artifact here |

### Parameterized Role Slots

| Slot | Allowed source | Required ownership / interface condition | Permitted participation | Required artifact-ownership relationship | Phase 4 capability validation | Cardinality |
|---|---|---|---|---|---|---|
| **Refusal Decision Owner Slot** | Approved Phase 3 Role universe, or a human authority holding the applicable `decision.<id>` | Must already own the conclusion, or hold the Right, that the refusal rests on | `CONTRIBUTING_ROLE` | Retains the decision; the refusal text cites it | Direct | `0..1` |

Where no approved Role or Right owner can be identified and the refusal is not within the user's
own action alone, the instance is `BLOCKED`. The slot is not widened and the lead does not decide.

## Activated Skills / Packs

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `pack.communication.difficult_conversations@0.1` *(candidate)* | `role.communication_difficult_conversations_specialist` *(candidate)* | Pending mapping record (`skill-pack.md` SP-1) |

## Inputs

| Input | Required knowledge state |
|---|---|
| The request, precisely scoped | `SOURCE` |
| The refusal decision and its owner | `DRAFT` minimum, attributed |
| Obligations that bear on refusal | `APPROVED` or cited at version |
| Relationship objective and stakes | `SOURCE` |

## Stages

### Stage `S1` — Scope what is being declined
- **Objective:** refuse the actual request, not a larger or smaller one
- **Entry Criteria:** preconditions met
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` restate the request precisely from the record; `ACTIVITY` separate the
  parts being declined from any part being accepted or deferred; `ACTIVITY` identify what would
  otherwise be read into the refusal
- **Artifact Contributions:** scope note, owned by the lead
- **Knowledge-State Expectations:** the restatement is a `FACT_CLAIM` linked to `EVIDENCE` where directly supported, otherwise
  `ASSUMPTION` and flagged for confirmation
- **Gate / Review References:** none
- **Exit Criteria:** the declined scope is explicit and bounded
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`
- **Open-Item Materiality:** an ambiguous request scope is `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S2` — Confirm the refusal decision and its availability
- **Objective:** establish that a refusal decision exists, who made it, and that it is available
- **Entry Criteria:** S1 complete
- **Participating Roles:** lead `LEAD_ROLE`; Refusal Decision Owner Slot; conditional contributors
- **Activities:** `ACTIVITY` obtain the refusal decision, attributed and at its version;
  `ACTIVITY` where refusal may breach an obligation, obtain that conclusion from its owning Role;
  `ACTIVITY` record what may and may not be said about the reason
- **Artifact Contributions:** the decision remains owned by its owner; the refusal cites it
- **Knowledge-State Expectations:** an unattributed refusal is `UNKNOWN` — the instance blocks
  rather than inventing one
- **Gate / Review References:** none
- **Exit Criteria:** the decision and its owner are recorded, and the obligation question is
  answered where raised
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** an unowned refusal decision is `MATERIAL_TO_NEXT_STEP_OR_GATE`
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

### Stage `S3` — Choose the rationale and the alternative
- **Objective:** decide how much to say and whether to offer anything
- **Entry Criteria:** S2 complete
- **Participating Roles:** lead `LEAD_ROLE`; `role.programme_partnership_manager` `CONSULTED_ROLE`
  where activated
- **Activities:** `ACTIVITY` select the one sufficient reason (`methodology-card.md` P-8);
  `ACTIVITY` discard reasons that add attack surface; `ACTIVITY` decide whether a narrower
  alternative exists and is within someone's authority to offer (T-13); `ACTIVITY` decide whether
  the relationship objective requires an appreciation opening (T-23)
- **Artifact Contributions:** rationale selection note
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** one rationale selected; the alternative decided and attributed if offered
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`
- **Open-Item Materiality:** an alternative nobody has authority to offer is
  `MATERIAL_TO_NEXT_STEP_OR_GATE` — it is removed

### Stage `S4` — Draft and filter
- **Objective:** produce a refusal that cannot be read as a maybe
- **Entry Criteria:** S3 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` draft: position, one reason, optional alternative, next step;
  `ACTIVITY` remove hedging that creates ambiguity about whether this is a no; `ACTIVITY` verify
  no sentence concedes the underlying point or admits fault; `ACTIVITY` apply the Communication
  Control Filter and record the ten component scores
- **Artifact Contributions:** Refusal text (`DRAFT`), owned by the lead
- **Knowledge-State Expectations:** `DRAFT`; filter scores are `CALCULATION` and are not approval
- **Gate / Review References:** none. The filter is not a gate
- **Exit Criteria:** the refusal is unambiguous, carries one rationale, and is scored
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S5` — Review
- **Objective:** have someone other than the author confirm the no is a no and concedes nothing
- **Entry Criteria:** S4 complete
- **Participating Roles:** lead `LEAD_ROLE` as producer, ineligible to review
- **Activities:** `ACTIVITY` route to `review.communication_strategy@0.1` **whenever any RC-5 condition holds**; `ACTIVITY` route to
  `review.legal_compliance` where refusal bears on an obligation
- **Artifact Contributions:** none
- **Knowledge-State Expectations:** satisfaction may support `REVIEWED`; not promoted here
- **Gate / Review References:** `GATE_REFERENCE` `review.communication_strategy@0.1`;
  `review.legal_compliance`
- **Exit Criteria:** triggered reviews `SATISFIED`
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `BLOCKED`
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

## Branches / Exception Paths

- `BRANCH` **Partial refusal.** Where part of the request is accepted, the accepted part is stated
  as precisely as the declined part; a vague acceptance beside a precise refusal is how scope
  creeps back.
- `BRANCH` **Relationship-preserving refusal.** Appreciation, clear refusal, future-safe
  alternative (T-23) — the refusal itself is not softened.
- `EXCEPTION_PATH` **No refusal decision.** S2 blocks. The lead does not decide to refuse, and
  does not draft a refusal on the assumption that one will be decided.
- `EXCEPTION_PATH` **Refusal would breach an obligation.** The instance is `ESCALATED` to the
  owning Role and the Decision Right holder for the obligation. Communication does not resolve it.
- `EXCEPTION_PATH` **Transmission requested.** Re-enters
  `workflow.communication.difficult_interaction_response@0.1` at its S11 gate.

No exception path bypasses a review or gate reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` — S4 → S3 where the draft reveals the rationale is insufficient; S5 → S3/S4 on a
review finding. Prior drafts, rationale selections and findings are preserved.

## Open-Item Materiality

`MATERIAL_TO_NEXT_STEP_OR_GATE`: an unowned refusal decision; an unanswered obligation question; an
unauthorised alternative; an unsatisfied mandatory review. None may support a `COMPLETE` or
`COMPLETE_WITH_OPEN_ITEMS` exit absent a named external human Decision Right, whose reference is
then recorded with the item left open.

## Completion Criteria

`COMPLETION_CRITERION` — an unambiguous refusal exists, attributed to a decision someone owns,
carrying one sufficient rationale, filtered and scored, with mandatory reviews `SATISFIED`.
Complete is a coordination position, never an approval, and never the refusal decision itself.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the request is withdrawn; the refusal decision is reversed by its owner;
the scope binding is revoked. The scope note, the decision citation and any findings survive.

## Outputs / Resulting Artifact States

| Output | State | Owner |
|---|---|---|
| Refusal text | `DRAFT`, or `REVIEWED` where satisfied | `role.communication_difficult_conversations_specialist` |
| Scope note | `DRAFT` | as above |
| Rationale selection note | `DRAFT` | as above |
| Refusal decision cited | unchanged | its owner |

## Authority / Review Boundary

This Workflow does not decide to refuse; does not determine whether refusal breaches an obligation;
does not accept the consequences of refusing; does not offer an alternative nobody has authority to
offer; does not satisfy any review it references; and does not transmit. Its specific leakage risk
is **the lead drafting a refusal that no one has decided**, which produces a message the entity has
not authorised and cannot easily retract.

## Criticality Scaling

`LOW`/`MEDIUM`: S2 and S5 conditional where the refusal is within the user's own action alone.
`HIGH`: both mandatory; the decision must be cited at version. `CRITICAL`: additionally
`review.legal_compliance` is mandatory and the obligation question must be answered in writing by
its owning Role. Criticality changes depth, not Role identity.

## Evidence / Traceability Requirements

The request as recorded; the declined scope; the refusal decision, its owner and version; the
obligation conclusion where obtained; the rationale selection and the discarded reasons; the filter
scores; review findings and closure.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter authority, Role scope, gate
references or artifact ownership.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent
execution, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
