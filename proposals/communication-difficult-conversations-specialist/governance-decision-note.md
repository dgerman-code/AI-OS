# Governance Decision Note

Status: `PROPOSED`
Version: 0.1
Governance Owner: AI-OS architecture governance

> This note **decides nothing**. It set out two questions that required human governance
> authority, with options, consequences and a recommendation. **A human governance authority has
> since decided both**, in `human-governance-decisions-og1-og2.md` (decision date 2026-09-15,
> commit `903c58dfa565f5f14a9af19efcccceabae328f26`). This note records those decisions; it did
> not make them, and it creates no Decision Right, promotes no artifact and approves nothing.
> Neither decision approves the package, activates any capability, or makes any runtime claim.

## 1. Why this note exists

The independent review of package baseline `81623de` returned `FAIL`. Most findings were
specification errors, and those are remediated in the package itself. Two are not errors: they are
**choices**, and a proposal that made them for itself would be exercising authority it does not
have.

A third item — the withdrawn candidate Decision Right — is recorded in §4 because governance
should see what was withdrawn and why, not because a decision is needed on it.

## 2. OG-1 — identifier shape

### The question

Should this package's candidate identifiers keep the **dotted namespace** form fixed by the
originating prompt, or be **normalised** to the shape the approved Phase 4 and Phase 5 templates
use?

| | Dotted form (as written) | Normalised form |
|---|---|---|
| Skill pack | `skill_pack.communication_difficult_conversations@0.1` | `skill_pack.communication_difficult_conversations@0.1` |
| Methodology | `method.communication_calm_direct_control@0.1` | `method.communication_calm_direct_control@0.1` |
| Workflows | `workflow.communication_difficult_interaction_response@0.1` | `workflow.communication_difficult_interaction_response@0.1` |
| Reviews | `review.communication_strategy@0.1` | already conformant |

### Is the answer mechanical?

**No, but it is close.** `skills/_templates/skill-pack-template.md` states `Pack ID:
skill_pack.<id>`; `workflows/_templates/workflow-card-template.md` states `Workflow ID:
workflow.<stable_snake_case_name>`; `reviews/_templates/review-profile-card-template.md` states
`review.<stable_snake_case_name>`. Every carded example in the approved registries follows those
shapes, and **no** approved artifact uses a dotted namespace segment.

What stops this being mechanical is that the templates are themselves `PROPOSED — Phase 4/5
standard candidate`, and the package's dotted IDs were fixed by the prompt that commissioned it.
A drafting agent normalising a prompt-fixed identifier is making a governance choice quietly, which
is the thing this note exists to avoid.

### Options

**A — keep the dotted IDs.** Consequence: the registry acquires two identifier conventions. Every
future validator, mapping record and cross-reference has to handle both, and "which convention does
this object use" becomes a question a reader must ask. There is no compatibility reason to pay
that: nothing has been built against these IDs.

**B — normalise to the approved shape.** Consequence: this package's IDs change once, before
anything depends on them, and the registry keeps one convention. The prompt's IDs remain traceable
as the originating text. Cost: a mechanical rename across the package and its cross-references.

### Recommendation

**Option B.** One canonical convention, normalised now while the cost is a rename rather than a
migration. Dual canonical identities are a defect that compounds; the only argument for A is that
the prompt said so, and the prompt did not know it was choosing a second convention.

### Status

**`HUMAN DECISION RECORDED: NORMALIZE IDENTIFIERS`** — OG-1, decided 2026-09-15 by the human
governance authority, recorded in `human-governance-decisions-og1-og2.md` at commit
`903c58dfa565f5f14a9af19efcccceabae328f26`. **Option B.**

Applied in the package: every candidate object now carries exactly one canonical identifier in the
approved registry shape, and the dual-identity lines are removed. The prompt-fixed IDs are recorded
as traceability metadata in `README.md` §7 and resolve to nothing.

**The earlier baseline was right to defer this.** At `9686c90` the package used the prompt's IDs
and recorded the divergence rather than normalising it, because a drafting agent normalising a
prompt-fixed identifier would have been making this governance choice quietly. That was the correct
posture then; it is superseded now by a decision, not by a better argument.

## 3. OG-2 — Role versus Specialisation

### The question

Should this capability be registered as a **new Professional Delivery Role** — the 60th in a
universe of 59 — or modelled as a **Specialisation / methodology pack** attached to one or more
existing Roles?

### Criteria, applied honestly

| Criterion | Reading | Favours |
|---|---|---|
| **Independent domain ownership** | It owns communication strategy, framing, triage and boundary formulation — a domain no existing Role's `Owns` list covers | Role |
| **Stable output responsibility** | It owns five recurring artifacts (diagnostic, strategy, draft, brief, escalation recommendation) that persist beyond one assignment | Role |
| **Unique competency boundary** | Difficult-conversation diagnosis and non-response strategy are not editorial, marketing, stakeholder or people competencies | Role |
| **Need for independent review eligibility** | `review.communication_strategy@0.1` needs a full-Profile reviewer, and no existing Role's scope covers its satisfaction criteria | Role |
| **Overlap with existing Roles** | Real overlap with `role.institutional_communications_editorial_specialist` (public voice), `role.institutional_affairs_stakeholder_specialist` (institutional relationships), `role.people_organisation_specialist` (employment matters), `role.marketing_growth_specialist` (external commercial messaging) — but each owns its **domain's** communication, not contested interaction as such | Mixed |
| **Cross-domain reuse without substantive authority** | The capability is needed in legal, procurement, grant, partnership and employment contexts alike, and must carry **no** substantive authority in any of them | **Specialisation** |
| **Governance surface** | A 60th Role adds a Role Card, mapping records, review eligibility rows and a maintenance obligation to the universe | **Specialisation** |

The last two are the real argument for B, and they are not weak: a capability that must work
everywhere and own nothing substantively is exactly the shape a pack has.

### Options

**A — a new Professional Delivery Role.** Discoverable for cross-domain work; owns its artifacts
and its professional conclusion cleanly; can be a full-Profile reviewer for its own Review Profile.
Cost: a 60th Role, its mappings, and the precedent that a cross-cutting capability gets a Role.

**B — a Specialisation / pack on existing Roles.** No new Role; the methodology and pack attach to
`role.institutional_communications_editorial_specialist`,
`role.institutional_affairs_stakeholder_specialist`, `role.people_organisation_specialist` and
others. Cost: **no owner for the artifacts** — a Conversation Diagnostic produced under an
editorial Role is owned by a Role whose card does not list it; **no full-Profile reviewer** for
`review.communication_strategy@0.1`; and cross-domain discoverability drops, because a lawyer
handling a hostile counterparty has to know that the editorial Role's pack is where the capability
lives.

### Recommendation

**Option A, weakly held.** The deciding criterion is `skills/_templates/skill-pack-template.md`'s
own reclassification warning: *if the pack begins to own a recurring standalone professional
artifact, professional conclusion or authority boundary independent of an assigned Role, stop and
reassess whether the capability belongs in the Role Registry instead.* This capability does own
five such artifacts and issues its own professional conclusion, which is the stated trigger to move
toward the Role Registry rather than away from it.

It is held weakly because the governance-surface argument is real and because Option B's costs are
solvable — an existing Role could take ownership of the artifacts, and the Review Profile could be
restructured around bounded contributors. That is a redesign, not a relabelling, and it is
governance's call, not this package's.

### Status

**`HUMAN DECISION RECORDED: PROFESSIONAL DELIVERY ROLE`** — OG-2, decided 2026-09-15 by the human
governance authority, recorded in `human-governance-decisions-og1-og2.md` at commit
`903c58dfa565f5f14a9af19efcccceabae328f26`. **Option A.**

The capability is modelled as a candidate **Professional Delivery Role**, proposed as the 60th in
the Role universe, subject to the normal Role Registry, Skill Registry, mapping, review and
approval process.

**What the decision does not do**, stated because a recorded decision is the easiest thing in a
package to over-read: it does not register the Role, does not approve it, does not activate it,
does not make it assignable, and does not add it to the approved Role universe — which remains 59
approved Roles. `roles/master-role-universe.md` is untouched by this package. No Role is created,
registered or approved here. The Role Card remains a **candidate** and says so in its first line.

**The earlier baseline was right to defer this too.** Recommending Option A while leaving the
choice open was the correct posture for a proposal that does not hold Role Registry authority.

## 4. Recorded for governance: the withdrawn candidate Decision Right

Not a decision item — a correction that governance should see.

Package revision 1 proposed `decision.external_high_stakes_communication_send` on the reasoning
that private high-stakes correspondence fell outside `decision.external_publication` because it is
"neither published nor available".

**That reasoning was wrong.** The approved Decision Subject is *"release of one content item, at a
stated version, to an audience outside the entity, under the entity's name"* — four elements, none
of them publicity. The analysis added a fifth condition the card does not contain, and then found a
gap produced entirely by the addition. A private letter sent in the entity's name satisfies all
four elements.

The candidate is **`WITHDRAWN_FROM_CURRENT_PACKAGE`**. It confers no authority and is not proposed.
`decision-right-gap-analysis.md` §5 records the reassessment in full.

**What governance may still wish to note**, without any action from this package: three adjacent
Phase 7 candidates remain uncarded — `decision.disclosure_authorisation`,
`decision.external_data_transmission` and `decision.legal_filing_or_representation`. Their absence
leaves **no act ungated**, because the release Right gates the act. It leaves three act classes
with fewer controls than a mature register would apply. That is a Phase 7 observation, and this
package does not fill it.

## 5. The remaining open items

`self-check.md` §6 carries OG-3 through OG-8. None requires a decision in this note:

| # | Item | Why it is not here |
|---:|---|---|
| OG-3 | The TA-7 Decision Right | **Closed** by the §4 reassessment — the Right was withdrawn, not decided |
| OG-4 | Uncarded adjacent Rights | Recorded in §4; a Phase 7 matter |
| OG-5 | Eight candidate Skills | Skill Registry change control; mechanical once OG-1 and OG-2 are decided |
| OG-6 | No Role-to-Skill mapping records exist | Follows OG-2 |
| OG-7 | Routing weights are declared, not validated | An evidence question, not an authority question |
| OG-8 | No full-Profile reviewer for the high-stakes review | Recorded deliberately; follows OG-2 |

## 6. What the decisions on OG-1 and OG-2 unblocked, and what they did not

Neither decision makes the package approvable. Both were prerequisites to work that is now done or
now possible:

| Now done in the package | Now possible, and still outside it |
|---|---|
| Identifiers normalised to one canonical shape each (OG-1) | Registering the eight candidate Skills — Skill Registry change control (OG-5) |
| The Role modelled as a candidate Professional Delivery Role, aligned to the Role Card standard (OG-2) | Registering the Role — Role Registry change control |
| Candidate Role-to-Skill mapping recorded as a proposal surface (`role-skill-mapping-candidates.md`) | Making any of those mappings authoritative — Phase 4 mapping is its own governed act (OG-6) |
| The full-Profile reviewer question re-read against the Role decision (OG-8) | Approving a reviewer path for the high-stakes Profile |

What remains true is what mattered before either decision: **the package specifies a capability
nobody has executed.** No Skill exists, no mapping is authoritative, no evaluation has run against a
built capability, and nothing here is approved.

## 7. Non-Runtime Statement

This note is declarative governance material. It specifies no implementation, binds no person or
runtime, and confers no authority on anyone or anything.
