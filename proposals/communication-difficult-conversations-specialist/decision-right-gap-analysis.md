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

| Act | Applicable `decision.<id>` | Register status | Assessment |
|---|---|---|---|
| TA-1 | `decision.external_publication` | **Carded exemplar** | **Covered.** Its subject is exactly this act. Use it |
| TA-2 | `decision.granting_authority_submission` | **Carded exemplar** | **Covered.** Use it |
| TA-3 | `decision.disclosure_authorisation` | Candidate, uncarded | **Covered in principle, not yet carded.** Reference it; treat an uncarded Right as unavailable until carded (§6) |
| TA-4 | `decision.external_data_transmission`; `decision.lawful_basis_adoption` for the basis | Candidates, uncarded | As TA-3 |
| TA-5 | `decision.contract_commitment` | **Carded exemplar** | **Covered.** A message that admits, waives, varies or accepts is a contractual act, whatever it looks like |
| TA-6 | `decision.legal_filing_or_representation` | Classified **"LIKELY DECISION RIGHT — NEEDS BOUNDARY REFINEMENT"**; boundary against `decision.formal_legal_opinion` unclear | **Not usable as a gate today.** Route through `role.legal_regulatory_lead` and treat as §6 until the boundary is drawn |
| **TA-7** | **none** | — | **This is the gap.** See §5 |

**Rule DG-1 — the act, not the artifact, selects the Right.** A "message" is not a category of
authority. What the message *does* is. A friendly-looking email that accepts a revised term is
TA-5 and is gated by `decision.contract_commitment`; a hostile-looking email that accepts nothing
may be TA-7. The reviewer at `review.high_stakes_external_communication@0.1` checks precisely this
mapping (§Review Scope, "gate identification").

**Rule DG-2 — several acts may be present at once.** A single message can be TA-4 and TA-5. Every
applicable Right applies; the least burdensome one is not selected.

## 5. The residual gap — TA-7

**What is genuinely uncovered:** a private, high-stakes communication that leaves the entity and
creates positional, relational, reputational or precedent exposure, while being
- not published (so not TA-1),
- not a submission to a granting authority (not TA-2),
- not a disclosure of controlled information (not TA-3),
- not a transmission of personal data (not TA-4),
- not a contractual act (not TA-5),
- not a legal filing or formal representation (not TA-6).

`decision.external_publication` does not stretch to cover it. Its subject is release **under the
entity's name to an audience outside the entity**, and its holder-eligibility and irreversibility
reasoning are built around content becoming publicly available. A final warning to one partner is
neither published nor available; treating it as publication would both distort that Right and
route the decision to a holder chosen for a different reason.

**Candidate, and its status:**

- Candidate ID: `decision.external_high_stakes_communication_send`
- Status: **`PROPOSED` and `BLOCKED`**
- Decision Class (proposed): `COMMITMENT_DECISION`
- Proposed Decision Subject: transmission of **one** communication, at a stated version, to a
  stated recipient set through a stated channel, where a high-stakes condition of
  `trigger-routing-spec.md` §5 holds and no other applicable Right covers the act
- Proposed Decision Effect: the communication leaves the entity and becomes part of the record
  between the parties. Costly to reverse; a correction is a **new** act

**Rule DG-3 — this candidate confers no authority and is not exercisable.** It is recorded so the
gap is visible, exactly as the Phase 7 universe records
`decision.cancellation_or_termination` without carding it. It must not be referenced as a
satisfied gate, must not be cited in a Decision Record, and must not be treated as approved because
it is written down. Carding it requires Phase 7 change control, which must settle at minimum:
holder eligibility class; cardinality; delegation policy; its `DECISION_RIGHT_SEPARATION`
relationships against `decision.external_publication`, `decision.contract_commitment` and
`decision.disclosure_authorisation`; and the boundary that keeps it from becoming a general
permission to send things.

**Rule DG-4 — the gap is not closed by this package.** Until Phase 7 cards a Right for TA-7, every
TA-7 act is handled under §6.

## 6. Fail-closed rule

**Rule DG-5 — missing authority fails closed.** Where an intended external act resolves to no
carded, applicable Decision Right, the act is:

1. **blocked** — the run does not proceed to transmission;
2. posture **`AUTHORITY_ABSENT`** — distinct from `GATE_UNSATISFIED`, because the problem is not
   that someone has not yet decided, it is that no one holds the authority to decide;
3. **escalated** to governance, naming the act, the recipient set, the channel, and the reason no
   Right applies;
4. **recorded** — `human_gate_reference` carries the literal `AUTHORITY_ABSENT`
   (`conversation-diagnostics-contract.md` DC-7), never `null` and never a description.

**Rule DG-6 — absence of prohibition is not permission.** "No Right forbids this message" is not a
basis for sending it. This is the specific failure mode the Role's authority limit 7 and the
high-stakes review's `CRITICAL_FINDING` list both exist to catch.

**Rule DG-7 — an uncarded candidate Right is not available.** TA-3, TA-4 and TA-6 resolve to
identifiers the Phase 7 universe has **not** carded. Until they are carded, an act that needs one
of them is in the same position as TA-7: blocked, `AUTHORITY_ABSENT`, escalated. Naming a candidate
identifier in a gate field does not make it exercisable, and the review checks for exactly this
substitution.

**Rule DG-8 — no Role and no review may supply the missing authority.** Not the communication Role,
not the owning substantive Role, not a satisfied review, not a high filter score, not urgency, not
seniority, and not the fact that the deadline has passed. A blocked act stays blocked until a human
holding a carded, applicable Right decides it.

## 7. What this package deliberately does not do

| Tempting shortcut | Why it is refused |
|---|---|
| Read `decision.external_publication` broadly enough to cover TA-7 | Widening a carded Right's subject is a Phase 7 change, made here silently |
| Cite `decision.external_commercial_communication` or `decision.institutional_position_release` as the gate | The Phase 7 universe classified both as role responsibility, not authority. Citing them would manufacture a gate out of a recorded finding that none exists |
| Card `decision.external_high_stakes_communication_send` in this package | Carding is Phase 7 change control. A proposal that cards its own Right has approved itself |
| Treat `review.high_stakes_external_communication@0.1` as the gate | A review informs a decision and never is one. It cannot be set `SATISFIED` by any Right, and satisfying it authorises nothing |
| Let the user's own authority stand in | The user's ability to press send is a credential, not authority (CREDENTIAL != HUMAN AUTHORITY) |

## 8. Summary for a governance reviewer

- **Covered and usable today:** TA-1 (`decision.external_publication`), TA-2
  (`decision.granting_authority_submission`), TA-5 (`decision.contract_commitment`) — all carded.
- **Covered in principle, blocked in practice** pending carding: TA-3, TA-4, TA-6.
- **Uncovered:** TA-7, with `decision.external_high_stakes_communication_send` recorded as a
  `PROPOSED` and `BLOCKED` candidate.
- **Net effect on the Role:** it can produce drafts for every act, and it can transmit none of
  them. Where a carded Right applies, the human holding it decides. Where none applies, the act is
  blocked with posture `AUTHORITY_ABSENT` and escalated.

That is the intended behaviour, and it is a real functional limit: built exactly to this package,
the capability would draft a final warning to a partner and then be unable to send it until Phase 7
acts. Stating that plainly is better than the alternative, which is a Right invented by a proposal.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no database schema, API, interface,
notification, workflow runtime, model routing, agent execution, signature, identity,
authentication or authorisation mechanism, and binds no person, organisation, job title, provider
or runtime identity.
