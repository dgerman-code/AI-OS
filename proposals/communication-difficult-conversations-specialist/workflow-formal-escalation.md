# Formal Escalation — Workflow Candidate

Status: `PROPOSED`
Template: Workflow Card Template (Phase 5 standard candidate)
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: **Formal Escalation**
- Workflow ID: `workflow.communication.formal_escalation@0.1`
- Registry-normalised alternative (open item **OG-1**): `workflow.communication_formal_escalation@0.1`
- Version: 0.1 · Status: PROPOSED
- Workflow Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands; **S2, S5 and S6 are mandatory at every band** — a formal
  escalation is decision-grade by construction
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Coordinate the production of a formal escalation — a neutral chronology, the unresolved matter,
and the action requested of a named authority — so that the record it creates is accurate, the
position it states is the owning Role's, and the act of escalating is authorised by someone who
holds that authority.

## Trigger

`TRIGGER` — the escalation ladder (`methodology-card.md` T-21) is exhausted: clarification,
boundary and deadline have been used and the matter is unresolved; **or** the matter is of a class
that escalates immediately, such as a safety, integrity, regulatory or legal-exposure issue.

## Preconditions

- `PRECONDITION` — a complete, verifiable chronology exists in the record;
- `PRECONDITION` — the unresolved matter is stated and its owning Role has a current conclusion;
- `PRECONDITION` — the escalation target authority is identified;
- `PRECONDITION` — the stakes band is declared and the sensitivity of the record is labelled.

## Scope

### Covers
- construction of a neutral, verifiable chronology;
- statement of the unresolved matter;
- statement of what is requested of the recipient authority;
- tone and register appropriate to a formal record;
- identification of the review and gate required before the escalation is sent.

### Does Not Cover
- the decision to escalate;
- the substantive conclusion being escalated;
- whether the matter is a breach, a default, a violation or a claim;
- the recipient's response;
- the transmitting act.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate)* | `LEAD_ROLE` | `ALWAYS` | S1, S3–S5 | Constructs the escalation artifact; does not decide to escalate and does not characterise the matter legally |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `ALWAYS` | S2, S5 | Owns every legal characterisation, admission and reservation of rights. A formal escalation is a legally consequential document, so this Role is not conditional here |
| **Matter Owner Slot** | `CONTRIBUTING_ROLE` | `ALWAYS` | S2 | Owns the substantive conclusion the escalation rests on |
| `role.institutional_affairs_stakeholder_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the recipient is an institutional or public authority)` | S2, S5 | Owns the institutional relationship position |
| `role.people_organisation_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the matter is an employment or grievance matter)` | S2, S5 | Owns the people-matter position |
| `role.integrity_due_diligence_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the matter concerns integrity, fraud or misconduct)` | S2 | Owns the integrity finding |
| `role.data_protection_gdpr_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the chronology discloses personal data)` | S2, S5 | Owns lawful basis for the disclosure |

### Parameterized Role Slots

| Slot | Allowed source | Required ownership / interface condition | Permitted participation | Required artifact-ownership relationship | Phase 4 capability validation | Cardinality |
|---|---|---|---|---|---|---|
| **Matter Owner Slot** | Approved Phase 3 Role universe | Already owns the conclusion the escalation rests on | `CONTRIBUTING_ROLE` | Retains ownership; the escalation cites it at version | Direct | `1..n` |

Cardinality is `1..n`, not `0..n`: an escalation with no substantive owner is an escalation about
nothing, and the instance is `BLOCKED`.

## Activated Skills / Packs

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `pack.communication.difficult_conversations@0.1` *(candidate)* | `role.communication_difficult_conversations_specialist` *(candidate)* | Pending mapping record (`skill-pack.md` SP-1) |

## Inputs

| Input | Required knowledge state |
|---|---|
| The full interaction history | `SOURCE`, unedited and attributed |
| The substantive conclusion at issue | `REVIEWED` or `APPROVED` |
| Legal characterisation, where any is stated | `REVIEWED` or `APPROVED`, owned by `role.legal_regulatory_lead` |
| Prior ladder steps taken | `FACT` with dates |
| Recipient authority and its remit | `SOURCE` |

## Stages

### Stage `S1` — Construct the chronology
- **Objective:** produce a record that survives being checked
- **Entry Criteria:** preconditions met
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` extract every relevant event with date, actor and source reference;
  `ACTIVITY` exclude characterisation, adjectives and inference from the chronology entirely;
  `ACTIVITY` mark gaps as gaps rather than bridging them; `ACTIVITY` record the ladder steps taken
  and their dates
- **Artifact Contributions:** chronology section of the Escalation artifact, owned by the lead
- **Knowledge-State Expectations:** every entry is `FACT` with provenance, or it is omitted. An
  inferred event is never a chronology entry
- **Gate / Review References:** none
- **Exit Criteria:** every entry is dated, attributed and source-linked; gaps are marked
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `ESCALATED`
- **Open-Item Materiality:** an unverifiable entry is `MATERIAL_TO_NEXT_STEP_OR_GATE` — it is
  removed or evidenced

### Stage `S2` — Obtain the substantive and legal positions
- **Objective:** ensure the escalation states other people's conclusions, not the lead's
- **Entry Criteria:** S1 complete
- **Participating Roles:** lead `LEAD_ROLE`; `role.legal_regulatory_lead`; Matter Owner Slot;
  conditional contributors
- **Activities:** `ACTIVITY` obtain the substantive conclusion at its version; `ACTIVITY` obtain
  the legal characterisation, or an explicit statement that none is made; `ACTIVITY` obtain the
  disclosure basis where personal data appears; `ACTIVITY` record what may not be asserted
- **Artifact Contributions:** each conclusion remains owned by its Role
- **Knowledge-State Expectations:** `REVIEWED` or `APPROVED`. A `DRAFT` legal characterisation does
  not go into a formal escalation
- **Gate / Review References:** none
- **Exit Criteria:** every position the escalation states is obtained and attributed
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** a missing or `DRAFT` legal characterisation is
  `MATERIAL_TO_NEXT_STEP_OR_GATE`
- **Mandatory at:** every band

### Stage `S3` — State the unresolved matter and the request
- **Objective:** say what is unresolved and what the recipient is being asked to do
- **Entry Criteria:** S2 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` state the matter in one paragraph, without accusation; `ACTIVITY`
  state the specific action requested and the authority it requires; `ACTIVITY` state the date by
  which the action is needed and why that date; `ACTIVITY` state what happens next if no action
  follows, **only** where that consequence is established and available
- **Artifact Contributions:** matter and request sections of the Escalation artifact
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** matter, request, date and — where stated — an established consequence
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S4` — Register, tone and filter
- **Objective:** produce a document that reads as a record, not as a complaint
- **Entry Criteria:** S3 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` apply the final-position architecture (`methodology-card.md` T-22);
  `ACTIVITY` remove every characterisation of the other party; `ACTIVITY` verify no sentence makes
  an admission or waives a right; `ACTIVITY` apply the Communication Control Filter and record the
  ten component scores
- **Artifact Contributions:** Escalation artifact (`DRAFT`), owned by the lead
- **Knowledge-State Expectations:** `DRAFT`; filter scores are `CALCULATION`, not approval
- **Gate / Review References:** none. The filter is not a gate
- **Exit Criteria:** the document is neutral in register and carries no admission or waiver
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S5` — Required reviews
- **Objective:** have the document checked by those who own what it asserts
- **Entry Criteria:** S4 complete
- **Participating Roles:** lead `LEAD_ROLE` as producer, ineligible to review; contributors as
  reviewers where their own eligibility permits
- **Activities:** `ACTIVITY` route to `review.high_stakes_external_communication@0.1`;
  `ACTIVITY` route to `review.communication_strategy@0.1`; `ACTIVITY` route to
  `review.legal_compliance`; `ACTIVITY` route to `review.institutional_position` and
  `review.data_protection` where their triggers hold; `ACTIVITY` route to
  `review.evidence_integrity_provenance` for the chronology
- **Artifact Contributions:** none
- **Knowledge-State Expectations:** satisfaction may support `REVIEWED`; not promoted here
- **Gate / Review References:** `GATE_REFERENCE` `review.high_stakes_external_communication@0.1`;
  `review.communication_strategy@0.1`; `review.legal_compliance`;
  `review.evidence_integrity_provenance`; `review.institutional_position`;
  `review.data_protection`
- **Exit Criteria:** every triggered review is `SATISFIED`
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `BLOCKED`, `ESCALATED`
- **Mandatory at:** every band

### Stage `S6` — Human decision gate
- **Objective:** obtain the human authority to escalate, or block
- **Entry Criteria:** S5 complete
- **Participating Roles:** none. A gate is not work
- **Activities:** `ACTIVITY` resolve the applicable `decision.<id>` per
  `decision-right-gap-analysis.md` §4 — for a filing or a submission to an authority, the
  applicable submission or filing Right; for an escalation to a regulator or a public authority,
  the applicable disclosure or publication Right; `ACTIVITY` where none resolves, set posture
  `AUTHORITY_ABSENT`, block and escalate internally
- **Artifact Contributions:** none
- **Knowledge-State Expectations:** unchanged
- **Gate / Review References:** `GATE_REFERENCE` the resolved `decision.<id>`
- **Exit Criteria:** a Decision Record exists for this escalation at this version, to this
  recipient — or the instance is `BLOCKED`
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`, `CANCELLED`
- **Open-Item Materiality:** every open item is `MATERIAL_TO_NEXT_STEP_OR_GATE` here
- **Mandatory at:** every band

## Branches / Exception Paths

- `BRANCH` **Immediate-escalation class.** Safety, integrity, regulatory and legal-exposure matters
  skip the ladder precondition, not the stages. S2, S5 and S6 still apply in full.
- `BRANCH` **Internal escalation.** Where the recipient is internal, S6 may resolve to no external
  Right because no external act occurs; the review set at S5 still applies, and the moment the
  matter moves outside the entity, S6 applies.
- `EXCEPTION_PATH` **Chronology cannot be verified.** S1 removes the entry. An escalation built on
  an unverifiable chronology is the failure mode this Workflow most needs to prevent, because the
  document survives and the error with it.
- `EXCEPTION_PATH` **No legal characterisation available.** The escalation states the facts and the
  request and makes **no** characterisation. It does not wait for one, and the lead does not supply
  one.
- `EXCEPTION_PATH` **No applicable Decision Right.** S6 blocks with posture `AUTHORITY_ABSENT`.

No exception path bypasses a review or gate reference carried by the normal path.

## Rework Rules

`REWORK_LOOP` — S3 → S1 where the request reveals a chronology gap; S4 → S3 where register work
would change meaning; S5 → S1/S2/S3/S4 on a finding. Every prior version, the findings and the
chronology history are preserved. Re-entering S5 makes any earlier satisfaction `STALE`.

## Open-Item Materiality

For the gate at S6: an unverifiable chronology entry; a missing or `DRAFT` substantive or legal
position; an unresolved disclosure basis; an unsatisfied review; an unresolved `CRITICAL_FINDING`;
and an unestablished stated consequence are all `MATERIAL_TO_NEXT_STEP_OR_GATE`. None may support a
`COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit unless a named external human Decision Right permits
progression, whose reference is then recorded with the item left open.

## Completion Criteria

`COMPLETION_CRITERION` — S6 produces either a Decision Record for the exact escalation or a
recorded block. Complete is a coordination position, never an approval.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the matter is resolved before escalation; the owning Role withdraws the
conclusion; the escalation decision is reversed; the scope binding is revoked. The chronology, the
positions at version, the findings and the fact of cancellation survive.

## Outputs / Resulting Artifact States

| Output | State | Owner |
|---|---|---|
| Escalation artifact | `DRAFT`, or `REVIEWED` where satisfied | `role.communication_difficult_conversations_specialist` |
| Verified chronology | `FACT` per entry, with provenance | as above |
| Substantive and legal positions cited | unchanged | each owning Role |

## Authority / Review Boundary

This Workflow does not decide to escalate; does not characterise the matter legally; does not
determine breach, default or violation; does not accept the risk of escalating; does not satisfy
any review it references; does not exercise any Decision Right; and does not transmit. Its specific
leakage risks are **(a)** a chronology that quietly includes an inference, and **(b)** the lead
supplying a legal characterisation because none was available. Both produce a permanent document
that asserts something no one owns.

## Criticality Scaling

Every band carries S2, S5 and S6 in full; a formal escalation is decision-grade by construction. At
`HIGH` and `CRITICAL` the independence class of the communication review rises per
`review-profile-communication-strategy.md`, `review.evidence_integrity_provenance` becomes
mandatory for the chronology, and every position must be `APPROVED` rather than `REVIEWED`.
Criticality changes depth, not Role identity.

## Evidence / Traceability Requirements

Every chronology entry with its source; the ladder steps and dates; each position at its version
and owner; the legal characterisation or its explicit absence; the disclosure basis; the filter
scores; review findings and closure; the gate record or the block.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter authority, Role scope, gate
references or artifact ownership.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent
execution, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
