# AI-OS Handoff & Review Registry Design

Status: PROPOSED — Phase 6 architecture candidate
Version: 0.1
Depends on: approved Phase 3 Role Registry, approved Phase 4 Skill Registry, approved Phase 5 Workflow Registry

## Purpose

Phase 5 established that a Workflow may **reference** a review requirement and a human gate but may define neither. That left two holes the registry pointed at and could not fill: what a `review.<id>` actually *is*, and what happens at the moment one Role hands work to another.

Phase 6 fills exactly those two holes, with two **separate** models:

1. the **Handoff Model** — the governed transfer of a work product between Roles;
2. the **Review Profile Registry** — reusable definitions of independent review.

They interact. They are not merged. A Handoff asks *is this package transferable?*; a Review asks *is this work sound?* Collapsing them would produce an object that checks completeness and calls the result assurance, which is the single most damaging thing this architecture could do.

## The separation this phase must preserve

```
ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != MODEL != RUNTIME
```

| Object | Owns |
|---|---|
| **Role** | methodology, professional scope, conclusions, artifact interfaces |
| **Skill** | reusable capability, bounded by the Phase 4 mapping records |
| **Workflow** | stages, participation, state expectations, gate references |
| **Handoff** | the governed transfer of a Role-owned work product, evidence package, dependency or responsibility-for-next-action **without transferring professional ownership** |
| **Review Profile** | what is reviewed, for what purpose, under what independence constraints, with what outputs and severity semantics |
| **Decision Right** | external human authority — Phase 6 references it and defines nothing about it |
| **Model / runtime** | implementation, out of scope entirely |

**A Handoff never transfers artifact ownership** unless the upstream Role Card already defines a legitimate ownership transition, in which case the transition is the Role Card's and the Handoff merely coordinates it.

**A Review Profile never makes the human decision it informs.**

---

## 1. Handoff Model

### 1.1 Identity

```
handoff.<stable_snake_case_name>
```

A Handoff Card is a reusable pattern for a recurring transfer, not a record of one transfer having happened. The stable ID carries no organisation, project, person, model, version or runtime technology.

### 1.2 Primitives

Thirteen declarative primitives. This is not a runtime DSL: there is no execution semantics, no queueing, no acknowledgement protocol and no persistence format.

| Primitive | Meaning |
|---|---|
| `HANDOFF_TRIGGER` | The condition under which this transfer becomes due |
| `SENDER_ROLE` | The approved `role.<id>` releasing the subject |
| `RECEIVER_ROLE` | The approved `role.<id>` taking it up for a bounded next activity |
| `HANDOFF_SUBJECT` | What is being handed over — artifact, evidence set, dependency, or responsibility for the next action |
| `HANDOFF_PACKAGE` | Everything that must travel with the subject for the receiver to proceed |
| `STATE_REQUIREMENT` | The knowledge state(s) the subject must hold at transfer |
| `OPEN_ITEM_CARRY` | The unresolved assumptions, conflicts and unknowns that travel with it, classified |
| `PROVENANCE_REQUIREMENT` | The source, version and traceability record that must accompany it |
| `RECEIPT_ACKNOWLEDGEMENT` | The receiver's statement that the package is complete enough to use — and nothing more |
| `RETURN_FOR_REWORK` | The conditions under which the receiver returns the package unaccepted |
| `HANDOFF_BLOCK` | A condition preventing transfer entirely |
| `REVIEW_REFERENCE` | A `review.<id>` that must be `SATISFIED` before transfer, where applicable |
| `DECISION_REFERENCE` | A `decision.<id>` human gate on the transfer, where applicable |

### 1.3 The ten questions every Handoff must answer

1. What exactly is being handed over?
2. Who sends it?
3. Who receives it?
4. What does the receiver need in order to proceed?
5. What provenance and evidence must accompany it?
6. Which assumptions, open items and conflicts remain unresolved?
7. What state must the subject be in?
8. What does acknowledgement mean?
9. What causes return for rework?
10. Which review or Decision Right may block progression?

A Handoff that cannot answer all ten is hiding a transfer of something in the gap.

### 1.4 Receipt semantics — the critical boundary

`RECEIVED` means: **the package was accepted as complete enough to inspect or use for the next bounded activity.**

It does **not** mean:

- the receiver agrees with the conclusion;
- the subject is `REVIEWED`, `APPROVED` or `CANONICAL`;
- professional ownership has moved;
- any review requirement has been satisfied;
- the sender's work is correct.

This is the distinction that makes the whole model work. A receiving Role that accepts a package and later finds the conclusion wrong has not endorsed anything by receiving it — and a sending Role cannot cite receipt as validation.

### 1.5 Completeness is not correctness

A Handoff checks **package completeness and transfer readiness**. That is a different question from whether the work is sound, and it is answered by a different object:

| | Handoff | Review |
|---|---|---|
| Asks | Is the package complete and transferable? | Is the work substantively sound? |
| Checked by | The receiving Role, against the package definition | An eligible independent reviewer, against a Review Profile |
| Failure produces | `RETURN_FOR_REWORK` — a transfer failure | A finding with a severity |
| Establishes | Nothing about quality | Nothing about completeness of any transfer |

A receiver acknowledging a handoff **is not performing independent review**, however carefully it inspects the package. A Handoff may require a `review.<id>` to already be `SATISFIED` before transfer; a Review may consume a handoff package as its evidence input. **A handoff rejection is not a review finding** unless a Review Profile explicitly says that condition is one.

### 1.6 Chained handoffs

Where a subject passes through several Roles, each transfer is its own Handoff with its own package, state requirement and carried open items. A chain does not accumulate authority: the fourth receiver has exactly what the first sender's Role Card permits it to have, and every open item carried at transfer 1 is still carried at transfer 4 unless it was resolved by a Role competent to resolve it.

A `RETURN_FOR_REWORK` at any link returns to the sender of that link, not to the head of the chain, unless the finding invalidates an earlier package — in which case the earlier link is returned too, and the intermediate work is marked dependent on a superseded input.

---

## 2. Review Profile Registry

### 2.1 Identity

```
review.<stable_snake_case_name>
```

The stable ID must not contain an organisation, project or client, a model or provider, an individual reviewer, a version number, or a runtime technology. A Review Profile defines **review architecture, not a reviewer instance**.

### 2.2 A Review Profile must NOT

1. grant a Role new professional authority;
2. create a Decision Right;
3. approve or canonicalize an artifact by itself — where a governed knowledge-state transition permits it, the most a review can support is `REVIEWED`, and never `APPROVED` or `CANONICAL`;
4. define business or policy decisions;
5. bind a model or vendor as reviewer identity;
6. execute the review;
7. override the owning Role's professional scope;
8. allow the author or producer to satisfy an independent-review requirement through self-check or QC.

### 2.3 Bounded scope

Every Review Profile states its subject artifact(s) and conclusion(s), the owning Role(s), its purpose, what it checks, **what it explicitly does not check**, required inputs and evidence, required traceability, criticality applicability, and any dependency on another review.

Generic "review everything" profiles are prohibited. **No single profile may absorb technical, financial, legal, ESG, security and evidence-integrity review** — that is not a review, it is an unaccountable opinion with a registry ID. The out-of-scope statement is the load-bearing part: it is where a profile says which neighbouring review must also run.

---

## 3. Reviewer independence model

This is the central architecture question of Phase 6. Independence is a property of the **relationship between the reviewer and the work in a specific assignment instance**, not a label.

### 3.1 Independence classes

| Class | Independence | Meaning |
|---|---|---|
| `PRODUCER_REVIEW` | **None** | The producing Role checking its own work. Internal quality control only. **Never satisfies an independent-review requirement.** |
| `PEER_REVIEW` | Assignment-level | A different Role instance in the same or similar professional domain, which did not produce the reviewed artifact or conclusion. |
| `CROSS_DOMAIN_REVIEW` | Domain-level | A reviewer from a different Role or domain, checking interfaces, consistency, assumptions or dependencies. **Does not substitute for domain review** — it cannot conclude on the domain it is checking across. |
| `INDEPENDENT_ASSURANCE_REVIEW` | Heightened | Full separation from the producing assignment and from the delivery line, required for decision-grade and high-criticality work. |

`PRODUCER_REVIEW` is in the vocabulary precisely so that internal QC has a name and can be recorded — and can therefore be recognised as *not* the thing an independent requirement asks for.

### 3.2 Independence constraints

For any requirement declaring `PEER_REVIEW`, `CROSS_DOMAIN_REVIEW` or `INDEPENDENT_ASSURANCE_REVIEW`:

1. the reviewer **cannot be the author or producer** of the reviewed artifact or conclusion;
2. the reviewer **cannot be the Workflow stage lead** where that Role authored the subject under review and leading would compromise independence;
3. a reviewer **cannot review a conclusion it owns as producer in the same assignment instance** — owning the conclusion elsewhere is fine; owning *this* one is disqualifying;
4. a Review Profile **cannot declare a participating Role independent merely by naming it so**, and neither can Workflow prose. Independence is established by the absence of a producing relationship, checked against Role and Workflow participation, not asserted;
5. **model-family diversity is not independence.** It may later be recorded as a runtime or assignment preference; it must never be used as a substitute for Role and assignment independence. Two different models running the same producing Role are not two reviewers;
6. where adequate independent reviewer eligibility **cannot be satisfied**, the review is `NOT_SATISFIED` and the Workflow or Handoff must block, rework or escalate. An unavailable reviewer does not lower the requirement.

Phase 6 defines no human names, no staffing assignment and no model selection.

---

### 3.3 Reviewer eligibility classes — full-Profile versus bounded

Independence answers *may this Role review this work*. It does not answer *is this Role competent for the whole of what this Profile asserts*. Conflating the two lets a Role with genuine expertise in one dimension acquire authority over a Profile its Role Card does not cover — by aggregation, and without any Role Card ever changing.

Two eligibility classes therefore sit alongside the independence classes:

| Class | Meaning |
|---|---|
| `FULL_PROFILE_REVIEWER_ELIGIBLE` | The Role's **approved Role scope already covers every satisfaction criterion and professional conclusion the Profile requires.** It may satisfy the Profile alone. |
| `BOUNDED_REVIEW_CONTRIBUTOR` | The Role's approved scope covers **one dimension** of the Profile. It may contribute a bounded `CROSS_DOMAIN_REVIEW`, an evidence or reconciliation check, or a domain-specific check — and **cannot satisfy the whole Profile.** |

Normative rules:

1. A Role may satisfy an entire Review Profile **only** if its approved Role scope already covers every satisfaction criterion and professional conclusion that Profile requires.
2. **Partial expertise does not aggregate into full Profile authority.** Two `BOUNDED_REVIEW_CONTRIBUTOR` Roles between them covering the Profile's dimensions do not thereby produce a full-Profile satisfaction, unless the Profile explicitly declares a multi-reviewer composition whose bounded contributions are themselves individually governed.
3. **Phase 6 never widens Role scope.** Where a Profile appears to need a Role to conclude outside its card, that is a Role Registry question raised there — never resolved by the Profile.
4. **Profile wording cannot make a Role eligible by declaration.** Eligibility is checked against the Role Card; a card that says a Role is eligible without that scope is defective.
5. Where **no** approved Role or assignment instance is fully eligible, the Profile remains `NOT_SATISFIED`. An unavailable full-Profile reviewer does not lower the requirement, and cross-role authority is never invented by aggregation.

Every Reviewer Eligibility table states the class per Role. A Role listed without a class is a defect.

### 3.4 Multi-Profile reviewer instances

A single reviewer instance **may** satisfy more than one Review Profile — but only where all seven of the following are independently true **for each Profile, each subject, each artifact version and each assignment**:

1. reviewer eligibility passes **separately** for each Profile, including the eligibility class in §3.3;
2. independence passes **separately** for each Profile;
3. satisfaction of one Profile grants **no** eligibility, authority, scope or satisfaction for another;
4. the reviewer does not review its own output from another Profile where that output becomes the subject or the evidence of the second review;
5. **no Profile involved declares `SEGREGATION_REQUIRED`**;
6. no declared inter-Profile dependency or conflict-of-interest condition requires separate instances;
7. combining Profiles does not create cross-domain professional authority by accumulation.

Every Review Profile therefore declares:

```
Reviewer Instance Segregation: ALLOWED_IF_INDEPENDENTLY_ELIGIBLE | SEGREGATION_REQUIRED
```

**Default for decision-grade and high-criticality work covering interdependent domains is `SEGREGATION_REQUIRED`**, unless the Profile explicitly and defensibly states that same-instance review preserves the separation the Profile depends on. The reasoning is concentration: where two Profiles check different aspects of one interdependent subject, a single reviewer's blind spot propagates into both, and the second review stops being a second look.

This is an **architecture eligibility rule**. It defines no staffing algorithm, no assignment logic and no human allocation.

### 3.5 `REVIEW_DEPENDENCY` — declarative Profile dependency

Some reviews are meaningless before another has run. `review.project_integration_coherence` cannot check consistency between positions that have not themselves been reviewed; `review.security` consumes security testing performed under a scope the Security Engineer defines.

A Profile may therefore declare a `REVIEW_DEPENDENCY`, stating:

- the **concrete prerequisite `review.<id>`** — never a category or a description;
- the **required prerequisite status**, normally `SATISFIED`;
- an **objective activation condition** where the dependency is conditional;
- the **bounded purpose** of the dependency.

Normative rules:

1. An unsatisfied, `STALE` or missing required prerequisite makes the dependent review **`REVIEW_BLOCKED`** — not failed. The dependent review has not found a defect; it cannot yet run.
2. **Satisfaction is not transitive.** A satisfied prerequisite does not satisfy the dependent Profile, contribute to its satisfaction, or reduce its criteria.
3. A dependency transfers **nothing**: no scope, no reviewer eligibility, no authority, no findings, no professional conclusion, no satisfaction.
4. **Direct self-dependency is prohibited.**
5. **Transitive cycles are prohibited** as an architecture validation rule, detectable by reading the cards.
6. Conditional dependencies use **objective, testable** triggers only.
7. A dependency **does not execute** the prerequisite review. It creates no scheduling, no call stack and no runtime semantics of any kind.
8. A dependent Profile still evaluates **its own** evidence and satisfaction criteria independently, and reaches its own conclusion.

`None` with a stated reason is a valid and common declaration. Dependencies are not to be manufactured for symmetry.

## 4. Finding taxonomy

### 4.1 Finding classes

| Class | Meaning |
|---|---|
| `NO_FINDING` | The review found nothing within its stated scope |
| `OBSERVATION` | A remark that does not assert a defect |
| `MINOR_FINDING` | A defect that does not affect the conclusion or its reliance |
| `MAJOR_FINDING` | A defect that affects the conclusion, its basis, or reliance on it |
| `CRITICAL_FINDING` | A defect that invalidates the conclusion, or a governance or integrity breach |

### 4.2 Severity is not materiality

These are two different questions and Phase 6 keeps them apart:

- **Finding severity** is a *review assessment* of how bad a defect is;
- **Open-item materiality** (Phase 5, `standard.workflow.common_constraints` §14A) answers whether *progression may continue*.

They correlate but do not determine one another. A `MINOR_FINDING` on an artifact that a terminal gate depends on may be `MATERIAL_TO_NEXT_STEP_OR_GATE`; an `OBSERVATION` about presentation never is. **Do not assume every minor finding blocks, and do not assume every critical finding can be carried forward.**

### 4.3 Mapping rules

| Finding | Effect on review satisfaction | Effect on progression |
|---|---|---|
| `CRITICAL_FINDING`, unresolved | **Cannot be review-satisfied under any Profile.** | Blocks, reworks or escalates |
| `MAJOR_FINDING`, unresolved | **Normally blocks satisfaction.** A Profile may permit a bounded conditional disposition, and only where a **named external Decision Right** governs any exceptional progression | Blocks unless that Decision Right applies |
| `MINOR_FINDING`, unresolved | May remain open only where the Profile's satisfaction criteria allow it **and** the item is `NON_MATERIAL_TO_NEXT_STEP` | Per Phase 5 materiality |
| `OBSERVATION` | Does not affect satisfaction | Does not block |
| `NO_FINDING` | Supports satisfaction | Does not block |

**A Review Profile cannot waive its own findings.** Waiver, where it exists at all, is a human Decision Right and lives in Phase 7.

---

## 5. Review result and satisfaction semantics

### 5.1 Statuses

| Status | Meaning |
|---|---|
| `NOT_STARTED` | The requirement exists; no review has begun |
| `IN_REVIEW` | Under way; no result |
| `REVIEW_PERFORMED_WITH_OPEN_FINDINGS` | The review happened and produced findings that remain open |
| `SATISFIED` | The Profile's satisfaction criteria are met by an eligible reviewer |
| `NOT_SATISFIED` | Criteria not met — including because no eligible reviewer exists |
| `REVIEW_BLOCKED` | The review cannot proceed (evidence package incomplete, prerequisite review unsatisfied) |
| `STALE` / `SUPERSEDED` | A previously satisfied review invalidated by material change to the subject |

### 5.2 Performed is not satisfied

`REVIEW_PERFORMED_WITH_OPEN_FINDINGS` exists to make this impossible to blur. A review can be thorough, competent and complete and still leave the requirement **unsatisfied**. "We reviewed it" is not "it passed".

### 5.3 Satisfied is not approved

`SATISFIED` is a **review requirement status**. It may permit a Workflow Stage or Handoff requirement to be treated as met. It does **not** make the artifact `APPROVED` or `CANONICAL`, and the human Decision Right remains entirely separate and unaffected.

Review satisfaction is attributable to the Profile's criteria and to an eligible independent reviewer instance. It is **never** attributable to Workflow progression: no number of completed stages satisfies a review.

### 5.4 Staleness

Where the subject changes materially after review, the prior review becomes `STALE` and its satisfaction no longer supports progression. What counts as material change is stated per Profile in its re-review triggers.

---

## 6. Rework semantics

A finding routes back declaratively. Phase 6 states *where* rework belongs; it does not schedule it.

A finding carries: the affected artifact; the affected owning Role; the affected Workflow Stage(s) or Handoff; the required rework destination; the evidence required to close it; and whether re-review is mandatory.

**A finding cannot be silently closed because the Workflow revisited a Stage.** Revisiting is not remediation. Closure preserves:

- the original finding text and its severity as assessed;
- reviewer attribution and the eligibility record (recorded at instance level later);
- the response and remediation evidence;
- the closure rationale;
- the prior artifact version;
- the new artifact version;
- the re-review outcome where re-review was required.

---

## 7. Criticality scaling

Phase 6 inherits `architecture/project-criticality-policy.md` in full.

Criticality **may** increase: required review types; independence depth (e.g. `PEER_REVIEW` → `INDEPENDENT_ASSURANCE_REVIEW`); evidence depth; reviewer eligibility constraints; the number of handoff checkpoints; mandatory re-review after material change; traceability granularity; finding-closure evidence; escalation rigour.

Criticality **must not**: change Role identity; create a new Review Profile merely because the project is larger where the review purpose is the same; turn a reviewer into a Decision Right holder; or make review satisfaction equivalent to approval.

---

## 8. Relationship to the other registries

| Registry | Direction | What Phase 6 may do |
|---|---|---|
| Role Registry (Phase 3, approved) | upstream | Reference `role.<id>` and Role-owned artifacts; respect every Owns / Does Not Own boundary |
| Skill Registry (Phase 4, approved) | upstream | Reference capabilities **only within existing Phase 4 compatibility**; a Handoff or Review never widens it |
| Workflow Registry (Phase 5, approved) | adjacent | A Workflow's `REVIEW_REQUIRED_REFERENCE` resolves to a Review Profile here; a Workflow stage transition may consume a Handoff. Phase 5 semantics are unchanged by Phase 6 |
| Decision Rights Register (Phase 7) | downstream | Reference `decision.<id>` only. Phase 6 defines no holder, no delegation, no waiver semantics |
| Model / runtime | out of scope | No binding of any kind |

## 9. Non-runtime statement

This document and every artifact in `reviews/` and `handoffs/` is declarative architecture. Nothing here implements or specifies orchestration, scheduling, queueing, agent execution, model routing, database schema, API surface, user interface or automation code. A later runtime **validates against** this registry; it does not mutate its semantics.

## 10. Status

All Phase 6 artifacts are `PROPOSED`. Nothing in this phase is APPROVED or CANONICAL, and inclusion in either registry confers no approval on any Handoff or Review Profile.
