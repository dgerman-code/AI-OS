# Difficult Conversations & Communication Strategy Specialist — Governed Registry Package

Status: `PROPOSED`
Package Version: 0.1
Branch: `proposal/communication-difficult-conversations-specialist`
Architecture basis: approved AI-OS Phase 1–13 baseline
Governance Owner: AI-OS architecture governance

> **This package is a proposal.** Nothing in it is approved, canonical, or in force. It creates
> no Decision Right, satisfies no review, approves nothing, and authorises no external act. It
> modifies no approved Phase 1–13 artifact. It claims no Phase 14 approval and no production
> readiness.

## 1. What this package is

`proposals/communication-difficult-conversations-specialist-production-spec.md` is a production
specification written in product language. This package converts it into AI-OS registry objects
— a Role Card candidate, a methodology, a skill pack, six workflow candidates, two Review Profile
candidates, routing rules, contracts and an evaluation suite — **without** altering any approved
artifact and **without** inventing authority.

The conversion is not a formatting exercise. The source brief describes a celebrity-named
autonomous agent. AI-OS does not have that object. The corrections this package makes are set out
in §4.

## 2. Package map

| # | Artifact | What it fixes in place |
|---:|---|---|
| 1 | `README.md` | This document: package map, provenance, non-goals, governance boundary |
| 2 | `role-card.md` | The Role Card candidate, following the Role Card Standard and inheriting `standard.role.common_constraints@0.2` |
| 3 | `methodology-card.md` | `method.communication.calm_direct_control@0.1` — principles, optimisation order, anti-goals, safety limits |
| 4 | `skill-pack.md` | The skill pack candidate, mapped to **existing approved skill IDs** where they exist; only genuinely missing capabilities are marked as candidates |
| 5 | `workflow-difficult-interaction-response.md` | The primary workflow candidate |
| 6 | `workflow-meeting-preparation.md` | Meeting / call / negotiation preparation |
| 7 | `workflow-boundary-setting.md` | Boundary formulation |
| 8 | `workflow-refusal.md` | Refusal drafting |
| 9 | `workflow-formal-escalation.md` | Formal escalation |
| 10 | `workflow-thread-diagnostics.md` | Read-only diagnosis of an existing thread |
| 11 | `review-profile-communication-strategy.md` | `review.communication_strategy@0.1` |
| 12 | `review-profile-high-stakes-external-communication.md` | `review.high_stakes_external_communication@0.1` |
| 13 | `trigger-routing-spec.md` | The 0–100 Communication Conflict Score, bands, and co-activation rules |
| 14 | `communication-control-filter.md` | The ten-factor filter and its scoring semantics |
| 15 | `conversation-diagnostics-contract.md` | Structured diagnostic input / output contract |
| 16 | `runtime-prompt-assembly.md` | How an approved package would be compiled into a runtime prompt |
| 17 | `decision-right-gap-analysis.md` | What existing Rights cover, what they do not, and the one residual gap |
| 18 | `evaluation-spec.md` | Evaluation suite, adversarial cases, hard-fail conditions |
| 19 | `examples.md` | Representative original examples |
| 20 | `self-check.md` | Completeness, provenance, authority, routing, safety and scope-creep checks |
| 21 | `governance-decision-note.md` | The two items that require human governance authority — OG-1 and OG-2 — with options, consequences and a recommendation, and the record of the withdrawn candidate Decision Right |

Two executable assurance artifacts sit outside the package directory, under the repository's
`validation/` area, because they are tooling rather than specification:
`validation/communication_package_validation.py` and
`validation/communication_package_probes.py`. Neither modifies an approved validator and neither
reads a Phase 14 artifact.

## 3. Provenance and attribution

The methodology in this package is **original AI-OS work**, assembled from public, high-level
communication principles. It reproduces no book, paid course, transcript, proprietary framework
or protected phrasing.

Where attribution is displayed, the approved wording is:

> Communication methodology informed by publicly available principles associated with Jefferson
> Fisher's work on difficult conversations, boundaries, clarity, assertiveness, emotional
> self-control, and conversational leadership.

and it must be shown together with:

> Not affiliated with or endorsed by Jefferson Fisher.

**Rule CP-1 — no impersonation, no endorsement.** No artifact, prompt, UI string, mode name,
role name, metric or log in this package may present the system as Jefferson Fisher, imply his
endorsement, licensing, training, review or approval, or use his name as the canonical role or
product name. A generated output that does so is a hard fail of the evaluation suite
(`evaluation-spec.md` HF-3).

**Rule CP-2 — the alias is a migration aid, not an identity.** `jefferson-fisher-communication`
exists only as a compatibility / research alias for discovery and migration. It is never the
canonical Role ID, never a display name, and never appears in a governed record as the role's
identity. The same applies to **Fisher Mode**, whose canonical product-facing name is
**Calm Direct Mode**.

## 4. Architectural corrections carried from the source brief

| Source brief says | AI-OS position | Why |
|---|---|---|
| A celebrity-named autonomous agent | One proposed **Professional Delivery Role**, plus methodology, skills, workflows, reviews and routing rules | ROLE != AGENT INSTANCE. An agent instance is a runtime execution, not a governed capability |
| "Fisher Mode" as the product mode | **Calm Direct Mode**, alias retained only for compatibility | CP-1 and CP-2 |
| One large persona prompt as the source of truth | A prompt **compiled at runtime** from approved registry objects (`runtime-prompt-assembly.md`) | The registry is the source of truth; a stored persona prompt drifts from it silently |
| Trigger score activates the specialist | The score is **routing evidence**. It selects no model, grants no Right and approves nothing | ROUTER != ORCHESTRATOR; routing does not confer authority |
| "Human gate before send" | A named `decision.<id>`, or **fail-closed block** where none applies | Missing authority fails closed; an unnamed gate is not a gate |

## 5. Preserved invariants

This package is written against, and does not weaken, these approved separations:

| Invariant | Where this package holds it |
|---|---|
| ROLE != AGENT INSTANCE | `role-card.md`, `runtime-prompt-assembly.md` §5 — no permanent autonomous agent is created |
| MODEL != ROLE | `trigger-routing-spec.md` §6 — the conflict score never selects a Model Profile |
| ROUTER != ORCHESTRATOR | `trigger-routing-spec.md` §6 — routing evidence is produced for the Orchestrator; the Router selects eligible model execution only under Phase 9 rules |
| REVIEW PROFILE != REVIEW INSTANCE | The two Review Profile candidates define profiles; no instance is created or pre-satisfied |
| DECISION RIGHT != DECISION RECORD | `decision-right-gap-analysis.md` — a Right is referenced, never exercised; no Decision Record is written by this package |
| KNOWLEDGE != CANONICAL RECORD | `role-card.md` §Evidence — conversation text is `SOURCE`; pattern labels are `AI_SUGGESTION`; nothing is promoted |
| CREDENTIAL != HUMAN AUTHORITY | `role-card.md` §Role-Specific Authority Limits — access to a mailbox is not authority to send from it |
| External send authority is human-only where an applicable approved Right requires it | `decision-right-gap-analysis.md` §4, §6 |
| Missing authority fails closed | `decision-right-gap-analysis.md` §6 — resolve the applicable Right **first**, and only where that genuinely returns nothing: `AUTHORITY_ABSENT`, block, escalate (DG-5, DG-5a). Where no external act is contemplated at all, the status is `NOT_APPLICABLE` (DC-7) |
| No celebrity impersonation or endorsement claim | CP-1, CP-2, `evaluation-spec.md` HF-3 |

## 6. Non-goals

This package does **not**:

- create, widen, map or approve any Decision Right;
- modify the approved role universe, skill universe, workflow universe, review universe or
  Decision Right universe;
- register anything as `APPROVED` or `CANONICAL`;
- specify runtime code, a provider or model integration, a database schema, an API, a queue, a
  worker, a scheduler, a deployment or any infrastructure;
- create a permanent autonomous agent;
- diagnose mental state, personality or pathology;
- provide legal, financial, regulatory, compliance, tax, technical or clinical conclusions.

## 7. Identifier-shape divergence — an open governance item

The prompt fixes the canonical candidate IDs used throughout this package
(`method.communication.calm_direct_control@0.1`, `pack.communication.difficult_conversations@0.1`,
`workflow.communication.difficult_interaction_response@0.1`, …). These use a **dotted namespace
segment**, while the approved Phase 4 and Phase 5 templates use
`skill_pack.<stable_snake_case_name>` and `workflow.<stable_snake_case_name>`.

This package uses the IDs the prompt fixes, and records the divergence as **OG-1** in
`self-check.md` §6 rather than silently normalising either side. Normalisation is a registry
change-control decision, not a drafting decision. Each affected artifact states the normalised
alternative next to its primary ID so that either choice is mechanical later.

## 7a. What the independent review corrected

The review of baseline `81623de` returned `FAIL`. Five findings were specification errors and are
fixed in place; two are human governance choices and are recorded in `governance-decision-note.md`
rather than decided. The corrections are listed here because a package that quietly absorbed them
would be harder to audit than one that says what it got wrong.

| # | What the package asserted | What is true |
|---:|---|---|
| 1 | New contracts written in the deprecated `FACT` label, with a `SOURCE` → `FACT` transition | The approved epistemic type is `FACT_CLAIM`, a source is **cited, never promoted**, and a claim is a **new linked item** with its own `EVIDENCE` (RC-4, DC-4) |
| 2 | Two different review triggers — the Profile's and the Role Card's | One trigger, **RC-5**, with four conditions, owned by the Role Card and referenced everywhere. Low stakes no longer bypass a carried conclusion or a consequential boundary |
| 3 | A read-only diagnosis forced to report `AUTHORITY_ABSENT` | `NOT_APPLICABLE` with `NO_EXTERNAL_ACT_CONTEMPLATED`. Nothing to authorise and nobody to authorise it are opposite findings (DC-7) |
| 4 | A nine-field object mixing filter factors with risk measures, presented as the filter | Two namespaces: `communication_control_filter` with exactly the ten factors, and `diagnostic_risks` with its own (DC-11) |
| 5 | Private high-stakes correspondence is outside `decision.external_publication` because it is private, so a new Right is needed | **The approved subject contains no publicity element.** TA-7 is covered. The candidate Right is `WITHDRAWN_FROM_CURRENT_PACKAGE` (DG-3) |

## 8. Reading order

For a governance reviewer: `README.md` → `decision-right-gap-analysis.md` → `role-card.md` →
`trigger-routing-spec.md` → `self-check.md`.

For an implementation team: `role-card.md` → `methodology-card.md` → `skill-pack.md` → the six
workflows → `conversation-diagnostics-contract.md` → `communication-control-filter.md` →
`runtime-prompt-assembly.md` → `evaluation-spec.md`.

## 9. Non-Runtime Statement

This package is declarative architecture and proposal material. It specifies no orchestration,
scheduling, queueing, agent execution, model routing, database schema, API, interface or
automation code, and binds no model, provider or runtime technology.
