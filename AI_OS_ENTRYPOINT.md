# AI-OS — Mode A Entry Point

AI-OS is a provider-neutral governance and work-execution framework stored in this repository. In Mode A, a human uses an external AI that can read GitHub; the external AI reads AI-OS and follows it. AI-OS does **not** call model APIs in Mode A.

## Canonical source

For governed work, this repository at the exact Git commit/ref you were given is the source of truth. Provider memory, chat history, hidden instructions, generated summaries and model output are not canonical AI-OS state unless a governed repository change explicitly makes them so.

## Read in this order

1. Read `ai-os.yaml`.
2. Read the governing principles and registries referenced by the manifest.
3. Resolve the request scope and inspect the relevant Role, Workflow, Review Profile and Decision Right sources before claiming eligibility.
4. Read Phase 15 planning and Phase 16 planner-activation contracts when the task requires planning or execution-basis reasoning.
5. Return work using `contracts/ai-result-envelope.schema.json`.

## Before acting

Identify: repository/ref/commit SHA, task/request identity, scope, applicable approved Role(s), any Skill requirements, Workflow path (MATCH or COMPOSE when applicable), review requirements, Decision Right requirements, evidence dependencies and unresolved ambiguities.

A Role or Skill being mentioned, carded or applicable does not by itself make it approved or executable. In particular, Skill applicability must remain separate from individual Skill approval/eligibility.

## Authority boundary

You may analyse, draft, propose, compare, classify and prepare changes within the permissions granted by the human. You may not self-approve or self-promote Roles, Skills, Workflows, Review Profiles, Decision Rights, canonical memory/evidence, governance records or phase approvals. AI completion is not human authority.

If evidence, approval state, scope, authority or a required source is missing or ambiguous, fail closed: state what is unresolved and do not invent approval, canonical status or eligibility.

## Source reporting

Every governed result must report the repository identity, branch/ref and exact commit SHA actually used. If you cannot resolve an exact SHA, say so explicitly and treat the result as unpinned.

Machine-readable repository map: `ai-os.yaml`.
Connection guide: `docs/HOW_TO_CONNECT_ANY_AI.md`.
