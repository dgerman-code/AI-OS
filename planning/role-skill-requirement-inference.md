# Role and Skill Requirement Inference

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. What is being inferred

Not "which persona should answer this". **Which approved Roles own the professional conclusions
this work will have to produce**, and which approved Skills those Roles need activated to produce
them.

The distinction is the whole document. A persona is chosen by fit; a Role is required by ownership.
If the work will produce a legal conclusion, `role.legal_regulatory_lead` is not a good choice — it
is the only Role whose card lists that conclusion, and without it the conclusion has no owner.

## 2. The inference is from ownership, not similarity

**Rule RS-1 — a Role is required because it owns a conclusion the work needs.** The chain is:

```text
deliverable → the conclusions it must carry → the Role whose approved card OWNS each conclusion
```

Never `request text → Role that sounds relevant`. A semantic score may **shortlist** Roles for
checking; it may not select one (`workflow-matching-and-composition.md` MC-4).

**Rule RS-2 — every requirement resolves against the approved registries, or it is unavailable.**
A `RoleRequirement` names a `role.<id>` from the approved Phase 2/3 role universe. A
`SkillRequirement` names a `skill.<id>` or `skill_pack.<id>` from the approved Phase 4 registry.
There is no third option: no inline description of a capability, no "a role like X", no synthesised
identifier.

**Rule RS-3 — the planner invents nothing.** It does not create a Role, widen a Role's scope,
create a Skill, create a pack, or declare a Role compatible with a Skill that Phase 4 mapping does
not allow. A Workflow cannot make a Role compatible with a Skill Phase 4 forbids, and a Work Plan
has strictly less power than a Workflow.

## 3. Derivation patterns

Illustrative, and each is an example of the ownership chain rather than a lookup table to be
applied mechanically.

| The work will produce | Owning Role(s) | Because |
|---|---|---|
| A financial model or its outputs | `role.financial_modelling_specialist` | Model design and integrity is its owned conclusion |
| A PPP / concession suitability position | `role.ppp_concession_specialist`; with `role.legal_regulatory_lead` where the structure is contractual; with `role.funding_bankability_architect` where financeability is in question | Three distinct conclusions, three owners |
| An EU grant application | `role.eu_grants_programmes_specialist`; `role.grant_financial_compliance_budget_specialist` for budget eligibility; `role.deliverables_reporting_specialist` where deliverables are defined | Programme rules, budget eligibility and deliverable design are separately owned |
| Legally consequential correspondence | `role.legal_regulatory_lead` **co-activated**, never replaced by the drafter | An admission or reservation is a legal conclusion |
| Publication under the entity's name | `role.institutional_communications_editorial_specialist`, plus the applicable Decision Right | Editorial standards are owned; publication authority is human |
| A technical feasibility position | `role.technical_feasibility_lead` or `role.sector_technical_expert` | Technical truth is owned, and not by a generalist |
| Evidence provenance for a contested record | `role.knowledge_evidence_steward` | Provenance integrity is its owned conclusion |
| A risk characterisation | `role.enterprise_project_risk_specialist` — and risk **acceptance** remains a human Decision Right | Characterising and accepting are different acts |

**Rule RS-4 — co-activation, never blending.** Where work spans domains, the planner requires
**each** owning Role. It never creates a combined requirement, never nominates one Role to "cover"
another's domain, and never lets a Role with adjacent competence stand in for the owner. Partial
expertise does not aggregate into ownership — the same rule Phase 6 applies to bounded review
contributors.

**Rule RS-5 — a Role gains nothing by being required.** Appearing in a plan confers exactly its
approved Role Card and nothing else. No plan widens a scope, and a Role required for one conclusion
does not thereby own a neighbouring one.

## 4. Conditional requirements

Some Roles are required only where a condition holds. The condition is **objective and recorded**,
never "if it seems necessary".

| Conditional Role | Objective activation condition |
|---|---|
| `role.legal_regulatory_lead` | A legal position, admission, reservation of rights, dispute or contractual interpretation is in the deliverable |
| `role.data_protection_gdpr_specialist` | Personal data would be processed or disclosed |
| `role.procurement_state_aid_specialist` | A live procedure, State Aid exposure, or public-funding rules apply |
| `role.integrity_due_diligence_specialist` | An integrity, sanctions or AML/KYC flag fired (T-12) |
| `role.institutional_affairs_stakeholder_specialist` | The counterparty is an institutional stakeholder |
| `role.people_organisation_specialist` | The matter is an employment or people matter |

**Rule RS-6 — a conditional requirement that fires becomes mandatory.** It is not advisory, not
"recommended", and not removable to shorten the plan. `governance-preflight.md` check G-5 fails a
plan whose fired conditions are unmet.

## 5. Skill requirements

**Rule RS-7 — Skills attach to a Role, never float.** A `SkillRequirement` names the Role it
activates for, and the Phase 4 basis — direct mapping or transitive through a pack — that makes the
activation permissible. A Skill required for no Role is a defect.

**Rule RS-8 — a candidate Skill is not a Skill.** Where a needed capability exists only as a
proposed or candidate entry, it is **unavailable**. The plan records
`REQUIRED_SKILL_UNAVAILABLE` and either constrains or fails closed (§6). A plan that activated a
candidate would be relying on an unregistered capability.

## 6. When a requirement cannot be met

**Rule RS-9 — fail closed or constrain; never substitute.** Three outcomes, and no fourth:

| Situation | Outcome |
|---|---|
| The owning Role exists, is approved and is available | Requirement met |
| The owning Role exists but is unavailable in this scope, or its mapping is absent | **`REQUIRED_ROLE_UNAVAILABLE`** — **BLOCK** where §6a records `load_bearing = LOAD_BEARING`; otherwise a plan explicitly constrained to work that does not need that conclusion, clearly marked as not covering it |
| No approved Role owns the conclusion **and the originally requested deliverable requires it** | **BLOCK** — `NO_APPROVED_ROLE_OWNS_CONCLUSION` (F-14) + escalate. This is a **governance gap**, not an availability problem, and it is **not** routed through F-5: there is no load-bearing determination to make, because there is no owning Role whose absence could be weighed. §6b |

### 6a. The load-bearing predicate — normative, and inspectable

F-5 and F-6 each need **one** disposition, so "load-bearing" cannot be a judgement call. It is a
predicate over material the plan has already recorded: the declared deliverables, the owned
professional conclusions, the stage dependency order, and the required gates and reviews. It never
reads a confidence value, an urgency, a deadline or a convenience.

**Rule LB-0 — every test is evaluated against the deliverable the user originally requested.**
The subject of LB-1 is the **declared deliverable as requested, before any constraint-induced
reduction**: what `WorkIntent.requested_outcome` asked for, plus what
`WorkRequirementSet.deliverables` derived from it, as they stood **before** the planner considered
narrowing anything. Evaluating the predicate against an already-reduced deliverable is circular —
remove the conclusion, call what is left the deliverable, then observe that the deliverable does not
need the conclusion — and that reasoning would clear every gap it was asked to judge.

The order is therefore fixed, and the two steps never merge:

| Step | What is decided | Against what |
|---:|---|---|
| **1** | `LOAD_BEARING` or `NOT_LOAD_BEARING` (LB-1) | The **original** requested deliverable, un-narrowed |
| **2** | Only if step 1 returned `NOT_LOAD_BEARING`: whether a reduced deliverable is admissible (LB-2) | The reduced deliverable |

**Rule LB-6 — a reduced deliverable is never evidence about the removed capability.** It is a
consequence of the determination, never an input to it. A `load_bearing_basis` may never cite a
narrowed deliverable as its reason; `governance-preflight.md` G-5 and G-6 fail the plan that records
one, because such a basis proves only that the narrowing happened.

**Rule LB-1 — the predicate.** An unavailable Role or Skill is `LOAD_BEARING` where **any** of the
following holds **of the original requested deliverable**, and `NOT_LOAD_BEARING` only where none
does:

| # | Condition | Read from |
|---:|---|---|
| LB-a | It owns a professional conclusion that the **originally requested deliverable** must carry — including a conclusion the user asked for **in terms**, however it was phrased | `WorkIntent.requested_outcome` and `WorkRequirementSet.deliverables` as first derived, before any narrowing (LB-0); the ownership chain of RS-1 |
| LB-b | It owns, or is a required participant in, a **mandatory review** the band requires | `ReviewRequirement` set, `work-classification-and-criticality.md` |
| LB-c | It is a prerequisite of an **authority or gate** the plan contemplates | `DecisionRequirement` set, `governance-preflight.md` G-10 |
| LB-d | It produces an **upstream artifact that every valid path** to the requested deliverable depends on | The stage dependency order (MC-12): no path from the plan's entry to the deliverable avoids that stage |
| LB-e | It is a **fired conditional requirement** (RS-6) | `RoleRequirement.activation` |

**Rule LB-2 — a reduced deliverable is validated only after `NOT_LOAD_BEARING` is independently
established.** LB-2 never decides the determination; it checks whether the narrowing LB-1 has
already permitted is admissible. A reduced deliverable is admissible only where it (i) does not
imply coverage of the missing capability, (ii) carries no conclusion that capability owns, and
(iii) is stated to the user as reduced (RS-10). Where step 1 returned `LOAD_BEARING`, LB-2 is not
reached at all and the disposition is BLOCK; where step 1 returned `NOT_LOAD_BEARING` and no
admissible reduced deliverable can be described, the plan blocks as well.

**Rule LB-3 — the determination is recorded as a first-class field, not inferred at read time.**
Every `RoleRequirement` and `SkillRequirement` whose `availability` is not `AVAILABLE` carries:

| Field | Content |
|---|---|
| `load_bearing` | `LOAD_BEARING` · `NOT_LOAD_BEARING` |
| `load_bearing_basis` | The conditions of LB-1 that fired, by letter, each with the plan element it was read from; or, for `NOT_LOAD_BEARING`, the reduced deliverable that survives under LB-2 |

`governance-preflight.md` G-5 and G-6 fail a plan that records an unavailable capability without
both fields. The same inputs therefore produce the same disposition, and a reader can check the
determination rather than trust it.

**Rule LB-4 — the predicate never reaches for a substitute.** It decides **block or constrain**. It
has no branch that assigns the conclusion to a different Role, and RS-9's three outcomes remain
three (RS-4).

**Rule LB-5 — a candidate capability is unavailable for the predicate too.** A Role, Skill or Review
Profile that exists only as a proposal counts as absent when LB-1 is evaluated. Treating a candidate
as present would make the determination depend on what someone hopes to approve later.

### 6b. No approved owner is a different failure from an unavailable owner

Two situations look alike and are not:

| Situation | Failure mode | Predicate | Disposition |
|---|---|---|---|
| An **approved** owning Role or Skill exists, and is unavailable in this scope, unmapped, or otherwise not activatable | **F-5** / **F-6** | §6a applies: `load_bearing` is determined against the original deliverable | BLOCK where `LOAD_BEARING`, CONSTRAIN where not |
| **No approved Role owns the conclusion at all**, and the originally requested deliverable requires it | **F-14** `NO_APPROVED_ROLE_OWNS_CONCLUSION` | None. There is no approved owner whose absence could be weighed, so no determination is made | **BLOCK** + escalate as a governance gap |

**Rule RS-12 — the no-owner case is never routed through F-5 as `NOT_LOAD_BEARING`.** That route
would let an unfilled hole in the approved universe be closed by a determination rather than by
governance. There is exactly one circumstance in which a missing owner does not block: where the
**originally requested deliverable, un-narrowed, does not require that conclusion at all** — in
which case there was never a requirement, LB-0 shows it, and nothing was removed. That is a finding
about the request, established before any narrowing, and it is recorded as such.

**Rule RS-13 — a conclusion the user asked for cannot be narrowed away.** Where the user's request
asks for a conclusion in terms — a communication strategy, a legal position, a recommendation — and
no approved Role owns it, the architecture does not produce a narrower result and present it as the
answer. It blocks and escalates. Narrowing is available only where the original deliverable permits
it under LB-0 and LB-1, and a plan may never establish that permission by narrowing first.

**Rule RS-10 — a constrained plan says what it does not cover.** Where the planner proceeds without
a Role, the plan states in terms the user will read: *this plan does not produce a legal position,
and nothing in it may be relied on as one.* A constrained plan that looks complete is worse than a
blocked one, because the gap is invisible at the point of reliance.

**Rule RS-11 — business necessity is not a Role.** "We need this today and legal is unavailable" is
not a basis for proceeding without the owner. It is a reason to escalate.

## 7. The requirement records

`RoleRequirement`:

| Field | Content |
|---|---|
| `role_ref` | An approved `role.<id>` — never a description |
| `owned_conclusion` | The conclusion this Role is required for |
| `activation` | `ALWAYS` or `CONDITIONAL(<objective condition>)` |
| `basis` | The material in the request or scope that produced the requirement |
| `availability` | `AVAILABLE` · `UNAVAILABLE` · `UNAPPROVED` |
| `load_bearing` | `LOAD_BEARING` · `NOT_LOAD_BEARING` — required wherever `availability` is not `AVAILABLE` (LB-3) |
| `load_bearing_basis` | The LB-1 conditions that fired, or the reduced deliverable that survives (LB-2) |
| `authority_note` | What the Role does **not** gain by participating — never blank |

`SkillRequirement`:

| Field | Content |
|---|---|
| `skill_ref` | An approved `skill.<id>` or `skill_pack.<id>` |
| `for_role` | The `role.<id>` it activates for (RS-7) |
| `phase_4_basis` | `DIRECT` · `TRANSITIVE` · `ABSENT` |
| `availability` | `AVAILABLE` · `CANDIDATE_NOT_ACTIVATABLE` (RS-8) |
| `load_bearing` | `LOAD_BEARING` · `NOT_LOAD_BEARING`, evaluated for the Role it activates for (LB-3) |
| `load_bearing_basis` | As `RoleRequirement` |

## 8. Worked inference

"Review this partner email. They blame us for the delay. Check whether they are right and prepare a
firm but professional response."

| Conclusion the work needs | Owning Role | Activation |
|---|---|---|
| What the record actually shows about the delay | `role.knowledge_evidence_steward` | `ALWAYS` — the request asks whether the claim is right, which is an evidence question |
| Whether the contract allocates responsibility for the delay | `role.legal_regulatory_lead` | `CONDITIONAL` — **fires**: "blame us" against a contracted counterparty is contractual |
| The partner relationship position | `role.programme_partnership_manager` or `role.consortium_partner_coordination_specialist` | `CONDITIONAL` on the partner's relationship class |
| Communication strategy and the draft itself | *No approved Role owns this today* | See below |

The fourth row is the honest result. At the Phase 13 baseline the approved universe has **no Role
that owns difficult-conversation communication strategy**; a candidate exists on a separate proposal
branch and is not approved. So by RS-9 this is the **third** row, not the second: there is no approved owner at all, which is
a governance gap rather than an availability problem, and §6b keeps it out of F-5 entirely.

Whether it blocks turns on LB-0 — on the deliverable **as the user requested it**, before anything
is narrowed:

| The request | The originally requested deliverable | Outcome |
|---|---|---|
| *"…prepare a firm but professional response. I do not want to damage the relationship."* | A reply that is **firm but professional** and **protects the relationship** — a communication-strategy conclusion, asked for in terms | **BLOCK**, `NO_APPROVED_ROLE_OWNS_CONCLUSION` (F-14), escalated as a governance gap |
| *"Check whether they are right."* and nothing further | An evidence position | No communication-strategy conclusion was ever required. LB-0 shows it, nothing is removed, and the plan proceeds |

The first row is the one the exemplar works through, and the earlier version of this document got
it wrong: it removed the communication-strategy conclusion, called the remainder the deliverable,
and concluded from the remainder that the removed conclusion had not been needed. LB-6 now names
that reasoning as a validation failure. A user who asks for a firm reply that preserves a
relationship has asked for exactly the conclusion the approved universe has no owner for, and the
honest answer is that the system cannot produce it — not a narrower answer presented as the answer
(RS-13).

What the planner must **not** do is assign the drafting to whichever Role sounds closest and call
the gap covered, and it must not narrow the deliverable in order to prove the gap did not matter.
`exemplars.md` Example 2 works this through in full.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no inference implementation, embedding,
index, model, schema or storage, and binds no provider or runtime technology.
