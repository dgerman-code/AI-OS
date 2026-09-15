# Decision Right Gap Analysis

Status: `PROPOSED`
Version: 0.1
Governance Owner: AI-OS architecture governance

> **This document creates no Decision Right, maps none, widens none and approves none.** It
> analyses what the approved and candidate registers already cover, identifies one residual gap,
> and records a blocked candidate for that gap. Everything here is a finding, not an authority.

## 1. The question

The Role produces drafts. Some of those drafts, when sent, are governed external acts. Which
`decision.<id>` authorises the sending — and what happens when none does?

## 2. Method

The analysis reads `decisions/master-decision-right-universe.md` and the carded exemplars in
`decisions/exemplars/`, and classifies each candidate by whether it covers a transmitting act this
Role's outputs can perform. **Nothing upstream is renamed, merged, reclassified or normalised
here.** Where the Phase 7 universe has already classified an identifier, that classification is
reported as it stands.

Three registry facts govern the result and are stated before the analysis, because they are what
makes the conclusion narrow:

1. `decision.external_publication` is a **carded exemplar** (✎). Its Decision Subject is the
   release of one content item, at a stated version, to an audience outside the entity, **under the
   entity's name**.
2. `decision.disclosure_authorisation` and `decision.external_data_transmission` are **candidate
   Rights in the Phase 7 universe**, not carded exemplars.
3. `decision.external_commercial_communication`, `decision.institutional_position_release`,
   `decision.external_reporting_release`, `decision.workforce_communication` and
   `decision.institutional_engagement` are classified by the Phase 7 universe as **"ROLE
   RESPONSIBILITY IN DISGUISE"** — an act the owning Role performs under its own Role Card, gated
   where external by a Right that already exists. **They are not Rights**, and this package must
   not reference them as gates.

That third fact is the one that closes off the easy answer. A reader looking for "a Right for
sending a communication" will find several plausible identifiers in the register; five of them are
recorded findings that no such separate authority exists.

## 3. The transmitting acts this Role's outputs can perform

| # | Act | Example |
|---:|---|---|
| TA-1 | Publication under the entity's name | A public statement, a holding line, a press response |
| TA-2 | Submission to a granting authority | A response to a clarification request or an audit finding |
| TA-3 | Disclosure of controlled information to a named recipient class | A chronology containing third-party confidential material |
| TA-4 | Transmission of personal data outside the entity | A grievance response quoting employee data |
| TA-5 | A contractual act — admission, waiver, variation, notice, acceptance | A letter that concedes a delay, or accepts a revised term |
| TA-6 | A legal filing or formal representation | A pre-action response, a formal complaint |
| TA-7 | **Private high-stakes correspondence that is none of the above** | A final warning to a partner; a firm reply to a hostile counterparty; a board-level disagreement letter — carrying no admission, no controlled information, no personal data, and not published |

## 4. Coverage map

**The approved subject, read exactly as written.** `decision.external_publication`'s Decision
Subject is:

> Release of **one** content item, at a stated version, to an audience outside the entity, under
> the entity's name.

Four elements, and no fifth. There is **no** element requiring the audience to be the public, the
content to be generally available, or the channel to be a published one. "An audience outside the
entity" is satisfied by one counterparty as readily as by a readership, and the Decision Effect —
"makes the content externally available and attributes it to the entity" — describes a letter to a
partner as accurately as a press release. Its irreversibility reasoning applies identically:
retraction removes availability, not the fact of having sent.

| Act | Applicable `decision.<id>` | Register status | Assessment |
|---|---|---|---|
| TA-1 | `decision.external_publication` | **Carded** | **Covered.** The canonical case |
| TA-2 | `decision.external_publication` **and** `decision.granting_authority_submission` | **Both carded** | **Covered.** A submission is also a release outside the entity under its name; the submission Right applies in addition, not instead |
| TA-3 | `decision.external_publication` | **Carded** | **Covered** for the release itself. `decision.disclosure_authorisation` would add a further control over *which* recipient class may receive controlled information; it is a Phase 7 candidate and is **not carded**, so it adds no gate today — see §6 |
| TA-4 | `decision.external_publication` | **Carded** | **Covered** for the release itself. `decision.external_data_transmission` and `decision.lawful_basis_adoption` would add further controls; both uncarded, as above |
| TA-5 | `decision.external_publication` **and** `decision.contract_commitment` | **Both carded** | **Covered.** A message that admits, waives, varies or accepts is both a release and a contractual act; **both** Rights apply |
| TA-6 | `decision.external_publication` | **Carded** | **Covered** for the release itself. `decision.legal_filing_or_representation` is classified "LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT" and is not usable as a gate; route the substance through `role.legal_regulatory_lead` |
| **TA-7** | **`decision.external_publication`** | **Carded** | **Covered.** See §5 |

**Rule DG-1 — the act, not the artifact, selects the Right.** A "message" is not a category of
authority. What the message *does* is. Several acts may be present at once, and then **every**
applicable Right applies; the least burdensome one is not selected.

**Rule DG-2 — additional Rights add, they never substitute.** Where an act is both a release and a
submission, or both a release and a contractual commitment, satisfying one Right does not satisfy
the other, and the review at `review.high_stakes_external_communication@0.1` checks that the
identified set matches what the message actually does.

**Rule DG-2a — publicity is not a discriminator, and no document may make it one.** Any release of
a content item, at a stated version, to an audience outside the entity, under the entity's name
resolves **`decision.external_publication`** — a public statement, a private letter and a
one-recipient email alike. No active statement in this package may route a private communication to
a different Right *instead of* the release Right on the grounds that it is private, offer a
publicity-conditioned split between two Rights, or make the release Right conditional on the
audience being a readership. Submission,
disclosure, transmission and commitment Rights apply **in addition** under DG-2 where the act is
also one of those things.

An earlier revision of two documents — the primary workflow's gate stage and the
communication-strategy Review Profile's Decision Right Boundary — carried exactly that split. It
was the same error §5 corrects, surviving in a second location: a fifth element, publicity, read
into a subject that has four.

## 5. TA-7, reassessed against the approved wording

**The prior reading was wrong, and this is the correction.** Revision 1 of this package concluded
that a private, high-stakes communication fell **outside** `decision.external_publication` because
it is "neither published nor available", and on that basis recorded a candidate Right
`decision.external_high_stakes_communication_send`. The independent review found the error, and it
is a plain one: **the approved subject contains no publicity element.** The reasoning added a
fifth condition — general availability — that the card does not state, and then found a gap
created entirely by that addition. The word "publication" in the Right's *name* was read as if it
were part of its *subject*; it is not, and a Right's name is not its scope.

Read as written, a final warning to a partner, a firm reply to a hostile counterparty and a
board-level disagreement letter are each **one content item, at a stated version, released to an
audience outside the entity, under the entity's name**. They are within the approved subject.

**Consequences, applied throughout this package:**

| # | Consequence |
|---:|---|
| 1 | **`decision.external_high_stakes_communication_send` is `WITHDRAWN_FROM_CURRENT_PACKAGE`.** It confers no authority, is not proposed, is not a candidate, and must not be referenced as a gate. It is recorded here only so the withdrawal is visible rather than silent |
| 2 | TA-7 resolves to `decision.external_publication`, like every other release |
| 3 | The fail-closed path of §6 remains in force and becomes what it should always have been: a genuine last resort, not the ordinary outcome for private correspondence |
| 4 | `role-card.md` §Human Decision Gates, `evaluation-spec.md` E23 and PC-2, `examples.md` and `self-check.md` are corrected to resolve the applicable approved Right first |

**Rule DG-3 — a Right's name is not its subject.** The only text that bounds a Right is its
Decision Subject and the clauses of its own card. Reading scope out of a title is how a package
invents a gap, and inventing a gap is how a package invents a Right.

**Rule DG-4 — this package proposes no Decision Right.** None is created, mapped, widened,
exercised or approved here. Amending the approved Phase 7 card is not attempted, and nothing above
reinterprets it beyond its written wording — the correction runs in the direction of reading
*less* into it, not more.

### 5.1 Is any residual gap left?

Examined honestly, and the answer is **no gap in send authority**. Two narrow observations remain,
and neither is a missing Right:

1. **An oral statement in a meeting** is not "one content item at a stated version", so the
   release Right does not attach to the speaking itself. This is not a gap: any commitment made
   orally is governed by the Right that governs that commitment — in practice
   `decision.contract_commitment` — and a communication package cannot fix the fact that speech is
   not a versioned artifact. `workflow-meeting-preparation.md` states this in its exception paths.
2. **Three adjacent controls are uncarded** — `decision.disclosure_authorisation`,
   `decision.external_data_transmission` and `decision.legal_filing_or_representation`. Their
   absence does not leave any act **ungated**, because the release Right gates the act; it leaves
   those acts with **fewer** controls than a mature register would apply. That is an observation
   for Phase 7, recorded in `governance-decision-note.md`, not a gap this package fills.

## 6. Fail-closed rule

**Rule DG-5 — resolve first, then fail closed.** The order is not optional: an applicable approved
Right is **searched for and resolved** before any fail-closed finding is recorded. Only where the
search genuinely returns nothing is the act:

1. **blocked** — the run does not proceed to transmission;
2. posture **`AUTHORITY_ABSENT`** — distinct from `GATE_UNSATISFIED`, because the problem is not
   that someone has not yet decided, it is that no one holds the authority to decide;
3. **escalated** to governance, naming the act, the recipient set, the channel, and the reason no
   Right applies;
4. **recorded** — `human_gate_status` carries the literal `AUTHORITY_ABSENT`
   (`conversation-diagnostics-contract.md` DC-7).

**Rule DG-5a — `AUTHORITY_ABSENT` is not the resting state.** After the §4 reassessment, every
transmitting act this Role's outputs can perform resolves to a carded Right. A package that
reported `AUTHORITY_ABSENT` on ordinary correspondence would be crying wolf, and a system that
cries wolf on every send teaches its users to click through the one that matters.

**Rule DG-5b — no external act, no gate.** Where nothing transmissible is produced — a read-only
diagnosis — the status is `NOT_APPLICABLE` with reason `NO_EXTERNAL_ACT_CONTEMPLATED`. It is not a
finding that authority is present; it is a finding that none is required **for this artifact**, and
any later workflow that contemplates a transmission resolves its own Right independently.

**Rule DG-6 — absence of prohibition is not permission.** "No Right forbids this message" is not a
basis for sending it.

**Rule DG-7 — an uncarded candidate Right is not available.** Naming a candidate identifier in a
gate field does not make it exercisable. Under the §4 reassessment this no longer blocks any act,
because the release Right carries the gate; it means only that the adjacent controls those
candidates would add are not yet in force.

**Rule DG-8 — no Role and no review may supply a missing authority.** Not the communication Role,
not the owning substantive Role, not a satisfied review, not a high filter score, not urgency, not
seniority, and not the fact that the deadline has passed.

## 7. What this package deliberately does not do

| Tempting shortcut | Why it is refused |
|---|---|
| Read a publicity element into `decision.external_publication` to preserve the earlier gap | That is what produced the error. The subject has four elements and the analysis now reads exactly those |
| Keep `decision.external_high_stakes_communication_send` "just in case" | A candidate Right with no demonstrated gap is an authority looking for a justification. It is withdrawn |
| Cite `decision.external_commercial_communication` or `decision.institutional_position_release` as the gate | The Phase 7 universe classified both as role responsibility, not authority. Citing them would manufacture a gate from a recorded finding that none exists |
| Treat `review.high_stakes_external_communication@0.1` as the gate | A review informs a decision and never is one |
| Let the user's own authority stand in | The ability to press send is a credential, not authority (CREDENTIAL != HUMAN AUTHORITY) |
| Report `AUTHORITY_ABSENT` rather than do the resolution work | DG-5a |

## 8. Summary for a governance reviewer

- **Covered by a carded Right — all seven acts.** `decision.external_publication` gates every
  release of a content item, at a stated version, to an audience outside the entity under the
  entity's name — TA-7 included. `decision.granting_authority_submission` and
  `decision.contract_commitment` apply **in addition** where the act is also a submission or a
  commitment.
- **Withdrawn:** `decision.external_high_stakes_communication_send`. The gap it was proposed to
  fill did not exist; it was produced by reading a publicity element into an approved subject that
  does not contain one, and the independent review was right to reject it.
- **Uncarded adjacent controls:** `decision.disclosure_authorisation`,
  `decision.external_data_transmission`, `decision.legal_filing_or_representation`. Their absence
  leaves no act **ungated**; it leaves three acts with fewer controls than a mature register would
  apply. Recorded for Phase 7 in `governance-decision-note.md`, not filled here.
- **Net effect on the Role:** it can produce drafts for every act and transmit none of them. For
  every one of those acts, a human holding a carded Right decides.

The correction narrows this package's claims rather than widening them: one fewer proposed Right,
one fewer asserted gap, and a fail-closed path that now means what it says because it is no longer
the ordinary outcome for ordinary correspondence.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no database schema, API, interface,
notification, workflow runtime, model routing, agent execution, signature, identity,
authentication or authorisation mechanism, and binds no person, organisation, job title, provider
or runtime identity.
