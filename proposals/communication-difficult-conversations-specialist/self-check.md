# Package Self-Check

Status: `PROPOSED`
Version: 0.1

> **This is a producer self-check.** The party that wrote a package is the last party who should
> certify it. What follows records what was checked and what was found; it approves nothing and
> replaces no independent review.

## 1. Non-production status

| Claim | Status |
|---|---|
| Any artifact in this package is `APPROVED` or `CANONICAL` | **No.** All 20 are `PROPOSED` |
| Any Decision Right is created, widened, mapped or approved | **No** |
| Any approved Phase 1–13 artifact is modified | **No.** The package is 20 new files in one new directory |
| Any runtime code, provider integration, schema, API, queue, worker, scheduler or infrastructure is specified | **No** |
| A permanent autonomous agent is created | **No** (`runtime-prompt-assembly.md` PA-5) |
| Phase 14 approval or production readiness is claimed | **No** |
| Anything in this package has been executed | **No.** No fixture exists and no run has been made |

## 2. Completeness against the required package

All twenty artifacts exist:

| # | Required | File | Present |
|---:|---|---|:---:|
| 1 | Package map, provenance, non-goals, governance boundary | `README.md` | ✓ |
| 2 | Role Card candidate | `role-card.md` | ✓ |
| 3 | Methodology | `methodology-card.md` | ✓ |
| 4 | Skill pack | `skill-pack.md` | ✓ |
| 5 | Primary workflow | `workflow-difficult-interaction-response.md` | ✓ |
| 6 | Meeting preparation | `workflow-meeting-preparation.md` | ✓ |
| 7 | Boundary setting | `workflow-boundary-setting.md` | ✓ |
| 8 | Refusal | `workflow-refusal.md` | ✓ |
| 9 | Formal escalation | `workflow-formal-escalation.md` | ✓ |
| 10 | Thread diagnostics | `workflow-thread-diagnostics.md` | ✓ |
| 11 | Communication strategy review profile | `review-profile-communication-strategy.md` | ✓ |
| 12 | High-stakes external communication review profile | `review-profile-high-stakes-external-communication.md` | ✓ |
| 13 | Trigger / routing spec | `trigger-routing-spec.md` | ✓ |
| 14 | Communication Control Filter | `communication-control-filter.md` | ✓ |
| 15 | Diagnostics contract | `conversation-diagnostics-contract.md` | ✓ |
| 16 | Runtime prompt assembly | `runtime-prompt-assembly.md` | ✓ |
| 17 | Decision Right gap analysis | `decision-right-gap-analysis.md` | ✓ |
| 18 | Evaluation spec | `evaluation-spec.md` | ✓ |
| 19 | Examples | `examples.md` | ✓ |
| 20 | Self-check | `self-check.md` | ✓ |
| 21 | Governance decision note *(added in remediation)* | `governance-decision-note.md` | ✓ |

## 3. Reference integrity — checked, not asserted

Every `role.<id>`, `skill.<id>`, `review.<id>` and `decision.<id>` cited in this package was
resolved against the approved registries under `roles/`, `skills/`, `reviews/` and `decisions/`.

| Class | Cited | Resolve to an existing registry entry | Deliberate candidates, not registry entries |
|---|---:|---:|---|
| `role.<id>` | 23 | 22 | `role.communication_difficult_conversations_specialist` |
| `skill.<id>` | 30 | 22 | the 8 candidates listed in `skill-pack.md` |
| `review.<id>` | 10 | 8 | `review.communication_strategy`, `review.high_stakes_external_communication` |
| `decision.<id>` | 14 | 13 | `decision.external_high_stakes_communication_send`, **withdrawn** |

**Every unresolved identifier is one this package explicitly proposes**, and each is marked
`PROPOSED` at every point of use — except
`decision.external_high_stakes_communication_send`, which is
**`WITHDRAWN_FROM_CURRENT_PACKAGE`** and appears only where the withdrawal is recorded. No
identifier is cited as if it existed when it does not.

The inherited standards cited — `standard.role.common_constraints@0.2`,
`standard.skill.common_constraints@0.1`, `standard.workflow.common_constraints@0.1`,
`standard.review.common_constraints@0.1` — all resolve.

## 4. Authority checks

| Check | Result |
|---|---|
| Does any artifact create, widen, map or infer a Decision Right? | No. `decision-right-gap-analysis.md` DG-3 states the one candidate confers no authority and is not exercisable |
| Does any artifact treat a review as a gate? | No. Each Review Profile's Decision Right Boundary states it neither exercises nor satisfies a Right |
| Does any artifact treat the filter as a review or approval? | No. `communication-control-filter.md` CF-6 to CF-9, and the three `false` flags in its recorded output |
| Does any artifact treat a routing score as authority? | No. `trigger-routing-spec.md` TR-7 to TR-10 |
| Is the fail-closed behaviour specified? | Yes, and **in the right order**: DG-5 resolves the applicable approved Right first, and only a genuinely empty result blocks with `AUTHORITY_ABSENT`. DG-5a states that this is not the resting state |
| Is "no gate needed" distinguished from "no authority exists"? | Yes. DC-7's three statuses; `NOT_APPLICABLE` with `NO_EXTERNAL_ACT_CONTEMPLATED` for a read-only artifact, and DC-7a stops it travelling |
| Is there one review trigger? | Yes. RC-5, four conditions, owned by the Role Card; the Profile and every workflow reference it and none restates a narrower one |
| Is the epistemic model the approved one? | Yes. `FACT_CLAIM`, not `FACT`; source stays `SOURCE`; a claim is a new linked item with its own `EVIDENCE` (RC-4, DC-4) |
| Can the Role transmit anything? | No. `role-card.md` authority limit 1; every workflow's S-gate stage has **no Role participation** |
| Does any artifact permit overriding a domain conclusion? | No. RC-1, TR-12, HF-8, and `review.communication_strategy@0.1`'s `CRITICAL_FINDING` list |
| Is "no Right forbids it" excluded as a basis? | Yes. DG-6 |
| Are uncarded candidate Rights excluded as usable gates? | Yes. DG-7 — this is a stricter position than the source brief took |

## 5. Invariant checks

| Invariant | Where held | Held? |
|---|---|:---:|
| ROLE != AGENT INSTANCE | `runtime-prompt-assembly.md` PA-5, PA-6; `trigger-routing-spec.md` TR-9 | ✓ |
| MODEL != ROLE | TR-8; PA-8 | ✓ |
| ROUTER != ORCHESTRATOR | TR-8 | ✓ |
| REVIEW PROFILE != REVIEW INSTANCE | Both Profiles define profiles; neither creates or pre-satisfies an instance | ✓ |
| DECISION RIGHT != DECISION RECORD | DG-3; no Decision Record is written anywhere in the package | ✓ |
| KNOWLEDGE != CANONICAL RECORD | `role-card.md` §Evidence — outputs stop at `DRAFT`; pattern labels are `AI_SUGGESTION` | ✓ |
| CREDENTIAL != HUMAN AUTHORITY | `role-card.md` authority limit 1; `decision-right-gap-analysis.md` §7 | ✓ |
| External send authority human-only where an applicable Right requires it | DG-1, DG-5; every workflow gate stage | ✓ |
| Missing authority fails closed | DG-5 | ✓ |
| No celebrity impersonation or endorsement | `README.md` CP-1, CP-2; `methodology-card.md` S-6; `evaluation-spec.md` HF-3; `runtime-prompt-assembly.md` A7 | ✓ |

## 6. Governance items — two decided, six open

OG-1 and OG-2 were decided by a human governance authority on 2026-09-15
(`human-governance-decisions-og1-og2.md`, commit `903c58dfa565f5f14a9af19efcccceabae328f26`) and
are recorded here as decided. The rest are recorded, not resolved: each requires a governance
decision this package must not make for itself.

| # | Gap | Why it is not resolved here |
|---:|---|---|
| **OG-1** | ~~Identifier-shape divergence~~ | **`HUMAN DECISION RECORDED: NORMALIZE IDENTIFIERS`**, 2026-09-15, commit `903c58df`. Applied: one canonical identifier per candidate object, in the approved registry shape; the dual-identity lines removed; the prompt-fixed IDs kept as traceability metadata in `README.md` §7. Normalising approved nothing |
| **OG-2** | ~~Role vs specialisation~~ | **`HUMAN DECISION RECORDED: PROFESSIONAL DELIVERY ROLE`**, 2026-09-15, commit `903c58df`. The capability is a candidate Professional Delivery Role, proposed as the 60th, subject to the normal Role Registry, Skill Registry, mapping, review and approval process. The approved universe remains **59 Roles**; `roles/master-role-universe.md` is untouched. Deciding registered nothing |
| **OG-3** | ~~The TA-7 Decision Right~~ | **Closed, not resolved by decision.** The gap was an error: the approved subject of `decision.external_publication` contains no publicity element, so TA-7 is covered. The candidate is withdrawn (`governance-decision-note.md` §4) |
| **OG-4** | **Uncarded adjacent Rights.** `decision.disclosure_authorisation`, `decision.external_data_transmission` and `decision.legal_filing_or_representation` | Those carding decisions are Phase 7's. Their absence leaves **no act ungated** — the release Right gates the act — but leaves three act classes with fewer controls than a mature register would apply |
| **OG-5** | **Eight candidate skills.** None exists in the approved skill universe | **Open, and unchanged by OG-2.** Reassessed after the Role decision: deciding that a Role owns the capability says nothing about whether the eight Skills exist, and none of them does. Skill Registry change control. `skill-pack.md` SP-1 makes the pack non-activatable while any Required Skill is a candidate, and §6a records what the Role decision did and did not move |
| **OG-6** | **No *authoritative* Role-to-Skill mapping record exists.** | **Partially advanced, not closed.** The Role decision made the mapping writable as a proposal: `role-skill-mapping-candidates.md` now states which Skills the Role requires and on what basis. That document is a **candidate proposal surface**, not a Phase 4 mapping record, and it authorises no activation. Phase 4 mapping remains its own governed act |
| **OG-7** | **Routing weights are declared, not validated.** | `trigger-routing-spec.md` §9 and `evaluation-spec.md` §7. They must not be treated as settled before the suite runs |
| **OG-8** | **No full-Profile reviewer exists for the high-stakes review.** No approved Role's scope spans legal, institutional, data-protection, integrity, risk and communication criteria | **Open, and only partly touched by OG-2.** Reassessed: the Role decision supplies a candidate full-Profile reviewer for `review.communication_strategy@0.1` — *once the Role is registered and approved, which it is not*. It supplies nothing for the high-stakes Profile, whose criteria still span five domains no single Role covers. Satisfaction requires per-dimension coverage; inventing a full-Profile reviewer would be the error |

### 6a. Mechanical reassessment of OG-5, OG-6 and OG-8 after OG-2

The decision changes what is *possible*, not what *exists*. Read strictly:

| Item | What OG-2 changed | What it did not change | Status |
|---|---|---|---|
| **OG-5** — eight candidate Skills | Nothing. A Role owning the capability does not bring a Skill into existence | All eight remain candidates in no approved registry; the pack stays non-activatable (SP-1) | **Open** |
| **OG-6** — Role-to-Skill mapping | The mapping is now writable as a **candidate proposal**, because there is a decided Role to map from. `role-skill-mapping-candidates.md` records it | No mapping is authoritative. Phase 4 mapping is a separate governed act, and a proposal-side document is explicitly not the authoritative source | **Advanced, not closed** |
| **OG-8** — full-Profile reviewer | For `review.communication_strategy@0.1`, a candidate full-Profile reviewer now exists *in candidate form* — conditional on Role registration and approval, neither of which has happened | For `review.high_stakes_external_communication@0.1`, nothing. Its criteria span legal, institutional, data-protection, integrity and risk dimensions, and no Role covers all five | **Open** |

**Not closed, and not reassessed here:**

| Item | Why it stays exactly as it was |
|---|---|
| **OG-4** — uncarded adjacent Rights | A Phase 7 matter. The approved Phase 7 register has not changed, so neither has this |
| **OG-7** — routing weights declared, not validated | An evidence question. No evaluation has run against a built capability, so no evidence exists to close it with |

## 7. Scope-creep checks

| Risk | Check | Result |
|---|---|---|
| The Role acquiring domain ownership | Its `Does Not Own` list, RC-1, and the co-activation table TR-11 | No domain conclusion is owned or reachable |
| A "communication review" becoming a mega-review | Each Profile's `Does Not Check` list names the neighbouring `review.<id>` | Both lists are populated and point at real Profiles |
| The high-stakes Profile absorbing its prerequisites | Its Method section forbids re-performing domain analysis | Explicit |
| The diagnostic vocabulary drifting toward diagnosis | `conversation-diagnostics-contract.md` §5 closed label set, DC-12, DC-13 | Closed set with a normative "Never means" column |
| The filter becoming a gate | CF-6; S9 and S11 are separate stages in the primary workflow | Separated by construction |
| Thread diagnostics acquiring a drafting stage | That workflow's Versioning section forbids it in any future version | Explicit |
| The package approving its own Decision Right | DG-3, and §7 of that document | Refused, with the reason stated |
| A new Role being created where a specialisation would do | **OG-2 — decided by a human authority**, Professional Delivery Role. See below | Decided; the Role is still a candidate and still unregistered |

**On OG-2, what was decided and what it cost.** The human decision adopted the Role. The reasoning
the package had offered is preserved below unchanged, because a decision does not retroactively make
the argument for it stronger, and a reviewer should be able to see what the decision was made on.
This package proposed a Role because the
capability owns a recurring standalone professional artifact (a communication strategy), issues a
professional conclusion of its own, and operates across domains rather than inside one — the three
conditions `skills/_templates/skill-pack-template.md` names as the trigger to reassess *toward* the
Role Registry. The cost is a 60th Role in a universe of 59, with the discoverability and maintenance
burden that carries. The alternative — attaching the pack to an existing owning Role — is cheaper
and weakens cross-domain discoverability, which is precisely where difficult-conversation work
arises. **The package stated its preference and did not decide.** A human authority decided, and
the cost named here — a 60th Role, its mappings, its maintenance — is now a cost the package
carries rather than a risk it flags.

## 8. Safety checks

| Check | Result |
|---|---|
| Is psychological or clinical assessment prohibited? | Yes, in four places: `role-card.md` limit 3, `methodology-card.md` S-1, DC-13, HF-2 |
| Is the prohibition backed by an alternative vocabulary? | Yes — the closed label set of DC §5, with hedging required |
| Are manipulation and coercion excluded categorically? | Yes. S-2, S-3, HF-9. Not "used sparingly" — out of scope |
| Is fabrication prohibited, with a specified alternative? | Yes. S-4, HF-1; named placeholders, and `[X]` form throughout `examples.md` |
| Can de-escalation weaken a protection? | No. P-15, MC-3, CF-8, and the `protection_conflicts` field that makes a refusal-to-soften visible |
| Is the non-therapy boundary stated? | Yes. `role-card.md` limit 4, S-1 |
| Is cross-scope carry prevented? | Yes. `role-card.md` §Context Breadth Limit, PA-6, HF-13 |
| Is privileged material protected from audience widening? | Yes. `role-card.md` §Sensitive Information Controls; the high-stakes Profile's disclosure-scope check |
| Is a hostile message read for facts before tone? | Yes. RC-3, S-7, DC-5, HF-14, and worked case `examples.md` §6.1 |

## 11. The independent review findings, and how each was closed

| # | Finding | Closed by |
|---:|---|---|
| 1 | Deprecated `FACT` vocabulary and a `SOURCE` → claim mutation in new contracts | **RC-4** and **DC-4**: the record stays `SOURCE`, an extraction is `EVIDENCE` bound to its location, and an assertion is a **new linked** `FACT_CLAIM`. Swept across the Role Card, skill pack, all six workflows, the diagnostics contract, the filter and the evaluation suite. `no deprecated FACT vocabulary is active` and `no SOURCE-to-claim epistemic mutation is described` fail if either returns |
| 2 | Two different review triggers | **RC-5** is the single trigger, four conditions, owned by the Role Card. The Review Profile's Applicability now maps to RC-5.1–RC-5.4 rather than restating a variant, and every workflow's review stage references it. **RC-5a**: stakes never lower the obligation. The validator parses RC-5 and fails any document stating a narrower trigger |
| 3 | A read-only diagnosis forced to report `AUTHORITY_ABSENT` | **DC-7**'s three statuses, with `NOT_APPLICABLE` + `NO_EXTERNAL_ACT_CONTEMPLATED` for an artifact that contemplates no external act, and **DC-7a** stopping it from travelling to a workflow that does. **TD-1** states it from the workflow's side |
| 4 | A nine-field object presented as the ten-factor filter | Two namespaces — `communication_control_filter` (exactly the ten factors and the seven derived figures) and `diagnostic_risks` (seven risk dimensions, its own names). **DC-13a** explains why `escalation_risk` legitimately appears in both and is a different number in each. The validator compares the factor names **both directions** and rejects a collision |
| 5 | TA-7 misread as outside `decision.external_publication` | **The approved subject has four elements and publicity is not one of them.** TA-1…TA-7 all resolve to that Right, with submission and commitment Rights applying **in addition** where the act also does those things. The candidate Right is `WITHDRAWN_FROM_CURRENT_PACKAGE`. **DG-3**: a Right's name is not its subject |
| 6 | The evaluation suite missed all of the above | Six new scenarios (E31–E36), six new hard fails (HF-15–HF-20) and two new positive controls (PC-6, PC-7), each keyed to one of the findings. HF-15 and HF-17 are the two the first revision would have failed |
| 7 | OG-1 and OG-2 need human decisions | `governance-decision-note.md` set out options, consequences and a recommendation for each and decided neither. A human governance authority decided both on 2026-09-15 (`human-governance-decisions-og1-og2.md`, commit `903c58df`), and the package now records them as **`HUMAN DECISION RECORDED`**. The validator fails if the note or the package decides a governance item for itself, and fails if either status drifts back to undecided |

## 12. Package assurance tooling

| Item | Count |
|---|---|
| Package validator | `validation/communication_package_validation.py` — **22 checks** in 9 groups |
| Package mutation fixture | `validation/communication_package_probes.py` — **32 committed controlled weakenings**, 32 `DETECTED`, 0 `REDUNDANT`, 0 `ERROR` |

Three checks and eleven probes were added when the OG-1 and OG-2 human decisions were applied:
identifier normalization (one canonical form per object, no dotted survivors, no second identity,
historical IDs disclaimed), the candidate Professional Delivery Role and its candidate mapping, and
the decision record's own boundary — that it approves OG-1 and OG-2 and nothing else.

Each probe weakens one rule in a temporary copy and re-runs the validator; classification is from
executed behaviour, and a probe whose target text is not found is an **error**, not a skip.
Containment checks read git state and cannot be evaluated in a temporary tree, so their verdicts
are **discarded** (`GIT_DEPENDENT`) — counting them would make every probe look detected by an
artefact of the harness.

**Two of the eleven new probes were `REDUNDANT` on their first run**, and both exposed a weakness
in the checks rather than in the package:

1. **The Role Card's Role Type reverted to "Specialisation" and was not caught.** The check tested
   whether the phrase "Professional Delivery Role" appeared anywhere in the card — and it still did,
   in the decision blockquote above the Identity section. The Identity line is what a reader and a
   registry pass actually take the type from, so that line is now parsed on its own and rejected if
   it names a specialisation.
2. **The candidate Skills were presented as activatable and were not caught.** The check confirmed
   that each Skill was *listed* as a candidate and that the fail-closed rule existed; it never read
   the block that says none of them exists. That block is now read directly.

Both are the same class of error: a check satisfied by the rule surviving *somewhere* while the
place a reader looks had been weakened.

**Three earlier probes were `REDUNDANT` on their first run**, and all three exposed a weakness in
the checks rather than in the package: a lowercase-only scan that could not see a filter factor
smuggled into the risk namespace in its own casing; a review-trigger scan keyed on the word
"review" that could not see a stage's `Mandatory at:` line narrowed without it; and a paragraph
merge that let one bullet's qualifier exempt the bullet beside it. All three are fixed, and the
third changed how the harness reads prose: **a bullet is now its own statement.**

## 9. What this self-check did **not** check

1. **Whether the specification is correct.** Whether the role boundary is drawn in the right place,
   whether the ten filter factors are the right ten, whether the routing weights are sane, and
   whether the closed label set is complete are questions for an independent review.
2. **Whether the capability would behave as specified.** Nothing has been executed; no fixture
   exists.
3. **Whether the attribution wording is legally sufficient.** `README.md` §3 states a wording and a
   disclaimer. Whether that is adequate in a given jurisdiction is a legal question this package
   does not answer and must not be read as answering.
4. **Whether a 60th Role is the right structural answer** — OG-2 is **decided**, and this
   self-check cannot tell you whether the decision was right. It records that a human authority
   made it, on the reasoning in `governance-decision-note.md` §3, and that the reasoning was held
   weakly by its own author.
5. **Whether the eight candidate skills are the right decomposition.** They are the capabilities
   the methodology needs; whether they are eight skills or three is a Skill Registry question.
6. **Whether the approved registries themselves are complete.** The reference check in §3 confirms
   that cited identifiers exist. It does not confirm that the right ones were cited.

## 10. Honest limitations of the package as a whole

- **The previous version of this list was wrong**, and it is worth reading what it said: it stated
  that the capability could draft a final warning to a partner and then be unable to send it,
  because no carded Right covered TA-7. That limitation did not exist — it was manufactured by a
  misreading of an approved subject, and it was recorded here as a virtue ("stated rather than
  engineered around"). A self-check that presents its own error as rigour is the failure mode this
  document is most exposed to.
- What is actually true: every transmitting act resolves to a carded Right, and the human holding
  it decides. Three adjacent Phase 7 candidates remain uncarded, which leaves those act classes
  with **fewer controls**, not ungated.
- The pack is not activatable while any Required Skill is a candidate (SP-1), and no **authoritative**
  Role-to-Skill mapping record exists (OG-6) — the candidate mapping in
  `role-skill-mapping-candidates.md` is a proposal surface and authorises nothing. In its current
  state the package specifies a capability that cannot yet be run at all, and the two governance
  decisions did not change that.
- The high-stakes review has no full-Profile reviewer (OG-8), so its satisfaction depends on
  assembling per-dimension coverage every time.
- The routing weights are guesses with a rationale (OG-7).

Each of these is a reason for a governance reviewer to look harder, not a reason to treat the
package as nearly done.
