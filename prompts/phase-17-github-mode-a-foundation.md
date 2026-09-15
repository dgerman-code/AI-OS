# Phase 17 — GitHub Mode A / Provider-Neutral AI Connection

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-17-github-mode-a`

## Purpose

Implement **Mode A** only:

`Human -> external AI -> GitHub AI-OS`

Any AI system that can read the repository should be able to discover and use AI-OS consistently without requiring provider-specific redesign.

This phase MUST remain provider-neutral. Do not implement Mode B (AI-OS calling model APIs), provider billing, API-key management, model orchestration, retries/fallbacks, runtime workers, queues, schedulers or deployment infrastructure.

## Governing constraints

Preserve all approved Phase 1-16 boundaries. In particular:

- GitHub is the canonical repository/control-plane source for Mode A.
- ROLE != MODEL.
- ROLE != AGENT INSTANCE.
- AI suggestion never becomes canonical automatically.
- Human authority remains explicit.
- No external AI may self-approve Roles, Skills, Workflows, Review Profiles, Decision Rights, canonical memory or governance records.
- A provider-specific instruction file may adapt syntax, but MUST NOT alter AI-OS semantics.
- A model/provider change MUST NOT change Role, Workflow, Decision Right, Skill approval, canonical evidence or governance meaning.
- Phase 16 limitations remain in force, including individually approved Skill eligibility.
- Do not create a PR.

## Required outcome

Create a minimal, durable, provider-neutral repository interface that lets an external AI answer four questions reliably:

1. **Where do I start?**
2. **What must I read before acting?**
3. **What am I allowed to do?**
4. **How must I return work/results?**

## Required artifacts

### 1. Root entrypoint

Create a root-level file named:

`AI_OS_ENTRYPOINT.md`

It should be short enough that any model can read it first. It must define:

- AI-OS purpose;
- Mode A meaning;
- canonical-source rule;
- mandatory discovery sequence;
- governance / authority boundary;
- task-start procedure;
- how to identify the relevant scope, Role, Workflow, Review Profile and Decision Right requirements;
- how to behave when evidence is missing or ambiguous;
- how to report source commit/ref;
- pointer to machine-readable manifest.

Do not duplicate the whole architecture in this file.

### 2. Machine-readable manifest

Create:

`ai-os.yaml`

The manifest should provide a stable machine-readable map of the repository. At minimum include:

- schema/version;
- mode: `A`;
- repository identity;
- entrypoint;
- governing principles location;
- registries and their locations;
- workflow registry location;
- Decision Rights location;
- review profiles location;
- model registry location (reference only; Mode A external AI is not selected by it);
- planning/orchestrator contracts;
- approval-record locations;
- canonical/memory governance references;
- required result envelope location;
- provider adapter/instruction locations;
- prohibited assumptions;
- human authority rule;
- change-control rule.

The manifest must reference existing sources rather than fabricate status.

### 3. Universal connection guide

Create:

`docs/HOW_TO_CONNECT_ANY_AI.md`

Explain in plain language how to connect an AI that can read GitHub.

Include:

- generic connection procedure;
- read-only mode;
- write-capable mode;
- minimum required repository permissions;
- branch/commit pinning;
- why a model should prefer exact commit SHA for governed work;
- what the AI may suggest vs what requires human approval;
- what happens if the AI cannot access a required file;
- how to avoid mixing provider-specific memory with canonical AI-OS state;
- a provider-neutral starter instruction the user can paste into any AI.

Do not claim capabilities that a provider may not support.

### 4. Standard result envelope

Create a machine-readable contract, for example:

`contracts/ai-result-envelope.schema.json`

It should define a provider-neutral response envelope for work returned by an external AI. Include fields such as:

- request/task identity;
- repository/ref/commit SHA used;
- scope;
- selected Role(s);
- Skill requirements, with approval/eligibility state distinguished from applicability;
- Workflow MATCH/COMPOSE reference as applicable;
- review requirements;
- Decision Right requirements;
- evidence/source references;
- assumptions;
- unresolved ambiguities;
- proposed changes;
- output artifacts;
- authority status;
- status/outcome.

The envelope must not allow an AI to claim governance approval merely because it completed work.

### 5. Provider instruction adapters

Create a small provider-adapter directory, e.g.:

`adapters/mode-a/`

At minimum provide:

- `generic.md`
- `openai-chatgpt.md`
- `anthropic-claude.md`
- `openai-codex.md`
- `google-gemini.md`

These are thin instruction adapters only. Each must:

- point first to `AI_OS_ENTRYPOINT.md` and `ai-os.yaml`;
- avoid copying governance logic;
- state that repository rules override adapter wording;
- explain how to use repository access for that provider only at a generic capability level;
- not claim a provider feature exists unless the adapter wording is conditional;
- not create provider-specific Role/Workflow/Decision semantics.

### 6. Discovery / conformance check

Create a lightweight validation script, e.g.:

`validation/phase_17_mode_a_validation.py`

It should fail closed if:

- root entrypoint missing;
- manifest missing or malformed;
- referenced critical registry paths do not exist;
- result-envelope schema invalid;
- adapters fail to point to the canonical entrypoint/manifest;
- an adapter introduces forbidden provider-specific governance language;
- manifest incorrectly implies Skills are approved merely because cards exist;
- Mode B/API orchestration semantics leak into Mode A.

Prefer static/repository checks. Do not introduce a runtime service.

### 7. Example session

Create:

`examples/mode-a-generic-session.md`

Show a simple example:

- user gives natural-language task;
- external AI reads entrypoint + manifest;
- identifies applicable scope/Role/Workflow path;
- reports any missing approval/evidence;
- returns a structured result envelope;
- does not exercise human authority.

Use one realistic AI-OS project example, but keep it generic and non-provider-specific.

## Acceptance criteria

Phase 17 Mode A foundation is acceptable only if:

- a new AI can discover the system from the repository root without prior hidden context;
- provider adapters remain thin and semantically equivalent;
- GitHub commit/ref used for work is explicitly reported;
- canonical-source and human-authority boundaries are explicit;
- carded Skills are not mistaken for individually approved Skills;
- provider memory/output cannot silently become canonical AI-OS state;
- no provider-specific governance is introduced;
- no Mode B implementation is introduced;
- validation passes;
- upstream approved artifacts remain unchanged.

## Required execution

Run at minimum:

```bash
python3 validation/phase_17_mode_a_validation.py
python3 validation/phase_17_mode_a_validation.py --json
git diff --check
```

Also manually test the discovery flow from repository root as if you were a new external AI with no hidden context.

## Required report

Return:

A. SUMMARY
B. EXACT STARTING HEAD
C. CHANGED FILES
D. ENTRYPOINT DESIGN
E. MANIFEST DESIGN
F. RESULT ENVELOPE
G. PROVIDER ADAPTERS
H. DISCOVERY TEST
I. VALIDATION RESULTS
J. CONTAINMENT
K. LIMITATIONS / DEFERRED MODE B ITEMS
L. IMPLEMENTATION SHA
M. VERDICT

If the Mode A foundation is coherent, provider-neutral, discoverable, fail-closed, validation passes and no upstream governed semantics are changed, end exactly:

`READY FOR INDEPENDENT PHASE 17 MODE A REVIEW`

## Commit / push

When complete:

- commit the implementation;
- push to `implementation/phase-17-github-mode-a`;
- do not create a PR;
- report exact commit SHA and confirm clean worktree.
