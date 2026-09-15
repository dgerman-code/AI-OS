# How to Connect Any AI to AI-OS — Mode A

Mode A means: **you use an external AI, and that AI reads AI-OS from GitHub**.

The provider does not become the source of governance. GitHub remains the canonical source for AI-OS rules and approved records.

## Generic connection procedure

1. Give the AI access to repository `dgerman-code/AI-OS` using whatever repository-reading capability that provider supports.
2. Tell it to start with `AI_OS_ENTRYPOINT.md` and `ai-os.yaml`.
3. For governed work, pin the task to a branch/ref and preferably an exact commit SHA.
4. Ask the AI to identify the relevant scope, Role(s), Workflow path, review requirements, Decision Right requirements, evidence dependencies and any blockers before it acts.
5. Require returned work to follow `contracts/ai-result-envelope.schema.json`.

## Read-only mode

Use read-only repository access when the AI should research, interpret, plan, review, compare or draft without changing the repository. Read-only is the safest default.

Minimum permission: enough to read the required repository files and resolve the ref/commit being used.

## Write-capable mode

Use write access only when you explicitly want the AI to edit repository files. Grant the minimum write permission needed and use a dedicated working branch where practical.

Write permission does not grant governance authority. An AI may propose or commit a change only within the human-granted task boundary; it cannot self-approve that change, exercise a Decision Right, or silently promote a PROPOSED artifact to APPROVED/CANONICAL.

## Why pin a commit SHA

A branch can move while work is in progress. An exact commit SHA gives a reproducible statement of which rules, registries and approval records the AI actually used. For decision-grade or reviewed work, prefer a pinned SHA and report it in the result.

If the AI can resolve only a branch/ref and not an exact SHA, it must say that the work is unpinned rather than inventing one.

## Missing files or access

If a required file cannot be read, the AI should stop that governed inference, identify the inaccessible source, and avoid guessing approval, eligibility, authority or canonical state. It may still provide clearly labelled non-governed analysis when that does not depend on the missing source.

## Provider memory is not AI-OS memory

Provider conversation history, saved memory, project instructions, local caches and generated summaries may help the provider work, but they do not become canonical AI-OS state. Canonical knowledge/memory follows the repository governance referenced by `ai-os.yaml`.

## What an external AI may do

It may analyse, draft, propose, prepare work products, identify applicable Roles and Workflows, surface required reviews/Decision Rights, and create changes when write access and the human task explicitly allow it.

It may not infer approval from existence, applicability or successful completion. It may not self-register or self-approve Roles, Skills, Workflows, Review Profiles, Decision Rights, canonical memory/evidence or phase approvals.

## Provider-neutral starter instruction

Paste this into any AI that can read the repository:

```text
Connect to repository dgerman-code/AI-OS.
Work in Mode A: you are an external AI reading AI-OS from GitHub.
Start by reading AI_OS_ENTRYPOINT.md and ai-os.yaml.
Treat the repository at the supplied ref/commit as the canonical AI-OS source.
Before acting, resolve the relevant scope, approved Role(s), Workflow path, review requirements, Decision Right requirements, evidence dependencies and unresolved ambiguities from repository sources.
Do not infer approval from card existence, mention or applicability. Do not exercise human authority or make provider memory canonical.
Report the exact repository ref and commit SHA actually used, and return governed results using contracts/ai-result-envelope.schema.json.
If a required source is unavailable or ambiguous, fail closed and state what is missing.
```

Provider-specific adapters under `adapters/mode-a/` add only thin operational hints. Repository governance always overrides adapter wording.
