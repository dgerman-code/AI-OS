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
| The owning Role exists but is unavailable in this scope, or its mapping is absent | **`REQUIRED_ROLE_UNAVAILABLE`** — block, or produce a plan explicitly constrained to work that does not need that conclusion, clearly marked as not covering it |
| No approved Role owns the conclusion | **Block.** The work needs a conclusion the approved universe has no owner for, which is a governance gap and is escalated, not filled |

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
| `authority_note` | What the Role does **not** gain by participating — never blank |

`SkillRequirement`:

| Field | Content |
|---|---|
| `skill_ref` | An approved `skill.<id>` or `skill_pack.<id>` |
| `for_role` | The `role.<id>` it activates for (RS-7) |
| `phase_4_basis` | `DIRECT` · `TRANSITIVE` · `ABSENT` |
| `availability` | `AVAILABLE` · `CANDIDATE_NOT_ACTIVATABLE` (RS-8) |

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
branch and is not approved. So by RS-9 the planner either blocks or produces a constrained plan:
evidence analysis and legal position, with drafting attached to the owning substantive Role and the
plan stating that no communication-strategy conclusion is produced.

What the planner must **not** do is assign the drafting to whichever Role sounds closest and call
the gap covered. `exemplars.md` Example 2 works this through in full.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no inference implementation, embedding,
index, model, schema or storage, and binds no provider or runtime technology.
