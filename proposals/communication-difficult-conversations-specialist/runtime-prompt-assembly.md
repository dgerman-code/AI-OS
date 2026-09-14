# Runtime Prompt Assembly

Status: `PROPOSED`
Version: 0.1
Governance Owner: AI-OS architecture governance

> This document describes **how a prompt would be assembled** if and when the package is approved.
> It specifies no compiler, no template engine, no model and no runtime. It creates no permanent
> autonomous agent.

## 1. The rule this document exists to enforce

**Rule PA-1 — the registry is the source of truth; the prompt is a projection of it.** A runtime
prompt is **compiled** from approved registry objects at assembly time. A stored persona prompt is
prohibited as a source of truth: it drifts from the registry silently, and the drift is invisible
precisely because the prompt is what the model actually saw.

The source specification contains a full drafted system prompt. That text is a **worked example of
the projection**, not the object of record. Where it and the registry differ, the registry wins,
and the projection is regenerated.

## 2. Assembly order

Each layer may **narrow** what the layers above it permit. No layer may widen one.

| # | Layer | Source object | May it widen? |
|---:|---|---|---|
| 1 | Common role constraints | `standard.role.common_constraints@0.2` | — (the floor) |
| 2 | Role Card | `role.communication_difficult_conversations_specialist` | **No** |
| 3 | Methodology | `method.communication.calm_direct_control@0.1` | **No** |
| 4 | Skill pack | `pack.communication.difficult_conversations@0.1` | **No** |
| 5 | Workflow stage | the active stage of the active workflow candidate | **No** |
| 6 | Scope constraints | the run's scope binding, sensitivity, residency and disclosure labels | **No** |
| 7 | Adjacent specialist findings | conclusions supplied by owning Roles, at their versions | **No** |
| 8 | Task input | the assignment and the interaction record | **No** |
| 9 | Output contract | `conversation-diagnostics-contract.md` §3 or §4 | **No** |

**Rule PA-2 — narrowing only, checked at assembly.** An assembly in which any layer grants
something a higher layer denies is a **failed assembly**, not a permissive one. The failure is
reported; it does not fall back to the broader permission.

**Rule PA-3 — layer 7 is quoted, never paraphrased.** A supplied conclusion enters the prompt as
its own text, attributed and versioned. Summarising it into the prompt is how `role-card.md` RC-1
gets violated before the model has written a word.

## 3. What each layer contributes

| Layer | Contributes |
|---|---|
| 1 | Universal authority limits; the knowledge-state taxonomy; the handoff interface; the Review / Decision separation |
| 2 | The owns / does-not-own boundary; the professional conclusion and its limits; the authority limits 1–9; the evidence requirements; the escalation conditions |
| 3 | The optimisation order; the anti-goals; the fifteen principles; Calm Direct Mode parameters; the safety limits |
| 4 | The available technique vocabulary and the evidence discipline the pack imposes |
| 5 | The stage objective, entry and exit criteria, and the artifact the stage contributes to |
| 6 | What may be read, what may be quoted, to whom it may be addressed, and where it may be stored |
| 7 | The substantive conclusions the output may carry, verbatim and versioned |
| 8 | The record, the objective, the constraints, the stakes, the audience and the deadline |
| 9 | The exact output shape required of this stage |

## 4. Invariants every assembly must carry

These appear in every assembled prompt, at layer 2 or above, and no lower layer may remove them:

1. the role boundary — what is owned and what is not;
2. the prohibition on changing a supplied conclusion (RC-1);
3. the prohibition on transmitting, and the statement that completing a draft is not sending it;
4. the prohibition on psychological or clinical assessment, with the bounded label vocabulary
   offered in its place;
5. the prohibition on fabrication, with the placeholder convention;
6. the requirement to surface a position-changing fact before drafting (RC-3);
7. the requirement to evaluate non-response and delay;
8. the requirement to name the required reviews and the human gate, or the fail-closed block;
9. the prohibition on presenting a draft as ready to send where a review or gate is unsatisfied;
10. the identity prohibitions CP-1 and CP-2 — no impersonation, no endorsement, no celebrity name
    as identity.

**Rule PA-4 — an assembly missing any invariant is invalid.** It is not run with a warning.

## 5. No permanent agent

**Rule PA-5 — assembly is per-assignment and disposable.** A prompt is assembled for one run in one
scope for one stage, and it does not survive the run. There is no standing assistant, no persistent
persona, no long-lived session identity and no accumulating memory across assignments
(ROLE != AGENT INSTANCE).

**Rule PA-6 — no cross-scope carry.** Nothing from a previous assignment enters a new assembly
except through a governed handoff or scope transfer. Conversation material is frequently personal,
privileged or commercially restricted, and an assistant that "remembers the last dispute" is a
disclosure mechanism.

**Rule PA-7 — no self-modification.** The assembled prompt does not edit the registry objects it
was compiled from, and no output of a run changes a layer of the next assembly.

## 6. Model selection is elsewhere

**Rule PA-8 — assembly does not select a model.** The assembled prompt is an input to whatever
model execution the Router selects, under approved Phase 9 rules, after the Orchestrator creates a
routing request. Nothing in this document chooses, constrains or ranks a Model Profile, and the
`communication_conflict_score` must not appear in a routing request as a model constraint
(`trigger-routing-spec.md` TR-8).

**Rule PA-9 — model output is `AI_SUGGESTION`.** Whatever the assembled prompt produces enters the
knowledge model as an AI-generated artifact at `DRAFT`, and is not evidence because a model
produced it (`standard.role.common_constraints@0.2`, Universal Authority Limits).

## 7. Worked projection sketch

Illustrative only — the exact wording is generated from the registry, and this sketch is not the
object of record:

```
[L1] Universal authority limits, knowledge-state taxonomy, review/decision separation.
[L2] You are acting as the Difficult Conversations & Communication Strategy Specialist.
     You own: communication strategy, framing, tone, brevity, boundary formulation, triage,
     de-escalation, redirection, drafting, timing and channel, escalation and documentation
     recommendation.
     You do not own: legal, financial, compliance, technical or institutional conclusions;
     contractual interpretation; risk acceptance; publication or send authority;
     canonicalisation; psychological diagnosis.
     You never transmit. Completing a draft is not sending it.
     You never change a supplied conclusion. You may say that its expression creates risk.
     You never assess a person. You describe what an exchange is doing, from a closed label set.
     You never invent a fact. A required-but-absent fact becomes a named placeholder.
     You are not Jefferson Fisher, you are not endorsed by him, and you do not present as him.
[L3] Optimise in this order: clarity, self-control, brevity, boundary strength, respect,
     strategic outcome. Do not optimise for: emotional victory, argument, over-justification,
     defensive explanation, rebutting every accusation, forced persuasion, unnecessary escalation.
     Tone never overrides a material protection.
[L4] Available techniques: T-1 … T-24.
[L5] Current stage: S8 — generate response variants. Exit when the recommended response exists
     and carries no unsourced assertion.
[L6] Scope: <scope-path>. Sensitivity: <labels>. Disclosure basis: <basis>.
     Do not quote restricted material to a wider audience than its label permits.
[L7] Supplied conclusions, verbatim and versioned:
     - role.legal_regulatory_lead @ v3: "<exact text>"
[L8] Task, record, constraints, stakes, audience, deadline.
[L9] Produce the output shape of conversation-diagnostics-contract.md §3.
```

Note what the sketch does **not** contain: a persona, a biography, a voice description, a
personality, or any instruction to sound like anyone.

## 8. Assembly-time checks

Before a prompt is used, the assembly is checked:

| # | Check | On failure |
|---:|---|---|
| A1 | Every layer resolves to an approved object at a stated version | Fail the assembly |
| A2 | No layer widens a higher layer (PA-2) | Fail the assembly |
| A3 | All ten invariants of §4 are present | Fail the assembly |
| A4 | Layer 7 conclusions are verbatim and attributed (PA-3) | Fail the assembly |
| A5 | Layer 6 labels are present and the disclosure basis is resolved where required | Fail the assembly |
| A6 | The output contract of layer 9 matches the stage | Fail the assembly |
| A7 | No identity, persona or endorsement string is present (CP-1, CP-2) | Fail the assembly |

**Rule PA-10 — a failed assembly is a blocked run, not a degraded one.** There is no reduced prompt
that runs anyway.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no compiler, template engine,
orchestration, scheduling, agent execution, model routing, database schema, API, interface or
automation code, and binds no model, provider or runtime technology. The sketch in §7 is
illustrative text, not a stored artifact.
