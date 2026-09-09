# Decision Record Template

Status: PROPOSED — Phase 7 standard candidate
Template Version: 0.1
Inherits: `standard.decision.common_constraints@0.1`

A **Decision Record** is evidence that one concrete human decision was made under a Decision Right in a specific context. It is an instance; the Decision Right is the type. Nineteen things must be provable.

This is a **semantic record model**. It states what a record must be able to prove, not how it is stored. No database schema, field type, identifier format or storage mechanism is specified or implied.

**A Decision Record is an immutable historical event.** It is never edited. A correction is a new Record that supersedes and links to the prior one, and both remain visible.

---

## 1. Authority

| # | Element | Notes |
|---:|---|---|
| 1 | Decision Right used | The concrete `decision.<id>` |
| 2 | Decision Right version | The version in force when the decision was made |
| 5 | Human holder identity | Recorded at runtime. **The registry never names a holder**, and no model or agent may appear here as a holder |
| 6 | Holder eligibility basis | Which eligibility class, and the authority basis relied on |
| 7 | Delegation chain or reference | Where the holder acted under delegation — the delegator, the scope and its limits |

Where cardinality is other than `SINGLE_HOLDER`, elements 5–7 are recorded **per participating holder**, and the record shows that the cardinality requirement was actually met.

## 2. Subject

| # | Element |
|---:|---|
| 3 | The exact subject — artifact, Workflow stage, Handoff, Review context |
| 4 | Subject version or reference identity, where the subject has versions |

Element 4 is what makes a decision attributable to a specific state of the world. A decision on "the model" without a version cannot later be shown to have been about what it was about.

## 3. Outcome

| # | Element |
|---:|---|
| 8 | The outcome — one of the outcomes the Right permits |
| 9 | Declared conditions, where the outcome is `APPROVE_WITH_CONDITIONS` |

Conditions recorded here **remain open and carried**. A conditional approval whose conditions are not carried is not a conditional approval; it is an unconditional one with prose attached.

## 4. Basis

| # | Element |
|---:|---|
| 10 | Open findings, risks and assumptions **known at decision time** |
| 11 | Required prerequisite reviews and gates, **and their statuses at decision time** |
| 12 | Rationale — the decision basis |
| 13 | Evidence considered |

Element 11 carries unusual weight. Where a decision permitted exceptional progression, this element shows the review standing `NOT_SATISFIED` at the moment of decision — and that is the record working correctly, not a defect in it. A record that shows only satisfied prerequisites cannot distinguish a clean decision from an exceptional one.

## 5. Time and validity

| # | Element |
|---:|---|
| 14 | Timestamp, recorded at runtime |
| 15 | Expiry or review date, where the Right declares one |

## 6. Lineage

| # | Element |
|---:|---|
| 16 | Supersedes / superseded-by linkage |

A superseded decision remains historically visible with its original content intact. Supersession replaces the operative effect; it does not remove the history.

## 7. Collective decisions

| # | Element |
|---:|---|
| 17 | Dissent or abstention, where the governance design of a collective Right uses it |

Recorded per participating holder. Where a body's constituting rules make dissent material, an unrecorded dissent makes the record incomplete.

## 8. Emergency decisions

| # | Element |
|---:|---|
| 18 | Emergency basis and retrospective obligations |

The record states the objective trigger relied on, what was bypassed, what was not, the time validity claimed, and the retrospective step owed. **A retrospective review later produces its own record; it does not amend this one.**

## 9. Separation of duties

| # | Element |
|---:|---|
| 19 | Applicable `DECISION_RIGHT_SEPARATION` relationships and compliance with them |

Where the Right declares a `SEPARATION_REQUIRED` relationship whose activation condition held, the record states **which relationships were active** and that the holder of this decision was **not** the holder of the separated one — identifying the separated decision by its own record. Where a separation was active and no separately eligible holder existed, the decision was not validly made and there is nothing to record: scarcity does not relax authority.

Where the relationship is `SAME_HOLDER_PERMITTED` and one human held both, the record says so explicitly rather than leaving it to be inferred from silence.

---

## What a Decision Record is not

- **not the Decision Right** — the Right is reusable, the Record is one event;
- **not a satisfied gate by its own existence** — the gate is satisfied only where the Record carries a permitted outcome whose declared effect satisfies it, under a valid holder and cardinality;
- **not a resolution of anything it names** — findings, risks and unknowns recorded in element 10 remain open after the decision;
- **not editable** — corrections supersede.

## Non-Runtime Statement

This template is declarative architecture. It specifies no database schema, field types, identifier formats, storage, retention mechanism, API, interface, signature scheme, identity system or authentication mechanism, and binds no person, organisation, job title, provider or runtime identity.
