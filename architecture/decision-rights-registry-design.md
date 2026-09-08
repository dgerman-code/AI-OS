# AI-OS Decision Rights Registry Design

Status: PROPOSED — Phase 7 architecture candidate
Version: 0.1
Depends on: approved Phase 3 Role Registry, Phase 4 Skill Registry, Phase 5 Workflow Registry, Phase 6 Handoff & Review architecture

## Purpose

Every phase since Phase 3 has written `decision.<id>` into its cards and defined none of them. Phase 5 said a Workflow may reference a gate and never satisfy it. Phase 6 said a Review may reference a gate and never make the decision it informs. Both were right, and both left the same hole: **95 distinct `decision.<id>` references now exist across the approved registries, and not one of them says who may decide, what deciding does, or what makes a decision valid.**

Phase 7 fills that hole. It defines the reusable governance model behind those references — and nothing else. It binds no person, no organisation, no job title and no system.

## The separation this phase must preserve

```
ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != DECISION RECORD != MODEL != RUNTIME
```

| Object | Owns |
|---|---|
| **Role** | professional methodology, scope, conclusions, artifact interfaces |
| **Workflow** | progression coordination; references gates |
| **Handoff** | governed transfer without ownership transfer |
| **Review Profile** | review requirements and satisfaction, without approval authority |
| **Decision Right** | a reusable definition of **one bounded human authority to make one class of decision** |
| **Decision Record** | evidence that **one concrete human decision was made** under a Decision Right in a specific context |
| **Model / runtime** | implementation, out of scope |

### A Decision Right is not

a Role; a reviewer; a Workflow stage; a business-rule engine; a model; a generic "approver" label; or permission to decide anything outside its declared scope.

### The Right is not the Record

A Decision Right is a **type**. A Decision Record is an **instance**. The Right says *this class of decision exists, this is who may make it and this is what making it does*. The Record says *this decision was made, on this subject, by this holder, on this basis*. Confusing them produces the most common governance failure in practice: a registry entry treated as though its existence were the decision.

---

## 1. Decision Right identity

```
decision.<stable_snake_case_name>
```

The ID must not contain a human name, an organisation, client or project, a provider or model, an implementation technology, a version number, or a transient job title.

Every Decision Right declares a bounded **decision subject** — what it decides about — and a bounded **decision effect** — what deciding does. A Right whose subject is "the project" or whose effect is "approval" is not bounded and is defective.

---

## 2. Decision classes

Eight classes. `decision.approve_anything` is not a pattern this registry admits.

| Class | Meaning |
|---|---|
| `PROGRESSION_DECISION` | Permits or refuses movement to a next governed state or stage despite conditions requiring human authority |
| `APPROVAL_DECISION` | Approves a bounded artifact or action **for a declared purpose** |
| `COMMITMENT_DECISION` | Creates an external, financial, contractual, regulatory, submission, publication or release commitment |
| `RISK_ACCEPTANCE_DECISION` | Accepts a declared residual risk or unresolved issue within bounded authority |
| `EXCEPTION_DECISION` | Permits a governed exception **without rewriting the underlying rule** or falsely satisfying an unsatisfied review |
| `EMERGENCY_DECISION` | Permits a time-critical exceptional act under explicit emergency conditions and mandatory retrospective controls |
| `REJECTION_DECISION` | Refuses approval, progression or commitment, and may route to rework or termination |
| `CANCELLATION_OR_TERMINATION_DECISION` | Cancels a Workflow, project or action, or terminates a pending governed path |

A Decision Right declares exactly one primary class. Where a Right's outcomes span classes — a progression Right whose `REJECT` outcome routes to termination — the secondary effect is declared in the effect table, not by claiming two classes.

---

## 3. Decision effect model

Every Decision Right states what each permitted outcome **does**. Six outcome values exist; **no Right must permit all six**, and a Right that permits an outcome without stating its effect is defective.

| Outcome | Meaning |
|---|---|
| `APPROVE` | The decision is made positively as scoped |
| `REJECT` | Refused |
| `APPROVE_WITH_CONDITIONS` | Positive, subject to conditions that **remain open and carried** |
| `DEFER` | No decision made; the gate remains unsatisfied |
| `ESCALATE` | Referred to a higher or different authority; no decision made here |
| `CANCEL` | The governed path is stopped |

For each permitted outcome a card declares the effect on: Workflow progression; Handoff eligibility; external action or commitment; Review status; knowledge state; whether conditions and open items remain active; and whether expiry or re-decision is required.

### Mandatory boundaries

These five hold for every Decision Right in the registry:

1. **A Decision Right may permit progression while a Review remains `NOT_SATISFIED`** — where that Right explicitly governs exceptional progression. **It must not relabel the review `SATISFIED`.** Phase 6 fixed the review half of this rule; Phase 7 fixes the decision half.
2. **A Decision Right may accept risk. It does not erase the risk or the finding.**
3. **A Decision Right may approve an artifact for a bounded use. It does not make the artifact `CANONICAL`** unless a separate Right explicitly governs canonical promotion.
4. **A Decision Right cannot create professional conclusions** outside upstream Role ownership. Approving a feasibility position is not concluding on feasibility.
5. **A Decision Right does not rewrite source facts, assumptions, findings, `UNKNOWN` or `CONFLICT_DETECTED` states.** Authority acts on what to *do* about the world; it does not act on what the world *is*.

---

## 4. Holder eligibility model

Phase 7 defines **eligibility classes**, never holders. Who actually holds a Right in a given organisation is assignment data the runtime records later.

| Class | Authority basis |
|---|---|
| `DESIGNATED_HUMAN_AUTHORITY` | An individual explicitly designated for this decision class in the governing arrangement |
| `GOVERNANCE_BODY_AUTHORITY` | A constituted body acting as a body — board, committee, steering group |
| `EXECUTIVE_AUTHORITY` | Executive management authority over the organisation or unit |
| `FUNCTIONAL_AUTHORITY` | Authority derived from a named function — finance, legal, security, release — within its own domain |
| `PROJECT_OR_PROGRAMME_SPONSOR_AUTHORITY` | Sponsor authority over a specific project or programme |
| `LEGAL_ENTITY_SIGNATORY_AUTHORITY` | Authority to bind the legal entity externally |

### Mandatory eligibility rules

1. **Role competence does not create Decision Right authority.** Knowing how to do the work is not authority to commit to it.
2. **Being Workflow `LEAD_ROLE` does not create approval authority.**
3. **Being a reviewer does not create Decision Right authority** — Phase 6 already denies reviewers approval power; this states the converse.
4. **Owning an artifact does not automatically create external commitment authority.** The Role that owns the model does not thereby bind the entity to it.
5. A Right may require **one or more authority bases** — legal, organisational, financial, programme, governance, security, release or sponsor.
6. A Right states whether **one holder suffices or a multi-human governance act is required.**
7. Holder identity is runtime and assignment data; the registry defines eligibility rules only.
8. **If no eligible holder is available, the decision is unmade and the gate unsatisfied.** Authority is never inferred from convenience, urgency or absence.

---

## 5. Cardinality and collective authority

Every Right declares its cardinality:

| Cardinality | Meaning |
|---|---|
| `SINGLE_HOLDER` | One eligible holder decides |
| `MULTI_HOLDER_ALL_REQUIRED` | Every named eligibility class must decide positively |
| `MULTI_HOLDER_THRESHOLD` | A declared threshold of eligible holders must decide positively |
| `GOVERNANCE_BODY_DECISION` | A constituted body decides as a body under its own constituting rules |

Threshold semantics are declared — *how many, of which eligibility classes, and whether any class is mandatory within the threshold*. No voting mechanism, tally procedure or runtime is implemented here.

Rules:

- **Cardinality cannot be bypassed by delegation** unless the Right explicitly permits it.
- **One person cannot count twice under two labels** in the same decision instance. Holding two eligible classes makes someone eligible twice over, not two holders.
- **A governance-body decision is not equivalent to one member acting alone**, however senior.
- **Absent required participants means the decision is not made** — not made by the remainder, and not made provisionally.

---

## 6. Delegation model

Every Right declares one delegation policy:

| Policy | Meaning |
|---|---|
| `NON_DELEGABLE` | The authority cannot be passed on |
| `DELEGABLE_WITHIN_ELIGIBILITY` | May be delegated to another holder of an eligible class |
| `DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS` | Delegable subject to stated further limits |

A delegation declaration states: who may delegate, by eligibility class; who may receive, by eligibility class; the scope of the delegation; its time and context limits; whether re-delegation is prohibited or allowed; the evidence required; and revocation semantics.

### Mandatory delegation rules

1. Delegation transfers **only the declared Decision Right scope** — never Role authority or professional ownership.
2. **Delegation never widens the subject or effect.** A delegate cannot decide more than the delegator could.
3. **Delegation cannot bypass cardinality.**
4. The chain is bounded: **re-delegation is prohibited by default** and permitted only where explicitly stated.
5. Expiry or revocation invalidates **future** exercise. It does not erase historically valid decisions.
6. **A revoked delegation does not automatically reverse a previously valid decision.**
7. **Emergency delegation must not become standing authority by use.** Repetition is not ratification.
8. The runtime records delegation instances later; Phase 7 defines the semantics.

---

## 7. Revocation and supersession

Four distinct things, routinely conflated:

| Concept | Meaning |
|---|---|
| **Holder / delegation revocation** | Removes the future ability to exercise authority |
| **Decision supersession** | A later valid decision replaces the operative effect of an earlier one |
| **Decision reversal** | An earlier decision is undone, where a Right explicitly permits reversal |
| **Artifact / workflow supersession** | An upstream object version becomes obsolete |

Rules:

- **Revoking a holder does not erase the audit trail.**
- **A superseded decision remains historically visible** with its original content intact.
- **Reversal requires a Right whose scope permits it** — it is not an implied power of the Right that made the original decision.
- **A decision cannot be silently edited after the fact.** Correction is a **new Decision Record linked to the prior record**, never a mutation of it.

---

## 8. Decision evidence model

A Decision Record must later be able to prove eighteen things. This is a **semantic record model**, not a database schema: it says what must be provable, not how it is stored.

| # | Element |
|---:|---|
| 1 | The `decision.<id>` used |
| 2 | The Decision Right version in force |
| 3 | The exact subject — artifact, Workflow, Handoff, Review context |
| 4 | Subject version or reference identity where applicable |
| 5 | Human holder identity (runtime) |
| 6 | Holder eligibility basis |
| 7 | Delegation chain or reference, where applicable |
| 8 | The decision outcome |
| 9 | Declared conditions |
| 10 | Open findings, risks and assumptions **known at decision time** |
| 11 | Required prerequisite reviews and gates, **and their statuses** |
| 12 | Rationale / decision basis |
| 13 | Evidence considered |
| 14 | Timestamp (runtime) |
| 15 | Expiry or review date where applicable |
| 16 | Supersedes / superseded-by linkage |
| 17 | Dissent or abstention, where collective authority uses it |
| 18 | Emergency basis and retrospective obligations, where relevant |

Element 11 is the one that makes exceptional progression auditable: a record that shows a gate satisfied while its prerequisite review stood `NOT_SATISFIED` is not a defect in the record — it is the record doing its job.

---

## 9. Gate satisfaction semantics

```
HUMAN_GATE_REFERENCE  ->  decision.<id>  ->  Decision Record
```

A human gate is satisfied **only when all five hold**:

1. the referenced Decision Right exists;
2. an eligible holder made the decision and the cardinality requirement is met;
3. the prerequisites the Right requires are met, **or** an allowed exceptional path is explicitly used;
4. the required evidence is present;
5. the Decision Record contains a **permitted outcome whose declared effect satisfies that gate.**

### What does not satisfy a gate

- **"Decision requested" is not a satisfied gate.** A pending decision is an unsatisfied one.
- **"A decision meeting happened" is not a satisfied gate.** A discussion is not a record.
- **"An approval email exists" is not a satisfied gate** unless it is attributable to the Decision Right and carries the required evidence. Correspondence is not authority.
- **`DEFER`, `ESCALATE` and `REJECT` do not satisfy a positive progression gate** unless the Right explicitly declares another effect.
- **Missing or invalid authority means the gate is unsatisfied** — not provisionally satisfied, not satisfied pending confirmation.

---

## 10. Exceptional progression

This closes the forward reference Phase 5 and Phase 6 both left open.

A named external `decision.<id>` may permit progression with an unresolved item or review **only if all eight hold**:

1. the Decision Right **explicitly includes that exception in its scope**;
2. the unresolved item **remains visible and open**;
3. **Review status remains unchanged** — `NOT_SATISFIED`, open finding, whatever it was;
4. the Decision Record **names the unresolved item, finding or risk**;
5. consequences and conditions are recorded;
6. an expiry or revisit trigger is declared where applicable;
7. the downstream Workflow or Handoff **receives the open-item carry**;
8. the decision **does not claim the underlying issue is resolved.**

**A Decision Right may authorise progression. It may not authorise fictional resolution.** The distinction is the whole content of this section: moving forward with a known problem is a legitimate governed act; declaring the problem gone is not a decision anyone has authority to make.

---

## 11. Risk acceptance and waiver boundary

Six things are routinely collapsed into "sign-off" and are kept apart here: accepting risk; waiving a process requirement; approving progression; approving an artifact; accepting legal or compliance nonconformance; overriding law or regulation.

Rules:

1. **No Decision Right in this registry may waive mandatory law or regulation.** A registry cannot create authority the legal order does not grant, and declaring otherwise would not make it so.
2. A risk-acceptance Right declares **which risk class and scope** it may accept.
3. It must identify the **residual risk and its evidence basis**.
4. **Risk remains recorded after acceptance.** Acceptance changes who carries it, not whether it exists.
5. Acceptance may carry an **expiry or review trigger**.
6. **A process waiver is separately scoped from risk acceptance** where the effects differ — waiving a step and accepting the risk the step would have found are different decisions.
7. **Review findings remain findings after waiver or risk acceptance.**
8. A human authority **cannot approve outside the legal or organisational authority the Right represents.**

---

## 12. Emergency authority

An Emergency Decision Right declares: an **objective emergency trigger**; what normal prerequisite or gate may be bypassed, if any; **what can never be bypassed**; the eligible emergency authority class; the maximum decision scope; time validity; mandatory evidence at exercise time; mandatory retrospective review or ratification; and expiry, rollback and recovery expectations.

Rules:

- **Urgency is never authority.** An emergency creates the conditions under which a *pre-declared* emergency Right may be exercised; it does not create authority where none was declared.
- **Emergency authority is not standing ordinary authority**, and does not become it through repeated use.
- **Emergency use does not retroactively satisfy skipped reviews.** They remain skipped and open until separately completed.
- **Retrospective review does not rewrite the historical emergency decision.** It assesses it; the record stands as made.

Emergency architecture is not software-specific. `decision.emergency_production_change` is one stress test; a regulatory notification deadline or a site-safety instruction has the same shape.

---

## 13. Cancellation and termination authority

Cancellation authority is a Decision Right question, not a Workflow ownership question. **A Workflow cannot decide who may cancel it.**

A Right states whether it may: cancel before commitment; terminate after commitment; pause or suspend; reject and return to rework; abandon with open items retained; or reverse a prior progression decision. These are different powers and a Right holds only those it declares.

Cancellation preserves: the reason; the state at cancellation; open findings and risks; artifacts and evidence; prior decisions; and external commitments already made. **No destructive history erasure**, and in particular cancelling a path does not undo commitments already given to third parties.

---

## 14. Knowledge-state boundary

| State | Governance |
|---|---|
| `REVIEWED` | **Review-governed.** Not created by a Decision Right by default |
| `APPROVED` | Requires a bounded approval Decision Right |
| `CANONICAL` | Requires a **distinct canonical-promotion authority**; never inferred from generic approval |
| `SUPERSEDED` | May follow a valid supersession decision; the prior artifact and record are retained |

A Decision Right may **never** turn `UNKNOWN` into a fact; `ASSUMPTION` into a fact; `CONFLICT_DETECTED` into resolved; or `AI_SUGGESTION` directly into `CANONICAL` without a governed human decision and its prerequisite controls.

Authority decides what to do about the state of knowledge. It does not decide what the state of knowledge is.

---

## 15. Decision Right dependencies

A Right may declare a bounded **prerequisite reference** to a concrete `decision.<id>`, with the required prior outcome.

Rules: satisfaction is **not transitive**; **authority does not transfer**; direct and transitive **cycles are prohibited** as an architecture validation rule; the dependency creates **no runtime call semantics**; and **collective or dual-control requirements use cardinality inside one Right rather than chaining pseudo-decisions** — a two-person requirement is one decision with `MULTI_HOLDER_ALL_REQUIRED`, not two Rights depending on each other.

---

## 16. Relationship to the other registries

| Registry | Direction | What Phase 7 may do |
|---|---|---|
| Role Registry (Phase 3) | upstream | Reference `role.<id>` and Role-owned artifacts; grant no Role anything |
| Skill Registry (Phase 4) | upstream | Reference capabilities within existing compatibility; widen nothing |
| Workflow Registry (Phase 5) | adjacent | A Workflow's `HUMAN_GATE_REFERENCE` resolves to a Right here; Phase 5 semantics unchanged |
| Handoff & Review (Phase 6) | adjacent | A `DECISION_REFERENCE` resolves here; **a Right never makes a review `SATISFIED`**; Phase 6 semantics unchanged |
| Memory / Canonical governance (Phase 8) | downstream | Canonical promotion is referenced here and may be substantively owned there |
| Model / runtime | out of scope | **No model or agent may hold a Decision Right by model identity alone** |

## 17. Human Approval Matrix

Architecture guidance for the eight carded Rights. **This is not runtime assignment**: it names eligibility classes, never holders.

| Decision Right | Class | Subject | Holder eligibility | Cardinality | Delegation | Primary upstream trigger | Required review state | External commitment? | Exceptional progression? | Accepts risk? | Knowledge-state effect |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `decision.exceptional_progression` | `EXCEPTION_DECISION` | One named unresolved item at one progression point | Sponsor; Governance body; Functional (single-domain only) | Single, or all-required across domains | **`NON_DELEGABLE`** | Phase 5 §14A material items; Phase 6 satisfaction rules | Records the review's status; **never changes it** | **No** | **Yes — this is the Right** | **No** | **None** |
| `decision.stage_gate_progression` | `PROGRESSION_DECISION` | One named stage gate | Sponsor; Governance body | Single → body at Enhanced Decision-Grade | With constraints; no re-delegation | `workflow.project_development_readiness` S7 | All band reviews `SATISFIED`, or exception taken separately | No | No | No | **None** |
| `decision.granting_authority_submission` | `COMMITMENT_DECISION` | One package to one authority | Signatory; Executive; Sponsor jointly only | Single → all-required on exposure | With constraints; no re-delegation | `workflow.eu_grant_application_development` S6 | `review.eu_programme_compliance` `SATISFIED` | **Yes** | No | No | **None** |
| `decision.external_publication` | `COMMITMENT_DECISION` | One content item to an external audience | Signatory; Executive; Communications functional (approved positions only) | Single → all-required for new positions or claims | Within eligibility; no re-delegation | `workflow.decision_grade_document_preparation` S5 | `review.factual_evidence` / `review.commercial_claims` `SATISFIED` | **Yes** | No | No | **None — publication is not canonical promotion** |
| `decision.contract_commitment` | `COMMITMENT_DECISION` | One obligation set with one counterparty | **Signatory only**; Governance body above threshold | Single → dual → body by value | With constraints; no re-delegation | `workflow.contract_review_cycle`, `workflow.transaction_execution_preparation` | `review.legal_compliance` `SATISFIED` | **Yes** | No | **No** — separate `decision.risk_acceptance` | **None** |
| `decision.risk_acceptance` | `RISK_ACCEPTANCE_DECISION` | One characterised residual risk | Executive; Governance body above ceiling; Functional in-domain | Single → body above ceiling | With constraints; no re-delegation | `workflow.project_development_readiness` S5; risk cycle | Informed by `review.risk_quantification` | No | **No — permits no progression** | **Yes — this is the Right** | **None** |
| `decision.production_release` | `COMMITMENT_DECISION` | One change set into production | Release functional; Executive; Governance body for accreditation | Single → all-required at Enhanced Decision-Grade | Within eligibility, change-class bound | `workflow.software_change_delivery` S6 | `review.security`, `review.test_coverage` `SATISFIED` | **Yes** | No | No | **None** |
| `decision.emergency_production_change` | `EMERGENCY_DECISION` | One time-critical change for one declared incident | **Pre-designated** emergency functional; Executive on regulatory exposure | **Single** — scrutiny sits in the retrospective step | **`NON_DELEGABLE`** | `workflow.software_change_delivery` emergency path | Reviews **bypassed remain `NOT_SATISFIED` and open** | **Yes** | Contains its own exception | No — separate | **None** |

### Authority gaps this matrix makes visible

1. **No Right in the eight changes a knowledge state.** `CANONICAL` promotion is a candidate in the universe and is deliberately uncarded pending open question 7.
2. **Two Rights are `NON_DELEGABLE`** — exceptional progression and emergency change — and both are the Rights an organisation under pressure will most want to delegate. That is why they are not delegable.
3. **No Right accepts risk except the risk-acceptance Right**, and it permits no progression. Every other card states the separation explicitly, because in practice the two acts are taken in one breath.
4. **Every commitment Right requires an authority class no Role holds.** Signatory and executive authority appear nowhere in the Role Registry, which is correct — and it means the matrix has a hard edge at the boundary between doing the work and binding the entity.

## 18. Non-runtime statement

This document and every artifact in `decisions/` is declarative architecture. Nothing here implements or specifies a database schema, API, user interface, notification system, workflow runtime, model routing, agent execution, electronic signature, identity management, authentication or authorisation system. A later runtime **validates against** these semantics; it does not mutate them.

## 19. Status

All Phase 7 artifacts are `PROPOSED`. Nothing is APPROVED or CANONICAL, and inclusion in this registry confers no authority on anyone.
