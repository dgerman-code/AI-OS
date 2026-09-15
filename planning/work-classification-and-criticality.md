# Work Classification and Criticality

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. Why a simple-looking request is not a simple request

"Prepare me for a meeting with EIB about this municipal infrastructure project" is one sentence. It
is also an IFI counterparty, a public-sector counterparty and regulated infrastructure: **three**
approved criticality triggers fire on a request the user thinks of as *booking a meeting*, and a
fourth consideration — that a commitment could arise in the room — raises the treatment further as
**conservative escalation** rather than as a trigger (§8, WC-2, WC-6). Neither the count nor the
band is affected by how plainly the sentence reads.

This document is how the planner notices.

## 2. Work requirement derivation

`WorkRequirementSet` is derived from the `WorkIntent` and the `ScopeResolution` together. Neither
alone is sufficient: the intent says what is being asked, the scope says what governs it.

| Requirement | Derived from |
|---|---|
| Deliverable class | `requested_outcome`, `primary_work_mode`, `secondary_work_modes` |
| Domain set | `entities`, subject matter, the scope's own domain |
| Act set | `act_direction`, `transmission_contemplated`, `commitment_possible` |
| Criticality band | §3 |
| Risk flags | §4 |
| Evidence needs | The claims the deliverable will have to support |
| Stop conditions | §6 |

## 3. Criticality

**Rule WC-1 — the approved policy is the policy.** Bands come from
`architecture/project-criticality-policy.md` and are not restated, reinterpreted or re-thresholded
here:

| Band | Approved condition |
|---|---|
| **Routine / Standard** | Typically below €10m and without material complexity triggers |
| **Enhanced Review Candidate** | Typically €10m–€50m, or smaller with meaningful complexity or external-decision exposure |
| **Enhanced Decision-Grade** | Automatically at €50m+; also below €50m where risk or complexity triggers justify it |
| **Major / Systemic** | Very large, strategic or systemically important; Enhanced mode plus workflow-specific specialist and review escalation |

**Rule WC-2 — criticality raises and never lowers.** The planner may move a band **up** on detected
triggers. It may never move one **down**: not on the user saying it is simple, not on a low
confidence score, not on the absence of a stated value, and not because a higher band would be slow.
An unresolved band is `CRITICALITY_UNRESOLVED` and blocks; it is not Routine by default.

**Rule WC-3 — monetary value is one trigger among many, and its absence proves nothing.** A request
with no stated value is not thereby Routine. Where value is unknown **and** a §4 trigger fires, the
band is at least Enhanced Decision-Grade.

## 4. Risk and high-stakes triggers

Each is an **observable feature** of the request, the referenced material or the resolved scope.
None is a judgement about the user.

| # | Trigger | Approved source |
|---:|---|---|
| T-1 | IFI / DFI or multi-lender financing | Criticality policy |
| T-2 | PPP, concession, project-finance or blended-finance structure | Criticality policy |
| T-3 | Public-sector, municipal or sovereign counterparty | Criticality policy |
| T-4 | Regulated infrastructure or licensed activity | Criticality policy |
| T-5 | Procurement, State Aid or public-funding exposure | Criticality policy |
| T-6 | Cross-border or multi-jurisdiction structure | Criticality policy |
| T-7 | Material ESG / E&S, land, resettlement, biodiversity or stakeholder risk | Criticality policy |
| T-8 | Novel technology or material technical uncertainty | Criticality policy |
| T-9 | Complex CAPEX / OPEX or long construction schedule | Criticality policy |
| T-10 | Guarantees, security package, covenants or offtake dependencies | Criticality policy |
| T-11 | External submission to lender, investor, regulator, granting authority or board | Criticality policy |
| T-12 | Integrity, sanctions, AML/KYC or political-exposure risk | Criticality policy |
| T-13 | Data, cybersecurity or safety criticality | Criticality policy |
| T-14 | Explicit human classification as decision-grade | Criticality policy |
| T-15 | A legal or contractual commitment is contemplated | Phase 7 commitment Rights |
| T-16 | External institutional communication under the entity's name | Phase 7 release Rights |

**Rule WC-4 — a trigger fires on evidence, not on vocabulary.** "EIB" in a request is evidence of
T-1. The word "risky" is not evidence of anything. Each fired trigger records the material that
fired it, so a reviewer can check it rather than trust it.

**Rule WC-5 — detection failure is not absence.** Where the planner cannot determine whether a
trigger applies and the answer would change the band, the outcome is `CRITICALITY_UNRESOLVED`, not
"no trigger". The dangerous case is the request that looks ordinary because nobody looked.

## 5. The conservative branch

**Rule WC-6 — `UNKNOWN` on a safety field routes conservatively.** Where `act_direction`,
`reversibility`, `commitment_possible` or `transmission_contemplated`
(`request-intent-model.md` RI-4) is `UNKNOWN`, the classifier plans as though the **consequential**
value held, and records that it did so:

| Field | `UNKNOWN` is planned as | Consequence |
|---|---|---|
| `act_direction` | `EXTERNAL` | A release gate is planned |
| `reversibility` | `IRREVERSIBLE` | Higher review rigor; no automatic execution |
| `commitment_possible` | `YES` | A commitment Right must be resolved |
| `transmission_contemplated` | `YES` | A transmission gate must be resolved |

**Rule WC-7 — planning conservatively is not asserting the conservative fact.** The plan records
`reversibility = UNKNOWN, planned as IRREVERSIBLE`. It does not record that the act **is**
irreversible. The distinction matters at review: a reviewer must be able to see that the system
did not know, rather than believe it established something.

**Rule WC-8 — the conservative branch may be narrowed only by clarification or evidence.** A later
confidence increase does not narrow it. A user saying "it's fine" does not narrow it unless the
statement resolves the field, in which case it is a stated value with the user as its source.

## 6. Stop conditions

Derived with the requirements, not bolted on afterwards. Each stage in the eventual plan carries
the conditions under which it must not proceed.

| Class | Example |
|---|---|
| Evidence | A required source is absent, unresolvable or stale for this use |
| Authority | A required Decision Right has no resolvable holder |
| Review | A required Review Profile is unavailable in this scope |
| Conflict | Two supplied conclusions contradict each other |
| Scope | Material would have to cross a boundary to proceed |
| Sensitivity | The audience is wider than the material's labels permit |

**Rule WC-9 — a stop condition is planned, not discovered.** The plan states what would stop each
stage before the run starts, so the Orchestrator's block is a foreseen state rather than a surprise.

## 7. What classification never does

**Rule WC-10 — it never downgrades an inherited requirement.** Criticality, sensitivity, residency,
materiality, review requirements and decision requirements arriving from approved architecture or
from resolved scope are floors. The classifier adds; it does not subtract.

**Rule WC-11 — it never classifies a person.** Triggers describe the work. No output of this stage
records a judgement about the user, the counterparty or anyone else.

**Rule WC-12 — it produces no governed record.** The `WorkRequirementSet` is `AI_SUGGESTION`. It
informs planning; it establishes nothing about the world.

## 8. Worked classification

"Prepare me for a meeting with EIB about this municipal infrastructure project."

| Element | Value |
|---|---|
| Deliverable class | Meeting preparation pack |
| Triggers fired | T-1 (EIB is an IFI), T-3 (municipal counterparty), T-4 (regulated infrastructure) |
| Triggers **not** fired | T-11. It is an *external submission*; a meeting is not one. Treating it as "submission-adjacent" would claim a trigger the approved policy does not give (WC-4) |
| Conservative escalation | `commitment_possible` `UNKNOWN` → `YES` (WC-6), and the band is raised under WC-2. Recorded as escalation, **not** as a fourth fired trigger (WC-7) |
| Value stated | None — and by WC-3 that does not make it Routine |
| Band | **Enhanced Decision-Grade**, on three fired triggers plus the conservative escalation, with no stated value |
| `act_direction` | `EXTERNAL` — the meeting is with an external institution |
| `commitment_possible` | `UNKNOWN` → planned as `YES` (WC-6): a meeting with a lender can produce a commitment |
| Stop conditions | Evidence: the project's financial and technical basis must resolve at a version; Authority: any commitment made in the meeting requires its own Right |

Three fired triggers and a conservative escalation on a request whose surface reading is "help
me get ready for a meeting". That gap —
between what the sentence looks like and what the work is — is what this stage exists to close.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no classifier, model, scoring
implementation, schema or storage, and binds no provider or runtime technology.
