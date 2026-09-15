# Thread Diagnostics — Workflow Candidate

Status: `PROPOSED`
Template: Workflow Card Template (Phase 5 standard candidate)
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: **Thread Diagnostics**
- Workflow ID: `workflow.communication_thread_diagnostics@0.1`
- Version: 0.1 · Status: PROPOSED
- Workflow Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Coordinate a **read-only** diagnosis of an existing interaction: what the record states, what is
actually in dispute, what each issue needs, and what the exchange is structurally doing — without
drafting anything and without recommending a message. It exists as its own pattern because the
diagnosis is frequently the whole deliverable, and because drafting before diagnosing is the most
common way a difficult exchange gets worse.

## Trigger

`TRIGGER` — a request to understand an interaction; or invocation as a child of
`workflow.communication_difficult_interaction_response@0.1` at its S2–S4.

## Preconditions

- `PRECONDITION` — an interaction record exists, unedited and attributed, at `SOURCE`;
- `PRECONDITION` — a scope binding with sensitivity, residency and disclosure labels exists;
- `PRECONDITION` — the disclosure basis for reading the record is established where the record
  contains personal, privileged or restricted material.

## Scope

### Covers
- fact / assumption / interpretation separation;
- identification of the actual disagreement;
- issue decomposition and response-need classification;
- boundary-issue identification;
- bounded pattern labelling of observable conversation structure;
- escalation-, relationship- and documentation-risk assessment;
- identification of material facts that change the user's position.

### Does Not Cover
- drafting;
- recommending a specific message;
- the response-posture decision;
- any substantive conclusion;
- any assessment of a person's motives, character or mental state;
- the transmitting act.

**This Workflow writes no message and transmits nothing.** It is the one pattern in this package
with no drafting stage, deliberately.

**Rule TD-1 — no external act, no gate, and that is a positive finding.** Because nothing
transmissible is produced, no Decision Right is required **for this act**, and the diagnostic
records `human_gate_status: NOT_APPLICABLE`. That is not a statement that authority is present,
and it does not travel: where this diagnostic later feeds
`workflow.communication_difficult_interaction_response@0.1`, that workflow resolves its own gate
at its S11 independently and may not inherit `NOT_APPLICABLE` from its input (DC-7a).

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate)* | `LEAD_ROLE` | `ALWAYS` | S1–S4 | Produces a diagnostic; concludes nothing substantive and recommends no message here |
| `role.data_protection_gdpr_specialist` | `CONSULTED_ROLE` | `CONDITIONAL(the record contains personal data with no established disclosure basis)` | S1 | Owns lawful basis; advances no artifact here |
| `role.knowledge_evidence_steward` | `CONSULTED_ROLE` | `CONDITIONAL(the record's provenance is contested)` | S1 | Owns evidence provenance standards |

## Composed Workflow References

None. This Workflow composes nothing: it is the leaf pattern the others compose.

## Activated Skills / Packs

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `skill_pack.communication_difficult_conversations@0.1` *(candidate)* | `role.communication_difficult_conversations_specialist` *(candidate)* | Pending mapping record (`skill-pack.md` SP-1) |

## Inputs

| Input | Required knowledge state |
|---|---|
| Interaction record | `SOURCE`, unedited, with sender / recipient / timestamp per message |
| Stated objective, where supplied | `SOURCE` |
| Known approved positions, as references | `APPROVED` or `CANONICAL` |
| Scope, sensitivity and disclosure labels | `SOURCE` |

## Stages

### Stage `S1` — Admit the record
- **Objective:** establish that the material may be read and is what it claims to be
- **Entry Criteria:** preconditions met
- **Participating Roles:** lead `LEAD_ROLE`; conditional consulted Roles
- **Activities:** `ACTIVITY` verify provenance per message; `ACTIVITY` identify truncation, missing
  messages and unattributed forwards; `ACTIVITY` confirm the disclosure basis where personal,
  privileged or restricted material is present
- **Artifact Contributions:** admissibility note of the Conversation Diagnostic, owned by the lead
- **Knowledge-State Expectations:** the record is `SOURCE`; a paraphrase of a thread is **not** the
  thread and is `UNKNOWN`
- **Gate / Review References:** none
- **Exit Criteria:** the record is admitted, or the gaps are named
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** an absent disclosure basis is `MATERIAL_TO_NEXT_STEP_OR_GATE` — the
  instance blocks rather than reading on

### Stage `S2` — Separate evidence
- **Objective:** distinguish what the record states from what it suggests
- **Entry Criteria:** S1 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` extract stated facts with provenance; `ACTIVITY` list assumptions and
  interpretations separately; `ACTIVITY` state the user's position and the counterparty's position
  as distinct objects, labelling any reconstruction; `ACTIVITY` identify the **actual**
  disagreement, as distinct from the stated one; `ACTIVITY` flag any fact that materially changes
  the user's position
- **Artifact Contributions:** evidence sections of the Conversation Diagnostic
- **Knowledge-State Expectations:** a `FACT_CLAIM` only where `EVIDENCE` bound to the record supports it, and the record stays `SOURCE` (RC-4); everything else
  `ASSUMPTION` or `UNKNOWN`
- **Gate / Review References:** none
- **Exit Criteria:** the three categories are separated and the actual disagreement is named
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `ESCALATED`
- **Open-Item Materiality:** a position-changing fact is `MATERIAL_TO_NEXT_STEP_OR_GATE` and is
  escalated to the substantive owning Role (`role-card.md` RC-3)

### Stage `S3` — Decompose and classify
- **Objective:** give every issue a response-need classification
- **Entry Criteria:** S2 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` decompose into separable issues; `ACTIVITY` classify each as
  `RESPOND | CLARIFY | REDIRECT | IGNORE | DOCUMENT | ESCALATE`; `ACTIVITY` record the materiality
  reasoning for each `IGNORE`; `ACTIVITY` identify boundary issues
- **Artifact Contributions:** triage table of the Conversation Diagnostic
- **Knowledge-State Expectations:** classifications are `AI_SUGGESTION` until adopted by the lead
  into its `DRAFT` conclusion
- **Gate / Review References:** none
- **Exit Criteria:** every issue carries exactly one classification and a reason
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`
- **Open-Item Materiality:** an unclassified issue is `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S4` — Pattern labelling and risk
- **Objective:** describe what the exchange is doing and what it puts at risk — without describing
  anyone
- **Entry Criteria:** S3 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` apply the bounded pattern labels of
  `conversation-diagnostics-contract.md` §5, each hedged and each tied to an observable feature of
  the exchange; `ACTIVITY` detect reactivity in wording; `ACTIVITY` score escalation, relationship
  and documentation risk; `ACTIVITY` record the power / decision context — who decides, who is
  merely copied
- **Artifact Contributions:** pattern and risk sections of the Conversation Diagnostic
- **Knowledge-State Expectations:** every pattern label is `AI_SUGGESTION`. **No label may name,
  characterise or diagnose a person** (`role-card.md` limit 3)
- **Gate / Review References:** **no gate; review as RC-5 requires.** A diagnostic transmits
  nothing, so there is nothing to authorise: the diagnostic records
  `human_gate_status: NOT_APPLICABLE` with `human_gate_reason: NO_EXTERNAL_ACT_CONTEMPLATED` —
  **never** `AUTHORITY_ABSENT`, which would claim an authority is missing where none is required
  (DC-7, DC-7a). That says nothing about review. `GATE_REFERENCE`
  `review.communication_strategy@0.1` **whenever any RC-5 condition holds of the diagnostic** —
  in particular RC-5.1 where the interaction is at `HIGH` or `CRITICAL` stakes, and RC-5.2 where
  the diagnostic carries a substantive conclusion supplied by another Role. Where no RC-5 condition
  holds, the review is advisory (TD-2)
- **Exit Criteria:** labels are applied with their observable basis; three risk dimensions scored;
  and every review RC-5 triggered is `SATISFIED`, or the stage does not exit
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** an unresolved `CRITICAL_FINDING` can never support an exit
- **Mandatory at:** any band where an RC-5 condition holds (`role-card.md` RC-5, RC-5a)

## Branches / Exception Paths

- `BRANCH` **Invoked as a child.** Where composed by
  `workflow.communication_difficult_interaction_response@0.1`, the diagnostic is handed to that
  parent's S5 and this instance completes. It does not continue into drafting.
- `EXCEPTION_PATH` **Record inadmissible.** S1 blocks. A diagnosis of a record that may not be read
  is a disclosure event, not a deliverable.
- `EXCEPTION_PATH` **Drafting requested mid-instance.** The request is routed to
  `workflow.communication_difficult_interaction_response@0.1`. This Workflow does not acquire a
  drafting stage because someone asked for one.
- `EXCEPTION_PATH` **A gate is demanded anyway.** Where a caller expects a Decision Right to be
  named for the diagnosis itself, the answer is `NOT_APPLICABLE` with its reason, not a fabricated
  reference and not `AUTHORITY_ABSENT`.
- `EXCEPTION_PATH` **Psychological assessment requested.** Refused and recorded. The diagnostic
  offers the observable-behaviour labels instead, and states why.

No exception path bypasses a review or gate reference carried by the normal path.

**Rule TD-2 — producing nothing transmissible removes the gate, not the review.** An earlier
revision of this Workflow said it carried no review reference *because* it produces nothing
transmissible. Those are two different questions, and conflating them let a high-stakes read-only
diagnosis go unreviewed: a gate exists because an act needs authorising, and a review exists
because a professional conclusion needs independent checking. A diagnostic of a `HIGH` or
`CRITICAL` interaction fires **RC-5.1** and is reviewed under `review.communication_strategy@0.1`;
one that carries another Role's substantive conclusion fires **RC-5.2**; and a `NOT_APPLICABLE`
gate status sits alongside a mandatory review without tension, because they answer different
questions. Where no RC-5 condition holds, the review is advisory — this rule makes no review
mandatory that RC-5 does not trigger.

**Rule TD-3 — self-review is prohibited here as everywhere.** The producing Role is ineligible to
review its own diagnostic, and a review triggered by TD-2 is satisfied by an independent reviewer
eligible under `review-profile-communication-strategy.md` or it is not satisfied at all.

## Rework Rules

`REWORK_LOOP` — S3 → S2 where classification reveals a missed fact; S4 → S3 where a pattern label
has no observable basis. Prior versions and the reason for the loop are preserved.

## Open-Item Materiality

`MATERIAL_TO_NEXT_STEP_OR_GATE`: an absent disclosure basis; a position-changing fact not yet
escalated; an unclassified issue; a pattern label with no observable basis; and **any review RC-5
triggered that is not `SATISFIED`** (TD-2). This Workflow has no terminal gate of its own; these
items block its handoff to any parent pattern, and none is curable by a Decision Right — there is
no Decision Right here to cure anything with, because nothing is transmitted, which is precisely
why the review obligation and the gate have to be judged separately.

## Completion Criteria

`COMPLETION_CRITERION` — a Conversation Diagnostic exists in which evidence is separated, the
actual disagreement is named, every issue is classified, every pattern label is hedged and
evidenced, and the three risk dimensions are scored. Complete is a coordination position, never an
approval, and never a conclusion about anyone's intent.

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the record is withdrawn; the disclosure basis lapses; the scope binding
is revoked; the user withdraws the request. The admissibility note and any escalated
position-changing fact survive.

## Outputs / Resulting Artifact States

| Output | State | Owner |
|---|---|---|
| Conversation Diagnostic | `DRAFT`; pattern labels within it `AI_SUGGESTION` | `role.communication_difficult_conversations_specialist` |
| Admissibility note | `DRAFT` | as above |
| Escalated position-changing claims | `FACT_CLAIM` linked to its `EVIDENCE`, referred to the owning Role | the substantive owning Role |

## Authority / Review Boundary

This Workflow does not draft, does not recommend a message, does not decide a response posture,
does not conclude on any substantive domain, does not assess any person, does not satisfy any
review, does not exercise any Decision Right, and does not transmit. It **is** subject to review
where RC-5 fires (TD-2), and it satisfies none of the reviews it is subject to. Its specific
leakage risks are **a pattern label being read as a finding about a person** and **the absence of
a transmission being read as the absence of a review obligation** (TD-2): the labels describe conversation
structure, they are `AI_SUGGESTION`, and `conversation-diagnostics-contract.md` §5 fixes the
permitted set so that the vocabulary cannot drift toward diagnosis.

## Criticality Scaling

At every band the stages are identical; what deepens is evidence. At `HIGH` and `CRITICAL`, every
`FACT_CLAIM` must link to `EVIDENCE` carrying a per-message provenance reference, every pattern label must name the observable
feature it rests on, and the admissibility note must state the disclosure basis explicitly rather
than by reference. Criticality changes depth, not Role identity.

## Evidence / Traceability Requirements

Per-message provenance; the disclosure basis; the fact / assumption split with sources; the
reconstruction labels; the triage classification and reason per issue; the observable basis of
every pattern label; the risk scores and their rubric version.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter authority, Role scope, gate
references or artifact ownership — and in particular no version of this Workflow may add a
drafting stage; that would make it a different pattern.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent
execution, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
