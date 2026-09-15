# How to Connect Any AI to AI-OS — Mode A

Mode A means: **you use an external AI, and that AI reads AI-OS from GitHub**.

The provider does not become the source of governance. GitHub remains the canonical source for AI-OS rules and approved records.

## Generic connection procedure

1. Give the AI access to repository `dgerman-code/AI-OS` using whatever repository-reading capability that provider supports.
2. Tell it to start with `AI_OS_ENTRYPOINT.md` and `ai-os.yaml`.
3. In an interactive chat, require it to follow `docs/CONVERSATIONAL_OPERATION_MODEL.md`.
4. For governed work, pin the task to a branch/ref and preferably an exact commit SHA.
5. Require it to resolve internally the relevant scope, Role(s), Workflow path, review requirements, Decision Right requirements, evidence dependencies and blockers before it acts.
6. Require governed result structure to remain compatible with `contracts/ai-result-envelope.schema.json`, but do not require raw JSON to be shown in normal conversation.

## Conversational behaviour

A connected AI should not repeat a full project bootstrap for every follow-up question.

Use FULL RESOLUTION for a new project, fresh baseline, material objective change, materially changed evidence set, stale/ambiguous working state or relevant governance change.

Use FAST TASK RESOLUTION for normal follow-up questions. Reuse the non-canonical working context, re-resolve the minimum sufficient Role set for the current task, answer directly and recommend one best next step.

If the conversation goes off-topic and later clearly returns to a known project, resume that project context. Ask a short clarification only when the referent is genuinely ambiguous.

Roles are reusable capability profiles. They are not permanent chat personas and do not remain active indefinitely. The AI should activate the minimum sufficient Role(s) for each substantive request.

The human may also explicitly request a Role, for example: `Use the Financial Modelling Specialist for this calculation.` This Direct Expert Mode remains subject to all normal Role, Skill, evidence, review and authority boundaries.

## Workflow matching safeguard

A semantically strong Workflow candidate is not automatically a MATCH.

Before reporting `MATCH`, the AI must apply the admissibility rules in `planning/workflow-matching-and-composition.md`. If a trigger, precondition, required Role, Review Profile, Decision Right, scope condition or other governing admissibility requirement fails, the AI must not report `MATCH + execution_eligible=false` as a substitute.

It may identify the Workflow as the best-fit candidate, but the governed outcome must remain non-MATCH until admissibility is satisfied.

A matched Workflow is used as written. If the user's objective expands and requires additional Roles/stages/reviews/gates, the AI must re-resolve the work rather than silently modifying the matched Workflow. Use another approved Workflow or the governed COMPOSE path where eligible.

## Default user-facing output

The normal user should receive the useful answer, not the internal governance trace.

Default NORMAL MODE should contain only:

- the direct answer;
- material recommendation/explanation;
- one best next step;
- at most one targeted clarification question when useful.

Do not normally display repository-reading narration, commit SHA/ref, internal Role IDs, Skill mechanics, Workflow diagnostics, Review/Decision Right mechanics or raw result-envelope JSON.

Use EXPLAIN MODE when the user asks why or which specialists/logic were used.

Use AUDIT MODE only when the user explicitly requests provenance, exact SHA/ref, technical governance diagnostics, validation evidence or the structured result envelope.

## Read-only mode

Use read-only repository access when the AI should research, interpret, plan, review, compare or draft without changing the repository. Read-only is the safest default.

Minimum permission: enough to read the required repository files and resolve the ref/commit being used.

## Write-capable mode

Use write access only when you explicitly want the AI to edit repository files. Grant the minimum write permission needed and use a dedicated working branch where practical.

Write permission does not grant governance authority. An AI may propose or commit a change only within the human-granted task boundary; it cannot self-approve that change, exercise a Decision Right, or silently promote a PROPOSED artifact to APPROVED/CANONICAL.

## Why pin a commit SHA

A branch can move while work is in progress. An exact commit SHA gives a reproducible statement of which rules, registries and approval records the AI actually used. For decision-grade or reviewed work, prefer a pinned SHA.

In NORMAL MODE the AI may keep that provenance internal unless the user asks for it or a provenance limitation materially changes the answer. In AUDIT MODE it should report it explicitly.

If the AI can resolve only a branch/ref and not an exact SHA, it must treat the governed work as unpinned rather than inventing one.

## Missing files or access

If a required file cannot be read, the AI should stop that governed inference, identify the inaccessible source when material, and avoid guessing approval, eligibility, authority or canonical state. It may still provide clearly labelled non-governed analysis when that does not depend on the missing source.

## Provider memory is not AI-OS memory

Provider conversation history, saved memory, project instructions, local caches and generated summaries may help the provider navigate a conversation, but they do not become canonical AI-OS state. Canonical knowledge/memory follows the repository governance referenced by `ai-os.yaml`.

## What an external AI may do

It may analyse, draft, propose, prepare work products, identify applicable Roles and Workflows, surface required reviews/Decision Rights, calculate, compare, recommend next actions, and create changes when write access and the human task explicitly allow it.

It may not infer approval from existence, applicability or successful completion. It may not self-register or self-approve Roles, Skills, Workflows, Review Profiles, Decision Rights, canonical memory/evidence or phase approvals.

It should not use authority language such as `I allow the project to proceed` unless a valid human authority record actually establishes that fact. Prefer `I recommend`, `the evidence supports`, `the next preparation step is`, or `a human authority could consider` as appropriate.

## Provider-neutral starter instruction

Paste this into any AI that can read the repository:

```text
Connect to repository dgerman-code/AI-OS.
Work in Mode A: you are an external AI reading AI-OS from GitHub.
Start with AI_OS_ENTRYPOINT.md and ai-os.yaml, and follow docs/CONVERSATIONAL_OPERATION_MODEL.md for interactive chat behaviour.
Treat the repository at the supplied ref/commit as the canonical AI-OS source; conversation history may be used only as non-canonical working context.

For a new project/fresh baseline/material objective or evidence change, perform FULL RESOLUTION. For ordinary follow-up questions, use FAST TASK RESOLUTION: resolve the request intent, relevant scope/context, minimum sufficient Role(s), Workflow/Work Plan need, material evidence/authority constraints, answer directly, and recommend one best next step.
Re-resolve Role activation for every substantive task; do not keep prior Roles permanently active. If I explicitly name an AI-OS Role, use it when applicable and eligible.

Do not label a Workflow MATCH merely because it is semantically close. Apply Workflow admissibility first. If an admissibility gate fails, keep it as a best-fit candidate if useful but use a governed non-MATCH outcome. Do not use MATCH + execution_eligible=false as a substitute for failed admissibility. Do not silently modify a matched Workflow; re-resolve or use governed COMPOSE when the objective expands.

Default to NORMAL MODE: give me only the useful answer, material recommendation, one best next step, and at most one targeted clarification question. Do not show repository-reading narration, SHA/ref, internal IDs, governance diagnostics or raw JSON unless I ask.
Use EXPLAIN MODE when I ask why/how/which specialists. Use AUDIT MODE when I explicitly ask for technical provenance, exact SHA/ref, validation/governance detail or the result envelope.

Do not infer approval from card existence, mention or applicability. Keep Skill applicability separate from individual approval/eligibility. Do not exercise human authority or make provider memory canonical.
If a required source is unavailable or ambiguous, fail closed on that governed inference and state the material limitation in plain language.
```

Provider-specific adapters under `adapters/mode-a/` add only thin operational hints. Repository governance always overrides adapter wording.
