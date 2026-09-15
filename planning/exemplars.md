# Exemplars

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

> Six worked examples, with the internal planning objects shown. They demonstrate the rules; they
> are not fixtures, and none has been executed. Every identifier used is either an approved
> registry identifier or an explicitly marked planning identifier.

## Example 1 — an ordinary writing request

> "Create a LinkedIn post about this news."

**`WorkIntent`**

| Field | Value |
|---|---|
| `objective` | Publish a short post about a news item |
| `primary_work_mode` | `DRAFTING` |
| `secondary_work_modes` | empty |
| `act_direction` | `EXTERNAL` — a LinkedIn post leaves the entity |
| `reversibility` | `COSTLY_TO_REVERSE` — deletion removes availability, not the fact of posting |
| `transmission_contemplated` | `YES` |
| `execute_or_prepare` | `UNKNOWN` |
| `audience` | `UNKNOWN` — **whose account?** |
| `channel` | `PUBLICATION` |

**Clarification.** Tone and length are **C1**: inferred, surfaced as assumptions. The account
question is **C4**: posting under the entity's name is a governed release; posting under the user's
personal account is not. That single question is asked; nothing else is.

**`ScopeResolution`.** Depends on the answer. Personal account → `PERSONAL / AD-HOC INITIATIVE`;
entity account → the organisation. **These are different scope families** (CS-2), so the answer
changes everything downstream.

**Assuming the entity's account:**

`WorkflowMatchAssessment` → `workflow.external_publication_preparation` is admissible and fits.
**MATCH.** The planner binds it at version and changes nothing about it (MC-6).

`RoleRequirement`: `role.institutional_communications_editorial_specialist`, `ALWAYS`.
`DecisionRequirement`: `decision.external_publication`, posture `REQUESTING_DECISION`.

**What the user sees:** "I'll draft a short professional post about the news. I've assumed a
professional register and about 150 words — tell me if you want something different. One thing I
need: post this from the company account or yours? From the company account it needs someone's
approval before it goes out."

**What they do not see:** a Workflow ID, a Role ID, a Decision Right ID, or a Model Profile.

**The point.** The request looks like C1 all the way through. The one question that matters is C4,
and a system tuned to "don't bother the user" would have posted under the wrong name.

---

## Example 2 — a difficult partner communication

> "Review this partner email. They blame us for the delay. Check whether they are right and prepare
> a firm but professional response. I do not want to damage the relationship."

**`WorkIntent`:** the request names two end results joined by *and* — *"check whether they are
right **and** prepare a … response"* — with **no stated priority** between them and no single
governing clause making one subordinate to the other. Tests 1 to 4 of RI-12 therefore do not
resolve a primary, and test 5 does:
`primary_work_mode` is **`UNKNOWN`** and `secondary_work_modes` is `{ANALYSIS, DRAFTING}` — the
complete set, not a remainder after a pick (RI-13). Nothing downstream supplies the primary later.
`act_direction` `EXTERNAL`;
`commitment_possible` `UNKNOWN` → planned as `YES` (WC-6) — a reply about delay responsibility can
concede; `execute_or_prepare` `PREPARE` ("prepare a response").

**`WorkRequirementSet`:** triggers **T-15** (contractual responsibility is in issue) and **T-16**
(external communication under the entity's name) both fire, and the contract value is **unresolved**
— the request states none and nothing in the resolved scope supplies one.

That combination is decided by **WC-3**, not by how the request reads: *where value is unknown **and**
a §4 trigger fires, the band is at least Enhanced Decision-Grade.* Two triggers have fired. So the
planning floor is **Enhanced Decision-Grade**, and it stays there until governing value or risk
information resolves otherwise under the approved policy — which is a fact arriving, not a judgement
the planner may make.

Three things this floor is **not**:

| Not | Because |
|---|---|
| Lowered because the request is short, plainly worded, or reads like ordinary correspondence | WC-4: a trigger fires on evidence, not on vocabulary. Wording is not evidence about value |
| Lowered because no value is stated | WC-3 exactly: absence of a stated value proves nothing, and with a trigger fired it raises the floor rather than leaving it open |
| A claim that the contract is large, or that any particular value applies | WC-7: planning conservatively is not asserting the conservative fact. The value remains `UNKNOWN`, recorded as `UNKNOWN` |

An earlier version of this exemplar set the floor one band lower and made it conditional on the
contract value turning out to be large. That inverted WC-3: it treated an unresolved value as a
reason to sit lower until something raised the band, where the approved rule makes an unresolved
value with a fired trigger a reason to sit higher until something resolves it.

**`RoleRequirement`s**

| Role | Owned conclusion | Activation |
|---|---|---|
| `role.knowledge_evidence_steward` | What the record shows about the delay | `ALWAYS` — "check whether they are right" is an evidence question |
| `role.legal_regulatory_lead` | Whether the contract allocates the delay | `CONDITIONAL` — **fires** |
| `role.programme_partnership_manager` | The partnership position | `CONDITIONAL` on the partner class |
| *communication strategy* | — | **No approved Role owns this at the Phase 13 baseline** |

**Not F-5.** The fourth row is not an approved Role that happens to be unavailable — the approved
universe has **no owner at all** for communication strategy in contested interactions. That is
`role-skill-requirement-inference.md` §6b, and the mode is **`F-14
NO_APPROVED_ROLE_OWNS_CONCLUSION`**, with no load-bearing determination to make (RS-12).

Whether it blocks is decided by **LB-0**, against the deliverable the user actually asked for:

> *"prepare a **firm but professional** response. **I do not want to damage the relationship.**"*

That is a communication-strategy conclusion, requested in terms. It is part of the original
deliverable before anything is narrowed, so the disposition is **BLOCK** + escalate.

**An earlier version of this exemplar got this wrong**, and the error is worth naming because it is
the one this predicate exists to prevent: it removed the communication-strategy conclusion, called
what remained the deliverable, and concluded from the remainder that the removed conclusion had not
been load-bearing. LB-6 now makes that a validation failure. A narrower plan — evidence position
plus legal position — is a perfectly good plan, and it is **not an answer to this request**;
offering it as one would be the silent scope change UX-5 and FE-1 forbid.

**What the user sees:** "I can check what the record shows about the delay and what the contract
says about responsibility — that part I can do properly. What I can't do is judge how firmly to put
it without damaging the relationship: nobody owns that conclusion in the approved system yet. Tell
me if you want the evidence and the legal position on their own, and I'll be explicit that the tone
call is yours."

The narrower plan below is what the user gets **if they ask for it** — a new `Request`, with a
deliverable that does not require the missing conclusion (RS-13). It is not what a blocked plan
quietly becomes.

**COMPOSE, on that narrower request** — no approved Workflow covers evidence analysis plus legal
position plus an external reply, so the narrower request would compose:

```text
S1  evidence intake        role.knowledge_evidence_steward
                           SOURCE: the email thread, at its versions
                           exit: each delay claim linked to EVIDENCE or marked UNKNOWN
S2  contractual position   role.legal_regulatory_lead   depends: S1
                           owns the conclusion; S3 carries it verbatim (never restated)
S3  drafting               <substantive owner>          depends: S1, S2
                           carries S1 and S2; makes no communication-strategy conclusion
S4  review                 review.legal_compliance          (no communication review: none applies
                                                            to a plan that makes no such conclusion)
S5  human gate             decision.external_publication   ← no Role participates (MC-13)
```

**The point.** Three of the four required conclusions have owners; the fourth does not, and the
user asked for it in terms. The honest result is a **block** that says so — not a draft produced by
whichever Role sounded closest, and not a narrower deliverable substituted for the requested one and
presented as complete.

---

## Example 3 — an investment / IFI request

> "Prepare me for a meeting with EIB about this municipal infrastructure project."

**Triggers:** T-1 (IFI), T-3 (municipal counterparty), T-4 (regulated infrastructure). **T-11 does
not fire.** T-11 is an *external submission* to a lender, investor, regulator, granting authority or
board, and a meeting is not a submission; calling it "submission-adjacent" would be claiming a
trigger the approved policy does not give, which is precisely what WC-4 forbids. What raises the
treatment instead is **conservative escalation**, and the plan says so as escalation rather than as
a fourth trigger: `commitment_possible` is `UNKNOWN` and routes to `YES` (WC-6), and WC-2 permits
raising a band and never lowering one. No value stated — and WC-3 says that does not make it
Routine. Band: **Enhanced Decision-Grade**, on three fired triggers plus that escalation.

Where a submission **is** actually contemplated — the meeting is to hand over an appraisal pack —
T-11 fires literally, on the submission, and is recorded as fired rather than as adjacency.

`commitment_possible`: `UNKNOWN` → planned as `YES`. A meeting with a lender can produce a
commitment, and the plan says what would need authority if one arises.

**`ScopeResolution`:** if two municipal projects are live, **`AMBIGUOUS_SCOPE`** — clarify and
block (CS-7). Assume one resolves.

**MATCH candidates:** `workflow.ifi_appraisal_readiness_preparation` and
`workflow.bankability_assessment` are both admissible and fit differently — the first prepares for
the institution, the second establishes financeability. Under **MC-5** this is a material ambiguity:
the planner asks *"is this about showing them the project is financeable, or about getting ready for
the conversation?"* — a question about the user's world, not about Workflow IDs (CL-7).

**Assuming appraisal readiness:** MATCH on
`workflow.ifi_appraisal_readiness_preparation` @ version, with `role.ifi_dfi_project_preparation_specialist`,
`role.funding_bankability_architect`, `role.financial_modelling_specialist`,
`role.technical_feasibility_lead` and `role.legal_regulatory_lead` as the Workflow declares —
unchanged (MC-6).

**`EvidenceRequirement`s:** the financial model at a version; the technical basis at a version; the
project's approved positions. Where the model is `STALE_AND_BLOCKING` for this use, **F-9** blocks
the **plan**, before the handoff — freshness is evaluated at the point of use, not at intake, and
Phase 15 has no stage to block (FE-11). Where the reference is one the approved intake check 7
accepts as `FUTURE_GOVERNANCE_REFERENCE`, it is carried as exactly that and the dependent act is
non-executable (FE-12); it is not a way to get a blocking requirement past the handoff.

**The point.** One sentence, three fired triggers plus a conservative escalation, a band the user
never mentioned, and a material
MATCH ambiguity that is resolved by a question about the meeting rather than about the registry.

---

## Example 4 — ambiguous authority

> "Send them confirmation that we accept the terms."

**`WorkIntent`:** `primary_work_mode` `ACTION` — RI-12 test 3, an explicit execution verb with
`commitment_possible = YES` — and `secondary_work_modes` empty; `act_direction`
`EXTERNAL`; `reversibility`
`IRREVERSIBLE`; `commitment_possible` `YES`; `transmission_contemplated` `YES`;
`execute_or_prepare` `EXECUTE`; `entities` — "them" `UNKNOWN`, "the terms" `UNKNOWN`.

**Three C4 clarifications** and one independent block:

| Question | Class |
|---|---|
| Which counterparty? | C4 — the Right and the scope both depend on it |
| Which terms, at which version? | C4 — accepting the wrong version is the failure this prevents |
| Send, or prepare for someone to send? | C4 (RI-6) |

**`ScopeResolution`:** `NO_VALID_SCOPE` while the counterparty is unresolved.

**`DecisionRequirement`:** an acceptance of terms is a commitment. The applicable approved Right is
resolved **first** (GP-3) — `decision.contract_commitment`, and additionally
`decision.external_publication` for the release itself, since the message goes outside the entity
under its name. Neither is exercised by the planner.

**Outcome:** **BLOCKED**, act posture `BLOCKED_FROM_TRANSMISSION`. Not a draft, not a send.

**What the user sees:** "I can't send this yet. Accepting terms commits the company, so it needs
approval from someone who holds that authority — and I don't know which counterparty or which
version of the terms you mean. Tell me those and I'll prepare it and route it for approval."

**The point.** The failure mode is not "refuses to help". It is refusing to **perform the act**
while doing all the work that does not require the authority — and saying so in a sentence the user
can act on.

---

## Example 5 — no exact Workflow exists

> "The regulator asked about our data handling on the grant-funded pilot. Pull together what we
> actually do, check it against the grant conditions and the DPA, and get me something I can send."

Four domains: evidence, grant compliance, data protection, external submission. No approved
Workflow covers the combination — `workflow.data_protection_impact_assessment_cycle` and
`workflow.grant_periodic_reporting_and_claim_preparation` each cover part and neither is admissible
whole.

**`WorkflowMatchAssessment`:** every candidate recorded with its rejection reason (MC-8). Outcome
`NO_MATCHING_WORKFLOW` → **F-3 → COMPOSE**.

```text
work_plan.<id>   scope: <the pilot>   criticality: Enhanced Decision-Grade (T-5, T-11, T-13)

S1  evidence intake            role.knowledge_evidence_steward
S2  grant-condition check      role.grant_financial_compliance_budget_specialist   depends: S1
S3  data-protection position   role.data_protection_gdpr_specialist                depends: S1
S4  drafting                   role.deliverables_reporting_specialist   depends: S2, S3
                               carries S2 and S3 verbatim
S5  independent review         review.data_protection  +  review.grant_compliance
S6  human gate                 decision.external_publication            ← no Role participates
```

Once the plan has **passed preflight** — and not before, because a spec derives only from a
validated stage (PL-8, step 12) — each validated stage may yield one
`planned_work_item_spec.<id>`. **No `work_item.<id>` is created here**, and no Task is defined here
(N-11, HO-6): `TASK != PLANNED WORK ITEM SPEC != WORK ITEM`. The specs carry no run reference, no
assignment, no execution status and no model.

**What happens to them today: nothing.** No approved Phase 11 contract defines a
`PlannedWorkItemSpec` as an intake object, so this exemplar does not claim the Orchestrator reads
one, re-validates one, or instantiates anything from one (HO-14). They are non-runtime planning
output. Carrying them across the boundary at all would need an approved execution-basis contract
that permits it, and none exists — which is PO-4, unchanged and unresolved by their existence
(HO-16).

**`work_plan.<id>` is not `workflow.<id>`** (MC-14). It is bound to this request, this scope, this
moment. Running the same request tomorrow produces a second plan, and the two are separate records
even if identical (MC-15). Nothing writes it to the registry, and passing preflight does not approve
it (MC-16).

**The point.** COMPOSE produces something that looks like a Workflow and is structurally not one —
and the difference is enforced by identity space and by the absence of any write path, not by a
convention.

---

## Example 6 — a repeated pattern

Over three months the planner composes four plans with a similar shape: evidence intake → a domain
position → drafting → review → external gate. Three validated; one was **blocked** at F-8.

The planner emits one `workflow_candidate.<id>`:

| Field | Content |
|---|---|
| `status` | `PROPOSED` — the only permitted value |
| `observed_plans` | The four, at their versions — **including the blocked one** (WL-8) |
| `common_structure` | The five-stage shape |
| `divergences` | **Two plans put the human gate before review; two after.** The pattern does not agree with itself on the thing that matters most |
| `scope_span` | Three of four came from one programme — weak evidence of organisational reusability (WL-7) |
| `granularity_assessment` | Meets the Phase 5 bar on stages and Roles; the gate placement is unsettled |
| `is_approved` | `false` |
| `is_matchable` | `false` |

**Nothing else happens.** The suggestion is not matched against (WL-3), does not influence any plan,
and cannot become a Workflow inside Phase 15 — there is no transition and no actor with the
authority (WL-4). A human may take it into Phase 5 change control as input material, where it earns
no shortcut for having been machine-generated (WL-9).

**The point.** The `divergences` row is the value. Four plans that "mostly agree" disagree about
whether a human decides before or after independent review — which is a governance question, and
exactly the thing an auto-registered pattern would have silently resolved by majority.

## Non-Runtime Statement

These exemplars are declarative architecture. They specify no implementation, contain no executable
fixture, and bind no provider or runtime technology. None has been executed.
