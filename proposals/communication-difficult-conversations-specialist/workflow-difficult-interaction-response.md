# Difficult Interaction Response — Workflow Candidate

Status: `PROPOSED`
Template: Workflow Card Template (Phase 5 standard candidate)
Inherits: `standard.workflow.common_constraints@0.1`

## Identity
- Workflow Name: **Difficult Interaction Response**
- Workflow ID: `workflow.communication_difficult_interaction_response@0.1`
- Version: 0.1
- Status: PROPOSED
- Workflow Family: Communication / Stakeholder Interaction
- Governance Owner: AI-OS architecture governance
- Criticality Applicability: all bands; stages S6, S10 and S11 become mandatory at high and
  critical bands
- Inherits: `standard.workflow.common_constraints@0.1`
- Supersedes / Superseded By: none

## Purpose

Coordinate the production of a response to a difficult interaction across the Role that owns
communication strategy and the Roles that own the substantive conclusions the response carries —
so that the message is calm and clear **without** anyone's conclusion being quietly changed on the
way to being phrased well.

## Trigger

`TRIGGER` — an inbound or anticipated interaction within an assigned scope for which
`communication_conflict_score >= 55` (`trigger-routing-spec.md` §4), **or** an explicit request
for communication strategy on a contested interaction at any score.

## Preconditions

- `PRECONDITION` — an interaction record exists, unedited and attributed, at state `SOURCE`;
- `PRECONDITION` — a scope binding exists and carries sensitivity, residency and disclosure labels;
- `PRECONDITION` — the stakes band is declared;
- `PRECONDITION` — every domain the interaction touches materially has a named owning Role;
- `PRECONDITION` — any `must_not_admit` or reservation-of-rights constraint in force is stated.

## Scope

### Covers
- diagnosis of the interaction;
- response-posture decision, including non-response;
- communication strategy and draft production;
- filter application and review routing;
- identification of the human gate required before any transmission.

### Does Not Cover
- the truth of any substantive conclusion the response carries;
- adoption of an institutional position (`role.institutional_communications_editorial_specialist`,
  `role.institutional_affairs_stakeholder_specialist`);
- any legal conclusion, admission or reservation of rights (`role.legal_regulatory_lead`);
- acceptance of risk (a human Decision Right);
- the transmitting act itself;
- satisfaction of any `review.<id>` it references.

## Participating Roles

| Role ID | Participation | Activation | Stage(s) | Authority boundary note |
|---|---|---|---|---|
| `role.communication_difficult_conversations_specialist` *(candidate)* | `LEAD_ROLE` | `ALWAYS` | S1–S9, S12 | Gains no authority to conclude on any substantive domain and no authority to transmit |
| `role.legal_regulatory_lead` | `CONTRIBUTING_ROLE` | `CONDITIONAL(legal exposure material, threatened or live dispute, admission or reservation of rights in scope)` | S6, S10 | Owns the legal conclusion; gains no ownership of the communication strategy and does not become the sender |
| `role.institutional_communications_editorial_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(audience is public, media, or the message states an institutional position)` | S6, S10 | Owns editorial standards and institutional voice; gains no authority to publish |
| `role.institutional_affairs_stakeholder_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(counterparty is an institutional stakeholder)` | S6 | Owns the institutional relationship position |
| `role.data_protection_gdpr_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the draft would disclose personal data)` | S6, S10 | Owns lawful basis; gains no authority to authorise the disclosure |
| `role.people_organisation_specialist` | `CONTRIBUTING_ROLE` | `CONDITIONAL(the interaction is an employment or people matter)` | S6, S10 | Owns the people-matter conclusion |
| **Substantive Owner Slot** | `CONTRIBUTING_ROLE` | `CONDITIONAL(the response carries a conclusion in that Role's domain)` | S6 | See slot table |
| `role.enterprise_project_risk_specialist` | `CONSULTED_ROLE` | `CONDITIONAL(stakes = critical)` | S5 | Characterises risk; accepts none |

### Parameterized Role Slots

| Slot | Allowed source | Required ownership / interface condition | Permitted participation | Required artifact-ownership relationship | Phase 4 capability validation | Cardinality |
|---|---|---|---|---|---|---|
| **Substantive Owner Slot** | Approved Phase 3 Role universe | The bound Role must **already own** the conclusion the response carries, per its own Role Card `Owns` list | `CONTRIBUTING_ROLE` | Owns and continues to own the substantive conclusion; the draft cites it at its version | Direct — the bound Role's existing capability basis; the slot adds none | `0..n`, one per material domain |

Wildcards are prohibited. The slot grants no ownership. Where no approved Role owns a conclusion
the response would have to carry, the instance is `BLOCKED` — the slot is not widened and the
communication Role does not fill the gap.

## Composed Workflow References

| Referenced Workflow | Version / reference policy | Bounded purpose | Expected inputs | Expected outputs | Parent Stage(s) | Activation |
|---|---|---|---|---|---|---|
| `workflow.communication_thread_diagnostics@0.1` | pinned 0.1 | Produce the Conversation Diagnostic | Interaction record, scope binding | Conversation Diagnostic (`DRAFT`) | S2–S4 | `ALWAYS` |
| `workflow.communication_boundary_setting@0.1` | pinned 0.1 | Produce a boundary formulation where one is required | Diagnostic, constraints | Boundary text (`DRAFT`) | S7 | `CONDITIONAL(a boundary issue is classified material)` |
| `workflow.communication_refusal@0.1` | pinned 0.1 | Produce a refusal where the posture is to decline | Diagnostic, constraints | Refusal text (`DRAFT`) | S7 | `CONDITIONAL(response posture = refuse)` |
| `workflow.communication_formal_escalation@0.1` | pinned 0.1 | Produce a formal escalation where the ladder is exhausted | Diagnostic, chronology | Escalation artifact (`DRAFT`) | S7 | `CONDITIONAL(escalation recommended and accepted)` |

A reference is declarative: it names a child pattern and does not execute it. It transfers no Role
ownership, Skill compatibility, review identity, Decision Right, gate or knowledge-state
authority. Self-reference, direct or transitive, is a registry defect and none exists here.

## Activated Skills / Packs

| Capability ID | For Role | Phase 4 basis |
|---|---|---|
| `skill_pack.communication_difficult_conversations@0.1` *(candidate)* | `role.communication_difficult_conversations_specialist` *(candidate)* | Pending — the mapping record does not yet exist (`skill-pack.md` SP-1) |

A Workflow cannot make a Role compatible with a Skill that Phase 4 does not allow. Until the
mapping exists, an instance of this Workflow is not executable in a governed run.

## Inputs

| Input | Required knowledge state |
|---|---|
| Interaction record | `SOURCE` |
| Stated objective, where supplied | `SOURCE` |
| Substantive conclusions the response may carry | `DRAFT` minimum; `REVIEWED`/`APPROVED` for decision-grade |
| Approved institutional or contractual positions | `APPROVED` or `CANONICAL`, cited by reference |
| Constraint statements (`must_not_admit`, reservations) | `SOURCE` |
| Scope, sensitivity, residency and disclosure labels | `SOURCE` |

## Stages

### Stage `S1` — Establish objective
- **Stage ID:** `S1`
- **Objective:** fix what the communication is for before any wording exists
- **Entry Criteria:** preconditions met; `STATE_EXPECTATION` interaction record `SOURCE`
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` read the assignment for a stated objective; `ACTIVITY` where absent,
  infer the most likely objective and label the inference; `ACTIVITY` ask only where the ambiguity
  would materially change the response
- **Artifact Contributions:** `ARTIFACT_CONTRIBUTION` objective section of the Conversation
  Diagnostic, owned by the lead
- **Knowledge-State Expectations:** `STATE_EXPECTATION` an inferred objective is `ASSUMPTION`, never
  a `FACT_CLAIM`. The Workflow does not itself promote states
- **Gate / Review References:** none
- **Exit Criteria:** an objective is recorded, and labelled stated or inferred
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`
- **Open-Item Materiality:** an unresolved objective is `MATERIAL_TO_NEXT_STEP_OR_GATE`; the stage
  cannot exit `COMPLETE_WITH_OPEN_ITEMS` on it

### Stage `S2` — Parse the record and separate evidence
- **Objective:** establish what the material states, distinct from what it suggests
- **Entry Criteria:** S1 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` extract stated facts with provenance; `ACTIVITY` list assumptions and
  interpretations separately; `ACTIVITY` reconstruct the counterparty's position and label the
  reconstruction; `ACTIVITY` identify facts that materially change the user's position
- **Artifact Contributions:** evidence sections of the Conversation Diagnostic, owned by the lead
- **Knowledge-State Expectations:** a `FACT_CLAIM` only where `EVIDENCE` bound to the record supports it, and the record stays `SOURCE` (RC-4); everything else
  `ASSUMPTION` or `UNKNOWN`
- **Gate / Review References:** none
- **Exit Criteria:** every material claim is classified and attributed
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `ESCALATED`
- **Open-Item Materiality:** a fact in the record that changes the user's position is
  `MATERIAL_TO_NEXT_STEP_OR_GATE` and is escalated before drafting (`role-card.md` RC-3)

### Stage `S3` — Classify issues by response need
- **Objective:** decide, per issue, what the response owes it
- **Entry Criteria:** S2 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` decompose the record into separable issues; `ACTIVITY` classify each
  as `RESPOND | CLARIFY | REDIRECT | IGNORE | DOCUMENT | ESCALATE`; `ACTIVITY` record the
  materiality test result for each `IGNORE`
- **Artifact Contributions:** triage table of the Conversation Diagnostic, owned by the lead
- **Knowledge-State Expectations:** classifications are `AI_SUGGESTION` until the lead adopts them
  into its `DRAFT` conclusion
- **Gate / Review References:** none
- **Exit Criteria:** every issue carries exactly one classification and a recorded reason
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`
- **Open-Item Materiality:** an unclassified issue is `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S4` — Identify escalation, boundary, power and risk context
- **Objective:** surface what the exchange is doing structurally and what it puts at risk
- **Entry Criteria:** S3 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` detect reactivity in wording; `ACTIVITY` identify boundary issues;
  `ACTIVITY` record the power / decision context — who decides, who is copied; `ACTIVITY` apply
  the bounded pattern labels of `conversation-diagnostics-contract.md` §5; `ACTIVITY` assess
  escalation, relationship and documentation risk
- **Artifact Contributions:** risk and pattern sections of the Conversation Diagnostic
- **Knowledge-State Expectations:** every pattern label is `AI_SUGGESTION` and hedged; **no label
  describes a person**
- **Gate / Review References:** none
- **Exit Criteria:** the three risk dimensions are scored and the power context is recorded
- **Possible Outcomes:** `COMPLETE`, `ESCALATED`
- **Open-Item Materiality:** an unresolved disclosure-basis question is
  `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S5` — Decide response posture
- **Objective:** decide **whether, when and how** to respond, before deciding what to say
- **Entry Criteria:** S4 complete
- **Participating Roles:** lead `LEAD_ROLE`; `role.enterprise_project_risk_specialist`
  `CONSULTED_ROLE` at critical band
- **Activities:** `ACTIVITY` evaluate respond now / delay / do not respond / document only / move
  channel / obtain substantive review / obtain independent communication review / escalate /
  require human approval before transmission; `ACTIVITY` record the chosen posture **and the
  rejected alternatives with reasons**; `ACTIVITY` set `high_stakes_communication`
- **Artifact Contributions:** Communication Strategy, owned by the lead
- **Knowledge-State Expectations:** the strategy is `DRAFT`
- **Gate / Review References:** none yet; the gate is identified at S11
- **Exit Criteria:** a posture is recorded with reasons, and the high-stakes flag is set
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`, `ESCALATED`
- **Open-Item Materiality:** non-material open items may be carried; an unset high-stakes flag is
  `MATERIAL_TO_NEXT_STEP_OR_GATE`

### Stage `S6` — Assemble adjacent specialist input
- **Objective:** obtain, unchanged and attributed, every substantive conclusion the response will
  carry
- **Entry Criteria:** S5 complete and the posture is not "do not respond"
- **Participating Roles:** lead `LEAD_ROLE`; every conditionally activated `CONTRIBUTING_ROLE`;
  Substantive Owner Slot bindings
- **Activities:** `ACTIVITY` request each required conclusion from its owning Role; `ACTIVITY`
  record each at its version; `ACTIVITY` raise `CONFLICT_DETECTED` where two conclusions disagree
  or where a conclusion contradicts the record
- **Artifact Contributions:** each conclusion remains owned by its own Role; the strategy cites it
- **Knowledge-State Expectations:** `DRAFT` minimum; `REVIEWED`/`APPROVED` for decision-grade
- **Gate / Review References:** none
- **Exit Criteria:** every material domain has a current, attributed conclusion, or the instance is
  `BLOCKED`
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** a missing conclusion in a material domain is
  `MATERIAL_TO_NEXT_STEP_OR_GATE`; the stage cannot exit `COMPLETE_WITH_OPEN_ITEMS` on it
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

### Stage `S7` — Draft the communication strategy
- **Objective:** state the approach, channel, timing, structure and documentation posture
- **Entry Criteria:** S6 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` select techniques from `methodology-card.md` §7 and record which;
  `ACTIVITY` invoke the boundary, refusal or escalation child workflow where activated;
  `ACTIVITY` fix what will **not** be answered and why
- **Artifact Contributions:** Communication Strategy (`DRAFT`), owned by the lead
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** the strategy names posture, channel, timing, structure, non-response set and
  documentation posture
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S8` — Generate response variants
- **Objective:** produce the message, and the alternatives the user can actually choose between
- **Entry Criteria:** S7 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` produce the recommended response; `ACTIVITY` produce a shorter variant
  and a firmer variant where meaningful; `ACTIVITY` mark every absent-but-required fact as a named
  placeholder; `ACTIVITY` verify each carried conclusion is unchanged in meaning (`role-card.md`
  RC-1)
- **Artifact Contributions:** Draft Communication (`DRAFT`), owned by the lead
- **Knowledge-State Expectations:** `DRAFT`; no placeholder is silently resolved
- **Gate / Review References:** none
- **Exit Criteria:** at least the recommended response exists and carries no unsourced assertion
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`
- **Open-Item Materiality:** an unresolved placeholder is `NON_MATERIAL_TO_NEXT_STEP` for drafting
  and `MATERIAL_TO_NEXT_STEP_OR_GATE` for the terminal gate

### Stage `S9` — Apply the Communication Control Filter
- **Objective:** check the draft against the ten factors and record the scores
- **Entry Criteria:** S8 complete
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` score all ten factors; `ACTIVITY` apply the advisory release
  thresholds of `communication-control-filter.md` §5; `ACTIVITY` revise and re-score where a
  threshold is unmet; `ACTIVITY` verify no revision weakened a protection (MC-3)
- **Artifact Contributions:** filter block of the Draft Communication
- **Knowledge-State Expectations:** scores are `CALCULATION` over a recorded rubric; they are not
  evidence and they are not approval
- **Gate / Review References:** none. **The filter is not a gate**
- **Exit Criteria:** ten component scores recorded with the rubric version
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`

### Stage `S10` — Required reviews
- **Objective:** obtain the reviews the stakes and content require
- **Entry Criteria:** S9 complete
- **Participating Roles:** lead `LEAD_ROLE` (as producer, ineligible to review); conditionally
  activated `CONTRIBUTING_ROLE`s as reviewers where their own eligibility permits
- **Activities:** `ACTIVITY` route to `review.communication_strategy@0.1` **whenever any RC-5 condition holds**; `ACTIVITY` route to
  `review.high_stakes_external_communication@0.1` where the high-stakes flag is set;
  `ACTIVITY` route to `review.legal_compliance`, `review.institutional_position` and
  `review.data_protection` where their triggers hold
- **Artifact Contributions:** none; a review produces findings, not artifacts owned here
- **Knowledge-State Expectations:** a satisfied review may support `REVIEWED`; the Workflow does
  not promote it
- **Gate / Review References:** `GATE_REFERENCE` `review.communication_strategy@0.1`;
  `review.high_stakes_external_communication@0.1`; `review.legal_compliance`;
  `review.institutional_position`; `review.data_protection`
- **Exit Criteria:** every triggered review is `SATISFIED`, or the stage does not exit
- **Possible Outcomes:** `COMPLETE`, `REWORK_REQUIRED`, `BLOCKED`, `ESCALATED`
- **Open-Item Materiality:** an unresolved `CRITICAL_FINDING` can never support an exit
- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)

### Stage `S11` — Human decision gate before transmission
- **Objective:** name and obtain the human authority for the external act, or block
- **Entry Criteria:** S10 complete
- **Participating Roles:** none. **This stage has no Role participation** — a gate is not work
- **Activities:** `ACTIVITY` resolve the applicable `decision.<id>` per
  `decision-right-gap-analysis.md` §4 — for **any** release of a content item outside the entity
  under its name, including a private letter or email, that is
  `decision.external_publication`, with `decision.granting_authority_submission` or
  `decision.contract_commitment` **in addition** where the act is also a submission or a
  commitment; `ACTIVITY` where the resolution genuinely returns nothing, set
  `human_gate_status: AUTHORITY_ABSENT`, block and escalate (DG-5, DG-5a)
- **Artifact Contributions:** none
- **Knowledge-State Expectations:** unchanged. A decision does not promote the draft
- **Gate / Review References:** `GATE_REFERENCE` the resolved `decision.<id>`. The rule is one
  rule, and it does not branch on publicity: **any release of a content item outside the entity
  under the entity's name resolves `decision.external_publication`** — a public statement, a
  private letter and a one-recipient email alike. Where the act is *also* a submission, a
  disclosure, a transmission of personal data or a contractual act, the applicable Right applies
  **in addition** and never instead (`decision-right-gap-analysis.md` §4 and §5; DG-1, DG-2, DG-3)
- **Exit Criteria:** a Decision Record exists for **this** draft at **this** version, for **this**
  audience and channel — or the instance is `BLOCKED`
- **Possible Outcomes:** `COMPLETE`, `BLOCKED`, `ESCALATED`, `CANCELLED`
- **Open-Item Materiality:** every open item is `MATERIAL_TO_NEXT_STEP_OR_GATE` here
- **Mandatory at:** every band where a transmitting act occurs

### Stage `S12` — Record and close
- **Objective:** leave the record the next person will need
- **Entry Criteria:** S11 complete, blocked or cancelled
- **Participating Roles:** lead `LEAD_ROLE`
- **Activities:** `ACTIVITY` record the posture, the rejected alternatives, the triage decisions,
  the filter scores, the reviews and the gate outcome or block; `ACTIVITY` record what was
  deliberately not answered
- **Artifact Contributions:** Escalation / Documentation Recommendation where applicable
- **Knowledge-State Expectations:** `DRAFT`
- **Gate / Review References:** none
- **Exit Criteria:** the record is complete enough to reconstruct the decision
- **Possible Outcomes:** `COMPLETE`, `COMPLETE_WITH_OPEN_ITEMS`

## Branches / Exception Paths

- `BRANCH` **Non-response.** Where S5 decides not to respond, S7–S9 are skipped — there is no draft
  to produce, vary or filter — and the instance proceeds through **S6 and S10 where they apply** to
  S12. The non-response is recorded with its reason. It is a decision, not an absence, and it is a
  decision `review.communication_strategy@0.1` reviews whenever an RC-5 condition holds.
  **S10 is never skipped by this branch.** Review applicability is decided by RC-5, not by whether
  anything is transmitted (RC-5a, `workflow-thread-diagnostics.md` TD-2): a non-response that
  carries another Role's conclusion (RC-5.2), states a consequential position by staying silent
  (RC-5.3) or sits at high or critical stakes (RC-5.1) is reviewed like any other strategy. S6
  likewise runs where a substantive owner's input is needed to decide **not** to answer.
- `BRANCH` **Document only.** Where S5 decides to document without responding, S7–S8 produce an
  internal record rather than a message; **S10 applies exactly as RC-5 requires**, and S11 is not
  entered because no external act occurs. The absence of a transmission removes the *gate*, never
  the *review*.
- `BRANCH` **Channel shift.** Where S5 moves the channel, the strategy records the move and the
  draft is produced for the new channel.
- `EXCEPTION_PATH` **Material fact in a hostile message.** S2 escalates to the substantive owning
  Role before drafting. Drafting does not proceed on a superseded position.
- `EXCEPTION_PATH` **Missing substantive owner.** S6 sets `BLOCKED` and escalates to governance.
  The communication Role does not supply the conclusion.
- `EXCEPTION_PATH` **No applicable Decision Right.** S11 blocks with
  `human_gate_status: AUTHORITY_ABSENT` — after the resolution of DG-5 has been attempted and
  returned nothing, which after the §4 reassessment is a genuine last resort rather than the
  ordinary outcome for correspondence.
- `EXCEPTION_PATH` **No external act at all.** Where S5 chose non-response or document-only, S11
  is not entered and the run records `human_gate_status: NOT_APPLICABLE` with reason
  `NO_EXTERNAL_ACT_CONTEMPLATED` (DC-7).
- `EXCEPTION_PATH` **User proceeds anyway.** Where the user indicates they will transmit without
  the required review or gate, the instance records the fact and escalates. It does not assist.

**No exception path bypasses a gate or review reference carried by the normal path.** The
non-response and document-only branches do not skip S11 by exemption: they skip it because no
external act occurs, and the moment one is contemplated, S11 applies.

**Rule DIR-1 — a gate and a review are removed by different things, and only one of them by
silence.** S11 is about an external act: where none occurs, there is nothing to authorise, and
`human_gate_status` is `NOT_APPLICABLE`. S10 is about the professional quality of a conclusion the
Role owns: it is decided by RC-5, which asks what the work *carries* and what is at stake, not
whether anything leaves the entity. **No branch, posture or exception path in this Workflow skips
S10 where an RC-5 condition holds**, and an earlier revision of the non-response branch did exactly
that by skipping S6–S10 together. Self-review remains prohibited on every path (S10's participating
Roles: the lead Role is the producer and is ineligible to review).

## Rework Rules

`REWORK_LOOP` — S8 → S7 on a strategy defect; S9 → S8 on a filter failure; S10 → S7 or S8 on a
review finding; S6 → S2 where a supplied conclusion contradicts the record. Each loop preserves
the prior draft, the prior filter scores and the finding that caused the loop. **No loop erases a
prior version**, and re-entering S10 makes any earlier satisfaction `STALE`.

## Open-Item Materiality

For the terminal gate at S11, the following are `MATERIAL_TO_NEXT_STEP_OR_GATE`: an unresolved
placeholder; a missing or stale substantive conclusion; an unsatisfied triggered review; an
unresolved `CRITICAL_FINDING`; an unresolved disclosure basis; and an unresolved
`CONFLICT_DETECTED`. A material item cannot support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS`
exit: the outcome is `BLOCKED`, `REWORK_REQUIRED` or `ESCALATED`.

**Rule DIR-2 — authority and review satisfaction are separate, and neither cures the other.**
An earlier revision of this section allowed terminal progression with **any** material item
unresolved where a named external human Decision Right permitted it. That exception was too broad
in the one direction that matters: it let an exercised Right stand in for an unsatisfied review or
an unresolved `CRITICAL_FINDING`, which are not authority questions at all.

| Item | Curable by a Decision Right? |
|---|---|
| An unsatisfied triggered review | **No.** A review is satisfied by a reviewer under its Profile, and by nothing else. No Right, no Role and no combination of both substitutes (`review-profile-communication-strategy.md` §Decision Right Boundary, DG-8) |
| An unresolved `CRITICAL_FINDING` | **No.** A finding is closed by being resolved or withdrawn by the review that raised it. A decision to proceed anyway is a decision taken *with an open critical finding*, and it does not close it |
| A missing or stale substantive conclusion | **No.** The owning Role supplies it |
| An unresolved disclosure basis | **No.** It is established or the record may not be used |
| An unresolved `CONFLICT_DETECTED` | **No.** It is resolved by the owning Roles |
| An unresolved **placeholder** in the draft | **Yes, narrowly** — where the holder of the applicable Right decides, on the record, to proceed with that specific placeholder open. The reference is recorded and the item stays open |

**Terminal progression requires both, separately:** every mandatory review condition satisfied
under the approved review contract, **and** every applicable Decision Right resolved. Satisfying
one never discharges the other, and this Workflow neither decides a waiver nor asserts one was
granted.

## Completion Criteria

`COMPLETION_CRITERION` — S12 exits with the record complete and S11 having produced either a
Decision Record for the exact draft or a recorded block. **Complete is a coordination position,
never an approval.**

## Termination / Cancellation Criteria

`TERMINATION_CONDITION` — the interaction is withdrawn; the scope binding is revoked; the
disclosure basis for the record lapses; the user withdraws the request; the deadline passes and
the message is moot. What survives cancellation: the diagnostic, the recorded posture and reasons,
any findings, and the fact of cancellation.

## Outputs / Resulting Artifact States

| Output | State | Owner |
|---|---|---|
| Conversation Diagnostic | `DRAFT` | `role.communication_difficult_conversations_specialist` |
| Communication Strategy | `DRAFT` | as above |
| Draft Communication | `DRAFT`, or `REVIEWED` where a review satisfied it | as above |
| Escalation / Documentation Recommendation | `DRAFT` | as above |
| Substantive conclusions cited | unchanged | each owning Role |

## Authority / Review Boundary

This Workflow does not own any substantive conclusion; does not adopt an institutional position;
does not make any legal, financial, technical or compliance determination; does not accept risk;
does not perform or satisfy any review it references; does not exercise any Decision Right; does
not transmit anything; and does not alter the artifact ownership of any participating Role.

Its specific leakage risks, written against this pattern rather than as boilerplate: **(a)** the
lead Role improving a supplied conclusion while rephrasing it; **(b)** the filter score at S9
being read as a release approval; **(c)** the non-response branch being used to skip S11 when a
message is in fact sent later, or to skip S10 when RC-5 fires on the strategy itself (DIR-1); **(d)** a conditionally activated reviewer at S10 also having been
a contributor at S6 on the same dimension. Each is a defect, not a permitted shortcut.

## Criticality Scaling

At `LOW`/`MEDIUM`: S6 and S10 activate only where their conditions hold; the filter thresholds are
the standard-internal set. At `HIGH`: S6 and S10 are mandatory;
`review.communication_strategy@0.1` is mandatory; evidence linkage is required for every factual
assertion. At `CRITICAL`: additionally
`review.high_stakes_external_communication@0.1` is mandatory, `role.enterprise_project_risk_specialist`
is consulted at S5, and the independence class of the communication review rises per
`review-profile-communication-strategy.md`. **Criticality changes depth, not Role identity, and
does not create a second Workflow.**

## Evidence / Traceability Requirements

Traceable at completion: the interaction record and its provenance; every extracted fact's source;
the assumption register; the triage classification and reason per issue; the posture decision and
its rejected alternatives; the technique selection; every carried conclusion at its version; the
filter component scores and rubric version; review findings and their closure; the gate record or
the block; and the full rework history.

## Versioning / Change Control

Version 0.1 — initial candidate. No version change may silently alter authority, Role scope, gate
references or artifact ownership.

## Non-Runtime Statement

This card is declarative architecture. It specifies no orchestration, scheduling, queueing, agent
execution, model routing, database schema, API, interface or automation code, and binds no model,
provider or runtime technology.
